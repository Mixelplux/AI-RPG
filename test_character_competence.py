"""Offline West-Road competence, causal, transaction and compatibility checks."""
import json
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine import character_competence as competence
from engine import west_road_predicament as west
from engine.save_system import build_save_data, save_game, load_game
from engine.world_state import validate_world_state
from test_west_road_predicament import ready, expect_invalid

REGION = "data/regions/bryn_shander.json"
PATH = Path(".artifacts/character_competence_save.json")


def withdrawn(tag=None):
    e = ready()
    state = e.get_world_state()
    state["player"]["competences"] = [] if tag is None else [tag]
    e = GameEngine(REGION, initial_world_state=state)
    assert e.process_command("advocate patrol")["success"]
    return e


def test_profiles_and_read_only():
    packets = []
    for tag in (None, "tactical_assessment", "outdoor_tracking", "surveillance_analysis"):
        e = withdrawn(tag)
        before = e.get_world_state()
        scene = e.scene_snapshot
        with patch.object(competence, "draw_d6", side_effect=AssertionError("query drew")):
            for _ in range(3):
                packet = e.get_competence_projection()
                assert e.get_current_scene_projection()["character_competence"] == packet
                assert e.get_player_perception()["character_competence"] == packet
                assert e.get_narration_context("look")["scene_snapshot"]["character_competence"] == packet
                text = e.get_narration()["description"]
                assert all(a["command"] in text for a in packet["approaches"])
        assert e.get_world_state() == before and e.scene_snapshot is scene
        assert len(packet["approaches"]) == 3
        assert len(packet["recognition"]) == (0 if tag is None else 1)
        assert packet["findings"] == []
        assert "pursue observers" in text and "restore coverage" in text
        survey = next(a for a in packet["approaches"] if a["command"] == "arrange guarded local survey")
        assert survey["cost_hours"] == (1 if tag == "tactical_assessment" else 2)
        packets.append(packet)
    assert len({json.dumps(p, sort_keys=True) for p in packets}) == 4
    e = GameEngine(REGION)
    e.world_state["player"]["competences"] = list(competence.TAGS)
    assert not e.get_competence_projection()["recognition"]
    for command in competence.OPERATIONS:
        assert not e.process_command(command)["success"]


def test_all_draws_and_profiles():
    for command, (relevant, finding) in competence.OPERATIONS.items():
        if finding is None:
            continue
        for tag in (None, "tactical_assessment", "outdoor_tracking", "surveillance_analysis"):
            for draw in range(1, 7):
                e = withdrawn(tag)
                before = e.get_world_state()
                with patch.object(competence, "draw_d6", return_value=draw) as rng:
                    result = e.process_command(command)
                    rng.assert_called_once_with()
                attempt = result["accepted_outcome"]
                expected = ("partial" if draw <= 2 else "full") if tag == relevant else ("failure" if draw <= 2 else "partial" if draw <= 4 else "full")
                assert result["success"] and attempt["result"] == expected
                assert attempt["draw"] == draw and attempt["cost_hours"] == 1
                assert e.world_state["time"]["elapsed_hours"] == before["time"]["elapsed_hours"] + 1
                if expected == "full":
                    assert e.world_state["west_road_predicament"]["phase"] == "withdrawal_route_found"
                    assert attempt["findings"] == ["west_road_withdrawal_route"]
                else:
                    assert e.world_state["west_road_predicament"]["phase"] == "observers_withdrew"
                    assert "west_road_withdrawal_route" not in e.get_player_discoveries()
                    assert attempt["findings"] == ([finding] if expected == "partial" else [])
                    if expected == "failure":
                        assert set(e.get_player_discoveries()) == set(before["player_discoveries"])
                    assert command not in [a["command"] for a in e.get_competence_projection()["approaches"]]
                    assert len(e.get_competence_projection()["approaches"]) == 2
                validate_world_state(e.get_world_state(), e.region)
                accepted = e.get_world_state()
                with patch.object(competence, "draw_d6", side_effect=AssertionError("repeat drew")):
                    repeat = e.process_command(command)
                assert repeat["accepted_outcome"] == attempt and not repeat["changed"]
                assert e.get_world_state() == accepted


