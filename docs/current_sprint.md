# Sprint 10.71 - One Hop-Count-Agnostic Sequential Local Destination Traversal

Status: Ready for Independent Review.

## Goal

Execute each resolved local `movement_hops` entry through authoritative
movement completion before the next entry begins.

## Expected Files

- `engine/game_engine.py`
- `test_interaction_kernel.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- Every successful hop is validated, has its scene rebuilt, and is published
  before the next hop.
- A later hop failure does not roll back already completed hops.
- Existing timed West Road traversal and its consequences apply at its hop.
- One-, two-, and three-hop routes remain compatible; save version remains
  `1` and route hops are not persisted.

## Verification

Focused four-hop, timed-hop, later-failure, resolver, movement, navigation,
save/load, narration-context, and provider-safe regressions; official
preflight; canonical record validation; `git diff --check`; and a validated
package-review packet.
