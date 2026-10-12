"""Bounded handling objectives, disclosure and contextual confirmation.

Frames are proposals, not authority. One production pathway serves all authored
handling targets; investigation retains its smaller independent frame.
"""
from copy import deepcopy
from dataclasses import asdict, dataclass, replace
import re

from engine import character_competence as competence
from engine import material_state as material
from engine.target_resolver import actor_aliases


@dataclass(frozen=True)
class HandlingFrame:
    operation: str
    objective: str
    target_ref: str
    method_ref: str | None = None
    constraints: tuple[str, ...] = ()


@dataclass(frozen=True)
class Confirmation:
    constraints: tuple[str, ...] = ()
    cooperative_only: bool = False


class ActionFocus:
    """Unsaved references and one proposal; never material consequence ownership."""
    def __init__(self):
        self.record = None
        self.pending = None

    def clear(self):
        self.record = self.pending = None

    def snapshot(self):
        return deepcopy({"focus": self.record, "pending": self.pending})

    def observe(self, engine):
        if self.pending and self.pending["basis"] != basis(engine, self.pending["frame"].target_ref):
            self.pending = None
        if self.record:
            item = material.target(engine.region, self.record["target_ref"])
            self.record["status"] = "active" if item and item["location_id"] == engine.world_state["player"]["current_location_id"] else "suspended"


def result(status, message, *, frame=None, changed=False, **extra):
    frame = frame if isinstance(frame, HandlingFrame) else None
    return {"success": status in {"assessed", "answered", "accepted", "replayed", "control", "interrupted"},
            "intent": "contextual_action", "message": message,
            "action": {"type": "contextual_action", "target": frame.target_ref if frame else None, "parameters": {}, "confidence": 1.0},
            "contextual_action": {"status": status, "changed": changed, "frame": asdict(frame) if frame else None, **extra}}


def basis(engine, identity):
    item = material.target(engine.region, identity)
    actor = item["cooperation"]["actor_id"] if item and item["cooperation"] else None
    from engine.world_state import get_effective_actor_location
    return (engine.world_state["player"]["current_location_id"],
            engine.world_state["time"].get("elapsed_hours", 0),
            engine.world_state["history"][-1]["history_id"] if engine.world_state["history"] else None,
            (actor, get_effective_actor_location(engine.region, engine.world_state, actor)) if actor else None)


def _mentions(text, aliases):
    return any(re.search(r"\b" + re.escape(alias.casefold()) + r"\b", text) for alias in aliases)


def _confirmation(text):
    """A bounded acknowledgment grammar, independent of scenario/target names."""
    words = re.sub(r"[, ]+", " ", text).strip()
    words = re.sub(r"^please | please$", "", words)
    if re.fullmatch(r"(?:confirm(?: (?:it|that|the proposal|the action|the plan))?|(?:yes|okay|ok|all right|alright)(?: (?:do|try|start) (?:it|that))?|go ahead|(?:do|try) (?:it|that))(?: carefully)?", words):
        return Confirmation()
    if re.fullmatch(r"(?:continue|proceed)(?: with)? (?:it|that|the proposal|the action|the plan|help|the help)", words):
        return Confirmation(cooperative_only="help" in words.split())
    return None


