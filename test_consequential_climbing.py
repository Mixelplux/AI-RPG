"""Offline M2-2a production-boundary validation; fixtures contain premises, not answers."""
import copy
import json
import socket
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from engine.activity_control import ActivityDevelopment
from engine.character_rules import CharacterRules, StrengthTrait, Vitality
from engine.historical_campaign import validate_campaign
from engine.domain_persistence import export, pack, restore, LEGACY_DEFAULTS
from engine.game_session import GameSession
from engine.information_adjudication import Unresolved
from engine.physical_world import (ClimbCircumstances, PhysicalObject, PhysicalRelation, TautProtection,
                                   Place, Surface, TraversalLink, CausalRecord, FallOccurrence)
from engine.save_system import save_game, load_game
from engine.traversal_resolution import ClimbRuling
from test_domain_acceptance import premises, command


def campaign(*, footing='grip_dependent', height=20, protected=False, hp=25,
             maximum=25, strength=14, rank=1, speed=90, actor='creature', locality='local'):
    root = premises(actor=actor, locality=locality, speed=speed)
    w = root.origin.world
    # 'base' is a meaningful elevated position here; names confer no geometry.
    world = replace(w, positions=((actor, 'base'),),
        surfaces=(replace(w.surfaces[0], slippery=True, difficult=True),),
        objects=(PhysicalObject('rope', 'rope-definition', True),
                 PhysicalObject('anchor', 'anchor-definition', True),
                 PhysicalObject('harness', 'harness-definition', True),
                 PhysicalObject('tool', 'tool-definition', True)),
        relationships=(PhysicalRelation('rope', 'carried', actor, 'established'),
                       PhysicalRelation('tool', 'held', actor, 'established')))
    protection = 'none'
    if protected:
        protection = TautProtection('rope', 'harness', 'anchor', 'base', True, True,
                                    'hidden:verified taut load-bearing system')
        world = replace(world, relationships=world.relationships + (
            PhysicalRelation('anchor', 'secured', 'base', 'verified'),
            PhysicalRelation('rope', 'secured', 'anchor', 'verified'),
            PhysicalRelation('rope', 'attached', 'harness', 'verified'),
            PhysicalRelation('harness', 'attached', actor, 'verified')))
    x = ClimbCircumstances('risk:first:established', 'first', footing, 'end', height,
                           'solid', protection, 'none', 'hidden:physical circumstances')
    world = replace(world, climb_circumstances=(x,))
    c = replace(root.origin.characters[0], strength=strength, proficiency_bonus=2,
                athletics_rank=rank, hit_points=hp, vitality=Vitality(maximum),
                ready_equipment=('rope', 'harness'))
    d = replace(root.origin, world=world, characters=(c,))
    a = root.activities[0]
    a = replace(a, ruling=ClimbRuling(True, 'context:2024 slippery grip test',
                                     'no_progress' if footing == 'load_bearing' else 'loss_of_grip', 15),
                authorization=replace(a.authorization, answered_choices=(x.id,)))
    return replace(root, origin=d, current=d, activities=(a,) + root.activities[1:], schema=2)


def change(root, *, world=None, character=None, scope=None):
    d = replace(root.origin, world=world or root.origin.world,
                characters=(character or root.origin.characters[0],))
    return replace(root, origin=d, current=d,
                   activities=(scope or root.activities[0],) + root.activities[1:])


class Dice:
    def __init__(self, *values):
        self.values = list(values)
        self.sides = []

    def __call__(self, sides):
        self.sides.append(sides)
        if not self.values:
            raise AssertionError('unexpected draw')
        return self.values.pop(0)


