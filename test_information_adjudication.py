"""Offline adjudication evidence, separated by failure boundary.

Suppliers below stipulate coherent rules, relevance, capabilities and access;
they do not supply scenario outcomes. The same session adjudicates every case.
"""
from dataclasses import replace
import json
import socket
import unittest
from unittest.mock import patch

from engine.activity_control import ActivityAuthorization, ActivityDevelopment
from engine.information_adjudication import (
    AdjudicationSession, Attempt, Method, Proposal, SessionState, propose_assessed,
)
from engine.information_resolution import (
    AccessGrant, BindingTerms, Constraint, Fact, Foundation, Identity,
    InformationSnapshot, Period, RepresentationError, Relationship, Source, ConstraintQuery,
)
from engine.narrative_realization import build_realization_request, realize


AUTHORED = Source("foundation", "authored")
ACCESS = Source("legitimate-access", "character", ("observation and supplied knowledge",))
HIDDEN = "SECRET-WARD-CAUSE"


def fact(subject, predicate, value, **kw):
    return Fact(subject + ":" + predicate, subject, predicate, value, AUTHORED, **kw)


def premises(*, permit="no", anchor="yes", capacity="yes", removal="yes",
             fee="yes", excluded="no", exemption="no", issuer="yes"):
    return (
        fact("actor", "capability:climb", capacity), fact("actor", "capability:float", "yes"),
        fact("actor", "capability:unweave", "yes"), fact("actor", "capability:revoke", "yes"),
        fact("actor", "trained", "no"), fact("actor", "permit", permit),
        fact("actor", "removal", removal), fact("target", "anchor", anchor),
        fact("target", "manageable", "yes"), fact("actor", "issuer", issuer),
        fact("agreement", "fee", fee), fact("actor", "excluded", excluded),
        fact("actor", "exemption", exemption), fact("agreement", "complete", "no"),
    )


def ward(**kw):
    terms = BindingTerms(("block",), triggers=("method=float",),
                         exceptions=("fact=actor|permit|yes",),
                         termination=("action=dispel", "method=unweave", "fact=actor|removal|yes"))
    return Constraint(HIDDEN, ("place",), ("cross", "dispel"), terms, AUTHORED, **kw)


def agreement():
    return Constraint("agreement-terms", ("agreement",), ("cross", "revoke", "end"), BindingTerms(
        ("obligation=pay one silver on departure",), prerequisites=("fact=agreement|fee|yes",),
        triggers=("action=cross",), exclusions=("fact=actor|excluded|yes",),
        exceptions=("fact=actor|exemption|yes",),
        termination=("action=end", "fact=agreement|complete|yes"),
        revocation=("action=revoke", "fact=actor|issuer|yes")), AUTHORED)


def methods():
    return (
        Method("hook", "cross", "climb", ("rope",), requirements=("fact=target|anchor|yes",),
               mechanic="d6", specialist="trained", conflicts=("no_climb",),
               observations=(("full", "You secure the hook and climb across."),
                             ("partial", "You secure a foothold but remain below the crossing."),
                             ("failure", "The hook slips; you remain below."),
                             ("blocked", "The hook cannot secure an anchor; you remain below."))),
        Method("float", "cross", "float", ("scroll",), (("scroll", 1),),
               observations=(("full", "You rise across the gap."),
                             ("partial", "You rise partway."), ("failure", "You remain below."),
                             ("blocked", "Your ascent stops; you remain below."))),
        Method("potion-float", "cross", "float", ("potion",), (("potion", 1),)),
        Method("unweave", "dispel", "unweave", operation="end_binding"),
        Method("revoke", "revoke", "revoke", operation="end_binding"),
        Method("end", "end", "revoke", operation="end_binding"),
        Method("lift", "cross", "climb", ("lever",),
               requirements=("fact=target|manageable|yes",), mechanic="d6", specialist="trained"),
        Method("depart", "leave", "climb"),
    )


def snapshot(facts=None, constraints=(), *, current=()):
    facts = premises() if facts is None else facts
    ids = tuple(Identity(s) for s in ("actor", "target", "place", "rope", "scroll", "potion", "lever", "agreement"))
    return InformationSnapshot((Foundation("world", "setting", "era", ids, facts, constraints=constraints),),
                               current=current)


