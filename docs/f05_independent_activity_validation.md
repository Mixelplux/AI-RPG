# F05 independent activity integration validation

October 17, 2026. One bounded offline validation following the preceding
read-only cross-scenario chat assessment's recommendation B. That assessment
identified independent resumed-supplier coverage as a test gap, not a new policy
defect. Owner reports damaged-gate structural smoke passed after SR-01.

Candidate: `D:/AI RPG/.artifacts/f01-f05-bounded-playable-integration-v1`, branch
`codex/f01-f05-bounded-playable-integration-v1`. Protected baseline, HEAD, main
and origin/main remain `d2ededee58294002f522cef5ab61577270311997`.
This is an uncommitted validation handoff, not owner acceptance or publication.

## Activity, ownership and design sufficiency

`test_f05_independent_activity.py` adds one test-local `ArchiveLockFixture` and
one sequence test. It reuses `footsteps_during_lockpicking` from the unchanged
`test_fixtures/f05_activity_control.json`: archive-lock purpose, established
lockpicks, `lock-attempt-1`, approaching footsteps/discovery risk, and the
`footsteps_at_door` choice. The source fixture establishes successful mechanical
resolution with fictional execution unfinished and two elapsed minutes.

The test explicitly stipulates one additional minute to finish; that quantity is
not a new F05 rule or a claim about real lockpicking. Effort/time is the only
expenditure modeled. Lockpicks are an available prerequisite, not a consumable.
The `no_damage` conflict reuses the existing lockpicking policy-test stipulation;
neither its desirability nor physical damage is adjudicated.

Accepted F05 D1–D6, existing fixture authority and the owner's explicit validation
scope supply sufficient intent. No design gap or production subsystem is needed.
The supplier uses structured authorization, not a language parser. It imports
only the reusable F05 types/function; it does not reuse the gate adapter or
material-handling execution to construct its sequence.

| Information | Test-local supplier responsibility |
|---|---|
| Purpose and chosen activity method | Bind the activity's fixture identity independently of the request, allowing F05 to detect mismatched authorization. |
| Intent, restrictions and answered risk | Receive the current structured player authorization unchanged; inquiry/preparation/withdrawal do not execute. |
| Prerequisite and restriction conflict | Derive missing lockpicks from current availability and supply the existing declared `no_damage` conflict on every checkpoint. |
| Progress, time and accepted outcome | Own retained state; establish predetermined success once, increment the resolution count once and retain its reference. |
| Meaningful development | Supply the existing footsteps development only once the fixture's supported work segment establishes it as heard; preserve its risk/response flags and choice key. |
| Completion and repeat protection | Derive completion from retained progress; execute work only on `continue`, and leave state unchanged on `control` or `complete`. |

The same `_decide()` construction is used before initial work, at interruption,
on resumed requests and after completion. Callers cannot pass a preassembled
checkpoint. Each trace record contains the supplier state, current authorization,
constructed checkpoint and actual policy decision. This tests the supplier
boundary rather than only replaying complete checkpoint objects.

## Observed sequence

| Phase | Decision and consequential state |
|---|---|
| Before execution | No progress, zero minutes, zero resolutions, no outcome reference, closed lock. Missing authorization raises existing policy validation error without state change. Noncommitment, wrong purpose, restriction conflict and missing tools also leave state unchanged. |
| Initial valid commitment | Supplier builds an unresolved checkpoint without footsteps; F05 allows continuation. Supplier establishes two minutes of partial work, one successful accepted result and its reference, then introduces the fixture's footsteps. |
| Interruption | Fresh checkpoint derives partial state and heard footsteps. F05 returns `control/discovery_risk/reuse`; lock remains closed and prior work/result remain. |
| Incomplete resumption | No answer or an answer to another risk still returns `discovery_risk`. Inquiry and wrong-method authorization also perform no work. |
| Answered risk plus another limit | Current authorization answering `footsteps_at_door` still returns `authorization_constraint` for `no_damage`, or `cannot_proceed` when lockpicks are absent. Each request preserves all consequential state present immediately before it. Availability changes are explicitly stipulated external fixture changes, not effects of rejection. |
| Valid resumption | After restoring availability, authorization answering this risk without the conflicting restriction returns `continue/reuse`. Supplier executes the final minute using the stored outcome. |
| Completion | Newly derived completed checkpoint returns `complete/concluded/reuse`: three total minutes, one resolution, same `lock-attempt-1`, successful open lock. |
| Repetition | Renewed, original and restricted repeat requests return completion without any change to time, resolution count, outcome, resources or progress. Completion identifies already finished work; it does not authorize another action. |

