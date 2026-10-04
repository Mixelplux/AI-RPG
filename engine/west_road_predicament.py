"""The fixed Bryn Shander reference predicament; not a situation framework."""

from copy import deepcopy

GREY = "captain_darvin_grey"
ELIN = "guard_elin_voss"
MERCHANT = "merchant_mara"
GATE = "bryn_shander_gate_north"
ROAD = "outside_trade_road_west"
INITIAL_EVIDENCE = ("west_road_tracks", "west_road_merchant_account")
COMMANDS = {
    "advocate patrol": ("investigating", "observers_withdrew"),
    "continue investigation": ("investigating", "wagon_intercepted"),
    "pursue observers": ("observers_withdrew", "withdrawal_route_found"),
    "restore coverage": ("observers_withdrew", "coverage_restored"),
    "protect supply stop": ("wagon_intercepted", "supply_stop_protected"),
    "locate raiders": ("wagon_intercepted", "raider_staging_area_found"),
}
PHASES = {"investigating"} | {target for _, target in COMMANDS.values()}
PHASE_DISCOVERIES = {
    "observers_withdrew": (),
    "wagon_intercepted": ("west_road_patrol_signs", "west_road_driver_account"),
    "withdrawal_route_found": ("west_road_withdrawal_route",),
    "coverage_restored": (),
    "supply_stop_protected": (),
    "raider_staging_area_found": ("west_road_staging_area",),
}
OLD_SAVE_MESSAGE = (
    "This save uses the previous Bryn Shander prototype situation. Start a new "
    "game to play the revised west-road predicament. Your save file has not been changed."
)


def enabled(region):
    return "west_road_predicament" in region


def shared_id(discovery_id):
    return "west_road_received:" + discovery_id


def validate_content(region):
    if not enabled(region):
        return
    content = region["west_road_predicament"]
    if not isinstance(content, dict) or set(content) != {"premise", "phase_text", "actor_responses"}:
        raise ValueError("West-road authored content fields are invalid.")
    if not isinstance(content["premise"], str) or not content["premise"].strip():
        raise ValueError("West-road premise is required.")
    texts = content["phase_text"]
    responses = content["actor_responses"]
    if not isinstance(texts, dict) or set(texts) != PHASES:
        raise ValueError("West-road phase text is incomplete.")
    if not isinstance(responses, dict) or set(responses) != {GREY, ELIN}:
        raise ValueError("West-road actor responses are incomplete.")
    for actor_text in responses.values():
        if not isinstance(actor_text, dict) or set(actor_text) != PHASES:
            raise ValueError("West-road actor phase responses are incomplete.")
    evidence = region.get("west_road_competence_evidence")
    if not isinstance(evidence, dict) or set(evidence) != {"observation", "tactical_assessment", "outdoor_tracking", "surveillance_analysis"} or any(not isinstance(t, str) or not t.strip() for t in evidence.values()):
        raise ValueError("West-road competence evidence is incomplete.")
    if any(not isinstance(t, str) or not t.strip() for t in list(texts.values()) + [t for v in responses.values() for t in v.values()]):
        raise ValueError("West-road authored text must be nonempty.")
    actors = {a["entity_id"]: a for a in region["entities"] if a.get("persistence") == "static"}
    if not {GREY, ELIN, MERCHANT} <= actors.keys() or any(actors[a]["location"] != GATE for a in (GREY, ELIN)) or actors[MERCHANT]["location"] != ROAD:
        raise ValueError("West-road reference actors must be at their authored locations.")
    discoveries = {d["discovery_id"] for d in region.get("discovery_declarations", [])}
    required = set(INITIAL_EVIDENCE) | {d for ds in PHASE_DISCOVERIES.values() for d in ds} | {"west_road_sign_direction", "west_road_observation_overlap"}
    if not required <= discoveries:
        raise ValueError("West-road discoveries are incomplete.")


def initial_record():
    return {"phase": "investigating", "last_outcome_history_id": None}


