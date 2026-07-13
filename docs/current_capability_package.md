# Authored Resolved-Thread Observation and Integrity

Status: Complete.

## Purpose and Owner-Visible Value

After the player resolves the authored Bryn Shander thread, the world should
continue to show the exact authored local consequence whenever the player is
at an eligible declared location. This package makes that durable outcome
visible without turning it into a quest, dialogue branch, or generic
consequence system.

## Included Internal Milestones

1. Sprint 10.37 — Resolved-thread authoritative integrity — complete.
2. Sprint 10.38 — Derived authored resolved observation — complete.
3. Sprint 10.39 — Player-facing projection, verification, and package closeout — complete.

No following sprint is staged.

## Scope, Ownership, and Compatibility

- World State `resolved_threads` remains the sole authoritative current fact.
  Region Pack declarations and causal history are validation inputs at the
  authoritative transition, World State, and load-replacement boundaries.
- Region Packs retain ownership of the exact `resolved_observation` prose and
  the existing declared thread perception locations. No new location-policy
  field is introduced.
- Perception and narration project already-validated resolved state. They do
  not treat history as an independent runtime authority.
- A valid resolved observation remains visible on every eligible later visit
  and after save/load. “Exactly once” means no duplicate copy in one
  perception or narration result, not one-time lifetime consumption.
- Candidate validation, derived projection rebuilding, and one final live
  commit preserve the existing atomic transition boundary.
- Save version remains `1`. No persistent field, migration, or legacy
  normalization rule is added by this package.

## Exclusions

No generic consequence system, new persistent domain, new command, dialogue
branch, actor relocation, time-based behavior, generic thread framework,
quests, objectives, journal, inventory, actor AI, provider integration, or
save version `2` is included.

## Expected Files and Systems

- `engine/world_state.py`
- `engine/unresolved_threads.py`
- `engine/game_engine.py`
- `engine/perception_builder.py`
- `engine/scene_narrator.py`
- `engine/region_validator.py` only if needed to preserve the existing strict
  declaration contract
- focused discovery, unresolved-thread, save/load, and narration tests
- package, sprint, architecture, decision, roadmap, and sprint-log records as
  required by completed milestones

## Architecture Decisions and Stop Conditions

ADR-050 owns the resolved-thread state and authored observation boundary. No
new ADR was required: this package adds Region-aware causal integrity and a
derived projection using the established ownership boundary.

Stop for a required new persistence model, save-version change, generic
projection or consequence mechanism, history becoming a second source of
runtime authority, broad narration refactor, unapproved player-visible scope,
or any `WORKFLOW.md` stop condition.

## Verification, Completion, and Rollback

Focused integrity, perception, narration, and save/load tests passed, followed
by the full root test inventory through the official interpreter. Malformed
save and live-load atomicity coverage, the scripted player revisit and
save/load behavior, canonical manifest agreement, official preflight, and
`git diff --check` passed. The package review packet was assembled after
closeout verification.

The rollback boundary is this package’s feature-branch changes only. Reverting
them removes a derived observation and stricter validation without a schema
migration or save conversion. Package closeout does not choose or start a
following package.
