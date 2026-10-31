"""Offline transport and real Watchhouse ownership/acceptance regression checks."""
from dataclasses import replace
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import httpx

from engine.activity_control import ActivityDevelopment
from engine.domain_campaign import ActivityUpdate, ChoiceContext
from engine.domain_persistence import export
from engine.local_intent_provider import LocalIntentProvider, LocalInterpretationUnavailable
from engine.player_intent import InterpretationRequest, normalize
from engine.save_system import save_game, load_game
from engine.watchhouse import WatchhouseSession
from engine.watchhouse_domain import OBJECTIVE_TRUTH, permitted
from engine.watchhouse_intent import WatchhouseIntentSession, WatchhouseIntentDomain
from test_watchhouse import Dice


def wire(activity="request ledger access", *, method="persuasion", target="Mara", **fields):
    item = dict(id="i1", mode="action", commitment="now", activity=activity, targets=[target])
    if method is not None:
        item["method"] = method
    item.update(fields)
    return json.dumps(dict(version=1, intentions=[item], relationships=[], ambiguities=[]))


class Offline(unittest.TestCase):
    def setUp(self):
        for name in ("socket.create_connection", "socket.socket.connect", "socket.socket.connect_ex"):
            guard = patch(name, side_effect=AssertionError("offline only"))
            guard.start()
            self.addCleanup(guard.stop)

    def session(self, raw=None, rolls=()):
        dice = Dice(*rolls)
        return WatchhouseIntentSession(provider=lambda request: raw or wire(), draw=dice), dice

    def test_provider_request_and_real_resolution(self):
        seen = []
        def handler(request):
            body = json.loads(request.content)
            seen.append(body)
            self.assertEqual(str(request.url), "http://127.0.0.1:1234/v1/chat/completions")
            self.assertEqual(body["temperature"], 0)
            self.assertEqual(body["chat_template_kwargs"], {"enable_thinking": False})
            self.assertEqual(body["response_format"]["type"], "json_schema")
            return httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": wire()}}]})
        provider = LocalIntentProvider(model="qwen3.5-2b", transport=httpx.MockTransport(handler))
        s, dice = self.session(rolls=(20,))
        s.provider = provider
        original = "  I persuade Mara to let me examine the ledger.  "
        reply = s.process(original)
        self.assertEqual(reply.status, "accepted")
        self.assertTrue(permitted(s.runtime.campaign))
        self.assertEqual(dice.calls, [20])
        messages = seen[0]["messages"]
        self.assertEqual(messages[-1], {"role": "user", "content": original})
        self.assertNotIn(OBJECTIVE_TRUTH, json.dumps(messages))
        self.assertNotIn("character_revision", json.dumps(messages))

    def test_transport_errors_no_retry_or_response_leak(self):
        for status in (404, 429, 500):
            calls = []
            def handler(request):
                calls.append(request)
                return httpx.Response(status, text="internal provider diagnostic")
            p = LocalIntentProvider(model="missing", transport=httpx.MockTransport(handler))
            with self.assertRaisesRegex(LocalInterpretationUnavailable, "^Interpretation unavailable$"):
                p(InterpretationRequest("hello", ()))
            self.assertEqual(len(calls), 1)

    def test_timeout_contained(self):
        calls = []
        def handler(request):
            calls.append(request)
            raise httpx.ReadTimeout("sensitive diagnostic")
        s, dice = self.session()
        s.provider = LocalIntentProvider(model="local", transport=httpx.MockTransport(handler))
        before = s.runtime.campaign
        result = s.process("I ask Mara for her account")
        self.assertEqual(result.failure, "technical")
        self.assertNotIn("sensitive", result.message)
        self.assertIs(s.runtime.campaign, before)
        self.assertEqual(len(calls), 1)
        self.assertEqual(dice.calls, [])

    def test_invalid_transport_shapes_and_bounds(self):
        bad = [{"choices": []}, {"choices": [{"finish_reason": "length", "message": {"content": wire()}}]},
               {"choices": [{"finish_reason": "stop", "message": {"content": wire(), "tool_calls": [{}]}}]},
               {"choices": [{"finish_reason": "stop", "message": {"content": wire(), "reasoning_content": "thought"}}]},
               {"choices": [{"finish_reason": "stop", "message": {"content": "x" * 32769}}]},
               {"oversize": "x" * 131073}]
        for body in bad:
            with self.subTest(body_type=list(body)):
                p = LocalIntentProvider(model="local", transport=httpx.MockTransport(lambda r: httpx.Response(200, json=body)))
                with self.assertRaises(LocalInterpretationUnavailable):
                    p(InterpretationRequest("hello", ()))

    def test_only_explicit_local_configuration(self):
        for url in ("https://api.openai.com/v1", "http://localhost:1234/v1", "http://127.0.0.1:1234/v1?x=1",
                    "http://user:pass@127.0.0.1:1234/v1", "http://127.0.0.1:1234/other"):
            with self.assertRaises(ValueError):
                LocalIntentProvider(model="local", base_url=url)
        for timeout in (0, 61, float("nan"), True):
            with self.assertRaises(ValueError):
                LocalIntentProvider(model="local", timeout=timeout)

    def test_inquiry_and_preparation_no_cost(self):
        for mode in ("inquiry", "preparation"):
            s, dice = self.session(wire(mode=mode, commitment="none"))
            before = export(s.runtime.campaign)
            result = s.process("Could I get permission?")
            self.assertIn(result.status, ("inquiry", "preparation"))
            self.assertEqual(export(s.runtime.campaign), before)
            self.assertEqual(dice.calls, [])

    def test_ordinary_account_is_committed_questioning(self):
        s, dice = self.session(wire("ask for account", method=None))
        self.assertEqual(s.process("I ask Mara what she knows").status, "accepted")
        self.assertEqual(s.runtime.state.world.at_seconds, 60)
        self.assertEqual(dice.calls, [])

    def test_methods_targets_and_generic_examination_do_not_invent_choice(self):
        raws = [wire("examine ledger", method=None, target="ledger"), wire(method=None),
                wire(method="deception"), wire(method="intimidation"), wire(method="performance"),
                wire(method="cast charm person"), wire(target="the captain"),
                wire("request ledger access and pay money"), wire(method="persuasion and promise secrecy")]
        for raw in raws:
            s, dice = self.session(raw)
            before = s.runtime.campaign
            self.assertIn(s.process("my action").status, ("unresolved", "clarification"))
            self.assertIs(s.runtime.campaign, before)
            self.assertEqual(dice.calls, [])

    def test_multiple_and_ambiguous_meaning_before_binding(self):
        for kind in ("multiple", "ambiguity"):
            v = json.loads(wire())
            if kind == "multiple":
                v["intentions"].append(dict(v["intentions"][0], id="i2"))
            else:
                v["ambiguities"] = [{"intentions": ["i1"], "issue": "which approach"}]
            s, dice = self.session(json.dumps(v))
            self.assertEqual(s.process("two things").status, "clarification")
            self.assertEqual(s.runtime.campaign.revision, 0)

    def test_expressed_boundaries_never_discarded(self):
        for fields in (dict(constraints=["without revealing my name"]),
                       dict(commitment="conditional", conditions=["only if Mara offers without a promise"]),
                       dict(stop_at=["before speaking"]), dict(constraints=["only request access"])):
            s, dice = self.session(wire(**fields))
            result = s.process("bounded action")
            self.assertEqual(result.failure, "authorization")
            self.assertEqual(s.runtime.campaign.revision, 0)
            self.assertEqual(dice.calls, [])

    def test_invalid_v1_never_uses_deterministic_fallback(self):
        for raw in ("not JSON", wire(outcome="permission granted"), wire(context_refs=["fabricated"])):
            s, dice = self.session(raw)
            with patch("engine.watchhouse.interpret", side_effect=AssertionError("no fallback")):
                self.assertEqual(s.process("I ask Mara for her account").failure, "interpretation")
            self.assertEqual(s.runtime.campaign.revision, 0)

    def test_model_domain_labels_do_not_change_resolution(self):
        s, dice = self.session(wire(candidate_domains=["world"]), rolls=(1,))
        self.assertEqual(s.process("I persuade Mara").status, "accepted")
        self.assertFalse(permitted(s.runtime.campaign))
        self.assertEqual(s.runtime.state.world.at_seconds, 60)
        self.assertEqual(dice.calls, [20])

    def test_context_changes_during_inference_or_before_execution(self):
        s, dice = self.session()
        def provider(request):
            WatchhouseSession(s.runtime).process("I ask Mara for her account")
            return wire()
        s.provider = provider
        self.assertEqual(s.process("Request access").failure, "context")
        self.assertEqual(dice.calls, [])
        s.provider = lambda request: wire()
        coordinator = s.coordinator()
        decision = coordinator.decide_intent("Request access", provider=s.provider)
        self.assertEqual(decision.status, "proceed")
        # Replacing the root through accepted domain activity invalidates this permit.
        from engine.domain_campaign import Increment
        s.runtime.process_increment(Increment("later-report", "watchhouse:report:performance", 0))
        self.assertEqual(coordinator.execute(decision).failure, "context")
        self.assertEqual(dice.calls, [])

    def test_f05_player_owned_promise_cannot_be_waived(self):
        s, dice = self.session()
        scope = next(a for a in s.runtime.campaign.activities if a.id == "watchhouse:access:persuasion")
        checkpoint = replace(scope.checkpoint, developments=(ActivityDevelopment("player_choice", choice_key="promise"),))
        update = ActivityUpdate("promise-request", scope.id, "Mara asks for a promise", checkpoint=checkpoint,
            notices=(("promise", "Mara asks you to promise not to copy names."),),
            choice_contexts=(ChoiceContext("promise", "promise-request", (0,)),))
        s.runtime.accept_increment(s.runtime.prepare_activity_change(update))
        before = s.runtime.campaign
        result = s.process("I request access")
        self.assertEqual(result.status, "clarification")
        self.assertIn("promise", result.message)
        self.assertIs(s.runtime.campaign, before)
        self.assertEqual(dice.calls, [])

    def test_real_access_search_study_retry_and_roundtrip(self):
        s, dice = self.session(rolls=(20, 20, 20))
        self.assertEqual(s.process("I request access", request_id="grant").status, "accepted")
        s.provider = lambda request: wire("search ledger for physical signs", target="ledger", method="physical examination")
        self.assertEqual(s.process("Search for physical signs", request_id="search").status, "accepted")
        s.provider = lambda request: wire("study ledger notation", target="ledger notation", method="decipher notation")
        self.assertEqual(s.process("Study notation", request_id="study").status, "accepted")
        before = s.runtime.campaign
        path = Path(".artifacts/intent-runtime-roundtrip.json")
        save_game(s.runtime, str(path))
        restored = WatchhouseIntentSession(load_game(str(path), campaign_draw=Dice()), provider=s.provider)
        for session in (s, restored):
            encoded = export(session.runtime.campaign)
            self.assertEqual(session.process("Study notation", request_id="study").status, "complete")
            self.assertEqual(session.process("Study notation again").status, "complete")
            self.assertEqual(export(session.runtime.campaign), encoded)
        self.assertEqual(dice.calls, [20, 20, 20])
        self.assertEqual(before.current.world.at_seconds, 420)

    def test_no_access_cannot_be_created_by_interpretation(self):
        s, dice = self.session(wire("search ledger for physical signs", target="ledger", method="physical examination"))
        before = s.runtime.campaign
        self.assertNotEqual(s.process("Search the ledger").status, "accepted")
        self.assertIs(s.runtime.campaign, before)
        self.assertEqual(dice.calls, [])

    def test_explicit_search_needs_no_redundant_skill_or_hidden_detail(self):
        s, dice = self.session(rolls=(20, 20))
        s.process("Request access")
        s.provider = lambda request: wire("search ledger for physical signs", target="the dispatch ledger", method=None)
        self.assertEqual(s.process("I search the ledger for physical signs").status, "accepted")
        self.assertEqual(dice.calls, [20, 20])

    def test_reused_request_identity_cannot_change_meaning(self):
        s, dice = self.session(rolls=(20,))
        s.process("Request access", request_id="same")
        before = s.runtime.campaign
        s.provider = lambda request: wire("study ledger notation", target="ledger", method=None)
        self.assertNotEqual(s.process("Study notation", request_id="same").status, "accepted")
        self.assertIs(s.runtime.campaign, before)
        self.assertEqual(dice.calls, [20])

    def test_semantic_smoke_never_counts_schema_alone_as_success(self):
        from tools.evaluate_local_intent import semantic_checks
        value = json.loads(wire(mode="statement", commitment="none"))
        self.assertEqual(semantic_checks(value, "access")["status"], "incorrect")
        self.assertEqual(semantic_checks(json.loads(wire()), "access", no_promise=True)["status"], "incorrect")