def _actors_and_targets(engine, text, *, social=False):
    present = set(engine.get_scene_snapshot()["entities"]["static"])
    actors = [a for a in engine.region.get("entities", []) if a.get("entity_id") in present
              and _mentions(text, actor_aliases(a, a["entity_id"], components=True))]
    spans = [(a["entity_id"], match.span()) for a in actors
             for alias in actor_aliases(a, a["entity_id"], names_only=True)
             for match in re.finditer(r"\b" + re.escape(alias) + r"\b", text)]
    # A full personal name outranks a component contained within it. Separate
    # explicit names still remain separate referents, even with shared first names.
    named_ids = {identity for identity, (start, end) in spans
                 if not any(left <= start and end <= right and (left, right) != (start, end)
                            for _, (left, right) in spans)}
    named = [a for a in actors if a["entity_id"] in named_ids] if named_ids else [
        a for a in actors if _mentions(text, actor_aliases(a, a["entity_id"], names_only=True, components=True))]
    if named:
        actors = named
    catalog = {a["entity_id"]: a for a in engine.region.get("entities", []) if a.get("persistence") == "static"}
    targets = []
    for item in material.declarations(engine.region):
        policy = item["cooperation"]
        helper_aliases = actor_aliases(catalog[policy["actor_id"]], policy["actor_id"], components=True) if policy else set()
        # Actor roles in earlier material aliases are actor references, not body
        # targets. 'Push Tessa' must never silently become 'push her cart'.
        features = [alias for alias in item["aliases"] if alias.casefold() not in helper_aliases]
        if _mentions(text, features) or social and policy and any(a["entity_id"] == policy["actor_id"] for a in actors):
            targets.append(item)
    return actors, targets


def _speech_operation(text, *, question=False):
    help_word = r"(?:help|assistance|a hand|assist)"
    query_head = re.match(r"^(?:(?:i )?(?:ask|question|check|wonder)|does|do|is|are|can|could|would|find out)\b", text)
    if (query_head or question) and re.search(r"\b(?:needs?|requires?|use)\b.*\b" + help_word + r"\b", text):
        return "inquire"
    if re.search(r"\boffer\b.*\b" + help_word + r"\b", text) or re.match(r"^i (?:can|will|would like to) help\b", text):
        return "cooperate"
    if re.search(r"\b(?:ask|request)\b.*\bto (?:help|assist|cooperate)\b", text) or re.search(r"\brequest\b.*\bcooperation\b", text):
        return "cooperate"
    return None


def _feasibility_objective(text):
    """Recognize epistemic ability clauses within a bounded assessment objective.

    Inspecting to learn whether handling is possible requests information. It
    never authorizes the handling mentioned in that subordinate clause. A guard
    on a commitment (including another 'if' clause) still fails closed.
    """
    objective = re.sub(r"^i (?:want|would like) to ", "", text)
    ability = r"(?:see|check|find out|assess) (?:if|whether) (?:i|we) (?:can|could)\b"
    if not re.match(r"^(?:inspect|examine|assess|check)\b", objective) and not re.match(ability, objective):
        return False
    clauses = list(re.finditer(ability, objective))
    if not clauses:
        return False
    epistemic_ifs = {m.start() + m.group().index(" if ") + 1 for m in clauses if " if " in m.group()}
    return all(m.start() in epistemic_ifs for m in re.finditer(r"\bif\b", objective))


