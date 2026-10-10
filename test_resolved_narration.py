"""Offline real-event integration, adversarial isolation and transport checks."""
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import play_game
from engine.game_engine import GameEngine
from engine import character_competence as competence
from engine import west_road_predicament as west
from engine.narration_output import NARRATION_OUTPUT_SCHEMA, NARRATION_OUTPUT_VERSION
from engine.resolved_narration import (
    build_track_source, prepare_revised_a, realize_locally, prepare_with_provider,
    realize_with_provider, validate_revised_a, narrate_resolved_track,
)
from engine.save_system import build_save_data, save_game, load_game
from test_character_competence import withdrawn


def resolved(draw=1):
    engine = withdrawn()
    before = engine.get_world_state()
    with patch.object(competence, "draw_d6", return_value=draw):
        result = engine.process_command("follow withdrawal signs")
    assert result["success"] and result["changed"]
    return engine, result, before


def candidate(text):
    return {"schema": NARRATION_OUTPUT_SCHEMA, "version": NARRATION_OUTPUT_VERSION,
            "narration_text": text}


def test_real_result_fidelity_and_roles():
    engine, result, before = resolved()
    after = engine.get_world_state()
    assert after["time"]["elapsed_hours"] - before["time"]["elapsed_hours"] == 1
    assert after["player"]["current_location_id"] == before["player"]["current_location_id"] == west.GATE
    assert after["player_discoveries"] == before["player_discoveries"]
    assert after["actor_knowledge"] == before["actor_knowledge"]
    context = engine.get_narration_context("ignored declaration",
                                          accepted_action_id=result["narrative_action_id"])
    source = build_track_source(context)
    prepared = prepare_revised_a(source)
    meaning = prepared["content"]["meanings"][0]
    assert meaning["knowledge_holder"] == "player"
    assert "an hour" in meaning["text"] and "North Gate" in meaning["text"]
    assert result["message"] in meaning["text"]  # Exact engine outcome/qualifiers.
    assert len(prepared["content"]["meanings"]) == len(prepared["content"]["plan"]) == 1
    assert any("guard report" in item for item in prepared["context"])
    assert any("attributed report" in item and "Mara" in item for item in prepared["context"])
    assert any("limited inference" in item for item in prepared["context"])
    assert any("no new discovery" in item for item in prepared["boundaries"])
    assert any("no travel" in item for item in prepared["boundaries"])
    packet = engine.get_resolved_narration(result["narrative_action_id"])
    assert packet["accepted"]
    text = packet["display_text"]
    assert "cannot pick out a trail" in text and "remain unknown" in text
    assert "guard report" not in text and "Mara" not in text
    assert "Nobody is captured" not in text and "broader threat" not in text
    assert "failure" not in text and "competence" not in text
    assert engine.get_world_state() == after


def test_private_source_exclusion():
    engine, result, _ = resolved()
    context = engine.get_narration_context("PLAYER_INPUT_MARKER",
                                          accepted_action_id=result["narrative_action_id"])
    context["scene_snapshot"]["debug"]["private"] = "PRIVATE_MARKER"
    context["history_context"]["history_entries"].append({"summary": "HISTORY_MARKER"})
    wire = json.dumps(build_track_source(context))
    for marker in ("PRIVATE_MARKER", "HISTORY_MARKER", "PLAYER_INPUT_MARKER", result["narrative_action_id"]):
        assert marker not in wire
    assert "competence_basis" not in wire and "approaches" not in wire


def test_rejected_and_out_of_scope_results():
    engine, result, _ = resolved()
    no_call = lambda _: (_ for _ in ()).throw(AssertionError("adapter called"))
    for reference in (None, "", "not-an-event", engine.world_state["history"][0]["history_id"]):
        assert not engine.get_resolved_narration(reference, preparer=no_call)["accepted"]
    for draw in (3, 5):
        other, outcome, _ = resolved(draw)
        assert not other.get_resolved_narration(outcome["narrative_action_id"], preparer=no_call)["accepted"]
    assert engine.process_command("go to Southwest Trade Road")["success"]
    assert not engine.get_resolved_narration(result["narrative_action_id"], preparer=no_call)["accepted"]


