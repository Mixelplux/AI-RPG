"""I1: structural, bounded language and GameEngine integration evidence, offline.

SituatedAuthority is a stipulated World/Action/Character/Actor supplier, not a
search, stealth or navigation mechanic. It owns its tiny atomic test state; no
scenario identifier is read by the common coordinator or selects an outcome.
"""
from copy import deepcopy
from dataclasses import replace
import socket
import unittest
from unittest.mock import patch

from engine.activity_control import ActivityCheckpoint
from engine.game_engine import GameEngine
from engine.gameplay_coordination import (
    AcceptedStep, Coordinator, Interpretation, interpret,
)
from engine.save_system import build_save_data


from test_fixtures.coordination_suppliers import context, SituatedAuthority

def runtime(current=None):
    owner = SituatedAuthority(current)
    return owner, Coordinator(owner.supply, owner)


def request(**changes):
    return replace(Interpretation("open", "Open the local door", "door-x"), **changes)


class OfflineCase(unittest.TestCase):
    def setUp(self):
        self.guards = [patch("socket.create_connection", side_effect=AssertionError("offline only")),
                       patch.object(socket.socket, "connect", side_effect=AssertionError("offline only")),
                       patch.object(socket.socket, "connect_ex", side_effect=AssertionError("offline only")),
                       patch("engine.narration_source.OpenAI", side_effect=AssertionError("offline only"))]
        for guard in self.guards:
            guard.start()
            self.addCleanup(guard.stop)


