"""Offline integration at the production acceptance/save boundaries, no scenario answers."""
import json
import socket
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment
from engine.character_rules import CreatureRules
from engine.domain_campaign import ActivityScope, Campaign, Domains, Increment, validate_campaign
from engine.domain_persistence import export, pack, restore
from engine.game_session import GameSession
from engine.information_adjudication import Unresolved
from engine.physical_world import PhysicalFrame, PhysicalObject, PhysicalRelation, Place, Surface, TraversalLink
from engine.save_system import build_save_data, save_game, load_game
from engine.traversal_resolution import ClimbRequest, ClimbRuling


def premises(*, distance=5, difficult=False, climb_speed=0, speed=60, actor='creature', locality='local'):
    world = PhysicalFrame('world:initial', 17,
        tuple(Place(p, locality) for p in ('base', 'middle', 'end')), (actor,), ((actor, 'base'),),
        (Surface('surface', True, False, False, difficult, 'hidden:material-basis'),),
        (TraversalLink('first', 'base', 'middle', 'surface', distance, False, 'authored:relation'),
         TraversalLink('next', 'middle', 'end', 'surface', distance, False, 'authored:relation'),
         TraversalLink('return', 'middle', 'base', 'surface', distance, False, 'authored:relation')),
        (PhysicalObject('rope', 'rope-definition', True), PhysicalObject('anchor', 'anchor-definition', True)),
        (PhysicalRelation('rope', 'carried', actor, 'established'),
         PhysicalRelation('rope', 'attached', 'anchor', 'established'),
         PhysicalRelation('anchor', 'located', 'base', 'established')))
    character = CreatureRules(actor, speed, climb_speed, None, None, None,
        known_routes=('first', 'next', 'return'), ready_equipment=('rope',), movement_spent=0)
    domains = Domains(world, 'character:initial', (character,))
    scopes = tuple(ActivityScope('activity:' + route, actor, route,
        ActivityAuthorization('activity:' + route, 'climb'), ActivityCheckpoint('activity:' + route, 'climb'),
        11, 'World contextual duration for this increment', ClimbRuling(False, 'stable ordinary climb'))
        for route in ('first', 'next', 'return'))
    return Campaign('campaign', actor, domains, domains, scopes)


