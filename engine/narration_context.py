from copy import deepcopy
from typing import Any, Dict

from engine.history_context import build_history_context_packet
from engine.world_state import get_player_location_id, get_time


NARRATION_CONTEXT_SCHEMA = "ai_rpg.narration_context_packet"
NARRATION_CONTEXT_VERSION = 1

NARRATION_CONTEXT_BOUNDARY_RULE = (
    "The narrator can describe. The engine decides what is true."
)
NARRATION_CONTEXT_DRIFT_GUARDRAIL = (
    "Narration context may support atmospheric prose, but future narration "
    "must not invent unstated specifics. Sensory description must be grounded "
    "in known scene facts and must not create durable world truth."
)
NARRATION_CONTEXT_ATMOSPHERE_EXAMPLE = (
    "If the scene contains a blizzard, narration may describe cold weather, "
    "but may not mention the player's gloves unless gloves are present in "
    "player state or context."
)
NARRATION_SAFE_HISTORY_EVENT_TYPES = frozenset({
    "player_conversation",
    "player_movement",
    "time_advanced",
})


def build_narration_context_packet(
    world_state: Dict[str, Any],
    scene_snapshot: Dict[str, Any],
    player_input: str,
    history_count: int | None = None,
    pressure_cue: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    history_context = build_history_context_packet(
        world_state,
        count=history_count,
    )
    history_context["history_entries"] = [
        entry
        for entry in history_context["history_entries"]
        if entry.get("event_type") in NARRATION_SAFE_HISTORY_EVENT_TYPES
    ]
    return {
        "schema": NARRATION_CONTEXT_SCHEMA,
        "version": NARRATION_CONTEXT_VERSION,
        "player_input": player_input,
        "current_time": deepcopy(get_time(world_state)),
        "player": {
            "current_location_id": get_player_location_id(world_state)
        },
        "scene_snapshot": deepcopy(scene_snapshot),
        "history_context": history_context,
        "pressure_cue": deepcopy(pressure_cue or {}),
        "boundary": {
            "type": "read_only_narration_input",
            "rule": NARRATION_CONTEXT_BOUNDARY_RULE,
            "drift_guardrail": NARRATION_CONTEXT_DRIFT_GUARDRAIL,
            "atmosphere_example": NARRATION_CONTEXT_ATMOSPHERE_EXAMPLE,
            "durability": (
                "Atmospheric prose derived from this packet is not durable "
                "world truth unless the engine records it."
            )
        }
    }
