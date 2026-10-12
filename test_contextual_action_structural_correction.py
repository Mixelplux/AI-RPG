"""Bounded epistemic objectives and material follow-through through production CLI."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine import character_competence as competence, game_engine, material_state as material
from engine.contextual_action import interpret
from engine.game_engine import GameEngine
from engine.save_system import build_save_data, load_game
from engine.world_state import validate_world_state
import test_contextual_action_owner_correction as smoke

MARKET = smoke.MARKET
OUTPUT = Path(".artifacts/contextual_action_structural_correction")
OBJECTIVE = "I want to inspect the crooked wheel and see if I can fix its fitting."


def cli(name, commands, *, draw=6, region_path=MARKET):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with patch.object(smoke, "OUTPUT", OUTPUT):
        engine, trace, text, draws = smoke.run_cli(commands, draw=draw, region_path=region_path)
    (OUTPUT / (name + "_cli.txt")).write_text(text, encoding="utf-8")
    (OUTPUT / (name + "_trace.json")).write_text(json.dumps(trace, indent=2), encoding="utf-8")
    return engine, trace, draws


def record(engine):
    return engine.get_world_state()[material.STATE_KEY]["delivery_cart"]


def status(row):
    return row["result"]["contextual_action"]["status"]


class StructuralCorrection(unittest.TestCase):
    def setUp(self):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        self.guard = patch("engine.narration_source.OpenAI", side_effect=smoke.denied)
        self.guard.start()
        self.addCleanup(self.guard.stop)

    def test_01_assessment_and_optional_adjustment_are_read_only(self):
        phrases = (OBJECTIVE,
                   "Inspect the crooked wheel and check if I can adjust its fitting",
                   "I would like to examine the wheel and see whether I could repair its fitting",
                   "See if I can fix the wheel fitting",
                   "Find out whether I can adjust the fitting",
                   "Inspect the wheel and see if I can fix its fitting without touching it")
        for index, phrase in enumerate(phrases):
            with self.subTest(phrase=phrase):
                engine, trace, draws = cli("assessment_" + str(index), [phrase, "confirm"])
                self.assertEqual(status(trace[0]), "assessed")
                self.assertIn("adjust the crooked wheel fitting", trace[0]["result"]["message"])
                self.assertEqual(trace[0]["before_material"], trace[0]["after_material"])
                self.assertEqual(status(trace[1]), "clarification_needed")
                self.assertEqual(engine.get_world_state(), GameEngine(MARKET).get_world_state())
                self.assertIsNone(engine.get_action_context()["pending"])
                self.assertEqual(draws, 0)

    def test_02_assessment_retires_pending_authorization(self):
        engine, trace, draws = cli("pending_assessment", ["Fix the wheel fitting", OBJECTIVE, "yes, do it"])
        self.assertEqual([status(r) for r in trace], ["authorization_required", "assessed", "clarification_needed"])
        self.assertEqual(engine.get_world_state(), GameEngine(MARKET).get_world_state())
        self.assertEqual(draws, 0)

    def test_03_conditional_commitments_still_fail_closed(self):
        phrases = ("Confirm if I can fix the wheel", "Fix the fitting if Tessa agrees",
                   "Yes, do it if I can fix the fitting", "Fix the fitting only if it is safe",
                   "Inspect the wheel and see if I can fix it if Tessa agrees",
                   "Inspect the wheel if I can fix its fitting",
                   "Inspect the wheel and see if I can fix it, but only if it is safe")
        for index, phrase in enumerate(phrases):
            with self.subTest(phrase=phrase):
                engine, trace, draws = cli("conditional_" + str(index), ["Fix the wheel fitting", phrase, "confirm"])
                self.assertEqual(status(trace[1]), "clarification_needed")
                self.assertEqual(status(trace[2]), "clarification_needed")
                self.assertEqual(engine.get_world_state(), GameEngine(MARKET).get_world_state())
                self.assertEqual(draws, 0)

    def test_04_direct_adjustment_requires_disclosure_and_executes_once(self):
        for index, phrase in enumerate(("I want to fix the wheel fitting", "Adjust the crooked wheel fitting",
                                       "Repair the cart's fitting", "Straighten the wheel")):
            with self.subTest(phrase=phrase):
                engine, trace, draws = cli("direct_" + str(index), [phrase, "yes, do it", "confirm", phrase])
                self.assertEqual(status(trace[0]), "authorization_required")
                self.assertIn("can jam", trace[0]["result"]["message"])
                self.assertIn("1 hour", trace[0]["result"]["message"])
                self.assertEqual(trace[0]["before_material"], trace[0]["after_material"])
                self.assertEqual(status(trace[1]), "accepted")
                self.assertEqual(draws, 1)
                self.assertEqual(record(engine)["conditions"]["fitting"], "aligned")
                self.assertEqual(record(engine)["conditions"]["position"], "blocked")
                self.assertEqual(record(engine)["cooperation"], "unasked")
                self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"], 1)
                self.assertTrue(all(r["outcomes"] == 1 for r in trace[1:]))

    def test_05_all_fitting_draws_cost_persistence_and_feasibility(self):
        for draw in range(1, 7):
            expected = competence.resolve(draw, False)
            engine, trace, draws = cli("fitting_" + str(draw), [OBJECTIVE, "Fix the wheel fitting", "confirm", "inspect wheel", "Fix the fitting", "confirm"], draw=draw)
            self.assertEqual(trace[2]["result"]["contextual_action"]["outcome"], expected)
            self.assertEqual(record(engine)["conditions"], dict(stability="braced", fitting={"full":"aligned", "partial":"seated", "failure":"jammed"}[expected], position="blocked", integrity="intact"))
            self.assertEqual(draws, 1)
            self.assertTrue(all(r["outcomes"] == 1 for r in trace[2:]))
            self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"], 1)
            adjust = engine.assess_contextual_action(interpret(engine, "Adjust the fitting"))
            move = engine.assess_contextual_action(interpret(engine, "Move the cart"))
            self.assertEqual(adjust["status"], "uncertain" if expected == "partial" else "impossible")
            self.assertEqual(move["status"], "impossible" if expected == "failure" else "uncertain")
            saved = build_save_data(engine)
            self.assertEqual(saved["save_version"], 1)
            path = OUTPUT / ("fitting_" + str(draw) + "_save.json")
            path.write_text(json.dumps(saved), encoding="utf-8")
            restored = load_game(str(path))
            self.assertEqual(build_save_data(restored), saved)
            self.assertIsNone(restored.get_action_context()["pending"])
            validate_world_state(restored.get_world_state(), restored.region)

    def test_06_full_adjustment_then_implicit_cooperation_and_movement(self):
        engine, trace, draws = cli("fitting_followthrough", [OBJECTIVE, "Fix the wheel fitting", "confirm", "inspect wheel",
                                  "Now let's move the cart out of the passage", "confirm", "confirm"], draw=(6, 6))
        self.assertEqual(status(trace[0]), "assessed")
        self.assertEqual(status(trace[4]), "authorization_required")
        self.assertEqual(trace[4]["before_material"], trace[4]["after_material"])
        self.assertEqual(trace[4]["after_material"]["delivery_cart"]["cooperation"], "unasked")
        self.assertEqual(trace[5]["result"]["contextual_action"]["outcome"], "full")
        self.assertEqual(record(engine)["conditions"], dict(stability="braced", fitting="aligned", position="clear", integrity="intact"))
        self.assertEqual(record(engine)["cooperation"], "willing")
        self.assertEqual(draws, 2)
        self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"], 2)
        history = engine.get_world_state()["history"]
        self.assertFalse(any(e["event_type"] == "material_cooperation" for e in history))
        preparation = next(e for e in history if e["event_type"] == "material_preparation" and e["method_id"] == "coordinated_shift")
        self.assertTrue(preparation["risk_authorized"])
        self.assertIn("request", preparation["summary"])
        self.assertEqual(preparation["cooperation_after"], "willing")
        validate_world_state(engine.get_world_state(), engine.region)

    def test_07_partial_fitting_followthrough_revalidates_timed_change(self):
        engine, trace, draws = cli("partial_fitting_followthrough", [OBJECTIVE, "Adjust the fitting", "confirm", "Move the cart", "yes, do it"], draw=(3, 6))
        self.assertEqual(trace[2]["result"]["contextual_action"]["outcome"], "partial")
        self.assertEqual(trace[4]["result"]["contextual_action"]["outcome"], "full")
        self.assertEqual(record(engine)["conditions"]["fitting"], "seated")
        self.assertEqual(record(engine)["conditions"]["position"], "clear")
        self.assertEqual(draws, 2)
        self.assertEqual(sum(e["event_type"] == "material_development" for e in engine.get_world_state()["history"]), 1)
        validate_world_state(engine.get_world_state(), engine.region)

    def test_08_failed_adjustment_refusal_and_no_assistance(self):
        engine, trace, draws = cli("failed_fitting_refusal", [OBJECTIVE, "Adjust the fitting", "confirm", "ask tessa if she needs help", "ask tessa to help", "Move the cart", "confirm"], draw=1)
        self.assertEqual(trace[2]["result"]["contextual_action"]["outcome"], "failure")
        self.assertEqual(status(trace[3]), "answered")
        self.assertIn("refuses", trace[4]["result"]["message"])
        self.assertEqual(record(engine)["cooperation"], "refused")
        self.assertEqual(record(engine)["conditions"]["position"], "blocked")
        self.assertEqual(draws, 1)
        self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"], 1)

    def test_09_partial_movement_then_different_approach_needs_new_authorization(self):
        engine, trace, draws = cli("partial_cart_different_approach", ["Move the cart without damaging cargo", "confirm", "inspect wheel",
                                  "Adjust the fitting", "Force the cart aside alone", "cancel action", "Force the cart aside alone", "confirm", "confirm"], draw=(3, 6))
        self.assertEqual(trace[1]["result"]["contextual_action"]["outcome"], "partial")
        self.assertEqual(status(trace[3]), "impossible")
        self.assertEqual(status(trace[4]), "constraint_conflict")
        self.assertEqual(status(trace[6]), "authorization_required")
        self.assertIn("damage the cargo", trace[6]["result"]["message"])
        self.assertEqual(trace[7]["result"]["contextual_action"]["outcome"], "full")
        self.assertEqual(record(engine)["conditions"]["position"], "clear")
        self.assertEqual(draws, 2)
        self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"], 2)
        validate_world_state(engine.get_world_state(), engine.region)

    def test_10_absent_helper_and_refusal_with_otherwise_feasible_method(self):
        for case in ("absent", "refusing"):
            region = json.loads(Path(MARKET).read_text(encoding="utf-8"))
            if case == "absent":
                region["entities"][0]["location"] = "side_lane"
            else:
                region["material_targets"][0]["cooperation"]["refuse_when"] = {"fitting":"crooked"}
            path = OUTPUT / (case + "_market.json")
            path.write_text(json.dumps(region), encoding="utf-8")
            engine, trace, draws = cli(case + "_helper", ["Now let's move the cart out of the passage", "confirm", "ask tessa to help", "Move the cart"], region_path=str(path))
            self.assertEqual(status(trace[0]), "impossible" if case == "absent" else "refused")
            self.assertEqual(draws, 0)
            self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"], 0)
            self.assertEqual(record(engine)["conditions"]["position"], "blocked")
            self.assertEqual(record(engine)["cooperation"], "unasked" if case == "absent" else "refused")
            self.assertFalse(any(e["event_type"] == "material_preparation" for e in engine.get_world_state()["history"]))
            validate_world_state(engine.get_world_state(), engine.region)

    def test_11_changed_circumstances_interrupt_fitting_without_draw(self):
        engine, trace, draws = cli("fitting_interrupted", ["wait", "Fix the fitting", "confirm", "confirm"])
        self.assertEqual(status(trace[1]), "authorization_required")
        self.assertEqual(status(trace[2]), "interrupted")
        self.assertEqual(draws, 0)
        self.assertEqual(record(engine)["conditions"]["fitting"], "crooked")
        self.assertEqual(record(engine)["conditions"]["position"], "narrow")
        self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"], 2)
        validate_world_state(engine.get_world_state(), engine.region)

    def test_12_atomic_fitting_publication_and_confirmation_constraints(self):
        engine = GameEngine(MARKET)
        engine.process_command("Fix the fitting")
        before = (engine.get_world_state(), engine.get_scene_snapshot(), engine.get_action_context())
        with patch.object(game_engine, "build_scene", side_effect=ValueError("injected")), patch.object(competence, "draw_d6", return_value=6):
            with self.assertRaises(ValueError): engine.process_command("confirm")
        self.assertEqual((engine.get_world_state(), engine.get_scene_snapshot(), engine.get_action_context()), before)
        engine, trace, draws = cli("fitting_constraints", [OBJECTIVE, "Fix the fitting without touching it", "confirm", "Fix the fitting", "yes, do it"])
        self.assertEqual(status(trace[1]), "constraint_conflict")
        self.assertEqual(status(trace[3]), "constraint_conflict")
        self.assertEqual(draws, 0)
        self.assertEqual(engine.get_world_state(), GameEngine(MARKET).get_world_state())

    def test_13_contextual_fitting_rephrasing_confirms_only_disclosed_method(self):
        engine, trace, draws = cli("fitting_contextual_confirmation", [OBJECTIVE, "Repair the wheel fitting", "Adjust the fitting", "confirm"])
        self.assertEqual(status(trace[1]), "authorization_required")
        self.assertEqual(trace[2]["result"]["contextual_action"]["outcome"], "full")
        self.assertEqual(status(trace[3]), "clarification_needed")
        self.assertEqual(draws, 1)
        self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"], 1)


if __name__ == "__main__":
    unittest.main()
