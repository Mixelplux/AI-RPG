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
THREAD_ID = "bryn_shander_west_road_bandit_report"
ACTOR_ID = "captain_darvin_grey"
KNOWLEDGE_ID = "west_road_report_completed"
TEXT = 'Captain Grey gives a firm nod. "The report is settled. The west-road patrol has its orders."'


def region_data():
    return json.loads(Path(REGION_PATH).read_text(encoding="utf-8"))


def invalid(region, text):
    try:
        validate_region(region)
    except ValueError as error:
        assert text in str(error), str(error)
        return
    raise AssertionError("Expected invalid Region Pack.")


def resolve(engine):
    assert engine.process_command("talk to captain")["success"]
    assert engine.process_command("investigate")["investigation"]["changed"]
    result = engine.process_command("present The Captain's Deliberate Trail to captain")["presentation"]
    assert result["changed"]
    return result


def test_declaration_validation():
    region = region_data(); validate_region(region)
    absent = deepcopy(region); del absent["resolved_thread_actor_knowledge_effect"]; validate_region(absent)
    for field in ("effect_id", "resolved_thread_id", "actor_entity_id", "knowledge_id"):
        bad = deepcopy(region); del bad["resolved_thread_actor_knowledge_effect"][field]; invalid(bad, "fields are invalid")
        bad = deepcopy(region); bad["resolved_thread_actor_knowledge_effect"][field] = ""; invalid(bad, "non-empty strings")
    bad = deepcopy(region); bad["resolved_thread_actor_knowledge_effect"]["extra"] = True; invalid(bad, "fields are invalid")
    bad = deepcopy(region); bad["resolved_thread_actor_knowledge_effect"]["resolved_thread_id"] = "missing"; invalid(bad, "unknown")
    bad = deepcopy(region); bad["resolved_thread_actor_knowledge_effect"]["actor_entity_id"] = "guard_elin_voss"; invalid(bad, "Captain Grey")
    bad = deepcopy(region); bad["resolved_thread_actor_knowledge_effect"]["effect_id"] = region["resolved_thread_actor_relocation_effect"]["effect_id"]; invalid(bad, "conflicts")
    bad = deepcopy(region); bad["conversation_actor_knowledge_response"]["target_entity_id"] = "guard_elin_voss"; invalid(bad, "must match resolved-thread")
    bad = deepcopy(region); bad["conversation_actor_knowledge_response"]["required_knowledge_id"] = "unrelated"; invalid(bad, "must match resolved-thread")


def test_atomic_resolution_response_noop_and_hidden_state():
    engine = GameEngine(REGION_PATH)
    assert engine.process_command("talk to captain")["actor_knowledge_response"] is None
    before = engine.get_world_state()
    assert engine.process_command("present wrong to captain")["presentation"]["changed"] is False
    assert engine.get_world_state() == before
    result = resolve(engine)
    assert result["actor_location_consequence"] == {"status": "applied"}
    assert result["actor_knowledge_consequence"] == {"status": "applied"}
    assert KNOWLEDGE_ID in engine.get_actor_knowledge(ACTOR_ID)
    source = engine.query_history(event_type="clue_presented")[-1]
    knowledge = engine.query_history(event_type="actor_knowledge_added")[-1]
    moved = engine.query_history(event_type="actor_moved")[-1]
    assert knowledge["source_history_id"] == source["history_id"] == moved["source_history_id"]
    assert engine.get_history().index(moved) < engine.get_history().index(knowledge)
    assert engine.process_command("talk to captain")["actor_knowledge_response"] == {"text": TEXT}
    assert "actor_knowledge" not in engine.get_scene_snapshot()
    assert "actor_knowledge" not in engine.get_player_perception()
    assert TEXT not in str(engine.get_narration_context("look", history_count=20))
    repeat = engine.process_command("present The Captain's Deliberate Trail to captain")["presentation"]
    assert not repeat["changed"]
    assert len([entry for entry in engine.query_history(event_type="actor_knowledge_added")
                if entry["knowledge_id"] == KNOWLEDGE_ID]) == 1


