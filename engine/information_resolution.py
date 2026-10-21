"""Read-only information handoffs. No gameplay, persistence or provider authority.

Owning systems supply accepted records and character access. Sources are provenance,
not credentials. These local records are neither entity nor Region Pack schemas.
All time values use one caller-supplied fictional integer timeline, [start, end).
"""
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations
from typing import Protocol


@dataclass(frozen=True)
class Source:
    ref: str
    owner: str
    basis: tuple[str, ...] = ()


@dataclass(frozen=True)
class Period:
    start: int = 0
    end: int | None = None

    def contains(self, at: int) -> bool:
        return self.start <= at and (self.end is None or at < self.end)

    def overlaps(self, other: "Period") -> bool:
        return ((self.end is None or other.start < self.end)
                and (other.end is None or self.start < other.end))


@dataclass(frozen=True)
class Identity:
    id: str
    kind: str = "subject"  # subject, definition, instance
    definition_id: str | None = None


@dataclass(frozen=True)
class Fact:
    id: str
    subject: str
    predicate: str
    value: str | None
    source: Source
    period: Period = Period()
    epistemic: str = "fact"  # fact, belief, claim, inference, uncertain
    holder: str | None = None
    availability: str = "available"  # available, established_unavailable


@dataclass(frozen=True)
class Relationship:
    id: str
    subject: str
    relation: str
    target: str
    source: Source
    period: Period = Period()


@dataclass(frozen=True)
class BindingTerms:
    effects: tuple[str, ...]
    prerequisites: tuple[str, ...] = ()
    triggers: tuple[str, ...] = ()
    exclusions: tuple[str, ...] = ()
    exceptions: tuple[str, ...] = ()
    termination: tuple[str, ...] = ()
    revocation: tuple[str, ...] = ()


@dataclass(frozen=True)
class Constraint:
    id: str
    subjects: tuple[str, ...]
    actions: tuple[str, ...]  # empty means all actions in this subject scope
    terms: BindingTerms | None
    source: Source
    period: Period = Period()
    availability: str = "available"


@dataclass(frozen=True)
class Foundation:
    id: str
    setting: str
    era: str
    identities: tuple[Identity, ...] = ()
    facts: tuple[Fact, ...] = ()
    relationships: tuple[Relationship, ...] = ()
    constraints: tuple[Constraint, ...] = ()


@dataclass(frozen=True)
class Query:
    subjects: tuple[str, ...]
    at: int
    predicates: tuple[str, ...] = ()
    relations: tuple[str, ...] = ()  # outgoing only; explicit names, no wildcard
    depth: int = 0
    include_history: bool = False


@dataclass(frozen=True)
class ConstraintQuery:
    subjects: tuple[str, ...]  # all material subjects, places and rule domains
    action: str
    at: int


@dataclass(frozen=True)
class AccessGrant:
    record_id: str
    character_id: str
    source: Source  # owning-system reference and legitimate basis for this access
    period: Period = Period()


@dataclass(frozen=True)
class Selection:
    record_id: str
    source: Source
    reason: str
    temporal: str
    via: tuple[str, ...] = ()
    access_source: Source | None = None


@dataclass(frozen=True)
class Availability:
    subject: str
    predicate: str
    classification: str
    record_ids: tuple[str, ...]


