"""I3-M1 fifteen-case matrix: common runtime, persisted authority, offline fault injection."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from engine.activity_control import ActivityDevelopment
from engine.campaign_continuity import hours_to_seconds
from engine.campaign_records import Boundary, WaitingIntent, pack, unpack
from engine.game_engine import GameEngine
from engine.information_adjudication import propose_assessed
from engine.information_resolution import Fact, Identity, Period, Query, Relationship
from engine.save_system import build_save_data, load_game
from test_fixtures.continuity_suppliers import (
    AUTHORED, HIDDEN, Draws, changed_inputs, declarations, engine, request, start, REGION,
)


class Continuity(unittest.TestCase):
    def setUp(self):
        for guard in (patch("socket.create_connection", side_effect=AssertionError("offline")),
                      patch.object(socket.socket, "connect", side_effect=AssertionError("offline")),
                      patch.object(socket.socket, "connect_ex", side_effect=AssertionError("offline")),
                      patch("engine.narration_source.OpenAI", side_effect=AssertionError("offline"))):
            guard.start()
            self.addCleanup(guard.stop)
        self.path = Path(".artifacts/i3-continuity-test.json")
        self.bad = Path(".artifacts/i3-continuity-malformed.json")

    def accepted(self, e, r, **kw):
        result = e.process_consequence(r, **kw)
        self.assertEqual(result["coordination"]["status"], "accepted", (result, e._consequences.diagnostic))
        self.assertNotIn(HIDDEN, json.dumps(result))
        return result

    def rejected(self, e, r, **kw):
        before = build_save_data(e)
        result = e.process_consequence(r, **kw)
        self.assertNotEqual(result["coordination"]["status"], "accepted", result)
        self.assertEqual(before, build_save_data(e))
        self.assertNotIn(HIDDEN, json.dumps(result))
        return result

    def restore(self, e, draws=None):
        e.save(str(self.path))
        return load_game(str(self.path), campaign_draw=draws)

    def partial(self):
        draws = Draws(3, 6)
        e = engine(draws=draws)
        a = start(e)
        self.accepted(e, request(a))
        return e, a, draws

    def test_01_complete_consequence_roundtrip(self):
        e, a, draws = self.partial()
        before = build_save_data(e)
        f = self.restore(e)
        del e
        self.assertEqual(build_save_data(f), before)
        state = f.get_campaign_state()
        self.assertEqual(state.activities[0].accepted, ("first",))
        self.assertEqual(state.activities[0].progress_seconds, 31)
        self.assertEqual(state.state.adjudication.inventory, (("actor", "wedge", 3),))
        self.assertEqual(state.state.adjudication.obligations, (("actor", "terms", "return the wedge"),))
        self.assertEqual(state.state.adjudication.history[0].assessment.draw, 3)
        self.assertEqual(state.state.adjudication.history[0].context["developments"][0]["time"], "Elapsed 31 seconds")
        self.assertEqual(state.state.facts[0].subject, "finding")
        self.assertEqual(draws.calls, 1)

    def test_02_retry_and_identity_conflict_after_restore(self):
        e, a, _ = self.partial()
        draws = Draws()
        f = self.restore(e, draws)
        f.revise_campaign(inputs=changed_inputs(f, capable=False))
        before = build_save_data(f)
        result = self.accepted(f, request(a))
        self.assertIn("Previously accepted result", result["message"])
        self.assertEqual(build_save_data(f), before)
        self.assertEqual(draws.calls, 0)
        self.rejected(f, request(a, means=()))
        self.rejected(f, request(a, method="use", target="finding", means=()))

    def test_03_interruption_restore_and_continuation(self):
        e, a, _ = self.partial()
        e.revise_campaign(undertaking=a, boundary=Boundary(blocked=True))
        f = self.restore(e, Draws(6))
        self.rejected(f, request(a, "next"))
        self.assertEqual(f.get_campaign_state().activities[0].accepted, ("first",))
        f.revise_campaign(undertaking=a, boundary=Boundary())
        self.accepted(f, request(a, "next"))
        self.assertEqual(f.get_campaign_state().activities[0].accepted, ("first", "next"))
        self.assertEqual(f.get_campaign_state().activities[0].progress_seconds, 62)

    def test_04_current_capability_and_hidden_restriction(self):
        e, a, _ = self.partial()
        f = self.restore(e)
        f.revise_campaign(inputs=changed_inputs(f, capable=False))
        self.rejected(f, request(a, "next"))
        f.revise_campaign(inputs=changed_inputs(f, blocked=True))
        # Re-enable capability explicitly; hidden binding legitimately blocks an
        # attempted action with its established costs, rather than technical rejection.
        i = f.get_campaign_state().inputs
        foundation = i.foundations[0]
        i = replace(i, foundations=(replace(foundation, facts=tuple(
            replace(x, value="yes") if x.id == "capability" else x for x in foundation.facts)),))
        f.revise_campaign(inputs=i)
        self.accepted(f, request(a, "next"))
        self.assertEqual(f.get_consequence_state().adjudication.history[-1].assessment.result, "blocked")

    def test_05_same_initial_and_resumed_means_restrictions(self):
        for restored in (False, True):
            with self.subTest(restored=restored):
                e = engine(effects=False)
                a = start(e)
                if restored:
                    self.accepted(e, request(a))
                    e = self.restore(e)
                self.rejected(e, request(a, "bad", means=()))
                e.revise_campaign(undertaking=a, boundary=Boundary(missing_means=("wedge",)))
                self.rejected(e, request(a, "missing"))

    def test_06_display_pause_and_restore_never_reroll(self):
        e = engine(draws=Draws(3))
        a = start(e)
        original = e.process_coordination
        def fail_after(**kwargs):
            original(**kwargs)
            raise RuntimeError("display unavailable")
        with patch.object(e, "process_coordination", side_effect=fail_after):
            result = e.process_consequence(request(a))
        self.assertEqual(result["coordination"]["failure"], "presentation")
        self.assertEqual(len(e.get_consequence_state().receipts), 1)
        draws = Draws()
        f = self.restore(e, draws)
        self.accepted(f, request(a))
        self.assertEqual(draws.calls, 0)

    def test_07_new_attempt_and_restart_policy(self):
        draws = Draws(3, 6)
        e = engine(draws=draws, effects=False)
        a = start(e)
        self.accepted(e, request(a))
        f = self.restore(e, draws)
        f.revise_campaign(undertaking=a, boundary=Boundary(restart_required=True))
        self.rejected(f, request(a, "restart"))
        # Existing F05 restart policy supplied by a trusted checkpoint, not new mechanics.
        b = start(f)
        self.accepted(f, request(b, "new-attempt"))
        self.assertEqual(draws.calls, 2)
        self.assertEqual(len(f.get_consequence_state().receipts), 2)
        self.assertNotEqual(a, b)

    def test_08_accepted_increment_survives_later_rejection(self):
        e, a, _ = self.partial()
        before = build_save_data(e)
        self.rejected(e, request(a, "bad"), propose=lambda assessed: replace(
            propose_assessed(assessed), result="failure"))
        f = self.restore(e)
        self.assertEqual(build_save_data(f), before)
        self.assertEqual(len(f.get_consequence_state().receipts), 1)

    def test_09_later_gameplay_retrieves_restored_fact_and_commitment(self):
        e, a, _ = self.partial()
        f = self.restore(e)
        b = f.begin_undertaking("search", "finding", "use")
        self.accepted(f, request(b, "dependent", target="finding", method="use", means=()))
        accepted = f.get_consequence_state().adjudication.history[-1]
        self.assertIn("first:fact:0", accepted.assessment.premise_ids)
        self.assertEqual(f.get_world_state()["time"], {"elapsed_seconds": 38})

    def test_10_identity_relationship_and_definition_closure(self):
        b, i = declarations()
        foundation = i.foundations[0]
        definition = Identity("definition", "definition")
        instance = Identity("instance", "instance", "definition")
        foundation = replace(foundation, identities=(*foundation.identities, definition, instance),
            relationships=(Relationship("active", "actor", "active_effect", "instance", AUTHORED),))
        e = GameEngine(REGION, campaign_config=(b, replace(i, foundations=(foundation,))), campaign_draw=Draws(3))
        a = start(e); self.accepted(e, request(a))
        f = self.restore(e)
        view = f.get_consequence_information()
        self.assertEqual(view.identity("instance"), instance)
        self.assertEqual(view.identity("finding").id, "finding")
        result = view.resolve(Query(("target",), 31, relations=("governs",), depth=1))
        self.assertEqual(result.relationships[0].target, "finding")
        self.assertIn("first:fact:0", {x.id for x in result.facts})

    def test_11_malformed_saves_leave_live_state_and_source_unchanged(self):
        e, a, _ = self.partial()
        payload = build_save_data(e)
        data = e.get_campaign_state()
        corruptions = [
            lambda p: p.update(save_version=99),
            lambda p: p.update(save_version=True),
            lambda p: p["world_state"].pop("continuing_gameplay"),
            lambda p: p["world_state"].update(time={"elapsed_seconds": 32}),
            lambda p: p["world_state"]["continuing_gameplay"].update(record="os.system"),
        ]
        replacements = [
            replace(data, unit="hours"), replace(data, content_digest="wrong"),
            replace(data, state=replace(data.state, receipts=())),
            replace(data, state=replace(data.state, facts=())),
            replace(data, bases=()),
            replace(data, blueprint=replace(data.blueprint, methods=tuple(
                replace(m, duration=32) if m.id == "inspect" else m for m in data.blueprint.methods))),
            replace(data, state=replace(data.state, receipts=(replace(data.state.receipts[0],
                step=replace(data.state.receipts[0].step, accessible=(("result", HIDDEN),))),))),
            replace(data, state=replace(data.state, adjudication=replace(
                data.state.adjudication, inventory=(("actor", "wedge", 4),)))),
            replace(data, activities=(replace(data.activities[0], progress_seconds=32),)),
        ]
        corruptions += [(lambda p, d=d: p["world_state"].update(continuing_gameplay=pack(d))) for d in replacements]
        for number, corrupt in enumerate(corruptions):
            with self.subTest(corruption=number):
                candidate = deepcopy(payload); corrupt(candidate)
                self.bad.write_text(json.dumps(candidate), encoding="utf-8")
                source = self.bad.read_bytes()
                root = e._consequences.campaign
                before = build_save_data(e)
                with self.assertRaises(ValueError):
                    e.load(str(self.bad))
                self.assertIs(e._consequences.campaign, root)
                self.assertEqual(build_save_data(e), before)
                self.assertEqual(self.bad.read_bytes(), source)
        self.bad.write_text('{"save_version":2,', encoding="utf-8")
        with self.assertRaises(ValueError):
            e.load(str(self.bad))

    def test_11b_save_failures_preserve_destination_and_live_state(self):
        e, a, _ = self.partial()
        e.save(str(self.path)); old = self.path.read_bytes(); before = build_save_data(e)
        for target in ("engine.save_system.os.fsync", "engine.save_system.os.replace"):
            with self.subTest(target=target), patch(target, side_effect=OSError("injected")):
                with self.assertRaises(OSError):
                    e.save(str(self.path))
                self.assertEqual(self.path.read_bytes(), old)
                self.assertEqual(build_save_data(e), before)
        with patch("engine.save_system.json.dumps", side_effect=ValueError("encoding")):
            with self.assertRaises(ValueError):
                e.save(str(self.path))
        self.assertEqual(self.path.read_bytes(), old)
        self.assertFalse(list(self.path.parent.glob(self.path.name + ".*.tmp")))

    def test_11c_reconstruction_failure_preserves_root_scene(self):
        e, a, _ = self.partial()
        e.save(str(self.path)); root=e._consequences.campaign
        with patch("engine.campaign_continuity.build_scene", side_effect=RuntimeError("scene")):
            with self.assertRaises(ValueError):
                e.load(str(self.path))
        self.assertIs(e._consequences.campaign, root)

    def test_11d_legacy_compatibility_no_promotion_or_downgrade(self):
        e = GameEngine("test_fixtures/bryn_shander_legacy.json")
        e.save(str(self.path)); payload = json.loads(self.path.read_text())
        self.assertEqual(payload["save_version"], 1)
        self.assertIsNone(load_game(str(self.path))._consequences)
        f = engine()
        with self.assertRaises(ValueError):
            f.load(str(self.path))
        with self.assertRaises(ValueError):
            load_game(str(self.path), require_campaign=True)
        f.save(str(self.path)); payload = json.loads(self.path.read_text()); payload["save_version"]=1
        self.bad.write_text(json.dumps(payload))
        with self.assertRaises(ValueError):
            load_game(str(self.bad))

    def test_12_second_resolution_and_technical_boundaries(self):
        e, a, _ = self.partial()
        before=build_save_data(e)
        e.get_history(); e.query_history(); e.get_scene_snapshot()
        self.assertEqual(build_save_data(e), before)
        f=self.restore(e)
        self.assertEqual(build_save_data(f), before)
        self.assertEqual(hours_to_seconds(2), 7200)
        for invalid in (True, -1, 1.5):
            with self.assertRaises(ValueError):
                hours_to_seconds(invalid)
        for mutator in (lambda: f.advance_time(), lambda: f.process_command("wait"),
                        lambda: f.reset()):
            with self.assertRaises(ValueError):
                mutator()
        self.assertEqual(build_save_data(f), before)

    def test_13_expiration_is_authoritative_without_scheduler_or_replay(self):
        e = engine(draws=Draws(3))
        e.revise_campaign(inputs=changed_inputs(e, blocked=True, expires=31))
        a=start(e)
        self.accepted(e, request(a))
        self.assertEqual(e.get_consequence_state().adjudication.history[0].assessment.result, "blocked")
        f=self.restore(e, Draws(3))
        self.accepted(f, request(a, "after-expiration"))
        self.assertEqual(f.get_consequence_state().adjudication.history[1].assessment.result, "partial")
        g=self.restore(f)
        self.assertEqual(len(g.get_consequence_state().receipts), 2)
        self.assertEqual(g.get_campaign_state().state.adjudication.at, 62)

    def test_14_historical_fact_distinct_from_current_applicability(self):
        e=engine(effects=False)
        data=e.get_campaign_state(); foundation=data.inputs.foundations[0]
        old=Fact("old", "target", "signal", "yes", AUTHORED, Period(0, 31))
        e.revise_campaign(inputs=replace(data.inputs, foundations=(replace(
            foundation, facts=(*foundation.facts, old)),)))
        a=start(e); self.accepted(e, request(a))
        f=self.restore(e)
        view=f.get_consequence_information()
        self.assertFalse(view.resolve(Query(("target",),31,("signal",))).facts)
        found=view.resolve(Query(("target",),31,("signal",),include_history=True))
        self.assertEqual(found.facts, (old,))
        self.assertEqual(found.selections[0].temporal, "historical")

    def test_15_stage_faults_are_contained_and_private(self):
        for target in ("engine.consequence_integration.prepare_candidate",
                       "engine.consequence_integration.Runtime._incorporate",
                       "engine.consequence_integration.Runtime._receipt",
                       "engine.campaign_continuity.prepare_root"):
            with self.subTest(target=target):
                e=engine(); a=start(e)
                with patch(target, side_effect=RuntimeError(HIDDEN)):
                    self.rejected(e, request(a))
                self.assertTrue(e._consequences.diagnostic)
                self.assertNotIn(HIDDEN,json.dumps(e._consequences.trace))
        e,a,_=self.partial()
        stages={x["stage"] for x in e._consequences.trace}
        self.assertTrue({"interpretation","responsibility_selection","retrieval",
                         "adjudication","validation","acceptance","presentation"}.issubset(stages))

    def test_waiting_duration_and_condition_intent_roundtrip(self):
        for intent in (WaitingIntent(duration_seconds=600), WaitingIntent(condition="guards-leave",basis=("available",))):
            with self.subTest(intent=intent):
                e=engine()
                a=e.begin_undertaking("wait","target","hold",waiting=intent)
                f=self.restore(e)
                self.assertEqual(f.get_campaign_state().activities[0].waiting,intent)
                self.rejected(f,request(a,"wait",action="wait",method="hold",means=()))
                self.assertEqual(f.get_world_state()["time"],{"elapsed_seconds":0})
        with self.assertRaises(ValueError):
            engine().begin_undertaking("wait","target","hold",waiting=WaitingIntent())

    def test_f05_perceived_interruptions_and_temporal_boundary(self):
        e,a,_=self.partial()
        for boundary in (Boundary(developments=(ActivityDevelopment("player_choice"),)),
                         Boundary(not_after_seconds=50)):
            e.revise_campaign(undertaking=a,boundary=boundary)
            self.rejected(e,request(a,"next"))
            self.accepted(e,request(a))  # recognition never means continuation
        e.revise_campaign(undertaking=a,boundary=Boundary(
            developments=(ActivityDevelopment("player_choice",perceived=False),)))
        self.accepted(e,request(a,"next"))

    def test_stale_changed_owner_inputs_cannot_publish(self):
        e=engine(); a=start(e)
        def stale(assessment):
            e.revise_campaign(inputs=changed_inputs(e,capable=False))
            return propose_assessed(assessment)
        result=e.process_consequence(request(a),propose=stale)
        self.assertNotEqual(result["coordination"]["status"],"accepted")
        self.assertEqual(len(e.get_consequence_state().receipts),0)
        self.assertEqual(e.get_world_state()["time"],{"elapsed_seconds":0})

    def test_reentrant_save_and_load_refuse_without_effects(self):
        e=engine();a=start(e)
        def propose(assessment):
            with self.assertRaises(ValueError):
                e.save(str(self.path))
            with self.assertRaises(ValueError):
                e.load(str(self.path))
            return propose_assessed(assessment)
        self.accepted(e,request(a),propose=propose)

    def test_owner_acceptance_cannot_bypass_current_f05_boundary(self):
        from engine.gameplay_coordination import DomainStep
        from engine.activity_control import ActivityCheckpoint
        e = engine(); a = start(e)
        e.revise_campaign(undertaking=a, boundary=Boundary(blocked=True))
        before = build_save_data(e)
        with self.assertRaises(Exception):
            e._consequences.accept(request(a),
                DomainStep("first", ActivityCheckpoint(a, "inspect"), ("action",)), e)
        self.assertEqual(build_save_data(e), before)

    def test_selective_causal_basis_retains_only_relevant_subjects(self):
        b, inputs = declarations()
        foundation = inputs.foundations[0]
        unrelated = Identity("irrelevant")
        foundation = replace(foundation, identities=(*foundation.identities, unrelated),
            facts=(*foundation.facts, Fact("irrelevant-fact", "irrelevant", "label", "unrelated", AUTHORED)))
        e = GameEngine(REGION, campaign_config=(b, replace(inputs, foundations=(foundation,))), campaign_draw=Draws(3))
        a = start(e); self.accepted(e, request(a))
        data = e.get_campaign_state()
        self.assertNotIn("irrelevant-fact", {f.id for base in data.bases for foundation in base.foundations for f in foundation.facts})
        f = self.restore(e)
        self.assertEqual(f.get_campaign_state().inputs, data.inputs)

    def test_runtime_declaration_mismatch_refuses_save_and_new_acceptance(self):
        e, a, _ = self.partial()
        runtime = e._consequences
        runtime.config = replace(runtime.config, effects=())
        with self.assertRaises(ValueError):
            e.save(str(self.path))
        result = e.process_consequence(request(a, "new"))
        self.assertNotEqual(result["coordination"]["status"], "accepted")
        self.assertEqual(len(e.get_consequence_state().receipts), 1)

    def test_failed_temporary_open_preserves_previous_disk_bytes(self):
        e, a, _ = self.partial()
        e.save(str(self.path)); previous = self.path.read_bytes()
        with patch("pathlib.Path.open", side_effect=OSError("write unavailable")):
            with self.assertRaises(OSError):
                e.save(str(self.path))
        self.assertEqual(self.path.read_bytes(), previous)

    def test_strict_record_shapes_and_scalar_types(self):
        e, a, _ = self.partial(); payload = build_save_data(e)
        for change in (lambda fields: fields.pop("bases"),
                       lambda fields: fields.update(schema=True),
                       lambda fields: fields.update(revision=False),
                       lambda fields: fields.update(unsupported="anything")):
            candidate = deepcopy(payload)
            change(candidate["world_state"]["continuing_gameplay"]["fields"])
            self.bad.write_text(json.dumps(candidate))
            with self.assertRaises(ValueError):
                load_game(str(self.bad))

    def test_restoration_uses_no_adjudication_or_draw(self):
        e, a, _ = self.partial()
        e.save(str(self.path))
        with patch("engine.information_adjudication.AdjudicationSession._assess",
                   side_effect=AssertionError("no adjudication on restore")), patch(
                   "engine.consequence_integration.prepare_candidate", side_effect=AssertionError("no replay")):
            f = load_game(str(self.path), campaign_draw=lambda: self.fail("no draw on restore"))
        self.assertEqual(f._consequences.trace[0]["stage"], "restoration")
        self.accepted(f, request(a))

    def test_defensive_world_and_data_views(self):
        e,a,_=self.partial(); before=build_save_data(e)
        e.world_state["time"]["elapsed_seconds"]=999
        e.scene_snapshot["location"]["name"]="changed"
        state=e.get_campaign_state(); state.state.adjudication.history[0].context.clear()
        self.assertEqual(build_save_data(e),before)


if __name__ == "__main__":
    unittest.main()
