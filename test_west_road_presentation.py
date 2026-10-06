"""Focused scene hierarchy and unchanged-scene CLI behavior checks."""
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import play_game
from engine.game_engine import GameEngine
from test_west_road_predicament import ready
from test_artifact_files import artifact_files

REGION = "data/regions/bryn_shander.json"


def render(engine):
    before = engine.get_world_state()
    scene = engine.scene_snapshot
    output = StringIO()
    with redirect_stdout(output):
        play_game.print_narration(engine.get_narration())
    assert engine.get_world_state() == before and engine.scene_snapshot is scene
    return output.getvalue()


def test_initial_and_evidence_presentation():
    e = GameEngine(REGION)
    text = render(e)
    assert "North Gate, Bryn Shander" in text
    assert text.count("Here:") == 1 and "Visible:" not in text and "Present here:" not in text
    assert "Captain Darvin Grey, Elin Voss, 2 watch guards" in text
    assert "Weather: blizzard" in text
    assert "caravan is overdue" in text and "unconfirmed" in text
    assert text.index("What now?") < text.index("Other actions:")
    assert "You can speak" not in text and "You can present" not in text
    assert "Speak with Captain Darvin Grey / Elin Voss" in text
    # No single-sentence blank paragraph per weather/group/affordance.
    assert len([line for line in text.splitlines() if line.strip()]) <= 12
    e = ready()
    text = render(e)
    assert "- advocate patrol (one hour; other approaches lose coverage)" in text
    assert "- continue investigation (one hour; traffic remains exposed)" in text
    assert text.index("advocate patrol") < text.index("Other actions:")
    e = GameEngine(REGION)
    e.process_command("go to Southwest Trade Road")
    e.process_command("investigate")
    assert "What now?\nSpeak with Mara" in render(e)
    e.process_command("talk to Mara")
    e.process_command("go to North Gate")
    text = render(e)
    assert "Present Repeated Watch Tracks to Captain Darvin Grey" in text
    assert "Mara's Account to Elin Voss" in text
    assert text.count("Present ") == 1
    e.process_command("present Repeated Watch Tracks to Elin")
    assert "What now?\nReport Mara's Account to Elin" in render(e)


def test_branch_and_terminal_circumstances():
    for command, phrases, choices in (
        ("advocate patrol", ("patrol has driven", "fresh signs", "fewer guards"), ("pursue observers", "restore coverage")),
        ("continue investigation", ("wagon was intercepted", "threatened supply stop"), ("protect supply stop", "locate raiders")),
    ):
        e = ready(); e.process_command(command)
        text = render(e)
        for phrase in phrases + choices:
            assert phrase in text
        assert "You advocated" not in text and "You chose one more hour" not in text
        assert text.count("Here:") == 1 and "Visible:" not in text
        assert text.index("What now?") < text.index("Other actions:")
        for internal in ("west_road_", "history_", "observers_withdrew", "wagon_intercepted", "phase", "accepted decisions"):
            assert internal not in text
    e.process_command("protect supply stop")
    text = render(e)
    assert "next departure is held safely" in text
    assert "broader threat remains unresolved" in text
    assert "- protect supply stop" not in text


def run_cli(engine, commands):
    from engine.narration_pipeline import validate_narration_preview_candidate

    output = StringIO()
    def offline_preview(context):
        return validate_narration_preview_candidate(context, {
            "schema": "ai_rpg.narration_output_packet", "version": 1,
            "narration_text": "Snow drifts across the ground before you.",
        })

    with patch.object(play_game.GameEngine, "start_new", return_value=engine), patch("builtins.input", side_effect=commands), patch("engine.game_engine.build_narration_preview_packet", side_effect=offline_preview), patch("socket.create_connection", side_effect=AssertionError("network forbidden")), redirect_stdout(output):
        play_game.main()
    return output.getvalue()


