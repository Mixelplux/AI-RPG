"""Offline architecture/compatibility evidence at the production Runtime boundary.

The independent owner is a contract fixture, not a new gameplay subsystem.
It supplies mechanics and owning-domain validation, never common acceptance.
"""
import ast
import copy
import json
import socket
import unittest
from dataclasses import fields, replace
from pathlib import Path
from unittest.mock import patch

from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment
from engine.character_rules import CreatureRules
from engine.climbing_domain import ClimbPlan, ClimbOptions, ClimbUpdate
from engine.domain_campaign import (Campaign, Domains, ActivityScope, ActivityStage, ActivityRun,
    Increment, AcceptedUnit, ActivityUpdate, ActivityResponse, ChoiceContext, Contribution,
    Proposal, validate_campaign)
from engine.domain_activity import effective_scope, successful_units
from engine.domain_persistence import export, pack, restore
from engine.game_session import GameSession
from engine.gameplay_coordination import AcceptedStep
from engine.information_adjudication import Unresolved
from engine.physical_world import (PhysicalFrame, PhysicalObject, PhysicalRelation, Place,
    CausalRecord, WorldPhysics, natural)
from engine.save_system import save_game, load_game
from test_domain_acceptance import premises, command as historical_command
from test_consequential_climbing import campaign as uncertain_campaign, Dice
from test_activity_continuity import foundation
from engine import historical_campaign, historical_activity


def modern(root):
    """Explicit test construction from baseline premises, never an automatic migration."""
    scopes = []
    for a in root.activities:
        plan = historical_activity.stages(a)
        scopes.append(ActivityScope(a.id, a.actor, 'physical-climbing-v1', a.objective or 'Climb the chosen route',
            a.authorization, a.checkpoint, tuple(ActivityStage(s.route,
                (ClimbPlan(s.duration_seconds, s.time_basis, s.ruling),)) for s in plan),
            a.supported_constraints, a.notices,
            tuple(ChoiceContext(c.key, c.source, c.stages) for c in a.choice_contexts)))
    return Campaign(root.id, root.actor, root.origin, root.origin, tuple(scopes))


def modern_command(old, *, stage=0):
    r = old.request
    return Increment(r.attempt, old.activity, stage,
                     (ClimbOptions(r.means, r.use_climb_speed, r.distance_feet),))