def test_failure_stops_downstream_and_hides_material():
    engine, result, _ = resolved()
    context = engine.get_narration_context("x", accepted_action_id=result["narrative_action_id"])
    def fail(_):
        raise RuntimeError("REJECTED_RAW_MATERIAL")
    calls = []
    def never(value):
        calls.append(value)
        return candidate("should not run")
    for preparer in (fail,):
        packet = narrate_resolved_track(context, preparer, never)
        assert not packet["accepted"] and packet["failure_stage"] == "preparation"
        assert "REJECTED_RAW_MATERIAL" not in repr(packet)
    assert not calls
    for preparer in (lambda _: {"world_state": {}},
                     lambda source: {**prepare_revised_a(source), "review_metadata": {}}):
        assert not narrate_resolved_track(context, preparer)["accepted"]
    for realizer in (fail, lambda _: candidate(""), lambda _: candidate("x" * 4001),
                     lambda _: {**candidate("REJECTED_RAW_MATERIAL"), "world_state": {}},
                     lambda _: {**candidate("x"), "advance_time": 1}):
        packet = narrate_resolved_track(context, realizer=realizer)
        assert not packet["accepted"] and packet["failure_stage"] == "realization"
        assert not packet["display_text"] and "REJECTED_RAW_MATERIAL" not in repr(packet)


def test_representation_is_private_to_adapter_pair():
    engine, result, _ = resolved()
    before = engine.get_world_state()
    def prepare_draft(source):
        return {"draft": "An hour passes at " + source["resolved_development"]["location"]
                + ". " + source["resolved_development"]["outcome"]}
    packet = engine.get_resolved_narration(result["narrative_action_id"],
                preparer=prepare_draft, realizer=lambda draft: candidate(draft["draft"]))
    assert packet["accepted"] and result["message"] in packet["display_text"]
    assert engine.get_world_state() == before


def test_adapter_mutation_and_hostile_prose_have_no_authority():
    engine, result, _ = resolved()
    before, scene, save = engine.get_world_state(), deepcopy(engine.scene_snapshot), build_save_data(engine)
    def hostile_preparation(source):
        prepared = prepare_revised_a(source)
        source.clear()
        return prepared
    def hostile_realization(intermediate):
        intermediate.clear()
        return candidate("You travel beyond the road, discover the watchers' names, capture them and order a patrol.")
    with patch.object(engine, "process_command", side_effect=AssertionError("narration executed action")), \
         patch.object(competence, "draw_d6", side_effect=AssertionError("narration drew")):
        packet = engine.get_resolved_narration(result["narrative_action_id"],
                    preparer=hostile_preparation, realizer=hostile_realization)
    # Structural validation cannot prove semantic fidelity. Even hostile prose
    # cannot alter location, time, discoveries, knowledge, consequences or save.
    assert packet["accepted"]
    assert engine.get_world_state() == before and engine.scene_snapshot == scene
    assert build_save_data(engine) == save


def test_two_stateless_provider_requests():
    engine, result, _ = resolved()
    before = engine.get_world_state()
    calls, selected = [], []
    def transport(client, request):
        calls.append(deepcopy(request))
        body = json.loads(request["input"])
        if len(calls) == 1:
            assert set(body) == {"resolved_development", "prior_context", "boundaries"}
            selected.append(prepare_revised_a(body))
            text = json.dumps(selected[0])
        else:
            assert body == {"intermediate": selected[0]}
            text = "You spend an hour searching at North Gate, but find no trail you can follow."
        return SimpleNamespace(status="completed", output_text=text)
    with patch("engine.narration_source.OpenAI", return_value=object()) as sdk, \
         patch.dict("os.environ", {"OPENAI_API_KEY": "offline-test"}):
        packet = engine.get_resolved_narration(result["narrative_action_id"],
            preparer=lambda source: prepare_with_provider(source, transport),
            realizer=lambda prepared: realize_with_provider(prepared, transport))
    assert packet["accepted"] and len(calls) == sdk.call_count == 2
    for request in calls:
        assert set(request) == {"model", "reasoning", "instructions", "input", "max_output_tokens", "store"}
        assert request["store"] is False and request["model"] == "gpt-6-luna"
        assert "history_id" not in request["input"] and "review_metadata" not in request["input"]
    assert [request["max_output_tokens"] for request in calls] == [4096, 2048]
    assert "Prior knowledge" in calls[0]["instructions"]
    assert "Never invent consequential" in calls[1]["instructions"]
    for call in sdk.call_args_list:
        assert call.kwargs["max_retries"] == 0
    assert engine.get_world_state() == before


