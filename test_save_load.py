import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.save_system import SAVE_VERSION, build_save_data, save_game, load_game


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)

    starting_location = engine.get_world_state()["player"]["current_location_id"]
    print(f"Starting location: {starting_location}")
    starting_time = engine.get_world_state()["time"]
    print(f"Starting time: {starting_time}")
    starting_pressures = engine.get_pressures()
    assert starting_pressures

    conversation_result = engine.process_command("talk to elin")
    assert conversation_result["success"]
    source_entry = deepcopy(engine.get_history()[-1])
    linked_result = engine.set_pressure_level_from_event(
        "bryn_shander_winter",
        70,
        source_entry["history_id"],
    )

    wait_result = engine.process_command("wait")
    advanced_time = engine.get_world_state()["time"]
    print(f"Advanced time: {advanced_time}")

    assert wait_result["success"]
    assert wait_result["time_advancement"]["previous_time"] == starting_time
    assert wait_result["time_advancement"]["new_time"] == advanced_time
    assert advanced_time != starting_time

    engine.process_command("go south")

    moved_location = engine.get_world_state()["player"]["current_location_id"]
    print(f"Moved location: {moved_location}")
    history_before_save = engine.get_history()
    assert len(history_before_save) >= 2
    history_ids_before_save = [
        entry.get("history_id")
        for entry in history_before_save
    ]
    assert all(history_ids_before_save)
    assert len(history_ids_before_save) == len(set(history_ids_before_save))
    time_entry = next(
        entry
        for entry in history_before_save
        if entry["event_type"] == "time_advanced"
    )
    assert time_entry["previous_time"] == starting_time
    assert time_entry["new_time"] == advanced_time
    assert history_before_save[-1]["event_type"] == "player_movement"

    with TemporaryDirectory() as temp_dir:
        save_path = f"{temp_dir}/test_save.json"
        save_payload = build_save_data(engine)
        assert save_payload["save_version"] == SAVE_VERSION == 1
        assert save_payload["world_state"]["pressures"] == engine.get_pressures()
        save_game(engine, save_path)
        loaded_engine = load_game(save_path)

    loaded_world_state = loaded_engine.get_world_state()

    loaded_location = loaded_world_state["player"]["current_location_id"]
    print(f"Loaded location: {loaded_location}")

    assert loaded_location == moved_location
    assert loaded_world_state["weather"] == engine.get_world_state()["weather"]
    assert loaded_world_state["time"] == advanced_time
    assert loaded_world_state["history"] == history_before_save
    assert loaded_world_state["pressures"] == engine.get_pressures()
    assert loaded_engine.get_pressures() == engine.get_pressures()
    loaded_source = loaded_engine.get_history_entry_by_id(
        source_entry["history_id"]
    )
    loaded_consequence = loaded_engine.get_history_entry_by_id(
        linked_result["history_id"]
    )
    assert loaded_source == source_entry
    assert loaded_consequence["source_history_id"] == source_entry["history_id"]

    loaded_history_ids = {
        entry["history_id"]
        for entry in loaded_world_state["history"]
    }
    post_load_wait_result = loaded_engine.process_command("wait")
    post_load_history = loaded_engine.get_history()

    assert post_load_wait_result["success"]
    assert len(post_load_history) == len(history_before_save) + 1
    assert post_load_history[-1]["history_id"] not in loaded_history_ids

    with TemporaryDirectory() as temp_dir:
        base_payload = build_save_data(engine)

        unlinked_payload = deepcopy(base_payload)
        del unlinked_payload["world_state"]["history"][1]["source_history_id"]
        unlinked_path = Path(temp_dir) / "unlinked.json"
        unlinked_path.write_text(json.dumps(unlinked_payload), encoding="utf-8")
        load_game(str(unlinked_path))

        invalid_references = (
            (None, "non-string"),
            ("", "empty"),
            ("history_999999", "dangling"),
            (linked_result["history_id"], "self"),
        )
        for invalid_reference, label in invalid_references:
            payload = deepcopy(base_payload)
            payload["world_state"]["history"][1]["source_history_id"] = (
                invalid_reference
            )
            path = Path(temp_dir) / f"{label}.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            try:
                load_game(str(path))
            except ValueError:
                pass
            else:
                raise AssertionError(f"Loaded {label} source reference.")

        forward_payload = deepcopy(base_payload)
        forward_payload["world_state"]["history"][0]["source_history_id"] = (
            linked_result["history_id"]
        )
        forward_path = Path(temp_dir) / "forward.json"
        forward_path.write_text(json.dumps(forward_payload), encoding="utf-8")
        try:
            load_game(str(forward_path))
        except ValueError:
            pass
        else:
            raise AssertionError("Loaded forward source reference.")

    print("Save/load test passed.")


if __name__ == "__main__":
    main()
