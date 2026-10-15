"""Offline structural and boundary checks. No live provider or semantic judge."""
from copy import deepcopy
import json
from pathlib import Path
from unittest.mock import patch

from engine.narrative_realization import build_realization_request, generate_with_provider, realize


def run():
    fixture = json.loads(Path("test_fixtures/f01_connected.json").read_text(encoding="utf-8"))
    original = deepcopy(fixture)
    calls = []

    def generate(**request):
        calls.append(request)
        return "A structurally valid candidate, not a fidelity certificate."

    for moment in fixture["moments"]:
        result = realize(moment, generate)
        assert result["status"] == "candidate"
        assert json.loads(calls[-1]["input"]) == moment
    assert len(calls) == 4 and fixture == original
    print("PASS: four contexts, exact serialization, no mutation; generator explicitly injected")

    base = fixture["moments"][0]
    for alter in (
        lambda c: c.update(hidden_truth="must never cross seam"),
        lambda c: c.pop("knowledge_limits"),
        lambda c: c["player_intent"].pop("authorization"),
        lambda c: c["developments"][0].pop("source"),
        lambda c: c["developments"][0].update(status="verified_by_repetition"),
        lambda c: c["continuity"].append(deepcopy(c["developments"][0])),
        lambda c: c.update(developments=[]),
    ):
        broken = deepcopy(base)
        alter(broken)
        before = len(calls)
        assert realize(broken, generate) == {"status": "unavailable", "text": "", "failure_stage": "context"}
        assert len(calls) == before
    print("PASS: malformed provenance/authorization/extra data rejected before generator")

    for bad in (None, {}, "", "  ", "x" * 4001):
        assert realize(base, lambda **r: bad)["failure_stage"] == "output"
    attempts = []

    def fail(**request):
        attempts.append(1)
        raise RuntimeError("private provider detail")

    result = realize(base, fail)
    assert result == {"status": "unavailable", "text": "", "failure_stage": "generation"}
    assert len(attempts) == 1 and "private" not in str(result)
    print("PASS: invalid output and provider errors fail closed; no retries or error disclosure")

    def mutate(**request):
        request.clear()
        return "candidate"

    assert realize(base, mutate)["status"] == "candidate" and fixture == original
    assert build_realization_request(fixture["moments"][3])["input"] == calls[3]["input"]
    # Deliberately false prose is structurally valid: never claim semantic validation.
    assert realize(base, lambda **r: "You fall and break your leg.")["status"] == "candidate"
    print("PASS: stateless reuse and copy isolation; structural checks do not certify fidelity")
    with patch("engine.narration_source.request_narration_text", return_value="Prose.") as provider:
        assert realize(base, generate_with_provider)["text"] == "Prose."
        request = build_realization_request(base)
        provider.assert_called_once_with(request["instructions"], request["input"], max_output_tokens=2048)
    print("PASS: opt-in provider adapter delegates exactly once with bounded output")


if __name__ == "__main__":
    run()
