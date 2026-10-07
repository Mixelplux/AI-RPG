"""Focused scene hierarchy and unchanged-scene CLI behavior checks."""
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import play_game
from engine.game_engine import GameEngine
from engine import character_competence, west_road_predicament
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
    assert "Here:" not in text and "Visible:" not in text and "Present here:" not in text
    assert "Captain Darvin Grey, Elin Voss, 2 watch guards" in text
    assert "A blizzard sweeps" in text
    assert "caravan is overdue" in text and "No one knows who" in text
    assert text.index("What now?") < text.index("Other actions:")
    assert "You can speak" not in text and "You can present" not in text
    assert "Captain Darvin Grey (talk to Grey) / Elin Voss (talk to Elin)" in text
    # No single-sentence blank paragraph per weather/group/affordance.
    assert len([line for line in text.splitlines() if line.strip()]) <= 12
    e = ready()
    text = render(e)
    assert "Urge an immediate patrol" in text and "one hour; other approaches lose coverage" in text
    assert "Keep the guards in place" in text and "one hour; road traffic remains exposed" in text
    assert "type 'advocate patrol'" in text and "type 'continue investigation'" in text
    assert text.index("advocate patrol") < text.index("Other actions:")
    e = GameEngine(REGION)
    e.process_command("go to Southwest Trade Road")
    e.process_command("investigate")
    assert "What now?\nThe tracks show people watched the road. Ask Mara" in render(e)
    e.process_command("talk to Mara")
    e.process_command("go to North Gate")
    text = render(e)
    assert "Present Repeated Watch Tracks to Captain Darvin Grey" in text
    assert "Mara's Account to Elin Voss" in text
    assert text.count("Present ") == 1
    e.process_command("present Repeated Watch Tracks to Elin")
    assert "What now?\nTell Elin about what Mara saw" in render(e)
    road = GameEngine(REGION)
    road.process_command("go to Southwest Trade Road")
    assert "Mara, Caravan Driver is here." in render(road)
    assert "Mara, Caravan Driver (talk to Mara)" in render(road)
    assert road.process_command("talk to Mara")["success"]


def test_branch_and_terminal_circumstances():
    for command, phrases, choices in (
        ("advocate patrol", ("patrol scattered", "fresh tracks", "fewer guards"), ("pursue observers", "restore coverage")),
        ("continue investigation", ("wagon was intercepted", "threatened supply stop"), ("protect supply stop", "locate raiders")),
    ):
        e = ready(); e.process_command(command)
        text = render(e)
        for phrase in phrases + choices:
            assert phrase in text
        assert "second wagon" not in text
        assert "You advocated" not in text and "You chose one more hour" not in text
        assert "Here:" not in text and "Visible:" not in text
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
    assert "You restored ordinary local coverage" in text
    assert "You choose to advocate patrol." not in text
    assert "Grey: " + e.region["west_road_predicament"]["actor_responses"][west_road_predicament.GREY]["observers_withdrew"] in text
    assert "Elin: " + e.region["west_road_predicament"]["actor_responses"][west_road_predicament.ELIN]["observers_withdrew"] in text
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


