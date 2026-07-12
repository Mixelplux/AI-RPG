from copy import deepcopy
from tempfile import TemporaryDirectory
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine.save_system import load_game, save_game
from play_game import main as play_game_main


REGION_PATH = "data/regions/bryn_shander.json"


def without_history(world_state):
    comparable_state = deepcopy(world_state)
    comparable_state["history"] = []
    return comparable_state


def main():
    engine = GameEngine(REGION_PATH)

    starting_state = engine.get_world_state()
    starting_location = starting_state["player"]["current_location_id"]
    starting_time = starting_state["time"]

    first_result = engine.process_command("talk to captain")
    assert first_result["success"]
    assert first_result["intent"] == "conversation"
    assert first_result["target_resolution"]["status"] == "resolved"
    assert first_result["target_resolution"]["target_type"] == "entity"
    assert first_result["target_resolution"]["identifier"] == (
        "captain_darvin_grey"
    )
    assert first_result["target_resolution"]["display_name"] == (
        "Captain Darvin Grey"
    )

    first_history = engine.get_history()
    assert len(first_history) == 6
    first_entry = first_history[0]
    assert first_entry["history_id"] == "history_000001"
    assert first_entry["event_type"] == "player_conversation"
    assert first_entry["summary"] == (
        "Player initiated a conversation with Captain Darvin Grey."
    )
    assert first_entry["location"] == starting_location
    assert first_entry["time"] == starting_time
    assert first_entry["target_entity_id"] == "captain_darvin_grey"
    assert first_entry["target_display_name"] == "Captain Darvin Grey"
    assert first_result["pressure_consequence"]["source_history_id"] == (
        first_entry["history_id"]
    )
    assert first_history[1]["event_type"] == "pressure_changed"
    assert first_history[2]["event_type"] == "actor_moved"
    assert first_history[2]["source_history_id"] == first_entry["history_id"]
    assert first_history[3]["event_type"] == "unresolved_thread_opened"
    assert first_history[3]["source_history_id"] == first_entry["history_id"]
    assert first_history[4]["event_type"] == "actor_knowledge_added"
    assert first_history[4]["source_history_id"] == first_entry["history_id"]

    after_first_state = engine.get_world_state()
    assert after_first_state["player"]["current_location_id"] == (
        starting_location
    )
    assert after_first_state["time"] == starting_time
    expected_after_first = without_history(starting_state)
    expected_after_first["pressures"]["bryn_shander_gate_scrutiny"][
        "level"
    ] = 25
    expected_after_first["actor_location_overrides"] = {
        "guard_elin_voss": "bryn_shander_main_street"
    }
    expected_after_first["open_threads"] = {
        "bryn_shander_west_road_bandit_report": {
            "thread_id": "bryn_shander_west_road_bandit_report",
            "status": "open",
            "created_by_history_id": first_entry["history_id"],
        }
    }
    expected_after_first["actor_knowledge"]["captain_darvin_grey"].append(
        "player_spoke_with_captain"
    )
    expected_after_first["evidence_traces"] = [{
        "trace_id": "captain_conversation_gate_trace",
        "evidence_id": "captain_conversation_trace",
        "location_id": "bryn_shander_gate_north",
    }]
    assert without_history(after_first_state) == expected_after_first

    second_result = engine.process_command("talk to captain")
    assert second_result["success"]
    conversation_entries = engine.query_history(
        event_type="player_conversation"
    )
    assert len(conversation_entries) == 2
    assert conversation_entries[0]["history_id"] == "history_000001"
    assert conversation_entries[1]["history_id"] == "history_000007"
    assert conversation_entries[1]["target_entity_id"] == (
        "captain_darvin_grey"
    )

    ambiguous_result = engine.process_command("talk to guard")
    assert not ambiguous_result["success"]
    assert ambiguous_result["target_resolution"]["status"] == "ambiguous"
    assert len(engine.query_history(event_type="player_conversation")) == 2

    unresolved_result = engine.process_command("talk to blacksmith")
    assert not unresolved_result["success"]
    assert unresolved_result["target_resolution"]["status"] == "unresolved"
    assert len(engine.query_history(event_type="player_conversation")) == 2

    exit_result = engine.process_command("talk to north")
    assert exit_result["success"]
    assert exit_result["target_resolution"]["status"] == "resolved"
    assert exit_result["target_resolution"]["target_type"] == "exit"
    assert len(engine.query_history(event_type="player_conversation")) == 2

    assert engine.get_world_state()["player"]["current_location_id"] == (
        starting_location
    )
    assert engine.get_world_state()["time"] == starting_time
    expected_final = without_history(starting_state)
    expected_final["pressures"]["bryn_shander_gate_scrutiny"]["level"] = 25
    expected_final["actor_location_overrides"] = {
        "guard_elin_voss": "bryn_shander_main_street"
    }
    expected_final["open_threads"] = {
        "bryn_shander_west_road_bandit_report": {
            "thread_id": "bryn_shander_west_road_bandit_report",
            "status": "open",
            "created_by_history_id": first_entry["history_id"],
        }
    }
    expected_final["actor_knowledge"]["captain_darvin_grey"].append(
        "player_spoke_with_captain"
    )
    expected_final["evidence_traces"] = [{
        "trace_id": "captain_conversation_gate_trace",
        "evidence_id": "captain_conversation_trace",
        "location_id": "bryn_shander_gate_north",
    }]
    assert without_history(engine.get_world_state()) == expected_final

    history_context = engine.get_history_context(count=2)
    assert history_context["history_entries"] == engine.get_history()[-2:]

    narration_context = engine.get_narration_context(
        "talk to captain",
        history_count=2
    )
    assert narration_context["history_context"]["history_entries"] == (
        [
            entry
            for entry in engine.get_history()[-2:]
            if entry["event_type"] not in {
                "pressure_changed", "actor_moved", "unresolved_thread_opened",
                "actor_knowledge_added", "evidence_trace_added"
            }
        ]
    )

    with TemporaryDirectory() as temp_dir:
        save_path = f"{temp_dir}/conversation_history_save.json"
        save_game(engine, save_path)
        loaded_engine = load_game(save_path)

    loaded_history = loaded_engine.get_history()
    assert loaded_history == engine.get_history()
    loaded_history_ids = {
        entry["history_id"]
        for entry in loaded_history
    }

    post_load_result = loaded_engine.process_command("talk to captain")
    assert post_load_result["success"]
    post_load_history = loaded_engine.get_history()
    assert len(post_load_history) == 8
    assert post_load_history[-1]["history_id"] == "history_000008"
    assert post_load_history[-1]["history_id"] not in loaded_history_ids
    assert post_load_history[-1]["target_entity_id"] == (
        "captain_darvin_grey"
    )

    movement_result = loaded_engine.process_command("go south")
    assert movement_result["success"]
    assert loaded_engine.get_world_state()["player"]["current_location_id"] == (
        "bryn_shander_main_street"
    )

    wait_result = loaded_engine.process_command("wait")
    assert wait_result["success"]
    assert loaded_engine.get_world_state()["time"] != starting_time

    destination_result = loaded_engine.process_command("head to the inn")
    assert destination_result["success"]
    assert destination_result["destination_resolution"]["status"] == (
        "resolved"
    )

    skill_result = loaded_engine.process_command("check athletics")
    assert skill_result["success"]
    assert skill_result["skill_check"]["check_name"] == "athletics"

    narration_preview = loaded_engine.get_narration_preview("look around")
    assert narration_preview["accepted"]
    assert narration_preview["display_text"] == (
        "The street remains quiet. "
        "The cold has become noticeably more severe."
    )

    loaded_engine.reset()
    assert loaded_engine.get_world_state()["history"] == []
    assert loaded_engine.get_world_state()["player"]["current_location_id"] == (
        starting_location
    )

    with TemporaryDirectory() as temp_dir:
        cli_save_path = f"{temp_dir}/cli_save.json"
        with patch("play_game.SAVE_PATH", cli_save_path), patch(
            "builtins.input",
            side_effect=[
                "pressures",
                "talk to captain",
                "history",
                "save",
                "load",
                "history type player_conversation",
                "quit",
            ]
        ):
            play_game_main()

    print("Interaction history test passed.")


if __name__ == "__main__":
    main()
