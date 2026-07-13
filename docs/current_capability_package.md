# Authored Discovery Use and Thread Resolution

Status: Complete.

## Purpose and Owner-Visible Value

This approved package closes the current investigation gameplay loop: a player
can recall an authored clue they previously discovered, present it to an
eligible present actor, receive the exact authored response, and durably
resolve the open thread that produced its local evidence.

## Included Internal Milestones

1. Sprint 10.31 — Player-safe clue recall.
2. Sprint 10.32 — Persistent resolved-thread representation.
3. Sprint 10.33 — Strict authored resolution declaration.
4. Sprint 10.34 — Deterministic discovery-presentation action.
5. Sprint 10.35 — Atomic thread-resolution transition.
6. Sprint 10.36 — Player integration and package closeout.

## Scope, Ownership, and Compatibility

- Region Packs own immutable resolution declarations, clue labels, exact
  response prose, and optional resolved observations.
- World State owns durable discovered-clue membership, open-thread state,
  resolved-thread state, and causal lifecycle history.
- Scene Snapshots, perception, and narration remain derived; raw identifiers
  and lifecycle metadata remain hidden from ordinary player-facing output.
- Candidate-state preparation, validation, projection rebuilding, and one
  final live commit preserve atomicity.
- Save version remains `1`; legacy missing fields normalize narrowly only at
  load time.

## Exclusions

No generic dialogue, semantic clue interpretation, clue combination, quests,
objectives, rewards, branching outcomes, generic thread framework, effect
framework, actor beliefs, checks, evidence reuse, automatic propagation,
travel, combat, inventory, factions, economy, provider integration, or save
version `2` is included.

## Verification, Completion, and Rollback

Each milestone requires focused tests, affected regressions, manifest
agreement, and `git diff --check` before its authorized checkpoint. Package
closeout requires the full official verification cycle, save/load and
duplicate-safe tests, a scripted player-facing smoke test, the ADR, and one
capability-package review packet. The package is recoverable by reverting its
feature-branch checkpoints; it does not begin another package.

## Meaningful Stop Conditions

Stop for an ownership conflict, save version change, generic framework, broad
refactor, unapproved player-visible behavior, loss of atomicity, history used
as current state, resolved-thread reopening, weakened current-scene targeting,
or any other condition listed in `WORKFLOW.md`.
