from typing import Any, Dict, List, TypedDict


class DestinationResolution(TypedDict):
    status: str
    location_id: str | None
    display_name: str | None
    match_type: str | None
    reason: str
    matches: List[Dict[str, str]]


def resolve_destination(
    destination_text: str,
    locations: List[Dict[str, Any]],
) -> DestinationResolution:
    """Identify a location from loaded region data without executing travel."""

    query = _normalize(destination_text)
    if not query:
        return _unresolved("unresolved", "No destination was provided.", [])

    candidates = [_candidate(location) for location in locations]
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
            "location_id": match["location_id"],
            "display_name": match["display_name"],
            "match_type": "exact" if exact_matches else "derived_alias",
            "reason": "Matched a known location in the loaded region.",
            "matches": [],
        }

    public_matches = [
        {
            "location_id": match["location_id"],
            "display_name": match["display_name"],
        }
        for match in matches
    ]
    if public_matches:
        return _unresolved(
            "ambiguous",
            "More than one known location matches that destination.",
            public_matches,
        )

    return _unresolved(
        "unresolved",
        "No known location matches that destination.",
        [],
    )


def _candidate(location: Dict[str, Any]) -> Dict[str, Any]:
    location_id = location.get("location_id") or location.get("id")
    display_name = location.get("name") or _display_name(location_id or "")
    normalized_name = _normalize(display_name)
    name_without_articles = " ".join(
        word
        for word in normalized_name.split()
        if word not in {"the", "of"}
    )
    return {
        "location_id": location_id,
        "display_name": display_name,
        "aliases": {
            _normalize(location_id or ""),
            normalized_name,
            name_without_articles,
        },
    }


def _unresolved(
    status: str,
    reason: str,
    matches: List[Dict[str, str]],
) -> DestinationResolution:
    return {
        "status": status,
        "location_id": None,
        "display_name": None,
        "match_type": None,
        "reason": reason,
        "matches": matches,
    }


def _normalize(value: str) -> str:
    characters = [
        character.lower() if character.isalnum() else " "
        for character in value
    ]
    return " ".join("".join(characters).split())


def _display_name(identifier: str) -> str:
    return identifier.replace("_", " ").title()
