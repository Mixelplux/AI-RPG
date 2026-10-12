# Bounded Contextual Action & Consequence V1 — implementation handoff

## Owner acceptance and controlled publication — October 11, 2026

The owner accepted the final corrected implementation and authorized publication.
This supersedes the historical pending-acceptance and uncommitted-only status
statements below. Publication changes lifecycle/acceptance records only; accepted
implementation, tests, fixtures and correction evidence remain unchanged.
Lifecycle closes with this milestone commit: no active or next package.

Final verification covers 51 action groups, 13 affected regressions, preflight,
lifecycle, exact file/commit checks, strict fast-forward and preservation. The
normal Medium-integrity context is approved for the existing main publication
checkout; no ACL or permanent tooling/profile changes are authorized. Exact
published SHA, actual GitHub main synchronization and preservation results are
recorded in .artifacts/contextual_action_publication/publication_report.md after
publication. Existing baseline provider-fixture failures and accepted limitations
remain as documented below. The planned architecture review is not begun.

## Historical implementation and correction handoff

October 11, 2026. Recommendation: ready for owner experiential smoke, with the
two unchanged baseline provider-fixture failures recorded below. Elevated.
Implementation is uncommitted and has not been accepted.

## Repository and authority

Baseline and feature HEAD: 09d660af6da8b75f980ac2a32d664ba28d3ba8a0.
Branch: codex/bounded-contextual-action-consequence-v1.
Worktree: D:/AI RPG/.artifacts/contextual-action-consequence-v1.
The index is empty. No commit, merge, push, publication or live provider call was made.
The original D:/AI RPG checkout remains at 618ad922c15d78d9d413cde73420fe1b0ce686fe
with its preserved experimental status. Protected main remains at the baseline.
Existing worktrees, saves and prior evidence were not edited. Verification uses
the existing official .venv through an ignored junction in this worktree.

Lifecycle remains active awaiting owner smoke/acceptance; no next package is
selected. This is an implementation handoff, not a committed review candidate.

## Implementation and decisions

- HandlingFrame is a compatible specialized frame; investigation's ActionFrame
  and its behavior remain intact. Raw and structured input use the same assessor
  and executor.
- A single pending proposal discloses the method, risk and one-hour cost. Natural
  confirmation revalidates current authority. Constraints cannot be acknowledged
  away. Added restrictions require a fresh compatible proposal. Even methods
  without additional damage risk disclose effort before execution.
- Optional material_conditions in World State own stability, fitting, position,
  integrity, bounded cooperation, initialization time and causal references.
  Only authored finite values/transitions are allowed. Existing history stores
  preparations, draws, accepted effects and time developments; there is no
  second outcome ledger. Validators reconcile material records with that history,
  including authorization restrictions and deterministic result text.
- Stabilization is deterministic. Adjustment/repositioning reuse engine-owned
  untrained d6 resolution. No new competence tag or skill grant was introduced.
- Preparation precedes the one-hour time transition. Existing time effects and
  the authored material development run before remaining feasibility is checked.
  An interruption preserves preparation/time but consumes no outcome draw.
  Candidate exceptions preserve published world, scene and pending focus.
- A method against an unchanged accepted material/cooperation basis recalls its
  existing outcome rather than rerolling. A materially different basis or method
  is required for another attempt; there is no generic retry planner.
- Both fixtures use the same production pathway and condition validator. One
  requires a present willing helper, the other has no NPC. Identifier renaming
  and declaration reordering are tested.
- Material narration uses existing local scene composition and deterministic
  results. Mutable circumstances come from conditions, not description seeds.
  The opt-in CLI avoids the older market narration route, including on look.
  No universal semantic validator or narration redesign was added.
- Saves retain envelope version 1. Undeclared packs get no new state fields.
  Declared packs require their material state; load never invents missing facts.
  Load/reset clear unsaved proposals/focus; a failed load preserves the session.

## Changed files

Existing: docs/current_capability_package.md, docs/current_sprint.md,
docs/current_sprint.json, engine/game_engine.py, engine/world_state.py,
engine/region_validator.py, engine/save_system.py, engine/narrative_projection.py,
play_game.py.

New: engine/contextual_action.py, engine/material_state.py,
data/regions/market_passage_v1.json, test_fixtures/archive_shutter.json,
test_contextual_action_consequence.py, tools/verify_contextual_action.py,
this handoff.

Default Region Packs, default campaign saves, standing doctrine and system
manifests are unchanged.

## Verification

