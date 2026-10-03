import json
from copy import deepcopy
from pathlib import Path
from test_artifact_files import artifact_files
from unittest.mock import patch

import engine.game_engine as game_engine_module
from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import build_save_data, load_game


REGION = "test_fixtures/bryn_shander_legacy.json"
DISCOVERY = "north_gate_second_hour_trace"
TITLE = "The Delayed Watch Mark"
CAPTAIN = "captain_darvin_grey"
NORTH = "bryn_shander_gate_north"
WEST = "bryn_shander_gate_west"
RESPONSE = (
    'Captain Grey studies the delayed watch mark, then straightens. '
    '"I am returning to the North Gate to address this lapse at once."'
)


def data():
    return json.loads(Path(REGION).read_text(encoding="utf-8"))


def rejected(region, fragment):
    try:
        validate_region(region)
    except ValueError as error:
        assert fragment in str(error), str(error)
        return
    raise AssertionError("Expected Region Pack validation failure.")


def reach_captain_with_mark(engine):
    assert engine.process_command("wait")["success"]
    assert engine.process_command("wait")["success"]
    assert engine.get_evidence_trace("north_gate_second_hour_trace") is not None
    assert engine.process_command("investigate")["investigation"]["discovery_id"] == DISCOVERY
    assert engine.process_command("go to Southwest Gate")["success"]
    assert engine.resolve_target("captain")["identifier"] == CAPTAIN


def test_strict_declaration_validation_and_pair_non_overlap():
    region = data()
    validate_region(region)
    absent = deepcopy(region)
    del absent["conversation_discovery_actor_relocation"]
    validate_region(absent)
    for field in (
        "effect_id", "target_entity_id", "required_discovery_id",
        "actor_entity_id", "destination_location_id", "response_text",
    ):
        bad = deepcopy(region)
        del bad["conversation_discovery_actor_relocation"][field]
        rejected(bad, "fields are invalid")
        bad = deepcopy(region)
        bad["conversation_discovery_actor_relocation"][field] = ""
        rejected(bad, "non-empty strings")
    bad = deepcopy(region)
    bad["conversation_discovery_actor_relocation"]["extra"] = True
    rejected(bad, "fields are invalid")
    for field, value, error in (
        ("target_entity_id", "missing", "static actor"),
        ("actor_entity_id", "guard_elin_voss", "must be Captain Grey"),
        ("required_discovery_id", "missing", "unknown"),
        ("required_discovery_id", "west_gate_elin_report_trace", "delayed-watch trace"),
        ("destination_location_id", "missing", "unknown"),
        ("destination_location_id", WEST, "must be the North Gate"),
    ):
        bad = deepcopy(region)
        bad["conversation_discovery_actor_relocation"][field] = value
        rejected(bad, error)
    bad = deepcopy(region)
    bad["conversation_discovery_actor_relocation"]["effect_id"] = (
        region["elapsed_time_actor_relocation_effect"]["effect_id"]
    )
    rejected(bad, "conflicts")
    bad = deepcopy(region)
    bad["conversation_discovery_resolution"]["required_discovery_id"] = DISCOVERY
    rejected(bad, "must not overlap")


