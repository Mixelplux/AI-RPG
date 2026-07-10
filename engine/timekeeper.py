from copy import deepcopy
from typing import Any, Dict


def advance_time_by_hours(
    current_time: Dict[str, Any],
    hours: int = 1
) -> Dict[str, Any]:
    if hours <= 0:
        raise ValueError("Time advancement hours must be positive.")

    advanced_time = deepcopy(current_time)
    elapsed_hours = advanced_time.get("elapsed_hours", 0)

    if not isinstance(elapsed_hours, int):
        raise ValueError("World State time.elapsed_hours must be an integer.")

    advanced_time["elapsed_hours"] = elapsed_hours + hours

    return advanced_time
