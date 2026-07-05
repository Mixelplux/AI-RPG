from copy import deepcopy
from typing import Any, Dict


def create_initial_world_state(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create the initial persistent World State.

    Sprint 6.3:
    - Tracks the player's current location.
    - Owns mutable runtime weather state.
    - Owns mutable runtime time state.
    - Uses the Region Pack only for initial weather and time values.
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

    return {
        "player": {
            "current_location_id": starting_location_id
        },
        "weather": deepcopy(initial_weather),
        "time": deepcopy(initial_time)
    }


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