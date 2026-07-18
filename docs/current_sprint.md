# Sprint 10.70 - One Hop-Count-Agnostic Unambiguous Local Destination Route Resolver

Status: Ready for Independent Review.

Sprint 10.70 is implemented and ready for independent review; `next_sprint`
is `null`.

## Goal

Replace fixed-depth abstract route resolution with one deterministic,
hop-count-agnostic, transient authored-route resolver.

## Expected Files

- `engine/interaction_kernel.py`
- `engine/game_engine.py`
- `test_interaction_kernel.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- Exactly one eligible simple authored route, including routes longer than
  three hops, is prevalidated and then composed through existing hop semantics.
- Zero or multiple routes fail without state mutation; cycles terminate.
- Immediate, two-hop, and three-hop observable behavior remains compatible.
- Save version remains `1`; route data is not persistent.

## Verification

Focused long-route, ambiguity, cycle, preservation, save/load, and no-state
tests plus affected movement, navigation, persistence, narration-context, and
provider-safe regressions pass. Preflight, canonical validation, diff checks,
and review-packet validation pass.
