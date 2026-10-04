"""One fixed market incident caused by West-Road guard allocation and time."""

from copy import deepcopy

from engine import west_road_predicament as west

STATE_KEY = "west_road_market_theft"
EVENT_TYPE = "market_approach_theft"
MARKET = "market_square"
THRESHOLD_HOURS = 2
REDUCED_PHASES = frozenset({"observers_withdrew", "withdrawal_route_found"})
INCIDENT_SUMMARY = "A crate of lamp oil was stolen from a teamster's supply sled at the market approach."
INCIDENT_TEXT = (
    "At the market approach, a teamster argues with one of Grey's watchmen "
    "beside a half-unloaded supply sled. One of the rear lashings has been cut; "
    "a crate of lamp oil is gone. The watchman says the usual patrol was thin "
    "while extra guards were tied up along the western road. "
    "Nobody here saw who took the crate."
)
NARRATION_LIMIT = (
    "The market theft is an independent incident. Its thief and motive are "
    "unknown. Do not connect it to the West-Road observers, their faction, "
    "or a conspiracy, and do not invent a quest or obligation from it."
)


def reduced_coverage(world):
    if "west_road_predicament" not in world:
        return False
    allocation = world["west_road_predicament"]
    if not isinstance(allocation, dict) or not isinstance(allocation.get("phase"), str):
        raise ValueError("West-Road guard allocation is invalid.")
    return allocation["phase"] in REDUCED_PHASES


def _elapsed_hours(world):
    time = world.get("time")
    if not isinstance(time, dict):
        raise ValueError("Market theft requires a valid elapsed-time record.")
    elapsed = time.get("elapsed_hours", 0)
    if type(elapsed) is not int or elapsed < 0:
        raise ValueError("Market theft requires nonnegative integer elapsed time.")
    return elapsed


def initial_record():
    return {"coverage_started_elapsed_hours": None, "theft_history_id": None}


def normalize_loaded_state(world):
    """Only a copied legacy payload may acquire missing additive timing state.

    Old saves did not record this condition's duration. Start monitoring an
    already-reduced allocation at saved time; never replay time on load.
    """
    if "west_road_predicament" in world and STATE_KEY not in world:
        history = world.get("history", [])
        if not isinstance(history, list) or any(not isinstance(e, dict) for e in history):
            raise ValueError("World State history must be a list of objects.")
        elapsed = _elapsed_hours(world)
        reduced = reduced_coverage(world)
        if any(e.get("event_type") == EVENT_TYPE for e in history):
            raise ValueError("Market theft history is missing its persistent record.")
        world[STATE_KEY] = initial_record()
        if reduced:
            world[STATE_KEY]["coverage_started_elapsed_hours"] = elapsed


def allocation_changed(candidate, was_reduced):
    """Called when the existing guard-allocation outcome is established."""
    record = candidate[STATE_KEY]
    if not reduced_coverage(candidate):
        record["coverage_started_elapsed_hours"] = None
    elif not was_reduced:
        record["coverage_started_elapsed_hours"] = candidate["time"].get("elapsed_hours", 0)


def advance_candidate(candidate, previous_time, new_time, time_history_id):
    """Establish truth inside the existing outer time transaction, once."""
    if not reduced_coverage(candidate):
        return candidate
    record = candidate[STATE_KEY]
    start = record["coverage_started_elapsed_hours"]
    if record["theft_history_id"] is not None or start is None:
        return candidate
    threshold = start + THRESHOLD_HOURS
    if previous_time.get("elapsed_hours", 0) < threshold <= new_time["elapsed_hours"]:
        # Import locally: world_state calls this module's validator.
        from engine.world_state import add_history_entry

        occurred_time = {**deepcopy(new_time), "elapsed_hours": threshold}
        candidate = add_history_entry(
            candidate, EVENT_TYPE,
            INCIDENT_SUMMARY,
            MARKET, occurred_time,
            {"source_history_id": time_history_id, "coverage_started_elapsed_hours": start},
        )
        candidate[STATE_KEY]["theft_history_id"] = candidate["history"][-1]["history_id"]
    return candidate