def test_survey_guards_alternates_and_limits():
    for tag in (None, "tactical_assessment", "outdoor_tracking", "surveillance_analysis"):
        e = withdrawn(tag)
        before = e.get_world_state()
        with patch.object(competence, "draw_d6", side_effect=AssertionError("survey drew")):
            r = e.process_command("arrange guarded local survey")
        assert r["accepted_outcome"]["result"] == "full"
        assert r["accepted_outcome"]["draw"] is None
        assert e.world_state["time"]["elapsed_hours"] - before["time"]["elapsed_hours"] == (1 if tag == "tactical_assessment" else 2)
    for actor in (west.GREY, west.ELIN):
        e = withdrawn(); e.set_actor_location(actor, "bryn_shander_gate_west")
        before = e.get_world_state()
        assert not competence.assess(e.region, e.world_state, e.scene_snapshot, "arrange guarded local survey")["eligible"]
        assert not e.process_command("arrange guarded local survey")["success"]
        assert e.get_world_state() == before
        # Existing outcome reporting remains coordinated at the gate.
        assert not e.get_competence_projection()["approaches"]
        assert not e.process_command("follow withdrawal signs")["success"]
    e = withdrawn()
    with patch.object(competence, "draw_d6", return_value=1):
        assert e.process_command("follow withdrawal signs")["accepted_outcome"]["result"] == "failure"
    with patch.object(competence, "draw_d6", return_value=3):
        assert e.process_command("reconstruct local observation circuit")["accepted_outcome"]["result"] == "partial"
    assert e.process_command("pursue observers")["success"]
    assert "west_road_withdrawal_route" in e.get_player_discoveries()
    # Unsupported and unknowable requests consume no draw/time; evidence cannot be invented.
    e = withdrawn(); before = e.get_world_state()
    with patch.object(competence, "draw_d6", side_effect=AssertionError("unsupported drew")):
        for question in ("identify attackers", "determine affiliation", "find distant destination", "follow withdrawal signs 6"):
            assert not e.attempt_competence(question)["success"]
    assert e.get_world_state() == before
    e.world_state["evidence_traces"] = []
    assert not e.get_competence_projection()["approaches"]
    assert not e.get_competence_projection()["recognition"]
    with patch.object(competence, "draw_d6", side_effect=AssertionError("absent evidence drew")):
        assert not e.process_command("follow withdrawal signs")["success"]
    for terminal in ("restore coverage", "pursue observers"):
        e = withdrawn(); assert e.process_command(terminal)["success"]
        assert not e.get_competence_projection()["approaches"]
        assert not e.process_command("follow withdrawal signs")["success"]


