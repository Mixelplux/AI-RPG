import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import engine.game_engine as game_engine_module
from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import build_save_data, load_game


REGION_PATH = "data/regions/bryn_shander.json"
TRIGGER = "captain_darvin_grey"
KNOWLEDGE_ID = "player_spoke_with_captain"
EFFECT_ID = "captain_conversation_grants_knowledge"


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
    del absent["conversation_actor_knowledge_effect"]
    validate_region(absent)
    invalid = deepcopy(region)
    invalid["conversation_actor_knowledge_effect"] = []
    expect_invalid(invalid, "must be a dictionary")
    for field in ("effect_id", "trigger_entity_id", "actor_entity_id", "knowledge_id"):
        missing = deepcopy(region)
        del missing["conversation_actor_knowledge_effect"][field]
        expect_invalid(missing, "missing=")
        empty = deepcopy(region)
        empty["conversation_actor_knowledge_effect"][field] = ""
        expect_invalid(empty, "non-empty string")
        non_string = deepcopy(region)
        non_string["conversation_actor_knowledge_effect"][field] = 1
        expect_invalid(non_string, "non-empty string")
    extra = deepcopy(region)
    extra["conversation_actor_knowledge_effect"]["extra"] = True
    expect_invalid(extra, "extra=['extra']")
    for field in ("trigger_entity_id", "actor_entity_id"):
        unknown = deepcopy(region)
        unknown["conversation_actor_knowledge_effect"][field] = "spawned_guard_1"
        expect_invalid(unknown, field)


def test_matching_material_duplicate_and_boundaries():
    engine = GameEngine(REGION_PATH)
    original_region = deepcopy(engine.region)
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
    consequence = result["actor_knowledge_consequence"]
    conversations = engine.query_history(event_type="player_conversation")
    additions = engine.query_history(event_type="actor_knowledge_added")
    assert consequence == {
        "effect_id": EFFECT_ID,
        "changed": True,
        "actor_id": TRIGGER,
        "knowledge_id": KNOWLEDGE_ID,
        "source_history_id": conversations[-1]["history_id"],
        "history_id": additions[-1]["history_id"],
    }
    assert engine.get_actor_knowledge(TRIGGER)[-1] == KNOWLEDGE_ID
    assert additions[-1]["source_history_id"] == conversations[-1]["history_id"]
    assert engine.get_history().index(conversations[-1]) < engine.get_history().index(additions[-1])
    assert result["pressure_consequence"]["changed"]
    assert result["actor_location_consequence"] is None
    assert result["unresolved_thread_consequence"]["changed"]
    assert [entry["event_type"] for entry in engine.get_history()] == [
        "player_conversation",
        "pressure_changed",
        "unresolved_thread_opened",
        "actor_knowledge_added",
        "evidence_trace_added",
    ]
    assert engine.region == original_region
    consequence["actor_id"] = "changed"
    assert engine.get_actor_knowledge(TRIGGER)[-1] == KNOWLEDGE_ID
    assert "actor_knowledge" not in engine.get_scene_snapshot()
    assert "actor_knowledge" not in engine.get_player_perception()
    narration = engine.get_narration_context("look", history_count=20)
    assert all(entry["event_type"] != "actor_knowledge_added" for entry in narration["history_context"]["history_entries"])

    repeated = engine.process_command("talk to captain")
    assert repeated["actor_knowledge_consequence"] == consequence | {
        "actor_id": TRIGGER, "changed": False, "history_id": None,
        "source_history_id": engine.query_history(event_type="player_conversation")[-1]["history_id"],
    }
    assert len(engine.query_history(event_type="player_conversation")) == 2
    assert len(engine.query_history(event_type="actor_knowledge_added")) == 1
    assert engine.get_actor_knowledge(TRIGGER).count(KNOWLEDGE_ID) == 1
    assert engine.process_command("talk to elin").get("actor_knowledge_consequence") is None


def test_atomic_failure_and_save_load():
    for target, error in (("validate_world_state", ValueError("state")),
                          ("build_scene", RuntimeError("scene"))):
        engine = GameEngine(REGION_PATH)
        before_state = engine.get_world_state()
        before_scene = engine.scene_snapshot
        with patch.object(game_engine_module, target, side_effect=error):
            try:
                engine.process_command("talk to captain")
            except type(error):
                pass
            else:
                raise AssertionError("Injected failure was swallowed.")
        assert engine.get_world_state() == before_state
        assert engine.scene_snapshot is before_scene

    engine = GameEngine(REGION_PATH)
    engine.process_command("talk to captain")
    history = engine.get_history()
    with TemporaryDirectory() as directory:
        path = Path(directory) / "conversation-knowledge.json"
        path.write_text(json.dumps(build_save_data(engine)), encoding="utf-8")
        loaded = load_game(str(path))
        assert loaded.get_actor_knowledge(TRIGGER)[-1] == KNOWLEDGE_ID
        addition = loaded.query_history(event_type="actor_knowledge_added")[-1]
        assert loaded.get_history_entry_by_id(addition["source_history_id"])["event_type"] == "player_conversation"
        repeated = loaded.process_command("talk to captain")
        assert not repeated["actor_knowledge_consequence"]["changed"]
        malformed = build_save_data(engine)
        malformed["world_state"]["history"][-1]["source_history_id"] = "history_999999"
        malformed_path = Path(directory) / "malformed.json"
        malformed_path.write_text(json.dumps(malformed), encoding="utf-8")
        before_state = engine.get_world_state()
        before_scene = engine.scene_snapshot
        try:
            engine.load(str(malformed_path))
        except ValueError:
            pass
        else:
            raise AssertionError("Expected malformed load to fail.")
        assert engine.get_world_state() == before_state
        assert engine.scene_snapshot is before_scene
    assert history == engine.get_history()


def main():
    test_declaration_validation()
    test_matching_material_duplicate_and_boundaries()
    test_atomic_failure_and_save_load()
    print("Conversation actor knowledge tests passed.")


if __name__ == "__main__":
    main()
