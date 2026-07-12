from collections import Counter

try:
    from engine.pressure_state import validate_initial_pressures
except ModuleNotFoundError:
    from pressure_state import validate_initial_pressures


def validate_region(region: dict) -> None:
    """
    Validate a Region Pack.

    Raises:
        ValueError if the Region Pack is invalid.
    """

    locations = region.get("locations", [])
    entities = region.get("entities", [])
    simulation_hooks = region.get("simulation_hooks", {})
    errors = []

    # --------------------------------------------------
    # Collect location IDs
    # --------------------------------------------------

    location_ids = [
        location["location_id"]
        for location in locations
    ]

    # --------------------------------------------------
    # Duplicate location IDs
    # --------------------------------------------------

    duplicates = [
        location_id
        for location_id, count in Counter(location_ids).items()
        if count > 1
    ]

    if duplicates:
        errors.append(
            f"Duplicate location_id(s): {duplicates}"
        )

    location_set = set(location_ids)

    # --------------------------------------------------
    # Entry location
    # --------------------------------------------------

    entry_location = simulation_hooks.get("entry_location")

    if entry_location not in location_set:
        errors.append(
            f"Invalid entry_location: {entry_location}"
        )

    # --------------------------------------------------
    # Connected locations
    # --------------------------------------------------

    for location in locations:

        for exit_data in location.get("connected_locations", []):

            destination = exit_data.get("location_id")

            if destination not in location_set:
                errors.append(
                    f"{location['location_id']} references missing location '{destination}'"
                )

    # --------------------------------------------------
    # Supported named static actors
    # --------------------------------------------------

    static_ids = []
    for index, entity in enumerate(entities):
        if not isinstance(entity, dict) or entity.get("persistence") != "static":
            continue
        entity_id = entity.get("entity_id")
        if not isinstance(entity_id, str) or not entity_id:
            errors.append(f"Static entity at index {index} requires a non-empty entity_id")
            continue
        static_ids.append(entity_id)
        entity_location = entity.get("location")
        if not isinstance(entity_location, str) or not entity_location:
            errors.append(f"Entity '{entity_id}' requires one authored location")
        elif entity_location not in location_set:
            errors.append(
                f"Entity '{entity_id}' has invalid location '{entity_location}'"
            )
        knowledge = entity.get("knowledge")
        if not isinstance(knowledge, list):
            errors.append(f"Static entity '{entity_id}' knowledge must be a list")
        elif any(not isinstance(item, str) or not item for item in knowledge):
            errors.append(
                f"Static entity '{entity_id}' knowledge must contain non-empty strings"
            )
        elif len(set(knowledge)) != len(knowledge):
            errors.append(f"Static entity '{entity_id}' knowledge must be unique")
    duplicate_static_ids = sorted(
        entity_id for entity_id, count in Counter(static_ids).items() if count > 1
    )
    if duplicate_static_ids:
        errors.append(f"Duplicate static entity_id(s): {duplicate_static_ids}")

    try:
        validate_initial_pressures(region)
    except ValueError as error:
        errors.append(str(error))

    try:
        validate_conversation_pressure_effects(region)
    except ValueError as error:
        errors.append(str(error))

    try:
        validate_conversation_actor_relocation_effect(region)
    except ValueError as error:
        errors.append(str(error))

    try:
        validate_conversation_actor_knowledge_effect(region)
    except ValueError as error:
        errors.append(str(error))

    try:
        validate_elapsed_time_pressure_effect(region)
    except ValueError as error:
        errors.append(str(error))

    try:
        validate_elapsed_time_actor_relocation_effect(region)
    except ValueError as error:
        errors.append(str(error))

    try:
        validate_pressure_observation_cue(region)
    except ValueError as error:
        errors.append(str(error))

    try:
        validate_conversation_unresolved_thread(region)
    except ValueError as error:
        errors.append(str(error))

    if errors:
        raise ValueError(
            "Region validation failed:\n\n" +
            "\n".join(f"- {error}" for error in errors)
        )


