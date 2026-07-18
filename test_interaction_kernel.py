from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.interaction_kernel import process_player_input
from engine.save_system import SAVE_VERSION, load_game, save_game
from engine.scene_loader import build_scene


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

    result = engine.process_command("move to Nowhere")

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


def test_two_hop_go_to_and_move_to_compose_existing_movement_hops():
    go_to_engine = GameEngine(REGION_PATH)
    move_to_engine = GameEngine(REGION_PATH)

    go_to = go_to_engine.process_command("go to Traders' Hall")
    move_to = move_to_engine.process_command("move to the Inn of the Four Candles")

    for result, engine, destination in (
        (go_to, go_to_engine, "traders_hall"),
        (move_to, move_to_engine, "inn_four_candles"),
    ):
        assert result["success"]
        assert result["intent"] == "movement"
        assert result["destination_location_id"] == destination
        assert result["message"] in {
            "You move south. You move east.",
            "You move south. You move west.",
        }
        assert engine.get_world_state()["player"]["current_location_id"] == destination
        history = engine.get_history()
        assert [entry["event_type"] for entry in history[-2:]] == [
            "player_movement",
            "player_movement",
        ]


def test_missing_two_hop_routes_fail_without_movement():
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_history = engine.get_history()

    for command in ("go to Nowhere", "move to Nowhere"):
        result = engine.process_command(command)

        assert result["intent"] == "movement"
        assert not result["success"]
    assert engine.get_world_state() == before_state
    assert engine.get_history() == before_history


def test_head_to_preserves_nonmoving_destination_lookup():
    engine = GameEngine(REGION_PATH)
    before_state = engine.get_world_state()
    before_history = engine.get_history()

    result = engine.process_command("head to the Western Trade Road")

    assert result["intent"] == "destination"
    assert result["success"]
    assert result["destination_resolution"]["location_id"] == "outside_trade_road_west"
    assert engine.get_world_state() == before_state
    assert engine.get_history() == before_history


def test_ambiguous_two_hop_routes_fail_without_movement():
    engine = GameEngine(REGION_PATH)
    north_gate = next(
        location
        for location in engine.region["locations"]
        if location["location_id"] == "bryn_shander_gate_north"
    )
    west_gate = next(
        location
        for location in engine.region["locations"]
        if location["location_id"] == "bryn_shander_gate_west"
    )
    north_gate["connected_locations"].append(
        {"direction": "west", "location_id": "bryn_shander_gate_west"}
    )
    west_gate["connected_locations"].append(
        {"direction": "north", "location_id": "traders_hall"}
    )
    engine.scene_snapshot = build_scene(engine.region, engine.world_state)
    before_state = engine.get_world_state()
    before_history = engine.get_history()

    result = engine.process_command("go to Traders' Hall")

    assert result["intent"] == "movement"
    assert not result["success"]
    assert "ambiguous" in result["message"]
    assert engine.get_world_state() == before_state
    assert engine.get_history() == before_history


def test_two_hop_resolution_is_bounded_and_prevalidates_both_hops():
    scene = {
        "location": {
            "connected_locations": [{"direction": "east", "location_id": "b"}]
        }
    }
    locations = [
        {"location_id": "a", "name": "A", "connected_locations": []},
        {
            "location_id": "b",
            "name": "B",
            "connected_locations": [
                {"direction": "north", "location_id": "c"},
                {"direction": "west", "location_id": "a"},
            ],
        },
        {"location_id": "c", "name": "C", "connected_locations": []},
        {
            "location_id": "unrelated",
            "name": "Unrelated",
            "connected_locations": [{"direction": "north", "location_id": "c"}],
        },
    ]
    before_scene, before_locations = deepcopy(scene), deepcopy(locations)

    result = process_player_input("move to C", scene, locations)

    assert result["success"]
    assert result["destination_location_id"] == "c"
    assert len(result["movement_hops"]) == 2
    assert scene == before_scene
    assert locations == before_locations

    locations[1]["connected_locations"][0] = {"location_id": "c"}
    invalid_result = process_player_input("go to C", scene, locations)

    assert not invalid_result["success"]
    assert "movement_hops" not in invalid_result


