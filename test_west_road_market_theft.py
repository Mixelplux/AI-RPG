"""Offline causal, compatibility, transaction and player-projection regressions."""

import json
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from engine import character_competence as competence
from engine import west_road_market_theft as theft
from engine.game_engine import GameEngine
from engine.narration_prompt import build_narration_prompt_packet
from engine.narration_request import build_narration_request_packet
from engine.save_system import SAVE_VERSION, build_save_data, load_game, save_game
from engine.world_state import validate_world_state
from test_artifact_files import artifact_files
from test_character_competence import withdrawn
from test_west_road_predicament import expect_invalid, ready

REGION = "data/regions/bryn_shander.json"


def incident(engine):
    events = [e for e in engine.get_history() if e["event_type"] == theft.EVENT_TYPE]
    record = engine.world_state[theft.STATE_KEY]
    assert len(events) <= 1
    assert record["theft_history_id"] == (events[0]["history_id"] if events else None)
    return events[0] if events else None


def partial(engine, command):
    with patch.object(competence, "draw_d6", return_value=3):
        result = engine.process_command(command)
    assert result["success"] and result["accepted_outcome"]["result"] == "partial"


def test_ordinary_and_tactical_headroom():
    ordinary = withdrawn()
    tactical = withdrawn("tactical_assessment")
    start = ordinary.world_state["time"]["elapsed_hours"]
    assert start == tactical.world_state["time"]["elapsed_hours"]
    assert ordinary.world_state[theft.STATE_KEY] == tactical.world_state[theft.STATE_KEY]
    assert ordinary.world_state[theft.STATE_KEY]["coverage_started_elapsed_hours"] == start
    assert not incident(ordinary) and not incident(tactical)
    for engine, cost in ((ordinary, 2), (tactical, 1)):
        result = engine.process_command("arrange guarded local survey")
        assert result["success"] and result["accepted_outcome"]["cost_hours"] == cost
        assert engine.world_state["time"]["elapsed_hours"] == start + cost
        assert engine.world_state["west_road_predicament"]["phase"] == "withdrawal_route_found"
    assert incident(ordinary)["time"]["elapsed_hours"] == start + 2
    assert not incident(tactical)
    assert tactical.process_command("wait")["success"]
    assert incident(tactical)["time"]["elapsed_hours"] == start + 2
    assert ordinary.world_state["player_discoveries"] == tactical.world_state["player_discoveries"]
    # No quest/thread or new actor knowledge comes from the independent incident.
    assert ordinary.world_state["open_threads"] == tactical.world_state["open_threads"] == {}
    assert ordinary.world_state["actor_knowledge"] == tactical.world_state["actor_knowledge"]


def test_composed_activities_and_timed_navigation():
    engine = withdrawn()
    start = engine.world_state["time"]["elapsed_hours"]
    partial(engine, "follow withdrawal signs")
    assert not incident(engine)
    partial(engine, "reconstruct local observation circuit")
    assert incident(engine)["time"]["elapsed_hours"] == start + 2
    assert engine.world_state["west_road_predicament"]["phase"] == "observers_withdrew"
    assert "arrange guarded local survey" not in engine.world_state["competence_attempts"]
    engine = withdrawn()
    partial(engine, "follow withdrawal signs")
    assert engine.process_command("go to Southwest Trade Road")["success"]
    assert incident(engine)
    assert engine.world_state["player"]["current_location_id"] != theft.MARKET


def test_restoration_and_nonqualifying_time():
    engine = withdrawn()
    partial(engine, "follow withdrawal signs")
    assert not incident(engine)
    assert engine.process_command("restore coverage")["success"]
    assert engine.world_state[theft.STATE_KEY]["coverage_started_elapsed_hours"] is None
    engine.advance_time(5)
    assert not incident(engine)
    assert engine.process_command("go to Market Square")["success"]
    assert theft.INCIDENT_TEXT not in engine.get_narration()["description"]
    for engine in (ready(), GameEngine(REGION)):
        engine.advance_time(5)
        assert not incident(engine)
    engine = ready()
    assert engine.process_command("continue investigation")["success"]
    engine.advance_time(5)
    assert not incident(engine)
    # Restoration after occurrence ends timing but preserves the established event.
    engine = withdrawn()
    engine.advance_time(2)
    established = incident(engine)
    assert engine.process_command("restore coverage")["success"]
    engine.advance_time(5)
    assert incident(engine) == established


