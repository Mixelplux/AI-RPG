"""Offline first contact, accessible composition, continuity and authority checks."""
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
from unittest.mock import patch

import play_game
from engine.game_engine import GameEngine
from engine import character_competence as competence, west_road_predicament as west
from engine.narration_output import NARRATION_OUTPUT_SCHEMA, NARRATION_OUTPUT_VERSION
from engine.scene_composition import build_scene_source, prepare_scene_revised_a, realize_scene_locally
from engine.save_system import build_save_data, save_game, load_game
from test_artifact_files import artifact_files
from test_character_competence import withdrawn

REGION = "data/regions/bryn_shander.json"
REPORT_ROUTE = ("go to Southwest Trade Road", "investigate", "talk to Mara", "go to North Gate",
                "present Repeated Watch Tracks to Elin", "present Mara's Account to Elin")


def candidate(text):
    return {"schema": NARRATION_OUTPUT_SCHEMA, "version": NARRATION_OUTPUT_VERSION,
            "narration_text": text}


def capture(engine):
    sources = []
    def prepare(source):
        sources.append(deepcopy(source))
        return prepare_scene_revised_a(source)
    packet = engine.get_scene_narration(preparer=prepare)
    assert packet["accepted"] and len(sources) == 1
    return packet, sources[0]


def commands(engine, route):
    for command in route:
        assert engine.process_command(command)["success"], command


def run_cli(engine, route, **adapters):
    output = StringIO()
    with patch.object(play_game.GameEngine, "start_new", return_value=engine), \
         patch("builtins.input", side_effect=list(route) + ["quit"]), \
         patch("engine.narration_source.OpenAI", side_effect=AssertionError("provider forbidden")) as provider, \
         redirect_stdout(output):
        play_game.main(**adapters)
    assert not provider.called
    return output.getvalue()


def test_first_contact_without_briefing():
    engine = GameEngine(REGION)
    before = build_save_data(engine)
    packet, source = capture(engine)
    text = packet["display_text"]
    assert "northern gate" in text and "blizzard" in text
    assert "Captain Darvin Grey, the guard commander" in text
    assert "Elin Voss, the city guard" in text and "2 watch guards" in text
    assert "travelers say" in text and "caravan is overdue" in text
    assert "Grey fears" in text and "Elin wants evidence" in text and "No one knows" in text
    assert "Whether to get involved" in text
    assert source["information"] == [] and before["world_state"]["player_discoveries"] == []
    assert "talk to Grey" in packet["guidance"]["other"] and "way south" in packet["guidance"]["other"]
    assert "go to Southwest Trade Road" in packet["guidance"]["choices"]
    assert all(word not in text.lower() for word in ("missing patrol", "your mission", "you agree", "first time"))
    assert build_save_data(engine) == before
    resume = engine.get_resume_summary()[0]
    assert "You were investigating" not in resume and "If you want to investigate" in resume


def test_only_accessible_facts_and_prior_information():
    engine = GameEngine(REGION)
    context = engine.get_narration_context("UNTRUSTED_INTENT_MARKER")
    context["scene_snapshot"]["debug"]["private"] = "PRIVATE_SCENE_MARKER"
    context["history_context"]["history_entries"].append({"summary": "PRIVATE_HISTORY_MARKER"})
    with patch.object(engine, "get_narration_context", return_value=context):
        _, source = capture(engine)
    wire = json.dumps(source)
    for marker in ("PRIVATE_SCENE_MARKER", "PRIVATE_HISTORY_MARKER", "UNTRUSTED_INTENT_MARKER",
                   "scene_snapshot", "history_context", "actor_knowledge", "history_id", "spawn_counts"):
        assert marker not in wire
    assert all("Mara reports" not in item["text"] for item in source["selected_facts"])
    commands(engine, REPORT_ROUTE)
    _, source = capture(engine)
    info = source["information"]
    assert any(item["status"] == "attributed report" and "Mara reports" in item["text"] for item in info)
    assert any(item["status"] == "limited inference" and "suggest" in item["text"] for item in info)
    prepared = prepare_scene_revised_a(source)
    assert any("attributed report" in item for item in prepared["context"])
    assert all("Mara reports" not in item["text"] for item in prepared["content"]["meanings"])
    # Crossing between the two local views needs place orientation, not a replay
    # of the same public premise or already exposed evidence.
    previous = engine.get_narration()
    commands(engine, ["go to Southwest Trade Road"])
    packet = engine.get_scene_narration(previous, {"success": True, "intent": "movement"})
    assert packet["accepted"] and "Southwest Trade Road" in packet["display_text"]
    assert "caravan is overdue" not in packet["display_text"]
    previous = engine.get_narration()
    commands(engine, ["go to North Gate"])
    packet = engine.get_scene_narration(previous, {"success": True, "intent": "movement"})
    assert packet["accepted"] and "northern gate" in packet["display_text"]
    assert "caravan is overdue" not in packet["display_text"] and "Whether to get involved" not in packet["display_text"]


