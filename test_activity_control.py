"""Offline F05 authority fixtures and real material-handling regressions."""
from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from engine.activity_control import (
    ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment,
    decide_activity_control,
)
from engine import character_competence as competence, contextual_action
from engine.game_engine import GameEngine
from engine.narrative_realization import build_realization_request, validate_context
from engine.save_system import build_save_data, load_game

FIXTURE = Path("test_fixtures/f05_activity_control.json")
MARKET = "data/regions/market_passage_v1.json"


def denied(*args, **kwargs):
    raise AssertionError("Provider/network or unexpected repeat resolution forbidden")


def checkpoint(data):
    data = deepcopy(data)
    for name in ("missing_means", "conflicting_constraints"):
        if name in data:
            data[name] = tuple(data[name])
    data["developments"] = tuple(ActivityDevelopment(**d) for d in data.get("developments", []))
    return ActivityCheckpoint(**data)


def authorization(data):
    data = deepcopy(data)
    for name in ("constraints", "answered_choices"):
        if name in data:
            data[name] = tuple(data[name])
    return ActivityAuthorization(**data)


class ActivityControlTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.cases = {case["id"]: case for case in self.fixtures["cases"]}
        for guard in (
            patch("socket.create_connection", side_effect=denied),
            patch.object(socket.socket, "connect", side_effect=denied),
            patch.object(socket.socket, "connect_ex", side_effect=denied),
            patch("engine.narration_source.OpenAI", side_effect=denied),
        ):
            guard.start()
            self.addCleanup(guard.stop)

    def decide(self, name):
        case = self.cases[name]
        return decide_activity_control(authorization(case["authorization"]),
                                       checkpoint(case["checkpoint"]))

    def test_authoritative_situations_and_f01_information_contract(self):
        before = deepcopy(self.fixtures)
        for case in self.fixtures["cases"]:
            with self.subTest(case=case["id"]):
                decision = self.decide(case["id"])
                self.assertEqual([decision.status, decision.reason, decision.resolution],
                                 case["expected"])
                self.assertEqual(decision.resolution_ref, case["checkpoint"].get("resolution_ref"))
                context = validate_context(case["f01_context"])
                supplied = json.loads(build_realization_request(context)["input"])
                self.assertEqual(supplied, context)
                self.assertNotIn("concealed_witness_17", json.dumps(asdict(decision)))
                self.assertNotIn("concealed_witness_17", json.dumps(supplied))
        self.assertEqual(self.fixtures, before)

    def test_lockpicking_resumes_accepted_result_only_with_current_authorization(self):
        case = self.cases["footsteps_during_lockpicking"]
        auth, point = authorization(case["authorization"]), checkpoint(case["checkpoint"])
        self.assertEqual(decide_activity_control(auth, point).status, "control")
        # Renewed authorization answers this perceptible risk, not all later risks.
        renewed = replace(auth, answered_choices=("footsteps_at_door",))
        decision = decide_activity_control(renewed, point)
        self.assertEqual((decision.status, decision.resolution, decision.resolution_ref),
                         ("continue", "reuse", "lock-attempt-1"))
        new_risk = replace(point, developments=(replace(point.developments[0],
                                                       choice_key="door_opens"),))
        self.assertEqual(decide_activity_control(renewed, new_risk).status, "control")

    def test_ordinary_hidden_unanswerable_and_nonobjectionable_events_do_not_overinterrupt(self):
        case = self.cases["footsteps_during_lockpicking"]
        auth, point = authorization(case["authorization"]), checkpoint(case["checkpoint"])
        event = point.developments[0]
        for changed in (replace(event, kind="ordinary"),
                        replace(event, perceived=False),
                        replace(event, opportunity_to_respond=False),
                        replace(event, potentially_objectionable=False)):
            with self.subTest(event=changed):
                decision = decide_activity_control(auth, replace(point, developments=(changed,)))
                self.assertEqual((decision.status, decision.resolution), ("continue", "reuse"))

    def test_prior_risk_does_not_waive_missing_tools_limits_or_changed_methods(self):
        case = self.cases["footsteps_during_lockpicking"]
        auth = replace(authorization(case["authorization"]),
                       answered_choices=("footsteps_at_door",),
                       constraints=("no_damage",))
        point = checkpoint(case["checkpoint"])
        for changed in (replace(point, missing_means=("lockpicks",)),
                        replace(point, conflicting_constraints=("no_damage",)),
                        replace(point, method="force_the_door"),
                        replace(point, purpose="search_the_next_building")):
            with self.subTest(point=changed):
                self.assertEqual(decide_activity_control(auth, changed).status, "control")

    def test_inquiry_preparation_and_withdrawal_do_not_commit_the_objective(self):
        point = ActivityCheckpoint("open the lock", "lockpicks")
        for intent in ("inquiry", "prepare", "withdraw"):
            with self.subTest(intent=intent):
                decision = decide_activity_control(
                    ActivityAuthorization(point.purpose, point.method, intent=intent), point)
                self.assertEqual((decision.status, decision.reason), ("control", intent))

    def test_conversation_does_not_authorize_bribes_promises_threats_or_disclosures(self):
        case = self.cases["merchant_routine_inquiry"]
        auth, point = authorization(case["authorization"]), checkpoint(case["checkpoint"])
        self.assertEqual(decide_activity_control(auth, point).status, "continue")
        for choice in ("pay_five_coins", "promise_delivery", "threaten_merchant",
                       "disclose_private_letter", "choose_other_route"):
            with self.subTest(choice=choice):
                changed = replace(point, developments=(
                    ActivityDevelopment("player_choice", choice_key=choice),))
                self.assertEqual(decide_activity_control(auth, changed).status, "control")
        accepted = replace(auth, answered_choices=("pay_five_coins",))
        paid = replace(point, developments=(ActivityDevelopment("player_choice",
                                                                choice_key="pay_five_coins"),))
        self.assertEqual(decide_activity_control(accepted, paid).status, "continue")

    def test_malformed_control_inputs_fail_before_any_execution(self):
        auth = ActivityAuthorization("search crates", "open and inspect")
        point = ActivityCheckpoint(auth.purpose, auth.method)
        invalid = [
            (None, point), (replace(auth, purpose=""), point),
            (replace(auth, intent="automatic"), point),
            (replace(auth, answered_choices=["any_risk"]), point),
            (auth, replace(point, blocked="yes")),
            (auth, replace(point, developments=({},))),
            (auth, replace(point, resolution_ref="")),
            (auth, replace(point, developments=(ActivityDevelopment("invented"),))),
        ]
        for changed_auth, changed_point in invalid:
            with self.subTest(auth=changed_auth, point=changed_point):
                with self.assertRaises(ValueError):
                    decide_activity_control(changed_auth, changed_point)

    def test_existing_natural_input_separates_assessment_preparation_and_commitment(self):
        engine = GameEngine(MARKET)
        before = build_save_data(engine)
        result = engine.process_command("Inspect the wheel and see if I can fix its fitting")
        self.assertEqual(result["contextual_action"]["status"], "assessed")
        self.assertEqual(build_save_data(engine), before)
        result = engine.process_command("Brace the cart")
        self.assertEqual(result["contextual_action"]["status"], "authorization_required")
        self.assertEqual(build_save_data(engine), before)
        with patch.object(competence, "draw_d6", side_effect=denied):
            result = engine.process_command("go ahead")
        # The established handling slice records completed bracing preparation
        # as an interruption when its own prerequisite is no longer applicable.
        self.assertEqual(result["contextual_action"]["status"], "interrupted")
        record = engine.get_world_state()["material_conditions"]["delivery_cart"]
        self.assertEqual(record["conditions"]["stability"], "braced")
        # Bracing authorizes support only. The authored initial obstruction
        # remains; moving the cart aside is a separate consequential action.
        self.assertEqual(record["conditions"]["position"], "blocked")
        initial = before["world_state"]["material_conditions"]["delivery_cart"]["conditions"]
        self.assertEqual({key: value for key, value in record["conditions"].items()
                          if key != "stability"},
                         {key: value for key, value in initial.items()
                          if key != "stability"})

    def test_real_interruption_preserves_paid_preparation_and_save_compatibility(self):
        engine = GameEngine(MARKET)
        engine.advance_time(1)
        engine.process_command("Adjust the wheel")
        with patch.object(competence, "draw_d6", side_effect=denied), patch.object(
                contextual_action, "decide_activity_control", wraps=decide_activity_control) as policy:
            result = engine.process_command("yes")
        self.assertEqual(policy.call_count, 1)
        self.assertEqual(result["contextual_action"]["status"], "interrupted")
        world = engine.get_world_state()
        self.assertEqual(world["time"]["elapsed_hours"], 2)
        self.assertEqual(world["material_conditions"]["delivery_cart"]["conditions"]["stability"],
                         "braced")
        path = Path(".artifacts/f05-interrupted-roundtrip.json")
        path.parent.mkdir(exist_ok=True)
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        engine.save(str(path))
        restored = load_game(str(path))
        self.assertEqual(build_save_data(restored), build_save_data(engine))
        self.assertEqual(build_save_data(restored)["save_version"], 1)

    def test_real_resolved_replay_never_draws_charges_or_publishes_again(self):
        engine = GameEngine(MARKET)
        engine.process_command("Adjust the wheel")
        with patch.object(competence, "draw_d6", return_value=3) as draw:
            accepted = engine.process_command("yes")
        self.assertEqual(accepted["contextual_action"]["status"], "accepted")
        self.assertEqual(draw.call_count, 1)
        before = build_save_data(engine)
        with patch.object(competence, "draw_d6", side_effect=denied):
            replay = engine.process_command("Adjust the wheel")
        self.assertEqual(replay["contextual_action"]["status"], "replayed")
        self.assertEqual(build_save_data(engine), before)

    def test_policy_failure_cannot_publish_partial_candidate_or_lose_authorization(self):
        engine = GameEngine(MARKET)
        engine.process_command("Adjust the wheel")
        before, scene, focus = build_save_data(engine), engine.get_scene_snapshot(), engine.get_action_context()
        with patch.object(contextual_action, "decide_activity_control",
                          side_effect=ValueError("injected policy failure")):
            with self.assertRaises(ValueError):
                engine.process_command("yes")
        self.assertEqual(build_save_data(engine), before)
        self.assertEqual(engine.get_scene_snapshot(), scene)
        self.assertEqual(engine.get_action_context(), focus)


if __name__ == "__main__":
    unittest.main()
