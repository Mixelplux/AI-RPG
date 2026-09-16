# Sprint 10.76 - Deterministic Current-Scene Projection

This readable sprint record is explanatory. Lifecycle enforcement comes only
from `docs/current_sprint.json`.

## Status

Routine implementation is complete. The candidate awaits owner review and
separate merge authorization.

## Goal

Derive a deterministic, player-safe, read-only structured projection of the
current scene without changing simulation, persistence, narration, or command
behavior.

## Authorized Scope

- `engine/current_scene_projection.py` and `test_current_scene_projection.py`.
- Shared safe-exit derivation in `engine/navigation_projection.py`, preserving
  its existing navigation output.
- `GameEngine.get_current_scene_projection()` and lifecycle records.

## Exclusions

Narration/provider context, generated prose, command parsing, movement or
pathfinding, persistence or save schema, save version, Region Pack format,
perception shape, provider transport, and CLI output.

## Verification

Run focused current-scene projection, navigation, actor-location, movement, and
save/load regressions; validate lifecycle records; parse JSON and assert save
version `1`; run `git diff --check`; inspect changed scope; and confirm clean
candidate state. No merge, push, or evidence packet is authorized.
