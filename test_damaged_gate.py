"""Offline behavioral integration, with network disabled for the whole suite."""
from copy import deepcopy
import json
import socket
import unittest
from unittest.mock import patch

from engine.damaged_gate import DamagedGate, GateFixture
from engine.narrative_realization import build_realization_request


class GateTests(unittest.TestCase):
    def test_ordinary_lift_language(self):
        for request in ("I lift the gate with the guard", "Let's raise the gate with assistance", "I heave the gate up"):
            with self.subTest(request=request):
                game = DamagedGate()
                turn = game.step(request)
                self.assertTrue(game.state["cart_passed"])
                self.assertTrue(game.state["damaged"])
                self.assertEqual(game.state["minutes"], 3)
                self.assertEqual(turn["control"].status, "complete")
                self.assertIn("guard", turn["text"])

    def test_inquiry_is_not_commitment(self):
        for request in ("Could I lift the gate?", "Can we pry it open?", "How could I repair it?", "Would lifting work?", "What can I do?", "I consider lifting it", "I might repair it", "Should we pry it?"):
            game = DamagedGate()
            turn = game.step(request)
            self.assertEqual(turn["intent"], "inquiry")
            self.assertEqual(game.state["attempts"], {})
            self.assertEqual(game.state["minutes"], 0)

    def test_prepare_and_help_do_not_commit(self):
        game = DamagedGate()
        game.step("Ask the guard to help lift the gate")
        game.step("Get the timber ready")
        game.step("Get the timber ready")
        self.assertEqual(game.state["minutes"], 1)
        self.assertEqual(game.state["attempts"], {})
        self.assertFalse(game.state["timber_used"])
        game.step("Prepare to lift the gate")
        self.assertEqual(game.state["attempts"], {})
        self.assertEqual(game.state["minutes"], 1)

    def test_tools_preparation_does_not_select_timber(self):
        game = DamagedGate()
        turn = game.step("Get the tools ready")
        self.assertIn("tools", turn["text"])
        self.assertTrue(game.state["tools_prepared"])
        self.assertFalse(game.state["prepared"])
        game = DamagedGate(GateFixture(tools=False))
        game.step("Get the tools ready")
        self.assertEqual(game.state["minutes"], 0)

    def test_inquiry_uses_current_means(self):
        for fixture, request in ((GateFixture(helper=False), "Can I lift it?"),
                                 (GateFixture(timber=False), "Could I pry it?"),
                                 (GateFixture(carpenter=False), "Could I repair it?"),
                                 (GateFixture(), "Can I lift it without damaging it?")):
            turn = DamagedGate(fixture).step(request)
            self.assertIn("not currently feasible", turn["text"])

    def test_explicit_renewal_changes_only_chosen_constraint(self):
        game = DamagedGate()
        game.step("Repair gate without timber")
        self.assertEqual(game.state["repair_stage"], "secured")
        game.step("Resume repair without timber")
        self.assertEqual(game.state["minutes"], 10)
        game.step("Resume repair with timber")
        self.assertEqual(game.state["minutes"], 35)

    def test_failure_result_reused_after_interruption(self):
        game = DamagedGate(GateFixture(repair="failure"))
        game.step("Repair gate")
        game.step("Resume repair with timber")
        game.step("Resume repair with timber")
        self.assertEqual(game.state["minutes"], 35)
        self.assertEqual(game.state["attempts"], {"repair": "failure"})
        self.assertTrue(game.state["damaged"])
        self.assertFalse(game.state["cart_passed"])

    def test_competence_and_examination(self):
        for competent in (True, False):
            game = DamagedGate(GateFixture(carpenter=competent, development="none"))
            turn = game.step("Examine the hinge")
            self.assertIn("carpentry" if competent else "cannot confidently", turn["text"])
            self.assertEqual(game.state["minutes"], 2)
            game.step("Inspect the gate")
            self.assertEqual(game.state["minutes"], 2)
            game.step("Repair the gate")
            self.assertEqual(game.state["cart_passed"], competent)

    def test_leverage_and_legitimate_failure_cost(self):
        for outcome in ("success", "failure"):
            game = DamagedGate(GateFixture(lever=outcome))
            game.step("Use the timber to open the gate")
            self.assertEqual(game.state["cart_passed"], outcome == "success")
            self.assertEqual(game.state["minutes"], 5)
            self.assertTrue(game.state["timber_used"])
            self.assertTrue(game.state["damaged"])
            game.step("Pry the gate open")
            self.assertEqual(game.state["minutes"], 5)

    def test_lift_failure_can_change_method(self):
        game = DamagedGate(GateFixture(lift="failure"))
        game.step("Lift the gate")
        game.step("Lift the gate")
        self.assertEqual(game.state["minutes"], 3)
        game.step("Use timber as leverage")
        self.assertTrue(game.state["cart_passed"])
        self.assertEqual(game.state["minutes"], 8)

    def test_missing_means_and_restrictions(self):
        for fixture, command in ((GateFixture(helper=False), "lift the gate"),
                                 (GateFixture(timber=False), "pry the gate"),
                                 (GateFixture(tools=False), "repair the gate"),
                                 (GateFixture(), "lift the gate alone"),
                                 (GateFixture(), "pry the gate without timber"),
                                 (GateFixture(), "repair the gate without damaging it")):
            game = DamagedGate(fixture)
            game.step(command)
            self.assertEqual(game.state["attempts"], {})
            self.assertEqual(game.state["minutes"], 0)

    def test_meaningful_interruption_and_resumption(self):
        game = DamagedGate()
        turn = game.step("Repair the gate")
        self.assertEqual(turn["control"].reason, "player_choice")
        self.assertEqual(game.state["repair_stage"], "secured")
        self.assertEqual(game.state["minutes"], 10)
        self.assertEqual(game.state["pins"], 1)
        attempts = deepcopy(game.state["attempts"])
        game.step("Stop for now")
        game.step("Continue repair")
        self.assertEqual(game.state["minutes"], 10)
        turn = game.step("Resume the repair with the timber brace")
        self.assertEqual(turn["control"].status, "complete")
        self.assertEqual(turn["control"].resolution, "reuse")
        self.assertEqual(game.state["minutes"], 35)
        self.assertEqual(game.state["attempts"], attempts)
        self.assertEqual(game.state["pins"], 1)
        self.assertTrue(game.state["timber_used"])
        self.assertFalse(game.state["damaged"])
        game.step("Repair the gate")
        self.assertEqual(game.state["minutes"], 35)

    def test_repair_restrictions_apply_equally_before_and_after_interruption(self):
        def physical_state(game):
            return {k: v for k, v in game.state.items() if k not in {"history", "turn"}}

        for condition in ("without further damage", "without damage", "don't damage"):
            for outcome in ("success", "failure"):
                with self.subTest(condition=condition, outcome=outcome):
                    initial = DamagedGate(GateFixture(repair=outcome))
                    untouched = physical_state(initial)
                    rejected = initial.step("repair the hinge " + condition)
                    self.assertEqual(rejected["control"].reason, "authorization_constraint")
                    self.assertEqual(physical_state(initial), untouched)

                    game = DamagedGate(GateFixture(repair=outcome))
                    game.step("repair the hinge")
                    secured = physical_state(game)
                    history = game.state["history"]
                    self.assertEqual((secured["minutes"], secured["pins"], secured["repair_stage"]),
                                     (10, 1, "secured"))
                    for request in ("continue repair with timber ", "finish with timber brace "):
                        turn = game.step(request + condition)
                        self.assertEqual((turn["control"].status, turn["control"].reason),
                                         (rejected["control"].status, rejected["control"].reason))
                        self.assertEqual(turn["control"].resolution, "reuse")
                        self.assertEqual(turn["context"]["player_intent"]["constraints"], ["no_damage"])
                        self.assertEqual(physical_state(game), secured)
                        self.assertEqual(game.state["history"][:len(history)], history)
                        self.assertIn("restriction", turn["text"])
                        self.assertNotIn("timber is unavailable", turn["text"])

                    completed = game.step("use timber to brace")
                    self.assertEqual(completed["control"].resolution, "reuse")
                    self.assertEqual(completed["control"].status, "complete")
                    self.assertEqual((game.state["minutes"], game.state["pins"]), (35, 1))
                    self.assertTrue(game.state["timber_used"])
                    self.assertEqual(game.state["attempts"], {"repair": outcome})
                    self.assertEqual(game.state["cart_passed"], outcome == "success")
                    finished = physical_state(game)
                    for request in ("use timber to brace", "repair the hinge",
                                    "continue repair with timber " + condition):
                        game.step(request)
                        self.assertEqual(physical_state(game), finished)

    def test_current_means_on_resume(self):
        game = DamagedGate()
        game.step("Repair the gate")
        game.step("Pry the gate")  # Uses timber; this changed method is explicitly chosen.
        game.step("Resume repair with timber")
        self.assertEqual(game.state["repair_stage"], "secured")
        self.assertEqual(game.state["minutes"], 15)
        self.assertEqual(game.state["pins"], 1)

    def test_contextual_bracing_authorizes_only_existing_repair(self):
        for request in ("brace the gate", "use timber to brace", "finish with timber brace",
                        "I use the timber to brace the hinge", "Please brace it with timber",
                        "finish the repair with a timber brace"):
            with self.subTest(request=request):
                game = DamagedGate()
                if "repair" not in request:  # Existing explicit repair vocabulary is unchanged.
                    game.step(request)
                    self.assertEqual(game.state["attempts"], {})
                    self.assertEqual(game.state["minutes"], 0)
                game.step("repair the hinge")
                turn = game.step(request)
                self.assertEqual(turn["intent"], "resume")
                self.assertEqual(turn["control"].resolution, "reuse")
                self.assertEqual(game.state["repair_stage"], "finished")
                self.assertEqual(game.state["minutes"], 35)
                self.assertEqual(game.state["pins"], 1)
                self.assertTrue(game.state["timber_used"])
                self.assertTrue(game.state["cart_passed"])
                for repeated in (request, "use timber to brace", "repair the hinge"):
                    game.step(repeated)
                self.assertEqual(game.state["minutes"], 35)
                self.assertEqual(game.state["pins"], 1)
                self.assertEqual(game.state["attempts"], {"repair": "success"})

    def test_paused_repair_ambiguity_inquiry_and_rejection_preserve_work(self):
        game = DamagedGate()
        game.step("examine the gate")
        game.step("repair the hinge")
        before = {k: v for k, v in game.state.items() if k not in {"history", "turn"}}
        for request in ("brace", "continue with repair", "continue repair", "use timber",
                        "Can I use timber to brace?", "I might finish with timber brace",
                        "Prepare to brace the gate", "brace the cart", "brace the gate with rope",
                        "use timber to brace then lift the gate", "finish with timber brace if safe",
                        "don't brace the gate", "brace the gate without timber"):
            with self.subTest(request=request):
                turn = game.step(request)
                self.assertEqual({k: v for k, v in game.state.items() if k not in {"history", "turn"}}, before)
                self.assertNotIn("No attempt has begun", turn["text"])
                if turn["intent"] == "unsupported":
                    self.assertIn("hinge remains secured", turn["text"])
                    self.assertIn("committed pin remain", turn["text"])
        turn = game.step("continue with repair")
        self.assertEqual(turn["intent"], "resume")
        self.assertIn("choose whether", turn["text"])
        game.step("finish with timber brace")
        self.assertEqual(game.state["minutes"], 37)
        self.assertEqual(game.state["pins"], 1)

    def test_bracing_reuses_failure_and_checks_current_means(self):
        for request in ("use timber to brace", "finish with timber brace", "brace the gate"):
            for fixture in (GateFixture(repair="failure"), GateFixture(timber=False)):
                with self.subTest(request=request, fixture=fixture):
                    game = DamagedGate(fixture)
                    game.step("repair the hinge")
                    game.step(request)
                    game.step(request)
                    self.assertEqual(game.state["pins"], 1)
                    self.assertEqual(game.state["attempts"], {"repair": fixture.repair})
                    self.assertEqual(game.state["minutes"], 35 if fixture.timber else 10)
                    self.assertTrue(game.state["damaged"])
                    self.assertFalse(game.state["cart_passed"])
            game = DamagedGate()
            game.step("repair without timber")
            game.step(request)  # Explicitly renew the previously withheld means.
            self.assertEqual(game.state["minutes"], 35)

    def test_non_interruption_and_repair_failure(self):
        for development in ("ordinary", "none"):
            for outcome in ("success", "failure"):
                game = DamagedGate(GateFixture(development=development, repair=outcome))
                turn = game.step("Fix the gate")
                self.assertEqual(turn["control"].status, "complete")
                self.assertEqual(game.state["minutes"], 30)
                self.assertEqual(game.state["pins"], 1)
                self.assertEqual(game.state["cart_passed"], outcome == "success")
                self.assertEqual(game.state["damaged"], outcome == "failure")
                self.assertFalse(game.state["timber_used"])

    def test_unavailable_support_does_not_erase_work(self):
        game = DamagedGate(GateFixture(timber=False))
        game.step("Repair gate")
        game.step("Resume repair with timber")
        self.assertEqual(game.state["minutes"], 10)
        self.assertEqual(game.state["repair_stage"], "secured")

    def test_unsupported_never_substitutes(self):
        for request in ("Burn the gate", "Lift it with a rope", "Lift then repair the gate", "Lift it if safe", "I lift the gate and attack the guard", "lift the gate with timber", "Clear the cart", "Repair the cart", "Lift the cart", "Repair the gate with dynamite", "repair with no tools"):
            game = DamagedGate()
            turn = game.step(request)
            self.assertEqual(turn["intent"], "unsupported", request)
            self.assertEqual(game.state["attempts"], {})
            self.assertEqual(game.state["minutes"], 0)

    def test_contract_provenance_access_continuity(self):
        game = DamagedGate()
        for request in ("look at the cart", "Examine hinge", "repair gate", "continue repair with timber", "look"):
            turn = game.step(request)
            context = turn["context"]
            self.assertEqual(json.loads(build_realization_request(context)["input"]), context)
            records = context["developments"] + context["continuity"]
            belief = [r for r in records if r["status"] == "reported"]
            self.assertEqual(len(belief), 1)
            self.assertIn("unverified belief", belief[0]["meaning"])
            self.assertEqual(len({r["id"] for r in records}), len(records))
            self.assertTrue(all(r["source"] and r["access"] and r["time"] for r in records))
        self.assertIn("repaired", turn["context"]["developments"][-1]["meaning"])
        self.assertNotIn("willing to help lift", turn["context"]["developments"][-1]["meaning"])

    def test_realization_is_non_authoritative_no_reexecution(self):
        game = DamagedGate()
        turn = game.step("lift gate")
        before = game.state
        calls = []

        def fake(**request):
            calls.append(json.loads(request["input"]))
            return "The guard helps you lift it; the cart clears, but the hinge remains damaged."

        self.assertEqual(game.present(turn, fake)["status"], "candidate")
        self.assertEqual(calls, [turn["context"]])
        self.assertEqual(game.present(turn, lambda **k: "You acquire a magic sword.")["status"], "candidate")
        self.assertEqual(game.present(turn, lambda **k: None)["status"], "unavailable")
        self.assertEqual(game.state, before)  # Structural success deliberately is not fidelity proof.

    def test_contract_failure_is_atomic(self):
        game = DamagedGate()
        before = game.state
        with patch("engine.damaged_gate.validate_context", side_effect=ValueError("bad context")):
            with self.assertRaises(ValueError):
                game.step("repair gate")
        self.assertEqual(game.state, before)


if __name__ == "__main__":
    with patch.object(socket.socket, "connect", side_effect=AssertionError("Offline tests must not connect")):
        unittest.main()
