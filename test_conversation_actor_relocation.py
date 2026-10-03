import json
from copy import deepcopy
from pathlib import Path
from test_artifact_files import artifact_files
from unittest.mock import patch

import engine.game_engine as game_engine_module
from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import load_game, save_game


REGION_PATH = "test_fixtures/bryn_shander_legacy.json"
THREAD = "bryn_shander_west_road_bandit_report"
ACTOR = "guard_elin_voss"
DESTINATION = "bryn_shander_gate_west"
EFFECT = "west_road_report_sends_elin_west"
CLUE = "The Captain's Deliberate Trail"


def region_data():
    return json.loads(Path(REGION_PATH).read_text(encoding="utf-8"))


def expect_invalid(region, text):
    try:
        validate_region(region)
    except ValueError as error:
        assert text in str(error), str(error)
        return
    raise AssertionError("Expected invalid Region Pack.")


def resolve(engine):
    engine.process_command("talk to captain")
    engine.process_command("investigate")
    return engine.process_command(f"present {CLUE} to captain")["presentation"]


def test_declaration_validation():
    region = region_data()
    validate_region(region)
    absent = deepcopy(region)
    del absent["resolved_thread_actor_relocation_effect"]
    del absent["resolved_thread_evidence_trace_effect"]
    del absent["conversation_player_discovery_response"]
    del absent["conversation_affordance"]
    validate_region(absent)
    for value in ([], "effect"):
        invalid = deepcopy(region)
        invalid["resolved_thread_actor_relocation_effect"] = value
        expect_invalid(invalid, "fields are invalid")
    for field in ("effect_id", "resolved_thread_id", "actor_entity_id", "destination_location_id"):
        invalid = deepcopy(region)
        invalid["resolved_thread_actor_relocation_effect"][field] = ""
        expect_invalid(invalid, "non-empty strings")
    for field in ("resolved_thread_id", "actor_entity_id", "destination_location_id"):
        invalid = deepcopy(region)
        invalid["resolved_thread_actor_relocation_effect"][field] = "unknown"
        expect_invalid(invalid, field)
    spawned = deepcopy(region)
    spawned["resolved_thread_actor_relocation_effect"]["actor_entity_id"] = "spawned_guard_1"
    expect_invalid(spawned, "static actor")
    conflicting = deepcopy(region)
    conflicting["resolved_thread_actor_relocation_effect"]["effect_id"] = (
        conflicting["conversation_pressure_effects"][0]["effect_id"]
    )
    expect_invalid(conflicting, "conflicts with another Region Pack effect identity")


def test_atomic_material_relocation_and_revisit():
    engine = GameEngine(REGION_PATH)
    original_validate, original_build = game_engine_module.validate_world_state, game_engine_module.build_scene
    counts = {"validate": 0, "build": 0}
    with patch.object(game_engine_module, "validate_world_state", side_effect=lambda *a, **k: (counts.__setitem__("validate", counts["validate"] + 1), original_validate(*a, **k))[1]), patch.object(game_engine_module, "build_scene", side_effect=lambda *a, **k: (counts.__setitem__("build", counts["build"] + 1), original_build(*a, **k))[1]):
        result = resolve(engine)
    assert counts == {"validate": 3, "build": 3}  # conversation, discovery, presentation
    consequence = result["actor_location_consequence"]
    assert consequence == {"status": "applied"}
    assert engine.get_world_state()["actor_location_overrides"] == {ACTOR: DESTINATION}
    presented = engine.query_history(event_type="clue_presented")[-1]
    resolved = engine.query_history(event_type="unresolved_thread_resolved")[-1]
    moved = engine.query_history(event_type="actor_moved")[-1]
    assert resolved["source_history_id"] == moved["source_history_id"] == presented["history_id"]
    revisit = GameEngine(REGION_PATH, entry_location_id=DESTINATION,
                         initial_world_state=engine.get_world_state())
    assert ACTOR in revisit.get_scene_snapshot()["entities"]["static"]
    assert revisit.resolve_target("elin")["status"] == "resolved"
    assert ACTOR in revisit.get_player_perception()["visible"]["entities"]["static"]
    assert engine.process_command(f"present {CLUE} to captain")["presentation"]["changed"] is False
    assert len(engine.query_history(event_type="actor_moved")) == 1


