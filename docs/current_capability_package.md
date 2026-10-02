# Sprint 10.76 - Deterministic Current-Scene Projection

This is an explanatory package record. `docs/current_sprint.json` is the only
machine-enforced lifecycle authority.

## Status

Sprint 10.76 is complete and included in the accepted `main` baseline
`3b3606a2c31d92b6fba75a7ddf5d90d015304772`. Lifecycle JSON is idle;
no new capability package is selected or active.

Current owner-authorized work is standalone proportional-engineering
documentation/process maintenance. Its boundary is process guidance and
directly necessary lifecycle-validator textual consistency. Runtime/gameplay,
architecture changes, new tools, and Sprint 10.77 are excluded. Verification
is record validation, affected validator checks, contradiction searches, and
diff/scope review. Staging, commits, and merges are not authorized.

## Goal

Add one deterministic, read-only, player-safe structured current-scene
projection from the existing Region Pack, Scene Snapshot, and Perception
Snapshot boundaries.

## Authorized Scope

- Add `engine/current_scene_projection.py` and
  `test_current_scene_projection.py`.
- Add `GameEngine.get_current_scene_projection()`.
- Share safe structured exit filtering with `engine/navigation_projection.py`
  while keeping existing navigation output unchanged.
- Update current lifecycle records.

## Exclusions

Narration/provider context, generated prose, command parsing, movement or
pathfinding, persistence or save schema, save version, Region Pack format,
perception shape, provider transport, and CLI output.

## Acceptance Criteria

- The result contains only player-facing location text, visible static actor
  names, safely labeled spawned groups, and immediate safe exits.
- It is deterministic, non-mutating, fail-closed, fresh-copy safe, and
  nonpersistent. No internal identifier is exposed or used as display text.
- The existing navigation result remains unchanged, and save version remains
  `1`.

## Required Verification

The completed Sprint 10.76 verification scope was focused projection,
navigation, actor-location, movement, and save/load
regressions; lifecycle validation; official-interpreter JSON parsing with
save-version assertion; `git diff --check`; changed-scope inspection; and
clean candidate evidence. It is historical scope, not the verification burden
for this maintenance task. No push or evidence packet is authorized here.
