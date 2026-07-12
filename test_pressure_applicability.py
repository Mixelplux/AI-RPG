import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.pressure_state import get_applicable_pressures
from engine.save_system import load_game, save_game


REGION_PATH = "data/regions/bryn_shander.json"
REGION_ID = "icewind_dale_bryn_shander"
GATE_LOCATION_ID = "bryn_shander_gate_north"
MAIN_STREET_LOCATION_ID = "bryn_shander_main_street"
WINTER_PRESSURE_ID = "bryn_shander_winter"
GATE_PRESSURE_ID = "bryn_shander_gate_scrutiny"
MAIN_STREET_PRESSURE_ID = "bryn_shander_main_street_watch"
EXTRA_REGION_PRESSURE_ID = "bryn_shander_supply_shortage"


def load_region() -> dict:
    return json.loads(Path(REGION_PATH).read_text(encoding="utf-8"))


def build_engine() -> GameEngine:
    return GameEngine(REGION_PATH)


def build_pressure(
    pressure_id: str,
    pressure_type: str,
    scope_type: str,
    scope_id: str,
    level: int,
) -> dict:
    return {
        "pressure_id": pressure_id,
        "pressure_type": pressure_type,
        "scope_type": scope_type,
        "scope_id": scope_id,
        "level": level,
        "provenance": {
            "kind": "region_pack",
            "source_id": REGION_ID,
        },
    }


def test_region_and_location_applicability() -> None:
    engine = build_engine()
    engine.world_state["pressures"][EXTRA_REGION_PRESSURE_ID] = build_pressure(
        EXTRA_REGION_PRESSURE_ID,
        "supply_shortage",
        "region",
        REGION_ID,
        12,
    )
    engine.world_state["pressures"][MAIN_STREET_PRESSURE_ID] = build_pressure(
        MAIN_STREET_PRESSURE_ID,
        "watch_rotation",
        "location",
        MAIN_STREET_LOCATION_ID,
        0,
    )

    region_result = engine.get_applicable_pressures()
    assert list(region_result) == sorted(region_result)
    assert region_result == {
        EXTRA_REGION_PRESSURE_ID: build_pressure(
            EXTRA_REGION_PRESSURE_ID,
            "supply_shortage",
            "region",
            REGION_ID,
            12,
        ),
        GATE_PRESSURE_ID: build_pressure(
            GATE_PRESSURE_ID,
            "guard_attention",
            "location",
            GATE_LOCATION_ID,
            10,
        ),
        WINTER_PRESSURE_ID: build_pressure(
            WINTER_PRESSURE_ID,
            "winter",
            "region",
            REGION_ID,
            65,
        ),
    }

    gate_result = engine.get_applicable_pressures(GATE_LOCATION_ID)
    assert gate_result == {
        EXTRA_REGION_PRESSURE_ID: build_pressure(
            EXTRA_REGION_PRESSURE_ID,
            "supply_shortage",
            "region",
            REGION_ID,
            12,
        ),
        GATE_PRESSURE_ID: build_pressure(
            GATE_PRESSURE_ID,
            "guard_attention",
            "location",
            GATE_LOCATION_ID,
            10,
        ),
        WINTER_PRESSURE_ID: build_pressure(
            WINTER_PRESSURE_ID,
            "winter",
            "region",
            REGION_ID,
            65,
        ),
    }
    assert MAIN_STREET_PRESSURE_ID not in gate_result

    main_street_result = engine.get_applicable_pressures(MAIN_STREET_LOCATION_ID)
    assert main_street_result == {
        EXTRA_REGION_PRESSURE_ID: build_pressure(
            EXTRA_REGION_PRESSURE_ID,
            "supply_shortage",
            "region",
            REGION_ID,
            12,
        ),
        MAIN_STREET_PRESSURE_ID: build_pressure(
            MAIN_STREET_PRESSURE_ID,
            "watch_rotation",
            "location",
            MAIN_STREET_LOCATION_ID,
            0,
        ),
        WINTER_PRESSURE_ID: build_pressure(
            WINTER_PRESSURE_ID,
            "winter",
            "region",
            REGION_ID,
            65,
        ),
    }


def test_omitted_location_tracks_current_location() -> None:
    engine = build_engine()
    engine.world_state["pressures"][MAIN_STREET_PRESSURE_ID] = build_pressure(
        MAIN_STREET_PRESSURE_ID,
        "watch_rotation",
        "location",
        MAIN_STREET_LOCATION_ID,
        0,
    )

    starting_result = engine.get_applicable_pressures()
    assert MAIN_STREET_PRESSURE_ID not in starting_result

    engine.process_command("go south")
    moved_result = engine.get_applicable_pressures()
    assert MAIN_STREET_PRESSURE_ID in moved_result
    assert GATE_PRESSURE_ID not in moved_result
    assert engine.get_world_state()["player"]["current_location_id"] == MAIN_STREET_LOCATION_ID


