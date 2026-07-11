from copy import deepcopy
from typing import Any, Dict

from engine.narration_output import (
    NARRATION_OUTPUT_SCHEMA,
    NARRATION_OUTPUT_VERSION,
)
from engine.narration_prompt import validate_narration_prompt_packet


NARRATION_SOURCE_SCHEMA = "ai_rpg.narration_source_result"
NARRATION_SOURCE_VERSION = 1
NARRATION_SOURCE_FIXED_SAMPLE = "fixed_sample_prose"
NARRATION_SOURCE_SAMPLE_PROSE = "The street remains quiet."
NARRATION_SOURCE_REQUIRED_KEYS = frozenset({
    "schema",
    "version",
    "source",
    "source_prompt",
    "candidate",
    "metadata",
})
NARRATION_SOURCE_METADATA = {
    "candidate_trust": "untrusted",
    "generation": "fixed_sample_only",
}


def build_fixed_sample_narration_source_result(
    narration_prompt: Dict[str, Any],
) -> Dict[str, Any]:
    """Return an untrusted fixed narration candidate from copied prompt."""

    prompt_copy = validate_narration_prompt_packet(narration_prompt)
    candidate = {
        "schema": NARRATION_OUTPUT_SCHEMA,
        "version": NARRATION_OUTPUT_VERSION,
        "narration_text": NARRATION_SOURCE_SAMPLE_PROSE,
    }

    return {
        "schema": NARRATION_SOURCE_SCHEMA,
        "version": NARRATION_SOURCE_VERSION,
        "source": NARRATION_SOURCE_FIXED_SAMPLE,
        "source_prompt": prompt_copy,
        "candidate": deepcopy(candidate),
        "metadata": deepcopy(NARRATION_SOURCE_METADATA),
    }


def validate_narration_source_result_packet(
    source_result: Dict[str, Any],
    originating_prompt: Dict[str, Any],
) -> Dict[str, Any]:
    if not isinstance(source_result, dict):
        raise ValueError("Narration source result must be an object.")

    missing_keys = NARRATION_SOURCE_REQUIRED_KEYS - set(source_result)
    if missing_keys:
        raise ValueError(
            "Narration source result is missing required fields: "
            f"{', '.join(sorted(missing_keys))}."
        )

    extra_keys = set(source_result) - NARRATION_SOURCE_REQUIRED_KEYS
    if extra_keys:
        raise ValueError(
            "Narration source result contains unsupported fields: "
            f"{', '.join(sorted(extra_keys))}."
        )

    if source_result.get("schema") != NARRATION_SOURCE_SCHEMA:
        raise ValueError("Narration source result schema is not supported.")

    if source_result.get("version") != NARRATION_SOURCE_VERSION:
        raise ValueError("Narration source result version is not supported.")

    if source_result.get("source") != NARRATION_SOURCE_FIXED_SAMPLE:
        raise ValueError("Narration source result source is not supported.")

    validated_originating_prompt = validate_narration_prompt_packet(
        originating_prompt
    )
    validated_source_prompt = validate_narration_prompt_packet(
        source_result["source_prompt"]
    )
    if validated_source_prompt != validated_originating_prompt:
        raise ValueError(
            "Narration source result prompt does not match the originating "
            "prompt."
        )

    candidate = source_result.get("candidate")
    if not isinstance(candidate, dict):
        raise ValueError("Narration source result candidate must be an object.")

    metadata = source_result.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError("Narration source result metadata must be an object.")

    missing_metadata_keys = set(NARRATION_SOURCE_METADATA) - set(metadata)
    if missing_metadata_keys:
        raise ValueError(
            "Narration source result metadata is missing required fields: "
            f"{', '.join(sorted(missing_metadata_keys))}."
        )

    extra_metadata_keys = set(metadata) - set(NARRATION_SOURCE_METADATA)
    if extra_metadata_keys:
        raise ValueError(
            "Narration source result metadata contains unsupported fields: "
            f"{', '.join(sorted(extra_metadata_keys))}."
        )

    if metadata != NARRATION_SOURCE_METADATA:
        raise ValueError("Narration source result metadata is not supported.")

    return {
        "schema": NARRATION_SOURCE_SCHEMA,
        "version": NARRATION_SOURCE_VERSION,
        "source": NARRATION_SOURCE_FIXED_SAMPLE,
        "source_prompt": deepcopy(validated_source_prompt),
        "candidate": deepcopy(candidate),
        "metadata": deepcopy(NARRATION_SOURCE_METADATA),
    }
