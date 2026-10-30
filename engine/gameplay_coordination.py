"""Bounded I1 coordination. No domain mechanics, provider or persistence authority.

Trusted suppliers own context, checkpoints, access and atomic domain execution.
Interpretations are untrusted. A decision is a single-use, context-bound permit;
only this coordinator's exact pending decision can execute. Public output is
assembled from accessible references, never internal reasons or raw exceptions.
"""
from dataclasses import dataclass, replace
import re

from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, decide_activity_control


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _refs(value):
    return isinstance(value, tuple) and all(_text(v) for v in value) and len(set(value)) == len(value)


@dataclass(frozen=True)
class Target:
    ref: str
    aliases: tuple[str, ...]
    activity: str
    methods: tuple[str, ...]
    routine_method: str | None = None


@dataclass(frozen=True)
class Interpretation:
    activity: str
    objective: str
    target: str | None
    method: str | None = None
    intent: str = "commit"
    constraints: tuple[str, ...] = ()
    independent: tuple[str, ...] = ()
    ambiguous: bool = False
    conditions: tuple[str, ...] = ()
    stop_at: tuple[str, ...] = ()


@dataclass(frozen=True)
class Undertaking:
    ref: str
    activity: str
    objective: str
    target: str
    method: str
    constraints: tuple[str, ...] = ()
    answered_choices: tuple[str, ...] = ()
    accepted_steps: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    stop_at: tuple[str, ...] = ()


@dataclass(frozen=True)
class SituatedContext:
    # Revision must cover every material domain premise, including hidden state.
    revision: str
    location: str
    targets: tuple[Target, ...] = ()
    means: tuple[str, ...] = ()
    routes: tuple[str, ...] = ()
    actors: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    unavailable: tuple[str, ...] = ()
    accessible: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class DomainStep:
    ref: str
    checkpoint: ActivityCheckpoint
    responsibilities: tuple[str, ...]
    required_means: tuple[str, ...] = ()
    public_refs: tuple[str, ...] = ()
    # A key identifies this exact choice/circumstance, never a blanket risk waiver.
    choices: tuple[tuple[str, str], ...] = ()  # (choice key, accessible text ref)
    supported_constraints: tuple[str, ...] = ()
    boundary: str = "clarification"  # clarification of instruction, or natural decision point
    response_phrases: tuple[tuple[str, str], ...] = ()  # supported phrase -> choice key
    # Owners establish these predicates and implement these stopping boundaries;
    # the Coordinator never evaluates natural-language conditions itself.
    satisfied_conditions: tuple[str, ...] = ()
    supported_stops: tuple[str, ...] = ()


@dataclass(frozen=True)
class AcceptedStep:
    ref: str
    public_refs: tuple[str, ...] = ()
    outcome: str = "complete"  # domain meaning, never inferred from missing findings
    accessible: tuple[tuple[str, str], ...] = ()  # accepted Character-safe result snapshot


@dataclass(frozen=True)
class CoordinationDecision:
    status: str
    message: str
    failure: str | None = None
    responsibilities: tuple[str, ...] = ()
    choices: tuple[str, ...] = ()
    undertaking: Undertaking | None = None
    context: SituatedContext | None = None
    step: DomainStep | None = None
    results: tuple[AcceptedStep, ...] = ()

    def player_result(self):
        # No asdict(): undertaking, hidden context, domain keys and diagnostics stay internal.
        return {"success": self.failure is None, "intent": "coordination",
                "message": self.message,
                "action": {"type": "coordination", "target": None, "parameters": {}, "confidence": 1.0},
                "coordination": {"status": self.status, "failure": self.failure,
                                 "results": [{"outcome": result.outcome,
                                              "text": " ".join(dict(result.accessible)[r] for r in result.public_refs)}
                                             for result in self.results],
                                 "choices": [{"id": str(i + 1), "text": text}
                                             for i, text in enumerate(self.choices)]}}


