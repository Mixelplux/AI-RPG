from copy import deepcopy
from typing import Any, Dict

from engine.world_state import set_player_location_id


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

    if action.get("type") != "move":
        return updated_world_state

    if not interaction_result.get("success"):
        return updated_world_state

    destination_location_id = interaction_result.get("destination_location_id")

    if destination_location_id:
        updated_world_state = set_player_location_id(
            updated_world_state,
            destination_location_id
        )

    return updated_world_state