"""The single isolated OpenAI Responses narration-preview adapter."""

from copy import deepcopy
import json
import os
from typing import Any, Callable, Dict

import tiktoken
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

from engine.narration_output import NARRATION_OUTPUT_SCHEMA, NARRATION_OUTPUT_VERSION
from engine.narration_prompt import validate_narration_prompt_packet

NARRATION_SOURCE_SCHEMA = "ai_rpg.narration_source_result"
NARRATION_SOURCE_VERSION = 1
NARRATION_SOURCE_OPENAI_RESPONSES = "openai_responses_preview"
NARRATION_SOURCE_REQUIRED_KEYS = frozenset({"schema", "version", "source", "source_prompt", "candidate", "metadata"})
NARRATION_SOURCE_METADATA = {"candidate_trust": "untrusted", "generation": "provider_generated", "provider": "openai", "api": "responses", "model": "gpt-4.1-mini"}
OPENAI_MODEL = "gpt-4.1-mini"
OPENAI_TIMEOUT_SECONDS = 20.0
OPENAI_MAX_OUTPUT_TOKENS = 256
OPENAI_MAX_INPUT_TOKENS = 8000
OPENAI_MAX_OUTPUT_CHARACTERS = 4000


class NarrationProviderError(Exception):
    def __init__(self, stage: str, reason: str = ""):
        self.stage = stage
        self.reason = reason
        super().__init__(stage)


def _provider_text(prompt: Dict[str, Any]) -> tuple[str, str]:
    validated = validate_narration_prompt_packet(prompt)
    instructions = json.dumps(validated["instructions"], sort_keys=True, separators=(",", ":"))
    input_text = json.dumps(validated["deterministic_input"], sort_keys=True, separators=(",", ":"))
    encoding = tiktoken.encoding_for_model(OPENAI_MODEL)
    if len(encoding.encode(instructions)) + len(encoding.encode(input_text)) > OPENAI_MAX_INPUT_TOKENS:
        raise NarrationProviderError("provider_input_limit")
    return instructions, input_text


def build_openai_responses_narration_source_result(
    narration_prompt: Dict[str, Any],
    transport: Callable[[Any, Dict[str, Any]], Any] | None = None,
) -> Dict[str, Any]:
    """Adapt validated neutral prompt material through one synchronous source."""
    prompt_copy = validate_narration_prompt_packet(narration_prompt)
    api_key = os.environ.get("OPENAI_API_KEY")
    if not isinstance(api_key, str) or not api_key.strip():
        raise NarrationProviderError("provider_configuration")
    instructions, input_text = _provider_text(prompt_copy)
    request = {"model": OPENAI_MODEL, "instructions": instructions, "input": input_text, "max_output_tokens": OPENAI_MAX_OUTPUT_TOKENS, "store": False}
    try:
        client = OpenAI(api_key=api_key, timeout=OPENAI_TIMEOUT_SECONDS, max_retries=0)
        response = (transport or (lambda c, r: c.responses.create(**r)))(client, request)
    except APITimeoutError:
        raise NarrationProviderError("provider_timeout") from None
    except (APIConnectionError, APIStatusError):
        raise NarrationProviderError("provider_request") from None
    except NarrationProviderError:
        raise
    except Exception:
        raise NarrationProviderError("provider_request") from None
    text = getattr(response, "output_text", None)
    status = getattr(response, "status", None)
    if status == "incomplete":
        detail = getattr(getattr(response, "incomplete_details", None), "reason", None)
        raise NarrationProviderError("provider_response", "incomplete_max_output_tokens" if detail == "max_output_tokens" else "incomplete_content_filter")
    if status == "failed":
        raise NarrationProviderError("provider_response", "failed_status")
    if status != "completed":
        raise NarrationProviderError("provider_response", "unexpected_response_shape")
    if any(
        getattr(content, "type", None) == "refusal"
        for item in (getattr(response, "output", None) or [])
        for content in (getattr(item, "content", None) or [])
    ):
        raise NarrationProviderError("provider_response", "refusal")
    if not isinstance(text, str) or not text.strip():
        raise NarrationProviderError("provider_response", "empty_output")
    if len(text) > OPENAI_MAX_OUTPUT_CHARACTERS:
        raise NarrationProviderError("provider_response", "unexpected_response_shape")
    return {"schema": NARRATION_SOURCE_SCHEMA, "version": NARRATION_SOURCE_VERSION, "source": NARRATION_SOURCE_OPENAI_RESPONSES, "source_prompt": deepcopy(prompt_copy), "candidate": {"schema": NARRATION_OUTPUT_SCHEMA, "version": NARRATION_OUTPUT_VERSION, "narration_text": text}, "metadata": deepcopy(NARRATION_SOURCE_METADATA)}


def validate_narration_source_result_packet(source_result: Dict[str, Any], originating_prompt: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(source_result, dict) or set(source_result) != NARRATION_SOURCE_REQUIRED_KEYS:
        raise ValueError("Narration source result fields are not supported.")
    if source_result.get("schema") != NARRATION_SOURCE_SCHEMA or source_result.get("version") != NARRATION_SOURCE_VERSION or source_result.get("source") != NARRATION_SOURCE_OPENAI_RESPONSES:
        raise ValueError("Narration source result identity is not supported.")
    prompt = validate_narration_prompt_packet(source_result["source_prompt"])
    if prompt != validate_narration_prompt_packet(originating_prompt):
        raise ValueError("Narration source result prompt does not match the originating prompt.")
    if not isinstance(source_result.get("candidate"), dict) or source_result.get("metadata") != NARRATION_SOURCE_METADATA:
        raise ValueError("Narration source result content is not supported.")
    return {"schema": NARRATION_SOURCE_SCHEMA, "version": NARRATION_SOURCE_VERSION, "source": NARRATION_SOURCE_OPENAI_RESPONSES, "source_prompt": deepcopy(prompt), "candidate": deepcopy(source_result["candidate"]), "metadata": deepcopy(NARRATION_SOURCE_METADATA)}
