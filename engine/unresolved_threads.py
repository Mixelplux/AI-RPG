from copy import deepcopy
from typing import Any

def validate_open_threads(open_threads: Any) -> None:
    if not isinstance(open_threads, dict):
        raise ValueError("World State open_threads must be a dictionary.")
    for thread_id, thread in open_threads.items():
        if not isinstance(thread_id, str) or not thread_id:
            raise ValueError("Open thread id must be a non-empty string.")
        if not isinstance(thread, dict):
            raise ValueError("Open thread record must be a dictionary.")
        required = {"thread_id", "status", "created_by_history_id"}
        if set(thread) != required:
            raise ValueError("Open thread record fields are invalid.")
        if thread["thread_id"] != thread_id:
            raise ValueError("Open thread record identity must match its key.")
        if thread["status"] != "open":
            raise ValueError("Open thread status must be exactly open.")
        if (not isinstance(thread["created_by_history_id"], str)
                or not thread["created_by_history_id"]):
            raise ValueError("Open thread created_by_history_id must be a non-empty string.")


def validate_open_thread_integrity(world_state: dict[str, Any], region: dict[str, Any]) -> None:
    """Validate the one declared open thread against durable causal history."""
    open_threads = world_state["open_threads"]
    validate_open_threads(open_threads)
    declaration = region.get("conversation_unresolved_thread")
    history = world_state.get("history", [])
    history_by_id = {entry.get("history_id"): (index, entry) for index, entry in enumerate(history)}
    openings = [
        (index, entry) for index, entry in enumerate(history)
        if entry.get("event_type") == "unresolved_thread_opened"
    ]
    for thread_id, thread in open_threads.items():
        if declaration is None or declaration.get("thread_id") != thread_id:
            raise ValueError("Open thread must match the active Region Pack declaration.")
        source = history_by_id.get(thread["created_by_history_id"])
        if source is None:
            raise ValueError("Open thread source history id is unknown.")
        source_index, source_entry = source
        if (source_entry.get("event_type") != "player_conversation"
                or source_entry.get("target_entity_id") != declaration["trigger_entity_id"]):
            raise ValueError("Open thread source must be its declared triggering conversation.")
        matching = [
            (index, entry) for index, entry in openings
            if entry.get("thread_id") == thread_id
        ]
        if len(matching) != 1:
            raise ValueError("Open thread must have exactly one opening lifecycle record.")
        opening_index, opening = matching[0]
        if (opening.get("status") != "open"
                or opening.get("source_history_id") != thread["created_by_history_id"]
                or opening_index <= source_index):
            raise ValueError("Open thread lifecycle record is causally inconsistent.")
    resolved_threads = world_state.get("resolved_threads", {})
    for _, opening in openings:
        thread_id = opening.get("thread_id")
        if thread_id not in open_threads and thread_id not in resolved_threads:
            raise ValueError("Opening lifecycle record has no persisted thread state.")