def validate_context(context):
    if not isinstance(context, SituatedContext) or not all(_text(v) for v in (context.revision, context.location)):
        raise ValueError("context")
    if not all(_refs(v) for v in (context.means, context.routes, context.actors, context.conditions, context.unavailable)):
        raise ValueError("context references")
    if (not isinstance(context.accessible, tuple)
            or any(not isinstance(p, tuple) or len(p) != 2 or not all(_text(v) for v in p) for p in context.accessible)
            or len(dict(context.accessible)) != len(context.accessible)):
        raise ValueError("accessible projection")
    if not isinstance(context.targets, tuple):
        raise ValueError("targets")
    identities = []
    for target in context.targets:
        if (not isinstance(target, Target) or not _text(target.ref) or not _text(target.activity)
                or not _refs(target.aliases) or not target.aliases or not _refs(target.methods)
                or target.routine_method is not None and target.routine_method not in target.methods):
            raise ValueError("target")
        identities.append((target.activity, target.ref))
    if len(set(identities)) != len(identities):
        raise ValueError("duplicate target")


def interpret(text, context):
    """Small explicit grammar: open/search/observe TARGET [using METHOD], modifiers.

    can/could I, how can I => inquiry; prepare to => preparation. Ambiguous,
    compound and out-of-grammar claimed forms are contained, never guessed.
    No synonym engine, inferred tools, model call or scenario-name matching.
    """
    if not isinstance(text, str):
        raise ValueError("input")
    raw = text.strip().casefold().rstrip(".?")
    # Existing bounded investigation owns this distinct phrase family.
    if raw.startswith("search for "):
        return None
    intent = "commit"
    for prefix, mode in (("can i ", "inquiry"), ("could i ", "inquiry"),
                         ("how can i ", "inquiry"), ("prepare to ", "prepare")):
        if raw.startswith(prefix):
            raw, intent = raw[len(prefix):], mode
            break
    match = re.match(r"^(open|search|observe)\b\s*(.*)$", raw)
    if not match:
        return None
    activity, body = match.groups()
    constraints = []
    for word in ("quietly", "carefully"):
        if re.search(r"\b" + word + r"\b", body):
            constraints.append(word)
            body = re.sub(r"\b" + word + r"\b", "", body).strip()
    compound = re.search(r"\b(?:and|then)\b|;", body)
    alternatives = bool(re.search(r"\b(?:or|maybe|perhaps|if|not|without)\b", body))
    method = None
    if " using " in body:
        body, method = body.split(" using ", 1)
        method = method.strip()
    body = re.sub(r"\s+", " ", body).strip()
    names = {body, re.sub(r"^the ", "", body)}
    candidates = [t.ref for t in context.targets if t.activity == activity
                  and names.intersection(a.casefold() for a in t.aliases)]
    return Interpretation(activity, text.strip(), candidates[0] if len(candidates) == 1 else None,
                          method, intent, tuple(constraints),
                          ("additional intention",) if compound else (),
                          alternatives or len(candidates) != 1
                          or text.strip().endswith("?") and intent == "commit")


