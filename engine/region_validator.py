from collections import Counter


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
    # Entity locations
    # --------------------------------------------------

    for entity in entities:

        entity_location = entity.get("location")

        if entity_location not in location_set:
            errors.append(
                f"Entity '{entity['entity_id']}' has invalid location '{entity_location}'"
            )

    if errors:
        raise ValueError(
            "Region validation failed:\n\n" +
            "\n".join(f"- {error}" for error in errors)
        )

if __name__ == "__main__":

    import json

    with open("data/regions/bryn_shander.json", "r") as f:
        region = json.load(f)

    validate_region(region) 