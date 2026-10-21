"""Offline interface tests; fixtures supply authority, never general adjudication.

Failures identify representation, retrieval or an owning-adjudicator dependency.
No test claims to verify general gameplay outcomes from returned information.
"""
from dataclasses import FrozenInstanceError, replace
from itertools import permutations
import socket
import unittest
from unittest.mock import patch

from engine.information_resolution import (
    AccessGrant, BindingTerms, CanonicalConflict, Constraint, ConstraintQuery,
    Fact, Foundation, Identity, InformationAccess, InformationSnapshot, Period,
    Query, RepresentationError, Relationship, Source,
)


AUTHORED = Source("canon:setting", "authored")
WORLD = Source("world:accepted-snapshot", "world_simulation", ("resolution:accepted",))
CHARACTER = Source("character:access", "character", ("legitimate observation",))


def fact(id, subject, predicate, value, **kwargs):
    return Fact(id, subject, predicate, value, kwargs.pop("source", AUTHORED), **kwargs)


def foundation(id="setting", *, subjects=(), facts=(), relationships=(), constraints=()):
    return Foundation(id, "test-setting", "test-era", tuple(Identity(s) for s in subjects),
                      facts, relationships, constraints)


def grant(id, character="player", **kwargs):
    return AccessGrant(id, character, CHARACTER, **kwargs)


def denied(*args, **kwargs):
    raise AssertionError("Live network forbidden in information-core tests")


def consumer(access: InformationAccess, subject, at):
    """A consumer depends only on the public access operations and value records."""
    identity = access.identity(subject)
    result = access.resolve(Query((subject,), at))
    constraints = access.applicable_constraints(ConstraintQuery((subject,), "inspect", at))
    return identity, tuple((f.predicate, f.value, f.epistemic) for f in result.facts), constraints


