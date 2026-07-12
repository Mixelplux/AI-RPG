from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.narration_context import (
    NARRATION_CONTEXT_ATMOSPHERE_EXAMPLE,
    NARRATION_CONTEXT_BOUNDARY_RULE,
    NARRATION_CONTEXT_DRIFT_GUARDRAIL,
    NARRATION_CONTEXT_SCHEMA,
    NARRATION_CONTEXT_VERSION,
)
from engine.save_system import load_game, save_game
from play_game import parse_narration_context_command


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)
    player_input = "look toward the south gate"

    empty_context = engine.get_narration_context(player_input)
    assert empty_context["schema"] == NARRATION_CONTEXT_SCHEMA
    assert empty_context["version"] == NARRATION_CONTEXT_VERSION
    assert empty_context["player_input"] == player_input
    assert empty_context["current_time"] == engine.get_world_state()["time"]
    assert empty_context["player"]["current_location_id"] == (
        engine.get_world_state()["player"]["current_location_id"]
    )
    assert empty_context["scene_snapshot"] == engine.get_scene_snapshot()
    assert empty_context["history_context"] == engine.get_history_context()
    assert empty_context["history_context"]["history_entries"] == []
    assert empty_context["boundary"]["rule"] == NARRATION_CONTEXT_BOUNDARY_RULE
    assert (
        empty_context["boundary"]["drift_guardrail"]
        == NARRATION_CONTEXT_DRIFT_GUARDRAIL
    )
    assert (
        empty_context["boundary"]["atmosphere_example"]
        == NARRATION_CONTEXT_ATMOSPHERE_EXAMPLE
    )
    assert "blizzard" in empty_context["boundary"]["atmosphere_example"]
    assert "gloves" in empty_context["boundary"]["atmosphere_example"]

    starting_world_state = engine.get_world_state()
    starting_history = engine.get_history()
    assert engine.get_narration_context(player_input) == empty_context
    assert engine.get_world_state() == starting_world_state
    assert engine.get_history() == starting_history

    for _ in range(4):
        wait_result = engine.process_command("wait")
        assert wait_result["success"]

    movement_result = engine.process_command("go south")
    assert movement_result["success"]

    full_history = engine.get_history()
    assert len(full_history) == 7

    bounded_context = engine.get_narration_context(
        "describe what I can see",
        history_count=2
    )
    assert bounded_context["history_context"]["limit"] == 2
    assert bounded_context["history_context"]["history_entries"] == (
        full_history[-2:]
    )
    assert all(
        entry.get("history_id")
        for entry in bounded_context["history_context"]["history_entries"]
    )

    world_state_before_context = engine.get_world_state()
    history_before_context = engine.get_history()
    scene_before_context = engine.get_scene_snapshot()
    repeated_context = engine.get_narration_context(
        "describe what I can see",
        history_count=2
    )
    assert repeated_context == bounded_context
    assert engine.get_world_state() == world_state_before_context
    assert engine.get_history() == history_before_context
    assert engine.get_scene_snapshot() == scene_before_context

    mutable_context = engine.get_narration_context("inspect the road")
    mutable_context["current_time"]["elapsed_hours"] = 999
    mutable_context["player"]["current_location_id"] = "mutated_location"
    mutable_context["scene_snapshot"]["scene_id"] = "mutated_scene"
    mutable_context["history_context"]["history_entries"][0]["summary"] = (
        "Mutated context."
    )
    mutable_context["history_context"]["history_entries"][0]["history_id"] = (
        "history_999999"
    )

    assert engine.get_world_state() == world_state_before_context
    assert engine.get_history() == history_before_context
    assert engine.get_scene_snapshot() == scene_before_context

    try:
        engine.get_narration_context("listen", history_count=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("Negative narration history count should fail.")

    assert parse_narration_context_command(
        "narration context look at the gate"
    ) == {"player_input": "look at the gate"}
    assert "error" in parse_narration_context_command("narration context")

    with TemporaryDirectory() as temp_dir:
        save_path = f"{temp_dir}/narration_context_save.json"
        save_game(engine, save_path)
        loaded_engine = load_game(save_path)

    loaded_context = loaded_engine.get_narration_context(
        "look at the road",
        history_count=3
    )
    assert loaded_context["history_context"]["history_entries"] == (
        full_history[-3:]
    )
    assert loaded_context["current_time"] == engine.get_world_state()["time"]
    assert loaded_context["player"]["current_location_id"] == (
        engine.get_world_state()["player"]["current_location_id"]
    )
    assert loaded_engine.get_history() == full_history

    print("Narration context test passed.")


if __name__ == "__main__":
    main()
