"""Offline Scene Context proving cases; no narrative detail becomes state."""

from copy import deepcopy
import json
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine.narration_prompt import build_narration_prompt_packet, validate_narration_prompt_packet
from engine.narration_request import build_narration_request_packet
from engine.narration_source import build_openai_responses_narration_source_result
from engine.scene_context import SCENE_NARRATION_CONTRACT
from engine.scene_continuity import SceneContinuity
from test_character_competence import withdrawn


REGION = "data/regions/bryn_shander.json"


def market(kind="clear", severity=0.1, period="day"):
    state = GameEngine(REGION).get_world_state()
    state["player"]["current_location_id"] = "market_square"
    state["weather"].update(type=kind, severity=severity)
    state["time"]["time_of_day"] = period
    return GameEngine(REGION, initial_world_state=state)


def prompt_for(engine, intention):
    return build_narration_prompt_packet(build_narration_request_packet(
        engine.get_narration_context(intention)
    ))


def test_grounding_and_conditions():
    ordinary = market()
    before, history, scene = ordinary.get_world_state(), ordinary.get_history(), ordinary.get_scene_snapshot()
    context = ordinary.get_narration_context("I look through the market to see what is still being sold.")
    derived = context["scene_context"]
    facts = derived["location_facts"]["description"]
    for grounding in ("temporary stalls", "commercial lanes", "Town Hall", "everyday provisions", "public business"):
        assert grounding in facts
    assert derived["expected_activity"]["availability"] == "ordinary"
    assert "permitted" in derived["expected_activity"]["constraint"]
    assert derived["conditions"]["weather"] == before["weather"]
    assert derived["conditions"]["time"] == {k: v for k, v in before["time"].items() if k != "calendar_system"}
    assert ordinary.get_narration_context(context["player_input"]) == context
    context["scene_context"]["conditions"]["weather"]["severity"] = 1
    assert ordinary.get_world_state() == before
    assert ordinary.get_history() == history and ordinary.get_scene_snapshot() == scene

    for kind, severity, period, expected in (
        ("blizzard", 0.65, "day", "sparse"),
        ("blizzard", 0.95, "day", "effectively_absent"),
        ("snow", 0.9, "day", "effectively_absent"),
        ("clear", 0.1, "night", "quiet"),
        ("clear", 0.1, "dawn", "limited"),
    ):
        e = market(kind, severity, period)
        packet = prompt_for(e, "look through the market")
        activity = packet["deterministic_input"]["scene_context"]["expected_activity"]
        assert activity["availability"] == expected
        assert "No bustling" in activity["constraint"] or "no " in activity["constraint"]
        assert packet["deterministic_input"]["scene_context"]["location_facts"] == derived["location_facts"]


def test_intention_and_provider_contract():
    e = market("blizzard", 0.95)
    before = e.get_world_state()
    for intention in (
        "I cross the square toward the burned inn.",
        "I look through the market to see what is still being sold.",
    ):
        prompt = prompt_for(e, intention)
        assert prompt["deterministic_input"]["scene_context"]["player_intention"]["declared_text"] == intention
        assert prompt["instructions"]["scene_narration_contract"] == SCENE_NARRATION_CONTRACT
        calls = []

        def transport(client, request):
            calls.append(request)
            return type("Response", (), {"status": "completed", "output_text": "Snow blows across empty stall frames."})()

        # Offline tokenizer contract only; this does not verify real token counts.
        encoding = type("OfflineEncoding", (), {"encode": lambda self, text: text.split()})()
        with patch.dict("os.environ", {"OPENAI_API_KEY": "offline-test"}), patch(
            "engine.narration_source.tiktoken.encoding_for_model", return_value=encoding
        ):
            build_openai_responses_narration_source_result(prompt, transport)
        sent = json.loads(calls[0]["input"])
        instructions = json.loads(calls[0]["instructions"])["scene_narration_contract"]
        assert sent["scene_context"] == prompt["deterministic_input"]["scene_context"]
        assert sent["scene_context"]["expected_activity"]["availability"] == "effectively_absent"
        for permission in ("anonymous incidental people", "common goods", "harmless props", "ordinary animals"):
            assert permission in instructions["incidental_freedom"]
        for protection in ("major clues", "important NPC presence", "hidden identities", "major threats", "faction actions", "success or failure", "story resolutions"):
            assert protection in instructions["consequential_limit"]
        for protection in ("damage or history", "hidden compartments", "NPC knowledge", "motives", "successful discoveries"):
            assert protection in instructions["consequential_limit"]
        for choice in ("helping", "spending", "threatening", "accepting offers", "revealing information", "avoidable danger", "abandoning"):
            assert choice in instructions["intention_limit"]
        assert "untrusted intent" in instructions["intention_limit"]
        assert "current scene" in instructions["intention_limit"]
        assert "expected activity" in instructions["presentation"]
        assert "second-person" in instructions["presentation"]
        assert "First-person declared player" in instructions["presentation"]
        assert "quoted NPC dialogue" in instructions["presentation"]
        for measurement_rule in ("not normally narrated", "qualitative, lived", "temperature", "visibility", "credible in-world reason", "rigid phrase table"):
            assert measurement_rule in instructions["measurements"]
        malformed_packets = [deepcopy(prompt), deepcopy(prompt)]
        malformed_packets[0]["deterministic_input"]["scene_context"] = []
        del malformed_packets[1]["deterministic_input"]["scene_context"]["expected_activity"]["constraint"]
        for malformed in malformed_packets:
            try:
                validate_narration_prompt_packet(malformed)
            except ValueError as error:
                assert "Scene Context" in str(error)
            else:
                raise AssertionError("Malformed Scene Context accepted")
    assert e.get_world_state() == before