def test_presence_and_npc_knowledge_are_authoritative():
    engine = GameEngine(REGION)
    engine.set_actor_location(west.ELIN, "bryn_shander_main_street")
    before = build_save_data(engine)
    packet, source = capture(engine)
    assert all(item["display_name"] != "Elin Voss" for item in source["presence"] + source["roles"])
    assert "talk to Elin" not in packet["guidance"].get("other", "")
    assert not any("type 'advocate patrol'" in text for text in source["opportunities"])
    # Public scenario concerns may mention an absent actor; no presence or speech is fabricated.
    assert "Elin Voss, the city guard" not in packet["display_text"]
    assert build_save_data(engine) == before


def test_opportunities_and_costs_match_predicates():
    cold = GameEngine(REGION)
    ready = GameEngine(REGION); commands(ready, REPORT_ROUTE)
    for engine in (cold, ready, withdrawn(), withdrawn("tactical_assessment")):
        _, source = capture(engine)
        expected = engine.get_player_perception()["contextual_actions"]["opportunities"]
        assert source["opportunities"] == expected
        decisions = west.available_commands(engine.world_state, engine.scene_snapshot)
        approaches = engine.get_competence_projection()["approaches"]
        choices = source["guidance"].get("choices", "")
        assert all("type '" + command + "'" in choices for command in decisions)
        for approach in approaches:
            text = next(text for text in expected if "type '" + approach["command"] + "'" in text)
            assert ("one hour" if approach["cost_hours"] == 1 else "2 hours") in text
        assert len([text for text in expected if text.startswith("You can choose:")]) == len(decisions) + len(approaches)


def test_voluntary_participation_and_leaving():
    engine = GameEngine(REGION)
    before = engine.get_world_state()
    text = run_cli(engine, ["go to Main Street"])
    assert "Whether to get involved" in text and "Main Street" in text
    after = engine.get_world_state()
    assert after["west_road_predicament"] == before["west_road_predicament"]
    assert after["player_discoveries"] == before["player_discoveries"]
    assert after["actor_knowledge"] == before["actor_knowledge"]
    assert not any(item["event_type"] == "west_road_commitment" for item in after["history"])


def test_report_sharing_remains_required():
    engine = GameEngine(REGION)
    commands(engine, REPORT_ROUTE[:4])
    before = engine.get_world_state()
    assert not engine.process_command("advocate patrol")["success"]
    capture(engine)
    assert engine.get_world_state() == before
    commands(engine, ["present Repeated Watch Tracks to Grey"])
    assert not west.available_commands(engine.world_state, engine.scene_snapshot)
    commands(engine, ["present Repeated Watch Tracks to Elin"])
    packet, _ = capture(engine)
    assert "what Mara saw" in packet["guidance"]["choices"]
    assert not west.available_commands(engine.world_state, engine.scene_snapshot)
    commands(engine, ["present Mara's Account to Elin"])
    assert set(west.available_commands(engine.world_state, engine.scene_snapshot)) == {"advocate patrol", "continue investigation"}