def test_noop_save_load_and_failure_isolation():
    engine = GameEngine(REGION_PATH)
    engine.set_actor_location(ACTOR, DESTINATION)
    moves_before = len(engine.query_history(event_type="actor_moved"))
    result = resolve(engine)
    assert result["changed"] and result["actor_location_consequence"] == {"status": "no_op"}
    assert len(engine.query_history(event_type="actor_moved")) == moves_before
    with artifact_files("test_conversation_actor_relocation") as directory:
        path = str(Path(directory) / "test_conversation_actor_relocation_relocation.json")
        save_game(engine, path)
        loaded = load_game(path)
        assert loaded.get_world_state()["actor_location_overrides"] == {ACTOR: DESTINATION}
        assert loaded.process_command(f"present {CLUE} to captain")["presentation"]["changed"] is False

    without_declaration = region_data()
    del without_declaration["resolved_thread_actor_relocation_effect"]
    del without_declaration["resolved_thread_evidence_trace_effect"]
    del without_declaration["conversation_player_discovery_response"]
    del without_declaration["conversation_affordance"]
    with artifact_files("test_conversation_actor_relocation") as directory:
        path = Path(directory) / "test_conversation_actor_relocation_without-relocation.json"
        path.write_text(json.dumps(without_declaration), encoding="utf-8")
        engine = GameEngine(str(path))
        result = resolve(engine)
    assert result["changed"] and result["actor_location_consequence"] is None

    for target, error in (("validate_world_state", ValueError("state")), ("build_scene", RuntimeError("scene"))):
        engine = GameEngine(REGION_PATH)
        engine.process_command("talk to captain"); engine.process_command("investigate")
        state, scene = engine.get_world_state(), engine.scene_snapshot
        with patch.object(game_engine_module, target, side_effect=error):
            try: engine.process_command(f"present {CLUE} to captain")
            except type(error): pass
            else: raise AssertionError("Injected failure was swallowed.")
        assert engine.get_world_state() == state and engine.scene_snapshot is scene


def test_relocation_preparation_and_history_failures_are_atomic():
    for target, error in (
        ("_prepare_actor_location_candidate", ValueError("relocation")),
    ):
        engine = GameEngine(REGION_PATH)
        engine.process_command("talk to captain"); engine.process_command("investigate")
        state, scene = engine.get_world_state(), engine.scene_snapshot
        with patch.object(engine, target, side_effect=error):
            try: engine.process_command(f"present {CLUE} to captain")
            except type(error): pass
            else: raise AssertionError("Injected failure was swallowed.")
        assert engine.get_world_state() == state
        assert engine.scene_snapshot is scene
        assert THREAD in engine.get_open_threads()
        assert THREAD not in engine.get_world_state()["resolved_threads"]
        assert not engine.get_world_state()["actor_location_overrides"]

    engine = GameEngine(REGION_PATH)
    engine.process_command("talk to captain"); engine.process_command("investigate")
    state, scene = engine.get_world_state(), engine.scene_snapshot
    original_add_history = game_engine_module.add_history_entry

    def fail_actor_move(candidate, event_type, *args, **kwargs):
        if event_type == "actor_moved":
            raise ValueError("actor history")
        return original_add_history(candidate, event_type, *args, **kwargs)

    with patch.object(game_engine_module, "add_history_entry", side_effect=fail_actor_move):
        try: engine.process_command(f"present {CLUE} to captain")
        except ValueError as error: assert "actor history" in str(error)
        else: raise AssertionError("Injected history failure was swallowed.")
    assert engine.get_world_state() == state
    assert engine.scene_snapshot is scene
    assert THREAD in engine.get_open_threads()
    assert THREAD not in engine.get_world_state()["resolved_threads"]
    assert not engine.get_world_state()["actor_location_overrides"]
    assert not engine.query_history(event_type="clue_presented")
    assert not engine.query_history(event_type="unresolved_thread_resolved")
    assert not engine.query_history(event_type="actor_moved")


if __name__ == "__main__":
    test_declaration_validation()
    test_atomic_material_relocation_and_revisit()
    test_noop_save_load_and_failure_isolation()
    test_relocation_preparation_and_history_failures_are_atomic()
    print("Resolved-thread actor relocation tests passed.")
