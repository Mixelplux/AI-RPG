"""Offline structural foundation checks; prose fixtures do not establish fidelity."""
from copy import deepcopy
import json
from pathlib import Path
from unittest.mock import patch
from engine.game_engine import GameEngine
from engine import character_competence as competence
from engine.narration_pipeline import build_narration_preview_packet
from engine.narration_prompt import build_narration_prompt_packet, validate_narration_prompt_packet
from engine.narration_request import build_narration_request_packet
from engine.narration_source import build_openai_responses_narration_source_result
from engine.save_system import build_save_data, save_game, load_game
from test_character_competence import withdrawn
from test_scene_context import market
from test_west_road_predicament import ready


def serialized(context, text="Offline fixture: snow skims the exposed paving."):
    """Capture the actual adapter request at its transport, not an intermediate dict."""
    calls = []
    def transport(client, request):
        calls.append(deepcopy(request))
        return type("Response", (), {"status": "completed", "output_text": text})()
    encoding = type("Encoding", (), {"encode": lambda self, s: s.split()})()
    with patch("engine.narration_source.OpenAI", return_value=object()), patch.dict("os.environ", {"OPENAI_API_KEY": "offline-test"}), patch(
        "engine.narration_source.tiktoken.encoding_for_model", return_value=encoding
    ):
        packet = build_narration_preview_packet(context, source_builder=lambda prompt:
            build_openai_responses_narration_source_result(prompt, transport))
    assert packet["accepted"] and len(calls) == 1
    return json.loads(calls[0]["input"]), packet

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Unsupported nested provider field was accepted")

def test_public_projection_and_restricted_input():
    for kind, severity, period, expected in (("clear", .1, "day", "ordinary"),
                                           ("blizzard", .95, "day", "effectively_absent"),
                                           ("clear", .1, "night", "quiet")):
        e = market(kind, severity, period)
        # Inject private fields at distinct authority/diagnostic levels. No file edits.
        e.scene_snapshot["location"]["private_fact"] = "PRIVATE_LOCATION_MARKER"
        e.scene_snapshot["location"]["state"]["private"] = "PRIVATE_STATE_MARKER"
        e.scene_snapshot["debug"]["private"] = "PRIVATE_DEBUG_MARKER"
        e.world_state["weather"]["private"] = "PRIVATE_WEATHER_MARKER"
        e.world_state["time"]["private"] = "PRIVATE_TIME_MARKER"
        e.add_actor_knowledge("captain_darvin_grey", "PRIVATE_ACTOR_MARKER")
        before, scene = e.get_world_state(), e.get_scene_snapshot()
        payloads = []
        context = e.get_narration_context("look")
        payload, packet = serialized(context)
        material = json.dumps(payload)
        assert "PRIVATE_" not in material
        assert not {"scene_snapshot", "history_context", "player", "current_time"} & set(payload)
        assert all(k not in material for k in ("captain_darvin_grey", "bryn_shander_winter", "spawn_counts", "threat_level", "calendar_system"))
        assert payload["scene_context"]["expected_activity"]["availability"] == expected
        assert payload["narrative_projection"]["familiarity"]["profile"] == "unspecified"
        assert not payload["narrative_projection"]["familiarity"]["public_features"]
        assert not payload["narrative_projection"]["acquired_information"]
        assert e.get_world_state() == before and e.get_scene_snapshot() == scene


