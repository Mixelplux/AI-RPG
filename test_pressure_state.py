import json
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.pressure_state import validate_pressure_state
from engine.region_validator import validate_region
from engine.save_system import SAVE_VERSION, build_save_data, load_game, save_game
from engine.world_state import create_initial_world_state
from play_game import print_pressures


REGION_PATH = "data/regions/bryn_shander.json"
PRESSURE_ID = "bryn_shander_winter"
REGION_ID = "icewind_dale_bryn_shander"
SECOND_PRESSURE_ID = "bryn_shander_supply_shortage"
EXPECTED_PRESSURE = {
    "pressure_id": PRESSURE_ID,
    "pressure_type": "winter",
    "scope_type": "region",
    "scope_id": REGION_ID,
    "level": 65,
    "provenance": {
        "kind": "region_pack",
        "source_id": REGION_ID,
    },
}
SECOND_PRESSURE = {
    "pressure_id": SECOND_PRESSURE_ID,
    "pressure_type": "supply_shortage",
    "scope_type": "region",
    "scope_id": REGION_ID,
    "level": 12,
    "provenance": {
        "kind": "region_pack",
        "source_id": REGION_ID,
    },
}


def load_region() -> dict:
    return json.loads(Path(REGION_PATH).read_text(encoding="utf-8"))


def build_engine() -> GameEngine:
    region = load_region()
    world_state = create_initial_world_state(region)
    world_state["pressures"][SECOND_PRESSURE_ID] = deepcopy(SECOND_PRESSURE)
    return GameEngine(REGION_PATH, initial_world_state=world_state)


def assert_invalid_region(region: dict, expected_text: str) -> None:
    try:
        validate_region(region)
    except ValueError as error:
        assert expected_text in str(error), str(error)
        return
    raise AssertionError(f"Expected invalid Region Pack: {expected_text}")


def assert_invalid_save(save_data: dict, expected_text: str) -> None:
    with TemporaryDirectory() as temp_dir:
        save_path = Path(temp_dir) / "invalid_save.json"
        save_path.write_text(json.dumps(save_data), encoding="utf-8")
        try:
            load_game(str(save_path))
        except ValueError as error:
            assert expected_text in str(error), str(error)
            return
    raise AssertionError(f"Expected invalid save: {expected_text}")


