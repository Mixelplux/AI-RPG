"""I2 interface/integrity evidence; all provider and network access forbidden."""
from dataclasses import replace
import json
import socket
import unittest
from unittest.mock import patch

from engine.consequence_integration import FactEffect, Runtime
from engine.game_engine import GameEngine
from engine.gameplay_coordination import AcceptedStep
from engine.information_adjudication import propose_assessed
from engine.information_resolution import (
    AccessGrant, Constraint, BindingTerms, Fact, Identity, Period, Query, Relationship, Source,
)
from engine.save_system import build_save_data, save_game
from test_fixtures.consequence_suppliers import (
    AUTHORED, HIDDEN, LOCATION, REGION, Premises, engine, methods, request,
)


class Integration(unittest.TestCase):
    def setUp(self):
        for guard in (patch('socket.create_connection', side_effect=AssertionError('offline')),
                      patch.object(socket.socket, 'connect', side_effect=AssertionError('offline')),
                      patch.object(socket.socket, 'connect_ex', side_effect=AssertionError('offline')),
                      patch('engine.narration_source.OpenAI', side_effect=AssertionError('offline'))):
            guard.start()
            self.addCleanup(guard.stop)

    def accepted(self, e, r=None, **kw):
        result = e.process_consequence(r or request(), **kw)
        self.assertEqual(result['coordination']['status'], 'accepted', (result, e._consequences.diagnostic))
        return result

    def rejected(self, e, r=None, **kw):
        before = e.get_consequence_state()
        result = e.process_consequence(r or request(), **kw)
        self.assertEqual(e.get_consequence_state(), before)
        self.assertNotEqual(result['coordination']['status'], 'accepted')
        self.assertNotIn(HIDDEN, json.dumps(result))
        return result

    def test_accepted_retry_precedes_current_method_eligibility(self):
        e = engine()
        self.accepted(e)
        prior = e.get_consequence_state()
        e._consequences.config = replace(e._consequences.config, methods=(methods()[1],), targets=(('gap', ('use',)),))
        self.accepted(e)
        self.assertEqual(e.get_consequence_state(), prior)

    def test_request_cannot_grant_control_of_another_actor(self):
        e = engine()
        before = e.get_consequence_state()
        with self.assertRaises(ValueError):
            e.process_consequence(request(actor='agreement'))
        self.assertEqual(e.get_consequence_state(), before)

    def test_request_cannot_make_unapproved_target_actionable(self):
        self.rejected(engine(), request(target='agreement'))
        self.rejected(engine(), request(target='gap'))  # lift is not authorized for gap

    def test_mundane_existing_mechanics_and_one_publication(self):
        e = engine()
        legacy = e.get_world_state()
        self.accepted(e)
        state = e.get_consequence_state()
        self.assertEqual((state.adjudication.at, state.adjudication.inventory), (2, (('actor', 'wedge', 0),)))
        self.assertEqual(state.adjudication.history[0].assessment.draw, 6)
        self.assertEqual(len(state.receipts), 1)
        self.assertEqual(e.get_world_state(), legacy)

    def test_hidden_binding_changes_result_without_disclosure(self):
        p = Premises()
        p.ward()
        e = engine(p)
        result = self.accepted(e)
        self.assertEqual(result['coordination']['results'][0]['outcome'], 'negative')
        self.assertNotIn(HIDDEN, json.dumps(result))
        self.assertIsNone(e.get_consequence_state().adjudication.history[0].assessment.draw)
        p.change('permit', 'yes')
        other = engine(p)
        self.assertEqual(self.accepted(other)['coordination']['results'][0]['outcome'], 'complete')

    def test_changed_mundane_premise_changes_outcome(self):
        p = Premises()
        p.change('manageable', 'no')
        self.assertEqual(self.accepted(engine(p))['coordination']['results'][0]['outcome'], 'negative')

    def test_method_means_and_capability_cannot_be_invented(self):
        for changes in ({'means': ()}, {'method': 'unavailable'}):
            self.rejected(engine(), request(**changes))
        p = Premises()
        p.change('capability:lift', 'no')
        self.rejected(engine(p))

    def test_inquiry_and_preparation_do_not_resolve(self):
        draw = unittest.mock.Mock(return_value=6)
        for intent in ('inquiry', 'prepare'):
            self.rejected(engine(draw=draw), request(intent=intent))
        draw.assert_not_called()

    def test_unhonored_constraint_is_not_silently_ignored(self):
        self.rejected(engine(), request(constraints=('quietly',)))

    def test_linked_effect_definition_is_discovered_iteratively(self):
        p = Premises()
        p.identities += (Identity('effect', 'instance', 'definition'), Identity('definition', 'definition'))
        p.relationships = (Relationship('active', 'target', 'active_effect', 'effect', AUTHORED),)
        p.constraints = (Constraint(HIDDEN, ('definition',), ('open',), BindingTerms(('block',)), AUTHORED),)
        e = engine(p)
        result = self.accepted(e)
        self.assertEqual(result['coordination']['results'][0]['outcome'], 'negative')
        self.assertIn(('identity', 'definition'), p.calls)
        p.relationships = ()
        self.assertEqual(self.accepted(engine(p))['coordination']['results'][0]['outcome'], 'complete')

    def test_dependency_cycle_is_bounded_without_omitting_constraint(self):
        p = Premises()
        p.relationships = (Relationship('loop', 'target', 'governs', 'target', AUTHORED),)
        self.accepted(engine(p))

    def test_unavailable_binding_is_unresolved_without_costs(self):
        p = Premises()
        p.constraints = (Constraint(HIDDEN, (LOCATION,), ('open',), None, AUTHORED,
                                    availability='established_unavailable'),)
        e = engine(p)
        self.rejected(e)
        self.assertEqual(e._consequences.diagnostic, ('retrieval', 'established_unavailable'))
        p.constraints = ()
        self.accepted(e)

    def test_unavailable_material_fact_not_replaced_by_claim(self):
        p = Premises()
        p.change('manageable', None, availability='established_unavailable')
        self.rejected(engine(p))

    def test_uncertain_material_fact_is_not_true(self):
        p = Premises()
        p.change('manageable', 'yes', epistemic='uncertain')
        self.rejected(engine(p))

    def test_coherent_cost_time_commitment_and_later_dependency(self):
        p = Premises()
        p.agreement()
        e = engine(p)
        self.accepted(e, request(related=('agreement',)))
        state = e.get_consequence_state().adjudication
        self.assertEqual((state.at, state.inventory, len(state.obligations)), (2, (('actor', 'wedge', 0),), 1))
        self.accepted(e, request('later', method='depart', means=()))
        self.assertEqual(e.get_consequence_state().adjudication.at, 3)

    def test_new_fact_identity_relationship_and_fresh_later_activity(self):
        effect = FactEffect('lift', 'gap', 'usable', 'yes', identity=Identity('gap'),
                            relation_from='target', relation='governs', visible=True)
        e = engine(effects=(effect,))
        self.accepted(e)
        prior_domain = e._coordination.domain
        view = e.get_consequence_information()
        self.assertEqual(view.identity('gap'), Identity('gap'))
        found = view.resolve(Query(('gap',), 2, ('usable',)))
        self.assertEqual(found.facts[0].value, 'yes')
        self.assertEqual(found.facts[0].period.start, 2)
        state = e.get_consequence_state()
        self.assertEqual(state.relationships[0].subject, 'target')
        self.accepted(e, request('later', target='gap', method='use', means=()))
        self.assertIsNot(e._coordination.domain, prior_domain)

    def test_existing_consequential_slot_not_rewritten(self):
        effect = FactEffect('lift', 'target', 'manageable', 'no')
        self.rejected(engine(effects=(effect,)))

    def test_invalid_new_fact_target_is_not_partially_published(self):
        self.rejected(engine(effects=(FactEffect('lift', 'unknown', 'usable', 'yes'),)))

    def test_hidden_fact_is_not_character_knowledge(self):
        effect = FactEffect('lift', 'target', 'new-condition', 'HIDDEN-NEW-FACT')
        e = engine(effects=(effect,))
        result = self.accepted(e)
        view = e.get_consequence_information()
        self.assertTrue(view.resolve(Query(('target',), 2, ('new-condition',))).facts)
        self.assertFalse(view.for_character(Query(('target',), 2, ('new-condition',)), 'actor', ()).facts)
        self.assertNotIn('HIDDEN-NEW-FACT', json.dumps(result))

    def test_invalid_proposals_have_no_effect(self):
        for change in ({'costs': ()}, {'result': 'full', 'revision': True},
                       {'method': 'use'}, {'capability': 'invented'}):
            with self.subTest(change=change):
                self.rejected(engine(), propose=lambda a: replace(propose_assessed(a), **change))

    def test_stale_material_fact_after_assessment(self):
        p = Premises()
        e = engine(p)
        def propose(a):
            p.change('manageable', 'no')
            return propose_assessed(a)
        self.rejected(e, propose=propose)
        self.assertEqual(e._consequences.diagnostic, ('acceptance', 'stale_premises'))

    def test_stale_relationship_after_assessment(self):
        p = Premises()
        e = engine(p)
        def propose(a):
            p.relationships = (Relationship('new', 'target', 'governs', 'agreement', AUTHORED),)
            return propose_assessed(a)
        self.rejected(e, propose=propose)
        self.assertEqual(e._consequences.diagnostic[0], 'acceptance')

    def test_stale_hidden_binding_after_assessment(self):
        p = Premises()
        e = engine(p)
        def propose(a):
            p.ward()
            return propose_assessed(a)
        self.rejected(e, propose=propose)

    def test_stale_legacy_premise_after_assessment(self):
        e = engine()
        def propose(a):
            e.world_state['weather'] = 'changed'
            return propose_assessed(a)
        self.rejected(e, propose=propose)

    def test_retry_after_time_and_balance_change_without_draw_or_proposal(self):
        draw = unittest.mock.Mock(return_value=6)
        e = engine(draw=draw)
        first = self.accepted(e)
        before = e.get_consequence_state()
        second = self.accepted(e, propose=lambda a: self.fail('accepted retry proposed again'))
        self.assertEqual(e.get_consequence_state(), before)
        self.assertEqual(first['coordination']['results'], second['coordination']['results'])
        self.assertEqual(draw.call_count, 1)

    def test_conflicting_retry_identity_rejected_and_new_attempt_is_current(self):
        e = engine()
        self.accepted(e)
        self.rejected(e, request(method='depart', means=()))
        self.assertEqual(e._consequences.diagnostic, ('acceptance', 'identity_conflict'))
        self.rejected(e, request('new'))  # wedge already spent

    def test_accepted_increment_survives_later_invalid_proposal(self):
        e = engine()
        self.accepted(e)
        prior = e.get_consequence_state()
        self.rejected(e, request('next', method='depart', means=()),
                      propose=lambda a: replace(propose_assessed(a), capability='invented'))
        self.assertEqual(e.get_consequence_state(), prior)
        self.accepted(e)

    def test_supplier_exception_is_contained(self):
        e = engine()
        with patch.object(e._consequences, 'information', side_effect=RuntimeError(HIDDEN)):
            result = self.rejected(e)
        self.assertNotIn(HIDDEN, json.dumps(result))

    def test_proposal_exception_is_contained(self):
        def fail(a):
            raise RuntimeError(HIDDEN)
        self.rejected(engine(), propose=fail)

    def test_receipt_failure_precedes_publication(self):
        e = engine()
        with patch.object(Runtime, '_receipt', side_effect=RuntimeError(HIDDEN)):
            self.rejected(e)

    def test_malformed_receipt_precedes_publication(self):
        e = engine()
        with patch.object(Runtime, '_receipt', return_value=AcceptedStep('wrong')):
            self.rejected(e)

    def test_presentation_fault_after_publication_does_not_recharge(self):
        e = engine()
        with patch('engine.gameplay_coordination.CoordinationDecision.player_result', side_effect=RuntimeError('display')):
            result = e.process_consequence(request())
            self.assertEqual(result['coordination']['failure'], 'presentation')
        before = e.get_consequence_state()
        self.accepted(e)
        self.assertEqual(e.get_consequence_state(), before)

    def test_reentrant_attempt_does_not_publish_nested_effects(self):
        e = engine()
        def propose(a):
            with self.assertRaises(ValueError):
                e.process_consequence(request('nested'))
            return propose_assessed(a)
        self.accepted(e, propose=propose)
        self.assertEqual(len(e.get_consequence_state().receipts), 1)

    def test_state_reads_are_defensive(self):
        e = engine()
        self.accepted(e)
        state = e.get_consequence_state()
        state.adjudication.history[0].context.clear()
        self.assertTrue(e.get_consequence_state().adjudication.history[0].context)

    def test_save_load_and_replacement_block_before_io(self):
        e = engine()
        self.accepted(e)
        before = e.get_consequence_state()
        with patch('builtins.open', side_effect=AssertionError('file opened')):
            for operation in (lambda: build_save_data(e), lambda: save_game(e, 'never.json'),
                              lambda: e.save('never.json'), lambda: e.load('never.json'), e.reset,
                              lambda: e.process_command('move north')):
                with self.assertRaisesRegex(ValueError, 'in-memory continuity'):
                    operation()
        self.assertEqual(e.get_consequence_state(), before)

    def test_default_save_and_command_behavior_remain_available(self):
        e = GameEngine(REGION)
        self.assertEqual(build_save_data(e)['save_version'], 1)
        self.assertIsInstance(e.process_command('look'), dict)
        with self.assertRaises(ValueError):
            e.process_consequence(request())

    def test_partial_progress_is_accepted_and_retry_does_not_reroll(self):
        draw = unittest.mock.Mock(return_value=3)
        e = engine(draw=draw)
        result = self.accepted(e)
        self.assertEqual(result['coordination']['results'][0]['outcome'], 'incomplete')
        self.accepted(e)
        self.assertEqual(draw.call_count, 1)
        self.assertEqual(e.get_consequence_state().adjudication.at, 2)

    def test_accepted_fictional_failure_retains_legitimate_cost(self):
        e = engine(draw=lambda: 1)
        result = self.accepted(e)
        self.assertEqual(result['coordination']['results'][0]['outcome'], 'negative')
        self.assertEqual(e.get_consequence_state().adjudication.inventory[0][2], 0)

    def test_invalid_draw_is_contained_without_acceptance(self):
        self.rejected(engine(draw=lambda: True))

    def test_expired_binding_does_not_apply(self):
        p = Premises()
        p.ward()
        p.constraints = (replace(p.constraints[0], period=Period(-2, 0)),)
        self.assertEqual(self.accepted(engine(p))['coordination']['results'][0]['outcome'], 'complete')

    def test_accepted_condition_removal_is_recognized_later(self):
        p = Premises()
        p.ward()
        p.change('permit', 'yes')
        e = engine(p)
        self.accepted(e, request('removal', method='remove', means=(), binding=HIDDEN))
        self.assertEqual(e.get_consequence_state().adjudication.ended, (HIDDEN,))
        p.change('permit', 'no')
        result = self.accepted(e)
        self.assertEqual(result['coordination']['results'][0]['outcome'], 'complete')

    def test_unauthorized_condition_removal_is_rejected(self):
        p = Premises()
        p.ward()
        self.rejected(engine(p), request(method='remove', means=(), binding=HIDDEN))

    def test_retry_does_not_duplicate_commitments(self):
        p = Premises()
        p.agreement()
        e = engine(p)
        r = request(related=('agreement',))
        self.accepted(e, r)
        prior = e.get_consequence_state()
        self.accepted(e, r)
        self.assertEqual(e.get_consequence_state(), prior)
        self.assertEqual(len(prior.adjudication.obligations), 1)

    def test_hidden_commitment_is_not_disclosed(self):
        p = Premises()
        p.agreement()
        result = self.accepted(engine(p), request(related=('agreement',)))
        self.assertNotIn('return the wedge', json.dumps(result))

    def test_legitimately_known_commitment_is_disclosed(self):
        p = Premises()
        p.agreement()
        grants = (AccessGrant('agreement-terms', 'actor', Source('known-terms', 'character', ('consented terms',))),)
        result = self.accepted(engine(p, grants=grants), request(related=('agreement',)))
        self.assertIn('return the wedge', json.dumps(result))

    def test_fact_reference_introduces_material_binding_scope(self):
        p = Premises()
        p.constraints = (
            Constraint('local', ('target',), ('open',), BindingTerms(('obligation=keep watch',),
                prerequisites=('fact=agreement|consent|yes',)), AUTHORED),
            Constraint(HIDDEN, ('agreement',), ('open',), BindingTerms(('block',)), AUTHORED),
        )
        p.facts += (Fact('consent', 'agreement', 'consent', 'yes', AUTHORED),)
        result = self.accepted(engine(p))
        self.assertEqual(result['coordination']['results'][0]['outcome'], 'negative')

    def test_changed_linked_definition_changes_applicability(self):
        p = Premises()
        p.identities += (Identity('effect', 'instance', 'definition'), Identity('definition', 'definition'))
        p.relationships = (Relationship('active', 'target', 'active_effect', 'effect', AUTHORED),)
        p.facts += (Fact('active-rule', 'definition', 'active', 'yes', AUTHORED),)
        p.constraints = (Constraint(HIDDEN, ('definition',), ('open',), BindingTerms(('block',),
            prerequisites=('fact=definition|active|yes',)), AUTHORED),)
        self.assertEqual(self.accepted(engine(p))['coordination']['results'][0]['outcome'], 'negative')
        p.change('active', 'no')
        self.assertEqual(self.accepted(engine(p))['coordination']['results'][0]['outcome'], 'complete')

    def test_relevant_but_unavailable_linked_definition_is_not_ignored(self):
        p = Premises()
        p.identities += (Identity('effect', 'instance', 'definition'), Identity('definition', 'definition'))
        p.relationships = (Relationship('active', 'target', 'active_effect', 'effect', AUTHORED),)
        p.constraints = (Constraint(HIDDEN, ('definition',), ('open',), None, AUTHORED,
            availability='established_unavailable'),)
        self.rejected(engine(p))

    def test_partial_new_fact_survives_rejected_later_attempt(self):
        effect = FactEffect('lift', 'target', 'foothold', 'established', result='partial')
        e = engine(effects=(effect,), draw=lambda: 3)
        self.accepted(e)
        self.rejected(e, request('later'))
        facts = e.get_consequence_information().resolve(Query(('target',), 2, ('foothold',))).facts
        self.assertEqual(facts[0].value, 'established')

    def test_stale_resource_owner_is_not_overwritten(self):
        e = engine()
        def propose(a):
            runtime = e._consequences
            runtime._state = replace(runtime._state, adjudication=replace(
                runtime._state.adjudication, inventory=(('actor', 'wedge', 0),)))
            return propose_assessed(a)
        result = e.process_consequence(request(), propose=propose)
        self.assertEqual(result['coordination']['status'], 'unresolved')
        state = e.get_consequence_state()
        self.assertEqual((state.adjudication.at, state.receipts), (0, ()))
        self.assertEqual(state.adjudication.inventory, (('actor', 'wedge', 0),))
        self.assertEqual(e._consequences.diagnostic, ('acceptance', 'stale_premises'))

    def test_stale_method_authorization_is_rejected(self):
        e = engine()
        def propose(a):
            e._consequences.config = replace(e._consequences.config, methods=(methods()[1],))
            return propose_assessed(a)
        self.rejected(e, propose=propose)

    def test_final_supplier_failure_prevents_publication(self):
        e = engine()
        with patch.object(e._consequences, 'information', side_effect=[
                e.get_consequence_information(), RuntimeError(HIDDEN)]):
            self.rejected(e)

    def test_candidate_validation_failure_prevents_publication(self):
        e = engine()
        with patch.object(Runtime, '_incorporate', side_effect=ValueError(HIDDEN)):
            self.rejected(e)
        self.assertEqual(e._consequences.diagnostic[0], 'validation')

    def test_unknown_public_receipt_reference_is_rejected(self):
        e = engine()
        with patch.object(Runtime, '_receipt', return_value=AcceptedStep(
                'increment-1', ('unknown',), accessible=(('safe', 'Accepted result.'),))):
            self.rejected(e)

    def test_visible_accepted_fact_is_available_to_later_presentation(self):
        e = engine(effects=(FactEffect('lift', 'target', 'visible-finding', 'OBSERVED', visible=True),))
        self.accepted(e)
        state = e.get_consequence_state()
        view = e.get_consequence_information()
        facts = view.for_character(Query(('target',), 2, ('visible-finding',)), 'actor', state.grants).facts
        self.assertEqual(facts[0].value, 'OBSERVED')


    def test_composed_relationship_path_reaches_base_information(self):
        p = Premises()
        p.identities += (Identity('definition', 'definition'),)
        p.relationships = (Relationship('definition-link', 'agreement', 'definition', 'definition', AUTHORED),)
        p.facts += (Fact('definition-fact', 'definition', 'rule', 'established', AUTHORED),)
        effect = FactEffect('lift', 'agreement', 'usable', 'yes', relation_from='target', relation='governs')
        e = engine(p, effects=(effect,))
        self.accepted(e)
        result = e.get_consequence_information().resolve(Query(('target',), 2,
            relations=('governs', 'definition'), depth=2))
        self.assertIn('definition-fact', {f.id for f in result.facts})
        selection = next(s for s in result.selections if s.record_id == 'definition-fact')
        self.assertEqual(selection.via, ('increment-1:relation:0', 'definition-link'))

    def test_composed_access_does_not_traverse_hidden_edges(self):
        e = engine(effects=(FactEffect('lift', 'agreement', 'usable', 'yes',
                                      relation_from='target', relation='governs'),))
        self.accepted(e)
        result = e.get_consequence_information().for_character(
            Query(('target',), 2, relations=('governs',), depth=1), 'actor', ())
        self.assertEqual((result.facts, result.relationships), ((), ()))

    def test_composed_availability_keeps_base_material_unavailability(self):
        p = Premises()
        p.change('manageable', None, availability='established_unavailable')
        view = engine(p).get_consequence_information()
        result = view.resolve(Query(('target',), 0, ('manageable',)))
        self.assertEqual(result.availability[0].classification, 'established_unavailable')

    def test_removed_binding_can_later_be_unavailable_without_reapplying(self):
        p = Premises()
        p.ward()
        p.change('permit', 'yes')
        e = engine(p)
        self.accepted(e, request('remove', method='remove', means=(), binding=HIDDEN))
        p.constraints = (replace(p.constraints[0], terms=None, availability='established_unavailable'),)
        self.accepted(e)


if __name__ == '__main__':
    unittest.main()
