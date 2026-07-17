# Sprint 10.65 - One Player-Safe Local Route Guidance Projection

Status: Ready for Independent Review.

Review state: Candidate prepared.

## Goal

Establish one bounded, deterministic, nonpersistent projection of immediate,
perceivable traversal options from the current player scene as natural local
route cues. Compass direction describes an immediate local route, never the
relative position of every known destination.

## Authorized Scope

- Preserve existing world topology and deterministic movement authority.
- Distinguish structural connectivity from player-facing route presentation.
- Project only immediate traversable connections relevant to the current scene.
- Permit one optional local orientation only when it helps express a local
  connection; do not present navigation as a raw compass grid.
- Use natural deterministic route cues, such as `Main Street continues south
  into town.`
- Keep the projection derived and nonpersistent.

## Boundaries

- Do not provide non-adjacent destination guidance.
- Do not add `go to the inn`, `find the blacksmith`, familiarity,
  destination-knowledge, pathfinding, multi-step routing, LLM intent parsing,
  global-coordinate, or complete-spatial-geometry behavior.
- Do not change structural topology except as minimally required to demonstrate
  this local-route seam.
- Do not alter movement authority, persistence, save compatibility, save
  version, provider behavior, or unrelated player-facing behavior.
- `next_sprint` remains `null`; this staging does not authorize another
  capability package.

## Completion

The implementation derives deterministic, player-safe natural-language route
cues solely from immediate traversable connections of the current scene. It
keeps connectivity authoritative in the simulation, introduces no persistent
route state, exposes no nonlocal destination relationship, and passes focused
projection and affected movement, scene, save/load, and provider-safe
regressions. No live provider request occurred. The candidate is ready for
independent review; `next_sprint` remains `null` and save version remains `1`.
