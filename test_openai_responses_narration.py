"""Deterministic, no-network checks for the isolated Responses adapter."""
import os

from engine.game_engine import GameEngine
from engine.narration_prompt import build_narration_prompt_packet
from engine.narration_request import build_narration_request_packet
from engine.narration_source import (
    OPENAI_MAX_INPUT_TOKENS,
    OPENAI_MODEL,
    NarrationProviderError,
    build_openai_responses_narration_source_result,
)


def main():
    engine = GameEngine("data/regions/bryn_shander.json")
    prompt = build_narration_prompt_packet(build_narration_request_packet(engine.get_narration_context("look around")))
    before = engine.get_world_state()
    old = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "test-key"
    calls = []
    class Response:
        status = "completed"
        output_text = "Snow tightens across the gate."
    def fake(client, request):
        calls.append((client.timeout, client.max_retries, request))
        return Response()
    result = build_openai_responses_narration_source_result(prompt, fake)
    assert result["source"] == "openai_responses_preview"
    assert result["metadata"]["model"] == OPENAI_MODEL
    assert result["candidate"]["narration_text"] == Response.output_text
    assert calls[0][0] == 20.0 and calls[0][1] == 0
    assert "reasoning" not in calls[0][2]
    assert calls[0][2]["store"] is False and calls[0][2]["max_output_tokens"] == 256
    assert engine.get_world_state() == before
    class RefusalResponse:
        status = "completed"
        output_text = ""
        output = [type("Item", (), {"content": [type("Content", (), {"type": "refusal"})()]})()]
    try:
        build_openai_responses_narration_source_result(prompt, lambda *_: RefusalResponse())
        raise AssertionError("refusal accepted")
    except NarrationProviderError as error:
        assert (error.stage, error.reason) == ("provider_response", "refusal")
    for status, reason in (("incomplete", "incomplete_max_output_tokens"), ("failed", "failed_status"), (None, "unexpected_response_shape")):
        response = type("Response", (), {"status": status, "output_text": "", "output": [], "incomplete_details": type("Detail", (), {"reason": "max_output_tokens"})()})()
        try:
            build_openai_responses_narration_source_result(prompt, lambda *_: response)
            raise AssertionError("invalid response accepted")
        except NarrationProviderError as error:
            assert error.stage == "provider_response" and error.reason == reason
    oversized = type("Response", (), {"status": "completed", "output_text": "x" * 4001, "output": []})()
    try:
        build_openai_responses_narration_source_result(prompt, lambda *_: oversized)
        raise AssertionError("oversized response accepted")
    except NarrationProviderError as error:
        assert error.stage == "provider_response"
    os.environ.pop("OPENAI_API_KEY", None)
    try:
        build_openai_responses_narration_source_result(prompt, fake)
        raise AssertionError("missing key invoked transport")
    except NarrationProviderError as error:
        assert error.stage == "provider_configuration"
    if old is not None:
        os.environ["OPENAI_API_KEY"] = old
    print("OpenAI Responses narration fake-transport test passed.")


if __name__ == "__main__":
    main()
