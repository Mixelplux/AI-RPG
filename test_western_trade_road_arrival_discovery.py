import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import engine.game_engine as game_engine_module
import engine.world_update as world_update_module
from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import build_save_data, load_game


REGION = "data/regions/bryn_shander.json"
WEST_GATE = "bryn_shander_gate_west"
WEST_ROAD = "outside_trade_road_west"
TRACE = "western_trade_road_arrival_trace"
EVIDENCE = "western_trade_road_patrol_marker"
DISCOVERY = "western_trade_road_patrol_marker"
TITLE = "The Exposed Patrol Marker"
TEXT = (
    "Your arrival at the western road exposes a wind-scoured patrol marker "
    "beneath the drift, pointing back toward Bryn Shander's gate."
)


def region_data():
    return json.loads(Path(REGION).read_text(encoding="utf-8"))


def west_gate_engine():
    return GameEngine(REGION, entry_location_id=WEST_GATE)


def expect_invalid(region, fragment):
    try:
        validate_region(region)
    except ValueError as error:
        assert fragment in str(error), str(error)
        return
    raise AssertionError("Expected invalid Region Pack.")


def assert_rollback(engine, state, scene):
    assert engine.get_world_state() == state
    assert engine.world_state is not state
    assert engine.scene_snapshot is scene


def test_strict_declaration_validation():
    region = region_data()
    validate_region(region)
    absent = deepcopy(region)
    del absent["west_road_arrival_evidence_trace"]
    validate_region(absent)
    required = (
        "effect_id", "source_location_id", "destination_location_id",
        "trace_id", "evidence_id", "discovery_id",
    )
    for field in required:
        invalid = deepcopy(region)
        del invalid["west_road_arrival_evidence_trace"][field]
        expect_invalid(invalid, "fields are invalid")
        invalid = deepcopy(region)
        invalid["west_road_arrival_evidence_trace"][field] = ""
        expect_invalid(invalid, "non-empty strings")
    invalid = deepcopy(region)
    invalid["west_road_arrival_evidence_trace"]["extra"] = True
    expect_invalid(invalid, "fields are invalid")
    for field, value, message in (
        ("source_location_id", "bryn_shander_main_street", "match the one-hour traversal"),
        ("destination_location_id", "bryn_shander_gate_west", "match the one-hour traversal"),
        ("discovery_id", "missing", "exactly one discovery"),
        ("trace_id", "north_gate_second_hour_trace", "match its discovery"),
        ("evidence_id", "delayed_watch_mark", "match its discovery"),
    ):
        invalid = deepcopy(region)
        invalid["west_road_arrival_evidence_trace"][field] = value
        expect_invalid(invalid, message)
    invalid = deepcopy(region)
    invalid["one_hour_west_road_exit_traversal"]["destination_location_id"] = WEST_GATE
    expect_invalid(invalid, "endpoints")
    invalid = deepcopy(region)
    invalid["west_road_arrival_evidence_trace"]["effect_id"] = (
        region["elapsed_time_evidence_trace_effect"]["effect_id"]
    )
    expect_invalid(invalid, "effect_id conflicts")
    invalid = deepcopy(region)
    invalid["west_road_arrival_evidence_trace"]["trace_id"] = (
        region["elapsed_time_evidence_trace_effect"]["trace_id"]
    )
    invalid["discovery_declarations"][-1]["trace_id"] = (
        region["elapsed_time_evidence_trace_effect"]["trace_id"]
    )
    expect_invalid(invalid, "trace_id conflicts")
    invalid = deepcopy(region)
    invalid["discovery_declarations"].append(
        deepcopy(region["discovery_declarations"][-1])
    )
    expect_invalid(invalid, "Duplicate discovery_id")


def test_exact_arrival_is_hidden_then_investigable():
    engine = west_gate_engine()
    assert not engine.process_command("investigate")["investigation"]["changed"]
    before_scene = engine.scene_snapshot
    result = engine.process_command("go west")
    assert result["success"] and result["time_advancement"]["duration_hours"] == 1
    assert TRACE not in repr(result)
    assert EVIDENCE not in repr(result)
    assert DISCOVERY not in repr(result)
    assert TITLE not in repr(result) and TEXT not in repr(result)
    assert engine.scene_snapshot is not before_scene
    assert TRACE not in repr(engine.get_scene_snapshot())
    assert TRACE not in repr(engine.get_player_perception())
    assert TRACE not in repr(engine.get_narration())
    assert engine.get_evidence_trace(TRACE) == {
        "trace_id": TRACE, "evidence_id": EVIDENCE, "location_id": WEST_ROAD,
    }
    history = engine.get_history()
    assert [entry["event_type"] for entry in history] == [
        "time_advanced", "pressure_changed", "actor_moved", "player_movement",
        "evidence_trace_added",
    ]
    assert history[-1]["source_history_id"] == history[-2]["history_id"]
    investigation = engine.process_command("investigate")["investigation"]
    assert investigation["changed"]
    assert investigation["discovery_id"] == DISCOVERY
    assert investigation["text"] == TEXT
    assert engine.get_known_clues()[-1] == {"title": TITLE, "text": TEXT}
    assert not engine.process_command("investigate")["investigation"]["changed"]


