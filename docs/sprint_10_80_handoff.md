# Sprint 10.80 - Scene Context V1 implementation handoff

October 4, 2026. READY FOR OWNER RE-SMOKE as an uncommitted working diff.
Owner smoke and acceptance are pending; the sprint remains active. No next
package has been selected.

## Repository and authority
Branch: `codex/scene-context-v1`.
HEAD and protected `main` baseline: `dad93cea3a6b38aa5cd6b9852f44340676be241f`
(`feat: add causal world follow-through v1`). Both remain unchanged.
No remote configured. No Git staging, commits, push or merge performed.
The owner runtime modification to `saves/savegame.json` was present at startup;
it was not edited or included in implementation review. Index is empty.

## Architecture and behavior
`engine/scene_context.py` derives a small read-only presentation interpretation
from the existing local scene, consuming no raw causal ledger or remote state.
The existing narration context, request and prompt carry it to the unchanged
provider adapter. Shape validation rejects missing activity constraints.
No new simulation, ownership, persisted state, save version or migration.

Scene Context supplies location facts, current weather (including severity,
temperature, wind and visibility) and existing time, qualitative expected
activity, the declared player intention and the existing locally filtered
competence projection. Market Square's authored seed now supplies open space,
stall/passage function, surrounding commercial/civic character and normal uses.
The original scene snapshot remains available as authoritative source material.

Market activity is a presentation bound, not a population or merchant schedule:
compatible daytime conditions permit ordinary activity; dawn or severity >= 0.5
limits it; evening/night quiets it. A blizzard suppresses it to sparse at most;
severity >= 0.8 makes ordinary outdoor commerce effectively absent. Blizzard
and severe-weather restrictions take precedence over time. Missing conditions
do not justify bustling commerce. No exact vendor count or stock is established.
Time is taken as supplied by the engine; no new clock progression is inferred.

The centralized narration contract permits ordinary incidental people, goods,
props, animals, social/sensory details and connective movement implied by intent.
They are prose only, not persistent resources, actors or interactable inventory.
Player intent does not establish facts, arrival, discoveries or consequential
choices. Clues, important NPCs, hidden motives, threats, faction activity,
consequences, outcomes and resolutions require supplied authority. Competence
may guide attention and interpretation while preserving status and uncertainty.
Instructions favor selective experiential narration without a prose template.
Existing player-equipment constraints, local theft guardrail, structured-output
rejection and fail-closed provider behavior remain intact.

## Verification
Passed with `.\.venv\Scripts\python.exe`:
- `py_compile` for all changed Python files.
- `test_scene_context.py`: normal Market Square, sparse/severe blizzards, severe
  snow, night/dawn, intent, perspective without truth changes, incidental and
  consequential contracts, missing constraints and provider-input propagation.
- `test_narration_context.py`, `test_narration_request.py`,
  `test_narration_prompt.py`, `test_narration_output.py`,
  `test_narration_pipeline.py`, `test_pressure_narration.py`.
- `test_character_competence.py`, `test_west_road_market_theft.py`,
  `test_west_road_scene_relevance.py`, `test_current_scene_projection.py`.
  Existing causal regressions cover local theft visibility, remote Market
  filtering, North Gate relevance, save/load compatibility and atomic rollback.
- `test_narration_source.py`, `test_openai_responses_narration.py` with the
  previously accepted offline tokenizer stub and fake transport; no network.
- `test_region_topology.py` for the authored region's maintained contracts.
- Maintained GitWorkflowTools verification with `Profiles/AINarrativeRPG.psd1`,
  including interpreter, preflight, lifecycle JSON and record checks; working
  and index diff checks. Exact changed-file review completed.

A pressure regression caught the initially generic activity key `level`, which
collided with its protected pressure-key prohibition. Renaming it to
`availability` resolved the regression; the affected checks passed afterward.
An ignored offline test harness initially lacked the repository import path;
the corrected harness passed. Generated verification files stay in `.artifacts/`.

