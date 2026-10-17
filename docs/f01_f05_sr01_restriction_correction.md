# SR-01 restriction consistency correction

October 17, 2026. Bounded offline implementation handoff; uncommitted and not
accepted or published. Candidate branch:
`codex/f01-f05-bounded-playable-integration-v1`.
Protected baseline/HEAD/main/origin-main:
`d2ededee58294002f522cef5ab61577270311997`.

## Root cause and exact correction

The [final structural review](f01_f05_final_structural_reconciliation.md) located
SR-01 in the gate-local continuation checkpoint supplier. Interpretation retained
`no_damage`, but resumed repair supplied only missing means and the accepted
resolution reference to the existing F05 policy. Initial execution also supplied
`conflicting_constraints=("no_damage",)`, so equivalent recognized restrictions
had different effects.

`engine/damaged_gate.py` now names that same existing tuple
`RESTRICTION_CONFLICTS` and uses it at both initial and resumed execution checks.
The resumed check precedes timber commitment, the five-minute support fitting and
the remaining twenty-minute repair. The accepted `engine/activity_control.py`
policy returns `control/authorization_constraint` as before. Blocked continuation
now identifies the restriction instead of falsely reporting unavailable timber;
it states that secured work, accepted result and prior costs remain.

No restriction meaning changed. In particular, this task does not assess or revise
the strict treatment of “without further damage.” Initial behavior is unchanged;
resumption is made consistent with it. Missing-timber handling, restriction
interpretation, outcome fixtures and accepted F05 decisions are reused. The
blocked instruction does not persist a new restriction into the original repair
authorization: a later unrestricted explicit timber choice proceeds normally,
as the existing state model intends.

Accepted F05 D3/D5/D6 and the owner's explicit consistency clarification provide
sufficient design intent. No unresolved design question or new policy was needed.
F01 receives the resulting authoritative account; its instructions, provider
settings, validation and lack of gameplay authority are unchanged.

## Regression evidence

One new parameterized offline regression compares initial and resumed repair for
`without further damage`, `without damage` and `don't damage`, with both accepted
success and failure outcomes. It covers the ordinary continuation phrase and the
contextual “finish with timber brace” phrase. Before the runtime correction all
six condition/outcome combinations reproduced the defect; the preserved test log
shows completion where control was expected. After correction they pass.

Assertions verify:

- Both paths return `control/authorization_constraint` for the existing conflict;
  initial repair has no expenditure, while resumed repair keeps its prior work.
- Blocked resumed inputs preserve all physical/resource/attempt fields, including
  ten elapsed minutes, one remaining pin, secured hinge and uncommitted timber.
  Existing authoritative history remains intact; recording the new exchange is
  expected and is not additional repair progress.
- Context retains the recognized restriction, and the account names the actual
  block without inventing a shortage.
- Subsequent `use timber to brace` reuses the original accepted outcome, completes
  at minute 35 with one pin spent and timber committed once, and preserves failure
  when failure was the fixture outcome.
- Repeated completed repair/brace/conditional continuation changes no physical
  state, outcome, elapsed work or resources.

Verification results:

| Check | Result |
|---|---|
| Changed Python syntax | Pass before execution |
| Focused regression | Pass: one parameterized test, six condition/outcome combinations |
| Full relevant unit set | **49 pass**: 23 gate, 11 accepted F05, seven consequential F01, eight API-readiness |
| Accepted F01 realization component | Five groups pass |
| Adjacent narration scripts | Three pass: output, source, fake Responses transport |
| Original eight sampled pre-action replay | All resulting states, contexts and serialized inputs identical |
| Actual default offline CLI | Restriction blocks, later explicit continuation completes, repeat has no expenditure |
| Shared workflow/lifecycle | Pass; lifecycle validator 7/7 |
| Links, whitespace, preservation and empty index | Pass |
| New API requests/generations | **0 / 0** |

Relevant unit/component runners deny network connections and DNS; fake provider
transport is used where needed. The launcher uses its existing default offline
path. No credential loading or live probe was needed. Both prior live budgets
remain exhausted. Historical outputs and original review judgments are unchanged.

Evidence: `.artifacts/sr01-restriction-correction-20261017/` contains
`regression-before.txt`, `focused-tests.txt`, `relevant-tests.txt`,
`adjacent-tests.txt`, `corrected-sequence.json`, `eight-case-offline-replay.json`,
`owner-cli-smoke.txt`, preservation manifests and `verification/workflow.log`.

## Owner smoke and readiness

Verified shortest default offline launch from PowerShell:

```powershell
Set-Location -LiteralPath 'D:\AI RPG\.artifacts\f01-f05-bounded-playable-integration-v1'
.\.venv\Scripts\python.exe -B tools/play_damaged_gate.py
```

Authorize repair, then give the restricted continuation:
`continue repair with timber without further damage`. It should return control,
report the restriction and retain the secured hinge and spent pin without more
work. Then choose the brace without that restriction, for example `use timber to
brace`. It should finish using the original repair result. Repeat that instruction
to check it adds no cost, then `quit`. No `--live` flag is authorized.

SR-01 is corrected under the existing logic. No other outstanding structural
defect is known from the bounded review and current affected regressions. The
candidate is **ready for owner structural acceptance review and renewed offline
smoke**; acceptance remains the owner's decision. Finite vocabulary, stipulated
competence/means/outcomes, unsaved sessions and lack of general upstream systems
remain explicit scope limits. These checks provide bounded evidence, not proof
over every instruction or a guarantee of future generated fidelity. Literary
refinement and the previously owner-classified minor pin omission do not block
this structural recommendation.

## Reconciliation and preservation

Updated the integration handoff, current package/sprint records, architecture,
Action & Resolution/Narrative Experience manifests, relationship map and DF-009
to distinguish the historical blocker from its correction. The final structural
report and earlier correction reports remain intact as historical records.
Accepted F01/F05 design, AGENTS/PROJECT/WORKFLOW, doctrine, ADRs, general system
classifications, persistence/save version and dependencies need no changes: this
repairs a gate checkpoint omission, not authority ownership or architecture.

Only gate runtime, its focused test and directly affected documentation changed.
All other prior candidate source, original checkout HEAD/status, saves,
credentials, historical evidence and protected references are preserved. Saves
and credentials were not accessed. Changes remain isolated and uncommitted with
an empty index; no staging, commit, merge, push, publication, acceptance or next
package transition occurred. The next step is owner review/smoke; any later Git
publication requires separate authorization under WORKFLOW.
