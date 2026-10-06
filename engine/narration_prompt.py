from copy import deepcopy
from typing import Any, Dict

from engine.narration_output import (
    NARRATION_OUTPUT_SCHEMA,
    NARRATION_OUTPUT_VERSION,
)
from engine.narration_request import (
    NARRATION_REQUEST_MODE,
    NARRATION_REQUEST_SCHEMA,
    NARRATION_REQUEST_VERSION,
    validate_narration_request_packet,
)
from engine.scene_context import SCENE_NARRATION_CONTRACT, validate_scene_context


NARRATION_PROMPT_SCHEMA = "ai_rpg.narration_prompt_packet"
NARRATION_PROMPT_VERSION = 1
NARRATION_PROMPT_MODE = "preview"

NARRATION_PROMPT_INSTRUCTIONS = {
    "authority_rule": "The narrator can describe. The engine decides what is true.",
    "output_format": "prose_only",
    "simulation_truth": "description_only_no_decisions",
    "state_mutation": "forbidden",
    "time_advancement": "forbidden",
    "history_creation": "forbidden",
    "persistence_claims": "forbidden",
    "structured_simulation_commands": "forbidden",
    "provider_payload": "forbidden",
    "scene_narration_contract": SCENE_NARRATION_CONTRACT,
}

REQUIRED_PROMPT_KEYS = frozenset({
    "schema",
    "version",
    "mode",
    "originating_request",
    "expected_output",
    "instructions",
    "deterministic_input",
})

REQUIRED_PROMPT_INPUT_KEYS = frozenset({
    "player_input",
    "current_time",
    "player",
    "scene_snapshot",
    "scene_context",
    "history_context",
    "pressure_cue",
    "boundary",
    "constraints",
})


def build_narration_prompt_packet(
    narration_request: Dict[str, Any],
) -> Dict[str, Any]:
    """Build provider-neutral prompt material from a validated request."""

    request_copy = validate_narration_request_packet(narration_request)
    context = request_copy["narration_context"]

    return {
        "schema": NARRATION_PROMPT_SCHEMA,
        "version": NARRATION_PROMPT_VERSION,
        "mode": NARRATION_PROMPT_MODE,
        "originating_request": {
            "schema": request_copy["schema"],
            "version": request_copy["version"],
            "mode": request_copy["mode"],
        },
        "expected_output": {
            "schema": NARRATION_OUTPUT_SCHEMA,
            "version": NARRATION_OUTPUT_VERSION,
            "format": "prose_only",
        },
        "instructions": deepcopy(NARRATION_PROMPT_INSTRUCTIONS),
        "deterministic_input": {
            "player_input": context["player_input"],
            "current_time": deepcopy(context["current_time"]),
            "player": deepcopy(context["player"]),
            "scene_snapshot": deepcopy(context["scene_snapshot"]),
            "scene_context": deepcopy(context["scene_context"]),
            "history_context": deepcopy(context["history_context"]),
            "pressure_cue": deepcopy(context["pressure_cue"]),
            "boundary": deepcopy(context["boundary"]),
            "constraints": deepcopy(request_copy["constraints"]),
        },
    }