- 24 production acceptance groups pass. These include objective paraphrases,
  constraints, contextual/stale confirmation, all d6 outcomes across both
  fixtures, distinct methods, cooperation/refusal, raw/structured execution,
  renamed identifiers, preparation/time interruption, rollback, malformed
  saves/history, persisted effects, scene fidelity, CLI and fractional-cost rejection.
- 30 existing assertion-based regression scripts passed: investigation, competence,
  North Gate working context, Scene Construction, player scene route, interaction
  kernel/history, history query/context, saves, navigation/current-scene/contextual
  projections, three time-effect scripts, elapsed observation, timed traversal,
  West Road predicament/theft/presentation/relevance, actor location/knowledge,
  discovery, scene/narration context, request/prompt and input foundation.
- test_world_update.py is an early print-only demonstration: it executed
  successfully and is not counted as an assertion-based pass.
- test_resolved_narration.py has 8 passing groups and 2 failing provider-fixture
  groups: test_two_stateless_provider_requests and
  test_provider_failure_and_invalid_preparation. An offline in-memory import
  comparison against exact protected Git source reproduces the same two failures
  and the same eight passes. They remain baseline failures, not claimed passes
  or repaired provider behavior. DF-008 remains deferred.
- Changed Python sources parse; lifecycle validation reports 7 passes, 0 failures.
  Git diff/index checks pass. Established GitWorkflowTools verification passes,
  reporting unchanged repository state during checks.
- Logs stay under this worktree's .artifacts/contextual_action_verification.
  The historical investigation EVIDENCE path is redirected in the verifier;
  no prior C:/tmp acceptance report/save is overwritten. All runs block network.

Reproduce: .\.venv\Scripts\python.exe -B tools/verify_contextual_action.py
The runner deliberately returns a failure for the unchanged resolved-narration
script; see the baseline comparison above. Do not report the whole run as green.

The shared Git workflow profile is copied into ignored .artifacts only to bind
its repository/expected preflight root to this worktree. Shared tooling and the
canonical AINarrativeRPG profile were not modified.

## Owner experiential smoke

From the implementation worktree run:
.\.venv\Scripts\python.exe -B play_game.py --scenario market

Opt-in saves use .artifacts/contextual_action_save.json, not saves/savegame.json.
Use separate reset runs for these experiences:
1. Observe the cart, wheel, driver and alternate route; no quest is announced.
2. Ask: Help get the cart out of the passage without damaging the cargo.
   Read the disclosed proposal, then say: All right, try it carefully.
   Judge the inferred preparation and accepted result. Outcomes are uncertain.
3. Reset; ask to adjust the wheel, or force the cart aside. Judge risk disclosure
   and the effect of cargo-preservation restrictions. Cancel unwanted proposals.
4. Reset; go to Side Lane, wait twice, return to Market Square. Observe the
   once-only development, then save/load and judge continuity.
5. Describe first-person movement around the cart, or find another route without
   intervening. These do not authorize physical intervention.

Owner smoke judges presentation, freedom and coherence. Automated tests own
mechanics, authority, persistence and rollback verification.

## Remaining limits

Bounded lexical interpretation; three handling families; finite authored
material consequences; one development per target; whole-hour effort. No
general physics, inventory, cargo transfer, economy, injuries/combat, general
repairs, arbitrary persuasion, NPC planning, provider integration or migration.
Ambiguous/unsupported language asks for clarification rather than inventing
execution. Partial/failed attempts may require a different supported method or
changed material circumstances. No subsequent objective starts automatically.

Await owner acceptance and separate Git authority. Do not select another package.


## Owner smoke correction — October 11, 2026

The first owner smoke exposed blocking interaction failures. The original
readiness assessment above is superseded by the corrected-candidate evidence in
contextual_action_owner_smoke_correction.md. Named actor/role resolution,
question/offer separation and contextual confirmation/rephrasing are corrected.
The exact failed inputs now execute once through the production CLI and the
normal --scenario market entry point. All 38 acceptance groups and 13 affected
regression scripts pass. Owner acceptance is pending; no Git authority is granted.

## Final structural correction — October 11, 2026

The later smoke's inspection/possible-repair failure is corrected by distinguishing
epistemic ability clauses from authorization guards. Fitting objectives resolve
the authored visible feature. Cooperative movement was traced and verified as
authoritatively adjudicated routine preparation after confirmation. All 51 action
acceptance groups and 13 affected regressions pass. The actual production CLI
demonstrates fitting alignment and separate cart movement; controlled evidence
covers partial/failure outcomes, refusal/absence, changed feasibility and a
different approach after partial movement. See
contextual_action_structural_correction.md for current evidence and limitations.
The isolated candidate remains uncommitted, awaiting owner acceptance.
