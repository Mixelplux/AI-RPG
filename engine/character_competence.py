"""Character competence authority for the fixed West-Road slice only."""
from random import randint

from engine import west_road_predicament as west

TAGS = frozenset({"tactical_assessment", "outdoor_tracking", "surveillance_analysis"})
OPERATIONS = {
    "follow withdrawal signs": ("outdoor_tracking", "west_road_sign_direction"),
    "reconstruct local observation circuit": ("surveillance_analysis", "west_road_observation_overlap"),
    "arrange guarded local survey": ("tactical_assessment", None),
}
LIMIT = "The signs cannot establish identity, affiliation, or an unverified destination. Nobody is captured; the broader threat remains unresolved."


def draw_d6():
    return randint(1, 6)


def resolve(draw, specialist):
    if type(draw) is not int or not 1 <= draw <= 6:
        raise ValueError("West-road draw must be an engine-owned d6 result.")
    if specialist:
        return "partial" if draw <= 2 else "full"
    return "failure" if draw <= 2 else "partial" if draw <= 4 else "full"


def evidence_applicable(region, world):
    if not west.enabled(region) or world.get("west_road_predicament", {}).get("phase") != "observers_withdrew":
        return False
    clue = next(d for d in region["discovery_declarations"] if d["discovery_id"] == "west_road_tracks")
    return "west_road_tracks" in world["player_discoveries"] and {
        "trace_id": clue["trace_id"], "evidence_id": clue["discovery_id"], "location_id": clue["location_id"]
    } in world["evidence_traces"]


def assess(region, world, scene, command):
    """One eligibility/cost decision used by projection and execution."""
    if command not in OPERATIONS:
        return {"eligible": False, "reason": "That competence operation is unsupported; no check is made."}
    tag, _ = OPERATIONS[command]
    specialist = tag in world["player"].get("competences", [])
    cost = 1 if command != "arrange guarded local survey" or specialist else 2
    result = {"eligible": False, "reason": "Fresh withdrawal evidence is not applicable here; no check is made.",
              "specialist": specialist, "cost_hours": cost, "uncertain": command != "arrange guarded local survey"}
    if not evidence_applicable(region, world) or world["player"]["current_location_id"] != west.GATE:
        return result
    # Grey and Elin's existing committed guards are the bounded survey resource.
    if not {west.GREY, west.ELIN} <= set(scene["entities"]["static"]):
        result["reason"] = "Return to Grey and Elin to coordinate the local investigation and report its findings."
        if command == "arrange guarded local survey":
            result["reason"] = "Grey and Elin must be present to arrange the committed guards' survey."
        return result
    if command in world.get("competence_attempts", {}):
        result["reason"] = "This approach already has an accepted outcome."
        return result
    result.update(eligible=True, reason="")
    return result


def project(region, world, scene):
    packet = {"observations": [], "recognition": [], "findings": [], "approaches": [], "accepted_outcomes": [], "limits": [LIMIT, "Narration cannot grant competences or guard resources, invent evidence, repair failure, or convert an uncertain inference into fact."]}
    if not west.enabled(region):
        return packet
    declarations = {d["discovery_id"]: d for d in region["discovery_declarations"]}
    for finding in world["player_discoveries"]:
        if finding in {"west_road_sign_direction", "west_road_observation_overlap", "west_road_withdrawal_route"}:
            packet["findings"].append({"text": declarations[finding]["text"], "status": "supported finding" if finding == "west_road_withdrawal_route" else "limited inference"})
    if evidence_applicable(region, world) and world["player"]["current_location_id"] in (west.GATE, west.ROAD):
        physical = region["west_road_competence_evidence"]
        packet["observations"] = [{"text": physical["observation"], "status": "direct observation" if world["player"]["current_location_id"] == west.ROAD else "guard report"}]
        for tag in world["player"].get("competences", []):
            packet["recognition"].append({"text": physical[tag], "status": "automatic competence; limited interpretation"})
    for command in OPERATIONS:
        decision = assess(region, world, scene, command)
        if decision["eligible"]:
            packet["approaches"].append({"command": command, "cost_hours": decision["cost_hours"], "uncertain": decision["uncertain"], "specialist": decision["specialist"]})
    for command, attempt in world.get("competence_attempts", {}).items():
        packet["accepted_outcomes"].append({"command": command, "result": attempt["result"], "cost_hours": attempt["cost_hours"], "text": outcome_text(region, command, attempt)})
    return packet


def outcome_text(region, command, attempt):
    result = attempt["result"]
    if result == "failure":
        text = "The investigation established no additional finding."
    elif result == "partial":
        finding = OPERATIONS[command][1]
        text = next(d["text"] for d in region["discovery_declarations"] if d["discovery_id"] == finding)
    else:
        text = next(d["text"] for d in region["discovery_declarations"] if d["discovery_id"] == "west_road_withdrawal_route")
    return result.capitalize() + ": " + text + " " + LIMIT