def test_copy_safety_and_fail_closed_reads() -> None:
    engine = build_engine()
    engine.world_state["pressures"][MAIN_STREET_PRESSURE_ID] = build_pressure(
        MAIN_STREET_PRESSURE_ID,
        "watch_rotation",
        "location",
        MAIN_STREET_LOCATION_ID,
        0,
    )

    scene_before = engine.get_scene_snapshot()
    world_before = engine.get_world_state()
    result = engine.get_applicable_pressures(GATE_LOCATION_ID)
    result[GATE_PRESSURE_ID]["level"] = 99
    result[WINTER_PRESSURE_ID]["provenance"]["source_id"] = "changed"
    assert engine.get_world_state() == world_before
    assert engine.get_scene_snapshot() == scene_before

    before_identity = engine.scene_snapshot
    before_world = engine.get_world_state()
    try:
        engine.get_applicable_pressures(123)  # type: ignore[arg-type]
    except ValueError as error:
        assert "non-empty string" in str(error)
    else:
        raise AssertionError("Non-string location_id was accepted.")
    assert engine.get_world_state() == before_world
    assert engine.scene_snapshot is before_identity

    for bad_location in ("", "missing_location"):
        try:
            engine.get_applicable_pressures(bad_location)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Invalid location was accepted: {bad_location!r}")
        assert engine.get_world_state() == before_world
        assert engine.scene_snapshot is before_identity

    engine.world_state["pressures"]["broken"] = "not a pressure"
    corrupted_world_before_failure = deepcopy(engine.world_state)
    try:
        engine.get_applicable_pressures(GATE_LOCATION_ID)
    except ValueError as error:
        assert "Pressure record must be a dictionary" in str(error)
    else:
        raise AssertionError("Malformed pressure state was accepted.")
    assert engine.world_state == corrupted_world_before_failure
    assert engine.scene_snapshot is before_identity

    injected_engine = build_engine()
    injected_world_before_failure = deepcopy(injected_engine.world_state)
    injected_scene_before_failure = injected_engine.scene_snapshot

    import engine.pressure_state as pressure_state_module

    original_validate_pressure_state = pressure_state_module.validate_pressure_state
    try:
        def boom_validate_pressure_state(*args, **kwargs):
            raise ValueError("pressure validation failure")

        pressure_state_module.validate_pressure_state = boom_validate_pressure_state
        try:
            injected_engine.get_applicable_pressures(GATE_LOCATION_ID)
        except ValueError as error:
            assert "pressure validation failure" in str(error)
        else:
            raise AssertionError("Injected validation failure was swallowed.")
    finally:
        pressure_state_module.validate_pressure_state = original_validate_pressure_state

    assert injected_engine.world_state == injected_world_before_failure
    assert injected_engine.scene_snapshot is injected_scene_before_failure


def test_save_load_preserves_applicability_results() -> None:
    engine = build_engine()
    engine.world_state["pressures"][MAIN_STREET_PRESSURE_ID] = build_pressure(
        MAIN_STREET_PRESSURE_ID,
        "watch_rotation",
        "location",
        MAIN_STREET_LOCATION_ID,
        0,
    )

    expected_gate = engine.get_applicable_pressures(GATE_LOCATION_ID)
    expected_main_street = engine.get_applicable_pressures(MAIN_STREET_LOCATION_ID)

    with TemporaryDirectory() as temp_dir:
        save_path = Path(temp_dir) / "applicability_save.json"
        save_game(engine, str(save_path))
        loaded_engine = load_game(str(save_path))

        assert loaded_engine.get_applicable_pressures(GATE_LOCATION_ID) == expected_gate
        assert loaded_engine.get_applicable_pressures(MAIN_STREET_LOCATION_ID) == expected_main_street
        assert loaded_engine.get_world_state()["pressures"] == engine.get_world_state()["pressures"]


def test_helper_matches_engine_facade() -> None:
    engine = build_engine()
    app_pressures = engine.get_applicable_pressures(GATE_LOCATION_ID)
    helper_pressures = get_applicable_pressures(
        engine.get_world_state()["pressures"],
        engine.region,
        GATE_LOCATION_ID,
    )
    assert app_pressures == helper_pressures


def main() -> None:
    test_region_and_location_applicability()
    test_omitted_location_tracks_current_location()
    test_copy_safety_and_fail_closed_reads()
    test_save_load_preserves_applicability_results()
    test_helper_matches_engine_facade()
    print("Pressure applicability tests passed.")


if __name__ == "__main__":
    main()
