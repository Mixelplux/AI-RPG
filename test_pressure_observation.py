from copy import deepcopy
from pathlib import Path
from test_artifact_files import artifact_files

from engine.game_engine import GameEngine
from engine.pressure_observation import derive_pressure_observation
from engine.region_validator import validate_region
from engine.save_system import load_game


PATH = "test_fixtures/bryn_shander_legacy.json"
CUE = {"cue_id": "winter_deepens_observation", "pressure_id": "bryn_shander_winter", "text": "The cold has become noticeably more severe."}


def main():
    engine = GameEngine(PATH)
    before = engine.get_world_state(); scene = engine.scene_snapshot; region = deepcopy(engine.region)
    assert engine.get_player_perception()["pressure_cues"] == []
    engine.process_command("wait")
    perception = engine.get_player_perception()
    assert perception["pressure_cues"] == [CUE]
    assert "level" not in str(perception["pressure_cues"])
    mutable = perception["pressure_cues"]; mutable[0]["text"] = "changed"
    assert engine.get_player_perception()["pressure_cues"] == [CUE]
    assert engine.scene_snapshot is not scene
    current_scene = engine.scene_snapshot
    engine.set_pressure_level("bryn_shander_winter", 69)
    assert engine.get_player_perception()["pressure_cues"] == []
    assert engine.scene_snapshot is current_scene
    engine.set_pressure_level("bryn_shander_winter", 71)
    assert engine.get_player_perception()["pressure_cues"] == [CUE]
    assert engine.region == region

    declaration = deepcopy(engine.region["pressure_observation_cue"])
    declaration["minimum_level"] = 0
    pressures = engine.get_applicable_pressures()
    pressures["bryn_shander_winter"]["level"] = 0
    assert derive_pressure_observation(pressures, declaration) == CUE
    assert derive_pressure_observation(pressures, None) is None

    for field, value in (("cue_id", ""), ("pressure_id", "unknown"), ("text", ""), ("minimum_level", True), ("minimum_level", -1), ("minimum_level", 101)):
        bad = deepcopy(engine.region); bad["pressure_observation_cue"][field] = value
        try: validate_region(bad)
        except ValueError: pass
        else: raise AssertionError(field)
    bad = deepcopy(engine.region); del bad["pressure_observation_cue"]["text"]
    try: validate_region(bad)
    except ValueError: pass
    else: raise AssertionError("missing")
    bad = deepcopy(engine.region); bad["pressure_observation_cue"]["extra"] = 1
    try: validate_region(bad)
    except ValueError: pass
    else: raise AssertionError("extra")

    with artifact_files("test_pressure_observation") as td:
        save = str(Path(td) / "test_pressure_observation_save.json"); engine.save(save); loaded = load_game(save)
        assert loaded.get_player_perception()["pressure_cues"] == [CUE]
        assert "pressure_observation_cue" not in loaded.get_world_state()
    assert before["history"] == []
    print("Pressure observation tests passed.")


if __name__ == "__main__": main()