def validate_conversation_actor_relocation_effect(region: dict) -> None:
    field = "conversation_actor_relocation_effect"
    if field not in region:
        return
    effect = region[field]
    if not isinstance(effect, dict):
        raise ValueError(f"{field} must be a dictionary.")
    required = {
        "effect_id", "trigger_entity_id", "actor_entity_id",
        "destination_location_id",
    }
    fields = set(effect)
    if fields != required:
        raise ValueError(
            f"{field} fields are invalid; "
            f"missing={sorted(required - fields)}, extra={sorted(fields - required)}."
        )
    for name in sorted(required):
        if not isinstance(effect[name], str) or not effect[name]:
            raise ValueError(f"{field}.{name} must be a non-empty string.")
    static_ids = {
        entity.get("entity_id")
        for entity in region.get("entities", [])
        if isinstance(entity, dict) and entity.get("persistence") == "static"
    }
    if effect["trigger_entity_id"] not in static_ids:
        raise ValueError(f"{field}.trigger_entity_id must reference a static actor.")
    if effect["actor_entity_id"] not in static_ids:
        raise ValueError(f"{field}.actor_entity_id must reference a static actor.")
    location_ids = {
        location.get("location_id")
        for location in region.get("locations", [])
        if isinstance(location, dict)
    }
    if effect["destination_location_id"] not in location_ids:
        raise ValueError(f"{field}.destination_location_id is unknown.")


def validate_conversation_actor_knowledge_effect(region: dict) -> None:
    field = "conversation_actor_knowledge_effect"
    if field not in region:
        return
    effect = region[field]
    if not isinstance(effect, dict):
        raise ValueError(f"{field} must be a dictionary.")
    required = {"effect_id", "trigger_entity_id", "actor_entity_id", "knowledge_id"}
    fields = set(effect)
    if fields != required:
        raise ValueError(
            f"{field} fields are invalid; "
            f"missing={sorted(required - fields)}, extra={sorted(fields - required)}."
        )
    for name in sorted(required):
        if not isinstance(effect[name], str) or not effect[name]:
            raise ValueError(f"{field}.{name} must be a non-empty string.")
    static_ids = {
        entity.get("entity_id")
        for entity in region.get("entities", [])
        if isinstance(entity, dict) and entity.get("persistence") == "static"
    }
    if effect["trigger_entity_id"] not in static_ids:
        raise ValueError(f"{field}.trigger_entity_id must reference a static actor.")
    if effect["actor_entity_id"] not in static_ids:
        raise ValueError(f"{field}.actor_entity_id must reference a static actor.")


def validate_conversation_unresolved_thread(region: dict) -> None:
    field = "conversation_unresolved_thread"
    if field not in region:
        return
    declaration = region[field]
    if not isinstance(declaration, dict):
        raise ValueError(f"{field} must be a dictionary.")
    required = {
        "thread_id", "description", "trigger_entity_id",
        "perception_location_ids", "evidence_text",
    }
    if set(declaration) != required:
        raise ValueError(f"{field} fields are invalid.")
    for name in ("thread_id", "description", "trigger_entity_id", "evidence_text"):
        if not isinstance(declaration[name], str) or not declaration[name]:
            raise ValueError(f"{field}.{name} must be a non-empty string.")
    static_ids = {
        entity.get("entity_id")
        for entity in region.get("entities", [])
        if isinstance(entity, dict) and entity.get("persistence") == "static"
    }
    if declaration["trigger_entity_id"] not in static_ids:
        raise ValueError(f"{field}.trigger_entity_id must reference a static actor.")
    locations = declaration["perception_location_ids"]
    if not isinstance(locations, list) or not locations:
        raise ValueError(f"{field}.perception_location_ids must be a non-empty list.")
    location_ids = {
        location.get("location_id")
        for location in region.get("locations", [])
        if isinstance(location, dict)
    }
    if any(not isinstance(location_id, str) or not location_id for location_id in locations):
        raise ValueError(f"{field}.perception_location_ids must contain non-empty strings.")
    if len(set(locations)) != len(locations) or any(location_id not in location_ids for location_id in locations):
        raise ValueError(f"{field}.perception_location_ids must contain unique known locations.")


