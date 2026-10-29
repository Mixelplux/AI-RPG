"""Offline end-to-end Watchhouse acceptance, epistemics and recovery evidence."""
import copy
import json
import socket
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from engine.activity_control import ActivityDevelopment
from engine.domain_campaign import Increment, Proposal, ActivityUpdate, ChoiceContext, validate_campaign
from engine.domain_activity import effective_scope
from engine.domain_persistence import export, restore
from engine.game_session import GameSession
from engine.information_adjudication import Unresolved
from engine.save_system import save_game, load_game
from engine.watchhouse import WatchhouseSession, new_campaign, interpret
from engine.watchhouse_domain import WATCHHOUSE, permitted, OBJECTIVE_TRUTH, REPORT, SEAL, STUDY
from engine.watchhouse_rules import INVESTIGATOR, check


ACCESS = 'I persuade Mara to let me examine the ledger'
REPORT_INPUT = 'I ask Mara for her account'
SEARCH = 'I search the ledger for signs of tampering'
STUDY_INPUT = 'I study the ledger notation'


class Dice:
    def __init__(self, *rolls):
        self.rolls, self.calls = list(rolls), []

    def __call__(self, sides):
        self.calls.append(sides)
        if not self.rolls:
            raise AssertionError('unexpected random draw')
        return self.rolls.pop(0)


