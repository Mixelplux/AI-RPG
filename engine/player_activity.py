"""Bounded player-input connection to the existing consequential owners.

The installed supplier returns current SituatedContext from legitimate domains.
Aliases and routine methods are supplied, never inferred from internal facts.
No callbacks, parser state or presentation state are saved in a campaign.
"""
from dataclasses import replace
import re
from uuid import uuid4

from engine import gameplay_coordination as coordination
from engine.consequence_integration import Request


def unresolved(message, failure="interpretation"):
    return coordination.CoordinationDecision("unresolved", message, failure).player_result()


def context(engine):
    supplier = engine._player_activity_context
    if supplier is None:
        raise ValueError("No situated activity supplier installed")
    current = supplier(engine)
    coordination.validate_context(current)
    if current.location != engine.world_state["player"]["current_location_id"]:
        raise ValueError("Stale situated location")
    return current


def process(engine, text, *, request_id=None, undertaking_id=None):
    runtime = engine._consequences
    if runtime.running:
        return unresolved("An activity is already being resolved.", "authorization")
    if (not isinstance(text, str) or not text.strip()
            or any(v is not None and (not isinstance(v, str) or not v.strip())
                   for v in (request_id, undertaking_id))):
        return unresolved("Supply one supported instruction.")
    raw = text.strip().casefold().rstrip(".?")
    if raw == "continue" and text.strip().endswith("?"):
        return unresolved("Specify a commitment to continue, or ask about a supported target.")
    if raw == "retry":
        prior = next((r for r in runtime.state.receipts if r.request.id == request_id), None)
        if prior is None or undertaking_id is not None and prior.request.undertaking != undertaking_id:
            return unresolved("Identify the accepted request to retry.")
        result = engine.process_consequence(prior.request)
        return identified(result, prior.request)
    try:
        current = context(engine)
    except Exception:
        return unresolved("The current activity context is unavailable. No activity was executed.", "context")
    if current.unavailable:
        return unresolved("Required situational information is unavailable. No activity was executed.", "context")
    data = runtime.campaign.data
    continued = None
    if raw == "continue":
        candidates = [a for a in data.activities if undertaking_id is None or a.id == undertaking_id]
        if len(candidates) != 1:
            return unresolved("Identify one undertaking to continue.", "authorization")
        continued = candidates[0]
        receipts = [r for r in data.state.receipts if r.request.undertaking == continued.id]
        if receipts and receipts[-1].step.outcome == "complete":
            return coordination.CoordinationDecision("complete",
                "That undertaking has concluded. A new instruction would begin a new attempt.").player_result()
        proposal = coordination.Interpretation(continued.action, "continue", continued.target,
            continued.method, constraints=continued.constraints)
    else:
        # Inspection is a bounded spelling of the supplied search activity, not
        # a new mechanic. Inquiry/preparation remain I1's explicit grammar.
        normalized = re.sub(r"^((?:(?:can|could) i |how can i |prepare to )?)(?:inspect|examine)\b",
                            r"\1search", text.strip(), flags=re.IGNORECASE)
        proposal = coordination.interpret(normalized, current)
        if proposal is None:
            return unresolved("That instruction is not supported here. No activity was executed.", "routing")
    if proposal.independent or proposal.ambiguous or proposal.target is None:
        return coordination.CoordinationDecision("clarification",
            "Specify one supported target and approach. No activity was executed.").player_result()
    targets = [t for t in current.targets if (t.ref, t.activity) == (proposal.target, proposal.activity)]
    if len(targets) != 1:
        return unresolved("That activity is not currently available.", "authorization")
    target = targets[0]
    method_id = proposal.method or target.routine_method
    if method_id is None:
        return coordination.CoordinationDecision("clarification",
            "Which method do you want to use? No activity was executed.").player_result()
    method = next((m for m in runtime.config.methods if m.id == method_id
                   and m.action == proposal.activity), None)
    if (method is None or method_id not in target.methods
            or method_id not in dict(runtime.config.targets).get(target.ref, ())):
        return unresolved("That method is not available for this activity.", "authorization")
    # This finite domain has no mechanics implementing carefulness/quietness.
    # Preserve such constraints by refusing, never silently dropping them.
    if proposal.constraints:
        return unresolved("The gameplay capability cannot honor those constraints.", "authorization")
    if undertaking_id is not None and continued is None:
        continued = next((a for a in data.activities if a.id == undertaking_id), None)
        if continued is None or (continued.action, continued.target, continued.method, continued.constraints) != (
                proposal.activity, target.ref, method.id, proposal.constraints):
            return unresolved("That instruction does not match the undertaking.", "authorization")
    identity = request_id or str(uuid4())
    prior = next((r for r in runtime.state.receipts if r.request.id == identity), None)
    undertaking = continued.id if continued else prior.request.undertaking if prior else None
    request = Request(identity, runtime.config.actor, proposal.activity, target.ref, method.id,
                      method.means, proposal.constraints, intent=proposal.intent, undertaking=undertaking)
    if prior and prior.request != request:
        return unresolved("That request identity belongs to a different accepted instruction.", "authorization")
    if prior:
        return identified(engine.process_consequence(prior.request), prior.request)
    if not set(method.means).issubset(current.means):
        return unresolved("The chosen method lacks required means.", "authorization")
    if proposal.intent != "commit":
        # Assessment uses the common coordinator without creating durable activity.
        return engine.process_consequence(request, context_supplier=lambda: context(engine))
    original = runtime.campaign
    created = None
    if undertaking is None:
        undertaking = engine.begin_undertaking(request.action, request.target, request.method,
                                               constraints=request.constraints)
        request = replace(request, undertaking=undertaking)
        created = runtime.campaign
    result = engine.process_consequence(request, context_supplier=lambda: context(engine))
    if created is not None and runtime.campaign is created:
        # No accepted increment or owner revision occurred. Do not retain an
        # implementation-only activity created for a rejected proposal.
        runtime.campaign = original
        return result
    return identified(result, request)


def identified(result, request):
    # Opaque transport references, not hidden world/context information.
    result["player_activity"] = {"request_id": request.id, "undertaking_id": request.undertaking}
    return result
