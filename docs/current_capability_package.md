# Sprint 10.67 - Immediate Local Travel Phrase Alignment

Status: Ready for Independent Review.

Review state: Candidate prepared.

## Goal

Remove the remaining local command inconsistency by allowing `go to <location>`
and `head to <location>` to use the existing local movement only when a named
location is uniquely and immediately traversable from the current scene.

## Authorized Scope

- For one uniquely matched immediate current-scene connection, resolve `go to`
  and `head to` through the same authoritative local movement used by a
  directional command and `move to <location>`.
- Keep existing structural topology, directional movement authority, local
  route projection, save compatibility, and save version `1` unchanged.
- Keep command handling deterministic, current-scene bounded, derived, and
  nonpersistent.
- Boundary: the interaction kernel owns classification and immediate-scene
  candidate resolution; the destination resolver remains the nonmoving
  loaded-region identification fallback when no immediate unique route matches.

## Boundaries

- A non-adjacent `go to` or `head to` retains the existing nonmoving
  destination-identification behavior; it must not become travel.
- Ambiguous or invalid targets fail closed without movement.
- Do not add nonlocal travel, pathfinding, multi-step routing, familiarity or
  destination knowledge, global coordinates, LLM intent parsing, persistence,
  migration, or a parser/navigation framework.
- `next_sprint` remains `null`; this staging does not authorize another
  capability package.

## Completion

The implementation moves the player only for an unambiguous immediate local
route named by `go to` or `head to`, with the same authoritative movement
result as its directional and `move to` forms. Non-adjacent phrases retain
nonmoving destination identification, while ambiguous and invalid phrases do
not move state. Focused phrase-alignment and affected movement, route,
save/load, narration-context, and provider-safe regressions pass. No live
provider request occurred. The candidate is ready for independent review;
`next_sprint` remains `null` and save version remains `1`.