def validate_resolved_thread_integrity(world_state: dict[str, Any], region: dict[str, Any]) -> None:
    """Validate resolved state against its declared presentation lifecycle."""

    resolved_threads = world_state["resolved_threads"]
    declaration = region.get("conversation_discovery_resolution")
    history = world_state.get("history", [])
    history_by_id = {
        entry.get("history_id"): (index, entry)
        for index, entry in enumerate(history)
    }
    openings = [
        (index, entry)
        for index, entry in enumerate(history)
        if entry.get("event_type") == "unresolved_thread_opened"
    ]
    resolutions = [
        (index, entry)
        for index, entry in enumerate(history)
        if entry.get("event_type") == "unresolved_thread_resolved"
    ]

    for thread_id, thread in resolved_threads.items():
        if declaration is None or declaration.get("required_thread_id") != thread_id:
            raise ValueError("Resolved thread must match the active Region Pack declaration.")

        presentation = history_by_id.get(thread["resolved_by_history_id"])
        if presentation is None:
            raise ValueError("Resolved thread presentation history id is unknown.")
        presentation_index, presentation_entry = presentation
        if (
            presentation_entry.get("event_type") != "clue_presented"
            or presentation_entry.get("target_entity_id") != declaration["target_entity_id"]
        ):
            raise ValueError("Resolved thread source must be its declared clue presentation.")

        matching_openings = [
            (index, entry)
            for index, entry in openings
            if entry.get("thread_id") == thread_id
        ]
        if len(matching_openings) != 1:
            raise ValueError("Resolved thread must have exactly one opening lifecycle record.")
        opening_index, opening = matching_openings[0]
        opening_source = history_by_id.get(opening.get("source_history_id"))
        if opening_source is None:
            raise ValueError("Resolved thread opening source history id is unknown.")
        opening_source_index, opening_source_entry = opening_source
        unresolved_declaration = region.get("conversation_unresolved_thread")
        if (
            opening.get("status") != "open"
            or unresolved_declaration is None
            or unresolved_declaration.get("thread_id") != thread_id
            or opening_source_entry.get("event_type") != "player_conversation"
            or opening_source_entry.get("target_entity_id")
            != unresolved_declaration["trigger_entity_id"]
            or not (opening_source_index < opening_index < presentation_index)
        ):
            raise ValueError("Resolved thread opening lifecycle record is causally inconsistent.")

        matching_resolutions = [
            (index, entry)
            for index, entry in resolutions
            if entry.get("thread_id") == thread_id
        ]
        if len(matching_resolutions) != 1:
            raise ValueError("Resolved thread must have exactly one resolution lifecycle record.")
        resolution_index, resolution = matching_resolutions[0]
        if (
            resolution.get("status") != "resolved"
            or resolution.get("source_history_id") != thread["resolved_by_history_id"]
            or resolution_index <= presentation_index
        ):
            raise ValueError("Resolved thread lifecycle record is causally inconsistent.")

    for _, resolution in resolutions:
        thread_id = resolution.get("thread_id")
        if thread_id not in resolved_threads:
            raise ValueError("Resolution lifecycle record has no persisted resolved state.")


def get_open_threads(world_state: dict[str, Any]) -> dict[str, dict[str, str]]:
    validate_open_threads(world_state["open_threads"])
    return deepcopy(world_state["open_threads"])


def prepare_open_thread_candidate(
    candidate_world_state: dict[str, Any],
    declaration: dict[str, Any],
    source_history_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    from engine.world_state import add_history_entry

    thread_id = declaration["thread_id"]
    open_threads = candidate_world_state["open_threads"]
    validate_open_threads(open_threads)
    resolved_threads = candidate_world_state.get("resolved_threads", {})
    if thread_id in resolved_threads:
        return candidate_world_state, {
            "thread_id": thread_id,
            "changed": False,
            "status": "resolved",
            "history_id": None,
            "source_history_id": source_history_id,
        }
    if thread_id in open_threads:
        return candidate_world_state, {
            "thread_id": thread_id,
            "changed": False,
            "status": "open",
            "history_id": None,
            "source_history_id": source_history_id,
        }

    candidate_world_state["open_threads"] = deepcopy(open_threads)
    candidate_world_state["open_threads"][thread_id] = {
        "thread_id": thread_id,
        "status": "open",
        "created_by_history_id": source_history_id,
    }
    candidate_world_state = add_history_entry(
        candidate_world_state,
        event_type="unresolved_thread_opened",
        summary=f"Unresolved thread opened: {declaration['description']}",
        location=None,
        time=deepcopy(candidate_world_state["time"]),
        extra={
            "thread_id": thread_id,
            "status": "open",
            "source_history_id": source_history_id,
        },
    )
    return candidate_world_state, {
        "thread_id": thread_id,
        "changed": True,
        "status": "open",
        "history_id": candidate_world_state["history"][-1]["history_id"],
        "source_history_id": source_history_id,
    }


def derive_unresolved_thread_evidence(
    open_threads: dict[str, dict[str, str]],
    declaration: dict[str, Any] | None,
    location_id: str,
) -> list[dict[str, str]]:
    if declaration is None or location_id not in declaration["perception_location_ids"]:
        return []
    thread = open_threads.get(declaration["thread_id"])
    if thread is None or thread["status"] != "open":
        return []
    return [{"text": declaration["evidence_text"]}]