def test_region_seed_validation() -> None:
    region = load_region()
    validate_region(region)

    without_seeds = deepcopy(region)
    del without_seeds["initial_pressures"]
    validate_region(without_seeds)
    assert create_initial_world_state(without_seeds)["pressures"] == {}
    with TemporaryDirectory() as temp_dir:
        region_path = Path(temp_dir) / "region_without_pressures.json"
        region_path.write_text(json.dumps(without_seeds), encoding="utf-8")
        assert GameEngine(str(region_path)).get_pressures() == {}

    copied_state = create_initial_world_state(region)
    copied_state["pressures"][PRESSURE_ID]["level"] = 0
    copied_state["pressures"][PRESSURE_ID]["provenance"]["source_id"] = "changed"
    assert region["initial_pressures"] == [EXPECTED_PRESSURE]

    malformed_field = deepcopy(region)
    malformed_field["initial_pressures"] = {}
    assert_invalid_region(malformed_field, "initial_pressures must be a list")

    malformed_record = deepcopy(region)
    malformed_record["initial_pressures"] = ["not_a_record"]
    assert_invalid_region(malformed_record, "record must be a dictionary")

    missing_field = deepcopy(region)
    del missing_field["initial_pressures"][0]["pressure_type"]
    assert_invalid_region(missing_field, "missing=['pressure_type']")

    extra_field = deepcopy(region)
    extra_field["initial_pressures"][0]["unsupported"] = True
    assert_invalid_region(extra_field, "extra=['unsupported']")

    for field_name in ("pressure_id", "pressure_type"):
        invalid_type = deepcopy(region)
        invalid_type["initial_pressures"][0][field_name] = 7
        assert_invalid_region(invalid_type, f"{field_name} must be a non-empty string")

        empty_value = deepcopy(region)
        empty_value["initial_pressures"][0][field_name] = ""
        assert_invalid_region(empty_value, f"{field_name} must be a non-empty string")

    duplicate = deepcopy(region)
    duplicate["initial_pressures"].append(
        deepcopy(duplicate["initial_pressures"][0])
    )
    assert_invalid_region(duplicate, "Duplicate pressure_id")

    invalid_scope_type = deepcopy(region)
    invalid_scope_type["initial_pressures"][0]["scope_type"] = "actor"
    assert_invalid_region(invalid_scope_type, "scope_type must be region or location")

    invalid_scope_type_value = deepcopy(region)
    invalid_scope_type_value["initial_pressures"][0]["scope_type"] = []
    assert_invalid_region(
        invalid_scope_type_value,
        "scope_type must be region or location",
    )

    invalid_scope_id_type = deepcopy(region)
    invalid_scope_id_type["initial_pressures"][0]["scope_id"] = 3
    assert_invalid_region(invalid_scope_id_type, "scope_id must be a non-empty string")

    invalid_region_scope = deepcopy(region)
    invalid_region_scope["initial_pressures"][0]["scope_id"] = "wrong_region"
    assert_invalid_region(invalid_region_scope, "scope_id must equal region_id")

    invalid_location_scope = deepcopy(region)
    invalid_location_scope["initial_pressures"][0].update({
        "scope_type": "location",
        "scope_id": "missing_location",
    })
    assert_invalid_region(invalid_location_scope, "scope_id is not in the Region Pack")

    valid_location_scope = deepcopy(region)
    valid_location_scope["initial_pressures"][0].update({
        "scope_type": "location",
        "scope_id": region["locations"][0]["location_id"],
    })
    validate_region(valid_location_scope)

    invalid_provenance_kind = deepcopy(region)
    invalid_provenance_kind["initial_pressures"][0]["provenance"]["kind"] = "save"
    assert_invalid_region(invalid_provenance_kind, "kind must be region_pack")

    invalid_provenance_type = deepcopy(region)
    invalid_provenance_type["initial_pressures"][0]["provenance"] = []
    assert_invalid_region(invalid_provenance_type, "provenance must be a dictionary")

    invalid_provenance_source = deepcopy(region)
    invalid_provenance_source["initial_pressures"][0]["provenance"]["source_id"] = "wrong"
    assert_invalid_region(invalid_provenance_source, "source_id must equal")

    missing_provenance_field = deepcopy(region)
    del missing_provenance_field["initial_pressures"][0]["provenance"]["source_id"]
    assert_invalid_region(missing_provenance_field, "Pressure provenance fields are invalid")

    extra_provenance_field = deepcopy(region)
    extra_provenance_field["initial_pressures"][0]["provenance"]["extra"] = 1
    assert_invalid_region(extra_provenance_field, "Pressure provenance fields are invalid")

    for invalid_level in (-1, 101):
        invalid = deepcopy(region)
        invalid["initial_pressures"][0]["level"] = invalid_level
        assert_invalid_region(invalid, "level must be from 0 through 100")

    boolean_level = deepcopy(region)
    boolean_level["initial_pressures"][0]["level"] = True
    assert_invalid_region(boolean_level, "not a boolean")

    float_level = deepcopy(region)
    float_level["initial_pressures"][0]["level"] = 65.0
    assert_invalid_region(float_level, "must be an integer")


def test_runtime_representation_and_reads() -> None:
    engine = GameEngine(REGION_PATH)
    pressures = engine.get_pressures()

    assert pressures == {PRESSURE_ID: EXPECTED_PRESSURE}
    assert engine.get_world_state()["pressures"] == pressures
    assert engine.get_pressure(PRESSURE_ID) == EXPECTED_PRESSURE
    assert engine.get_pressure("unknown_pressure") is None

    region_seed_before = deepcopy(engine.region["initial_pressures"])
    world_before = engine.get_world_state()
    scene_before = engine.get_scene_snapshot()

    pressures[PRESSURE_ID]["level"] = 0
    pressures[PRESSURE_ID]["provenance"]["source_id"] = "mutated"
    one_pressure = engine.get_pressure(PRESSURE_ID)
    assert one_pressure is not None
    one_pressure["level"] = 1
    one_pressure["provenance"]["source_id"] = "also_mutated"

    assert engine.get_pressure(PRESSURE_ID) == EXPECTED_PRESSURE
    assert engine.region["initial_pressures"] == region_seed_before
    assert engine.get_world_state() == world_before
    assert engine.get_scene_snapshot() == scene_before

    mismatched_key = {"wrong_key": deepcopy(EXPECTED_PRESSURE)}
    try:
        validate_pressure_state(mismatched_key, load_region())
    except ValueError as error:
        assert "key must match" in str(error)
    else:
        raise AssertionError("Mismatched pressure dictionary key was accepted.")

    output = StringIO()
    with redirect_stdout(output):
        print_pressures(engine.get_pressures())
    rendered = output.getvalue()
    assert "=== PRESSURES ===" in rendered
    assert PRESSURE_ID in rendered
    assert "level=65" in rendered


