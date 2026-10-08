"""Offline tests of the owner launch loop and its real narration boundary."""

from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from unittest.mock import patch

import play_game
from engine.game_engine import GameEngine
from engine.narration_pipeline import build_narration_preview_packet
from engine.narration_source import (
    NARRATION_SOURCE_SCHEMA, NARRATION_SOURCE_VERSION,
    NARRATION_SOURCE_OPENAI_RESPONSES, NARRATION_SOURCE_METADATA,
)
from engine.narration_output import NARRATION_OUTPUT_SCHEMA, NARRATION_OUTPUT_VERSION


REGION = "data/regions/bryn_shander.json"
INTENTION = "i walk through the market and see what people are selling"


def run_cli(engine, commands, source=None):
    prompts, states = [], []
    output = StringIO()
    iterator = iter(commands)

    def offline_source(prompt):
        prompts.append(deepcopy(prompt))
        activity = prompt["deterministic_input"]["scene_context"]["expected_activity"]
        # Test source only: proves conditions affect the presented source result.
        text = {
            "ordinary": "Provisions lie on the stalls as carts pass between them.",
            "sparse": "Snow drives the few remaining sellers toward shelter.",
            "effectively_absent": "Blowing snow scours shuttered stalls; outdoor trade has stopped.",
        }.get(activity["availability"], "The surroundings come into view.")
        candidate = {
            "schema": NARRATION_OUTPUT_SCHEMA, "version": NARRATION_OUTPUT_VERSION,
            "narration_text": text,
        }
        if source is not None:
            candidate = source(candidate)
        return {
            "schema": NARRATION_SOURCE_SCHEMA, "version": NARRATION_SOURCE_VERSION,
            "source": NARRATION_SOURCE_OPENAI_RESPONSES,
            "source_prompt": deepcopy(prompt), "candidate": candidate,
            "metadata": deepcopy(NARRATION_SOURCE_METADATA),
        }

    def read_input(_):
        states.append(engine.get_world_state())
        return next(iterator)

    with patch.object(play_game.GameEngine, "start_new", return_value=engine), \
         patch("builtins.input", side_effect=read_input), \
         patch("engine.game_engine.build_narration_preview_packet",
               side_effect=lambda context: build_narration_preview_packet(
                   context, source_builder=offline_source)), \
         patch("socket.create_connection", side_effect=AssertionError("network forbidden")), \
         redirect_stdout(output):
        play_game.main()
    return output.getvalue(), prompts, states


def test_owner_smoke_route():
    for kind, severity, availability, prose in (
        ("clear", 0.1, "ordinary", "Provisions lie"),
        ("blizzard", 0.5, "sparse", "few remaining sellers"),
        ("blizzard", 0.9, "effectively_absent", "outdoor trade has stopped"),
    ):
        state = GameEngine(REGION).get_world_state()
        state["weather"].update(type=kind, severity=severity)
        state["time"]["time_of_day"] = "day"
        engine = GameEngine(REGION, initial_world_state=state)
        output, prompts, states = run_cli(engine, ["go to market square", "look", INTENTION, "quit"])
        assert [p["deterministic_input"]["player_input"] for p in prompts] == [
            "go to market square", "look", INTENTION,
        ]
        assert prose in output
        assert "You cannot go that way" not in output
        assert "You take a closer look" not in output
        assert "central Market Square" not in output
        assert "The weather is blizzard" not in output
        assert states[1] == states[2] == states[3] == engine.get_world_state()
        presentations = [p["deterministic_input"]["scene_context"]["presentation"] for p in prompts]
        assert [p["stage"] for p in presentations] == ["orient", "expand", "follow"]
        assert presentations[0]["established_details"] == []
        assert presentations[1]["established_details"]
        assert presentations[2]["established_details"] == presentations[1]["established_details"]
        assert presentations[2]["focus"] == INTENTION
        assert presentations[1]["previous_conditions"]["weather"]["type"] == kind
        assert "You move " not in output
        assert "You make your way to Market Square." in output
        for prompt in prompts:
            context = prompt["deterministic_input"]
            scene = context["scene_context"]
            assert "player" not in context and "scene_snapshot" not in context
            assert "temporary stalls" in scene["location_facts"]["description"]
            assert scene["expected_activity"]["availability"] == availability
            assert scene["conditions"]["weather"]["type"] == kind
            assert "calendar_system" not in scene["conditions"]["time"]
            assert scene["player_intention"]["declared_text"] == context["player_input"]
            contract = prompt["instructions"]["scene_narration_contract"]
            assert "Do not contradict" in contract["continuity"]
            assert "authority restrictions always take precedence" in contract["continuity"]
            assert "add resolution" in contract["progression"]
            assert "what the new action reveals" in contract["progression"]
            assert "express their effects" in contract["condition_continuation"]
            assert "common goods" in contract["incidental_freedom"]
            assert "important NPC presence" in contract["consequential_limit"]
            assert "spending" in contract["intention_limit"]
            assert "abandoning the goal" in contract["intention_limit"]