def validate_state(world, region=None):
    tags = world.get("player", {}).get("competences", [])
    if not isinstance(tags, list) or any(not isinstance(t, str) or t not in TAGS for t in tags) or len(tags) != len(set(tags)):
        raise ValueError("Player competences must be unique supported tags.")
    attempts = world.get("competence_attempts", {})
    if not isinstance(attempts, dict):
        raise ValueError("Competence attempts must be a dictionary.")
    events = world.get("history", [])
    by_id = {e.get("history_id"): e for e in events}
    positions = {e.get("history_id"): i for i, e in enumerate(events)}
    fields = {"draw", "result", "specialist", "cost_hours", "findings", "source_history_id", "time_history_id", "outcome_history_id"}
    for command, attempt in attempts.items():
        if command not in OPERATIONS or not isinstance(attempt, dict) or set(attempt) != fields:
            raise ValueError("Competence attempt shape is invalid.")
        uncertain = command != "arrange guarded local survey"
        if type(attempt["specialist"]) is not bool:
            raise ValueError("Competence attempt specialist flag is invalid.")
        if attempt["specialist"] != (OPERATIONS[command][0] in tags):
            raise ValueError("Competence attempt basis disagrees with player competences.")
        expected = resolve(attempt["draw"], attempt["specialist"]) if uncertain else "full"
        cost = 1 if uncertain or attempt["specialist"] else 2
        finding = OPERATIONS[command][1]
        findings = ([] if expected == "failure" else [finding] if expected == "partial" else ["west_road_withdrawal_route"])
        if (not uncertain and attempt["draw"] is not None) or attempt["result"] != expected or type(attempt["cost_hours"]) is not int or attempt["cost_hours"] != cost or attempt["findings"] != findings:
            raise ValueError("Competence attempt resolution is inconsistent.")
        refs = [attempt[k] for k in ("source_history_id", "time_history_id", "outcome_history_id")]
        if any(not isinstance(r, str) or r not in by_id for r in refs) or not positions[refs[0]] < positions[refs[1]] < positions[refs[2]]:
            raise ValueError("Competence causal references are invalid.")
        source, time, outcome = [by_id[r] for r in refs]
        mirrored = outcome.get("attempt")
        if not isinstance(mirrored, dict) or any(type(mirrored.get(k)) is not type(attempt[k]) for k in fields):
            raise ValueError("Competence outcome record types are inconsistent.")
        if (source.get("event_type") != "west_road_competence_attempt" or source.get("command") != command
                or type(source.get("specialist")) is not bool or source.get("specialist") != attempt["specialist"] or source.get("from_phase") != "observers_withdrew"
                or time.get("event_type") != "time_advanced" or time.get("source_history_id") != refs[0]
                or outcome.get("event_type") != "west_road_competence_result" or outcome.get("source_history_id") != refs[0]
                or outcome.get("attempt") != attempt):
            raise ValueError("Competence causal events are inconsistent.")
        previous, current = time.get("previous_time", {}).get("elapsed_hours", 0), time.get("new_time", {}).get("elapsed_hours")
        if type(previous) is not int or type(current) is not int or current - previous != cost:
            raise ValueError("Competence cost/time is inconsistent.")
        if not set(findings) <= set(world["player_discoveries"]):
            raise ValueError("Competence accepted findings are missing.")
        if region is not None:
            if not west.enabled(region):
                raise ValueError("Competence attempts require the West-Road predicament.")
            prior = [e for e in events[:positions[refs[0]]] if e.get("event_type") == "west_road_outcome"]
            if not prior or prior[-1].get("phase") != "observers_withdrew":
                raise ValueError("Competence attempt lacks applicable withdrawal evidence.")
            if source.get("location") != west.GATE or source.get("assistance_entity_ids") != ([west.GREY, west.ELIN] if not uncertain else []):
                raise ValueError("Competence attempt coordination/assistance is inconsistent.")
            for finding_id in findings:
                declaration = next(d for d in region["discovery_declarations"] if d["discovery_id"] == finding_id)
                trace = {"trace_id": declaration["trace_id"], "evidence_id": finding_id, "location_id": declaration["location_id"]}
                if trace not in world["evidence_traces"]:
                    raise ValueError("Competence finding lacks its physical evidence.")
                if expected == "partial" and not any(e.get("event_type") == "player_discovery_added" and e.get("discovery_id") == finding_id and e.get("source_history_id") == refs[0] for e in events[positions[refs[1]]:positions[refs[2]]]):
                    raise ValueError("Competence limited finding lacks its causal source.")
            if expected == "full" and not any(e.get("event_type") == "west_road_commitment" and e.get("command") == "pursue observers" and e.get("source_history_id") == refs[0] for e in events[positions[refs[1]]:positions[refs[2]]]):
                raise ValueError("Competence full result lacks its pursuit continuation.")
    recorded = [e for e in events if e.get("event_type") in ("west_road_competence_attempt", "west_road_competence_result")]
    if len(recorded) != 2 * len(attempts):
        raise ValueError("Competence history/attempt count is inconsistent.")
    for finding in ("west_road_sign_direction", "west_road_observation_overlap"):
        if finding in world.get("player_discoveries", []) and not any(finding in a["findings"] for a in attempts.values()):
            raise ValueError("Competence finding lacks an accepted attempt.")
