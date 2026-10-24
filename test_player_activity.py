"""M2-M1 integration matrix. All gameplay uses GameEngine.process_command."""
from dataclasses import replace
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from engine.campaign_records import Boundary
from engine.information_resolution import Constraint, BindingTerms, Query
from engine.save_system import build_save_data, load_game
from test_fixtures.player_activity_suppliers import InspectionSuppliers, AUTHORED
from test_fixtures.continuity_suppliers import Draws, LOCATION


class PlayerActivity(unittest.TestCase):
    def setUp(self):
        for guard in (patch("socket.create_connection", side_effect=AssertionError("offline")),
                      patch.object(socket.socket, "connect", side_effect=AssertionError("offline")),
                      patch.object(socket.socket, "connect_ex", side_effect=AssertionError("offline")),
                      patch("engine.narration_source.OpenAI", side_effect=AssertionError("offline"))):
            guard.start()
            self.addCleanup(guard.stop)
        self.suppliers = InspectionSuppliers()
        self.engine = self.suppliers.engine()

    def command(self, text="inspect cargo panel", **kwargs):
        result = self.engine.process_command(text, **kwargs)
        self.assertNotIn("PRIVATE", json.dumps(result))
        return result

    def accepted(self, text="inspect cargo panel", **kwargs):
        result = self.command(text, **kwargs)
        self.assertEqual(result["coordination"]["status"], "accepted", (result, self.engine._consequences.diagnostic))
        return result

    def unchanged(self, text, **kwargs):
        before = build_save_data(self.engine)
        result = self.command(text, **kwargs)
        self.assertNotEqual(result["coordination"]["status"], "accepted", result)
        self.assertEqual(build_save_data(self.engine), before)
        return result

    def test_01_two_circumstances_same_runtime(self):
        for name, duration, draw in (("cargo panel", 19, 3), ("archive slab", 13, 6)):
            with self.subTest(name=name):
                s = InspectionSuppliers(name, duration=duration, draws=Draws(draw))
                e = s.engine()
                r = e.process_command(f"examine the {name} using inspection")
                self.assertEqual(r["coordination"]["status"], "accepted", r)
                data = e.get_campaign_state()
                self.assertEqual(data.state.adjudication.at, duration)
                self.assertEqual(data.state.adjudication.inventory, (("actor", "lamp", 3),))
                self.assertEqual(data.state.adjudication.history[0].assessment.draw, draw)
                self.assertEqual(len(data.state.facts), 1)
                self.assertEqual(len(data.activities), 1)
                self.assertEqual(data.activities[0].id, r["player_activity"]["undertaking_id"])

    def test_02_inquiry_and_preparation_read_only(self):
        for text, status in (("can I inspect the cargo panel?", "inquiry"),
                             ("prepare to examine cargo panel", "preparation")):
            r = self.unchanged(text)
            self.assertEqual(r["coordination"]["status"], status)
        self.assertEqual(self.suppliers.draws.calls, 0)

    def test_03_later_activity_depends_on_accepted_finding(self):
        self.unchanged("inspect surface finding")
        self.accepted()
        self.accepted("inspect surface finding")
        data = self.engine.get_campaign_state()
        self.assertEqual(data.state.adjudication.at, 26)
        self.assertIn(data.state.facts[0].id, data.state.adjudication.history[1].assessment.premise_ids)

    def test_04_missing_prerequisite_and_unavailable_information(self):
        self.engine.revise_campaign(inputs=self.suppliers.inputs(self.engine, accessible="no"))
        blocked = self.accepted()
        self.assertEqual(blocked["coordination"]["results"][0]["outcome"], "negative")
        self.assertEqual(self.engine.get_campaign_state().state.facts, ())
        for changes in ({"availability": "established_unavailable"}, {"capability": "no"}):
            self.engine = self.suppliers.engine()
            self.engine.revise_campaign(inputs=self.suppliers.inputs(self.engine, **changes))
            self.unchanged("inspect cargo panel")
        self.assertEqual(self.suppliers.draws.calls, 0)

    def test_05_constraints_and_unsupported_language_never_legacy(self):
        for text in ("inspect cargo panel quietly", "inspect cargo panel carefully",
                     "inspect cargo panel without a lamp", "inspect cargo panel and move north",
                     "move north", "wait", "search for treasure", "attack guard", "look",
                     "inspect cargo panel using magic", "inspect", "perhaps inspect cargo panel"):
            with self.subTest(text=text), patch.object(self.engine, "_process_legacy_command", side_effect=AssertionError("legacy")):
                self.unchanged(text)
        self.assertEqual(self.suppliers.draws.calls, 0)

    def test_06_hidden_binding_is_applied_without_disclosure(self):
        data = self.engine.get_campaign_state()
        binding = Constraint("PRIVATE-restriction", (LOCATION,), ("search",), BindingTerms(("block",)), AUTHORED)
        self.engine.revise_campaign(inputs=replace(data.inputs, constraints=(binding,)))
        r = self.accepted()
        self.assertEqual(r["coordination"]["results"][0]["outcome"], "negative")
        self.assertEqual(self.suppliers.draws.calls, 0)
        self.assertEqual(self.engine.get_campaign_state().state.facts, ())
        self.assertEqual(self.engine.get_campaign_state().state.adjudication.at, 19)

    def test_07_interruption_restore_retry_and_current_continuation(self):
        r = self.accepted(request_id="first")
        a = r["player_activity"]["undertaking_id"]
        self.engine.revise_campaign(undertaking=a, boundary=Boundary(blocked=True))
        self.unchanged("continue", undertaking_id=a)
        path = Path(".artifacts/m2-player-activity-test.json")
        self.engine.save(str(path))
        draws = Draws(6)
        fresh = InspectionSuppliers()
        self.engine = load_game(str(path), campaign_draw=draws)
        self.engine.set_player_activity_context(fresh.context)
        before = build_save_data(self.engine)
        retry = self.accepted("retry", request_id="first")
        self.assertIn("Previously accepted", retry["message"])
        self.assertEqual(build_save_data(self.engine), before)
        self.assertEqual(draws.calls, 0)
        self.unchanged("continue", undertaking_id=a)
        self.engine.revise_campaign(undertaking=a, boundary=Boundary())
        self.accepted("continue", undertaking_id=a, request_id="second")
        self.assertEqual(draws.calls, 1)
        data = self.engine.get_campaign_state()
        self.assertEqual(data.activities[0].accepted, ("first", "second"))
        self.assertEqual(data.activities[0].progress_seconds, 38)
        self.assertEqual(data.state.adjudication.inventory, (("actor", "lamp", 2),))
        self.accepted("inspect surface finding")
        self.assertEqual(self.engine.get_campaign_state().state.adjudication.at, 45)

    def test_08_distinct_new_attempt_revalidates(self):
        r = self.accepted(request_id="first")
        a = r["player_activity"]["undertaking_id"]
        self.engine.revise_campaign(inputs=self.suppliers.inputs(self.engine, capability="no"))
        self.accepted("retry", request_id="first")
        self.unchanged("continue", undertaking_id=a, request_id="new")
        self.unchanged("inspect cargo panel", request_id="new")
        self.assertEqual(self.suppliers.draws.calls, 1)

    def test_09_id_conflict_and_ambiguous_continuation(self):
        self.accepted(request_id="first")
        self.unchanged("inspect surface finding", request_id="first")
        self.accepted("inspect surface finding", request_id="second")
        self.unchanged("continue")
        self.unchanged("retry", request_id="missing")

    def test_10_changed_situated_scope_and_means_reject(self):
        for field, value in (("available", False), ("means", ()), ("unavailable", ("dependency",))):
            with self.subTest(field=field):
                s = InspectionSuppliers()
                self.engine = s.engine()
                setattr(s, field, value)
                self.unchanged("inspect cargo panel")

    def test_11_final_situated_revalidation_no_publication(self):
        original = self.suppliers.draws
        def changed():
            value = original()
            self.suppliers.available = False
            return value
        self.engine = InspectionSuppliers(draws=changed).engine()
        self.engine.set_player_activity_context(self.suppliers.context)
        self.unchanged("inspect cargo panel")
        self.assertEqual(self.engine._consequences.diagnostic, ("acceptance", "stale_situated_context"))

    def test_12_failed_presentation_keeps_accepted_result(self):
        original = self.engine.process_coordination
        def display_failure(*args, **kwargs):
            original(*args, **kwargs)
            raise RuntimeError("display unavailable")
        with patch.object(self.engine, "process_coordination", side_effect=display_failure):
            result = self.command(request_id="first")
            self.assertEqual(result["coordination"]["failure"], "presentation")
        before = build_save_data(self.engine)
        self.suppliers.available = False
        self.accepted("retry", request_id="first")
        self.assertEqual(build_save_data(self.engine), before)

    def test_13_repeated_text_is_new_attempt_unless_id_reused(self):
        self.accepted(request_id="first")
        before = build_save_data(self.engine)
        self.accepted(request_id="first")
        self.assertEqual(build_save_data(self.engine), before)
        self.accepted(request_id="second")
        data = self.engine.get_campaign_state()
        self.assertEqual(len(data.activities), 2)
        self.assertEqual(self.suppliers.draws.calls, 2)

    def test_14_load_existing_engine_retains_installed_services(self):
        self.accepted()
        path = Path(".artifacts/m2-existing-engine-test.json")
        self.engine.save(str(path))
        self.engine.load(str(path), campaign_draw=Draws(6))
        self.accepted("inspect surface finding")

    def test_15_completed_undertaking_and_question_do_not_reroll(self):
        self.suppliers = InspectionSuppliers(draws=Draws(6))
        self.engine = self.suppliers.engine()
        r = self.accepted()
        a = r["player_activity"]["undertaking_id"]
        self.unchanged("continue?", undertaking_id=a)
        result = self.unchanged("continue", undertaking_id=a)
        self.assertEqual(result["coordination"]["status"], "complete")
        self.assertEqual(self.suppliers.draws.calls, 1)

    def test_16_retry_does_not_require_current_supplier_or_means(self):
        self.accepted(request_id="first")
        self.suppliers.means = ()
        before = build_save_data(self.engine)
        self.accepted(request_id="first")
        self.engine.set_player_activity_context(lambda e: (_ for _ in ()).throw(RuntimeError("PRIVATE")))
        self.accepted("retry", request_id="first")
        self.assertEqual(build_save_data(self.engine), before)
        self.assertEqual(self.suppliers.draws.calls, 1)

    def test_17_changed_internal_requirement_after_draw_is_stale(self):
        draws = Draws(3)
        def change():
            value = draws()
            self.engine.revise_campaign(inputs=self.suppliers.inputs(self.engine, capability="no"))
            return value
        self.suppliers.draws = change
        self.engine = self.suppliers.engine()
        result = self.command()
        self.assertNotEqual(result["coordination"]["status"], "accepted")
        self.assertEqual(self.engine.get_campaign_state().state.receipts, ())
        self.assertEqual(self.engine.get_campaign_state().state.adjudication.at, 0)
        self.assertEqual(self.engine.get_campaign_state().state.adjudication.inventory, (("actor", "lamp", 4),))

    def test_18_partial_save_then_new_supplier_revalidates_availability(self):
        r = self.accepted(request_id="first")
        path = Path(".artifacts/m2-context-restoration-test.json")
        self.engine.save(str(path))
        self.engine = load_game(str(path), campaign_draw=Draws(6))
        fresh = InspectionSuppliers()
        fresh.available = False
        self.engine.set_player_activity_context(fresh.context)
        self.unchanged("continue", undertaking_id=r["player_activity"]["undertaking_id"])
        self.accepted("retry", request_id="first")


if __name__ == "__main__":
    unittest.main()
