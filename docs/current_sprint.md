# Sprint 10.76 - Deterministic Current-Scene Projection

This readable sprint record is explanatory. Lifecycle enforcement comes only
from `docs/current_sprint.json`.

## Status

Sprint 10.76 is complete and included in the accepted `main` baseline
`3b3606a2c31d92b6fba75a7ddf5d90d015304772`. Lifecycle JSON is idle:
no active sprint/package and no selected next sprint.

The owner-authorized proportional-engineering documentation maintenance is
standalone work while idle. It does not open or implement Sprint 10.77.

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

The completed package's verification scope was focused current-scene
projection, navigation, actor-location, movement, and
save/load regressions; validate lifecycle records; parse JSON and assert save
version `1`; run `git diff --check`; inspect changed scope; and confirm clean
candidate state. These historical requirements do not prescribe verification
for the current documentation maintenance; use `WORKFLOW.md` and its
authorized scope. No staging, commit, merge, push, or packet is authorized here.
