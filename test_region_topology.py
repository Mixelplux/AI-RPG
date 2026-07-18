from copy import deepcopy

from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.scene_loader import load_region


REGION_PATH = "data/regions/bryn_shander.json"


def expect_invalid(region, expected_text):
    try:
        validate_region(region)
    except ValueError as error:
        assert expected_text in str(error)
        return
    raise AssertionError("Expected region topology validation to fail.")


def test_representative_topology_is_reciprocal_and_reachable():
    region = load_region(REGION_PATH)
    validate_region(region)

    locations = {location["location_id"]: location for location in region["locations"]}
    expected_anchors = {
        "bryn_shander_gate_north",
        "market_square",
        "bryn_shander_gate_east",
        "bryn_shander_gate_west",
        "inn_four_candles",
        "blackiron_blades",
        "traders_hall",
        "house_of_the_triad",
        "council_hall",
        "town_hall",
        "speakers_palace",
    }
    assert expected_anchors <= set(locations)
    assert locations["bryn_shander_gate_west"]["name"] == "Southwest Gate"

    for source_id, location in locations.items():
        destinations = [connection["location_id"] for connection in location["connected_locations"]]
        assert source_id not in destinations
        assert len(destinations) == len(set(destinations))
        for destination_id in destinations:
            reverse_destinations = {
                connection["location_id"]
                for connection in locations[destination_id]["connected_locations"]
            }
            assert source_id in reverse_destinations


def test_topology_validator_rejects_unpaired_duplicate_self_and_unreachable_edges():
    region = load_region(REGION_PATH)

    missing_reverse = deepcopy(region)
    north_gate = next(
        location for location in missing_reverse["locations"]
        if location["location_id"] == "bryn_shander_gate_north"
    )
    north_gate["connected_locations"] = [
        connection for connection in north_gate["connected_locations"]
        if connection["location_id"] != "outside_tundra_route_north"
    ]
    expect_invalid(missing_reverse, "lacks an explicitly authored reciprocal connection")

    duplicate = deepcopy(region)
    duplicate["locations"][0]["connected_locations"].append(
        {"direction": "south", "location_id": "bryn_shander_main_street"}
    )
    expect_invalid(duplicate, "duplicate connection target")

    self_link = deepcopy(region)
    self_link["locations"][0]["connected_locations"].append(
        {"direction": "inside", "location_id": "bryn_shander_gate_north"}
    )
    expect_invalid(self_link, "unintended self-link")

    unreachable = deepcopy(region)
    unreachable["locations"].append({
        "location_id": "isolated_test_location",
        "connected_locations": [],
    })
    expect_invalid(unreachable, "Locations unreachable from entry_location")


def test_representative_routes_choose_authored_equal_hop_order_and_cross_town_path():
    market_engine = GameEngine(REGION_PATH)
    market_route = market_engine.process_command("go to Market Square")

    assert market_route["success"]
    assert [hop["destination_location_id"] for hop in market_route["movement_hops"]] == [
        "bryn_shander_main_street",
        "inn_four_candles",
        "market_square",
    ]

    civic_engine = GameEngine(REGION_PATH)
    civic_route = civic_engine.process_command("go to Speaker's Palace")

    assert civic_route["success"]
    assert [hop["destination_location_id"] for hop in civic_route["movement_hops"]] == [
        "bryn_shander_main_street",
        "inn_four_candles",
        "market_square",
        "town_hall",
        "speakers_palace",
    ]


def main():
    test_representative_topology_is_reciprocal_and_reachable()
    test_topology_validator_rejects_unpaired_duplicate_self_and_unreachable_edges()
    test_representative_routes_choose_authored_equal_hop_order_and_cross_town_path()
    print("Representative Bryn Shander topology tests passed.")


if __name__ == "__main__":
    main()
