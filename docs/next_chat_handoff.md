# Next Chat Handoff: Sprint 10.6 Staged

## Source State

- Project: AI Narrative RPG Engine
- Source branch: `main`
- Source commit: `eda236ac74eba329411fb728921d0bcdb292fd09`
- Sprint 10.5 is complete, closed out, committed, and the architecture-review packet records a clean repository.
- ADR-039 is accepted.
- The post-Sprint 10.5 architecture recommendation was explicitly accepted.

## Current Sprint

- Sprint 10.6 - Read-Only Applicable Pressures for One Location
- Status: planned and staged for implementation
- Exactly one sprint is defined.
- Implementation has not begun during the staging pass.
- Sprint 10.7 is not defined.

## Accepted Capability

Add one canonical read-only operation, preferably:

```python
GameEngine.get_applicable_pressures(location_id=None)
```

An omitted location uses the player's current durable location. An explicit location must be a non-empty string exactly matching a Region Pack `location_id` and must not move the player.

The result includes every exact region-scoped pressure and every exact requested-location-scoped pressure, including valid level `0` records. It excludes other-location pressures, uses deterministic ordering, and returns defensive copies.

Applicability means exact scope membership only. It does not imply activity, visibility, perceptibility, importance, narrative relevance, or escalation eligibility.

## Ownership

- `engine/pressure_state.py`: pure validation, exact scope filtering, deterministic ordering, defensive results.
- `engine/game_engine.py`: default-location resolution, explicit Region Pack location validation, and public facade.
- No scene, perception, narration, event, movement, or command code may reimplement scope filtering.

## Required Preservation

The operation creates no history, advances no time, moves no player, rebuilds or replaces no scene, changes no pressure, mutates no Region Pack data, adds no persistence field, and preserves save version `1`.

Existing `get_pressures()`, `get_pressure()`, pressure mutation, conversation consequence, and causal-history contracts remain unchanged.

## Planned ADR

ADR-040 - Pressure Applicability Is a Pure Scope-Aware Read Boundary

The ADR is proposed during implementation and should be accepted only during verified closeout.

## Next Action

Perform the separate bounded implementation pass required by `WORKFLOW.md`:

1. Confirm live branch, HEAD, and Git status.
2. Confirm the four canonical Sprint 10.6 files were promoted and deeply agree.
3. Perform Startup Review against the live repository.
4. Implement only the pure pressure applicability helper and GameEngine facade.
5. Add focused `test_pressure_applicability.py` coverage and bounded save/load regression coverage.
6. Run all official environment, focused, regression, manifest, launch/smoke, and diff checks through `.\.venv\Scripts\python.exe` only.
7. Do not close out or commit unless separately authorized by the workflow and user instruction.
8. Do not define Sprint 10.7.
