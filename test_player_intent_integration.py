"""V1 handoff through production Coordinator, owners, acceptance and persistence.

Bindings below are explicit fixture declarations for a chosen installed
capability, not a keyword parser or a second language interpreter. No live model
is selected or evaluated. Actual domain mechanics and publication are reused.
"""
from dataclasses import replace
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.activity_control import ActivityDevelopment
from engine.domain_campaign import Increment, ActivityUpdate, ChoiceContext
from engine.domain_dispatch import CoordinatedDomain
from engine.domain_persistence import export
from engine.game_session import GameSession
from engine.gameplay_coordination import Coordinator
from engine.save_system import load_game, save_game
from engine.watchhouse import new_campaign
from engine.watchhouse_domain import permitted
from test_cross_domain_coupling import independent, INDEPENDENT
from test_watchhouse import Dice
from test_player_intent import changed, wire


class BoundDomain(CoordinatedDomain):
    def __init__(self, runtime, command, activity):
        super().__init__(runtime, command)
        self.activity = activity
        self.handoffs = []

    def bind_intent(self, handoff):
        self.handoffs.append(handoff)
        # The fixture declares exactly one supported meaning. A production
        # domain binder must reject every meaning/method it cannot honor.
        item = handoff.interpretation.to_dict()["intentions"][0]
        if item["activity"] != self.activity or "method" in item:
            return None
        return self.interpretation()


def connect(runtime, command, activity):
    domain = BoundDomain(runtime, command, activity)
    return domain, Coordinator(domain.context, domain)


