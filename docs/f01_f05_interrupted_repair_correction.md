# Interrupted repair interaction correction — owner review candidate

October 17, 2026. Offline structural correction within the existing damaged-gate
candidate; no implementation acceptance or publication is claimed.
Baseline/HEAD: `d2ededee58294002f522cef5ab61577270311997`.

## Diagnosis and accepted boundary

Replaying the owner's exact seven inputs reproduced the failure. Examination
took two minutes; repair secured the hinge, spent one pin and reached elapsed
minute 12. All five subsequent instructions were rejected without changing
physical state. The interpreter recognized repair verbs and resume verbs, but
not the offered bracing action or “finish.” Its supplied-means check also read
“continue with repair” as an unfamiliar resource. Rejection falsely stated that
no attempt had begun. The failure preceded F05 authorization and resolution.

Accepted F05 D2 interpretation, D3 consequential choice, D5 current means and D6
resumption already supply sufficient design intent. The existing resume branch
requires explicit support selection, checks current timber, reuses the accepted
repair result and preserves initial work/costs. It is adapted at the input seam;
neither it nor accepted F05 control policy needs replacement. No design gap,
new mechanic, general parser or narrator involvement is needed.

## Correction

`engine/damaged_gate.py` gives its bounded interpreter the fact that a repair has
already started. Whole-instruction matches recognize “brace the gate,” “use timber
to brace,” “finish with timber brace,” and nearby explicit forms naming this gate,
hinge or repair. Existing safety exclusions run first. Questions, tentative
proposals, preparation, extra acts, unfamiliar resources and unrelated targets do
not enter this authorization path. Existing initial repair interpretation stays
unchanged; bracing aliases alone cannot initiate a repair.

These instructions select the existing repair continuation. They do not execute
new resolution, replace means, grant authority to narration or replay the pin cost.
“Continue with repair” is recognized as resumption but still asks whether to commit
the timber. Bare “brace” remains unclear and asks for a choice without advancing.
Explicit timber refusal likewise preserves the pause. Repeated instructions after
completion apply no new result or expenditure.

Unrecognized input during a paused repair explicitly preserves the secured hinge,
elapsed work and committed pin. Preparation/help accounts also avoid claiming no
previous attempt occurred. These are authoritative interaction accounts, not F01
prompt or literary changes.

## Verification and evidence

- Syntax parsing passes for both changed Python files.
- 48 offline unit tests pass: damaged-gate integration (22), accepted F05,
  consequential F01 regressions and API-readiness tests. Three added parameterized
  tests cover contextual authorization, ambiguity/inquiry/rejection preservation,
  reuse of failure, unavailable means, renewed constraints and repeat protection.
- Accepted F01's five test groups and three adjacent narration scripts pass with
  socket connection and DNS disabled; transport is mocked where required.
- Replay from each of the original eight preserved pre-action states produces
  identical sampled contexts, resulting states and serialized inputs. This is
  deterministic regression evidence, not new live narration evaluation.
- The actual offline CLI completes the resumed repair and handles ambiguous input
  and repeated authorization. The exact owner sequence now completes on “brace
  the gate,” at 37 minutes total including examination, with one pin spent and
  timber committed once. Later inputs do not duplicate work or cost.
- Shared Git workflow verification, lifecycle validation and whitespace checks
  pass. The lifecycle remains the same active package; no new package is selected.

Evidence is under `.artifacts/interrupted-repair-correction-20261017/`:
`owner-sequence-before.json`, `owner-sequence-after.json`, `owner-cli-smoke.txt`,
`eight-case-offline-replay.json`, `adjacent-checks.txt`, preservation manifests and
`verification/workflow.log`. Original eight outputs, four comparison outputs and
prior correction evidence remain intact. New API requests/generations: **0**.

## Renewed owner smoke

Run this exact command sequence in PowerShell:

```powershell
Set-Location -LiteralPath 'D:\AI RPG\.artifacts\f01-f05-bounded-playable-integration-v1'
.\.venv\Scripts\python.exe -B tools/play_damaged_gate.py
```

Ask about the repair first, examine the hinge, then authorize repair in your own
words. At the support decision, try an unclear continuation and check that it
waits without erasing prior work. Then choose the timber brace, for example “use
timber to brace” or “finish with timber brace.” Check that completion preserves
the spent pin and that repeating the instruction does not repeat work. Type
`quit` to end. Record the input, actual response and expected consequence for any
unexpected behavior; classify consequential misunderstanding separately from
expression or pacing.

The session is unsaved, offline by default and limited to the existing gate
approaches with stipulated competence, means and outcomes. It does not understand
arbitrary instructions. Do not use `--live`: both historical live budgets are
exhausted. No launch or authorization blocker remains for this offline smoke.
Owner experience and acceptance remain to be assessed.

## Reconciliation and preservation

Updated the integration handoff, current package/sprint records, architecture and
Action & Resolution manifest to reflect this bounded interpretation correction.
F01/F05 contracts, ADRs, doctrine, AGENTS/PROJECT/WORKFLOW, relationship map,
Narrative Experience manifest and deferred findings need no new changes: authority,
system relationships, narrative instructions and deferred presentation observations
are unchanged. Save semantics and the persistence manifest need no changes because
the session has no save integration. No dependencies or provider settings changed.

Changes remain isolated, uncommitted and unstaged on
`codex/f01-f05-bounded-playable-integration-v1`, with an empty index. Original
checkout status, historical evidence and protected references are preserved.
Saves and credentials were not accessed or changed. No merge, publication or next
implementation package is authorized. Recommended next action is renewed bounded
owner smoke, then owner review of this uncommitted correction.
