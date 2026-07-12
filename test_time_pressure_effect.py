from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import load_game


REGION_PATH = "data/regions/bryn_shander.json"


def assert_rejected(region, fragment):
    try:
        validate_region(region)
    except ValueError as error:
        assert fragment in str(error)
    else:
        raise AssertionError("Expected Region Pack validation failure.")


def main():
    engine = GameEngine(REGION_PATH)
    validate_region(engine.region)
    effect = engine.region["elapsed_time_pressure_effect"]
    assert set(effect) == {
        "effect_id", "trigger_elapsed_hours", "pressure_id", "new_level"
    }

    for field, value in (
        ("effect_id", ""),
        ("trigger_elapsed_hours", True),
        ("trigger_elapsed_hours", 0),
        ("pressure_id", "unknown"),
        ("new_level", True),
        ("new_level", 101),
    ):
        malformed = deepcopy(engine.region)
        malformed["elapsed_time_pressure_effect"][field] = value
        assert_rejected(malformed, "elapsed_time_pressure_effect" if field != "pressure_id" else "Unknown elapsed-time")

    missing = deepcopy(engine.region)
    del missing["elapsed_time_pressure_effect"]
    validate_region(missing)

    initial_scene = engine.scene_snapshot
    result = engine.advance_time(1)
    consequence = result["pressure_consequence"]
    assert consequence == {
        "changed": True,
        "pressure_id": "bryn_shander_winter",
        "previous_level": 65,
        "new_level": 70,
        "history_id": "history_000002",
        "source_history_id": "history_000001",
        "effect_id": "winter_deepens_after_first_hour",
    }
    history = engine.get_history()
    assert [entry["event_type"] for entry in history] == [
        "time_advanced", "pressure_changed"
    ]
    assert history[1]["source_history_id"] == history[0]["history_id"]
    assert engine.scene_snapshot is not initial_scene
    assert engine.advance_time(1)["pressure_consequence"] is None

    multi = GameEngine(REGION_PATH)
    assert multi.advance_time(3)["pressure_consequence"]["changed"]
    assert multi.advance_time(1)["pressure_consequence"] is None

    noop = GameEngine(REGION_PATH)
    noop.set_pressure_level("bryn_shander_winter", 70)
    noop_result = noop.advance_time(1)["pressure_consequence"]
    assert not noop_result["changed"]
    assert noop_result["history_id"] is None
    assert noop_result["source_history_id"] == "history_000002"
    assert [entry["event_type"] for entry in noop.get_history()][-1] == "time_advanced"

    direct = GameEngine(REGION_PATH)
    waited = GameEngine(REGION_PATH)
    direct_result = direct.advance_time(1)
    wait_result = waited.process_command("wait")["time_advancement"]
    assert direct_result == wait_result
    assert direct.get_world_state() == waited.get_world_state()

    failing = GameEngine(REGION_PATH)
    before_state = failing.get_world_state()
    before_scene = failing.scene_snapshot
    with patch("engine.game_engine.prepare_pressure_level_change", side_effect=ValueError("fail")):
        try:
            failing.advance_time(1)
        except ValueError:
            pass
        else:
            raise AssertionError("Expected preparation failure.")
    assert failing.get_world_state() == before_state
    assert failing.scene_snapshot is before_scene

    for target in ("engine.game_engine.validate_world_state", "engine.game_engine.build_scene"):
        failing = GameEngine(REGION_PATH)
        before_state = failing.get_world_state()
        before_scene = failing.scene_snapshot
        with patch(target, side_effect=ValueError("fail")):
            try:
                failing.advance_time(1)
            except ValueError:
                pass
            else:
                raise AssertionError(f"Expected failure from {target}.")
        assert failing.get_world_state() == before_state
        assert failing.scene_snapshot is before_scene

    with TemporaryDirectory() as temp_dir:
        save_path = str(Path(temp_dir) / "before.json")
        saved = GameEngine(REGION_PATH)
        saved.save(save_path)
        loaded = load_game(save_path)
        assert loaded.advance_time(1)["pressure_consequence"]["changed"]
        loaded.save(save_path)
        reloaded = load_game(save_path)
        assert reloaded.advance_time(1)["pressure_consequence"] is None

    assert "elapsed_time_pressure_effect" not in engine.get_world_state()
    print("Time pressure effect tests passed.")


if __name__ == "__main__":
    main()