def test_large_time_step_and_idempotence():
    engine = withdrawn()
    start = engine.world_state["time"]["elapsed_hours"]
    engine.advance_time(5)
    established = incident(engine)
    assert established["time"]["elapsed_hours"] == start + 2
    source = engine.get_history_entry_by_id(established["source_history_id"])
    assert source["new_time"]["elapsed_hours"] == start + 5
    engine.advance_time(3)
    assert incident(engine) == established
    engine = withdrawn()
    engine.process_command("arrange guarded local survey")
    before = engine.get_world_state()
    assert not engine.process_command("arrange guarded local survey")["changed"]
    assert engine.get_world_state() == before


def test_interval_helper_restarts_without_reusing_old_hours():
    engine = withdrawn()
    engine.advance_time(1)
    assert engine.process_command("restore coverage")["success"]
    engine.advance_time(1)
    assert not incident(engine)
    assert not engine.process_command("advocate patrol")["success"]
    # Gameplay has no second allocation branch after restoration. Test the
    # specific transition helper in isolation without inventing a command.
    candidate = engine.get_world_state()
    candidate["west_road_predicament"]["phase"] = "observers_withdrew"
    theft.allocation_changed(candidate, was_reduced=False)
    fresh_start = candidate["time"]["elapsed_hours"]
    assert candidate[theft.STATE_KEY]["coverage_started_elapsed_hours"] == fresh_start
    candidate["time"]["elapsed_hours"] += 1
    theft.allocation_changed(candidate, was_reduced=True)
    assert candidate[theft.STATE_KEY]["coverage_started_elapsed_hours"] == fresh_start


def test_occurrence_elsewhere_does_not_grant_player_knowledge():
    engine = withdrawn()
    knowledge = deepcopy(engine.world_state["actor_knowledge"])
    discoveries = list(engine.get_player_discoveries())
    engine.advance_time(2)
    assert incident(engine) and engine.world_state["player"]["current_location_id"] != theft.MARKET
    before, scene = engine.get_world_state(), engine.scene_snapshot
    for packet in (engine.get_narration(), engine.get_player_perception(),
                   engine.get_current_scene_projection(), engine.get_narration_context("look around"),
                   engine.get_known_clues(), engine.get_resume_summary()):
        assert "lamp oil" not in repr(packet)
    assert engine.world_state["actor_knowledge"] == knowledge
    assert list(engine.get_player_discoveries()) == discoveries
    assert engine.get_world_state() == before and engine.scene_snapshot is scene


