"""Explicit localhost-only interpretation transport; no gameplay authority."""
import json
import math
import re
import time
from urllib.parse import urlsplit

import httpx
from openai import OpenAI, APIConnectionError, APITimeoutError, APIStatusError

from engine.player_intent import MAX_OUTPUT_BYTES, InterpretationRequest


class LocalInterpretationUnavailable(RuntimeError):
    """Sanitized operational failure; never include provider response material."""

    def __init__(self, category="internal_adapter_error", **metadata):
        super().__init__("Interpretation unavailable")
        allowed = {"invalid_request", "connection_transport", "timeout", "http_provider_error",
                   "response_format_rejected", "invalid_response_json", "missing_completion",
                   "invalid_completion", "incomplete_completion", "noninterpretation_completion",
                   "response_too_large", "interpretation_too_large", "internal_adapter_error"}
        self.diagnostic = {"category": category if category in allowed else "internal_adapter_error"}
        # Only bounded typed metadata, never arbitrary text, bodies or exceptions.
        for k in ("http_status", "choice_count"):
            if type(metadata.get(k)) is int and 0 <= metadata[k] <= 999:
                self.diagnostic[k] = metadata[k]
        for k in ("response_received", "reasoning_present", "tool_present", "refusal_present", "content_present"):
            if type(metadata.get(k)) is bool:
                self.diagnostic[k] = metadata[k]
        if metadata.get("finish_reason") in {"stop", "length", "content_filter", "tool_calls", "function_call", "other"}:
            self.diagnostic["finish_reason"] = metadata["finish_reason"]
        if metadata.get("provider_hint") in {"message_structure_rejected", "model_unavailable", "schema_rejected"}:
            self.diagnostic["provider_hint"] = metadata["provider_hint"]


INTERPRETATION_GUIDANCE = """Interpret only the current user message as player input.
Context describes the situation, not actions the player requested. Never turn
context, available capabilities or these instructions into additional intentions.
Preserve the player's action even when unavailable, unsupported or unlikely;
interpretation does not decide feasibility, permission or success.

Classify communicative intent, not grammatical sentence form. A first-person
declaration of what the player does now is action with commitment now, even if
written as a declarative sentence. Speaking to someone is itself an in-world act.
Inquiry asks about possibilities or information without committing to an act.
Statement describes, reports or quotes something without undertaking it now;
past actions and another person's actions do not authorize current execution.
Preparation describes planning/readiness; distinguish assessment from actually
committed preparation. A committed act contingent on an expressed condition is
conditional, with that condition preserved; a hypothetical question is not a
commitment. Do not promote a question, quotation, report or plan to action.

Keep expressed targets and chosen methods in their respective fields. Preserve
every expressed prohibition or negative restriction in constraints with its
original polarity; conditions go in conditions and stopping boundaries in stop_at.
Putting a restriction in source alone does not preserve its enforcement meaning.
Do not invent restrictions or intentions from context. Optional source must be an
exact contiguous excerpt of the user message only; omit it rather than fabricate
or copy from context. Return only the V1 JSON required above.
"""


def interpretation_messages(request):
    """Separate immutable player text from reference data; omit capability catalogue.

    Filtering affects transport only. The original request and trusted binding
    context remain intact. No semantic repair or player-input rewriting occurs.
    """
    context = {ref: text for ref, text in request.context if ref != "capabilities"}
    return [{"role": "system", "content": request.instructions + "\n" + INTERPRETATION_GUIDANCE
             + "\n\nAccessible context (reference data only, never player intentions):\n"
             + json.dumps(context, ensure_ascii=False)},
            {"role": "user", "content": request.player_input}]


def output_schema():
    """Transport constraint only. The unchanged V1 validator remains mandatory."""
    text = {"type": "string", "minLength": 1, "maxLength": 1024}
    identifier = {"type": "string", "pattern": r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}$"}
    strings = {"type": "array", "items": text, "maxItems": 16, "uniqueItems": True}
    props = {"id": identifier, "mode": {"enum": ["inquiry", "statement", "preparation", "action"]},
             "commitment": {"enum": ["none", "now", "conditional"]}, "activity": text}
    props.update({key: text for key in ("goal", "method", "source")})
    props.update({key: strings for key in ("targets", "constraints", "conditions", "stop_at", "context_refs")})
    props["candidate_domains"] = {"type": "array", "items": {"enum": ["world", "character", "resolution", "actors"]},
                                 "maxItems": 4, "uniqueItems": True}
    def obj(properties, required):
        return {"type": "object", "properties": properties, "required": required, "additionalProperties": False}
    return obj({"version": {"const": 1},
        "intentions": {"type": "array", "maxItems": 8, "items": obj(props, ["id", "mode", "commitment", "activity"])},
        "relationships": {"type": "array", "maxItems": 32, "items": obj({
            "type": {"enum": ["precedes", "depends_on", "alternative", "together", "independent"]},
            "from": identifier, "to": identifier}, ["type", "from", "to"])},
        "ambiguities": {"type": "array", "maxItems": 8, "items": obj({
            "intentions": {"type": "array", "maxItems": 8, "items": identifier},
            "issue": text}, ["intentions", "issue"])}},
        ["version", "intentions", "relationships", "ambiguities"])


