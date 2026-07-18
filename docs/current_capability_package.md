# Sprint 10.69 - One Unambiguous Three-Hop Local Destination Traversal

Status: Ready for Independent Review.

Sprint 10.69 is implemented and ready for independent review. `next_sprint`
is `null`; no following sprint or capability is authorized or staged.

## Goal

From A, resolve `go to D` or `move to D` only through exactly one eligible
authored local route A -> B -> C -> D, validating every hop before movement
and ending canonically at D.

## Authorized Scope

- Resolve only routes containing exactly two intermediate locations and three
  eligible immediate movement hops.
- Reuse the existing canonical immediate movement semantics for every hop.
- Keep direct and two-hop traversal behavior unchanged.
- Keep route resolution derived, transient, deterministic, and bounded to
  three hops.
- Preserve save version `1` and existing persistence architecture.

## Boundaries

- No arbitrary-length pathfinding, configurable depth, ranking, tie-breaking,
  shortest-path selection, generic pathfinding framework, persistent route
  state, migration, destination knowledge, dynamic routes, encounter system,
  parser expansion, or travel narration.
- Missing or ambiguous eligible three-hop routes fail with no movement.
- `next_sprint` remains `null`; provider requests are forbidden.

## Completion

Only one valid A -> B -> C -> D route moves the player, after complete-route
validation and through existing per-hop transitions. Direct and two-hop travel
remain unchanged; failures do not mutate state. Focused and affected
regressions, save/load compatibility, canonical validation, and review-packet
validation pass. The candidate remains unmerged pending independent review.