def test_end_to_end_atomic_recall_and_path_separation():
    engine = GameEngine(REGION)
    reach_captain_with_mark(engine)
    original_validate = game_engine_module.validate_world_state
    original_build = game_engine_module.build_scene
    calls = {"validate": 0, "build": 0}
    with patch.object(game_engine_module, "validate_world_state", side_effect=lambda *a, **k: (calls.__setitem__("validate", calls["validate"] + 1), original_validate(*a, **k))[1]), patch.object(game_engine_module, "build_scene", side_effect=lambda *a, **k: (calls.__setitem__("build", calls["build"] + 1), original_build(*a, **k))[1]):
        presentation = engine.process_command("present The Delayed Watch Mark to captain")["presentation"]
    assert calls == {"validate": 1, "build": 1}
    assert presentation == {
        "changed": True, "response_text": RESPONSE, "resolved_observation": None,
        "actor_location_consequence": {"status": "applied"},
        "actor_knowledge_consequence": None, "evidence_trace_consequence": None,
    }
    history = engine.get_history()
    source = history[-2]
    moved = history[-1]
    assert source["event_type"] == "clue_presented"
    assert moved["event_type"] == "actor_moved"
    assert moved["source_history_id"] == source["history_id"]
    assert engine.resolve_target("captain")["status"] != "resolved"
    assert engine.process_command("go to North Gate")["success"]
    assert engine.resolve_target("captain")["identifier"] == CAPTAIN
    for packet in (
        engine.get_scene_snapshot(), engine.get_player_perception(),
        engine.get_narration_context("look"), engine.get_narration_preview("look"),
    ):
        assert DISCOVERY not in repr(packet)
    west_road = GameEngine(REGION)
    assert west_road.process_command("talk to captain")["success"]
    assert west_road.process_command("investigate")["investigation"]["changed"]
    result = west_road.process_command("present The Captain's Deliberate Trail to captain")["presentation"]
    assert result["changed"] and result["actor_knowledge_consequence"] == {"status": "applied"}
    assert result["evidence_trace_consequence"] == {"status": "applied"}


def test_ineligible_noop_rollback_and_save_load():
    engine = GameEngine(REGION)
    assert not engine.present_clue(TITLE, "captain")["changed"]
    reach_captain_with_mark(engine)
    assert not engine.present_clue("The Captain's Deliberate Trail", "captain")["changed"]
    engine.region.pop("conversation_discovery_actor_relocation")
    assert not engine.present_clue(TITLE, "captain")["changed"]
    engine = GameEngine(REGION)
    reach_captain_with_mark(engine)
    before_state, live_state, before_scene = engine.get_world_state(), engine.world_state, engine.scene_snapshot
    for target in ("_prepare_actor_location_candidate", "validate_world_state", "build_scene"):
        owner = game_engine_module.GameEngine if target.startswith("_") else game_engine_module
        with patch.object(owner, target, side_effect=RuntimeError(target)):
            try:
                engine.present_clue(TITLE, "captain")
            except RuntimeError:
                pass
            else:
                raise AssertionError("Expected injected failure.")
        assert engine.get_world_state() == before_state and engine.world_state is live_state
        assert engine.scene_snapshot is before_scene
    assert engine.present_clue(TITLE, "captain")["actor_location_consequence"] == {"status": "applied"}
    assert engine.process_command("go to North Gate")["success"]
    moved_count = len(engine.query_history(event_type="actor_moved"))
    assert engine.present_clue(TITLE, "captain")["actor_location_consequence"] == {"status": "no_op"}
    assert len(engine.query_history(event_type="actor_moved")) == moved_count
    with artifact_files("test_delayed_watch_discovery_actor_recall") as directory:
        path = Path(directory) / "test_delayed_watch_discovery_actor_recall_save.json"
        path.write_text(json.dumps(build_save_data(engine)), encoding="utf-8")
        loaded = load_game(str(path))
        assert loaded.resolve_target("captain")["identifier"] == CAPTAIN
        assert loaded.present_clue(TITLE, "captain")["actor_location_consequence"] == {"status": "no_op"}


def test_selective_history_rollback_and_direct_target_ineligibility():
    for failed_event in ("clue_presented", "actor_moved"):
        engine = GameEngine(REGION)
        reach_captain_with_mark(engine)
        before_state, live_state, before_scene = (
            engine.get_world_state(), engine.world_state, engine.scene_snapshot
        )
        before_history = engine.get_history()
        original_add = game_engine_module.add_history_entry

        def fail_selected(candidate, event_type, *args, **kwargs):
            if event_type == failed_event:
                raise RuntimeError(failed_event)
            return original_add(candidate, event_type, *args, **kwargs)

        with patch.object(game_engine_module, "add_history_entry", side_effect=fail_selected):
            try:
                engine.present_clue(TITLE, "captain")
            except RuntimeError as error:
                assert str(error) == failed_event
            else:
                raise AssertionError("Expected selective history failure.")
        assert engine.get_world_state() == before_state and engine.world_state is live_state
        assert engine.scene_snapshot == before_scene and engine.scene_snapshot is before_scene
        assert engine.resolve_target("captain")["identifier"] == CAPTAIN
        assert engine.get_history() == before_history

    engine = GameEngine(REGION)
    assert engine.process_command("wait")["success"]
    assert engine.process_command("wait")["success"]
    assert engine.process_command("investigate")["investigation"]["discovery_id"] == DISCOVERY
    before_state, before_scene = engine.get_world_state(), engine.scene_snapshot
    before_history = engine.get_history()
    assert not engine.present_clue(TITLE, "elin")["changed"]
    assert engine.get_world_state() == before_state and engine.scene_snapshot is before_scene
    assert not engine.present_clue(TITLE, "captain")["changed"]
    assert engine.get_world_state() == before_state and engine.scene_snapshot is before_scene
    assert engine.get_history() == before_history


