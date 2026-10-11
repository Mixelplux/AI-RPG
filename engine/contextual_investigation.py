"""Bounded contextual investigation; derived access and unsaved intent only."""
from copy import deepcopy
from dataclasses import asdict, dataclass
import re

from engine import west_road_predicament as west
from engine import character_competence as competence


@dataclass(frozen=True)
class ActionFrame:
    operation: str
    objective: str
    target_ref: str | None
    method: str
    constraints: tuple[str, ...] = ()
    recipient_ref: str | None = None
    stop_boundary: str = "finding"


@dataclass(frozen=True)
class Candidate:
    ref: str
    kind: str
    label: str
    cue: str
    aliases: tuple[str, ...]
    purposes: tuple[str, ...]
    finding_id: str | None = None


class WestRoadInvestigation:
    """One authored access policy; trace existence alone does not grant access."""
    def candidates(self, engine):
        if not west.enabled(engine.region) or engine.world_state["west_road_predicament"]["phase"] != "investigating":
            return ()
        world, scene = engine.get_world_state(), engine.get_scene_snapshot()
        local = world["player"]["current_location_id"]
        candidates = []
        if local == west.ROAD:
            trace = engine.get_evidence_trace("west_road_tracks_trace")
            if trace == {"trace_id": "west_road_tracks_trace", "evidence_id": "west_road_tracks", "location_id": local}:
                candidates.append(Candidate("west_road_tracks_trace", "evidence", "off-road marks",
                    "Marks away from the wagon path are available for closer examination.",
                    ("tracks", "marks", "signs", "footprints", "repeated watch tracks"),
                    ("watch", "observation", "wagons", "roadside"), "west_road_tracks"))
            if west.MERCHANT in scene["entities"]["static"]:
                candidates.append(Candidate(west.MERCHANT, "actor", "Mara",
                    "Mara, the caravan driver, is here if you want to ask what she saw.",
                    ("mara", "driver", "merchant"), ("account", "saw", "witness"), "west_road_merchant_account"))
        return tuple(candidates)

    def findings(self, engine):
        if not west.enabled(engine.region):
            return ()
        return tuple(Candidate(d["discovery_id"], "finding", d["title"], d["text"],
            ("tracks", "marks", "signs", "repeated watch tracks") if d["discovery_id"] == "west_road_tracks"
            else ("mara", "account", "merchant", "driver"), (), d["discovery_id"])
            for d in engine.region["discovery_declarations"]
            if d["discovery_id"] in west.INITIAL_EVIDENCE and d["discovery_id"] in engine.get_player_discoveries())

    def recipients(self, engine):
        if not west.enabled(engine.region):
            return ()
        return tuple(a for a in engine.region["entities"] if a["entity_id"] in (west.GREY, west.ELIN)
            and a["entity_id"] in engine.get_scene_snapshot()["entities"]["static"])

    def ask(self, engine, candidate):
        if candidate.ref != west.MERCHANT or candidate not in self.candidates(engine):
            return None
        return engine._merchant_account()


class InvestigationFocus:
    """References and one semantic frame; no duplicated world or saved knowledge."""
    def __init__(self):
        self._record = None

    def snapshot(self):
        return deepcopy(self._record)

    def clear(self):
        self._record = None

    def remember(self, engine, frame, references, event_refs):
        old_refs = self._record["recent_event_refs"] if self._record else []
        self._record = {"frame": asdict(frame), "references": list(dict.fromkeys(references))[:4],
            "scope_location": engine.get_world_state()["player"]["current_location_id"], "status": "active",
            "recent_event_refs": list(dict.fromkeys(old_refs + event_refs))[-4:]}

    def observe(self, engine, result):
        if self._record is None or not result.get("success"):
            return None
        if result.get("intent") == "west_road_decision":
            self.clear()
            return "The accepted decision concludes this investigation focus. Your findings and reports remain recorded."
        if engine.get_world_state()["player"]["current_location_id"] != self._record["scope_location"]:
            if self._record["status"] != "suspended":
                self._record["status"] = "suspended"
                return "Your local investigation focus is suspended. Accepted findings and reports are unchanged."
        return None

    def interrupt(self, reason):
        if self._record is None:
            return None
        self.clear()
        return f"The unsaved investigation focus ends on {reason}; accepted findings and reports remain in World State."


def _text(value):
    return re.sub(r"\s+", " ", value.casefold().replace("â€™", "'").strip()).rstrip(".!?")


def _mentions(text, aliases):
    return any(re.search(r"\b" + re.escape(alias) + r"\b", text) for alias in aliases)


