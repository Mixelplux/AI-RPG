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


def test_immediate_go_to_and_head_to_match_directional_movement():
    directional_engine = GameEngine(REGION_PATH)
    go_to_engine = GameEngine(REGION_PATH)
    head_to_engine = GameEngine(REGION_PATH)

    directional = directional_engine.process_command("go south")
    go_to = go_to_engine.process_command("go to Main Street")
    head_to = head_to_engine.process_command("head to Main Street")

    for result, engine in ((go_to, go_to_engine), (head_to, head_to_engine)):
        assert result["success"]
        assert result["intent"] == "movement"
        assert result["destination_location_id"] == directional["destination_location_id"]
        assert result["message"] == directional["message"]
        assert engine.get_world_state()["player"]["current_location_id"] == (
            directional_engine.get_world_state()["player"]["current_location_id"]
        )


def test_article_bearing_immediate_destination_phrase_matches_local_movement():
    directional_engine = GameEngine(REGION_PATH)
    article_engine = GameEngine(REGION_PATH)
    directional_engine.process_command("go south")
    article_engine.process_command("go south")

    directional = directional_engine.process_command("go west")
    article = article_engine.process_command("head to the Inn of the Four Candles")

    assert article["success"]
    assert article["intent"] == "movement"
    assert article["destination_location_id"] == directional["destination_location_id"]
    assert article["message"] == directional["message"]
    assert article_engine.get_world_state()["player"]["current_location_id"] == (
        directional_engine.get_world_state()["player"]["current_location_id"]
    )


def test_non_adjacent_go_to_and_head_to_stay_nonmoving_destination_lookup():
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_history = engine.get_history()

    for command in ("go to Western Trade Road", "head to Western Trade Road"):
        result = engine.process_command(command)

        assert result["intent"] == "destination"
        assert result["success"]
        assert result["destination_resolution"]["location_id"] == (
            "outside_trade_road_west"
        )
    assert engine.get_world_state() == before_state
    assert engine.get_history() == before_history


def test_article_bearing_non_adjacent_phrase_stays_nonmoving_destination_lookup():
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_history = engine.get_history()

    result = engine.process_command("go to the Western Trade Road")

    assert result["intent"] == "destination"
    assert result["success"]
    assert result["destination_resolution"]["location_id"] == "outside_trade_road_west"
    assert engine.get_world_state() == before_state
    assert engine.get_history() == before_history


def test_ambiguous_and_invalid_destination_phrases_fail_closed():
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

    ambiguous = process_player_input("go to Market", scene, locations)
    invalid_engine = GameEngine(REGION_PATH)
    before_state = invalid_engine.get_world_state()
    invalid = invalid_engine.process_command("head to Nowhere")

    assert not ambiguous["success"]
    assert ambiguous["intent"] == "destination"
    assert "destination_location_id" not in ambiguous
    assert scene == before_scene
    assert not invalid["success"]
    assert invalid_engine.get_world_state() == before_state


def main():
    test_move_to_named_immediate_route_matches_directional_movement()
    test_named_routes_are_current_scene_only_and_fail_closed()
    test_ambiguous_immediate_names_do_not_resolve_or_mutate_scene()
    test_immediate_go_to_and_head_to_match_directional_movement()
    test_article_bearing_immediate_destination_phrase_matches_local_movement()
    test_non_adjacent_go_to_and_head_to_stay_nonmoving_destination_lookup()
    test_article_bearing_non_adjacent_phrase_stays_nonmoving_destination_lookup()
    test_ambiguous_and_invalid_destination_phrases_fail_closed()
    print("Interaction-kernel local route command tests passed.")


if __name__ == "__main__":
    main()