def test_pressure_level_change_atomicity() -> None:
    engine = build_engine()

    starting_world_state = engine.get_world_state()
    starting_scene_snapshot = engine.get_scene_snapshot()
    starting_history = engine.get_history()

    no_op_result = engine.set_pressure_level(PRESSURE_ID, 65)
    assert list(no_op_result) == [
        "changed",
        "pressure_id",
        "previous_level",
        "new_level",
        "history_id",
    ]
    assert no_op_result == {
        "changed": False,
        "pressure_id": PRESSURE_ID,
        "previous_level": 65,
        "new_level": 65,
        "history_id": None,
    }
    assert engine.get_world_state() == starting_world_state
    assert engine.get_scene_snapshot() == starting_scene_snapshot
    assert engine.get_history() == starting_history

    result = engine.set_pressure_level(PRESSURE_ID, 70)
    assert list(result) == [
        "changed",
        "pressure_id",
        "previous_level",
        "new_level",
        "history_id",
    ]
    assert result == {
        "changed": True,
        "pressure_id": PRESSURE_ID,
        "previous_level": 65,
        "new_level": 70,
        "history_id": "history_000001",
    }

    world_state_after_change = engine.get_world_state()
    expected_world_state = deepcopy(starting_world_state)
    expected_world_state["pressures"][PRESSURE_ID]["level"] = 70
    expected_world_state["history"].append(
        {
            "history_id": "history_000001",
            "event_type": "pressure_changed",
            "summary": (
                "Pressure bryn_shander_winter changed from 65 to 70."
            ),
            "time": deepcopy(starting_world_state["time"]),
            "pressure_id": PRESSURE_ID,
            "pressure_type": "winter",
            "scope_type": "region",
            "scope_id": REGION_ID,
            "previous_level": 65,
            "new_level": 70,
        }
    )
    assert world_state_after_change == expected_world_state
    assert world_state_after_change["time"] == starting_world_state["time"]
    assert world_state_after_change["player"] == starting_world_state["player"]
    assert world_state_after_change["weather"] == starting_world_state["weather"]
    assert world_state_after_change["pressures"][PRESSURE_ID]["level"] == 70
    assert world_state_after_change["pressures"][PRESSURE_ID]["pressure_type"] == "winter"
    assert world_state_after_change["pressures"][PRESSURE_ID]["scope_type"] == "region"
    assert world_state_after_change["pressures"][PRESSURE_ID]["scope_id"] == REGION_ID
    assert world_state_after_change["pressures"][PRESSURE_ID]["provenance"] == EXPECTED_PRESSURE["provenance"]
    assert world_state_after_change["pressures"][SECOND_PRESSURE_ID] == SECOND_PRESSURE
    assert engine.region["initial_pressures"] == [EXPECTED_PRESSURE]
    assert engine.get_scene_snapshot() == starting_scene_snapshot

    history = engine.get_history()
    assert len(history) == 1
    entry = history[0]
    assert list(entry) == [
        "history_id",
        "event_type",
        "summary",
        "time",
        "pressure_id",
        "pressure_type",
        "scope_type",
        "scope_id",
        "previous_level",
        "new_level",
    ]
    assert entry["history_id"] == "history_000001"
    assert entry["event_type"] == "pressure_changed"
    assert entry["summary"] == "Pressure bryn_shander_winter changed from 65 to 70."
    assert entry["time"] == starting_world_state["time"]
    assert entry["pressure_id"] == PRESSURE_ID
    assert entry["pressure_type"] == "winter"
    assert entry["scope_type"] == "region"
    assert entry["scope_id"] == REGION_ID
    assert entry["previous_level"] == 65
    assert entry["new_level"] == 70
    assert "location" not in entry

    durable_state_before_result_mutation = engine.get_world_state()
    durable_history_before_result_mutation = engine.get_history()
    result["new_level"] = 10
    result["history_id"] = "history_999999"
    assert result["new_level"] == 10
    assert result["history_id"] == "history_999999"
    assert engine.get_world_state() == durable_state_before_result_mutation
    assert engine.get_history() == durable_history_before_result_mutation
    assert engine.get_pressure(PRESSURE_ID)["level"] == 70
    assert engine.get_pressure(SECOND_PRESSURE_ID) == SECOND_PRESSURE


