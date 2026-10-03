from copy import deepcopy
import json
from pathlib import Path
from test_artifact_files import artifact_files

from engine.game_engine import GameEngine
from engine.save_system import build_save_data, load_game
from engine.world_state import validate_world_state


REGION_PATH = "test_fixtures/bryn_shander_legacy.json"


def expect_value_error(callable_):
    try:
        callable_()
    except ValueError:
        return
    raise AssertionError("Expected ValueError.")


def test_explicit_causal_and_inspection():
    engine = GameEngine(REGION_PATH)
    scene = engine.scene_snapshot
    first = engine.create_evidence_trace("trace_one", "opaque_kind", "bryn_shander_gate_north")
    assert first["changed"] and first["history_id"]
    assert engine.scene_snapshot is scene
    assert engine.get_evidence_trace("trace_one")["evidence_id"] == "opaque_kind"
    assert engine.get_evidence_traces_at_location("bryn_shander_gate_north")[0]["trace_id"] == "trace_one"
    assert not engine.create_evidence_trace("trace_one", "opaque_kind", "bryn_shander_gate_north")["changed"]
    expect_value_error(lambda: engine.create_evidence_trace("trace_one", "other", "bryn_shander_gate_north"))
    causal = engine.create_evidence_trace_from_event("trace_two", "opaque_two", "bryn_shander_gate_north", first["history_id"])
    assert causal["changed"] and engine.get_history_entry_by_id(causal["history_id"])["source_history_id"] == first["history_id"]
    copied = engine.get_evidence_traces(); copied[0]["trace_id"] = "mutated"
    assert engine.get_evidence_trace("trace_one")["trace_id"] == "trace_one"


def test_conversation_and_persistence():
    engine = GameEngine(REGION_PATH)
    result = engine.process_command("talk to captain")
    consequence = result["evidence_trace_consequence"]
    assert consequence["changed"] and consequence["source_history_id"]
    assert engine.get_history_entry_by_id(consequence["history_id"])["source_history_id"] == consequence["source_history_id"]
    assert engine.query_history(event_type="evidence_trace_added") == [
        engine.get_history_entry_by_id(consequence["history_id"])
    ]
    context = engine.get_narration_context("look", history_count=20)
    preview = engine.get_narration_preview("look")
    for packet in (context, preview):
        rendered = repr(packet)
        assert "evidence_trace_added" not in rendered
        assert "captain_conversation_gate_trace" not in rendered
        assert "captain_conversation_trace" not in rendered
    assert all(entry["event_type"] != "evidence_trace_added" for entry in context["history_context"]["history_entries"])
    assert not engine.process_command("talk to captain")["evidence_trace_consequence"]["changed"]
    with artifact_files("test_evidence_traces") as directory:
        path = Path(directory) / "test_evidence_traces_trace.json"
        path.write_text(json.dumps(build_save_data(engine)), encoding="utf-8")
        loaded = load_game(str(path))
        assert loaded.get_evidence_trace("captain_conversation_gate_trace")
        assert "captain_conversation_gate_trace" not in repr(loaded.get_narration_context("look", history_count=20))
        assert not loaded.process_command("talk to captain")["evidence_trace_consequence"]["changed"]
        legacy = build_save_data(engine); del legacy["world_state"]["evidence_traces"]
        legacy_path = Path(directory) / "test_evidence_traces_legacy.json"; legacy_path.write_text(json.dumps(legacy), encoding="utf-8")
        assert load_game(str(legacy_path)).get_evidence_traces() == []
        malformed = deepcopy(build_save_data(engine)); malformed["world_state"]["evidence_traces"][0]["location_id"] = "missing"
        bad_path = Path(directory) / "test_evidence_traces_bad.json"; bad_path.write_text(json.dumps(malformed), encoding="utf-8")
        before = engine.get_world_state(); expect_value_error(lambda: engine.load(str(bad_path)))
        assert engine.get_world_state() == before


def test_validation():
    engine = GameEngine(REGION_PATH)
    state = engine.get_world_state()
    for value in ({}, [{"trace_id": "x"}], [{"trace_id": "x", "evidence_id": "y", "location_id": "missing"}], [{"trace_id": "x", "evidence_id": "y", "location_id": "bryn_shander_gate_north"}] * 2):
        candidate = deepcopy(state); candidate["evidence_traces"] = value
        expect_value_error(lambda candidate=candidate: validate_world_state(candidate, engine.region))


def main():
    test_explicit_causal_and_inspection()
    test_conversation_and_persistence()
    test_validation()
    print("Evidence trace tests passed.")


if __name__ == "__main__":
    main()
