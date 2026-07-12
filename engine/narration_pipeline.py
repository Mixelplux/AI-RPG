from copy import deepcopy
from typing import Any, Callable, Dict

from engine.narration_output import (
    validate_narration_output_packet,
)
from engine.narration_prompt import (
    build_narration_prompt_packet,
    validate_narration_prompt_packet,
)
from engine.narration_request import (
    build_narration_request_packet,
    validate_narration_request_packet,
)
from engine.narration_source import (
    NARRATION_SOURCE_FIXED_SAMPLE,
    NARRATION_SOURCE_SCHEMA,
    NARRATION_SOURCE_VERSION,
    build_fixed_sample_narration_source_result,
    validate_narration_source_result_packet,
)


NARRATION_PIPELINE_SCHEMA = "ai_rpg.narration_pipeline_packet"
NARRATION_PIPELINE_VERSION = 1
NARRATION_PIPELINE_SOURCE = NARRATION_SOURCE_FIXED_SAMPLE

NarrationSourceBuilder = Callable[[Dict[str, Any]], Dict[str, Any]]
NarrationRequestBuilder = Callable[[Dict[str, Any]], Dict[str, Any]]
NarrationPromptBuilder = Callable[[Dict[str, Any]], Dict[str, Any]]


def build_narration_preview_packet(
    narration_context: Dict[str, Any],
    source_builder: NarrationSourceBuilder = (
        build_fixed_sample_narration_source_result
    ),
    request_builder: NarrationRequestBuilder = build_narration_request_packet,
    prompt_builder: NarrationPromptBuilder = build_narration_prompt_packet,
) -> Dict[str, Any]:
    try:
        narration_request = request_builder(deepcopy(narration_context))
    except ValueError as error:
        return build_narration_preview_failure_packet(
            narration_context,
            {},
            "request_construction",
            str(error),
            narration_request={},
            source_result={},
        )
    except Exception as error:
        return build_narration_preview_failure_packet(
            narration_context,
            {},
            "request_construction",
            _bounded_error_message(error),
            narration_request={},
            source_result={},
        )

    try:
        narration_request = validate_narration_request_packet(
            narration_request
        )
    except ValueError as error:
        return build_narration_preview_failure_packet(
            narration_context,
            {},
            "request_validation",
            str(error),
            narration_request=_copy_request_if_present(narration_request),
            narration_prompt={},
            source_result={},
        )

    try:
        narration_prompt = prompt_builder(deepcopy(narration_request))
    except ValueError as error:
        return build_narration_preview_failure_packet(
            narration_context,
            {},
            "prompt_construction",
            str(error),
            narration_request=narration_request,
            narration_prompt={},
            source_result={},
        )
    except Exception as error:
        return build_narration_preview_failure_packet(
            narration_context,
            {},
            "prompt_construction",
            _bounded_error_message(error),
            narration_request=narration_request,
            narration_prompt={},
            source_result={},
        )

    try:
        narration_prompt = validate_narration_prompt_packet(
            narration_prompt
        )
    except ValueError as error:
        return build_narration_preview_failure_packet(
            narration_context,
            {},
            "prompt_validation",
            str(error),
            narration_request=narration_request,
            narration_prompt=_copy_prompt_if_present(narration_prompt),
            source_result={},
        )

    try:
        source_result = source_builder(deepcopy(narration_prompt))
    except Exception as error:
        return build_narration_preview_failure_packet(
            narration_context,
            {},
            "source_exception",
            _bounded_error_message(error),
            narration_request=narration_request,
            narration_prompt=narration_prompt,
            source_result={},
        )

    try:
        source_result = validate_narration_source_result_packet(
            source_result,
            narration_prompt,
        )
    except ValueError as error:
        return build_narration_preview_failure_packet(
            narration_context,
            {},
            "source_result_validation",
            str(error),
            narration_request=narration_request,
            narration_prompt=narration_prompt,
            source_result={},
        )

    candidate = deepcopy(source_result["candidate"])
    return _build_preview_from_candidate(
        narration_context,
        candidate,
        narration_request=narration_request,
        narration_prompt=narration_prompt,
        source_result=source_result,
    )


