# Sprint 10.72 - One Deterministic Mundane Multi-Route Local Destination Resolver

Status: Ready for Independent Review.

## Goal

Resolve one local mundane route from static authored topology by fewest hops,
then stable authored connection ordering.

## Expected Files

- `engine/interaction_kernel.py`
- `test_interaction_kernel.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- Multiple valid simple local routes select the fewest authored connections.
- Equal-hop routes select the stable first route induced by authored connection
  ordering; no player route choice is required.
- Directionality remains intact and route selection reads no hidden dynamic
  world-state condition.
- The selected ordered `movement_hops` remains transient and provisional until
  sequential authoritative traversal completes it; save version remains `1`.

## Verification

Focused shortest-route, stable tie-break, directionality, unreachable-route,
sequential traversal, save/load, narration-context, and provider-safe
regressions; official preflight; canonical record validation; `git diff
--check`; and a validated package-review packet.
