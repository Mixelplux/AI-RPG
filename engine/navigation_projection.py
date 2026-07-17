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


def derive_navigation_projection(
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]],
) -> Dict[str, list[Dict[str, str]]]:
    """Return player-safe local cues for directly perceivable scene exits.

    Scene exits are the existing boundary for local perception and remain the
    only navigation authority consulted here. Destination identifiers join
    authored display names but never leave the derived projection. Each cue
    describes one immediate way from the current scene, not a destination's
    position in a wider map.
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

    route_cues: list[Dict[str, str]] = []
    seen_destinations: set[str] = set()
    for exit_data in scene_snapshot.get("exits", []):
        if not isinstance(exit_data, dict):
            continue

        destination_id = exit_data.get("location_id")
        direction = exit_data.get("direction")
        destination_name = names_by_id.get(destination_id)
        orientation = _LOCAL_ORIENTATIONS.get(direction)

        if (
            not isinstance(destination_id, str)
            or destination_id == current_location_id
            or destination_id in seen_destinations
            or destination_name is None
            or orientation is None
        ):
            continue

        route_cues.append({
            "text": f"The way {orientation} leads to {destination_name.strip()}.",
        })
        seen_destinations.add(destination_id)

    return {"route_cues": deepcopy(route_cues)}
