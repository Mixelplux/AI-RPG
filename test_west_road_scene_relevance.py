"""Offline regressions for local scene presentation of persistent West-Road state."""
import json
from pathlib import Path
from unittest.mock import patch

from engine import character_competence as competence
from engine.save_system import load_game, save_game
from engine.west_road_presentation import CURRENT_CIRCUMSTANCES, CURRENT_CHOICE_HINTS
from test_artifact_files import artifact_files
from test_character_competence import withdrawn
from test_west_road_market_theft import incident, partial


def cases():
    for label, tag, command in (
        ("ordinary", None, "arrange guarded local survey"),
        ("tactical", "tactical_assessment", "arrange guarded local survey"),
        ("pursuit", None, "pursue observers"),
        ("pursuit_after_threshold", None, "pursue observers"),
        ("partial", None, "follow withdrawal signs"),
        ("restored", None, "restore coverage"),
    ):
        engine = withdrawn(tag)
        if label == "restored":
            partial(engine, "follow withdrawal signs")
        if label == "partial":
            partial(engine, command)
        else:
            assert engine.process_command(command)["success"]
        if label == "restored":
            engine.advance_time(3)
        if label == "pursuit_after_threshold":
            engine.advance_time(2)
        theft_occurred = label in ("ordinary", "pursuit_after_threshold")
        assert bool(incident(engine)) == theft_occurred, label
        yield label, engine, theft_occurred


def assert_market(engine, theft_occurred):
    before, scene = engine.get_world_state(), engine.scene_snapshot
    phase = before["west_road_predicament"]["phase"]
    with patch.object(competence, "draw_d6", side_effect=AssertionError("scene read drew")):
        for _ in range(3):
            text = engine.get_narration()["description"]
            assert "Market Square" in engine.get_narration()["title"]
            assert ("lamp oil" in text) == theft_occurred
            assert ("lamp oil" in engine.get_current_scene_projection()["location"]["description"]) == theft_occurred
            assert bool(incident(engine)) == theft_occurred
            assert all(value not in text for value in CURRENT_CIRCUMSTANCES.values())
            assert all(value not in text for value in CURRENT_CHOICE_HINTS.values())
            for packet in (
                engine.get_competence_projection(),
                engine.get_player_perception()["character_competence"],
                engine.get_current_scene_projection()["character_competence"],
                engine.get_narration_context("look")["scene_snapshot"]["character_competence"],
            ):
                assert all(packet[layer] == [] for layer in (
                    "observations", "recognition", "findings", "approaches", "accepted_outcomes"
                ))
            context = json.dumps(engine.get_narration_context("look"))
            for remote in ("abandoned lookout", "withdrawal route", "local pursuit is complete"):
                assert remote not in text.lower() and remote not in context.lower()
    assert engine.get_world_state() == before and engine.scene_snapshot is scene
    assert engine.world_state["west_road_predicament"]["phase"] == phase


def test_market_projection_and_return():
    for label, engine, theft_occurred in cases():
        before = engine.get_world_state()
        discovery_ids = engine.get_player_discoveries()
        assert discovery_ids == tuple(before["player_discoveries"])
        clues = engine.get_known_clues()
        expected_clues = tuple(
            {"title": declaration["title"], "text": declaration["text"]}
            for declaration in engine.region["discovery_declarations"]
            if declaration["discovery_id"] in discovery_ids
        )
        assert clues == expected_clues and clues
        local_packet = engine.get_competence_projection()
        assert engine.process_command("go to Market Square")["success"]
        after = engine.get_world_state()
        for field in ("west_road_predicament", "west_road_market_theft", "competence_attempts",
                      "player_discoveries", "actor_knowledge", "time"):
            assert after[field] == before[field], (label, field)
        assert_market(engine, theft_occurred)
        # Explicit persistent review and resume continue to expose accepted facts.
        assert engine.get_player_discoveries() == discovery_ids
        assert engine.get_known_clues() == expected_clues
        assert engine.get_resume_summary()
        assert engine.process_command("go to North Gate")["success"]
        assert engine.get_competence_projection() == local_packet
        phase = engine.world_state["west_road_predicament"]["phase"]
        assert CURRENT_CIRCUMSTANCES[phase] in engine.get_narration()["description"]
        assert engine.process_command("go to Southwest Trade Road")["success"]
        assert CURRENT_CIRCUMSTANCES[phase] in engine.get_narration()["description"]
        assert engine.get_competence_projection()["findings"] == local_packet["findings"]


def test_market_save_load_projection():
    with artifact_files("west_road_scene_relevance") as root:
        for label, engine, theft_occurred in cases():
            assert engine.process_command("go to Market Square")["success"]
            path = Path(root) / ("west_road_scene_relevance_" + label + ".json")
            save_game(engine, str(path))
            saved = path.read_bytes()
            loaded = load_game(str(path))
            assert loaded.get_world_state() == engine.get_world_state()
            assert loaded.get_known_clues() == engine.get_known_clues()
            assert_market(loaded, theft_occurred)
            assert path.read_bytes() == saved
            assert loaded.process_command("go to North Gate")["success"]
            phase = loaded.world_state["west_road_predicament"]["phase"]
            assert CURRENT_CIRCUMSTANCES[phase] in loaded.get_narration()["description"]


if __name__ == "__main__":
    for test in (test_market_projection_and_return, test_market_save_load_projection):
        test()
        print("PASS:", test.__name__)