No model, roll, hidden observer decision or consequential narration participates.
Diagnostic trace growth is not activity progress. The existing source fixture is
also asserted unchanged by the sequence.

## Results and finding classification

- New file syntax passes before execution.
- Focused independent sequence passes.
- **50 relevant tests pass:** one independent supplier test, 11 accepted F05,
  23 gate, seven consequential F01 and eight API-readiness tests. Runners deny
  network/DNS; no provider request is made.
- Shared workflow verification and lifecycle validation (7/7), documentation
  links, whitespace, empty index and preservation checks pass.
- Production F05 policy, gate behavior, F01 instructions and all pre-existing
  test/fixture source remain byte-identical to task start.

| Classification | Finding |
|---|---|
| Reusable policy defect | None exposed. Existing logic handles both independently supplied phases consistently. |
| Supplier/integration defect | None exposed in this new bounded supplier. Rejected requests preserve truth; accepted continuation reuses the original result. |
| Evidence gap | The previously identified lack of an independent stateful initial/interruption/resumption/completion supplier sequence is addressed. This does not establish correctness for every future supplier. |
| Deliberate fixture limitation | Structured authorization, predetermined success, explicit tool availability, stipulated discovery event and duration; no production perception, inventory, NPC, parser, persistence or lockpicking system. |

Evidence: `.artifacts/f05-independent-activity-20261017/` contains
`supplier-trace.json`, focused/relevant test logs, preservation manifests and
`verification/workflow.log`. Original eight live outputs, four comparisons,
correction evidence and final review remain unchanged. API requests/generations:
**0/0**; neither exhausted live budget was extended.

## Confidence and recommendation

The sequence demonstrates transfer of unchanged F05 policy through a second
stateful supplier with a different interruption basis from the gate. It closes
the specific recommended test gap without implementing general systems. Together
with the gate regressions, SR-01 correction and owner-reported gate smoke, current
evidence supports **bounded F01/F05 structural acceptance review**. No additional
structural blocker is known from these checks; publication preparation may follow
only after the owner's acceptance and separate Git authority.

Supplier completeness remains a caller obligation. The policy validates shape
and supplied relationships, not truth or semantic completeness; a future supplier
can still omit a prerequisite, restriction or development. Predetermined success
does not test probabilistic outcomes, production scene discovery, open-ended
language, save/load, real-time actor behavior or arbitrary activity chains. Gate
tests separately cover controlled failure; this one new activity does not claim
statistical or universal correctness. F01 fidelity evidence/classifications and
deferred literary findings are unchanged; this task evaluated no narration.

## Documentation and preservation

Updated current package/sprint records, integration handoff, Action & Resolution
manifest and relationship map to record test evidence and its limits. No new
production relationship is claimed. Architecture, other manifests, deferred
findings, accepted contracts/design, doctrine, ADRs and AGENTS/PROJECT/WORKFLOW
need no change: runtime behavior, authority, persistence and scope boundaries
are unchanged. The gate owner-smoke result is owner-reported evidence, not a new
automated acceptance decision.

Original checkout HEAD/status, historical evidence, saves, credentials, candidate
runtime and protected main/origin-main are preserved. Saves and credentials were
not accessed. Changes remain isolated, uncommitted and unstaged with an empty
index. No commit, merge, push, publication, acceptance or next package was started.
