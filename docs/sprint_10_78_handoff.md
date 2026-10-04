# Character Competence V1 - Sprint 10.78 implementation handoff

## Repository state
Uncommitted working diff on `codex/character-competence-v1` against exact HEAD and
protected `main`: `d9c0cb9056007b938902dc4f1a439130763179b2`.
Start state was clean and lifecycle idle. Owner authorized package selection,
feature branch and lifecycle staging, implementation and verification; explicitly
withheld staging/commit/push/merge. Index remains empty. Sprint 10.78 remains active
pending owner review; latest completed is 10.77, next_sprint is null.

Changed files within approved surfaces:
- `engine/character_competence.py` (new bounded authority).
- `engine/game_engine.py` (atomic attempts, existing pursuit preparation, safe views).
- `engine/world_state.py`, `engine/save_system.py` (initial values and validation/load).
- `engine/west_road_predicament.py` (authored contract and partial report membership).
- `engine/contextual_action_projection.py` (same-authority approaches/costs/rules).
- `data/regions/bryn_shander.json` (minimum withdrawal detail and two limited findings).
- `test_character_competence.py` (new offline behavioral and persistence checks).
- `docs/architecture.md`, `docs/decisions.md` (bounded ownership/compatibility, ADR-061).
- `docs/current_capability_package.md`, `docs/current_sprint.md`,
  `docs/current_sprint.json`, and this handoff.

## Implementation and competence semantics
Unique authoritative tags: tactical_assessment, outdoor_tracking,
surveillance_analysis. Defaults are empty; profiles can be supplied through an
initial World State, without production classes or a character-creation UI.
No biography, equipment, generic modifiers or leveling affect competence.

Applicable withdrawal evidence requires the existing tracks discovery/physical
trace and observers_withdrew phase. Routine recognition derives deterministically
from those authored facts; queries never persist recognition or draw. Projection
separates local observation/guard report, automatic limited interpretation,
partial inference, accepted route finding, approaches, costs, outcomes and limits.
At the North Gate the existing Grey/Elin coordination boundary applies to new
operations. Guard assistance is recorded only for the guarded survey, never added
to competences. Fresh detail is limited to prints toward the existing low rise and
two trampled positions with overlapping road sightlines.

Follow withdrawal signs uses outdoor_tracking; reconstruct local observation
circuit uses surveillance_analysis. Each costs one hour and draws one engine d6.
Without relevant competence: 1-2 failure, 3-4 partial, 5-6 full. With it: 1-2 partial,
3-6 full. Guarded survey is deterministic with the committed guards coordinated by
Grey and Elin; cost two hours, reduced to one by tactical_assessment.

Failure discovers nothing. Tracking partial finds local direction; surveillance
partial supports overlapping positions/circuit but does not confirm the route.
Other applicable approaches and ordinary continuation remain available. Full
resolution reuses the existing pursue-observers outcome/withdrawal route, reporting
and phase validation, inside the same copied candidate as time and accepted attempt.
No identity, affiliation, distant destination, capture or new traversable place.
Repeated invocation returns its accepted result, even after later continuation,
without a draw, additional time or publication. No anti-save-scumming guarantee.

## Persistence and transaction review
Version 1 remains supported by the established additive copied-load normalization
precedent (ADR-036). Missing competences/attempts become empty in the copied loaded
payload. Present malformed tags/records/draws/results/costs/findings/references reject.
Acceptance validates source/time/result chronology, outcome mirror, time cost,
limited discovery sources, physical trace and full pursuit continuation. The
accepted specialist basis must agree with authoritative competence tags; V1
has no competence gain/loss mechanism.
Prototype saves missing the required predicament still reject; historical completed
pursuit needs no competence attempt. Source files are never rewritten on load.

Simulation retains sole ownership. The shared authority supplies eligibility and
resolution; projections/provider input cannot choose a die result or supply evidence.
Existing preparation helpers apply time consequences. Candidate validation and scene
construction precede one publish. Injected failures preserve world and scene identity.
Player-safe competence packets enter perception, current scene, ordinary narration
and the existing flexible narration-context scene dictionary; no new provider schema
or live request path. Independent agent review was neither requested nor required.

## Verification
Passed with the official `.venv/Scripts/python.exe`:
- Syntax checks for all changed Python sources and the new test script.
- `test_character_competence.py`: all six draws for each uncertain operation across
  all four profiles; recognition/projection read-only/copy-safe; profile distinctions;
  guards, alternate/ordinary continuations, unsupported/absent evidence; accepted
  replays; survey cost; time consequences; injected rollback boundaries; authored
  contract/partial sharing; all profiles around save/load results; no loaded reroll;
  historical completed pursuit and other branch compatibility; missing-field
  normalization, malformed records and failed-load session/source preservation.
- Existing `test_west_road_predicament.py`, `test_west_road_presentation.py`.
- Discovery, contextual action, current scene, save/load, world update tests.
- Narration context/request/prompt/pipeline/output tests.
- Elapsed-time observation, time pressure/actor/evidence consequences tests.
- Navigation, one-hour West-Road traversal, arrival discovery, actor-response tests.
- Maintained GitWorkflowTools verification (profile invariants and mutation detection),
  lifecycle validation, diff whitespace and targeted source/scope review.

