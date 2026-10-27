"""Offline continuing play at the common Runtime boundary; no authored outcomes."""
import copy
import json
import socket
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from engine.activity_control import ActivityCheckpoint, ActivityDevelopment
from engine.historical_activity import (ActivityRun, ActivityStage, ActivityUpdate,
    ActivityResponse, ChoiceContext, effective_scope, successful_units)
from engine.historical_campaign import Increment, AcceptedUnit, validate_campaign
from engine.domain_persistence import export, pack, restore, CONTINUITY_DEFAULTS
from engine.game_session import GameSession
from engine.information_adjudication import Unresolved
from engine.physical_world import ClimbCircumstances
from engine.save_system import save_game, load_game
from engine.traversal_resolution import ClimbRequest, ClimbRuling
from test_domain_acceptance import premises
from test_consequential_climbing import campaign, Dice


ACTIVITY = 'activity:first'


def foundation(*, uncertain=False, protected=False, **kwargs):
    root = campaign(protected=protected, **kwargs) if uncertain else premises(**kwargs)
    first = root.activities[0]
    next_ruling = (ClimbRuling(True, 'context:next supported progress', 'no_progress', 4)
                   if uncertain else first.ruling)
    first = replace(first, objective='Reach the established final position by climbing',
        continuations=(ActivityStage('next', 19, 'World meaningful upper section', next_ruling),))
    if uncertain:
        w = root.origin.world
        x = ClimbCircumstances('risk:next:original', 'next', 'load_bearing', None,
                               None, None, 'none', 'none', 'hidden:upper footing')
        d = replace(root.origin, world=replace(w, climb_circumstances=w.climb_circumstances + (x,)))
        root = replace(root, origin=d, current=d)
    return replace(root, activities=(first,), schema=3)


def run(identity='run:one', *, means=(), climb=False):
    return ActivityRun(identity, ACTIVITY, means, climb)


def step(root, identity='manual:first'):
    scope = effective_scope(root, ACTIVITY)
    link = next(l for l in root.current.world.links if l.id == scope.target)
    return Increment(ACTIVITY, ClimbRequest(identity, scope.actor, scope.target, link.distance_feet))


def cp(*developments, **kwargs):
    return ActivityCheckpoint(ACTIVITY, 'climb', developments=developments, **kwargs)


def change(runtime, event):
    runtime.accept_increment(runtime.prepare_activity_change(event))


def boundary(root, scope):
    if len(successful_units(root, ACTIVITY)) == 1 and not any(
            type(u) is ActivityUpdate and u.id == 'development:boundary' for u in root.accepted):
        return ActivityUpdate('development:boundary', ACTIVITY, 'World recognizable changed situation',
            checkpoint=cp(ActivityDevelopment('player_choice', choice_key='risk:recognized')),
            notices=(('risk:recognized', 'The upper passage now exposes you to a new recognizable risk.'),),
            choice_contexts=(ChoiceContext('risk:recognized', 'development:boundary', (1,)),))


