"""Derived player-safe presentation of fixed contextual action opportunities."""

from typing import Any

from engine.action_eligibility import (
    find_eligible_investigation_discovery,
    is_clue_presentation_acceptable,
)
from engine.target_resolver import resolve_scene_target


def derive_contextual_action_projection(
    region: dict[str, Any],
    world_state: dict[str, Any],
    scene_snapshot: dict[str, Any],
    conversation_affordance: dict[str, str] | None = None,
) -> dict[str, list[str]]:
    """Return fixed, advisory opportunities as player-safe natural-language text.

    Internal identities are used only to reuse existing resolver predicates and
    never leave this derived presentation.
    """

    opportunities: list[str] = []
    visible_static_ids = scene_snapshot.get("entities", {}).get("static", [])
    static_by_id = {
        actor.get("entity_id"): actor
        for actor in region.get("entities", [])
        if isinstance(actor, dict) and actor.get("persistence") == "static"
    }

    visible_actors: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for actor_id in visible_static_ids:
        actor = static_by_id.get(actor_id)
        name = actor.get("name") if isinstance(actor, dict) else None
        if not isinstance(name, str) or not name.strip():
            continue
        target = resolve_scene_target(name, scene_snapshot, region.get("entities", []))
        if (
            target.get("status") == "resolved"
            and target.get("target_type") == "entity"
            and target.get("identifier") == actor_id
        ):
            visible_actors.append((actor, target))
            opportunities.append(f"You can speak with {name.strip()}.")

    if find_eligible_investigation_discovery(region, world_state) is not None:
        opportunities.append("You can investigate this area.")

    discovered_ids = set(world_state.get("player_discoveries", []))
    for clue in region.get("discovery_declarations", []):
        title = clue.get("title") if isinstance(clue, dict) else None
        if (
            not isinstance(title, str)
            or not title.strip()
            or clue.get("discovery_id") not in discovered_ids
        ):
            continue
        for actor, target in visible_actors:
            if is_clue_presentation_acceptable(region, world_state, clue, target):
                opportunities.append(
                    f"You can present {title.strip()} to {actor['name'].strip()}."
                )

    if isinstance(conversation_affordance, dict):
        display_text = conversation_affordance.get("display_text")
        if isinstance(display_text, str) and display_text.strip():
            opportunities.append(display_text.strip())

    from engine import west_road_predicament as west_road
    if west_road.enabled(region):
        for command in west_road.available_commands(world_state, scene_snapshot):
            cost = " (one hour; other approaches lose coverage)" if command == "advocate patrol" else " (one hour; traffic remains exposed)" if command == "continue investigation" else ""
            opportunities.append("You can choose: " + command + cost + ".")
    return {"opportunities": opportunities}