def test_commitment_updates_scene_without_replay():
    engine = GameEngine(REGION); commands(engine, REPORT_ROUTE)
    previous = engine.get_narration()
    before = engine.get_world_state()
    result = engine.process_command("advocate patrol")
    after = engine.get_world_state()
    assert after["time"]["elapsed_hours"] - before["time"]["elapsed_hours"] == 1
    packet = engine.get_scene_narration(previous, result)
    assert packet["accepted"]
    text = packet["display_text"] + "\n" + packet["guidance"]["choices"]
    assert result["scene_response"]["outcome"] not in text
    assert "restore coverage" in text and "pursue observers" in text
    assert "other approaches" in text
    assert "type 'advocate patrol'" not in text and "type 'continue investigation'" not in text
    assert engine.get_world_state() == after


def test_failed_tracking_and_remaining_choices():
    engine = withdrawn()
    previous = engine.get_narration()
    before = engine.get_world_state()
    with patch.object(competence, "draw_d6", return_value=1) as draw:
        result = engine.process_command("follow withdrawal signs")
    after = engine.get_world_state()
    assert draw.call_count == 1 and after["time"]["elapsed_hours"] - before["time"]["elapsed_hours"] == 1
    assert after["player"]["current_location_id"] == before["player"]["current_location_id"] == west.GATE
    assert after["player_discoveries"] == before["player_discoveries"]
    assert after["actor_knowledge"] == before["actor_knowledge"]
    resolved = engine.get_resolved_narration(result["narrative_action_id"])
    assert resolved["accepted"] and "remain unknown" in resolved["display_text"]
    packet = engine.get_scene_narration(previous, result)
    assert packet["accepted"] and packet["display_text"] == ""
    assert "type 'follow withdrawal signs'" not in packet["guidance"]["choices"]
    assert all("type '" + command + "'" in packet["guidance"]["choices"] for command in (
        "restore coverage", "pursue observers", "reconstruct local observation circuit", "arrange guarded local survey"))
    with patch.object(competence, "draw_d6", side_effect=AssertionError("query/retry drew")):
        assert engine.get_scene_narration(previous, result) == packet
        assert not engine.process_command("follow withdrawal signs")["changed"]
    assert engine.get_world_state() == after


def test_cli_route_and_single_outcome():
    engine = GameEngine(REGION)
    with patch.object(competence, "draw_d6", return_value=1) as draw:
        text = run_cli(engine, REPORT_ROUTE + ("advocate patrol", "follow withdrawal signs"))
    assert draw.call_count == 1
    assert text.count("You spend an hour at North Gate searching") == 1
    assert text.count("Mara reports seeing two observers") == 1
    assert "The tracks suggest people watched the road" in text
    following = text.split("You spend an hour at North Gate searching", 1)[1].split("=== SCENE ===", 1)[1]
    assert "cannot pick out" not in following and "Mara reports" not in following
    assert "restore coverage" in following and "arrange guarded local survey" in following
    assert "blizzard" not in following and "withdrawal" not in following.replace("follow withdrawal signs", "")


def test_save_load_and_reorientation():
    engine = withdrawn()
    with patch.object(competence, "draw_d6", return_value=1):
        engine.process_command("follow withdrawal signs")
    with artifact_files("test_scene_construction") as directory:
        path = Path(directory) / "test_scene_construction_save.json"
        save_game(engine, str(path))
        original = path.read_bytes()
        loaded = load_game(str(path))
        before = build_save_data(loaded)
        assert before["save_version"] == 1
        capture(loaded)
        save_game(loaded, str(path))
        assert path.read_bytes() == original and build_save_data(loaded) == before
        with patch.object(play_game, "SAVE_PATH", str(path)):
            text = run_cli(loaded, ["load"])
        following = text.split("Game loaded.", 1)[1]
        assert "Previously:" in following and "North Gate" in following
        assert all(word not in following.lower() for word in ("first time", "first meeting", "new acquaintance"))
        assert build_save_data(loaded) == before
    cold = GameEngine(REGION)
    commands(cold, ["go to Main Street", "go to North Gate"])
    text = cold.get_scene_narration()["display_text"]
    assert "Whether to get involved" in text and "first time" not in text.lower()


