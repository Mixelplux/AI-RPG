from copy import deepcopy
from typing import Any, Dict


PRESSURE_FIELDS = {
    "pressure_id",
    "pressure_type",
    "scope_type",
    "scope_id",
    "level",
    "provenance",
}
PROVENANCE_FIELDS = {"kind", "source_id"}
SUPPORTED_SCOPE_TYPES = {"region", "location"}
REGION_PACK_PROVENANCE = "region_pack"


def validate_pressure_record(
    pressure: Any,
    region_id: str | None = None,
    location_ids: set[str] | None = None,
) -> None:
    if not isinstance(pressure, dict):
        raise ValueError("Pressure record must be a dictionary.")

    fields = set(pressure)
    if fields != PRESSURE_FIELDS:
        missing = sorted(PRESSURE_FIELDS - fields)
        extra = sorted(fields - PRESSURE_FIELDS)
        raise ValueError(
            f"Pressure record fields are invalid; missing={missing}, extra={extra}."
        )

    pressure_id = pressure["pressure_id"]
    if not isinstance(pressure_id, str) or not pressure_id:
        raise ValueError("pressure_id must be a non-empty string.")

    pressure_type = pressure["pressure_type"]
    if not isinstance(pressure_type, str) or not pressure_type:
        raise ValueError("pressure_type must be a non-empty string.")

    scope_type = pressure["scope_type"]
    if not isinstance(scope_type, str) or scope_type not in SUPPORTED_SCOPE_TYPES:
        raise ValueError("scope_type must be region or location.")

    scope_id = pressure["scope_id"]
    if not isinstance(scope_id, str) or not scope_id:
        raise ValueError("scope_id must be a non-empty string.")

    if region_id is not None:
        if scope_type == "region" and scope_id != region_id:
            raise ValueError("Region-scoped pressure scope_id must equal region_id.")
        if scope_type == "location" and scope_id not in (location_ids or set()):
            raise ValueError("Location-scoped pressure scope_id is not in the Region Pack.")

    level = pressure["level"]
    if isinstance(level, bool) or not isinstance(level, int):
        raise ValueError("Pressure level must be an integer and not a boolean.")
    if level < 0 or level > 100:
        raise ValueError("Pressure level must be from 0 through 100.")

    provenance = pressure["provenance"]
    if not isinstance(provenance, dict):
        raise ValueError("Pressure provenance must be a dictionary.")

    provenance_fields = set(provenance)
    if provenance_fields != PROVENANCE_FIELDS:
        missing = sorted(PROVENANCE_FIELDS - provenance_fields)
        extra = sorted(provenance_fields - PROVENANCE_FIELDS)
        raise ValueError(
            f"Pressure provenance fields are invalid; missing={missing}, extra={extra}."
        )

    if provenance["kind"] != REGION_PACK_PROVENANCE:
        raise ValueError("Pressure provenance kind must be region_pack.")

    source_id = provenance["source_id"]
    if not isinstance(source_id, str) or not source_id:
        raise ValueError("Pressure provenance source_id must be a non-empty string.")
    if region_id is not None and source_id != region_id:
        raise ValueError(
            "Pressure provenance source_id must equal the containing region_id."
        )


def validate_initial_pressures(region: Dict[str, Any]) -> None:
    if "initial_pressures" not in region:
        return

    initial_pressures = region["initial_pressures"]
    if not isinstance(initial_pressures, list):
        raise ValueError("initial_pressures must be a list.")

    region_id = region.get("region_id")
    location_ids = {
        location.get("location_id")
        for location in region.get("locations", [])
        if isinstance(location, dict)
    }
    seen_ids = set()

    for index, pressure in enumerate(initial_pressures):
        try:
            validate_pressure_record(pressure, region_id, location_ids)
        except ValueError as error:
            raise ValueError(f"initial_pressures[{index}]: {error}") from error

        pressure_id = pressure["pressure_id"]
        if pressure_id in seen_ids:
            raise ValueError(f"Duplicate pressure_id: {pressure_id}.")
        seen_ids.add(pressure_id)


def build_initial_pressure_state(region: Dict[str, Any]) -> dict[str, dict]:
    validate_initial_pressures(region)
    return {
        pressure["pressure_id"]: deepcopy(pressure)
        for pressure in region.get("initial_pressures", [])
    }


def validate_pressure_state(
    pressures: Any,
    region: Dict[str, Any] | None = None,
) -> None:
    if not isinstance(pressures, dict):
        raise ValueError("World State pressures must be a dictionary.")

    region_id = region.get("region_id") if region is not None else None
    location_ids = None
    if region is not None:
        location_ids = {
            location.get("location_id")
            for location in region.get("locations", [])
            if isinstance(location, dict)
        }

    pressure_ids = list(pressures)
    if any(
        not isinstance(pressure_id, str) or not pressure_id
        for pressure_id in pressure_ids
    ):
        raise ValueError("World State pressure keys must be non-empty strings.")

    for pressure_id in sorted(pressure_ids):
        pressure = pressures[pressure_id]
        validate_pressure_record(pressure, region_id, location_ids)
        if pressure_id != pressure["pressure_id"]:
            raise ValueError(
                "World State pressure key must match the record pressure_id."
            )


def get_pressures(world_state: Dict[str, Any]) -> dict[str, dict]:
    return deepcopy(world_state["pressures"])


def get_pressure(
    world_state: Dict[str, Any],
    pressure_id: str,
) -> dict | None:
    pressure = world_state["pressures"].get(pressure_id)
    return deepcopy(pressure) if pressure is not None else None


def prepare_pressure_level_change(
    pressures: Any,
    pressure_id: str,
    new_level: int,
) -> tuple[dict[str, dict], dict[str, Any]]:
    validate_pressure_state(pressures)

    if pressure_id not in pressures:
        raise ValueError("Unknown pressure_id.")

    if isinstance(new_level, bool) or not isinstance(new_level, int):
        raise ValueError("Pressure level must be an integer and not a boolean.")
    if new_level < 0 or new_level > 100:
        raise ValueError("Pressure level must be from 0 through 100.")

    previous_pressure = pressures[pressure_id]
    previous_level = previous_pressure["level"]
    result = {
        "changed": previous_level != new_level,
        "pressure_id": pressure_id,
        "previous_level": previous_level,
        "new_level": new_level,
        "history_id": None,
    }

    if previous_level == new_level:
        return deepcopy(pressures), result

    updated_pressures = deepcopy(pressures)
    updated_pressures[pressure_id]["level"] = new_level

    return updated_pressures, result