class ContinuityTests(unittest.TestCase):
    def runtime(self, root=None, dice=None):
        return GameSession.start_domains(root or foundation(), draw=dice or Dice())

    def interrupted(self, **kwargs):
        runtime = self.runtime(**kwargs)
        result = runtime.advance_activity(run(), refresh=boundary)
        self.assertEqual(result.status, 'control', result)
        self.assertEqual(len(result.receipts), 1)
        return runtime

    def answer(self, runtime, choices=('risk:recognized',), identity='response:one'):
        change(runtime, ActivityResponse(identity, ACTIVITY, choices, runtime.campaign.revision))

    def assert_rejects(self, runtime, event):
        before = runtime.campaign
        with self.assertRaises((ValueError, Unresolved)):
            runtime.accept_increment(runtime.prepare_activity_change(event))
        self.assertIs(runtime.campaign, before)

    def test_ordinary_uninterrupted_climbing_keeps_one_objective(self):
        runtime = self.runtime()
        outcome = runtime.advance_activity(run())
        self.assertEqual(outcome.status, 'complete', outcome)
        self.assertEqual(len(outcome.receipts), 2)
        self.assertEqual(len(runtime.campaign.activities), 1)
        self.assertEqual(runtime.state.world.at_seconds, 47)
        self.assertEqual(runtime.state.characters[0].movement_spent, 20)
        self.assertEqual(dict(runtime.state.world.positions)[runtime.campaign.actor], 'end')
        self.assertTrue(effective_scope(runtime.campaign, ACTIVITY).checkpoint.complete)
        validate_campaign(runtime.campaign)

    def test_progress_then_interruption_preserves_real_position_time_and_cost(self):
        runtime = self.interrupted()
        self.assertEqual(dict(runtime.state.world.positions)['creature'], 'middle')
        self.assertEqual(runtime.state.world.at_seconds, 28)
        self.assertEqual(runtime.state.characters[0].movement_spent, 10)
        self.assertEqual(runtime.campaign.revision, 2)
        self.assertEqual(runtime.advance_activity(run()).status, 'control')

    def test_resume_reuses_accepted_check_and_costs(self):
        dice = Dice(20, 20)
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=dice)
        before = runtime.campaign.accepted[0]
        self.assertEqual(dice.sides, [20])
        self.answer(runtime)
        result = runtime.advance_activity(run())
        self.assertEqual(result.status, 'complete', result)
        self.assertEqual(dice.sides, [20, 20])
        self.assertIs(runtime.campaign.accepted[0], before)
        self.assertEqual(runtime.state.characters[0].movement_spent, 30)
        self.assertEqual(runtime.state.world.at_seconds, 47)
        final = runtime.campaign
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')
        self.assertIs(runtime.campaign, final)
        self.assertEqual(dice.sides, [20, 20])

    def test_changed_surface_and_capability_still_permit_continuation(self):
        runtime = self.interrupted()
        original = runtime.campaign.activities[0]
        w, c = runtime.state.world, runtime.state.characters[0]
        change(runtime, ActivityUpdate('world:rain', ACTIVITY, 'World wet difficult surface',
            surfaces=(replace(w.surfaces[0], slippery=True, difficult=True),),
            characters=(replace(c, speed=90, strength=18),), elapsed_seconds=7))
        self.answer(runtime)
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')
        self.assertEqual(runtime.state.characters[0].movement_spent, 25)
        self.assertEqual(runtime.state.world.at_seconds, 54)
        self.assertEqual(runtime.campaign.activities[0], original)

    def test_physical_route_block_returns_control_without_failed_attempt(self):
        runtime = self.runtime()
        def blocked(root, scope):
            if len(successful_units(root, ACTIVITY)) == 1:
                return ActivityUpdate('world:blocked', ACTIVITY, 'World fallen obstruction',
                    links=(replace(root.current.world.links[1], blocked=True),))
        result = runtime.advance_activity(run(), refresh=blocked)
        self.assertEqual(result.status, 'control', result)
        self.assertEqual(len(successful_units(runtime.campaign, ACTIVITY)), 1)
        self.assertEqual(runtime.state.characters[0].movement_spent, 10)
        self.assertEqual(runtime.state.world.at_seconds, 28)

    def test_missing_means_rechecked_on_resumption(self):
        runtime = self.runtime()
        r = run(means=('rope',))
        self.assertEqual(runtime.advance_activity(r, refresh=boundary).status, 'control')
        w = runtime.state.world
        change(runtime, ActivityUpdate('world:rope-damaged', ACTIVITY, 'World material damage',
            objects=(replace(w.objects[0], intact=False),)))
        self.answer(runtime)
        before = runtime.campaign
        self.assertEqual(runtime.advance_activity(r).status, 'control')
        self.assertIs(runtime.campaign, before)

    def test_character_incapacity_rechecked_without_inventing_fall(self):
        runtime = self.interrupted()
        c = runtime.state.characters[0]
        change(runtime, ActivityUpdate('character:stunned', ACTIVITY, 'Character established condition',
            characters=(replace(c, conditions=('stunned',)),)))
        self.answer(runtime)
        before = runtime.campaign
        self.assertEqual(runtime.advance_activity(run()).status, 'control')
        self.assertIs(runtime.campaign, before)
        self.assertFalse(runtime.state.world.falls)

    def test_constraints_apply_initially_and_on_resumption(self):
        base = foundation()
        a = base.activities[0]
        a = replace(a, supported_constraints=('quietly',),
                    authorization=replace(a.authorization, constraints=('quietly',)))
        for initial in (True, False):
            with self.subTest(initial=initial):
                scope = replace(a, checkpoint=cp(conflicting_constraints=('quietly',))) if initial else a
                runtime = self.runtime(replace(base, activities=(scope,)))
                if not initial:
                    self.assertEqual(runtime.process_increment(step(runtime.campaign)).status, 'accepted')
                    change(runtime, ActivityUpdate('world:noise', ACTIVITY, 'World unavoidable noisy movement',
                        checkpoint=cp(conflicting_constraints=('quietly',))))
                before = runtime.campaign
                result = runtime.advance_activity(run())
                self.assertEqual(result.status, 'control', result)
                self.assertIs(runtime.campaign, before)
                self.assertEqual(effective_scope(runtime.campaign, ACTIVITY).authorization.constraints, ('quietly',))

    def test_unsupported_constraints_never_assumed(self):
        base = foundation(); a = base.activities[0]
        runtime = self.runtime(replace(base, activities=(replace(a,
            authorization=replace(a.authorization, constraints=('fly invisibly',))),)))
        self.assertEqual(runtime.advance_activity(run()).status, 'unresolved')
        self.assertFalse(runtime.campaign.accepted)

    def test_perception_and_opportunity_control_new_risk(self):
        for perceived, opportunity, objectionable, expected in (
            (True, True, True, 'control'), (False, True, True, 'complete'),
            (True, False, True, 'complete'), (True, True, False, 'complete')):
            base=foundation(); a=base.activities[0]
            d=ActivityDevelopment('increased_discovery_risk', perceived, opportunity, objectionable,
                                  'hidden:observer-risk')
            runtime=self.runtime(replace(base, activities=(replace(a, checkpoint=cp(d), notices=(
                (d.choice_key, 'Nearby movement makes your activity more likely to be noticed.'),
            ) if perceived and opportunity and objectionable else (),
                choice_contexts=(ChoiceContext(d.choice_key, ACTIVITY, (0, 1)),)),)))
            outcome=runtime.advance_activity(run())
            self.assertEqual(outcome.status, expected, outcome)
            self.assertNotIn('hidden', outcome.message)
            self.assertNotIn('observer', outcome.message)

    def test_ordinary_development_is_not_an_interruption(self):
        base=foundation(); a=base.activities[0]
        runtime=self.runtime(replace(base, activities=(replace(a, checkpoint=cp(
            ActivityDevelopment('ordinary', choice_key='ordinary:wind'))),)))
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')

    def test_hidden_binding_unavailable_has_no_information_leak(self):
        runtime=self.interrupted()
        w=runtime.state.world
        change(runtime, ActivityUpdate('world:hidden', ACTIVITY, 'hidden:supplier premise',
            surfaces=(replace(w.surfaces[0], unresolved_bindings=('hidden:inaccessible ward',)),)))
        self.answer(runtime)
        before=runtime.campaign
        outcome=runtime.advance_activity(run())
        self.assertEqual(outcome.status, 'unresolved')
        self.assertNotIn('ward', outcome.message)
        self.assertNotIn('hidden', outcome.message)
        self.assertIs(runtime.campaign, before)

    def test_new_exposure_requires_exact_recognizable_risk_answer(self):
        for perceived in (True, False):
            with self.subTest(perceived=perceived):
                dice=Dice(20, 1, 3)
                runtime=self.runtime(foundation(uncertain=True), dice)
                def expose(root, scope):
                    if len(successful_units(root, ACTIVITY)) == 1 and not any(
                            type(u) is ActivityUpdate for u in root.accepted):
                        x=ClimbCircumstances('risk:new-exposure', 'next', 'grip_dependent', 'base', 10,
                            'solid', 'none', 'none', 'hidden:support changed')
                        return ActivityUpdate('world:exposure', ACTIVITY, 'World support changes',
                            circumstances=(x,), ruling=ClimbRuling(True, 'context:grip under exposure', 'loss_of_grip', 4),
                            checkpoint=cp(ActivityDevelopment('player_choice', perceived=perceived,
                                choice_key=x.id)), notices=((x.id, 'The upper climb now exposes you to a fall.'),)
                                if perceived else (),
                            choice_contexts=(ChoiceContext(x.id, 'world:exposure', (1,)),))
                result=runtime.advance_activity(run(), refresh=expose)
                if perceived:
                    self.assertEqual(result.status, 'control', result)
                    self.assertEqual(dice.sides, [20])
                    self.answer(runtime, ('risk:new-exposure',))
                    result=runtime.advance_activity(run())
                self.assertEqual(result.status, 'failed', result)
                self.assertEqual(dice.sides, [20,20,6])
                self.assertEqual(runtime.state.characters[0].hit_points, 22)
                self.assertEqual(dict(runtime.state.world.positions)['creature'], 'base')
                self.assertNotIn('support changed', result.message)
                self.assertNotIn('hidden', result.message)

    def test_failed_progress_protected_grip_and_fall_remain_distinct(self):
        from test_consequential_climbing import change as change_origin
        for footing, protected, kind, values in (
            ('load_bearing', False, 'supported_no_progress', (1,)),
            ('grip_dependent', True, 'grip_lost_protected', (1,)),
            ('grip_dependent', False, 'fell', (1,2,3))):
            base=foundation(uncertain=True, protected=protected)
            if footing=='load_bearing':
                w=base.origin.world
                x=replace(w.climb_circumstances[0], footing=footing, drop_feet=0)
                a=replace(base.activities[0], ruling=ClimbRuling(True,'context:stable progress','no_progress',4))
                base=change_origin(base,world=replace(w,climb_circumstances=(x,)+w.climb_circumstances[1:]),scope=a)
            dice=Dice(*values); runtime=self.runtime(base,dice)
            outcome=runtime.advance_activity(run())
            self.assertEqual(outcome.status,'failed',outcome)
            self.assertEqual(runtime.campaign.accepted[0].consequence.kind,kind)
            before=runtime.campaign
            self.assertEqual(runtime.advance_activity(run()).status,'failed')
            self.assertIs(runtime.campaign,before)

    def test_new_attempt_after_supported_failure_is_legitimate(self):
        base=foundation(uncertain=True,protected=True)
        dice=Dice(1,20,20); runtime=self.runtime(base,dice)
        self.assertEqual(runtime.advance_activity(run()).status,'failed')
        self.assertEqual(runtime.advance_activity(run('run:new-attempt')).status,'complete')
        self.assertEqual(dice.sides,[20,20,20])
        self.assertEqual(runtime.state.characters[0].movement_spent,45)
        self.assertEqual(runtime.state.world.at_seconds,58)
        self.assertEqual(len(successful_units(runtime.campaign,ACTIVITY)),2)

    def test_new_identity_does_not_retry_after_actual_fall_and_prone(self):
        dice=Dice(1,2,3); runtime=self.runtime(foundation(uncertain=True),dice)
        self.assertEqual(runtime.advance_activity(run()).status,'failed')
        before=runtime.campaign
        self.assertEqual(runtime.advance_activity(run('fresh')).status,'control')
        self.assertIs(runtime.campaign,before)
        self.assertEqual(dice.sides,[20,6,6])

    def test_stale_and_malformed_updates_publish_nothing(self):
        runtime=self.runtime()
        proposal=runtime.prepare_activity_change(ActivityUpdate('world:rain',ACTIVITY,'World rain'))
        runtime.process_increment(step(runtime.campaign))
        before=runtime.campaign
        with self.assertRaises(Unresolved): runtime.accept_increment(proposal)
        self.assertIs(runtime.campaign,before)
        for event in (ActivityUpdate('bad',ACTIVITY,'',elapsed_seconds=1),
                      ActivityUpdate('bad',ACTIVITY,'World',elapsed_seconds=True),
                      ActivityUpdate('bad',ACTIVITY,'World',characters=(replace(
                          runtime.state.characters[0],movement_spent=0),)),
                      ActivityUpdate('bad',ACTIVITY,'World',checkpoint=cp(complete=True)),
                      ActivityUpdate('bad',ACTIVITY,'World',checkpoint=cp(resolution_ref='dangling'))):
            self.assert_rejects(runtime,event)

    def test_answers_cannot_waive_restrictions_or_missing_means(self):
        runtime=self.interrupted()
        change(runtime,ActivityUpdate('world:missing',ACTIVITY,'World missing means',
            checkpoint=cp(ActivityDevelopment('player_choice',choice_key='risk:recognized'),missing_means=('needed',)),
            notices=effective_scope(runtime.campaign,ACTIVITY).notices,
            choice_contexts=effective_scope(runtime.campaign,ACTIVITY).choice_contexts))
        self.answer(runtime)
        before=runtime.campaign
        self.assertEqual(runtime.advance_activity(run()).status,'control')
        self.assertIs(runtime.campaign,before)

    def test_hidden_unknown_and_stale_answers_reject(self):
        runtime=self.interrupted()
        for choices in (('hidden:unknown',),('risk:recognized','hidden:unknown')):
            self.assert_rejects(runtime,ActivityResponse('response:bad',ACTIVITY,choices,runtime.campaign.revision))
        stale=ActivityResponse('response:stale',ACTIVITY,('risk:recognized',),runtime.campaign.revision-1)
        self.assert_rejects(runtime,stale)
        change(runtime,ActivityUpdate('world:hidden-choice',ACTIVITY,'World hidden development',
            checkpoint=cp(ActivityDevelopment('player_choice',perceived=False,choice_key='hidden:choice')),
            choice_contexts=(ChoiceContext('hidden:choice', 'world:hidden-choice', (1,)),)))
        self.assert_rejects(runtime,ActivityResponse('response:hidden',ACTIVITY,('hidden:choice',),runtime.campaign.revision))

    def test_replaced_checkpoint_does_not_reuse_stale_answer(self):
        runtime=self.interrupted(); self.answer(runtime)
        change(runtime,ActivityUpdate('world:second-risk',ACTIVITY,'World new risk',checkpoint=cp(
            ActivityDevelopment('player_choice',choice_key='risk:second')),
            notices=(('risk:second','The next section introduces a different recognizable risk.'),),
            choice_contexts=(ChoiceContext('risk:second', 'world:second-risk', (1,)),)))
        self.assertEqual(runtime.advance_activity(run()).status,'control')
        self.assertNotIn('risk:recognized',effective_scope(runtime.campaign,ACTIVITY).authorization.answered_choices)

    def test_repeated_update_is_idempotent_but_changed_identity_rejects(self):
        runtime=self.runtime(); event=ActivityUpdate('world:one',ACTIVITY,'World time',elapsed_seconds=5)
        proposal=runtime.prepare_activity_change(event); runtime.accept_increment(proposal)
        before=runtime.campaign; runtime.accept_increment(proposal)
        self.assertIs(runtime.campaign,before)
        self.assert_rejects(runtime,replace(event,elapsed_seconds=6))
        self.assertEqual(runtime.process_increment(step(runtime.campaign,'world:one')).status,'unresolved')

    def test_run_identity_preserves_means_method_and_activity(self):
        runtime=self.interrupted()
        self.assertEqual(runtime.advance_activity(run(means=('rope',))).status,'unresolved')
        self.assertEqual(runtime.advance_activity(run(climb=True)).status,'unresolved')
        before=runtime.campaign
        self.assertEqual(runtime.advance_activity(replace(run(),activity='wrong')).status,'unresolved')
        self.assertIs(runtime.campaign,before)

    def test_checkpoint_resolution_refs_never_bypass_integrity(self):
        runtime=self.interrupted()
        for ref in ('dangling','run:one:stage:0','some-other-activity:result'):
            self.assert_rejects(runtime,ActivityUpdate('bad:'+ref,ACTIVITY,'World change',
                checkpoint=cp(resolution_ref=ref)))
            base=foundation(); a=base.activities[0]
            with self.assertRaises(ValueError):
                self.runtime(replace(base,activities=(replace(a,checkpoint=cp(resolution_ref=ref)),)))

    def test_structurally_varied_world_character_premises_drive_costs(self):
        for distance,difficult,climb,cost in ((3,False,False,12),(7,True,False,42),
                                             (6,False,True,12),(8,True,True,32)):
            base=foundation(distance=distance,difficult=difficult,climb_speed=90,
                            speed=120,actor='other',locality='different')
            runtime=self.runtime(base)
            self.assertEqual(runtime.advance_activity(run(climb=climb)).status,'complete')
            self.assertEqual(runtime.state.characters[0].movement_spent,cost)

    def test_supplier_cannot_return_predetermined_gameplay_answer(self):
        runtime=self.runtime(); before=runtime.campaign
        self.assertEqual(runtime.advance_activity(run(),refresh=lambda *_: True).status,'unresolved')
        self.assertIs(runtime.campaign,before)

    def test_accepted_history_and_proposals_cannot_forge_stage_association(self):
        runtime=self.runtime()
        proposal=runtime.prepare_increment(step(runtime.campaign))
        for unit in (replace(proposal.unit,duration_seconds=900),
                     replace(proposal.unit,command=replace(proposal.unit.command,activity='other')),
                     replace(proposal.unit,result=replace(proposal.unit.result,rolls=(20,)))):
            before=runtime.campaign
            with self.assertRaises((ValueError,Unresolved)):
                runtime.accept_increment(replace(proposal,unit=unit))
            self.assertIs(runtime.campaign,before)

    def test_control_projection_preserves_progress_and_only_accessible_notice(self):
        runtime=self.interrupted()
        result=runtime.advance_activity(run())
        self.assertIn('5 feet to the next established position', result.message)
        self.assertIn('upper passage', result.message)
        self.assertNotIn('hidden', result.message)
        self.assert_rejects(runtime, ActivityUpdate('bad:notice',ACTIVITY,'World',
            checkpoint=cp(ActivityDevelopment('player_choice',perceived=False,choice_key='hidden:risk')),
            notices=(('hidden:risk','hidden:omniscient cause'),)))

    def test_changed_risk_identity_and_route_meaning_are_checked(self):
        runtime=self.runtime(foundation(uncertain=True,protected=True))
        x=runtime.state.world.climb_circumstances[0]
        self.assert_rejects(runtime,ActivityUpdate('bad:risk',ACTIVITY,'World',
            circumstances=(replace(x,drop_feet=30),)))
        fresh=replace(x,id='risk:revised',drop_feet=30)
        change(runtime,ActivityUpdate('world:revised-risk',ACTIVITY,'World revised exposure',circumstances=(fresh,)))
        self.assert_rejects(runtime,ActivityUpdate('bad:historical-risk',ACTIVITY,'World',
            circumstances=(replace(x,drop_feet=40),)))
        link=runtime.state.world.links[0]
        self.assert_rejects(runtime,ActivityUpdate('bad:route',ACTIVITY,'World',
            links=(replace(link,destination='end'),)))

    def test_presentation_failure_after_acceptance_does_not_repeat_mechanics(self):
        dice=Dice(20,20); runtime=self.runtime(foundation(uncertain=True,protected=True),dice)
        command=step(runtime.campaign)
        receipt=runtime.accept_increment(runtime.prepare_increment(command))
        root=runtime.campaign
        # A failed expression layer cannot erase acceptance or trigger new dice.
        with patch('engine.historical_campaign.owners',side_effect=AssertionError('no owner reread on retry')):
            result=runtime.process_increment(command)
        self.assertEqual(result.results,(receipt,))
        self.assertIs(runtime.campaign,root)
        self.assertEqual(dice.sides,[20])

    def test_later_supplier_failure_retains_accepted_progress_in_safe_handoff(self):
        dice=Dice(20); runtime=self.runtime(foundation(uncertain=True,protected=True),dice)
        def supplier(root,scope):
            if successful_units(root,ACTIVITY):
                raise ValueError('hidden:unavailable supplier fact')
        result=runtime.advance_activity(run(),refresh=supplier)
        self.assertEqual(result.status,'unresolved')
        self.assertEqual(len(result.receipts),1)
        self.assertIn('5 feet',result.message)
        self.assertNotIn('hidden',result.message)
        self.assertEqual(dict(runtime.state.world.positions)['creature'],'middle')
        self.assertEqual(runtime.state.characters[0].movement_spent,15)
        self.assertEqual(dice.sides,[20])


