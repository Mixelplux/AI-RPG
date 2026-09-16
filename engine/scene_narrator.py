from copy import deepcopy
from typing import Dict, Any, List


def format_entity_name(entity_id: str) -> str:
    """
    Convert an entity id into a readable display name.

    Example:
    captain_darvin_grey -> Captain Darvin Grey
    """
    return entity_id.replace("_", " ").title()


def count_spawned_templates(spawned_entities: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Count spawned entities by template.

    Example:
    [
        {"template": "city_guard"},
        {"template": "city_guard"}
    ]

    becomes:
    {
        "city_guard": 2
    }
    """
    counts = {}

    for entity in spawned_entities:
        template = entity.get("template", "unknown")
        counts[template] = counts.get(template, 0) + 1

    return counts


def format_spawned_entity_label(template: str, count: int) -> str:
    """
    Convert a spawned entity template and count into readable text.

    Example:
    city_guard, 2 -> 2 city guards
    """
    readable = template.replace("_", " ")

    if count == 1:
        return f"1 {readable}"

    return f"{count} {readable}s"


def format_navigation(route_cues: List[Dict[str, str]]) -> str | None:
    """Render already-derived immediate route cues without map-like prose."""

    if not route_cues:
        return None

    cues = [
        cue["text"]
        for cue in route_cues
        if isinstance(cue.get("text"), str) and cue["text"]
    ]
    if not cues:
        return None

    return " ".join(cues)


def format_contextual_actions(opportunities: List[str]) -> str | None:
    """Render already player-safe, advisory opportunity text."""

    texts = [text for text in opportunities if isinstance(text, str) and text]
    return " ".join(texts) if texts else None


def narrate_scene(perception_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a Perception Snapshot into a structured narrative object.

    v0.1 rules:
    - Use only information from the Perception Snapshot.
    - Do not mutate the input.
    - Do not invent world facts.
    - Do not handle player input.
    """

    perception = deepcopy(perception_snapshot)

    location = perception["visible"]["location"]
    environment = perception.get("environment", {})
    entities = perception["visible"]["entities"]
    resolved_thread_observation = perception.get("resolved_thread_observation", {})
    navigation = perception.get("navigation", {})
    contextual_actions = perception.get("contextual_actions", {})

    location_name = location.get("name", "Unknown Location")
    description_seed = location.get("description_seed", "")

    weather = environment.get("weather", {})
    weather_type = weather.get("type")

    static_entities = entities.get("static", [])
    spawned_entities = entities.get("spawned", [])

    visible_entity_names = [
        format_entity_name(entity_id)
        for entity_id in static_entities
    ]

    spawned_counts = count_spawned_templates(spawned_entities)

    spawned_labels = [
        format_spawned_entity_label(template, count)
        for template, count in spawned_counts.items()
    ]

    description_parts = []

    if description_seed:
        description_parts.append(description_seed)

    if weather_type is not None:
        description_parts.append(f"The weather is {weather_type}.")

    entity_descriptions = visible_entity_names + spawned_labels

    if entity_descriptions:
        description_parts.append(
            "Present here: " + ", ".join(entity_descriptions) + "."
        )

    if resolved_thread_observation:
        description_parts.append(resolved_thread_observation["text"])

    navigation_text = format_navigation(navigation.get("route_cues", []))
    if navigation_text:
        description_parts.append(navigation_text)

    contextual_action_text = format_contextual_actions(
        contextual_actions.get("opportunities", [])
    )
    if contextual_action_text:
        description_parts.append(contextual_action_text)

    return {
        "title": f"{location_name}, Bryn Shander",
        "description": "\n\n".join(description_parts),
        "visible_entities": visible_entity_names,
        "navigation": deepcopy(navigation.get("route_cues", [])),
        "contextual_actions": deepcopy(contextual_actions.get("opportunities", [])),
        "player_prompt": "What do you do?"
    }
