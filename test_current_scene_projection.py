from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from engine.current_scene_projection import build_current_scene_projection
from engine.game_engine import GameEngine
from engine.navigation_projection import derive_navigation_projection
from engine.save_system import SAVE_VERSION, build_save_data, load_game


REGION_PATH = "data/regions/bryn_shander.json"
CAPTAIN = "captain_darvin_grey"
ELIN = "guard_elin_voss"
MAIN_STREET = "bryn_shander_main_street"


INITIAL_PROJECTION = {
    "schema": "ai_rpg.current_scene_projection",
    "version": 1,
    "location": {
        "name": "North Gate",
        "description": (
            "The northern gate opens onto the wind-lashed approach and the "
            "town's central thoroughfare."
        ),
    },
    "entities": {
        "actors": [
            {"display_name": "Captain Darvin Grey"},
            {"display_name": "Elin Voss"},
        ],
        "groups": [],
    },
    "exits": [
        {"orientation": "north", "destination_name": "Northern Gate Approach"},
        {"orientation": "south", "destination_name": "Main Street"},
    ],
}


def test_exact_initial_projection_is_deterministic_and_copy_safe():
    engine = GameEngine(REGION_PATH)
    before_world = engine.get_world_state()
    before_history = engine.get_history()
    before_scene = engine.get_scene_snapshot()

    first = engine.get_current_scene_projection()
    second = engine.get_current_scene_projection()
    assert first == INITIAL_PROJECTION
    assert second == first
    assert engine.get_world_state() == before_world
    assert engine.get_history() == before_history
    assert engine.get_scene_snapshot() == before_scene

    first["location"]["name"] = "Changed"
    first["entities"]["actors"][0]["display_name"] = "Changed"
    first["exits"].append({"orientation": "west", "destination_name": "Changed"})
    assert engine.get_current_scene_projection() == INITIAL_PROJECTION


def test_actor_relocation_and_player_movement_rebuild_projection():
    engine = GameEngine(REGION_PATH)
    assert engine.set_actor_location(CAPTAIN, MAIN_STREET)["changed"]
    assert engine.get_current_scene_projection()["entities"]["actors"] == [
        {"display_name": "Elin Voss"}
    ]

    destination_engine = GameEngine(REGION_PATH, entry_location_id=MAIN_STREET)
    assert destination_engine.set_actor_location(CAPTAIN, MAIN_STREET)["changed"]
    assert destination_engine.get_current_scene_projection()["entities"]["actors"] == [
        {"display_name": "Captain Darvin Grey"}
    ]

    assert engine.process_command("go south")["success"]
    moved = engine.get_current_scene_projection()
    assert moved["location"]["name"] == "Main Street"
    assert moved["exits"] == [
        {"orientation": "north", "destination_name": "North Gate"},
    ]


def test_player_facing_weather_keeps_type_and_redacts_internal_severity():
    engine = GameEngine(REGION_PATH)

    narration = engine.get_narration()
    description = narration["description"]
    assert "The weather is blizzard." in description
    assert "severity" not in description
    assert "0.65" not in description

    projection = engine.get_current_scene_projection()
    assert "severity" not in json.dumps(projection, sort_keys=True)
    assert engine.get_world_state()["weather"]["severity"] == 0.65
    assert engine.get_scene_snapshot()["local_state"]["weather"]["severity"] == 0.65
    assert engine.get_player_perception()["environment"]["weather"]["severity"] == 0.65


def test_exit_filtering_order_and_navigation_remain_unchanged():
    region = {
        "locations": [
            {"location_id": "gate", "name": "North Gate"},
            {"location_id": "road", "name": "Main Street"},
            {"location_id": "vault", "name": "Hidden Vault"},
        ],
        "entities": [],
    }
    scene = {
        "location": {"location_id": "gate"},
        "entities": {"static": [], "spawned": []},
        "exits": [
            {"direction": "north", "location_id": "road"},
            {"direction": "secret", "location_id": "vault"},
            {"direction": "south", "location_id": "gate"},
            {"direction": "south", "location_id": "road"},
            {"direction": "west", "location_id": "missing"},
        ],
    }
    perception = {
        "visible": {
            "location": {"id": "gate", "name": "North Gate", "description_seed": "A gate."},
            "entities": {"static": [], "spawned": []},
        }
    }
    before_region, before_scene, before_perception = (
        deepcopy(region), deepcopy(scene), deepcopy(perception)
    )

    projection = build_current_scene_projection(region, scene, perception)
    assert projection["exits"] == [
        {"orientation": "north", "destination_name": "Main Street"}
    ]
    assert derive_navigation_projection(scene, region["locations"]) == {
        "route_cues": [{"text": "The way north leads to Main Street."}]
    }
    assert region == before_region
    assert scene == before_scene
    assert perception == before_perception