def test_explicit_navigation_and_narrow_intention():
    engine = GameEngine(REGION)
    assert engine.process_command("go to market square")["success"]
    for command in (INTENTION, "I stroll around the stalls", "I move among the carts"):
        before = engine.get_world_state()
        result = engine.process_command(command)
        assert result["success"] and result["intent"] == "player_intention"
        assert result["action"]["type"] == "narrate_intention"
        assert engine.get_world_state() == before
    for command in ("go north", "walk north", "i walk north", "move to Main Street"):
        result = engine.process_command(command)
        assert result["intent"] == "movement"
    assert engine.process_command("go to market square")["success"]
    assert engine.process_command("move to Main Street")["success"]
    assert engine.process_command("head to Market Square")["intent"] == "destination"
    assert engine.process_command("frobnicate")["intent"] == "unknown"


def test_failure_does_not_dump_grounding_or_mutate():
    engine = GameEngine(REGION, entry_location_id="market_square")
    before = engine.get_world_state()
    output, prompts, _ = run_cli(engine, ["look", "quit"],
                                 source=lambda c: {**c, "world_state": {}})
    assert len(prompts) == 2
    assert output.count("Scene narration is unavailable") == 2
    assert "central Market Square" not in output
    assert "You take a closer look" not in output
    assert engine.get_world_state() == before
    assert all(not p["deterministic_input"]["scene_context"]["presentation"]["established_details"]
               for p in prompts)


def test_new_details_and_scene_reset():
    engine = GameEngine(REGION, entry_location_id="market_square")
    details = iter([
        "You see closed stalls and pedestrians seeking shelter.",
        "You notice snow collecting on folded awnings.",
        "You follow the shuttered storefronts.",
        "You return to the quiet square.",
    ])
    _, prompts, _ = run_cli(engine, ["look", INTENTION, "go north", "go to market square", "quit"],
                            source=lambda c: {**c, "narration_text": next(details)})
    presentations = [p["deterministic_input"]["scene_context"]["presentation"] for p in prompts]
    assert "closed stalls" in " ".join(presentations[1]["established_details"])
    assert "folded awnings" in " ".join(presentations[2]["established_details"])
    assert presentations[-1]["stage"] == "orient"
    assert presentations[-1]["established_details"] == []


def test_continuity_bounds_and_interruption_presentation():
    from engine.scene_continuity import SceneContinuity, MAX_DETAILS, validate_scene_presentation
    continuity = SceneContinuity()
    scene = {"location": {"location_id": "market_square"}}
    continuity.presentation(scene, "look", "expand")
    for n in range(40):
        continuity.remember(f"You notice ordinary detail {n}.", {"time": {"elapsed_hours": n}})
    value = continuity.presentation(scene, "talk to a trader", "narrow")
    assert len(value["established_details"]) == MAX_DETAILS
    assert value["stage"] == "narrow"
    assert "detail 0." in value["established_details"][0]
    assert "detail 39." in value["established_details"][-1]
    validate_scene_presentation(value)
    value["established_details"].clear()
    assert continuity.details
    # Nonroutine/failed travel remains visible instead of being compressed away.
    result = {"success": False, "intent": "movement", "movement_hops": [{}],
              "message": "The way is blocked."}
    assert play_game.travel_presentation(result, None) == result["message"]
    result.update(success=True, message="You stop at a disturbance.")
    assert play_game.travel_presentation(result, None) == result["message"]


def test_focused_observation_and_interaction():
    engine = GameEngine(REGION, entry_location_id="market_square")
    _, prompts, _ = run_cli(engine, ["inspect the awnings", "talk", "look", "quit"])
    presentations = [p["deterministic_input"]["scene_context"]["presentation"] for p in prompts]
    assert [p["stage"] for p in presentations] == ["orient", "follow", "narrow", "expand"]
    assert presentations[2]["established_details"]
    assert presentations[3]["established_details"]


def test_live_prompt_causal_locality():
    from test_west_road_scene_relevance import cases
    for _, engine, theft_occurred in cases():
        output, prompts, _ = run_cli(engine, ["go to Market Square", "look", INTENTION, "quit"])
        assert len(prompts) == 3
        for prompt in prompts:
            material = json.dumps(prompt["deterministic_input"]).lower()
            assert ("lamp oil" in material) == theft_occurred
            for remote in ("abandoned lookout", "withdrawal route", "local pursuit is complete"):
                assert remote not in material
            perspective = prompt["deterministic_input"]["scene_context"]["character_perspective"]
            assert all(perspective[layer] == [] for layer in (
                "observations", "recognition", "findings", "approaches", "accepted_outcomes",
            ))
        assert "You cannot go that way" not in output


def main():
    test_owner_smoke_route()
    test_explicit_navigation_and_narrow_intention()
    test_failure_does_not_dump_grounding_or_mutate()
    test_live_prompt_causal_locality()
    test_new_details_and_scene_reset()
    test_continuity_bounds_and_interruption_presentation()
    test_focused_observation_and_interaction()
    print("Player scene route passed: arrivals, weather, look, intent, navigation, contracts and fail-closed output.")


if __name__ == "__main__":
    main()
