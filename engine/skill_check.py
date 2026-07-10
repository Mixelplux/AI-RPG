from typing import TypedDict


class SkillCheckResult(TypedDict):
    check_name: str
    target_difficulty: int
    result_value: int
    succeeded: bool


def resolve_skill_check(
    check_name: str,
    target_difficulty: int,
    result_value: int,
) -> SkillCheckResult:
    """Resolve a deterministic skill check and return its structured result."""

    normalized_name = check_name.strip()
    if not normalized_name:
        raise ValueError("check_name must not be empty")

    return {
        "check_name": normalized_name,
        "target_difficulty": target_difficulty,
        "result_value": result_value,
        "succeeded": result_value >= target_difficulty,
    }