def test_nested_contract():
    prompt = build_narration_prompt_packet(build_narration_request_packet(market().get_narration_context("look")))
    for section in ("location_facts", "expected_activity", "player_intention", "character_perspective"):
        malformed = deepcopy(prompt)
        malformed["deterministic_input"]["scene_context"][section]["private"] = "PRIVATE_MARKER"
        invalid(lambda: validate_narration_prompt_packet(malformed))
    for section in ("weather", "time"):
        malformed = deepcopy(prompt)
        malformed["deterministic_input"]["scene_context"]["conditions"][section]["private"] = "PRIVATE_MARKER"
        invalid(lambda: validate_narration_prompt_packet(malformed))
    for field in ("familiarity", "pressure_cue", "accepted_action"):
        malformed = deepcopy(prompt)
        malformed["deterministic_input"]["narrative_projection"][field]["private"] = "PRIVATE_MARKER"
        invalid(lambda: validate_narration_prompt_packet(malformed))
    for field, record in (("presence", {"display_name": "guard"}),
                          ("groups", {"display_name": "guards", "count": 2}),
                          ("routes", {"orientation": "south", "destination_name": "square"}),
                          ("acquired_information", {"text": "a report", "status": "attributed report"})):
        malformed = deepcopy(prompt)
        malformed["deterministic_input"]["narrative_projection"][field] = [{**record, "private": "PRIVATE_MARKER"}]
        invalid(lambda: validate_narration_prompt_packet(malformed))

def test_commitments_and_competence():
    for command in ("advocate patrol", "continue investigation"):
        e = ready()
        result = e.process_command(command)
        before = e.get_world_state()
        payload, _ = serialized(e.get_narration_context("I chose " + command, accepted_action_id=result["narrative_action_id"]))
        action = payload["narrative_projection"]["accepted_action"]
        assert action["action"] == command and action["cost_hours"] == 1
        assert action["outcome"] == result["scene_response"]["outcome"]
        assert action["actor_responses"] == [{"speaker": "Grey", "text": result["scene_response"]["grey"]}, {"speaker": "Elin", "text": result["scene_response"]["elin"]}]
        assert action["remaining_uncertainty"] and not payload["scene_context"]["character_perspective"]["accepted_outcomes"]
        subsequent, _ = serialized(e.get_narration_context("look at the changed situation"))
        assert subsequent["narrative_projection"]["current_situation"]
        assert e.get_world_state() == before
    for command, tag in (("follow withdrawal signs", "outdoor_tracking"),
                         ("reconstruct local observation circuit", "surveillance_analysis")):
        for profile in (None, tag):
            for draw in range(1, 7):
                e = withdrawn(profile)
                with patch.object(competence, "draw_d6", return_value=draw):
                    result = e.process_command(command)
                before, saved = e.get_world_state(), build_save_data(e)
                with patch.object(competence, "draw_d6", side_effect=AssertionError("narration/retry drew")):
                    for _ in range(2):
                        payload, _ = serialized(e.get_narration_context("describe the accepted result", accepted_action_id=result["narrative_action_id"]))
                        action = payload["narrative_projection"]["accepted_action"]
                        assert action["result"] == competence.resolve(draw, bool(profile))
                        assert action["cost_hours"] == 1 and action["outcome"] == result["message"]
                        assert ("outdoor tracking" in action["competence_basis"] or "surveillance analysis" in action["competence_basis"]) == bool(profile)
                        assert bool(action["actor_responses"]) == (action["result"] == "full")
                        assert "Nobody is captured" in action["remaining_uncertainty"][0]
                    assert not e.process_command(command)["changed"]
                assert e.get_world_state() == before and build_save_data(e) == saved
                # Current profile changes cannot rewrite the accepted specialist basis.
                e.world_state["player"]["competences"] = [tag] if not profile else []
                historical = e.get_narration_context("recall", accepted_action_id=result["narrative_action_id"])["narrative_projection"]["accepted_action"]
                assert historical["competence_basis"] == action["competence_basis"]
    for tag, cost in ((None, 2), ("tactical_assessment", 1)):
        e = withdrawn(tag)
        result = e.process_command("arrange guarded local survey")
        action = e.get_narration_context("describe", accepted_action_id=result["narrative_action_id"])["narrative_projection"]["accepted_action"]
        assert action["cost_hours"] == cost and "deterministic" in action["competence_basis"]
    e = market()
    assert not e.get_narration_context("I capture everyone and find gold")["narrative_projection"]["accepted_action"]
    invalid(lambda: ready().get_narration_context("look", accepted_action_id="invented result"))

