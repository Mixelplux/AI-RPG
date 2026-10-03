from copy import deepcopy
import json
from pathlib import Path
from test_artifact_files import artifact_files

from engine.game_engine import GameEngine
import engine.game_engine as game_engine_module
from engine.region_validator import validate_region
from engine.save_system import SAVE_VERSION, build_save_data, load_game
from engine.world_state import create_initial_world_state, validate_world_state


REGION_PATH = "test_fixtures/bryn_shander_legacy.json"
ACTOR_ID = "captain_darvin_grey"
OTHER_ACTOR_ID = "guard_elin_voss"


def expect_value_error(callable_) -> None:
    try:
        callable_()
    except ValueError:
        return
    raise AssertionError("Expected ValueError.")


def test_region_validation_and_new_game_seeding() -> None:
    engine = GameEngine(REGION_PATH)
    seeds = tuple(engine.region["entities"][0]["knowledge"])
    assert engine.get_actor_knowledge(ACTOR_ID) == seeds
    assert engine.get_actor_knowledge(OTHER_ACTOR_ID) == (
        "familiar_with_local_travelers", "rotating_shift_schedule"
    )
    state = engine.get_world_state()
    assert state["actor_knowledge"][ACTOR_ID] == list(seeds)
    state["actor_knowledge"][ACTOR_ID].append("runtime_only")
    assert engine.get_actor_knowledge(ACTOR_ID) == seeds
    engine.region["entities"][0]["knowledge"].append("authored_later")
    assert engine.get_actor_knowledge(ACTOR_ID) == seeds

    for invalid_knowledge in (None, "knowledge", [""], ["known", "known"], [{}]):
        invalid = deepcopy(engine.region)
        invalid["entities"][0]["knowledge"] = invalid_knowledge
        expect_value_error(lambda invalid=invalid: validate_region(invalid))


def test_sparse_state_validation_and_inspection() -> None:
    engine = GameEngine(REGION_PATH)
    state = create_initial_world_state(engine.region)
    state["actor_knowledge"] = {ACTOR_ID: ["known"]}
    validate_world_state(state, engine.region)
    assert engine.get_actor_knowledge(ACTOR_ID) == (
        "recent_bandit_activity_on_west_road",
        "supply_shortage_preparing_for_winter_peak",
    )
    assert GameEngine(REGION_PATH, initial_world_state=state).get_actor_knowledge(
        ACTOR_ID
    ) == ("known",)

    invalid_values = (
        [], {ACTOR_ID: []}, {"": ["known"]}, {1: ["known"]},
        {"missing": ["known"]}, {"spawned_guard_1": ["known"]},
        {ACTOR_ID: "known"}, {ACTOR_ID: [""]}, {ACTOR_ID: [1]},
        {ACTOR_ID: ["known", "known"]}, {ACTOR_ID: [{"id": "known"}]},
    )
    for invalid_value in invalid_values:
        candidate = create_initial_world_state(engine.region)
        candidate["actor_knowledge"] = invalid_value
        expect_value_error(lambda candidate=candidate: validate_world_state(candidate, engine.region))

    result = engine.get_actor_knowledge(ACTOR_ID)
    assert isinstance(result, tuple)
    assert result == engine.get_actor_knowledge(ACTOR_ID)
    expect_value_error(lambda: engine.get_actor_knowledge("missing"))
    expect_value_error(lambda: engine.get_actor_knowledge(""))


def test_persistence_legacy_and_atomic_live_load() -> None:
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_scene = engine.scene_snapshot
    with artifact_files("test_actor_knowledge") as temporary_directory:
        payload = build_save_data(engine)
        assert payload["save_version"] == SAVE_VERSION == 1
        assert payload["world_state"]["actor_knowledge"] == before_state["actor_knowledge"]
        path = Path(temporary_directory) / "test_actor_knowledge_knowledge.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        loaded = load_game(str(path))
        assert loaded.get_actor_knowledge(ACTOR_ID) == engine.get_actor_knowledge(ACTOR_ID)

        legacy = deepcopy(payload)
        del legacy["world_state"]["actor_knowledge"]
        legacy_path = Path(temporary_directory) / "test_actor_knowledge_legacy.json"
        legacy_path.write_text(json.dumps(legacy), encoding="utf-8")
        legacy_loaded = load_game(str(legacy_path))
        assert legacy_loaded.get_actor_knowledge(ACTOR_ID) == ()

        malformed = deepcopy(payload)
        malformed["world_state"]["actor_knowledge"] = {"missing": ["known"]}
        malformed_path = Path(temporary_directory) / "test_actor_knowledge_malformed.json"
        malformed_path.write_text(json.dumps(malformed), encoding="utf-8")
        expect_value_error(lambda: load_game(str(malformed_path)))
        expect_value_error(lambda: engine.load(str(malformed_path)))
    assert engine.get_world_state() == before_state
    assert engine.get_scene_snapshot() == before_scene
    assert "actor_knowledge" not in engine.get_player_perception()
    assert "actor_knowledge" not in engine.get_narration_context("look")