def validate_state(world, region):
    if not enabled(region):
        return
    if "west_road_predicament" not in world:
        raise ValueError(OLD_SAVE_MESSAGE)
    record = world["west_road_predicament"]
    if not isinstance(record, dict) or set(record) != {"phase", "last_outcome_history_id"} or not isinstance(record["phase"], str) or record["phase"] not in PHASES:
        raise ValueError("West-road current phase is invalid.")
    phase = record["phase"]
    events = world.get("history", [])
    decisions = [e for e in events if e.get("event_type") == "west_road_commitment"]
    outcomes = [e for e in events if e.get("event_type") == "west_road_outcome"]
    if phase == "investigating":
        if record["last_outcome_history_id"] is not None or decisions or outcomes:
            raise ValueError("Uncommitted west-road state has outcome history.")
        expected_commands = []
    else:
        command = next(c for c, (_, target) in COMMANDS.items() if target == phase)
        source_phase = COMMANDS[command][0]
        expected_commands = [command] if source_phase == "investigating" else ["advocate patrol" if source_phase == "observers_withdrew" else "continue investigation", command]
        if len(decisions) != len(expected_commands) or len(outcomes) != len(expected_commands):
            raise ValueError("West-road commitment/outcome count is inconsistent.")
        indexes = {e.get("history_id"): i for i, e in enumerate(events)}
        for index, (decision, outcome, expected) in enumerate(zip(decisions, outcomes, expected_commands)):
            before, after = COMMANDS[expected]
            if decision.get("command") != expected or decision.get("from_phase") != before or outcome.get("phase") != after or outcome.get("source_history_id") != decision.get("history_id") or outcome.get("witness_entity_ids") != [GREY, ELIN]:
                raise ValueError("West-road causal outcome is inconsistent.")
            if indexes[decision["history_id"]] >= indexes[outcome["history_id"]] or (index and indexes[outcomes[index - 1]["history_id"]] >= indexes[decision["history_id"]]):
                raise ValueError("West-road causal ordering is inconsistent.")
            timed = expected in ("advocate patrol", "continue investigation")
            time_id = outcome.get("time_history_id")
            time_event = next((e for e in events if e.get("history_id") == time_id), None)
            if timed:
                if time_event is None or time_event.get("event_type") != "time_advanced" or time_event.get("source_history_id") != decision["history_id"]:
                    raise ValueError("West-road timed outcome is inconsistent.")
                previous = time_event.get("previous_time")
                current = time_event.get("new_time")
                if not isinstance(previous, dict) or not isinstance(current, dict):
                    raise ValueError("West-road time records are invalid.")
                previous_hours, current_hours = previous.get("elapsed_hours", 0), current.get("elapsed_hours")
                if type(previous_hours) is not int or type(current_hours) is not int or current_hours - previous_hours != 1 or not indexes[decision["history_id"]] < indexes[time_id] < indexes[outcome["history_id"]]:
                    raise ValueError("West-road timed outcome is inconsistent.")
            if not timed and time_id is not None:
                raise ValueError("West-road follow-up unexpectedly advanced time.")
        if record["last_outcome_history_id"] != outcomes[-1]["history_id"] or outcomes[-1]["phase"] != phase:
            raise ValueError("West-road current outcome reference is inconsistent.")
        if not set(INITIAL_EVIDENCE) <= set(world["player_discoveries"]) or not {shared_id(d) for d in INITIAL_EVIDENCE} <= set(world["actor_knowledge"].get(ELIN, [])):
            raise ValueError("West-road commitment lacks shared initial evidence.")
    permitted = set(INITIAL_EVIDENCE)
    for command in expected_commands:
        permitted.update(PHASE_DISCOVERIES[COMMANDS[command][1]])
    scenario_discoveries = set(INITIAL_EVIDENCE) | {d for ds in PHASE_DISCOVERIES.values() for d in ds}
    acquired = set(world["player_discoveries"]) & scenario_discoveries
    if not acquired <= permitted or not (permitted - set(INITIAL_EVIDENCE)) <= acquired:
        raise ValueError("West-road phase/discoveries are inconsistent.")
    traces = {t["trace_id"]: t for t in world["evidence_traces"]}
    for d in region["discovery_declarations"]:
        expected_trace = {"trace_id": d["trace_id"], "evidence_id": d["discovery_id"], "location_id": d["location_id"]}
        if d["discovery_id"] in acquired and traces.get(d["trace_id"]) != expected_trace:
            raise ValueError("West-road discovery lacks its evidence.")
    for actor in (GREY, ELIN):
        for membership in world["actor_knowledge"].get(actor, []):
            if membership.startswith("west_road_received:"):
                discovery = membership.split(":", 1)[1]
                if discovery not in world["player_discoveries"] or not any(e.get("event_type") == "west_road_evidence_shared" and e.get("actor_id") == actor and e.get("discovery_id") == discovery for e in events):
                    raise ValueError("West-road actor information was not shared.")