def test_pressure_level_change_validation_and_atomic_failure() -> None:
    engine = build_engine()
    starting_world_state = engine.get_world_state()
    starting_history = engine.get_history()
    starting_scene_snapshot = engine.get_scene_snapshot()

    for bad_pressure_id in ("missing_pressure", ""):
        try:
            engine.set_pressure_level(bad_pressure_id, 70)
        except ValueError as error:
            assert "pressure" in str(error).lower()
        else:
            raise AssertionError("Unknown pressure_id was accepted.")
        assert engine.get_world_state() == starting_world_state
        assert engine.get_history() == starting_history
        assert engine.get_scene_snapshot() == starting_scene_snapshot

    for invalid_level in (True, "70", 65.0, -1, 101):
        try:
            engine.set_pressure_level(PRESSURE_ID, invalid_level)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Invalid level was accepted: {invalid_level!r}")

        assert engine.get_world_state() == starting_world_state
        assert engine.get_history() == starting_history
        assert engine.get_scene_snapshot() == starting_scene_snapshot

    import engine.game_engine as game_engine_module

    original_add_history_entry = game_engine_module.add_history_entry
    try:
        def boom_add_history_entry(*args, **kwargs):
            raise RuntimeError("history failure")

        game_engine_module.add_history_entry = boom_add_history_entry
        try:
            engine.set_pressure_level(PRESSURE_ID, 70)
        except RuntimeError as error:
            assert "history failure" in str(error)
        else:
            raise AssertionError("History failure was swallowed.")
    finally:
        game_engine_module.add_history_entry = original_add_history_entry

    assert engine.get_world_state() == starting_world_state
    assert engine.get_history() == starting_history
    assert engine.get_scene_snapshot() == starting_scene_snapshot

    original_validate_world_state = game_engine_module.validate_world_state
    try:
        def boom_validate_world_state(*args, **kwargs):
            raise ValueError("candidate validation failure")

        game_engine_module.validate_world_state = boom_validate_world_state
        try:
            engine.set_pressure_level(PRESSURE_ID, 70)
        except ValueError as error:
            assert "candidate validation failure" in str(error)
        else:
            raise AssertionError("Candidate validation failure was swallowed.")
    finally:
        game_engine_module.validate_world_state = original_validate_world_state

    assert engine.get_world_state() == starting_world_state
    assert engine.get_history() == starting_history
    assert engine.get_scene_snapshot() == starting_scene_snapshot


def test_save_load_and_legacy_normalization() -> None:
    engine = build_engine()
    starting_scene_snapshot = engine.get_scene_snapshot()
    result = engine.set_pressure_level(PRESSURE_ID, 70)

    with TemporaryDirectory() as temp_dir:
        save_path = Path(temp_dir) / "pressure_save.json"
        save_game(engine, str(save_path))
        saved_payload = json.loads(save_path.read_text(encoding="utf-8"))
        loaded_engine = load_game(str(save_path))

        assert saved_payload["save_version"] == SAVE_VERSION == 1
        assert saved_payload["world_state"]["pressures"] == engine.get_pressures()
        assert saved_payload["world_state"]["history"] == engine.get_history()
        assert loaded_engine.get_pressures() == engine.get_pressures()
        assert loaded_engine.get_history() == engine.get_history()
        assert loaded_engine.get_history()[0]["history_id"] == result["history_id"]
        assert loaded_engine.get_history()[0]["time"] == engine.get_history()[0]["time"]
        assert loaded_engine.get_history()[0]["pressure_id"] == PRESSURE_ID
        assert loaded_engine.get_history()[0]["pressure_type"] == "winter"
        assert loaded_engine.get_history()[0]["scope_type"] == "region"
        assert loaded_engine.get_history()[0]["scope_id"] == REGION_ID

        legacy_payload = build_save_data(engine)
        del legacy_payload["world_state"]["pressures"]
        legacy_path = Path(temp_dir) / "legacy_save.json"
        legacy_path.write_text(json.dumps(legacy_payload), encoding="utf-8")
        legacy_engine = load_game(str(legacy_path))

        assert "pressures" in legacy_engine.get_world_state()
        assert legacy_engine.get_pressures() == {}
        assert legacy_engine.region["initial_pressures"] == [EXPECTED_PRESSURE]
        assert legacy_engine.get_scene_snapshot() == starting_scene_snapshot

        next_history_result = loaded_engine.set_pressure_level(
            PRESSURE_ID,
            65,
        )
        assert next_history_result["history_id"] == "history_000002"
        assert next_history_result["history_id"] != result["history_id"]
        assert loaded_engine.get_history()[-1]["history_id"] == "history_000002"

    malformed_payload = build_save_data(engine)
    malformed_payload["world_state"]["pressures"] = []
    assert_invalid_save(malformed_payload, "pressures must be a dictionary")


def main() -> None:
    test_region_seed_validation()
    test_runtime_representation_and_reads()
    test_pressure_level_change_atomicity()
    test_pressure_level_change_validation_and_atomic_failure()
    test_save_load_and_legacy_normalization()
    print("Pressure state tests passed.")


if __name__ == "__main__":
    main()
