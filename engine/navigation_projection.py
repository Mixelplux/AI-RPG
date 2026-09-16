"""Derived, player-safe presentation of immediate scene navigation."""

from copy import deepcopy
from typing import Any, Dict


_LOCAL_ORIENTATIONS = {
    "north": "north",
    "south": "south",
    "east": "east",
    "west": "west",
    "up": "up",
    "down": "down",
    "in": "inside",
    "out": "outside",
}


def derive_safe_exits(
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]],
) -> list[Dict[str, str]]:
    """Return immediate exits that have safe authored display text.

    Identifiers are used only to join the current scene's structural exits to
    authored location names.  They never leave this derived result.
    """

    if not isinstance(scene_snapshot, dict) or not isinstance(locations, list):
        return []

    location = scene_snapshot.get("location")
    if not isinstance(location, dict):
        return []
    current_location_id = location.get("location_id")
    if not isinstance(current_location_id, str) or not current_location_id:
        return []

    names_by_id = {
        location.get("location_id"): location["name"].strip()
        for location in locations
        if isinstance(location, dict)
        and isinstance(location.get("location_id"), str)
        and location["location_id"]
        and isinstance(location.get("name"), str)
        and location["name"].strip()
    }

    exits = scene_snapshot.get("exits")
    if not isinstance(exits, list):
        return []

    safe_exits: list[Dict[str, str]] = []
    seen_destinations: set[str] = set()
    for exit_data in exits:
        if not isinstance(exit_data, dict):
            continue

        destination_id = exit_data.get("location_id")
        orientation = _LOCAL_ORIENTATIONS.get(exit_data.get("direction"))
        destination_name = names_by_id.get(destination_id)
        if (
            not isinstance(destination_id, str)
            or not destination_id
            or destination_id == current_location_id
            or destination_id in seen_destinations
            or orientation is None
            or destination_name is None
        ):
            continue

        safe_exits.append({
            "orientation": orientation,
            "destination_name": destination_name,
        })
        seen_destinations.add(destination_id)

    return deepcopy(safe_exits)


def derive_navigation_projection(
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]],
) -> Dict[str, list[Dict[str, str]]]:
    """Return player-safe local cues for directly perceivable scene exits."""

    route_cues = [
        {
            "text": (
                f"The way {safe_exit['orientation']} leads to "
                f"{safe_exit['destination_name']}."
            ),
        }
        for safe_exit in derive_safe_exits(scene_snapshot, locations)
    ]
    return {"route_cues": deepcopy(route_cues)}
