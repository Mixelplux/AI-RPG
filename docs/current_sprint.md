# Physical Traversal Core V1a — M1 Core Domain Foundations

## Acceptance and lifecycle closure

Owner formally accepted M1 on October 26, 2026 after both blocking defects were
corrected and verified. No known blocking defects remain. M1 is complete and
closed using the existing JSON terminal state `complete`; lifecycle is idle.
`active_sprint`, `active_capability_package` and `next_sprint` are null;
`latest_completed_sprint.id` is `physical-traversal-v1a-m1`.
JSON remains the sole machine lifecycle authority. No M2 is selected, staged or
started; further implementation requires separate owner authorization.

## Accepted boundary and evidence

Risk: Elevated. Baseline: `85ec1811315686f9ea6691235078bf10c25265fc`.
Branch: `codex/physical-traversal-v1a-m1`.
Accepted: reusable local World position/surfaces/physical objects, shared PC/NPC
Character facts, actual 2024 climbing resolution, separate World-established fall
contributions and common assessment interfaces. Results remain provisional;
consequential publication and new-domain persistence are M2 obligations.

Accepted evidence: 54 focused traversal tests, 246 affected regression tests,
offline legacy save/load, syntax, whitespace, documentation and lifecycle checks
passed after corrections. See the [handoff](physical_traversal_m1_handoff.md) for
defect evidence, verification limits, documentation reconciliation and exact
publication inventory. Closure changes records only; accepted mechanics remain
unchanged and gameplay tests need not be repeated for these wording changes.

The two P3 observations remain deferred to M2: narrow unnecessarily broad
Character dependencies and evaluate named dependency records instead of positional
tuples. Preserve the accepted exposed/unsecured, properly protected and near-ground
failure matrix through consequential acceptance, continuation and persistence;
see the [required M2 validation](physical_traversal_m1_design.md#required-m2-validation-not-implementation-in-m1).

## Git and environment disposition

All 17 M1 publication paths remain uncommitted; index empty. Owner acceptance
does not authorize staging, commit, merge or push. Publication preparation stops
before those actions. Original dirty checkout, saves, shared tooling and unrelated
worktrees are preserved. No providers are invoked.

The ignored worktree-local `.venv` junction continues to expose the approved
`D:\AI RPG\.venv`; no environment recreation or package installation.
Prepublication preflight uses this isolated root for both `RepoRoot` and
`ExpectedRepoRoot`. Shared workflow tools and their canonical profile remain
unchanged; that profile targets the original checkout, so isolated checks use
explicit worktree paths.
