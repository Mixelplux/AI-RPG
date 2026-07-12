from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import SAVE_VERSION, build_save_data, load_game
from engine.world_state import create_initial_world_state, validate_world_state


REGION_PATH = "data/regions/bryn_shander.json"
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
    before_scene = engine.get_scene_snapshot()
    with TemporaryDirectory() as temporary_directory:
        payload = build_save_data(engine)
        assert payload["save_version"] == SAVE_VERSION == 1
        assert payload["world_state"]["actor_knowledge"] == before_state["actor_knowledge"]
        path = Path(temporary_directory) / "knowledge.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        loaded = load_game(str(path))
        assert loaded.get_actor_knowledge(ACTOR_ID) == engine.get_actor_knowledge(ACTOR_ID)

        legacy = deepcopy(payload)
        del legacy["world_state"]["actor_knowledge"]
        legacy_path = Path(temporary_directory) / "legacy.json"
        legacy_path.write_text(json.dumps(legacy), encoding="utf-8")
        legacy_loaded = load_game(str(legacy_path))
        assert legacy_loaded.get_actor_knowledge(ACTOR_ID) == ()

        malformed = deepcopy(payload)
        malformed["world_state"]["actor_knowledge"] = {"missing": ["known"]}
        malformed_path = Path(temporary_directory) / "malformed.json"
        malformed_path.write_text(json.dumps(malformed), encoding="utf-8")
        expect_value_error(lambda: load_game(str(malformed_path)))
        expect_value_error(lambda: engine.load(str(malformed_path)))
    assert engine.get_world_state() == before_state
    assert engine.get_scene_snapshot() == before_scene
    assert "actor_knowledge" not in engine.get_player_perception()
    assert "actor_knowledge" not in engine.get_narration_context("look")


def main() -> None:
    test_region_validation_and_new_game_seeding()
    test_sparse_state_validation_and_inspection()
    test_persistence_legacy_and_atomic_live_load()
    print("Actor knowledge tests passed.")


if __name__ == "__main__":
    main()
