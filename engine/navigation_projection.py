"""Derived, player-safe presentation of immediate scene navigation."""

from copy import deepcopy
from typing import Any, Dict


_PLAYER_FACING_DIRECTIONS = {
    "north": "north",
    "south": "south",
    "east": "east",
    "west": "west",
    "up": "up",
    "down": "down",
    "in": "inside",
    "out": "outside",
}


def derive_navigation_projection(
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]],
) -> Dict[str, list[Dict[str, str]]]:
    """Return only safely presentable, directly perceivable current-scene exits.

    Scene exits are the existing boundary for local perception.  Destination
    identifiers are used only to join authored display names and never leave
    this derived projection.
    """

    current_location_id = scene_snapshot.get("location", {}).get("location_id")
    names_by_id = {
        location.get("location_id"): location.get("name")
        for location in locations
        if isinstance(location, dict)
        and isinstance(location.get("location_id"), str)
        and location["location_id"]
        and isinstance(location.get("name"), str)
        and location["name"].strip()
    }

    routes: list[Dict[str, str]] = []
    seen_destinations: set[str] = set()
    for exit_data in scene_snapshot.get("exits", []):
        if not isinstance(exit_data, dict):
            continue

        destination_id = exit_data.get("location_id")
        direction = exit_data.get("direction")
        destination_name = names_by_id.get(destination_id)
        player_facing_direction = _PLAYER_FACING_DIRECTIONS.get(direction)

        if (
            not isinstance(destination_id, str)
            or destination_id == current_location_id
            or destination_id in seen_destinations
            or destination_name is None
            or player_facing_direction is None
        ):
            continue

        routes.append({
            "direction": player_facing_direction,
            "destination_name": destination_name.strip(),
        })
        seen_destinations.add(destination_id)

    return {"routes": deepcopy(routes)}