def validate_conversation_pressure_effects(region: dict) -> None:
    if "conversation_pressure_effects" not in region:
        return

    effects = region["conversation_pressure_effects"]
    if not isinstance(effects, list):
        raise ValueError("conversation_pressure_effects must be a list.")

    required_fields = {
        "effect_id",
        "target_entity_id",
        "pressure_id",
        "new_level",
    }
    entity_id_counts = Counter(
        entity.get("entity_id")
        for entity in region.get("entities", [])
        if isinstance(entity, dict)
    )
    pressure_ids = {
        pressure.get("pressure_id")
        for pressure in region.get("initial_pressures", [])
        if isinstance(pressure, dict)
    }
    seen_effect_ids = set()
    seen_target_ids = set()

    for index, effect in enumerate(effects):
        prefix = f"conversation_pressure_effects[{index}]"
        if not isinstance(effect, dict):
            raise ValueError(f"{prefix} must be a dictionary.")

        fields = set(effect)
        if fields != required_fields:
            missing = sorted(required_fields - fields)
            extra = sorted(fields - required_fields)
            raise ValueError(
                f"{prefix} fields are invalid; missing={missing}, extra={extra}."
            )

        for field in ("effect_id", "target_entity_id", "pressure_id"):
            value = effect[field]
            if not isinstance(value, str) or not value:
                raise ValueError(f"{prefix}.{field} must be a non-empty string.")

        effect_id = effect["effect_id"]
        target_entity_id = effect["target_entity_id"]
        pressure_id = effect["pressure_id"]
        new_level = effect["new_level"]

        if effect_id in seen_effect_ids:
            raise ValueError(f"Duplicate conversation pressure effect_id: {effect_id}.")
        if target_entity_id in seen_target_ids:
            raise ValueError(
                "Multiple conversation pressure effects target entity: "
                f"{target_entity_id}."
            )
        if entity_id_counts[target_entity_id] != 1:
            raise ValueError(
                "Conversation effect target_entity_id must reference exactly "
                f"one Region Pack entity: {target_entity_id}."
            )
        if pressure_id not in pressure_ids:
            raise ValueError(f"Unknown conversation effect pressure: {pressure_id}.")
        if isinstance(new_level, bool) or not isinstance(new_level, int):
            raise ValueError(
                f"{prefix}.new_level must be an integer and not a boolean."
            )
        if new_level < 0 or new_level > 100:
            raise ValueError(f"{prefix}.new_level must be from 0 through 100.")

        seen_effect_ids.add(effect_id)
        seen_target_ids.add(target_entity_id)


def validate_elapsed_time_pressure_effect(region: dict) -> None:
    if "elapsed_time_pressure_effect" not in region:
        return

    effect = region["elapsed_time_pressure_effect"]
    if not isinstance(effect, dict):
        raise ValueError("elapsed_time_pressure_effect must be a dictionary.")

    required_fields = {
        "effect_id", "trigger_elapsed_hours", "pressure_id", "new_level"
    }
    fields = set(effect)
    if fields != required_fields:
        missing = sorted(required_fields - fields)
        extra = sorted(fields - required_fields)
        raise ValueError(
            "elapsed_time_pressure_effect fields are invalid; "
            f"missing={missing}, extra={extra}."
        )

    for field in ("effect_id", "pressure_id"):
        value = effect[field]
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"elapsed_time_pressure_effect.{field} must be a non-empty string."
            )

    trigger = effect["trigger_elapsed_hours"]
    if isinstance(trigger, bool) or not isinstance(trigger, int) or trigger <= 0:
        raise ValueError(
            "elapsed_time_pressure_effect.trigger_elapsed_hours must be a "
            "positive integer and not a boolean."
        )

    new_level = effect["new_level"]
    if isinstance(new_level, bool) or not isinstance(new_level, int):
        raise ValueError(
            "elapsed_time_pressure_effect.new_level must be an integer and "
            "not a boolean."
        )
    if new_level < 0 or new_level > 100:
        raise ValueError(
            "elapsed_time_pressure_effect.new_level must be from 0 through 100."
        )

    pressure_ids = {
        pressure.get("pressure_id")
        for pressure in region.get("initial_pressures", [])
        if isinstance(pressure, dict)
    }
    if effect["pressure_id"] not in pressure_ids:
        raise ValueError(
            "Unknown elapsed-time pressure effect pressure: "
            f"{effect['pressure_id']}."
        )