def test_two_hop_save_load_and_existing_timed_hop_semantics():
    engine = GameEngine(REGION_PATH, entry_location_id="traders_hall")

    result = engine.process_command("move to Western Trade Road")

    assert result["success"]
    assert result["destination_location_id"] == "outside_trade_road_west"
    assert len(result["movement_hops"]) == 2
    assert len(result["time_advancements"]) == 1
    assert engine.get_world_state()["time"]["elapsed_hours"] == 1
    assert engine.get_world_state()["player"]["current_location_id"] == (
        "outside_trade_road_west"
    )

    with TemporaryDirectory() as directory:
        save_path = Path(directory) / "two-hop-save.json"
        save_game(engine, str(save_path))
        loaded = load_game(str(save_path))

    assert SAVE_VERSION == 1
    assert loaded.get_world_state() == engine.get_world_state()


def test_three_hop_go_to_and_move_to_validate_then_compose_hops():
    go_engine = GameEngine(REGION_PATH, entry_location_id="inn_four_candles")
    move_engine = GameEngine(REGION_PATH, entry_location_id="inn_four_candles")

    for command, engine in (("go to West Gate", go_engine), ("move to West Gate", move_engine)):
        before_history = engine.get_history()
        result = engine.process_command(command)
        assert result["success"]
        assert result["destination_location_id"] == "bryn_shander_gate_west"
        assert len(result["movement_hops"]) == 3
        assert engine.get_world_state()["player"]["current_location_id"] == "bryn_shander_gate_west"
        assert len(engine.get_history()) == len(before_history) + 3

    with TemporaryDirectory() as directory:
        save_path = Path(directory) / "three-hop-save.json"
        save_game(go_engine, str(save_path))
        loaded = load_game(str(save_path))
    assert SAVE_VERSION == 1
    assert loaded.get_world_state() == go_engine.get_world_state()
    assert "movement_hops" not in loaded.get_world_state()


def test_three_hop_ambiguity_and_invalid_final_hop_fail_without_mutation():
    scene = {"location": {"connected_locations": [
        {"direction": "east", "location_id": "b1"},
        {"direction": "west", "location_id": "b2"},
    ]}}
    locations = [
        {"location_id": "b1", "name": "B1", "connected_locations": [{"direction": "north", "location_id": "c1"}]},
        {"location_id": "b2", "name": "B2", "connected_locations": [{"direction": "south", "location_id": "c2"}]},
        {"location_id": "c1", "name": "C1", "connected_locations": [{"direction": "east", "location_id": "d"}, {"direction": "west", "location_id": "b1"}]},
        {"location_id": "c2", "name": "C2", "connected_locations": [{"direction": "east", "location_id": "d"}]},
        {"location_id": "d", "name": "D", "connected_locations": []},
        {"location_id": "unrelated", "name": "Unrelated", "connected_locations": [{"direction": "north", "location_id": "d"}]},
    ]
    before_scene, before_locations = deepcopy(scene), deepcopy(locations)
    ambiguous = process_player_input("go to D", scene, locations)
    assert not ambiguous["success"]
    assert "ambiguous" in ambiguous["message"]
    assert scene == before_scene and locations == before_locations

    locations[2]["connected_locations"][0] = {"location_id": "d"}
    locations[1]["connected_locations"] = []
    invalid = process_player_input("move to D", scene, locations)
    assert not invalid["success"]
    assert "movement_hops" not in invalid


def test_hop_agnostic_resolver_handles_long_routes_and_cycles():
    for hop_count in (5, 10):
        locations = []
        for index in range(hop_count + 1):
            location_id = f"node_{index}"
            connections = [] if index == hop_count else [{"direction": f"d{index}", "location_id": f"node_{index + 1}"}]
            if index > 0:
                connections.append({"direction": f"back{index}", "location_id": f"node_{index - 1}"})
            locations.append({"location_id": location_id, "name": "Destination" if index == hop_count else f"Node {index}", "connected_locations": connections})
        scene = {"location": locations[0]}
        before_scene, before_locations = deepcopy(scene), deepcopy(locations)
        result = process_player_input("go to Destination", scene, locations)
        assert result["success"]
        assert len(result["movement_hops"]) == hop_count
        assert result["destination_location_id"] == f"node_{hop_count}"
        visited_location_ids = ["node_0"] + [
            hop["destination_location_id"] for hop in result["movement_hops"]
        ]
        assert len(visited_location_ids) == len(set(visited_location_ids))
        assert scene == before_scene and locations == before_locations


