# Deterministic Local Investigation and Evidence Discovery

Status: Complete.

## Purpose and Owner-Visible Value

This package creates the first complete deliberate discovery loop from hidden
simulation truth to durable player knowledge:

```text
world event -> hidden evidence trace -> player investigation -> durable discovery
```

The player can investigate the current location, discover at most one authored
clue supported by an existing trace, and retain that discovery through
save/load. Region Packs own immutable discovery policy and exact player-facing
observation prose; World State owns mutable truth and discovery membership.

## Architecture Direction and Compatibility

- Evidence traces remain hidden simulation records and keep their existing
  schema.
- Player discoveries are separate sparse persistent membership state; history
  records accepted transitions without replacing current state.
- Scene Snapshots and perception remain derived. Discovery does not enter
  ordinary perception, narration, or scene data.
- Candidate World State preparation, validation, and one final commit preserve
  atomicity. Inspection APIs return defensive copies and duplicate material
  operations are successful no-ops where appropriate.
- Save version remains `1`; compatibility uses the established narrow
  candidate-load normalization pattern only when needed.

## Accepted Internal Milestones

1. Sprint 10.25 — fail-closed narration-history projection.
2. Sprint 10.26 — narrow resolved-conversation consequence extraction.
3. Sprint 10.27 — Region Pack discovery declarations and authored discovery
   text.
4. Sprint 10.28 — sparse persistent player-discovery representation.
5. Sprint 10.29 — atomic local discovery transition and durable history.
6. Sprint 10.30 — deterministic investigation command, full verification, and
   final package review.

## Boundaries and Exclusions

The package does not add evidence interpretation, clue combination,
reliability, certainty, suspicion, belief, truth scores, actor reactions,
actor-knowledge propagation, unresolved-thread resolution, quests,
objectives, markers, journals, evidence inventory, trace movement/removal/
destruction/aging/decay, automatic or remote discovery, multiple discoveries
per action, random checks, attributes, skills, proficiency, travel, combat,
schedules, factions, economy, live AI, provider integration, save version `2`,
trace-schema provenance fields, or unrelated refactors.

Raw trace IDs, evidence IDs, lifecycle metadata, and causal identifiers must
never be exposed to the player. Only traces with valid authored discovery
declarations may be discoverable. Movement, scene entry, ordinary perception,
narration, and conversation never automatically discover evidence.

## Verification and Meaningful Stop Conditions

Each milestone requires focused tests, affected regressions, canonical manifest
agreement, and `git diff --check` before its checkpoint. Package closeout adds
the full required verification cycle, a player-facing investigation playtest,
and a capability-package review packet.

Stop for conflicting authority; a new ownership or persistence model; a save
version change; unapproved player-visible behavior; a generic framework or
broad refactor; discovery requiring interpretation, belief, or reliability;
trace-schema changes; evidence entering snapshots, ordinary perception, or
narration; inability to atomically commit discovery and history; material
narration behavior change from the fail-closed projection; Region Pack prose
ownership conflict; need for a broad player-knowledge model; material
repository ambiguity; irreversible risk; or unresolved required verification
outside safe scope.

## Git, Checkpoints, and Owner Review

Feature branch: `feature/deterministic-evidence-discovery`.

Each completed milestone receives one focused checkpoint commit after its
required verification. Do not merge, rebase, force-push, or begin another
capability package. The package is recoverable by reverting its feature-branch
commits.

Routine in-scope milestone progression needs no owner interruption. A final
capability-package review records the smallest complete evidence packet and
returns one owner decision request: accept, reject, defer, or request deeper
review of this package.

## Closeout Reconciliation

Checkpoint d61f884 implemented the approved outcomes of Sprints 10.27 through
10.30 together rather than creating a checkpoint per internal milestone. The
work remained within this approved package and introduced no new owner-level
architecture boundary. This record does not fabricate separate commits. Future
packages retain one focused checkpoint per milestone.