class Coordinator:
    """One session-local undertaking. Context and domain suppliers are trusted owners.

    domain.assess(undertaking, context) is read-only and returns DomainStep or None.
    domain.execute(undertaking, step, context) owns atomic execution and returns
    AcceptedStep. A supplier must not publish on exception/rejection. I1 does not
    implement I2 acceptance or recovery for a nonconforming gameplay authority.
    """
    def __init__(self, context_supplier, domain):
        self.context_supplier = context_supplier
        self.domain = domain
        self.undertaking = None
        self._pending = None
        self._offered = ()
        self._choice_context = None
        self._answered_context = None
        self._responses = ()
        self._serial = 0

    def clear(self):
        self.undertaking = self._pending = self._choice_context = None
        self._answered_context = None
        self._offered = ()
        self._responses = ()

    def _context(self):
        context = self.context_supplier()
        validate_context(context)
        return context

    @staticmethod
    def _result(status, message, failure=None, **fields):
        return CoordinationDecision(status, message, failure, **fields)

    def decide_intent(self, player_input, *, provider):
        """V1 input through one replaceable provider and a trusted owner binder.

        provider(request) returns untrusted JSON text. domain.bind_intent(handoff)
        is a read-only capability binding, returning existing Interpretation IDs;
        it receives the full validated meaning, original input and trusted context.
        It is not a second general-purpose language interpreter. The owner must
        reject unsupported meaning/methods; no verb or candidate-domain dispatch
        is inferred here. Existing callers can continue using decide/process.
        """
        from engine.player_intent import IntentHandoff, InvalidInterpretation, normalize, request_for
        self._pending = None
        try:
            context = self._context()
        except Exception:
            return self._result("unresolved", "The current situation is unavailable. No activity was executed.", "context")
        try:
            request = request_for(player_input, context)
        except (ValueError, TypeError):
            return self._result("unresolved", "That input could not be interpreted. No activity was executed.", "interpretation")
        try:
            raw = provider(request)
        except Exception:
            return self._result("unresolved", "Interpretation is unavailable. No activity was executed.", "technical")
        try:
            validated = normalize(raw, context_ids=tuple(ref for ref, _ in request.context),
                                   player_input=player_input)
        except InvalidInterpretation:
            return self._result("unresolved", "That interpretation is invalid. No activity was executed.", "interpretation")
        value = validated.to_dict()
        if value["ambiguities"]:
            return self._result("clarification", "Clarify the intended activity, target or method. No activity was executed.")
        if len(value["intentions"]) != 1:
            return self._result("clarification", "Choose one immediate undertaking. No activities have been executed or queued.")
        intention = value["intentions"][0]
        if intention["mode"] == "statement":
            return self._result("statement", "No activity was executed.")
        handoff = IntentHandoff(validated, player_input, context)
        try:
            if self._context() != context:
                return self._result("unresolved", "Circumstances changed. Reassess before continuing.", "context")
            binder = getattr(self.domain, "bind_intent", None)
            if binder is None:
                return self._result("unresolved", "No gameplay capability can bind this meaning here.", "routing")
            proposal = binder(handoff)
            if proposal is None:
                return self._result("unresolved", "That meaning is not supported by the current gameplay capability.", "routing")
            if not isinstance(proposal, Interpretation):
                raise ValueError("binding")
            # Executable commitment is still subject to current F05/domain checks.
            # No binder may promote an inquiry or read-only preparation to commit,
            # discard stated boundaries, or add restrictions from mere omissions.
            intent = ("inquiry" if intention["mode"] == "inquiry" else
                      "prepare" if intention["commitment"] == "none" else "commit")
            proposal = replace(proposal, objective=intention.get("goal", intention["activity"]),
                               intent=intent, constraints=tuple(intention.get("constraints", ())),
                               conditions=tuple(intention.get("conditions", ())),
                               stop_at=tuple(intention.get("stop_at", ())))
        except Exception:
            return self._result("unresolved", "The gameplay binding is unavailable. No activity was executed.", "technical")
        return self.decide(interpretation=proposal, expected_context=context)

    def decide(self, *, text=None, interpretation=None, resume=False, answers=(), expected_context=None):
        self._pending = None
        if (type(resume) is not bool or not _refs(answers) or len(answers) > 1
                or answers and not resume or resume and (text is not None or interpretation is not None)):
            return self._result("unresolved", "Supply one instruction or one continuation choice.", "interpretation")
        try:
            context = self._context()
        except Exception:
            return self._result("unresolved", "The current situation is unavailable. No activity was executed.", "context")
        if expected_context is not None and context != expected_context:
            return self._result("unresolved", "Circumstances changed. Reassess before continuing.", "context")
        if text is not None and interpretation is None and not resume and isinstance(text, str):
            phrase = text.strip().casefold().rstrip(".")
            responses = dict(self._responses)
            if (phrase in responses and self.undertaking is not None
                    and phrase.startswith(self.undertaking.activity + " ")
                    and not phrase.endswith("?")):
                if context != self._choice_context:
                    return self._result("unresolved", "Circumstances changed. Reassess before continuing.", "authorization")
                answers = (str(self._offered.index(responses[phrase]) + 1),)
                resume, text = True, None
        if resume:
            if self.undertaking is None or not _refs(answers):
                return self._result("unresolved", "There is no valid undertaking to continue.", "authorization")
            offered = {str(i + 1): key for i, key in enumerate(self._offered)}
            if answers and (context != self._choice_context or not set(answers).issubset(offered)):
                return self._result("clarification", "Those choices need a fresh assessment.", "authorization")
            answers = tuple(offered[answer] for answer in answers)
            self._offered = ()
            self._responses = ()
            prior_answers = self.undertaking.answered_choices if context == self._answered_context else ()
            undertaking = replace(self.undertaking, answered_choices=tuple(dict.fromkeys(prior_answers + answers)))
            if answers:
                self._answered_context = context
            intent = "commit"
        else:
            self._offered = ()
            self._responses = ()
            self._choice_context = None
            try:
                if (text is None) == (interpretation is None):
                    raise ValueError("exactly one input")
                proposal = interpret(text, context) if text is not None else interpretation
                if proposal is None:
                    return None  # Only an unclaimed raw command may leave this runtime.
                if (not isinstance(proposal, Interpretation) or not _text(proposal.activity)
                        or not _text(proposal.objective) or proposal.intent not in {"inquiry", "prepare", "commit"}
                        or type(proposal.ambiguous) is not bool or not _refs(proposal.constraints)
                        or not _refs(proposal.independent) or proposal.target is not None and not _text(proposal.target)
                        or not _refs(proposal.conditions) or not _refs(proposal.stop_at)
                        or proposal.method is not None and not _text(proposal.method)):
                    raise ValueError("interpretation")
            except Exception:
                return self._result("unresolved", "That interpretation is invalid. No activity was executed.", "interpretation")
            if proposal.independent:
                return self._result("clarification", "Choose one undertaking to begin; the independent activities have not been executed.")
            if proposal.ambiguous or proposal.target is None:
                return self._result("clarification", "Specify one target and intended approach. No activity was executed.")
            matches = [t for t in context.targets if (t.activity, t.ref) == (proposal.activity, proposal.target)]
            if len(matches) != 1:
                return self._result("unresolved", "That activity is not supported in the current situation.", "routing")
            target = matches[0]
            method = proposal.method or target.routine_method
            if method is None:
                return self._result("clarification", "Which method do you want to use? No activity was executed.")
            if method not in target.methods:
                return self._result("unresolved", "That method is not available for this activity.", "authorization")
            self._serial += 1
            undertaking = Undertaking(str(self._serial), proposal.activity, proposal.objective,
                                      proposal.target, method, proposal.constraints,
                                      conditions=proposal.conditions, stop_at=proposal.stop_at)
            previous = self.undertaking
            if previous and (previous.activity, previous.target) == (undertaking.activity, undertaking.target):
                undertaking = replace(undertaking, ref=previous.ref,
                                      constraints=tuple(dict.fromkeys(previous.constraints + undertaking.constraints)),
                                      answered_choices=previous.answered_choices if previous.method == undertaking.method
                                      and context == self._answered_context else (),
                                      accepted_steps=previous.accepted_steps,
                                      conditions=tuple(dict.fromkeys(previous.conditions + undertaking.conditions)),
                                      stop_at=tuple(dict.fromkeys(previous.stop_at + undertaking.stop_at)))
            intent = proposal.intent
        current_targets = [t for t in context.targets
                           if (t.activity, t.ref) == (undertaking.activity, undertaking.target)]
        if len(current_targets) != 1 or undertaking.method not in current_targets[0].methods:
            return self._result("unresolved", "The authorized target or method is no longer available.", "authorization")
        if context.unavailable:
            return self._result("unresolved", "Required situational information is unavailable. No activity was executed.", "context")
        try:
            step = self.domain.assess(undertaking, context)
            if step is None:
                return self._result("unresolved", "No responsible gameplay capability supports that activity here.", "routing")
            self._validate_step(step, context)
            if not set(undertaking.constraints).issubset(step.supported_constraints):
                return self._result("unresolved", "The gameplay capability cannot honor those constraints.", "authorization")
            if intent == "commit" and not set(undertaking.conditions).issubset(step.satisfied_conditions):
                return self._result("unresolved", "The activity's conditions are not established. No activity was executed.", "authorization")
            if not set(undertaking.stop_at).issubset(step.supported_stops):
                return self._result("unresolved", "The gameplay capability cannot honor those stopping boundaries.", "authorization")
            authorization = ActivityAuthorization(undertaking.ref, undertaking.method, intent,
                                                 undertaking.constraints, undertaking.answered_choices)
            missing = tuple(dict.fromkeys(step.checkpoint.missing_means + tuple(
                m for m in step.required_means if m not in context.means)))
            checkpoint = replace(step.checkpoint, missing_means=missing)
            control = decide_activity_control(authorization, checkpoint)
        except Exception:
            return self._result("unresolved", "The gameplay assessment is unavailable. No activity was executed.", "domain")
        fields = dict(responsibilities=step.responsibilities, undertaking=undertaking, context=context, step=step)
        public = dict(context.accessible)
        description = " ".join(public[r] for r in step.public_refs)
        if intent != "commit":
            # Read-only preparation assessment; does not establish physical preparation.
            return self._result("inquiry" if intent == "inquiry" else "preparation",
                                ("No attempt has been made. " if intent == "inquiry" else
                                 "This is a preparation assessment; no action has been taken. ") + description, **fields)
        self.undertaking = undertaking
        if control.status == "complete" or step.ref in undertaking.accepted_steps:
            return self._result("complete", description, **fields)
        if control.status != "continue":
            self._offered = tuple(key for key, _ in step.choices)
            self._choice_context = context
            self._responses = tuple((phrase.strip().casefold().rstrip("."), key) for phrase, key in step.response_phrases)
            choices = tuple(public[r] for _, r in step.choices)
            if step.boundary == "decision":
                return self._result("decision", description, **fields)
            return self._result("clarification", "The activity cannot continue as authorized. " +
                                description,
                                choices=choices, **fields)
        decision = self._result("proceed", description or "The next situated activity may proceed.", **fields)
        self._pending = decision
        return decision

    @staticmethod
    def _validate_step(step, context):
        if (not isinstance(step, DomainStep) or not _text(step.ref)
                or not isinstance(step.checkpoint, ActivityCheckpoint)
                or not _refs(step.responsibilities) or not step.responsibilities
                or not _refs(step.required_means) or not _refs(step.public_refs)
                or not _refs(step.supported_constraints)
                or not _refs(step.satisfied_conditions) or not _refs(step.supported_stops)
                or step.boundary not in {"clarification", "decision"}
                or not isinstance(step.response_phrases, tuple)
                or any(not isinstance(p, tuple) or len(p) != 2 or not all(_text(v) for v in p)
                       for p in step.response_phrases)
                or len({p.strip().casefold().rstrip(".") for p, _ in step.response_phrases}) != len(step.response_phrases)
                or any(key not in dict(step.choices) for _, key in step.response_phrases)
                or not isinstance(step.choices, tuple)
                or any(not isinstance(p, tuple) or len(p) != 2 or not all(_text(v) for v in p) for p in step.choices)
                or len(dict(step.choices)) != len(step.choices)):
            raise ValueError("step")
        visible = dict(context.accessible)
        if not set(step.public_refs + tuple(r for _, r in step.choices)).issubset(visible):
            raise ValueError("disclosure")

    def execute(self, decision):
        if decision is not self._pending or decision is None:
            return self._result("unresolved", "There is no current execution permission.", "authorization")
        self._pending = None  # Consumed even when an owner rejects or throws.
        try:
            current = self._context()
        except Exception:
            return self._result("unresolved", "The current situation is unavailable. No activity was executed.", "context")
        if current != decision.context:
            return self._result("unresolved", "Circumstances changed. Reassess before continuing.", "context")
        try:
            # Read-only reassessment also binds domain-owned mutable premises to the permit.
            step = self.domain.assess(decision.undertaking, current)
            if step != decision.step:
                return self._result("unresolved", "The next activity changed. Reassess before continuing.", "domain")
            receipt = self.domain.execute(decision.undertaking, step, current)
            if (not isinstance(receipt, AcceptedStep) or receipt.ref != step.ref
                    or not _refs(receipt.public_refs)
                    or receipt.outcome not in {"positive", "negative", "incomplete", "unresolved", "complete"}):
                raise ValueError("receipt")
            # The owning Character/domain boundary can project newly accepted meaning
            # which was not knowable in the pre-execution context.
            accessible = receipt.accessible or current.accessible
            validate_context(replace(current, accessible=accessible))
            if not set(receipt.public_refs).issubset(dict(accessible)):
                raise ValueError("receipt disclosure")
            receipt = replace(receipt, accessible=accessible)
        except Exception:
            return self._result("unresolved", "The gameplay operation is unavailable; no fictional outcome is asserted.", "technical")
        self.undertaking = replace(decision.undertaking,
                                  accepted_steps=decision.undertaking.accepted_steps + (receipt.ref,))
        message = " ".join(dict(receipt.accessible)[r] for r in receipt.public_refs)
        return self._result("accepted", message or "The accepted result has no supplied description.",
                            responsibilities=decision.responsibilities, undertaking=self.undertaking, results=(receipt,))

    def process(self, **request):
        return self._progress(self.decide(**request))

    def process_intent(self, player_input, *, provider):
        return self._progress(self.decide_intent(player_input, provider=provider))

    def _progress(self, decision):
        results, messages, responsibilities = (), [], ()
        # Bounded synchronous progression of this undertaking only. No queued tasks,
        # speculative future steps or new independent authorization. Each step has
        # its own fresh F05 decision and owning-domain execution/acceptance.
        for _ in range(16):
            if decision is None or decision.status != "proceed":
                break
            accepted = self.execute(decision)
            if accepted.status != "accepted":
                decision = accepted
                break
            results += accepted.results
            messages.append(accepted.message)
            responsibilities = tuple(dict.fromkeys(responsibilities + accepted.responsibilities))
            decision = self.decide(resume=True)
        else:
            if decision is not None and decision.status == "proceed":
                self._pending = None
                decision = self._result("unresolved", "Further progression could not be bounded safely.", "domain")
        if not results:
            return (replace(decision, message="The authorized activity has concluded.")
                    if decision is not None and decision.status == "complete" and not decision.message else decision)
        boundary_message = decision.message.replace("No activity was executed.", "No further activity was executed.")
        if boundary_message and boundary_message not in messages:
            messages.append(boundary_message)
        # Already accepted meaning survives a later failure; do not recast it as
        # failure or erase it because the next checkpoint could not be assessed.
        return replace(decision, status="accepted" if decision.status == "complete" else decision.status,
                       message=" ".join(messages), results=results,
                       responsibilities=tuple(dict.fromkeys(responsibilities + decision.responsibilities)),
                       undertaking=self.undertaking)


class SceneObservation:
    """Existing safe scene projection, read-only; no search/door mechanics supplied."""
    def assess(self, undertaking, context):
        if undertaking.activity != "observe" or undertaking.target != context.location:
            return None
        return DomainStep("observe:" + context.revision, ActivityCheckpoint(undertaking.ref, "observe"),
                          ("world", "character"), public_refs=("scene",))

    def execute(self, undertaking, step, context):
        return AcceptedStep(step.ref, ("scene",))
