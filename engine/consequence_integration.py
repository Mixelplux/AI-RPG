"""Opt-in I2 owning-domain integration; engine-lifetime truth, no disk durability.

Information suppliers and finite effect declarations are trusted domain inputs.
Proposals are untrusted. All mutable I2 consequences and receipts share one root.
Legacy world state is a read-only premise here, never a second cost/time owner.
"""
from copy import deepcopy
from dataclasses import dataclass, replace

from engine.activity_control import ActivityAuthorization, ActivityCheckpoint
from engine.gameplay_coordination import (
    AcceptedStep, DomainStep, Interpretation, SituatedContext, Target, validate_context,
)
from engine.information_adjudication import (
    Attempt, SessionState, Unresolved, prepare_candidate, propose_assessed,
)
from engine.information_resolution import (
    AccessGrant, Availability, ConstraintQuery, Fact, Identity, InformationSnapshot, Period,
    Query, Relationship, Result, Source,
)

CONTINUITY_LIMIT = ('I2 opt-in runtime has in-memory continuity only; save/load '
                    'and legacy commands are unavailable. Use process_consequence.')


@dataclass(frozen=True)
class Request:
    id: str
    actor: str
    action: str
    target: str
    method: str
    means: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    related: tuple[str, ...] = ()
    binding: str | None = None
    intent: str = 'commit'


@dataclass(frozen=True)
class FactEffect:
    """Supported domain consequence declaration, not a scenario answer.

    A successful supported method establishes this previously unspecified slot.
    Optional identity/relation and character access are explicit owner inputs.
    """
    method: str
    subject: str
    predicate: str
    value: str
    result: str = 'full'
    identity: Identity | None = None
    relation_from: str | None = None
    relation: str | None = None
    visible: bool = False


@dataclass(frozen=True)
class Config:
    information: object  # callable returning current InformationAccess
    methods: tuple
    actor: str
    targets: tuple  # (target identity, supported method identities)
    inventory: tuple = ()
    grants: tuple = ()
    effects: tuple[FactEffect, ...] = ()
    draw: object = None


@dataclass(frozen=True)
class Receipt:
    request: Request
    step: AcceptedStep


@dataclass(frozen=True)
class State:
    adjudication: SessionState
    identities: tuple = ()
    facts: tuple = ()
    relationships: tuple = ()
    grants: tuple = ()
    receipts: tuple[Receipt, ...] = ()


class InformationView:
    """Compose current owning-domain records, preserving selective access."""
    def __init__(self, base, state):
        self.base = base
        ids = {i.id: i for i in state.identities}
        for record in (*state.facts, *state.relationships):
            subjects = (record.subject, record.target) if isinstance(record, Relationship) else (record.subject,)
            for subject in subjects:
                if subject not in ids:
                    identity = base.identity(subject)
                    if identity is None:
                        raise ValueError('Unknown consequential subject')
                    ids[subject] = identity
        # Include referenced definition identities for newly owned instances.
        for identity in tuple(ids.values()):
            if identity.definition_id and identity.definition_id not in ids:
                ids[identity.definition_id] = base.identity(identity.definition_id)
        for grant in state.grants:
            ids.setdefault(grant.character_id, base.identity(grant.character_id))
        self.owned_record_ids = {r.id for r in (*state.facts, *state.relationships)}
        self.owned = InformationSnapshot((), identities=tuple(ids.values()),
            current=state.facts, relationships=state.relationships)

    def identity(self, subject):
        return self.owned.identity(subject) or self.base.identity(subject)

    @staticmethod
    def _merge(left, right):
        def merge(field):
            records = {}
            for value in (*getattr(left, field), *getattr(right, field)):
                key = value.record_id if field == 'selections' else value.id if field != 'availability' else (value.subject, value.predicate)
                if key in records and records[key] != value and field != 'availability':
                    raise ValueError('Conflicting authoritative records')
                if field == 'availability' and key in records:
                    prior = records[key]
                    kinds = {prior.classification, value.classification} - {'unspecified'}
                    classification = next((kind for kind in ('established_unavailable', 'uncertain', 'available')
                                           if kind in kinds), 'unspecified')
                    value = Availability(value.subject, value.predicate, classification,
                                         tuple(sorted(set(prior.record_ids + value.record_ids))))
                records[key] = value
            return tuple(records.values())
        return Result(left.request, **{f: merge(f) for f in
            ('facts', 'relationships', 'constraints', 'selections', 'availability')})

    def _resolve(self, query, character=None, grants=()):
        self.owned.resolve(query)  # Validate the original read-only query contract.
        def layer_reads(part):
            if character is None:
                return self.base.resolve(part), self.owned.resolve(part)
            own = tuple(g for g in grants if g.record_id in self.owned_record_ids)
            base = tuple(g for g in grants if g.record_id not in self.owned_record_ids)
            return (self.base.for_character(part, character, base),
                    self.owned.for_character(part, character, own) if own else Result(part))

        paths = {subject: () for subject in query.subjects}
        pending = list(query.subjects)
        result = Result(query)
        while pending:
            subject = pending.pop(0)
            path = paths[subject]
            part = replace(query, subjects=(subject,), relations=(), depth=0)
            for found in layer_reads(part):
                selections = tuple(replace(s, via=path,
                    reason='related subject' if path else s.reason) for s in found.selections)
                result = self._merge(result, replace(found, selections=selections))
            if len(path) >= query.depth:
                continue
            part = replace(query, subjects=(subject,), depth=1)
            for found in layer_reads(part):
                edges = found.relationships
                selections = tuple(replace(s, via=path) for s in found.selections
                                   if s.record_id in {e.id for e in edges})
                result = self._merge(result, Result(query, relationships=edges, selections=selections))
                for edge in edges:
                    if edge.target not in paths:
                        paths[edge.target] = (*path, edge.id)
                        pending.append(edge.target)
        return replace(result, request=query)

    def resolve(self, query):
        return self._resolve(query)

    def applicable_constraints(self, query):
        return self.base.applicable_constraints(query)

    def for_character(self, query, character, grants):
        if isinstance(query, ConstraintQuery):
            base_grants = tuple(g for g in grants if g.record_id not in self.owned_record_ids)
            return self.base.for_character(query, character, base_grants)
        return self._resolve(query, character, grants)