class Structural(OfflineCase):
    def test_ordinary_local_permission_executes_one_owned_step(self):
        owner, coordinator = runtime()
        result = coordinator.process(interpretation=request())
        self.assertEqual(result.status, "accepted")
        self.assertEqual((owner.minutes, owner.execute_calls), (1, 1))
        self.assertEqual(coordinator.undertaking.accepted_steps, owner.accepted)

    def test_inquiry_and_preparation_are_read_only(self):
        for intent in ("inquiry", "prepare"):
            owner, coordinator = runtime()
            result = coordinator.process(interpretation=request(intent=intent))
            self.assertEqual(result.status, "inquiry" if intent == "inquiry" else "preparation")
            self.assertEqual(owner.minutes, 0)
            self.assertIsNone(coordinator.undertaking)

    def test_castle_begins_locally_then_returns_route_choice(self):
        owner, coordinator = runtime()
        self.assertEqual(coordinator.process(interpretation=request(activity="search", target="site-x")).status, "decision")
        original = coordinator.undertaking
        result = coordinator.process(resume=True)
        self.assertEqual(result.status, "decision")
        self.assertEqual(owner.minutes, 1)
        self.assertEqual(result.choices, ())
        self.assertEqual(len(result.step.choices), 2)
        answer = "2"
        result = coordinator.process(resume=True, answers=(answer,))
        self.assertEqual(result.status, "accepted")
        self.assertEqual(coordinator.undertaking.ref, original.ref)
        self.assertEqual(coordinator.undertaking.accepted_steps[:1], original.accepted_steps)

    def test_constraints_modify_same_activity_and_domain_participation(self):
        for constraints in (("quietly",), ("carefully",), ("quietly", "carefully")):
            owner, coordinator = runtime()
            result = coordinator.process(interpretation=request(activity="search", target="site-x", constraints=constraints))
            self.assertEqual(result.status, "decision")
            self.assertIn("character", result.responsibilities)
            self.assertEqual(coordinator.undertaking.activity, "search")
            self.assertEqual(coordinator.undertaking.constraints, constraints)

    def test_guard_circumstances_change_participation_and_control(self):
        _, routine = runtime()
        base = routine.process(interpretation=request())
        owner, guarded = runtime(context(actors=("guard",), conditions=("footsteps",)))
        risk = guarded.process(interpretation=request())
        self.assertNotIn("actors", base.responsibilities)
        self.assertIn("actors", risk.responsibilities)
        self.assertEqual(risk.status, "clarification")
        self.assertEqual(owner.minutes, 0)
        accepted = guarded.process(resume=True, answers=("1",))
        self.assertEqual(accepted.status, "accepted")
        self.assertEqual(guarded.process(resume=True).status, "complete")
        self.assertEqual(owner.minutes, 1)

    def test_hidden_actor_does_not_disclose_or_interrupt(self):
        owner, coordinator = runtime(context(actors=("HIDDEN-GUARD",), conditions=("hidden-footsteps",)))
        result = coordinator.process(interpretation=request())
        self.assertEqual(result.status, "accepted")
        self.assertIn("actors", result.responsibilities)
        self.assertNotIn("HIDDEN", str(result.player_result()))
        self.assertNotIn("footsteps", str(result.player_result()))

    def test_methods_need_player_choice_not_first_available(self):
        current = context()
        current = replace(current, targets=(replace(current.targets[0], methods=("key", "force"), routine_method=None),))
        owner, coordinator = runtime(current)
        self.assertEqual(coordinator.process(interpretation=request()).status, "clarification")
        self.assertEqual(owner.execute_calls, 0)
        self.assertEqual(coordinator.process(interpretation=request(method="force")).status, "accepted")

    def test_missing_means_cannot_be_waived_by_an_answer(self):
        owner, coordinator = runtime(context(means=()))
        result = coordinator.process(interpretation=request())
        self.assertEqual(result.status, "clarification")
        result = coordinator.process(resume=True, answers=("waive-tools",))
        self.assertEqual(result.failure, "authorization")
        self.assertEqual(owner.minutes, 0)

    def test_independent_intentions_do_not_execute_either(self):
        owner, coordinator = runtime()
        result = coordinator.process(interpretation=request(independent=("pay a merchant",)))
        self.assertEqual(result.status, "clarification")
        self.assertEqual(owner.execute_calls, 0)

    def test_geography_controls_next_step_without_invented_route(self):
        for routes, expected in (((), "decision"), (("east",), "accepted"), (("east", "west"), "decision")):
            owner, coordinator = runtime(context(routes=routes))
            result = coordinator.process(interpretation=request(activity="search", target="site-x"))
            self.assertEqual(result.status, expected)
            self.assertEqual(owner.minutes, 2 if expected == "accepted" else 1)

    def test_location_and_opaque_id_changes_use_same_runtime(self):
        owner, coordinator = runtime(context(location="unrelated-storage-42"))
        result = coordinator.process(interpretation=request(activity="search", target="site-x"))
        self.assertEqual(owner.accepted, ("site-x:unrelated-storage-42",))
        self.assertEqual(result.status, "decision")

    def test_established_unavailable_information_never_becomes_invention(self):
        owner, coordinator = runtime(context(unavailable=("HIDDEN-WARD",)))
        result = coordinator.process(interpretation=request())
        self.assertEqual(result.failure, "context")
        self.assertNotIn("HIDDEN", str(result.player_result()))
        self.assertEqual((owner.minutes, owner.execute_calls), (0, 0))

    def test_malformed_interpretations_are_contained(self):
        for proposal in (object(), {}, request(intent="nonsense"), request(target=42), request(constraints=["quietly"]),
                         request(independent="attack"), request(ambiguous="yes"), request(method=[])):
            owner, coordinator = runtime()
            result = coordinator.process(interpretation=proposal)
            self.assertEqual(result.failure, "interpretation")
            self.assertEqual(owner.minutes, 0)

    def test_unavailable_method_or_domain_cannot_be_inferred(self):
        owner, coordinator = runtime()
        self.assertEqual(coordinator.process(interpretation=request(method="missing-scroll")).failure, "authorization")
        self.assertEqual(coordinator.process(interpretation=request(activity="combat")).failure, "routing")
        self.assertEqual(owner.execute_calls, 0)

    def test_constraint_conflict_and_unknown_constraint_fail_closed(self):
        owner, coordinator = runtime()
        owner.conflicts = ("quietly",)
        self.assertEqual(coordinator.process(interpretation=request(constraints=("quietly",))).status, "clarification")
        self.assertEqual(coordinator.process(interpretation=request(constraints=("no-spending",))).failure, "authorization")
        self.assertEqual(owner.execute_calls, 0)

    def test_supplier_failures_are_safe_and_do_not_advance(self):
        for failure, category in (("context", "context"), ("assess", "domain"), ("execute", "technical")):
            owner, coordinator = runtime()
            owner.failure = failure
            result = coordinator.process(interpretation=request())
            self.assertEqual(result.failure, category)
            self.assertEqual((owner.minutes, owner.accepted), (0, ()))
            self.assertNotIn("HIDDEN", str(result.player_result()))

    def test_public_refs_must_be_character_accessible(self):
        owner, coordinator = runtime()
        original = owner.assess(request_undertaking(), owner.current)
        for step in (replace(original, public_refs=("HIDDEN",)), replace(original, choices=(("risk", "HIDDEN"),)),
                     replace(original, checkpoint=ActivityCheckpoint("wrong", "handle"))):
            owner.override = step
            result = coordinator.process(interpretation=request())
            self.assertNotEqual(result.status, "accepted")
            self.assertNotIn("HIDDEN", str(result.player_result()))
        self.assertEqual(owner.execute_calls, 0)

    def test_stale_decision_context_and_domain_changes_are_rejected(self):
        for change in ("context", "domain"):
            owner, coordinator = runtime()
            decision = coordinator.decide(interpretation=request())
            if change == "context":
                owner.current = replace(owner.current, means=())
            else:
                owner.required_means = ("absent",)
            result = coordinator.execute(decision)
            self.assertEqual(result.status, "unresolved")
            self.assertEqual(owner.execute_calls, 0)

    def test_permit_is_exact_single_use_and_cannot_be_forged(self):
        owner, coordinator = runtime()
        permit = coordinator.decide(interpretation=request())
        self.assertEqual(coordinator.execute(replace(permit)).failure, "authorization")
        self.assertEqual(coordinator.execute(permit).status, "accepted")
        self.assertEqual(coordinator.execute(permit).failure, "authorization")
        self.assertEqual(owner.execute_calls, 1)

    def test_fresh_decision_retires_prior_permission(self):
        owner, coordinator = runtime()
        permit = coordinator.decide(interpretation=request())
        coordinator.decide(interpretation=request(ambiguous=True))
        self.assertEqual(coordinator.execute(permit).failure, "authorization")
        self.assertEqual(owner.execute_calls, 0)

    def test_invalid_receipt_and_changed_context_failure_are_contained(self):
        for receipt in (None, AcceptedStep("wrong-reference"), AcceptedStep("door-x:hall-a", ("HIDDEN",))):
            owner, coordinator = runtime()
            with patch.object(owner, "execute", return_value=receipt):
                result = coordinator.process(interpretation=request())
            self.assertEqual(result.failure, "technical")
            self.assertEqual(owner.minutes, 0)
            self.assertEqual(coordinator.undertaking.accepted_steps, ())
            self.assertNotIn("HIDDEN", str(result.player_result()))
        owner, coordinator = runtime()
        permit = coordinator.decide(interpretation=request())
        owner.failure = "context"
        self.assertEqual(coordinator.execute(permit).failure, "context")
        self.assertEqual(owner.execute_calls, 0)

    def test_changed_risk_does_not_accept_old_choice_key(self):
        owner, coordinator = runtime(context(conditions=("footsteps",)))
        coordinator.process(interpretation=request())
        owner.current = replace(owner.current, revision="revision-2")
        result = coordinator.process(resume=True, answers=("1",))
        self.assertEqual(result.failure, "authorization")
        self.assertEqual(owner.execute_calls, 0)

    def test_answered_risk_survives_rephrasing_in_same_circumstances(self):
        owner, coordinator = runtime(context(conditions=("footsteps",)))
        coordinator.decide(interpretation=request())
        prior = coordinator.decide(resume=True, answers=("1",))
        self.assertEqual(prior.status, "proceed")
        fresh = coordinator.decide(interpretation=request(objective="Open that door"))
        self.assertEqual(fresh.status, "proceed")
        self.assertEqual(coordinator.execute(prior).failure, "authorization")
        self.assertEqual(coordinator.execute(fresh).status, "accepted")

    def test_rephrasing_preserves_restrictions_and_accepted_refs(self):
        owner, coordinator = runtime()
        coordinator.process(interpretation=request(constraints=("carefully",)))
        before = coordinator.undertaking
        result = coordinator.process(interpretation=request(objective="Open it"))
        self.assertEqual(result.status, "complete")
        self.assertEqual(coordinator.undertaking.ref, before.ref)
        self.assertEqual(coordinator.undertaking.constraints, ("carefully",))
        self.assertEqual(owner.minutes, 1)

    def test_explicit_method_change_preserves_accepted_progress_and_constraints(self):
        current = context()
        current = replace(current, targets=(replace(current.targets[0], methods=("handle", "key")),))
        owner, coordinator = runtime(current)
        coordinator.process(interpretation=request(constraints=("carefully",)))
        accepted = coordinator.undertaking.accepted_steps
        result = coordinator.process(interpretation=request(method="key"))
        self.assertEqual(result.status, "complete")
        self.assertEqual(coordinator.undertaking.accepted_steps, accepted)
        self.assertEqual(coordinator.undertaking.constraints, ("carefully",))
        self.assertEqual(owner.minutes, 1)

    def test_clear_retires_continuity_and_execution_permission(self):
        owner, coordinator = runtime()
        permit = coordinator.decide(interpretation=request())
        coordinator.clear()
        self.assertEqual(coordinator.execute(permit).failure, "authorization")
        self.assertEqual(coordinator.process(resume=True).failure, "authorization")

    def test_resume_revalidates_target_method_and_means(self):
        for change in ("target", "method", "means"):
            owner, coordinator = runtime()
            coordinator.process(interpretation=request(activity="search", target="site-x"))
            if change == "target":
                owner.current = replace(owner.current, targets=())
            elif change == "method":
                owner.current = replace(owner.current, targets=(replace(owner.current.targets[1], methods=(), routine_method=None),))
            else:
                owner.current = replace(owner.current, means=())
            result = coordinator.process(resume=True)
            self.assertNotEqual(result.status, "accepted")
            self.assertEqual(owner.minutes, 1)

    def test_numbered_choices_exclude_internal_keys_and_multiple_answers(self):
        owner, coordinator = runtime(context(conditions=("footsteps",)))
        decision = coordinator.process(interpretation=request())
        public = decision.player_result()["coordination"]["choices"]
        self.assertEqual([choice["id"] for choice in public], ["1"])
        self.assertNotIn("revision", str(public))
        self.assertEqual(coordinator.process(resume=True, answers=("1", "2")).failure, "interpretation")
        self.assertEqual(owner.minutes, 0)
    def test_contradictory_api_requests_are_contained(self):
        owner, coordinator = runtime()
        for kwargs in (dict(text="open door", interpretation=request()),
                       dict(interpretation=request(), answers=("1",)),
                       dict(text="pay someone", resume=True), dict(resume="yes")):
            self.assertEqual(coordinator.process(**kwargs).failure, "interpretation")
        self.assertEqual(owner.execute_calls, 0)

    def test_malformed_context_and_checkpoint_do_not_reach_execution(self):
        for invalid in (replace(context(), accessible=(("x", "text"), ("x", "other"))),
                        replace(context(), means=["hands"]),
                        replace(context(), targets=(replace(context().targets[0], routine_method="absent"),))):
            owner, coordinator = runtime(invalid)
            self.assertEqual(coordinator.process(interpretation=request()).failure, "context")
            self.assertEqual(owner.execute_calls, 0)
        owner, coordinator = runtime()
        step = owner.assess(request_undertaking(), owner.current)
        owner.override = replace(step, checkpoint=replace(step.checkpoint, blocked="no"))
        self.assertEqual(coordinator.process(interpretation=request()).failure, "domain")
        self.assertEqual(owner.execute_calls, 0)

    def test_unanswered_new_risk_is_not_waived_by_previous_answer(self):
        owner, coordinator = runtime(context(conditions=("footsteps",)))
        coordinator.process(interpretation=request(activity="search", target="site-x"))
        self.assertEqual(coordinator.process(resume=True, answers=("1",)).status, "decision")
        result = coordinator.process(resume=True)
        self.assertEqual(result.status, "decision")
        self.assertEqual(owner.minutes, 1)


