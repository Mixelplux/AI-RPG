import json
from copy import deepcopy
from pathlib import Path

from engine.region_validator import validate_region
from engine.game_engine import GameEngine


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


if __name__ == "__main__":
    test_discovery_declarations()
    test_atomic_local_discovery_and_no_op()
    print("Discovery declaration tests passed.")