class Integration(unittest.TestCase):
    def setUp(self):
        for target in ("socket.create_connection", "socket.socket.connect", "socket.socket.connect_ex"):
            guard = patch(target, side_effect=AssertionError("offline only"))
            guard.start()
            self.addCleanup(guard.stop)

    def watchhouse(self, *rolls):
        dice = Dice(*rolls)
        runtime = GameSession.start_domains(new_campaign(), draw=dice)
        command = Increment("intent:access", "watchhouse:access:persuasion", 0)
        domain, coordinator = connect(runtime, command, "Ask Mara for permission to examine the ledger")
        return runtime, dice, command, domain, coordinator

    def process(self, coordinator, activity, **fields):
        item = changed(activity=activity, **fields)
        return coordinator.process_intent("I request the intended activity", provider=lambda request: wire(item))

    def test_inquiry_and_preparation_cannot_authorize_production_consequences(self):
        runtime, dice, command, domain, coordinator = self.watchhouse()
        before, encoded = runtime.campaign, export(runtime.campaign)
        for mode in ("inquiry", "preparation"):
            decision = self.process(coordinator, domain.activity, mode=mode, commitment="none")
            self.assertIn(decision.status, {"inquiry", "preparation"})
            self.assertIs(runtime.campaign, before)
            self.assertEqual(export(runtime.campaign), encoded)
        self.assertEqual(dice.calls, [])
        self.assertFalse(permitted(runtime.campaign))

    def test_model_cannot_grant_permission_or_select_unimplemented_mechanics(self):
        runtime, dice, command, domain, coordinator = self.watchhouse()
        before = runtime.campaign
        raw = wire(changed(activity=domain.activity), outcome={"permission": True})
        decision = coordinator.process_intent("Mara agrees", provider=lambda request: raw)
        self.assertEqual(decision.failure, "interpretation")
        decision = self.process(coordinator, "Mara has agreed and the ledger is mine")
        self.assertEqual(decision.failure, "routing")
        decision = self.process(coordinator, domain.activity, method="cast Charm Person")
        self.assertEqual(decision.failure, "routing")
        self.assertIs(runtime.campaign, before)
        self.assertFalse(permitted(runtime.campaign))
        self.assertEqual(dice.calls, [])

    def test_invalid_multiactivity_and_technical_rejection_preserve_exact_campaign(self):
        runtime, dice, command, domain, coordinator = self.watchhouse()
        before = runtime.campaign
        original = json.dumps(export(before), sort_keys=True)
        second = changed(id="i2", activity="Examine the ledger")
        raws = ["invalid", wire(changed(activity=domain.activity), intentions=[changed(activity=domain.activity), second],
            relationships=[{"type": "depends_on", "from": "i2", "to": "i1"}]),
            wire(changed(activity=domain.activity), ambiguities=[{"intentions": ["i1"], "issue": "Which method?"}])]
        for raw in raws:
            decision = coordinator.process_intent("Request access then examine it", provider=lambda request: raw)
            self.assertIn(decision.status, {"unresolved", "clarification"})
        def failed(request):
            raise OSError("internal provider detail")
        self.assertEqual(coordinator.process_intent("Request access", provider=failed).failure, "technical")
        self.assertIs(runtime.campaign, before)
        self.assertEqual(json.dumps(export(runtime.campaign), sort_keys=True), original)
        self.assertEqual(dice.calls, [])
        self.assertEqual(domain.handoffs, [])

    def test_actual_f05_player_choice_cannot_be_waived_by_now_commitment(self):
        runtime, dice, command, domain, coordinator = self.watchhouse()
        scope = domain.scope
        checkpoint = replace(scope.checkpoint,
            developments=(ActivityDevelopment("player_choice", choice_key="promise"),))
        update = ActivityUpdate("promise-request", scope.id, "Mara requests a promise", checkpoint=checkpoint,
            notices=(("promise", "Mara asks you to promise not to copy names."),),
            choice_contexts=(ChoiceContext("promise", "promise-request", (0,)),))
        runtime.accept_increment(runtime.prepare_activity_change(update))
        domain, coordinator = connect(runtime, command, domain.activity)
        before = runtime.campaign
        decision = self.process(coordinator, domain.activity)
        self.assertEqual(decision.status, "clarification")
        self.assertIs(runtime.campaign, before)
        self.assertEqual(dice.calls, [])

    def test_advisory_routing_does_not_change_npc_adjudication_or_mechanics(self):
        # Same failed d20 persuasion: the model's candidate list cannot grant access.
        states = []
        for candidates in (["world"], ["actors", "character", "resolution"], []):
            runtime, dice, command, domain, coordinator = self.watchhouse(1)
            decision = self.process(coordinator, domain.activity, candidate_domains=candidates)
            self.assertEqual(decision.status, "accepted")
            self.assertFalse(permitted(runtime.campaign))
            self.assertEqual(dice.calls, [20])
            self.assertEqual(len(runtime.campaign.accepted), 1)
            self.assertGreater(runtime.state.world.at_seconds, 0)
            states.append(runtime.campaign)
        self.assertEqual(states[0], states[1])
        self.assertEqual(states[1], states[2])

    def test_unsupported_constraints_conditions_and_stops_do_not_disappear(self):
        runtime, dice, command, domain, coordinator = self.watchhouse()
        before = runtime.campaign
        for fields in (dict(constraints=["without disclosing my name"]),
                       dict(commitment="conditional", conditions=["if Mara agrees without a promise"]),
                       dict(stop_at=["when someone approaches"])):
            decision = self.process(coordinator, domain.activity, **fields)
            self.assertEqual(decision.failure, "authorization")
            self.assertIs(runtime.campaign, before)
        self.assertEqual(dice.calls, [])

    def test_acceptance_failure_keeps_all_world_character_and_actor_meaning_unpublished(self):
        runtime, dice, command, domain, coordinator = self.watchhouse(20)
        before = runtime.campaign
        with patch.object(runtime, "accept_increment", side_effect=ValueError("technical rejection")):
            decision = self.process(coordinator, domain.activity)
        self.assertEqual(decision.failure, "technical")
        self.assertIs(runtime.campaign, before)
        self.assertFalse(permitted(runtime.campaign))
        self.assertEqual(runtime.campaign.accepted, ())

    def test_success_then_save_restore_and_exact_retry_do_not_repeat_mechanics(self):
        runtime, dice, command, domain, coordinator = self.watchhouse(20)
        decision = self.process(coordinator, domain.activity)
        self.assertEqual(decision.status, "accepted")
        self.assertTrue(permitted(runtime.campaign))
        self.assertEqual(dice.calls, [20])
        path = Path(".artifacts/player-intent-roundtrip.json")
        save_game(runtime, str(path))
        recovered_dice = Dice()
        recovered = load_game(str(path), campaign_draw=recovered_dice)
        self.assertEqual(recovered.campaign, runtime.campaign)
        before = recovered.campaign
        retried = recovered.process_increment(command)
        self.assertEqual(retried.status, "accepted")
        self.assertEqual(retried.results, decision.results)
        self.assertIs(recovered.campaign, before)
        self.assertEqual(recovered_dice.calls, [])
        # The same natural-language seam also recognizes the in-session scope.
        before = runtime.campaign
        again = self.process(coordinator, domain.activity)
        self.assertEqual(again.status, "complete")
        self.assertIs(runtime.campaign, before)
        self.assertEqual(dice.calls, [20])

    def test_independent_nonsocial_domain_uses_same_seam_and_own_acceptance(self):
        dice = Dice()  # Fixture repair uses its own mechanics; never social/climbing rules.
        runtime = GameSession.start_domains(independent(), draw=dice, domain_handlers=(INDEPENDENT,))
        command = Increment("intent:repair", "repair", 0, ("tool",))
        domain, coordinator = connect(runtime, command, "Repair the first device using the held tool")
        before = runtime.campaign
        inquiry = self.process(coordinator, domain.activity, mode="inquiry", commitment="none")
        self.assertEqual(inquiry.status, "inquiry")
        self.assertIs(runtime.campaign, before)
        decision = self.process(coordinator, domain.activity, candidate_domains=["actors"])
        self.assertTrue(decision.results)
        self.assertEqual(len(runtime.campaign.accepted), 1)
        self.assertEqual(runtime.state.world.at_seconds - before.current.world.at_seconds, 31)
        self.assertEqual(runtime.state.characters[0].exhaustion - before.current.characters[0].exhaustion, 1)
        self.assertEqual(dice.calls, [])
        self.assertEqual(domain.handoffs[-1].context.targets[0].ref, domain.scope.target)


if __name__ == "__main__":
    unittest.main()