The direct `test_narration_source.py` run was environment-blocked by tiktoken's
missing tokenizer cache trying a download through an unavailable proxy. Its provider
transport is mocked; no live provider was contacted. The same source contract passed
with an offline tokenizer stub. Real tokenizer/cache behavior was not verified and
no dependency/environment repair was attempted. This does not block the changed
projection/context contract, covered independently above. Filesystem checks used
deterministic `.artifacts/` paths, with no TemporaryDirectory. No exhaustive suite.

## Risks / owner smoke
Owner smoke passed and Character Competence V1 was accepted October 4, 2026. The
existing direct disk-save write is
unchanged; this package adds no crash-safe replacement or general migration.
Both new uncertain approaches deliberately preserve the existing gate coordination
and report boundary; full results end the same bounded pursuit branch.
No production profile-selection UI was authorized or added.

From repository root, open an offline, test-seeded comparison session:

```powershell
.\.venv\Scripts\python.exe -i -c "from test_character_competence import withdrawn; from unittest.mock import patch; from engine import character_competence as competence"
```

At the Python prompt, paste this helper, ending its definition with a blank line:

```python
def smoke(tag, command, draw=3):
    e = withdrawn(tag)
    before = e.get_world_state()["time"]["elapsed_hours"]
    print("PROFILE:", tag or "non-specialist")
    print(e.get_narration()["description"])
    with patch.object(competence, "draw_d6", return_value=draw):
        print(e.process_command(command)["message"])
    print("Hours spent:", e.get_world_state()["time"]["elapsed_hours"] - before)
    print(e.get_narration()["description"])
    return e

profiles = (None, "tactical_assessment", "outdoor_tracking", "surveillance_analysis")
for tag in profiles: e = smoke(tag, "follow withdrawal signs")
for tag in profiles: e = smoke(tag, "reconstruct local observation circuit")
for tag in profiles: e = smoke(tag, "arrange guarded local survey")
```

Run each loop separately. Every call starts in identical withdrawal circumstances.
At draw 3, tracking is full only for the outdoor specialist; circuit reconstruction
is full only for the surveillance specialist. Other profiles obtain partial results
and retain alternative approaches plus ordinary pursuit/coverage. Survey succeeds
for all four, costing one hour for tactical competence and two for the others.
Compare evidence layers, accepted discoveries, remaining choices and time, as well
as the displayed rules. This injected draw is a test-only comparison; play rolls d6.

Then run `e = smoke(None, "follow withdrawal signs", 1)`: no additional discovery
should appear. `e.process_command("pursue observers")` still succeeds. On a fresh
accepted attempt, repeat its command and verify unchanged time/state; save to an
unused `.artifacts/` path, load, and repeat again. Never infer identity, affiliation,
a distant destination or new adventure from any result. No production profile UI.

## Completion review

Repository reconciled against the protected baseline: 11 modified tracked files
and 3 untracked candidate files, 14 total; no unrelated changes and no staged
changes. Branch/HEAD/main match the state above, with main/HEAD ahead/behind 0/0.
No local origin/main ref is available; no fetch, push, commit or merge was performed.

One required correction was reproduced and fixed: persisted specialist attempts
could disagree with `player.competences`, retaining improved resolution or survey
cost without its authoritative basis. Validation now rejects the mismatch. A new
regression covers all three operations in both directions and verifies source-file
and active-session preservation on failed load.

Completion-review verification passed: changed-Python syntax checks; all seven
focused competence groups; the 20 affected regression scripts listed above; 36
accepted-outcome narration-prompt cases; and maintained Git verification, including
lifecycle validation and diff checks. After the correction, the focused suite and
affected save/load, West-Road and World State regressions were rerun successfully.

Exact regression entry points, each run with `.\.venv\Scripts\python.exe`:

```text
test_west_road_predicament.py
test_west_road_presentation.py
test_discovery.py
test_contextual_action_projection.py
test_current_scene_projection.py
test_save_load.py
test_world_update.py
test_narration_context.py
test_narration_request.py
test_narration_prompt.py
test_narration_pipeline.py
test_narration_output.py
test_elapsed_time_transition_observation.py
test_time_pressure_effect.py
test_time_actor_relocation.py
test_time_evidence_trace_effect.py
test_navigation_projection.py
test_one_hour_west_road_exit_traversal.py
test_western_trade_road_arrival_discovery.py
test_actor_knowledge_response.py
```

`test_character_competence.py` ran before and after correction; `py_compile`
covered the six changed engine modules and that test. Maintained verification used
`D:\Codex Tools\GitWorkflowTools\Invoke-GitWorkflowVerification.ps1` with
`Profiles\AINarrativeRPG.psd1`, including `tools/validate_project_records.ps1`,
`tools/preflight.ps1`, lifecycle JSON parsing and working/index diff checks.

The actual Codex environment still lacks the real tokenizer cache. A cache-only
narration-source check stopped before any download; the source contract passed
with an offline tokenizer stub. Exact token counts/input-limit behavior for the
extended prompt remain unverified. The provider adapter is unchanged, and safe
context/prompt propagation passes offline; this limitation does not block owner
smoke. No live provider was contacted.

Completion-review verdict: READY FOR OWNER SMOKE. Owner smoke passed and the owner
accepted Sprint 10.78 on October 4, 2026. Real tokenizer-backed narration token
counting remains unverified because the tokenizer cache was unavailable. The offline
narration contract passed, the provider adapter is unchanged, and this is an accepted
non-blocking environment limitation. No live provider was contacted.

## Candidate status
Accepted and frozen pending final Git integration. `next_sprint` remains null.