def test_route_isolation_and_duplicate_noop():
    engine = west_gate_engine()
    engine.process_command("go east")
    assert engine.get_evidence_trace(TRACE) is None
    assert not engine.process_command("investigate")["investigation"]["changed"]
    engine = west_gate_engine()
    engine.process_command("go west")
    assert engine.get_evidence_trace(TRACE) is not None
    trace_events = [
        entry for entry in engine.query_history(event_type="evidence_trace_added")
        if entry["trace_id"] == TRACE
    ]
    engine.process_command("go east")
    reverse = engine.process_command("go west")
    assert reverse["success"]
    assert [
        entry for entry in engine.query_history(event_type="evidence_trace_added")
        if entry["trace_id"] == TRACE
    ] == trace_events
    assert engine.get_evidence_trace(TRACE)["location_id"] == WEST_ROAD
    other = GameEngine(REGION)
    other.process_command("go south")
    other.process_command("go east")
    state = other.get_world_state()
    assert other.process_command("go north")["success"]
    assert other.get_evidence_trace(TRACE) is None
    assert other.get_world_state()["time"] == state["time"]


def test_save_load_preserves_eligibility_trace_and_discovery():
    with TemporaryDirectory() as directory:
        before = Path(directory) / "before.json"
        after_arrival = Path(directory) / "after-arrival.json"
        after_discovery = Path(directory) / "after-discovery.json"
        engine = west_gate_engine()
        engine.save(str(before))
        loaded = load_game(str(before))
        assert loaded.get_evidence_trace(TRACE) is None
        loaded.process_command("go west")
        loaded.save(str(after_arrival))
        arrived = load_game(str(after_arrival))
        trace_history = arrived.query_history(event_type="evidence_trace_added")
        assert len(trace_history) == 1 and arrived.get_evidence_trace(TRACE)
        assert arrived.process_command("investigate")["investigation"]["changed"]
        arrived.save(str(after_discovery))
        discovered = load_game(str(after_discovery))
        assert DISCOVERY in discovered.get_player_discoveries()
        assert not discovered.process_command("investigate")["investigation"]["changed"]
        discovered.process_command("go east")
        discovered.process_command("go west")
        assert len([
            entry for entry in discovered.query_history(event_type="evidence_trace_added")
            if entry["trace_id"] == TRACE
        ]) == 1
        assert build_save_data(discovered)["save_version"] == 1


def test_event_specific_rollback_and_single_publication():
    original_engine_add = game_engine_module.add_history_entry
    original_movement_add = world_update_module.add_history_entry
    for event_type, module, original in (
        ("time_advanced", game_engine_module, original_engine_add),
        ("pressure_changed", game_engine_module, original_engine_add),
        ("actor_moved", game_engine_module, original_engine_add),
        ("player_movement", world_update_module, original_movement_add),
        ("evidence_trace_added", game_engine_module, original_engine_add),
    ):
        engine = west_gate_engine()
        state, scene = engine.get_world_state(), engine.scene_snapshot

        def fail_event(candidate, *args, **kwargs):
            actual = kwargs.get("event_type", args[0] if args else None)
            if actual == event_type:
                raise RuntimeError(event_type)
            return original(candidate, *args, **kwargs)

        with patch.object(module, "add_history_entry", side_effect=fail_event):
            try:
                engine.process_command("go west")
            except RuntimeError as error:
                assert str(error) == event_type
            else:
                raise AssertionError("Expected injected history failure.")
        assert_rollback(engine, state, scene)

    for target, owner in (
        ("advance_time_by_hours", game_engine_module),
        ("_prepare_pressure_level_from_event_candidate", game_engine_module.GameEngine),
        ("_prepare_actor_location_candidate", game_engine_module.GameEngine),
        ("apply_interaction", game_engine_module),
        ("_prepare_evidence_trace_candidate", game_engine_module.GameEngine),
        ("validate_world_state", game_engine_module),
        ("build_scene", game_engine_module),
    ):
        engine = west_gate_engine()
        state, scene = engine.get_world_state(), engine.scene_snapshot
        with patch.object(owner, target, side_effect=RuntimeError(target)):
            try:
                engine.process_command("go west")
            except RuntimeError as error:
                assert str(error) == target
            else:
                raise AssertionError("Expected injected transition failure.")
        assert_rollback(engine, state, scene)


def main():
    test_strict_declaration_validation()
    test_exact_arrival_is_hidden_then_investigable()
    test_route_isolation_and_duplicate_noop()
    test_save_load_preserves_eligibility_trace_and_discovery()
    test_event_specific_rollback_and_single_publication()
    print("Western Trade Road arrival discovery tests passed.")


if __name__ == "__main__":
    main()
