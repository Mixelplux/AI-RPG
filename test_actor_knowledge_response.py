import json
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import engine.game_engine as game_engine_module
from engine.actor_knowledge_response import derive_conversation_actor_knowledge_response
from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import build_save_data, load_game
import play_game


REGION_PATH = "data/regions/bryn_shander.json"
ACTOR_ID = "captain_darvin_grey"
KNOWLEDGE_ID = "west_road_report_completed"
RESPONSE_TEXT = (
    'Captain Grey gives a firm nod. "The report is settled. The west-road patrol has its orders."'
)


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
    del absent["conversation_actor_knowledge_response"]
    validate_region(absent)
    for malformed in ([], "response"):
        invalid = deepcopy(region)
        invalid["conversation_actor_knowledge_response"] = malformed
        expect_invalid(invalid, "fields are invalid")
    for field in ("response_id", "target_entity_id", "required_knowledge_id", "response_text"):
        missing = deepcopy(region)
        del missing["conversation_actor_knowledge_response"][field]
        expect_invalid(missing, "fields are invalid")
        for value in ("", 1):
            invalid = deepcopy(region)
            invalid["conversation_actor_knowledge_response"][field] = value
            expect_invalid(invalid, "non-empty strings")
    extra = deepcopy(region)
    extra["conversation_actor_knowledge_response"]["extra"] = True
    expect_invalid(extra, "fields are invalid")
    unknown = deepcopy(region)
    unknown["conversation_actor_knowledge_response"]["target_entity_id"] = "spawned_guard_1"
    expect_invalid(unknown, "must reference a static actor")


def test_derivation_copy_safety():
    region = region_data()
    original = deepcopy(region)
    result = derive_conversation_actor_knowledge_response(region, ACTOR_ID, (KNOWLEDGE_ID,))
    assert result == {"text": RESPONSE_TEXT}
    result["text"] = "changed"
    assert region == original
    assert derive_conversation_actor_knowledge_response(region, "guard_elin_voss", (KNOWLEDGE_ID,)) is None
    assert derive_conversation_actor_knowledge_response(region, ACTOR_ID, ()) is None


def test_command_start_ordering_repetition_and_isolation():
    engine = GameEngine(REGION_PATH)
    first = engine.process_command("talk to captain")
    assert first["success"]
    assert first["actor_knowledge_response"] is None
    assert KNOWLEDGE_ID not in engine.get_actor_knowledge(ACTOR_ID)
    investigation = engine.process_command("investigate")
    assert investigation["investigation"]["changed"]
    presented = engine.process_command("present The Captain's Deliberate Trail to captain")
    assert presented["presentation"]["changed"]
    assert KNOWLEDGE_ID in engine.get_actor_knowledge(ACTOR_ID)

    second = engine.process_command("talk to captain")
    assert second["actor_knowledge_response"] == {"text": RESPONSE_TEXT}
    third = engine.process_command("talk to captain")
    assert third["actor_knowledge_response"] == {"text": RESPONSE_TEXT}
    assert len(engine.query_history(event_type="player_conversation")) == 3
    assert "actor_knowledge_response" not in engine.get_world_state()
    assert "actor_knowledge" not in engine.get_scene_snapshot()
    assert "actor_knowledge" not in engine.get_player_perception()
    narration = engine.get_narration_context("look", history_count=20)
    assert RESPONSE_TEXT not in str(narration)

    other_actor = engine.process_command("talk to elin")
    assert other_actor["actor_knowledge_response"] is None
    engine.set_actor_location(ACTOR_ID, "bryn_shander_main_street")
    absent_actor = engine.process_command("talk to captain")
    assert not absent_actor["success"]
    assert absent_actor["actor_knowledge_response"] is None


def test_failure_isolation_and_save_load():
    engine = GameEngine(REGION_PATH)
    engine.process_command("talk to captain")
    engine.process_command("investigate")
    engine.process_command("present The Captain's Deliberate Trail to captain")
    before_state = engine.get_world_state()
    before_scene = engine.scene_snapshot
    with patch.object(game_engine_module, "build_scene", side_effect=RuntimeError("scene")):
        try:
            engine.process_command("talk to captain")
        except RuntimeError:
            pass
        else:
            raise AssertionError("Injected failure was swallowed.")
    assert engine.get_world_state() == before_state
    assert engine.scene_snapshot is before_scene

    with TemporaryDirectory() as directory:
        path = Path(directory) / "response-save.json"
        save_data = build_save_data(engine)
        assert "actor_knowledge_response" not in json.dumps(save_data)
        path.write_text(json.dumps(save_data), encoding="utf-8")
        loaded = load_game(str(path))
        assert loaded.process_command("talk to captain")["actor_knowledge_response"] == {
            "text": RESPONSE_TEXT
        }


def test_gameplay_output():
    output = StringIO()
    with patch("builtins.input", side_effect=["talk to captain", "investigate", "present The Captain's Deliberate Trail to captain", "talk to captain", "quit"]), redirect_stdout(output):
        play_game.main()
    assert output.getvalue().count(RESPONSE_TEXT) == 1


def main():
    test_declaration_validation()
    test_derivation_copy_safety()
    test_command_start_ordering_repetition_and_isolation()
    test_failure_isolation_and_save_load()
    test_gameplay_output()
    print("Actor knowledge response tests passed.")


if __name__ == "__main__":
    main()