def test_explicit_atomic_addition_and_duplicate_noop() -> None:
    engine = GameEngine(REGION_PATH)
    knowledge_id = "heard_about_the_eastgate_patrol"
    before_scene = engine.scene_snapshot
    before_history = engine.get_history()
    before_world_state = engine.world_state

    result = engine.add_actor_knowledge(ACTOR_ID, knowledge_id)
    assert result == {
        "changed": True,
        "actor_id": ACTOR_ID,
        "knowledge_id": knowledge_id,
        "history_id": "history_000001",
    }
    assert engine.world_state is not before_world_state
    assert engine.scene_snapshot is before_scene
    assert engine.get_actor_knowledge(ACTOR_ID)[-1] == knowledge_id
    entry = engine.get_history_entry_by_id(result["history_id"])
    assert entry == {
        "history_id": result["history_id"],
        "event_type": "actor_knowledge_added",
        "summary": f"Actor {ACTOR_ID} gained knowledge {knowledge_id}.",
        "time": engine.get_world_state()["time"],
        "actor_id": ACTOR_ID,
        "knowledge_id": knowledge_id,
    }
    assert engine.query_history(event_type="actor_knowledge_added") == [entry]

    state_before_duplicate = engine.world_state
    history_before_duplicate = engine.get_history()
    scene_before_duplicate = engine.scene_snapshot
    duplicate = engine.add_actor_knowledge(ACTOR_ID, knowledge_id)
    assert duplicate == {
        "changed": False,
        "actor_id": ACTOR_ID,
        "knowledge_id": knowledge_id,
        "history_id": None,
    }
    assert engine.world_state is state_before_duplicate
    assert engine.get_history() == history_before_duplicate
    assert engine.scene_snapshot is scene_before_duplicate
    assert before_history == []


def test_addition_validation_and_candidate_failure_are_atomic() -> None:
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_scene = engine.get_scene_snapshot()
    for actor_id, knowledge_id in (
        ("", "known"), ("missing", "known"), (ACTOR_ID, ""),
        (ACTOR_ID, None),
    ):
        expect_value_error(
            lambda actor_id=actor_id, knowledge_id=knowledge_id:
            engine.add_actor_knowledge(actor_id, knowledge_id)
        )
    assert engine.get_world_state() == before_state
    assert engine.get_scene_snapshot() == before_scene

    original_validate = game_engine_module.validate_world_state
    try:
        game_engine_module.validate_world_state = (
            lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("blocked"))
        )
        expect_value_error(
            lambda: engine.add_actor_knowledge(ACTOR_ID, "candidate_failure")
        )
    finally:
        game_engine_module.validate_world_state = original_validate
    assert engine.get_world_state() == before_state
    assert engine.get_scene_snapshot() == before_scene


def test_added_membership_persists_through_save_load() -> None:
    engine = GameEngine(REGION_PATH)
    result = engine.add_actor_knowledge(ACTOR_ID, "saved_knowledge")
    with artifact_files("test_actor_knowledge") as temporary_directory:
        path = Path(temporary_directory) / "test_actor_knowledge_knowledge_addition.json"
        path.write_text(json.dumps(build_save_data(engine)), encoding="utf-8")
        loaded = load_game(str(path))
    assert loaded.get_actor_knowledge(ACTOR_ID)[-1] == "saved_knowledge"
    assert loaded.get_history_entry_by_id(result["history_id"]) == (
        engine.get_history_entry_by_id(result["history_id"])
    )