def request_undertaking():
    from engine.gameplay_coordination import Undertaking
    return Undertaking("1", "open", "open", "door-x", "handle")


class BoundedLanguage(OfflineCase):
    def test_explicit_supported_language_modes_constraints_and_method(self):
        cases = (("Can I open the door?", "inquiry", (), None),
                 ("Could I search the castle?", "inquiry", (), None),
                 ("How can I open the door?", "inquiry", (), None),
                 ("Prepare to open the door", "prepare", (), None),
                 ("Open the door", "commit", (), None),
                 ("Search the castle quietly", "commit", ("quietly",), None),
                 ("Search the castle carefully", "commit", ("carefully",), None),
                 ("Open the door using handle", "commit", (), "handle"))
        for text, intent, constraints, method in cases:
            with self.subTest(text=text):
                proposal = interpret(text, context())
                self.assertEqual((proposal.intent, proposal.constraints, proposal.method), (intent, constraints, method))
                self.assertFalse(proposal.ambiguous)

    def test_bounded_runtime_not_just_parser(self):
        for text, expected in (("Open the door", "accepted"), ("Can I open the door?", "inquiry"),
                               ("Prepare to open the door", "preparation"), ("Search the castle quietly", "decision"),
                               ("Open the door or search the castle", "clarification"),
                               ("Open the door and pay the merchant", "clarification"),
                               ("Open the door?", "clarification"), ("Open the unknown thing", "clarification"),
                               ("Open the door without permission", "clarification")):
            owner, coordinator = runtime()
            result = coordinator.process(text=text)
            self.assertEqual(result.status, expected, text)
            self.assertEqual(owner.execute_calls, 1 if expected in {"accepted", "decision"} else 0)

    def test_unclaimed_language_is_distinct_from_claimed_unsupported(self):
        _, coordinator = runtime()
        self.assertIsNone(coordinator.process(text="help"))
        self.assertIsNotNone(coordinator.process(text="search"))


