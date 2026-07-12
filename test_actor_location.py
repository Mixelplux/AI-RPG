from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import build_save_data, load_game
from engine.scene_loader import load_region
from engine.world_state import create_initial_world_state, validate_world_state


REGION_PATH = "data/regions/bryn_shander.json"
ACTOR_ID = "captain_darvin_grey"
BASELINE = "bryn_shander_gate_north"
DESTINATION = "bryn_shander_main_street"


def expect_value_error(callable_):
    try:
        callable_()
    except ValueError:
        return
    raise AssertionError("Expected ValueError.")


def main():
    region = load_region(REGION_PATH)

    missing_id = deepcopy(region)
    missing_id["entities"][0]["entity_id"] = ""
    expect_value_error(lambda: validate_region(missing_id))

    duplicate_id = deepcopy(region)
    duplicate_id["entities"][1]["entity_id"] = ACTOR_ID
    expect_value_error(lambda: validate_region(duplicate_id))

    unknown_location = deepcopy(region)
    unknown_location["entities"][0]["location"] = "missing"
    expect_value_error(lambda: validate_region(unknown_location))

    state = create_initial_world_state(region)
    assert state["actor_location_overrides"] == {}
    missing_field = deepcopy(state)
    del missing_field["actor_location_overrides"]
    validate_world_state(missing_field, region)

    bad_actor = deepcopy(state)
    bad_actor["actor_location_overrides"] = {"missing": DESTINATION}
    expect_value_error(lambda: validate_world_state(bad_actor, region))
    bad_destination = deepcopy(state)
    bad_destination["actor_location_overrides"] = {ACTOR_ID: "missing"}
    expect_value_error(lambda: validate_world_state(bad_destination, region))
    redundant = deepcopy(state)
    redundant["actor_location_overrides"] = {ACTOR_ID: BASELINE}
    expect_value_error(lambda: validate_world_state(redundant, region))

    engine = GameEngine(REGION_PATH)
    original_scene_identity = id(engine.scene_snapshot)
    assert ACTOR_ID in engine.get_scene_snapshot()["entities"]["static"]

    no_op = engine.set_actor_location(ACTOR_ID, BASELINE)
    assert no_op == {
        "changed": False, "entity_id": ACTOR_ID,
        "previous_location_id": BASELINE, "new_location_id": BASELINE,
        "history_id": None,
    }
    assert id(engine.scene_snapshot) == original_scene_identity
    assert engine.get_history() == []

    move = engine.set_actor_location(ACTOR_ID, DESTINATION)
    assert move["changed"] and move["previous_location_id"] == BASELINE
    assert move["new_location_id"] == DESTINATION
    assert engine.get_world_state()["actor_location_overrides"] == {
        ACTOR_ID: DESTINATION
    }
    assert len(engine.query_history(event_type="actor_moved")) == 1
    assert ACTOR_ID not in engine.get_scene_snapshot()["entities"]["static"]
    assert engine.resolve_target("captain")["status"] == "unresolved"

    destination_engine = GameEngine(REGION_PATH, entry_location_id=DESTINATION)
    destination_engine.set_actor_location(ACTOR_ID, DESTINATION)
    scene = destination_engine.get_scene_snapshot()
    assert scene["entities"]["static"].count(ACTOR_ID) == 1
    assert destination_engine.resolve_target("captain")["status"] == "resolved"
    assert ACTOR_ID in destination_engine.get_player_perception()["visible"]["entities"]["static"]

    returned_state = engine.get_world_state()
    returned_state["actor_location_overrides"].clear()
    assert engine.get_world_state()["actor_location_overrides"] == {ACTOR_ID: DESTINATION}
    move["entity_id"] = "changed"
    assert engine.get_history()[-1]["entity_id"] == ACTOR_ID

    before_state = engine.get_world_state()
    before_scene_identity = id(engine.scene_snapshot)
    expect_value_error(lambda: engine.set_actor_location("missing", DESTINATION))
    expect_value_error(lambda: engine.set_actor_location(ACTOR_ID, "missing"))
    assert engine.get_world_state() == before_state
    assert id(engine.scene_snapshot) == before_scene_identity

    with patch("engine.game_engine.build_scene", side_effect=RuntimeError("boom")):
        try:
            engine.set_actor_location(ACTOR_ID, BASELINE)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Expected scene construction failure.")
    assert engine.get_world_state() == before_state
    assert id(engine.scene_snapshot) == before_scene_identity

    back = engine.set_actor_location(ACTOR_ID, BASELINE)
    assert back["changed"] and back["previous_location_id"] == DESTINATION
    assert engine.get_world_state()["actor_location_overrides"] == {}

    engine.set_actor_location(ACTOR_ID, DESTINATION)
    with TemporaryDirectory() as temp_dir:
        save_path = Path(temp_dir) / "actor.json"
        save_path.write_text(json.dumps(build_save_data(engine)), encoding="utf-8")
        loaded = load_game(str(save_path))
        assert loaded.get_world_state()["actor_location_overrides"] == {
            ACTOR_ID: DESTINATION
        }

        legacy = build_save_data(engine)
        del legacy["world_state"]["actor_location_overrides"]
        legacy_path = Path(temp_dir) / "legacy.json"
        legacy_path.write_text(json.dumps(legacy), encoding="utf-8")
        legacy_engine = load_game(str(legacy_path))
        assert legacy_engine.get_world_state()["actor_location_overrides"] == {}

    print("Actor location test passed.")


if __name__ == "__main__":
    main()