def test_time_and_atomic_boundaries():
    e = withdrawn()
    # Existing effects must occur during a competence operation as during ordinary time.
    effect = deepcopy(e.region["elapsed_time_pressure_effect"])
    effect["trigger_elapsed_hours"] = e.world_state["time"]["elapsed_hours"] + 1
    effect["new_level"] = 80
    e.region["elapsed_time_pressure_effect"] = effect
    with patch.object(competence, "draw_d6", return_value=1):
        result = e.process_command("follow withdrawal signs")
    assert result["time_advancement"]["pressure_consequence"] is not None
    assert e.world_state["pressures"][effect["pressure_id"]]["level"] == 80
    for draw in (1, 3, 5):
        for boundary in ("_prepare_time_advance_candidate", "_publish_west_road_candidate"):
            e = withdrawn(); before = e.get_world_state(); scene = e.scene_snapshot; world = e.world_state
            with patch.object(competence, "draw_d6", return_value=draw), patch.object(e, boundary, side_effect=RuntimeError("injected")):
                try:
                    e.process_command("follow withdrawal signs")
                except RuntimeError:
                    pass
                else:
                    raise AssertionError("Boundary not reached")
            assert e.get_world_state() == before and e.scene_snapshot is scene and e.world_state is world
    for boundary in ("engine.game_engine.validate_world_state", "engine.game_engine.build_scene"):
        e = withdrawn(); before = e.get_world_state(); scene = e.scene_snapshot
        with patch.object(competence, "draw_d6", return_value=5), patch(boundary, side_effect=RuntimeError("injected")):
            try:
                e.process_command("follow withdrawal signs")
            except RuntimeError:
                pass
            else:
                raise AssertionError("Boundary not reached")
        assert e.get_world_state() == before and e.scene_snapshot is scene
    for command in ("follow withdrawal signs", "arrange guarded local survey"):
        e = withdrawn(); before = e.get_world_state()
        with patch.object(competence, "draw_d6", return_value=5), patch.object(e, "_acquire_west_road_discovery", side_effect=RuntimeError("finding")):
            try:
                e.process_command(command)
            except RuntimeError:
                pass
            else:
                raise AssertionError("Finding boundary not reached")
        assert e.get_world_state() == before
    for invalid in (True, 0, 7, "6", None):
        e = withdrawn(); before = e.get_world_state()
        with patch.object(competence, "draw_d6", return_value=invalid):
            expect_invalid(lambda: e.process_command("follow withdrawal signs"))
        assert e.get_world_state() == before


def test_authored_contract_and_partial_sharing():
    from engine.region_validator import validate_region
    e = withdrawn()
    for field in ("observation", "outdoor_tracking", "surveillance_analysis", "tactical_assessment"):
        bad = deepcopy(e.region); bad["west_road_competence_evidence"][field] = None
        expect_invalid(lambda: validate_region(bad))
    for finding in ("west_road_sign_direction", "west_road_observation_overlap"):
        bad = deepcopy(e.region); bad["discovery_declarations"] = [d for d in bad["discovery_declarations"] if d["discovery_id"] != finding]
        expect_invalid(lambda: validate_region(bad))
    with patch.object(competence, "draw_d6", return_value=3):
        e.process_command("follow withdrawal signs")
    assert e.process_command("present Local Withdrawal Direction to Elin")["presentation"]["changed"]
    validate_world_state(e.get_world_state(), e.region)
    before = e.get_world_state()
    assert e.process_command("restore coverage")["success"]
    with patch.object(competence, "draw_d6", side_effect=AssertionError("historical repeat drew")):
        assert not e.process_command("follow withdrawal signs")["changed"]
    assert e.world_state["competence_attempts"] == before["competence_attempts"]
    packet = e.get_competence_projection(); packet["findings"].clear()
    assert e.get_competence_projection()["findings"]


def test_saved_competence_basis_rejection():
    active = ready()
    before = active.get_world_state()
    world, scene = active.world_state, active.scene_snapshot
    try:
        for command, (relevant, _) in competence.OPERATIONS.items():
            for specialist in (False, True):
                e = withdrawn(relevant if specialist else None)
                with patch.object(competence, "draw_d6", return_value=5):
                    e.process_command(command)
                data = build_save_data(e)
                # V1 has no competence gain/loss: the accepted basis must agree
                # with the persisted authoritative tags, even for the same result.
                data["world_state"]["player"]["competences"] = [] if specialist else [relevant]
                PATH.write_text(json.dumps(data), encoding="utf-8")
                original = PATH.read_bytes()
                expect_invalid(lambda: active.load(str(PATH)))
                assert PATH.read_bytes() == original
                assert active.get_world_state() == before
                assert active.world_state is world and active.scene_snapshot is scene
    finally:
        PATH.unlink(missing_ok=True)