def interpret(engine, raw):
    text = re.sub(r"\s+", " ", raw.casefold().replace("’", "'").strip()).rstrip(".!?")
    if text in {"cancel action", "finish action", "decline involvement", "leave it alone", "do not get involved", "don't get involved"}:
        return "cancel"
    confirmation = _confirmation(text)
    if confirmation:
        return result("clarification_needed", "A question does not confirm a material commitment.") if raw.strip().endswith("?") else confirmation
    if text in {"maybe", "yes or no", "either one", "continue", "yes continue"}:
        return result("clarification_needed", "Name one intended action; that response does not authorize a proposal.")
    if text in {"look", "look around", "look here", "wait"} or text.startswith(("go to ", "head to ", "move to ")):
        return None
    if re.match(r"^(?:talk|speak|greet)\b", text):
        return None
    if re.match(r"^i\s+(?:walk|move|wander|stroll)\s+(?:through|around|about|among|along)\b", text):
        return None
    if re.search(r"\b(as long as|provided|unless|only if|until|while|before|after)\b", text):
        return result("clarification_needed", "That conditional limit is outside the supported handling contract; state a supported objective and restriction explicitly.")
    positive = text
    constraints = []
    clauses = re.split(r"[;,]|\bbut\b|\band (?=don't|do not|without|stop)\b", text.replace(" without ", "; without "))
    positive_clauses = []
    for clause in clauses:
        clause = clause.strip()
        if not clause:
            continue
        if re.search(r"\b(without|don't|do not|avoid|not|stop|keep(?:ing)?)\b", clause):
            recognized = False
            if re.search(r"\b(damag\w*|harm\w*|intact|cargo|contents)\b", clause):
                constraints.append("preserve_integrity"); recognized = True
            if re.search(r"\b(talk\w*|ask\w*|speak\w*|driver|cooperat\w*)\b", clause):
                constraints.append("no_talk"); recognized = True
            if re.search(r"\b(mov\w*|push\w*|reposition\w*)\b", clause):
                constraints.append("no_move"); recognized = True
            if re.search(r"\b(adjust\w*|repair\w*|fix\w*)\b", clause):
                constraints.append("no_adjust"); recognized = True
            if re.search(r"\b(touch\w*|interven\w*|assess\w*|inspect\w*)\b", clause):
                constraints.append("assess_only"); recognized = True
            if not recognized or re.search(r"\b(and|spend|pay|steal|break|hour|kill|magic)\b", clause):
                return result("clarification_needed", "That restriction is unsupported or ambiguous; no action has been applied.")
        else:
            positive_clauses.append(clause)
    positive = " ".join(positive_clauses)
    confirmation = _confirmation(positive)
    if confirmation:
        return replace(confirmation, constraints=tuple(dict.fromkeys(constraints)))
    if not positive:
        return result("clarification_needed", "State a positive objective; restrictions alone authorize no action.")
    if re.fullmatch(r"(?:find|look for|show me) (?:another|an? alternate|an? alternative) (?:route|way)", positive):
        routes = engine.get_player_perception()["navigation"]["route_cues"]
        return result("assessed", " ".join(cue["text"] for cue in routes) or "No alternative local route is supplied.")
    if re.search(r"\b(or|maybe|perhaps|possibly|might)\b", positive):
        return result("clarification_needed", "Choose one definite action; alternatives or tentative language do not confirm a proposal.")
    speech = _speech_operation(positive, question=raw.strip().endswith("?"))
    feasibility = _feasibility_objective(positive)
    if "if" in positive.split() and speech != "inquire" and not feasibility:
        return result("clarification_needed", "That conditional action needs clarification; it is not a confirmation or agreement.")
    actors, targets = _actors_and_targets(engine, positive, social=bool(speech or re.search(r"\bhelp\b", positive)))
    if len(actors) > 1:
        return result("clarification_needed", "Name one unambiguous present actor; no cooperation or handling has occurred.")
    pronouns = r"\b(it|that|this|her|him|them)\b" if speech or re.search(r"\bhelp\b", positive) else r"\b(it|that|this)\b"
    if not targets and re.search(pronouns, positive):
        focus = engine._action_focus.record
        if focus:
            targets = [d for d in material.declarations(engine.region) if d["target_id"] == focus["target_ref"]]
    family = re.search(r"\b(help|clear|secure|close|shut|brace|steady|stabiliz\w*|adjust|straighten|fix|repair|push|pull|shift|reposition|assess|inspect|examine|check|move|force|ask|request|offer|cooperat\w*)\b", positive)
    if not targets and not family:
        return None
    if len(targets) != 1:
        if actors and (speech or re.search(r"\bhelp\b", positive)):
            return result("unsupported", "That actor has no unambiguous authored handling association for this exchange.")
        return result("clarification_needed", "Name one material target or its visible feature.")
    item = targets[0]
    if actors and (item["cooperation"] is None or actors[0]["entity_id"] != item["cooperation"]["actor_id"]):
        return result("unsupported", "That actor is not the declared helper for this material target; no cooperation or handling is inferred.")
    if re.search(r"\b(unload|take|steal|destroy|burn|kill|attack|buy|pay|bribe|threaten|magic|climb|carry|drag away|transfer|reward|promise|recruit|follow|pursue|wait|hours?|minutes?|coins?|gold)\b", positive):
        return result("unsupported", "That approach is outside the supported local handling capabilities.")
    if re.search(r"\b(using|by)\b", positive) or re.search(r"\bwith\b", positive) and not actors and not re.search(r"\b(help|cooperation|support|care)\b", positive):
        return result("unsupported", "That additional method is not supported; no preparation or handling occurs.")
    operations = set()
    if speech:
        operations.add(speech)
    elif re.search(r"\b(ask|question|request)\b", positive):
        return result("unsupported", "Only a question about needing help or an explicit cooperation request is supported here; neither handling nor agreement is inferred.")
    elif feasibility or re.search(r"\b(assess|inspect|examine|check|could|whether)\b", positive) or raw.strip().endswith("?"):
        operations.add("assess")
    else:
        if re.search(r"\b(brace|steady|stabiliz\w*)\b", positive): operations.add("stabilize")
        if re.search(r"\b(adjust|straighten|fix|repair)\b", positive): operations.add("adjust")
        if re.search(r"\b(clear|secure|close|push|pull|shift|reposition|move|out of|aside|shut)\b", positive): operations.add("reposition")
        # A bounded help objective chooses a relevant handling family, not a script.
        if not operations and re.search(r"\b(help|sort out)\b", positive): operations.add("reposition")
    if "stabilize" in operations and len(operations) == 2 and operations & {"adjust", "reposition"}:
        operations.remove("stabilize")
    if len(operations) != 1:
        return result("clarification_needed", "Choose one objective or approach; no additional commitment is inferred.")
    operation = operations.pop()
    method = None
    if operation in material.OPERATIONS:
        choices = [m for m in item["methods"] if m["operation"] == operation]
        if re.search(r"\b(force|hard|roughly|alone)\b", positive):
            choices = [m for m in choices if m["risk"] and not m["cooperate"]]
        else:
            choices = sorted(choices, key=lambda m: (bool(m["risk"]), m["method_id"]))[:1]
        if len(choices) != 1:
            return result("unsupported", "No declared method supports that approach.")
        method = choices[0]["method_id"]
    return HandlingFrame(operation, positive, item["target_id"], method, tuple(dict.fromkeys(constraints)))


