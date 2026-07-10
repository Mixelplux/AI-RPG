from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.save_system import load_game, save_game
from play_game import parse_history_query


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)

    assert engine.query_history() == []
    assert engine.query_history(count=1) == []
    assert engine.get_default_history_query_count() == 10

    starting_time = engine.get_world_state()["time"]

    for _ in range(6):
        wait_result = engine.process_command("wait")
        assert wait_result["success"]

    first_advanced_time = engine.get_world_state()["time"]
    assert first_advanced_time != starting_time

    movement_south_result = engine.process_command("go south")
    assert movement_south_result["success"]

    for _ in range(6):
        wait_result = engine.process_command("wait")
        assert wait_result["success"]

    movement_north_result = engine.process_command("go north")
    assert movement_north_result["success"]

    full_history = engine.get_history()
    assert len(full_history) == 14
    history_ids = [entry.get("history_id") for entry in full_history]
    assert history_ids == [
        f"history_{index:06d}"
        for index in range(1, len(full_history) + 1)
    ]
    assert len(history_ids) == len(set(history_ids))

    default_history = engine.query_history()
    assert default_history == full_history[-10:]
    assert all(entry.get("history_id") for entry in default_history)

    recent_two = engine.query_history(count=2)
    assert recent_two == full_history[-2:]

    time_entries = engine.query_history(event_type="time_advanced")
    all_time_entries = [
        entry for entry in full_history
        if entry["event_type"] == "time_advanced"
    ]
    assert len(all_time_entries) == 12
    assert len(time_entries) == 10
    assert time_entries == all_time_entries[-10:]
    assert all(
        entry["event_type"] == "time_advanced"
        for entry in time_entries
    )

    movement_entries = engine.query_history(event_type="player_movement")
    assert len(movement_entries) == 2
    assert all(
        entry["event_type"] == "player_movement"
        for entry in movement_entries
    )

    main_street_entries = engine.query_history(
        location="bryn_shander_main_street"
    )
    assert len(main_street_entries) == 7
    assert all(
        entry["location"] == "bryn_shander_main_street"
        for entry in main_street_entries
    )

    combined_entries = engine.query_history(
        count=1,
        event_type="time_advanced",
        location="bryn_shander_main_street"
    )
    assert combined_entries == [main_street_entries[-1]]

    world_state_before_query = engine.get_world_state()
    query_result = engine.query_history(count=1)
    query_result[0]["summary"] = "Mutated outside world state."
    query_result[0]["history_id"] = "history_999999"

    assert engine.get_world_state() == world_state_before_query
    assert engine.get_history() == full_history

    first_history_id = full_history[0]["history_id"]
    assert parse_history_query(f"history id {first_history_id}") == {
        "history_id": first_history_id
    }

    world_state_before_lookup = engine.get_world_state()
    lookup_result = engine.get_history_entry_by_id(first_history_id)
    assert lookup_result == full_history[0]
    lookup_result["summary"] = "Mutated lookup result."

    assert engine.get_world_state() == world_state_before_lookup
    assert engine.get_history() == full_history
    assert engine.get_history_entry_by_id("history_missing") is None
    assert engine.get_world_state() == world_state_before_lookup

    try:
        engine.query_history(count=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("Negative history query count should fail.")

    with TemporaryDirectory() as temp_dir:
        save_path = f"{temp_dir}/history_query_save.json"
        save_game(engine, save_path)
        loaded_engine = load_game(save_path)

    assert loaded_engine.query_history(count=2) == recent_two
    assert loaded_engine.query_history(event_type="time_advanced") == (
        time_entries
    )
    assert loaded_engine.query_history() == default_history
    assert loaded_engine.get_history() == full_history
    assert loaded_engine.get_history_entry_by_id(first_history_id) == (
        full_history[0]
    )
    assert loaded_engine.get_world_state()["time"] == (
        engine.get_world_state()["time"]
    )

    loaded_history_ids = {
        entry["history_id"]
        for entry in loaded_engine.get_history()
    }
    post_load_wait_result = loaded_engine.process_command("wait")
    assert post_load_wait_result["success"]
    post_load_history = loaded_engine.get_history()
    post_load_history_id = post_load_history[-1]["history_id"]
    assert post_load_history_id not in loaded_history_ids
    assert post_load_history_id == "history_000015"

    print("History query test passed.")


if __name__ == "__main__":
    main()
