# Sprint 10.66 - Immediate Local Route Command Alignment

Status: Active.

Review state: Staged.

`next_sprint` is `null`. This is the active, owner-authorized capability
package; no following sprint is authorized or staged.

## Goal

For one immediate, named current-scene route, make `move to <adjacent
location>` resolve to the already authoritative directional movement result.

## Expected Files

- `engine/interaction_kernel.py`
- `test_interaction_kernel.py`
- `test_navigation_projection.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- At the current scene, `move to Main Street` succeeds only when Main Street
  names one immediately traversable connection and yields the same destination
  and movement behavior as the matching directional command.
- Resolution is deterministic and restricted to current-scene immediate exits;
  non-adjacent, unavailable, ambiguous, or unrecognized names do not move the
  player or expose a route beyond the scene.
- Existing structural connectivity and movement authority remain unchanged;
  the local name form reuses rather than duplicates movement resolution.
- `go to <destination>` and `head to <destination>` do not become travel
  commands in this sprint.
- No persistence, history, parser framework, provider behavior, migration, or
  save-version change is introduced. Save version remains `1` and
  `next_sprint` remains `null`.

## Verification

- Official-interpreter preflight, canonical-record validation, and `git diff
  --check` pass for staging.
- Focused command-alignment coverage proves immediate named-route success,
  directional equivalence, deterministic ambiguity handling, nonlocal refusal,
  no-state-change failure, and no broad `go to` travel behavior.
- Affected interaction-kernel, navigation-projection, movement, save/load,
  narration-context, and provider-safe regressions pass. No live provider
  request occurs.