def build_narration_preview_failure_packet(
    narration_context: Dict[str, Any],
    candidate: Dict[str, Any],
    failure_stage: str,
    error: str,
    narration_request: Dict[str, Any] | None = None,
    narration_prompt: Dict[str, Any] | None = None,
    source_result: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    return {
        "schema": NARRATION_PIPELINE_SCHEMA,
        "version": NARRATION_PIPELINE_VERSION,
        "accepted": False,
        "source": NARRATION_PIPELINE_SOURCE,
        "narration_context": deepcopy(narration_context),
        "narration_request": deepcopy(narration_request or {}),
        "narration_prompt": deepcopy(narration_prompt or {}),
        "candidate": deepcopy(candidate),
        "source_result": deepcopy(source_result or {}),
        "failure_stage": failure_stage,
        "error": error,
        "display_text": "",
    }


def validate_narration_preview_candidate(
    narration_context: Dict[str, Any],
    candidate: Dict[str, Any],
) -> Dict[str, Any]:
    narration_request = build_narration_request_packet(narration_context)
    narration_prompt = build_narration_prompt_packet(narration_request)
    source_result = {
        "schema": NARRATION_SOURCE_SCHEMA,
        "version": NARRATION_SOURCE_VERSION,
        "source": NARRATION_SOURCE_FIXED_SAMPLE,
        "source_prompt": deepcopy(narration_prompt),
        "candidate": deepcopy(candidate),
        "metadata": {
            "candidate_trust": "untrusted",
            "generation": "fixed_sample_only",
        },
    }
    return _build_preview_from_candidate(
        narration_context,
        candidate,
        narration_request=narration_request,
        narration_prompt=narration_prompt,
        source_result=source_result,
    )


def _build_preview_from_candidate(
    narration_context: Dict[str, Any],
    candidate: Dict[str, Any],
    narration_request: Dict[str, Any],
    narration_prompt: Dict[str, Any],
    source_result: Dict[str, Any],
) -> Dict[str, Any]:
    try:
        validated_output = validate_narration_output_packet(candidate)
    except ValueError as error:
        return build_narration_preview_failure_packet(
            narration_context,
            candidate,
            "candidate_validation",
            str(error),
            narration_request=narration_request,
            narration_prompt=narration_prompt,
            source_result=source_result,
        )

    pressure_cue = narration_context["pressure_cue"]
    if pressure_cue:
        cue_text = pressure_cue["text"]
        base_text = validated_output["narration_text"].replace(cue_text, "")
        base_text = base_text.strip()
        composed_text = f"{base_text} {cue_text}" if base_text else cue_text
        validated_output = validate_narration_output_packet({
            "schema": validated_output["schema"],
            "version": validated_output["version"],
            "narration_text": composed_text,
        })

    return {
        "schema": NARRATION_PIPELINE_SCHEMA,
        "version": NARRATION_PIPELINE_VERSION,
        "accepted": True,
        "source": NARRATION_PIPELINE_SOURCE,
        "narration_context": deepcopy(narration_context),
        "narration_request": deepcopy(narration_request),
        "narration_prompt": deepcopy(narration_prompt),
        "candidate": deepcopy(candidate),
        "source_result": deepcopy(source_result),
        "validated_output": deepcopy(validated_output),
        "display_text": validated_output["narration_text"],
    }


def _copy_request_if_present(narration_request: Any) -> Dict[str, Any]:
    if isinstance(narration_request, dict):
        return deepcopy(narration_request)

    return {}


def _copy_prompt_if_present(narration_prompt: Any) -> Dict[str, Any]:
    if isinstance(narration_prompt, dict):
        return deepcopy(narration_prompt)

    return {}


def _bounded_error_message(error: Exception) -> str:
    message = str(error) or error.__class__.__name__
    if len(message) > 160:
        return f"{message[:157]}..."
    return message