def validate_elapsed_time_actor_relocation_effect(region: dict) -> None:
    field = "elapsed_time_actor_relocation_effect"
    if field not in region:
        return
    effect = region[field]
    if not isinstance(effect, dict):
        raise ValueError(f"{field} must be a dictionary.")
    required_fields = {
        "effect_id", "trigger_elapsed_hours", "actor_entity_id",
        "destination_location_id",
    }
    fields = set(effect)
    if fields != required_fields:
        raise ValueError(
            f"{field} fields are invalid; "
            f"missing={sorted(required_fields - fields)}, "
            f"extra={sorted(fields - required_fields)}."
        )
    for name in ("effect_id", "actor_entity_id", "destination_location_id"):
        if not isinstance(effect[name], str) or not effect[name]:
            raise ValueError(f"{field}.{name} must be a non-empty string.")
    trigger = effect["trigger_elapsed_hours"]
    if isinstance(trigger, bool) or not isinstance(trigger, int) or trigger < 0:
        raise ValueError(
            f"{field}.trigger_elapsed_hours must be a non-negative integer "
            "and not a boolean."
        )
    static_ids = {
        entity.get("entity_id")
        for entity in region.get("entities", [])
        if isinstance(entity, dict) and entity.get("persistence") == "static"
    }
    if effect["actor_entity_id"] not in static_ids:
        raise ValueError(f"{field}.actor_entity_id must reference a static actor.")
    location_ids = {
        location.get("location_id")
        for location in region.get("locations", [])
        if isinstance(location, dict)
    }
    if effect["destination_location_id"] not in location_ids:
        raise ValueError(f"{field}.destination_location_id is unknown.")


def validate_pressure_observation_cue(region: dict) -> None:
    if "pressure_observation_cue" not in region:
        return
    cue = region["pressure_observation_cue"]
    if not isinstance(cue, dict):
        raise ValueError("pressure_observation_cue must be a dictionary.")
    required = {"cue_id", "pressure_id", "minimum_level", "text"}
    if set(cue) != required:
        raise ValueError("pressure_observation_cue must contain exactly cue_id, pressure_id, minimum_level, and text.")
    for field in ("cue_id", "pressure_id", "text"):
        if not isinstance(cue[field], str) or not cue[field]:
            raise ValueError(f"pressure_observation_cue.{field} must be a non-empty string.")
    level = cue["minimum_level"]
    if isinstance(level, bool) or not isinstance(level, int) or not 0 <= level <= 100:
        raise ValueError("pressure_observation_cue.minimum_level must be an integer from 0 through 100 and not a boolean.")
    ids = [p.get("pressure_id") for p in region.get("initial_pressures", []) if isinstance(p, dict)]
    if ids.count(cue["pressure_id"]) != 1:
        raise ValueError("pressure_observation_cue.pressure_id must reference exactly one seeded pressure.")

if __name__ == "__main__":

    import json

    with open("data/regions/bryn_shander.json", "r") as f:
        region = json.load(f)

    validate_region(region)
