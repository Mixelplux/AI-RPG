import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import load_game, save_game
from engine.world_update import apply_interaction


REGION_PATH = "data/regions/bryn_shander.json"
PRESSURE_ID = "bryn_shander_gate_scrutiny"
EFFECT_ID = "north_gate_captain_scrutiny"


def load_region() -> dict:
    return json.loads(Path(REGION_PATH).read_text(encoding="utf-8"))


def new_pressure_test_engine() -> GameEngine:
    engine = GameEngine(REGION_PATH)
    engine.region.pop("conversation_actor_relocation_effect", None)
    return engine


def assert_invalid(region: dict, text: str) -> None:
    try:
        validate_region(region)
    except ValueError as error:
        assert text in str(error), str(error)
        return
    raise AssertionError(f"Expected invalid Region Pack containing: {text}")


def test_declaration_validation() -> None:
    region = load_region()
    validate_region(region)

    absent = deepcopy(region)
    del absent["conversation_pressure_effects"]
    validate_region(absent)

    invalid_container = deepcopy(region)
    invalid_container["conversation_pressure_effects"] = {}
    assert_invalid(invalid_container, "must be a list")

    invalid_item = deepcopy(region)
    invalid_item["conversation_pressure_effects"] = ["bad"]
    assert_invalid(invalid_item, "must be a dictionary")

    missing = deepcopy(region)
    del missing["conversation_pressure_effects"][0]["effect_id"]
    assert_invalid(missing, "missing=['effect_id']")

    extra = deepcopy(region)
    extra["conversation_pressure_effects"][0]["extra"] = True
    assert_invalid(extra, "extra=['extra']")

    for field in ("effect_id", "target_entity_id", "pressure_id"):
        for value in ("", 7):
            invalid = deepcopy(region)
            invalid["conversation_pressure_effects"][0][field] = value
            assert_invalid(invalid, f"{field} must be a non-empty string")

    duplicate_effect = deepcopy(region)
    duplicate_effect["conversation_pressure_effects"].append(
        deepcopy(duplicate_effect["conversation_pressure_effects"][0])
    )
    duplicate_effect["conversation_pressure_effects"][1][
        "target_entity_id"
    ] = "guard_elin_voss"
    assert_invalid(duplicate_effect, "Duplicate conversation pressure effect_id")

    duplicate_target = deepcopy(region)
    duplicate_target["conversation_pressure_effects"].append(
        deepcopy(duplicate_target["conversation_pressure_effects"][0])
    )
    duplicate_target["conversation_pressure_effects"][1]["effect_id"] = "other"
    assert_invalid(duplicate_target, "Multiple conversation pressure effects")

    unknown_entity = deepcopy(region)
    unknown_entity["conversation_pressure_effects"][0][
        "target_entity_id"
    ] = "missing"
    assert_invalid(unknown_entity, "must reference exactly one Region Pack entity")

    duplicate_entity = deepcopy(region)
    duplicate_entity["entities"].append(
        deepcopy(duplicate_entity["entities"][0])
    )
    assert_invalid(
        duplicate_entity,
        "must reference exactly one Region Pack entity",
    )

    unknown_pressure = deepcopy(region)
    unknown_pressure["conversation_pressure_effects"][0][
        "pressure_id"
    ] = "missing"
    assert_invalid(unknown_pressure, "Unknown conversation effect pressure")

    for level, text in ((True, "not a boolean"), (25.0, "must be an integer"),
                        (-1, "from 0 through 100"), (101, "from 0 through 100")):
        invalid = deepcopy(region)
        invalid["conversation_pressure_effects"][0]["new_level"] = level
        assert_invalid(invalid, text)


