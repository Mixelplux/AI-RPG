# I3-M1 — Durable Consequential Continuity and Safe Resumption

Implementation handoff, October 24, 2026. **Owner-accepted after structural
verification and successful interactive/scripted experiential testing.**
Risk: Elevated. Publication preparation only is authorized; no staging, commit,
push or merge performed or authorized.

Baseline/HEAD: `a4a9874d0576c353c9c6738f7c9091f8555891ea`.
Branch: `codex/i3-m1-continuity-preparation`.
Worktree: `C:\Users\Richard\.codex\worktrees\i3-m1-continuity-preparation\AI RPG`.
The index is empty and the implementation remains an uncommitted working diff.
Original dirty checkout, owner saves and unrelated worktrees are preserved.

The owner approved the revised [preparation](i3_m1_preparation.md), including its
October 24 seconds/waiting reconciliation, then separately authorized this source
implementation, version-2 format, narrow validator/ADR work and offline Elevated
verification. That authorization supersedes historical preparation stop language;
it did not itself authorize acceptance, migration, live providers or Git publication.
The owner subsequently accepted the bounded implementation and authorized exact
publication preparation; migration, live providers and Git publication remain
unauthorized.

## Architecture and ownership

The same GameEngine → Coordinator → consequence_integration.Runtime.accept path
serves I2 and I3. There is no separate scenario adjudicator. Default legacy gameplay
and explicitly opted-in I2 retain their original contracts. New I3 configuration is
an explicit pair of Blueprint and Inputs, with an optional controlled draw supplier.

One private campaign root holds declarative domain inputs, adjudication state,
identities/facts/relationships/access, resources/conditions/commitments, accepted
mechanics, receipts, activities and World State with its prepared scene. Current
world/scene getters are defensive views of that root; legacy mutation cannot
silently alter it. Derived adjudication time and World State time publish together.
The old constructor caches are inactive in I3, not independently mutable truth.

World/Character/Action/Actor suppliers retain domain authority. The trusted
revise_campaign boundary accepts supplied current information, location or an F05
checkpoint, validates the whole candidate and prepares the scene before replacement.
It is not player input, an actor decision algorithm or untrusted provider acceptance.
A stale proposal cannot publish over such an owner change.

The immutable finite record vocabulary in campaign_records has exact field/type
checks and a closed list of supported domain records. It cannot import/execute
saved modules, objects or callbacks. campaign_continuity validates representations,
reference closure, declarations/content, accepted request/assessment/receipt coupling,
resource/time accounting, effects, access, commitments, activity progress and causal
history. Safe receipt validation uses read-only presentation of retained accepted
authority and pure retained-draw consistency checks; it never samples, adjudicates
an attempt or reapplies a consequence during restoration.

Current owner inputs are complete declarative snapshots. Historical acceptance
bases retain actual retrieved base premises, Character grant requirements and
definition closure; unrelated subjects are omitted. Accepted safe receipts survive;
full private F01 contexts and incidental/generated prose are not saved. Fresh
contexts are derived from accepted safe meaning, preserving its completion timestamp.

## Identities, interruption and continuation

Campaign and undertaking IDs are generated UUIDs. Explicit request IDs identify
attempts within their campaign; increment IDs are separately namespaced by campaign
and request. History IDs retain their World State identity and link the increment
to its accepted fictional completion time. Receipt equality binds actor, action,
target, method, means, constraints, binding, intent and undertaking.

Accepted recognition precedes current eligibility and returns prior accessible
meaning without cost, roll, time or effect. Conflicting reuse rejects. Recognition
does not permit continuation: a new request ID with explicit commit is a new
attempt/increment and requires fresh current domain dependencies and F05 checks.

