import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import engine.game_engine as game_engine_module
from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import build_save_data, load_game


REGION_PATH = "data/regions/bryn_shander.json"
THREAD_ID = "bryn_shander_west_road_bandit_report"
TRACE_ID = "west_gate_elin_report_trace"
EVIDENCE_ID = "elin_west_road_patrol_orders"
LOCATION_ID = "bryn_shander_gate_west"
DISCOVERY_ID = "west_gate_elin_report_trace"


def region_data():
    return json.loads(Path(REGION_PATH).read_text(encoding="utf-8"))


def rejected(region, fragment):
    try:
        validate_region(region)
    except ValueError as error:
        assert fragment in str(error), str(error)
        return
    raise AssertionError("Expected Region Pack validation failure.")


def prepare_resolution(engine):
    assert engine.process_command("talk to captain")["success"]
    assert engine.process_command("investigate")["investigation"]["changed"]


def resolve(engine):
    prepare_resolution(engine)
    result = engine.process_command(
        "present The Captain's Deliberate Trail to captain"
    )["presentation"]
    assert result["changed"]
    return result


def test_declaration_validation_and_compatibility():
    region = region_data()
    validate_region(region)
    absent = deepcopy(region)
    del absent["resolved_thread_evidence_trace_effect"]
    del absent["conversation_player_discovery_response"]
    del absent["conversation_affordance"]
    validate_region(absent)
    for field in ("effect_id", "resolved_thread_id", "trace_id", "evidence_id", "location_id"):
        bad = deepcopy(region)
        del bad["resolved_thread_evidence_trace_effect"][field]
        rejected(bad, "fields are invalid")
        bad = deepcopy(region)
        bad["resolved_thread_evidence_trace_effect"][field] = ""
        rejected(bad, "non-empty strings")
    bad = deepcopy(region)
    bad["resolved_thread_evidence_trace_effect"]["extra"] = "no"
    rejected(bad, "fields are invalid")
    bad = deepcopy(region)
    bad["resolved_thread_evidence_trace_effect"]["resolved_thread_id"] = "unknown"
    rejected(bad, "unknown")
    bad = deepcopy(region)
    bad["resolved_thread_evidence_trace_effect"]["location_id"] = "unknown"
    rejected(bad, "location_id is unknown")
    bad = deepcopy(region)
    del bad["resolved_thread_actor_relocation_effect"]
    rejected(bad, "requires a matching")
    bad = deepcopy(region)
    bad["resolved_thread_actor_relocation_effect"]["destination_location_id"] = "bryn_shander_gate_north"
    rejected(bad, "must match the resolved-thread relocation destination")
    bad = deepcopy(region)
    bad["discovery_declarations"][2]["evidence_id"] = "other"
    rejected(bad, "evidence_id must match its discovery")
    bad = deepcopy(region)
    bad["discovery_declarations"][2]["location_id"] = "bryn_shander_gate_north"
    rejected(bad, "location_id must match its discovery")
    bad = deepcopy(region)
    bad["resolved_thread_evidence_trace_effect"]["trace_id"] = "missing"
    rejected(bad, "exactly one discovery")
    bad = deepcopy(region)
    bad["resolved_thread_evidence_trace_effect"]["effect_id"] = region["resolved_thread_actor_relocation_effect"]["effect_id"]
    rejected(bad, "effect_id conflicts")
    bad = deepcopy(region)
    bad["resolved_thread_evidence_trace_effect"]["trace_id"] = region["elapsed_time_evidence_trace_effect"]["trace_id"]
    rejected(bad, "trace_id conflicts")


def test_atomic_composition_and_hidden_investigation():
    engine = GameEngine(REGION_PATH)
    result = resolve(engine)
    assert result["actor_location_consequence"] == {"status": "applied"}
    assert result["actor_knowledge_consequence"] == {"status": "applied"}
    assert result["evidence_trace_consequence"] == {"status": "applied"}
    assert engine.get_evidence_trace(TRACE_ID) == {
        "trace_id": TRACE_ID, "evidence_id": EVIDENCE_ID, "location_id": LOCATION_ID,
    }
    history = engine.get_history()
    source = next(entry for entry in history if entry["event_type"] == "clue_presented")
    dependent = [entry for entry in history if entry.get("source_history_id") == source["history_id"] and entry["event_type"] in {
        "actor_moved", "actor_knowledge_added", "evidence_trace_added"
    }]
    assert [entry["event_type"] for entry in dependent] == [
        "actor_moved", "actor_knowledge_added", "evidence_trace_added"
    ]
    assert all(entry["source_history_id"] == source["history_id"] for entry in dependent)
    assert engine.process_command("investigate")["investigation"]["changed"] is False
    for packet in (
        engine.get_scene_snapshot(), engine.get_player_perception(),
        engine.get_narration_context("look", history_count=20),
        engine.get_narration_preview("look"), engine.process_command("talk to captain"),
    ):
        assert TRACE_ID not in repr(packet)
        assert EVIDENCE_ID not in repr(packet)
    assert engine.process_command("go south")["success"]
    assert engine.process_command("go east")["success"]
    assert engine.process_command("go north")["success"]
    investigation = engine.process_command("investigate")["investigation"]
    assert investigation["changed"] and investigation["discovery_id"] == DISCOVERY_ID
    assert investigation["text"] == engine.region["discovery_declarations"][2]["text"]
    assert engine.process_command("investigate")["investigation"]["changed"] is False