def assess(engine, frame, *, world=None):
    """Shared pure assessment used by raw/structured execution and projection."""
    if not isinstance(frame, HandlingFrame) or not isinstance(frame.operation, str) or not isinstance(frame.target_ref, str) or frame.method_ref is not None and not isinstance(frame.method_ref, str) or frame.operation not in material.OPERATIONS | {"assess", "inquire", "cooperate"} or not isinstance(frame.objective, str) or not frame.objective.strip() or not isinstance(frame.constraints, tuple) or any(not isinstance(c, str) or c not in material.CONSTRAINTS for c in frame.constraints) or len(set(frame.constraints)) != len(frame.constraints):
        return {"status": "unsupported", "reason": "Unsupported handling frame."}
    item = material.target(engine.region, frame.target_ref)
    if item is None:
        return {"status": "unsupported", "reason": "No declared material target supports that action."}
    world = world if world is not None else engine.world_state
    if item["location_id"] != world["player"]["current_location_id"]:
        return {"status": "impossible", "reason": "That material target is not accessible here."}
    record = world[material.STATE_KEY][item["target_id"]]
    if frame.operation == "assess":
        if frame.method_ref is not None:
            return {"status": "unsupported", "reason": "Assessment does not authorize a handling method."}
        return {"status": "feasible", "cost_hours": 0, "risk": "", "steps": []}
    conflicts = set() if frame.operation == "inquire" else {"assess_only"}
    if frame.operation in {"cooperate", "inquire"}:
        if frame.method_ref is not None:
            return {"status": "unsupported", "reason": "An exchange does not authorize a physical handling method."}
        conflicts.add("no_talk")
        method = None
        needs_cooperation = True
    else:
        method = next((m for m in item["methods"] if m["method_id"] == frame.method_ref and m["operation"] == frame.operation), None)
        if method is None:
            return {"status": "unsupported", "reason": "That method is not declared for this operation."}
        if not material.matches(record["conditions"], method["when"]):
            return {"status": "impossible", "reason": "The current material conditions do not permit that method."}
        conflicts.update(method["conflicts"])
        if frame.operation == "reposition": conflicts.add("no_move")
        if frame.operation == "adjust": conflicts.add("no_adjust")
        if method["cooperate"]: conflicts.add("no_talk")
        needs_cooperation = method["cooperate"]
    if set(frame.constraints) & conflicts:
        return {"status": "constraint_conflict", "reason": "That method conflicts with your explicit restriction; acknowledgment cannot override it."}
    if needs_cooperation:
        policy = item["cooperation"]
        from engine.world_state import get_effective_actor_location
        if policy is None or get_effective_actor_location(engine.region, world, policy["actor_id"]) != item["location_id"]:
            return {"status": "impossible", "reason": "The required helper is not present."}
        refuses = policy["refuse_when"] and all(record["conditions"][k] == v for k, v in policy["refuse_when"].items())
        if (refuses or record["cooperation"] == "refused") and frame.operation not in {"cooperate", "inquire"}:
            return {"status": "refused", "reason": policy["refusal"]}
    if method is None:
        return {"status": "feasible", "cost_hours": 0, "risk": "", "steps": ["request cooperation"]}
    steps = material.routine_steps(method)
    return {"status": "uncertain" if frame.operation != "stabilize" else "feasible",
            "cost_hours": 1, "risk": method["risk"], "steps": steps}


