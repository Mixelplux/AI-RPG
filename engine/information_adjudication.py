"""Bounded owning-boundary adjudication over InformationAccess, offline only.

This disposable session is not a campaign/save API. Trusted suppliers establish
context, methods, capability, access and completeness. Proposal suppliers are
untrusted. See docs/information_grounded_adjudication_v1_handoff.md for the finite
term semantics and the distinction between rejection and fictional failure.
"""
from dataclasses import dataclass, replace
from typing import Callable

from engine.activity_control import (
    ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment,
    decide_activity_control,
)
from engine.character_competence import resolve as resolve_d6
from engine.information_resolution import (
    AccessGrant, ConstraintQuery, InformationAccess, Query,
)
from engine.narrative_realization import validate_context


@dataclass(frozen=True)
class Method:
    id: str
    action: str
    capability: str
    means: tuple[str, ...] = ()
    costs: tuple[tuple[str, int], ...] = ()
    requirements: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    mechanic: str = "routine"  # routine or existing d6
    specialist: str | None = None  # optional retrieved actor predicate
    duration: int = 1
    operation: str = "attempt"  # attempt or end_binding
    observations: tuple[tuple[str, str], ...] = (
        ("full", "You complete the attempt."),
        ("partial", "You make limited progress; the undertaking remains incomplete."),
        ("failure", "Your attempt makes no progress."),
        ("blocked", "You attempt the chosen method, but cannot complete it."),
    )


@dataclass(frozen=True)
class Attempt:
    id: str
    actor: str
    action: str
    method: str | None
    target: str
    location: str
    at: int
    authorization: ActivityAuthorization
    means: tuple[str, ...] = ()
    related: tuple[str, ...] = ()
    relations: tuple[str, ...] = ()
    binding: str | None = None
    developments: tuple[ActivityDevelopment, ...] = ()

    def identity(self):
        """Resume may change time/answered choices, never the accepted undertaking."""
        return (self.actor, self.action, self.method, self.target, self.location,
                self.means, self.related, self.relations, self.binding,
                self.authorization.purpose, self.authorization.method,
                self.authorization.constraints)


@dataclass(frozen=True)
class Assessment:
    attempt: Attempt
    revision: int
    premise_ids: tuple[str, ...]
    applied_bindings: tuple[str, ...]
    mechanical_result: str | None
    draw: int | None
    result: str
    obligations: tuple[tuple[str, str], ...]
    ended: tuple[str, ...]
    costs: tuple[tuple[str, int], ...]
    capability: str


@dataclass(frozen=True)
class Proposal:
    revision: int
    method: str
    means: tuple[str, ...]
    capability: str
    result: str
    costs: tuple[tuple[str, int], ...]
    obligations: tuple[tuple[str, str], ...]
    ended: tuple[str, ...]


def propose_assessed(assessment: Assessment) -> Proposal:
    """Predetermined offline stand-in, not an AI implementation or scenario table."""
    a = assessment
    return Proposal(a.revision, a.attempt.method, a.attempt.means, a.capability,
                    a.result, a.costs, a.obligations, a.ended)


@dataclass(frozen=True)
class Accepted:
    attempt: Attempt
    assessment: Assessment
    context: dict  # private; session.state returns defensive copies


@dataclass(frozen=True)
class SessionState:
    at: int = 0
    inventory: tuple[tuple[str, str, int], ...] = ()  # actor, resource, units
    ended: tuple[str, ...] = ()
    obligations: tuple[tuple[str, str, str], ...] = ()  # actor, binding, obligation
    history: tuple[Accepted, ...] = ()


class Unresolved(Exception):
    def __init__(self, stage, reason):
        self.stage, self.reason = stage, reason
        super().__init__(reason)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _tokens(values):
    return isinstance(values, tuple) and all(_text(v) for v in values)


