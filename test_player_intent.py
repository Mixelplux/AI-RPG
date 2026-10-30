"""Offline V1 contract and Coordinator evidence, no inference experiments."""
from dataclasses import replace
import json
import socket
import unittest
from unittest.mock import patch

from engine.gameplay_coordination import Coordinator, Interpretation
from engine.player_intent import InvalidInterpretation, normalize, MAX_OUTPUT_BYTES, MAX_TEXT
from test_fixtures.coordination_suppliers import SituatedAuthority, context


def intention(**changes):
    return dict(id="i1", mode="action", commitment="now", activity="Open the door", **changes)


def payload(item=None, **changes):
    value = dict(version=1, intentions=[item or intention()], relationships=[], ambiguities=[])
    value.update(changes)
    return value


def wire(item=None, **changes):
    return json.dumps(payload(item, **changes))


def changed(**changes):
    value = intention()
    value.update(changes)
    return value


class Contract(unittest.TestCase):
    def reject(self, value, **kwargs):
        with self.assertRaises(InvalidInterpretation):
            normalize(json.dumps(value), **kwargs)

    def test_canonical_exact_serialization_and_copy_isolation(self):
        value = payload(changed(activity="  Open the door  ", method="use the handle"))
        result = normalize(json.dumps(value))
        self.assertEqual(result.json, '{"ambiguities":[],"intentions":[{"activity":"Open the door",'
            '"commitment":"now","id":"i1","method":"use the handle","mode":"action"}],'
            '"relationships":[],"version":1}')
        copy = result.to_dict()
        copy["intentions"][0]["commitment"] = "none"
        self.assertEqual(normalize(result.json), result)
        self.assertNotIn("constraints", result.to_dict()["intentions"][0])

    def test_wrong_shapes_types_versions_and_missing_fields(self):
        for value in ([], None, {}, payload(version=True), payload(version=1.0),
                      payload(version=2), payload(intentions={}), payload(relationships=None),
                      payload(ambiguities=""), payload(changed(id="a space")),
                      payload(changed(mode=[])), payload(changed(commitment=1)),
                      payload(changed(activity=" ")), payload(changed(targets="door"))):
            with self.subTest(value=value):
                self.reject(value)
        for key in ("id", "activity", "mode", "commitment"):
            item = intention()
            del item[key]
            self.reject(payload(item))

    def test_null_and_duplicate_arrays_and_unknown_fields(self):
        optional = ("goal", "targets", "method", "constraints", "conditions", "stop_at",
                    "context_refs", "candidate_domains", "source")
        for key in optional:
            with self.subTest(key=key):
                self.reject(payload(changed(**{key: None})))
        for key in ("targets", "constraints", "conditions", "stop_at", "context_refs", "candidate_domains"):
            self.reject(payload(changed(**{key: ["same", "same"]})))
        for key in ("execute", "authorized", "outcome", "success", "roll", "cost", "elapsed_time",
                    "world_state", "npc_decision", "queue", "tool_calls", "missing_information"):
            with self.subTest(authority=key):
                self.reject(payload(**{key: True}))
                self.reject(payload(changed(**{key: True})))
        self.reject(payload(candidate_domains=["authorization"]))
        self.reject(payload(changed(candidate_domains=["authorization"])))
        self.reject(payload(intentions=[{}]))

    def test_malformed_duplicate_keys_non_json_and_deep_output(self):
        for raw in ("", "null", "{} trailing", "```json\n{}\n```", '{"version":1,"version":1}',
                    wire().replace('"now"', 'NaN'), wire().replace('"now"', 'Infinity'),
                    wire().replace('"now"', '{"a":1,"a":2}'), '[' * 1100 + ']' * 1100,
                    wire().replace("Open the door", "\\ud800")):
            with self.subTest(raw=raw[:60]), self.assertRaises(InvalidInterpretation):
                normalize(raw)
        for raw in (b"{}", {}, None):
            with self.assertRaises(InvalidInterpretation):
                normalize(raw)

    def test_bounds(self):
        self.reject(payload(intentions=[changed(id=f"i{i}") for i in range(9)]))
        self.reject(payload(changed(activity="a" * (MAX_TEXT + 1))))
        self.reject(payload(changed(targets=[str(i) for i in range(17)])))
        self.reject(payload(changed(id="a" * 65)))
        with self.assertRaises(InvalidInterpretation):
            normalize(" " * MAX_OUTPUT_BYTES + wire())
        # Each field fits; the aggregate UTF-8 byte bound still applies.
        value = payload(intentions=[changed(id=f"i{i}", targets=["界" * 1020 + str(n)
            for n in range(16)]) for i in range(2)])
        with self.assertRaises(InvalidInterpretation):
            normalize(json.dumps(value, ensure_ascii=False))

    def test_commitment_matrix_preserves_in_world_questions(self):
        accepted = (("inquiry", "none"), ("statement", "none"), ("preparation", "none"),
                    ("preparation", "now"), ("preparation", "conditional"),
                    ("action", "now"), ("action", "conditional"))
        for mode in ("inquiry", "statement", "preparation", "action"):
            for commitment in ("none", "now", "conditional"):
                item = changed(mode=mode, commitment=commitment,
                               activity="Ask Mara what she knows about the dispatch")
                if commitment == "conditional":
                    item["conditions"] = ["if Mara is available"]
                with self.subTest(mode=mode, commitment=commitment):
                    if (mode, commitment) in accepted:
                        self.assertEqual(normalize(wire(item)).to_dict()["intentions"][0], item)
                    else:
                        self.reject(payload(item))
        self.reject(payload(changed(commitment="conditional")))
        self.reject(payload(changed(conditions=["if nobody is watching"])))
        normalize(wire(changed(mode="inquiry", commitment="none", conditions=["with my hands tied"])))

    def test_methods_constraints_conditions_and_stops_stay_distinct(self):
        item = changed(activity="Cross the bridge", method="use the rope", commitment="conditional",
                       constraints=["use only the rope"], conditions=["if it looks secure"],
                       stop_at=["if dizziness worsens"], targets=["opposite bank"])
        self.assertEqual(normalize(wire(item)).to_dict()["intentions"][0], item)

    def test_context_and_source_are_grounded_without_inventing_references(self):
        item = changed(context_refs=["prior:1"], source="do that again")
        normalized = normalize(wire(item), context_ids=("prior:1",), player_input="Please do that again.")
        self.assertEqual(normalized.to_dict()["intentions"][0], item)
        with self.assertRaises(InvalidInterpretation):
            normalize(wire(item), context_ids=("other",), player_input="Please do that again.")
        with self.assertRaises(InvalidInterpretation):
            normalize(wire(item), context_ids=("prior:1",), player_input="Do something else.")

    def test_relationships_and_ambiguities_reference_existing_unique_intentions(self):
        items = [intention(), changed(id="i2", activity="Search the room")]
        for kind in ("precedes", "depends_on", "alternative", "together", "independent"):
            relationship = dict(type=kind, **{"from": "i1", "to": "i2"})
            result = normalize(wire(intentions=items, relationships=[relationship]))
            self.assertEqual(result.to_dict()["relationships"], [relationship])
        self.reject(payload(intentions=[intention(), intention()]))
        for relation in ({"type": "execute", "from": "i1", "to": "i2"},
                         {"type": "precedes", "from": "i1", "to": "i1"},
                         {"type": "precedes", "from": "i1", "to": "absent"},
                         {"type": "precedes", "from": "i1", "to": "i2", "authorized": True}):
            self.reject(payload(intentions=items, relationships=[relation]))
        self.reject(payload(ambiguities=[{"intentions": ["absent"], "issue": "which target?"}]))
        self.reject(payload(ambiguities=[{"intentions": ["i1"], "issue": "which?", "execute": True}]))
        for cycle in ([{"type": "precedes", "from": "i1", "to": "i2"},
                       {"type": "depends_on", "from": "i1", "to": "i2"}],
                      [{"type": "together", "from": "i1", "to": "i2"},
                       {"type": "independent", "from": "i2", "to": "i1"}],
                      [{"type": "alternative", "from": "i1", "to": "i2"}] * 2):
            self.reject(payload(intentions=items, relationships=cycle))
        normalize(wire(intentions=[], ambiguities=[{"intentions": [], "issue": "What is intended?"}]))


