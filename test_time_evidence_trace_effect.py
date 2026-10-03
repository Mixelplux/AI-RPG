from copy import deepcopy
from pathlib import Path
from test_artifact_files import artifact_files
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import load_game
from engine.scene_loader import build_scene as real_build_scene
from engine.world_state import validate_world_state as real_validate_world_state


REGION_PATH = "test_fixtures/bryn_shander_legacy.json"
TRACE_ID = "north_gate_second_hour_trace"


def rejected(region, fragment):
    try:
        validate_region(region)
    except ValueError as error:
        assert fragment in str(error)
    else:
        raise AssertionError("Expected Region Pack validation failure.")


def main():
    engine = GameEngine(REGION_PATH)
    effect = engine.region["elapsed_time_evidence_trace_effect"]
    assert set(effect) == {"effect_id", "trigger_elapsed_hours", "trace_id", "evidence_id", "location_id"}
    for field, value, fragment in (
        ("effect_id", "", "effect_id"), ("trigger_elapsed_hours", True, "trigger_elapsed_hours"),
        ("trigger_elapsed_hours", 0, "trigger_elapsed_hours"), ("trace_id", 1, "trace_id"),
        ("location_id", "missing", "location_id is unknown"),
    ):
        malformed = deepcopy(engine.region); malformed["elapsed_time_evidence_trace_effect"][field] = value
        rejected(malformed, fragment)
    malformed = deepcopy(engine.region); del malformed["elapsed_time_evidence_trace_effect"]["evidence_id"]
    rejected(malformed, "fields are invalid")
    malformed = deepcopy(engine.region); malformed["elapsed_time_evidence_trace_effect"]["extra"] = "no"
    rejected(malformed, "fields are invalid")
    malformed = deepcopy(engine.region); malformed["elapsed_time_evidence_trace_effect"]["trace_id"] = "missing"
    rejected(malformed, "exactly one discovery")
    malformed = deepcopy(engine.region); malformed["discovery_declarations"][1]["location_id"] = "bryn_shander_gate_west"
    rejected(malformed, "must match its discovery")
    malformed = deepcopy(engine.region); malformed["elapsed_time_evidence_trace_effect"]["effect_id"] = malformed["elapsed_time_pressure_effect"]["effect_id"]
    rejected(malformed, "effect_id conflicts")
    malformed = deepcopy(engine.region); malformed["elapsed_time_evidence_trace_effect"]["trace_id"] = malformed["conversation_evidence_trace_effect"]["trace_id"]
    rejected(malformed, "trace_id conflicts")
    malformed = deepcopy(engine.region); del malformed["elapsed_time_evidence_trace_effect"]
    del malformed["conversation_discovery_actor_relocation"]
    validate_region(malformed)

    before_scene = engine.scene_snapshot
    assert engine.advance_time(1)["evidence_trace_consequence"] is None
    result = engine.advance_time(1)
    trace = result["evidence_trace_consequence"]
    assert trace["changed"] and trace["trace_id"] == TRACE_ID and trace["evidence_id"] == "delayed_watch_mark"
    history = engine.get_history()
    assert [entry["event_type"] for entry in history] == ["time_advanced", "pressure_changed", "actor_moved", "time_advanced", "evidence_trace_added"]
    assert history[-1]["source_history_id"] == history[-2]["history_id"]
    assert engine.get_evidence_trace(TRACE_ID)["location_id"] == "bryn_shander_gate_north"
    assert engine.scene_snapshot is not before_scene
    assert engine.advance_time(1)["evidence_trace_consequence"] is None
    assert engine.process_command("investigate")["investigation"]["text"] == engine.region["discovery_declarations"][1]["text"]
    for packet in (engine.get_scene_snapshot(), engine.get_player_perception(), engine.get_narration_context("look"), engine.get_narration_preview("look")):
        assert TRACE_ID not in repr(packet) and "delayed_watch_mark" not in repr(packet)

    multi = GameEngine(REGION_PATH)
    combined = multi.advance_time(2)
    assert combined["pressure_consequence"]["changed"] and combined["actor_location_consequence"]["changed"]
    assert combined["evidence_trace_consequence"]["changed"]

    noop = GameEngine(REGION_PATH)
    noop.create_evidence_trace(TRACE_ID, "delayed_watch_mark", "bryn_shander_gate_north")
    assert not noop.advance_time(2)["evidence_trace_consequence"]["changed"]
    assert len(noop.query_history(event_type="evidence_trace_added")) == 1

    conflict = GameEngine(REGION_PATH)
    conflict.world_state["evidence_traces"].append({"trace_id": TRACE_ID, "evidence_id": "other", "location_id": "bryn_shander_gate_north"})
    before_state, before_scene = conflict.get_world_state(), conflict.scene_snapshot
    try:
        conflict.advance_time(2)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected conflicting trace rejection.")
    assert conflict.get_world_state() == before_state and conflict.scene_snapshot is before_scene

    for target in ("engine.game_engine.GameEngine._prepare_evidence_trace_candidate", "engine.game_engine.validate_world_state", "engine.game_engine.build_scene"):
        failing = GameEngine(REGION_PATH); state, scene = failing.get_world_state(), failing.scene_snapshot
        with patch(target, side_effect=ValueError("fail")):
            try: failing.advance_time(2)
            except ValueError: pass
            else: raise AssertionError(f"Expected {target} failure.")
        assert failing.get_world_state() == state and failing.scene_snapshot is scene
    failing = GameEngine(REGION_PATH); state, scene = failing.get_world_state(), failing.scene_snapshot
    from engine.game_engine import add_history_entry as real_add_history
    calls = 0
    def fail_evidence_history(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 4: raise ValueError("evidence history fail")
        return real_add_history(*args, **kwargs)
    with patch("engine.game_engine.add_history_entry", side_effect=fail_evidence_history):
        try: failing.advance_time(2)
        except ValueError: pass
        else: raise AssertionError("Expected evidence-history failure.")
    assert failing.get_world_state() == state and failing.scene_snapshot is scene

    with artifact_files("test_time_evidence_trace_effect") as directory:
        path = str(Path(directory) / "test_time_evidence_trace_effect_time-trace.json")
        saved = GameEngine(REGION_PATH); saved.save(path)
        loaded = load_game(path); assert loaded.advance_time(2)["evidence_trace_consequence"]["changed"]
        loaded.save(path); reloaded = load_game(path)
        assert reloaded.get_evidence_trace(TRACE_ID) and reloaded.advance_time(1)["evidence_trace_consequence"] is None

    print("Time evidence trace effect tests passed.")


if __name__ == "__main__":
    main()
