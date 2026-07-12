from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import build_save_data, load_game


REGION_PATH = "data/regions/bryn_shander.json"
THREAD_ID = "bryn_shander_west_road_bandit_report"
EVIDENCE = {
    "text": (
        "Watch patrols at the North Gate speak in low voices about the "
        "unanswered bandit report on the western road."
    )
}


def expect_value_error(callable_) -> None:
    try:
        callable_()
    except ValueError:
        return
    raise AssertionError("Expected ValueError.")


def test_declaration_and_state_validation() -> None:
    engine = GameEngine(REGION_PATH)
    declaration = engine.region["conversation_unresolved_thread"]
    for field, value in (("thread_id", ""), ("description", ""),
                         ("trigger_entity_id", "missing"), ("evidence_text", "")):
        invalid = deepcopy(engine.region)
        invalid["conversation_unresolved_thread"][field] = value
        expect_value_error(lambda invalid=invalid: validate_region(invalid))
    invalid = deepcopy(engine.region)
    invalid["conversation_unresolved_thread"]["perception_location_ids"] = []
    expect_value_error(lambda: validate_region(invalid))
    invalid = deepcopy(engine.region)
    invalid["conversation_unresolved_thread"]["perception_location_ids"] = [
        "bryn_shander_gate_north", "bryn_shander_gate_north"
    ]
    expect_value_error(lambda: validate_region(invalid))
    assert declaration["thread_id"] == THREAD_ID


def test_atomic_creation_duplicate_prevention_and_perception() -> None:
    engine = GameEngine(REGION_PATH)
    assert engine.get_open_threads() == {}
    assert engine.get_player_perception()["unresolved_thread_evidence"] == []

    result = engine.process_command("talk to captain")
    consequence = result["unresolved_thread_consequence"]
    assert consequence["changed"] is True
    assert consequence["thread_id"] == THREAD_ID
    source = engine.get_history_entry_by_id(consequence["source_history_id"])
    assert source["event_type"] == "player_conversation"
    opened = engine.get_history_entry_by_id(consequence["history_id"])
    assert opened["event_type"] == "unresolved_thread_opened"
    assert opened["source_history_id"] == source["history_id"]
    assert engine.get_open_threads() == {
        THREAD_ID: {
            "thread_id": THREAD_ID,
            "status": "open",
            "created_by_history_id": source["history_id"],
        }
    }
    assert engine.get_player_perception()["unresolved_thread_evidence"] == [EVIDENCE]

    engine.process_command("go south")
    assert engine.get_player_perception()["unresolved_thread_evidence"] == []
    engine.process_command("go north")
    assert engine.get_player_perception()["unresolved_thread_evidence"] == [EVIDENCE]
    repeat = engine.process_command("talk to captain")["unresolved_thread_consequence"]
    assert repeat["changed"] is False
    assert repeat["history_id"] is None
    assert len(engine.query_history(event_type="unresolved_thread_opened")) == 1

    perception = engine.get_player_perception()
    perception["unresolved_thread_evidence"][0]["text"] = "changed"
    assert engine.get_player_perception()["unresolved_thread_evidence"] == [EVIDENCE]


def test_save_load_legacy_and_atomic_failure() -> None:
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_scene = engine.get_scene_snapshot()
    with patch("engine.game_engine.prepare_open_thread_candidate", side_effect=RuntimeError("thread")):
        try:
            engine.process_command("talk to captain")
        except RuntimeError:
            pass
        else:
            raise AssertionError("Injected thread failure was swallowed.")
    assert engine.get_world_state() == before_state
    assert engine.get_scene_snapshot() == before_scene

    engine.process_command("talk to captain")
    with TemporaryDirectory() as temporary_directory:
        path = Path(temporary_directory) / "thread.json"
        engine.save(str(path))
        loaded = load_game(str(path))
        assert loaded.get_open_threads() == engine.get_open_threads()
        assert loaded.get_player_perception()["unresolved_thread_evidence"] == [EVIDENCE]

        legacy = build_save_data(GameEngine(REGION_PATH))
        del legacy["world_state"]["open_threads"]
        legacy_path = Path(temporary_directory) / "legacy.json"
        import json
        legacy_path.write_text(json.dumps(legacy), encoding="utf-8")
        legacy_loaded = load_game(str(legacy_path))
        assert legacy_loaded.get_open_threads() == {}

        malformed = build_save_data(engine)
        malformed["world_state"]["open_threads"][THREAD_ID]["status"] = "closed"
        malformed_path = Path(temporary_directory) / "malformed.json"
        malformed_path.write_text(__import__("json").dumps(malformed), encoding="utf-8")
        expect_value_error(lambda: load_game(str(malformed_path)))


def test_causal_integrity_narration_isolation_and_live_load_atomicity() -> None:
    engine = GameEngine(REGION_PATH)
    engine.process_command("talk to captain")
    assert engine.query_history(event_type="unresolved_thread_opened")
    assert all(entry["event_type"] != "unresolved_thread_opened" for entry in engine.get_narration_context("look", history_count=10)["history_context"]["history_entries"])
    with TemporaryDirectory() as temporary_directory:
        valid = build_save_data(engine)
        for label, mutate in (
            ("phantom", lambda p: p["world_state"]["open_threads"].__setitem__("phantom", {"thread_id":"phantom","status":"open","created_by_history_id":"history_000001"})),
            ("mismatch", lambda p: p["world_state"]["open_threads"][THREAD_ID].__setitem__("thread_id", "other")),
            ("wrong_source", lambda p: p["world_state"]["open_threads"][THREAD_ID].__setitem__("created_by_history_id", "history_000002")),
            ("missing_open", lambda p: p["world_state"].__setitem__("history", [e for e in p["world_state"]["history"] if e["event_type"] != "unresolved_thread_opened"])),
            ("duplicate_open", lambda p: p["world_state"]["history"].append(deepcopy(p["world_state"]["history"][-1]) | {"history_id":"history_999999"})),
        ):
            payload = deepcopy(valid); mutate(payload)
            path = Path(temporary_directory) / f"{label}.json"
            import json; path.write_text(json.dumps(payload), encoding="utf-8")
            expect_value_error(lambda path=path: load_game(str(path)))
        bad = deepcopy(valid); bad["world_state"]["open_threads"][THREAD_ID]["created_by_history_id"] = "history_000002"
        path = Path(temporary_directory) / "bad_live.json"; import json; path.write_text(json.dumps(bad), encoding="utf-8")
        before_state, before_scene = engine.get_world_state(), engine.get_scene_snapshot()
        expect_value_error(lambda: engine.load(str(path)))
        assert engine.get_world_state() == before_state and engine.get_scene_snapshot() == before_scene


def main() -> None:
    test_declaration_and_state_validation()
    test_atomic_creation_duplicate_prevention_and_perception()
    test_save_load_legacy_and_atomic_failure()
    test_causal_integrity_narration_isolation_and_live_load_atomicity()
    print("Unresolved thread tests passed.")


if __name__ == "__main__":
    main()