def _replay(engine, frame):
    record = engine.world_state[material.STATE_KEY][frame.target_ref]
    return next((e for e in reversed(engine.world_state["history"])
                 if e.get("event_type") == "material_outcome" and e.get("target_id") == frame.target_ref
                 and e.get("method_id") == frame.method_ref and e.get("after") == record["conditions"]
                 and e.get("cooperation_after") == record["cooperation"]), None)


def execute(engine, frame, *, authorized=False):
    assessment = assess(engine, frame)
    status = assessment["status"]
    if status not in {"feasible", "uncertain"}:
        return result(status, assessment["reason"], frame=frame)
    item = material.target(engine.region, frame.target_ref)
    if frame.operation == "inquire":
        policy = item["cooperation"]
        record = engine.world_state[material.STATE_KEY][frame.target_ref]
        actor = next(a for a in engine.region["entities"] if a["entity_id"] == policy["actor_id"])
        refuses = policy["refuse_when"] and all(record["conditions"][k] == v for k, v in policy["refuse_when"].items())
        eligible = any(material.matches(record["conditions"], m["when"]) for m in item["methods"])
        if refuses:
            text = actor["name"] + ": Current conditions prevent the supported cooperative handling approach. This question makes no new agreement."
        elif record["cooperation"] == "willing":
            text = actor["name"] + " has already agreed to supported help. This question does not change that agreement."
        else:
            text = actor["name"] + (": The " + item["label"] + " could use supported handling. No help has been agreed." if eligible else ": No supported handling help is needed under the current conditions.")
        return result("answered", text, frame=frame)
    if frame.operation == "assess":
        text = " ".join(material.observations(engine.region, engine.world_state))
        approaches = [m["label"] for m in item["methods"] if material.matches(engine.world_state[material.STATE_KEY][frame.target_ref]["conditions"], m["when"])]
        return result("assessed", text + " Supported approaches: " + "; ".join(approaches) + ". Handling takes 1 hour; uncertain attempts can fail.", frame=frame)
    if frame.operation in material.OPERATIONS:
        replay = _replay(engine, frame)
        if replay:
            return result("replayed", replay["summary"], frame=frame, narrative_action_id=replay["history_id"], outcome=replay["result"], cost_hours=0)
    if frame.operation in material.OPERATIONS and not authorized:
        engine._action_focus.pending = {"frame": frame, "basis": basis(engine, frame.target_ref), "disclosure": deepcopy(assessment)}
        engine._action_focus.record = {"target_ref": frame.target_ref, "objective": frame.objective, "status": "active", "event_refs": [], "frame": frame}
        risk = assessment["risk"] or "No additional material damage risk is declared; the attempt can still fail."
        return result("authorization_required", f"Proposed method: {assessment['steps'][-1]}. Material risk: {risk} Cost: 1 hour. Confirm this proposal or choose another approach.", frame=frame)
    from engine.world_state import copy_world_state
    candidate = copy_world_state(engine.world_state)
    if frame.operation == "cooperate":
        policy = item["cooperation"]
        record = candidate[material.STATE_KEY][frame.target_ref]
        refuses = policy["refuse_when"] and all(record["conditions"][k] == v for k, v in policy["refuse_when"].items())
        choice = "refused" if refuses else "willing"
        text = policy["refusal"] if refuses else policy["offer"]
        if record["cooperation"] == choice:
            return result("replayed", text, frame=frame)
        candidate = material.transition(engine.region, candidate, frame.target_ref, "material_cooperation", {}, cooperation=choice, extra={"actor_id": policy["actor_id"]}, summary=text)
        outcome, time_result = "cooperation", None
    else:
        method = next(m for m in item["methods"] if m["method_id"] == frame.method_ref)
        effects = {"stability": "braced"} if method["brace"] else {}
        candidate = material.transition(engine.region, candidate, frame.target_ref, "material_preparation", effects,
            cooperation="willing" if method["cooperate"] else None,
            extra={"method_id": method["method_id"], "constraints": list(frame.constraints), "risk_authorized": authorized},
            summary="Accepted routine preparation: " + "; ".join(assessment["steps"][:-1]) + ".")
        source_id = candidate["history"][-1]["history_id"]
        candidate, time_result = engine._prepare_time_advance_candidate(candidate, 1)
        time_event = next(e for e in reversed(candidate["history"]) if e["event_type"] == "time_advanced")
        time_event["source_history_id"] = source_id
        # The preparation/time effects remain accepted if an authored development
        # makes the remaining action impossible. No draw is consumed then.
        now = assess(engine, frame, world=candidate)
        if now["status"] not in {"feasible", "uncertain"}:
            draw, outcome, effects = None, "interrupted", {}
            text = "After preparation and 1 hour of effort, changed circumstances stop the remaining action. " + now["reason"]
        else:
            draw = None if frame.operation == "stabilize" else competence.draw_d6()
            outcome = "full" if draw is None else competence.resolve(draw, False)
            effects = method["outcomes"][outcome]["effects"]
            text = method["outcomes"][outcome]["text"] + " Effort: 1 hour."
        candidate = material.transition(engine.region, candidate, frame.target_ref, "material_outcome", effects,
            source_id=source_id, extra={"method_id": method["method_id"], "time_history_id": time_event["history_id"], "draw": draw, "result": outcome}, summary=text)
    # No world, scene, pending proposal or focus changes before this succeeds.
    engine._publish_candidate(candidate)
    event_id = candidate["history"][-1]["history_id"]
    engine._action_focus.pending = None
    engine._action_focus.record = {"target_ref": frame.target_ref, "objective": frame.objective, "status": "active", "event_refs": [event_id], "frame": frame}
    packet = result("interrupted" if outcome == "interrupted" else "accepted", text, frame=frame, changed=True,
                    outcome=outcome, cost_hours=1 if time_result else 0, routine_steps=assessment["steps"])
    packet["narrative_action_id"] = event_id
    if time_result: packet["time_advancement"] = time_result
    return packet