class IndependentOwner:
    """Mechanically distinct repair-contract fixture over actual World/Character.

    Deliberately uses no traversal request, links, speed, movement expenditure,
    climb rulings, dice or falls. Capability less fatigue governs an object's
    repair, with time and fatigue charged coherently even on a failed attempt.
    These formulas are fixture semantics, not approved game rules.
    """
    id = 'fixture:independent-contract'

    def validate_scope(self, campaign, scope):
        if scope.authorization.method != 'fixture-repair':
            raise ValueError('fixture method')
        objects = {o.id for o in campaign.origin.world.objects}
        for s in scope.stages:
            if (s.target not in objects or len(s.payload) != 3
                    or any(not natural(v) for v in s.payload) or not s.payload[0]):
                raise ValueError('fixture plan')

    def validate_command(self, campaign, command, scope):
        if command.payload != ('tool',):
            raise ValueError('fixture means')

    def means(self, command):
        return command.payload

    def assess(self, campaign, command, scope, *, execution):
        self.validate_command(campaign, command, scope)
        c = next(c for c in campaign.current.characters if c.id == scope.actor)
        w = campaign.current.world
        if c.strength is None:
            raise Unresolved('retrieval', 'fixture_material_unavailable')
        if c.exhaustion + scope.payload[2] > 6:
            raise Unresolved('eligibility', 'fixture_resource_limit')
        if ('tool' not in c.ready_equipment or not any(r.object == 'tool' and r.kind == 'held'
                and r.target == c.id for r in w.relationships)):
            raise Unresolved('eligibility', 'fixture_means_unavailable')
        if not next(o for o in w.objects if o.id == 'tool').intact:
            raise Unresolved('eligibility', 'fixture_means_unavailable')
        WorldPhysics(w).require_new_identities((f'{campaign.id}:accepted:{campaign.revision + 1}',))
        return c

    def prepare(self, campaign, command, scope, draw):
        c = self.assess(campaign, command, scope, execution=True)
        obj = next(o for o in campaign.current.world.objects if o.id == scope.target)
        evidence = (obj.intact, c.strength, c.exhaustion, c.strength - c.exhaustion >= scope.payload[1])
        return self.evaluate(campaign, command, scope, evidence)

    def evaluate(self, campaign, command, scope, evidence):
        c = self.assess(campaign, command, scope, execution=True)
        obj = next(o for o in campaign.current.world.objects if o.id == scope.target)
        success = c.strength - c.exhaustion >= scope.payload[1]
        expected = (obj.intact, c.strength, c.exhaustion, success)
        if evidence != expected:
            raise ValueError('fixture evidence mismatch')
        revision = campaign.revision + 1
        seconds, _, fatigue = scope.payload
        w = campaign.current.world
        w = replace(w, revision=f'{campaign.id}:world:{revision}', at_seconds=w.at_seconds + seconds,
            objects=tuple(replace(o, intact=True) if o.id == obj.id and success else o for o in w.objects),
            history=w.history + (CausalRecord(f'{campaign.id}:accepted:{revision}',
                w.at_seconds + seconds, (c.id, obj.id), command.id),))
        current = replace(campaign.current, world=w, character_revision=f'{campaign.id}:character:{revision}',
            characters=tuple(replace(x, exhaustion=x.exhaustion + fatigue) if x.id == c.id else x
                             for x in campaign.current.characters))
        meaning = f'The object is repaired. {seconds} seconds pass; fatigue increases by {fatigue}.' if success else (
            f'The repair does not succeed. {seconds} seconds pass; fatigue increases by {fatigue}.')
        return Contribution(current, expected, success,
            AcceptedStep(command.id, ('repair',), 'complete', (('repair', meaning),)))

    def decision_basis(self, campaign, scope, index):
        c = next(c for c in campaign.current.characters if c.id == scope.actor)
        return (scope.stages[index].payload, c.strength)

    def initial_choices(self, campaign, scope):
        return ()

    def update(self, campaign, event, scope):
        if not event.payload:
            return campaign.current
        if len(event.payload) != 2 or event.payload[0] != 'strength' or not natural(event.payload[1]):
            raise ValueError('fixture fact contribution')
        return replace(campaign.current, characters=tuple(replace(c, strength=event.payload[1])
            if c.id == scope.actor else c for c in campaign.current.characters))


INDEPENDENT = IndependentOwner()


def independent(*, strength=15, threshold=10):
    w = PhysicalFrame('fixture:world', 0, (Place('workshop', 'fixture'),), ('worker',), (('worker', 'workshop'),),
        objects=(PhysicalObject('a', 'fixture:device', False), PhysicalObject('b', 'fixture:device', False),
                 PhysicalObject('tool', 'fixture:tool', True)),
        relationships=(PhysicalRelation('tool', 'held', 'worker', 'fixture:possession'),))
    # Movement statistics and expenditure intentionally unavailable, never defaulted.
    c = CreatureRules('worker', None, None, strength, None, None, ready_equipment=('tool',))
    state = Domains(w, 'fixture:character', (c,))
    scope = ActivityScope('repair', 'worker', INDEPENDENT.id, 'Restore the two established devices',
        ActivityAuthorization('repair', 'fixture-repair'), ActivityCheckpoint('repair', 'fixture-repair'),
        (ActivityStage('a', (31, threshold, 1)), ActivityStage('b', (43, threshold, 1))))
    return Campaign('fixture', 'worker', state, state, (scope,))


def response(runtime, activity, key='choice'):
    e = ActivityResponse('answer:' + str(runtime.campaign.revision), activity, (key,), runtime.campaign.revision)
    runtime.accept_increment(runtime.prepare_activity_change(e))


def boundary(runtime, activity, source='boundary', key='choice', *, perceived=True):
    scope = effective_scope(runtime.campaign, activity)
    cp = replace(scope.checkpoint, developments=(ActivityDevelopment('player_choice', perceived=perceived, choice_key=key),))
    return ActivityUpdate(source, activity, 'fixture:recognized development', checkpoint=cp,
        notices=((key, 'Continuing now requires a consequential choice.'),) if perceived else (),
        choice_contexts=(ChoiceContext(key, source, (scope.index,)),))


class CommonContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.network = patch.object(socket, 'create_connection', side_effect=AssertionError('offline only'))
        cls.network.start()

    @classmethod
    def tearDownClass(cls):
        cls.network.stop()

    def runtime(self, root=None, owner=INDEPENDENT, dice=None):
        return GameSession.start_domains(root or independent(), draw=dice or Dice(), domain_handlers=(owner,))

    def test_duplicate_public_references_reject_before_coordinator_publication(self):
        class DuplicateReceiptOwner(IndependentOwner):
            def evaluate(self, *args):
                contribution = super().evaluate(*args)
                return replace(contribution, receipt=replace(contribution.receipt,
                    public_refs=('repair', 'repair')))

        owner = DuplicateReceiptOwner()
        r = self.runtime(owner=owner)
        before = r.campaign
        command = Increment('duplicate-receipt', 'repair', 0, ('tool',))
        proposal = r.prepare_increment(command)
        with self.assertRaises(ValueError):
            r.accept_increment(proposal)
        decision = r.process_increment(command)
        self.assertEqual(decision.status, 'unresolved')
        self.assertEqual(decision.failure, 'technical')
        # The same producer output is rejected before position, time, fatigue,
        # object condition, revision or accepted identity can become authoritative.
        self.assertIs(r.campaign, before)
        self.assertEqual(r.state, before.current)
        self.assertEqual((r.campaign.revision, r.campaign.accepted), (0, ()))
        self.assertFalse(r.running)
        from engine.domain_campaign import apply_unit
        with self.assertRaises(ValueError):
            apply_unit(before, proposal.unit, handlers=(owner,))

    def test_accepted_effect_cannot_reuse_changed_later_decision_premises(self):
        class FatiguePremisesOwner(IndependentOwner):
            def decision_basis(self, campaign, scope, index):
                return super().decision_basis(campaign, scope, index) + (
                    campaign.current.characters[0].exhaustion,)

        owner = FatiguePremisesOwner()
        for initially_answered in (False, True):
            with self.subTest(initially_answered=initially_answered):
                root = independent()
                a = root.activities[0]
                a = replace(a,
                    authorization=replace(a.authorization, answered_choices=('choice',) if initially_answered else ()),
                    checkpoint=replace(a.checkpoint, developments=(ActivityDevelopment(
                        'player_choice', choice_key='choice'),)),
                    notices=(('choice', 'Continue with the established fatigue stakes.'),),
                    choice_contexts=(ChoiceContext('choice', a.id, (0, 1)),))
                r = self.runtime(replace(root, activities=(a,)), owner=owner)
                if not initially_answered:
                    response(r, a.id)
                before = r.campaign
                command = Increment('changes-later-premises', a.id, 0, ('tool',))
                p = r.prepare_increment(command)
                with self.assertRaisesRegex(ValueError, 'changed decision stakes'):
                    r.accept_increment(p)
                self.assertIs(r.campaign, before)
                self.assertNotEqual(r.process_increment(command).status, 'accepted')
                self.assertIs(r.campaign, before)

                # Construct the formerly accepted sequence without publication.
                # Both an unfinished save and a completed save must fail: the
                # intermediate violation cannot disappear when the choice expires.
                from engine.domain_campaign import apply_unit, prepare
                forged = apply_unit(before, p.unit, handlers=(owner,))
                for completed in (False, True):
                    if completed:
                        later = Increment('later-stage', a.id, 1, ('tool',))
                        forged = apply_unit(forged, prepare(forged, later, handlers=(owner,)).unit,
                                            handlers=(owner,))
                    with self.assertRaisesRegex(ValueError, 'changed decision stakes'):
                        r.restore_domains(forged)
                    with self.assertRaisesRegex(ValueError, 'changed decision stakes'):
                        restore({'save_version': 3, 'domain_campaign': pack(forged)}, handlers=(owner,))
                    self.assertIs(r.campaign, before)

    def test_spanning_choice_survives_effects_that_leave_declared_premises_unchanged(self):
        root = independent()
        a = root.activities[0]
        a = replace(a, checkpoint=replace(a.checkpoint, developments=(ActivityDevelopment(
            'player_choice', choice_key='choice'),)),
            notices=(('choice', 'Continue with the established capability and plan.'),),
            choice_contexts=(ChoiceContext('choice', a.id, (0, 1)),))
        r = self.runtime(replace(root, activities=(a,)))
        response(r, a.id)
        first = Increment('unchanged-premises:first', a.id, 0, ('tool',))
        self.assertEqual(r.process_increment(first).status, 'accepted')
        self.assertEqual(r.state.characters[0].exhaustion, 1)
        r = self.runtime(restore(export(r.campaign, handlers=(INDEPENDENT,)), handlers=(INDEPENDENT,)))
        self.assertIn('choice', effective_scope(r.campaign, a.id).authorization.answered_choices)
        self.assertEqual(r.process_increment(Increment('unchanged-premises:second', a.id, 1, ('tool',))).status, 'accepted')
        self.assertEqual(restore(export(r.campaign, handlers=(INDEPENDENT,)), handlers=(INDEPENDENT,)), r.campaign)

    def test_climbing_receipt_meaning_is_independent_of_receipt_producer(self):
        from engine import climbing_domain
        cases = ((premises(), (), 'You discover an accessible secret passage.'),
                 (uncertain_campaign(hp=1), (1, 6, 6),
                  'After losing consciousness you see the hidden cause and the landing.'))
        for old, rolls, invented in cases:
            with self.subTest(invented=invented):
                r = GameSession.start_domains(modern(old), draw=Dice(*rolls))
                command = modern_command(historical_command())
                p = r.prepare_increment(command)
                forged_receipt = replace(p.unit.receipt, accessible=(('movement', invented),))
                forged_unit = replace(p.unit, receipt=forged_receipt)
                before = r.campaign
                with patch.object(climbing_domain, 'safe_receipt', return_value=forged_receipt):
                    with self.assertRaises(Unresolved):
                        r.accept_increment(replace(p, unit=forged_unit))
                    self.assertIs(r.campaign, before)
                    # A coherent forged save previously passed if producer and
                    # persisted receipt agreed on arbitrary accessible text.
                    from engine.domain_campaign import apply_unit
                    with patch.object(climbing_domain, 'safe_receipt', return_value=p.unit.receipt):
                        candidate = apply_unit(before, p.unit)
                    forged = replace(candidate, accepted=(forged_unit,))
                    with self.assertRaises(Unresolved):
                        r.restore_domains(forged)
                    with self.assertRaises(Unresolved):
                        restore({'save_version': 3, 'domain_campaign': pack(forged)})
                    self.assertIs(r.campaign, before)
                r.accept_increment(p)
                self.assertEqual(restore(export(r.campaign)), r.campaign)
                if old.schema >= 2:
                    self.assertIn('awareness ends', dict(p.unit.receipt.accessible)['movement'])

    def test_independent_runtime_changes_world_character_and_time_without_movement_vocabulary(self):
        r = self.runtime()
        outcome = r.advance_activity(ActivityRun('repair-run', 'repair', ('tool',)))
        self.assertEqual(outcome.status, 'complete', outcome)
        self.assertEqual(len(outcome.receipts), 2)
        self.assertEqual(r.state.world.at_seconds, 74)
        self.assertEqual(r.state.characters[0].exhaustion, 2)
        self.assertIsNone(r.state.characters[0].movement_spent)
        self.assertEqual(r.state.world.positions, r.campaign.origin.world.positions)
        self.assertTrue(all(o.intact for o in r.state.world.objects))
        self.assertEqual(r.domain_draw.sides, [])
        validate_campaign(r.campaign, handlers=(INDEPENDENT,))
        self.assertNotIn('climb', outcome.message.casefold())

    def test_independent_fixture_depends_on_capability_and_preserves_failed_costs(self):
        r = self.runtime(independent(strength=8))
        run = ActivityRun('failed-run', 'repair', ('tool',))
        failed = r.advance_activity(run)
        self.assertEqual(failed.status, 'failed', failed)
        self.assertEqual(r.state.world.at_seconds, 31)
        self.assertEqual(r.state.characters[0].exhaustion, 1)
        self.assertFalse(r.state.world.objects[0].intact)
        root = r.campaign
        self.assertEqual(r.advance_activity(run).status, 'failed')
        self.assertIs(r.campaign, root)

    def test_independent_interruption_save_load_exact_retry_and_resumption(self):
        r = self.runtime()
        run = ActivityRun('repair-run', 'repair', ('tool',))
        def refresh(root, scope):
            if scope.index == 1 and not any(getattr(e, 'id', '') == 'boundary' for e in root.accepted):
                return boundary(r, 'repair')
        first = r.advance_activity(run, refresh=refresh)
        self.assertEqual(first.status, 'control', first)
        self.assertEqual(len(first.receipts), 1)
        root = r.campaign
        command = root.accepted[0].command
        self.assertEqual(r.process_increment(command).status, 'accepted')
        self.assertIs(r.campaign, root)
        path = Path('.artifacts/coupling-independent.json')
        save_game(r, str(path))
        before = path.read_bytes()
        loaded = load_game(str(path), domain_handlers=(INDEPENDENT,), campaign_draw=Dice())
        self.assertEqual(loaded.campaign, root)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(loaded.advance_activity(run).status, 'control')
        response(loaded, 'repair')
        self.assertEqual(loaded.advance_activity(run).status, 'complete')
        self.assertEqual(loaded.state.world.at_seconds, 74)
        self.assertEqual(loaded.state.characters[0].exhaustion, 2)
        self.assertEqual(loaded.domain_draw.sides, [])
        self.assertEqual(loaded.process_increment(command).status, 'accepted')
        self.assertEqual(len(successful_units(loaded.campaign, 'repair')), 2)
        self.assertEqual(export(loaded.campaign, handlers=(INDEPENDENT,))['save_version'], 3)

    def test_independent_rejections_leave_root_unchanged(self):
        r = self.runtime()
        c = Increment('one', 'repair', 0, ('tool',))
        p = r.prepare_increment(c)
        for u in (replace(p.unit, progressed=False), replace(p.unit, evidence=(False, 99, 0, True)),
                  replace(p.unit, receipt=replace(p.unit.receipt, accessible=(('repair', 'Invented success'),))),
                  replace(p.unit, command=replace(c, stage=1)),
                  replace(p.unit, command=replace(c, payload=('absent-tool',)))):
            before = r.campaign
            with self.subTest(unit=u), self.assertRaises((ValueError, Unresolved)):
                r.accept_increment(replace(p, unit=u))
            self.assertIs(r.campaign, before)
        r.accept_increment(p)
        before = r.campaign
        with self.assertRaises((ValueError, Unresolved)):
            r.prepare_increment(replace(c, payload=('changed',)))
        self.assertIs(r.campaign, before)
        stale = r.prepare_increment(Increment('two', 'repair', 1, ('tool',)))
        e = ActivityUpdate('facts', 'repair', 'supplier', payload=('strength', 16))
        r.accept_increment(r.prepare_activity_change(e))
        before = r.campaign
        with self.assertRaises(Unresolved):
            r.accept_increment(stale)
        self.assertIs(r.campaign, before)

    def test_hidden_choice_and_unavailable_inputs_do_not_disclose_or_draw(self):
        r = self.runtime()
        event = boundary(r, 'repair', perceived=False)
        r.accept_increment(r.prepare_activity_change(event))
        with self.assertRaises(ValueError):
            response(r, 'repair')
        self.assertEqual(r.advance_activity(ActivityRun('run', 'repair', ('tool',))).status, 'complete')
        r = self.runtime(independent(strength=None))
        before = r.campaign
        result = r.advance_activity(ActivityRun('run', 'repair', ('tool',)))
        self.assertEqual(result.status, 'unresolved')
        self.assertNotIn('strength', result.message)
        self.assertIs(r.campaign, before)
        self.assertEqual(r.domain_draw.sides, [])

    def test_common_choice_context_binds_independent_mechanics_and_cannot_be_laundered(self):
        r = self.runtime()
        r.accept_increment(r.prepare_activity_change(boundary(r, 'repair')))
        response(r, 'repair')
        for e in (ActivityUpdate('changed-facts', 'repair', 'supplier', payload=('strength', 16)),
                  ActivityUpdate('changed-stage', 'repair', 'supplier', stage=ActivityStage('a', (31, 20, 1)))):
            before = r.campaign
            with self.assertRaises(ValueError):
                r.accept_increment(r.prepare_activity_change(e))
            self.assertIs(r.campaign, before)
        e = boundary(r, 'repair', source='fresh-boundary', key='fresh-choice')
        e = replace(e, payload=('strength', 16))
        r.accept_increment(r.prepare_activity_change(e))
        self.assertEqual(r.advance_activity(ActivityRun('run', 'repair', ('tool',))).status, 'control')
        response(r, 'repair', 'fresh-choice')
        self.assertEqual(r.advance_activity(ActivityRun('run', 'repair', ('tool',))).status, 'complete')

    def test_unknown_owners_invalid_records_and_corruption_reject_before_adoption(self):
        r = self.runtime()
        r.advance_activity(ActivityRun('run', 'repair', ('tool',)))
        envelope = export(r.campaign, handlers=(INDEPENDENT,))
        with self.assertRaises(ValueError):
            restore(envelope)
        variants = []
        for field, value in (('schema', 3), ('schema', True), ('revision', 100)):
            bad = copy.deepcopy(envelope)
            bad['domain_campaign']['fields'][field] = value
            variants.append(bad)
        bad = copy.deepcopy(envelope)
        bad['domain_campaign']['fields']['accepted']['tuple'][0]['fields']['progressed'] = False
        variants.append(bad)
        bad = copy.deepcopy(envelope)
        del bad['domain_campaign']['fields']['activities']['tuple'][0]['fields']['choice_contexts']
        variants.append(bad)
        bad = copy.deepcopy(envelope)
        bad['domain_campaign']['fields']['accepted']['tuple'][0]['fields']['evidence'] = {'record': 'eval', 'fields': {}}
        variants.append(bad)
        for bad in variants:
            before = r.campaign
            with self.assertRaises((ValueError, Unresolved)):
                r.restore_domains(restore(bad, handlers=(INDEPENDENT,)))
            self.assertIs(r.campaign, before)

    def test_atomic_writer_failure_and_duplicate_keys(self):
        r = self.runtime()
        path = Path('.artifacts/coupling-atomic.json')
        save_game(r, str(path))
        before, root = path.read_bytes(), r.campaign
        r.advance_activity(ActivityRun('run', 'repair', ('tool',)))
        with patch('engine.save_system.os.replace', side_effect=OSError('fixture write failure')):
            with self.assertRaises(OSError):
                save_game(r, str(path))
        self.assertEqual(path.read_bytes(), before)
        self.assertNotEqual(r.campaign, root)
        payload = before.decode('utf-8').replace('"schema": 4', '"schema": 4, "schema": 4')
        path.write_text(payload, encoding='utf-8')
        with self.assertRaises(ValueError):
            load_game(str(path), domain_handlers=(INDEPENDENT,))

    def test_reentrant_attempt_cannot_publish_and_failed_draw_preserves_history(self):
        r = self.runtime()
        p = r.prepare_increment(Increment('one', 'repair', 0, ('tool',)))
        r.running = True
        with self.assertRaises(Unresolved):
            r.accept_increment(p)
        r.running = False
        r.accept_increment(p)
        root = r.campaign
        with self.assertRaises(Unresolved):
            r.accept_increment(replace(p, unit=replace(p.unit, progressed=False)))
        self.assertIs(r.campaign, root)

    def test_common_modules_have_no_mechanical_fields_or_branches(self):
        prohibited = {'ClimbRequest', 'ClimbRuling', 'ClimbResult', 'TraversalConsequence', 'use_climb_speed',
            'failure_mode', 'failure_movement_cost', 'climb_circumstances', 'distance_feet', 'movement_charge'}
        for name in ('domain_campaign', 'domain_activity', 'domain_dispatch', 'consequence_integration'):
            tree = ast.parse(Path('engine', name + '.py').read_text(encoding='utf-8-sig'))
            identifiers = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
            attributes = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
            self.assertFalse(prohibited.intersection(identifiers | attributes), name)
            self.assertFalse(any(isinstance(n, ast.ImportFrom) and n.module in {
                'engine.climbing_domain', 'engine.traversal_resolution', 'engine.traversal_coordination'}
                for n in ast.walk(tree)), name)
        for cls in (ActivityScope, ActivityStage, ActivityRun, Increment, AcceptedUnit, ActivityUpdate):
            self.assertFalse(prohibited.intersection(f.name for f in fields(cls)))