def test_choice_parity_and_plain_language():
    def assert_parity(engine):
        projected = engine.get_player_perception()["contextual_actions"]["opportunities"]
        choices = [text for text in projected if text.startswith("You can choose:")]
        expected = west_road_predicament.available_commands(engine.world_state, engine.scene_snapshot)
        expected += [item["command"] for item in engine.get_competence_projection()["approaches"]]
        assert len(choices) == len(expected)
        assert all(sum("type '" + command + "'" in text for text in choices) == 1 for command in expected)
        assert "d6" not in render(engine) and "1-2" not in render(engine)
        return choices

    for engine in (GameEngine(REGION), ready()):
        assert_parity(engine)
    engine = ready(); engine.process_command("advocate patrol")
    assert_parity(engine)
    choices = [text for text in engine.get_player_perception()["contextual_actions"]["opportunities"] if text.startswith("You can choose:")]
    expected = west_road_predicament.available_commands(engine.world_state, engine.scene_snapshot)
    expected += [item["command"] for item in engine.get_competence_projection()["approaches"]]
    assert len(choices) == len(expected)
    assert all(sum("type '" + command + "'" in text for text in choices) == 1 for command in expected)
    for approach in engine.get_competence_projection()["approaches"]:
        line = next(text for text in choices if "type '" + approach["command"] + "'" in text)
        assert ("one hour" if approach["cost_hours"] == 1 else "2 hours") in line
    with patch.object(character_competence, "draw_d6", return_value=3):
        engine.process_command("follow withdrawal signs")
    choices = assert_parity(engine)
    assert not any("type 'follow withdrawal signs'" in text for text in choices)
    assert all("type '" + command + "'" in " ".join(choices) for command in ("pursue observers", "restore coverage"))
    for initial, followup in (("advocate patrol", "restore coverage"), ("continue investigation", "protect supply stop")):
        terminal = ready()
        assert terminal.process_command(initial)["success"]
        assert_parity(terminal)
        assert terminal.process_command(followup)["success"]
        assert assert_parity(terminal) == []
    off_gate = ready()
    off_gate.process_command("go to Southwest Trade Road")
    assert assert_parity(off_gate) == []
    from test_character_competence import withdrawn
    tactical = withdrawn("tactical_assessment")
    assert "one hour" in next(text for text in assert_parity(tactical) if "type 'arrange guarded local survey'" in text)


def test_result_flow_and_replay():
    for draw, phrase in ((1, "cannot pick out a trail"), (3, "complete route remains unconfirmed"), (5, "withdrawal route")):
        engine = ready()
        engine.process_command("advocate patrol")
        with patch.object(character_competence, "draw_d6", return_value=draw):
            text = run_cli(engine, ["follow withdrawal signs", "follow withdrawal signs", "quit"])
        assert phrase in text
        assert text.count("An hour passes.") == 1
        assert text.count("That approach has already been resolved.") == 1
        assert engine.world_state["competence_attempts"]["follow withdrawal signs"]["draw"] == draw
        assert text.count("A blizzard sweeps") == 1
        if draw == 3:
            finding = character_competence.outcome_text(engine.region, "follow withdrawal signs", engine.world_state["competence_attempts"]["follow withdrawal signs"])
            assert text.count(finding) == 2  # accepted result and replay; never the refreshed scene
    engine = GameEngine(REGION)
    rejected = run_cli(engine, ["follow withdrawal signs", "quit"])
    assert "Fresh withdrawal evidence is not applicable" in rejected
    assert "An hour passes." not in rejected
    engine = ready(); engine.process_command("advocate patrol")
    fixed = run_cli(engine, ["restore coverage", "quit"])
    assert fixed.count(engine.region["west_road_predicament"]["phase_text"]["coverage_restored"]) == 1


def test_approach_aware_recap():
    from test_character_competence import withdrawn
    for command, draw, phrase in (
        ("follow withdrawal signs", 5, "followed the watchers' fresh tracks"),
        ("reconstruct local observation circuit", 5, "compared the watchers' roadside positions"),
        ("arrange guarded local survey", None, "arranged a guarded survey"),
    ):
        engine = withdrawn()
        with patch.object(character_competence, "draw_d6", return_value=draw):
            assert engine.process_command(command)["success"]
        summary = engine.get_resume_summary()[0]
        assert phrase in summary and "Nobody was captured" in summary
        assert "then followed the observers' withdrawal route" not in summary
        with artifact_files("test_west_road_presentation") as directory:
            path = Path(directory) / "approach_recap.json"
            engine.save(str(path))
            loaded = GameEngine(REGION)
            loaded.load(str(path))
            assert loaded.get_resume_summary()[0] == summary
    engine = withdrawn()
    assert engine.process_command("pursue observers")["success"]
    assert "then followed the observers' withdrawal route" in engine.get_resume_summary()[0]