class BindingAuthority(SituatedAuthority):
    """Test-only declared capability binding; not a language interpreter."""
    def __init__(self, current=None):
        super().__init__(current)
        self.handoffs = []
        self.binding = Interpretation("open", "owner objective", "door-x", "handle")
        self.satisfied = self.stops = ()
        self.seen_undertakings = []

    def bind_intent(self, handoff):
        self.handoffs.append(handoff)
        return self.binding

    def assess(self, undertaking, current):
        self.seen_undertakings.append(undertaking)
        return replace(super().assess(undertaking, current),
                       satisfied_conditions=self.satisfied, supported_stops=self.stops)


class Coordination(unittest.TestCase):
    def setUp(self):
        for target in ("socket.create_connection", "socket.socket.connect", "socket.socket.connect_ex"):
            guard = patch(target, side_effect=AssertionError("offline only"))
            guard.start()
            self.addCleanup(guard.stop)
        self.owner = BindingAuthority()
        self.coordinator = Coordinator(self.owner.supply, self.owner)

    def process(self, item=None, text="Open the door", **changes):
        return self.coordinator.process_intent(text, provider=lambda request: wire(item, **changes))

    def test_full_handoff_and_player_safe_provider_request(self):
        self.owner.current = context(conditions=("hidden-secret",), means=("hands", "hidden-means"))
        captured = []
        text = "  I open the door.  "
        result = self.coordinator.process_intent(text, provider=lambda request: (captured.append(request), wire())[1])
        self.assertEqual(result.status, "accepted")
        self.assertEqual(captured[0].player_input, text)
        self.assertNotIn("hidden-secret", repr(captured[0]))
        self.assertNotIn("hidden-means", repr(captured[0]))
        handoff = self.owner.handoffs[0]
        self.assertEqual(handoff.player_input, text)
        self.assertEqual(handoff.context.conditions, ("hidden-secret",))
        self.assertEqual(handoff.interpretation.to_dict(), payload())

    def test_inquiry_and_uncommitted_preparation_cannot_be_promoted_by_binder(self):
        for mode, expected in (("inquiry", "inquiry"), ("preparation", "preparation")):
            with self.subTest(mode=mode):
                result = self.process(changed(mode=mode, commitment="none"))
                self.assertEqual(result.status, expected)
                self.assertEqual((self.owner.minutes, self.owner.execute_calls), (0, 0))
                self.assertIsNone(self.coordinator.undertaking)
        self.assertEqual(self.process(changed(mode="statement", commitment="none")).status, "statement")
        self.assertEqual(len(self.owner.handoffs), 2)

    def test_affirmative_scope_omission_and_specificity_do_not_add_restrictions(self):
        for text, description in (("I run toward the cart", "Run toward the cart"),
                                  ("I examine the ledger", "Examine the ledger"),
                                  ("I ask Mara what she knows", "Ask Mara what she knows")):
            # Declared fixture capability exercises the same seam; these are not
            # implementations of travel, evidence or NPC mechanics.
            owner = BindingAuthority()
            coordinator = Coordinator(owner.supply, owner)
            result = coordinator.process_intent(text, provider=lambda request: wire(changed(activity=description)))
            self.assertEqual(result.status, "accepted")
            self.assertEqual(owner.executed_constraints, ((),))
            self.assertEqual(coordinator.undertaking.objective, description)

    def test_constraints_are_retained_and_cannot_be_silently_dropped(self):
        result = self.process(changed(method="use the handle", constraints=["quietly"]))
        self.assertEqual(result.status, "accepted")
        self.assertEqual(self.owner.executed_constraints, (("quietly",),))
        self.assertEqual(self.owner.handoffs[0].interpretation.to_dict()["intentions"][0]["method"], "use the handle")
        result = self.process(changed(constraints=["without touching anything"]))
        self.assertEqual(result.failure, "authorization")
        self.assertEqual(self.owner.execute_calls, 1)

    def test_conditions_and_stopping_boundaries_require_owner_support(self):
        item = changed(commitment="conditional", conditions=["if nobody is watching"],
                       stop_at=["on hearing footsteps"])
        self.assertEqual(self.process(item).failure, "authorization")
        self.owner.satisfied = ("if nobody is watching",)
        self.assertEqual(self.process(item).failure, "authorization")
        self.assertEqual(self.owner.execute_calls, 0)
        self.owner.stops = ("on hearing footsteps",)
        self.assertEqual(self.process(item).status, "accepted")
        undertaking = self.owner.seen_undertakings[0]
        self.assertEqual(undertaking.conditions, ("if nobody is watching",))
        self.assertEqual(undertaking.stop_at, ("on hearing footsteps",))
        self.assertEqual(undertaking.constraints, ())

    def test_f05_still_returns_control_for_perceptible_consequential_development(self):
        self.owner.current = context(conditions=("footsteps",))
        self.assertEqual(self.process().status, "clarification")
        self.assertEqual(self.owner.execute_calls, 0)

    def test_multiple_intentions_never_bind_execute_or_queue_even_if_related(self):
        for kind in ("precedes", "depends_on", "together", "independent", "alternative"):
            result = self.process(intentions=[intention(), changed(id="i2", activity="Search the room")],
                relationships=[{"type": kind, "from": "i1", "to": "i2"}])
            self.assertEqual(result.status, "clarification")
        self.assertEqual(self.owner.handoffs, [])
        self.assertEqual(self.owner.execute_calls, 0)
        self.assertIsNone(self.coordinator.undertaking)

    def test_material_ambiguity_does_not_reach_domain_binding(self):
        result = self.process(changed(activity="Deal with the guard"),
            ambiguities=[{"intentions": ["i1"], "issue": "Consequential method unspecified"}])
        self.assertEqual(result.status, "clarification")
        self.assertEqual(self.owner.handoffs, [])
        self.assertEqual(self.owner.execute_calls, 0)

    def test_candidate_domains_cannot_select_owner_or_adjudicate(self):
        self.assertEqual(self.process(changed(candidate_domains=["actors"])).status, "accepted")
        self.assertEqual(self.coordinator.undertaking.activity, "open")
        self.assertEqual(self.owner.execute_calls, 1)

    def test_continuation_preserves_accepted_steps_without_reroll_or_charge(self):
        first = self.process()
        before = self.owner.current, self.owner.minutes, self.owner.accepted
        accepted_ref = "accepted:" + self.coordinator.undertaking.accepted_steps[0]
        result = self.process(changed(activity="Continue the same undertaking", context_refs=[accepted_ref]),
                              text="Continue that")
        self.assertEqual(first.status, "accepted")
        self.assertEqual(result.status, "complete")
        self.assertEqual((self.owner.current, self.owner.minutes, self.owner.accepted), before)
        self.assertEqual(self.owner.execute_calls, 1)
        self.assertEqual(self.owner.handoffs[-1].interpretation.to_dict()["intentions"][0]["context_refs"], [accepted_ref])

    def test_provider_validation_binding_and_context_failures_do_not_execute(self):
        def broken(request):
            raise RuntimeError("SECRET-provider-diagnostic")
        result = self.coordinator.process_intent("Open", provider=broken)
        self.assertEqual(result.failure, "technical")
        self.assertNotIn("SECRET", repr(result.player_result()))
        for raw in ("{", wire(changed(context_refs=["invented"])), wire(outcome="success")):
            self.assertEqual(self.coordinator.process_intent("Open", provider=lambda request: raw).failure,
                             "interpretation")
        self.owner.binding = None
        self.assertEqual(self.process().failure, "routing")
        self.owner.binding = object()
        self.assertEqual(self.process().failure, "technical")
        self.assertEqual(self.owner.execute_calls, 0)
        self.assertEqual(self.owner.minutes, 0)

    def test_stale_context_during_provider_or_binding_is_rejected(self):
        def provider(request):
            self.owner.current = replace(self.owner.current, revision="changed")
            return wire()
        self.assertEqual(self.coordinator.process_intent("Open", provider=provider).failure, "context")
        self.assertEqual(self.owner.handoffs, [])
        def binder(handoff):
            self.owner.current = replace(self.owner.current, revision="changed-again")
            return Interpretation("open", "Open", "door-x")
        self.owner.bind_intent = binder
        self.assertEqual(self.process().failure, "context")
        self.assertEqual(self.owner.execute_calls, 0)

    def test_invalid_input_consumes_old_pending_permit_and_cannot_fall_through(self):
        old = self.coordinator.decide(interpretation=Interpretation("open", "Open", "door-x"))
        self.assertEqual(old.status, "proceed")
        self.coordinator.process_intent("Open", provider=lambda request: "malformed")
        self.assertEqual(self.coordinator.execute(old).failure, "authorization")
        self.assertEqual(self.owner.execute_calls, 0)

    def test_owner_condition_change_before_execution_invalidates_the_permission(self):
        self.owner.satisfied = ("if nobody is watching",)
        item = changed(commitment="conditional", conditions=["if nobody is watching"])
        decision = self.coordinator.decide_intent("Open if nobody is watching", provider=lambda request: wire(item))
        self.assertEqual(decision.status, "proceed")
        self.owner.satisfied = ()
        self.assertEqual(self.coordinator.execute(decision).failure, "domain")
        self.assertEqual(self.owner.execute_calls, 0)

    def test_stop_boundary_returns_control_on_an_actual_owner_checkpoint(self):
        self.owner.stops = ("on hearing footsteps",)
        self.owner.current = context(conditions=("footsteps",))
        decision = self.process(changed(stop_at=["on hearing footsteps"]))
        self.assertEqual(decision.status, "clarification")
        self.assertEqual(decision.undertaking.stop_at, self.owner.stops)
        self.assertEqual(self.owner.execute_calls, 0)

    def test_missing_consequential_method_is_clarification_without_a_selected_method(self):
        target = replace(self.owner.current.targets[0], routine_method=None)
        self.owner.current = replace(self.owner.current, targets=(target,))
        self.owner.binding = replace(self.owner.binding, method=None)
        self.assertEqual(self.process().status, "clarification")
        self.assertEqual(self.owner.execute_calls, 0)

    def test_explicit_game_engine_seam_contains_failure_without_legacy_fallback(self):
        from engine.game_engine import GameEngine
        engine = GameEngine("data/regions/market_passage_v1.json",
                            coordination_context=self.owner.supply, coordination_domain=self.owner)
        before = engine.get_world_state()
        with patch.object(engine, "_process_legacy_command", side_effect=AssertionError("no fallback")):
            rejected = engine.process_player_intent("Open the door", provider=lambda request: "invalid")
            self.assertEqual(rejected["coordination"]["failure"], "interpretation")
            self.assertEqual(engine.get_world_state(), before)
            accepted = engine.process_player_intent("Open the door", provider=lambda request: wire())
            self.assertEqual(accepted["coordination"]["status"], "accepted")

    def test_no_binder_or_bad_player_input_fails_closed_before_any_execution(self):
        domain = SituatedAuthority()
        coordinator = Coordinator(domain.supply, domain)
        self.assertEqual(coordinator.process_intent("Open", provider=lambda request: wire()).failure, "routing")
        for text in (None, "", " ", "x" * 8193):
            with self.subTest(text=str(text)[:20]):
                result = self.coordinator.process_intent(text, provider=lambda request: self.fail("must not invoke"))
                self.assertEqual(result.failure, "interpretation")
        self.assertEqual(self.owner.execute_calls, 0)


if __name__ == "__main__":
    unittest.main()
