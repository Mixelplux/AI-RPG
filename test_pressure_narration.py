from copy import deepcopy

from engine.game_engine import GameEngine
from engine.narration_pipeline import build_narration_preview_packet
from engine.narration_source import NARRATION_SOURCE_METADATA


PATH = "test_fixtures/bryn_shander_legacy.json"
CUE = {
    "cue_id": "winter_deepens_observation",
    "pressure_id": "bryn_shander_winter",
    "text": "The cold has become noticeably more severe.",
}


def build_preview(context):
    return build_narration_preview_packet(
        context,
        source_builder=lambda prompt: {
            "schema": "ai_rpg.narration_source_result", "version": 1,
            "source": "openai_responses_preview", "source_prompt": prompt,
            "candidate": {"schema": "ai_rpg.narration_output_packet", "version": 1, "narration_text": "The street remains quiet."},
            "metadata": NARRATION_SOURCE_METADATA,
        },
    )


def main():
    engine = GameEngine(PATH)
    baseline = build_preview(engine.get_narration_context("look around"))
    assert baseline["accepted"]
    assert baseline["display_text"] == "The street remains quiet."
    assert baseline["narration_context"]["pressure_cue"] == {}
    assert baseline["narration_prompt"]["deterministic_input"]["pressure_cue"] == {}

    engine.process_command("wait")
    world_before = engine.get_world_state()
    scene_before = engine.get_scene_snapshot()
    region_before = deepcopy(engine.region)
    preview = build_preview(engine.get_narration_context("look around"))
    cue_text = CUE["text"]

    assert preview["accepted"]
    assert preview["narration_context"]["pressure_cue"] == CUE
    assert preview["narration_request"]["narration_context"]["pressure_cue"] == CUE
    assert preview["narration_prompt"]["deterministic_input"]["pressure_cue"] == CUE
    assert preview["display_text"].count(cue_text) == 1
    assert preview["validated_output"]["narration_text"].count(cue_text) == 1
    def keys(value):
        if isinstance(value, dict):
            return set(value).union(*(keys(item) for item in value.values()))
        if isinstance(value, list):
            return set().union(*(keys(item) for item in value))
        return set()

    assert not {"level", "previous_level", "new_level"} & keys(preview)
    assert "pressure_changed" not in repr(preview)
    assert "source_history_id" not in repr(preview)
    assert preview == build_preview(engine.get_narration_context("look around"))

    mutable = deepcopy(preview)
    mutable["narration_context"]["pressure_cue"]["text"] = "changed"
    assert build_preview(engine.get_narration_context("look around")) == preview

    duplicate_candidate = deepcopy(preview["candidate"])
    duplicate_candidate["narration_text"] = f"{cue_text} {cue_text}"
    normalized = build_narration_preview_packet(
        engine.get_narration_context("look around"),
        source_builder=lambda prompt: {
            **deepcopy(preview["source_result"]),
            "source_prompt": prompt,
            "candidate": duplicate_candidate,
        },
    )
    assert normalized["display_text"] == cue_text

    engine.set_pressure_level("bryn_shander_winter", 69)
    hidden = build_preview(engine.get_narration_context("look around"))
    assert hidden["narration_context"]["pressure_cue"] == {}
    assert cue_text not in hidden["display_text"]

    engine.set_pressure_level("bryn_shander_winter", 71)
    failure = build_narration_preview_packet(
        engine.get_narration_context("look around"),
        request_builder=lambda context: (_ for _ in ()).throw(ValueError("fail")),
    )
    assert not failure["accepted"]
    assert failure["display_text"] == ""
    assert engine.get_world_state() != world_before
    failure_world = engine.get_world_state()
    failure_scene = engine.get_scene_snapshot()
    assert engine.region == region_before
    assert engine.get_world_state() == failure_world
    assert engine.get_scene_snapshot() == failure_scene
    assert scene_before["scene_id"] == failure_scene["scene_id"]

    print("Pressure narration tests passed.")


if __name__ == "__main__":
    main()