class F05IntegrityTests(unittest.TestCase):
    runtime = ContinuityTests.runtime
    interrupted = ContinuityTests.interrupted
    answer = ContinuityTests.answer
    assert_rejects = ContinuityTests.assert_rejects

    def test_original_answer_cannot_authorize_a_different_later_decision(self):
        dice = Dice(20)
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=dice)
        before = runtime.campaign
        key = before.origin.world.climb_circumstances[0].id
        event = ActivityUpdate('bad:repurposed-original', ACTIVITY, 'World new observation risk',
            checkpoint=cp(ActivityDevelopment('player_choice', choice_key=key)),
            notices=((key, 'The upper route now exposes you to observers.'),),
            choice_contexts=(ChoiceContext(key, 'bad:repurposed-original', (1,)),))
        self.assert_rejects(runtime, event)
        # Even a forged proposal bypassing preparation must fail before publication.
        from engine.historical_campaign import Proposal
        with self.assertRaises(ValueError):
            runtime.accept_increment(Proposal(before, event))
        outcome = runtime.advance_activity(run(), refresh=lambda *_: event)
        self.assertEqual(outcome.status, 'unresolved')
        self.assertEqual(len(outcome.receipts), 1)
        self.assertNotIn('observers', outcome.message)
        self.assertIs(runtime.campaign, before)
        self.assertEqual(dice.sides, [20])
        self.assertEqual(runtime.state.characters[0].movement_spent, 15)
        self.assertEqual(runtime.state.world.at_seconds, 28)

    def test_answered_choice_cannot_change_notice_or_classification(self):
        runtime = self.interrupted()
        self.answer(runtime)
        scope = effective_scope(runtime.campaign, ACTIVITY)
        development = scope.checkpoint.developments[0]
        for checkpoint, notices in (
                (scope.checkpoint, (('risk:recognized', 'A different dangerous commitment is required.'),)),
                (cp(replace(development, kind='increased_discovery_risk', potentially_objectionable=True)), scope.notices),
                (cp(replace(development, potentially_objectionable=True)), scope.notices)):
            self.assert_rejects(runtime, ActivityUpdate('bad:changed-meaning', ACTIVITY,
                'World different decision', checkpoint=checkpoint, notices=notices,
                choice_contexts=scope.choice_contexts))

    def test_same_answered_choice_survives_checkpoint_replacement_and_restore(self):
        dice = Dice(20, 20)
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=dice)
        first = runtime.campaign.accepted[0]
        self.answer(runtime)
        scope = effective_scope(runtime.campaign, ACTIVITY)
        checkpoint = replace(scope.checkpoint, developments=scope.checkpoint.developments + (
            ActivityDevelopment('ordinary', choice_key='ordinary:breeze'),))
        change(runtime, ActivityUpdate('world:same-decision', ACTIVITY, 'World same established decision',
            checkpoint=checkpoint, notices=scope.notices, choice_contexts=scope.choice_contexts))
        self.assertIn('risk:recognized', effective_scope(runtime.campaign, ACTIVITY).authorization.answered_choices)
        with patch('engine.traversal_resolution.TraversalResolution.resolve', side_effect=AssertionError('no sampling')):
            restored = restore(export(runtime.campaign))
        runtime.restore_domains(restored)
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')
        self.assertEqual(runtime.campaign.accepted[0], first)
        self.assertEqual(dice.sides, [20, 20])
        self.assertEqual(runtime.state.characters[0].movement_spent, 30)
        final = runtime.campaign
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')
        self.assertIs(runtime.campaign, final)
        self.assertEqual(dice.sides, [20, 20])

    def test_original_fully_established_choice_keeps_its_authorization(self):
        base = foundation(uncertain=True, protected=True)
        key = base.origin.world.climb_circumstances[0].id
        checkpoint = cp(ActivityDevelopment('player_choice', choice_key=key))
        notices = ((key, 'The chosen climb has the established protected grip-loss risk.'),)
        contexts = (ChoiceContext(key, ACTIVITY, (0,)),)
        a = replace(base.activities[0], checkpoint=checkpoint, notices=notices, choice_contexts=contexts)
        dice = Dice(20, 20)
        runtime = self.runtime(replace(base, activities=(a,)), dice)
        change(runtime, ActivityUpdate('world:same-original', ACTIVITY, 'World unchanged original risk',
            checkpoint=checkpoint, notices=notices, choice_contexts=contexts))
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')
        self.assertEqual(dice.sides, [20, 20])

    def test_new_risk_needs_its_own_fresh_response(self):
        dice = Dice(20, 20)
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=dice)
        self.answer(runtime)
        change(runtime, ActivityUpdate('world:fresh-risk', ACTIVITY, 'World new recognizable risk',
            checkpoint=cp(ActivityDevelopment('player_choice', choice_key='risk:fresh')),
            notices=(('risk:fresh', 'The upper opening now exposes your activity to passersby.'),),
            choice_contexts=(ChoiceContext('risk:fresh', 'world:fresh-risk', (1,)),)))
        before = runtime.campaign
        result = runtime.advance_activity(run())
        self.assertEqual(result.status, 'control')
        self.assertIn('passersby', result.message)
        self.assert_rejects(runtime, ActivityResponse('bad:old-answer', ACTIVITY,
            ('risk:recognized',), before.revision))
        self.assertIs(runtime.campaign, before)
        self.assertEqual(dice.sides, [20])
        self.answer(runtime, ('risk:fresh',), 'response:fresh')
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')
        self.assertEqual(dice.sides, [20, 20])

    def test_choice_identity_cannot_be_rebound_after_temporary_absence(self):
        runtime = self.interrupted()
        self.answer(runtime)
        scope = effective_scope(runtime.campaign, ACTIVITY)
        change(runtime, ActivityUpdate('world:quiet-interval', ACTIVITY, 'World intervening circumstances', checkpoint=cp()))
        self.assert_rejects(runtime, ActivityUpdate('bad:reintroduced', ACTIVITY, 'World changed choice',
            checkpoint=scope.checkpoint, notices=(('risk:recognized', 'A different choice now applies.'),),
            choice_contexts=scope.choice_contexts))
        change(runtime, ActivityUpdate('world:original-again', ACTIVITY, 'World same retained decision',
            checkpoint=scope.checkpoint, notices=scope.notices, choice_contexts=scope.choice_contexts))
        self.assertIn('risk:recognized', effective_scope(runtime.campaign, ACTIVITY).authorization.answered_choices)
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')

    def test_recognizable_choices_require_complete_accessible_notices(self):
        runtime = self.interrupted()
        for kind in ('player_choice', 'increased_discovery_risk'):
            checkpoint = cp(ActivityDevelopment(kind, potentially_objectionable=True, choice_key='risk:incomplete'))
            for notices in ((), (('risk:incomplete', ''),), (('wrong:key', 'A new decision is required.'),)):
                with self.subTest(kind=kind, notices=notices):
                    event = ActivityUpdate('bad:incomplete', ACTIVITY, 'World changed risk',
                        checkpoint=checkpoint, notices=notices)
                    self.assert_rejects(runtime, event)
                    base = foundation()
                    a = replace(base.activities[0], checkpoint=checkpoint, notices=notices)
                    with self.assertRaises(ValueError):
                        self.runtime(replace(base, activities=(a,)))

    def test_recognizable_choices_require_answerable_unique_identities(self):
        runtime = self.interrupted()
        for key in (None, '', ' '):
            self.assert_rejects(runtime, ActivityUpdate('bad:no-key', ACTIVITY, 'World visible decision',
                checkpoint=cp(ActivityDevelopment('player_choice', choice_key=key))))
            base = foundation()
            a = replace(base.activities[0], checkpoint=cp(ActivityDevelopment('player_choice', choice_key=key)))
            with self.assertRaises(ValueError):
                self.runtime(replace(base, activities=(a,)))
        first = ActivityDevelopment('player_choice', choice_key='risk:duplicate')
        second = ActivityDevelopment('increased_discovery_risk', potentially_objectionable=True,
                                     choice_key='risk:duplicate')
        self.assert_rejects(runtime, ActivityUpdate('bad:duplicate', ACTIVITY, 'World conflicting choices',
            checkpoint=cp(first, second), notices=(('risk:duplicate', 'Two different decisions cannot share one answer.'),)))

    def test_hidden_or_unanswerable_developments_do_not_offer_or_leak_choices(self):
        for perceived, opportunity in ((False, True), (True, False)):
            runtime = self.runtime()
            checkpoint = cp(ActivityDevelopment('player_choice', perceived=perceived,
                opportunity_to_respond=opportunity, choice_key='hidden:decision'))
            change(runtime, ActivityUpdate('world:hidden', ACTIVITY, 'hidden:source', checkpoint=checkpoint,
                choice_contexts=(ChoiceContext('hidden:decision', 'world:hidden', (0, 1)),)))
            self.assert_rejects(runtime, ActivityResponse('bad:hidden-answer', ACTIVITY,
                ('hidden:decision',), runtime.campaign.revision))
            self.assert_rejects(runtime, ActivityUpdate('bad:hidden-notice', ACTIVITY, 'World access',
                checkpoint=checkpoint, notices=(('hidden:decision', 'hidden:unearned knowledge'),)))
            outcome = runtime.advance_activity(run())
            self.assertEqual(outcome.status, 'complete')
            self.assertNotIn('hidden', outcome.message)
            self.assertNotIn('unearned', outcome.message)

    def test_newly_perceived_choice_requires_a_notice_and_response(self):
        runtime = self.interrupted()
        hidden = cp(ActivityDevelopment('player_choice', perceived=False, choice_key='risk:latent'))
        contexts = (ChoiceContext('risk:latent', 'world:latent', (1,)),)
        change(runtime, ActivityUpdate('world:latent', ACTIVITY, 'World hidden development', checkpoint=hidden,
            choice_contexts=contexts))
        visible = replace(hidden, developments=(replace(hidden.developments[0], perceived=True),))
        self.assert_rejects(runtime, ActivityUpdate('bad:unexplained-visible', ACTIVITY,
            'World newly perceived development', checkpoint=visible))
        change(runtime, ActivityUpdate('world:revealed', ACTIVITY, 'World newly perceived development',
            checkpoint=visible, notices=(('risk:latent', 'The next passage exposes you to a newly noticed danger.'),),
            choice_contexts=contexts))
        self.assertEqual(runtime.advance_activity(run()).status, 'control')
        self.answer(runtime, ('risk:latent',), 'response:latent')
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')

    def test_responses_bind_current_revision_and_their_own_activity_notice(self):
        base = foundation()
        other = replace(base.activities[0], id='activity:other',
            authorization=replace(base.activities[0].authorization, purpose='activity:other'),
            checkpoint=ActivityCheckpoint('activity:other', 'climb', developments=(
                ActivityDevelopment('player_choice', choice_key='risk:other'),)),
            notices=(('risk:other', 'A different activity requires its own decision.'),),
            choice_contexts=(ChoiceContext('risk:other', 'activity:other', (0,)),))
        runtime = self.interrupted(root=replace(base, activities=base.activities + (other,)))
        for activity, choices, revision in (
                (ACTIVITY, ('risk:recognized',), runtime.campaign.revision - 1),
                (ACTIVITY, ('risk:other',), runtime.campaign.revision),
                ('activity:other', ('risk:recognized',), runtime.campaign.revision)):
            self.assert_rejects(runtime, ActivityResponse('bad:situated-answer', activity, choices, revision))

    def test_retained_answer_does_not_waive_current_restrictions_or_missing_means(self):
        for restriction in ('missing_means', 'conflicting_constraints'):
            base = foundation(uncertain=True, protected=True)
            a = base.activities[0]
            a = replace(a, supported_constraints=('quietly',),
                        authorization=replace(a.authorization, constraints=('quietly',)))
            dice = Dice(20)
            runtime = self.interrupted(root=replace(base, activities=(a,)), dice=dice)
            self.answer(runtime)
            scope = effective_scope(runtime.campaign, ACTIVITY)
            checkpoint = replace(scope.checkpoint, **{restriction: ('quietly',)})
            change(runtime, ActivityUpdate('world:restriction', ACTIVITY, 'World current prerequisite',
                checkpoint=checkpoint, notices=scope.notices, choice_contexts=scope.choice_contexts))
            self.assertIn('risk:recognized', effective_scope(runtime.campaign, ACTIVITY).authorization.answered_choices)
            before = runtime.campaign
            self.assertEqual(runtime.advance_activity(run()).status, 'control')
            self.assertIs(runtime.campaign, before)
            self.assertEqual(dice.sides, [20])
            self.assertEqual(runtime.state.characters[0].movement_spent, 15)

    def test_incomplete_supplier_update_rejects_before_any_mechanical_resolution(self):
        dice = Dice()
        runtime = self.runtime(foundation(uncertain=True, protected=True), dice)
        before = runtime.campaign
        event = ActivityUpdate('bad:supplier-choice', ACTIVITY, 'World incomplete decision',
            checkpoint=cp(ActivityDevelopment('player_choice', choice_key='risk:no-notice')))
        outcome = runtime.advance_activity(run(), refresh=lambda *_: event)
        self.assertEqual(outcome.status, 'unresolved')
        self.assertIs(runtime.campaign, before)
        self.assertFalse(outcome.receipts)
        self.assertEqual(dice.sides, [])