class InformationTests(unittest.TestCase):
    def setUp(self):
        for guard in (patch("socket.create_connection", side_effect=denied),
                      patch.object(socket.socket, "connect", side_effect=denied)):
            guard.start()
            self.addCleanup(guard.stop)

    def selected(self, result, *ids):
        self.assertEqual(result.missing_expected(ids), (), "retrieval: expected information omitted")

    def test_composition_accumulates_across_domains_and_is_order_independent(self):
        packs = (
            foundation("temple", subjects=("temple", "faction", "deity"),
                       facts=(fact("temple.name", "temple", "name", "Night Temple"),)),
            foundation("faction", subjects=("faction",),
                       facts=(fact("faction.name", "faction", "name", "Silver Veil"),)),
            foundation("deity", subjects=("deity",),
                       facts=(fact("deity.doctrine", "deity", "doctrine", "Protect initiates"),)),
        )
        results = [InformationSnapshot(p).resolve(Query(("temple", "faction", "deity"), 2))
                   for p in permutations(packs)]
        self.assertTrue(all(result == results[0] for result in results))
        self.selected(results[0], "temple.name", "faction.name", "deity.doctrine")

    def test_supported_canonical_contradiction_has_no_specificity_or_order_precedence(self):
        for subject, predicate in (("guard", "rank"), ("spell", "duration"), ("deity", "doctrine")):
            with self.subTest(domain=subject):
                broad = foundation("broad", subjects=(subject,),
                                   facts=(fact("broad.fact", subject, predicate, "one"),))
                local = foundation("specific-local", subjects=(subject,),
                                   facts=(fact("local.fact", subject, predicate, "two"),))
                for packs in permutations((broad, local)):
                    with self.assertRaises(CanonicalConflict) as raised:
                        InformationSnapshot(packs)
                    self.assertEqual(raised.exception.conflicts, (("broad.fact", "local.fact"),))

    def test_compatible_repetition_preserves_both_source_references(self):
        a = fact("a", "deity", "doctrine", "Protect initiates")
        b = replace(a, id="b", source=Source("canon:temple", "authored"))
        core = InformationSnapshot((foundation(subjects=("deity",), facts=(a, b)),))
        result = core.resolve(Query(("deity",), 1))
        self.assertEqual({s.source.ref for s in result.selections}, {a.source.ref, b.source.ref})

    def test_explicit_distinctions_do_not_create_false_canonical_conflicts(self):
        records = (
            fact("past", "temple", "doctrine", "Old law", period=Period(0, 5)),
            fact("present", "temple", "doctrine", "New law", period=Period(5)),
            fact("secret", "temple", "secret_practice", "Defy doctrine"),
            fact("claim", "temple", "doctrine", "Competing belief", epistemic="claim", holder="priest"),
        )
        core = InformationSnapshot((foundation(subjects=("temple", "priest"), facts=records),))
        self.selected(core.resolve(Query(("temple",), 5)), "present", "secret", "claim")
        self.assertNotIn("past", {f.id for f in core.resolve(Query(("temple",), 5)).facts})

    def test_guard_bribe_reassignment_promotion_and_historical_meaning(self):
        guard = "guard:seren"
        initial = fact("guard.initial-rank", guard, "rank", "Guard")
        history = (
            fact("guard.bribe", guard, "accepted_bribe", "Accepted five silver at North Gate",
                 source=WORLD, period=Period(1, 2)),
            fact("guard.assignment", guard, "assignment", "North Gate",
                 source=WORLD, period=Period(0, 5)),
        )
        current = (
            fact("guard.reassigned", guard, "assignment", "Palace", source=WORLD, period=Period(5)),
            fact("guard.promoted", guard, "rank", "Captain", source=WORLD, period=Period(8)),
        )
        core = InformationSnapshot((foundation(subjects=(guard,), facts=(initial,)),),
                                   current=current, history=history)
        now = core.resolve(Query((guard,), 10))
        self.assertEqual({f.value for f in now.facts}, {"Palace", "Captain"})
        past = core.resolve(Query((guard,), 10, include_history=True))
        self.selected(past, *(f.id for f in (*history, *current)), initial.id)
        self.assertEqual(core.identity(guard), Identity(guard))
        self.assertEqual(next(f for f in past.facts if f.id == "guard.bribe"), history[0])
        self.assertEqual({s.temporal for s in past.selections if s.record_id == "guard.bribe"},
                         {"historical"})
        self.assertEqual(history[0].source.basis, ("resolution:accepted",))
        # A known earlier record is not promoted to current merely because it exists.
        self.assertEqual(core.resolve(Query((guard,), 10, ("accepted_bribe",))).facts, ())

    def test_matron_competing_interests_and_legitimate_knowledge(self):
        matron, player = "matron:veyr", "player"
        records = (
            fact("veyr.obligation", matron, "obligation", "Protect the temple treasury"),
            fact("veyr.objective", matron, "objective", "Keep the faction alliance"),
            fact("veyr.belief", matron, "player_loyalty", "Doubtful", epistemic="belief", holder=matron),
            fact("veyr.claim", matron, "player_loyalty", "Proven", epistemic="claim", holder=player),
            fact("secret", "faction", "plan", "Replace Veyr"),
        )
        relation = Relationship("veyr.faction", matron, "member_of", "faction", AUTHORED)
        core = InformationSnapshot((foundation(subjects=(matron, player, "faction"),
                                               facts=records, relationships=(relation,)),))
        query = Query((matron,), 2, relations=("member_of",), depth=1)
        internal = core.resolve(query)
        self.selected(internal, *(f.id for f in records))
        accessible = core.for_character(query, matron, tuple(grant(f.id, matron) for f in records[:4])
                                        + (grant(relation.id, matron),))
        self.assertNotIn("secret", repr(accessible))
        self.assertEqual({f.epistemic for f in accessible.facts}, {"fact", "belief", "claim"})
        self.assertEqual({f.value for f in accessible.facts if f.predicate == "player_loyalty"},
                         {"Doubtful", "Proven"})
        # No concession, loyalty decision or NPC action is inferred by retrieval.

    def ward_snapshot(self, *, removed=False):
        removal_time = 9
        ward = Constraint("ward:hidden", ("tower",), ("levitate",),
                          BindingTerms(("Prevent levitation",),
                                       exceptions=("Bearer of the ward seal",),
                                       termination=("Accepted ritual removal",)), WORLD,
                          Period(0, removal_time if removed else None))
        history = (() if not removed else
                   (fact("ward.removed", "tower", "ward_event", "Ritually removed",
                         source=WORLD, period=Period(removal_time, removal_time + 1)),))
        return InformationSnapshot((foundation(subjects=("tower", "player")),),
                                   constraints=(ward,), history=history)

    def test_hidden_ward_is_retrieved_without_player_request_or_knowledge(self):
        core = self.ward_snapshot()
        query = ConstraintQuery(("tower",), "levitate", 3)
        internal = core.applicable_constraints(query)
        self.selected(internal, "ward:hidden")
        self.assertEqual(internal.constraints[0].terms.effects, ("Prevent levitation",))
        player = core.for_character(query, "player", ())
        self.assertEqual(player.constraints, ())
        self.assertNotIn("ward:hidden", repr(player))
        revealed = core.for_character(query, "player", (grant("ward:hidden"),))
        self.selected(revealed, "ward:hidden")
        self.assertEqual(core.applicable_constraints(ConstraintQuery(("tower",), "walk", 3)).constraints, ())

    def test_legitimate_supplied_ward_removal_changes_current_scope_not_history(self):
        before, after = self.ward_snapshot(), self.ward_snapshot(removed=True)
        self.selected(before.applicable_constraints(ConstraintQuery(("tower",), "levitate", 10)), "ward:hidden")
        self.assertEqual(after.applicable_constraints(ConstraintQuery(("tower",), "levitate", 9)).constraints, ())
        self.selected(after.applicable_constraints(ConstraintQuery(("tower",), "levitate", 8)), "ward:hidden")
        self.selected(after.resolve(Query(("tower",), 11, include_history=True)), "ward.removed")
        # Snapshots supply the accepted change. No authoritative mutation API is implemented.

    def test_binding_agreement_returns_conditions_exclusions_and_all_material_terms(self):
        terms = BindingTerms(
            effects=("Escort the pilgrims",), prerequisites=("Fee paid",),
            triggers=("Pilgrims enter pass",), exclusions=("No escort for armed invaders",),
            exceptions=("Medical emergency permits delay",),
            termination=("Pilgrims reach sanctuary", "End of tenth day"),
            revocation=("Both parties release the oath",))
        agreement = Constraint("agreement", ("guide", "pilgrims", "pass"), ("travel",), terms, WORLD,
                               Period(2, 10))
        core = InformationSnapshot((foundation(subjects=("guide", "pilgrims", "pass")),),
                                   constraints=(agreement,))
        for subject in agreement.subjects:
            self.assertEqual(core.applicable_constraints(ConstraintQuery((subject,), "travel", 4))
                             .constraints[0].terms, terms)
        for at in (1, 10):
            self.assertEqual(core.applicable_constraints(ConstraintQuery(("pass",), "travel", at)).constraints, ())
        self.assertEqual(core.applicable_constraints(ConstraintQuery(("pass",), "trade", 4)).constraints, ())
        self.assertEqual(core.applicable_constraints(ConstraintQuery(("elsewhere",), "travel", 4)).constraints, ())
        # Applying the fee/exclusion/effect is an owning-adjudicator dependency, not this core's job.

    def cross_domain(self, reverse=False):
        edges = (
            Relationship("temple.faction", "temple", "affiliated_with", "faction", AUTHORED),
            Relationship("faction.deity", "faction", "worships", "deity", AUTHORED),
            Relationship("deity.temple", "deity", "patron_of", "temple", AUTHORED),
            Relationship("temple.shop", "temple", "near", "shop", AUTHORED),
        )
        facts = (fact("doctrine", "deity", "doctrine", "Protect initiates"),
                 fact("shop.stock", "shop", "stock", "Rope"))
        pack = foundation(subjects=("temple", "faction", "deity", "shop", "player"),
                          facts=facts, relationships=tuple(reversed(edges)) if reverse else edges)
        return InformationSnapshot((pack,))

    def test_cross_domain_selective_traversal_has_paths_and_stable_diagnostics(self):
        core = self.cross_domain()
        query = Query(("temple",), 1, relations=("affiliated_with", "worships"), depth=2)
        result = core.resolve(query)
        self.selected(result, "doctrine", "temple.faction", "faction.deity")
        self.assertNotIn("shop.stock", {f.id for f in result.facts})
        self.assertEqual(next(s.via for s in result.selections if s.record_id == "doctrine"),
                         ("temple.faction", "faction.deity"))
        self.assertEqual(result, self.cross_domain(reverse=True).resolve(query))
        shallow = core.resolve(replace(query, depth=1))
        self.assertEqual(shallow.missing_expected(("doctrine",)), ("doctrine",))
        # Known fixture representation + this mismatch identifies a retrieval failure.
        cyclic = core.resolve(replace(query, relations=query.relations + ("patron_of",), depth=50))
        self.assertEqual(len(cyclic.relationships), 3)

    def test_character_traversal_requires_access_to_edges_as_well_as_content(self):
        core = self.cross_domain()
        query = Query(("temple",), 1, relations=("affiliated_with", "worships"), depth=2)
        self.assertEqual(core.for_character(query, "player", (grant("doctrine"),)).facts, ())
        result = core.for_character(query, "player", tuple(grant(id) for id in
                                    ("doctrine", "temple.faction", "faction.deity")))
        self.selected(result, "doctrine")
        self.assertTrue(all(s.access_source == CHARACTER for s in result.selections))

    def test_reference_catalogs_do_not_establish_instances_or_character_capability(self):
        domains = ("monster", "spell", "equipment", "deity", "faction", "organization", "rule", "condition")
        definitions = tuple(Identity(f"{d}:definition", "definition") for d in domains)
        records = tuple(fact(f"{d}.properties", f"{d}:definition", "properties", f"{d} reference terms")
                        for d in domains)
        pack = Foundation("catalog", "test-setting", "test-era", definitions, records)
        core = InformationSnapshot((pack,))
        for d in domains:
            with self.subTest(domain=d):
                definition, values, _ = consumer(core, f"{d}:definition", 1)
                self.assertEqual(definition.kind, "definition")
                self.assertEqual(values[0][1], f"{d} reference terms")
                missing = core.resolve(Query((f"{d}:instance",), 1, ("exists",)))
                self.assertEqual(missing.availability[0].classification, "unspecified")
                self.assertIsNone(core.identity(f"{d}:instance"))
        self.assertEqual(core.resolve(Query(("player",), 1, ("knows_spell", "can_cast"))).facts, ())
        monster = Identity("monster:one", "instance", "monster:definition")
        current = fact("monster.present", monster.id, "location", "tower", source=WORLD)
        instantiated = InformationSnapshot((pack,), identities=(monster,), current=(current,))
        self.assertEqual(instantiated.identity(monster.id).definition_id, "monster:definition")
        self.selected(instantiated.resolve(Query((monster.id,), 1)), "monster.present")
        self.assertEqual(core.resolve(Query((monster.id,), 1)).facts, ())

    def test_availability_distinguishes_unavailable_unspecified_uncertain_and_claim(self):
        records = (
            fact("unavailable", "subject", "oath", None, availability="established_unavailable"),
            fact("uncertain", "subject", "identity", "Not yet resolved", epistemic="uncertain"),
            fact("claim", "subject", "location", "North", epistemic="claim", holder="witness"),
            fact("inference", "subject", "motive", "May be afraid", epistemic="inference", holder="witness"),
        )
        core = InformationSnapshot((foundation(subjects=("subject", "witness"), facts=records),))
        result = core.resolve(Query(("subject",), 1, ("oath", "identity", "location", "motive", "name")))
        statuses = {a.predicate: a.classification for a in result.availability}
        self.assertEqual(statuses, {"oath": "established_unavailable", "identity": "uncertain",
                                    "location": "available", "motive": "available", "name": "unspecified"})
        self.assertEqual({f.epistemic for f in result.facts}, {"fact", "uncertain", "claim", "inference"})

    def test_unavailable_current_information_never_falls_back_to_authored_value(self):
        initial = fact("initial", "guard", "assignment", "Gate")
        unavailable = fact("known", "guard", "assignment", None, source=WORLD,
                           availability="established_unavailable")
        core = InformationSnapshot((foundation(subjects=("guard",), facts=(initial,)),), current=(unavailable,))
        result = core.resolve(Query(("guard",), 1))
        self.assertEqual(result.facts, (unavailable,))
        self.assertEqual(result.availability[0].classification, "established_unavailable")

    def test_known_binding_with_unavailable_terms_remains_in_constraint_results(self):
        unavailable = Constraint("known.binding", ("tower",), ("levitate",), None, WORLD,
                                 availability="established_unavailable")
        pack = foundation(subjects=("tower", "player"))
        core = InformationSnapshot((pack,), constraints=(unavailable,))
        query = ConstraintQuery(("tower",), "levitate", 4)
        result = core.applicable_constraints(query)
        self.selected(result, "known.binding")
        self.assertIsNone(result.constraints[0].terms)
        self.assertEqual(result.availability[0].classification, "established_unavailable")
        self.assertEqual(core.for_character(query, "player", ()).availability, ())
        accessible = core.for_character(query, "player", (grant("known.binding"),))
        self.assertEqual(accessible.availability, result.availability)
        with self.assertRaises(RepresentationError):
            InformationSnapshot((pack,), constraints=(replace(unavailable, availability="available"),))
        with self.assertRaises(RepresentationError):
            InformationSnapshot((pack,), constraints=(replace(unavailable, terms=BindingTerms(("Invented",))),))

    def test_claims_and_inferences_never_override_current_objective_truth(self):
        truth = fact("truth", "guard", "location", "Gate")
        report = fact("report", "guard", "location", "Palace", source=CHARACTER,
                      epistemic="claim", holder="witness")
        core = InformationSnapshot((foundation(subjects=("guard", "witness"), facts=(truth,)),), current=(report,))
        self.selected(core.resolve(Query(("guard",), 1)), "truth", "report")

    def test_character_grants_are_individual_time_bounded_and_metadata_is_safe(self):
        visible = fact("known", "guard", "location", "Gate")
        secret = fact("hidden", "guard", "location", "Palace", source=WORLD, period=Period(3))
        core = InformationSnapshot((foundation(subjects=("guard", "player", "other"), facts=(visible,)),),
                                   current=(secret,))
        query = Query(("guard",), 5, ("location", "secret_name"))
        result = core.for_character(query, "player", (grant("known"),))
        self.assertEqual(result.facts, (visible,))
        self.assertNotIn("hidden", repr(result))
        self.assertEqual(result.selections[0].temporal, "retained")
        self.assertEqual(result.availability[-1].classification, "not_accessible")
        for grants in ((grant("known", "other"),), (grant("known", period=Period(0, 5)),)):
            self.assertEqual(core.for_character(query, "player", grants).facts, ())
        self.assertEqual(core.resolve(query).facts, (secret,))

    def test_internal_and_character_absence_cannot_disclose_hidden_existence(self):
        a = foundation(subjects=("place", "player"), facts=(fact("secret", "place", "secret", "Hidden"),))
        b = replace(a, facts=())
        query = Query(("place",), 1, ("secret",))
        self.assertEqual(InformationSnapshot((a,)).for_character(query, "player", ()),
                         InformationSnapshot((b,)).for_character(query, "player", ()))

    def test_immutable_input_and_output_and_deterministic_rebuild(self):
        record = fact("f", "subject", "name", "Original")
        pack = foundation(subjects=("subject",), facts=(record,))
        core = InformationSnapshot((pack,))
        before = core.resolve(Query(("subject",), 1))
        with self.assertRaises(FrozenInstanceError):
            before.facts[0].value = "Changed"
        with self.assertRaises(FrozenInstanceError):
            pack.facts = ()
        self.assertEqual(consumer(core, "subject", 1), consumer(InformationSnapshot((pack,)), "subject", 1))
        self.assertEqual(before, core.resolve(Query(("subject",), 1)))

    def test_same_operations_across_unrelated_identities_and_information_domains(self):
        for subject, domain in (("actor:17", "promise"), ("artifact:9", "equipment"),
                                ("order:3", "religion"), ("spell:4", "magic")):
            with self.subTest(domain=domain):
                related = f"{domain}:reference"
                edge = Relationship("edge", subject, "governed_by", related, AUTHORED)
                binding = Constraint("binding", (related,), ("use",),
                                     BindingTerms((f"Respect {domain} conditions",)), AUTHORED)
                record = fact("record", related, "terms", f"{domain} reference meaning")
                pack = foundation(subjects=(subject, related), facts=(record,),
                                  relationships=(edge,), constraints=(binding,))
                core = InformationSnapshot((pack,))
                result = core.resolve(Query((subject,), 5, relations=("governed_by",), depth=1))
                self.selected(result, "record", "edge")
                # Consumer uses the selected subjects, never an internal index.
                scope = (subject,) + tuple(e.target for e in result.relationships)
                constraints = core.applicable_constraints(ConstraintQuery(scope, "use", 5))
                self.selected(constraints, "binding")

    def test_multiple_paths_choose_a_stable_shortest_path_and_stop_at_depth(self):
        edges = (
            Relationship("b", "start", "link", "right", AUTHORED),
            Relationship("a", "start", "link", "left", AUTHORED),
            Relationship("d", "right", "link", "end", AUTHORED),
            Relationship("c", "left", "link", "end", AUTHORED),
        )
        pack = foundation(subjects=("start", "left", "right", "end"),
                          facts=(fact("end.fact", "end", "name", "End"),), relationships=edges)
        query = Query(("start",), 1, relations=("link",), depth=2)
        result = InformationSnapshot((pack,)).resolve(query)
        self.assertEqual(next(s.via for s in result.selections if s.record_id == "end.fact"), ("a", "c"))
        self.assertEqual(result, InformationSnapshot((replace(pack, relationships=tuple(reversed(edges))),))
                         .resolve(query))

    def test_character_recall_keeps_historical_meaning_and_report_attribution(self):
        report = fact("report", "guard", "assignment", "Reported at Gate", source=CHARACTER,
                      epistemic="claim", holder="witness", period=Period(1, 3))
        core = InformationSnapshot((foundation(subjects=("guard", "player", "witness")),), history=(report,))
        query = Query(("guard",), 8, include_history=True)
        result = core.for_character(query, "player", (grant("report"),))
        self.assertEqual(result.facts, (report,))
        self.assertEqual(result.selections[0].temporal, "historical")
        self.assertEqual(result.facts[0].holder, "witness")
        self.assertEqual(result.facts[0].source, CHARACTER)

    def test_expired_edges_are_not_traversed_and_global_action_constraints_are_selected(self):
        edge = Relationship("edge", "temple", "worships", "deity", AUTHORED, Period(0, 5))
        rule = Constraint("rule", ("temple",), (), BindingTerms(("Keep oath",)), AUTHORED)
        pack = foundation(subjects=("temple", "deity"), relationships=(edge,), constraints=(rule,),
                          facts=(fact("doctrine", "deity", "law", "Old law"),))
        core = InformationSnapshot((pack,))
        self.assertEqual(core.resolve(Query(("temple",), 5, relations=("worships",), depth=1)).facts, ())
        self.selected(core.applicable_constraints(ConstraintQuery(("temple",), "unusual_action", 6)), "rule")

    def test_access_basis_order_cannot_change_character_results(self):
        core = InformationSnapshot((foundation(subjects=("subject", "player"),
                                               facts=(fact("f", "subject", "name", "Name"),)),))
        grants = (grant("f"), AccessGrant("f", "player", replace(CHARACTER, basis=("prior encounter",))))
        query = Query(("subject",), 1)
        self.assertEqual(core.for_character(query, "player", grants),
                         core.for_character(query, "player", tuple(reversed(grants))))

    def test_representation_validation_rejects_ambiguous_or_mutable_inputs(self):
        base = foundation(subjects=("subject", "player"), facts=(fact("f", "subject", "name", "One"),))
        bad = (
            lambda: InformationSnapshot((base, replace(base, id="other", era="other-era"))),
            lambda: InformationSnapshot((base,), identities=(Identity("subject", "definition"),)),
            lambda: InformationSnapshot((replace(base, facts=(replace(base.facts[0], subject="unknown"),)),)),
            lambda: InformationSnapshot((replace(base, facts=(replace(base.facts[0], epistemic="claim"),)),)),
            lambda: InformationSnapshot((replace(base, facts=(replace(base.facts[0], period=Period(2, 2)),)),)),
            lambda: InformationSnapshot((replace(base, facts=(replace(base.facts[0], source=Source("x", "provider")),)),)),
            lambda: InformationSnapshot((base,), identities=(Identity("instance", "instance", "missing"),)),
            lambda: InformationSnapshot((base,), current=(base.facts[0],)),
            lambda: InformationSnapshot((replace(base, facts=list(base.facts)),)),
            lambda: InformationSnapshot((base,), current=(fact("a", "subject", "x", "A", source=WORLD),
                                                          fact("b", "subject", "x", "B", source=WORLD))),
        )
        for index, construct in enumerate(bad):
            with self.subTest(case=index), self.assertRaises(RepresentationError):
                construct()

    def test_invalid_query_and_access_grants_fail_closed(self):
        core = InformationSnapshot((foundation(subjects=("subject", "player"),
                                               facts=(fact("f", "subject", "name", "One"),)),))
        for query in (Query(("subject",), True), Query(("subject",), 1, depth=-1),
                      Query(["subject"], 1), Query(("subject",), 1, include_history="yes")):
            with self.assertRaises(RepresentationError):
                core.resolve(query)
        for access in ((AccessGrant("f", "player", AUTHORED),),
                       (AccessGrant("f", "player", Source("access", "character")),),
                       (grant("unknown"),)):
            with self.assertRaises(RepresentationError):
                core.for_character(Query(("subject",), 1), "player", access)


if __name__ == "__main__":
    unittest.main()