def available_commands(world, scene):
    phase = world["west_road_predicament"]["phase"]
    if world["player"]["current_location_id"] != GATE or not {GREY, ELIN} <= set(scene["entities"]["static"]):
        return []
    if phase == "investigating" and (not set(INITIAL_EVIDENCE) <= set(world["player_discoveries"]) or not {shared_id(d) for d in INITIAL_EVIDENCE} <= set(world["actor_knowledge"].get(ELIN, []))):
        return []
    return [c for c, (before, _) in COMMANDS.items() if before == phase]


def actor_response(region, world, actor_id):
    if actor_id not in (GREY, ELIN):
        return None
    phase = world["west_road_predicament"]["phase"]
    if phase != "investigating":
        outcome = next(e for e in world["history"] if e["history_id"] == world["west_road_predicament"]["last_outcome_history_id"])
        if actor_id not in outcome["witness_entity_ids"]:
            return None
    return {"text": region["west_road_predicament"]["actor_responses"][actor_id][phase]}


def summary(region, world):
    """One continuity paragraph; the following scene supplies local detail."""
    phase = world["west_road_predicament"]["phase"]
    if phase == "investigating":
        discoveries = set(world["player_discoveries"])
        received = set(world["actor_knowledge"].get(ELIN, []))
        evidence = [(INITIAL_EVIDENCE[0], "the tracks"), (INITIAL_EVIDENCE[1], "Mara's account")]
        found = [label for discovery, label in evidence if discovery in discoveries]
        reported = [label for discovery, label in evidence if shared_id(discovery) in received]
        lines = ["You were investigating reports that west-road travelers were being watched."]
        if found:
            lines.append("You gathered " + " and ".join(found) + ".")
        if reported:
            lines.append("You reported " + " and ".join(reported) + " to Elin.")
        if len(found) < 2:
            missing = [label for discovery, label in evidence if discovery not in discoveries]
            lines.append("You still need " + " and ".join(missing) + ".")
        elif len(reported) < 2:
            missing = [label for discovery, label in evidence if shared_id(discovery) not in received]
            lines.append("Report " + " and ".join(missing) + " to Elin before choosing a response.")
        else:
            lines.append("Decide whether to push for an immediate patrol or continue investigating.")
        text = " ".join(lines)
        if len(found) == 2 and len(reported) == 2:
            text = "You found signs that west-road travelers were being watched and reported the tracks and Mara's account to Elin. Decide whether to push for an immediate patrol or continue investigating."
    else:
        text = {
            "observers_withdrew": "You advocated immediate patrol action. The observers withdrew, leaving fresh signs. Decide whether to pursue them or restore normal coverage.",
            "wagon_intercepted": "You chose one more hour of investigation. Another wagon was intercepted, revealing a threatened supply stop. Decide whether to protect it or search for the raiders.",
            "withdrawal_route_found": "You advocated immediate patrol action, then followed the observers' withdrawal route. Nobody was captured, and patrol coverage remains extended. The broader threat remains unresolved.",
            "coverage_restored": "You advocated immediate patrol action. After the observers withdrew, you restored normal coverage rather than following them. The broader threat remains unresolved.",
            "supply_stop_protected": "You chose one more hour of investigation. After another wagon was intercepted, you protected the threatened supply stop. Its next departure is held safely; the raiders remain unlocated.",
            "raider_staging_area_found": "You chose one more hour of investigation, then searched for the raiders and found a likely staging area. There was no confrontation; the supply stop still lacks dedicated protection.",
        }[phase]
    return ["Previously: " + text]