def test_rollback_and_save_load():
    for target in ("_prepare_actor_knowledge_from_event_candidate", "validate_world_state", "build_scene"):
        engine = GameEngine(REGION_PATH); engine.process_command("talk to captain"); engine.process_command("investigate")
        state, scene = engine.get_world_state(), engine.scene_snapshot
        with patch.object(game_engine_module.GameEngine if target.startswith("_") else game_engine_module, target, side_effect=RuntimeError(target)):
            try: engine.process_command("present The Captain's Deliberate Trail to captain")
            except RuntimeError: pass
            else: raise AssertionError("Expected injected failure")
        assert engine.get_world_state() == state and engine.scene_snapshot is scene
    engine = GameEngine(REGION_PATH); engine.process_command("talk to captain")
    with TemporaryDirectory() as directory:
        path = Path(directory) / "before.json"; path.write_text(json.dumps(build_save_data(engine)), encoding="utf-8")
        loaded = load_game(str(path)); resolve(loaded)
        after = Path(directory) / "after.json"; after.write_text(json.dumps(build_save_data(loaded)), encoding="utf-8")
        reloaded = load_game(str(after)); assert KNOWLEDGE_ID in reloaded.get_actor_knowledge(ACTOR_ID)
        assert reloaded.process_command("talk to captain")["actor_knowledge_response"] == {"text": TEXT}


def test_preexisting_knowledge_noop_composition_and_history_failure_rollback():
    engine = GameEngine(REGION_PATH)
    engine.process_command("talk to captain")
    engine.add_actor_knowledge(ACTOR_ID, KNOWLEDGE_ID)
    before_additions = len(engine.query_history(event_type="actor_knowledge_added"))
    engine.process_command("investigate")
    original_validate, original_build = game_engine_module.validate_world_state, game_engine_module.build_scene
    counts = {"validate": 0, "build": 0}
    with patch.object(game_engine_module, "validate_world_state", side_effect=lambda *a, **k: (counts.__setitem__("validate", counts["validate"] + 1), original_validate(*a, **k))[1]), patch.object(game_engine_module, "build_scene", side_effect=lambda *a, **k: (counts.__setitem__("build", counts["build"] + 1), original_build(*a, **k))[1]):
        result = engine.process_command("present The Captain's Deliberate Trail to captain")["presentation"]
    assert result["changed"] and result["actor_location_consequence"] == {"status": "applied"}
    assert result["actor_knowledge_consequence"] == {"status": "no_op"}
    assert engine.get_actor_knowledge(ACTOR_ID).count(KNOWLEDGE_ID) == 1
    assert len(engine.query_history(event_type="actor_knowledge_added")) == before_additions
    assert counts == {"validate": 1, "build": 1}
    assert THREAD_ID in engine.get_world_state()["resolved_threads"]

    engine = GameEngine(REGION_PATH); engine.process_command("talk to captain"); engine.process_command("investigate")
    before_state, live_state, before_scene = engine.get_world_state(), engine.world_state, engine.scene_snapshot
    original_add = game_engine_module.add_history_entry
    def fail_knowledge_history(candidate, event_type, *args, **kwargs):
        if event_type == "actor_knowledge_added": raise RuntimeError("knowledge history")
        return original_add(candidate, event_type, *args, **kwargs)
    with patch.object(game_engine_module, "add_history_entry", side_effect=fail_knowledge_history):
        try: engine.process_command("present The Captain's Deliberate Trail to captain")
        except RuntimeError as error: assert "knowledge history" in str(error)
        else: raise AssertionError("Expected knowledge-history failure")
    assert engine.get_world_state() == before_state and engine.world_state is live_state
    assert engine.scene_snapshot is before_scene
    assert THREAD_ID not in engine.get_world_state()["resolved_threads"]
    assert KNOWLEDGE_ID not in engine.get_actor_knowledge(ACTOR_ID)


def main():
    test_declaration_validation(); test_atomic_resolution_response_noop_and_hidden_state(); test_rollback_and_save_load(); test_preexisting_knowledge_noop_composition_and_history_failure_rollback()
    print("Resolved-thread actor-knowledge acknowledgment tests passed.")


if __name__ == "__main__": main()