def test_specific_result_composition():
    engine = GameEngine(REGION)
    clue_text = next(d["text"] for d in engine.region["discovery_declarations"] if d["discovery_id"] == "west_road_tracks")
    text = run_cli(engine, [
        "go to Southwest Trade Road", "investigate", "investigate",
        "go to North Gate", "present Repeated Watch Tracks to Elin",
        "present Repeated Watch Tracks to Elin", "present Unknown Clue to Elin",
        "present", "go to Atlantis", "check tracking", "quit",
    ])
    assert text.count(clue_text) == 1
    assert text.count("You find no new clues here.") == 1
    assert text.count("Elin Voss hears the report.") == 1
    assert text.count("Elin Voss already received that report.") == 1
    assert text.count("You cannot present that clue here.") == 1
    assert text.count("Usage: present <clue title> to <actor>") == 1
    assert text.count("You cannot reach that destination locally.") == 1
    assert text.count("You attempt a tracking check.") == 1
    assert "You investigate the area." not in text and "You present a clue." not in text


def test_investigating_guidance_stages():
    def hint(engine):
        return engine.get_narration()["current_choice_hint"]

    def choices(engine):
        return engine.get_narration()["scene_sections"]["choices"]

    def assert_gate_travel(engine):
        text = choices(engine)
        assert "(go to Southwest Trade Road)" in text
        assert "(investigate)" not in text and "(talk to Mara)" not in text

    fresh = GameEngine(REGION)
    assert "speak with Mara" in hint(fresh) and "Elin needs both reports" in hint(fresh)
    assert_gate_travel(fresh)
    assert GameEngine(REGION).process_command("go to Southwest Trade Road")["success"]
    assert not west_road_predicament.available_commands(fresh.world_state, fresh.scene_snapshot)

    tracks = GameEngine(REGION)
    tracks.process_command("go to Southwest Trade Road")
    assert "(investigate)" in choices(tracks) and "(talk to Mara)" in choices(tracks)
    tracks.process_command("investigate")
    assert "Ask Mara" in hint(tracks) and "(talk to Mara)" in choices(tracks)
    tracks.process_command("go to North Gate")
    assert_gate_travel(tracks)
    tracks.process_command("present Repeated Watch Tracks to Elin")
    assert "Elin has your report about the tracks" in hint(tracks)
    assert "Elin still needs Mara's report" in hint(tracks)
    assert_gate_travel(tracks)
    tracks.process_command("go to Southwest Trade Road")
    assert "Elin still needs Mara's report" in hint(tracks)
    assert "(talk to Mara)" in choices(tracks)

    mara = GameEngine(REGION)
    mara.process_command("go to Southwest Trade Road")
    mara.process_command("talk to Mara")
    assert "Examine the tracks" in hint(mara)
    mara.process_command("go to North Gate")
    assert "Elin needs both reports" in hint(mara)
    assert_gate_travel(mara)
    mara.process_command("present Mara's Account to Elin")
    assert "Elin has Mara's report" in hint(mara)
    assert "Elin still needs your findings from the tracks" in hint(mara)
    assert_gate_travel(mara)

    both = GameEngine(REGION)
    for command in ("go to Southwest Trade Road", "investigate", "talk to Mara"):
        both.process_command(command)
    assert "(go to North Gate)" in choices(both)
    assert "present Repeated Watch Tracks" not in choices(both)
    assert "present Mara's Account" not in choices(both)
    assert both.process_command("go to North Gate")["success"]
    assert "what the tracks show and what Mara saw" in hint(both)
    assert "at the North Gate" not in hint(both)
    both.process_command("present Repeated Watch Tracks to Grey")
    both.process_command("present Mara's Account to Grey")
    assert "what the tracks show and what Mara saw" in hint(both)
    assert "Use: present Repeated Watch Tracks to Elin; present Mara's Account to Elin." in choices(both)
    assert not west_road_predicament.available_commands(both.world_state, both.scene_snapshot)
    both.process_command("present Repeated Watch Tracks to Elin")
    assert "what Mara saw" in hint(both) and "what the tracks show" not in hint(both)
    assert "at the North Gate" not in hint(both)
    assert not west_road_predicament.available_commands(both.world_state, both.scene_snapshot)
    both.process_command("present Mara's Account to Elin")
    assert west_road_predicament.available_commands(both.world_state, both.scene_snapshot) == ["advocate patrol", "continue investigation"]
    assert "immediate patrol" in render(both) and "Keep the guards in place" in render(both)

    mixed = GameEngine(REGION)
    for command in ("go to Southwest Trade Road", "investigate", "talk to Mara", "go to North Gate", "present Repeated Watch Tracks to Grey", "present Mara's Account to Elin"):
        mixed.process_command(command)
    assert "what the tracks show" in hint(mixed) and "what Mara saw" not in hint(mixed)
    assert not west_road_predicament.available_commands(mixed.world_state, mixed.scene_snapshot)