def test_hop_agnostic_resolver_respects_authored_directionality():
    locations = [
        {"location_id": "a", "name": "A", "connected_locations": [
            {"direction": "east", "location_id": "b"},
        ]},
        {"location_id": "b", "name": "B", "connected_locations": [
            {"direction": "east", "location_id": "c"},
        ]},
        {"location_id": "c", "name": "C", "connected_locations": []},
    ]

    forward = process_player_input(
        "go to C", {"location": locations[0]}, locations
    )
    reverse = process_player_input(
        "go to A", {"location": locations[2]}, locations
    )

    assert forward["success"]
    assert [hop["destination_location_id"] for hop in forward["movement_hops"]] == [
        "b", "c",
    ]
    assert not reverse["success"]
    assert "movement_hops" not in reverse


def test_long_route_publishes_each_hop_and_preserves_timed_intermediate_arrival():
    engine = GameEngine(REGION_PATH)
    road = next(
        location
        for location in engine.region["locations"]
        if location["location_id"] == "outside_trade_road_west"
    )
    road["connected_locations"].append({
        "direction": "west",
        "location_id": "sequential_route_destination",
    })
    engine.region["locations"].append({
        "location_id": "sequential_route_destination",
        "name": "Sequential Route Destination",
        "type": "test_route",
        "description_seed": "A test-only authored continuation beyond the Western Trade Road.",
        "state": {},
        "spawn_rules": {},
        "connected_locations": [],
    })
    engine.scene_snapshot = build_scene(engine.region, engine.world_state)

    result = engine.process_command("go to Sequential Route Destination")

    assert result["success"]
    assert len(result["movement_hops"]) == 5
    assert result["destination_location_id"] == "sequential_route_destination"
    assert engine.get_world_state()["player"]["current_location_id"] == (
        "sequential_route_destination"
    )
    movement_history = [
        entry for entry in engine.get_history()
        if entry["event_type"] == "player_movement"
    ]
    assert [entry["location"] for entry in movement_history] == [
        "bryn_shander_main_street",
        "traders_hall",
        "bryn_shander_gate_west",
        "outside_trade_road_west",
        "sequential_route_destination",
    ]
    assert len(result["time_advancements"]) == 1
    assert engine.get_world_state()["time"]["elapsed_hours"] == 1
    assert engine.get_world_state()["evidence_traces"] == [{
        "trace_id": "western_trade_road_arrival_trace",
        "evidence_id": "western_trade_road_patrol_marker",
        "location_id": "outside_trade_road_west",
    }]

    assert "movement_hops" not in engine.get_world_state()


def test_later_route_hop_failure_preserves_earlier_authoritative_hop():
    engine = GameEngine(REGION_PATH)
    original_complete_hop = engine._complete_movement_hop
    completed_hop_count = 0

    def fail_before_second_hop(hop):
        nonlocal completed_hop_count
        completed_hop_count += 1
        if completed_hop_count == 2:
            raise RuntimeError("test-only later-hop failure")
        return original_complete_hop(hop)

    engine._complete_movement_hop = fail_before_second_hop

    try:
        engine.process_command("go to Western Trade Road")
        assert False, "Expected the injected later-hop failure."
    except RuntimeError as error:
        assert str(error) == "test-only later-hop failure"

    assert engine.get_world_state()["player"]["current_location_id"] == (
        "bryn_shander_main_street"
    )
    movement_history = [
        entry for entry in engine.get_history()
        if entry["event_type"] == "player_movement"
    ]
    assert [entry["location"] for entry in movement_history] == [
        "bryn_shander_main_street"
    ]


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
    test_two_hop_go_to_and_move_to_compose_existing_movement_hops()
    test_missing_two_hop_routes_fail_without_movement()
    test_head_to_preserves_nonmoving_destination_lookup()
    test_ambiguous_two_hop_routes_fail_without_movement()
    test_two_hop_resolution_is_bounded_and_prevalidates_both_hops()
    test_two_hop_save_load_and_existing_timed_hop_semantics()
    test_three_hop_go_to_and_move_to_validate_then_compose_hops()
    test_three_hop_ambiguity_and_invalid_final_hop_fail_without_mutation()
    test_hop_agnostic_resolver_handles_long_routes_and_cycles()
    test_hop_agnostic_resolver_respects_authored_directionality()
    test_long_route_publishes_each_hop_and_preserves_timed_intermediate_arrival()
    test_later_route_hop_failure_preserves_earlier_authoritative_hop()
    test_ambiguous_and_invalid_destination_phrases_fail_closed()
    print("Interaction-kernel local route command tests passed.")


if __name__ == "__main__":
    main()