def test_moved_location_result_retrieval():
    path = Path(".artifacts/narrative_realization_v1/moved_location_retry_save.json")
    for tag, draw, expected in ((None, 1, "failure"), (None, 3, "partial"),
                                (None, 5, "full"), ("outdoor_tracking", 1, "partial"),
                                ("outdoor_tracking", 3, "full")):
        e = withdrawn(tag)
        with patch.object(competence, "draw_d6", return_value=draw):
            original = e.process_command("follow withdrawal signs")
        action_id = original["narrative_action_id"]
        historical = e.get_narration_context("describe result", accepted_action_id=action_id)["narrative_projection"]["accepted_action"]
        assert historical["result"] == expected and historical["outcome"] == original["message"]
        assert historical["cost_hours"] == 1 and historical["remaining_uncertainty"] == [competence.LIMIT]
        assert ("outdoor tracking" in historical["competence_basis"]) == bool(tag)
        assert bool(historical["actor_responses"]) == (expected == "full")
        assert e.process_command("go to Market Square")["success"]
        save_game(e, str(path))
        restored = load_game(str(path))
        assert build_save_data(restored) == build_save_data(e)
        for engine in (e, restored):
            before, saved = engine.get_world_state(), build_save_data(engine)
            engine.scene_snapshot["debug"]["private"] = "PRIVATE_REMOTE_MARKER"
            with patch.object(competence, "draw_d6", side_effect=AssertionError("moved retry drew")):
                for _ in range(2):
                    retry = engine.process_command("follow withdrawal signs")
                    assert retry["success"] and retry["changed"] is False
                    assert retry["narrative_action_id"] == action_id
                    assert retry["accepted_outcome"] == original["accepted_outcome"]
                    payload, _ = serialized(engine.get_narration_context(
                        "follow withdrawal signs", accepted_action_id=retry["narrative_action_id"]))
                    projection = payload["narrative_projection"]
                    assert projection["accepted_action"] == historical
                    assert projection["current_situation"] == "" and projection["acquired_information"] == []
                    assert projection["presence"] == []
                    assert payload["scene_context"]["location_facts"]["name"] == "Market Square"
                    assert all(payload["scene_context"]["character_perspective"][layer] == []
                               for layer in ("observations", "recognition", "findings", "approaches", "accepted_outcomes"))
                    material = json.dumps(payload)
                    assert all(marker not in material for marker in (
                        "PRIVATE_REMOTE_MARKER", action_id, "captain_darvin_grey", "history_context", "scene_snapshot"))
                    # The local context must be identical to ordinary observation;
                    # only the explicitly selected result may add remote history.
                    observation, _ = serialized(engine.get_narration_context("follow withdrawal signs"))
                    without_result = deepcopy(projection)
                    without_result["accepted_action"] = {}
                    assert without_result == observation["narrative_projection"]
                    assert payload["scene_context"] == observation["scene_context"]
                for focus in ("look", "inspect the awnings", "reconstruct local observation circuit"):
                    ordinary, _ = serialized(engine.get_narration_context(focus))
                    assert ordinary["narrative_projection"]["accepted_action"] == {}
                    assert original["message"] not in json.dumps(ordinary)
                assert not engine.process_command("reconstruct local observation circuit")["success"]
                invalid(lambda: engine.get_narration_context("look", accepted_action_id="unaccepted reference"))
            assert engine.get_world_state() == before and build_save_data(engine) == saved


