# Sprint 10.69 - One Unambiguous Three-Hop Local Destination Traversal

Status: Ready for Independent Review.

Sprint 10.69 is implemented and ready for independent review. `next_sprint`
is `null`; no following sprint or capability is authorized or staged.

## Goal

Resolve one uniquely eligible three-hop authored local route for `go to
<location>` and `move to <location>`, prevalidating every hop and preserving
canonical movement and persistence behavior.

## Expected Files

- `engine/interaction_kernel.py`
- `engine/game_engine.py`
- `test_interaction_kernel.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- `go to D` and `move to D` traverse A -> B -> C -> D only when there is
  exactly one eligible three-hop route.
- The entire route validates before any mutation; zero or multiple routes
  leave world state and history unchanged.
- Existing immediate and two-hop traversal results remain unchanged.
- Route resolution remains transient, derived, bounded to three hops, and
  deterministic for cycles and unrelated connections.
- Save/load preserves canonical location at save version `1`, without new
  persistent state, migration, or parser behavior.

## Verification

- Official-interpreter preflight, syntax checks, canonical-record validation,
  and `git diff --check` pass.
- Focused tests cover unique success, complete-route prevalidation, zero and
  ambiguous failures without movement, immediate and two-hop preservation,
  bounded cycles/unrelated connections, save/load, and transient route data.
- Affected interaction-kernel, timed movement, navigation, save/load,
  narration-context, and provider-safe regressions pass without live provider
  requests. The committed candidate and review packet validate.
