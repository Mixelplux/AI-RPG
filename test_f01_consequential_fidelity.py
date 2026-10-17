"""Offline consequence/decision contract regressions, not a semantic prose judge.

Historical bad prose demonstrates the structural validator's limit. Authored
references demonstrate permitted selection; they do not predict model behavior.
"""
from copy import deepcopy
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from engine.damaged_gate import DamagedGate, GateFixture
from engine.narrative_realization import build_realization_request, realize


class ConsequentialFidelityTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(Path("test_fixtures/f01_consequential_decision.json").read_text(encoding="utf-8"))
        for guard in (patch.object(socket.socket, "connect", side_effect=AssertionError("offline")),
                      patch("socket.getaddrinfo", side_effect=AssertionError("offline"))):
            guard.start()
            self.addCleanup(guard.stop)
        self.game = DamagedGate()
        self.game.step("look")
        self.game.step("Examine the hinge")
        self.turn = self.game.step("Repair the gate")

    def test_preserved_case_is_reproduced_by_current_authority(self):
        self.assertEqual(self.turn["context"], self.fixture["context"])
        self.assertEqual(self.turn["control"].reason, "player_choice")
        self.assertEqual(self.game.state["pins"], 1)
        self.assertEqual(self.game.state["minutes"], 12)
        self.assertEqual(self.game.state["repair_stage"], "secured")
        self.assertFalse(self.game.state["timber_used"])

    def test_historical_omission_remains_structurally_valid(self):
        historical = self.fixture["recorded_omission"]
        self.assertNotIn("spare pin", historical)
        self.assertIn("commits one spare pin", self.turn["context"]["developments"][0]["meaning"])
        before = self.game.state
        # Never claim this correction implements semantic detection/rejection.
        result = self.game.present(self.turn, lambda **request: historical)
        self.assertEqual(result, {"status": "candidate", "text": historical})
        self.assertEqual(self.game.state, before)

    def test_revised_guidance_reaches_generator_without_changing_context(self):
        calls = []
        def generate(**request):
            calls.append(request)
            return self.fixture["authored_reference_prose"][0]
        context_before = deepcopy(self.turn["context"])
        result = self.game.present(self.turn, generate)
        self.assertEqual(len(calls), 1)
        self.assertEqual(json.loads(calls[0]["input"]), context_before)
        self.assertEqual(self.turn["context"], context_before)
        self.assertNotEqual(calls[0]["instructions"], self.fixture["original_instructions"])
        # Focused instruction regression, not keyword validation of generated prose.
        policy = " ".join(calls[0]["instructions"].split())
        self.assertIn("At a decision point", policy)
        self.assertIn("accepted work, commitments and consequential costs", policy)
        self.assertEqual(result["status"], "candidate")

    def test_authored_paraphrases_can_omit_irrelevant_inventory_and_caveats(self):
        before = self.game.state
        supplied = " ".join(r["meaning"] for r in self.turn["context"]["developments"])
        self.assertIn("Repair tools", supplied)
        self.assertIn("guard", supplied)
        for text in self.fixture["authored_reference_prose"]:
            self.assertIn("spare pin", text)
            self.assertNotIn("commits one spare pin", text)  # no verbatim-reproduction requirement
            self.assertNotIn("Repair tools", text)
            self.assertNotIn("guard", text)
            self.assertNotIn("unknown", text)
            self.assertNotIn("remains available", text)
            result = self.game.present(self.turn, lambda **request: text)
            self.assertEqual(result["text"], text)
            self.assertEqual(self.game.state, before)

    def test_record_order_does_not_remove_consequence_from_request(self):
        context = deepcopy(self.turn["context"])
        context["developments"].reverse()
        before = deepcopy(context)
        request = build_realization_request(context)
        cost = [r for r in json.loads(request["input"])["developments"] if r["status"] == "resolved"]
        self.assertEqual(len(cost), 1)
        self.assertIn("commits one spare pin", cost[0]["meaning"])
        self.assertEqual(context, before)

    def test_other_spent_means_and_failure_are_not_repaired_by_presentation(self):
        game = DamagedGate(GateFixture(lever="failure"))
        game.step("look")
        turn = game.step("Use timber as leverage")
        before = game.state
        calls = []
        def generate(**request):
            calls.append(json.loads(request["input"]))
            return "You lever at the gate for five minutes, but the timber splits. The cart is still blocked."
        self.assertEqual(game.present(turn, generate)["status"], "candidate")
        current = " ".join(r["meaning"] for r in calls[0]["developments"])
        self.assertIn("five minutes", current)
        self.assertIn("splits and is spent", current)
        self.assertTrue(game.state["timber_used"])
        self.assertEqual(game.state, before)

    def test_known_consequence_does_not_become_mandatory_recital_on_observation(self):
        turn = self.game.step("look")
        before = self.game.state
        self.assertTrue(any("commits one spare pin" in r["meaning"] for r in turn["context"]["continuity"]))
        text = "The hinge is secured, but its mounting still needs timber support before the repair can continue."
        self.assertEqual(self.game.present(turn, lambda **request: text)["text"], text)
        self.assertEqual(self.game.state, before)


if __name__ == "__main__":
    unittest.main()