def _result(status, message, *, frame=None, changed=False, findings=None):
    return {"success": status in {"survey", "accepted", "already_acquired", "control"},
        "intent": "contextual_investigation", "message": message,
        "action": {"type": "contextual_investigation", "target": None, "parameters": {}, "confidence": 1.0},
        "contextual": {"status": status, "changed": changed, "frame": asdict(frame) if frame else None,
                       "findings": findings or []}}


def context(engine):
    policy = engine._investigation_policy
    return deepcopy({"leads": [asdict(c) for c in policy.candidates(engine)],
                     "findings": [asdict(c) for c in policy.findings(engine)],
                     "focus": engine._investigation_focus.snapshot()})


def interpret(raw, engine):
    """Compose one supported operation from purpose, method and explicit limits."""
    text = _text(raw)
    if text in {"cancel investigation", "finish investigation", "resume investigation"}:
        return text
    # Preserve accepted legacy shortcuts and unrelated gameplay commands.
    if text in {"investigate", "search for clues", "look", "look around", "look here", "clues", "known clues"} or text.startswith(("present ", "talk to ", "go to ", "head to ", "move to ")):
        return None
    if text in {"yes", "yes continue", "continue", "yes, continue"}:
        return _result("clarification_needed", "State the investigation action you want to take; no action is pending for confirmation.")
    verbs = r"\b(survey|investigate|examine|inspect|study|check|ask|question|tell|report|share|look|search|find|learn|understand)\b"
    if not re.search(verbs, text):
        return None
    # Consequential/non-investigation commands retain their existing route.
    if text in west.COMMANDS or text in competence.OPERATIONS or text.startswith("check ") and not re.search(r"\b(deliveries|recorded|tally|seal|tracks|marks|road|evidence)\b", text):
        return None
    markers = ("lead", "leads", "evidence", "investigation", "clues", "tracks", "marks", "signs", "footprints",
               "road", "situation", "mara", "elin", "driver", "account", "tally", "seal", "deliveries", "recorded", "note", "that", "those", "it", "her", "him")
    if not _mentions(text, markers):
        return None
    # Split off restrictions before operation/target recognition: a negated ask
    # must never turn a survey into a conversation, nor an excluded account a report.
    clauses = re.split(r"[;,]|\bbut\b|\band (?=don't|do not|without|stop)\b", text.replace(" without ", "; without "))
    positive, restrictions = [], []
    for clause in clauses:
        clause = clause.strip()
        if not clause:
            continue
        if re.search(r"\b(don't|do not|not|without|avoid|keep .* out|stop|stay)\b", clause):
            restrictions.append(clause)
        else:
            positive.append(clause)
    primary = " ".join(positive)
    if not primary:
        return _result("clarification_needed", "Give a supported positive action; your restrictions have not authorized an action.")
    constraints = []
    excluded = []
    for clause in restrictions:
        if re.search(r"\band\b", clause):
            return _result("clarification_needed", "Separate the restriction from any additional requested action; no effects have been applied.")
        if re.search(r"\b(stay|near|local|nearby)\b", clause):
            constraints.append("local_only")
        if re.search(r"\b(question(?:ing)?|ask(?:ing)?|talk(?:ing)?|speak(?:ing)?)\b", clause):
            constraints.append("no_questioning")
        if re.search(r"\b(follow(?:ing)?|pursu(?:e|ing)|trail)\b", clause):
            constraints.append("no_following")
        if re.search(r"\b(mention|disclose|share|report|tell|keep|account)\b", clause):
            for candidate in engine._investigation_policy.findings(engine):
                if _mentions(clause, candidate.aliases):
                    excluded.append(candidate.ref)
            if "mara" in clause or "account" in clause:
                excluded.append("west_road_merchant_account")
        if re.search(r"\bstop\b", clause) and not re.search(r"\b(lead|finding|examination|reply|report|receipt|first|useful)\b", clause):
            return _result("clarification_needed", "That stopping condition is unsupported; no effects have been applied.")
        recognized = re.search(r"\b(stay|near|local|nearby|question(?:ing)?|ask(?:ing)?|talk(?:ing)?|speak(?:ing)?|follow(?:ing)?|pursu(?:e|ing)|trail|mention|disclose|share|report|tell|keep|account|stop)\b", clause)
        if not recognized or re.search(r"\b(steal|fight|climb|break|open|touch|move|injure|guard|magic|spend|hour)\b", clause):
            return _result("clarification_needed", "That restriction or method is outside this bounded inquiry; no effects have been applied.")
    constraints += ["exclude:" + ref for ref in excluded]
    # Unsupported methods/extra commitments cannot disappear during normalization.
    if re.search(r"\b(follow|pursue|recruit|divert|patrol|climb|steal|fight|break|open|buy|capture|bribe|intimidate|threaten|force|hours?|spend|destroy|hide|conceal|erase|burn|remove|alter|kill|attack|arrest|catch|sell|take|wait|send|magic)\b", primary):
        return _result("unavailable", "That method or consequential choice is outside this local investigation. Choose an explicit supported action.")
    if re.search(r"\b(by|using)\b", primary) or (
            re.search(r"\bwith\b", primary) and not re.search(r"\b(tell|report|share)\b", primary)):
        return _result("clarification_needed", "Specify the supported local inspection, question or report without an additional method; no effects have been applied.")
    operations = set()
    if re.search(r"\b(tell|report|share)\b", primary):
        operations.add("report")
    if re.search(r"\b(ask|question)\b", primary):
        operations.add("ask")
    if re.search(r"\b(examine|inspect|study|check)\b", primary):
        operations.add("examine")
    if len(operations) > 1:
        return _result("clarification_needed", "Choose one inquiry or report at a time; no effects have been applied.")
    operation = next(iter(operations), "survey")
    stop_words = {"survey": {"lead", "leads"}, "examine": {"finding", "examination"},
                  "ask": {"reply"}, "report": {"report", "receipt"}}
    for clause in restrictions:
        if "stop" in clause and not _mentions(clause, stop_words[operation]):
            return _result("clarification_needed", "That stopping condition conflicts with the selected action; no effects have been applied.")
    if operation == "report" and re.search(r"\b(and|or)\b", primary):
        return _result("clarification_needed", "Choose one finding and one recipient for each report; no information has been shared.")
    if operation == "ask" and re.search(r"\b(where|why|join|help|reward|pay|give|guard|camp|identity|who)\b", primary):
        return _result("unavailable", "Only the driver's supported account of what she saw is available in this inquiry.")
    if operation == "ask" and "no_questioning" in constraints:
        return _result("clarification_needed", "Questioning conflicts with your restriction; no conversation has occurred.")
    candidates = engine._investigation_policy.findings(engine) if operation == "report" else engine._investigation_policy.candidates(engine)
    wanted_kind = {"examine": "evidence", "ask": "actor", "report": "finding"}.get(operation)
    choices = [c for c in candidates if wanted_kind is None or c.kind == wanted_kind]
    matched = [c for c in choices if _mentions(primary, c.aliases)]
    if not matched and operation == "examine":
        matched = [c for c in choices if _mentions(primary, c.purposes)]
    if not matched and operation != "survey" and re.search(r"\b(that|those|it|her|him)\b", primary):
        record = engine._investigation_focus.snapshot()
        refs = record["references"] if record else []
        matched = [c for c in choices if c.ref in refs or c.finding_id in refs]
        if record and not matched:
            return _result("unavailable", "The previously selected subject is not available for this action now; choose a current target explicitly.")
    if operation != "survey" and len(matched) != 1:
        status = "clarification_needed" if not matched or len(matched) > 1 else "unavailable"
        return _result(status, "Choose one currently accessible subject for that inquiry or one acquired finding for the report.")
    recipient = None
    if operation == "report":
        recipients = [a for a in engine._investigation_policy.recipients(engine)
            if _mentions(primary, (a["name"].casefold(), a["name"].split(",")[0].casefold(),
                                  "elin" if a["entity_id"] == west.ELIN else "grey" if a["entity_id"] == west.GREY else a["name"].casefold()))]
        if len(recipients) != 1:
            return _result("clarification_needed", "Name one supported recipient who is present; no report has been shared.")
        recipient = recipients[0]["entity_id"]
        if "exclude:" + matched[0].ref in constraints:
            return _result("clarification_needed", "The selected report conflicts with your disclosure restriction; no report has been shared.")
    methods = {"survey": "local_scan", "examine": "inspect_evidence", "ask": "question_actor", "report": "relay_finding"}
    stops = {"survey": "leads", "examine": "finding", "ask": "reply", "report": "receipt"}
    # A constrained signs-only scan excludes a witness lead; no conversation is implied.
    objective = "signs" if operation == "survey" and re.search(r"\b(tracks|marks|signs|ground|footprints)\b", primary) else primary
    return ActionFrame(operation, objective, matched[0].ref if operation != "survey" else None,
                       methods[operation], tuple(dict.fromkeys(constraints)), recipient, stops[operation])


