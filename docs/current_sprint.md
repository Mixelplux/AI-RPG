# Sprint 10.63 - One-Time Consequence-Bearing Conversation Response

Status: Ready for independent review.

Review state: Candidate prepared.

`next_sprint` is `null`.

## Goal

Make the discovery-gated Elin patrol-dispatch response and its declared world
consequence occur exactly once, using canonical persistent state.

## Expected Files

- `data/regions/bryn_shander.json`
- `engine/player_discovery_response.py`
- `engine/conversation_affordance.py`
- `engine/game_engine.py`
- `engine/region_validator.py`
- `test_discovery_gated_relocated_actor_response.py`
- `test_discovery_gated_conversation_affordance.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- The special response remains unavailable before the qualifying discovery.
- The first eligible Elin conversation returns the authored response and
  applies one durable patrol-dispatch consequence.
- Later Elin conversations neither return the special response nor reapply
  the consequence, including after save/load.
- Other Elin and actor conversations retain their existing behavior; derived
  player-safe projection remains non-mutating and cue wording is unchanged.

## Verification

- Official-interpreter preflight through the established workspace procedure
  and canonical-record validation pass.
- Focused affected conversation, discovery, evidence, thread-resolution,
  relocation, travel, contextual-action, narration-preview, and save/load
  tests pass.
- `git diff --check`, a clean committed review candidate, and the required
  review-packet assembly and validation pass.