def validate_narration_prompt_packet(
    narration_prompt: Dict[str, Any],
) -> Dict[str, Any]:
    if not isinstance(narration_prompt, dict):
        raise ValueError("Narration prompt must be an object.")

    missing_keys = REQUIRED_PROMPT_KEYS - set(narration_prompt)
    if missing_keys:
        raise ValueError(
            "Narration prompt is missing required fields: "
            f"{', '.join(sorted(missing_keys))}."
        )

    extra_keys = set(narration_prompt) - REQUIRED_PROMPT_KEYS
    if extra_keys:
        raise ValueError(
            "Narration prompt contains unsupported fields: "
            f"{', '.join(sorted(extra_keys))}."
        )

    if narration_prompt.get("schema") != NARRATION_PROMPT_SCHEMA:
        raise ValueError("Narration prompt schema is not supported.")

    if narration_prompt.get("version") != NARRATION_PROMPT_VERSION:
        raise ValueError("Narration prompt version is not supported.")

    if narration_prompt.get("mode") != NARRATION_PROMPT_MODE:
        raise ValueError("Narration prompt mode is not supported.")

    originating_request = narration_prompt.get("originating_request")
    if not isinstance(originating_request, dict):
        raise ValueError("Narration prompt originating request must be an object.")

    if originating_request.get("schema") != NARRATION_REQUEST_SCHEMA:
        raise ValueError("Narration prompt request schema is not supported.")

    if originating_request.get("version") != NARRATION_REQUEST_VERSION:
        raise ValueError("Narration prompt request version is not supported.")

    if originating_request.get("mode") != NARRATION_REQUEST_MODE:
        raise ValueError("Narration prompt request mode is not supported.")

    expected_output = narration_prompt.get("expected_output")
    if not isinstance(expected_output, dict):
        raise ValueError("Narration prompt expected output must be an object.")

    if expected_output.get("schema") != NARRATION_OUTPUT_SCHEMA:
        raise ValueError("Narration prompt expected output schema is not supported.")

    if expected_output.get("version") != NARRATION_OUTPUT_VERSION:
        raise ValueError("Narration prompt expected output version is not supported.")

    if expected_output.get("format") != "prose_only":
        raise ValueError("Narration prompt expected output format is not supported.")

    if narration_prompt.get("instructions") != NARRATION_PROMPT_INSTRUCTIONS:
        raise ValueError("Narration prompt instructions are not supported.")

    deterministic_input = narration_prompt.get("deterministic_input")
    _validate_prompt_input_shape(deterministic_input)

    return deepcopy(narration_prompt)


def copy_narration_prompt_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    return deepcopy(packet)


def _validate_prompt_input_shape(deterministic_input: Any) -> None:
    if not isinstance(deterministic_input, dict):
        raise ValueError("Narration prompt deterministic input must be an object.")

    missing_keys = REQUIRED_PROMPT_INPUT_KEYS - set(deterministic_input)
    if missing_keys:
        raise ValueError(
            "Narration prompt deterministic input is missing required fields: "
            f"{', '.join(sorted(missing_keys))}."
        )

    extra_keys = set(deterministic_input) - REQUIRED_PROMPT_INPUT_KEYS
    if extra_keys:
        raise ValueError(
            "Narration prompt deterministic input contains unsupported fields: "
            f"{', '.join(sorted(extra_keys))}."
        )

    pressure_cue = deterministic_input.get("pressure_cue")
    validate_scene_context(deterministic_input.get("scene_context"))
    if not isinstance(pressure_cue, dict):
        raise ValueError("Narration prompt pressure cue must be an object.")
    if pressure_cue and (
        set(pressure_cue) != {"cue_id", "pressure_id", "text"}
        or any(
            not isinstance(pressure_cue.get(field), str)
            or not pressure_cue[field]
            for field in ("cue_id", "pressure_id", "text")
        )
    ):
        raise ValueError("Narration prompt pressure cue is malformed.")

    if not isinstance(deterministic_input.get("current_time"), dict):
        raise ValueError("Narration prompt current time must be an object.")

    if not isinstance(deterministic_input.get("player"), dict):
        raise ValueError("Narration prompt player must be an object.")

    if "current_location_id" not in deterministic_input["player"]:
        raise ValueError(
            "Narration prompt player is missing current_location_id."
        )

    if not isinstance(deterministic_input.get("scene_snapshot"), dict):
        raise ValueError("Narration prompt scene snapshot must be an object.")

    if not isinstance(deterministic_input.get("history_context"), dict):
        raise ValueError("Narration prompt history context must be an object.")

    if not isinstance(deterministic_input.get("boundary"), dict):
        raise ValueError("Narration prompt boundary must be an object.")

    if not isinstance(deterministic_input.get("constraints"), dict):
        raise ValueError("Narration prompt constraints must be an object.")