Activities retain method/constraints, start, accepted increment references and
accepted effort in seconds, plus their supported unresolved checkpoint. Initial and
resumed execution enforce the same capability, means, conflicts, hidden conditions
and supported boundary. Owner-supplied blocked/missing-means/restart/development
checkpoints remain effective after restoration. A not_after_seconds checkpoint
prevents an indivisible supported increment from silently crossing an owner-supplied
meaningful boundary; it does not invent partial mechanics or a stopping time.
Earlier independently accepted progress survives later rejection. F05 enforcement
also lives at Runtime.accept, so coordinator bypass cannot waive the boundary.

The fixture uses existing routine/d6 resolution and finite effects for partial
inspection, retained finding/relationship and a commitment. A second accepted
attempt continues the same undertaking under fresh circumstances. It supplies
checkpoints and facts, not search rules or scenario-selected outcomes. An F05
restart-required checkpoint returns control; a fresh authorized undertaking/attempt
can proceed. No new spell, search or other restart mechanic is implemented.

## Persistence and failure guarantees

Default saves remain version 1. Explicit I3 saves are version 2 with the finite
continuing_gameplay section inside World State, retaining complete consequential
state and declared seconds/origin. No sidecar or separate receipt file exists.

The I3 writer captures a validated non-running root, encodes it completely, writes
an exclusive same-directory temporary file, flushes/fsyncs it, then atomically
replaces the destination. No fallible cleanup runs after successful replacement.
Pre-replacement encoding/open/write/sync/replace failure preserves the old destination
and live accepted state. Cleanup failure cannot mask the original failure.

GameEngine delegates load construction to GameSession/save_system. A separate
engine validates decoded records, installed finite rules, exact referenced public
Region content digest, all required state and derived scene before one prepared
runtime adoption. Malformed/incomplete state, broken references, changed declarations,
receipt mismatch and scene-preparation failure preserve the old root/scene and
source bytes. Load while acceptance is running refuses. No defaulting of missing
I3 sections, synthetic receipt recovery, reroll, effect replay or time advancement.

Valid version-1 saves continue through existing normalization/default construction.
Version-1-to-I3 promotion and version-2 downgrade refuse. Legacy I2 still refuses
save/load before I/O. No owner saves were converted or opened for testing.
New ordinary saves under saves/ are ignored; existing intentional saves/test_save.json
remains tracked. The publication/lifecycle validator blocks pending changes to
other tracked player-save paths. The historical tracked saves/savegame.json is
preserved, not silently removed from the owner's checkout or staged for deletion.

Guarantees apply to the successfully saved snapshot and supported synchronous
runtime. Unsaved play, global recognition across rollback/branches, concurrent
writers, automatic journaling and directory-level power-loss durability are not
claimed. Version-1 writer disk semantics remain unchanged.

## Seconds, waiting, historical meaning and re-entry

I3 uses canonical nonnegative integer seconds with a declared campaign origin.
Durations, activity effort, attempt/acceptance times, facts, terms/access periods
and causal history use that timeline. Booleans cannot stand in for integer fields.
hours_to_seconds explicitly converts known integer authored hours losslessly.
Legacy hour helpers/dispatch/fixtures remain unchanged and isolated; I3 rejects
direct legacy time advancement, reset and bare-wait dispatch. No second mutable
hours clock or sub-hour rounding is introduced.

WaitingIntent retains exactly a duration_seconds or condition reference, with
legitimate information-basis references for a condition. It and the unresolved
undertaking survive restoration without a deadline being invented. General
duration/event-wait execution is deliberately unavailable in M1: the common path
returns a safe unresolved authorization rather than making an event happen.
No calendar, daylight, combat timing, scheduler or provider semantics are inferred.

The bounded timed-development evidence uses existing binding Period expiration:
a condition governs an initial attempt, an authorized supported duration passes,
and after fresh restoration it no longer governs the next interaction. Prior
blocked result, costs, commitment and causal basis remain retained. Historical
facts are retrievable explicitly while absent from current applicability; re-entry
does not trigger consequences twice. Supplied meaningful temporal checkpoints
stop ordinary progression under F05. General retrospective offscreen adjudication
remains later I3 work; no West Road/gate/cart timing becomes production policy.