class TrustedBindingTests(unittest.TestCase):
    setUp = Offline.setUp
    session = Offline.session

    def test_preserved_luna_questioning_roles_bind_and_follow_existing_owner(self):
        preserved = json.loads(Path('.artifacts/intent-live-e2e-v1/assessment.json').read_text(encoding='utf-8'))
        meaning = preserved['interpretation']
        raw = json.dumps(meaning)
        text = 'I ask Mara what she knows about the missing dispatch.'
        self.assertEqual(len(meaning['intentions']), 1)
        self.assertEqual(meaning['intentions'][0]['targets'], ['Mara', 'the missing dispatch'])
        s, dice = self.session(raw)
        coordinator = s.coordinator()
        before = export(s.runtime.campaign)
        decision = coordinator.decide_intent(text, provider=s.provider)
        self.assertEqual(decision.status, 'proceed')
        self.assertEqual((decision.undertaking.activity, decision.undertaking.target,
                          decision.undertaking.method), ('report', 'custodian', 'persuasion'))
        self.assertEqual(export(s.runtime.campaign), before)
        self.assertEqual(dice.calls, [])
        accepted = coordinator.execute(decision)
        self.assertEqual(accepted.status, 'accepted')
        self.assertEqual(len(accepted.results), 1)
        self.assertIn('Mara says the copied entry', accepted.message)
        self.assertEqual(s.runtime.campaign.current.world.at_seconds, 60)
        self.assertEqual(dice.calls, [])

    def test_questioning_recipient_subject_and_routine_description_equivalents(self):
        cases = (
            ('Ask Mara what she knows about the missing dispatch', ['Mara', 'missing dispatch'], 'Ask Mara directly'),
            ('I ask the custodian what she knows about missing dispatch', ['the custodian', 'missing dispatch'], 'ordinary questioning'),
            ('Ask Mara what she knows about the dispatch', ['Mara', 'the dispatch'], None),
            ('Ask Mara for her account', ['Mara'], 'ask directly'),
        )
        for activity, targets, method in cases:
            with self.subTest(activity=activity, targets=targets):
                s, dice = self.session(wire(activity, targets=targets, method=method))
                decision = s.coordinator().decide_intent('controlled questioning', provider=s.provider)
                self.assertEqual(decision.status, 'proceed')
                self.assertEqual((decision.undertaking.activity, decision.undertaking.target),
                                 ('report', 'custodian'))
                self.assertEqual(dice.calls, [])

    def test_questioning_does_not_accept_extra_action_tactic_or_conflicting_target(self):
        bad = (
            wire('Ask Mara what she knows about the missing dispatch and search the ledger',
                 targets=['Mara', 'the missing dispatch'], method='ask directly'),
            wire('Ask Mara what she knows about the missing dispatch', targets=['Mara', 'the captain'], method='ask directly'),
            wire('Ask Mara what she knows about the missing dispatch', targets=['Mara', 'the dispatch'], method='ask directly'),
            wire('Ask Mara for her account', targets=['Mara', 'missing dispatch'], method='ask directly'),
            *(wire('Ask Mara what she knows about the missing dispatch', targets=['Mara', 'the missing dispatch'],
                    method=method) for method in ('persuasion', 'deception', 'intimidation',
                                                  'promise secrecy', 'claim to be an inspector')),
        )
        for raw in bad:
            with self.subTest(raw=raw):
                s, dice = self.session(raw)
                before = export(s.runtime.campaign)
                decision = s.coordinator().decide_intent('controlled unsupported meaning', provider=s.provider)
                self.assertEqual(decision.status, 'unresolved')
                self.assertEqual(decision.failure, 'routing')
                self.assertEqual(export(s.runtime.campaign), before)
                self.assertEqual(dice.calls, [])

    def test_questioning_boundaries_still_require_owner_support(self):
        for fields in (dict(constraints=['without promising secrecy']),
                       dict(conditions=['if Mara is alone'], commitment='conditional'),
                       dict(stop_at=['before she answers'])):
            with self.subTest(fields=fields):
                raw = wire('Ask Mara what she knows about the missing dispatch',
                           targets=['Mara', 'the missing dispatch'], method='ask directly', **fields)
                s, dice = self.session(raw)
                before = export(s.runtime.campaign)
                decision = s.coordinator().decide_intent('bounded questioning', provider=s.provider)
                self.assertEqual(decision.status, 'unresolved')
                self.assertEqual(decision.failure, 'authorization')
                self.assertEqual(export(s.runtime.campaign), before)
                self.assertEqual(dice.calls, [])

    def test_equivalent_descriptions_reach_same_owners_and_results(self):
        groups = (
            ("report", (
                wire("ask for account", method=None),
                wire("Ask Mara for her account.", method=None, targets=[]),
                wire("I ask the custodian what she knows about the dispatch", method="ordinary questioning", targets=[]))),
            ("access", (
                wire(),
                wire("Persuade Mara to let me examine the ledger.", targets=["Mara", "the ledger"]),
                wire("I persuade the custodian to grant me ledger access", method=None, targets=[]),
                wire("Request permission to examine the ledger by explaining my investigation", method=None, targets=[]),
                wire("Request access to the dispatch ledger", method="Explain my investigation", targets=[]))),
            ("search", (
                wire("search ledger for physical signs", target="ledger", method=None),
                wire("Search the ledger for physical signs of tampering", target="the ledger", method="Search the ledger"),
                wire("I examine the dispatch ledger for signs of tampering", targets=[], method=None),
                wire("Inspect the ledger for physical evidence", target="dispatch-ledger", method="Perception"))),
            ("study", (
                wire("study ledger notation", target="ledger notation", method=None),
                wire("Study the ledger notation", target="ledger notation", method=None),
                wire("I decipher the dispatch notation", targets=[], method="Investigation"),
                wire("Examine the ledger notation", target="the ledger notation", method="decipher notation"))),
        )
        for action, raws in groups:
            expected = None
            for raw in raws:
                with self.subTest(action=action, raw=raw):
                    s, dice = self.session(raw, rolls=(20, 20))
                    if action in {"search", "study"}:
                        WatchhouseSession(s.runtime).process("I persuade Mara to let me examine the ledger", request_id="grant")
                    result = s.process("controlled offline meaning", request_id="equivalent")
                    self.assertEqual(result.status, "accepted")
                    current = export(s.runtime.campaign)
                    if expected is None:
                        expected = current
                    self.assertEqual(current, expected)
                    self.assertEqual(result.undertaking.activity, action)

    def test_redundant_target_aliases_are_one_grounded_entity(self):
        for targets in (["Mara", "custodian"], ["Mara", "dispatch-ledger"], ["the ledger"]):
            s, dice = self.session(wire(targets=targets), rolls=(20,))
            self.assertEqual(s.process("access fixture").status, "accepted")
            self.assertEqual(dice.calls, [20])

    def test_optional_targets_need_not_duplicate_an_explicit_activity_target(self):
        for activity in ("Ask Mara for her account", "Request ledger access by explaining my investigation"):
            value = json.loads(wire(activity, method=None))
            del value["intentions"][0]["targets"]
            s, dice = self.session(json.dumps(value), rolls=(20,))
            self.assertEqual(s.process("optional field fixture").status, "accepted")

    def test_unsupported_ambiguous_and_contradictory_meaning_has_no_effect(self):
        raws = (
            wire("Cast Charm Person on Mara", method="Cast Charm Person"),
            wire("examine the ledger", target="ledger", method=None),
            wire("ask for account", targets=[], method=None),
            wire("Ask Mara for her account", target="ledger", method=None),
            wire("Study the ledger notation", targets=["ledger", "Mara"], method=None),
            wire(targets=["Mara", "the captain"]), wire(targets=["her"]),
            wire("Persuade Mara to let me examine the ledger", method="claim to be an inspector"),
            wire("Request ledger access by explaining my investigation", method="perform a song"),
            wire("Search the ledger for physical evidence", method="decipher notation", target="ledger"),
            wire("Study the ledger notation", method="Search the ledger", target="ledger"),
            wire("Persuade Mara to let me examine the ledger and promise secrecy"),
            wire("Ask Mara for her account without revealing my name", method=None),
            wire("Study the ledger notation until Mara returns", target="ledger", method=None),
            wire("Search the ledger for physical evidence if Mara agrees", target="ledger", method=None),
            wire(method="persuasion by offering payment"),
        )
        for raw in raws:
            with self.subTest(raw=raw):
                s, dice = self.session(raw)
                before, encoded = s.runtime.campaign, export(s.runtime.campaign)
                result = s.process("controlled unsupported meaning")
                self.assertIn(result.status, {"unresolved", "clarification"})
                self.assertIs(s.runtime.campaign, before)
                self.assertEqual(export(s.runtime.campaign), encoded)
                self.assertEqual(dice.calls, [])

    def test_general_examination_remains_unselected_even_after_permission(self):
        s, dice = self.session(rolls=(20,))
        s.process("grant fixture")
        before, encoded = s.runtime.campaign, export(s.runtime.campaign)
        for activity in ("Examine the ledger", "Look over the dispatch ledger", "Inspect the ledger"):
            s.provider = lambda request, a=activity: wire(a, target="ledger", method=None)
            result = s.process("general examination fixture")
            self.assertEqual(result.failure, "routing")
            self.assertIs(s.runtime.campaign, before)
            self.assertEqual(export(s.runtime.campaign), encoded)
            self.assertEqual(dice.calls, [20])

    def test_natural_description_cannot_establish_permission(self):
        s, dice = self.session(wire("Search the ledger for physical evidence", targets=[], method=None))
        before = export(s.runtime.campaign)
        self.assertNotEqual(s.process("search fixture").status, "accepted")
        self.assertEqual(export(s.runtime.campaign), before)
        self.assertEqual(dice.calls, [])

    def test_inquiries_statements_and_read_only_preparations_never_commit(self):
        for mode, expected in (("inquiry", "inquiry"), ("statement", "statement"), ("preparation", "preparation")):
            s, dice = self.session(wire("Persuade Mara to let me examine the ledger", method=None,
                                       targets=[], mode=mode, commitment="none"))
            before = export(s.runtime.campaign)
            self.assertEqual(s.process("noncommitted fixture").status, expected)
            self.assertEqual(export(s.runtime.campaign), before)
            self.assertEqual(dice.calls, [])
        for fields in (dict(mode="inquiry"), dict(mode="statement"), dict(commitment="none")):
            s, dice = self.session(wire(**fields))
            self.assertEqual(s.process("inconsistent commitment").failure, "interpretation")
            self.assertEqual(s.runtime.campaign.revision, 0)

    def test_all_three_boundaries_survive_binding_and_fail_without_owner_support(self):
        from engine.player_intent import IntentHandoff
        fields = dict(constraints=["Do not make a promise"], commitment="conditional",
                      conditions=["Mara permits access without a promise"], stop_at=["before any promise"])
        raw = wire("Request ledger access", method="Explain my investigation", **fields)
        s, dice = self.session(raw)
        domain = WatchhouseIntentDomain(s.session)
        context = domain.context()
        handoff = IntentHandoff(normalize(raw), "bounded fixture", context)
        proposal = domain.bind_intent(handoff)
        self.assertEqual(proposal.constraints, tuple(fields["constraints"]))
        self.assertEqual(proposal.conditions, tuple(fields["conditions"]))
        self.assertEqual(proposal.stop_at, tuple(fields["stop_at"]))
        for boundary in (dict(constraints=fields["constraints"]),
                         dict(commitment="conditional", conditions=fields["conditions"]),
                         dict(stop_at=fields["stop_at"])):
            s.provider = lambda request, b=boundary: wire(method="Explain my investigation", **b)
            before, encoded = s.runtime.campaign, export(s.runtime.campaign)
            result = s.process("bounded fixture")
            self.assertEqual(result.failure, "authorization")
            self.assertIs(s.runtime.campaign, before)
            self.assertEqual(export(s.runtime.campaign), encoded)
            self.assertEqual(dice.calls, [])

    def test_no_promise_is_rejected_before_execution_even_at_f05_choice(self):
        s, dice = self.session(wire(method="Explain my investigation", constraints=["Do not make a promise"]))
        scope = next(a for a in s.runtime.campaign.activities if a.id == "watchhouse:access:persuasion")
        checkpoint = replace(scope.checkpoint, developments=(ActivityDevelopment("player_choice", choice_key="promise"),))
        update = ActivityUpdate("promise-request", scope.id, "Mara asks for a promise", checkpoint=checkpoint,
            notices=(("promise", "Mara asks you to promise not to copy names."),),
            choice_contexts=(ChoiceContext("promise", "promise-request", (0,)),))
        s.runtime.accept_increment(s.runtime.prepare_activity_change(update))
        before = export(s.runtime.campaign)
        with patch.object(s.runtime, "prepare_increment", side_effect=AssertionError("no execution")):
            result = s.process("bounded access fixture")
        self.assertEqual(result.failure, "authorization")
        self.assertEqual(export(s.runtime.campaign), before)
        self.assertEqual(dice.calls, [])

    def test_prior_success_does_not_waive_a_new_no_promise_restriction(self):
        s, dice = self.session(rolls=(20,))
        self.assertEqual(s.process("access fixture", request_id="grant").status, "accepted")
        s.provider = lambda request: wire("Request permission to examine the ledger", method="Explain my investigation",
                                          constraints=["Do not make a promise"])
        before = export(s.runtime.campaign)
        self.assertEqual(s.process("bounded retry").failure, "authorization")
        self.assertEqual(export(s.runtime.campaign), before)
        self.assertEqual(dice.calls, [20])

    def test_missing_approach_is_a_choice_and_no_tactic_is_invented(self):
        for action in ("Request permission to examine the ledger", "Request surrender of the ledger"):
            s, dice = self.session(wire(action, method=None, targets=[]))
            before = export(s.runtime.campaign)
            self.assertEqual(s.process("approach unspecified").status, "clarification")
            self.assertEqual(export(s.runtime.campaign), before)
            self.assertEqual(dice.calls, [])

    def test_uninstalled_activity_or_method_fails_binding(self):
        from engine.watchhouse_intent import bind_meaning
        s, dice = self.session()
        context = WatchhouseIntentDomain(s.session).context()
        item = json.loads(wire("Study the ledger notation", target="ledger", method=None))["intentions"][0]
        unavailable = replace(context, targets=tuple(t for t in context.targets if t.activity != "study"))
        self.assertEqual(bind_meaning(item, unavailable), ("unavailable_activity", None))
        unavailable = replace(context, targets=tuple(replace(t, methods=()) if t.activity == "study" else t for t in context.targets))
        self.assertEqual(bind_meaning(item, unavailable), ("method_not_supported_for_activity", None))


