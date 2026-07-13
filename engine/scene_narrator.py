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

    location_name = location.get("name", "Unknown Location")
    description_seed = location.get("description_seed", "")

    weather = environment.get("weather", {})
    weather_type = weather.get("type")
    weather_severity = weather.get("severity")

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
        if weather_severity is not None:
            description_parts.append(
                f"The weather is {weather_type} with severity {weather_severity}."
            )
        else:
            description_parts.append(
                f"The weather is {weather_type}."
            )

    entity_descriptions = visible_entity_names + spawned_labels

    if entity_descriptions:
        description_parts.append(
            "Present here: " + ", ".join(entity_descriptions) + "."
        )

    if resolved_thread_observation:
        description_parts.append(resolved_thread_observation["text"])

    return {
        "title": f"{location_name}, Bryn Shander",
        "description": "\n\n".join(description_parts),
        "visible_entities": visible_entity_names,
        "player_prompt": "What do you do?"
    }