class Reads:
    """Record actual immutable reads; replay immediately before publication."""
    def __init__(self, information):
        self.information, self.values = information, []

    def _read(self, operation, *args):
        result = getattr(self.information, operation)(*args)
        self.values.append((operation, args, deepcopy(result)))
        return result

    def identity(self, subject):
        return self._read('identity', subject)

    def resolve(self, query):
        return self._read('resolve', query)

    def applicable_constraints(self, query):
        return self._read('applicable_constraints', query)

    def for_character(self, query, character, grants):
        return self._read('for_character', query, character, grants)

    def current(self, information):
        return all(getattr(information, op)(*args) == value for op, args, value in self.values)


class Runtime:
    """Engine-owned simulation aggregate; coordinators/domains hold no truth."""
    def __init__(self, config):
        if type(config) is not Config or not callable(config.information):
            raise ValueError('Explicit I2 configuration required')
        # Reuse finite method/inventory validation without executing an attempt.
        from engine.information_adjudication import AdjudicationSession
        AdjudicationSession(config.information(), config.methods,
            state=SessionState(inventory=config.inventory), grants=config.grants, draw=config.draw)
        if not isinstance(config.effects, tuple) or any(type(e) is not FactEffect for e in config.effects):
            raise ValueError('Finite domain effects required')
        for e in config.effects:
            if (not all(isinstance(v, str) and v.strip() for v in
                        (e.method, e.subject, e.predicate, e.value))
                    or e.method not in {m.id for m in config.methods}
                    or e.result not in {'full', 'partial'} or type(e.visible) is not bool
                    or bool(e.relation_from) != bool(e.relation)
                    or e.identity is not None and e.identity.id != e.subject):
                raise ValueError('Invalid supported fact effect')
        if (not isinstance(config.actor, str) or not config.actor.strip()
                or config.information().identity(config.actor) is None
                or not isinstance(config.targets, tuple) or not config.targets):
            raise ValueError('Explicit controlling actor and target scopes required')
        targets = dict(config.targets)
        if len(targets) != len(config.targets) or any(
                not isinstance(target, str) or not target.strip() or not isinstance(choices, tuple)
                or not choices or len(set(choices)) != len(choices)
                or not set(choices).issubset({m.id for m in config.methods})
                for target, choices in config.targets):
            raise ValueError('Invalid supported target methods')
        self.config = config
        self._state = State(SessionState(inventory=config.inventory))
        self.running = False
        self.diagnostic = None

    @property
    def state(self):
        return deepcopy(self._state)

    def information(self):
        return InformationView(self.config.information(), self._state)

    def prior(self, request):
        return next((r for r in self._state.receipts if r.request.id == request.id), None)

    def discover(self, information, request, location, at):
        # Action/Resolution's finite supported dependency semantics. Retrieval
        # supplies records, never applicability or outcomes. Relationships may
        # introduce effects, definitions, equipment or governing rule subjects.
        relations = ('active_effect', 'definition', 'governs', 'equipment')
        pending = [request.actor, request.target, location, *request.means, *request.related]
        seen = set()
        while pending:
            subject = pending.pop(0)
            if subject in seen:
                continue
            if len(seen) >= 64:
                raise Unresolved('retrieval', 'dependency_limit')
            seen.add(subject)
            identity = information.identity(subject)
            if identity is None:
                raise Unresolved('retrieval', 'unknown_subject')
            if identity.definition_id:
                pending.append(identity.definition_id)
            found = information.resolve(Query((subject,), at, relations=relations, depth=1))
            pending.extend(edge.target for edge in found.relationships)
            constraints = information.applicable_constraints(ConstraintQuery((subject,), request.action, at))
            for binding in constraints.constraints:
                if binding.id in self._state.adjudication.ended:
                    continue
                if binding.terms is None:
                    raise Unresolved('retrieval', 'established_unavailable')
                for group in (binding.terms.prerequisites, binding.terms.triggers,
                              binding.terms.exclusions, binding.terms.exceptions,
                              binding.terms.termination, binding.terms.revocation):
                    for token in group:
                        if token.startswith('fact='):
                            parts = token[5:].split('|')
                            if len(parts) == 3:
                                pending.append(parts[0])
        return tuple(sorted(seen - {request.actor, request.target, location, *request.means}))

    def _incorporate(self, candidate, information, request, result):
        for index, effect in enumerate(self.config.effects):
            if (effect.method, effect.result) != (request.method, result):
                continue
            # Only an actually unspecified slot may gain consequential specificity.
            existing = information.resolve(Query((effect.subject,), candidate.adjudication.at,
                                                  (effect.predicate,))) if information.identity(effect.subject) else None
            if existing and (existing.facts or existing.availability and any(
                    a.classification == 'established_unavailable' for a in existing.availability)):
                raise Unresolved('validation', 'established_slot')
            identities = candidate.identities
            if effect.identity is not None:
                prior = information.identity(effect.subject)
                if prior is not None and prior != effect.identity:
                    raise Unresolved('validation', 'identity_conflict')
                if prior is None:
                    identities += (effect.identity,)
            record_id = f'{request.id}:fact:{index}'
            source = Source(request.id, 'world_simulation', ('Accepted supported domain effect',))
            period = Period(candidate.adjudication.at)
            fact = Fact(record_id, effect.subject, effect.predicate, effect.value, source, period)
            relationships = candidate.relationships
            if effect.relation:
                relationships += (Relationship(f'{request.id}:relation:{index}', effect.relation_from,
                    effect.relation, effect.subject, source, period),)
            grants = candidate.grants
            if effect.visible:
                grants += (AccessGrant(record_id, request.actor,
                    Source(request.id, 'character', ('Legitimately observed accepted result',)), period),)
            candidate = replace(candidate, identities=identities, facts=(*candidate.facts, fact),
                                relationships=relationships, grants=grants)
            # Validate all owned representations before acceptance.
            InformationView(information, candidate)
        return candidate

    @staticmethod
    def _receipt(request, result, context):
        text = ' '.join(record['meaning'] for record in context['developments'])
        outcome = {'full': 'complete', 'partial': 'incomplete', 'failure': 'negative', 'blocked': 'negative'}[result]
        receipt = AcceptedStep(request.id, ('result',), outcome, (('result', text),))
        validate_context(SituatedContext('receipt', 'receipt', accessible=receipt.accessible))
        if not text or receipt.public_refs != ('result',):
            raise ValueError('Invalid safe receipt')
        return receipt

    def accept(self, request, step, engine, propose=propose_assessed):
        if self.running:
            raise Unresolved('acceptance', 'reentrant')
        self.running = True
        self.diagnostic = None
        stage = 'retrieval'
        try:
            prior = self.prior(request)
            if prior:
                if prior.request != request:
                    raise Unresolved('acceptance', 'identity_conflict')
                return prior.step
            if (request.actor != self.config.actor
                    or request.method not in dict(self.config.targets).get(request.target, ())):
                raise Unresolved('authorization', 'actor_or_target_scope')
            root, config = self._state, self.config
            legacy = engine.get_world_state()
            location = legacy['player']['current_location_id']
            reads = Reads(self.information())
            related = self.discover(reads, request, location, root.adjudication.at)
            attempt = Attempt(request.id, request.actor, request.action, request.method,
                request.target, location, root.adjudication.at,
                ActivityAuthorization(request.action, request.method, request.intent, request.constraints),
                request.means, related, binding=request.binding)
            stage = 'adjudication'
            result, state = prepare_candidate(reads, config.methods, root.adjudication, attempt,
                grants=(*config.grants, *root.grants), draw=config.draw, propose=propose)
            if result['status'] != 'accepted':
                raise Unresolved(result['stage'], result['reason'])
            stage = 'validation'
            candidate = self._incorporate(replace(root, adjudication=state), reads, request,
                                          state.history[-1].assessment.result)
            stage = 'receipt'
            receipt = self._receipt(request, state.history[-1].assessment.result, result['context'])
            if type(receipt) is not AcceptedStep or receipt.ref != request.id or receipt.outcome not in {
                    'complete', 'incomplete', 'negative', 'positive', 'unresolved'}:
                raise Unresolved('receipt', 'invalid_receipt')
            validate_context(SituatedContext('receipt', location, accessible=receipt.accessible))
            if (not isinstance(receipt.public_refs, tuple) or not receipt.public_refs
                    or not all(isinstance(v, str) and v.strip() for v in receipt.public_refs)
                    or len(set(receipt.public_refs)) != len(receipt.public_refs)
                    or not set(receipt.public_refs).issubset(dict(receipt.accessible))):
                raise Unresolved('receipt', 'invalid_access')
            candidate = replace(candidate, receipts=(*root.receipts, Receipt(request, receipt)))
            # All fallible construction/validation precedes final freshness check.
            stage = 'acceptance'
            current = self.information()
            if (self._state is not root or self.config != config or engine.get_world_state() != legacy
                    or not reads.current(current)):
                raise Unresolved('acceptance', 'stale_premises')
            self._state = candidate
            return receipt
        except Unresolved as exc:
            self.diagnostic = (exc.stage, exc.reason)
            raise
        except Exception:
            self.diagnostic = (stage, 'operation_unavailable')
            raise
        finally:
            self.running = False