def test_trigger_eligibility_noop_conflict_and_single_publication():
    for commands in ((), ("talk to guard",), ("talk to captain", "investigate")):
        engine = GameEngine(REGION_PATH)
        for command in commands:
            engine.process_command(command)
        result = engine.process_command("present wrong to captain")["presentation"]
        assert not result["changed"] and engine.get_evidence_trace(TRACE_ID) is None
    engine = GameEngine(REGION_PATH)
    engine.region["conversation_discovery_resolution"]["required_thread_id"] = "other"
    prepare_resolution(engine)
    assert not engine.process_command("present The Captain's Deliberate Trail to captain")["presentation"]["changed"]
    assert engine.get_evidence_trace(TRACE_ID) is None
    engine = GameEngine(REGION_PATH)
    del engine.region["resolved_thread_evidence_trace_effect"]
    result = resolve(engine)
    assert result["evidence_trace_consequence"] is None
    assert engine.get_evidence_trace(TRACE_ID) is None
    engine = GameEngine(REGION_PATH)
    engine.create_evidence_trace(TRACE_ID, EVIDENCE_ID, LOCATION_ID)
    prepare_resolution(engine)
    history_count = len(engine.query_history(event_type="evidence_trace_added"))
    original_validate = game_engine_module.validate_world_state
    original_build = game_engine_module.build_scene
    calls = {"validate": 0, "build": 0}
    with patch.object(game_engine_module, "validate_world_state", side_effect=lambda *a, **k: (calls.__setitem__("validate", calls["validate"] + 1), original_validate(*a, **k))[1]), patch.object(game_engine_module, "build_scene", side_effect=lambda *a, **k: (calls.__setitem__("build", calls["build"] + 1), original_build(*a, **k))[1]):
        result = engine.process_command("present The Captain's Deliberate Trail to captain")["presentation"]
    assert result["evidence_trace_consequence"] == {"status": "no_op"}
    assert calls == {"validate": 1, "build": 1}
    assert len(engine.query_history(event_type="evidence_trace_added")) == history_count
    engine = GameEngine(REGION_PATH)
    engine.world_state["evidence_traces"].append({"trace_id": TRACE_ID, "evidence_id": "other", "location_id": LOCATION_ID})
    prepare_resolution(engine)
    before_state, live_state, before_scene = engine.get_world_state(), engine.world_state, engine.scene_snapshot
    try:
        engine.process_command("present The Captain's Deliberate Trail to captain")
    except ValueError as error:
        assert "Conflicting evidence trace identity" in str(error)
    else:
        raise AssertionError("Expected trace conflict.")
    assert engine.get_world_state() == before_state and engine.world_state is live_state
    assert engine.scene_snapshot is before_scene


def test_rollback_and_save_load():
    for target in (
        "_prepare_actor_location_candidate", "_prepare_actor_knowledge_from_event_candidate",
        "_prepare_evidence_trace_candidate", "validate_world_state", "build_scene",
    ):
        engine = GameEngine(REGION_PATH)
        prepare_resolution(engine)
        before_state, live_state, before_scene = engine.get_world_state(), engine.world_state, engine.scene_snapshot
        owner = game_engine_module.GameEngine if target.startswith("_") else game_engine_module
        with patch.object(owner, target, side_effect=RuntimeError(target)):
            try:
                engine.process_command("present The Captain's Deliberate Trail to captain")
            except RuntimeError:
                pass
            else:
                raise AssertionError("Expected injected failure.")
        assert engine.get_world_state() == before_state and engine.world_state is live_state
        assert engine.scene_snapshot is before_scene
    engine = GameEngine(REGION_PATH)
    prepare_resolution(engine)
    before_state, before_scene = engine.get_world_state(), engine.scene_snapshot
    original_add = game_engine_module.add_history_entry
    def fail_evidence_history(candidate, event_type, *args, **kwargs):
        if event_type == "evidence_trace_added":
            raise RuntimeError("evidence history")
        return original_add(candidate, event_type, *args, **kwargs)
    with patch.object(game_engine_module, "add_history_entry", side_effect=fail_evidence_history):
        try:
            engine.process_command("present The Captain's Deliberate Trail to captain")
        except RuntimeError as error:
            assert "evidence history" in str(error)
        else:
            raise AssertionError("Expected evidence-history failure.")
    assert engine.get_world_state() == before_state and engine.scene_snapshot is before_scene
    with TemporaryDirectory() as directory:
        before = GameEngine(REGION_PATH)
        before.process_command("talk to captain")
        path = Path(directory) / "before.json"
        path.write_text(json.dumps(build_save_data(before)), encoding="utf-8")
        loaded = load_game(str(path))
        assert resolve(loaded)["evidence_trace_consequence"] == {"status": "applied"}
        loaded.save(str(path))
        reloaded = load_game(str(path))
        assert reloaded.get_evidence_trace(TRACE_ID)
        assert reloaded.process_command("present The Captain's Deliberate Trail to captain")["presentation"]["changed"] is False
        assert reloaded.get_evidence_trace(TRACE_ID)
        historical = GameEngine(REGION_PATH)
        resolve(historical)
        legacy = build_save_data(historical)
        legacy["world_state"]["evidence_traces"] = [
            trace for trace in legacy["world_state"]["evidence_traces"]
            if trace["trace_id"] != TRACE_ID
        ]
        legacy["world_state"]["history"] = [
            entry for entry in legacy["world_state"]["history"]
            if not (entry["event_type"] == "evidence_trace_added" and entry["trace_id"] == TRACE_ID)
        ]
        legacy_path = Path(directory) / "already-resolved.json"
        legacy_path.write_text(json.dumps(legacy), encoding="utf-8")
        assert load_game(str(legacy_path)).get_evidence_trace(TRACE_ID) is None


def main():
    test_declaration_validation_and_compatibility()
    test_atomic_composition_and_hidden_investigation()
    test_trigger_eligibility_noop_conflict_and_single_publication()
    test_rollback_and_save_load()
    print("Resolved-thread evidence trace consequence tests passed.")


if __name__ == "__main__":
    main()