def test_established_background_and_focus_provider_contract():
    # Exercise the validated provider boundary with both market and non-market
    # context. Prose is a fixture, not a claim about generated narrative quality.
    for e in (market("blizzard", 0.95), GameEngine(REGION)):
        before = e.get_world_state()
        continuity = SceneContinuity()
        established = "You see a few people passing between nearby buildings."
        calls = []

        def transport(client, request):
            calls.append(request)
            return type("Response", (), {
                "status": "completed", "output_text": established,
            })()

        encoding = type("OfflineEncoding", (), {"encode": lambda self, text: text.split()})()
        with patch.dict("os.environ", {"OPENAI_API_KEY": "offline-test"}), patch(
            "engine.narration_source.tiktoken.encoding_for_model", return_value=encoding
        ), patch("socket.create_connection", side_effect=AssertionError("network forbidden")):
            for stage, focus in (
                ("orient", "look around on arrival"),
                ("expand", "look"),
                ("follow", "I examine what people are carrying"),
                ("narrow", "talk to someone nearby"),
            ):
                context = e.get_narration_context(focus)
                scene = context["scene_context"]
                scene["presentation"] = continuity.presentation(e.get_scene_snapshot(), focus, stage)
                prompt = build_narration_prompt_packet(build_narration_request_packet(context))
                build_openai_responses_narration_source_result(prompt, transport)
                sent = json.loads(calls[-1]["input"])
                sent_scene = sent["scene_context"]
                presentation = sent_scene["presentation"]
                assert presentation["stage"] == stage
                assert presentation["focus"] == sent["player_input"] == focus
                assert sent_scene["player_intention"]["declared_text"] == focus
                assert presentation["established_details"] == ([] if stage == "orient" else [established])
                assert presentation["previous_conditions"] == ({} if stage == "orient" else scene["conditions"])
                contract = json.loads(calls[-1]["instructions"])["scene_narration_contract"]
                for rule in ("already known background constraints", "not a checklist", "compatibility, not by repeating"):
                    assert rule in contract["continuity"]
                for rule in ("orient on arrival", "Expand on look", "previously unmentioned observable",
                             "Follow focused", "Narrow interaction", "prioritize the current focus",
                             "negative observation still resolves the focus", "supplied activity bounds",
                             "observable basis or limits", "concise focused result is sufficient"):
                    assert rule in contract["progression"]
                assert "relevance alone does not call for a recap" in contract["progression"]
                for rule in ("express their effects", "describe material changes", "Unchanged conditions need no mention"):
                    assert rule in contract["condition_continuation"]
                # Remembering prior prose must not replace current authoritative bounds.
                assert sent_scene["conditions"] == scene["conditions"]
                assert sent_scene["expected_activity"] == scene["expected_activity"]
                continuity.remember(established, scene["conditions"])
        assert e.get_world_state() == before


def test_competence_perspective():
    ordinary, specialist = withdrawn(), withdrawn("outdoor_tracking")
    for e in (ordinary, specialist):
        before, snapshot = e.get_world_state(), e.get_scene_snapshot()
        context = e.get_narration_context("examine the roadside marks")
        assert context["scene_context"]["character_perspective"] == e.get_competence_projection()
        assert e.get_world_state() == before and e.get_scene_snapshot() == snapshot
    a, b = [e.get_narration_context("examine the roadside marks")["scene_context"] for e in (ordinary, specialist)]
    assert a["location_facts"] == b["location_facts"] and a["conditions"] == b["conditions"]
    assert a["character_perspective"]["observations"] == b["character_perspective"]["observations"]
    assert not a["character_perspective"]["recognition"] and b["character_perspective"]["recognition"]
    assert "limited interpretation" in b["character_perspective"]["recognition"][0]["status"]
    assert specialist.process_command("go to Market Square")["success"]
    local = specialist.get_narration_context("look")["scene_context"]["character_perspective"]
    assert all(local[layer] == [] for layer in ("observations", "recognition", "findings", "approaches", "accepted_outcomes"))


def main():
    test_grounding_and_conditions()
    test_intention_and_provider_contract()
    test_established_background_and_focus_provider_contract()
    test_competence_perspective()
    print("Scene Context proving cases passed: grounding, conditions, intention, perspective, freedom, consequence protection and offline provider propagation.")


if __name__ == "__main__":
    main()
