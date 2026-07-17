from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from engine.elapsed_time_transition_observation import (
    derive_elapsed_time_transition_observation,
)
from engine.game_engine import GameEngine
from engine.save_system import build_save_data, load_game


REGION_PATH = "data/regions/bryn_shander.json"


def scene(location_id, location_name, actors):
    return {
        "location": {"location_id": location_id, "name": location_name},
        "entities": {"static": actors, "spawned": []},
    }


def main():
    catalog = [
        {"entity_id": "first", "name": "First Actor", "persistence": "static"},
        {"entity_id": "second", "name": "Second Actor", "persistence": "static"},
    ]
    before = scene("north", "North Gate", ["second", "first"])
    after = scene("north", "North Gate", [])
    before_copy = deepcopy(before)
    after_copy = deepcopy(after)
    catalog_copy = deepcopy(catalog)
    assert derive_elapsed_time_transition_observation(before, after, catalog) == (
        "An hour passes. Second Actor is no longer at the North Gate."
    )
    assert before == before_copy
    assert after == after_copy
    assert catalog == catalog_copy

    assert derive_elapsed_time_transition_observation(
        before,
        scene("north", "North Gate", ["second", "first"]),
        catalog,
    ) == "An hour passes."
    assert derive_elapsed_time_transition_observation(
        before,
        scene("west", "West Gate", []),
        catalog,
    ) == "An hour passes."

    engine = GameEngine(REGION_PATH)
    start_state = engine.get_world_state()
    result = engine.process_command("wait")
    assert result["message"] == (
        "An hour passes. Captain Darvin Grey is no longer at the North Gate."
    )
    assert result["time_advancement"]["actor_location_consequence"]["changed"]
    assert "captain_moves_west_after_first_hour" not in result["message"]
    assert "history_" not in result["message"]
    assert "pressure" not in result["message"].lower()
    assert "evidence" not in result["message"].lower()
    assert "observation" not in engine.get_world_state()
    assert len(engine.get_history()) == 3
    assert start_state["player"] == engine.get_world_state()["player"]

    no_change = GameEngine(REGION_PATH, entry_location_id="bryn_shander_gate_west")
    assert no_change.process_command("wait")["message"] == "An hour passes."

    with TemporaryDirectory() as temp_dir:
        save_path = str(Path(temp_dir) / "wait-observation.json")
        engine.save(save_path)
        payload = build_save_data(engine)
        assert "observation" not in payload
        assert "elapsed_time_transition_observation" not in str(payload)
        loaded = load_game(save_path)
        assert loaded.get_world_state() == engine.get_world_state()
        assert loaded.process_command("wait")["message"] == "An hour passes."

    print("Elapsed-time transition observation tests passed.")


if __name__ == "__main__":
    main()