class IntegratedGameEngine(OfflineCase):
    def engine(self, owner=None):
        return GameEngine("data/regions/market_passage_v1.json", **({
            "coordination_context": owner.supply, "coordination_domain": owner} if owner else {}))

    def test_gameengine_common_runtime_all_eight_situations(self):
        cases = (("Open the door", context(), "accepted"),
                 ("Can I open the door?", context(), "inquiry"),
                 ("Search the castle", context(), "decision"),
                 ("Search the castle quietly", context(), "decision"),
                 ("Open the door", context(actors=("guard",), conditions=("footsteps",)), "clarification"),
                 ("Open the door or use magic", context(), "clarification"),
                 ("Open the door and search the castle", context(), "clarification"),
                 ("Open the door", context(means=()), "clarification"))
        for text, current, expected in cases:
            owner = SituatedAuthority(current)
            engine = self.engine(owner)
            before = engine.get_world_state()
            with patch.object(engine, "_process_legacy_command", side_effect=AssertionError("claimed input fell through")), \
                 patch.object(engine, "process_contextual_action", side_effect=AssertionError("claimed input fell through")):
                result = engine.process_command(text)
            self.assertEqual(result["coordination"]["status"], expected, text)
            self.assertEqual(engine.get_world_state(), before)  # Fixture owns its separate stipulated results.
            self.assertEqual(owner.minutes, 1 if expected in {"accepted", "decision"} else 0)

    def test_production_scene_observation_uses_existing_safe_projection(self):
        engine = self.engine()
        before = build_save_data(engine)
        result = engine.process_command("Observe surroundings")
        self.assertEqual(result["coordination"]["status"], "accepted")
        self.assertEqual(result["message"], engine.get_player_perception()["visible"]["location"]["description_seed"])
        self.assertEqual(build_save_data(engine), before)

    def test_default_unsupported_claimed_input_is_terminal(self):
        engine = self.engine()
        before = deepcopy(engine.get_world_state())
        with patch.object(engine, "_process_legacy_command", side_effect=AssertionError("fallthrough")):
            for text in ("Open the door", "Search the castle", "Can I open the door?", "Prepare to search the castle"):
                result = engine.process_command(text)
                self.assertIn(result["coordination"]["status"], {"clarification", "unresolved"})
        self.assertEqual(engine.get_world_state(), before)

    def test_unclaimed_commands_keep_supported_routes(self):
        engine = self.engine()
        with patch.object(engine, "process_contextual_action", return_value=None), \
             patch.object(engine, "process_contextual_investigation", return_value=None), \
             patch.object(engine, "_process_legacy_command", return_value={"success": True, "message": "legacy"}) as legacy:
            engine.process_command("help")
        legacy.assert_called_once_with("help")

    def test_supplied_interpretation_crosses_same_engine_runtime(self):
        owner = SituatedAuthority()
        engine = self.engine(owner)
        result = engine.process_coordination(interpretation=request(activity="search", target="site-x"))
        self.assertEqual(result["coordination"]["status"], "decision")
        self.assertEqual(engine.process_coordination(resume=True)["coordination"]["status"], "decision")

    def test_engine_reset_clears_unsaved_undertaking_and_old_permit(self):
        engine = self.engine()
        engine.process_command("Observe surroundings")
        self.assertIsNotNone(engine._coordination.undertaking)
        engine.reset()
        self.assertIsNone(engine._coordination.undertaking)
        self.assertEqual(engine.process_coordination(resume=True)["coordination"]["failure"], "authorization")

    def test_errors_do_not_reach_legacy_or_disclose_supplier_exception(self):
        owner = SituatedAuthority()
        engine = self.engine(owner)
        before = engine.get_world_state()
        for failure in ("context", "assess", "execute"):
            owner.failure = failure
            with patch.object(engine, "_process_legacy_command", side_effect=AssertionError("fallthrough")):
                result = engine.process_command("Open the door")
            self.assertNotIn("HIDDEN", str(result))
            self.assertEqual(engine.get_world_state(), before)
            self.assertEqual(owner.minutes, 0)


