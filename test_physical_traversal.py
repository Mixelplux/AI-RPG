"""Offline M1 contract tests through owning domains and the common coordinator."""
import unittest
from dataclasses import replace

from engine.character_rules import CharacterRules, CreatureRules, StrengthTrait
from engine.gameplay_coordination import Coordinator, Interpretation, SituatedContext, Target
from engine.information_adjudication import Unresolved
from engine.physical_world import (
    CausalRecord, FallOccurrence, PhysicalFrame, PhysicalObject, PhysicalRelation,
    Place, Surface, TraversalLink, WorldPhysics,
)
from engine.traversal_coordination import TraversalDomain
from engine.traversal_resolution import ClimbRequest, ClimbRuling, TraversalResolution


def premises(actor='pc', locality='courtyard', route='wall'):
    # Only owner premises, never a preselected resolution, die or consequence.
    frame = PhysicalFrame('w1', 40,
        (Place('bottom', locality), Place('top', locality)), (actor,), ((actor, 'bottom'),),
        (Surface('stone', True, False, False, False, 'authored:stone'),),
        (TraversalLink(route, 'bottom', 'top', 'stone', 10, False, 'authored:wall'),))
    profile = CreatureRules(actor, 30, 0, 14, 2, 1, known_routes=(route,), hit_points=20, movement_spent=0)
    return frame, profile