def test_persistent_winter_wording_and_reentry():
    engine = GameEngine(REGION)
    assert not engine.get_player_perception()["pressure_cues"]
    original_weather = deepcopy(engine.world_state["weather"])
    engine.process_command("go to Southwest Trade Road")
    cue = engine.get_player_perception()["pressure_cues"][0]["text"]
    assert cue == "Bitter cold persists across the area."
    assert cue in render(engine)
    engine.process_command("go to North Gate")
    assert cue in render(engine)
    engine.process_command("go to Southwest Trade Road")
    assert cue in render(engine)
    assert "has become noticeably more severe" not in render(engine)
    assert engine.world_state["weather"] == original_weather
    assert engine.world_state["pressures"]["bryn_shander_winter"]["level"] == 70
    engine.set_pressure_level("bryn_shander_winter", 71)
    assert engine.get_player_perception()["pressure_cues"][0]["text"] == cue
    engine.process_command("go to Market Square")
    assert engine.get_player_perception()["pressure_cues"][0]["text"] == cue
    with artifact_files("test_west_road_presentation") as directory:
        path = Path(directory) / "winter_reentry.json"
        engine.save(str(path))
        loaded = GameEngine(REGION)
        loaded.load(str(path))
        assert loaded.get_world_state() == engine.get_world_state()
        assert loaded.get_player_perception()["pressure_cues"][0]["text"] == cue
        loaded.process_command("go to North Gate")
        assert cue in render(loaded)


def test_followup_display_language():
    engine = ready()
    engine.process_command("advocate patrol")
    text = render(engine)
    assert "Follow the watchers' fresh tracks" in text
    assert "Piece together the watchers' roadside positions" in text
    assert "Coordinate a survey with the committed guards" in text
    assert "one hour; the result is uncertain" in text and "2 hours; the guards can establish" in text
    assert "local observation circuit" not in text.replace("type 'reconstruct local observation circuit'", "")
    assert "road-focused coverage" not in text and "fresh withdrawal signs" not in text
    engine.process_command("pursue observers")
    assert "road-focused coverage" not in render(engine)
    assert "road-focused coverage" not in engine.get_resume_summary()[0]
    assert "The withdrawal route is known" in render(engine)
    assert "local pursuit" not in render(engine)


def test_report_recipient_feedback():
    preview = GameEngine(REGION)
    transcript = run_cli(preview, ["go to Southwest Trade Road", "investigate", "talk to Mara",
                                   "go to North Gate", "present Repeated Watch Tracks to Grey", "quit"])
    refreshed = transcript.split("Captain Darvin Grey hears the report.", 1)[1].split("Goodbye.", 1)[0]
    assert "What now?" in refreshed and "Use: present Repeated Watch Tracks to Elin" in refreshed
    assert refreshed.index("What now?") < refreshed.index("Other actions:")
    engine = GameEngine(REGION)
    for command in ("go to Southwest Trade Road", "investigate", "talk to Mara", "go to North Gate"):
        assert engine.process_command(command)["success"]
    grey = engine.process_command("present Repeated Watch Tracks to Grey")
    assert "Elin still needs this report" in grey["presentation"]["response_text"]
    assert not west_road_predicament.available_commands(engine.world_state, engine.scene_snapshot)
    elin = engine.process_command("present Repeated Watch Tracks to Elin")
    assert "Elin still needs this report" not in elin["presentation"]["response_text"]
    assert "observers' identity remains unknown" in elin["presentation"]["response_text"]
    assert not west_road_predicament.available_commands(engine.world_state, engine.scene_snapshot)
    assert "what Mara saw" in engine.get_narration()["current_choice_hint"]
    assert "at the North Gate" not in engine.get_narration()["current_choice_hint"]
    assert "Use: present Mara's Account to Elin." in engine.get_narration()["current_choice_hint"]
    engine.process_command("present Mara's Account to Elin")
    assert west_road_predicament.available_commands(engine.world_state, engine.scene_snapshot)
    late_grey = engine.process_command("present Mara's Account to Grey")
    assert "Elin still needs" not in late_grey["presentation"]["response_text"]