def test_exact_noop_counts_and_pre_presentation_save_load_path():
    engine = GameEngine(REGION)
    reach_captain_with_mark(engine)
    assert engine.present_clue(TITLE, "captain")["actor_location_consequence"] == {"status": "applied"}
    assert engine.process_command("go to North Gate")["success"]
    source_count = len(engine.query_history(event_type="clue_presented"))
    moved_count = len(engine.query_history(event_type="actor_moved"))
    original_validate, original_build = game_engine_module.validate_world_state, game_engine_module.build_scene
    calls = {"validate": 0, "build": 0}
    with patch.object(game_engine_module, "validate_world_state", side_effect=lambda *a, **k: (calls.__setitem__("validate", calls["validate"] + 1), original_validate(*a, **k))[1]), patch.object(game_engine_module, "build_scene", side_effect=lambda *a, **k: (calls.__setitem__("build", calls["build"] + 1), original_build(*a, **k))[1]):
        result = engine.present_clue(TITLE, "captain")
    assert result["changed"] and result["response_text"] == RESPONSE
    assert result["actor_location_consequence"] == {"status": "no_op"}
    assert calls == {"validate": 1, "build": 1}
    assert len(engine.query_history(event_type="clue_presented")) == source_count + 1
    assert len(engine.query_history(event_type="actor_moved")) == moved_count
    assert "fired" not in repr(engine.get_world_state())
    assert engine.resolve_target("captain")["identifier"] == CAPTAIN

    with artifact_files("test_delayed_watch_discovery_actor_recall") as directory:
        path = Path(directory) / "test_delayed_watch_discovery_actor_recall_before-presentation.json"
        saved = GameEngine(REGION)
        assert saved.process_command("wait")["success"]
        assert saved.process_command("wait")["success"]
        assert saved.process_command("investigate")["investigation"]["discovery_id"] == DISCOVERY
        saved.save(str(path))
        loaded = load_game(str(path))
        assert DISCOVERY in loaded.get_player_discoveries()
        assert loaded.resolve_target("captain")["status"] != "resolved"
        assert loaded.process_command("go to Southwest Gate")["success"]
        result = loaded.present_clue(TITLE, "captain")
        assert result["response_text"] == RESPONSE
        source, moved = loaded.get_history()[-2:]
        assert source["event_type"] == "clue_presented"
        assert moved["event_type"] == "actor_moved"
        assert moved["source_history_id"] == source["history_id"]
        loaded.save(str(path))
        reloaded = load_game(str(path))
        assert reloaded.process_command("go to North Gate")["success"]
        moved_count = len(reloaded.query_history(event_type="actor_moved"))
        assert reloaded.present_clue(TITLE, "captain")["actor_location_consequence"] == {"status": "no_op"}
        assert len(reloaded.query_history(event_type="actor_moved")) == moved_count


def main():
    test_strict_declaration_validation_and_pair_non_overlap()
    test_end_to_end_atomic_recall_and_path_separation()
    test_ineligible_noop_rollback_and_save_load()
    test_selective_history_rollback_and_direct_target_ineligibility()
    test_exact_noop_counts_and_pre_presentation_save_load_path()
    print("Delayed-watch discovery actor recall tests passed.")


if __name__ == "__main__":
    main()