class ConsequentialClimbingTests(unittest.TestCase):
    def run_attempt(self, root, values):
        draw = Dice(*values)
        runtime = GameSession.start_domains(root, draw=draw)
        decision = runtime.process_increment(command(actor=root.actor))
        self.assertEqual(decision.status, 'accepted', decision)
        return runtime, draw, decision

    def assert_blocked(self, root):
        draw = Dice()
        runtime = GameSession.start_domains(root, draw=draw)
        before = runtime.campaign
        decision = runtime.process_increment(command(actor=root.actor))
        self.assertNotEqual(decision.status, 'accepted')
        self.assertIs(runtime.campaign, before)
        self.assertEqual(draw.sides, [])
        self.assertNotIn('hidden:', decision.message)

    def test_exposed_failure_is_coherent_actual_fall(self):
        r, draw, decision = self.run_attempt(campaign(), (1, 3, 4))
        u = r.campaign.accepted[0]
        self.assertFalse(u.result.success)
        self.assertEqual(u.result.rolls, (1,))
        self.assertEqual(u.consequence.kind, 'fell')
        self.assertEqual(u.consequence.injury.rolls, (3, 4))
        self.assertEqual(draw.sides, [20, 6, 6])
        self.assertEqual(dict(r.state.world.positions)['creature'], 'end')
        self.assertEqual(r.state.characters[0].hit_points, 18)
        self.assertIn('prone', r.state.characters[0].conditions)
        self.assertEqual(r.state.characters[0].movement_spent, 15)
        self.assertEqual(r.state.world.at_seconds, 28)
        self.assertEqual(r.state.world.falls, (u.consequence.fall,))
        self.assertEqual(r.state.world.falls[0].cause, u.command.request.attempt)
        self.assertEqual(r.campaign.revision, 1)
        self.assertNotIn('hidden', decision.message)
        self.assertNotIn('20 feet', decision.message)

    def test_success_draws_no_fall_dice(self):
        r, draw, _ = self.run_attempt(campaign(), (11,))
        self.assertTrue(r.campaign.accepted[0].result.success)
        self.assertEqual(draw.sides, [20])
        self.assertEqual(dict(r.state.world.positions)['creature'], 'middle')
        self.assertEqual(r.state.characters[0].hit_points, 25)
        self.assertFalse(r.state.world.falls)

    def test_protection_verifies_actual_relationships(self):
        root = campaign(protected=True)
        r, draw, decision = self.run_attempt(root, (1,))
        self.assertEqual(draw.sides, [20])
        self.assertEqual(r.campaign.accepted[0].consequence.kind, 'grip_lost_protected')
        self.assertEqual(dict(r.state.world.positions)['creature'], 'base')
        self.assertEqual(r.state.characters[0].hit_points, 25)
        self.assertEqual(r.state.world.relationships, root.origin.world.relationships)
        self.assertIn('taut protection', decision.message)
        for index in range(2, 6):
            w = root.origin.world
            self.assert_blocked(change(root, world=replace(w,
                relationships=w.relationships[:index] + w.relationships[index+1:])))

    def test_rope_in_inventory_is_not_protection(self):
        root = campaign(protected=True)
        w = root.origin.world
        self.assert_blocked(change(root, world=replace(w, relationships=w.relationships[:2])))

    def test_missing_unknown_damaged_or_slack_protection_blocks_before_draw(self):
        root = campaign(protected=True)
        w, x = root.origin.world, root.origin.world.climb_circumstances[0]
        for p in (replace(x.protection, taut=False), replace(x.protection, load_bearing=None)):
            self.assert_blocked(change(root, world=replace(w, climb_circumstances=(replace(x, protection=p),))))
        for intact in (False, None):
            self.assert_blocked(change(root, world=replace(w,
                objects=(replace(w.objects[0], intact=intact),) + w.objects[1:])))
        self.assert_blocked(change(root, character=replace(root.origin.characters[0], ready_equipment=('rope',))))

    def test_near_ground_load_bearing_failure_retains_real_footing(self):
        r, draw, _ = self.run_attempt(campaign(footing='load_bearing', height=0), (1,))
        self.assertEqual(r.campaign.accepted[0].consequence.kind, 'supported_no_progress')
        self.assertEqual(dict(r.state.world.positions)['creature'], 'base')
        self.assertEqual(draw.sides, [20])
        self.assertEqual(r.state.characters[0].hit_points, 25)
        self.assertFalse(r.state.world.falls)

    def test_short_actual_fall_has_no_damage_or_invented_prone(self):
        r, draw, _ = self.run_attempt(campaign(height=9), (1,))
        self.assertEqual(r.campaign.accepted[0].consequence.kind, 'fell')
        self.assertEqual(r.campaign.accepted[0].consequence.injury.bludgeoning_damage, 0)
        self.assertEqual(draw.sides, [20])
        self.assertNotIn('prone', r.state.characters[0].conditions)
        self.assertEqual(len(r.state.world.falls), 1)

    def test_fall_damage_cap(self):
        r, draw, _ = self.run_attempt(campaign(height=1000, hp=200, maximum=200), (1,) + (6,) * 20)
        self.assertEqual(r.state.characters[0].hit_points, 80)
        self.assertEqual(draw.sides, [20] + [6] * 20)

    def test_different_world_and_character_premises_change_results(self):
        for actor, locality, rank, expected in (('pc', 'tower', 0, False), ('npc', 'mine', 2, True)):
            root = campaign(actor=actor, locality=locality, rank=rank, protected=True)
            r, _, _ = self.run_attempt(root, (10,))
            self.assertEqual(r.campaign.accepted[0].result.success, expected)
        for difficult, expected in ((False, 10), (True, 15)):
            root = campaign(protected=True)
            w = root.origin.world
            r, _, _ = self.run_attempt(change(root, world=replace(w,
                surfaces=(replace(w.surfaces[0], difficult=difficult),)),
                scope=replace(root.activities[0], ruling=replace(root.activities[0].ruling,
                    failure_movement_cost=expected))), (20,))
            self.assertEqual(r.state.characters[0].movement_spent, expected)

    def test_training_advantage_exhaustion_and_special_speed(self):
        root = campaign(protected=True)
        c = root.origin.characters[0]
        cases = (
            (replace(c, traits=(StrengthTrait('feature:strength', True),)), (1, 11), True, [20, 20], 15),
            (replace(c, conditions=('poisoned',)), (20, 1), False, [20, 20], 15),
            (replace(c, conditions=('poisoned',), traits=(StrengthTrait('feature:strength', True),)), (11,), True, [20], 15),
            (replace(c, exhaustion=1), (11,), False, [20], 15),
        )
        for character, values, success, sides, spent in cases:
            r, draw, _ = self.run_attempt(change(root, character=character), values)
            self.assertEqual(r.campaign.accepted[0].result.success, success)
            self.assertEqual(draw.sides, sides)
            self.assertEqual(r.state.characters[0].movement_spent, spent)
        root = change(root, character=replace(c, climb_speed=90),
            scope=replace(root.activities[0], ruling=replace(root.activities[0].ruling, failure_movement_cost=10)))
        draw = Dice(1)
        r = GameSession.start_domains(root, draw=draw)
        self.assertEqual(r.process_increment(command(climb=True)).status, 'accepted')
        self.assertFalse(r.campaign.accepted[0].result.success)
        self.assertEqual(r.state.characters[0].movement_spent, 10)
        self.assertEqual(draw.sides, [20])

    def test_no_natural_one_or_twenty_override(self):
        r, _, _ = self.run_attempt(campaign(strength=30, rank=2, protected=True), (1,))
        self.assertTrue(r.campaign.accepted[0].result.success)
        # -5 still meets DC15 on 20; Exhaustion makes a real failed natural20.
        root = campaign(strength=1, rank=0, protected=True)
        r, _, _ = self.run_attempt(change(root, character=replace(root.origin.characters[0], exhaustion=1)), (20,))
        self.assertFalse(r.campaign.accepted[0].result.success)

    def test_unresolved_or_unsupported_material_inputs_never_become_safe_failure(self):
        root = campaign()
        w, x = root.origin.world, root.origin.world.climb_circumstances[0]
        for x in (replace(x, footing=None), replace(x, landing=None), replace(x, drop_feet=None),
                  replace(x, protection=None), replace(x, assistance=None), replace(x, assistance='helper'),
                  replace(x, landing_medium='liquid'), replace(x, unresolved_bindings=('hidden:effect',))):
            self.assert_blocked(change(root, world=replace(w, climb_circumstances=(x,))))
        self.assert_blocked(change(root, world=replace(w, climb_circumstances=())))
        c = root.origin.characters[0]
        for c in (replace(c, vitality=None), replace(c, strength=None),
                  replace(c, unresolved_rules=('damage:mitigation',)), replace(c, conditions=('petrified',))):
            self.assert_blocked(change(root, character=c))

    def test_progress_only_classification_cannot_sanitize_exposure(self):
        root = campaign()
        a = root.activities[0]
        for mode in (None, 'no_progress'):
            self.assert_blocked(change(root, scope=replace(a, ruling=replace(a.ruling, failure_mode=mode))))

    def test_failure_expenditure_is_explicit_and_scoped(self):
        root = campaign(protected=True)
        a = root.activities[0]
        for cost in (0, 5, 15):
            r, _, _ = self.run_attempt(change(root, scope=replace(a,
                ruling=replace(a.ruling, failure_movement_cost=cost))), (1,))
            self.assertEqual(r.state.characters[0].movement_spent, cost)
        for cost in (None, 16, True):
            if cost is True:
                with self.assertRaises(ValueError):
                    GameSession.start_domains(change(root, scope=replace(a,
                        ruling=replace(a.ruling, failure_movement_cost=cost))))
            else:
                self.assert_blocked(change(root, scope=replace(a,
                    ruling=replace(a.ruling, failure_movement_cost=cost))))

    def test_f05_unanswered_risk_restriction_and_intent_prevent_draws(self):
        root = campaign()
        a = root.activities[0]
        self.assert_blocked(change(root, scope=replace(a,
            authorization=replace(a.authorization, answered_choices=()))))
        for intent in ('inquiry', 'prepare'):
            draw = Dice()
            r = GameSession.start_domains(change(root, scope=replace(a,
                authorization=replace(a.authorization, intent=intent))), draw=draw)
            self.assertIn(r.process_increment(command()).status, {'inquiry', 'preparation'})
            self.assertEqual(draw.sides, [])
            self.assertEqual(r.campaign.accepted, ())
        self.assert_blocked(change(root, scope=replace(a, checkpoint=replace(a.checkpoint, blocked=True))))
        self.assert_blocked(change(root, scope=replace(a, authorization=replace(a.authorization, constraints=('quiet',)))))
        d = ActivityDevelopment('player_choice', choice_key='risk:other')
        self.assert_blocked(change(root, scope=replace(a, checkpoint=replace(a.checkpoint, developments=(d,)))))

    def test_zero_hp_unconscious_and_world_drop_publish_together(self):
        root = campaign(hp=5)
        # A held object still attached to the rope loses the held edge only.
        w = root.origin.world
        w = replace(w, relationships=w.relationships + (PhysicalRelation('tool', 'attached', 'rope', 'known'),))
        r, _, decision = self.run_attempt(change(root, world=w), (1, 3, 4))
        c = r.state.characters[0]
        self.assertEqual(c.hit_points, 0)
        self.assertFalse(c.vitality.dead)
        self.assertFalse(c.vitality.stable)
        self.assertEqual((c.vitality.death_successes, c.vitality.death_failures), (0, 0))
        self.assertTrue({'unconscious', 'incapacitated', 'prone'}.issubset(c.conditions))
        edges = {(e.object, e.kind, e.target) for e in r.state.world.relationships}
        self.assertNotIn(('tool', 'held', 'creature'), edges)
        self.assertIn(('tool', 'attached', 'rope'), edges)
        self.assertNotIn(('tool', 'located', 'end'), edges)
        self.assertIn('awareness ends', decision.message)
        capability = CharacterRules(r.state.character_revision, r.state.characters).physical_capability('creature')
        self.assertEqual(capability.speed, 0)
        self.assertFalse(capability.coordinated_movement or capability.actions)
        self.assertEqual(r.process_increment(command(route='next', attempt='new')).status, 'unresolved')

    def test_loose_held_object_drops_at_landing(self):
        r, _, _ = self.run_attempt(campaign(hp=5), (1, 3, 4))
        self.assertIn(('tool', 'located', 'end'), {(e.object, e.kind, e.target) for e in r.state.world.relationships})

    def test_temporary_hp_and_massive_damage_threshold(self):
        root = campaign(hp=5, maximum=10)
        root = change(root, character=replace(root.origin.characters[0], vitality=Vitality(10, temporary_hp=4)))
        r, _, _ = self.run_attempt(root, (1, 3, 4))
        self.assertEqual(r.state.characters[0].hit_points, 2)
        self.assertEqual(r.state.characters[0].vitality.temporary_hp, 0)
        for hp, maximum, values, dead in ((5, 7, (6, 6), True), (5, 8, (6, 6), False)):
            r, _, _ = self.run_attempt(campaign(hp=hp, maximum=maximum), (1,) + values)
            self.assertEqual(r.state.characters[0].vitality.dead, dead)

    def test_monster_zero_hp_treatment_is_explicit_not_an_actor_name_branch(self):
        for actor in ('pc', 'npc'):
            root = campaign(hp=5, actor=actor)
            root = change(root, character=replace(root.origin.characters[0], vitality=Vitality(25, zero_hp_rule='instant_death')))
            r, _, _ = self.run_attempt(root, (1, 3, 4))
            self.assertTrue(r.state.characters[0].vitality.dead)
            self.assertEqual(r.state.characters[0].hit_points, 0)

    def test_character_immediate_damage_at_zero_without_death_save_progression(self):
        root = campaign(hp=5)
        c = root.origin.characters[0]
        for stable, failures in ((True, 0), (False, 2)):
            c0 = replace(c, hit_points=0, conditions=('unconscious', 'incapacitated', 'prone'),
                         vitality=Vitality(25, stable=stable, death_failures=failures))
            out = CharacterRules('now', (c0,)).apply_fall_damage(c.id, 3)
            self.assertFalse(out.vitality.stable)
            self.assertEqual(out.vitality.death_failures, failures + 1)
            self.assertEqual(out.vitality.dead, failures == 2)

    def test_exact_retry_without_owner_reads_or_draws(self):
        r, draw, first = self.run_attempt(campaign(hp=5), (1, 3, 4))
        before = r.campaign
        with patch('engine.historical_campaign.owners', side_effect=AssertionError('owner read')):
            self.assertEqual(r.process_increment(command()).results, first.results)
            proposal = r.prepare_increment(command())
            self.assertEqual(r.accept_increment(proposal), first.results[0])
        self.assertIs(r.campaign, before)
        self.assertEqual(draw.sides, [20, 6, 6])
        self.assertEqual(r.process_increment(command(distance=4)).status, 'unresolved')
        malformed = replace(proposal, unit=replace(proposal.unit, duration_seconds=True))
        with self.assertRaises((ValueError, Unresolved)):
            r.accept_increment(malformed)
        self.assertIs(r.campaign, before)

    def test_stale_world_or_character_rejects_resolved_proposal(self):
        for field in ('world', 'character'):
            root = campaign()
            r = GameSession.start_domains(root, draw=Dice(1, 3, 4))
            p = r.prepare_increment(command())
            other = change(root, world=replace(root.origin.world, at_seconds=18)) if field == 'world' else change(
                root, character=replace(root.origin.characters[0], hit_points=24))
            r.restore_domains(other)
            before = r.campaign
            with self.assertRaises(Unresolved):
                r.accept_increment(p)
            self.assertIs(r.campaign, before)

    def test_root_change_during_draw_cannot_publish_old_proposal(self):
        root = campaign()
        r = GameSession.start_domains(root)
        changed = change(root, world=replace(root.origin.world, at_seconds=18))
        values = iter((1, 3, 4))
        def draw(sides):
            r.restore_domains(changed)
            return next(values)
        r.domain_draw = draw
        self.assertEqual(r.process_increment(command()).status, 'unresolved')
        self.assertIs(r.campaign, changed)
        self.assertFalse(r.campaign.accepted)

    def test_forged_results_damage_disposition_and_receipts_reject_atomically(self):
        r = GameSession.start_domains(campaign(), draw=Dice(1, 3, 4))
        before = r.campaign
        p = r.prepare_increment(command())
        u, c = p.unit, p.unit.consequence
        units = (
            replace(u, result=replace(u.result, rolls=(21,))),
            replace(u, result=replace(u.result, rolls=(True,))),
            replace(u, result=replace(u.result, total=99)),
            replace(u, result=replace(u.result, success=True)),
            replace(u, consequence=replace(c, kind='supported_no_progress')),
            replace(u, consequence=replace(c, position='base')),
            replace(u, consequence=replace(c, fall=replace(c.fall, distance_feet=0))),
            replace(u, consequence=replace(c, injury=replace(c.injury, rolls=(3,)))),
            replace(u, consequence=replace(c, injury=replace(c.injury, bludgeoning_damage=0))),
            replace(u, receipt=replace(u.receipt, accessible=(('movement', 'hidden:invented safe failure'),))),
        )
        for unit in units:
            with self.assertRaises((Unresolved, ValueError)):
                r.accept_increment(replace(p, unit=unit))
            self.assertIs(r.campaign, before)

    def test_bad_die_and_receipt_producer_never_publish_fiction(self):
        for values in ((0,), (True,), (1, 7), (1, 3, False)):
            r = GameSession.start_domains(campaign(), draw=Dice(*values))
            before = r.campaign
            self.assertEqual(r.process_increment(command()).status, 'unresolved')
            self.assertIs(r.campaign, before)
        r = GameSession.start_domains(campaign(), draw=Dice(1, 3, 4))
        before = r.campaign
        with patch('engine.historical_campaign.safe_receipt', return_value=None):
            self.assertEqual(r.process_increment(command()).status, 'unresolved')
        self.assertIs(r.campaign, before)

    def test_save_load_preserves_accepted_dice_injury_and_retry_without_draw(self):
        r, _, first = self.run_attempt(campaign(hp=5), (1, 3, 4))
        path = Path('.artifacts/m2_2a_save.json')
        path.parent.mkdir(exist_ok=True)
        try:
            with patch('engine.traversal_resolution.die', side_effect=AssertionError('no restore draw')):
                save_game(r, str(path))
                loaded = load_game(str(path), campaign_draw=Dice())
                self.assertEqual(loaded.campaign, r.campaign)
                self.assertEqual(loaded.process_increment(command()).results, first.results)
                self.assertEqual(loaded.campaign, r.campaign)
        finally:
            path.unlink(missing_ok=True)

    def test_corrupt_or_unsupported_restoration_preserves_live_root(self):
        r, _, _ = self.run_attempt(campaign(hp=5), (1, 3, 4))
        root = r.campaign
        units = root.accepted
        variants = (replace(root, schema=99),
                    replace(root, current=replace(root.current, characters=(replace(root.current.characters[0], hit_points=1),))),
                    replace(root, accepted=(replace(units[0], result=replace(units[0].result, total=999)),)),
                    replace(root, accepted=(replace(units[0], consequence=None),)))
        for candidate in variants:
            with self.assertRaises((ValueError, Unresolved)):
                r.restore_domains(candidate)
            self.assertIs(r.campaign, root)
        encoded = export(root)
        for key, value in (('schema', 3), ('unknown', 1)):
            bad = copy.deepcopy(encoded)
            bad['domain_campaign']['fields'][key] = value
            with self.assertRaises((ValueError, Unresolved)):
                restore(bad)
        bad = copy.deepcopy(encoded)
        del bad['domain_campaign']['fields']['accepted']['tuple'][0]['fields']['consequence']
        with self.assertRaises(ValueError):
            restore(bad)
        self.assertIs(r.campaign, root)

    def test_real_old_schema_one_bytes_remain_valid(self):
        r = GameSession.start_domains(premises())
        self.assertEqual(r.process_increment(command()).status, 'accepted')
        encoded = export(r.campaign)
        def strip(value):
            if type(value) is dict:
                if value.get('record') in LEGACY_DEFAULTS:
                    for name in LEGACY_DEFAULTS[value['record']]:
                        value['fields'].pop(name, None)
                for child in value.values():
                    strip(child)
            elif type(value) is list:
                for child in value:
                    strip(child)
        strip(encoded)
        with patch('engine.traversal_resolution.die', side_effect=AssertionError('no old restore draw')):
            self.assertEqual(restore(json.loads(json.dumps(encoded))), r.campaign)
        # Schema 1 cannot be used to smuggle new consequential meaning.
        with self.assertRaises(ValueError):
            validate_campaign(replace(campaign(), schema=1))

    def test_published_codec_fixture_retains_legacy_sparse_zero_hp_meaning(self):
        path = Path('test_fixtures/physical_traversal_m2_1_schema1.json')
        with patch('engine.traversal_resolution.TraversalResolution.resolve', side_effect=AssertionError('no resolution')):
            r = load_game(str(path), campaign_draw=Dice())
            self.assertEqual(r.campaign.schema, 1)
            self.assertEqual(r.state.characters[0].hit_points, 0)
            self.assertEqual(len(r.campaign.accepted), 1)
            self.assertEqual(r.process_increment(command()).status, 'accepted')
        root = campaign(protected=True)
        self.assert_blocked(change(root, character=replace(root.origin.characters[0], hit_points=0,
            conditions=('unconscious', 'incapacitated', 'prone'))))

    def test_second_real_attempt_has_new_draws_and_survives_restoration(self):
        draw = Dice(1, 20)
        r = GameSession.start_domains(campaign(protected=True), draw=draw)
        self.assertEqual(r.process_increment(command()).status, 'accepted')
        self.assertEqual(r.process_increment(command(attempt='second')).status, 'accepted')
        self.assertEqual(draw.sides, [20, 20])
        self.assertEqual(r.state.characters[0].movement_spent, 30)
        with patch('engine.traversal_resolution.TraversalResolution.resolve', side_effect=AssertionError('no resolution')):
            restored = restore(export(r.campaign))
            self.assertEqual(restored, r.campaign)

    def test_current_root_guard_remains_last_publication_check(self):
        root = campaign()
        r = GameSession.start_domains(root, draw=Dice(1, 3, 4))
        p = r.prepare_increment(command())
        changed = change(root, world=replace(root.origin.world, at_seconds=18))
        original = validate_campaign
        def validation(candidate):
            r.campaign = changed
            return original(candidate)
        with patch('engine.historical_campaign.validate_campaign', side_effect=validation):
            with self.assertRaises(Unresolved):
                r.accept_increment(p)
        self.assertIs(r.campaign, changed)
        r.campaign = root
        with patch('engine.historical_campaign.validate_campaign', side_effect=validation):
            with self.assertRaises(Unresolved):
                r.restore_domains(root)
        self.assertIs(r.campaign, changed)

    def test_corrupted_new_schema_file_is_rejected_without_live_or_save_repair(self):
        r, _, _ = self.run_attempt(campaign(hp=5), (1, 3, 4))
        root = r.campaign
        path = Path('.artifacts/m2_2a_corrupt.json')
        try:
            data = export(root)
            data['domain_campaign']['fields']['current']['fields']['characters']['tuple'][0]['fields']['vitality']['fields']['dead'] = 'false'
            content = json.dumps(data)
            path.write_text(content, encoding='utf-8')
            with self.assertRaises(ValueError):
                load_game(str(path))
            self.assertIs(r.campaign, root)
            self.assertEqual(path.read_text(), content)
        finally:
            path.unlink(missing_ok=True)

    def test_save_failure_keeps_prior_bytes_and_live_state(self):
        r, _, _ = self.run_attempt(campaign(), (1, 3, 4))
        path = Path('.artifacts/m2_2a_atomic.json')
        try:
            path.write_text('prior valid bytes', encoding='utf-8')
            for operation in ('os.fsync', 'os.replace'):
                before = r.campaign
                with patch('engine.save_system.' + operation, side_effect=OSError('injected')):
                    with self.assertRaises(OSError):
                        save_game(r, str(path))
                self.assertEqual(path.read_text(), 'prior valid bytes')
                self.assertIs(r.campaign, before)
        finally:
            path.unlink(missing_ok=True)


