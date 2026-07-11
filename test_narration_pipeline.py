from copy import deepcopy
from tempfile import TemporaryDirectory

from engine.game_engine import GameEngine
from engine.narration_output import (
    NARRATION_OUTPUT_SCHEMA,
    NARRATION_OUTPUT_VERSION,
)
from engine.narration_pipeline import (
    NARRATION_PIPELINE_SCHEMA,
    NARRATION_PIPELINE_SOURCE,
    NARRATION_PIPELINE_VERSION,
    build_narration_preview_packet,
    validate_narration_preview_candidate,
)
from engine.narration_prompt import (
    NARRATION_PROMPT_SCHEMA,
    build_narration_prompt_packet,
)
from engine.narration_request import (
    NARRATION_REQUEST_SCHEMA,
    build_narration_request_packet,
)
from engine.narration_source import (
    NARRATION_SOURCE_FIXED_SAMPLE,
    NARRATION_SOURCE_METADATA,
    NARRATION_SOURCE_SCHEMA,
    NARRATION_SOURCE_VERSION,
)
from engine.save_system import load_game, save_game
from play_game import parse_narration_preview_command


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)

    narration_context = engine.get_narration_context("look around")
    preview_packet = engine.get_narration_preview("look around")

    assert preview_packet["schema"] == NARRATION_PIPELINE_SCHEMA
    assert preview_packet["version"] == NARRATION_PIPELINE_VERSION
    assert preview_packet["accepted"] is True
    assert preview_packet["source"] == NARRATION_PIPELINE_SOURCE
    assert preview_packet["display_text"] == "The street remains quiet."
    assert preview_packet["narration_request"]["schema"] == (
        NARRATION_REQUEST_SCHEMA
    )
    assert preview_packet["narration_request"]["narration_context"] == (
        narration_context
    )
    assert preview_packet["narration_prompt"]["schema"] == (
        NARRATION_PROMPT_SCHEMA
    )
    assert preview_packet["narration_prompt"]["originating_request"][
        "schema"
    ] == NARRATION_REQUEST_SCHEMA
    assert preview_packet["narration_prompt"]["deterministic_input"][
        "player_input"
    ] == narration_context["player_input"]
    assert preview_packet["source_result"]["schema"] == NARRATION_SOURCE_SCHEMA
    assert preview_packet["source_result"]["version"] == (
        NARRATION_SOURCE_VERSION
    )
    assert preview_packet["source_result"]["source"] == (
        NARRATION_SOURCE_FIXED_SAMPLE
    )
    assert preview_packet["source_result"]["metadata"] == (
        NARRATION_SOURCE_METADATA
    )
    assert preview_packet["source_result"]["candidate"] == (
        preview_packet["candidate"]
    )
    assert preview_packet["source_result"]["source_prompt"] == (
        preview_packet["narration_prompt"]
    )
    assert preview_packet["candidate"]["schema"] == NARRATION_OUTPUT_SCHEMA
    assert preview_packet["candidate"]["version"] == NARRATION_OUTPUT_VERSION
    assert preview_packet["validated_output"]["narration_text"] == (
        "The street remains quiet."
    )
    assert preview_packet["narration_context"] == narration_context
    assert preview_packet["narration_context"] is not narration_context
    assert preview_packet["candidate"]["narration_text"] == (
        "The street remains quiet."
    )
    assert preview_packet["validated_output"]["narration_text"] == (
        preview_packet["display_text"]
    )

    world_state_before_preview = engine.get_world_state()
    history_before_preview = engine.get_history()
    scene_before_preview = engine.get_scene_snapshot()
    time_before_preview = engine.get_world_state()["time"]

    repeated_preview = engine.get_narration_preview("look around")
    assert repeated_preview == preview_packet
    assert engine.get_world_state() == world_state_before_preview
    assert engine.get_history() == history_before_preview
    assert engine.get_scene_snapshot() == scene_before_preview
    assert engine.get_world_state()["time"] == time_before_preview

    preview_copy = build_narration_preview_packet(narration_context)
    preview_copy["display_text"] = "Mutated preview."
    preview_copy["candidate"]["narration_text"] = "Mutated candidate."
    preview_copy["narration_request"]["narration_context"]["player_input"] = (
        "mutated request."
    )
    preview_copy["narration_prompt"]["deterministic_input"]["player_input"] = (
        "mutated prompt."
    )
    preview_copy["source_result"]["candidate"]["narration_text"] = (
        "Mutated source candidate."
    )
    preview_copy["source_result"]["metadata"]["candidate_trust"] = "trusted"
    preview_copy["validated_output"]["narration_text"] = (
        "Mutated validated text."
    )
    preview_copy["narration_context"]["player_input"] = "mutated input"
    assert engine.get_narration_preview("look around") == preview_packet
    assert engine.get_world_state() == world_state_before_preview
    assert engine.get_history() == history_before_preview
    assert engine.get_scene_snapshot() == scene_before_preview

    invalid_candidate = {
        "schema": NARRATION_OUTPUT_SCHEMA,
        "version": NARRATION_OUTPUT_VERSION,
        "narration_text": "The street remains quiet.",
        "world_state": {"weather": "clear"},
    }
    invalid_result = validate_narration_preview_candidate(
        narration_context,
        invalid_candidate,
    )
    assert invalid_result["accepted"] is False
    assert invalid_result["source"] == NARRATION_PIPELINE_SOURCE
    assert invalid_result["display_text"] == ""
    assert invalid_result["failure_stage"] == "candidate_validation"
    assert "world_state" in invalid_result["error"]

    structured_invalid_candidate = {
        "schema": NARRATION_OUTPUT_SCHEMA,
        "version": NARRATION_OUTPUT_VERSION,
        "narration_text": "The street remains quiet.",
        "metadata": {
            "history": [{"summary": "Created history."}]
        },
    }
    structured_invalid_result = validate_narration_preview_candidate(
        narration_context,
        structured_invalid_candidate,
    )
    assert structured_invalid_result["accepted"] is False
    assert structured_invalid_result["display_text"] == ""
    assert structured_invalid_result["failure_stage"] == (
        "candidate_validation"
    )
    assert "history" in structured_invalid_result["error"]

    source_boundary_result = build_narration_preview_packet(
        narration_context,
        source_builder=lambda copied_prompt: {
            "schema": NARRATION_SOURCE_SCHEMA,
            "version": NARRATION_SOURCE_VERSION,
            "source": NARRATION_SOURCE_FIXED_SAMPLE,
            "source_prompt": copied_prompt,
            "candidate": {
                "schema": NARRATION_OUTPUT_SCHEMA,
                "version": NARRATION_OUTPUT_VERSION,
                "narration_text": "The street remains quiet.",
            },
            "metadata": deepcopy(NARRATION_SOURCE_METADATA),
        },
    )
    assert source_boundary_result["accepted"] is True
    assert source_boundary_result["display_text"] == "The street remains quiet."
    assert source_boundary_result["source_result"]["source_prompt"] == (
        source_boundary_result["narration_prompt"]
    )

    malformed_source_result = build_narration_preview_packet(
        narration_context,
        source_builder=lambda copied_prompt: {
            "schema": NARRATION_SOURCE_SCHEMA,
            "version": NARRATION_SOURCE_VERSION,
            "source": NARRATION_SOURCE_FIXED_SAMPLE,
            "source_prompt": copied_prompt,
            "metadata": deepcopy(NARRATION_SOURCE_METADATA),
        },
    )
    assert malformed_source_result["accepted"] is False
    assert malformed_source_result["display_text"] == ""
    assert malformed_source_result["failure_stage"] == (
        "source_result_validation"
    )
    assert malformed_source_result["candidate"] == {}
    assert malformed_source_result["source_result"] == {}
    assert "candidate" in malformed_source_result["error"]

    raw_invalid_source_result = build_narration_preview_packet(
        narration_context,
        source_builder=lambda copied_prompt: {
            "schema": NARRATION_SOURCE_SCHEMA,
            "version": NARRATION_SOURCE_VERSION,
            "source": NARRATION_SOURCE_FIXED_SAMPLE,
            "source_prompt": copied_prompt,
            "candidate": {
                "schema": NARRATION_OUTPUT_SCHEMA,
                "version": NARRATION_OUTPUT_VERSION,
                "narration_text": "Do not leak this source-result prose.",
            },
            "metadata": deepcopy(NARRATION_SOURCE_METADATA),
            "raw_payload": {
                "secret": "Do not leak this malformed source payload."
            },
        },
    )
    assert raw_invalid_source_result["accepted"] is False
    assert raw_invalid_source_result["display_text"] == ""
    assert raw_invalid_source_result["failure_stage"] == (
        "source_result_validation"
    )
    assert raw_invalid_source_result["candidate"] == {}
    assert raw_invalid_source_result["source_result"] == {}
    assert "raw_payload" in raw_invalid_source_result["error"]
    assert "Do not leak this source-result prose" not in (
        raw_invalid_source_result["error"]
    )
    assert "Do not leak this malformed source payload" not in (
        raw_invalid_source_result["error"]
    )

    mismatched_prompt_result = build_narration_preview_packet(
        narration_context,
        source_builder=lambda _copied_prompt: {
            "schema": NARRATION_SOURCE_SCHEMA,
            "version": NARRATION_SOURCE_VERSION,
            "source": NARRATION_SOURCE_FIXED_SAMPLE,
            "source_prompt": build_narration_prompt_packet(
                build_narration_request_packet(
                    engine.get_narration_context("different input")
                )
            ),
            "candidate": {
                "schema": NARRATION_OUTPUT_SCHEMA,
                "version": NARRATION_OUTPUT_VERSION,
                "narration_text": "The street remains quiet.",
            },
            "metadata": deepcopy(NARRATION_SOURCE_METADATA),
        },
    )
    assert mismatched_prompt_result["accepted"] is False
    assert mismatched_prompt_result["display_text"] == ""
    assert mismatched_prompt_result["candidate"] == {}
    assert mismatched_prompt_result["source_result"] == {}
    assert mismatched_prompt_result["failure_stage"] == (
        "source_result_validation"
    )
    assert "originating prompt" in mismatched_prompt_result["error"]

    malformed_context = deepcopy(narration_context)
    del malformed_context["schema"]
    request_construction_result = build_narration_preview_packet(
        malformed_context,
    )
    assert request_construction_result["accepted"] is False
    assert request_construction_result["display_text"] == ""
    assert request_construction_result["narration_request"] == {}
    assert request_construction_result["narration_prompt"] == {}
    assert request_construction_result["source_result"] == {}
    assert request_construction_result["failure_stage"] == (
        "request_construction"
    )
    assert "schema" in request_construction_result["error"]

    malformed_request_result = build_narration_preview_packet(
        narration_context,
        request_builder=lambda _copied_context: {
            "schema": NARRATION_REQUEST_SCHEMA,
            "version": 1,
            "mode": "preview",
            "narration_context": deepcopy(narration_context),
            "expected_output": {},
            "constraints": {},
        },
    )
    assert malformed_request_result["accepted"] is False
    assert malformed_request_result["display_text"] == ""
    assert malformed_request_result["failure_stage"] == "request_validation"
    assert "expected output" in malformed_request_result["error"]

    malformed_prompt_result = build_narration_preview_packet(
        narration_context,
        prompt_builder=lambda _copied_request: {
            "schema": NARRATION_PROMPT_SCHEMA,
            "version": 1,
            "mode": "preview",
            "originating_request": {},
            "expected_output": {},
            "instructions": {},
            "deterministic_input": {},
        },
    )
    assert malformed_prompt_result["accepted"] is False
    assert malformed_prompt_result["display_text"] == ""
    assert malformed_prompt_result["failure_stage"] == "prompt_validation"
    assert "request schema" in malformed_prompt_result["error"]

    def raising_prompt_builder(_copied_request):
        raise RuntimeError("deterministic prompt failure for testing")

    prompt_exception_result = build_narration_preview_packet(
        narration_context,
        prompt_builder=raising_prompt_builder,
    )
    assert prompt_exception_result["accepted"] is False
    assert prompt_exception_result["display_text"] == ""
    assert prompt_exception_result["narration_prompt"] == {}
    assert prompt_exception_result["failure_stage"] == "prompt_construction"
    assert "deterministic prompt failure" in prompt_exception_result["error"]

    def raising_request_builder(_copied_context):
        raise RuntimeError("deterministic request failure for testing")

    request_exception_result = build_narration_preview_packet(
        narration_context,
        request_builder=raising_request_builder,
    )
    assert request_exception_result["accepted"] is False
    assert request_exception_result["display_text"] == ""
    assert request_exception_result["narration_request"] == {}
    assert request_exception_result["narration_prompt"] == {}
    assert request_exception_result["failure_stage"] == "request_construction"
    assert "deterministic request failure" in request_exception_result["error"]

    def raising_source(_copied_context):
        raise RuntimeError("deterministic source failure for testing")

    source_exception_result = build_narration_preview_packet(
        narration_context,
        source_builder=raising_source,
    )
    assert source_exception_result["accepted"] is False
    assert source_exception_result["display_text"] == ""
    assert source_exception_result["candidate"] == {}
    assert source_exception_result["source_result"] == {}
    assert source_exception_result["failure_stage"] == "source_exception"
    assert "deterministic source failure" in source_exception_result["error"]

    invalid_source_candidate_result = build_narration_preview_packet(
        narration_context,
        source_builder=lambda copied_prompt: {
            "schema": NARRATION_SOURCE_SCHEMA,
            "version": NARRATION_SOURCE_VERSION,
            "source": NARRATION_SOURCE_FIXED_SAMPLE,
            "source_prompt": copied_prompt,
            "candidate": {
                "schema": NARRATION_OUTPUT_SCHEMA,
                "version": NARRATION_OUTPUT_VERSION,
                "narration_text": "Do not display this invalid candidate.",
                "world_state": {"weather": "changed"},
            },
            "metadata": deepcopy(NARRATION_SOURCE_METADATA),
        },
    )
    assert invalid_source_candidate_result["accepted"] is False
    assert invalid_source_candidate_result["display_text"] == ""
    assert invalid_source_candidate_result["failure_stage"] == (
        "candidate_validation"
    )
    assert "world_state" in invalid_source_candidate_result["error"]
    assert (
        invalid_source_candidate_result["candidate"]["narration_text"]
        == "Do not display this invalid candidate."
    )
    assert invalid_source_candidate_result["source_result"]["candidate"] == (
        invalid_source_candidate_result["candidate"]
    )

    non_object_candidate_result = build_narration_preview_packet(
        narration_context,
        source_builder=lambda copied_prompt: {
            "schema": NARRATION_SOURCE_SCHEMA,
            "version": NARRATION_SOURCE_VERSION,
            "source": NARRATION_SOURCE_FIXED_SAMPLE,
            "source_prompt": copied_prompt,
            "candidate": "not an object",
            "metadata": deepcopy(NARRATION_SOURCE_METADATA),
        },
    )
    assert non_object_candidate_result["accepted"] is False
    assert non_object_candidate_result["display_text"] == ""
    assert non_object_candidate_result["candidate"] == {}
    assert non_object_candidate_result["source_result"] == {}
    assert non_object_candidate_result["failure_stage"] == (
        "source_result_validation"
    )
    assert "candidate" in non_object_candidate_result["error"]

    bad_metadata_result = build_narration_preview_packet(
        narration_context,
        source_builder=lambda copied_prompt: {
            "schema": NARRATION_SOURCE_SCHEMA,
            "version": NARRATION_SOURCE_VERSION,
            "source": NARRATION_SOURCE_FIXED_SAMPLE,
            "source_prompt": copied_prompt,
            "candidate": {
                "schema": NARRATION_OUTPUT_SCHEMA,
                "version": NARRATION_OUTPUT_VERSION,
                "narration_text": "The street remains quiet.",
            },
            "metadata": {
                "candidate_trust": "trusted",
                "generation": "fixed_sample_only",
            },
        },
    )
    assert bad_metadata_result["accepted"] is False
    assert bad_metadata_result["display_text"] == ""
    assert bad_metadata_result["candidate"] == {}
    assert bad_metadata_result["source_result"] == {}
    assert bad_metadata_result["failure_stage"] == (
        "source_result_validation"
    )
    assert "metadata" in bad_metadata_result["error"]

    request_copy = build_narration_request_packet(narration_context)
    request_copy["narration_context"]["player_input"] = "mutated request"
    prompt_copy = build_narration_prompt_packet(
        build_narration_request_packet(narration_context)
    )
    prompt_copy["deterministic_input"]["player_input"] = "mutated prompt"
    assert engine.get_narration_preview("look around") == preview_packet

    assert parse_narration_preview_command(
        "narration preview describe the road"
    ) == {"player_input": "describe the road"}
    assert "error" in parse_narration_preview_command("narration preview")

    with TemporaryDirectory() as temp_dir:
        save_path = f"{temp_dir}/narration_pipeline_save.json"
        save_game(engine, save_path)
        loaded_engine = load_game(save_path)

    loaded_preview = loaded_engine.get_narration_preview("look around")
    assert loaded_preview == preview_packet
    assert loaded_engine.get_history() == history_before_preview
    assert loaded_engine.get_world_state() == world_state_before_preview

    print("Narration pipeline test passed.")


if __name__ == "__main__":
    main()