def visible_text(world, location_id):
    """Projection is read-only and local; observation never establishes truth."""
    if location_id == MARKET and world.get(STATE_KEY, {}).get("theft_history_id") is not None:
        return INCIDENT_TEXT
    return None


def validate_state(world, region=None):
    events = world.get("history", [])
    incidents = [e for e in events if e.get("event_type") == EVENT_TYPE]
    if "west_road_predicament" not in world:
        if STATE_KEY in world or incidents:
            raise ValueError("Market theft requires the West-Road predicament.")
        return
    if region is not None and not west.enabled(region):
        raise ValueError("Market theft state requires West-Road content.")
    record = world.get(STATE_KEY)
    if not isinstance(record, dict) or set(record) != {"coverage_started_elapsed_hours", "theft_history_id"}:
        raise ValueError("Market theft record shape is invalid.")
    now = _elapsed_hours(world)
    start, theft_id = record["coverage_started_elapsed_hours"], record["theft_history_id"]
    if reduced_coverage(world):
        patrol = next((e for e in events if e.get("event_type") == "west_road_outcome" and e.get("phase") == "observers_withdrew"), None)
        patrol_time = patrol.get("time") if patrol else None
        patrol_hour = patrol_time.get("elapsed_hours", 0) if isinstance(patrol_time, dict) else None
        if (type(start) is not int or type(patrol_hour) is not int
                or not 0 <= patrol_hour <= start <= now):
            raise ValueError("Reduced guard coverage interval is invalid.")
    elif start is not None:
        raise ValueError("Normal guard coverage cannot retain an active interval.")
    if theft_id is None:
        if incidents or (start is not None and now >= start + THRESHOLD_HOURS):
            raise ValueError("Market theft threshold/history is inconsistent.")
        return
    if not isinstance(theft_id, str) or len(incidents) != 1 or incidents[0].get("history_id") != theft_id:
        raise ValueError("Market theft must reference exactly one incident.")
    incident = incidents[0]
    if set(incident) != {"history_id", "event_type", "summary", "location", "time", "source_history_id", "coverage_started_elapsed_hours"}:
        raise ValueError("Market theft incident fields are invalid.")
    if incident["summary"] != INCIDENT_SUMMARY or not isinstance(incident["time"], dict):
        raise ValueError("Market theft incident facts/time are invalid.")
    positions = {e["history_id"]: i for i, e in enumerate(events)}
    source_id = incident.get("source_history_id")
    if not isinstance(source_id, str) or source_id not in positions or positions[source_id] >= positions[theft_id]:
        raise ValueError("Market theft needs an earlier time transition.")
    source = events[positions[source_id]]
    if not isinstance(source.get("previous_time"), dict) or not isinstance(source.get("new_time"), dict):
        raise ValueError("Market theft time transition is invalid.")
    event_start = incident["coverage_started_elapsed_hours"]
    occurred = incident.get("time", {}).get("elapsed_hours")
    previous = source.get("previous_time", {}).get("elapsed_hours", 0)
    current = source.get("new_time", {}).get("elapsed_hours")
    prior_outcomes = [e for e in events[:positions[source_id]] if e.get("event_type") == "west_road_outcome"]
    patrol = next((e for e in prior_outcomes if e.get("phase") == "observers_withdrew"), None)
    patrol_time = patrol.get("time") if patrol else None
    patrol_hour = patrol_time.get("elapsed_hours", 0) if isinstance(patrol_time, dict) else None
    if (type(event_start) is not int or type(occurred) is not int or type(previous) is not int
            or type(current) is not int or type(patrol_hour) is not int
            or source.get("event_type") != "time_advanced" or incident.get("location") != MARKET
            or incident["time"] != {**source["new_time"], "elapsed_hours": occurred}
            or occurred != event_start + THRESHOLD_HOURS or not 0 <= patrol_hour <= event_start <= previous < occurred <= current <= now
            or not prior_outcomes or prior_outcomes[-1].get("phase") not in REDUCED_PHASES
            or (start is not None and start != event_start)):
        raise ValueError("Market theft lacks a qualifying continuous two-hour interval.")
