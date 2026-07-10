from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.save_system import save_game, load_game


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)

    starting_location = engine.get_world_state()["player"]["current_location_id"]
    print(f"Starting location: {starting_location}")
    starting_time = engine.get_world_state()["time"]
    print(f"Starting time: {starting_time}")

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
    assert history_before_save[0]["event_type"] == "time_advanced"
    assert history_before_save[0]["previous_time"] == starting_time
    assert history_before_save[0]["new_time"] == advanced_time
    assert history_before_save[-1]["event_type"] == "player_movement"

    with TemporaryDirectory() as temp_dir:
        save_path = f"{temp_dir}/test_save.json"
        save_game(engine, save_path)
        loaded_engine = load_game(save_path)

    loaded_world_state = loaded_engine.get_world_state()

    loaded_location = loaded_world_state["player"]["current_location_id"]
    print(f"Loaded location: {loaded_location}")

    assert loaded_location == moved_location
    assert loaded_world_state["weather"] == engine.get_world_state()["weather"]
    assert loaded_world_state["time"] == advanced_time
    assert loaded_world_state["history"] == history_before_save

    loaded_history_ids = {
        entry["history_id"]
        for entry in loaded_world_state["history"]
    }
    post_load_wait_result = loaded_engine.process_command("wait")
    post_load_history = loaded_engine.get_history()

    assert post_load_wait_result["success"]
    assert len(post_load_history) == len(history_before_save) + 1
    assert post_load_history[-1]["history_id"] not in loaded_history_ids

    print("Save/load test passed.")


if __name__ == "__main__":
    main()