Real tokenizer counts/input-limit behavior remain unverified under the known
cache limitation; no retry or cache remediation was attempted. Live prose
quality has not been tested. Full gameplay suite was not run; save serialization
is untouched, and affected competence/causal save-load regressions passed.
The standalone legacy `run_scene_test.py` prompt builder is unchanged; the
supported narration context/request/prompt/provider path carries Scene Context.

## Original implementation files (before player-path correction)
- `data/regions/bryn_shander.json`
- `engine/scene_context.py` (new)
- `engine/narration_context.py`
- `engine/narration_request.py`
- `engine/narration_prompt.py`
- `test_scene_context.py` (new)
- `docs/current_capability_package.md`
- `docs/current_sprint.json`
- `docs/current_sprint.md`
- `docs/sprint_10_80_handoff.md` (new)

Original working tree: seven modified tracked implementation files, three untracked
implementation files, plus the pre-existing modified owner save. Index: empty.
Owner next step: review the bounded diff and smoke Market Square narration
under ordinary and blizzard conditions, focused player intent and relevant
competence. Acceptance and any later Git authority are separate decisions.

## Owner-smoke player-path correction

Root cause: `play_game.py` displayed `get_narration()`'s deterministic scene
description, while AI Scene Context narration was reachable only through the
diagnostic preview command. Observation printed the interaction kernel's inert
acknowledgment and did not invoke narration. Keyword-anywhere movement
classification sent the smoke sentence's `walk` through directional resolution.

The CLI now presents Market Square refreshes through `get_narration_preview()`:
existing context -> request -> prompt -> provider source -> validated prose.
This happens after simulation accepts travel, using the current local scene,
weather, time, competence and causal filtering. Successful observation and
bounded player-intention commands use that same boundary and preserve declared
input. Scene comparison still prevents repeated automatic requests on unchanged
scenes. Load/reset use `look` as presentation intent; later refreshes carry the
latest accepted command. No prose template or new description system was added.
Provider rejection presents an unavailable/retry notice, without raw grounding,
rejected prose or provider error details. It cannot mutate simulation state.

The only classification change recognizes first-person `I walk/move/wander/stroll`
followed by `through/around/about/among/along` as within-scene intention. Explicit
`go to`, `head to`, `move to` and existing directional movement retain their
routes. Unknown input and other parser categories remain unchanged. Observation
presentation intentionally changes from acknowledgment to useful generated prose.
The central contract now explicitly requires grounding to inform prose and
weather to affect the experienced activity. Existing incidental-detail freedom,
consequential restrictions and player-agency limits reach the live prompt.

Exact files changed by this correction:
- `play_game.py`
- `engine/interaction_kernel.py`
- `engine/scene_context.py` (existing uncommitted candidate file)
- `test_player_scene_route.py` (new)
- `test_west_road_market_theft.py`
- `test_west_road_presentation.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/sprint_10_80_handoff.md`

Correction verification passed with the official interpreter:
- Syntax checks for all correction Python files.
- Actual CLI-loop reproducer: normal/sparse/severe-blizzard Market arrivals,
  `look`, exact smoke intention, explicit navigation, state immutability,
  request/prompt permissions, rejected-output handling and causal locality
  across six accepted West-Road scenarios.
- Existing Scene Context, interaction kernel, narration context/request/prompt/
  output/pipeline, pressure narration and Character Competence tests.
- Market theft, West-Road scene relevance and current-scene projection tests,
  including their existing causal save/load and rollback assertions.
- West-Road presentation, navigation projection and one-hour exit regressions.
- Provider source and Responses adapter checks with the accepted offline
  tokenizer stub and fake transport. No live provider contacted or cache retry.
- Maintained Git verification, lifecycle validation and diff checks; exact
  correction diff/file review.

The causal CLI regression initially failed because it expected deterministic
theft prose and had no offline source for the newly connected route. Its existing
visibility assertion now exercises the real prompt/pipeline with a fake source
that renders only supplied local facts; it passed. The presentation regression
likewise uses offline validated prose and now expects a scene response to `look`.
No causal simulation or persistence code changed. Standalone save/load tests were
not rerun because serialization is untouched; affected causal roundtrips passed.