def session(*, facts=None, constraints=(), draw=6, grants=(), method_rules=None, info=None):
    access = info or snapshot(facts, constraints)
    controlled = draw if callable(draw) else lambda: draw
    return AdjudicationSession(access, methods() if method_rules is None else method_rules,
        state=SessionState(inventory=(("actor", "rope", 1), ("actor", "scroll", 3),
                                      ("actor", "potion", 1), ("actor", "lever", 1))),
        grants=grants, draw=controlled)


def attempt(s, method="hook", *, id=None, action=None, **kw):
    m = next((m for m in methods() if m.id == method), None)
    action = action or (m.action if m else "cross")
    return Attempt(id or f"attempt-{len(s.state.history)}", "actor", action, method,
                   "target", "place", s.state.at,
                   ActivityAuthorization(action, method or "choose"),
                   means=m.means if m else (), related=("agreement",), **kw)


def outcome(s, result):
    assert result["status"] == "accepted", result
    return s.state.history[-1].assessment.result


class AdjudicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.network = patch.object(socket.socket, "connect", side_effect=AssertionError("Network forbidden"))
        cls.network.start()
        cls.connection = patch("socket.create_connection", side_effect=AssertionError("Network forbidden"))
        cls.connection.start()

    @classmethod
    def tearDownClass(cls):
        cls.connection.stop()
        cls.network.stop()

    def assertUnchanged(self, s, request, proposer, *, stage="acceptance", status="rejected"):
        before = s.state
        reply = s.step(request, proposer)
        self.assertEqual((reply["status"], reply["stage"]), (status, stage), reply)
        self.assertIsNone(reply["context"])
        self.assertEqual(s.state, before)
        return reply

    def test_hidden_ward_orders_and_method_distinction(self):
        for order in (("hook", "float"), ("float", "hook")):
            with self.subTest(order=order):
                s = session(constraints=(ward(),))
                for method in order:
                    reply = s.step(attempt(s, method))
                    self.assertEqual(outcome(s, reply), "blocked" if method == "float" else "full")
                    self.assertNotIn(HIDDEN, json.dumps(reply))
                self.assertEqual(s.state.at, 2)
                self.assertEqual(dict(((a, r), n) for a, r, n in s.state.inventory)[("actor", "scroll")], 2)
                self.assertEqual(s.state.history[order.index("float")].assessment.applied_bindings, (HIDDEN,))

    def test_changed_authoritative_exception_changes_result(self):
        for permit, expected in (("no", "blocked"), ("yes", "full")):
            s = session(facts=premises(permit=permit), constraints=(ward(),))
            self.assertEqual(outcome(s, s.step(attempt(s, "float"))), expected)
            self.assertIn("actor:permit", s.state.history[-1].assessment.premise_ids)

    def test_changed_trigger_applies_to_chosen_method_not_identity(self):
        c = ward()
        c = replace(c, terms=replace(c.terms, triggers=("method=hook",)))
        s = session(constraints=(c,))
        self.assertEqual(outcome(s, s.step(attempt(s, "hook"))), "blocked")
        self.assertEqual(outcome(s, s.step(attempt(s, "float"))), "full")

    def test_removal_changes_later_applicability_preserves_history(self):
        s = session(constraints=(ward(),))
        self.assertEqual(outcome(s, s.step(attempt(s, "float"))), "blocked")
        earlier = s.state.history[0]
        self.assertEqual(outcome(s, s.step(attempt(s, "unweave", binding=HIDDEN))), "full")
        self.assertEqual(s.state.ended, (HIDDEN,))
        later = s.step(attempt(s, "float"))
        self.assertEqual(outcome(s, later), "full")
        self.assertEqual(s.state.history[0], earlier)
        self.assertTrue(any("ascent stops" in r["meaning"] for r in later["context"]["continuity"]))
        self.assertNotIn(HIDDEN, json.dumps(later))

    def test_removal_requires_actual_authority(self):
        s = session(facts=premises(removal="no"), constraints=(ward(),))
        self.assertUnchanged(s, attempt(s, "unweave", binding=HIDDEN), propose_assessed,
                             stage="authorization", status="unresolved")
        self.assertEqual(outcome(s, s.step(attempt(s, "float"))), "blocked")

    def test_unrelated_binding_can_prevent_removal(self):
        veto = Constraint("veto", ("place",), ("dispel",), BindingTerms(("block",)), AUTHORED)
        s = session(constraints=(ward(), veto))
        self.assertEqual(outcome(s, s.step(attempt(s, "unweave", binding=HIDDEN))), "blocked")
        self.assertEqual(s.state.ended, ())

    def test_expiry_uses_existing_half_open_time(self):
        s = session(constraints=(ward(period=Period(0, 1)),))
        self.assertEqual(outcome(s, s.step(attempt(s, "float"))), "blocked")
        self.assertEqual(outcome(s, s.step(attempt(s, "float"))), "full")

    def test_agreement_prerequisite_exclusion_exception_changed_premises(self):
        for changes, applies in (({}, True), ({"fee": "no"}, False),
                                 ({"excluded": "yes"}, False), ({"exemption": "yes"}, False)):
            with self.subTest(changes=changes):
                s = session(facts=premises(**changes), constraints=(agreement(),))
                self.assertEqual(outcome(s, s.step(attempt(s))), "full")
                self.assertEqual(bool(s.state.obligations), applies)

    def test_agreement_effect_changed_from_obligation_to_prohibition(self):
        c = agreement()
        s = session(constraints=(replace(c, terms=replace(c.terms, effects=("block",))),))
        self.assertEqual(outcome(s, s.step(attempt(s))), "blocked")
        self.assertEqual(s.state.obligations, ())

    def test_trigger_controls_effect(self):
        c = agreement()
        s = session(constraints=(replace(c, terms=replace(c.terms, triggers=("method=float",))),))
        self.assertEqual(outcome(s, s.step(attempt(s))), "full")
        self.assertEqual(s.state.obligations, ())

    def test_revocation_preserves_and_applies_retained_commitment(self):
        guard = Constraint("departure-obligation", ("place",), ("leave",), BindingTerms(
            ("block",), prerequisites=("commitment=agreement-terms|pay one silver on departure",)), AUTHORED)
        grant = AccessGrant("agreement-terms", "actor", ACCESS)
        s = session(constraints=(agreement(), guard), grants=(grant,))
        first = s.step(attempt(s))
        self.assertEqual(outcome(s, first), "full")
        self.assertIn("Your accepted obligation", json.dumps(first["context"]))
        commitment = s.state.obligations
        self.assertEqual(outcome(s, s.step(attempt(s, "revoke", binding="agreement-terms"))), "full")
        self.assertEqual(s.state.obligations, commitment)
        later = s.step(attempt(s, "depart"))
        self.assertEqual(outcome(s, later), "blocked")
        self.assertIn("Your accepted obligation", json.dumps(later["context"]["continuity"]))
        self.assertEqual(outcome(s, s.step(attempt(s))), "full")
        self.assertEqual(s.state.history[-1].assessment.obligations, ())

    def test_revocation_requires_issuer(self):
        s = session(facts=premises(issuer="no"), constraints=(agreement(),))
        self.assertUnchanged(s, attempt(s, "revoke", binding="agreement-terms"), propose_assessed,
                             stage="authorization", status="unresolved")

    def test_termination_requires_all_terms(self):
        for complete, expected in (("no", "unresolved"), ("yes", "accepted")):
            fs = tuple(replace(f, value=complete) if f.predicate == "complete" else f for f in premises())
            s = session(facts=fs, constraints=(agreement(),))
            reply = s.step(attempt(s, "end", binding="agreement-terms"))
            self.assertEqual(reply["status"], expected)
            self.assertEqual(bool(s.state.ended), complete == "yes")

    def test_mundane_constraints_mechanics_and_no_magical_explanation(self):
        for manageable, draw, expected in (("no", 6, "blocked"), ("yes", 1, "failure"),
                                           ("yes", 3, "partial"), ("yes", 6, "full")):
            fs = tuple(replace(f, value=manageable) if f.predicate == "manageable" else f for f in premises())
            s = session(facts=fs, draw=draw)
            reply = s.step(attempt(s, "lift"))
            self.assertEqual(outcome(s, reply), expected)
            rendered = json.dumps(reply["context"]).lower()
            self.assertFalse(any(word in rendered for word in ("ward", "magic", "curse")))
            self.assertEqual(s.state.history[-1].assessment.draw, None if manageable == "no" else draw)

    def test_actual_capability_not_proposal_grants_eligibility(self):
        s = session(facts=premises(capacity="no"))
        proposer = unittest.mock.Mock(side_effect=AssertionError("Must not generate"))
        self.assertUnchanged(s, attempt(s), proposer, stage="authorization", status="unresolved")
        proposer.assert_not_called()

    def test_actual_means_not_proposal_grants_resources(self):
        s = session()
        request = replace(attempt(s), means=("dragon",))
        self.assertUnchanged(s, request, propose_assessed, stage="authorization", status="control")

    def test_consumed_resources_prevent_later_attempt(self):
        s = session()
        for _ in range(3):
            self.assertEqual(outcome(s, s.step(attempt(s, "float"))), "full")
        self.assertUnchanged(s, attempt(s, "float"), propose_assessed, stage="authorization", status="control")

    def test_invalid_ai_proposals_no_mutation_knowledge_or_fictional_failure(self):
        mutations = (
            lambda p: replace(p, result="full"),  # bypass hidden binding
            lambda p: replace(p, method="potion-float"),
            lambda p: replace(p, means=("potion",)),
            lambda p: replace(p, costs=()),
            lambda p: replace(p, capability="unlimited-flight"),
            lambda p: replace(p, ended=(HIDDEN,)),
            lambda p: replace(p, obligations=(("invented", "secret knowledge"),)),
            lambda p: replace(p, revision=99),
            lambda p: replace(p, revision=False),
            lambda p: {"result": "full", "knowledge": HIDDEN},
            lambda p: None,
        )
        for change in mutations:
            s = session(constraints=(ward(),))
            self.assertUnchanged(s, attempt(s, "float"), lambda a: change(propose_assessed(a)))

    def test_ai_cannot_override_mechanics(self):
        s = session(draw=1)
        self.assertUnchanged(s, attempt(s), lambda a: replace(propose_assessed(a), result="full"))

    def test_proposal_exception_is_technical_rejection(self):
        s = session()
        def broken(a):
            raise RuntimeError("untrusted private payload")
        reply = self.assertUnchanged(s, attempt(s), broken, stage="proposal")
        self.assertNotIn("private", json.dumps(reply))

    def test_missing_unavailable_uncertain_facts_are_distinct(self):
        variants = (
            (tuple(f for f in premises() if f.predicate != "anchor"), "unspecified"),
            (tuple(replace(f, value=None, availability="established_unavailable") if f.predicate == "anchor" else f
                   for f in premises()), "established_unavailable"),
            (tuple(replace(f, epistemic="uncertain") if f.predicate == "anchor" else f
                   for f in premises()), "uncertain"),
        )
        for fs, reason in variants:
            s = session(facts=fs)
            reply = self.assertUnchanged(s, attempt(s), propose_assessed, stage="retrieval", status="unresolved")
            self.assertEqual(reply["reason"], reason)

    def test_unavailable_hidden_terms_do_not_disclose_existence(self):
        s = session(constraints=(replace(ward(), terms=None, availability="established_unavailable"),))
        reply = self.assertUnchanged(s, attempt(s, "float"), propose_assessed, stage="retrieval", status="unresolved")
        self.assertNotIn(HIDDEN, json.dumps(reply))

    def test_authoritative_retrieval_can_supply_previously_unavailable_slot(self):
        fs = tuple(replace(f, value=None, availability="established_unavailable") if f.predicate == "anchor" else f
                   for f in premises())
        current = (Fact("accepted-anchor", "target", "anchor", "yes", Source("accepted", "world_simulation")),)
        s = session(info=snapshot(fs, current=current))
        self.assertEqual(outcome(s, s.step(attempt(s))), "full")
        self.assertIn("accepted-anchor", s.state.history[-1].assessment.premise_ids)

    def test_ambiguous_method_or_means_returns_player_control(self):
        s = session(constraints=(ward(),))
        reply = self.assertUnchanged(s, attempt(s, None), propose_assessed, stage="authorization", status="control")
        self.assertEqual(reply["reason"], "choose_method")
        self.assertNotIn(HIDDEN, json.dumps(reply))
        request = replace(attempt(s, "float"), means=("scroll", "potion"))
        self.assertUnchanged(s, request, propose_assessed, stage="authorization", status="control")

    def test_unsupported_terms_are_not_silently_permission(self):
        for field, terms in (("triggers", ("when the moon approves",)), ("effects", ("invent-magic",)),
                             ("exceptions", ("arbitrary exception",)), ("termination", ("anything",))):
            c = ward()
            c = replace(c, terms=replace(c.terms, **{field: terms}))
            s = session(constraints=(c,))
            self.assertUnchanged(s, attempt(s), propose_assessed, stage="representation", status="unresolved")

    def test_representation_failure_distinct_from_retrieval(self):
        with self.assertRaises(RepresentationError):
            snapshot((fact("unknown", "p", "v"),))
        s = session()
        self.assertUnchanged(s, replace(attempt(s), target="unknown"), propose_assessed,
                             stage="retrieval", status="unresolved")

    def test_safe_retained_inference_report_attribution_not_hidden_cause(self):
        inferred = fact("actor", "interpretation", "The obstacle may oppose upward movement.",
                        epistemic="inference", holder="actor")
        claim = fact("actor", "report", "A guide reports an old restriction.", epistemic="claim", holder="actor")
        grants = tuple(AccessGrant(f.id, "actor", ACCESS) for f in (inferred, claim))
        s = session(facts=(*premises(), inferred, claim), constraints=(ward(),), grants=grants)
        reply = s.step(attempt(s, "float"))
        records = reply["context"]["developments"]
        self.assertTrue(any(r["status"] == "inferred" and "may" in r["meaning"] for r in records))
        self.assertTrue(any(r["status"] == "reported" and "guide reports" in r["meaning"] for r in records))
        serialized = build_realization_request(reply["context"])["input"]
        self.assertNotIn(HIDDEN, serialized)
        self.assertNotIn("binding_terms", serialized)

    def test_no_grant_no_character_knowledge(self):
        secret = fact("actor", "private", HIDDEN)
        s = session(facts=(*premises(), secret), constraints=(ward(),))
        reply = s.step(attempt(s, "float"))
        self.assertNotIn(HIDDEN, build_realization_request(reply["context"])["input"])

    def test_f05_controls_interruption_withdrawal_constraints_and_hidden_development(self):
        for request_change in (
            lambda a: replace(a, authorization=replace(a.authorization, intent="inquiry")),
            lambda a: replace(a, authorization=replace(a.authorization, intent="withdraw")),
            lambda a: replace(a, authorization=replace(a.authorization, constraints=("no_climb",))),
            lambda a: replace(a, developments=(ActivityDevelopment("player_choice", choice_key="route"),)),
            lambda a: replace(a, authorization=replace(a.authorization, method="float")),
        ):
            s = session()
            self.assertUnchanged(s, request_change(attempt(s)), propose_assessed, stage="authorization", status="control")
        s = session()
        hidden = ActivityDevelopment("player_choice", perceived=False)
        self.assertEqual(outcome(s, s.step(attempt(s, developments=(hidden,)))), "full")

    def test_resumption_keeps_accepted_result_without_draw_cost_or_proposal(self):
        draws = unittest.mock.Mock(return_value=3)
        s = session(draw=draws)
        request = attempt(s)
        accepted = s.step(request)
        self.assertEqual(outcome(s, accepted), "partial")
        before = s.state
        request = replace(request, at=before.at,
                          developments=(ActivityDevelopment("player_choice", choice_key="continue"),))
        self.assertUnchanged(s, request, propose_assessed, stage="authorization", status="control")
        request = replace(request, authorization=replace(request.authorization, answered_choices=("continue",)))
        proposal = unittest.mock.Mock(side_effect=AssertionError("Do not repropose"))
        replay = s.step(request, proposal)
        self.assertEqual(replay["status"], "reused")
        self.assertEqual(replay["context"], accepted["context"])
        self.assertEqual(s.state, before)
        draws.assert_called_once()
        proposal.assert_not_called()
        changed = replace(request, method="float", means=("scroll",), authorization=ActivityAuthorization("cross", "float"))
        self.assertUnchanged(s, changed, propose_assessed)

    def test_presentation_failure_rolls_back_acceptance(self):
        s = session()
        with patch("engine.information_adjudication.validate_context", side_effect=ValueError("bad safe context")):
            self.assertUnchanged(s, attempt(s), propose_assessed, stage="presentation", status="unresolved")

    def test_f01_generation_failure_does_not_undo_or_reroll(self):
        s = session()
        request = attempt(s)
        result = s.step(request)
        before = s.state
        def unavailable(**kwargs):
            raise RuntimeError("offline")
        self.assertEqual(realize(result["context"], unavailable)["status"], "unavailable")
        self.assertEqual(s.state, before)
        self.assertEqual(s.step(replace(request, at=s.state.at))["status"], "reused")

    def test_defensive_state_and_result_copies(self):
        s = session()
        result = s.step(attempt(s))
        result["context"]["developments"][0]["meaning"] = "fake"
        external = s.state
        external.history[0].context["developments"][0]["meaning"] = "other fake"
        self.assertNotIn("fake", json.dumps(s.state.history[0].context))

    def test_reentrant_proposal_cannot_publish_a_second_attempt(self):
        s = session()
        def callback(a):
            self.assertEqual(s.step(replace(a.attempt, id="nested"))["status"], "rejected")
            return propose_assessed(a)
        self.assertEqual(outcome(s, s.step(attempt(s), callback)), "full")
        self.assertEqual(len(s.state.history), 1)

    def test_opaque_identity_permutations_and_changed_fact_use_common_mechanism(self):
        for prefix in ("arbitrary-", "unrelated-"):
            for value, expected in (("sealed", "blocked"), ("open", "full")):
                actor, place, target, capability, method, rule = (prefix + s for s in
                    ("person", "site", "object", "ability", "approach", "condition"))
                f = (fact(actor, "capability:" + capability, "yes"), fact(target, "condition", value))
                c = Constraint(rule, (place,), (), BindingTerms(("block",),
                    triggers=(f"fact={target}|condition|sealed",)), AUTHORED)
                access = InformationSnapshot((Foundation("independent", "elsewhere", "era",
                    tuple(Identity(s) for s in (actor, place, target)), f, constraints=(c,)),))
                s = AdjudicationSession(access, (Method(method, "interact", capability),))
                a = Attempt("one", actor, "interact", method, target, place, 0,
                            ActivityAuthorization("interact", method))
                self.assertEqual(outcome(s, s.step(a)), expected)
                self.assertIn(target + ":condition", s.state.history[-1].assessment.premise_ids)

    def test_relationship_retrieval_expands_hidden_binding_scope(self):
        edge = Relationship("rule-link", "target", "governed_by", "doctrine", AUTHORED)
        c = Constraint(HIDDEN, ("doctrine",), ("cross",), BindingTerms(("block",)), AUTHORED)
        # Deliberate shallow query demonstrates omission evidence, not a claim
        # that InformationAccess can certify upstream relevance completeness.
        access = InformationSnapshot((Foundation("linked", "setting", "era",
            tuple(Identity(s) for s in ("actor", "target", "place", "rope", "scroll", "potion", "lever", "agreement", "doctrine")),
            premises(), (edge,), (c,)),))
        shallow = access.applicable_constraints(ConstraintQuery(("target",), "cross", 0))
        self.assertEqual(shallow.missing_expected((HIDDEN,)), (HIDDEN,))
        s = session(info=access)
        request = replace(attempt(s), relations=("governed_by",))
        reply = s.step(request)
        self.assertEqual(outcome(s, reply), "blocked")
        self.assertIn(HIDDEN, s.state.history[-1].assessment.premise_ids)
        self.assertIn("rule-link", s.state.history[-1].assessment.premise_ids)
        self.assertNotIn(HIDDEN, json.dumps(reply))

    def test_current_unavailable_truth_never_falls_back_to_authored_truth(self):
        current = (Fact("unknown-current-anchor", "target", "anchor", None,
                        Source("accepted", "world_simulation"), availability="established_unavailable"),)
        s = session(info=snapshot(current=current))
        reply = self.assertUnchanged(s, attempt(s), propose_assessed, stage="retrieval", status="unresolved")
        self.assertEqual(reply["reason"], "established_unavailable")

    def test_invalid_mechanics_inputs_do_not_publish(self):
        s = session(draw=True)
        self.assertUnchanged(s, attempt(s), propose_assessed, stage="adjudication", status="unresolved")

    def test_character_grant_does_not_become_authoritative_fact(self):
        fs = tuple(replace(f, epistemic="claim", holder="actor") if f.predicate == "anchor" else f for f in premises())
        s = session(facts=fs, grants=(AccessGrant("target:anchor", "actor", ACCESS),))
        self.assertUnchanged(s, attempt(s), propose_assessed, stage="retrieval", status="unresolved")

    def test_immaterial_missing_exception_does_not_block_ordinary_method(self):
        fs = tuple(f for f in premises() if f.predicate != "permit")
        s = session(facts=fs, constraints=(ward(),))
        self.assertEqual(outcome(s, s.step(attempt(s, "hook"))), "full")
        # For the triggered levitation method, the same missing exception is
        # material: it could change whether the binding blocks the attempt.
        self.assertUnchanged(s, attempt(s, "float"), propose_assessed,
                             stage="retrieval", status="unresolved")

    def test_decisive_supported_condition_is_order_independent_with_unavailable_operand(self):
        c = ward()
        for prerequisites in (("fact=missing|slot|yes", "action=other"),
                              ("action=other", "fact=missing|slot|yes")):
            s = session(constraints=(replace(c, terms=replace(c.terms, prerequisites=prerequisites)),))
            self.assertEqual(outcome(s, s.step(attempt(s, "float"))), "full")

    def test_inquiry_without_knowledge_reads_observation_only_and_changes_nothing(self):
        info = snapshot(constraints=(ward(),))
        draws = unittest.mock.Mock(side_effect=AssertionError("Inquiry must not draw"))
        s = session(info=info, draw=draws)
        request = attempt(s, "float")
        s.step(request)
        before = s.state
        ask = replace(request, at=s.state.at, authorization=replace(request.authorization, intent="inquiry"))
        proposal = unittest.mock.Mock(side_effect=AssertionError("Inquiry must not propose"))
        with patch.object(info, "resolve", side_effect=AssertionError("No internal facts")), \
                patch.object(info, "applicable_constraints", side_effect=AssertionError("No internal constraints")), \
                patch.object(s, "_assess", side_effect=AssertionError("No action assessment")):
            reply = s.step(ask, proposal)
        self.assertEqual(reply["status"], "inquired")
        self.assertEqual(reply["context"]["player_intent"]["authorization"], "inquiry")
        text = build_realization_request(reply["context"])["input"]
        self.assertIn("Earlier accepted observation: Your ascent stops", text)
        self.assertIn("alone does not establish its cause", text)
        for private in (HIDDEN, "binding_terms", "premise_ids", "established_unavailable"):
            self.assertNotIn(private, text)
        self.assertEqual(s.state, before)
        proposal.assert_not_called()
        draws.assert_not_called()
        reply["context"]["developments"][0]["meaning"] = "tampered"
        self.assertEqual(s.state, before)

    def test_inquiry_preserves_granted_knowledge_inference_and_report_attribution(self):
        knowledge = fact("actor", "lore", "Some barriers distinguish methods of ascent.")
        inferred = fact("actor", "inference", "The effect may depend on the chosen method.",
                        epistemic="inference", holder="actor")
        report = fact("actor", "report", "A guide reports that old barriers once stood here.",
                      epistemic="claim", holder="actor")
        secret = fact("target", "cause", HIDDEN)
        grants = tuple(AccessGrant(f.id, "actor", ACCESS) for f in (knowledge, inferred, report))
        s = session(facts=(*premises(), knowledge, inferred, report, secret), constraints=(ward(),), grants=grants)
        request = attempt(s, "float")
        s.step(request)
        before = s.state
        reply = s.step(replace(request, at=s.state.at,
                               authorization=replace(request.authorization, intent="inquiry")))
        self.assertEqual(reply["status"], "inquired")
        records = {r["id"]: r for r in reply["context"]["developments"]}
        self.assertEqual(records["known-actor:lore"]["status"], "established")
        self.assertEqual(records["known-actor:inference"]["status"], "inferred")
        self.assertIn("may", records["known-actor:inference"]["meaning"])
        self.assertEqual(records["known-actor:report"]["status"], "reported")
        self.assertIn("A guide reports", records["known-actor:report"]["meaning"])
        self.assertEqual(records["known-actor:report"]["source"], AUTHORED.ref)
        self.assertNotIn(HIDDEN, build_realization_request(reply["context"])["input"])
        self.assertEqual(s.state, before)

    def test_inquiry_does_not_grant_expired_or_other_character_information(self):
        lore = fact("actor", "lore", "RESTRICTED-LORE")
        for grant in (AccessGrant(lore.id, "actor", ACCESS, Period(0, 1)),
                      AccessGrant(lore.id, "target", ACCESS)):
            s = session(facts=(*premises(), lore), constraints=(ward(),), grants=(grant,))
            request = attempt(s, "float")
            s.step(request)  # elapsed 1: no legitimate access supplied in the accepted context
            before = s.state
            reply = s.step(replace(request, at=s.state.at,
                                   authorization=replace(request.authorization, intent="inquiry")))
            self.assertEqual(reply["status"], "inquired")
            self.assertNotIn("RESTRICTED-LORE", json.dumps(reply["context"]))
            self.assertEqual(s.state, before)

    def test_inquiry_requires_this_characters_accepted_observation(self):
        s = session(constraints=(ward(),))
        request = attempt(s, "float")
        ask = replace(request, authorization=replace(request.authorization, intent="inquiry"))
        self.assertUnchanged(s, ask, propose_assessed, stage="authorization", status="control")
        s.step(request)
        self.assertUnchanged(s, replace(ask, actor="target", at=s.state.at), propose_assessed)

    def test_inquiry_failure_is_read_only_and_does_not_publish_diagnostics(self):
        s = session(constraints=(ward(),))
        request = attempt(s, "float")
        s.step(request)
        ask = replace(request, at=s.state.at, authorization=replace(request.authorization, intent="inquiry"))
        with patch("engine.information_adjudication.validate_context", side_effect=ValueError(HIDDEN)):
            reply = self.assertUnchanged(s, ask, propose_assessed, stage="presentation", status="unresolved")
        self.assertNotIn(HIDDEN, json.dumps(reply))

    def test_inquiry_after_removal_preserves_earlier_observation_and_current_consequences(self):
        s = session(constraints=(ward(),))
        request = attempt(s, "float")
        s.step(request)
        s.step(attempt(s, "unweave", binding=HIDDEN))
        before = s.state
        reply = s.step(replace(request, at=s.state.at,
                               authorization=replace(request.authorization, intent="inquiry")))
        self.assertEqual(reply["status"], "inquired")
        self.assertIn("ascent stops", reply["context"]["developments"][0]["meaning"])
        self.assertEqual(reply["context"]["developments"][0]["time"], "Elapsed 1")
        self.assertEqual(s.state, before)
        self.assertEqual(outcome(s, s.step(attempt(s, "float"))), "full")

    def test_rejected_draw_is_provisional_retry_samples_again_and_acceptance_is_reused(self):
        draws = unittest.mock.Mock(side_effect=(1, 6))
        charged_hook = replace(methods()[0], costs=(("rope", 1),))
        s = session(draw=draws, method_rules=(charged_hook,))
        request = attempt(s)
        before = s.state
        self.assertUnchanged(s, request, lambda a: replace(propose_assessed(a), result="full"))
        self.assertEqual(s.state, before)  # sample 1 is not an accepted fictional failure
        self.assertEqual(draws.call_count, 1)
        self.assertEqual(outcome(s, s.step(request)), "full")  # same intended attempt, sample 6
        self.assertEqual(s.state.history[0].assessment.draw, 6)
        self.assertEqual(len(s.state.history), 1)
        self.assertIn(("actor", "rope", 0), s.state.inventory)
        accepted = s.state
        replay = s.step(replace(request, at=s.state.at))
        self.assertEqual(replay["status"], "reused")
        self.assertEqual(s.state, accepted)
        self.assertEqual(draws.call_count, 2)


if __name__ == "__main__":
    unittest.main()
