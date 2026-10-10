# Scene Construction V1 implementation handoff

October 10, 2026. Elevated. Implementation and automated verification complete;
owner acceptance received. Lifecycle is complete and idle with no next package.
The owner separately authorized final verification, staging and one implementation
commit for merge review. Merge and push remain separately authorized actions.

## Repository and scope

Worktree: D:/AI RPG/.artifacts/scene-construction-v1.
Branch: codex/scene-construction-v1.
Protected baseline and direct candidate parent:
48d469f07bb68e9ed4b1538ea09bd0525abde296.
Local main and origin/main remain at this baseline. Finalization prepares the
accepted implementation as one committed candidate on this branch; the exact
commit identity is reported in the merge review. The older experimental checkout and unrelated owner saves remain
untouched. The worktree uses the existing official interpreter through a .venv
junction; no interpreter/dependency replacement or shared-tool edit occurred.

The request mentioned a missing patrol. Accepted content establishes an overdue
caravan and reports of observers; this implementation preserves that premise and
does not create a missing patrol or other consequential event.

## Behavior and ownership

The initial North Gate passage grounds the player in the gate/blizzard, visible
Grey/Elin roles and watch guards, the uncertain public road situation and competing
concerns. Involvement is explicitly voluntary. Existing command guidance offers
conversation, investigation via the road, or travel elsewhere. Merely receiving
the scene acquires no clue, shares no report and makes no commitment.

The existing engine predicates derive every opportunity and cost. Their text and
existing staged guidance form a copied read-only handoff alongside the accepted
safe context/projection. No raw scene/debug/history data or private actor knowledge
enters scene preparation. Scene construction selects and expresses supplied meaning;
it does not adjudicate, grant knowledge, choose NPC behavior or become a second
authority. Public roles are limited to already present names and authored types.

The local pair uses Revised A privately, then stateless realization and established
output validation. A different adapter pair consumes the same source and uses a
tuple instead; the engine/CLI require no Revised A representation. Guidance stays
engine-owned even when an adapter mutates its copy. Adapter failure returns to
the existing deterministic scene/delta. No provider adapter was added or invoked.

Scene refresh selection is extracted from the existing CLI behavior and reused
for fallback and composition. Already delivered outcomes are suppressed. A failed
tracking attempt still consumes its engine-owned hour, stays at North Gate, adds
no finding/knowledge, and removes only that resolved approach. A choice-only refresh
needs no invented passage. Moving between gate/road reorients without replaying
the same public premise or already presented evidence. Load has no presentation
cache, so it may reorient, never assert a first-ever meeting. A fresh recap no
longer assigns the player an investigation they did not undertake.

Bounded epistemic corrections: track guidance says the signs suggest observation;
Mara's report remains attributed, and subsequent guidance refers to the retained
account without replaying it. The failed-search source describes reported prints
rather than deriving fictional meaning from the internal withdrawal command label.
Diagnostic context/history/pressure views and detailed scene functions remain.

## Changed files

- engine/scene_composition.py: safe source composition and local adapter pair.
- engine/scene_context.py: shared existing refresh selection.
- engine/game_engine.py: read-only narration entry point; bounded epistemic guidance.
- engine/resolved_narration.py: reported-print source wording only; accepted action path retained.
- engine/west_road_predicament.py: voluntary fresh recap wording only; no mechanics changed.
- play_game.py: scene integration, engine-owned guidance, and deterministic fallback.
- test_scene_construction.py: 14 focused behavior/authority/compatibility checks.
- test_west_road_presentation.py: one expectation updated for qualified track wording.
- tools/play_scene_construction_smoke.py: offline unbriefed-start launcher.
- docs/architecture.md, current_capability_package.md, current_sprint.md,
  current_sprint.json and this handoff: implementation/lifecycle records.

No Region Pack, simulation transition, eligibility, persistence implementation,
provider configuration or owner save changes. Save envelope remains version 1.

## Verification

Fourteen new checks cover first-contact coherence, accessible facts, public roles
and unchanged NPC knowledge, opportunity/cost parity, leaving voluntarily, actual
report-sharing prerequisites, commitment refresh, failure/retry, single CLI outcome,
load/re-entry, copy isolation, malformed-output/failure fallback, ordinary-location
and diagnostic preservation, and alternate representation/generic source use.

All 20 affected regression scripts passed: resolved narration; bounded narration
input foundation; context/request/prompt/source/output/pipeline/OpenAI fake transport;
player scene route; pressure narration; Scene Context; competence; predicament;
scene relevance; presentation; save/load; market theft; current-scene projection;
contextual-action projection. These ran under socket guards with zero network
attempts, using the existing tokenizer cache. No dependencies were downloaded.
Logs: .artifacts/scene_construction_verification.log. After final recap wording,
the new suite, predicament and presentation passed again; after the final
cross-location suppression, new suite, resolved narration and presentation passed.

