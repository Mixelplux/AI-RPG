"""Pure derivation for the one authored discovery-gated conversation affordance."""

from typing import Any


def derive_conversation_affordance(
    region: dict[str, Any],
    player_location_id: str | None,
    scene_snapshot: dict[str, Any],
    player_discoveries: tuple[str, ...],
    history: tuple[dict[str, Any], ...],
) -> dict[str, str] | None:
    """Return the exact player-safe affordance when its three eligibility facts hold."""

    declaration = region.get("conversation_affordance")
    if not isinstance(declaration, dict):
        return None
    response = region.get("conversation_player_discovery_response")
    if not isinstance(response, dict):
        return None
    if player_location_id != declaration["location_id"]:
        return None
    if any(
        entry.get("event_type") == response["consequence_event_type"]
        for entry in history
    ):
        return None

    scene_location = scene_snapshot.get("location", {}).get("location_id")
    visible_static = scene_snapshot.get("entities", {}).get("static", [])
    if (
        scene_location != declaration["location_id"]
        or declaration["target_entity_id"] not in visible_static
        or declaration["required_discovery_id"] not in player_discoveries
    ):
        return None

    actor = next(
        (
            entity
            for entity in region.get("entities", [])
            if entity.get("entity_id") == declaration["target_entity_id"]
        ),
        None,
    )
    if not isinstance(actor, dict):
        return None
    target_display_name = actor["name"]
    return {
        "affordance_id": declaration["affordance_id"],
        "display_text": declaration["display_text"],
        "command_text": f"talk to {target_display_name}",
        "target_display_name": target_display_name,
    }
