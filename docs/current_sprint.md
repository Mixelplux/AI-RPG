# Sprint 10.68 - One Unambiguous Two-Hop Local Destination Traversal

Status: Ready for Independent Review.

Capability: Deterministic Abstract Local Destination Traversal.

Sprint 10.68 is implemented and ready for independent review. `next_sprint`
is `null`; no following sprint or capability is authorized or staged.

## Goal

Resolve only an unambiguous, eligible, two-hop authored local traversal for
`go to <location>` and `move to <location>`, reusing existing movement
semantics per hop and preserving canonical persistence.

## Expected Files

- `engine/interaction_kernel.py`
- `engine/game_engine.py`
- `test_interaction_kernel.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- From A, `go to C` and `move to C` move A -> B -> C only for exactly one
  eligible two-hop local route, ending at canonical location C.
- The complete route validates before any movement mutation; missing or
  ambiguous routes deterministically leave movement state unchanged.
- Direct and immediate movement behavior remains unchanged, and each accepted
  hop uses existing immediate movement semantics.
- Route resolution is bounded, derived, transient, cycle-safe, and does not
  consider unrelated connections beyond the two-hop candidate set.
- Save/load preserves the resulting canonical location without changing save
  version `1` or the persistence architecture.
- No general pathfinding, ranking, tie-breaking, command expansion, provider
  request, or excluded system is introduced; `next_sprint` remains `null`.

## Verification

- Official-interpreter preflight, syntax checks, canonical-record validation,
  and `git diff --check` pass.
- Focused tests cover successful `go to` and `move to` two-hop traversal,
  complete-route prevalidation, missing and ambiguous failures without
  movement, direct/immediate preservation, cycles/unrelated connections, and
  save/load persistence.
- Affected interaction-kernel, movement, navigation-projection, save/load,
  narration-context, and provider-safe regressions pass. No live provider
  request occurs.
- The bounded candidate is committed and review-packet validation passes;
  save version remains `1` and `next_sprint` remains `null`.