def test_observation_and_safe_local_revelation():
    engine = withdrawn("tactical_assessment")
    engine.process_command("arrange guarded local survey")
    assert engine.process_command("go to Market Square")["success"]
    assert not incident(engine)
    assert theft.INCIDENT_TEXT not in engine.get_narration()["description"]
    # It happens during time advancement even when no later scene is visited.
    engine.process_command("wait")
    established = incident(engine)
    before, scene = engine.get_world_state(), engine.scene_snapshot
    region_before = deepcopy(engine.region)
    for _ in range(3):
        assert theft.INCIDENT_TEXT in engine.get_narration()["description"]
        finding_text = next(d["text"] for d in engine.region["discovery_declarations"] if d["discovery_id"] == "west_road_withdrawal_route")
        assert finding_text not in engine.get_narration()["description"]
        assert any(clue["text"] == finding_text for clue in engine.get_known_clues())
        assert theft.INCIDENT_TEXT in engine.get_current_scene_projection()["location"]["description"]
        assert theft.INCIDENT_TEXT in engine.get_player_perception()["visible"]["location"]["description_seed"]
        context = engine.get_narration_context("look around")
        assert theft.INCIDENT_TEXT in context["scene_snapshot"]["location"]["description_seed"]
        assert theft.NARRATION_LIMIT in context["boundary"]["drift_guardrail"]
        prompt = build_narration_prompt_packet(build_narration_request_packet(context))
        assert theft.INCIDENT_TEXT in repr(prompt) and theft.NARRATION_LIMIT in repr(prompt)
        assert engine.get_world_state() == before and engine.scene_snapshot is scene
    assert engine.region == region_before
    assert "observers" not in theft.INCIDENT_TEXT.lower()
    for internal in ("consequence triggered", "supported finding", "limited inference", theft.STATE_KEY, "Narration cannot", "Full:"):
        assert internal not in engine.get_narration()["description"]
    assert engine.process_command("go to North Gate")["success"]
    assert engine.get_narration()["description"].count(finding_text) == 1
    assert theft.INCIDENT_TEXT not in engine.get_narration()["description"]
    assert theft.INCIDENT_TEXT not in repr(engine.get_narration_context("look around"))
    for _ in range(2):
        assert engine.process_command("go to Market Square")["success"]
        assert incident(engine) == established
        assert engine.get_narration()["description"].count(theft.INCIDENT_TEXT) == 1
        assert engine.process_command("go to North Gate")["success"]
    assert engine.world_state["open_threads"] == before["open_threads"] == {}


def test_save_load_before_after_and_restoration():
    with artifact_files("market_theft_roundtrip") as root:
        path = Path(root) / "market_theft_roundtrip_save.json"
        engine = withdrawn("tactical_assessment")
        engine.process_command("arrange guarded local survey")
        assert not incident(engine)
        save_game(engine, str(path))
        original = path.read_bytes()
        loaded = load_game(str(path))
        assert SAVE_VERSION == 1 and loaded.get_world_state() == engine.get_world_state()
        assert original == path.read_bytes() and not incident(loaded)
        loaded.process_command("wait")
        established = incident(loaded)
        save_game(loaded, str(path))
        after = load_game(str(path))
        assert after.get_world_state() == loaded.get_world_state()
        after.advance_time(3)
        assert incident(after) == established
        # An ended sub-threshold interval also round-trips without later accumulation.
        engine = withdrawn()
        partial(engine, "follow withdrawal signs")
        engine.process_command("restore coverage")
        save_game(engine, str(path))
        loaded = load_game(str(path))
        loaded.advance_time(3)
        assert not incident(loaded)
        # A theft with restored coverage remains established after reload as well.
        engine = withdrawn()
        engine.advance_time(2)
        engine.process_command("restore coverage")
        save_game(engine, str(path))
        loaded = load_game(str(path))
        assert loaded.get_world_state() == engine.get_world_state()
        loaded.advance_time(3)
        assert incident(loaded) == incident(engine)


def test_legacy_normalization_without_retroactive_theft():
    with artifact_files("market_theft_legacy") as root:
        path = Path(root) / "market_theft_legacy_save.json"
        for kind in ("initial", "withdrawn", "pursued", "restored"):
            engine = GameEngine(REGION) if kind == "initial" else withdrawn()
            if kind == "pursued":
                engine.process_command("pursue observers")
            elif kind == "restored":
                engine.process_command("restore coverage")
            data = build_save_data(engine)
            del data["world_state"][theft.STATE_KEY]
            # Genuine legacy state can be well past the new threshold, with no incident.
            data["world_state"]["time"]["elapsed_hours"] = data["world_state"]["time"].get("elapsed_hours", 0) + 7
            path.write_text(json.dumps(data), encoding="utf-8")
            source = path.read_bytes()
            loaded = load_game(str(path))
            assert not incident(loaded) and source == path.read_bytes()
            start = loaded.world_state["time"]["elapsed_hours"]
            assert loaded.world_state[theft.STATE_KEY]["coverage_started_elapsed_hours"] == (start if kind in ("withdrawn", "pursued") else None)
            loaded.advance_time(1)
            assert not incident(loaded)
            loaded.advance_time(1)
            assert bool(incident(loaded)) == (kind in ("withdrawn", "pursued"))