def test_conversation_result_composition():
    for target, actor in (("Grey", west_road_predicament.GREY), ("Elin", west_road_predicament.ELIN)):
        engine = GameEngine(REGION)
        expected = engine.region["west_road_predicament"]["actor_responses"][actor]["investigating"]
        text = run_cli(engine, ["talk to " + target, "quit"])
        assert text.count(expected) == 1
        assert "You begin a conversation." not in text and "Target: " not in text
    engine = GameEngine(REGION)
    text = run_cli(engine, ["go to Southwest Trade Road", "talk to Mara", "quit"])
    assert text.count("Mara reports seeing two observers") == 1
    assert "You begin a conversation." not in text and "Target: " not in text
    with patch.object(west_road_predicament, "actor_response", return_value=None):
        fallback = run_cli(GameEngine(REGION), ["talk to Grey", "quit"])
    assert "You begin a conversation." in fallback
    assert "Target: Captain Darvin Grey." in fallback
    from test_discovery_gated_relocated_actor_response import REGION as LEGACY_REGION, TEXT, resolve_and_arrive
    legacy = GameEngine(LEGACY_REGION)
    resolve_and_arrive(legacy, discover=True)
    gated = run_cli(legacy, ["talk to elin", "talk to elin", "quit"])
    assert gated.count(TEXT) == 1
    assert gated.count("You begin a conversation.") == 1  # Later conversation has no specific reply.
    assert gated.count("Target: Elin Voss.") == 1
    rejected = run_cli(GameEngine(REGION), ["talk to stranger", "quit"])
    assert "No matching target is present" in rejected


def test_followup_result_not_repeated_in_refresh():
    engine = ready()
    engine.process_command("advocate patrol")
    clue = next(d["text"] for d in engine.region["discovery_declarations"]
                if d["discovery_id"] == "west_road_withdrawal_route")
    text = run_cli(engine, ["pursue observers", "quit"])
    assert text.count(clue) == 1
    assert "Grey: The withdrawal route" in text and "Elin: The route from the road" in text
    assert "What now?\nThe withdrawal route is known" in text
    assert "west_road_withdrawal_route" in engine.world_state["player_discoveries"]
    from test_character_competence import withdrawn
    for command in ("follow withdrawal signs", "reconstruct local observation circuit", "arrange guarded local survey"):
        engine = withdrawn()
        with patch.object(character_competence, "draw_d6", return_value=5):
            text = run_cli(engine, [command, "quit"])
        assert text.count(clue) == 1
        assert "Grey values the information; Elin notes the cost" in text
        assert "What now?\nThe withdrawal route is known" in text
    for first, followup in (("advocate patrol", "restore coverage"),
                            ("continue investigation", "protect supply stop"),
                            ("continue investigation", "locate raiders")):
        engine = ready()
        engine.process_command(first)
        outcome = engine.region["west_road_predicament"]["phase_text"][
            west_road_predicament.COMMANDS[followup][1]]
        text = run_cli(engine, [followup, "quit"])
        assert text.count(outcome) == 1


def main():
    for test in (test_initial_and_evidence_presentation, test_branch_and_terminal_circumstances, test_no_repeat_after_invalid_or_no_op, test_refresh_after_material_actions, test_brief_resume_and_following_scene, test_choice_parity_and_plain_language, test_result_flow_and_replay, test_approach_aware_recap, test_specific_result_composition, test_investigating_guidance_stages, test_persistent_winter_wording_and_reentry, test_followup_display_language, test_report_recipient_feedback, test_conversation_result_composition, test_followup_result_not_repeated_in_refresh):
        test()
        print("PASS:", test.__name__)


if __name__ == "__main__":
    main()
