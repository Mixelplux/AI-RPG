from copy import deepcopy
from typing import Any, Dict

from engine.narration_context import (
    NARRATION_CONTEXT_SCHEMA,
    NARRATION_CONTEXT_VERSION,
)
from engine.narration_output import (
    NARRATION_OUTPUT_SCHEMA,
    NARRATION_OUTPUT_VERSION,
    build_narration_output_contract,
)
from engine.scene_context import validate_scene_context


NARRATION_REQUEST_SCHEMA = "ai_rpg.narration_request_packet"
NARRATION_REQUEST_VERSION = 1
NARRATION_REQUEST_MODE = "preview"

NARRATION_REQUEST_CONSTRAINTS = {
    "authority_rule": "The narrator can describe. The engine decides what is true.",
    "candidate_output": "prose_only",
    "state_mutation": "forbidden",
    "time_advancement": "forbidden",
    "history_creation": "forbidden",
    "persistence_claims": "forbidden",
    "provider_payload": "forbidden",
}

REQUIRED_NARRATION_CONTEXT_KEYS = frozenset({
    "schema",
    "version",
    "player_input",
    "current_time",
    "player",
    "scene_snapshot",
    "scene_context",
    "history_context",
    "pressure_cue",
    "boundary",
})

REQUIRED_REQUEST_KEYS = frozenset({
    "schema",
    "version",
    "mode",
    "narration_context",
    "expected_output",
    "constraints",
})


def build_narration_request_packet(
    narration_context: Dict[str, Any],
) -> Dict[str, Any]:
    """Build a provider-neutral request from an existing context packet."""

    _validate_narration_context_shape(narration_context)

    return {
        "schema": NARRATION_REQUEST_SCHEMA,
        "version": NARRATION_REQUEST_VERSION,
        "mode": NARRATION_REQUEST_MODE,
        "narration_context": deepcopy(narration_context),
        "expected_output": {
            "schema": NARRATION_OUTPUT_SCHEMA,
            "version": NARRATION_OUTPUT_VERSION,
            "contract": build_narration_output_contract(),
        },
        "constraints": deepcopy(NARRATION_REQUEST_CONSTRAINTS),
    }


def validate_narration_request_packet(
    narration_request: Dict[str, Any],
) -> Dict[str, Any]:
    if not isinstance(narration_request, dict):
        raise ValueError("Narration request must be an object.")

    missing_keys = REQUIRED_REQUEST_KEYS - set(narration_request)
    if missing_keys:
        raise ValueError(
            "Narration request is missing required fields: "
            f"{', '.join(sorted(missing_keys))}."
        )

    if narration_request.get("schema") != NARRATION_REQUEST_SCHEMA:
        raise ValueError("Narration request schema is not supported.")

    if narration_request.get("version") != NARRATION_REQUEST_VERSION:
        raise ValueError("Narration request version is not supported.")

    if narration_request.get("mode") != NARRATION_REQUEST_MODE:
        raise ValueError("Narration request mode is not supported.")

    expected_output = narration_request.get("expected_output")
    if not isinstance(expected_output, dict):
        raise ValueError("Narration request expected output must be an object.")

    if expected_output.get("schema") != NARRATION_OUTPUT_SCHEMA:
        raise ValueError("Narration request expected output schema is not supported.")

    if expected_output.get("version") != NARRATION_OUTPUT_VERSION:
        raise ValueError("Narration request expected output version is not supported.")

    if not isinstance(expected_output.get("contract"), dict):
        raise ValueError("Narration request expected output contract must be an object.")

    if narration_request.get("constraints") != NARRATION_REQUEST_CONSTRAINTS:
        raise ValueError("Narration request constraints are not supported.")

    _validate_narration_context_shape(narration_request.get("narration_context"))

    return deepcopy(narration_request)


def copy_narration_request_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    return deepcopy(packet)


def _validate_narration_context_shape(narration_context: Any) -> None:
    if not isinstance(narration_context, dict):
        raise ValueError("Narration context must be an object.")

    missing_keys = REQUIRED_NARRATION_CONTEXT_KEYS - set(narration_context)
    if missing_keys:
        raise ValueError(
            "Narration context is missing required fields: "
            f"{', '.join(sorted(missing_keys))}."
        )

    if narration_context.get("schema") != NARRATION_CONTEXT_SCHEMA:
        raise ValueError("Narration context schema is not supported.")

    if narration_context.get("version") != NARRATION_CONTEXT_VERSION:
        raise ValueError("Narration context version is not supported.")

    extra_keys = set(narration_context) - REQUIRED_NARRATION_CONTEXT_KEYS
    if extra_keys:
        raise ValueError(
            "Narration context contains unsupported fields: "
            f"{', '.join(sorted(extra_keys))}."
        )

    _validate_pressure_cue(narration_context.get("pressure_cue"))
    validate_scene_context(narration_context.get("scene_context"))

    if not isinstance(narration_context.get("history_context"), dict):
        raise ValueError("Narration context history context must be an object.")

    if not isinstance(narration_context.get("scene_snapshot"), dict):
        raise ValueError("Narration context scene snapshot must be an object.")

    player = narration_context.get("player")
    if not isinstance(player, dict):
        raise ValueError("Narration context player must be an object.")

    if "current_location_id" not in player:
        raise ValueError(
            "Narration context player is missing current_location_id."
        )


def _validate_pressure_cue(pressure_cue: Any) -> None:
    if not isinstance(pressure_cue, dict):
        raise ValueError("Narration context pressure cue must be an object.")
    if not pressure_cue:
        return
    if set(pressure_cue) != {"cue_id", "pressure_id", "text"}:
        raise ValueError(
            "Narration context pressure cue must contain exactly cue_id, "
            "pressure_id, and text."
        )
    if any(
        not isinstance(pressure_cue[field], str) or not pressure_cue[field]
        for field in ("cue_id", "pressure_id", "text")
    ):
        raise ValueError(
            "Narration context pressure cue fields must be non-empty strings."
        )