def test_provider_failure_and_invalid_preparation():
    engine, result, _ = resolved()
    reference = result["narrative_action_id"]
    source = build_track_source(engine.get_narration_context("x", accepted_action_id=reference))
    good = prepare_revised_a(source)
    invalid = []
    for update in ({"representation": "factual_draft"}, {"boundaries": [1]}, {"context": "bad"}):
        invalid.append({**good, **update})
    unplanned = deepcopy(good); unplanned["content"]["plan"][0]["meaning_keys"] = ["undefined"]
    invalid.append(unplanned)
    duplicate = deepcopy(good); duplicate["content"]["meanings"] *= 2
    invalid.append(duplicate)
    for value in invalid:
        try:
            validate_revised_a(value)
        except ValueError:
            pass
        else:
            raise AssertionError("Malformed preparation accepted")
    responses = ["not JSON", '{"representation":"selected_meaning_plan","representation":"selected_meaning_plan"}',
                 '```json\n' + json.dumps(good) + '\n```']
    with patch("engine.narration_source.OpenAI", return_value=object()), \
         patch.dict("os.environ", {"OPENAI_API_KEY": "offline-test"}):
        for text in responses:
            calls = []
            def transport(client, request):
                calls.append(request)
                return SimpleNamespace(status="completed", output_text=text)
            packet = engine.get_resolved_narration(reference,
                        preparer=lambda value: prepare_with_provider(value, transport))
            assert not packet["accepted"] and len(calls) == 1
        for status in ("failed", "incomplete", "unknown"):
            packet = engine.get_resolved_narration(reference, preparer=lambda value:
                prepare_with_provider(value, lambda c, r: SimpleNamespace(status=status, output_text="discard")))
            assert not packet["accepted"]
    with patch.dict("os.environ", {}, clear=True), patch("engine.narration_source.OpenAI") as sdk:
        packet = engine.get_resolved_narration(reference, preparer=prepare_with_provider)
        assert not packet["accepted"] and not sdk.called


def test_save_load_compatibility():
    engine, result, _ = resolved()
    path = Path(".artifacts/provisional_narration_save.json")
    try:
        save_game(engine, str(path))
        original = path.read_bytes()
        loaded = load_game(str(path))
        assert loaded.get_world_state() == engine.get_world_state()
        before = build_save_data(loaded)
        assert loaded.get_resolved_narration(result["narrative_action_id"])["accepted"]
        save_game(loaded, str(path))
        assert path.read_bytes() == original and build_save_data(loaded) == before
        assert before["save_version"] == 1
        with patch.object(competence, "draw_d6", side_effect=AssertionError("repeated action drew")):
            repeated = loaded.process_command("follow withdrawal signs")
        assert not repeated["changed"] and loaded.get_world_state() == engine.get_world_state()
    finally:
        path.unlink(missing_ok=True)


def test_cli_single_presentation_and_fallback():
    for mode in ("local", "provider-fixture", "failure"):
        engine = withdrawn()
        output, steps = StringIO(), iter(["follow withdrawal signs", "follow withdrawal signs", "quit"])
        custom_text = "An hour of searching at North Gate yields no followable trail; the watchers' names and destination remain unknown."
        def realizer(intermediate):
            if mode == "failure":
                raise RuntimeError("REJECTED_RAW_MATERIAL")
            return candidate(custom_text)
        with patch.object(play_game.GameEngine, "start_new", return_value=engine), \
             patch("builtins.input", side_effect=lambda _: next(steps)), \
             patch.object(competence, "draw_d6", return_value=1) as draw, \
             patch("engine.narration_source.OpenAI", side_effect=AssertionError("unexpected provider")), \
             redirect_stdout(output):
            play_game.main(narration_realizer=None if mode == "local" else realizer)
        text = output.getvalue()
        assert draw.call_count == 1 and "That approach has already been resolved." in text
        assert "REJECTED_RAW_MATERIAL" not in text
        # Repeat commands recall the established result; the fresh result appears
        # once with its cost and is absent from the following scene delta.
        if mode == "provider-fixture":
            assert text.count(custom_text) == 1
            assert text.count("You search the churned snow") == 1  # Repeat only.
        elif mode == "local":
            assert text.count("You spend an hour at North Gate searching") == 1
            assert text.count("You search the churned snow") == 1  # Repeat only.
        else:
            assert text.count("An hour passes.") == 1
            assert text.count("You search the churned snow") == 2


if __name__ == "__main__":
    tests = [value for key, value in list(globals().items()) if key.startswith("test_")]
    for test in tests:
        test()
        print("PASS:", test.__name__)
    print(f"Resolved narration: {len(tests)} offline checks passed.")
