from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.navigation_projection import derive_navigation_projection
from engine.save_system import SAVE_VERSION, load_game, save_game


REGION_PATH = "data/regions/bryn_shander.json"


def test_direct_routes_are_player_facing_and_deterministic():
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_history = engine.get_history()
    before_scene = engine.get_scene_snapshot()

    first = engine.get_player_perception()
    second = engine.get_player_perception()

    expected_routes = [
        {"direction": "north", "destination_name": "Northern Tundra Route"},
        {"direction": "south", "destination_name": "Main Street"},
    ]
    assert first["navigation"] == {"routes": expected_routes}
    assert second == first
    assert engine.get_world_state() == before_state
    assert engine.get_history() == before_history
    assert engine.get_scene_snapshot() == before_scene

    narration = engine.get_narration()
    assert narration["navigation"] == expected_routes
    assert "Northern Tundra Route lies north." in narration["description"]
    assert "Main Street lies south." in narration["description"]
    assert "outside_tundra_route_north" not in narration["description"]
    assert "bryn_shander_main_street" not in narration["description"]


def test_non_adjacent_or_ineligible_geography_is_not_projected():
    scene = {
        "location": {"location_id": "gate"},
        "exits": [
            {"direction": "north", "location_id": "road"},
            {"direction": "north", "location_id": "missing"},
            {"direction": "secret", "location_id": "hidden"},
            {"direction": "south", "location_id": "gate"},
            {"direction": "south", "location_id": "road"},
        ],
    }
    locations = [
        {"location_id": "gate", "name": "North Gate"},
        {"location_id": "road", "name": "Main Street"},
        {"location_id": "hidden", "name": "Hidden Vault"},
        {"location_id": "distant", "name": "Distant Keep"},
    ]
    before_scene, before_locations = deepcopy(scene), deepcopy(locations)

    projection = derive_navigation_projection(scene, locations)

    assert projection == {
        "routes": [{"direction": "north", "destination_name": "Main Street"}]
    }
    assert scene == before_scene
    assert locations == before_locations
    assert "Hidden Vault" not in str(projection)
    assert "Distant Keep" not in str(projection)
    assert "road" not in str(projection)


def test_movement_and_save_load_remain_compatible():
    engine = GameEngine(REGION_PATH)
    result = engine.process_command("go south")
    assert result["success"]
    assert engine.get_world_state()["player"]["current_location_id"] == (
        "bryn_shander_main_street"
    )
    assert engine.get_history()[-1]["event_type"] == "player_movement"
    assert engine.get_player_perception()["navigation"]["routes"] == [
        {"direction": "north", "destination_name": "North Gate"},
        {"direction": "east", "destination_name": "Traders' Hall"},
        {"direction": "west", "destination_name": "The Inn of the Four Candles"},
    ]

    with TemporaryDirectory() as directory:
        path = Path(directory) / "navigation-save.json"
        save_game(engine, str(path))
        loaded = load_game(str(path))

    assert SAVE_VERSION == 1
    assert loaded.get_world_state() == engine.get_world_state()
    assert loaded.get_player_perception()["navigation"] == (
        engine.get_player_perception()["navigation"]
    )


def main():
    test_direct_routes_are_player_facing_and_deterministic()
    test_non_adjacent_or_ineligible_geography_is_not_projected()
    test_movement_and_save_load_remain_compatible()
    print("Navigation projection tests passed.")


if __name__ == "__main__":
    main()
