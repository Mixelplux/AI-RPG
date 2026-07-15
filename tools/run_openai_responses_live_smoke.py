"""Owner-invoked, one-request live verification; intentionally not a test_ file."""

from engine.game_engine import GameEngine
from engine.save_system import SAVE_VERSION


def main() -> None:
    engine = GameEngine("data/regions/bryn_shander.json")
    world_before = engine.get_world_state()
    history_before = engine.get_history()
    scene_before = engine.get_scene_snapshot()
    preview = engine.get_narration_preview("look around")
    if (
        preview.get("accepted") is not True
        or preview.get("source") != "openai_responses_preview"
        or not preview.get("display_text")
        or engine.get_world_state() != world_before
        or engine.get_history() != history_before
        or engine.get_scene_snapshot() != scene_before
        or SAVE_VERSION != 1
    ):
        stage = preview.get("failure_stage", "provider_response")
        reason = preview.get("error", "")
        allowed = {"incomplete_max_output_tokens", "incomplete_content_filter", "empty_output", "refusal", "failed_status", "unexpected_response_shape"}
        suffix = f" reason={reason}" if stage == "provider_response" and reason in allowed else ""
        print(f"LIVE_SMOKE_FAIL stage={stage}{suffix}")
        return
    print("LIVE_SMOKE_PASS provider=openai model=gpt-4.1-mini")


if __name__ == "__main__":
    main()