def test_malformed_fields_reject_and_failed_load_preserves_session():
    active = ready()
    before, world, scene = active.get_world_state(), active.world_state, active.scene_snapshot
    one_hour = withdrawn()
    partial(one_hour, "follow withdrawal signs")
    occurred = withdrawn()
    occurred.advance_time(2)
    with artifact_files("market_theft_invalid") as root:
        path = Path(root) / "market_theft_invalid_save.json"
        bad_states = []
        for record in (None, [], {}, {"coverage_started_elapsed_hours": None}, {"extra": 1}):
            data = build_save_data(one_hour)
            data["world_state"][theft.STATE_KEY] = record
            bad_states.append(data)
        for start in (None, True, -1, 1.5, "2", one_hour.world_state["time"]["elapsed_hours"] + 1):
            data = build_save_data(one_hour)
            data["world_state"][theft.STATE_KEY]["coverage_started_elapsed_hours"] = start
            bad_states.append(data)
        for reference in (False, 1, "missing"):
            data = build_save_data(one_hour)
            data["world_state"][theft.STATE_KEY]["theft_history_id"] = reference
            bad_states.append(data)
        for change in ("remove_record", "erase_reference", "remove_event", "duplicate_event", "wrong_time", "malformed_time", "wrong_summary", "wrong_source", "unsupported_identity", "mismatched_start"):
            data = build_save_data(occurred)
            state = data["world_state"]
            event = next(e for e in state["history"] if e["event_type"] == theft.EVENT_TYPE)
            if change == "remove_record":
                del state[theft.STATE_KEY]
            elif change == "erase_reference":
                state[theft.STATE_KEY]["theft_history_id"] = None
            elif change == "remove_event":
                state["history"].remove(event)
            elif change == "duplicate_event":
                state["history"].append({**deepcopy(event), "history_id": "history_999999"})
            elif change == "wrong_time":
                event["time"]["elapsed_hours"] -= 1
            elif change == "malformed_time":
                event["time"] = None
            elif change == "wrong_summary":
                event["summary"] = "The observers stole the crate."
            elif change == "wrong_source":
                event["source_history_id"] = state["history"][0]["history_id"]
            elif change == "unsupported_identity":
                event["thief"] = "West-Road observers"
            elif change == "mismatched_start":
                event["coverage_started_elapsed_hours"] -= 1
            bad_states.append(data)
        for data in bad_states:
            path.write_text(json.dumps(data), encoding="utf-8")
            source = path.read_bytes()
            expect_invalid(lambda: active.load(str(path)))
            assert source == path.read_bytes() and active.get_world_state() == before
            assert active.world_state is world and active.scene_snapshot is scene
        # A well-formed save can still fail during derived-scene construction.
        save_game(occurred, str(path))
        source = path.read_bytes()
        with patch("engine.game_engine.build_scene", side_effect=RuntimeError("injected load scene failure")):
            try:
                active.load(str(path))
            except RuntimeError:
                pass
            else:
                raise AssertionError("Expected load scene failure")
        assert source == path.read_bytes() and active.get_world_state() == before
        assert active.world_state is world and active.scene_snapshot is scene


def test_command_and_scene_failure_rollback():
    for boundary in ("engine.game_engine.validate_world_state", "engine.game_engine.build_scene"):
        for command in ("arrange guarded local survey", "wait"):
            engine = withdrawn()
            if command == "wait":
                partial(engine, "follow withdrawal signs")
            before, world, scene = engine.get_world_state(), engine.world_state, engine.scene_snapshot
            with patch(boundary, side_effect=RuntimeError("injected publish failure")):
                try:
                    engine.process_command(command)
                except RuntimeError:
                    pass
                else:
                    raise AssertionError("Expected publish failure")
            assert engine.get_world_state() == before and not incident(engine)
            assert engine.world_state is world and engine.scene_snapshot is scene
    engine = withdrawn()
    before = engine.get_world_state()
    for command in ("advocate patrol", "identify thief", "go to Unauthored Market"):
        assert not engine.process_command(command)["success"]
        assert engine.get_world_state() == before
    # Incident created before a later discovery error must still roll back.
    with patch.object(engine, "_acquire_west_road_discovery", side_effect=RuntimeError("injected discovery failure")):
        try:
            engine.process_command("arrange guarded local survey")
        except RuntimeError:
            pass
        else:
            raise AssertionError("Expected discovery failure")
    assert engine.get_world_state() == before and not incident(engine)
    validate_world_state(engine.get_world_state(), engine.region)


