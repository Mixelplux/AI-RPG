from copy import deepcopy

from engine.game_engine import GameEngine
from engine.narration_output import (
    NARRATION_OUTPUT_SCHEMA,
    NARRATION_OUTPUT_VERSION,
)
from engine.narration_prompt import build_narration_prompt_packet
from engine.narration_request import build_narration_request_packet
from engine.narration_source import (
    NARRATION_SOURCE_FIXED_SAMPLE,
    NARRATION_SOURCE_METADATA,
    NARRATION_SOURCE_SAMPLE_PROSE,
    NARRATION_SOURCE_SCHEMA,
    NARRATION_SOURCE_VERSION,
    build_fixed_sample_narration_source_result,
    validate_narration_source_result_packet,
)


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)
    narration_context = engine.get_narration_context("look around")
    narration_request = build_narration_request_packet(narration_context)
    narration_prompt = build_narration_prompt_packet(narration_request)
    context_before_source = deepcopy(narration_context)
    request_before_source = deepcopy(narration_request)
    prompt_before_source = deepcopy(narration_prompt)
    world_state_before_source = engine.get_world_state()
    history_before_source = engine.get_history()
    scene_before_source = engine.get_scene_snapshot()
    time_before_source = engine.get_world_state()["time"]

    source_result = build_fixed_sample_narration_source_result(
        narration_prompt
    )

    assert source_result["schema"] == NARRATION_SOURCE_SCHEMA
    assert source_result["version"] == NARRATION_SOURCE_VERSION
    assert source_result["source"] == NARRATION_SOURCE_FIXED_SAMPLE
    assert source_result["metadata"]["candidate_trust"] == "untrusted"
    assert source_result["metadata"]["generation"] == "fixed_sample_only"
    assert source_result["source_prompt"] == narration_prompt
    assert source_result["source_prompt"] is not narration_prompt
    assert source_result["source_prompt"]["deterministic_input"][
        "player_input"
    ] == narration_context["player_input"]
    assert "source_request" not in source_result
    assert "narration_context" not in source_result["source_prompt"]
    assert "world_state" not in source_result["source_prompt"]
    assert "messages" not in source_result["source_prompt"]
    assert "provider" not in source_result["source_prompt"]

    candidate = source_result["candidate"]
    assert candidate["schema"] == NARRATION_OUTPUT_SCHEMA
    assert candidate["version"] == NARRATION_OUTPUT_VERSION
    assert candidate["narration_text"] == NARRATION_SOURCE_SAMPLE_PROSE
    assert "contract" not in candidate

    validated_result = validate_narration_source_result_packet(
        source_result,
        narration_prompt,
    )
    assert validated_result == source_result
    assert validated_result is not source_result
    assert validated_result["source_prompt"] is not source_result["source_prompt"]
    assert validated_result["candidate"] is not source_result["candidate"]
    assert validated_result["metadata"] is not source_result["metadata"]
    assert validate_narration_source_result_packet(
        source_result,
        narration_prompt,
    ) == validated_result

    repeated_source_result = build_fixed_sample_narration_source_result(
        narration_prompt
    )
    assert repeated_source_result == source_result

    different_context = engine.get_narration_context(
        "describe the market square"
    )
    different_request = build_narration_request_packet(different_context)
    different_prompt = build_narration_prompt_packet(different_request)
    different_source_result = build_fixed_sample_narration_source_result(
        different_prompt
    )
    assert different_source_result["candidate"] == source_result["candidate"]

    source_result["source_prompt"]["deterministic_input"]["player_input"] = (
        "mutated input"
    )
    source_result["candidate"]["narration_text"] = "Mutated candidate."
    source_result["metadata"]["candidate_trust"] = "mutated trust"
    assert narration_context == context_before_source
    assert narration_request == request_before_source
    assert narration_prompt == prompt_before_source
    assert build_fixed_sample_narration_source_result(
        narration_prompt
    ) == repeated_source_result
    assert validated_result["source_prompt"] == prompt_before_source
    assert validated_result["candidate"]["narration_text"] == (
        NARRATION_SOURCE_SAMPLE_PROSE
    )
    assert validated_result["metadata"] == NARRATION_SOURCE_METADATA

    malformed_prompt = deepcopy(narration_prompt)
    malformed_prompt["instructions"]["state_mutation"] = "allowed"
    try:
        build_fixed_sample_narration_source_result(malformed_prompt)
        raise AssertionError("Malformed narration prompt was accepted.")
    except ValueError as error:
        assert "instructions" in str(error)

    def assert_source_result_rejected(source_result_value, expected_text):
        try:
            validate_narration_source_result_packet(
                source_result_value,
                narration_prompt,
            )
            raise AssertionError(
                f"Invalid source result was accepted: {expected_text}"
            )
        except ValueError as error:
            assert expected_text in str(error)

    valid_source_result = build_fixed_sample_narration_source_result(
        narration_prompt
    )
    source_result_before_validation = deepcopy(valid_source_result)
    prompt_before_validation = deepcopy(narration_prompt)
    validate_narration_source_result_packet(
        valid_source_result,
        narration_prompt,
    )
    assert valid_source_result == source_result_before_validation
    assert narration_prompt == prompt_before_validation

    assert_source_result_rejected([], "object")

    missing_candidate = deepcopy(valid_source_result)
    del missing_candidate["candidate"]
    assert_source_result_rejected(missing_candidate, "candidate")

    extra_top_level = deepcopy(valid_source_result)
    extra_top_level["unexpected"] = "not allowed"
    assert_source_result_rejected(extra_top_level, "unsupported")

    wrong_schema = deepcopy(valid_source_result)
    wrong_schema["schema"] = "wrong.schema"
    assert_source_result_rejected(wrong_schema, "schema")

    wrong_version = deepcopy(valid_source_result)
    wrong_version["version"] = 2
    assert_source_result_rejected(wrong_version, "version")

    wrong_source = deepcopy(valid_source_result)
    wrong_source["source"] = "other_source"
    assert_source_result_rejected(wrong_source, "source")

    non_object_prompt = deepcopy(valid_source_result)
    non_object_prompt["source_prompt"] = "not an object"
    assert_source_result_rejected(non_object_prompt, "prompt")

    invalid_prompt = deepcopy(valid_source_result)
    invalid_prompt["source_prompt"]["instructions"]["state_mutation"] = (
        "allowed"
    )
    assert_source_result_rejected(invalid_prompt, "instructions")

    substituted_prompt = deepcopy(valid_source_result)
    substituted_prompt["source_prompt"] = different_prompt
    assert_source_result_rejected(substituted_prompt, "originating prompt")

    non_object_candidate = deepcopy(valid_source_result)
    non_object_candidate["candidate"] = "not an object"
    assert_source_result_rejected(non_object_candidate, "candidate")

    non_object_metadata = deepcopy(valid_source_result)
    non_object_metadata["metadata"] = "not an object"
    assert_source_result_rejected(non_object_metadata, "metadata")

    missing_metadata = deepcopy(valid_source_result)
    del missing_metadata["metadata"]["generation"]
    assert_source_result_rejected(missing_metadata, "generation")

    extra_metadata = deepcopy(valid_source_result)
    extra_metadata["metadata"]["extra"] = "not allowed"
    assert_source_result_rejected(extra_metadata, "unsupported")

    altered_candidate_trust = deepcopy(valid_source_result)
    altered_candidate_trust["metadata"]["candidate_trust"] = "trusted"
    assert_source_result_rejected(altered_candidate_trust, "metadata")

    altered_generation = deepcopy(valid_source_result)
    altered_generation["metadata"]["generation"] = "model_generated"
    assert_source_result_rejected(altered_generation, "metadata")

    assert engine.get_world_state() == world_state_before_source
    assert engine.get_history() == history_before_source
    assert engine.get_scene_snapshot() == scene_before_source
    assert engine.get_world_state()["time"] == time_before_source

    print("Narration source test passed.")


if __name__ == "__main__":
    main()
