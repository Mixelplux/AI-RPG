"""Offline behavioral verification of the ordinary revised reference situation."""
import json
from contextlib import redirect_stdout
from io import StringIO
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import SAVE_VERSION, build_save_data, save_game
from engine.world_state import validate_world_state
from engine import west_road_predicament as west

REGION = "data/regions/bryn_shander.json"
OUTPUT = Path(".artifacts")


def expect_invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected rejected state/content.")


def ready():
    e = GameEngine(REGION)
    for command in ("go to Southwest Trade Road", "investigate", "talk to Mara", "go to North Gate", "present Repeated Watch Tracks to Elin", "present Mara's Account to Elin"):
        assert e.process_command(command)["success"], command
    assert e.world_state["west_road_predicament"]["phase"] == "investigating"
    return e


def assert_no_change(e, command):
    before = e.get_world_state()
    scene = e.scene_snapshot
    e.process_command(command)
    assert e.get_world_state() == before, command
    assert e.scene_snapshot is scene, command


def roundtrip(e, label):
    path = OUTPUT / ("west_road_" + label + ".json")
    try:
        save_game(e, str(path))
        loaded = GameEngine(REGION)
        loaded.load(str(path))
        assert loaded.get_world_state() == e.get_world_state()
        assert loaded.get_narration() == e.get_narration()
        assert loaded.get_resume_summary() == e.get_resume_summary()
        return loaded
    finally:
        path.unlink(missing_ok=True)


def test_evidence_and_prerequisites():
    e = GameEngine(REGION)
    assert set(e.get_world_state()["west_road_predicament"]) == {"phase", "last_outcome_history_id"}
    for command in west.COMMANDS:
        assert_no_change(e, command)
    roundtrip(e, "initial")
    assert e.process_command("talk to Grey")["actor_knowledge_response"]
    e.process_command("wait")
    assert e.world_state["west_road_predicament"]["phase"] == "investigating"
    assert {west.GREY, west.ELIN} <= set(e.scene_snapshot["entities"]["static"])
    e.process_command("go to Southwest Trade Road")
    discovery = e.process_command("investigate")["investigation"]
    assert discovery["changed"] and "not identity or an attack" in discovery["text"]
    assert_no_change(e, "investigate")
    assert_no_change(e, "continue investigation")
    e.process_command("talk to Mara")
    assert_no_change(e, "talk to Mara")
    assert set(e.get_player_discoveries()) == set(west.INITIAL_EVIDENCE)
    roundtrip(e, "evidence")
    e.process_command("go to North Gate")
    assert_no_change(e, "advocate patrol")
    e.process_command("present Repeated Watch Tracks to Elin")
    assert_no_change(e, "continue investigation")
    e.process_command("present Mara's Account to Elin")
    assert_no_change(e, "present Mara's Account to Elin")
    assert e.get_open_threads() == {} and e.world_state["resolved_threads"] == {}
    commands = west.available_commands(e.world_state, e.scene_snapshot)
    assert commands == ["advocate patrol", "continue investigation"]
    text = e.get_narration()["description"]
    assert all(c in text for c in commands) and "one hour" in text
    assert "watch guards" in text and "Elin Voss" in e.get_narration()["visible_entities"]
    roundtrip(e, "shared")
    e.set_actor_location(west.ELIN, "bryn_shander_gate_west")
    assert_no_change(e, "advocate patrol")


def test_all_outcomes():
    for initial, followups in (("advocate patrol", ("pursue observers", "restore coverage")), ("continue investigation", ("protect supply stop", "locate raiders"))):
        for followup in followups:
            e = ready()
            hours = e.world_state["time"].get("elapsed_hours", 0)
            r = e.process_command(initial)
            assert r["success"]
            assert e.world_state["time"]["elapsed_hours"] == hours + 1
            phase = west.COMMANDS[initial][1]
            assert e.world_state["west_road_predicament"]["phase"] == phase
            for command in west.COMMANDS:
                if command not in followups:
                    assert_no_change(e, command)
            assert set(west.available_commands(e.world_state, e.scene_snapshot)) == set(followups)
            assert e.process_command("talk to Grey")["actor_knowledge_response"]["text"] in r["message"]
            assert e.process_command("talk to Elin")["actor_knowledge_response"]["text"] in r["message"]
            if initial == "continue investigation":
                assert {"west_road_patrol_signs", "west_road_driver_account"} <= set(e.get_player_discoveries())
            else:
                assert "west_road_patrol_signs" not in e.get_player_discoveries()
            e = roundtrip(e, phase)
            hours = e.world_state["time"]["elapsed_hours"]
            assert e.process_command(followup)["success"]
            assert e.world_state["time"]["elapsed_hours"] == hours
            phase = west.COMMANDS[followup][1]
            assert e.world_state["west_road_predicament"]["phase"] == phase
            for command in west.COMMANDS:
                assert_no_change(e, command)
            assert not west.available_commands(e.world_state, e.scene_snapshot)
            assert "broader threat remains unresolved" in e.get_narration()["description"]
            recap = " ".join(e.get_resume_summary())
            assert ("You advocated immediate patrol action" if initial == "advocate patrol" else "You chose one more hour of investigation") in recap
            assert "Choose:" not in recap
            assert len([h for h in e.get_history() if h["event_type"] == "west_road_commitment"]) == 2
            roundtrip(e, phase)