def execute(engine, frame):
    """Validate the current frame/access, then use the owning engine transaction."""
    methods = {"survey": ("local_scan", "leads"), "examine": ("inspect_evidence", "finding"),
               "ask": ("question_actor", "reply"), "report": ("relay_finding", "receipt")}
    if not isinstance(frame, ActionFrame) or not isinstance(frame.operation, str) or frame.operation not in methods or not isinstance(frame.objective, str) or not frame.objective.strip():
        return _result("unavailable", "Unsupported investigation frame; no effects have been applied.")
    if (frame.method, frame.stop_boundary) != methods[frame.operation] or not isinstance(frame.constraints, tuple) or any(
            not isinstance(c, str) or c not in {"local_only", "no_questioning", "no_following"} and not c.startswith("exclude:") for c in frame.constraints):
        return _result("unavailable", "Unsupported method, restriction or stopping boundary; no effects have been applied.")
    policy, focus = engine._investigation_policy, engine._investigation_focus
    declared = {d["discovery_id"] for d in engine.region.get("discovery_declarations", [])}
    if any(c.startswith("exclude:") and c[8:] not in declared for c in frame.constraints):
        return _result("unavailable", "That information restriction has no supported subject; no effects have been applied.")
    history_count = len(engine.get_history())
    if frame.operation == "survey":
        if frame.target_ref is not None or frame.recipient_ref is not None:
            return _result("unavailable", "A local survey does not authorize another target or recipient.")
        candidates = [c for c in policy.candidates(engine)
            if "exclude:" + (c.finding_id or c.ref) not in frame.constraints
            and not (c.kind == "actor" and ("no_questioning" in frame.constraints or frame.objective == "signs"))]
        message = "\n".join(c.cue for c in candidates) or "No supported accessible leads are apparent within this local inquiry."
        result = _result("survey", message, frame=frame)
        focus.remember(engine, frame, [c.ref for c in candidates], [])
        return result
    if frame.operation != "report" and frame.recipient_ref is not None:
        return _result("unavailable", "This inquiry does not authorize a report recipient.")
    if frame.operation == "ask" and "no_questioning" in frame.constraints:
        return _result("unavailable", "Questioning is excluded; no conversation has occurred.")
    candidates = policy.findings(engine) if frame.operation == "report" else policy.candidates(engine)
    candidate = next((c for c in candidates if c.ref == frame.target_ref), None)
    kind = {"examine": "evidence", "ask": "actor", "report": "finding"}[frame.operation]
    if candidate is None or candidate.kind != kind:
        return _result("unavailable", "That selected subject is not accessible for this action now.")
    if "exclude:" + (candidate.finding_id or candidate.ref) in frame.constraints:
        return _result("unavailable", "The selected subject conflicts with your information restriction; no effects have been applied.")
    if frame.operation == "examine":
        accepted = engine.investigate(discovery_id=candidate.finding_id)
        if accepted["text"] is None:
            return _result("unavailable", "The selected evidence cannot yield that finding here.")
        result = _result("accepted" if accepted["changed"] else "already_acquired", accepted["text"],
                         frame=frame, changed=accepted["changed"], findings=[candidate.finding_id])
    elif frame.operation == "ask":
        accepted = policy.ask(engine, candidate)
        if accepted is None:
            return _result("unavailable", "No supported reply is available for that subject.")
        result = _result("accepted", accepted["message"], frame=frame,
                         changed=len(engine.get_history()) > history_count, findings=[candidate.finding_id])
    else:
        recipient = next((a for a in policy.recipients(engine) if a["entity_id"] == frame.recipient_ref), None)
        if recipient is None or "exclude:" + candidate.ref in frame.constraints:
            return _result("unavailable", "The selected report or recipient is not authorized here.")
        accepted = engine.present_clue(candidate.label, recipient["name"])
        if not accepted.get("response_text"):
            return _result("unavailable", "That finding cannot be shared with this recipient here.")
        result = _result("accepted", accepted["response_text"], frame=frame, changed=accepted["changed"], findings=[candidate.finding_id])
    events = engine.get_history()[history_count:]
    focus.remember(engine, frame, [candidate.finding_id or candidate.ref], [e["history_id"] for e in events])
    return result


def process(engine, raw=None, *, frame=None):
    proposal = frame if frame is not None else interpret(raw, engine)
    if proposal is None or isinstance(proposal, dict):
        return proposal
    if isinstance(proposal, str):
        focus = engine._investigation_focus
        if proposal in {"cancel investigation", "finish investigation"}:
            focus.clear()
            return _result("control", "You end the local investigation focus. Accepted findings and reports remain unchanged.")
        record = focus.snapshot()
        current = {c.ref for c in engine._investigation_policy.candidates(engine)} | {c.ref for c in engine._investigation_policy.findings(engine)}
        if not record or not set(record["references"]) & current:
            return _result("unavailable", "No current investigation subject can be resumed; choose a fresh inquiry.")
        # Resuming focus does not execute an action or restore authority from a cache.
        focus._record["status"] = "active"
        focus._record["scope_location"] = engine.get_world_state()["player"]["current_location_id"]
        return _result("control", "You resume the investigation focus using current circumstances. Choose your next action.")
    return execute(engine, proposal)