def _bound_constraints(engine, frame):
    """A rephrasing cannot silently discard limits on the same handling goal."""
    pending = engine._action_focus.pending
    focus = engine._action_focus.record
    bound = pending["frame"] if pending else focus.get("frame") if focus else None
    if (isinstance(bound, HandlingFrame) and bound.operation in material.OPERATIONS
            and frame.operation in material.OPERATIONS and bound.target_ref == frame.target_ref):
        return replace(frame, constraints=tuple(dict.fromkeys(bound.constraints + frame.constraints)))
    return frame


def _confirm(engine, confirmation):
    pending = engine._action_focus.pending
    if pending is None:
        return result("clarification_needed", "There is no single disclosed proposal to confirm; an already resolved action is not repeated.")
    frame = replace(pending["frame"], constraints=tuple(dict.fromkeys(pending["frame"].constraints + confirmation.constraints)))
    if pending["basis"] != basis(engine, frame.target_ref):
        engine._action_focus.pending = None
        return result("stale_authorization", "Circumstances changed. State the action again for a fresh assessment and disclosure.")
    assessment = assess(engine, frame)
    if assessment["status"] not in {"feasible", "uncertain"}:
        engine._action_focus.pending = None
        if assessment["status"] == "constraint_conflict":
            engine._action_focus.record["frame"] = frame
        return result(assessment["status"], assessment["reason"], frame=frame)
    item = material.target(engine.region, frame.target_ref)
    method = next(m for m in item["methods"] if m["method_id"] == frame.method_ref)
    if confirmation.cooperative_only and not method["cooperate"]:
        engine._action_focus.pending = None
        return result("clarification_needed", "That help reference does not identify the disclosed method; no action is confirmed.")
    if any(assessment[k] != pending["disclosure"][k] for k in ("cost_hours", "risk", "steps")):
        engine._action_focus.pending = None
        return result("stale_authorization", "The method, risk or cost changed; a fresh proposal must be disclosed before execution.")
    return execute(engine, frame, authorized=True)