class WatchhouseTests(unittest.TestCase):
    def test_new_urging_after_permission_is_independent_and_retry_safe(self):
        s, dice = self.session(20, 1)
        s.process(ACCESS, request_id='grant')
        threat = 'I request permission to examine the ledger by threatening to report her'
        reply = s.process(threat, request_id='threat')
        self.assertEqual(reply.status, 'accepted')
        self.assertIn('refuses', reply.message)
        self.assertTrue(permitted(s.runtime.campaign))
        self.assertIs(s.runtime.campaign.accepted[-1].evidence[2], False)
        # A different hesitant approach still needs its own check after a grant.
        s.process('I request permission to examine the ledger by performing a song', request_id='song')
        self.assertIs(s.runtime.campaign.accepted[-1].evidence[2], False)
        self.assertTrue(permitted(s.runtime.campaign))
        self.assertEqual(dice.calls, [20, 20])
        before_retry = s.runtime.campaign
        again = s.process('I request permission to examine the ledger by performing a song', request_id='new-song')
        self.assertNotEqual(again.status, 'accepted')
        self.assertIs(s.runtime.campaign, before_retry)
        path = Path('.artifacts/watchhouse-corrected-influence.json')
        save_game(s.runtime, str(path))
        recovered = WatchhouseSession(load_game(str(path), campaign_draw=Dice()))
        self.assertEqual(recovered.runtime.campaign, s.runtime.campaign)
        root = recovered.runtime.campaign
        self.assertEqual(recovered.process(threat, request_id='threat'), reply)
        self.assertIs(recovered.runtime.campaign, root)
        self.assertTrue(permitted(root))
        self.assertEqual(root.current.world.at_seconds, 180)

    def test_controlled_interpretations_use_existing_coordinator_and_owner(self):
        from engine.domain_dispatch import CoordinatedDomain
        from engine.gameplay_coordination import Coordinator, Interpretation
        s, dice = self.session(20)
        command = Increment('interpreted', 'watchhouse:access:persuasion', 0)
        adapter = CoordinatedDomain(s.runtime, command)
        intended = adapter.interpretation()
        before = s.runtime.campaign
        for proposal in (replace(intended, intent='inquiry'), replace(intended, intent='prepare'),
                         replace(intended, ambiguous=True), replace(intended, target='someone-else'),
                         replace(intended, method='intimidation')):
            decision = Coordinator(adapter.context, adapter).process(interpretation=proposal)
            self.assertNotEqual(decision.status, 'accepted')
            self.assertIs(s.runtime.campaign, before)
        self.assertEqual(dice.calls, [])
        decision = Coordinator(adapter.context, adapter).process(interpretation=intended)
        self.assertEqual(decision.status, 'accepted')
        self.assertTrue(permitted(s.runtime.campaign))
        self.assertEqual(dice.calls, [20])
        # Interpreted examination still cannot override the actor's permission.
        denied, no_dice = self.session()
        adapter = CoordinatedDomain(denied.runtime, Increment('search', 'watchhouse:search:perception', 0))
        before = denied.runtime.campaign
        decision = Coordinator(adapter.context, adapter).process(interpretation=adapter.interpretation())
        self.assertNotEqual(decision.status, 'accepted')
        self.assertIs(denied.runtime.campaign, before)
        self.assertEqual(no_dice.calls, [])

    @classmethod
    def setUpClass(cls):
        cls.network = patch.object(socket, 'create_connection', side_effect=AssertionError('offline only'))
        cls.network.start()

    @classmethod
    def tearDownClass(cls):
        cls.network.stop()

    def session(self, *rolls, **premises):
        dice = Dice(*rolls)
        return WatchhouseSession(GameSession.start_domains(new_campaign(**premises), draw=dice)), dice

    def test_inquiry_preparation_broad_goal_and_compound_do_not_commit(self):
        s, dice = self.session()
        before = s.runtime.campaign
        for text in ('Could I examine the ledger?', 'I want to solve the mystery',
                     'I prepare to question Mara', ACCESS + '?', ACCESS + ' and promise her a reward',
                     ACCESS + ' without mentioning my name', 'I threaten Mara',
                     'I cast Charm Person on Mara', 'I persuade Mara to give me her account then take the ledger'):
            result = s.process(text)
            self.assertIn(result.status, ('inquiry', 'clarification'))
            self.assertIs(s.runtime.campaign, before)
        self.assertEqual(dice.calls, [])

    def test_willing_report_preserves_claim_and_belief_without_roll(self):
        s, dice = self.session()
        self.assertEqual(s.process(REPORT_INPUT).status, 'accepted')
        self.assertIn(REPORT, s.process('What have I learned?').message)
        self.assertNotIn(OBJECTIVE_TRUTH, s.process('review findings').message)
        self.assertFalse(permitted(s.runtime.campaign))
        self.assertEqual(dice.calls, [])

    def test_unwilling_no_roll_or_ledger_transfer(self):
        s, dice = self.session()
        original = s.runtime.state.world.relationships
        reply = s.process('I persuade Mara to surrender the ledger')
        self.assertEqual(reply.status, 'accepted')
        self.assertIn('refuses', reply.message)
        self.assertEqual(s.runtime.state.world.relationships, original)
        self.assertFalse(permitted(s.runtime.campaign))
        self.assertEqual(dice.calls, [])

    def test_hesitant_success_accepts_access_time_and_then_evidence(self):
        s, dice = self.session(11, 8, 9)
        self.assertEqual(s.process(ACCESS).status, 'accepted')  # +4 => DC 15
        self.assertTrue(permitted(s.runtime.campaign))
        self.assertEqual(s.process(SEARCH).status, 'accepted')  # +3 => 11: fails
        self.assertNotIn(SEAL, s.process('review findings').message)
        self.assertEqual(s.process(STUDY_INPUT).status, 'accepted')  # +4 => 13
        self.assertIn(STUDY, s.process('review findings').message)
        self.assertEqual(s.runtime.state.world.at_seconds, 420)
        self.assertEqual(dice.calls, [20, 20, 20])

    def test_failed_influence_cooldown_cannot_be_evaded_with_new_id(self):
        s, dice = self.session(1, 20)
        self.assertEqual(s.process(ACCESS, request_id='first').status, 'accepted')
        before = s.runtime.campaign
        self.assertIn(s.process(ACCESS, request_id='second').status, ('clarification', 'unresolved'))
        self.assertIs(s.runtime.campaign, before)
        self.assertEqual(dice.calls, [20])
        reply = s.process('I request permission to examine the ledger by claiming I am an inspector')
        self.assertEqual(reply.status, 'accepted')
        self.assertTrue(permitted(s.runtime.campaign))
        self.assertEqual(dice.calls, [20, 20])

    def test_unsupported_effects_fail_closed_without_draw_or_knowledge(self):
        for field, value in (('conditions', ('poisoned',)), ('unresolved_rules', ('unknown',)), ('exhaustion', 6)):
            s, dice = self.session()
            before = s.runtime.campaign
            bad = replace(before.current.characters[0], **{field: value})
            state = replace(before.current, characters=(bad, before.current.characters[1]))
            # Trusted bootstrap premises, not an accepted mid-activity rewrite.
            root = replace(before, origin=state, current=state)
            s = WatchhouseSession(GameSession.start_domains(root, draw=dice))
            basis = s.runtime.campaign
            self.assertNotEqual(s.process(ACCESS).status, 'accepted')
            self.assertIs(s.runtime.campaign, basis)
            self.assertEqual(dice.calls, [])

    def test_no_search_or_study_without_legitimate_access(self):
        s, dice = self.session()
        before = s.runtime.campaign
        for text in (SEARCH, STUDY_INPUT):
            self.assertNotEqual(s.process(text).status, 'accepted')
            self.assertIs(s.runtime.campaign, before)
        self.assertEqual(dice.calls, [])

    def test_friendly_and_hostile_advantage_and_intelligence_dc(self):
        for attitude, rolls, expected in (('friendly', (1, 11), True), ('hostile', (20, 10), False),
                                          ('indifferent', (15,), False)):
            s, dice = self.session(*rolls, attitude=attitude, intelligence=20 if attitude == 'indifferent' else 12)
            self.assertEqual(s.process(ACCESS).status, 'accepted')
            self.assertEqual(permitted(s.runtime.campaign), expected)
            self.assertEqual(len(dice.calls), len(rolls))

    def test_ability_checks_have_no_automatic_natural_twenty_success(self):
        untrained = (1, 1, 1, 2, (0, 0, 0, 0, 0, 0))
        self.assertFalse(check(untrained, 'persuasion', 20, (20,)))
        self.assertTrue(check(INVESTIGATOR, 'persuasion', 5, (1,)))

    def test_explicit_player_methods_do_not_invent_a_lie_or_threat(self):
        s, dice = self.session()
        self.assertEqual(s.process('I deceive Mara to let me examine the ledger').status, 'clarification')
        result = s.process('I request permission to examine the ledger by threatening to report her')
        self.assertEqual(result.status, 'accepted')
        self.assertIn('refuses', result.message)
        self.assertFalse(permitted(s.runtime.campaign))
        self.assertEqual(dice.calls, [])

    def test_exact_retry_and_completed_examination_do_not_repeat_time_or_draw(self):
        s, dice = self.session(20, 20)
        first = s.process(ACCESS, request_id='permission')
        before = s.runtime.campaign
        self.assertEqual(s.process(ACCESS, request_id='permission'), first)
        self.assertIs(s.runtime.campaign, before)
        self.assertEqual(s.process(SEARCH, request_id='physical').status, 'accepted')
        before = s.runtime.campaign
        self.assertEqual(s.process(SEARCH).status, 'recorded')
        self.assertIs(s.runtime.campaign, before)
        self.assertIn(SEAL, s.process('review findings').message)
        self.assertEqual(dice.calls, [20, 20])

    def test_conflicting_request_id_cannot_reuse_prior_permission(self):
        s, dice = self.session(20)
        s.process(ACCESS, request_id='same')
        before = s.runtime.campaign
        self.assertEqual(s.process(SEARCH, request_id='same').status, 'unresolved')
        self.assertIs(s.runtime.campaign, before)
        self.assertEqual(dice.calls, [20])

    def test_forged_receipt_result_roll_and_permission_reject_atomically(self):
        s, dice = self.session(20)
        root = s.runtime.campaign
        proposal = s.runtime.prepare_increment(Increment('access', 'watchhouse:access:persuasion', 0))
        u = proposal.unit
        for forged in (
            replace(u, receipt=replace(u.receipt, accessible=(('watchhouse-result', OBJECTIVE_TRUTH),))),
            replace(u, evidence=((), 'access', True, 0)),
            replace(u, evidence=((20,), 'access', 1, 0)),
            replace(u, evidence=((21,), 'access', True, 0)),
            replace(u, evidence=((20,), 'access', True, 86400)),
            replace(u, progressed=False),
        ):
            with self.assertRaises((ValueError, Unresolved)):
                s.runtime.accept_increment(Proposal(root, forged))
            self.assertIs(s.runtime.campaign, root)
            self.assertFalse(permitted(s.runtime.campaign))
        self.assertEqual(s.runtime.accept_increment(proposal), u.receipt)

    def test_stale_proposal_does_not_publish_any_partial_result(self):
        s, dice = self.session(20)
        proposal = s.runtime.prepare_increment(Increment('access', 'watchhouse:access:persuasion', 0))
        s.process(REPORT_INPUT)
        before = s.runtime.campaign
        with self.assertRaises(Unresolved):
            s.runtime.accept_increment(proposal)
        self.assertIs(s.runtime.campaign, before)
        self.assertFalse(permitted(before))

    def test_changed_player_choice_returns_control_without_consequences(self):
        s, dice = self.session()
        scope = effective_scope(s.runtime.campaign, 'watchhouse:access:persuasion')
        cp = replace(scope.checkpoint, developments=(ActivityDevelopment('player_choice', choice_key='promise'),))
        event = ActivityUpdate('choice', scope.id, 'Mara asks for a promise', checkpoint=cp,
            notices=(('promise', 'Mara asks you to promise not to copy names. Do you agree?'),),
            choice_contexts=(ChoiceContext('promise', 'choice', (0,)),))
        s.runtime.accept_increment(s.runtime.prepare_activity_change(event))
        before = s.runtime.campaign
        reply = s.process(ACCESS)
        self.assertEqual(reply.status, 'clarification')
        self.assertIn('promise not to copy names', reply.message)
        self.assertIs(s.runtime.campaign, before)
        self.assertEqual(dice.calls, [])

    def test_save_restore_and_retries_reconstruct_without_randomness(self):
        s, dice = self.session(20, 20, 20)
        for identity, text in (('a', ACCESS), ('b', SEARCH), ('c', STUDY_INPUT)):
            self.assertEqual(s.process(text, request_id=identity).status, 'accepted')
        path = Path('.artifacts/watchhouse-roundtrip.json')
        save_game(s.runtime, str(path))
        raw = json.loads(path.read_text())
        self.assertEqual(raw['save_version'], 3)
        loaded = load_game(str(path), campaign_draw=Dice())
        recovered = WatchhouseSession(loaded)
        self.assertEqual(loaded.campaign, s.runtime.campaign)
        self.assertEqual(recovered.process('review findings'), s.process('review findings'))
        before = loaded.campaign
        self.assertEqual(recovered.process(ACCESS, request_id='a').status, 'accepted')
        self.assertIs(loaded.campaign, before)
        self.assertEqual(validate_campaign(restore(export(before))), before)

    def test_failed_attempt_wait_survives_restore(self):
        s, dice = self.session(1)
        s.process(ACCESS)
        restored = WatchhouseSession(GameSession.start_domains(restore(export(s.runtime.campaign)), draw=Dice()))
        before = restored.runtime.campaign
        self.assertNotEqual(restored.process(ACCESS).status, 'accepted')
        self.assertIs(restored.runtime.campaign, before)

    def test_corrupt_restore_preserves_existing_root(self):
        s, dice = self.session(20)
        s.process(ACCESS)
        root = s.runtime.campaign
        state = replace(root.current, world=replace(root.current.world, at_seconds=0))
        with self.assertRaises(ValueError):
            s.runtime.restore_domains(replace(root, current=state))
        self.assertIs(s.runtime.campaign, root)
        envelope = copy.deepcopy(export(root))
        envelope['domain_campaign']['fields']['schema'] = 5
        with self.assertRaises(ValueError):
            restore(envelope)

    def test_disk_replacement_failure_preserves_old_save_and_live_results(self):
        s, dice = self.session(20)
        path = Path('.artifacts/watchhouse-atomic.json')
        save_game(s.runtime, str(path))
        previous = path.read_bytes()
        s.process(ACCESS)
        root = s.runtime.campaign
        with patch('engine.save_system.os.replace', side_effect=OSError('injected replacement failure')):
            with self.assertRaises(OSError):
                save_game(s.runtime, str(path))
        self.assertEqual(path.read_bytes(), previous)
        self.assertIs(s.runtime.campaign, root)
        self.assertFalse(permitted(load_game(str(path)).campaign))

    def test_unknown_profile_and_conflicting_npc_facts_reject(self):
        for bad in ((True, 12, 14, 2, (1, 0, 0, 0, 1, 1)), (14, 12, 14, 2, (True,) * 6)):
            with self.assertRaises(ValueError):
                new_campaign(profile=bad)
        root = new_campaign()
        a = root.activities[0]
        stage = replace(a.stages[0], payload=(*a.payload[:5], 'hostile'))
        altered = replace(root, activities=(replace(a, stages=(stage,)), *root.activities[1:]))
        with self.assertRaises(ValueError):
            GameSession.start_domains(altered)

    def test_legacy_and_other_domain_roots_cannot_be_adopted_as_watchhouse(self):
        with self.assertRaises(ValueError):
            WatchhouseSession(object())
        from test_cross_domain_coupling import independent, INDEPENDENT
        with self.assertRaises(ValueError):
            WatchhouseSession(GameSession.start_domains(independent(), domain_handlers=(INDEPENDENT,)))

    def test_invalid_random_evidence_does_not_publish_or_disclose(self):
        for roll in (True, 0, 21):
            s, dice = self.session(roll)
            before = s.runtime.campaign
            self.assertEqual(s.process(ACCESS).status, 'unresolved')
            self.assertIs(s.runtime.campaign, before)
            self.assertFalse(permitted(before))

    def test_cli_save_load_and_player_examples_use_the_same_runtime(self):
        import io
        import play_watchhouse
        path = Path('.artifacts/watchhouse-cli.json')
        with patch('sys.argv', ['play_watchhouse.py', '--save', str(path)]), \
                patch('builtins.input', side_effect=['help', REPORT_INPUT, 'save', 'quit']), \
                patch('sys.stdout', new_callable=io.StringIO) as output:
            play_watchhouse.main()
        self.assertIn('Mara says', output.getvalue())
        self.assertIn('Saved.', output.getvalue())
        with patch('sys.argv', ['play_watchhouse.py', '--load', str(path)]), \
                patch('builtins.input', side_effect=['review findings', 'quit']), \
                patch('sys.stdout', new_callable=io.StringIO) as output:
            play_watchhouse.main()
        self.assertIn(REPORT, output.getvalue())


if __name__ == '__main__':
    unittest.main()
