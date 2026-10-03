from copy import deepcopy
from pathlib import Path
from test_artifact_files import artifact_files

from engine.contextual_action_projection import derive_contextual_action_projection
from engine.game_engine import GameEngine
from engine.save_system import SAVE_VERSION, build_save_data, load_game


REGION = "test_fixtures/bryn_shander_legacy.json"
CAPTAIN_CLUE = "The Captain's Deliberate Trail"
AFFORDANCE_TEXT = (
    "Elin Voss is at the Southwest Gate with the patrol orders. "
    "You can speak with her about them."
)


def opportunities(engine: GameEngine) -> list[str]:
    return engine.get_player_perception()["contextual_actions"]["opportunities"]


def prepare_discovered_captain_clue(engine: GameEngine) -> None:
    assert engine.process_command("talk to captain")["success"]
    assert engine.process_command("investigate")["investigation"]["changed"]


def arrive_at_west_gate_with_discovery_affordance(engine: GameEngine) -> None:
    prepare_discovered_captain_clue(engine)
    assert engine.present_clue(CAPTAIN_CLUE, "captain")["changed"]
    assert engine.process_command("go to Southwest Gate")["success"]
    assert engine.process_command("investigate")["investigation"]["changed"]


def test_authorized_categories_are_projected_and_narrated():
    engine = GameEngine(REGION)
    initial = opportunities(engine)
    assert "You can speak with Captain Darvin Grey." in initial
    assert "You can speak with Elin Voss." in initial
    assert "You can investigate this area." not in initial
    assert not any("present" in text.casefold() for text in initial)

    assert engine.process_command("talk to captain")["success"]
    assert "You can investigate this area." in opportunities(engine)

    assert engine.process_command("investigate")["investigation"]["changed"]
    clue_text = f"You can present {CAPTAIN_CLUE} to Captain Darvin Grey."
    assert clue_text in opportunities(engine)

    narration = engine.get_narration()
    assert clue_text in narration["contextual_actions"]
    assert clue_text in narration["description"]

    west_engine = GameEngine(REGION)
    arrive_at_west_gate_with_discovery_affordance(west_engine)
    assert AFFORDANCE_TEXT in opportunities(west_engine)
    assert AFFORDANCE_TEXT in west_engine.get_narration()["description"]