class Domain:
    """I1 adapter. Requirements and acceptance remain with Action/owning runtime."""
    def __init__(self, engine, runtime):
        self.engine, self.runtime = engine, runtime
        self.request = None
        self.propose = propose_assessed

    def bind(self, request, propose):
        if (type(request) is not Request or not all(isinstance(v, str) and v.strip()
                for v in (request.id, request.actor, request.action, request.target, request.method))
                or request.intent not in {'commit', 'inquiry', 'prepare'}
                or any(not isinstance(values, tuple) or len(set(values)) != len(values)
                       or any(not isinstance(v, str) or not v.strip() for v in values)
                       for values in (request.means, request.constraints, request.related))):
            raise ValueError('Explicit bounded request required')
        if request.actor != self.runtime.config.actor:
            raise ValueError('Only the explicitly controlled actor may undertake activity')
        self.request, self.propose = request, propose

    def context(self):
        r = self.request
        if r is None:
            raise ValueError('No bound activity')
        location = self.engine.world_state['player']['current_location_id']
        root = self.runtime._state
        # Fresh actual dependency values are rechecked by the owner at acceptance.
        prior = self.runtime.prior(r)
        available = (r.method,) if prior else tuple(m.id for m in self.runtime.config.methods
            if m.action == r.action and m.id in dict(self.runtime.config.targets).get(r.target, ()))
        return SituatedContext(str(len(root.receipts)), location,
            targets=(Target(r.target, (r.target,), r.action, available),), means=r.means,
            accessible=(('limit', CONTINUITY_LIMIT),))

    def assess(self, undertaking, context):
        r = self.request
        prior = self.runtime.prior(r)
        method = next((m for m in self.runtime.config.methods if m.id == r.method), None)
        complete = r.id in undertaking.accepted_steps
        return DomainStep(r.id, ActivityCheckpoint(undertaking.ref, r.method, complete=complete,
            conflicting_constraints=method.conflicts if method and not prior else ()), ('world', 'character', 'action'),
            supported_constraints=())

    def execute(self, undertaking, step, context):
        r = self.request
        if (undertaking.activity, undertaking.target, undertaking.method, undertaking.constraints) != (
                r.action, r.target, r.method, r.constraints):
            raise Unresolved('authorization', 'request_mismatch')
        return self.runtime.accept(r, step, self.engine, self.propose)