def test_malformed_load_inputs_reject_without_ending_cli_session():
    import play_game

    active = ready()
    before, world, scene = active.get_world_state(), active.world_state, active.scene_snapshot
    base = build_save_data(withdrawn())
    with artifact_files("market_theft_load_shapes") as root:
        path = Path(root) / "market_theft_load_shapes_save.json"
        for legacy in (False, True):
            for field, value in (
                ("west_road_predicament", None),
                ("west_road_predicament", {"phase": []}),
                ("time", None),
                ("time", {"elapsed_hours": True}),
                ("history", [None]),
            ):
                data = deepcopy(base)
                if legacy:
                    del data["world_state"][theft.STATE_KEY]
                data["world_state"][field] = value
                path.write_text(json.dumps(data), encoding="utf-8")
                source = path.read_bytes()
                expect_invalid(lambda: active.load(str(path)))
                assert source == path.read_bytes() and active.get_world_state() == before
                assert active.world_state is world and active.scene_snapshot is scene
        output = StringIO()
        with patch("builtins.input", side_effect=["load", "quit"]), patch.object(play_game, "SAVE_PATH", str(path)), redirect_stdout(output):
            play_game.main()
        assert "Could not load saved game:" in output.getvalue()
        assert "Goodbye." in output.getvalue()


def test_cli_causal_comparisons_and_save_load_fiction():
    import play_game

    cases = (
        ("ordinary", None, ["arrange guarded local survey", "save", "load", "go to Market Square", "save", "load", "quit"], True),
        ("tactical", "tactical_assessment", ["arrange guarded local survey", "save", "load", "go to Market Square", "wait", "save", "load", "quit"], True),
        ("restored", None, ["wait", "restore coverage", "save", "load", "wait", "wait", "go to Market Square", "quit"], False),
    )
    with artifact_files("market_theft_cli") as root:
        for label, tag, commands, should_occur in cases:
            engine = withdrawn(tag)
            output = StringIO()
            inputs = iter(commands)

            def next_input(prompt):
                command = next(inputs)
                if command == "go to Market Square" or (label == "tactical" and command == "wait"):
                    assert "lamp oil" not in output.getvalue()
                return command

            path = Path(root) / ("market_theft_cli_" + label + ".json")
            with patch.object(GameEngine, "start_new", return_value=engine), patch("builtins.input", side_effect=next_input), patch.object(play_game, "SAVE_PATH", str(path)), redirect_stdout(output):
                play_game.main()
            text = output.getvalue()
            assert "Game loaded." in text and "Goodbye." in text
            assert (theft.INCIDENT_TEXT in text) == should_occur
            assert bool(incident(engine)) == should_occur
            for diagnostic in ("supported finding", "limited inference", "consequence triggered", theft.STATE_KEY):
                assert diagnostic not in text


if __name__ == "__main__":
    for test in (
        test_ordinary_and_tactical_headroom,
        test_composed_activities_and_timed_navigation,
        test_restoration_and_nonqualifying_time,
        test_large_time_step_and_idempotence,
        test_interval_helper_restarts_without_reusing_old_hours,
        test_occurrence_elsewhere_does_not_grant_player_knowledge,
        test_observation_and_safe_local_revelation,
        test_save_load_before_after_and_restoration,
        test_legacy_normalization_without_retroactive_theft,
        test_malformed_fields_reject_and_failed_load_preserves_session,
        test_command_and_scene_failure_rollback,
        test_malformed_load_inputs_reject_without_ending_cli_session,
        test_cli_causal_comparisons_and_save_load_fiction,
    ):
        test()
        print("PASS:", test.__name__)
