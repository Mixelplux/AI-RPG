from copy import deepcopy

from engine.game_engine import GameEngine
from engine.interaction_kernel import process_player_input


REGION_PATH = "data/regions/bryn_shander.json"


def test_move_to_named_immediate_route_matches_directional_movement():
    directional_engine = GameEngine(REGION_PATH)
    named_engine = GameEngine(REGION_PATH)

    directional = directional_engine.process_command("go south")
    named = named_engine.process_command("move to Main Street")

    assert directional["success"]
    assert named["success"]
    assert named["destination_location_id"] == directional["destination_location_id"]
    assert named["message"] == directional["message"]
    assert named_engine.get_world_state()["player"]["current_location_id"] == (
        directional_engine.get_world_state()["player"]["current_location_id"]
    )
    assert named_engine.get_history()[-1]["event_type"] == "player_movement"


def test_named_routes_are_current_scene_only_and_fail_closed():
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_history = engine.get_history()

    result = engine.process_command("move to Western Trade Road")

    assert not result["success"]
    assert engine.get_world_state() == before_state
    assert engine.get_history() == before_history


def test_ambiguous_immediate_names_do_not_resolve_or_mutate_scene():
    scene = {
        "location": {
            "connected_locations": [
                {"direction": "north", "location_id": "first"},
                {"direction": "south", "location_id": "second"},
            ]
        }
    }
    locations = [
        {"location_id": "first", "name": "Market"},
        {"location_id": "second", "name": "Market"},
    ]
    before_scene = deepcopy(scene)

    result = process_player_input("move to Market", scene, locations)

    assert not result["success"]
    assert "destination_location_id" not in result
    assert scene == before_scene


def test_go_to_stays_nonmoving_destination_lookup():
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_history = engine.get_history()

    result = engine.process_command("go to Main Street")

    assert result["intent"] == "destination"
    assert result["success"]
    assert result["destination_resolution"]["location_id"] == "bryn_shander_main_street"
    assert engine.get_world_state() == before_state
    assert engine.get_history() == before_history


def main():
    test_move_to_named_immediate_route_matches_directional_movement()
    test_named_routes_are_current_scene_only_and_fail_closed()
    test_ambiguous_immediate_names_do_not_resolve_or_mutate_scene()
    test_go_to_stays_nonmoving_destination_lookup()
    print("Interaction-kernel local route command tests passed.")


if __name__ == "__main__":
    main()
