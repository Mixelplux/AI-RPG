from copy import deepcopy

from engine.game_engine import GameEngine
from engine.narration_output import (
    NARRATION_OUTPUT_SCHEMA,
    NARRATION_OUTPUT_VERSION,
)
from engine.narration_request import (
    NARRATION_REQUEST_CONSTRAINTS,
    NARRATION_REQUEST_MODE,
    NARRATION_REQUEST_SCHEMA,
    NARRATION_REQUEST_VERSION,
    build_narration_request_packet,
    validate_narration_request_packet,
)


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)
    narration_context = engine.get_narration_context("look around")
    context_before_request = deepcopy(narration_context)
    world_state_before_request = engine.get_world_state()
    history_before_request = engine.get_history()
    scene_before_request = engine.get_scene_snapshot()
    time_before_request = engine.get_world_state()["time"]

    narration_request = build_narration_request_packet(narration_context)

    assert narration_request["schema"] == NARRATION_REQUEST_SCHEMA
    assert narration_request["version"] == NARRATION_REQUEST_VERSION
    assert narration_request["mode"] == NARRATION_REQUEST_MODE
    assert narration_request["narration_context"] == narration_context
    assert narration_request["narration_context"] is not narration_context
    assert narration_request["expected_output"]["schema"] == (
        NARRATION_OUTPUT_SCHEMA
    )
    assert narration_request["expected_output"]["version"] == (
        NARRATION_OUTPUT_VERSION
    )
    assert isinstance(narration_request["expected_output"]["contract"], dict)
    assert narration_request["constraints"] == NARRATION_REQUEST_CONSTRAINTS
    assert "system" not in narration_request
    assert "messages" not in narration_request
    assert "provider" not in narration_request

    repeated_request = build_narration_request_packet(narration_context)
    assert repeated_request == narration_request
    assert validate_narration_request_packet(narration_request) == (
        narration_request
    )

    narration_request["narration_context"]["player_input"] = "mutated input"
    narration_request["constraints"]["candidate_output"] = "mutated"
    narration_request["expected_output"]["contract"]["type"] = "mutated"
    assert narration_context == context_before_request
    assert build_narration_request_packet(narration_context) == (
        repeated_request
    )

    malformed_context = deepcopy(narration_context)
    del malformed_context["schema"]
    try:
        build_narration_request_packet(malformed_context)
        raise AssertionError("Malformed narration context was accepted.")
    except ValueError as error:
        assert "schema" in str(error)

    malformed_request = deepcopy(repeated_request)
    malformed_request["constraints"]["state_mutation"] = "allowed"
    try:
        validate_narration_request_packet(malformed_request)
        raise AssertionError("Malformed narration request was accepted.")
    except ValueError as error:
        assert "constraints" in str(error)

    assert engine.get_world_state() == world_state_before_request
    assert engine.get_history() == history_before_request
    assert engine.get_scene_snapshot() == scene_before_request
    assert engine.get_world_state()["time"] == time_before_request

    print("Narration request test passed.")


if __name__ == "__main__":
    main()
