from copy import deepcopy
from typing import Any, Dict

from engine.world_state import (
    add_history_entry,
    get_player_location_id,
    get_time,
    set_player_location_id,
)


def apply_interaction(
    world_state: Dict[str, Any],
    interaction_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Apply a validated Interaction Result to persistent World State.

    Sprint 6.1:
    - Movement updates world_state.player.current_location_id.
    - Scene Snapshots are no longer mutated as persistent state.
    """

    updated_world_state = deepcopy(world_state)

    action = interaction_result.get("action", {})

    if action.get("type") == "talk":
        return apply_conversation_interaction(
            updated_world_state,
            interaction_result
        )

    if action.get("type") != "move":
        return updated_world_state

    if not interaction_result.get("success"):
        return updated_world_state

    destination_location_id = interaction_result.get("destination_location_id")

    if destination_location_id:
        origin_location_id = get_player_location_id(updated_world_state)
        current_time = get_time(updated_world_state)
        updated_world_state = set_player_location_id(
            updated_world_state,
            destination_location_id
        )
        updated_world_state = add_history_entry(
            updated_world_state,
            event_type="player_movement",
            summary=(
                f"Player moved from {origin_location_id} "
                f"to {destination_location_id}."
            ),
            location=destination_location_id,
            time=current_time
        )

    return updated_world_state


def apply_conversation_interaction(
    world_state: Dict[str, Any],
    interaction_result: Dict[str, Any]
) -> Dict[str, Any]:
    if not interaction_result.get("success"):
        return world_state

    target_resolution = interaction_result.get("target_resolution", {})

    if target_resolution.get("status") != "resolved":
        return world_state

    if target_resolution.get("target_type") != "entity":
        return world_state

    target_entity_id = target_resolution.get("identifier")
    target_display_name = target_resolution.get("display_name")

    if not target_entity_id or not target_display_name:
        return world_state

    return add_history_entry(
        world_state,
        event_type="player_conversation",
        summary=(
            "Player initiated a conversation with "
            f"{target_display_name}."
        ),
        location=get_player_location_id(world_state),
        time=get_time(world_state),
        extra={
            "target_entity_id": target_entity_id,
            "target_display_name": target_display_name
        }
    )