def test_hidden_internal_state_is_redacted_and_unlabeled_spawns_fail_closed():
    engine = GameEngine(REGION_PATH)
    projection = engine.get_current_scene_projection()
    rendered = json.dumps(projection, sort_keys=True)
    for internal_value in (
        "bryn_shander_gate_north",
        "outside_tundra_route_north",
        CAPTAIN,
        ELIN,
        "city_guard",
        "alertness",
        "knowledge",
        "relationships",
        "spawn_counts",
    ):
        assert internal_value not in rendered
    assert projection["entities"]["groups"] == []

    hidden_perception = engine.get_player_perception()
    hidden_perception["visible"]["entities"]["static"].remove(CAPTAIN)
    hidden = build_current_scene_projection(
        engine.region, engine.get_scene_snapshot(), hidden_perception
    )
    assert hidden["entities"]["actors"] == [{"display_name": "Elin Voss"}]

    mismatched = deepcopy(hidden_perception)
    mismatched["visible"]["location"]["id"] = "another_location"
    assert build_current_scene_projection(
        engine.region, engine.get_scene_snapshot(), mismatched
    ) == {
        "schema": "ai_rpg.current_scene_projection",
        "version": 1,
        "location": {"name": "", "description": ""},
        "entities": {"actors": [], "groups": []},
        "exits": [],
    }


def test_malformed_region_entities_are_rejected_without_raw_value_fallback():
    engine = GameEngine(REGION_PATH)
    malformed_region = deepcopy(engine.region)
    malformed_region["entities"] = {CAPTAIN: "Captain Darvin Grey"}

    try:
        build_current_scene_projection(
            malformed_region,
            engine.get_scene_snapshot(),
            engine.get_player_perception(),
        )
    except ValueError as error:
        assert "Region entities" in str(error)
    else:
        raise AssertionError("Expected malformed region entities to be rejected.")


def test_explicitly_labeled_visible_spawned_groups_are_aggregated_in_order():
    region = {
        "locations": [{"location_id": "gate", "name": "North Gate"}],
        "entities": [],
    }
    scene = {
        "location": {"location_id": "gate"},
        "exits": [],
        "entities": {
            "static": [],
            "spawned": [
                {"template": "watch_internal"},
                {"template": "merchant_internal"},
                {"template": "watch_internal"},
            ],
        },
    }
    perception = {
        "visible": {
            "location": {"id": "gate", "name": "North Gate", "description_seed": "A gate."},
            "entities": {
                "static": [],
                "spawned": [
                    {"template": "watch_internal", "display_name": "Gate Guard"},
                    {"template": "merchant_internal", "display_name": "Merchant"},
                    {"template": "watch_internal", "display_name": "Gate Guard"},
                ],
            },
        }
    }

    projection = build_current_scene_projection(region, scene, perception)
    assert projection["entities"]["groups"] == [
        {"display_name": "Gate Guard", "count": 2},
        {"display_name": "Merchant", "count": 1},
    ]
    assert "watch_internal" not in json.dumps(projection)
    assert "merchant_internal" not in json.dumps(projection)


def test_save_load_reproduces_projection_without_persisting_it():
    engine = GameEngine(REGION_PATH)
    assert engine.process_command("go south")["success"]
    expected = engine.get_current_scene_projection()
    save_data = build_save_data(engine)
    assert SAVE_VERSION == save_data["save_version"] == 1
    assert "current_scene_projection" not in save_data
    assert "current_scene_projection" not in save_data["world_state"]

    with TemporaryDirectory() as directory:
        path = Path(directory) / "current-scene.json"
        path.write_text(json.dumps(save_data), encoding="utf-8")
        loaded = load_game(str(path))

    assert loaded.get_world_state() == engine.get_world_state()
    assert loaded.get_current_scene_projection() == expected


def test_query_does_not_invoke_provider_narration_parser_or_movement():
    engine = GameEngine(REGION_PATH)
    with patch("engine.game_engine.narrate_scene", side_effect=AssertionError), patch(
        "engine.game_engine.build_narration_preview_packet", side_effect=AssertionError
    ), patch("engine.game_engine.process_player_input", side_effect=AssertionError), patch(
        "engine.game_engine.GameEngine._complete_movement_hop", side_effect=AssertionError
    ):
        assert engine.get_current_scene_projection() == INITIAL_PROJECTION


def main():
    test_exact_initial_projection_is_deterministic_and_copy_safe()
    test_actor_relocation_and_player_movement_rebuild_projection()
    test_player_facing_weather_keeps_type_and_redacts_internal_severity()
    test_exit_filtering_order_and_navigation_remain_unchanged()
    test_hidden_internal_state_is_redacted_and_unlabeled_spawns_fail_closed()
    test_malformed_region_entities_are_rejected_without_raw_value_fallback()
    test_explicitly_labeled_visible_spawned_groups_are_aggregated_in_order()
    test_save_load_reproduces_projection_without_persisting_it()
    test_query_does_not_invoke_provider_narration_parser_or_movement()
    print("Current-scene projection tests passed.")


if __name__ == "__main__":
    main()
