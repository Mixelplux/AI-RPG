import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import engine.game_engine as game_engine_module
from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import load_game, save_game


REGION_PATH = "data/regions/bryn_shander.json"
TRIGGER = "captain_darvin_grey"
ACTOR = "guard_elin_voss"
BASELINE = "bryn_shander_gate_north"
DESTINATION = "bryn_shander_main_street"
EFFECT_ID = "captain_conversation_moves_elin"


def region_data():
    return json.loads(Path(REGION_PATH).read_text(encoding="utf-8"))


def expect_invalid(region, text):
    try:
        validate_region(region)
    except ValueError as error:
        assert text in str(error), str(error)
        return
    raise AssertionError("Expected invalid Region Pack.")


def test_declaration_validation():
    region = region_data()
    validate_region(region)
    absent = deepcopy(region)
    del absent["conversation_actor_relocation_effect"]
    validate_region(absent)
    invalid = deepcopy(region)
    invalid["conversation_actor_relocation_effect"] = []
    expect_invalid(invalid, "must be a dictionary")
    for field in ("effect_id", "trigger_entity_id", "actor_entity_id",
                  "destination_location_id"):
        missing = deepcopy(region)
        del missing["conversation_actor_relocation_effect"][field]
        expect_invalid(missing, "missing=")
        empty = deepcopy(region)
        empty["conversation_actor_relocation_effect"][field] = ""
        expect_invalid(empty, "non-empty string")
    extra = deepcopy(region)
    extra["conversation_actor_relocation_effect"]["extra"] = True
    expect_invalid(extra, "extra=['extra']")
    for field, text in (("trigger_entity_id", "trigger_entity_id"),
                        ("actor_entity_id", "actor_entity_id"),
                        ("destination_location_id", "destination_location_id")):
        unknown = deepcopy(region)
        unknown["conversation_actor_relocation_effect"][field] = "missing"
        expect_invalid(unknown, text)


def test_material_and_repeat():
    engine = GameEngine(REGION_PATH)
    original_validate = game_engine_module.validate_world_state
    original_build = game_engine_module.build_scene
    counts = {"validate": 0, "build": 0}

    def counted_validate(*args, **kwargs):
        counts["validate"] += 1
        return original_validate(*args, **kwargs)

    def counted_build(*args, **kwargs):
        counts["build"] += 1
        return original_build(*args, **kwargs)

    with patch.object(game_engine_module, "validate_world_state", counted_validate), patch.object(
        game_engine_module, "build_scene", counted_build
    ):
        result = engine.process_command("talk to captain")

    assert counts == {"validate": 1, "build": 1}
    consequence = result["actor_location_consequence"]
    assert consequence == {
        "effect_id": EFFECT_ID,
        "trigger_entity_id": TRIGGER,
        "actor_entity_id": ACTOR,
        "previous_location_id": BASELINE,
        "new_location_id": DESTINATION,
        "changed": True,
        "history_id": engine.get_history()[-1]["history_id"],
    }
    conversations = engine.query_history(event_type="player_conversation")
    moves = engine.query_history(event_type="actor_moved")
    assert len(conversations) == len(moves) == 1
    assert moves[0]["source_history_id"] == conversations[0]["history_id"]
    assert engine.get_world_state()["actor_location_overrides"] == {
        ACTOR: DESTINATION
    }
    assert ACTOR not in engine.get_scene_snapshot()["entities"]["static"]
    assert engine.resolve_target("elin")["status"] == "unresolved"
    assert ACTOR not in engine.get_player_perception()["visible"]["entities"]["static"]

    durable = engine.get_world_state()
    consequence["actor_entity_id"] = "changed"
    result["target_resolution"]["identifier"] = "changed"
    assert engine.get_world_state() == durable

    repeated = engine.process_command("talk to captain")
    assert repeated["actor_location_consequence"]["changed"] is False
    assert repeated["actor_location_consequence"]["history_id"] is None
    assert len(engine.query_history(event_type="player_conversation")) == 2
    assert len(engine.query_history(event_type="actor_moved")) == 1
    assert engine.get_world_state()["actor_location_overrides"] == {
        ACTOR: DESTINATION
    }

    other = engine.process_command("talk to captain")
    assert other["actor_location_consequence"]["changed"] is False
    failed = engine.process_command("talk to elin")
    assert not failed["success"]
    look = engine.process_command("look around")
    assert "actor_location_consequence" not in look


def test_failure_atomicity_and_baseline_removal():
    for target, error in (("validate_world_state", ValueError("state")),
                          ("build_scene", RuntimeError("scene"))):
        engine = GameEngine(REGION_PATH)
        state = engine.get_world_state()
        scene_identity = id(engine.scene_snapshot)
        with patch.object(game_engine_module, target, side_effect=error):
            try:
                engine.process_command("talk to captain")
            except type(error):
                pass
            else:
                raise AssertionError("Injected failure was swallowed.")
        assert engine.get_world_state() == state
        assert id(engine.scene_snapshot) == scene_identity

    engine = GameEngine(REGION_PATH)
    engine.set_actor_location(ACTOR, DESTINATION)
    engine.region["conversation_actor_relocation_effect"][
        "destination_location_id"
    ] = BASELINE
    result = engine.process_command("talk to captain")
    assert result["actor_location_consequence"]["changed"]
    assert engine.get_world_state()["actor_location_overrides"] == {}


def test_save_load():
    engine = GameEngine(REGION_PATH)
    engine.process_command("talk to captain")
    history = engine.get_history()
    with TemporaryDirectory() as temp_dir:
        path = str(Path(temp_dir) / "actor-relocation.json")
        save_game(engine, path)
        loaded = load_game(path)
    assert loaded.get_history() == history
    assert loaded.get_world_state()["actor_location_overrides"] == {
        ACTOR: DESTINATION
    }
    repeated = loaded.process_command("talk to captain")
    assert repeated["actor_location_consequence"]["changed"] is False
    assert len(loaded.query_history(event_type="actor_moved")) == 1


def main():
    test_declaration_validation()
    test_material_and_repeat()
    test_failure_atomicity_and_baseline_removal()
    test_save_load()
    print("Conversation actor relocation tests passed.")


if __name__ == "__main__":
    main()