## Diagnostics and validation matrix

Runtime keeps a bounded private trace (128 records) of stage, attempt, revision and
safe reason code. Correlation crosses interpretation/responsibility selection,
retrieval, adjudication, validation, acceptance, persistence/restoration and
presentation; underlying domain diagnostic retains earliest failure. Optional trace
failure cannot affect gameplay. No hidden values, raw provider material or trace
records enter player-facing output or campaign truth. Rejections remain technical
or authorization outcomes; accepted blocked/failed attempts retain legitimate costs.

| Preparation case | Executed evidence in test_campaign_continuity.py |
|---|---|
| 1 Consequential round trip | test_01: independent engine, exact exported state, finding, balances, commitment, accepted mechanics and safe historical completion time. |
| 2 Retry recognition | test_02: current capability changed, identical retry unchanged with zero draws; conflicting request reuse refuses. |
| 3 Interrupted undertaking | test_03: blocked checkpoint and progress restored; fresh owner circumstances allow remaining increment. Waiting-intent round trip is separate. |
| 4 Changed circumstances | test_04: changed capability refuses; supplied hidden restriction changes accepted outcome without disclosure. |
| 5 Same restrictions | test_05: initial/resumed missing means and checkpoints; owning-boundary bypass and temporal/development cases also covered. |
| 6 Resolved mechanics | test_06: post-acceptance display failure then restore/retry; no new draw. |
| 7 New attempt/restart | test_07: existing F05 restart policy stops continuation; distinct authorized undertaking/attempt resolves anew. |
| 8 Prior increment retained | test_08: invalid later proposal cannot remove accepted progress, including across save. |
| 9 Later dependency | test_09: later activity actually retrieves accepted finding and requires the restored commitment. |
| 10 Stable identity/relationships | test_10: instance/definition, accepted identity and relationship traversal survive fresh restore. |
| 11 Recovery/compatibility | test_11 and 11b–11d plus strict shapes, declarations, temporary open and no-replay tests: corruption/faults preserve disk/live roots; v1 preserved, promotion/downgrade refused. |
| 12 Technical/time boundaries | test_12: exact 31/38-second values, explicit hour conversion and no technical/legacy advancement. |
| 13 Timed development/re-entry | test_13: existing period expiry changes the next restored interaction without replay or a scheduler. |
| 14 History/current distinction | test_14: retained expired fact accessible only as historical with its source/period. |
| 15 Failure attribution/access | test_15 and display/stale/reentrancy tests: earliest stage, intact authority and no hidden marker in public results/private reason codes. |

## Verification results

- Final syntax: all seven changed/new engine Python modules, new fixture, focused
  test and smoke compiled with the official worktree interpreter before execution.
- I3 focused suite: **29 tests passed**; socket/provider guards remain active.
- **21 directly affected regression scripts passed**: eight unittest scripts,
  **231 cases**, plus **13 standalone scripts**. Combined: **260 unittest cases**
  plus the 13 standalone regressions. Final save/load regression was repeated after
  the GameSession keyword forwarding change and passed.
- Covered I1/I2, F05, Information Resolution/adjudication, F01, material consequences,
  save/load, history/context/query, time/pressure/relocation/evidence and scene/
  narrative/player projection. Existing I2 refusal tests were preserved.
- Scripted offline owner smoke passed through partial progress, interruption,
  save, fresh reconstruction, unchanged recognition, blocked resumption, current
  authorized continuation and later dependency: final 69 seconds, two wedges and
  three receipts. Final focused/source/save/smoke checks passed after refinements.
- Player-save publication guard verified with simulated Git path output: player
  save rejected; intentional test fixture allowed; no player data read or changed.
