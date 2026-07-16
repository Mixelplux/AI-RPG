# Sprint 10.61 - Derived Player-Safe Navigation Projection

Status: Ready for independent review.

## Value and Scope

Make immediate, legitimate movement opportunities legible in scene narration by
deriving a player-safe navigation projection from the existing current-scene
exits and authored location data. The projection is nonpersistent and does not
change command interpretation, movement resolution, save format, provider
behavior, or Region Pack gameplay content.

## Boundaries

- Surface only directly connected exits in the current scene whose destination
  is authored and has a player-facing name.
- Use natural spatial language; do not show location identifiers, global map
  topology, hidden locations, or implementation data.
- Reuse the existing movement resolution and state-mutation path unchanged.
- Keep save version `1`, `next_sprint` `null`, and all provider/API requests
  forbidden.
- Do not begin contextual action surfacing, elapsed-time narration, parser
  expansion, travel redesign, or another capability.

## Completion

The derived projection, scene presentation, focused player-safety,
non-mutation, determinism, movement, and save/load coverage are complete.
Provider-safe regressions passed. The package is ready for independent review
on a committed, clean feature-branch candidate; `next_sprint` remains `null`.