@dataclass(frozen=True)
class Result:
    request: Query | ConstraintQuery
    facts: tuple[Fact, ...] = ()
    relationships: tuple[Relationship, ...] = ()
    constraints: tuple[Constraint, ...] = ()
    selections: tuple[Selection, ...] = ()
    availability: tuple[Availability, ...] = ()

    def missing_expected(self, record_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Test expectation comparison, not automatic completeness certification."""
        selected = {s.record_id for s in self.selections}
        return tuple(sorted(set(record_ids) - selected))


class InformationAccess(Protocol):
    """Consumer contract: immutable values, deterministic order, no storage access.

    resolve/applicable_constraints are trusted internal operations. Only the result
    of for_character may cross a character/presentation boundary. Do not forward
    internal diagnostics. Suppliers remain responsible for authority/completeness.
    """
    def resolve(self, query: Query) -> Result: ...
    def identity(self, subject_id: str) -> Identity | None: ...
    def for_character(self, query: Query | ConstraintQuery, character_id: str,
                      grants: tuple[AccessGrant, ...]) -> Result: ...
    def applicable_constraints(self, query: ConstraintQuery) -> Result: ...


class RepresentationError(ValueError):
    pass


class CanonicalConflict(RepresentationError):
    def __init__(self, conflicts: tuple[tuple[str, str], ...]):
        self.conflicts = conflicts
        super().__init__(f"Conflicting canonical records (no precedence): {conflicts}")


def _text(value):
    if not isinstance(value, str) or not value.strip():
        raise RepresentationError("Expected non-empty text")


def _texts(values):
    if not isinstance(values, tuple):
        raise RepresentationError("Collections must be immutable tuples")
    for value in values:
        _text(value)


def _time(at):
    if type(at) is not int:
        raise RepresentationError("Fictional time must be an integer")


def _source(source):
    if not isinstance(source, Source):
        raise RepresentationError("Source required")
    _text(source.ref)
    if source.owner not in {"authored", "world_simulation", "character",
                            "actors", "resolution"}:
        raise RepresentationError("Unsupported owning-system source")
    _texts(source.basis)


def _period(period):
    if not isinstance(period, Period):
        raise RepresentationError("Period required")
    _time(period.start)
    if period.end is not None:
        _time(period.end)
        if period.end <= period.start:
            raise RepresentationError("Period must have positive duration")


def _tuple(values):
    if not isinstance(values, tuple):
        raise RepresentationError("Collections must be immutable tuples")


class InformationSnapshot:
    """One validated immutable handoff, backed by private rebuildable indexes.

    Current facts explicitly overlay authored slots, only for objective facts.
    Conflicting current suppliers fail closed. Claims never overlay objective truth.
    History is supplied separately and never silently becomes a current fallback.
    Conditions in binding terms are retained for the owning adjudicator to apply.
    """

    def __init__(self, foundations: tuple[Foundation, ...], *,
                 identities: tuple[Identity, ...] = (),
                 current: tuple[Fact, ...] = (), history: tuple[Fact, ...] = (),
                 relationships: tuple[Relationship, ...] = (),
                 constraints: tuple[Constraint, ...] = ()):
        for values in (foundations, identities, current, history, relationships, constraints):
            _tuple(values)
        if len({f.id for f in foundations}) != len(foundations):
            raise RepresentationError("Duplicate foundation identity")
        if len({(f.setting, f.era) for f in foundations}) > 1:
            raise RepresentationError("Foundations must share setting and era")
        authored = []
        all_identities = list(identities)
        all_relationships = list(relationships)
        all_constraints = list(constraints)
        for foundation in sorted(foundations, key=lambda f: f.id):
            for text in (foundation.id, foundation.setting, foundation.era):
                _text(text)
            for values in (foundation.identities, foundation.facts,
                           foundation.relationships, foundation.constraints):
                _tuple(values)
            records = foundation.facts + foundation.relationships + foundation.constraints
            if any(r.source.owner != "authored" for r in records):
                raise RepresentationError("Foundation records require authored sources")
            authored.extend(foundation.facts)
            all_identities.extend(foundation.identities)
            all_relationships.extend(foundation.relationships)
            all_constraints.extend(foundation.constraints)
        self._identities = self._unique(all_identities)
        for identity in self._identities.values():
            _text(identity.id)
            if identity.kind not in {"subject", "definition", "instance"}:
                raise RepresentationError("Unsupported identity kind")
            if identity.definition_id is not None:
                definition = self._identities.get(identity.definition_id)
                if (identity.kind != "instance" or definition is None
                        or definition.kind != "definition"):
                    raise RepresentationError("Instance requires a known definition")
        authored = tuple(self._unique(authored).values())
        self._current_ids = frozenset(f.id for f in current)
        self._history_ids = frozenset(f.id for f in history)
        if (self._current_ids & self._history_ids
                or {f.id for f in authored} & (self._current_ids | self._history_ids)):
            raise RepresentationError("Record identity cannot cross information layers")
        self._facts = self._unique(authored + current + history)
        self._relationships = self._unique(all_relationships)
        self._constraints = self._unique(all_constraints)
        record_ids = [*self._facts, *self._relationships, *self._constraints]
        if len(record_ids) != len(set(record_ids)):
            raise RepresentationError("Record IDs must be unique across record kinds")
        self._by_subject = defaultdict(list)
        self._edges = defaultdict(list)
        self._binding = defaultdict(list)
        for fact in self._facts.values():
            self._record(fact)
            self._subject(fact.subject)
            _text(fact.predicate)
            if fact.epistemic not in {"fact", "belief", "claim", "inference", "uncertain"}:
                raise RepresentationError("Unsupported epistemic status")
            if fact.holder is not None:
                self._subject(fact.holder)
            if fact.epistemic in {"belief", "claim", "inference"} and fact.holder is None:
                raise RepresentationError("Attributed information requires a holder")
            if fact.availability not in {"available", "established_unavailable"}:
                raise RepresentationError("Unsupported availability")
            if fact.availability == "available":
                _text(fact.value)
            elif fact.value is not None:
                raise RepresentationError("Unavailable information cannot supply a value")
            if fact.id in self._current_ids and fact.source.owner == "authored":
                raise RepresentationError("Current information requires an owning gameplay source")
            self._by_subject[fact.subject].append(fact)
        self._check_conflicts(authored, canonical=True)
        self._check_conflicts(current, canonical=False)
        for edge in self._relationships.values():
            self._record(edge)
            self._subject(edge.subject)
            self._subject(edge.target)
            _text(edge.relation)
            self._edges[edge.subject].append(edge)
        for constraint in self._constraints.values():
            self._record(constraint)
            _texts(constraint.subjects)
            _texts(constraint.actions)
            if not constraint.subjects:
                raise RepresentationError("Constraints require subject scope")
            if constraint.availability == "available":
                if not isinstance(constraint.terms, BindingTerms):
                    raise RepresentationError("Available constraints require binding terms")
                for values in vars(constraint.terms).values():
                    _texts(values)
                if not constraint.terms.effects:
                    raise RepresentationError("Constraints require meaningful effects")
            elif constraint.availability != "established_unavailable" or constraint.terms is not None:
                raise RepresentationError("Unavailable constraints must explicitly omit terms")
            for subject in constraint.subjects:
                self._subject(subject)
                self._binding[subject].append(constraint)

    @staticmethod
    def _unique(records):
        result = {}
        for record in records:
            if record.id in result and result[record.id] != record:
                raise RepresentationError(f"Inconsistent identity: {record.id}")
            result[record.id] = record
        return dict(sorted(result.items()))

    def _subject(self, subject):
        _text(subject)
        if subject not in self._identities:
            raise RepresentationError(f"Unknown subject: {subject}")

    @staticmethod
    def _record(record):
        _text(record.id)
        _source(record.source)
        _period(record.period)

    @staticmethod
    def _check_conflicts(facts, *, canonical):
        slots = defaultdict(list)
        for fact in facts:
            if fact.epistemic == "fact":
                slots[(fact.subject, fact.predicate)].append(fact)
        conflicts = []
        for records in slots.values():
            for a, b in combinations(sorted(records, key=lambda f: f.id), 2):
                # Missing content is not evidence of a conflicting value.
                if (a.value is not None and b.value is not None and a.value != b.value
                        and a.period.overlaps(b.period)):
                    conflicts.append((a.id, b.id))
        if conflicts:
            pairs = tuple(sorted(conflicts))
            if canonical:
                raise CanonicalConflict(pairs)
            raise RepresentationError(f"Conflicting current facts: {pairs}")

    @staticmethod
    def _query(query):
        _texts(query.subjects)
        _texts(query.predicates)
        _texts(query.relations)
        _time(query.at)
        if type(query.depth) is not int or query.depth < 0:
            raise RepresentationError("Traversal depth must be a nonnegative integer")
        if type(query.include_history) is not bool:
            raise RepresentationError("include_history must be boolean")

    def resolve(self, query: Query) -> Result:
        self._query(query)
        return self._resolve(query, None)

    def identity(self, subject_id: str) -> Identity | None:
        """Trusted identity lookup; definitions never establish instance existence."""
        _text(subject_id)
        return self._identities.get(subject_id)

    def for_character(self, query: Query | ConstraintQuery, character_id: str,
                      grants: tuple[AccessGrant, ...]) -> Result:
        if isinstance(query, Query):
            self._query(query)
        else:
            self._constraint_query(query)
        self._subject(character_id)
        _tuple(grants)
        access = {}
        known = self._facts.keys() | self._relationships.keys() | self._constraints.keys()
        for grant in sorted(grants, key=lambda g: (g.record_id, g.source.ref, g.source.basis)):
            _source(grant.source)
            _period(grant.period)
            self._subject(grant.character_id)
            if grant.source.owner != "character" or not grant.source.basis:
                raise RepresentationError("Access requires Character System source and basis")
            if grant.record_id not in known:
                raise RepresentationError("Access grant references an unknown record")
            if grant.character_id == character_id and grant.period.contains(query.at):
                access.setdefault(grant.record_id, grant.source)
        if isinstance(query, ConstraintQuery):
            internal = self.applicable_constraints(query)
            selected = tuple(c for c in internal.constraints if c.id in access)
            selections = tuple(Selection(c.id, c.source, "accessible binding scope", "current",
                                         access_source=access[c.id]) for c in selected)
            return Result(query, constraints=selected, selections=selections,
                          availability=self._constraint_availability(selected))
        return self._resolve(query, access)

    def _resolve(self, query, access):
        paths = {s: () for s in sorted(set(query.subjects))}
        queue = deque((s, 0) for s in paths)
        traversed = {}
        while queue:
            subject, depth = queue.popleft()
            if depth >= query.depth:
                continue
            for edge in self._edges.get(subject, ()):
                if (edge.relation not in query.relations or not edge.period.contains(query.at)
                        or (access is not None and edge.id not in access)):
                    continue
                traversed[edge.id] = edge
                if edge.target not in paths:
                    paths[edge.target] = paths[subject] + (edge.id,)
                    queue.append((edge.target, depth + 1))
        facts = []
        temporal = {}
        for subject in sorted(paths):
            candidates = self._by_subject.get(subject, ())
            # Internal reads use current truth. Character reads retain only supplied
            # accessible knowledge; hidden developments cannot erase that knowledge.
            overridden = {f.predicate for f in candidates
                          if f.id in self._current_ids and f.epistemic == "fact"
                          and f.period.contains(query.at)
                          and (access is None or f.id in access)}
            for fact in candidates:
                if query.predicates and fact.predicate not in query.predicates:
                    continue
                if access is not None and fact.id not in access:
                    continue
                historical = (fact.id in self._history_ids
                              or not fact.period.contains(query.at)
                              or (fact.id not in self._current_ids and fact.epistemic == "fact"
                                  and fact.predicate in overridden))
                if fact.period.start > query.at or (historical and not query.include_history):
                    continue
                facts.append(fact)
                temporal[fact.id] = ("historical" if historical else
                                     "current" if access is None else "retained")
        facts = tuple(sorted(facts, key=lambda f: f.id))
        edges = tuple(traversed[k] for k in sorted(traversed))
        selections = []
        for record in (*facts, *edges):
            via = paths[record.subject]
            selections.append(Selection(
                record.id, record.source, "relationship" if isinstance(record, Relationship)
                else ("related subject" if via else "direct subject"),
                temporal.get(record.id, "current"), via,
                None if access is None else access[record.id]))
        availability = []
        for subject in sorted(paths):
            predicates = query.predicates or tuple(sorted({f.predicate for f in facts
                                                          if f.subject == subject}))
            for predicate in sorted(set(predicates)):
                selected = [f for f in facts if f.subject == subject and f.predicate == predicate]
                if not selected:
                    # Character views do not disclose the existence of hidden records.
                    classification = "unspecified" if access is None else "not_accessible"
                    availability.append(Availability(subject, predicate, classification, ()))
                for fact in selected:
                    classification = ("established_unavailable"
                                      if fact.availability == "established_unavailable"
                                      else "uncertain" if fact.epistemic == "uncertain"
                                      else "available")
                    availability.append(Availability(subject, predicate, classification, (fact.id,)))
        return Result(query, facts, edges, selections=tuple(sorted(selections, key=lambda s: s.record_id)),
                      availability=tuple(availability))

    def applicable_constraints(self, query: ConstraintQuery) -> Result:
        """Return all binding candidates matching supplied subject/action/time scope.

        Hidden constraints are included. Prerequisites, exclusions and other terms
        are returned intact; deciding their outcome belongs to Action & Resolution.
        A query must supply relevant places/domains as well as the attempted target.
        """
        self._constraint_query(query)
        selected = {}
        for subject in query.subjects:
            for constraint in self._binding.get(subject, ()):
                if (constraint.period.contains(query.at)
                        and (not constraint.actions or query.action in constraint.actions)):
                    selected[constraint.id] = constraint
        constraints = tuple(selected[k] for k in sorted(selected))
        selections = tuple(Selection(c.id, c.source, "binding subject/action/time scope", "current")
                           for c in constraints)
        return Result(query, constraints=constraints, selections=selections,
                      availability=self._constraint_availability(constraints))

    @staticmethod
    def _constraint_availability(constraints):
        return tuple(Availability(subject, "binding_terms", c.availability, (c.id,))
                     for c in constraints for subject in sorted(set(c.subjects)))

    @staticmethod
    def _constraint_query(query):
        _texts(query.subjects)
        _text(query.action)
        _time(query.at)