- Lifecycle validator: **8 passes, zero failures**. Final preflight, workflow,
  documentation, whitespace and exact inventory/index evidence is recorded below.

Logs and deterministic test saves are ignored under .artifacts/i3-*. No providers
were invoked. Initial source editing found a non-unique text-edit anchor before
execution; it was corrected at the unique initializer. No required product
verification failure remains.

## Owner smoke

From the worktree root:

~~~powershell
.\.venv\Scripts\python.exe -m tools.smoke_i3 --scripted
.\.venv\Scripts\python.exe -m tools.smoke_i3
~~~

Interactive sequence: progress → interrupt → save → restore → retry → resume →
continue → depend → status → quit. Retry must leave 31 seconds/three wedges/one
receipt unchanged; resume must refuse while the supplied checkpoint remains blocked.
Continue supplies changed legitimate fixture circumstances and accepts the next
increment. Depend retrieves the restored finding/commitment; final counters are
69 seconds/two wedges/three receipts. Only the smoke's ignored save is written.

## Exact changed-file inventory

1. .gitignore
2. docs/architecture.md
3. docs/current_capability_package.md
4. docs/current_sprint.json
5. docs/current_sprint.md
6. docs/decisions.md
7. docs/design/systems/persistence.md
8. docs/design/systems/system-map.md
9. docs/i3_m1_preparation.md
10. docs/i3_m1_handoff.md
11. engine/campaign_continuity.py
12. engine/campaign_records.py
13. engine/consequence_integration.py
14. engine/game_engine.py
15. engine/game_session.py
16. engine/information_adjudication.py
17. engine/save_system.py
18. test_campaign_continuity.py
19. test_fixtures/continuity_suppliers.py
20. tools/smoke_i3.py
21. tools/validate_project_records.ps1

Additional directly necessary files remain within the approved subsystems.
Shared tools/profile, owner saves, production content and unrelated worktrees are
unchanged. Environment junction and generated evidence remain ignored.

## Documentation reconciliation and limits

Runtime architecture, Persistence manifest, system relationship map, ADR-062 and
current lifecycle/package/sprint records describe the actual candidate. The preparation
retains historical authority/evidence with an explicit superseding implementation
authorization. PROJECT/AGENTS/WORKFLOW, accepted gameplay Design, unrelated manifests,
prior handoffs and deferred findings need no change: no doctrine, general domain
capability, production content or deferred actor/history system was added.

This is bounded opt-in integration with explicitly supplied methods, capability,
scope, information and checkpoints. It is not general language interpretation,
production search/game content, an activity-specific restart model or autonomous
world development. Legacy scenario time owners require explicit adapters; they
are not silently mixed into seconds-based I3 campaigns. Exact Region content pinning
rejects material revisions; there is no content/save migration policy.

Tuple scans, whole-file snapshots and repeated accepted-history validation are
sufficient for this milestone, not demonstrated large-campaign performance.
Selected bases avoid exhaustive per-action world retention; indexing, compaction,
backends and causal retention policy need future evidence and authorization.
Receipts and relevant commitments are not pruned to satisfy arbitrary caps.

The owner accepted I3-M1 October 24, 2026. Lifecycle is complete/idle: active sprint
and package null, latest completed I3-M1, next_sprint null. This closes only the
bounded accepted milestone. The implementation remains uncommitted and the index
empty. Stop after publication preparation; no staging, commit, merge, push,
migration, live provider or later milestone.

### Final mechanical evidence

Established GitWorkflowTools verification passed with repository state unchanged
during verification. A worktree-specific copy of the established profile is ignored
under .artifacts; external shared tools/profile remain unchanged. Its Windows
PowerShell 5 preflight reported 19 passes, two warnings (supported older shell and
the expected dirty implementation), zero failures/blocks. Lifecycle: eight passes.
Direct worktree preflight under PowerShell 7: 20 passes, one expected dirty-tree warning, zero failures/blocks.