def test_material_unmatched_and_no_op_behavior() -> None:
    engine = new_pressure_test_engine()
    before = engine.get_world_state()
    scene_before = engine.get_scene_snapshot()
    region_before = deepcopy(engine.region)

    result = engine.process_command("talk to captain")
    history = engine.get_history()
    source = next(entry for entry in history if entry["event_type"] == "player_conversation")
    consequence = next(entry for entry in history if entry["event_type"] == "pressure_changed")
    thread_opened = next(entry for entry in history if entry["event_type"] == "unresolved_thread_opened")

    assert result["pressure_consequence"] == {
        "effect_id": EFFECT_ID,
        "changed": True,
        "pressure_id": PRESSURE_ID,
        "previous_level": 10,
        "new_level": 25,
        "history_id": consequence["history_id"],
        "source_history_id": source["history_id"],
    }
    assert source["event_type"] == "player_conversation"
    assert source["target_entity_id"] == "captain_darvin_grey"
    expected_source_state = apply_interaction(before, result)
    assert source == expected_source_state["history"][-1]
    assert consequence["event_type"] == "pressure_changed"
    assert consequence["source_history_id"] == source["history_id"]
    assert thread_opened["event_type"] == "unresolved_thread_opened"
    assert thread_opened["source_history_id"] == source["history_id"]
    assert source["time"] == consequence["time"] == before["time"]
    assert engine.get_pressure(PRESSURE_ID)["level"] == 25
    assert engine.get_pressure("bryn_shander_winter") == before["pressures"][
        "bryn_shander_winter"
    ]
    assert engine.get_world_state()["time"] == before["time"]
    assert engine.get_scene_snapshot() == scene_before

    durable = engine.get_world_state()
    result["pressure_consequence"]["new_level"] = 99
    result["target_resolution"]["identifier"] = "changed"
    assert engine.get_world_state() == durable
    assert engine.region == region_before
    assert engine.get_scene_snapshot() == scene_before

    pressure_before_repeat = engine.get_pressure(PRESSURE_ID)
    repeated = engine.process_command("talk to captain")
    assert repeated["pressure_consequence"]["changed"] is False
    assert repeated["pressure_consequence"]["history_id"] is None
    assert repeated["pressure_consequence"]["source_history_id"] == (
        engine.get_history()[-1]["history_id"]
    )
    assert engine.get_history()[-1]["event_type"] == "player_conversation"
    assert len(engine.get_history()) == 5
    assert engine.get_pressure(PRESSURE_ID) == pressure_before_repeat

    elin = engine.process_command("talk to elin")
    assert elin["success"]
    assert "pressure_consequence" not in elin
    assert engine.get_history()[-1]["target_entity_id"] == "guard_elin_voss"
    assert len(engine.get_history()) == 6

    for command in ("talk to blacksmith", "talk to guard"):
        history_before = engine.get_history()
        failed = engine.process_command(command)
        assert not failed["success"]
        assert engine.get_history() == history_before

    history_before = engine.get_history()
    failed_conversation = {
        "success": False,
        "intent": "conversation",
        "message": "Conversation failed.",
        "action": {
            "type": "talk",
            "target": None,
            "parameters": {},
            "confidence": 1.0,
        },
        "world_changes": [],
    }
    with patch(
        "engine.game_engine.process_player_input",
        return_value=failed_conversation,
    ):
        unsuccessful = engine.process_command("talk")
    assert not unsuccessful["success"]
    assert engine.get_history() == history_before

    exit_result = engine.process_command("talk to north")
    assert exit_result["success"]
    assert "pressure_consequence" not in exit_result
    assert len(engine.get_history()) == 6


def test_matched_atomic_failures() -> None:
    import engine.game_engine as game_engine_module

    def assert_unchanged_after_failure(engine, callable_) -> None:
        state = engine.get_world_state()
        scene = engine.get_scene_snapshot()
        try:
            callable_()
        except (KeyError, RuntimeError, ValueError):
            pass
        else:
            raise AssertionError("Injected failure was swallowed.")
        assert engine.get_world_state() == state
        assert engine.get_scene_snapshot() == scene

    engine = new_pressure_test_engine()
    with patch.object(game_engine_module, "apply_interaction", side_effect=RuntimeError("source")):
        assert_unchanged_after_failure(
            engine, lambda: engine.process_command("talk to captain")
        )

    engine = new_pressure_test_engine()
    with patch.object(game_engine_module, "prepare_pressure_level_change", side_effect=RuntimeError("pressure")):
        assert_unchanged_after_failure(
            engine, lambda: engine.process_command("talk to captain")
        )

    engine = new_pressure_test_engine()
    del engine.region["conversation_pressure_effects"][0]["pressure_id"]
    assert_unchanged_after_failure(
        engine, lambda: engine.process_command("talk to captain")
    )

    engine = new_pressure_test_engine()
    original_add = game_engine_module.add_history_entry
    with patch.object(
        game_engine_module,
        "add_history_entry",
        side_effect=RuntimeError("consequence"),
    ):
        assert_unchanged_after_failure(
            engine, lambda: engine.process_command("talk to captain")
        )
    game_engine_module.add_history_entry = original_add

    engine = new_pressure_test_engine()
    with patch.object(game_engine_module, "validate_world_state", side_effect=ValueError("state")):
        assert_unchanged_after_failure(
            engine, lambda: engine.process_command("talk to captain")
        )

    engine = new_pressure_test_engine()
    with patch.object(game_engine_module, "build_scene", side_effect=RuntimeError("scene")):
        assert_unchanged_after_failure(
            engine, lambda: engine.process_command("talk to captain")
        )


def test_save_load_without_replay() -> None:
    engine = new_pressure_test_engine()
    engine.process_command("talk to captain")
    history = engine.get_history()

    with TemporaryDirectory() as temp_dir:
        path = str(Path(temp_dir) / "save.json")
        save_game(engine, path)
        loaded = load_game(path)

    loaded.region.pop("conversation_actor_relocation_effect", None)

    assert loaded.get_history() == history
    assert loaded.get_pressure(PRESSURE_ID)["level"] == 25
    existing_ids = {entry["history_id"] for entry in history}
    result = loaded.process_command("talk to captain")
    assert result["pressure_consequence"]["changed"] is False
    assert loaded.get_history()[:-1] == history
    assert loaded.get_history()[-1]["history_id"] not in existing_ids
    assert "conversation_pressure_effects" not in loaded.get_world_state()


def main() -> None:
    test_declaration_validation()
    test_material_unmatched_and_no_op_behavior()
    test_matched_atomic_failures()
    test_save_load_without_replay()
    print("Conversation pressure effect tests passed.")


if __name__ == "__main__":
    main()