class ClimbingReplacementTests(unittest.TestCase):
    def test_deterministic_and_uncertain_gameplay_equivalence(self):
        cases = [(premises(), historical_command(), ())]
        for protected in (False, True):
            for footing in ('load_bearing', 'grip_dependent'):
                for rolls in ((20,), (1, 3, 4)):
                    old = uncertain_campaign(protected=protected, footing=footing)
                    cases.append((old, historical_command(), rolls))
        for hp in (1, 30):
            for drop in (5, 20):
                cases.append((uncertain_campaign(hp=hp, maximum=max(25, hp), height=drop), historical_command(), (1, 6, 6)))
        for speed in (0, 15):
            cases.append((premises(climb_speed=speed), historical_command(climb=bool(speed)), ()))
        for strength, rank, roll in ((8, 0, 20), (8, 0, 1), (20, 2, 1), (20, 2, 20)):
            cases.append((uncertain_campaign(strength=strength, rank=rank), historical_command(), (roll, 4, 5)))
        for condition in ('prone', 'stunned', 'restrained', 'exhaustion'):
            old = foundation(uncertain=True)
            c = old.origin.characters[0]
            c = replace(c, exhaustion=2) if condition == 'exhaustion' else replace(c, conditions=(condition,))
            d = replace(old.origin, characters=(c,))
            cases.append((replace(old, origin=d, current=d), historical_command(), (20,)))
        for old, command, rolls in cases:
            with self.subTest(protected=old.origin.world.climb_circumstances, rolls=rolls):
                legacy = GameSession.start_domains(old, draw=Dice(*rolls))
                new = GameSession.start_domains(modern(old), draw=Dice(*rolls))
                before = new.campaign
                a, b = legacy.process_increment(command), new.process_increment(modern_command(command))
                self.assertEqual(b.status, a.status, (a, b))
                self.assertEqual(b.message, a.message)
                self.assertEqual(new.state, legacy.state)
                self.assertEqual(new.domain_draw.sides, legacy.domain_draw.sides)
                self.assertEqual(new.domain_draw.values, legacy.domain_draw.values)
                if b.status == 'accepted':
                    unit = new.campaign.accepted[-1]
                    self.assertEqual(unit.evidence[0], legacy.campaign.accepted[-1].result)
                    self.assertEqual(pack(unit.evidence[1]), pack(legacy.campaign.accepted[-1].consequence)
                                     if old.schema >= 2 else pack(unit.evidence[1]))
                    root = new.campaign
                    retry = new.process_increment(modern_command(command))
                    self.assertEqual((retry.status, retry.message, retry.results), (b.status, b.message, b.results))
                    self.assertIs(new.campaign, root)
                    self.assertEqual(restore(export(new.campaign)), root)
                else:
                    self.assertIs(new.campaign, before)

    def test_new_climbing_continuity_rechecks_f05_and_current_means(self):
        r = GameSession.start_domains(modern(foundation()), draw=Dice())
        run = ActivityRun('climb-run', 'activity:first', (ClimbOptions(),))
        def refresh(root, scope):
            if scope.index == 1 and not any(getattr(e, 'id', '') == 'boundary' for e in root.accepted):
                return boundary(r, 'activity:first')
        result = r.advance_activity(run, refresh=refresh)
        self.assertEqual(result.status, 'control', result)
        self.assertEqual(len(result.receipts), 1)
        r = GameSession.start_domains(restore(export(r.campaign)), draw=Dice())
        response(r, 'activity:first')
        self.assertEqual(r.advance_activity(run).status, 'complete')
        self.assertEqual(r.state.world.at_seconds, 47)
        self.assertEqual(r.state.characters[0].movement_spent, 20)
        self.assertEqual(dict(r.state.world.positions)['creature'], 'end')

    def test_climbing_choice_binding_uses_domain_risk_and_rule_stakes(self):
        r = GameSession.start_domains(modern(foundation(uncertain=True)), draw=Dice(20, 20))
        r.accept_increment(r.prepare_activity_change(boundary(r, 'activity:first')))
        response(r, 'activity:first')
        s = effective_scope(r.campaign, 'activity:first')
        p = s.payload[0]
        altered = replace(p, ruling=replace(p.ruling, failure_movement_cost=p.ruling.failure_movement_cost + 1))
        event = ActivityUpdate('changed-stakes', s.id, 'rule owner', stage=ActivityStage(s.target, (altered,)))
        before = r.campaign
        with self.assertRaises(ValueError):
            r.accept_increment(r.prepare_activity_change(event))
        self.assertIs(r.campaign, before)

    def test_schema4_climbing_rejects_forged_dice_consequences_receipts_and_restore(self):
        r = GameSession.start_domains(modern(uncertain_campaign()), draw=Dice(1, 3, 4))
        p = r.prepare_increment(modern_command(historical_command()))
        result, consequence = p.unit.evidence
        variants = (
            replace(p.unit, evidence=(replace(result, success=True), consequence)),
            replace(p.unit, evidence=(replace(result, rolls=(20,)), consequence)),
            replace(p.unit, evidence=(result, replace(consequence, position='middle'))),
            replace(p.unit, evidence=(result, replace(consequence,
                injury=replace(consequence.injury, bludgeoning_damage=0)))),
            replace(p.unit, receipt=replace(p.unit.receipt, accessible=(('movement', 'hidden invented cause'),))),
        )
        for unit in variants:
            before = r.campaign
            with self.assertRaises((ValueError, Unresolved)):
                r.accept_increment(replace(p, unit=unit))
            self.assertIs(r.campaign, before)
        r.accept_increment(p)
        root = r.campaign
        for unit in variants:
            with self.assertRaises((ValueError, Unresolved)):
                restore({'save_version': 3, 'domain_campaign': pack(replace(root, accepted=(unit,)))})
            self.assertIs(r.campaign, root)
        self.assertEqual(r.domain_draw.sides, [20, 6, 6])

    def test_schema4_current_conditions_and_restrictions_gate_continuation_without_draws(self):
        root = modern(foundation(uncertain=True))
        a = root.activities[0]
        root = replace(root, activities=(replace(a, supported_constraints=('carefully',),
            authorization=replace(a.authorization, constraints=('carefully',))),))
        r = GameSession.start_domains(root, draw=Dice(20, 20))
        run = ActivityRun('climb-run', a.id, (ClimbOptions(),))
        def refresh(current, scope):
            if scope.index == 1 and not any(getattr(e, 'id', '') == 'capacity-change' for e in current.accepted):
                c = replace(current.current.characters[0], conditions=('stunned',))
                return ActivityUpdate('capacity-change', a.id, 'Character current capacity',
                    payload=(ClimbUpdate(characters=(c,)),))
        first = r.advance_activity(run, refresh=refresh)
        self.assertEqual(first.status, 'control', first)
        self.assertEqual(len(first.receipts), 1)
        self.assertEqual(r.domain_draw.sides, [20])
        self.assertEqual(effective_scope(r.campaign, a.id).authorization.constraints, ('carefully',))
        c = replace(r.state.characters[0], conditions=())
        e = ActivityUpdate('capacity-restored', a.id, 'Character current capacity', payload=(ClimbUpdate(characters=(c,)),))
        r.accept_increment(r.prepare_activity_change(e))
        self.assertEqual(r.advance_activity(run).status, 'complete')
        self.assertEqual(r.domain_draw.sides, [20, 20])

    def test_schema4_inquiry_and_failed_later_supplier_preserve_no_draw_and_prior_receipts(self):
        root = modern(foundation(uncertain=True))
        a = root.activities[0]
        inquiry = replace(root, activities=(replace(a, authorization=replace(a.authorization, intent='inquiry')),))
        r = GameSession.start_domains(inquiry, draw=Dice())
        before = r.campaign
        result = r.process_increment(modern_command(historical_command()))
        self.assertNotEqual(result.status, 'accepted')
        self.assertIs(r.campaign, before)
        self.assertEqual(r.domain_draw.sides, [])
        r = GameSession.start_domains(root, draw=Dice(20))
        run = ActivityRun('climb-run', a.id, (ClimbOptions(),))
        def broken_supplier(current, scope):
            if scope.index == 1:
                raise RuntimeError('hidden supplier detail must not be disclosed')
        result = r.advance_activity(run, refresh=broken_supplier)
        self.assertEqual(result.status, 'unresolved')
        self.assertEqual(len(result.receipts), 1)
        self.assertIn('climb', result.message)
        self.assertNotIn('hidden', result.message)
        self.assertEqual(r.domain_draw.sides, [20])
        self.assertEqual(restore(export(r.campaign)), r.campaign)

    def test_schemas_1_2_3_roundtrip_and_unfinished_historical_activity_remain_historical(self):
        for old in (premises(), uncertain_campaign(), foundation(uncertain=True)):
            r = GameSession.start_domains(old, draw=Dice(20, 20))
            schema = old.schema
            encoded = export(old)
            raw = json.dumps(encoded)
            loaded = GameSession.start_domains(restore(json.loads(raw)), draw=Dice(20, 20))
            self.assertEqual(loaded.campaign.schema, schema)
            self.assertIs(type(loaded.campaign), historical_campaign.Campaign)
            self.assertEqual(json.dumps(export(loaded.campaign)), raw)
            if schema == 3:
                run = historical_activity.ActivityRun('historical-run', 'activity:first')
                first = loaded.process_increment(historical_campaign.Increment('activity:first',
                    historical_command().request))
                self.assertEqual(first.status, 'accepted', first)
                loaded = GameSession.start_domains(restore(export(loaded.campaign)), draw=Dice(20))
                self.assertEqual(loaded.advance_activity(run).status, 'complete')
                self.assertEqual(loaded.campaign.schema, 3)
            else:
                result = loaded.process_increment(historical_command())
                self.assertEqual(result.status, 'accepted', result)
            self.assertEqual(encoded, json.loads(raw))


if __name__ == '__main__':
    unittest.main(verbosity=2)