def test_save_roundtrip_normalization_rejection():
    try:
        for tag in (None, "tactical_assessment", "outdoor_tracking", "surveillance_analysis"):
            for command in competence.OPERATIONS:
                for draw in (1, 3, 5):
                    e = withdrawn(tag)
                    save_game(e, str(PATH)); e = load_game(str(PATH))
                    with patch.object(competence, "draw_d6", return_value=draw):
                        accepted = e.process_command(command)["accepted_outcome"]
                    save_game(e, str(PATH)); loaded = load_game(str(PATH))
                    assert loaded.get_world_state() == e.get_world_state()
                    assert loaded.get_narration() == e.get_narration()
                    with patch.object(competence, "draw_d6", side_effect=AssertionError("loaded repeat drew")):
                        assert loaded.process_command(command)["accepted_outcome"] == accepted
                    assert loaded.get_world_state() == e.get_world_state()
        e = withdrawn()
        for command, draw in (("follow withdrawal signs", 1), ("reconstruct local observation circuit", 3)):
            with patch.object(competence, "draw_d6", return_value=draw):
                e.process_command(command)
        e.process_command("restore coverage")
        save_game(e, str(PATH)); loaded = load_game(str(PATH))
        with patch.object(competence, "draw_d6", side_effect=AssertionError("multiple loaded attempts drew")):
            for command in e.world_state["competence_attempts"]:
                assert not loaded.process_command(command)["changed"]
        assert loaded.get_world_state() == e.get_world_state()
        for initial, followup in (("advocate patrol", "pursue observers"), ("continue investigation", "locate raiders")):
            e = ready(); e.process_command(initial); e.process_command(followup)
            data = build_save_data(e)
            del data["world_state"]["player"]["competences"]
            del data["world_state"]["competence_attempts"]
            PATH.write_text(json.dumps(data), encoding="utf-8")
            original = PATH.read_bytes()
            loaded = load_game(str(PATH))
            assert loaded.world_state["player"]["competences"] == [] and loaded.world_state["competence_attempts"] == {}
            assert PATH.read_bytes() == original
        e = withdrawn("outdoor_tracking")
        with patch.object(competence, "draw_d6", return_value=1):
            e.process_command("follow withdrawal signs")
        data = build_save_data(e); command = "follow withdrawal signs"
        bad_states = []
        for tags in (None, {}, ["unknown"], ["outdoor_tracking", "outdoor_tracking"], [True]):
            bad = deepcopy(data); bad["world_state"]["player"]["competences"] = tags; bad_states.append(bad)
        for attempts in (None, [], {"unknown": {}}):
            bad = deepcopy(data); bad["world_state"]["competence_attempts"] = attempts; bad_states.append(bad)
        for key, value in (("draw", True), ("draw", 7), ("result", "full"), ("cost_hours", 2), ("findings", []), ("source_history_id", "absent"), ("specialist", 1), ("outcome_history_id", "absent")):
            bad = deepcopy(data); bad["world_state"]["competence_attempts"][command][key] = value; bad_states.append(bad)
        bad = deepcopy(data); bad["world_state"]["history"][-1]["attempt"]["specialist"] = 1; bad_states.append(bad)
        bad = deepcopy(data); del bad["world_state"]["west_road_predicament"]; bad_states.append(bad)
        bad = deepcopy(data); bad["save_version"] = 2; bad_states.append(bad)
        active = ready(); before = active.get_world_state(); scene = active.scene_snapshot
        for bad in bad_states:
            PATH.write_text(json.dumps(bad), encoding="utf-8"); original = PATH.read_bytes()
            expect_invalid(lambda: active.load(str(PATH)))
            assert PATH.read_bytes() == original and active.get_world_state() == before and active.scene_snapshot is scene
    finally:
        PATH.unlink(missing_ok=True)


if __name__ == "__main__":
    for test in (test_profiles_and_read_only, test_all_draws_and_profiles, test_survey_guards_alternates_and_limits, test_time_and_atomic_boundaries, test_authored_contract_and_partial_sharing, test_saved_competence_basis_rejection, test_save_roundtrip_normalization_rejection):
        test()
        print("PASS:", test.__name__)
