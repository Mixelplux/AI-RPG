from copy import deepcopy
from typing import Any, Dict

from engine.pressure_state import (
    build_initial_pressure_state,
    validate_pressure_state,
)
from engine.actor_knowledge import (
    build_initial_actor_knowledge,
    validate_actor_knowledge,
)
from engine.evidence_traces import validate_evidence_traces
from engine import west_road_predicament as west_road
from engine import character_competence
from engine.unresolved_threads import (
    validate_open_threads,
    validate_open_thread_integrity,
    validate_resolved_thread_integrity,
)


DEFAULT_HISTORY_QUERY_COUNT = 10
HISTORY_ID_PREFIX = "history_"


def create_initial_world_state(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create the initial persistent World State.
    """

    locations = region.get("locations", [])

    if not locations:
        raise ValueError("Region Pack has no locations.")

    starting_location_id = locations[0].get("location_id")

    if not starting_location_id:
        raise ValueError("First location is missing location_id.")

    region_state = region.get("region_state", {})
    initial_weather = region_state.get("weather")

    if initial_weather is None:
        raise ValueError("Region Pack is missing initial weather in region_state.weather.")

    initial_time = region.get("time")

    if initial_time is None:
        raise ValueError("Region Pack is missing initial time in time.")

    state = {
        "player": {
            "current_location_id": starting_location_id,
            "competences": [],
        },
        "weather": deepcopy(initial_weather),
        "time": deepcopy(initial_time),
        "history": [],
        "pressures": build_initial_pressure_state(region),
        "actor_location_overrides": {},
        "open_threads": {},
        "resolved_threads": {},
        "actor_knowledge": build_initial_actor_knowledge(region),
        "evidence_traces": [],
        "player_discoveries": [],
        "competence_attempts": {},
    }
    if west_road.enabled(region):
        state["west_road_predicament"] = west_road.initial_record()
        clue = next(d for d in region["discovery_declarations"] if d["discovery_id"] == "west_road_tracks")
        state["evidence_traces"].append({"trace_id": clue["trace_id"], "evidence_id": clue["discovery_id"], "location_id": clue["location_id"]})
    return state


def validate_world_state(
    world_state: Dict[str, Any],
    region: Dict[str, Any] | None = None,
) -> None:
    """
    Validate the minimum required World State shape for runtime use.
    """

    if not isinstance(world_state, dict):
        raise ValueError("World State must be a dictionary.")

    if region is not None and west_road.enabled(region) and "west_road_predicament" not in world_state:
        raise ValueError(west_road.OLD_SAVE_MESSAGE)

    if "player" not in world_state:
        raise ValueError("World State is missing player.")

    if "current_location_id" not in world_state["player"]:
        raise ValueError("World State player is missing current_location_id.")

    if "weather" not in world_state:
        raise ValueError("World State is missing weather.")

    if "time" not in world_state:
        raise ValueError("World State is missing time.")

    if "pressures" not in world_state:
        raise ValueError("World State is missing pressures.")

    if "open_threads" not in world_state:
        raise ValueError("World State is missing open_threads.")
    if "resolved_threads" not in world_state:
        raise ValueError("World State is missing resolved_threads.")
    if "actor_knowledge" not in world_state:
        raise ValueError("World State is missing actor_knowledge.")
    if "evidence_traces" not in world_state:
        raise ValueError("World State is missing evidence_traces.")
    if "player_discoveries" not in world_state:
        raise ValueError("World State is missing player_discoveries.")
    discoveries = world_state["player_discoveries"]
    if (not isinstance(discoveries, list) or any(not isinstance(item, str) or not item for item in discoveries)
            or len(set(discoveries)) != len(discoveries)):
        raise ValueError("World State player_discoveries must be unique non-empty strings.")
    if region is not None:
        declaration_ids = {
            item.get("discovery_id")
            for item in region.get("discovery_declarations", [])
            if isinstance(item, dict)
        }
        if any(item not in declaration_ids for item in discoveries):
            raise ValueError("World State player_discoveries contains an unknown discovery_id.")

    validate_pressure_state(world_state["pressures"])
    validate_open_threads(world_state["open_threads"])
    if not isinstance(world_state["resolved_threads"], dict):
        raise ValueError("World State resolved_threads must be a dictionary.")
    for thread_id, record in world_state["resolved_threads"].items():
        if (not isinstance(thread_id, str) or not thread_id or not isinstance(record, dict)
                or set(record) != {"thread_id", "status", "resolved_by_history_id"}
                or record["thread_id"] != thread_id or record["status"] != "resolved"
                or not isinstance(record["resolved_by_history_id"], str) or not record["resolved_by_history_id"]):
            raise ValueError("World State resolved_threads records are invalid.")
    if set(world_state["open_threads"]) & set(world_state["resolved_threads"]):
        raise ValueError("A thread cannot be both open and resolved.")
    validate_actor_knowledge(world_state["actor_knowledge"], region)
    validate_evidence_traces(world_state["evidence_traces"], region)

    overrides = world_state.get("actor_location_overrides", {})
    if not isinstance(overrides, dict):
        raise ValueError("World State actor_location_overrides must be a dictionary.")
    for entity_id, location_id in overrides.items():
        if not isinstance(entity_id, str) or not entity_id:
            raise ValueError("Actor override entity_id must be a non-empty string.")
        if not isinstance(location_id, str) or not location_id:
            raise ValueError("Actor override location_id must be a non-empty string.")

    if region is not None:
        actors = {
            entity["entity_id"]: entity
            for entity in region.get("entities", [])
            if isinstance(entity, dict) and entity.get("persistence") == "static"
        }
        location_ids = {
            location.get("location_id")
            for location in region.get("locations", [])
            if isinstance(location, dict)
        }
        for entity_id, location_id in overrides.items():
            if entity_id not in actors:
                raise ValueError(f"Unknown static actor override: {entity_id}.")
            if location_id not in location_ids:
                raise ValueError(f"Unknown actor override destination: {location_id}.")
            if location_id == actors[entity_id]["location"]:
                raise ValueError(f"Redundant baseline actor override: {entity_id}.")

    if "history" in world_state and not isinstance(
        world_state["history"],
        list
    ):
        raise ValueError("World State history must be a list.")

    if "history" in world_state:
        validate_history_entry_ids(world_state["history"])
        history_ids = {
            entry["history_id"] for entry in world_state["history"]
        }
        for thread in world_state["open_threads"].values():
            if thread["created_by_history_id"] not in history_ids:
                raise ValueError("Open thread source history id is unknown.")
        for thread in world_state["resolved_threads"].values():
            if thread["resolved_by_history_id"] not in history_ids:
                raise ValueError("Resolved thread history id is unknown.")
    if region is not None:
        validate_open_thread_integrity(world_state, region)
        validate_resolved_thread_integrity(world_state, region)
        west_road.validate_state(world_state, region)
    character_competence.validate_state(world_state, region)


def copy_world_state(world_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a defensive copy of World State.
    """

    validate_world_state(world_state)
    return deepcopy(world_state)


def get_static_actor(region: Dict[str, Any], entity_id: str) -> Dict[str, Any]:
    if not isinstance(entity_id, str) or not entity_id:
        raise ValueError("entity_id must be a non-empty string.")
    matches = [
        entity for entity in region.get("entities", [])
        if isinstance(entity, dict)
        and entity.get("persistence") == "static"
        and entity.get("entity_id") == entity_id
    ]
    if len(matches) != 1:
        raise ValueError("Unknown supported static actor entity_id.")
    return deepcopy(matches[0])


def get_effective_actor_location(
    region: Dict[str, Any], world_state: Dict[str, Any], entity_id: str
) -> str:
    actor = get_static_actor(region, entity_id)
    return world_state.get("actor_location_overrides", {}).get(
        entity_id, actor["location"]
    )


def get_player_location_id(world_state: Dict[str, Any]) -> str:
    return world_state["player"]["current_location_id"]


def set_player_location_id(
    world_state: Dict[str, Any],
    location_id: str
) -> Dict[str, Any]:
    updated_world_state = deepcopy(world_state)
    updated_world_state["player"]["current_location_id"] = location_id

    return updated_world_state


def get_weather(world_state: Dict[str, Any]) -> Dict[str, Any]:
    return world_state["weather"]


def get_time(world_state: Dict[str, Any]) -> Dict[str, Any]:
    return world_state["time"]


def set_time(
    world_state: Dict[str, Any],
    time: Dict[str, Any]
) -> Dict[str, Any]:
    updated_world_state = deepcopy(world_state)
    updated_world_state["time"] = deepcopy(time)

    return updated_world_state


def get_history(world_state: Dict[str, Any]) -> list[Dict[str, Any]]:
    return deepcopy(world_state.get("history", []))


def validate_history_entry_ids(history: list[Dict[str, Any]]) -> None:
    seen_ids = set()

    for entry in history:
        if not isinstance(entry, dict):
            raise ValueError("World State history entries must be dictionaries.")

        if "source_history_id" in entry:
            source_history_id = entry["source_history_id"]
            if not isinstance(source_history_id, str) or not source_history_id:
                raise ValueError(
                    "World State source_history_id must be a non-empty string."
                )
            if source_history_id not in seen_ids:
                raise ValueError(
                    "World State source_history_id must reference an earlier "
                    "history entry."
                )

        if "history_id" not in entry:
            continue

        history_id = entry["history_id"]

        if not isinstance(history_id, str) or not history_id:
            raise ValueError("World State history_id must be a non-empty string.")

        if history_id in seen_ids:
            raise ValueError("World State history_id values must be unique.")

        seen_ids.add(history_id)


def get_history_entry_by_id(
    world_state: Dict[str, Any],
    history_id: str
) -> Dict[str, Any] | None:
    for entry in get_history(world_state):
        if entry.get("history_id") == history_id:
            return entry

    return None


def query_history(
    world_state: Dict[str, Any],
    count: int | None = None,
    event_type: str | None = None,
    location: str | None = None
) -> list[Dict[str, Any]]:
    if count is None:
        count = DEFAULT_HISTORY_QUERY_COUNT

    if count is not None and count < 0:
        raise ValueError("History query count must not be negative.")

    history = get_history(world_state)

    if event_type is not None:
        history = [
            entry for entry in history
            if entry.get("event_type") == event_type
        ]

    if location is not None:
        history = [
            entry for entry in history
            if entry.get("location") == location
        ]

    history = history[-count:] if count else []

    return history


def add_history_entry(
    world_state: Dict[str, Any],
    event_type: str,
    summary: str,
    location: str | None = None,
    time: Dict[str, Any] | None = None,
    extra: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    updated_world_state = deepcopy(world_state)
    history = updated_world_state.setdefault("history", [])

    if extra and "history_id" in extra:
        raise ValueError("History entry identifiers are engine-owned.")

    entry: Dict[str, Any] = {
        "history_id": build_next_history_id(history),
        "event_type": event_type,
        "summary": summary
    }

    if location is not None:
        entry["location"] = location

    if time is not None:
        entry["time"] = deepcopy(time)

    if extra:
        entry.update(deepcopy(extra))

    history.append(entry)

    return updated_world_state


def build_next_history_id(history: list[Dict[str, Any]]) -> str:
    used_ids = {
        entry.get("history_id")
        for entry in history
        if isinstance(entry, dict) and entry.get("history_id") is not None
    }
    max_sequence = 0

    for history_id in used_ids:
        sequence = parse_history_id_sequence(history_id)

        if sequence is not None:
            max_sequence = max(max_sequence, sequence)

    next_sequence = max_sequence + 1

    while True:
        candidate = format_history_id(next_sequence)

        if candidate not in used_ids:
            return candidate

        next_sequence += 1


def format_history_id(sequence: int) -> str:
    return f"{HISTORY_ID_PREFIX}{sequence:06d}"


def parse_history_id_sequence(history_id: Any) -> int | None:
    if not isinstance(history_id, str):
        return None

    if not history_id.startswith(HISTORY_ID_PREFIX):
        return None

    suffix = history_id[len(HISTORY_ID_PREFIX):]

    if not suffix.isdigit():
        return None

    return int(suffix)