def test_adapters_cannot_mutate_simulation_or_guidance():
    engine = withdrawn()
    before, scene = build_save_data(engine), deepcopy(engine.scene_snapshot)
    expected = engine.get_scene_narration()["guidance"]
    def mutating(source):
        selected = prepare_scene_revised_a(source)
        source.clear()
        return selected
    def hostile(intermediate):
        intermediate.clear()
        return {**candidate("Unsupported result"), "world_state": {"player_discoveries": ["invented"]}}
    with patch.object(engine, "process_command", side_effect=AssertionError("composition executed")), \
         patch.object(competence, "draw_d6", side_effect=AssertionError("composition drew")):
        assert engine.get_scene_narration(preparer=mutating)["guidance"] == expected
        failed = engine.get_scene_narration(realizer=hostile)
        assert not failed["accepted"] and failed["display_text"] == ""
    assert build_save_data(engine) == before and engine.scene_snapshot == scene


def test_deterministic_fallback_and_stage_failure():
    engine = GameEngine(REGION)
    before = build_save_data(engine)
    calls = []
    def broken(_):
        raise RuntimeError("PRIVATE_ERROR_MARKER")
    def downstream(value):
        calls.append(value)
        return candidate("Unexpected call")
    failed = engine.get_scene_narration(preparer=broken, realizer=downstream)
    assert not failed["accepted"] and failed["failure_stage"] == "preparation" and calls == []
    for adapters in ({"scene_preparer": broken}, {"scene_realizer": broken},
                     {"scene_realizer": lambda _: candidate("")},
                     {"scene_realizer": lambda _: candidate("x" * 4001)}):
        text = run_cli(engine, [], **adapters)
        assert "North Gate" in text and "caravan is overdue" in text and "talk to Grey" in text
        assert "PRIVATE_ERROR_MARKER" not in text and "Unexpected call" not in text
        assert build_save_data(engine) == before


def test_ordinary_location_and_diagnostics_unchanged():
    engine = GameEngine(REGION)
    commands(engine, ["go to Main Street"])
    baseline, before = engine.get_narration(), build_save_data(engine)
    with patch.object(engine, "get_narration_context", side_effect=AssertionError("ordinary scene composed")):
        assert not engine.get_scene_narration()["accepted"]
        output = StringIO()
        with redirect_stdout(output):
            play_game.print_composed_scene(engine, baseline)
        expected = StringIO()
        with redirect_stdout(expected):
            play_game.print_narration(baseline)
        assert output.getvalue() == expected.getvalue()
    assert engine.get_narration() == baseline and build_save_data(engine) == before
    gate = GameEngine(REGION)
    debug = run_cli(gate, ["narration context look"])
    assert "NARRATION CONTEXT" in debug and "scene id:" in debug and "current time:" in debug
    assert "scene_sections" in gate.get_narration()


def test_alternate_representation_and_generic_source():
    engine = GameEngine(REGION)
    captured = []
    def alternate(source):
        captured.append(deepcopy(source))
        assert "representation" not in source and "meanings" not in source
        return tuple(item["text"] for item in source["selected_facts"])
    def realize(values):
        assert isinstance(values, tuple)
        return candidate("\n\n".join(values))
    assert engine.get_scene_narration(preparer=alternate, realizer=realize)["accepted"]
    source = captured[0]
    assert source["opportunities"] == engine.get_player_perception()["contextual_actions"]["opportunities"]
    # The composition helper itself accepts supplied ordinary scene projections;
    # the gameplay integration is deliberately bounded to the accepted reference slice.
    commands(engine, ["go to Main Street"])
    ordinary = {"title": "Main Street", "scene_sections": {
        "orientation": engine.get_current_scene_projection()["location"]["description"],
        "situation": "", "choices": "", "other": "", "evidence": [], "conditions": [],
    }}
    source = build_scene_source(engine.get_narration_context("look"), ordinary,
                                engine.get_player_perception()["contextual_actions"]["opportunities"], [])
    text = realize_scene_locally(prepare_scene_revised_a(source))["narration_text"]
    assert "West-road" not in text and "caravan" not in text and source["information"] == []


if __name__ == "__main__":
    tests = [value for key, value in list(globals().items()) if key.startswith("test_")]
    with patch("socket.create_connection", side_effect=AssertionError("network forbidden")), \
         patch("socket.socket.connect", side_effect=AssertionError("network forbidden")):
        for test in tests:
            test()
            print("PASS:", test.__name__)
    print(f"Scene Construction: {len(tests)} offline checks passed.")