def test_atomic_failures():
    for initial in ("advocate patrol", "continue investigation"):
        for target in ("engine.game_engine.validate_world_state", "engine.game_engine.build_scene", "engine.game_engine.GameEngine._prepare_time_advance_candidate"):
            e = ready()
            before = e.get_world_state()
            world, scene = e.world_state, e.scene_snapshot
            with patch(target, side_effect=RuntimeError("injected failure")):
                try:
                    e.process_command(initial)
                except RuntimeError:
                    pass
                else:
                    raise AssertionError("Injected failure not reached")
            assert e.get_world_state() == before
            assert e.world_state is world and e.scene_snapshot is scene
    e = ready()
    before = e.get_world_state()
    with patch.object(e, "_acquire_west_road_discovery", side_effect=RuntimeError("after time preparation")):
        try:
            e.process_command("continue investigation")
        except RuntimeError:
            pass
        else:
            raise AssertionError("Expected consequence failure")
    assert e.get_world_state() == before
    for initial, followup in (("advocate patrol", "pursue observers"), ("continue investigation", "locate raiders")):
        e = ready(); e.process_command(initial)
        before = e.get_world_state()
        with patch("engine.game_engine.build_scene", side_effect=RuntimeError("follow-up scene")):
            try:
                e.process_command(followup)
            except RuntimeError:
                pass
        assert e.get_world_state() == before


def test_integrity_and_copies():
    e = ready(); e.process_command("continue investigation")
    valid = e.get_world_state()
    for phase in ("investigating", "observers_withdrew", "unknown"):
        bad = deepcopy(valid); bad["west_road_predicament"]["phase"] = phase
        expect_invalid(lambda: validate_world_state(bad, e.region))
    bad = deepcopy(valid); bad["west_road_predicament"]["last_outcome_history_id"] = "missing"
    expect_invalid(lambda: validate_world_state(bad, e.region))
    bad = deepcopy(valid); bad["player_discoveries"].remove("west_road_patrol_signs")
    expect_invalid(lambda: validate_world_state(bad, e.region))
    bad = deepcopy(valid); bad["history"][-1]["source_history_id"] = bad["history"][-1]["history_id"]
    expect_invalid(lambda: validate_world_state(bad, e.region))
    bad = deepcopy(valid); bad["history"][-1]["witness_entity_ids"] = [west.ELIN]
    expect_invalid(lambda: validate_world_state(bad, e.region))
    bad = deepcopy(valid); bad["actor_knowledge"][west.ELIN].remove(west.shared_id(west.INITIAL_EVIDENCE[0]))
    expect_invalid(lambda: validate_world_state(bad, e.region))
    bad = deepcopy(valid); bad["evidence_traces"][0]["evidence_id"] = "different"
    expect_invalid(lambda: validate_world_state(bad, e.region))
    bad = deepcopy(valid)
    time_event = next(h for h in bad["history"] if h.get("source_history_id") and h["event_type"] == "time_advanced")
    del time_event["new_time"]
    expect_invalid(lambda: validate_world_state(bad, e.region))
    returned = e.get_world_state(); returned["west_road_predicament"]["phase"] = "unknown"
    resume = e.get_resume_summary(); resume.clear()
    narration = e.get_narration(); narration["description"] = "changed"
    assert e.get_world_state() == valid and e.get_resume_summary()
    text = e.get_narration()["description"] + " ".join(e.get_resume_summary())
    for internal in (west.GREY, west.ELIN, "history_", "west_road_received:", "Project-authored"):
        assert internal not in text
    bad_region = deepcopy(e.region); del bad_region["west_road_predicament"]["phase_text"]["wagon_intercepted"]
    expect_invalid(lambda: validate_region(bad_region))
    # Save construction also rejects an inconsistent current scenario before writing.
    e.world_state["west_road_predicament"]["phase"] = "investigating"
    expect_invalid(lambda: build_save_data(e))


def test_old_save_rejection():
    legacy = GameEngine("test_fixtures/bryn_shander_legacy.json")
    legacy.process_command("talk to captain")
    legacy.process_command("investigate")
    legacy.process_command("present The Captain's Deliberate Trail to captain")
    payload = build_save_data(legacy); payload["region_path"] = REGION
    path = OUTPUT / "west_road_old_save.json"
    original = json.dumps(payload).encode("utf-8")
    path.write_bytes(original)
    try:
        active = ready(); before = active.get_world_state(); scene = active.scene_snapshot
        try:
            active.load(str(path))
        except ValueError as error:
            assert str(error) == west.OLD_SAVE_MESSAGE
        else:
            raise AssertionError("Old save accepted")
        assert active.get_world_state() == before and active.scene_snapshot is scene
        assert path.read_bytes() == original
    finally:
        path.unlink(missing_ok=True)


def test_cli_smoke():
    import play_game
    for initial, followup in (("advocate patrol", "restore coverage"), ("continue investigation", "protect supply stop")):
        path = OUTPUT / "west_road_cli_save.json"
        commands = ["go to Southwest Trade Road", "investigate", "talk to Mara", "go to North Gate", "present Repeated Watch Tracks to Elin", "present Mara's Account to Elin", initial, "save", "load", followup, "quit"]
        output = StringIO()
        try:
            with patch("builtins.input", side_effect=commands), patch.object(play_game, "SAVE_PATH", str(path)), redirect_stdout(output):
                play_game.main()
            text = output.getvalue()
            assert "Game loaded." in text and "Previously:" in text
            assert "broader threat remains unresolved" in text
            assert "Time advanced: 1 hour." in text
            for internal in ("[Intent:", "Project-authored", "elapsed_hours", "west_road_received:", "history_"):
                assert internal not in text
        finally:
            path.unlink(missing_ok=True)


def main():
    assert SAVE_VERSION == 1
    for test in (test_evidence_and_prerequisites, test_all_outcomes, test_atomic_failures, test_integrity_and_copies, test_old_save_rejection, test_cli_smoke):
        test()
        print("PASS:", test.__name__)


if __name__ == "__main__":
    main()
