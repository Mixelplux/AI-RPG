"""One offline test-local supplier; not a production lockpicking implementation."""
from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from engine.activity_control import (
    ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment,
    decide_activity_control,
)


class ArchiveLockFixture:
    """Own fixture truth/execution; F05 only grants or withholds continuation.

    The existing footsteps case establishes successful resolution and two minutes
    of partial work. One final minute is a local test quantity, not an F05 rule.
    The no_damage conflict is the same stipulated limit used in existing F05
    lockpicking tests; this fixture does not adjudicate physical damage.
    """

    def __init__(self, case):
        self.purpose = case["authorization"]["purpose"]
        self.method = case["authorization"]["method"]
        self.accepted_ref = case["checkpoint"]["resolution_ref"]
        self.footsteps = ActivityDevelopment(**case["checkpoint"]["developments"][0])
        self.state = dict(progress="not_started", minutes=0, resolutions=0,
                          outcome=None, resolution_ref=None, lock_open=False,
                          lockpicks_available=True, footsteps_heard=False)
        self.trace = []  # Diagnostic observations are not authoritative progress.

    def _decide(self, authorization):
        # Derive every checkpoint from activity truth, never from the request's
        # asserted target/method, and never accept a caller-built checkpoint.
        point = ActivityCheckpoint(
            self.purpose, self.method,
            missing_means=() if self.state["lockpicks_available"] else ("lockpicks",),
            conflicting_constraints=("no_damage",),
            resolution_ref=self.state["resolution_ref"],
            complete=self.state["progress"] == "finished",
            developments=(self.footsteps,) if self.state["footsteps_heard"] else (),
        )
        decision = decide_activity_control(authorization, point)
        self.trace.append(dict(state=deepcopy(self.state),
                               authorization=asdict(authorization),
                               checkpoint=asdict(point), decision=asdict(decision)))
        return decision

    def request(self, authorization):
        decision = self._decide(authorization)
        if decision.status != "continue":
            return decision
        if self.state["progress"] == "not_started":
            # Predetermined authority, not a roll or a conclusion from narration.
            self.state["minutes"] += 2
            self.state["resolutions"] += 1
            self.state.update(progress="partial", outcome="success", resolution_ref=self.accepted_ref,
                              footsteps_heard=True)
            return self._decide(authorization)  # New perceptible risk, same result.
        self.state["minutes"] += 1
        self.state.update(progress="finished", lock_open=self.state["outcome"] == "success")
        return self._decide(authorization)


class IndependentActivityTests(unittest.TestCase):
    def test_independent_supplier_retains_authority_across_interruption_and_resumption(self):
        cases = json.loads(Path("test_fixtures/f05_activity_control.json").read_text(encoding="utf-8"))["cases"]
        source = next(c for c in cases if c["id"] == "footsteps_during_lockpicking")
        source_before = deepcopy(source)
        self.activity = activity = ArchiveLockFixture(source)
        initial = ActivityAuthorization(**source["authorization"])
        renewed = replace(initial, answered_choices=(activity.footsteps.choice_key,))

        def unchanged(request, reason):
            before = deepcopy(activity.state)
            decision = activity.request(request)
            self.assertEqual((decision.status, decision.reason), ("control", reason))
            self.assertEqual(activity.state, before)
            return decision

        for socket_guard in (
            patch.object(socket.socket, "connect", side_effect=AssertionError("offline")),
            patch("socket.getaddrinfo", side_effect=AssertionError("offline")),
        ):
            socket_guard.start()
            self.addCleanup(socket_guard.stop)

        # Missing/invalid authorization cannot create the fixture's accepted result.
        before = deepcopy(activity.state)
        with self.assertRaises(ValueError):
            activity.request(None)
        self.assertEqual(activity.state, before)
        for intent in ("inquiry", "prepare", "withdraw"):
            unchanged(replace(initial, intent=intent), intent)
        unchanged(replace(initial, purpose="open another lock"), "authorization_scope")
        unchanged(replace(initial, constraints=("no_damage",)), "authorization_constraint")
        activity.state["lockpicks_available"] = False  # Stipulated external fact.
        unchanged(initial, "cannot_proceed")
        activity.state["lockpicks_available"] = True

        start = len(activity.trace)
        interrupted = activity.request(initial)
        self.assertEqual((interrupted.status, interrupted.reason, interrupted.resolution),
                         ("control", "discovery_risk", "reuse"))
        self.assertEqual([r["decision"]["status"] for r in activity.trace[start:]],
                         ["continue", "control"])
        self.assertIsNone(activity.trace[start]["checkpoint"]["resolution_ref"])
        self.assertEqual(activity.state, dict(
            progress="partial", minutes=2, resolutions=1, outcome="success",
            resolution_ref=activity.accepted_ref, lock_open=False,
            lockpicks_available=True, footsteps_heard=True))

        # The same supplier now derives a resumed checkpoint from retained truth.
        unchanged(initial, "discovery_risk")  # Renewed commitment alone is insufficient.
        unchanged(replace(initial, answered_choices=("another_risk",)), "discovery_risk")
        unchanged(replace(renewed, intent="inquiry"), "inquiry")
        unchanged(replace(renewed, method="force the door"), "authorization_scope")
        restricted = unchanged(replace(renewed, constraints=("no_damage",)),
                               "authorization_constraint")
        self.assertEqual(restricted.resolution_ref, activity.accepted_ref)
        activity.state["lockpicks_available"] = False
        unavailable = unchanged(renewed, "cannot_proceed")
        self.assertEqual(unavailable.resolution_ref, activity.accepted_ref)
        activity.state["lockpicks_available"] = True

        start = len(activity.trace)
        completed = activity.request(renewed)
        self.assertEqual((completed.status, completed.reason, completed.resolution),
                         ("complete", "concluded", "reuse"))
        self.assertEqual([r["decision"]["status"] for r in activity.trace[start:]],
                         ["continue", "complete"])
        self.assertEqual((activity.state["minutes"], activity.state["resolutions"]), (3, 1))
        self.assertEqual(activity.state["resolution_ref"], interrupted.resolution_ref)
        self.assertEqual(activity.state["outcome"], "success")
        self.assertTrue(activity.state["lock_open"])
        finished = deepcopy(activity.state)
        for request in (renewed, initial, replace(renewed, constraints=("no_damage",))):
            self.assertEqual(activity.request(request).status, "complete")
            self.assertEqual(activity.state, finished)
        self.assertEqual(source, source_before)


if __name__ == "__main__":
    unittest.main()
