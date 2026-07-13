import json
from copy import deepcopy
from pathlib import Path

from engine.region_validator import validate_region
from engine.game_engine import GameEngine
from engine.save_system import build_save_data, load_game
from tempfile import TemporaryDirectory


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


if __name__ == "__main__":
    test_discovery_declarations()
    test_atomic_local_discovery_and_no_op()
    test_wrong_location_and_unknown_save_membership_fail_closed()
    print("Discovery declaration tests passed.")