def test_no_repeat_after_invalid_or_no_op():
    e = ready(); e.process_command("advocate patrol")
    before = deepcopy(e.get_world_state())
    text = run_cli(e, ["continue investigation", "advocate patrol", "clues", "help", "quit"])
    assert text.count("=== SCENE ===") == 1
    assert "You've committed to patrol action" in text
    assert "'pursue observers'" in text and "'restore coverage'" in text
    assert "accepted decisions remain unchanged" not in text
    assert e.get_world_state() == before
    e = ready(); e.process_command("continue investigation")
    before = e.get_world_state()
    text = run_cli(e, ["restore coverage", "continue investigation", "quit"])
    assert text.count("=== SCENE ===") == 1
    assert "'protect supply stop'" in text and "'locate raiders'" in text
    assert e.get_world_state() == before
    e = GameEngine(REGION)
    text = run_cli(e, ["investigate", "look", "quit"])
    assert text.count("=== SCENE ===") == 2 and "no new clues" in text
    assert "Snow drifts across the ground" in text
    assert "You take a closer look" not in text


def test_refresh_after_material_actions():
    e = ready()
    text = run_cli(e, ["advocate patrol", "restore coverage", "quit"])
    assert text.count("=== SCENE ===") == 3
    assert "Guards are back on ordinary local coverage" in text
    assert text.count("You choose to advocate patrol.") == 1
    assert "Grey: Your patrol broke up" not in text
    e = GameEngine(REGION)
    text = run_cli(e, ["go to Southwest Trade Road", "investigate", "talk to Mara", "quit"])
    assert text.count("=== SCENE ===") == 4
    assert "Southwest Trade Road, Bryn Shander" in text
    assert "Mara, Caravan Driver" in text


def test_brief_resume_and_following_scene():
    cases = [(ready(), ("reported the tracks and Mara's account to Elin", "immediate patrol or continue investigating"))]
    patrol = ready(); patrol.process_command("advocate patrol")
    cases.append((patrol, ("immediate patrol action", "pursue them or restore normal coverage")))
    investigation = ready(); investigation.process_command("continue investigation")
    cases.append((investigation, ("Another wagon was intercepted", "protect it or search for the raiders")))
    terminal = ready(); terminal.process_command("continue investigation"); terminal.process_command("protect supply stop")
    cases.append((terminal, ("protected the threatened supply stop", "next departure is held safely")))
    for engine, phrases in cases:
        before = engine.get_world_state()
        recap = engine.get_resume_summary()
        assert len(recap) == 1 and recap[0].startswith("Previously: ")
        assert len(recap[0].split()) <= 65
        for phrase in phrases:
            assert phrase in recap[0]
        for clue in engine.region["discovery_declarations"]:
            assert clue["text"] not in recap[0]
        for unwanted in ("Captain Darvin Grey", "North Gate", "Reported to Elin:", "Weather:", "history_", "west_road_"):
            assert unwanted not in recap[0]
        assert engine.get_world_state() == before
        with artifact_files("test_west_road_presentation") as directory:
            path = Path(directory) / "test_west_road_presentation_resume.json"
            engine.save(str(path))
            with patch.object(play_game, "SAVE_PATH", str(path)):
                text = run_cli(engine, ["load", "quit"])
            following = text.split("Game loaded.", 1)[1]
            assert following.index("Previously:") < following.index("=== SCENE ===")
            assert following.count("Previously:") == 1
            assert following.count("=== SCENE ===") == 1
            assert "North Gate, Bryn Shander" in following
        assert engine.get_world_state() == before
    # Incomplete acquisition/sharing must not be narrated as completed.
    fresh = GameEngine(REGION)
    assert "You gathered" not in fresh.get_resume_summary()[0]
    fresh.process_command("go to Southwest Trade Road")
    fresh.process_command("investigate")
    assert "You still need Mara's account" in fresh.get_resume_summary()[0]
    fresh.process_command("talk to Mara")
    fresh.process_command("go to North Gate")
    fresh.process_command("present Repeated Watch Tracks to Elin")
    assert "Report Mara's account to Elin" in fresh.get_resume_summary()[0]


def main():
    for test in (test_initial_and_evidence_presentation, test_branch_and_terminal_circumstances, test_no_repeat_after_invalid_or_no_op, test_refresh_after_material_actions, test_brief_resume_and_following_scene):
        test()
        print("PASS:", test.__name__)


if __name__ == "__main__":
    main()
