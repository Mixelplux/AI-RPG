import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from engine.conversation_affordance import derive_conversation_affordance
from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import load_game


REGION = "data/regions/bryn_shander.json"
ACTOR = "guard_elin_voss"
DISCOVERY = "west_gate_elin_report_trace"
AFFORDANCE = {
    "affordance_id": "west_gate_elin_orders_conversation",
    "display_text": "Elin Voss is at the West Gate with the patrol orders. You can speak with her about them.",
    "command_text": "talk to Elin Voss",
    "target_display_name": "Elin Voss",
}


def data():
    return json.loads(Path(REGION).read_text(encoding="utf-8"))


def invalid(region, expected):
    try:
        validate_region(region)
    except ValueError as error:
        assert expected in str(error), str(error)
        return
    raise AssertionError("Expected Region Pack validation failure.")


def resolve_and_arrive(engine, discover=False):
    engine.process_command("talk to captain")
    engine.process_command("investigate")
    assert engine.present_clue("The Captain's Deliberate Trail", "captain")["changed"]
    assert engine.process_command("go south")["success"]
    assert engine.process_command("go east")["success"]
    assert engine.process_command("go north")["success"]
    if discover:
        assert engine.process_command("investigate")["investigation"]["discovery_id"] == DISCOVERY


def test_validation():
    region = data()
    validate_region(region)
    absent = deepcopy(region)
    del absent["conversation_affordance"]
    validate_region(absent)

    for field in (
        "affordance_id", "location_id", "target_entity_id",
        "required_discovery_id", "display_text",
    ):
        missing = deepcopy(region)
        del missing["conversation_affordance"][field]
        invalid(missing, "conversation_affordance fields are invalid")
        empty = deepcopy(region)
        empty["conversation_affordance"][field] = ""
        invalid(empty, "conversation_affordance values must be non-empty strings")

    extra = deepcopy(region)
    extra["conversation_affordance"]["priority"] = 1
    invalid(extra, "conversation_affordance fields are invalid")
    multiple = deepcopy(region)
    multiple["conversation_affordance"] = [
        deepcopy(region["conversation_affordance"]),
        deepcopy(region["conversation_affordance"]),
    ]
    invalid(multiple, "conversation_affordance fields are invalid")
    unknown_location = deepcopy(region)
    unknown_location["conversation_affordance"]["location_id"] = "missing"
    invalid(unknown_location, "conversation_affordance.location_id is unknown")
    unknown_actor = deepcopy(region)
    unknown_actor["conversation_affordance"]["target_entity_id"] = "missing"
    invalid(unknown_actor, "conversation_affordance.target_entity_id must reference one static actor")
    unknown_discovery = deepcopy(region)
    unknown_discovery["conversation_affordance"]["required_discovery_id"] = "missing"
    invalid(unknown_discovery, "conversation_affordance.required_discovery_id is unknown")
    mismatched_pair = deepcopy(region)
    mismatched_pair["conversation_affordance"]["target_entity_id"] = "captain_darvin_grey"
    invalid(mismatched_pair, "must match one discovery-gated conversation response")
    unsupported_location = deepcopy(region)
    unsupported_location["conversation_affordance"]["location_id"] = "traders_hall"
    invalid(unsupported_location, "cannot be present at declaration location")
    missing_response = deepcopy(region)
    del missing_response["conversation_player_discovery_response"]
    invalid(missing_response, "must match one discovery-gated conversation response")


def test_projection_and_existing_talk_authority():
    engine = GameEngine(REGION)
    assert engine.get_player_perception()["conversation_affordance"] == {}
    resolve_and_arrive(engine)
    assert engine.get_player_perception()["conversation_affordance"] == {}

    assert engine.process_command("talk to elin")["player_discovery_response"] is None
    assert engine.process_command("investigate")["investigation"]["discovery_id"] == DISCOVERY
    perception = engine.get_player_perception()
    assert perception["conversation_affordance"] == AFFORDANCE
    assert set(perception["conversation_affordance"]) == set(AFFORDANCE)
    assert DISCOVERY not in repr(perception["conversation_affordance"])
    assert ACTOR not in repr(perception["conversation_affordance"])
    assert engine.get_narration()["description"].find(AFFORDANCE["display_text"]) == -1
    result = engine.process_command(perception["conversation_affordance"]["command_text"])
    assert result["success"]
    assert result["player_discovery_response"] == {
        "text": engine.region["conversation_player_discovery_response"]["response_text"]
    }

    world_before = engine.get_world_state()
    scene_before = engine.scene_snapshot

    perception["conversation_affordance"]["display_text"] = "changed"
    assert engine.get_player_perception()["conversation_affordance"] == AFFORDANCE
    assert engine.get_player_perception()["conversation_affordance"] == AFFORDANCE
    assert engine.get_world_state() == world_before
    assert engine.scene_snapshot is scene_before

    scene_without_elin = deepcopy(engine.get_scene_snapshot())
    scene_without_elin["entities"]["static"].remove(ACTOR)
    assert derive_conversation_affordance(
        engine.region,
        "bryn_shander_gate_west",
        scene_without_elin,
        tuple(engine.get_world_state()["player_discoveries"]),
    ) is None

    stale = deepcopy(engine.get_player_perception()["conversation_affordance"])
    assert stale == AFFORDANCE
    assert engine.process_command("go east")["success"]
    assert engine.get_player_perception()["conversation_affordance"] == {}
    stale_result = engine.process_command("talk to elin")
    assert not stale_result["success"]
    assert stale_result["player_discovery_response"] is None


def test_save_load_and_reentry_reconstruct_the_projection():
    engine = GameEngine(REGION)
    resolve_and_arrive(engine, discover=True)
    assert engine.get_player_perception()["conversation_affordance"] == AFFORDANCE

    with TemporaryDirectory() as directory:
        save_path = str(Path(directory) / "save.json")
        engine.save(save_path)
        loaded = load_game(save_path)
        assert loaded.get_player_perception()["conversation_affordance"] == AFFORDANCE
        assert "conversation_affordance" not in loaded.get_world_state()

    assert engine.process_command("go east")["success"]
    assert engine.get_player_perception()["conversation_affordance"] == {}
    assert engine.process_command("go east")["success"]
    assert engine.process_command("go north")["success"]
    assert engine.get_player_perception()["conversation_affordance"] == AFFORDANCE


def main():
    test_validation()
    test_projection_and_existing_talk_authority()
    test_save_load_and_reentry_reconstruct_the_projection()
    print("Discovery-gated conversation-affordance tests passed.")


if __name__ == "__main__":
    main()