class TraversalTests(unittest.TestCase):
    def setUp(self):
        self.frame, self.profile = premises()
        self.character_revision = 'c1'
        self.resolution = TraversalResolution(
            lambda: WorldPhysics(self.frame),
            lambda: CharacterRules(self.character_revision, (self.profile,)))
        self.request = ClimbRequest('attempt1', 'pc', 'wall', 10)
        self.ruling = ClimbRuling(False, 'ordinary:stable-handholds')

    def surface(self, **values):
        self.frame = replace(self.frame, surfaces=(replace(self.frame.surfaces[0], **values),))

    def assess(self, **values):
        return self.resolution.assess(replace(self.request, **values), self.ruling)

    def no_draw(self, sides):
        self.fail('deterministic or unresolved action must not roll')

    def dice(self, *values):
        draws = iter(values)
        def draw(sides):
            value = next(draws)
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, sides)
            return value
        return draw

    def difficult(self):
        self.surface(slippery=True)
        self.ruling = ClimbRuling(True, 'context:slippery-grip-uncertainty')

    def test_ordinary_climb_without_check(self):
        a = self.assess()
        self.assertEqual((a.status, a.movement_cost), ('deterministic', 20))
        result = self.resolution.resolve(a, self.no_draw)
        self.assertTrue(result.success)
        self.assertEqual(result.destination, 'top')
        self.assertEqual(result.rolls, ())

    def test_difficult_terrain_and_special_speed(self):
        self.surface(difficult=True)
        self.assertEqual(self.assess().movement_cost, 30)
        self.profile = replace(self.profile, climb_speed=20)
        special = self.assess(use_climb_speed=True)
        self.assertEqual((special.movement_cost, special.status), (20, 'deterministic'))
        self.surface(difficult=False)
        self.assertEqual(self.assess(use_climb_speed=True).movement_cost, 10)

    def test_selected_speed_and_prior_movement(self):
        self.profile = replace(self.profile, climb_speed=15, movement_spent=10)
        self.assertEqual(self.assess(use_climb_speed=True).status, 'unavailable')
        self.assertEqual(self.assess().status, 'deterministic')

    def test_absent_climb_speed_is_not_manufactured(self):
        self.assertEqual(self.assess(use_climb_speed=True).status, 'unavailable')

    def test_slippery_does_not_force_optional_dm_check(self):
        self.surface(slippery=True)
        self.assertTrue(self.resolution.resolve(self.assess(), self.no_draw).success)

    def test_unjustified_check_is_rejected(self):
        self.ruling = ClimbRuling(True, 'unjustified')
        with self.assertRaises(Unresolved):
            self.assess()

    def test_sparse_handholds_justify_check(self):
        self.surface(few_handholds=True)
        self.ruling = ClimbRuling(True, 'context:sparse')
        self.assertEqual(self.assess().dc, 15)

    def test_strength_athletics_and_training_change_result(self):
        self.difficult()
        trained = self.resolution.resolve(self.assess(), self.dice(11))
        self.assertEqual((trained.total, trained.success), (15, True))
        self.profile = replace(self.profile, athletics_rank=0)
        self.assertFalse(self.resolution.resolve(self.assess(), self.dice(11)).success)
        self.profile = replace(self.profile, strength=18)
        self.assertTrue(self.resolution.resolve(self.assess(), self.dice(11)).success)

    def test_expertise_does_not_stack_twice(self):
        self.difficult()
        self.profile = replace(self.profile, athletics_rank=2)
        self.assertEqual(self.resolution.resolve(self.assess(), self.dice(9)).total, 15)

    def test_climb_speed_does_not_waive_check(self):
        self.difficult()
        self.profile = replace(self.profile, climb_speed=30)
        result = self.resolution.resolve(self.assess(use_climb_speed=True), self.dice(2))
        self.assertFalse(result.success)

    def test_poison_disadvantage_and_trait_cancellation(self):
        self.difficult()
        self.profile = replace(self.profile, conditions=('poisoned',))
        self.assertFalse(self.resolution.resolve(self.assess(), self.dice(19, 2)).success)
        self.profile = replace(self.profile, traits=(StrengthTrait('feature:strength-advantage', True),))
        result = self.resolution.resolve(self.assess(), self.dice(11))
        self.assertEqual((result.rolls, result.success), ((11,), True))

    def test_multiple_advantage_sources_still_use_two_dice(self):
        self.difficult()
        self.profile = replace(self.profile, traits=(StrengthTrait('feature:a', True), StrengthTrait('feature:b', True)))
        self.assertTrue(self.resolution.resolve(self.assess(), self.dice(2, 11)).success)

    def test_exhaustion_changes_speed_and_check(self):
        self.difficult()
        self.profile = replace(self.profile, exhaustion=1, climb_speed=30)
        a = self.assess(use_climb_speed=True)
        self.assertEqual((a.speed, a.modifier), (25, 2))
        self.assertFalse(self.resolution.resolve(a, self.dice(12)).success)
        self.profile = replace(self.profile, exhaustion=6)
        self.assertEqual(self.assess().status, 'unavailable')

    def test_immobilizing_conditions_apply_to_both_speeds(self):
        for condition in ('grappled', 'restrained', 'paralyzed', 'unconscious'):
            with self.subTest(condition=condition):
                self.profile = replace(self.profile, climb_speed=40, conditions=(condition,))
                capability = self.resolution.characters().physical_capability('pc')
                self.assertEqual((capability.speed, capability.climb_speed), (0, 0))
                for special in (False, True):
                    a = self.assess(use_climb_speed=special)
                    self.assertEqual((a.status, a.reason, a.speed), ('unavailable', 'movement_unavailable', 0))

    def test_stunned_preserves_allowance_but_restricts_general_coordination_and_economy(self):
        self.profile = replace(self.profile, climb_speed=40, conditions=('stunned',))
        capability = self.resolution.characters().physical_capability('pc')
        self.assertEqual((capability.speed, capability.climb_speed), (30, 40))
        self.assertFalse(capability.coordinated_movement)
        self.assertEqual((capability.actions, capability.bonus_actions, capability.reactions), (False, False, False))
        # This is a reusable Character capability query, independent of climbing,
        # Athletics, a target, or a die. Basic movement allowance remains positive.
        sparse = replace(self.profile, strength=None, proficiency_bonus=None, athletics_rank=None)
        self.assertEqual(CharacterRules('sparse', (sparse,)).physical_capability('pc'), capability)

    def test_stunned_blocks_coordinated_climbing_even_without_a_check(self):
        self.profile = replace(self.profile, climb_speed=40, conditions=('stunned',))
        before = self.frame, self.profile
        for check in (False, True):
            self.surface(slippery=check)
            self.ruling = ClimbRuling(check, 'context:physical-grip')
            for special, speed in ((False, 30), (True, 40)):
                with self.subTest(check=check, special=special):
                    a = self.assess(use_climb_speed=special)
                    self.assertEqual((a.status, a.reason, a.speed),
                                     ('unavailable', 'coordinated_movement_unavailable', speed))
                    with self.assertRaises(Unresolved):
                        self.resolution.resolve(a, self.no_draw)
        self.assertEqual(self.frame.falls, before[0].falls)
        self.assertEqual(self.profile, before[1])

    def test_stunned_does_not_replace_other_speed_reductions(self):
        self.profile = replace(self.profile, climb_speed=40, exhaustion=1, conditions=('stunned',))
        a = self.assess()
        self.assertEqual((a.speed, a.reason), (25, 'coordinated_movement_unavailable'))
        self.profile = replace(self.profile, conditions=('stunned', 'grappled'))
        a = self.assess()
        self.assertEqual((a.speed, a.reason), (0, 'movement_unavailable'))

    def test_becoming_stunned_invalidates_climb_without_creating_a_fall(self):
        a = self.assess()
        before = self.frame
        self.profile = replace(self.profile, conditions=('stunned',))
        with self.assertRaises(Unresolved) as caught:
            self.resolution.resolve(a, self.no_draw)
        self.assertEqual(caught.exception.reason, 'stale_traversal_assessment')
        self.assertEqual(self.frame, before)
        self.assertEqual(self.assess().reason, 'coordinated_movement_unavailable')

    def test_unsupported_conditions_are_not_ignored(self):
        self.profile = replace(self.profile, conditions=('frightened',))
        with self.assertRaises(Unresolved):
            self.assess()

    def test_incapacitated_alone_does_not_invent_a_movement_prohibition(self):
        self.profile = replace(self.profile, conditions=('incapacitated',))
        capability = self.resolution.characters().physical_capability('pc')
        self.assertEqual((capability.speed, capability.coordinated_movement), (30, True))
        self.assertEqual((capability.actions, capability.bonus_actions, capability.reactions), (False, False, False))
        self.assertEqual(self.assess().status, 'deterministic')

    def test_no_natural_one_or_twenty_ability_check_override(self):
        self.difficult()
        self.profile = replace(self.profile, strength=30, proficiency_bonus=6, athletics_rank=2)
        self.assertTrue(self.resolution.resolve(self.assess(), self.dice(1)).success)
        self.profile = replace(self.profile, strength=1, athletics_rank=0, exhaustion=5)
        a = self.assess(distance_feet=1)
        self.assertFalse(self.resolution.resolve(a, self.dice(20)).success)

    def test_failed_objective_does_not_assert_fall_injury_or_safe_position(self):
        self.difficult()
        before = self.frame, self.profile
        result = self.resolution.resolve(self.assess(), self.dice(1))
        self.assertEqual((result.success, result.destination, result.disposition),
                         (False, None, 'objective_not_achieved'))
        self.assertEqual((self.frame, self.profile), before)
        self.assertEqual(self.frame.falls, ())

    def test_partial_extent_is_not_destination_arrival(self):
        result = self.resolution.resolve(self.assess(distance_feet=5), self.no_draw)
        self.assertTrue(result.success)
        self.assertIsNone(result.destination)

    def test_physical_changes_alter_applicability(self):
        for values in ({'climbable': False},):
            self.surface(**values)
            self.assertEqual(self.assess().status, 'unavailable')
        self.surface(climbable=True)
        self.frame = replace(self.frame, links=(replace(self.frame.links[0], blocked=True),))
        self.assertEqual(self.assess().status, 'unavailable')

    def test_missing_material_world_facts_fail_closed(self):
        for key in ('climbable', 'slippery', 'few_handholds', 'difficult'):
            with self.subTest(key=key):
                self.frame, _ = premises()
                self.surface(**{key: None})
                with self.assertRaises(Unresolved):
                    self.assess()

    def test_missing_character_facts_fail_closed(self):
        self.difficult()
        original = self.profile
        for key in ('speed', 'strength', 'proficiency_bonus', 'athletics_rank', 'movement_spent'):
            with self.subTest(key=key):
                self.profile = replace(original, **{key: None})
                with self.assertRaises(Unresolved):
                    self.assess()

    def test_material_hidden_binding_cannot_be_silently_omitted(self):
        self.surface(unresolved_bindings=('hidden:ward',))
        with self.assertRaises(Unresolved):
            self.assess()
        result = self.coordinator().process(interpretation=Interpretation('climb', 'reach top', 'wall'))
        self.assertEqual(result.status, 'unresolved')
        self.assertNotIn('ward', result.message)

    def test_unsupported_creature_effect_blocks_climb_and_fall(self):
        self.profile = replace(self.profile, unresolved_rules=('effect:unknown',))
        with self.assertRaises(Unresolved):
            self.assess()
        self.fall()
        with self.assertRaises(Unresolved):
            self.resolution.resolve_fall('fall:1', self.no_draw)

    def test_relationship_change_invalidates_prepared_means(self):
        self.gear()
        a = self.assess(means=('rope:1',))
        self.frame = replace(self.frame, relationships=tuple(e for e in self.frame.relationships if e.kind != 'secured'))
        with self.assertRaises(Unresolved):
            self.resolution.resolve(a, self.no_draw)

    def test_stale_world_or_character_rejected_before_draw(self):
        for change in ('surface', 'character', 'time'):
            with self.subTest(change=change):
                self.frame, self.profile = premises()
                a = self.assess()
                if change == 'surface':
                    self.surface(difficult=True)
                elif change == 'character':
                    self.profile = replace(self.profile, movement_spent=16)
                else:
                    self.frame = replace(self.frame, at_seconds=41)
                with self.assertRaises(Unresolved):
                    self.resolution.resolve(a, self.no_draw)

    def test_state_change_during_sampling_is_contained(self):
        self.difficult()
        a = self.assess()
        def changed(sides):
            self.profile = replace(self.profile, strength=16)
            return 20
        with self.assertRaises(Unresolved):
            self.resolution.resolve(a, changed)

    def test_invalid_die_is_technical_not_failure(self):
        self.difficult()
        for value in (0, 21, True, '15'):
            with self.subTest(value=value), self.assertRaises(Unresolved):
                self.resolution.resolve(self.assess(), lambda sides: value)

    def test_untrusted_assessment_cannot_change_rule_or_cost(self):
        self.difficult()
        a = self.assess()
        for forged in (replace(a, dc=1), replace(a, movement_cost=0), replace(a, status='deterministic')):
            with self.subTest(forged=forged), self.assertRaises(Unresolved):
                self.resolution.resolve(forged, self.no_draw)

    def test_existing_codec_cannot_publish_provisional_traversal_as_campaign_truth(self):
        from engine.campaign_records import pack, unpack
        for value in (self.frame, self.profile, self.resolution.characters().physical_capability('pc'), self.assess(),
                      self.resolution.resolve(self.assess(), self.no_draw)):
            with self.subTest(value=type(value).__name__), self.assertRaises(ValueError):
                pack(value)
        with self.assertRaises(ValueError):
            unpack({'record': 'ClimbResult', 'fields': {}})

    def test_different_actor_place_and_route_use_same_rules(self):
        for actor, locality, route in (('npc:porter', 'quarry', 'face'), ('pc:second', 'ruins', 'stairwall')):
            with self.subTest(actor=actor):
                self.frame, self.profile = premises(actor, locality, route)
                self.request = ClimbRequest('new-attempt', actor, route, 10)
                result = self.resolution.resolve(self.assess(), self.no_draw)
                self.assertEqual((result.success, result.assessment.movement_cost), (True, 20))

    def gear(self):
        self.frame = replace(self.frame, objects=(PhysicalObject('rope:1', 'hemp-rope', True),
            PhysicalObject('harness:1', 'harness', True)), relationships=(
                PhysicalRelation('rope:1', 'held', 'pc', 'handling'),
                PhysicalRelation('rope:1', 'secured', 'top', 'accepted-knot'),
                PhysicalRelation('rope:1', 'attached', 'harness:1', 'accepted-attachment')))
        self.profile = replace(self.profile, ready_equipment=('rope:1',))

    def test_rope_preserves_identity_and_multiple_relationships(self):
        self.gear()
        a = self.assess(means=('rope:1',))
        obj, relations = a.dependencies.equipment[0]
        self.assertEqual(obj.id, 'rope:1')
        self.assertEqual({r.kind for r in relations}, {'held', 'secured', 'attached'})
        # Dropping handling cannot erase established attachments or retain use.
        self.frame = replace(self.frame, relationships=tuple(e for e in self.frame.relationships if e.kind != 'held'))
        WorldPhysics(self.frame)
        self.assertEqual(len(self.frame.relationships), 2)
        with self.assertRaises(Unresolved):
            self.assess(means=('rope:1',))

    def test_readiness_cannot_manufacture_object(self):
        self.profile = replace(self.profile, ready_equipment=('imaginary-rope',))
        with self.assertRaises(Unresolved):
            self.assess(means=('imaginary-rope',))

    def test_physical_possession_cannot_manufacture_readiness(self):
        self.gear()
        self.profile = replace(self.profile, ready_equipment=())
        with self.assertRaises(Unresolved):
            self.assess(means=('rope:1',))

    def test_damaged_equipment_and_stale_inventory_cannot_be_used(self):
        self.gear()
        self.frame = replace(self.frame, objects=(replace(self.frame.objects[0], intact=False), self.frame.objects[1]))
        with self.assertRaises(Unresolved):
            self.assess(means=('rope:1',))

    def test_exclusive_holding_conflict_rejected(self):
        self.gear()
        self.frame = replace(self.frame, creatures=('pc', 'npc'), relationships=self.frame.relationships +
            (PhysicalRelation('rope:1', 'held', 'npc', 'conflict'),))
        with self.assertRaises(ValueError):
            WorldPhysics(self.frame)

    def test_dangling_relationship_and_duplicate_identity_rejected(self):
        self.gear()
        with self.assertRaises(ValueError):
            WorldPhysics(replace(self.frame, relationships=(PhysicalRelation('rope:1', 'attached', 'missing', 'bad'),)))
        with self.assertRaises(ValueError):
            WorldPhysics(replace(self.frame, objects=self.frame.objects + (self.frame.objects[0],)))

    def test_physical_position_and_causal_history_are_world_owned(self):
        self.frame = replace(self.frame, history=(CausalRecord('setup:1', 39, ('pc', 'wall'), 'authorized-approach'),))
        WorldPhysics(self.frame)
        self.assertFalse(hasattr(self.profile, 'position'))
        with self.assertRaises(ValueError):
            WorldPhysics(replace(self.frame, positions=(('pc', 'bottom'), ('pc', 'top'))))
        with self.assertRaises(ValueError):
            WorldPhysics(replace(self.frame, history=(CausalRecord('future', 41, ('pc',), 'bad'),)))

    def fall(self, distance=25, medium='solid'):
        self.frame = replace(self.frame, falls=(FallOccurrence('fall:1', 'pc', 'top', 'bottom', distance,
                                                           medium, 'world:actual-loss-of-support'),))

    def test_genuine_fall_has_separate_damage_rule(self):
        self.fall()
        result = self.resolution.resolve_fall('fall:1', self.dice(3, 4))
        self.assertEqual((result.bludgeoning_damage, result.prone, result.landing), (7, True, 'bottom'))
        self.assertEqual(self.profile.hit_points, 20)
        self.assertEqual(dict(self.frame.positions)['pc'], 'bottom')

    def test_fall_rejects_changed_world_for_reused_and_replaced_supplier_instances(self):
        for reused in (True, False):
            with self.subTest(reused=reused):
                frame, profile = premises()
                frame = replace(frame, falls=(FallOccurrence('fall:1', 'pc', 'top', 'bottom', 20,
                                                             'solid', 'world:loss-of-support'),))
                worlds = [WorldPhysics(frame)]
                characters = CharacterRules('c1', (profile,))
                resolution = TraversalResolution(lambda: worlds[0], lambda: characters)
                draws = []
                def changed(sides):
                    draws.append(sides)
                    if len(draws) == 1:
                        updated = replace(frame, revision='w2', falls=(replace(frame.falls[0], distance_feet=100),))
                        validated = WorldPhysics(updated)
                        if reused:
                            worlds[0].frame = validated.frame
                        else:
                            worlds[0] = validated
                    return 3
                with self.assertRaises(Unresolved) as caught:
                    resolution.resolve_fall('fall:1', changed)
                self.assertEqual((caught.exception.stage, caught.exception.reason),
                                 ('validation', 'stale_fall_assessment'))
                self.assertEqual(draws, [6, 6])
                self.assertEqual((worlds[0].frame.revision, worlds[0].frame.falls[0].distance_feet), ('w2', 100))
                self.assertEqual(characters.creature('pc').hit_points, 20)

    def test_fall_rejects_revision_change_on_reused_character_supplier(self):
        self.fall(20)
        world = WorldPhysics(self.frame)
        characters = CharacterRules('c1', (self.profile,))
        resolution = TraversalResolution(lambda: world, lambda: characters)
        def changed(sides):
            characters.revision = 'c2'
            return 3
        with self.assertRaises(Unresolved) as caught:
            resolution.resolve_fall('fall:1', changed)
        self.assertEqual(caught.exception.reason, 'stale_fall_assessment')

    def test_unchanged_reused_fall_suppliers_remain_valid(self):
        self.fall(20)
        world = WorldPhysics(self.frame)
        characters = CharacterRules('c1', (self.profile,))
        resolution = TraversalResolution(lambda: world, lambda: characters)
        result = resolution.resolve_fall('fall:1', self.dice(3, 4))
        self.assertEqual((result.rolls, result.bludgeoning_damage), ((3, 4), 7))

    def test_failed_progress_does_not_prevent_a_later_world_established_fall(self):
        self.frame = replace(self.frame, places=self.frame.places + (Place('ledge', 'courtyard'),),
            positions=(('pc', 'top'),),
            links=(replace(self.frame.links[0], origin='top', destination='ledge'),))
        self.difficult()
        before = self.frame
        failed = self.resolution.resolve(self.assess(), self.dice(1))
        self.assertEqual((failed.success, failed.destination, failed.disposition),
                         (False, None, 'objective_not_achieved'))
        self.assertEqual(self.frame, before)
        # Explicit missing-M2 supplier boundary: World has independently established
        # loss of grip and an actual fall; M1 does not infer it from the failed die.
        self.fall(20)
        result = self.resolution.resolve_fall('fall:1', self.dice(3, 4))
        self.assertEqual((result.bludgeoning_damage, result.prone), (7, True))
        self.assertEqual(self.frame.relationships, before.relationships)
        self.assertEqual(self.profile.hit_points, 20)  # no consequential publication

    def test_short_fall_and_damage_cap(self):
        self.fall(9)
        result = self.resolution.resolve_fall('fall:1', self.no_draw)
        self.assertEqual((result.bludgeoning_damage, result.prone), (0, False))
        self.fall(1000)
        result = self.resolution.resolve_fall('fall:1', self.dice(*([6] * 20)))
        self.assertEqual((len(result.rolls), result.bludgeoning_damage), (20, 120))

    def test_unestablished_or_unsupported_fall_is_unresolved(self):
        with self.assertRaises(Unresolved):
            self.resolution.resolve_fall('not-a-fall', self.no_draw)
        self.fall(medium='liquid')
        with self.assertRaises(Unresolved):
            self.resolution.resolve_fall('fall:1', self.no_draw)
        self.fall(distance=None)
        with self.assertRaises(Unresolved):
            self.resolution.resolve_fall('fall:1', self.no_draw)

    def coordinator(self):
        domain = TraversalDomain(self.resolution, self.request, self.ruling)
        def context():
            return SituatedContext(f'{self.frame.revision}:{self.character_revision}', 'bottom',
                (Target('wall', ('wall',), 'climb', ('climb',), 'climb'),))
        return Coordinator(context, domain)

    def test_common_coordinator_assesses_inquiry_without_execution_or_disclosure(self):
        self.difficult()
        before = self.frame, self.profile
        decision = self.coordinator().process(interpretation=Interpretation('climb', 'reach top', 'wall', intent='inquiry'))
        self.assertEqual(decision.status, 'inquiry')
        self.assertEqual((self.frame, self.profile), before)
        self.assertNotIn('slippery', decision.message)
        self.assertNotIn(self.ruling.basis, decision.message)
        self.assertEqual(set(decision.responsibilities), {'world_simulation', 'character_system', 'action_resolution'})

    def test_common_coordinator_requires_legitimate_access(self):
        self.profile = replace(self.profile, known_routes=())
        result = self.coordinator().process(interpretation=Interpretation('climb', 'reach top', 'wall'))
        self.assertEqual(result.status, 'unresolved')

    def test_common_coordinator_respects_constraints_and_missing_means(self):
        result = self.coordinator().process(interpretation=Interpretation('climb', 'reach top', 'wall', constraints=('quiet',)))
        self.assertEqual(result.status, 'unresolved')
        self.request = replace(self.request, means=('rope:1',))
        self.assertEqual(self.coordinator().process(interpretation=Interpretation('climb', 'reach top', 'wall')).status,
                         'unresolved')

    def test_common_execution_cannot_publish_before_m2(self):
        before = self.frame, self.profile
        result = self.coordinator().process(interpretation=Interpretation('climb', 'reach top', 'wall'))
        self.assertEqual(result.status, 'unresolved')
        self.assertEqual((self.frame, self.profile), before)

    def test_common_coordinator_rejects_changed_premises(self):
        coordinator = self.coordinator()
        decision = coordinator.decide(interpretation=Interpretation('climb', 'reach top', 'wall'))
        self.assertEqual(decision.status, 'proceed')
        self.frame = replace(self.frame, revision='w2')
        self.assertEqual(coordinator.execute(decision).status, 'unresolved')


if __name__ == '__main__':
    unittest.main()