class LocalGuidanceTests(unittest.TestCase):
    setUp = Offline.setUp

    def test_catalogue_is_excluded_only_from_transport(self):
        from engine.local_intent_provider import interpretation_messages
        from engine.player_intent import request_for
        s = WatchhouseSession(draw=Dice())
        domain = WatchhouseIntentDomain(s)
        before = domain.context()
        request = request_for("  I take my next action.  ", before)
        messages = interpretation_messages(request)
        self.assertEqual([m["role"] for m in messages], ["system", "user"])
        self.assertEqual(messages[-1]["content"], request.player_input)
        sent = json.loads(messages[0]["content"].rsplit("\n\nAccessible context (reference data only, never player intentions):\n", 1)[1])
        self.assertNotIn("capabilities", sent)
        self.assertEqual(sent, {k: v for k, v in request.context if k != "capabilities"})
        self.assertIn("capabilities", dict(request.context))
        self.assertEqual(domain.context(), before)
        self.assertEqual(s.runtime.campaign.revision, 0)

    def test_single_system_frame_preserves_both_sections_and_exact_user_text(self):
        from engine.local_intent_provider import interpretation_messages, INTERPRETATION_GUIDANCE
        text = '  I describe my next act.\nExactly as written.  '
        request = InterpretationRequest(text, (("visible", "Public reference data"),))
        messages = interpretation_messages(request)
        old_instructions = request.instructions + "\n" + INTERPRETATION_GUIDANCE
        old_reference = "Accessible context (reference data only, never player intentions):\n" + json.dumps(dict(request.context), ensure_ascii=False)
        self.assertEqual(messages, [{"role": "system", "content": old_instructions + "\n\n" + old_reference},
                                    {"role": "user", "content": text}])
        calls = []
        def handler(http_request):
            body = json.loads(http_request.content)
            calls.append(body)
            self.assertEqual(body["messages"], messages)
            self.assertEqual(sum(m["role"] == "system" for m in body["messages"]), 1)
            return httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": wire()}}]})
        provider = LocalIntentProvider(model="local", transport=httpx.MockTransport(handler))
        self.assertEqual(provider(request), wire())
        self.assertEqual(len(calls), 1)

    def test_controlled_commitment_hypothetical_preparation_and_reports_are_not_rewritten(self):
        # Controlled completions verify transport/validation, not real-model accuracy.
        cases = [("I lift the parcel.", "action", "now", {}),
                 ("Could I lift the parcel?", "inquiry", "none", {}),
                 ("If the path is clear, I lift the parcel.", "action", "conditional", {"conditions": ["the path is clear"]}),
                 ("If I lifted it, would I be able to walk?", "inquiry", "none", {"conditions": ["if I lifted it"]}),
                 ("I plan how to lift the parcel.", "preparation", "none", {}),
                 ("I lifted the parcel yesterday.", "statement", "none", {}),
                 ('The courier said "I lift the parcel".', "statement", "none", {})]
        for text, mode, commitment, fields in cases:
            raw = wire("lift the parcel", target="parcel", method=None, mode=mode,
                       commitment=commitment, source=text, **fields)
            def handler(request):
                body = json.loads(request.content)
                self.assertEqual(body["messages"][-1]["content"], text)
                self.assertEqual(body["temperature"], 0)
                self.assertEqual(body["max_tokens"], 2048)
                self.assertEqual(body["chat_template_kwargs"], {"enable_thinking": False})
                return httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": raw}}]})
            provider = LocalIntentProvider(model="local", transport=httpx.MockTransport(handler))
            response = provider(InterpretationRequest(text, ()))
            self.assertEqual(response, raw)
            value = normalize(response, player_input=text).to_dict()["intentions"][0]
            self.assertEqual((value["mode"], value["commitment"]), (mode, commitment))

    def test_unsupported_action_and_negative_restriction_remain_untrusted_fields(self):
        from tools.evaluate_local_intent import diagnostic_case
        text = "I activate my imaginary tool without opening the box."
        raw = wire("activate imaginary tool", target="imaginary tool", method=None,
                   constraints=["without opening the box"], source=text)
        provider = LocalIntentProvider(model="local", transport=httpx.MockTransport(lambda request:
            httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": raw}}]})))
        result = diagnostic_case(provider, ("unsupported-fixture", text, "spell"))
        item = result["interpretation"]["intentions"][0]
        self.assertEqual(item["constraints"], ["without opening the box"])
        self.assertEqual(item["source"], text)
        self.assertEqual(result["binding"]["category"], "unsupported_activity")
        self.assertTrue(result["state_unchanged"])
        self.assertFalse(result["executed"])

    def test_bad_source_is_not_repaired_by_adapter(self):
        from tools.evaluate_local_intent import diagnostic_case
        raw = wire(source="not from this player input")
        provider = LocalIntentProvider(model="local", transport=httpx.MockTransport(lambda request:
            httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": raw}}]})))
        result = diagnostic_case(provider, ("source-fixture", "I act.", "access"))
        self.assertEqual(result["structural"]["category"], "source_not_verbatim")
        self.assertTrue(result["state_unchanged"])


class OperationalTests(unittest.TestCase):
    setUp = Offline.setUp

    def failure(self, handler):
        calls = []
        def wrapped(request):
            calls.append(request)
            return handler(request)
        provider = LocalIntentProvider(model="local", transport=httpx.MockTransport(wrapped))
        with self.assertRaises(LocalInterpretationUnavailable) as caught:
            provider(InterpretationRequest("private fixture input", ()))
        self.assertEqual(str(caught.exception), "Interpretation unavailable")
        self.assertEqual(len(calls), 1)
        self.assertEqual(provider.last_diagnostic, caught.exception.diagnostic)
        self.assertNotIn("private", json.dumps(provider.last_diagnostic))
        return provider.last_diagnostic

    def test_connection_and_timeout_are_separate(self):
        def connection(request):
            raise httpx.ConnectError("private connection detail")
        def timeout(request):
            raise httpx.ReadTimeout("private timeout detail")
        self.assertEqual(self.failure(connection)["category"], "connection_transport")
        self.assertEqual(self.failure(timeout)["category"], "timeout")

    def test_http_and_response_format_rejections_are_separate(self):
        schema = self.failure(lambda request: httpx.Response(400, json={"error": "private invalid json schema"}))
        self.assertEqual(schema["category"], "response_format_rejected")
        self.assertEqual(schema["http_status"], 400)
        generic = self.failure(lambda request: httpx.Response(503, json={"error": "private unavailable model"}))
        self.assertEqual(generic["category"], "http_provider_error")
        self.assertEqual(generic["http_status"], 503)

    def test_completion_failure_categories_and_no_body_disclosure(self):
        cases = [({}, "missing_completion"),
            ({"choices": [{"finish_reason": "length"}]}, "incomplete_completion"),
            ({"choices": [{"finish_reason": "stop", "message": {}}]}, "missing_completion"),
            ({"choices": [{"finish_reason": "stop", "message": {"content": wire(), "reasoning_content": "private reasoning"}}]}, "noninterpretation_completion"),
            ({"choices": [{"finish_reason": "stop", "message": {"content": "x" * 32769}}]}, "interpretation_too_large")]
        for value, expected in cases:
            with self.subTest(category=expected):
                result = self.failure(lambda request: httpx.Response(200, json=value))
                self.assertEqual(result["category"], expected)
                self.assertTrue(result["response_received"])
        result = self.failure(lambda request: httpx.Response(200, text="private malformed envelope"))
        self.assertEqual(result["category"], "invalid_response_json")

    def test_message_structure_hint_is_allowlisted_without_error_body(self):
        for text in ("private detail: roles must alternate user and assistant",
                     "private template detail: system message must be at the beginning and first"):
            result = self.failure(lambda request: httpx.Response(400, json={"error": text}))
            self.assertEqual(result["category"], "http_provider_error")
            self.assertEqual(result["provider_hint"], "message_structure_rejected")

    def test_v1_rejection_is_distinct_from_provider_completion_failure(self):
        from tools.evaluate_local_intent import diagnostic_case, CASES, private_evidence
        provider = LocalIntentProvider(model="local", transport=httpx.MockTransport(lambda request:
            httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": "not JSON"}}]})))
        result = private_evidence(diagnostic_case(provider, CASES[0]))
        self.assertEqual(result["operational"]["category"], "completion_accepted")
        self.assertFalse(result["operational"]["v1_valid"])
        self.assertEqual(result["structural"]["category"], "json_syntax")
        self.assertTrue(result["state_unchanged"])

    def test_provider_category_reaches_evaluator_without_sensitive_text(self):
        from tools.evaluate_local_intent import diagnostic_case, CASES, private_evidence
        provider = LocalIntentProvider(model="local", transport=httpx.MockTransport(lambda request:
            httpx.Response(422, json={"error": "private unsupported response_format"})))
        result = private_evidence(diagnostic_case(provider, CASES[0]))
        self.assertEqual(result["operational"]["category"], "response_format_rejected")
        self.assertNotIn("private", json.dumps(result))
        self.assertFalse(result["executed"])

    def test_metadata_only_evidence_omits_input_source_and_descriptions(self):
        from tools.evaluate_local_intent import diagnostic_case, CASES, private_evidence
        raw = wire("private activity", target="private target", method="private method", goal="private goal")
        result = private_evidence(diagnostic_case(lambda request: raw, CASES[0]))
        self.assertNotIn("input", result)
        self.assertNotIn("interpretation", result)
        self.assertNotIn("private", json.dumps(result))
        self.assertEqual(result["interpretation_summary"]["items"][0]["mode"], "action")
        self.assertTrue(result["state_unchanged"])


class DiagnosticTests(unittest.TestCase):
    # Reuse outbound-network guards; no local inference in automated verification.
    setUp = Offline.setUp
    def diagnostic(self, raw, case_index=0):
        from tools.evaluate_local_intent import diagnostic_case, CASES
        from engine.gameplay_coordination import Coordinator
        with patch.object(Coordinator, "execute", side_effect=AssertionError("no execution")), \
             patch.object(Coordinator, "_progress", side_effect=AssertionError("no progression")):
            result = diagnostic_case(lambda request: raw, CASES[case_index])
        self.assertTrue(result["state_unchanged"])
        self.assertFalse(result["executed"])
        return result

    def test_equivalent_activity_is_semantically_checked_independent_of_binding(self):
        result = self.diagnostic(wire("ask Mara for her account", method=None))
        self.assertEqual(result["semantic"]["status"], "matches_frozen_checks")
        self.assertEqual(result["binding"]["category"], "compatible")
        self.assertEqual(result["interpretation"]["intentions"][0]["activity"], "ask Mara for her account")
        result = self.diagnostic(wire("study ledger notation", target="dispatch-ledger", method=None), 3)
        self.assertEqual(result["binding"]["category"], "compatible")
        self.assertEqual(result["semantic"]["checks"]["target_meaning"], "review")

    def test_natural_method_is_not_confused_with_model_misunderstanding(self):
        result = self.diagnostic(wire("search ledger for physical signs", method="Perception", target="ledger"), 2)
        self.assertEqual(result["semantic"]["status"], "matches_frozen_checks")
        self.assertEqual(result["binding"]["category"], "compatible")

    def test_targets_and_methods_have_separate_rejection_categories(self):
        for fields, expected in ((dict(targets=[]), "compatible"),
                (dict(targets=["captain"]), "unsupported_target"),
                (dict(method="cast spell"), "unsupported_method"),
                (dict(method="physical examination"), "method_not_supported_for_activity")):
            result = self.diagnostic(wire(**fields), 1)
            self.assertEqual(result["binding"]["category"], expected)

    def test_compatible_probe_grants_no_authority_and_never_draws(self):
        result = self.diagnostic(wire(), 1)
        self.assertEqual(result["binding"]["category"], "compatible")
        self.assertEqual(result["semantic"]["status"], "matches_frozen_checks")
        result = self.diagnostic(wire(mode="statement", commitment="none"), 1)
        self.assertEqual(result["binding"]["runtime_route"], "statement_no_authorization")
        self.assertEqual(result["semantic"]["status"], "incorrect")

    def test_restriction_polarity_and_unfamiliar_wording(self):
        for constraints, expected in ((["without making a promise"], "pass"),
                (["make a promise"], "fail"), ([], "fail"),
                (["promise not to copy names"], "review")):
            result = self.diagnostic(wire(constraints=constraints), 5)
            self.assertEqual(result["semantic"]["checks"]["restriction_polarity"], expected)

    def test_condition_polarity_and_relationship_direction(self):
        from tools.evaluate_local_intent import semantic_checks
        value = json.loads(wire(commitment="conditional", conditions=["Mara offers permission without a promise"]))
        expected = ("Mara offers permission without a promise",)
        self.assertEqual(semantic_checks(value, "access", conditions=expected)["checks"]["conditions_and_polarity"], "pass")
        value["intentions"][0]["conditions"] = ["Mara requires a promise"]
        self.assertNotEqual(semantic_checks(value, "access", conditions=expected)["checks"]["conditions_and_polarity"], "pass")
        value = json.loads(wire("ask for account", method=None))
        value["intentions"].append(dict(value["intentions"][0], id="i2"))
        value["relationships"] = [{"type": "precedes", "from": "i1", "to": "i2"}]
        self.assertEqual(semantic_checks(value, "report", count=2, relationships=(("precedes", 0, 1),))["checks"]["relationships_and_direction"], "pass")
        self.assertEqual(semantic_checks(value, "report", count=2, relationships=(("precedes", 1, 0),))["checks"]["relationships_and_direction"], "fail")

    def test_structural_categories_do_not_change_v1_validation(self):
        for raw, expected in (("invalid", "json_syntax"), (wire(mode="invalid"), "mode_or_commitment_enum"),
                (wire(mode="statement"), "commitment_condition_consistency"),
                (wire(context_refs=["missing"]), "unknown_context_reference"),
                (wire(source="not a source excerpt"), "source_not_verbatim"),
                (wire().replace('"version": 1', '"version": 1, "version": 1'), "duplicate_json_key")):
            result = self.diagnostic(raw)
            self.assertFalse(result["structural"]["valid"])
            self.assertEqual(result["structural"]["category"], expected)
            self.assertIsNone(result["binding"])

    def test_capture_excludes_unknown_fields_and_redacts_entire_sensitive_string(self):
        from tools.evaluate_local_intent import sanitized
        value = json.loads(wire(goal="password fixture marker", source="x" * 2048))
        value["intentions"][0]["reasoning"] = "do not capture"
        value["provider_diagnostics"] = "do not capture"
        captured = sanitized(value)
        self.assertEqual(captured["intentions"][0]["goal"], "[REDACTED]")
        self.assertEqual(len(captured["intentions"][0]["source"]), 1024)
        self.assertNotIn("do not capture", json.dumps(captured))

    def test_accidental_execution_is_blocked(self):
        from tools.evaluate_local_intent import diagnostic_case, CASES
        from engine.watchhouse_intent import WatchhouseIntentDomain
        def bad_binder(domain, handoff):
            domain.runtime.process_increment(None)
        with patch.object(WatchhouseIntentDomain, "bind_intent", bad_binder):
            result = diagnostic_case(lambda request: wire(), CASES[1])
        self.assertEqual(result["binding"]["category"], "binder_exception")
        self.assertTrue(result["state_unchanged"])

    def test_exactly_six_offline_calls_can_never_progress_gameplay(self):
        from tools.evaluate_local_intent import diagnostic_case, CASES
        calls = []
        def provider(request):
            calls.append(request)
            return wire()
        rows = [diagnostic_case(provider, case) for case in CASES]
        self.assertEqual(len(calls), 6)
        self.assertTrue(all(r["state_unchanged"] and not r["executed"] for r in rows))


if __name__ == "__main__":
    unittest.main()
