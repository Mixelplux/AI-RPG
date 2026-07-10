from copy import deepcopy
from typing import Any, Dict

from engine.world_state import (
    DEFAULT_HISTORY_QUERY_COUNT,
    get_player_location_id,
    get_time,
    query_history,
)


HISTORY_CONTEXT_SCHEMA = "ai_rpg.history_context_packet"
HISTORY_CONTEXT_VERSION = 1
MAX_HISTORY_CONTEXT_COUNT = 25


def build_history_context_packet(
    world_state: Dict[str, Any],
    count: int | None = None
) -> Dict[str, Any]:
    limit = validate_history_context_count(count)

    return {
        "schema": HISTORY_CONTEXT_SCHEMA,
        "version": HISTORY_CONTEXT_VERSION,
        "limit": limit,
        "default_limit": DEFAULT_HISTORY_QUERY_COUNT,
        "max_limit": MAX_HISTORY_CONTEXT_COUNT,
        "current_time": deepcopy(get_time(world_state)),
        "player": {
            "current_location_id": get_player_location_id(world_state)
        },
        "history_entries": query_history(world_state, count=limit)
    }


def validate_history_context_count(count: int | None) -> int:
    if count is None:
        return DEFAULT_HISTORY_QUERY_COUNT

    if not isinstance(count, int):
        raise ValueError("History context count must be an integer.")

    if count < 0:
        raise ValueError("History context count must not be negative.")

    if count > MAX_HISTORY_CONTEXT_COUNT:
        raise ValueError(
            "History context count must not exceed "
            f"{MAX_HISTORY_CONTEXT_COUNT}."
        )

    return count
