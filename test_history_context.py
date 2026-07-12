from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.history_context import (
    HISTORY_CONTEXT_SCHEMA,
    HISTORY_CONTEXT_VERSION,
    MAX_HISTORY_CONTEXT_COUNT,
)
from engine.save_system import load_game, save_game
from play_game import parse_history_query


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)

    empty_context = engine.get_history_context()
    assert empty_context["schema"] == HISTORY_CONTEXT_SCHEMA
    assert empty_context["version"] == HISTORY_CONTEXT_VERSION
    assert empty_context["limit"] == engine.get_default_history_query_count()
    assert empty_context["max_limit"] == MAX_HISTORY_CONTEXT_COUNT
    assert empty_context["history_entries"] == []
    assert empty_context["current_time"] == engine.get_world_state()["time"]
    assert empty_context["player"]["current_location_id"] == (
        engine.get_world_state()["player"]["current_location_id"]
    )

    starting_world_state = engine.get_world_state()
    assert engine.get_history_context() == empty_context
    assert engine.get_world_state() == starting_world_state

    for _ in range(6):
        wait_result = engine.process_command("wait")
        assert wait_result["success"]

    movement_south_result = engine.process_command("go south")
    assert movement_south_result["success"]

    for _ in range(6):
        wait_result = engine.process_command("wait")
        assert wait_result["success"]

    movement_north_result = engine.process_command("go north")
    assert movement_north_result["success"]

    full_history = engine.get_history()
    assert len(full_history) == 16

    default_context = engine.get_history_context()
    assert default_context["history_entries"] == full_history[-10:]
    assert len(default_context["history_entries"]) == 10
    assert all(
        entry.get("history_id")
        for entry in default_context["history_entries"]
    )

    explicit_context = engine.get_history_context(count=2)
    assert explicit_context["limit"] == 2
    assert explicit_context["history_entries"] == full_history[-2:]

    empty_limited_context = engine.get_history_context(count=0)
    assert empty_limited_context["limit"] == 0
    assert empty_limited_context["history_entries"] == []

    world_state_before_context = engine.get_world_state()
    mutable_context = engine.get_history_context(count=1)
    mutable_context["current_time"]["elapsed_hours"] = 999
    mutable_context["player"]["current_location_id"] = "mutated_location"
    mutable_context["history_entries"][0]["summary"] = "Mutated context."
    mutable_context["history_entries"][0]["history_id"] = "history_999999"

    assert engine.get_world_state() == world_state_before_context
    assert engine.get_history() == full_history

    try:
        engine.get_history_context(count=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("Negative history context count should fail.")

    try:
        engine.get_history_context(count=MAX_HISTORY_CONTEXT_COUNT + 1)
    except ValueError:
        pass
    else:
        raise AssertionError("Oversized history context count should fail.")

    assert parse_history_query("history context") == {"context": True}
    assert parse_history_query("history context 2") == {
        "context": True,
        "count": 2
    }
    assert "error" in parse_history_query("history context not-a-number")

    with TemporaryDirectory() as temp_dir:
        save_path = f"{temp_dir}/history_context_save.json"
        save_game(engine, save_path)
        loaded_engine = load_game(save_path)

    loaded_context = loaded_engine.get_history_context(count=3)
    assert loaded_context["history_entries"] == full_history[-3:]
    assert loaded_context["current_time"] == engine.get_world_state()["time"]
    assert loaded_context["player"]["current_location_id"] == (
        engine.get_world_state()["player"]["current_location_id"]
    )
    assert loaded_engine.get_history() == full_history

    look_result = loaded_engine.process_command("look")
    assert look_result["success"]

    print("History context test passed.")


if __name__ == "__main__":
    main()
