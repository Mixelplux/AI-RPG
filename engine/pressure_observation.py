from copy import deepcopy
from typing import Any


def derive_pressure_observation(
    applicable_pressures: dict[str, dict],
    declaration: dict[str, Any] | None,
) -> dict[str, str] | None:
    if declaration is None:
        return None
    pressure = applicable_pressures.get(declaration["pressure_id"])
    if pressure is None or pressure["level"] < declaration["minimum_level"]:
        return None
    return deepcopy({
        "cue_id": declaration["cue_id"],
        "pressure_id": declaration["pressure_id"],
        "text": declaration["text"],
    })
