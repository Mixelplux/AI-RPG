from copy import deepcopy
from typing import Any, Dict


NARRATION_OUTPUT_SCHEMA = "ai_rpg.narration_output_packet"
NARRATION_OUTPUT_VERSION = 1

NARRATION_OUTPUT_RULE = (
    "The narrator can describe. The engine decides what is true."
)
NARRATION_OUTPUT_AUTHORITY = (
    "Narration output is presentational prose only and is not accepted world "
    "truth."
)
NARRATION_OUTPUT_DRIFT_LIMIT = (
    "Freeform narration drift is controlled by context limits, prompt rules, "
    "this output contract, and later review or validation layers; this "
    "contract does not attempt to fully prove whether prose contains invented "
    "details."
)
NARRATION_OUTPUT_ATMOSPHERE_EXAMPLE = (
    "Narration may describe a blizzard if the context contains a blizzard, "
    "but should not mention gloves unless gloves are present in context."
)

ALLOWED_NARRATION_OUTPUT_KEYS = frozenset({
    "schema",
    "version",
    "narration_text",
})

FORBIDDEN_STRUCTURED_OUTPUT_KEYS = frozenset({
    "actor_knowledge",
    "advance_time",
    "consequence",
    "consequences",
    "create_history",
    "durable_fact",
    "durable_facts",
    "evidence",
    "exit",
    "exits",
    "history",
    "history_entry",
    "history_entries",
    "history_mutation",
    "history_mutations",
    "inventory",
    "location",
    "locations",
    "mutation",
    "mutations",
    "new_entities",
    "new_entity",
    "npc_relationship",
    "npc_relationships",
    "npc_schedule",
    "npc_schedules",
    "player_condition",
    "player_conditions",
    "pressure",
    "pressures",
    "quest",
    "quests",
    "relationship_state",
    "rumor",
    "rumors",
    "schedule",
    "schedules",
    "time_advance",
    "time_advancement",
    "world_state",
    "world_state_mutation",
    "world_state_mutations",
})


def build_narration_output_contract() -> Dict[str, Any]:
    return {
        "schema": NARRATION_OUTPUT_SCHEMA,
        "version": NARRATION_OUTPUT_VERSION,
        "type": "read_only_narration_output_contract",
        "allowed_fields": sorted(ALLOWED_NARRATION_OUTPUT_KEYS),
        "required_fields": [
            "schema",
            "version",
            "narration_text",
        ],
        "forbidden_structured_fields": sorted(
            FORBIDDEN_STRUCTURED_OUTPUT_KEYS
        ),
        "rule": NARRATION_OUTPUT_RULE,
        "authority": NARRATION_OUTPUT_AUTHORITY,
        "drift_limit": NARRATION_OUTPUT_DRIFT_LIMIT,
        "atmosphere_example": NARRATION_OUTPUT_ATMOSPHERE_EXAMPLE,
    }


def build_narration_output_packet(narration_text: str) -> Dict[str, Any]:
    if not isinstance(narration_text, str):
        raise ValueError("Narration text must be a string.")

    return {
        "schema": NARRATION_OUTPUT_SCHEMA,
        "version": NARRATION_OUTPUT_VERSION,
        "narration_text": narration_text,
        "contract": build_narration_output_contract(),
    }


def validate_narration_output_packet(
    narration_output: Dict[str, Any]
) -> Dict[str, Any]:
    if not isinstance(narration_output, dict):
        raise ValueError("Narration output must be an object.")

    _reject_forbidden_structured_fields(narration_output)

    extra_keys = set(narration_output) - ALLOWED_NARRATION_OUTPUT_KEYS
    if extra_keys:
        raise ValueError(
            "Narration output contains unsupported structured fields: "
            f"{', '.join(sorted(extra_keys))}."
        )

    if narration_output.get("schema") != NARRATION_OUTPUT_SCHEMA:
        raise ValueError("Narration output schema is not supported.")

    if narration_output.get("version") != NARRATION_OUTPUT_VERSION:
        raise ValueError("Narration output version is not supported.")

    narration_text = narration_output.get("narration_text")
    if not isinstance(narration_text, str):
        raise ValueError("Narration text must be a string.")

    return build_narration_output_packet(narration_text)


def _reject_forbidden_structured_fields(value: Any) -> None:
    if isinstance(value, dict):
        for key, child_value in value.items():
            normalized_key = str(key).lower()
            if normalized_key in FORBIDDEN_STRUCTURED_OUTPUT_KEYS:
                raise ValueError(
                    "Narration output may not include structured mutation "
                    f"field: {key}."
                )
            _reject_forbidden_structured_fields(child_value)
        return

    if isinstance(value, list):
        for item in value:
            _reject_forbidden_structured_fields(item)


def copy_narration_output_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    return deepcopy(packet)