class ProgressionCorrection(OfflineCase):
    def test_domain_positive_negative_incomplete_and_unresolved_meanings_survive(self):
        samples = (("positive", "You find a fresh scrape beside the sill."),
                   ("negative", "No tracks are found in the area examined."),
                   ("incomplete", "Only the near half of the hall has been examined."),
                   ("unresolved", "The marks remain too indistinct to identify."))
        for kind, text in samples:
            owner, coordinator = runtime()
            owner.result_kind, owner.result_text = kind, text
            decision = coordinator.process(text="search castle")
            public = decision.player_result()["coordination"]["results"]
            self.assertEqual(public, [{"outcome": kind, "text": text}])
            self.assertIn(text, decision.message)
            self.assertNotIn("HIDDEN", str(decision.player_result()))

    def test_result_and_natural_boundary_arrive_in_one_command(self):
        owner, coordinator = runtime()
        decision = coordinator.process(text="search castle")
        self.assertEqual(decision.status, "decision")
        self.assertIn(owner.result_text, decision.message)
        self.assertIn("One passage leads east", decision.message)
        self.assertEqual(decision.player_result()["coordination"]["choices"], [])
        self.assertNotIn("?", decision.message)
        self.assertNotIn("Choose", decision.message)
        self.assertEqual(owner.minutes, 1)

    def test_free_form_direction_uses_disclosed_owner_scope(self):
        for direction in ("east", "west"):
            owner, coordinator = runtime()
            coordinator.process(text="search castle")
            result = coordinator.process(text="search " + direction)
            self.assertEqual(result.status, "accepted")
            self.assertEqual(owner.minutes, 2)
            self.assertIn("passage to the " + direction, result.message)
            self.assertEqual(owner.selected_directions, (direction,))
            self.assertEqual(len(coordinator.undertaking.accepted_steps), 2)

    def test_refinement_is_prospective_and_does_not_repeat_accepted_hall(self):
        owner, coordinator = runtime()
        first = coordinator.process(text="search castle")
        original_refs = coordinator.undertaking.accepted_steps
        refined = coordinator.process(text="search castle carefully")
        self.assertEqual(owner.minutes, 1)
        self.assertEqual(coordinator.undertaking.accepted_steps, original_refs)
        self.assertEqual(refined.results, ())
        self.assertNotIn("No useful signs", refined.message)  # No invented rerun or new finding.
        self.assertEqual(owner.executed_constraints, ((),))
        coordinator.process(text="search west")
        self.assertEqual(owner.executed_constraints, ((), ("carefully",)))
        self.assertIn("No useful signs", first.message)

    def test_new_constraint_is_enforced_before_any_subsequent_work(self):
        owner, coordinator = runtime()
        coordinator.process(text="search castle")
        owner.conflicts = ("carefully",)
        coordinator.process(text="search castle carefully")
        coordinator.process(text="search west")
        self.assertEqual(owner.minutes, 1)
        self.assertEqual(owner.executed_constraints, ((),))

    def test_one_supported_route_progresses_without_an_extra_command(self):
        owner, coordinator = runtime(context(routes=("east",)))
        decision = coordinator.process(text="search castle")
        self.assertEqual(decision.status, "accepted")
        self.assertEqual(owner.minutes, 2)
        self.assertEqual(len(decision.results), 2)
        self.assertEqual(decision.choices, ())
        self.assertIn(owner.result_text, decision.message)
        self.assertIn("passage to the east", decision.message)
        self.assertEqual(owner.selected_directions, ("east",))

    def test_stale_free_form_direction_never_executes_or_falls_through(self):
        owner = SituatedAuthority()
        engine = GameEngine("data/regions/market_passage_v1.json", coordination_context=owner.supply,
                            coordination_domain=owner)
        engine.process_command("search castle")
        owner.current = replace(owner.current, means=(), revision="changed")
        with patch.object(engine, "_process_legacy_command", side_effect=AssertionError("fallthrough")):
            result = engine.process_command("search west")
        self.assertEqual(result["coordination"]["failure"], "authorization")
        self.assertEqual(owner.minutes, 1)

    def test_direction_inquiry_or_question_never_commits(self):
        for text in ("Can I search west?", "search west?"):
            owner, coordinator = runtime()
            coordinator.process(text="search castle")
            result = coordinator.process(text=text)
            self.assertNotEqual(result.status, "accepted")
            self.assertEqual(owner.minutes, 1)
            self.assertEqual(owner.selected_directions, ())

    def test_changed_means_after_first_acceptance_stops_automatic_next_step(self):
        owner, coordinator = runtime(context(routes=("east",)))
        execute = owner.execute
        def remove_means(*args):
            receipt = execute(*args)
            owner.current = replace(owner.current, means=(), revision="changed-means")
            return receipt
        with patch.object(owner, "execute", side_effect=remove_means):
            result = coordinator.process(text="search castle")
        self.assertEqual(result.status, "decision")
        self.assertEqual(owner.minutes, 1)
        self.assertEqual(owner.selected_directions, ())
        self.assertEqual(len(result.results), 1)

    def test_accepted_result_survives_failed_next_assessment(self):
        owner, coordinator = runtime()
        execute = owner.execute
        def publish_then_lose_context(*args):
            receipt = execute(*args)
            owner.failure = "context"
            return receipt
        with patch.object(owner, "execute", side_effect=publish_then_lose_context):
            result = coordinator.process(text="search castle")
        self.assertEqual(result.failure, "context")
        self.assertEqual(owner.minutes, 1)
        self.assertEqual(result.results[0].outcome, "negative")
        self.assertIn(owner.result_text, result.message)
        self.assertNotIn("No activity was executed", result.message)
        self.assertEqual(coordinator.undertaking.accepted_steps, owner.accepted)

    def test_later_execution_failure_does_not_erase_first_result(self):
        owner, coordinator = runtime(context(routes=("east",)))
        execute = owner.execute
        def fail_second(undertaking, step, current):
            if undertaking.accepted_steps:
                raise RuntimeError("HIDDEN-TECHNICAL")
            return execute(undertaking, step, current)
        with patch.object(owner, "execute", side_effect=fail_second):
            result = coordinator.process(text="search castle")
        self.assertEqual(result.failure, "technical")
        self.assertEqual(owner.minutes, 1)
        self.assertIn(owner.result_text, result.message)
        self.assertNotIn("HIDDEN", str(result.player_result()))
        self.assertEqual(len(result.results), 1)

    def test_explicit_ambiguity_still_asks_for_clarification(self):
        owner, coordinator = runtime()
        result = coordinator.process(text="open door or use another method")
        self.assertEqual(result.status, "clarification")
        self.assertEqual(owner.minutes, 0)

    def test_missing_result_description_does_not_mean_no_findings(self):
        owner, coordinator = runtime()
        with patch.object(owner, "execute", return_value=AcceptedStep("door-x:hall-a")):
            result = coordinator.process(text="open door")
        self.assertIn("no supplied description", result.message)
        self.assertNotIn("nothing", result.message)
        self.assertNotIn("No useful signs", result.message)

    def test_unbounded_supplier_stops_without_queuing_or_repeating_a_step(self):
        from engine.gameplay_coordination import DomainStep
        owner, coordinator = runtime()
        def next_step(undertaking, current):
            return DomainStep(str(len(undertaking.accepted_steps)), ActivityCheckpoint(undertaking.ref, undertaking.method),
                              ("world",))
        with patch.object(owner, "assess", side_effect=next_step):
            result = coordinator.process(text="open door")
        self.assertEqual(result.failure, "domain")
        self.assertEqual(owner.minutes, 16)
        self.assertEqual(len(set(owner.accepted)), 16)
        self.assertIsNone(coordinator._pending)

if __name__ == "__main__":
    unittest.main()