def process(engine, raw=None, *, frame=None):
    if frame is not None and not isinstance(frame, HandlingFrame):
        return result("unsupported", "Supply a supported handling frame.")
    if not material.declarations(engine.region):
        return result("unsupported", "This Region Pack has no material handling declarations.", frame=frame) if frame is not None else None
    proposal = frame if frame is not None else interpret(engine, raw)
    if isinstance(proposal, dict):
        engine._action_focus.pending = None
        return proposal
    if proposal is None:
        return proposal
    if proposal == "cancel":
        engine._action_focus.clear()
        return result("control", "You leave the handling objective unfinished. Accepted world consequences remain.")
    if isinstance(proposal, Confirmation):
        return _confirm(engine, proposal)
    proposal = _bound_constraints(engine, proposal)
    pending = engine._action_focus.pending
    if frame is None and pending and (proposal.operation, proposal.target_ref, proposal.method_ref) == (pending["frame"].operation, pending["frame"].target_ref, pending["frame"].method_ref):
        return _confirm(engine, Confirmation(constraints=proposal.constraints))
    # A different request retires a prior proposal only after execution succeeds
    # or returns a non-mutating rejection, never if candidate construction fails.
    packet = execute(engine, proposal)
    if packet["contextual_action"]["status"] not in {"authorization_required", "answered"}:
        engine._action_focus.pending = None
    if packet["contextual_action"]["status"] == "assessed":
        old = engine._action_focus.record
        old_frame = old.get("frame") if old else None
        if not isinstance(old_frame, HandlingFrame) or old_frame.operation not in material.OPERATIONS or old_frame.target_ref != proposal.target_ref:
            engine._action_focus.record = {"target_ref": proposal.target_ref, "objective": proposal.objective, "status": "active", "event_refs": []}
    if packet["contextual_action"]["status"] == "constraint_conflict":
        engine._action_focus.record = {"target_ref": proposal.target_ref, "objective": proposal.objective,
                                      "status": "active", "event_refs": [], "frame": proposal}
    if packet["contextual_action"]["status"] == "answered" and not pending:
        old = engine._action_focus.record
        old_frame = old.get("frame") if old else None
        if not isinstance(old_frame, HandlingFrame) or old_frame.operation not in material.OPERATIONS or old_frame.target_ref != proposal.target_ref:
            engine._action_focus.record = {"target_ref": proposal.target_ref, "objective": proposal.objective,
                                          "status": "active", "event_refs": [], "frame": proposal}
    return packet