def command(route='first', attempt='attempt:one', *, distance=5, climb=False, actor='creature'):
    return Increment('activity:' + route, ClimbRequest(attempt, actor, route, distance, climb, ('rope',)))


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.runtime = GameSession.start_domains(premises())
        self.command = command()
        self.root = self.runtime.campaign

    def test_real_world_character_and_attempt_publish_together(self):
        result = self.runtime.process_increment(self.command)
        self.assertEqual(result.status, 'accepted')
        current = self.runtime.state
        self.assertEqual(dict(current.world.positions)['creature'], 'middle')
        self.assertEqual(current.world.at_seconds, 28)
        self.assertEqual(current.characters[0].movement_spent, 10)
        self.assertEqual(self.runtime.campaign.revision, 1)
        self.assertEqual(current.world.history[-1].cause, self.command.request.attempt)
        self.assertEqual(current.world.objects, self.root.current.world.objects)
        self.assertEqual(current.world.relationships, self.root.current.world.relationships)
        self.assertNotIn('hidden', result.message)
        self.assertNotIn('material-basis', result.message)

    def test_rejected_proposal_does_not_publish_anything(self):
        proposal = self.runtime.prepare_increment(self.command)
        variants = (
            replace(proposal.unit, duration_seconds=99),
            replace(proposal.unit, result=replace(proposal.unit.result, success=False)),
            replace(proposal.unit, result=replace(proposal.unit.result,
                assessment=replace(proposal.unit.result.assessment, movement_cost=0))),
            replace(proposal.unit, result=replace(proposal.unit.result, destination='end')),
            replace(proposal.unit, result=replace(proposal.unit.result, success=1)),
        )
        for unit in variants:
            with self.subTest(unit=unit):
                with self.assertRaises((ValueError, Unresolved)):
                    self.runtime.accept_increment(replace(proposal, unit=unit))
                self.assertIs(self.runtime.campaign, self.root)

    def test_malformed_receipt_prevents_publication(self):
        proposal = self.runtime.prepare_increment(self.command)
        for receipt in (None, replace(proposal.unit.receipt, ref='wrong'),
                        replace(proposal.unit.receipt, accessible=(('movement', 'hidden:material-basis'),)),
                        replace(proposal.unit.receipt, public_refs=('secret',))):
            with self.assertRaises((ValueError, Unresolved)):
                self.runtime.accept_increment(replace(proposal, unit=replace(proposal.unit, receipt=receipt)))
            self.assertIs(self.runtime.campaign, self.root)

    def test_malformed_receipt_through_coordinator_has_no_effects(self):
        proposal = self.runtime.prepare_increment(self.command)
        bad = replace(proposal, unit=replace(proposal.unit, receipt=replace(proposal.unit.receipt, ref='bad')))
        with patch.object(self.runtime, 'prepare_increment', return_value=bad):
            result = self.runtime.process_increment(self.command)
        self.assertEqual(result.status, 'unresolved')
        self.assertIs(self.runtime.campaign, self.root)

    def test_faulty_receipt_producer_cannot_publish_before_coordinator_rejects(self):
        good = self.runtime.prepare_increment(self.command).unit.receipt
        for bad in (replace(good, ref='bad'), replace(good, public_refs=('unknown',)),
                    replace(good, accessible=(('movement', 'hidden basis'),)),
                    replace(good, outcome='invalid')):
            with patch('engine.domain_campaign.safe_receipt', return_value=bad):
                self.assertEqual(self.runtime.process_increment(self.command).status, 'unresolved')
            self.assertIs(self.runtime.campaign, self.root)

    def test_each_authoritative_dependency_change_stales_prepared_unit(self):
        for change in ('time', 'position', 'surface', 'expenditure', 'capability'):
            runtime = GameSession.start_domains(premises())
            proposal = runtime.prepare_increment(self.command)
            d = runtime.campaign.origin
            w, c = d.world, d.characters[0]
            if change == 'time':
                w = replace(w, at_seconds=18)
            elif change == 'position':
                w = replace(w, positions=(('creature', 'middle'),))
            elif change == 'surface':
                w = replace(w, surfaces=(replace(w.surfaces[0], difficult=True),))
            elif change == 'expenditure':
                c = replace(c, movement_spent=5)
            else:
                c = replace(c, conditions=('stunned',))
            d = replace(d, world=w, characters=(c,))
            runtime.restore_domains(replace(runtime.campaign, origin=d, current=d))
            current = runtime.campaign
            with self.assertRaises(Unresolved):
                runtime.accept_increment(proposal)
            self.assertIs(runtime.campaign, current)

    def test_stale_dependent_root_never_publishes(self):
        stale = self.runtime.prepare_increment(self.command)
        other = command(attempt='attempt:other')
        self.runtime.accept_increment(self.runtime.prepare_increment(other))
        current = self.runtime.campaign
        with self.assertRaises(Unresolved):
            self.runtime.accept_increment(stale)
        self.assertIs(self.runtime.campaign, current)

    def test_retry_returns_same_receipt_without_position_read_or_charge(self):
        proposal = self.runtime.prepare_increment(self.command)
        first = self.runtime.accept_increment(proposal)
        root = self.runtime.campaign
        self.assertEqual(self.runtime.accept_increment(proposal), first)
        with patch('engine.domain_campaign.owners', side_effect=AssertionError('retry must not retrieve')):
            result = self.runtime.process_increment(self.command)
        self.assertEqual(result.results, (first,))
        self.assertIs(self.runtime.campaign, root)

    def test_same_identity_different_meaning_rejects(self):
        self.runtime.process_increment(self.command)
        root = self.runtime.campaign
        for changed in (command(route='next'), command(distance=4), command(climb=True)):
            self.assertEqual(self.runtime.process_increment(changed).status, 'unresolved')
            self.assertIs(self.runtime.campaign, root)

    def test_retry_rejects_invalid_exact_field_types_before_lookup(self):
        proposal = self.runtime.prepare_increment(self.command)
        self.runtime.accept_increment(proposal)
        root = self.runtime.campaign

        class Text(str):
            pass

        requests = [replace(self.command.request, **change) for change in (
            {'distance_feet': 5.0}, {'use_climb_speed': 0},
            {'means': ['rope']}, {'attempt': Text('attempt:one')},
            {'creature': Text('creature')}, {'route': Text('first')},
            {'means': (Text('rope'),)},
        )]
        commands = [replace(self.command, request=r) for r in requests]
        commands.append(replace(self.command, activity=Text(self.command.activity)))
        with patch('engine.domain_campaign.owners', side_effect=AssertionError('retry must not retrieve')):
            for changed in commands:
                with self.subTest(command=changed):
                    self.assertEqual(self.runtime.process_increment(changed).status, 'unresolved')
                    with self.assertRaises(ValueError):
                        self.runtime.prepare_increment(changed)
                    unit = replace(proposal.unit, command=changed)
                    with self.assertRaises(ValueError):
                        self.runtime.accept_increment(replace(proposal, unit=unit))
                    self.assertIs(self.runtime.campaign, root)
            self.assertEqual(self.runtime.process_increment(self.command).results, (proposal.unit.receipt,))
        self.assertIs(self.runtime.campaign, root)

    def test_initial_campaign_rejects_nonnull_checkpoint_resolution_reference(self):
        a = self.root.activities[0]
        bad = replace(a, checkpoint=replace(a.checkpoint, resolution_ref='attempt:never-accepted'))
        candidate = replace(self.root, activities=(bad,) + self.root.activities[1:])
        with self.assertRaisesRegex(ValueError, 'checkpoint resolution references are unsupported'):
            GameSession.start_domains(candidate)
        self.assertIs(self.runtime.campaign, self.root)

    def test_execution_rejects_unsupported_resolution_reuse_before_domain_reads(self):
        from engine.domain_campaign import prepare
        a = self.root.activities[0]
        bad = replace(a, checkpoint=replace(a.checkpoint, resolution_ref='attempt:never-accepted'))
        candidate = replace(self.root, activities=(bad,) + self.root.activities[1:])
        with patch('engine.domain_campaign.owners', side_effect=AssertionError('must reject before reads')):
            with self.assertRaisesRegex(ValueError, 'checkpoint resolution references are unsupported'):
                prepare(candidate, self.command)
        self.assertIs(self.runtime.campaign, self.root)

    def test_distinct_valid_attempt_advances_with_current_premises(self):
        self.runtime.process_increment(self.command)
        next_command = command('next', 'attempt:two')
        result = self.runtime.process_increment(next_command)
        self.assertEqual(result.status, 'accepted')
        self.assertEqual(dict(self.runtime.state.world.positions)['creature'], 'end')
        self.assertEqual(self.runtime.state.characters[0].movement_spent, 20)
        self.assertEqual(self.runtime.state.world.at_seconds, 39)
        self.assertEqual(len(self.runtime.campaign.accepted), 2)

    def test_new_attempt_on_same_route_after_real_return_is_distinct(self):
        for cmd in (self.command, command('return', 'return-attempt'), command(attempt='new-attempt')):
            self.assertEqual(self.runtime.process_increment(cmd).status, 'accepted')
        self.assertEqual(self.runtime.state.characters[0].movement_spent, 30)
        self.assertEqual(len(self.runtime.campaign.accepted), 3)

    def test_only_selected_speed_is_required_and_material(self):
        for climb in (False, True):
            base = premises(climb_speed=40)
            c = replace(base.origin.characters[0], **({'speed': None} if climb else {'climb_speed': None}))
            d = replace(base.origin, characters=(c,))
            runtime = GameSession.start_domains(replace(base, origin=d, current=d))
            self.assertEqual(runtime.process_increment(command(climb=climb)).status, 'accepted')

    def test_exact_answered_choice_can_continue_but_missing_means_cannot(self):
        scope = self.root.activities[0]
        development = ActivityDevelopment('player_choice', choice_key='known-risk:one')
        scope = replace(scope, authorization=replace(scope.authorization, answered_choices=('known-risk:one',)),
                        checkpoint=replace(scope.checkpoint, developments=(development,)))
        base = replace(self.root, activities=(scope,) + self.root.activities[1:])
        runtime = GameSession.start_domains(base)
        self.assertEqual(runtime.process_increment(self.command).status, 'accepted')
        scope = replace(scope, checkpoint=replace(scope.checkpoint, missing_means=('missing-rope',)))
        base = replace(self.root, activities=(scope,) + self.root.activities[1:])
        runtime = GameSession.start_domains(base)
        self.assertNotEqual(runtime.process_increment(self.command).status, 'accepted')
        self.assertIs(runtime.campaign, base)

    def test_inquiry_and_preparation_use_common_control_without_execution(self):
        for intent, status in (('inquiry', 'inquiry'), ('prepare', 'preparation')):
            a = self.root.activities[0]
            a = replace(a, authorization=replace(a.authorization, intent=intent))
            base = replace(self.root, activities=(a,) + self.root.activities[1:])
            runtime = GameSession.start_domains(base)
            self.assertEqual(runtime.process_increment(self.command).status, status)
            self.assertIs(runtime.campaign, base)

    def test_fresh_identity_is_not_permission_to_repeat_from_wrong_position(self):
        self.runtime.process_increment(self.command)
        current = self.runtime.campaign
        self.assertEqual(self.runtime.process_increment(command(attempt='fresh')).status, 'unresolved')
        self.assertIs(self.runtime.campaign, current)

    def test_authorization_restriction_choice_and_access_fail_closed(self):
        a = self.root.activities[0]
        variants = [replace(a, authorization=replace(a.authorization, intent=intent))
                    for intent in ('inquiry', 'prepare', 'withdraw')]
        variants += [replace(a, checkpoint=replace(a.checkpoint, blocked=True)),
                     replace(a, checkpoint=replace(a.checkpoint, restart_required=True)),
                     replace(a, authorization=replace(a.authorization, constraints=('quietly',))),
                     replace(a, checkpoint=replace(a.checkpoint, developments=(ActivityDevelopment('player_choice'),)))]
        for changed in variants:
            campaign = replace(self.root, activities=(changed,) + self.root.activities[1:])
            runtime = GameSession.start_domains(campaign)
            self.assertNotEqual(runtime.process_increment(self.command).status, 'accepted')
            self.assertIs(runtime.campaign, campaign)
        c = replace(self.root.origin.characters[0], known_routes=())
        domains = replace(self.root.origin, characters=(c,))
        runtime = GameSession.start_domains(replace(self.root, origin=domains, current=domains))
        self.assertEqual(runtime.process_increment(self.command).status, 'unresolved')

    def test_unsupported_checks_and_partial_endpoints_stop_before_draw(self):
        a = self.root.activities[0]
        changed = replace(a, ruling=ClimbRuling(True, 'requires grounded failure semantics'))
        w = replace(self.root.origin.world, surfaces=(replace(self.root.origin.world.surfaces[0], slippery=True),))
        c = replace(self.root.origin.characters[0], strength=14, proficiency_bonus=2, athletics_rank=1)
        d = replace(self.root.origin, world=w, characters=(c,))
        r = GameSession.start_domains(replace(self.root, origin=d, current=d,
            activities=(changed,) + self.root.activities[1:]))
        self.assertEqual(r.process_increment(self.command).status, 'unresolved')
        self.assertEqual(self.runtime.process_increment(command(distance=2)).status, 'unresolved')

    def test_varied_valid_premises_drive_mechanics_without_named_answers(self):
        for distance, terrain, climb, expected_cost in ((4, False, False, 8), (7, True, False, 21),
                                                       (6, False, True, 6), (8, True, True, 16)):
            with self.subTest(distance=distance, terrain=terrain, climb=climb):
                runtime = GameSession.start_domains(premises(distance=distance, difficult=terrain,
                    climb_speed=40, actor='other-creature', locality='arbitrary-location'))
                result = runtime.process_increment(command(distance=distance, climb=climb, actor='other-creature'))
                self.assertEqual(result.status, 'accepted')
                self.assertEqual(runtime.state.characters[0].movement_spent, expected_cost)

    def test_hidden_unavailable_binding_blocks_without_disclosure(self):
        d = self.root.origin
        w = replace(d.world, surfaces=(replace(d.world.surfaces[0], unresolved_bindings=('hidden:ward',)),))
        d = replace(d, world=w)
        runtime = GameSession.start_domains(replace(self.root, origin=d, current=d))
        result = runtime.process_increment(self.command)
        self.assertEqual(result.status, 'unresolved')
        self.assertNotIn('ward', result.message)


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.runtime = GameSession.start_domains(premises())
        self.runtime.process_increment(command())
        self.path = Path('.artifacts/domain_acceptance_test.json')
        self.corrupt_path = Path('.artifacts/domain_acceptance_corrupt_test.json')

    def tearDown(self):
        self.path.unlink(missing_ok=True)
        self.corrupt_path.unlink(missing_ok=True)

    def test_checkpoint_references_reject_before_adoption_and_preserve_save(self):
        save_game(self.runtime, str(self.path))
        root, saved = self.runtime.campaign, self.path.read_bytes()
        # Even the same activity's accepted ID is unsupported as a separate
        # checkpoint reuse instruction. Its exact command retry remains supported.
        for scope_index, ref in ((0, 'attempt:never-accepted'), (1, 'attempt:one'), (0, 'attempt:one')):
            with self.subTest(scope=scope_index, ref=ref):
                activities = list(root.activities)
                a = activities[scope_index]
                activities[scope_index] = replace(a, checkpoint=replace(a.checkpoint, resolution_ref=ref))
                candidate = replace(root, activities=tuple(activities))
                envelope = {'save_version': 3, 'domain_campaign': pack(candidate)}
                with self.assertRaisesRegex(ValueError, 'checkpoint resolution references are unsupported'):
                    self.runtime.restore_domains(candidate)
                with self.assertRaises(ValueError):
                    restore(envelope)
                self.corrupt_path.write_text(json.dumps(envelope), encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_game(str(self.corrupt_path))
                self.assertIs(self.runtime.campaign, root)
                self.assertEqual(self.path.read_bytes(), saved)
        restored = load_game(str(self.path))
        before = restored.campaign
        self.assertEqual(restored.process_increment(command()).status, 'accepted')
        self.assertIs(restored.campaign, before)

    def test_duplicate_v3_keys_reject_without_changing_live_root_or_save(self):
        save_game(self.runtime, str(self.path))
        root, saved = self.runtime.campaign, self.path.read_bytes()
        encoded = json.dumps(export(root))
        variants = [encoded.replace('"save_version": 3', replacement, 1) for replacement in (
            '"save_version": 4, "save_version": 3',
            '"save_version": 3, "save_version": 4',
            '"save_version": 3, "save_version": 1',
            '"save_version": 3, "save_version": 2',
            '"save_version": 3, "save_version": 3',
        )]
        variants += [encoded.replace('"schema": 1', '"schema": 2, "schema": 1', 1),
                     encoded.replace('"record": "Campaign"',
                                     '"record": "Unknown", "record": "Campaign"', 1),
                     encoded.replace('"blocked": false', '"blocked": false, "blocked": false', 1)]
        for corrupted in variants:
            with self.subTest(payload=corrupted[:80]):
                self.assertNotEqual(corrupted, encoded)
                self.corrupt_path.write_text(corrupted, encoding='utf-8')
                before = self.corrupt_path.read_bytes()
                with self.assertRaisesRegex(ValueError, 'Duplicate JSON keys in version-3 save'):
                    load_game(str(self.corrupt_path))
                self.assertIs(self.runtime.campaign, root)
                self.assertEqual(self.path.read_bytes(), saved)
                self.assertEqual(self.corrupt_path.read_bytes(), before)

    def test_legacy_versions_retain_duplicate_key_decoding_behavior(self):
        from engine.save_system import load_save_data
        from engine.game_engine import GameEngine
        legacy = build_save_data(GameEngine('test_fixtures/bryn_shander_legacy.json'))
        v1 = json.dumps(legacy).replace('"save_version": 1', '"save_version": 9, "save_version": 1', 1)
        self.corrupt_path.write_text(v1, encoding='utf-8')
        self.assertEqual(load_save_data(str(self.corrupt_path))['save_version'], 1)
        self.assertIsInstance(load_game(str(self.corrupt_path)), GameEngine)
        # This checks the unchanged v2 file decoder, not semantic campaign validity.
        v2 = '{"save_version": 9, "save_version": 2, "payload": {"value": 1, "value": 2}}'
        self.corrupt_path.write_text(v2, encoding='utf-8')
        self.assertEqual(load_save_data(str(self.corrupt_path)),
                         {'save_version': 2, 'payload': {'value': 2}})
        from test_fixtures.continuity_suppliers import engine, request, start
        continuing = engine()
        continuing.process_consequence(request(start(continuing)))
        accepted = build_save_data(continuing)
        v2 = json.dumps(accepted).replace('"save_version": 2',
                                          '"save_version": 9, "save_version": 2', 1)
        self.corrupt_path.write_text(v2, encoding='utf-8')
        self.assertEqual(build_save_data(load_game(str(self.corrupt_path))), accepted)

    def test_save_load_retains_identity_relationship_cost_time_and_retry(self):
        save_game(self.runtime, str(self.path))
        restored = load_game(str(self.path))
        self.assertEqual(restored.campaign, self.runtime.campaign)
        before = restored.campaign
        self.assertEqual(restored.process_increment(command()).status, 'accepted')
        self.assertIs(restored.campaign, before)
        self.assertEqual(restored.process_increment(command('next', 'new')).status, 'accepted')

    def test_restore_rejects_bad_references_or_meaning_without_adoption(self):
        root = self.runtime.campaign
        variants = [replace(root, current=replace(root.current,
            world=replace(root.current.world, positions=(('creature', 'missing'),)))),
            replace(root, current=replace(root.current,
                characters=(replace(root.current.characters[0], movement_spent=0),))),
            replace(root, actor='missing'), replace(root, schema=2), replace(root, revision=99),
            replace(root, accepted=()),
            replace(root, current=replace(root.current, characters=(replace(root.current.characters[0],
                ready_equipment=('missing-object',)),))),
            replace(root, accepted=(replace(root.accepted[0], receipt=replace(root.accepted[0].receipt,
                accessible=(('movement', 'secret'),))),))]
        for candidate in variants:
            with self.assertRaises((ValueError, Unresolved)):
                self.runtime.restore_domains(candidate)
            self.assertIs(self.runtime.campaign, root)

    def test_strict_codec_rejects_corruption_unknown_versions_fields_and_types(self):
        envelope = export(self.runtime.campaign)
        variants = [dict(envelope, save_version=4), dict(envelope, save_version=True),
                    dict(envelope, extra=True), {'save_version': 3, 'domain_campaign': {'record': 'eval', 'fields': {}}}]
        for variant in variants:
            with self.assertRaises(ValueError):
                restore(variant)
        encoded = json.dumps(envelope)
        self.path.write_text(encoded[:-9], encoding='utf-8')
        with self.assertRaises(ValueError):
            load_game(str(self.path))
        self.assertEqual(self.runtime.campaign, restore(envelope))

    def test_failed_replace_preserves_previous_save_live_state_and_cleans_temp(self):
        save_game(self.runtime, str(self.path))
        saved, root = self.path.read_bytes(), self.runtime.campaign
        self.runtime.process_increment(command('next', 'new'))
        current = self.runtime.campaign
        with patch('engine.save_system.os.replace', side_effect=OSError('injected replace failure')):
            with self.assertRaises(OSError):
                save_game(self.runtime, str(self.path))
        self.assertEqual(self.path.read_bytes(), saved)
        self.assertIs(self.runtime.campaign, current)
        self.assertEqual(load_game(str(self.path)).campaign, root)
        self.assertEqual(list(self.path.parent.glob(self.path.name + '.*.tmp')), [])

    def test_failed_fsync_and_encoding_preserve_existing_save(self):
        save_game(self.runtime, str(self.path))
        saved, root = self.path.read_bytes(), self.runtime.campaign
        for target in ('engine.save_system.os.fsync', 'engine.save_system.json.dumps'):
            with patch(target, side_effect=OSError('injected prepublication failure')):
                with self.assertRaises(OSError):
                    save_game(self.runtime, str(self.path))
            self.assertEqual(self.path.read_bytes(), saved)
            self.assertIs(self.runtime.campaign, root)
        self.assertEqual(list(self.path.parent.glob(self.path.name + '.*.tmp')), [])

    def test_v3_aggregate_does_not_fit_or_mutate_legacy_codec(self):
        from engine.campaign_records import pack
        with self.assertRaises(ValueError):
            pack(self.runtime.campaign)
        self.assertEqual(build_save_data(self.runtime)['save_version'], 3)


if __name__ == '__main__':
    with patch.object(socket.socket, 'connect', side_effect=AssertionError('offline tests')):
        unittest.main()