def test_attribution_and_historical_phase():
    e = withdrawn("outdoor_tracking")
    before, saved = e.get_world_state(), build_save_data(e)
    gate, _ = serialized(e.get_narration_context("inspect the tracks"))
    perspective = gate["scene_context"]["character_perspective"]
    assert perspective["observations"][0]["status"] == "guard report"
    assert perspective["observations"][0]["text"] == e.get_competence_projection()["observations"][0]["text"]
    assert perspective["recognition"][0]["status"] == "automatic competence; limited interpretation"
    information = gate["narrative_projection"]["acquired_information"]
    declarations = {d["discovery_id"]: d for d in e.region["discovery_declarations"]}
    for discovery, status in (("west_road_tracks", "limited inference"), ("west_road_merchant_account", "attributed report")):
        assert {"text": declarations[discovery]["text"], "status": status} in information
    assert e.get_world_state() == before and build_save_data(e) == saved
    assert e.process_command("go to Southwest Trade Road")["success"]
    before = build_save_data(e)
    road, _ = serialized(e.get_narration_context("look"))
    assert road["scene_context"]["character_perspective"]["observations"][0]["status"] == "direct observation"
    assert build_save_data(e) == before
    e = ready()
    result = e.process_command("advocate patrol")
    action_id = result["narrative_action_id"]
    original, _ = serialized(e.get_narration_context("look", accepted_action_id=action_id))
    historical = original["narrative_projection"]["accepted_action"]
    assert e.process_command("restore coverage")["success"]
    before = build_save_data(e)
    later, _ = serialized(e.get_narration_context("look", accepted_action_id=action_id))
    assert later["narrative_projection"]["accepted_action"] == historical
    assert build_save_data(e) == before
    for bad in ("", 42, [], {}, e.get_history()[0]["history_id"]):
        if bad == action_id:
            continue
        invalid(lambda: e.get_narration_context("look", accepted_action_id=bad))


def test_nested_types_and_previous_conditions():
    from engine.scene_continuity import SceneContinuity
    from engine.scene_context import SCENE_NARRATION_CONTRACT
    e = market()
    before = build_save_data(e)
    context = e.get_narration_context("look")
    cache = SceneContinuity()
    cache.enter(e.get_scene_snapshot()["location"]["location_id"])
    conditions = deepcopy(context["scene_context"]["conditions"])
    conditions["time"]["private"] = "PRIVATE_PREVIOUS_CONDITION"
    cache.remember("An ordinary test sentence.", conditions)
    context["scene_context"]["presentation"] = cache.presentation(e.get_scene_snapshot(), "look", "expand")
    payload, _ = serialized(context)
    assert "PRIVATE_PREVIOUS_CONDITION" not in json.dumps(payload)
    prompt = build_narration_prompt_packet(build_narration_request_packet(context))
    for field, value in (("cost_hours", -1), ("cost_hours", True), ("actor_responses", [{"speaker": 1, "text": "bad"}])):
        malformed = deepcopy(prompt)
        malformed["deterministic_input"]["narrative_projection"]["accepted_action"] = {
            "action": "test", "competence_basis": "test", "outcome": "test", "result": "failure",
            "cost_hours": 1, "consequences": [], "actor_responses": [], "remaining_uncertainty": []}
        malformed["deterministic_input"]["narrative_projection"]["accepted_action"][field] = value
        invalid(lambda: validate_narration_prompt_packet(malformed))
    malformed = deepcopy(prompt)
    malformed["deterministic_input"]["narrative_projection"]["familiarity"]["profile"] = "resident"
    invalid(lambda: validate_narration_prompt_packet(malformed))
    malformed = deepcopy(prompt)
    malformed["deterministic_input"]["scene_context"]["presentation"]["previous_conditions"]["time"]["private"] = "bad"
    invalid(lambda: validate_narration_prompt_packet(malformed))
    assert not {"hybrid_result", "information_access"} & set(SCENE_NARRATION_CONTRACT)
    assert build_save_data(e) == before

def main():
    with patch("socket.create_connection", side_effect=AssertionError("network forbidden")), patch("socket.socket.connect", side_effect=AssertionError("network forbidden")):
        for test in (test_public_projection_and_restricted_input, test_nested_contract, test_commitments_and_competence, test_moved_location_result_retrieval, test_attribution_and_historical_phase, test_nested_types_and_previous_conditions,):
            test()
            print("PASS:", test.__name__)

if __name__ == "__main__":
    main()
