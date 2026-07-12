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