Nine changed Python files pass py_compile. Worktree preflight: 20 passes, one
expected dirty-worktree warning, zero failures/blocks. Lifecycle validator: seven
passes. Maintained GitWorkflowTools with Profiles/AINarrativeRPG.psd1 passed,
including additional worktree preflight/record checks; its PowerShell 5.1 invocation
reports the established version and dirty-tree warnings. Direct worktree diff/index
checks pass. No staged changes. The scripted offline smoke launcher completed.

Two checks found directly caused issues that were repaired: the first local
realizer initially returned a decorated output packet rather than a raw candidate,
and guidance initially repeated Mara's reported detail. A new diagnostic assertion
also expected a heading absent from the unchanged diagnostic route; the fixture
now checks the actual scene/time fields. All affected checks passed afterward.

## Owner experiential smoke

Historical reproduction route; acceptance is complete and no further gameplay
research or owner smoke is required for this finalization.

From the isolated worktree root:

```powershell
Set-Location -LiteralPath 'D:\AI RPG\.artifacts\scene-construction-v1'
.\.venv\Scripts\python.exe tools/play_scene_construction_smoke.py
```

Read the introduction before acting. Evaluate orientation, the public uncertainty,
Grey/Elin's competing concerns and freedom to engage. A short complete test route:

```text
talk to Grey
go to Southwest Trade Road
investigate
talk to Mara
go to North Gate
present Repeated Watch Tracks to Elin
present Mara's Account to Elin
advocate patrol
follow withdrawal signs
quit
```

Expected: reports remain qualified; decisions require both reports actually shared
with Elin; patrol costs its existing hour and changes coverage; the fixed failed
search costs one hour, stays at the gate and adds no discovery. Its result appears
once; the following scene supplies remaining choices without replaying it. You may
instead leave with `go to Main Street`; this route is not mandatory gameplay.
Launcher-only RNG fixes the ordinary tracking draw to failure, blocks provider
construction/connections, and redirects saves to .artifacts/scene_construction_smoke_save.json.

## Acceptance and deferred findings

Owner-accepted October 10, 2026. Evidence:
C:/tmp/AI-RPG-Scene-Construction-Acceptance-20261010/acceptance_report.md.
The aggregate summary and checks confirm 12 routes, 110 commands, 26 evaluation
cases and 1,775 passing assertions, with no unresolved blocking failures and zero
network/provider attempts. Acceptance-start fingerprints match all fourteen
implementation/record files and the canonical region before finalization edits.
Only acceptance, authority, completion and deferred-finding records change here.

The following findings are nonblocking and deferred, without corrections in V1:

- Mara's caravan: the overdue overview can read as stale after her report; modeled
  caravan identity and resolution of the original overdue report are absent.
- Pursuing observers: the existing deterministic, zero-additional-time follow-up
  could be distinguished more clearly from uncertain, paid tracking. Mechanics pass.
- Public prerequisite guidance: Elin's two-report requirement is accepted public
  briefing. A persisted first-heard policy fact would require an excluded epistemic
  or familiarity capability; scene exposure grants no clue or receipt.
- Load reorientation: present-tense wording can restate a recorded failed check.
  Save restoration performs no new check, draw, cost, discovery or receipt.

No doctrine, persistence, save-version, gameplay or provider changes are included
in finalization. Candidate and protected-baseline merge acceptance remain owner
decisions; do not merge, push or select another package automatically.

Finalization verification repeated all fourteen focused checks and all twenty
affected regression scripts under socket guards: all pass, zero network attempts.
All nine changed Python sources pass AST syntax checks. Lifecycle validation
passes all seven checks. Worktree-aware preflight passes after explicitly supplying
the isolated expected repository root; its initial default-root mismatch was an
invocation-context error. GitWorkflowTools candidate verification uses a local
copy of Profiles/AINarrativeRPG.psd1 with only the repository/preflight root changed;
the shared tools and canonical profile are untouched. Complete diff/scope review
confirms exactly fourteen accepted files; production, tests, launcher and region
bytes remain identical to acceptance evidence. No new implementation was made.

## Implementation limits and runtime metadata

This is bounded local composition for the accepted gate/road slice. Other locations
and explicit preview/observation routes retain existing behavior. The source helper
accepts supplied ordinary projections without West-Road facts; this does not claim
general scene construction, familiarity, sensory simulation or NPC agency. Existing
time-of-day limitations and terminal follow-up branches remain. Broad UI/voice work,
procedural situations, persistent narrative memory and live semantic evaluation are
deferred. Structural validation cannot certify arbitrary replacement prose; only
the conservative local behavior and offline fixtures were evaluated here.

Execution is Codex in the GPT-6 family as identified by this session. The exact
runtime model ID and reasoning-effort setting are not exposed to the agent; no
claim that the brief's recommended GPT-6.1 Sol / High configuration was applied
can be verified. No model switch or provider invocation was made.
