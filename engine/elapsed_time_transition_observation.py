"""One derived player-safe observation for the accepted one-hour wait."""

from typing import Any


def derive_elapsed_time_transition_observation(
    command_start_scene: dict[str, Any],
    completed_scene: dict[str, Any],
    entity_catalog: list[dict[str, Any]],
) -> str:
    """Describe one elapsed hour and, at most, one visible actor absence.

    This intentionally compares only the static actors projected into the two
    scene snapshots. The catalog supplies authored public display names only;
    it is not used to infer any mutable simulation fact or reason for absence.
    """

    observation = "An hour passes."
    start_location = command_start_scene.get("location", {})
    completed_location = completed_scene.get("location", {})
    if start_location.get("location_id") != completed_location.get("location_id"):
        return observation

    completed_actor_ids = set(
        completed_scene.get("entities", {}).get("static", [])
    )
    for actor_id in command_start_scene.get("entities", {}).get("static", []):
        if actor_id in completed_actor_ids:
            continue
        actor_name = _player_safe_actor_name(actor_id, entity_catalog)
        location_name = start_location.get("name")
        if actor_name and isinstance(location_name, str) and location_name:
            return f"{observation} {actor_name} is no longer at the {location_name}."

    return observation


def _player_safe_actor_name(
    actor_id: Any,
    entity_catalog: list[dict[str, Any]],
) -> str | None:
    if not isinstance(actor_id, str) or not actor_id:
        return None

    for entity in entity_catalog:
        if (
            isinstance(entity, dict)
            and entity.get("persistence") == "static"
            and entity.get("entity_id") == actor_id
            and isinstance(entity.get("name"), str)
            and entity["name"]
        ):
            return entity["name"]
    return None