def test_projection_excludes_ineligible_or_unsafe_opportunities():
    engine = GameEngine(REGION)
    world = engine.get_world_state()
    scene = engine.get_scene_snapshot()
    region = engine.region

    assert "You can investigate this area." not in derive_contextual_action_projection(
        region, world, scene
    )["opportunities"]
    assert AFFORDANCE_TEXT not in derive_contextual_action_projection(
        region, world, scene
    )["opportunities"]

    absent_scene = deepcopy(scene)
    absent_scene["entities"]["static"] = []
    assert not any(
        "Captain Darvin Grey" in text
        for text in derive_contextual_action_projection(region, world, absent_scene)[
            "opportunities"
        ]
    )

    hidden_scene = deepcopy(scene)
    hidden_scene["entities"]["static"].remove("captain_darvin_grey")
    assert not any(
        "Captain Darvin Grey" in text
        for text in derive_contextual_action_projection(region, world, hidden_scene)[
            "opportunities"
        ]
    )

    ambiguous_region = deepcopy(region)
    ambiguous_region["entities"][1]["name"] = "Captain Darvin Grey"
    assert not any(
        text == "You can speak with Captain Darvin Grey."
        for text in derive_contextual_action_projection(
            ambiguous_region, world, scene
        )["opportunities"]
    )

    spawned_only_scene = deepcopy(scene)
    spawned_only_scene["entities"]["static"] = []
    spawned_only_scene["entities"]["spawned"] = [{"template": "captain_darvin_grey"}]
    assert not derive_contextual_action_projection(
        region, world, spawned_only_scene
    )["opportunities"]

    trace_world = deepcopy(world)
    trace_world["evidence_traces"] = [
        {
            "trace_id": "captain_conversation_gate_trace",
            "evidence_id": "captain_conversation_trace",
            "location_id": "bryn_shander_gate_north",
        }
    ]
    trace_world["player_discoveries"] = ["north_gate_captain_trace"]
    assert "You can investigate this area." not in derive_contextual_action_projection(
        region, trace_world, scene
    )["opportunities"]
    assert not any(
        "present" in text.casefold()
        for text in derive_contextual_action_projection(region, trace_world, scene)[
            "opportunities"
        ]
    )

    unknown_clue_world = deepcopy(trace_world)
    unknown_clue_world["player_discoveries"] = ["not_a_declared_clue"]
    assert not any(
        "present" in text.casefold()
        for text in derive_contextual_action_projection(
            region, unknown_clue_world, scene
        )["opportunities"]
    )

    undiscovered_world = deepcopy(trace_world)
    undiscovered_world["player_discoveries"] = []
    assert not any(
        "present" in text.casefold()
        for text in derive_contextual_action_projection(
            region, undiscovered_world, scene
        )["opportunities"]
    )

    resolved_world = deepcopy(trace_world)
    resolved_world["open_threads"] = {}
    resolved_world["resolved_threads"] = {
        "bryn_shander_west_road_bandit_report": {"status": "resolved"}
    }
    assert not any(
        "present" in text.casefold()
        for text in derive_contextual_action_projection(region, resolved_world, scene)[
            "opportunities"
        ]
    )

    hidden_target_scene = deepcopy(scene)
    hidden_target_scene["entities"]["static"].remove("captain_darvin_grey")
    eligible_world = deepcopy(trace_world)
    eligible_world["open_threads"] = {"bryn_shander_west_road_bandit_report": {}}
    assert not any(
        "present" in text.casefold()
        for text in derive_contextual_action_projection(
            region, eligible_world, hidden_target_scene
        )["opportunities"]
    )


def test_projection_is_deterministic_non_mutating_and_not_persisted():
    engine = GameEngine(REGION)
    prepare_discovered_captain_clue(engine)
    before_world = engine.get_world_state()
    before_history = engine.get_history()
    before_scene = engine.get_scene_snapshot()

    first = engine.get_player_perception()["contextual_actions"]
    second = engine.get_player_perception()["contextual_actions"]
    assert second == first
    assert engine.get_world_state() == before_world
    assert engine.get_history() == before_history
    assert engine.get_scene_snapshot() == before_scene
    assert "captain_darvin_grey" not in repr(first)
    assert "north_gate_captain_trace" not in repr(first)

    save_data = build_save_data(engine)
    assert SAVE_VERSION == 1
    assert "contextual_actions" not in save_data
    assert "contextual_actions" not in save_data["world_state"]

    with artifact_files("test_contextual_action_projection") as directory:
        save_path = str(Path(directory) / "test_contextual_action_projection_contextual-actions.json")
        engine.save(save_path)
        loaded = load_game(save_path)

    assert loaded.get_world_state() == engine.get_world_state()
    assert loaded.get_player_perception()["contextual_actions"] == first


def test_stale_clue_opportunity_remains_subject_to_existing_resolver():
    engine = GameEngine(REGION)
    prepare_discovered_captain_clue(engine)
    stale = f"You can present {CAPTAIN_CLUE} to Captain Darvin Grey."
    assert stale in opportunities(engine)

    assert engine.process_command("go south")["success"]
    result = engine.process_command(
        f"present {CAPTAIN_CLUE} to captain"
    )["presentation"]
    assert not result["changed"]


def main():
    test_authorized_categories_are_projected_and_narrated()
    test_projection_excludes_ineligible_or_unsafe_opportunities()
    test_projection_is_deterministic_non_mutating_and_not_persisted()
    test_stale_clue_opportunity_remains_subject_to_existing_resolver()
    print("Contextual action projection tests passed.")


if __name__ == "__main__":
    main()