def test_causally_referenced_addition_and_duplicate_noop() -> None:
    engine = GameEngine(REGION_PATH)
    source_result = engine.add_actor_knowledge(ACTOR_ID, "source_knowledge")
    source_id = source_result["history_id"]
    source_entry = engine.get_history_entry_by_id(source_id)
    before_scene = engine.scene_snapshot

    result = engine.add_actor_knowledge_from_event(
        OTHER_ACTOR_ID, "causally_added_knowledge", source_id
    )
    assert result == {
        "changed": True,
        "actor_id": OTHER_ACTOR_ID,
        "knowledge_id": "causally_added_knowledge",
        "source_history_id": source_id,
        "history_id": "history_000002",
    }
    assert engine.get_actor_knowledge(OTHER_ACTOR_ID)[-1] == "causally_added_knowledge"
    entry = engine.get_history_entry_by_id(result["history_id"])
    assert entry == {
        "history_id": result["history_id"],
        "event_type": "actor_knowledge_added",
        "summary": "Actor guard_elin_voss gained knowledge causally_added_knowledge.",
        "time": engine.get_world_state()["time"],
        "actor_id": OTHER_ACTOR_ID,
        "knowledge_id": "causally_added_knowledge",
        "source_history_id": source_id,
    }
    assert engine.get_history_entry_by_id(source_id) == source_entry
    assert engine.scene_snapshot is before_scene
    assert engine.query_history(event_type="actor_knowledge_added")[-1] == entry

    before_state = engine.world_state
    before_history = engine.get_history()
    duplicate = engine.add_actor_knowledge_from_event(
        OTHER_ACTOR_ID, "causally_added_knowledge", source_id
    )
    assert duplicate == result | {"changed": False, "history_id": None}
    assert engine.world_state is before_state
    assert engine.get_history() == before_history
    assert engine.scene_snapshot is before_scene
    duplicate["source_history_id"] = "mutated"
    assert engine.get_history_entry_by_id(source_id) == source_entry


def test_causally_referenced_addition_validation_persistence_and_atomic_load() -> None:
    engine = GameEngine(REGION_PATH)
    source_id = engine.add_actor_knowledge(ACTOR_ID, "source_knowledge")["history_id"]
    before_state = engine.get_world_state()
    before_scene = engine.scene_snapshot
    for args in (
        (ACTOR_ID, "known", None), (ACTOR_ID, "known", ""),
        (ACTOR_ID, "known", 1), (ACTOR_ID, "known", "history_999999"),
        ("missing", "known", source_id), (ACTOR_ID, "", source_id),
        (ACTOR_ID, None, source_id),
    ):
        expect_value_error(lambda args=args: engine.add_actor_knowledge_from_event(*args))
    assert engine.get_world_state() == before_state
    assert engine.scene_snapshot is before_scene

    result = engine.add_actor_knowledge_from_event(
        ACTOR_ID, "persisted_causal_knowledge", source_id
    )
    with artifact_files("test_actor_knowledge") as temporary_directory:
        path = Path(temporary_directory) / "test_actor_knowledge_causal_knowledge.json"
        path.write_text(json.dumps(build_save_data(engine)), encoding="utf-8")
        loaded = load_game(str(path))
        assert loaded.get_history_entry_by_id(result["history_id"])["source_history_id"] == source_id
        assert loaded.get_history_entry_by_id(source_id) == engine.get_history_entry_by_id(source_id)
        assert not loaded.add_actor_knowledge_from_event(
            ACTOR_ID, "persisted_causal_knowledge", source_id
        )["changed"]

        malformed = build_save_data(engine)
        malformed["world_state"]["history"][-1]["source_history_id"] = "history_999999"
        malformed_path = Path(temporary_directory) / "test_actor_knowledge_bad_causal_knowledge.json"
        malformed_path.write_text(json.dumps(malformed), encoding="utf-8")
        live_before = engine.get_world_state()
        scene_before = engine.scene_snapshot
        expect_value_error(lambda: engine.load(str(malformed_path)))
        assert engine.get_world_state() == live_before
        assert engine.scene_snapshot is scene_before


def main() -> None:
    test_region_validation_and_new_game_seeding()
    test_sparse_state_validation_and_inspection()
    test_persistence_legacy_and_atomic_live_load()
    test_explicit_atomic_addition_and_duplicate_noop()
    test_addition_validation_and_candidate_failure_are_atomic()
    test_added_membership_persists_through_save_load()
    test_causally_referenced_addition_and_duplicate_noop()
    test_causally_referenced_addition_validation_persistence_and_atomic_load()
    print("Actor knowledge tests passed.")


if __name__ == "__main__":
    main()
