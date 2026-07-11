from copy import deepcopy

from engine.game_engine import GameEngine
from engine.narration_output import (
    NARRATION_OUTPUT_SCHEMA,
    NARRATION_OUTPUT_VERSION,
)
from engine.narration_prompt import (
    NARRATION_PROMPT_INSTRUCTIONS,
    NARRATION_PROMPT_MODE,
    NARRATION_PROMPT_SCHEMA,
    NARRATION_PROMPT_VERSION,
    build_narration_prompt_packet,
    validate_narration_prompt_packet,
)
from engine.narration_request import (
    NARRATION_REQUEST_SCHEMA,
    NARRATION_REQUEST_VERSION,
    build_narration_request_packet,
)


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)
    narration_context = engine.get_narration_context("look around")
    narration_request = build_narration_request_packet(narration_context)
    request_before_prompt = deepcopy(narration_request)
    world_state_before_prompt = engine.get_world_state()
    history_before_prompt = engine.get_history()
    scene_before_prompt = engine.get_scene_snapshot()
    time_before_prompt = engine.get_world_state()["time"]

    narration_prompt = build_narration_prompt_packet(narration_request)

    assert narration_prompt["schema"] == NARRATION_PROMPT_SCHEMA
    assert narration_prompt["version"] == NARRATION_PROMPT_VERSION
    assert narration_prompt["mode"] == NARRATION_PROMPT_MODE
    assert narration_prompt["originating_request"]["schema"] == (
        NARRATION_REQUEST_SCHEMA
    )
    assert narration_prompt["originating_request"]["version"] == (
        NARRATION_REQUEST_VERSION
    )
    assert narration_prompt["originating_request"]["mode"] == "preview"
    assert narration_prompt["expected_output"]["schema"] == (
        NARRATION_OUTPUT_SCHEMA
    )
    assert narration_prompt["expected_output"]["version"] == (
        NARRATION_OUTPUT_VERSION
    )
    assert narration_prompt["expected_output"]["format"] == "prose_only"
    assert narration_prompt["instructions"] == NARRATION_PROMPT_INSTRUCTIONS
    assert "engine decides what is true" in (
        narration_prompt["instructions"]["authority_rule"].lower()
    )
    assert narration_prompt["instructions"]["output_format"] == "prose_only"
    assert narration_prompt["instructions"]["state_mutation"] == "forbidden"
    assert narration_prompt["instructions"]["time_advancement"] == "forbidden"
    assert narration_prompt["instructions"]["history_creation"] == "forbidden"
    assert narration_prompt["instructions"]["persistence_claims"] == "forbidden"
    assert narration_prompt["instructions"]["structured_simulation_commands"] == (
        "forbidden"
    )

    deterministic_input = narration_prompt["deterministic_input"]
    assert deterministic_input["player_input"] == (
        narration_context["player_input"]
    )
    assert deterministic_input["current_time"] == narration_context["current_time"]
    assert deterministic_input["player"] == narration_context["player"]
    assert deterministic_input["scene_snapshot"] == (
        narration_context["scene_snapshot"]
    )
    assert deterministic_input["history_context"] == (
        narration_context["history_context"]
    )
    assert deterministic_input["boundary"] == narration_context["boundary"]
    assert deterministic_input["constraints"] == narration_request["constraints"]

    assert "system" not in narration_prompt
    assert "messages" not in narration_prompt
    assert "provider" not in narration_prompt
    assert "model" not in narration_prompt
    assert "temperature" not in narration_prompt
    assert "api_key" not in narration_prompt

    repeated_prompt = build_narration_prompt_packet(narration_request)
    assert repeated_prompt == narration_prompt
    assert validate_narration_prompt_packet(narration_prompt) == (
        narration_prompt
    )

    narration_prompt["deterministic_input"]["player_input"] = "mutated"
    narration_prompt["deterministic_input"]["scene_snapshot"]["scene_id"] = (
        "mutated_scene"
    )
    narration_prompt["instructions"]["state_mutation"] = "allowed"
    assert narration_request == request_before_prompt
    assert build_narration_prompt_packet(narration_request) == repeated_prompt

    validated_prompt = validate_narration_prompt_packet(repeated_prompt)
    validated_prompt["deterministic_input"]["player"]["current_location_id"] = (
        "mutated_location"
    )
    assert validate_narration_prompt_packet(repeated_prompt) == repeated_prompt

    malformed_request = deepcopy(narration_request)
    malformed_request["constraints"]["state_mutation"] = "allowed"
    try:
        build_narration_prompt_packet(malformed_request)
        raise AssertionError("Malformed narration request was accepted.")
    except ValueError as error:
        assert "constraints" in str(error)

    malformed_prompt = deepcopy(repeated_prompt)
    malformed_prompt["instructions"]["state_mutation"] = "allowed"
    try:
        validate_narration_prompt_packet(malformed_prompt)
        raise AssertionError("Malformed narration prompt was accepted.")
    except ValueError as error:
        assert "instructions" in str(error)

    extra_field_prompt = deepcopy(repeated_prompt)
    extra_field_prompt["messages"] = []
    try:
        validate_narration_prompt_packet(extra_field_prompt)
        raise AssertionError("Provider-style prompt field was accepted.")
    except ValueError as error:
        assert "messages" in str(error)

    malformed_input_prompt = deepcopy(repeated_prompt)
    del malformed_input_prompt["deterministic_input"]["scene_snapshot"]
    try:
        validate_narration_prompt_packet(malformed_input_prompt)
        raise AssertionError("Malformed deterministic input was accepted.")
    except ValueError as error:
        assert "scene_snapshot" in str(error)

    assert engine.get_world_state() == world_state_before_prompt
    assert engine.get_history() == history_before_prompt
    assert engine.get_scene_snapshot() == scene_before_prompt
    assert engine.get_world_state()["time"] == time_before_prompt

    print("Narration prompt test passed.")


if __name__ == "__main__":
    main()
