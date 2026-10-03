"""Narrow, pure predicates shared by existing contextual action resolvers."""

from typing import Any


def find_eligible_investigation_discovery(
    region: dict[str, Any],
    world_state: dict[str, Any],
) -> dict[str, Any] | None:
    """Return the first declaration the existing investigate resolver can acquire."""

    location_id = world_state.get("player", {}).get("current_location_id")
    trace_ids = {
        trace.get("trace_id")
        for trace in world_state.get("evidence_traces", [])
        if isinstance(trace, dict) and trace.get("location_id") == location_id
    }
    discoveries = set(world_state.get("player_discoveries", []))
    return next(
        (
            declaration
            for declaration in region.get("discovery_declarations", [])
            if declaration.get("location_id") == location_id
            and declaration.get("trace_id") in trace_ids
            and declaration.get("discovery_id") not in discoveries
        ),
        None,
    )


def is_clue_presentation_acceptable(
    region: dict[str, Any],
    world_state: dict[str, Any],
    clue: dict[str, Any] | None,
    target: dict[str, Any],
) -> bool:
    """Match the established present-clue resolver's acceptance boundary."""

    if (
        not isinstance(clue, dict)
        or clue.get("discovery_id") not in world_state.get("player_discoveries", [])
        or target.get("status") != "resolved"
        or target.get("target_type") != "entity"
    ):
        return False

    from engine import west_road_predicament as west_road
    if west_road.enabled(region):
        return (target.get("identifier") in (west_road.GREY, west_road.ELIN)
                and west_road.shared_id(clue["discovery_id"]) not in world_state["actor_knowledge"].get(target["identifier"], []))

    declaration = region.get("conversation_discovery_resolution")
    recall = region.get("conversation_discovery_actor_relocation")
    resolution_matches = (
        isinstance(declaration, dict)
        and clue.get("discovery_id") == declaration.get("required_discovery_id")
        and target.get("identifier") == declaration.get("target_entity_id")
    )
    recall_matches = (
        isinstance(recall, dict)
        and clue.get("discovery_id") == recall.get("required_discovery_id")
        and target.get("identifier") == recall.get("target_entity_id")
    )
    if not resolution_matches and not recall_matches:
        return False
    if recall_matches:
        return True

    thread_id = declaration.get("required_thread_id")
    return (
        isinstance(thread_id, str)
        and thread_id not in world_state.get("resolved_threads", {})
        and thread_id in world_state.get("open_threads", {})
    )
