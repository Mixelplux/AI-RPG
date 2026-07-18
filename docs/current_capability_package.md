# Sprint 10.66 - Immediate Local Route Command Alignment

Status: Ready for Independent Review.

Review state: Candidate prepared.

## Goal

Align deterministic local movement commands with the immediate named route
options already projected from the current scene. A command such as `move to
Main Street` resolves only to that existing immediate connection and executes
the same movement as its corresponding directional command.

## Authorized Scope

- Resolve a named adjacent location only when it is an immediately traversable
  connection in the current player scene.
- Route successful local name resolution through the existing authoritative
  movement path, producing the same destination and movement behavior as the
  corresponding directional command.
- Preserve structural topology, deterministic movement authority, player-safe
  route projection, save compatibility, and save version `1`.
- Keep command interpretation deterministic, bounded, derived from current
  scene connectivity, and nonpersistent.

## Boundaries

- Do not provide non-adjacent destination guidance, familiarity or knowledge,
  pathfinding, multi-step routing, global coordinates, or LLM intent parsing.
- Do not generalize `go to <destination>` into travel; it remains deferred
  unless a separately staged architecture review proves unification necessary
  and bounded.
- Do not add a navigation framework, alter topology, add persistence or
  migration, change save version, or change unrelated command behavior.
- `next_sprint` remains `null`; this staging does not authorize another
  capability package.

## Completion

The implementation accepts an unambiguous named immediate local route through
the bounded `move to <adjacent location>` form, executes the same authoritative
movement as the matching directional command, and rejects nonlocal or
unavailable names without state change. Focused command-alignment and affected
movement, route-projection, save/load, narration-context, and provider-safe
regressions passed. No live provider request occurred. The candidate is ready
for independent review; `next_sprint` remains `null` and save version remains
`1`.