Known tokenizer-cache limitation remains unchanged. Offline results prove routing
and presentation contracts, not live provider prose quality or real token counts.
The owner should run the supplied three-command smoke in the configured local
provider environment; unavailable narration is reported explicitly on failure.

Final working diff includes eleven modified tracked implementation/record files
and four untracked implementation/record files, plus the pre-existing modified
owner `saves/savegame.json`. Index is empty. HEAD and protected `main` remain
`dad93cea3a6b38aa5cd6b9852f44340676be241f`; branch remains
`codex/scene-context-v1`. No staging, commits, push, merge, next package or owner
save edits. READY FOR OWNER RE-SMOKE; acceptance remains pending.
## Latest correction: Luna-low validation — October 5, 2026

READY FOR OWNER RE-SMOKE. The October 5 correction below supersedes earlier
Git-state and provider-default statements in this historical handoff. Sprint
10.80 remains active; owner acceptance and commit/merge authority remain separate.

### Runtime and contract correction

`engine/narration_source.py` centrally selects provisional `gpt-6-luna` with
`reasoning.effort=low`; [official Luna documentation](https://developers.openai.com/api/docs/models/gpt-6-luna)
supports that effort on Responses. Timeout remains 20 seconds, retries zero,
output budget 256 tokens including reasoning, local input ceiling 8,000 tokens,
output character ceiling 4,000, `store=False`, with no tools or conversation state.
The installed tiktoken model registry cannot resolve Luna. Local input counting
therefore keeps the existing Mini-associated o200k tokenizer independently of
API selection; real provider usage/tokenizer equivalence is not claimed. The known
cache limitation was not retried or repaired.

The Scene Context contract now requests second-person house narration even for
first-person player intentions, while allowing natural quoted NPC speech.
Measurements inform qualitative lived description; exact numbers require a
credible in-world reason supplied by context. No post-generation replacement or
fixed phrase table is used. Restrained, active, concrete prose and occasional
evocative detail remain permitted. Incidental goods, people, activity, movement
and sensory freedom remain intact. Explicit restrictions now also identify
unsupported building damage/history, hidden compartments, NPC knowledge/motives
and discoveries. No simulation, causal, competence, save or elevated-mode changes.
Preview helper metadata and the existing live-smoke diagnostic now consume the
central runtime configuration rather than a duplicate Mini literal.

Exact files changed by this correction (all reconciled into Sprint 10.80 index):

- `engine/narration_source.py`
- `engine/narration_pipeline.py`
- `engine/scene_context.py`
- `test_openai_responses_narration.py`
- `test_scene_context.py`
- `tools/run_openai_responses_live_smoke.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/decisions.md` (dated configuration supersession note at ADR-058)
- `docs/sprint_10_80_handoff.md`

Lifecycle JSON, active sprint/package identity, Routine risk and `next_sprint=null`
are unchanged. Its provider prohibition continues to enforce offline automated
verification; the explicit owner-invoked evaluator exception is recorded in the
package and this handoff.

### Focused evaluator validation

Authorized live command, from repository root with an environment API key:

```powershell
.\.venv\Scripts\python.exe -m tools.narrator_eval --configuration luna-low --repetitions 3 --scenario market_blizzard_arrival --scenario market_browsing --scenario burned_inn_approach --scenario failed_hidden_search --scenario tactical_observation
```

Live validation was NOT RUN: `OPENAI_API_KEY` is unavailable in the execution
environment. No live provider was contacted. Raw temperature/visibility leakage,
first-person narration and authority violations are consequently unassessed;
offline checks cannot prove those prose qualities. Owner re-smoke/review remains
necessary for active intention, harmless texture, burned-inn fidelity, failed-search
uncertainty and competence interpretation.

The unchanged evaluator successfully exercised exactly these five cases with
three repetitions and Luna-low using fake transport and offline tokenization.
All 15 requests carried the corrected contract and Luna/low setting; JSONL records
were complete with no request-integrity/marker flags. These fabricated outputs
are integration evidence only, not model-quality evidence. Ignored artifacts:
`.artifacts/narrator_eval/luna_low_validation_offline/20261005T093702Z-39837b5839e9/`.
Its manifest explicitly records `validation_mode=offline_fake_transport`.

Preservation caveat: the separate evaluator's historical test still asserts Mini
as production default and absence of reasoning. It is intentionally unchanged and
was not treated as current runtime validation. The unchanged harness also inherits
the adapter's reasoning field when a configuration has `reasoning=null`; a future
mixed-model Mini comparison therefore needs separate evaluator maintenance to
remove inherited reasoning. The focused Luna-low path explicitly overrides it
and passed offline. No evaluator change was folded into this product correction.

### Verification and final Git boundary

Passed with the official interpreter and offline tokenizer/fake transport:

- Syntax checks for all six changed Python files.
- Responses adapter (Luna/low, bounded request fields, input rejection before
  transport, output limits, refusal/incomplete failures and missing key).
- Narration source, context, request, prompt, output and pipeline scripts.
- Pressure narration and Scene Context proving cases, including new contract
  propagation, unchanged intention input and existing incidental/authority rules.
- Character Competence regressions, including accepted outcomes and save roundtrip.
- Sprint 10.79 West-Road scene-relevance/local-causal regressions and causal save/load.
- Player scene route regressions, including locality and fail-closed presentation.
- Focused 15-request evaluator integration described above.
- Lifecycle validation, maintained Git verification, diff checks and exact
  correction file/index review. No real tokenizer-cache retry or full paid run.

The complete corrected staged Sprint 10.80 candidate has these 20 paths:

- `data/regions/bryn_shander.json`
- `docs/current_capability_package.md`
- `docs/current_sprint.json`
- `docs/current_sprint.md`
- `docs/decisions.md`
- `docs/sprint_10_80_handoff.md`
- `engine/interaction_kernel.py`
- `engine/narration_context.py`
- `engine/narration_pipeline.py`
- `engine/narration_prompt.py`
- `engine/narration_request.py`
- `engine/narration_source.py`
- `engine/scene_context.py`
- `play_game.py`
- `test_openai_responses_narration.py`
- `test_player_scene_route.py`
- `test_scene_context.py`
- `test_west_road_market_theft.py`
- `test_west_road_presentation.py`
- `tools/run_openai_responses_live_smoke.py`

The same five evaluator files remain byte-identical, unstaged and untracked:

- `docs/narrator_model_evaluation_v1.md`
- `test_narrator_eval.py`
- `tools/narrator_eval.py`
- `tools/narrator_eval_models.json`
- `tools/narrator_eval_scenarios.json`

The only tracked unstaged change is the pre-existing owner `saves/savegame.json`.
It was never opened or written by this task; length and modification time match
the task-start metadata. Generated artifacts are ignored and excluded from the
index. Branch is still `codex/scene-context-v1`; HEAD and protected `main` remain
`dad93cea3a6b38aa5cd6b9852f44340676be241f`. No commits, push or merge occurred.

## Continuity and progression correction — October 5, 2026

READY FOR OWNER RE-SMOKE as a staged, uncommitted implementation handoff.
This section supersedes the preceding candidate file count. Sprint 10.80 remains
active, Routine, with `next_sprint=null`; no lifecycle transition was made.

Root cause: each runtime request contained authoritative Scene Context but no
record of descriptions actually presented. The same generic contract applied to
arrival, look and focused actions, permitting independent incidental invention
and repeated overviews. Destination-route messages concatenated each internal
hop's directional acknowledgment directly into CLI output.

`engine/scene_continuity.py` holds a CLI-session presentation record, separate
from GameEngine/world state and serialization. It retains deduplicated sentence
excerpts from accepted, displayed narration as descriptive claims: at most 24
entries, at most 4,000 characters each, at most 8,000 total characters. Initial
orientation (first four entries) and recent resolution are favored; oldest entries
are discarded when the character budget requires it. This avoids semantic guessing
or an extra provider call. It is a bounded claim record, not durable world truth,
an authoritative fact extractor, or an ever-growing player/provider transcript.
Older details can age out at the explicit bound. Failed/rejected narration never
enters the record. Location transitions and successful load/reset clear it; in-scene
actions and ordinary interactions retain it. Nothing is saved or restored.

The existing preview API accepts optional presentation input and copies it into
Scene Context. Existing context/request/prompt validators carry and validate its
shape. Diagnostic/evaluator callers remain compatible without supplying it.
The CLI selects `orient` when no prior description exists, `expand` for general
look, `follow` for focused observations/within-scene intentions, and `narrow` for
ordinary Market Square conversations. Focus is the declared input. Previous
conditions accompany current authoritative conditions, permitting justified
evolution without turning narrator claims into authority.

The central contract directs the narrator to preserve compatible low-consequence
claims, defer to authoritative state, and explain changes justified by state,
meaningful time, accepted action or established facts. It directs look to add
resolution and focused action to reveal new detail, spending most prose on changes
or discoveries. Persistent conditions should usually appear through their effects
after establishment, with material changes still described. Existing second-person,
incidental freedom, competence, equipment, consequence and provider restrictions
remain intact. Continuity is a prompt contract, not a semantic prose verifier;
offline tests establish data flow and instructions, not guaranteed model compliance.

CLI travel compression applies only to successful destination routes whose message
consists entirely of routine `You move ...` acknowledgments. It emits one named
destination transition. Failed/nonroutine messages stay visible, and explicit
direction commands retain their behavior. Pathfinding, hop execution, time,
navigation and causal consequences are unchanged. No interruption system was added.

Exact files changed by this correction:

- `engine/scene_continuity.py` (new)
- `engine/scene_context.py`
- `engine/game_engine.py`
- `play_game.py`
- `test_player_scene_route.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/sprint_10_80_handoff.md`

Verification with the official project interpreter passed:

- Syntax checks for all five correction Python files.
- Real CLI loop: arrival continuity, look expansion, browsing focus/known market
  state, newly established detail, previous weather, scene reset, focused observation,
  conversation narrowing, bounded record, rejected-output exclusion, authority
  markers, routine travel compression and failed/nonroutine message preservation.
- Scene Context; narration context/request/prompt/output/pipeline; pressure narration;
  interaction kernel; West-Road presentation.
- Narration source and Responses provider tests with the established offline
  tokenizer stub/fake transport. No live calls or tokenizer-cache retries.
- Character Competence; West-Road market theft and scene relevance; current-scene
  projection, including causal locality, save/load and atomic rollback assertions.
- Explicit navigation projection, one-hour exit traversal and save/load regression.
- Maintained GitWorkflowTools verification (preflight, interpreter, lifecycle JSON
  and project-record checks), working/index diff checks and exact diff review.

A newly added test initially misplaced a nonroutine-message assertion in another
test function; correcting the test resolved its NameError. Product regression checks
had already passed. No unresolved verification failure remains. Live provider prose
and real tokenizer counts remain unverified under the known limitation.

Final candidate: the preceding 20 staged Sprint 10.80 paths plus
`engine/game_engine.py` and `engine/scene_continuity.py` (22 staged paths total).
All eight correction files are included. The same five evaluator files listed
above remain byte-identical, unstaged and untracked. The only tracked unstaged
change is the pre-existing owner save, whose length (24,918 bytes) and modification
time (2026-10-04 19:43:39 UTC) remain unchanged; it was not opened or edited.
Generated files remain ignored. Branch, HEAD and protected main remain unchanged.
No commit, merge, push, model reevaluation or next-package work occurred.

Owner next step: `go to market square`, `look`, then
`i walk through the market and see what people are selling`. Assess progressive
resolution, compatible new detail, effect-based weather and coherent travel under
the unchanged provisional Luna-low runtime. Acceptance remains pending.

## Repetition correction — October 5, 2026

Owner transcript exposed repeated scene inventories across arrival, look and
focused browsing. Inspection and offline boundary tests confirm established
details, current focus, previous conditions and orient/expand/follow stages already
reach the provider. The likely cause is instruction ambiguity: preserving prior
facts was emphasized, while the repetition exception allowed any direct action
relevance and gave no explicit treatment of negative observations.

The targeted correction changes only the existing Scene Context narration
contract in `engine/scene_context.py`: established descriptive claims are already
known background, preserved by compatibility rather than restatement; location
grounding and expected activity are bounds, not an inventory. Subsequent broad
observation favors previously unmentioned observable ordinary detail. Focused
turns prioritize the current action, with only essential brief references to known
facts. Negative observations resolve that focus within supplied activity bounds;
a concise result suffices without a recap or consequential invention. Unchanged
weather needs no mention unless it materially affects the focus; relevant effects
and material changes remain available.

This applies to every scene using the existing contract. No location-specific
rule, phrase suppression, prose framework, packet schema, stage routing, world
state, causal behavior, persistence or model configuration changed.

`test_scene_context.py` adds fake-transport boundary coverage for orient, expand,
follow and narrow in market and non-market contexts. It verifies separate prior
details/current focus, previous/current conditions, unchanged authoritative
activity bounds, background and negative-result instructions, and world-state
immutability. Fixture prose is not evidence of generated prose quality.

Verification passed with the official project interpreter:

- Syntax checks for both changed Python files.
- Scene Context and real offline player route tests, including the three-command
  route and its orient/expand/follow metadata.
- Narration context, request, prompt, output, pipeline, source, Responses adapter
  and pressure narration regressions. Provider checks used fake transport and an
  offline tokenizer stub with network connections forbidden.
- Maintained Git verification, lifecycle/project-record checks, working/index
  whitespace checks and targeted diff review.

Correction files: `engine/scene_context.py`, `test_scene_context.py`, and this
handoff. They reconcile into the existing 22-path staged, uncommitted candidate.
Branch and HEAD remain `codex/scene-context-v1` at
`dad93cea3a6b38aa5cd6b9852f44340676be241f`; protected main is unchanged.
Owner save, evaluator files and separate narrator-smoke tooling were not edited
or newly staged. No commit, merge, push or live provider call occurred.

Ready for one short owner transcript re-smoke with the unchanged Luna-low runtime:
`go to market square`, `look`, then
`i walk through the market and see what people are selling`. Stop after those
three turns unless additional continuity evidence is clearly needed. Actual prose
improvement and owner acceptance remain pending; offline contract assertions pass.

## Owner acceptance and completion review — October 5, 2026

The owner completed the final live narrator re-smoke using the real narrator
(`gpt-6-luna`, reasoning `low`) with this sequence:

1. `go to market square`
2. `look`
3. `i walk through the market and see what people are selling`

The owner accepted the result and explicitly said “accepted, continue.” Accepted
behavior: route-hop chatter is compressed; arrival orients; look remains in
continuity and adds useful information; focused browsing resolves the declared
intent; compatible incidental details remain available; established details act
as background; unchanged weather can remain implicit; narration stays in second
person; no unsupported consequential facts were observed. The repetition
correction materially improved information progression. Minor storm-condition
prose repetition is accepted narrative refinement, not a Sprint 10.80 defect.
No additional smoke is required.

Finalization review confirms that the staged package implements general Scene
Context instructions and data flow across locations, with authored Market Square
grounding/activity where specific location interpretation exists. Current focus
and orient/expand/follow/narrow stages travel through the existing validated
narration boundary. Established details remain bounded descriptive claims,
compatible incidental details may continue, and consequential facts remain
constrained by authoritative input. Weather and expected activity constrain
narration. No simulation authority, causal-follow-through behavior, save format
or save version changed. Provider behavior remains fail-closed; no credential
handling or evaluator harness is included in the product candidate.

Finalization authorization: the owner authorized one commit with subject
`feat: add scene context v1`. No merge or push is authorized. The owner save,
evaluator files, narrator-smoke scripts and credential-bridge tooling remain
outside the product candidate. `next_sprint` remains null; save version remains 1.