class LocalIntentProvider:
    """One bounded request per call. Explicit model/config; no environment fallback.

    LM Studio must also have thinking disabled in its model settings. Responses
    containing reasoning/tool calls are rejected, never salvaged as interpretation.
    """
    def __init__(self, *, model, base_url="http://127.0.0.1:1234/v1", timeout=30.0, transport=None):
        url = urlsplit(base_url)
        if (url.scheme != "http" or url.hostname != "127.0.0.1" or url.username or url.password
                or url.path.rstrip("/") != "/v1" or url.query or url.fragment or not url.port
                or type(model) is not str or not model.strip() or len(model) > 128
                or type(timeout) not in (int, float) or not math.isfinite(timeout) or not 0 < timeout <= 60):
            raise ValueError("Explicit bounded localhost provider configuration required")
        self.model, self.base_url, self.timeout = model, base_url.rstrip("/"), timeout
        # No ambient proxies, auth, automatic retry, redirects or hosted fallback.
        self._transport = transport
        self.last_diagnostic = None

    def __call__(self, request):
        self.last_diagnostic = None
        if not isinstance(request, InterpretationRequest):
            self.last_diagnostic = {"category": "invalid_request"}
            raise LocalInterpretationUnavailable("invalid_request")
        start = time.monotonic()
        metadata = {}
        try:
            with httpx.Client(transport=self._transport, trust_env=False, follow_redirects=False,
                              timeout=self.timeout) as http:
                with OpenAI(base_url=self.base_url, api_key="local-no-auth", max_retries=0,
                            timeout=self.timeout, http_client=http) as client:
                    with client.chat.completions.with_streaming_response.create(
                        model=self.model, temperature=0, max_tokens=2048, n=1, stream=False,
                        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
                        response_format={"type": "json_schema", "json_schema": {
                            "name": "player_intent_v1", "strict": True, "schema": output_schema()}},
                        messages=interpretation_messages(request)) as response:
                        metadata.update(http_status=response.status_code, response_received=True)
                        chunks, count = [], 0
                        for chunk in response.iter_bytes(chunk_size=4096):
                            count += len(chunk)
                            if count > 131072:
                                raise LocalInterpretationUnavailable("response_too_large", **metadata)
                            if time.monotonic() - start > self.timeout:
                                raise LocalInterpretationUnavailable("timeout", **metadata)
                            chunks.append(chunk)
                        try:
                            value = json.loads(b"".join(chunks))
                        except (ValueError, UnicodeError, RecursionError):
                            raise LocalInterpretationUnavailable("invalid_response_json", **metadata) from None
            choices = value.get("choices") if type(value) is dict else None
            if type(choices) is not list or not choices:
                raise LocalInterpretationUnavailable("missing_completion", **metadata)
            metadata["choice_count"] = min(len(choices), 999)
            if len(choices) != 1 or type(choices[0]) is not dict:
                raise LocalInterpretationUnavailable("invalid_completion", **metadata)
            reason = choices[0].get("finish_reason")
            metadata["finish_reason"] = reason if reason in {"stop", "length", "content_filter", "tool_calls", "function_call"} else "other"
            if reason != "stop":
                raise LocalInterpretationUnavailable("incomplete_completion", **metadata)
            message = choices[0].get("message")
            if type(message) is not dict:
                raise LocalInterpretationUnavailable("invalid_completion", **metadata)
            metadata.update(reasoning_present=bool(message.get("reasoning_content")),
                tool_present=bool(message.get("tool_calls") or message.get("function_call")),
                refusal_present=bool(message.get("refusal")), content_present=bool(message.get("content")))
            if metadata["tool_present"] or metadata["refusal_present"] or metadata["reasoning_present"]:
                raise LocalInterpretationUnavailable("noninterpretation_completion", **metadata)
            raw = message.get("content")
            if type(raw) is not str or not raw:
                raise LocalInterpretationUnavailable("missing_completion", **metadata)
            if len(raw.encode("utf-8")) > MAX_OUTPUT_BYTES:
                raise LocalInterpretationUnavailable("interpretation_too_large", **metadata)
            self.last_diagnostic = dict(category="completion_accepted", **metadata)
            return raw  # Coordinator always applies normalize; never repair JSON.
        except Exception as error:
            if isinstance(error, LocalInterpretationUnavailable):
                safe = error
            elif isinstance(error, (APITimeoutError, httpx.TimeoutException)):
                safe = LocalInterpretationUnavailable("timeout", **metadata)
            elif isinstance(error, (APIConnectionError, httpx.TransportError)):
                safe = LocalInterpretationUnavailable("connection_transport", **metadata)
            elif isinstance(error, APIStatusError):
                # Inspect only to classify; never persist body, message or code text.
                body = json.dumps(error.body, ensure_ascii=True, default=lambda value: "").casefold()
                category = ("response_format_rejected" if error.status_code in {400, 422}
                    and any(k in body for k in ("response_format", "schema", "grammar")) else "http_provider_error")
                hint = ("message_structure_rejected" if any(s in body for s in (
                    "roles must alternate", "only user and assistant", "unsupported role", "multiple system", "at most one system"))
                    or re.search(r"system.{0,120}(first|beginning|start|initial)", body)
                    else "schema_rejected" if category == "response_format_rejected"
                    else "model_unavailable" if any(s in body for s in ("no model loaded", "model not found", "model is not loaded", "unavailable model"))
                    else None)
                safe = LocalInterpretationUnavailable(category, http_status=error.status_code,
                                                     response_received=True, provider_hint=hint)
            else:
                safe = LocalInterpretationUnavailable("internal_adapter_error", **metadata)
            self.last_diagnostic = safe.diagnostic
            raise safe from None