class AuthorizationContextTests(unittest.TestCase):
    runtime = ContinuityTests.runtime
    interrupted = ContinuityTests.interrupted
    answer = ContinuityTests.answer

    def reject_without_effect(self, runtime, event):
        from engine.historical_campaign import Proposal
        root = runtime.campaign
        draws, pending = list(runtime.domain_draw.sides), list(runtime.domain_draw.values)
        with patch('engine.traversal_resolution.TraversalResolution.resolve', side_effect=AssertionError('no resolution')):
            for operation in (lambda: runtime.prepare_activity_change(event),
                              lambda: runtime.accept_increment(Proposal(root, event))):
                with self.assertRaises((ValueError, Unresolved)):
                    operation()
                self.assertIs(runtime.campaign, root)
            result = runtime.advance_activity(run('run:invalid-context'), refresh=lambda *_: event)
        self.assertEqual(result.status, 'unresolved')
        self.assertIs(runtime.campaign, root)
        self.assertEqual(runtime.domain_draw.sides, draws)
        self.assertEqual(runtime.domain_draw.values, pending)

    def upper_risk(self, runtime):
        scope = effective_scope(runtime.campaign, ACTIVITY)
        risk = ClimbCircumstances('risk:recognized', 'next', 'grip_dependent', 'base', 10,
            'solid', 'none', 'none', 'hidden:new upper support and exposed fall')
        return ActivityUpdate('world:changed-upper-risk', ACTIVITY, 'World upper support changes',
            circumstances=(risk,), ruling=ClimbRuling(True, 'context:new exposed grip test', 'loss_of_grip', 4),
            checkpoint=scope.checkpoint, notices=scope.notices, choice_contexts=scope.choice_contexts)

    def original_observer_choice(self, *, spanning=False, preauthorized=False):
        base = foundation(uncertain=True, protected=True)
        key = 'choice:observer'
        a = replace(base.activities[0],
            checkpoint=cp(ActivityDevelopment('player_choice', choice_key=key)),
            notices=((key, 'Continuing through this section exposes your activity to observers.'),),
            choice_contexts=(ChoiceContext(key, ACTIVITY, (0, 1) if spanning else (0,)),))
        if preauthorized:
            a = replace(a, authorization=replace(a.authorization, answered_choices=a.authorization.answered_choices + (key,)))
        runtime = self.runtime(replace(base, activities=(a,)), Dice(20, 20))
        answer = ActivityResponse('response:original-observer', ACTIVITY, (key,), runtime.campaign.revision)
        if not preauthorized:
            change(runtime, answer)
        first_command = step(runtime.campaign)
        self.assertEqual(runtime.process_increment(first_command).status, 'accepted')
        return runtime, a, answer, first_command

    def test_review_same_key_and_notice_cannot_authorize_changed_upper_fall_risk(self):
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20, 1, 3))
        self.answer(runtime)
        before = runtime.campaign
        self.reject_without_effect(runtime, self.upper_risk(runtime))
        self.assertEqual(runtime.state.world.at_seconds, 28)
        self.assertEqual(runtime.state.characters[0].movement_spent, 15)
        self.assertEqual(runtime.state.characters[0].hit_points, 25)
        self.assertIs(runtime.campaign.accepted[0], before.accepted[0])

    def test_risk_changes_cannot_bypass_binding_by_omitting_checkpoint(self):
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20))
        self.answer(runtime)
        event = replace(self.upper_risk(runtime), checkpoint=None, notices=(), choice_contexts=())
        self.reject_without_effect(runtime, event)

    def test_changed_failure_stakes_need_fresh_authorization(self):
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20))
        self.answer(runtime)
        scope = effective_scope(runtime.campaign, ACTIVITY)
        self.reject_without_effect(runtime, ActivityUpdate('world:changed-stakes', ACTIVITY,
            'Resolution newly established failure expenditure', ruling=replace(scope.ruling, failure_movement_cost=9)))

    def test_review_same_key_and_notice_cannot_authorize_different_upper_observer(self):
        runtime, original, _, _ = self.original_observer_choice()
        key = original.choice_contexts[0].key
        # Neither copying the lower-stage context, retroactively broadening it,
        # nor claiming a new occurrence permits reuse of the answered identity.
        for context in (original.choice_contexts[0],
                replace(original.choice_contexts[0], stages=(0, 1)),
                ChoiceContext(key, 'world:upper-observer', (1,))):
            with self.subTest(context=context):
                self.reject_without_effect(runtime, ActivityUpdate('world:upper-observer', ACTIVITY,
                    'World a different witness can now observe the upper section',
                    checkpoint=original.checkpoint, notices=original.notices, choice_contexts=(context,)))
        self.assertEqual(runtime.domain_draw.sides, [20])
        self.assertEqual(runtime.state.world.at_seconds, 28)

    def test_new_occurrence_in_same_stage_cannot_reuse_answered_identity(self):
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20))
        self.answer(runtime)
        scope = effective_scope(runtime.campaign, ACTIVITY)
        self.reject_without_effect(runtime, ActivityUpdate('world:different-occurrence', ACTIVITY,
            'World a different consequential observation decision', checkpoint=scope.checkpoint,
            notices=scope.notices, choice_contexts=(replace(scope.choice_contexts[0], source='world:different-occurrence'),)))

    def test_unchanged_multistage_occurrence_keeps_answer_across_progress_and_restore(self):
        runtime, original, answer, command = self.original_observer_choice(spanning=True)
        first = runtime.campaign.accepted[-1]
        checkpoint = replace(original.checkpoint, developments=original.checkpoint.developments + (
            ActivityDevelopment('ordinary', choice_key='ordinary:breeze'),))
        change(runtime, ActivityUpdate('world:ordinary-breeze', ACTIVITY, 'World ordinary breeze',
            checkpoint=checkpoint, notices=original.notices, choice_contexts=original.choice_contexts))
        root = runtime.campaign
        change(runtime, answer)
        self.assertIs(runtime.campaign, root)
        with patch('engine.traversal_resolution.TraversalResolution.resolve', side_effect=AssertionError('no sampling')):
            runtime.restore_domains(restore(export(root)))
        self.assertIn('choice:observer', effective_scope(runtime.campaign, ACTIVITY).authorization.answered_choices)
        self.assertEqual(runtime.advance_activity(run('run:unchanged-observer')).status, 'complete')
        self.assertEqual(runtime.campaign.accepted[1], first)
        self.assertEqual(runtime.domain_draw.sides, [20, 20])
        final = runtime.campaign
        self.assertEqual(runtime.process_increment(command).status, 'accepted')
        self.assertIs(runtime.campaign, final)
        self.assertEqual(runtime.domain_draw.sides, [20, 20])

    def test_unrelated_world_changes_and_elapsed_time_do_not_revoke_answer(self):
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20, 20))
        self.answer(runtime)
        # A new circumstance on the completed lower route is not the upper choice.
        risk = ClimbCircumstances('risk:lower-after-progress', 'first', 'load_bearing',
            None, None, None, 'none', 'none', 'hidden:irrelevant lower footing')
        change(runtime, ActivityUpdate('world:unrelated', ACTIVITY, 'World later lower-route change',
            circumstances=(risk,), elapsed_seconds=5))
        self.assertIn('risk:recognized', effective_scope(runtime.campaign, ACTIVITY).authorization.answered_choices)
        self.assertEqual(runtime.domain_draw.sides, [20])
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')
        self.assertEqual(runtime.domain_draw.sides, [20, 20])
        self.assertEqual(runtime.state.world.at_seconds, 52)

    def test_completed_route_change_does_not_revoke_spanning_occurrence(self):
        runtime, original, _, _ = self.original_observer_choice(spanning=True)
        risk = ClimbCircumstances('risk:lower-now-changed', 'first', 'load_bearing',
            None, None, None, 'none', 'none', 'hidden:change behind accepted progress')
        change(runtime, ActivityUpdate('world:lower-changed', ACTIVITY, 'World change behind progress',
            circumstances=(risk,), checkpoint=original.checkpoint, notices=original.notices,
            choice_contexts=original.choice_contexts))
        self.assertIn('choice:observer', effective_scope(runtime.campaign, ACTIVITY).authorization.answered_choices)
        self.assertEqual(runtime.advance_activity(run('run:spanning')).status, 'complete')
        self.assertEqual(runtime.domain_draw.sides, [20, 20])

    def test_expired_lower_answer_cannot_authorize_new_upper_risk_without_checkpoint(self):
        for preauthorized in (False, True):
            runtime, original, _, _ = self.original_observer_choice(preauthorized=preauthorized)
            key = original.choice_contexts[0].key
            risk = ClimbCircumstances(key, 'next', 'grip_dependent', 'base', 10,
                'solid', 'none', 'none', 'hidden:new upper fall')
            change(runtime, ActivityUpdate('world:upper-without-choice', ACTIVITY, 'World new upper risk',
                circumstances=(risk,), ruling=ClimbRuling(True, 'context:new fall risk', 'loss_of_grip', 4), checkpoint=cp()))
            root = runtime.campaign
            self.assertNotIn(key, effective_scope(root, ACTIVITY).authorization.answered_choices)
            self.assertEqual(runtime.advance_activity(run('run:expired')).status, 'control')
            self.assertIs(runtime.campaign, root)
            self.assertEqual(runtime.domain_draw.sides, [20])

    def test_fresh_upper_risk_with_identical_notice_needs_own_answer_after_restore(self):
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20, 20))
        self.answer(runtime)
        old_answer = runtime.campaign.accepted[-1]
        event = self.upper_risk(runtime)
        key = 'risk:fresh-upper-fall'
        event = replace(event, circumstances=(replace(event.circumstances[0], id=key),),
            checkpoint=cp(ActivityDevelopment('player_choice', choice_key=key)),
            notices=((key, event.notices[0][1]),), choice_contexts=(ChoiceContext(key, event.id, (1,)),))
        change(runtime, event)
        root = runtime.campaign
        change(runtime, old_answer)
        self.assertIs(runtime.campaign, root)
        with patch('engine.traversal_resolution.TraversalResolution.resolve', side_effect=AssertionError('no sampling')):
            runtime.restore_domains(restore(export(root)))
        root = runtime.campaign
        self.assertEqual(runtime.advance_activity(run()).status, 'control')
        self.assertIs(runtime.campaign, root)
        self.assertEqual(runtime.domain_draw.sides, [20])
        self.answer(runtime, (key,), 'response:fresh-upper')
        self.assertEqual(runtime.advance_activity(run()).status, 'complete')
        self.assertEqual(runtime.domain_draw.sides, [20, 20])

    def test_missing_duplicate_unknown_and_mismatched_contexts_reject(self):
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20))
        scope = effective_scope(runtime.campaign, ACTIVITY)
        context = scope.choice_contexts[0]
        for contexts in ((), (context, context), (replace(context, key='unknown'),),
                (replace(context, source='unknown'),), (replace(context, stages=()),),
                (replace(context, stages=('unknown',)),), (replace(context, stages=(1, 1)),),
                (replace(context, stages=(True,)),), (replace(context, stages=(-1,)),)):
            with self.subTest(contexts=contexts):
                self.reject_without_effect(runtime, ActivityUpdate('world:malformed-context', ACTIVITY,
                    'World decision metadata', checkpoint=scope.checkpoint, notices=scope.notices, choice_contexts=contexts))
        base = foundation()
        a = replace(base.activities[0], checkpoint=scope.checkpoint, notices=scope.notices)
        with self.assertRaises(ValueError):
            self.runtime(replace(base, activities=(a,)))

    def revisiting_observer_choice(self, *, spanning=False):
        base = foundation(speed=90)
        a = base.activities[0]
        a = replace(a, continuations=(ActivityStage('return', 5, 'World return section', a.ruling),
            ActivityStage('first', 7, 'World revisit the established lower section', a.ruling),) + a.continuations,
            checkpoint=cp(ActivityDevelopment('player_choice', choice_key='choice:lower-observer')),
            notices=(('choice:lower-observer', 'The lower section exposes your activity to a witness.'),),
            choice_contexts=(ChoiceContext('choice:lower-observer', ACTIVITY, (0, 2) if spanning else (0,)),))
        runtime = self.runtime(replace(base, activities=(a,)))
        self.answer(runtime, ('choice:lower-observer',))
        self.assertEqual(runtime.process_increment(step(runtime.campaign, 'visit:first')).status, 'accepted')
        return runtime, a

    def test_context_cannot_alias_a_later_visit_to_the_same_route(self):
        runtime, original = self.revisiting_observer_choice()
        self.assertEqual(runtime.process_increment(step(runtime.campaign, 'visit:return')).status, 'accepted')
        self.assertEqual(effective_scope(runtime.campaign, ACTIVITY).target, 'first')
        self.reject_without_effect(runtime, ActivityUpdate('world:later-witness', ACTIVITY,
            'World a later observer decision on the same route', checkpoint=original.checkpoint, notices=original.notices,
            choice_contexts=original.choice_contexts))

    def test_future_scoped_risk_change_rejects_during_an_intervening_stage(self):
        runtime, _ = self.revisiting_observer_choice(spanning=True)
        self.assertEqual(effective_scope(runtime.campaign, ACTIVITY).target, 'return')
        risk = ClimbCircumstances('risk:revisited-route', 'first', 'grip_dependent', 'base', 10,
            'solid', 'none', 'none', 'hidden:future scoped route now exposes a fall')
        self.reject_without_effect(runtime, ActivityUpdate('world:future-risk', ACTIVITY,
            'World a materially changed risk ahead', circumstances=(risk,)))

    def test_complete_accessible_notices_remain_required_with_valid_context(self):
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20))
        scope = effective_scope(runtime.campaign, ACTIVITY)
        for notices in ((), (('risk:recognized', ''),), (('unknown', 'An unmatched decision.'),),
                        scope.notices + (('risk:recognized', 'A contradictory duplicate.'),)):
            self.reject_without_effect(runtime, ActivityUpdate('world:incomplete-notice', ACTIVITY,
                'World decision metadata', checkpoint=scope.checkpoint, notices=notices, choice_contexts=scope.choice_contexts))

    def test_hidden_new_risk_retains_internal_context_without_disclosure(self):
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20, 20))
        self.answer(runtime)
        event = self.upper_risk(runtime)
        key = 'hidden:upper-risk'
        event = replace(event, id='hidden:owner-occurrence',
            circumstances=(replace(event.circumstances[0], id=key),),
            checkpoint=cp(ActivityDevelopment('player_choice', perceived=False, choice_key=key)), notices=(),
            choice_contexts=(ChoiceContext(key, 'hidden:owner-occurrence', (1,)),))
        change(runtime, event)
        self.assertEqual(restore(export(runtime.campaign)), runtime.campaign)
        outcome = runtime.advance_activity(run())
        self.assertEqual(outcome.status, 'complete')
        self.assertNotIn('hidden:', outcome.message)
        self.assertNotIn('upper support', outcome.message)
        self.assertEqual(runtime.domain_draw.sides, [20, 20])

    def test_coherent_mismatched_history_rejects_live_restore_decoder_and_file_load(self):
        from engine.historical_activity import apply_update
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=Dice(20))
        self.answer(runtime)
        root = runtime.campaign
        event = self.upper_risk(runtime)
        occurrence = replace(event, circumstances=(), ruling=None,
            choice_contexts=(replace(event.choice_contexts[0], source=event.id),))
        good_path = Path('.artifacts/authorization_context_good.json')
        bad_path = Path('.artifacts/authorization_context_bad.json')
        try:
            save_game(runtime, str(good_path))
            saved = good_path.read_bytes()
            for changed in (event, occurrence):
                # Construct exactly the coherent history the old identity check
                # allowed. Prove rejection is the context invariant, not a stale
                # final snapshot or a malformed record that would fail anyway.
                with patch('engine.historical_activity.validate_choice_history', return_value=None):
                    bad = apply_update(root, changed)
                    self.assertEqual(validate_campaign(bad), bad)
                envelope = {'save_version': 3, 'domain_campaign': pack(bad)}
                bad_path.write_text(json.dumps(envelope), encoding='utf-8')
                bad_bytes = bad_path.read_bytes()
                with patch('engine.traversal_resolution.TraversalResolution.resolve', side_effect=AssertionError('no sampling')):
                    for operation in (lambda: runtime.restore_domains(bad), lambda: restore(envelope),
                                      lambda: load_game(str(bad_path))):
                        with self.assertRaises(ValueError):
                            operation()
                        self.assertIs(runtime.campaign, root)
                        self.assertEqual(runtime.domain_draw.sides, [20])
                self.assertEqual(good_path.read_bytes(), saved)
                self.assertEqual(bad_path.read_bytes(), bad_bytes)
        finally:
            good_path.unlink(missing_ok=True)
            bad_path.unlink(missing_ok=True)

    def test_schema_three_requires_complete_context_records(self):
        runtime = self.interrupted()
        envelope = export(runtime.campaign)
        for record, field in (('ActivityScope', 'choice_contexts'), ('ActivityUpdate', 'choice_contexts'),
                              ('ChoiceContext', 'source'), ('ChoiceContext', 'stages')):
            broken = copy.deepcopy(envelope)
            def remove(value):
                if type(value) is dict:
                    if value.get('record') == record:
                        del value['fields'][field]
                        return True
                    return any(remove(child) for child in value.values())
                if type(value) is list:
                    return any(remove(child) for child in value)
                return False
            self.assertTrue(remove(broken))
            with self.assertRaises(ValueError):
                restore(broken)


