"""Deterministic, player-safe structured projection of the current scene."""

from collections import defaultdict
from typing import Any

from engine.navigation_projection import derive_safe_exits


_SCHEMA = "ai_rpg.current_scene_projection"
_VERSION = 1


def _safe_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None


def _current_location_id(scene_snapshot: dict[str, Any]) -> str | None:
    location = scene_snapshot.get("location")
    if not isinstance(location, dict):
        return None
    return _safe_text(location.get("location_id") or location.get("id"))


def _visible_scene_data(
    scene_snapshot: dict[str, Any],
    perception_snapshot: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Return visible scene data only when it describes this exact scene."""

    current_location_id = _current_location_id(scene_snapshot)
    visible = perception_snapshot.get("visible")
    if not isinstance(visible, dict):
        return None

    visible_location = visible.get("location")
    if not isinstance(visible_location, dict):
        return None
    visible_location_id = _safe_text(visible_location.get("id"))
    if current_location_id is None or visible_location_id != current_location_id:
        return None

    visible_entities = visible.get("entities")
    if not isinstance(visible_entities, dict):
        return None
    return visible_location, visible_entities


def _visible_actors(
    region: dict[str, Any],
    scene_snapshot: dict[str, Any],
    visible_entities: dict[str, Any],
) -> list[dict[str, str]]:
    scene_entities = scene_snapshot.get("entities")
    if not isinstance(scene_entities, dict):
        return []
    scene_static = scene_entities.get("static")
    visible_static = visible_entities.get("static")
    if not isinstance(scene_static, list) or not isinstance(visible_static, list):
        return []

    visible_ids = {
        actor_id for actor_id in visible_static
        if isinstance(actor_id, str) and actor_id
    }
    actors_by_id: dict[str, str] = {}
    for actor in region.get("entities", []):
        if not isinstance(actor, dict) or actor.get("persistence") != "static":
            continue
        actor_id = actor.get("entity_id")
        display_name = _safe_text(actor.get("name"))
        if isinstance(actor_id, str) and actor_id and display_name is not None:
            actors_by_id[actor_id] = display_name

    actor_names: list[str] = []
    seen_ids: set[str] = set()
    for actor_id in scene_static:
        if (
            not isinstance(actor_id, str)
            or actor_id in seen_ids
            or actor_id not in visible_ids
        ):
            continue
        display_name = actors_by_id.get(actor_id)
        if display_name is None:
            continue
        actor_names.append(display_name)
        seen_ids.add(actor_id)

    return [
        {"display_name": display_name}
        for display_name in sorted(actor_names, key=lambda value: (value.casefold(), value))
    ]


def _visible_groups(
    scene_snapshot: dict[str, Any],
    visible_entities: dict[str, Any],
) -> list[dict[str, Any]]:
    """Aggregate only spawned entities carrying an explicit safe display name.

    The legacy Scene and Perception snapshots carry internal spawn templates.
    Those templates are deliberately never humanized or exposed as a fallback.
    A group therefore appears only when a visible spawned record explicitly
    supplies a distinct player-facing ``display_name``.
    """

    scene_entities = scene_snapshot.get("entities")
    if not isinstance(scene_entities, dict):
        return []
    scene_spawned = scene_entities.get("spawned")
    visible_spawned = visible_entities.get("spawned")
    if not isinstance(scene_spawned, list) or not isinstance(visible_spawned, list):
        return []

    labels_by_template: dict[str, list[str]] = defaultdict(list)
    for spawned in visible_spawned:
        if not isinstance(spawned, dict):
            continue
        template = _safe_text(spawned.get("template"))
        display_name = _safe_text(spawned.get("display_name"))
        if (
            template is not None
            and display_name is not None
            and display_name.casefold() != template.casefold()
        ):
            labels_by_template[template].append(display_name)

    counts: dict[str, int] = defaultdict(int)
    for spawned in scene_spawned:
        if not isinstance(spawned, dict):
            continue
        template = _safe_text(spawned.get("template"))
        if template is None or not labels_by_template.get(template):
            continue
        display_name = labels_by_template[template].pop(0)
        counts[display_name] += 1

    return [
        {"display_name": display_name, "count": counts[display_name]}
        for display_name in sorted(counts, key=lambda value: (value.casefold(), value))
    ]


def build_current_scene_projection(
    region: dict[str, Any],
    scene_snapshot: dict[str, Any],
    perception_snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Build a fresh, fail-closed, JSON-compatible player scene projection."""

    projection: dict[str, Any] = {
        "schema": _SCHEMA,
        "version": _VERSION,
        "location": {"name": "", "description": ""},
        "entities": {"actors": [], "groups": []},
        "exits": [],
    }
    if not all(isinstance(value, dict) for value in (region, scene_snapshot, perception_snapshot)):
        return projection

    visible_data = _visible_scene_data(scene_snapshot, perception_snapshot)
    if visible_data is None:
        return projection
    visible_location, visible_entities = visible_data

    projection["location"] = {
        "name": _safe_text(visible_location.get("name")) or "",
        "description": _safe_text(visible_location.get("description_seed")) or "",
    }
    projection["entities"] = {
        "actors": _visible_actors(region, scene_snapshot, visible_entities),
        "groups": _visible_groups(scene_snapshot, visible_entities),
    }
    projection["exits"] = derive_safe_exits(
        scene_snapshot,
        region.get("locations", []),
    )
    return projection
