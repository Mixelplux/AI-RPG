from typing import Any, Dict, List, TypedDict


class TargetResolution(TypedDict):
    status: str
    target_type: str | None
    identifier: str | None
    direction: str | None
    display_name: str | None
    matches: List[Dict[str, str | None]]


def resolve_scene_target(
    target_text: str,
    scene_snapshot: Dict[str, Any],
    entity_catalog: List[Dict[str, Any]] | None = None,
) -> TargetResolution:
    """Resolve target text against entities and exits in the current scene only."""

    query = _normalize(target_text)
    if not query:
        return _unresolved("unresolved", [])

    candidates = _entity_candidates(scene_snapshot, entity_catalog or [])
    candidates.extend(_exit_candidates(scene_snapshot))

    exact_matches = [
        candidate
        for candidate in candidates
        if query in candidate["aliases"]
    ]
    matches = exact_matches or [
        candidate
        for candidate in candidates
        if any(query in alias.split() for alias in candidate["aliases"])
    ]

    if len(matches) == 1:
        match = matches[0]
        return {
            "status": "resolved",
            "target_type": match["target_type"],
            "identifier": match["identifier"],
            "direction": match["direction"],
            "display_name": match["display_name"],
            "matches": [],
        }

    public_matches = [_public_candidate(match) for match in matches]
    status = "ambiguous" if public_matches else "unresolved"
    return _unresolved(status, public_matches)


def _entity_candidates(
    scene_snapshot: Dict[str, Any],
    entity_catalog: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    entities = scene_snapshot.get("entities", {})
    catalog_by_id = {
        entity.get("entity_id"): entity
        for entity in entity_catalog
    }
    candidates = []

    for entity_id in entities.get("static", []):
        metadata = catalog_by_id.get(entity_id, {})
        display_name = metadata.get("name") or _display_name(entity_id)
        aliases = {
            _normalize(entity_id),
            _normalize(display_name),
            _normalize(metadata.get("type", "")),
        }
        candidates.append(_candidate(
            "entity", entity_id, None, display_name, aliases
        ))

    seen_templates = set()
    for spawned in entities.get("spawned", []):
        template = spawned.get("template")
        if not template or template in seen_templates:
            continue
        seen_templates.add(template)
        display_name = _display_name(template)
        candidates.append(_candidate(
            "entity",
            template,
            None,
            display_name,
            {_normalize(template), _normalize(display_name)},
        ))

    return candidates


def _exit_candidates(
    scene_snapshot: Dict[str, Any],
) -> List[Dict[str, Any]]:
    candidates = []
    for exit_data in scene_snapshot.get("exits", []):
        direction = exit_data.get("direction")
        identifier = exit_data.get("location_id")
        if not direction:
            continue
        display_name = f"{direction.title()} exit"
        candidates.append(_candidate(
            "exit",
            identifier,
            direction,
            display_name,
            {
                _normalize(direction),
                _normalize(identifier or ""),
                _normalize(display_name),
            },
        ))
    return candidates


def _candidate(
    target_type: str,
    identifier: str | None,
    direction: str | None,
    display_name: str,
    aliases: set[str],
) -> Dict[str, Any]:
    return {
        "target_type": target_type,
        "identifier": identifier,
        "direction": direction,
        "display_name": display_name,
        "aliases": {alias for alias in aliases if alias},
    }


def _public_candidate(candidate: Dict[str, Any]) -> Dict[str, str | None]:
    return {
        "target_type": candidate["target_type"],
        "identifier": candidate["identifier"],
        "direction": candidate["direction"],
        "display_name": candidate["display_name"],
    }


def _unresolved(
    status: str,
    matches: List[Dict[str, str | None]],
) -> TargetResolution:
    return {
        "status": status,
        "target_type": None,
        "identifier": None,
        "direction": None,
        "display_name": None,
        "matches": matches,
    }


def _normalize(value: str) -> str:
    return " ".join(value.lower().replace("_", " ").split())


def _display_name(identifier: str) -> str:
    return identifier.replace("_", " ").title()