class IndependentReviewCorrectionTests(unittest.TestCase):
    run_attempt = ConsequentialClimbingTests.run_attempt

    def collision_root(self, kind, identity):
        root = campaign()
        w = root.origin.world
        records = {
            'places': Place(identity, 'local'),
            'surfaces': Surface(identity, True, False, False, False, 'established'),
            'links': TraversalLink(identity, 'base', 'middle', 'surface', 5, False, 'established'),
            'objects': PhysicalObject(identity, 'ordinary-object', True),
            'history': CausalRecord(identity, 17, ('creature',), 'established'),
            'falls': FallOccurrence(identity, 'creature', 'base', 'end', 20, 'solid', 'past-event'),
            'climb_circumstances': ClimbCircumstances(identity, 'next', 'load_bearing', None,
                None, None, 'none', 'none', 'established'),
        }
        if kind == 'creatures':
            other = replace(root.origin.characters[0], id=identity)
            w = replace(w, creatures=w.creatures + (identity,), positions=w.positions + ((identity, 'end'),))
            d = replace(root.origin, world=w, characters=root.origin.characters + (other,))
            return replace(root, origin=d, current=d)
        return change(root, world=replace(w, **{kind: getattr(w, kind) + (records[kind],)}))

    def assert_collision_never_draws(self, identity):
        for kind in ('places', 'surfaces', 'links', 'objects', 'history', 'falls',
                     'climb_circumstances', 'creatures'):
            with self.subTest(kind=kind, identity=identity):
                draw = Dice(1, 3, 4, 20)
                r = GameSession.start_domains(self.collision_root(kind, identity), draw=draw)
                before = r.campaign
                # The original defect discarded failure then accepted success
                # under this same attempt identity. Neither call may draw now.
                for _ in range(2):
                    self.assertEqual(r.process_increment(command()).status, 'unresolved')
                    with self.assertRaises(Unresolved):
                        r.prepare_increment(command())
                    self.assertIs(r.campaign, before)
                self.assertEqual(draw.sides, [])

    def test_fall_identity_collision_rejects_every_world_record_kind_before_sampling(self):
        self.assert_collision_never_draws('attempt:one:fall')

    def test_causal_identity_collision_rejects_every_world_record_kind_before_sampling(self):
        self.assert_collision_never_draws('campaign:accepted:1')

    def test_unproposed_fall_identity_does_not_block_protected_failure(self):
        root = campaign(protected=True)
        w = root.origin.world
        root = change(root, world=replace(w, objects=w.objects + (
            PhysicalObject('attempt:one:fall', 'ordinary-object', True),)))
        r, draw, _ = self.run_attempt(root, (1,))
        self.assertEqual(draw.sides, [20])
        self.assertEqual(r.campaign.accepted[0].consequence.kind, 'grip_lost_protected')

    def contradictory_roots(self):
        root = campaign(protected=True)
        w = root.origin.world
        for edge in (PhysicalRelation('anchor', 'located', 'end', 'established'),
                     PhysicalRelation('anchor', 'secured', 'end', 'established'),
                     PhysicalRelation('harness', 'located', 'end', 'established')):
            yield change(root, world=replace(w, relationships=w.relationships + (edge,)))
        other = replace(root.origin.characters[0], id='other')
        w = replace(w, creatures=w.creatures + ('other',), positions=w.positions + (('other', 'end'),))
        for obj, kind in (('anchor', 'carried'), ('harness', 'held'), ('harness', 'attached')):
            bad_world = replace(w, relationships=w.relationships + (
                PhysicalRelation(obj, kind, 'other', 'established'),))
            d = replace(root.origin, world=bad_world, characters=root.origin.characters + (other,))
            yield replace(root, origin=d, current=d)

    def test_contradictory_protection_dispositions_reject_without_sampling(self):
        for root in self.contradictory_roots():
            draw = Dice()
            with self.assertRaises(ValueError):
                GameSession.start_domains(root, draw=draw)
            self.assertEqual(draw.sides, [])

    def test_contradictory_protection_rejects_restoration_without_adoption_or_draws(self):
        r = GameSession.start_domains(campaign(protected=True), draw=Dice())
        before = r.campaign
        accepted, _, _ = self.run_attempt(campaign(protected=True), (1,))
        with patch('engine.traversal_resolution.die', side_effect=AssertionError('restore must not draw')):
            for root in self.contradictory_roots():
                with self.assertRaises(ValueError):
                    restore({'save_version': 3, 'domain_campaign': pack(root)})
                with self.assertRaises(ValueError):
                    r.restore_domains(root)
                self.assertIs(r.campaign, before)
            # Also reject a forged accepted history with the same conflicting
            # fact consistently inserted into both historical and current World.
            root = accepted.campaign
            edge = PhysicalRelation('anchor', 'located', 'end', 'established')
            origin = replace(root.origin, world=replace(root.origin.world,
                relationships=root.origin.world.relationships + (edge,)))
            current = replace(root.current, world=replace(root.current.world,
                relationships=root.current.world.relationships + (edge,)))
            bad = replace(root, origin=origin, current=current)
            with self.assertRaises(ValueError):
                restore({'save_version': 3, 'domain_campaign': pack(bad)})
            self.assertIs(r.campaign, before)

    def test_coherent_locations_and_extended_rope_connections_survive_both_results(self):
        root = campaign(protected=True)
        w = root.origin.world
        extra = (PhysicalRelation('anchor', 'located', 'base', 'established'),
                 PhysicalRelation('harness', 'located', 'base', 'established'),
                 PhysicalRelation('rope', 'secured', 'end', 'extended rope connection'))
        root = change(root, world=replace(w, relationships=w.relationships + extra))
        for roll, position in ((1, 'base'), (20, 'middle')):
            r, draw, decision = self.run_attempt(root, (roll,))
            edges = {(e.object, e.kind, e.target) for e in r.state.world.relationships}
            self.assertIn(('anchor', 'located', 'base'), edges)
            self.assertIn(('harness', 'located', position), edges)
            self.assertIn(('harness', 'attached', 'creature'), edges)
            self.assertIn(('rope', 'secured', 'end'), edges)
            with patch('engine.traversal_resolution.die', side_effect=AssertionError('no repeat draw')):
                self.assertEqual(restore(export(r.campaign)), r.campaign)
                self.assertEqual(r.process_increment(command()).results, decision.results)
            self.assertEqual(draw.sides, [20])

    def test_protection_with_unsupported_success_branch_blocks_before_sampling(self):
        root = campaign(protected=True)
        w = root.origin.world
        # Holding a fixed anchor is coherent here, but moving while retaining
        # that point-object hold needs a release/handling effect not implemented.
        root = change(root, world=replace(w, relationships=w.relationships + (
            PhysicalRelation('anchor', 'held', 'creature', 'established'),)))
        draw = Dice()
        r = GameSession.start_domains(root, draw=draw)
        before = r.campaign
        self.assertEqual(r.process_increment(command()).status, 'unresolved')
        self.assertIs(r.campaign, before)
        self.assertEqual(draw.sides, [])

    def test_ordinary_schema_two_climbing_needs_no_protection_or_equipment_model(self):
        root = premises()
        w = replace(root.origin.world, objects=(), relationships=())
        c = replace(root.origin.characters[0], ready_equipment=())
        d = replace(root.origin, world=w, characters=(c,))
        root = replace(root, origin=d, current=d, schema=2)
        cmd = command()
        cmd = replace(cmd, request=replace(cmd.request, means=()))
        draw = Dice()
        r = GameSession.start_domains(root, draw=draw)
        self.assertEqual(r.process_increment(cmd).status, 'accepted')
        self.assertEqual(draw.sides, [])
        self.assertEqual(r.state.world.objects, ())
        self.assertEqual(r.state.world.climb_circumstances, ())

    def test_supported_uncertainty_does_not_require_equipment(self):
        root = campaign(footing='load_bearing', height=0)
        root = change(root, world=replace(root.origin.world, objects=(), relationships=()),
                      character=replace(root.origin.characters[0], ready_equipment=()))
        cmd = command()
        cmd = replace(cmd, request=replace(cmd.request, means=()))
        draw = Dice(1)
        r = GameSession.start_domains(root, draw=draw)
        self.assertEqual(r.process_increment(cmd).status, 'accepted')
        self.assertEqual(r.campaign.accepted[0].consequence.kind, 'supported_no_progress')
        self.assertEqual(draw.sides, [20])

    def test_damage_at_zero_uses_damage_taken_despite_temporary_hp(self):
        c = campaign().origin.characters[0]
        for temporary in (0, 9, 10, 100):
            for stable, successes, failures in ((True, 0, 0), (False, 2, 0), (False, 1, 2)):
                for damage in (0, 1, 9, 10, 11):
                    with self.subTest(temporary=temporary, stable=stable, failures=failures, damage=damage):
                        before = replace(c, hit_points=0, conditions=('unconscious', 'incapacitated', 'prone'),
                            vitality=Vitality(10, temporary_hp=temporary, stable=stable,
                                              death_successes=successes, death_failures=failures))
                        out = CharacterRules('zero-boundary', (before,)).apply_fall_damage(c.id, damage)
                        expected_failures = failures + int(damage > 0)
                        self.assertEqual(out.hit_points, 0)
                        self.assertEqual(out.vitality.temporary_hp, max(0, temporary - damage))
                        self.assertEqual(out.vitality.death_failures, expected_failures)
                        self.assertEqual(out.vitality.death_successes, successes)
                        self.assertEqual(out.vitality.dead, damage > 0 and (damage >= 10 or expected_failures == 3))
                        self.assertEqual(out.vitality.stable, stable and damage == 0)
                        self.assertTrue({'unconscious', 'incapacitated', 'prone'}.issubset(out.conditions))
                        self.assertEqual(before.vitality.temporary_hp, temporary)

    def test_positive_hp_damage_keeps_temporary_absorption_and_overflow_semantics(self):
        c = campaign(hp=5, maximum=10).origin.characters[0]
        for temporary in (0, 4, 10):
            for damage in (0, 4, 5, 9, 14, 15, 19, 25):
                with self.subTest(temporary=temporary, damage=damage):
                    before = replace(c, vitality=Vitality(10, temporary_hp=temporary))
                    out = CharacterRules('positive-boundary', (before,)).apply_fall_damage(c.id, damage)
                    remaining = max(0, damage - temporary)
                    self.assertEqual(out.hit_points, max(0, 5 - remaining))
                    self.assertEqual(out.vitality.temporary_hp, max(0, temporary - damage))
                    self.assertEqual(out.vitality.dead, remaining - 5 >= 10)
                    self.assertEqual((out.vitality.death_successes, out.vitality.death_failures), (0, 0))
                    self.assertEqual('prone' in out.conditions, damage > 0)
                    self.assertEqual('unconscious' in out.conditions, remaining >= 5 and remaining < 15)


if __name__ == '__main__':
    with patch.object(socket.socket, 'connect', side_effect=AssertionError('offline tests')):
        unittest.main()
