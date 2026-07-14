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
WEST_GATE = "bryn_shander_gate_west"
WEST_ROAD = "outside_trade_road_west"


def region_data():
    return json.loads(Path(REGION_PATH).read_text(encoding="utf-8"))


def west_gate_engine():
    return GameEngine(REGION_PATH, entry_location_id=WEST_GATE)


def expect_invalid(region, fragment):
    try:
        validate_region(region)
    except ValueError as error:
        assert fragment in str(error), str(error)
        return
    raise AssertionError("Expected invalid Region Pack.")


def test_declaration_validation():
    region = region_data()
    validate_region(region)
    absent = deepcopy(region)
    del absent["one_hour_west_road_exit_traversal"]
    validate_region(absent)
    for invalid_value in ([], [deepcopy(region["one_hour_west_road_exit_traversal"])]):
        invalid = deepcopy(region)
        invalid["one_hour_west_road_exit_traversal"] = invalid_value
        expect_invalid(invalid, "fields are invalid")
    for field, value, message in (
        ("source_location_id", "", "non-empty string"),
        ("destination_location_id", "missing", "known locations"),
        ("source_location_id", "bryn_shander_main_street", "West Gate"),
        ("duration_hours", 2, "exactly one hour"),
        ("duration_hours", True, "exactly one hour"),
    ):
        invalid = deepcopy(region)
        invalid["one_hour_west_road_exit_traversal"][field] = value
        expect_invalid(invalid, message)
    invalid = deepcopy(region)
    invalid["one_hour_west_road_exit_traversal"]["extra"] = "no"
    expect_invalid(invalid, "fields are invalid")
    disconnected = deepcopy(region)
    disconnected["locations"][2]["connected_locations"] = [
        {"direction": "east", "location_id": "bryn_shander_main_street"}
    ]
    expect_invalid(disconnected, "directly connected")


def test_exact_atomic_time_costed_traversal_and_history_order():
    engine = west_gate_engine()
    before_scene = engine.scene_snapshot
    original_validate = game_engine_module.validate_world_state
    original_build = game_engine_module.build_scene
    calls = {"validate": 0, "build": 0}
    with patch.object(game_engine_module, "validate_world_state", side_effect=lambda *a, **k: (calls.__setitem__("validate", calls["validate"] + 1), original_validate(*a, **k))[1]), patch.object(game_engine_module, "build_scene", side_effect=lambda *a, **k: (calls.__setitem__("build", calls["build"] + 1), original_build(*a, **k))[1]):
        result = engine.process_command("go west")
    assert calls == {"validate": 1, "build": 1}
    assert result["success"]
    assert result["time_advancement"]["duration_hours"] == 1
    assert engine.get_world_state()["time"]["elapsed_hours"] == 1
    assert engine.get_world_state()["player"]["current_location_id"] == WEST_ROAD
    assert engine.scene_snapshot is not before_scene
    history = engine.get_history()
    assert [entry["event_type"] for entry in history] == [
        "time_advanced", "pressure_changed", "actor_moved", "player_movement"
    ]
    assert history[1]["source_history_id"] == history[0]["history_id"]
    assert history[2]["source_history_id"] == history[0]["history_id"]
    assert history[3]["location"] == WEST_ROAD
    assert history[3]["time"] == engine.get_world_state()["time"]


def test_second_hour_trace_once_and_undeclared_routes_unchanged():
    engine = west_gate_engine()
    engine.world_state["time"]["elapsed_hours"] = 1
    result = engine.process_command("go west")
    assert result["time_advancement"]["evidence_trace_consequence"]["changed"]
    assert engine.get_evidence_trace("north_gate_second_hour_trace")
    trace_history = len(engine.query_history(event_type="evidence_trace_added"))
    before_time = deepcopy(engine.get_world_state()["time"])
    reverse = engine.process_command("go east")
    assert reverse["success"] and "time_advancement" not in reverse
    assert engine.get_world_state()["time"] == before_time
    repeat = engine.process_command("go west")
    assert repeat["time_advancement"]["evidence_trace_consequence"] is None
    assert len(engine.query_history(event_type="evidence_trace_added")) == trace_history
    wrong_destination = west_gate_engine()
    before_time = deepcopy(wrong_destination.get_world_state()["time"])
    wrong_destination.process_command("go east")
    assert wrong_destination.get_world_state()["time"] == before_time


def test_save_load_before_after_and_no_replay():
    with TemporaryDirectory() as directory:
        before_path = Path(directory) / "before.json"
        after_path = Path(directory) / "after.json"
        engine = west_gate_engine()
        engine.save(str(before_path))
        loaded = load_game(str(before_path))
        result = loaded.process_command("go west")
        assert result["time_advancement"]["duration_hours"] == 1
        loaded.process_command("go east")
        crossed = loaded.process_command("go west")
        assert crossed["time_advancement"]["evidence_trace_consequence"]["changed"]
        loaded.save(str(after_path))
        reloaded = load_game(str(after_path))
        state = reloaded.get_world_state()
        assert state["time"]["elapsed_hours"] == 2
        assert state["player"]["current_location_id"] == WEST_ROAD
        history = reloaded.get_history()
        reloaded.process_command("go east")
        reloaded.process_command("go west")
        assert len(reloaded.query_history(event_type="evidence_trace_added")) == 1
        assert reloaded.get_history()[:len(history)] == history
        assert build_save_data(reloaded)["save_version"] == 1


def test_complete_rollback_at_preparation_and_publication_boundaries():
    for target, owner in (
        ("advance_time_by_hours", game_engine_module),
        ("add_history_entry", game_engine_module),
        ("_prepare_pressure_level_from_event_candidate", game_engine_module.GameEngine),
        ("_prepare_actor_location_candidate", game_engine_module.GameEngine),
        ("apply_interaction", game_engine_module),
        ("validate_world_state", game_engine_module),
        ("build_scene", game_engine_module),
    ):
        engine = west_gate_engine()
        before_state, before_scene = engine.get_world_state(), engine.scene_snapshot
        with patch.object(owner, target, side_effect=RuntimeError(target)):
            try:
                engine.process_command("go west")
            except RuntimeError:
                pass
            else:
                raise AssertionError(f"Expected {target} failure.")
        assert engine.get_world_state() == before_state
        assert engine.scene_snapshot is before_scene


def main():
    test_declaration_validation()
    test_exact_atomic_time_costed_traversal_and_history_order()
    test_second_hour_trace_once_and_undeclared_routes_unchanged()
    test_save_load_before_after_and_no_replay()
    test_complete_rollback_at_preparation_and_publication_boundaries()
    print("One-hour West-Road exit traversal tests passed.")


if __name__ == "__main__":
    main()