def _condition(token):
    """Only equality against chosen context or an authoritative scalar fact."""
    if not _text(token) or "=" not in token:
        raise Unresolved("representation", "unsupported_condition")
    kind, value = token.split("=", 1)
    if kind in {"method", "action", "means", "capability"} and _text(value):
        return kind, (value,)
    parts = tuple(value.split("|"))
    if kind == "commitment" and len(parts) == 2 and all(_text(v) for v in parts):
        return kind, parts
    if kind == "fact" and len(parts) == 3 and all(_text(v) for v in parts):
        return kind, parts
    raise Unresolved("representation", "unsupported_condition")


def _effect(token):
    if token == "block":
        return "block", ""
    if _text(token) and token.startswith("obligation=") and _text(token[11:]):
        return "obligation", token[11:]
    raise Unresolved("representation", "unsupported_effect")


class AdjudicationSession:
    """Action/Resolution checks; session world consequences publish once.

    Information and method suppliers are trusted, storage-independent handoffs.
    A proposal callback receives immutable internal assessment, never mutable state
    or player presentation. No provider adapter is imported or invoked.
    """
    def __init__(self, information: InformationAccess, methods: tuple[Method, ...],
                 *, state=SessionState(), grants: tuple[AccessGrant, ...] = (),
                 draw: Callable[[], int] | None = None, time_unit=None):
        from copy import deepcopy
        if not isinstance(methods, tuple) or not methods or not all(isinstance(m, Method) for m in methods):
            raise ValueError("Explicit bounded methods required")
        if len({m.id for m in methods}) != len(methods):
            raise ValueError("Duplicate method")
        for m in methods:
            if not all(_text(v) for v in (m.id, m.action, m.capability)):
                raise ValueError("Method identity/action/capability required")
            if (m.mechanic not in {"routine", "d6"} or m.operation not in {"attempt", "end_binding"}
                    or type(m.duration) is not int or m.duration < 0
                    or m.specialist is not None and not _text(m.specialist)):
                raise ValueError("Unsupported method mechanics")
            if not all(_tokens(v) and len(v) == len(set(v)) for v in (m.means, m.requirements, m.conflicts)):
                raise ValueError("Invalid method collections")
            if (not isinstance(m.costs, tuple) or any(not isinstance(c, tuple) or len(c) != 2
                    or c[0] not in m.means or type(c[1]) is not int or c[1] <= 0 for c in m.costs)
                    or len({c[0] for c in m.costs}) != len(m.costs)):
                raise ValueError("Invalid explicit method costs")
            if (not isinstance(m.observations, tuple)
                    or any(not isinstance(o, tuple) or len(o) != 2 or not _text(o[1]) for o in m.observations)
                    or len(m.observations) != 4
                    or {o[0] for o in m.observations} != {"full", "partial", "failure", "blocked"}):
                raise ValueError("Safe observations required for every supported result")
        if (not isinstance(state, SessionState) or type(state.at) is not int or state.at < 0
                or state.history or state.ended or state.obligations
                or not isinstance(state.inventory, tuple)):
            raise ValueError("Only explicit initial session state; no restoration API")
        if (any(not isinstance(i, tuple) or len(i) != 3 or not _text(i[0]) or not _text(i[1])
                or type(i[2]) is not int or i[2] < 0 for i in state.inventory)
                or len({i[:2] for i in state.inventory}) != len(state.inventory)):
            raise ValueError("Invalid authoritative inventory")
        if not isinstance(grants, tuple) or not all(isinstance(g, AccessGrant) for g in grants):
            raise ValueError("Explicit character grants required")
        self._information, self._methods = information, {m.id: m for m in methods}
        self._state, self._grants, self._draw = deepcopy(state), grants, draw
        self._time_unit = time_unit
        self._running = False

    @property
    def state(self):
        from copy import deepcopy
        return deepcopy(self._state)

    def _fact(self, subject, predicate, at, premises):
        result = self._information.resolve(Query((subject,), at, (predicate,)))
        facts = result.facts
        premises.update(f.id for f in facts)
        # An unavailable objective slot must not fall back to an attributed claim.
        objective = tuple(f for f in facts if f.epistemic == "fact")
        if any(f.availability != "available" for f in objective):
            raise Unresolved("retrieval", "established_unavailable")
        if not objective:
            reason = "uncertain" if any(f.epistemic == "uncertain" for f in facts) else "unspecified"
            raise Unresolved("retrieval", reason)
        if len({f.value for f in objective}) != 1:
            raise Unresolved("retrieval", "conflicting_facts")
        return objective[0].value

    def _evaluate(self, token, attempt, premises):
        kind, values = _condition(token)
        value = values[0]
        if kind == "method":
            return attempt.method == value
        if kind == "action":
            return attempt.action == value
        if kind == "means":
            return value in attempt.means
        if kind == "capability":
            return self._fact(attempt.actor, "capability:" + value, attempt.at, premises) == "yes"
        if kind == "commitment":
            return (attempt.actor, *values) in self._state.obligations
        subject, predicate, expected = values
        return self._fact(subject, predicate, attempt.at, premises) == expected

    def _group(self, tokens, attempt, premises, *, any_match=False):
        # Order-independent three-valued equality: a decisive known operand can
        # make missing information immaterial. Otherwise preserve its diagnostic.
        values, missing = [], None
        for token in tokens:
            try:
                values.append(self._evaluate(token, attempt, premises))
            except Unresolved as exc:
                if exc.stage != "retrieval":
                    raise
                missing = missing or exc
        if any_match and any(values):
            return True
        if not any_match and False in values:
            return False
        if missing is not None:
            raise missing
        return any(values) if any_match else all(values)

    def _applies(self, terms, attempt, premises):
        missing, inactive = None, False
        for tokens, any_match, required in (
                (terms.prerequisites, False, True), (terms.triggers, False, True),
                (terms.exclusions, True, False), (terms.exceptions, True, False)):
            try:
                inactive |= self._group(tokens, attempt, premises, any_match=any_match) != required
            except Unresolved as exc:
                if exc.stage != "retrieval":
                    raise
                missing = missing or exc
        if inactive:
            return False
        if missing is not None:
            raise missing
        return True

    def _ending_allowed(self, terms, attempt, premises):
        missing = None
        for tokens in (terms.termination, terms.revocation):
            if not tokens:
                continue
            try:
                if self._group(tokens, attempt, premises):
                    return True
            except Unresolved as exc:
                if exc.stage != "retrieval":
                    raise
                missing = missing or exc
        if missing is not None:
            raise missing
        return False

    def _assess(self, attempt, method):
        scope = tuple(sorted(set((attempt.actor, attempt.target, attempt.location,
                                  *attempt.means, *attempt.related))))
        related = self._information.resolve(Query(scope, attempt.at, relations=attempt.relations,
                                                  depth=1 if attempt.relations else 0))
        scope = tuple(sorted(set(scope) | {r.target for r in related.relationships}))
        for subject in scope:
            if self._information.identity(subject) is None:
                raise Unresolved("retrieval", "unknown_subject")
        premises = {r.id for r in related.relationships}
        selected = self._information.applicable_constraints(ConstraintQuery(scope, attempt.action, attempt.at))
        bindings = tuple(c for c in selected.constraints if c.id not in self._state.ended)
        for c in bindings:
            premises.add(c.id)
            if c.availability != "available" or c.terms is None:
                raise Unresolved("retrieval", "established_unavailable")
            for group in (c.terms.prerequisites, c.terms.triggers, c.terms.exclusions,
                          c.terms.exceptions, c.terms.termination, c.terms.revocation):
                for token in group:
                    _condition(token)
            for token in c.terms.effects:
                _effect(token)
        capability = self._fact(attempt.actor, "capability:" + method.capability, attempt.at, premises)
        if capability != "yes":
            raise Unresolved("authorization", "unsupported_capability")
        eligible = self._group(method.requirements, attempt, premises)
        blocked, obligations, applied = not eligible, [], []
        ending = None
        if method.operation == "end_binding":
            ending = next((c for c in bindings if c.id == attempt.binding), None)
            if ending is None:
                raise Unresolved("adjudication", "no_applicable_binding")
            t = ending.terms
            # Each nonempty termination/revocation group is conjunctive. Either
            # complete group may authorize ending; ordinary attempts never end it.
            if not self._ending_allowed(t, attempt, premises):
                raise Unresolved("authorization", "ending_not_authorized")
        for c in bindings:
            if ending is not None and c.id == ending.id:
                continue  # the condition being legitimately removed cannot veto its own removal
            t = c.terms
            if self._applies(t, attempt, premises):
                applied.append(c.id)
                for token in t.effects:
                    effect, value = _effect(token)
                    if effect == "block":
                        blocked = True
                    else:
                        obligations.append((c.id, value))
        draw, mechanical = None, None
        if not blocked and method.mechanic == "d6":
            specialist = False
            if method.specialist is not None:
                specialist = self._fact(attempt.actor, method.specialist, attempt.at, premises) == "yes"
            if self._draw is None:
                raise Unresolved("adjudication", "missing_controlled_mechanics")
            # A sampled draw is provisional until the complete candidate publishes.
            # Rejection discards it; no pending roll or accepted result is stored.
            draw = self._draw()
            mechanical = resolve_d6(draw, specialist)
        result = "blocked" if blocked else mechanical or "full"
        # Effects of a triggered agreement attach to the attempt, including a
        # failed/blocked attempt; authors must express exclusions when appropriate.
        obligations = tuple(sorted(set(obligations)))
        ended = (ending.id,) if ending is not None and result == "full" else ()
        return Assessment(attempt, len(self._state.history), tuple(sorted(premises)),
                          tuple(applied), mechanical, draw, result, obligations, ended,
                          method.costs, method.capability)

    def _accessible_meanings(self, subjects, actor, at):
        """Character facts only; no internal constraints or retrieval diagnostics."""
        accessible = self._information.for_character(Query(subjects, at), actor, self._grants)
        meanings = []
        for fact in accessible.facts:
            if fact.availability != "available" or fact.value is None:
                continue
            status = "inferred" if fact.epistemic == "inference" else "reported" if fact.epistemic in {"claim", "belief", "uncertain"} else "established"
            label = "Retained inference" if status == "inferred" else "Retained unverified information" if status == "reported" else "Retained knowledge"
            meanings.append(dict(id=f"known-{fact.id}", meaning=f"{label}: {fact.value}",
                                 authority="Character System", status=status, source=fact.source.ref,
                                 time=f"Elapsed {at}", access="Explicit legitimate character grant"))
        return meanings

    def _inquiry(self, attempt, prior):
        """Explain only an already accepted observation within legitimate access.

        F05 has returned control for inquiry. This does not assess/execute an
        action, invoke a proposal, establish knowledge or publish any session state.
        """
        from copy import deepcopy
        subjects = tuple(sorted(set((attempt.actor, attempt.target, attempt.location, *attempt.related))))
        observation = deepcopy(prior.context["developments"][0])
        observation.update(id="inquiry-observation",
                           meaning="Earlier accepted observation: " + observation["meaning"])
        developments = [observation, *self._accessible_meanings(subjects, attempt.actor, self._state.at)]
        if len(developments) == 1:
            developments.append(dict(
                id="inquiry-limit", meaning="The observed effect alone does not establish its cause.",
                authority="Character System", status="established", source="Limits of the accepted observation",
                time=f"Elapsed {self._state.at}", access="No additional character information supplied"))
        retained = prior.context["continuity"] + prior.context["developments"][1:]
        continuity = [{**record, "id": f"inquiry-prior-{i}"} for i, record in enumerate(retained)]
        return validate_context(dict(
            moment="Inquiry about an accepted observable effect", focus=attempt.action,
            player_intent=dict(objective="Understand the earlier observed effect", method=attempt.method,
                               authorization="inquiry", constraints=list(attempt.authorization.constraints)),
            developments=developments, continuity=continuity,
            knowledge_limits=["An observation alone does not establish its cause; retained information and inferences do not verify current applicability."],
            unresolved=[], boundaries=["Read-only inquiry: no new action, cost, roll, accepted consequence or knowledge acquisition."]))

    def _presentation(self, attempt, method, assessment, candidate):
        """Safe deterministic F01 handoff. Never send internal assessment to F01."""
        observation = dict(method.observations)[assessment.result]
        observation += f" Elapsed effort: {method.duration}" + (" seconds." if self._time_unit == "seconds" else ".")
        if method.costs:
            observation += " Used: " + ", ".join(f"{count} {resource}" for resource, count in method.costs) + "."
        def meaning(identity, text, authority, status="resolved", source="Accepted session result", access="Directly observed result"):
            return dict(id=identity, meaning=text, authority=authority, status=status,
                        source=source, time=f"Elapsed {candidate.at}", access=access)
        developments = [meaning(f"result-{len(candidate.history)}", observation, "Action & Resolution / World Simulation")]
        subjects = tuple(sorted(set((attempt.actor, attempt.target, attempt.location, *attempt.related))))
        developments.extend(self._accessible_meanings(subjects, attempt.actor, candidate.at))
        known_bindings = self._information.for_character(
            ConstraintQuery(tuple(sorted(set((attempt.actor, attempt.target, attempt.location, *attempt.related)))),
                            attempt.action, attempt.at), attempt.actor, self._grants)
        known_ids = {c.id for c in known_bindings.constraints}
        for binding, obligation in assessment.obligations:
            if binding in known_ids:
                developments.append(meaning(f"commitment-{len(developments)}", "Your accepted obligation: " + obligation,
                                            "Action & Resolution / Actors & Social Dynamics"))
        continuity = []
        for accepted in candidate.history:
            # Preserve accessible commitments, inference and attribution as well
            # as the observed result. Prior prose never becomes current truth.
            for record in accepted.context["developments"]:
                continuity.append({**record, "id": f"prior-{len(continuity)}"})
        return validate_context(dict(
            moment=f"Authorized interaction {len(candidate.history) + 1}", focus=attempt.action,
            player_intent=dict(objective=attempt.action, method=attempt.method,
                               authorization=attempt.authorization.intent,
                               constraints=list(attempt.authorization.constraints)),
            developments=developments, continuity=continuity,
            knowledge_limits=["An observed result does not establish an unseen cause; retained knowledge is not verification of current applicability."],
            unresolved=[], boundaries=["Only accepted accessible meaning; narration cannot change results, means, costs or commitments."]))

    def step(self, attempt: Attempt, propose: Callable[[Assessment], Proposal] = propose_assessed):
        if self._running:
            return dict(status="rejected", stage="acceptance", reason="reentrant_attempt", context=None)
        self._running = True
        try:
            return self._step(attempt, propose)
        finally:
            self._running = False

    def _step(self, attempt, propose):
        from copy import deepcopy
        def stop(status, stage, reason):
            return dict(status=status, stage=stage, reason=reason, context=None)
        if (not isinstance(attempt, Attempt) or not all(_text(v) for v in
                (attempt.id, attempt.actor, attempt.action, attempt.target, attempt.location))
                or type(attempt.at) is not int or attempt.at != self._state.at
                or not isinstance(attempt.authorization, ActivityAuthorization)
                or not all(_tokens(v) and len(v) == len(set(v)) for v in (attempt.means, attempt.related, attempt.relations))
                or not isinstance(attempt.developments, tuple)
                or attempt.binding is not None and not _text(attempt.binding)):
            return stop("unresolved", "representation", "invalid_context")
        if attempt.method is None:
            return stop("control", "authorization", "choose_method")
        if not _text(attempt.method):
            return stop("unresolved", "representation", "invalid_method")
        method = self._methods.get(attempt.method)
        if method is None or method.action != attempt.action:
            return stop("control", "authorization", "unsupported_method")
        if (method.operation == "attempt" and attempt.binding is not None
                or method.operation == "end_binding" and attempt.binding is None):
            return stop("control", "authorization", "binding_scope")
        prior = next((a for a in self._state.history if a.attempt.id == attempt.id), None)
        if prior is not None and prior.attempt.identity() != attempt.identity():
            return stop("rejected", "acceptance", "attempt_identity_conflict")
        try:
            control = decide_activity_control(attempt.authorization, ActivityCheckpoint(
                attempt.action, method.id, conflicting_constraints=method.conflicts,
                developments=attempt.developments, resolution_ref=attempt.id if prior else None))
        except ValueError:
            return stop("unresolved", "representation", "invalid_authorization")
        if control.status != "continue":
            if control.reason == "inquiry" and prior is not None:
                try:
                    context = self._inquiry(attempt, prior)
                except Exception:
                    return stop("unresolved", "presentation", "safe_context_unavailable")
                return dict(status="inquired", stage="presentation", reason="accessible_information", context=context)
            return stop("control", "authorization", control.reason)
        if prior is not None:
            return dict(status="reused", stage="acceptance", reason="accepted_result", context=deepcopy(prior.context))
        if attempt.means != method.means:
            return stop("control", "authorization", "choose_means")
        inventory = {(actor, resource): count for actor, resource, count in self._state.inventory}
        costs = dict(method.costs)
        if any(inventory.get((attempt.actor, r), 0) < max(1, costs.get(r, 0)) for r in method.means):
            return stop("control", "authorization", "missing_means")
        try:
            assessment = self._assess(attempt, method)
        except Unresolved as exc:
            return stop("unresolved", exc.stage, exc.reason)
        except Exception:
            return stop("unresolved", "adjudication", "supplier_or_mechanics_failure")
        try:
            proposal = propose(assessment)
        except Exception:
            return stop("rejected", "proposal", "proposal_unavailable")
        # Full structural/type check before comparing consequential values (bool
        # must not masquerade as an integer revision or charge).
        if (type(proposal) is not Proposal or type(proposal.revision) is not int
                or not all(_text(v) for v in (proposal.method, proposal.capability, proposal.result))
                or not all(_tokens(v) for v in (proposal.means, proposal.ended))
                or not isinstance(proposal.obligations, tuple)
                or any(not _tokens(o) or len(o) != 2 for o in proposal.obligations)
                or not isinstance(proposal.costs, tuple)
                or any(not isinstance(c, tuple) or len(c) != 2 or not _text(c[0])
                       or type(c[1]) is not int for c in proposal.costs)
                or proposal != propose_assessed(assessment)):
            return stop("rejected", "acceptance", "proposal_contradicts_authority")
        candidate_inventory = tuple((actor, r, count - costs.get(r, 0) if actor == attempt.actor else count)
                                    for actor, r, count in self._state.inventory)
        obligations = set(self._state.obligations)
        for binding, value in assessment.obligations:
            obligations.add((attempt.actor, binding, value))
        candidate = replace(self._state, at=self._state.at + method.duration,
                            inventory=candidate_inventory,
                            ended=tuple(sorted(set(self._state.ended) | set(assessment.ended))),
                            obligations=tuple(sorted(obligations)))
        try:
            context = self._presentation(attempt, method, assessment, candidate)
        except Exception:
            return stop("unresolved", "presentation", "safe_context_unavailable")
        candidate = replace(candidate, history=(*candidate.history, Accepted(attempt, assessment, context)))
        self._state = candidate  # one publication, after all consequential and safe-context checks
        return dict(status="accepted", stage="acceptance", reason="validated", context=deepcopy(context))


def prepare_candidate(information, methods, state, attempt, *, grants=(), draw=None, time_unit=None,
                      propose=propose_assessed):
    """Pure owning-domain preparation over a trusted accepted state snapshot.

    The caller owns current-premise validation and publication. The disposable
    evaluator below never becomes the authoritative runtime or restoration API.
    Existing standalone session behavior is unchanged.
    """
    from copy import deepcopy
    evaluator = AdjudicationSession(information, methods,
        state=SessionState(at=state.at, inventory=state.inventory), grants=grants, draw=draw, time_unit=time_unit)
    evaluator._state = deepcopy(state)
    result = evaluator.step(attempt, propose)
    return result, evaluator.state