class ContinuityPersistenceTests(unittest.TestCase):
    runtime = ContinuityTests.runtime
    interrupted = ContinuityTests.interrupted
    answer = ContinuityTests.answer
    def setUp(self):
        self.path=Path('.artifacts/activity_continuity_test.json')
    def tearDown(self):
        self.path.unlink(missing_ok=True)

    def test_save_load_between_increments_and_after_interruption(self):
        for interrupted in (False,True):
            dice=Dice(20,20); runtime=self.runtime(foundation(uncertain=True,protected=True),dice)
            if interrupted:
                self.assertEqual(runtime.advance_activity(run(),refresh=boundary).status,'control')
            else:
                self.assertEqual(runtime.process_increment(step(runtime.campaign)).status,'accepted')
            save_game(runtime,str(self.path)); saved=runtime.campaign
            with patch('engine.traversal_resolution.TraversalResolution.resolve',side_effect=AssertionError('no reroll')):
                restored=load_game(str(self.path))
                self.assertEqual(restored.campaign,saved)
            restored.domain_draw=dice
            if interrupted:
                self.assertEqual(restored.advance_activity(run()).status,'control')
                self.answer(restored)
            self.assertEqual(restored.advance_activity(run('resumed')).status,'complete')
            self.assertEqual(dice.sides,[20,20])
            self.assertEqual(restored.state.characters[0].movement_spent,30)
            self.assertEqual(restored.state.world.at_seconds,47)

    def test_corrupt_aggregate_rejects_without_live_adoption(self):
        runtime=self.interrupted(); self.answer(runtime)
        root=runtime.campaign
        save_game(runtime,str(self.path)); saved=self.path.read_bytes()
        first=root.accepted[0]; update=root.accepted[1]; response=root.accepted[2]
        corruptions=(replace(root,revision=999),
            replace(root,accepted=(replace(first,result=replace(first.result,total=999)),update,response)),
            replace(root,accepted=(replace(first,command=replace(first.command,activity='missing')),update,response)),
            replace(root,accepted=(first,replace(update,checkpoint=cp(resolution_ref='run:one:stage:0')),response)),
            replace(root,accepted=(first,update,replace(response,choices=('hidden:unknown',)))),
            replace(root,accepted=(first,response,update)),
            replace(root,current=replace(root.current,world=replace(root.current.world,at_seconds=0))))
        for candidate in corruptions:
            with self.subTest(candidate=candidate.revision):
                with self.assertRaises((ValueError,Unresolved)):
                    runtime.restore_domains(candidate)
                with self.assertRaises((ValueError,Unresolved)):
                    restore({'save_version':3,'domain_campaign':pack(candidate)})
                self.assertIs(runtime.campaign,root)
                self.assertEqual(self.path.read_bytes(),saved)

    def test_corrupt_choice_meaning_and_completeness_reject_without_adoption(self):
        dice = Dice(20)
        runtime = self.interrupted(root=foundation(uncertain=True, protected=True), dice=dice)
        self.answer(runtime)
        scope = effective_scope(runtime.campaign, ACTIVITY)
        change(runtime, ActivityUpdate('world:same-choice', ACTIVITY, 'World retained decision',
            checkpoint=scope.checkpoint, notices=scope.notices, choice_contexts=scope.choice_contexts))
        root = runtime.campaign
        save_game(runtime, str(self.path))
        saved = self.path.read_bytes()
        last = root.accepted[-1]
        original_key = root.origin.world.climb_circumstances[0].id
        corruptions = (
            replace(last, notices=()),
            replace(last, notices=(('risk:recognized', 'A different consequential choice.'),)),
            replace(last, checkpoint=cp(ActivityDevelopment('player_choice')), notices=()),
            replace(last, checkpoint=cp(ActivityDevelopment('player_choice', choice_key=original_key)),
                    notices=((original_key, 'An unrelated upper-route decision.'),)),
            replace(last, checkpoint=cp(*scope.checkpoint.developments * 2)),
        )
        corrupt_path = self.path.with_suffix('.corrupt.json')
        try:
            self._reject_choice_corruptions(runtime, root, corruptions, corrupt_path, saved)
        finally:
            corrupt_path.unlink(missing_ok=True)
        self.assertEqual(self.path.read_bytes(), saved)
        self.assertEqual(dice.sides, [20])

    def _reject_choice_corruptions(self, runtime, root, corruptions, corrupt_path, saved):
        with patch('engine.traversal_resolution.TraversalResolution.resolve', side_effect=AssertionError('no sampling')):
            for event in corruptions:
                candidate = replace(root, accepted=root.accepted[:-1] + (event,))
                with self.assertRaises((ValueError, Unresolved)):
                    runtime.restore_domains(candidate)
                envelope = {'save_version': 3, 'domain_campaign': pack(candidate)}
                with self.assertRaises((ValueError, Unresolved)):
                    restore(envelope)
                corrupt_path.write_text(json.dumps(envelope), encoding='utf-8')
                corrupt_bytes = corrupt_path.read_bytes()
                with self.assertRaises((ValueError, Unresolved)):
                    load_game(str(corrupt_path))
                self.assertIs(runtime.campaign, root)
                self.assertEqual(corrupt_path.read_bytes(), corrupt_bytes)
                self.assertEqual(self.path.read_bytes(), saved)

    def test_old_schema_meanings_and_original_record_bytes_remain_supported(self):
        for base in (premises(),campaign(protected=True)):
            runtime=self.runtime(base,Dice(20))
            from test_domain_acceptance import command
            self.assertEqual(runtime.process_increment(command()).status,'accepted')
            envelope=export(runtime.campaign)
            def remove_additions(value):
                if type(value) is not dict:return
                if value.get('record') in CONTINUITY_DEFAULTS:
                    for name in CONTINUITY_DEFAULTS[value['record']]:value['fields'].pop(name)
                for child in value.values():
                    if type(child) is list:
                        for x in child:remove_additions(x)
                    else:remove_additions(child)
            remove_additions(envelope)
            self.assertEqual(restore(envelope),runtime.campaign)

    def test_new_schema_missing_fields_and_old_schema_continuity_reject(self):
        root=foundation(); envelope=export(root)
        del envelope['domain_campaign']['fields']['activities']['tuple'][0]['fields']['objective']
        with self.assertRaises(ValueError):restore(envelope)
        for schema in (1,2):
            with self.assertRaises(ValueError):validate_campaign(replace(root,schema=schema))

    def test_save_failure_preserves_prior_bytes_and_current_root(self):
        runtime=self.interrupted(); save_game(runtime,str(self.path))
        saved=self.path.read_bytes(); before=runtime.campaign
        with patch('engine.save_system.os.replace',side_effect=OSError('offline injected failure')):
            with self.assertRaises(OSError):save_game(runtime,str(self.path))
        self.assertEqual(self.path.read_bytes(),saved)
        self.assertIs(runtime.campaign,before)


if __name__=='__main__':
    with patch.object(socket,'create_connection',side_effect=AssertionError('offline only')):
        unittest.main()