Final documentation verification passed: 138 local links, strict UTF-8/no BOM,
whitespace, JSON lifecycle semantics, exact 21-file inventory, unchanged baseline
and empty index. No save or production content diff; ignored new player saves and
tracked intentional fixture verified without reading player data. No Git candidate,
commit, merge, push or live-provider operation occurred.

## Owner acceptance and publication preparation — October 24, 2026

The owner confirms both interactive and scripted smokes passed: accepted partial
progress survived interruption/fresh restoration; identical retry caused no added
cost/time/receipt; restriction still blocked resumption; changed legitimate
circumstances permitted continuation; a subsequent action retrieved restored
consequences. Final accounting: **69 seconds, 2 wedges, 3 receipts**.
The owner accepts the reported **260 unittest cases and 13 standalone regressions**
and this bounded implementation with its stated compatibility/recovery limits.

Non-blocking observation: the smoke expresses a return-wedge obligation alongside
a consumed-wedge cost. This is a fixture-presentation ambiguity. Record only; no
fixture, source, semantics or test correction is part of publication preparation.

The exact 21-file inventory above is unchanged. Acceptance reconciliation changes
only the nine documentation/record files already in that inventory. The twelve
source/config/test/tool files are pinned before reconciliation and verified unchanged.
Gameplay evidence is reused because no accepted source or behavior changes.

Publication identity is an **uncommitted exact-content manifest**, not a commit or
Git tree. HEAD/parent baseline remains a4a9874d0576c353c9c6738f7c9091f8555891ea on
codex/i3-m1-continuity-preparation; no distinct candidate commit exists yet.
A SHA-256 manifest of exactly the 21 candidate source/document files is prepared
under ignored .artifacts/i3-publication-candidate.json; its final fingerprint is
reported separately to avoid a self-referential handoff hash. No saves, credentials
or ignored development data enter the content manifest.

Established GitWorkflowTools verification is applicable now. New-GitWorkflowCandidate
is deliberately not invoked: it performs stage-all and commit and would exceed the
owner's current authority. The existing strict fast-forward tool can be used only
after separately authorized candidate staging/commit and a clean committed candidate
with the verified main parent. No replacement Git workflow, temporary index, commit,
merge or push is used in this preparation.

### Publication-preparation result

Acceptance/status reconciliation is confined to the nine documentation files already
in the accepted 21-file inventory. The 12 implementation/config/test/tool files are
byte-identical to their pins captured from the owner-accepted worktree at task start.
No source modification, behavior correction or fixture ambiguity fix was made.

Required checks passed: 10 Python files compiled in memory with the official
interpreter (no bytecode/artifact rewrite), eight lifecycle/record checks, completed/
idle JSON semantics, strict UTF-8/no BOM, whitespace, 138 local documentation links,
exact inventory and empty index. GitWorkflowTools verification passed and reported
repository state unchanged during verification. Accepted gameplay evidence and
owner smokes are reused; no unrelated suite or provider was rerun.

Preservation checks passed: existing direct .artifacts file metadata, worktree/original
save file metadata, worktree registration list and all 16 unrelated worktrees'
HEAD/status match the captured start state. No player save contents were read or hashed;
existing ignored development files were preserved. New evidence uses only ignored
i3-publication-* files; prior evidence/profile remains untouched. No saves/data diff.

Published remote main and local main remain at the expected baseline. There is no
discrepancy between accepted implementation source and the prepared publication
content; documentation differences record acceptance, idle lifecycle, preservation
and readiness only. The exact content manifest covers the same 21 paths and is
reported separately after the last documentation edit.

**Readiness:** prepublication checks are complete. The official candidate operation
is ready for separately authorized staging/commit. Strict fast-forward publication
is not executable yet: it requires that distinct, clean committed candidate and
separate merge authorization, with main still at the verified parent. No commit,
Git tree candidate, staged index, merge or push was created here. No subsequent
development is selected or started.
