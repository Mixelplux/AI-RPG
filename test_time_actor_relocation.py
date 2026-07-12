from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import load_game
from engine.scene_loader import build_scene as real_build_scene
from engine.world_state import validate_world_state as real_validate_world_state


REGION_PATH = "data/regions/bryn_shander.json"
ACTOR_ID = "captain_darvin_grey"
BASELINE = "bryn_shander_gate_north"
DESTINATION = "bryn_shander_gate_west"


def rejected(region, fragment):
    try:
        validate_region(region)
    except ValueError as error:
        assert fragment in str(error)
    else:
        raise AssertionError("Expected Region Pack validation failure.")


def main():
    engine = GameEngine(REGION_PATH)
    effect = engine.region["elapsed_time_actor_relocation_effect"]
    assert set(effect) == {
        "effect_id", "trigger_elapsed_hours", "actor_entity_id",
        "destination_location_id",
    }
    for field, value in (("effect_id", ""), ("trigger_elapsed_hours", True),
                         ("trigger_elapsed_hours", -1), ("actor_entity_id", "missing"),
                         ("destination_location_id", "missing")):
        malformed = deepcopy(engine.region)
        malformed["elapsed_time_actor_relocation_effect"][field] = value
        rejected(malformed, "elapsed_time_actor_relocation_effect")
    malformed = deepcopy(engine.region)
    malformed["elapsed_time_actor_relocation_effect"]["extra"] = "no"
    rejected(malformed, "elapsed_time_actor_relocation_effect fields are invalid")

    no_time = GameEngine(REGION_PATH)
    before_no_time = no_time.get_world_state()
    try:
        no_time.advance_time(0)
    except ValueError:
        pass
    else:
        raise AssertionError("Zero-duration time advancement was accepted.")
    assert no_time.get_world_state() == before_no_time
    before_scene = engine.scene_snapshot
    result = engine.advance_time(1)
    consequence = result["actor_location_consequence"]
    assert consequence == {
        "effect_id": "captain_moves_west_after_first_hour",
        "trigger_elapsed_hours": 1,
        "actor_entity_id": ACTOR_ID,
        "previous_location_id": BASELINE,
        "new_location_id": DESTINATION,
        "changed": True,
        "history_id": "history_000003",
    }
    history = engine.get_history()
    assert [entry["event_type"] for entry in history] == [
        "time_advanced", "pressure_changed", "actor_moved"
    ]
    assert history[1]["source_history_id"] == history[0]["history_id"]
    assert history[2]["source_history_id"] == history[0]["history_id"]
    assert engine.get_world_state()["actor_location_overrides"] == {ACTOR_ID: DESTINATION}
    assert ACTOR_ID not in engine.get_scene_snapshot()["entities"]["static"]
    assert engine.scene_snapshot is not before_scene
    assert engine.advance_time(1)["actor_location_consequence"] is None

    destination = GameEngine(REGION_PATH, entry_location_id=DESTINATION)
    destination.advance_time(1)
    assert destination.get_scene_snapshot()["entities"]["static"].count(ACTOR_ID) == 1
    assert destination.resolve_target("captain")["status"] == "resolved"
    assert ACTOR_ID in destination.get_player_perception()["visible"]["entities"]["static"]

    direct = GameEngine(REGION_PATH)
    waited = GameEngine(REGION_PATH)
    with patch("engine.game_engine.validate_world_state", wraps=real_validate_world_state) as validate_call, patch(
        "engine.game_engine.build_scene", wraps=real_build_scene
    ) as scene_call:
        wait_result = waited.process_command("wait")["time_advancement"]
    assert validate_call.call_count == 1
    assert scene_call.call_count == 1
    assert direct.advance_time(1) == wait_result
    assert direct.get_world_state() == waited.get_world_state()

    same = GameEngine(REGION_PATH)
    same.set_actor_location(ACTOR_ID, DESTINATION)
    same_result = same.advance_time(1)["actor_location_consequence"]
    assert not same_result["changed"] and same_result["history_id"] is None
    assert [entry["event_type"] for entry in same.get_history()] == [
        "actor_moved", "time_advanced", "pressure_changed"
    ]

    for target in ("engine.game_engine.prepare_pressure_level_change",
                   "engine.game_engine.GameEngine._prepare_actor_location_candidate",
                   "engine.game_engine.validate_world_state",
                   "engine.game_engine.build_scene"):
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

    consequence["actor_entity_id"] = "changed"
    actor_history = engine.query_history(event_type="actor_moved")
    assert actor_history[-1]["entity_id"] == ACTOR_ID
    with TemporaryDirectory() as temp_dir:
        save_path = str(Path(temp_dir) / "actor-time.json")
        engine.save(save_path)
        loaded = load_game(save_path)
        assert loaded.get_world_state() == engine.get_world_state()
        assert loaded.advance_time(1)["actor_location_consequence"] is None

    print("Time actor relocation tests passed.")


if __name__ == "__main__":
    main()
