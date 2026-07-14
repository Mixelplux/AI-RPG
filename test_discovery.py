import json
from copy import deepcopy
from pathlib import Path

from engine.region_validator import validate_region
from engine.game_engine import GameEngine
from engine.save_system import build_save_data, load_game
from tempfile import TemporaryDirectory
from unittest.mock import patch


THREAD_ID = "bryn_shander_west_road_bandit_report"


def expect_value_error(callable_) -> None:
    try:
        callable_()
    except ValueError:
        return
    raise AssertionError("Expected ValueError.")


def build_resolved_engine() -> GameEngine:
    engine = GameEngine("data/regions/bryn_shander.json")
    engine.process_command("talk to captain")
    engine.process_command("investigate")
    assert engine.process_command("present The Captain's Deliberate Trail to captain")["presentation"]["changed"]
    return engine


def test_discovery_declarations() -> None:
    region = json.loads(Path("data/regions/bryn_shander.json").read_text(encoding="utf-8"))
    validate_region(region)
    declaration = region["discovery_declarations"][0]
    assert declaration["text"].startswith("Fresh boot prints")
    for mutation in (
        lambda value: value.__setitem__("discovery_id", ""),
        lambda value: value.__setitem__("location_id", "missing"),
        lambda value: value.__setitem__("extra", "bad"),
    ):
        invalid = deepcopy(region)
        mutation(invalid["discovery_declarations"][0])
        try:
            validate_region(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("Expected invalid declaration.")


def test_atomic_local_discovery_and_no_op() -> None:
    engine = GameEngine("data/regions/bryn_shander.json")
    assert engine.process_command("investigate")["investigation"]["changed"] is False
    engine.process_command("talk to captain")
    result = engine.process_command("investigate")["investigation"]
    assert result["changed"] and result["text"].startswith("Fresh boot prints")
    assert engine.get_player_discoveries() == ("north_gate_captain_trace",)
    assert engine.get_known_clues() == (({
        "title": "The Captain's Deliberate Trail",
        "text": result["text"],
    }),)
    recalled = engine.process_command("clues")
    assert recalled["known_clues"] == list(engine.get_known_clues())
    assert "north_gate_captain_trace" not in str(recalled["known_clues"])
    assert engine.process_command("investigate")["investigation"]["changed"] is False


def test_wrong_location_and_unknown_save_membership_fail_closed() -> None:
    engine = GameEngine("data/regions/bryn_shander.json")
    engine.create_evidence_trace(
        "captain_conversation_gate_trace",
        "captain_conversation_trace",
        "bryn_shander_main_street",
    )
    before_state, before_scene = engine.get_world_state(), engine.get_scene_snapshot()
    assert engine.investigate()["changed"] is False
    assert engine.process_command("known clues")["known_clues"] == []
    assert engine.get_world_state() == before_state
    assert engine.get_scene_snapshot() == before_scene
    with TemporaryDirectory() as directory:
        path = Path(directory) / "bad.json"
        payload = build_save_data(engine)
        payload["world_state"]["player_discoveries"] = ["unknown"]
        path.write_text(json.dumps(payload), encoding="utf-8")
        try:
            engine.load(str(path))
        except ValueError:
            pass
        else:
            raise AssertionError("Unknown discovery membership loaded.")
        assert engine.get_world_state() == before_state
        assert engine.get_scene_snapshot() == before_scene


def test_presenting_a_known_clue_resolves_the_open_thread_once() -> None:
    engine = GameEngine("data/regions/bryn_shander.json")
    engine.process_command("talk to captain")
    engine.process_command("investigate")
    result = engine.process_command("Present The Captain's Deliberate Trail TO Captain")["presentation"]
    assert result["changed"] is True
    assert result["response_text"] == (
        "Captain Darvin Grey studies the trail, then nods. "
        "‘That is enough to confirm the report. I will send a patrol west at once.’"
    )
    assert "Ã¢â‚¬" not in result["response_text"]
    assert engine.get_open_threads() == {}
    assert set(engine.get_world_state()["resolved_threads"]) == {"bryn_shander_west_road_bandit_report"}
    history_count = len(engine.query_history(event_type="unresolved_thread_opened"))
    assert engine.process_command("present The Captain's Deliberate Trail to captain")["presentation"]["changed"] is False
    assert engine.process_command("talk to captain")["success"] is True
    assert engine.get_open_threads() == {}
    assert set(engine.get_world_state()["resolved_threads"]) == {"bryn_shander_west_road_bandit_report"}
    assert len(engine.query_history(event_type="unresolved_thread_opened")) == history_count


def test_malformed_presentation_and_resolved_save_compatibility() -> None:
    engine = GameEngine("data/regions/bryn_shander.json")
    for command in ("present", "present clue", "present to captain", "present clue to"):
        result = engine.process_command(command)
        assert result["intent"] == "clue_presentation" and result["success"] is False
    engine.process_command("talk to captain")
    engine.process_command("investigate")
    engine.process_command("present The Captain's Deliberate Trail to captain")
    with TemporaryDirectory() as directory:
        path = Path(directory) / "resolved.json"
        engine.save(str(path))
        assert load_game(str(path)).get_world_state()["resolved_threads"] == engine.get_world_state()["resolved_threads"]
        legacy = build_save_data(GameEngine("data/regions/bryn_shander.json"))
        del legacy["world_state"]["resolved_threads"]
        legacy_path = Path(directory) / "legacy.json"
        legacy_path.write_text(json.dumps(legacy), encoding="utf-8")
        assert load_game(str(legacy_path)).get_world_state()["resolved_threads"] == {}


def test_resolved_thread_integrity_rejects_malformed_history_and_preserves_live_state() -> None:
    engine = build_resolved_engine()
    valid = build_save_data(engine)
    history = valid["world_state"]["history"]
    opening = next(entry for entry in history if entry["event_type"] == "unresolved_thread_opened")
    presentation = next(entry for entry in history if entry["event_type"] == "clue_presented")
    resolution = next(entry for entry in history if entry["event_type"] == "unresolved_thread_resolved")

    def write_payload(directory: str, label: str, mutate) -> Path:
        payload = deepcopy(valid)
        mutate(payload)
        path = Path(directory) / f"{label}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    with TemporaryDirectory() as directory:
        mutations = (
            ("declaration_mismatch", lambda p: p["world_state"]["resolved_threads"].__setitem__(
                "other_thread", {"thread_id": "other_thread", "status": "resolved", "resolved_by_history_id": presentation["history_id"]}
            )),
            ("false_presentation", lambda p: p["world_state"]["resolved_threads"][THREAD_ID].__setitem__(
                "resolved_by_history_id", opening["history_id"]
            )),
            ("presentation_target_mismatch", lambda p: next(entry for entry in p["world_state"]["history"] if entry["history_id"] == presentation["history_id"]).__setitem__(
                "target_entity_id", "guard_elin_voss"
            )),
            ("missing_opening", lambda p: p["world_state"].__setitem__(
                "history", [entry for entry in p["world_state"]["history"] if entry["event_type"] != "unresolved_thread_opened"]
            )),
            ("duplicate_opening", lambda p: p["world_state"]["history"].append(
                deepcopy(opening) | {"history_id": "history_999901"}
            )),
            ("missing_resolution", lambda p: p["world_state"].__setitem__(
                "history", [entry for entry in p["world_state"]["history"] if entry["event_type"] != "unresolved_thread_resolved"]
            )),
            ("duplicate_resolution", lambda p: p["world_state"]["history"].append(
                deepcopy(resolution) | {"history_id": "history_999902"}
            )),
            ("mismatched_resolution_source", lambda p: next(entry for entry in p["world_state"]["history"] if entry["history_id"] == resolution["history_id"]).__setitem__(
                "source_history_id", opening["history_id"]
            )),
            ("contradictory_open_and_resolved", lambda p: p["world_state"]["open_threads"].__setitem__(
                THREAD_ID, {"thread_id": THREAD_ID, "status": "open", "created_by_history_id": opening["source_history_id"]}
            )),
        )
        for label, mutate in mutations:
            expect_value_error(lambda path=write_payload(directory, label, mutate): load_game(str(path)))

        bad_path = write_payload(
            directory,
            "bad_live_load",
            lambda p: p["world_state"]["resolved_threads"][THREAD_ID].__setitem__(
                "resolved_by_history_id", opening["history_id"]
            ),
        )
        live_state = engine.world_state
        live_scene = engine.scene_snapshot
        expect_value_error(lambda: engine.load(str(bad_path)))
        assert engine.world_state is live_state
        assert engine.scene_snapshot is live_scene


def test_failed_resolved_transition_preserves_live_identity() -> None:
    engine = GameEngine("data/regions/bryn_shander.json")
    engine.process_command("talk to captain")
    engine.process_command("investigate")
    live_state = engine.world_state
    live_scene = engine.scene_snapshot
    with patch("engine.game_engine.validate_world_state", side_effect=ValueError("reject")):
        expect_value_error(lambda: engine.process_command("present The Captain's Deliberate Trail to captain"))
    assert engine.world_state is live_state
    assert engine.scene_snapshot is live_scene


def test_resolved_observation_is_derived_locally_and_persists_through_save_load() -> None:
    engine = GameEngine("data/regions/bryn_shander.json")
    observation = engine.region["conversation_discovery_resolution"]["resolved_observation"]
    assert engine.get_player_perception()["resolved_thread_observation"] == {}
    engine.process_command("talk to captain")
    engine.process_command("investigate")
    engine.process_command("present The Captain's Deliberate Trail to captain")
    assert engine.get_player_perception()["resolved_thread_observation"] == {"text": observation}
    engine.process_command("go south")
    assert engine.get_player_perception()["resolved_thread_observation"] == {}
    engine.process_command("go north")
    assert engine.get_player_perception()["resolved_thread_observation"] == {"text": observation}
    with TemporaryDirectory() as directory:
        path = Path(directory) / "resolved-observation.json"
        engine.save(str(path))
        loaded = load_game(str(path))
        assert loaded.get_player_perception()["resolved_thread_observation"] == {"text": observation}


def test_resolved_observation_is_rendered_once_on_each_eligible_visit() -> None:
    engine = build_resolved_engine()
    observation = engine.region["conversation_discovery_resolution"]["resolved_observation"]
    assert engine.get_narration()["description"].count(observation) == 1
    engine.process_command("go south")
    assert observation not in engine.get_narration()["description"]
    engine.process_command("go north")
    assert engine.get_narration()["description"].count(observation) == 1


if __name__ == "__main__":
    test_discovery_declarations()
    test_atomic_local_discovery_and_no_op()
    test_wrong_location_and_unknown_save_membership_fail_closed()
    test_presenting_a_known_clue_resolves_the_open_thread_once()
    test_malformed_presentation_and_resolved_save_compatibility()
    test_resolved_thread_integrity_rejects_malformed_history_and_preserves_live_state()
    test_failed_resolved_transition_preserves_live_identity()
    test_resolved_observation_is_derived_locally_and_persists_through_save_load()
    test_resolved_observation_is_rendered_once_on_each_eligible_visit()
    print("Discovery declaration tests passed.")
