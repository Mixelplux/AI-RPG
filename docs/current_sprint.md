# Sprint 10.62 - Derived Player-Safe Contextual Action Projection

Status: Ready for independent review.

Review state: Independent review pending.

`next_sprint` remains `null`.

## Goal

Project the fixed set of currently legitimate player actions into natural,
player-safe scene presentation without adding simulation authority or changing
the established command and resolver paths.

## Expected Files

- `engine/action_eligibility.py`
- `engine/contextual_action_projection.py`
- `engine/game_engine.py`
- `engine/perception_builder.py`
- `engine/scene_narrator.py`
- `test_contextual_action_projection.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- Only the four authorized opportunity categories are projected, as safe
  natural-language text, in deterministic authored order.
- Existing investigation and clue-presentation eligibility predicates remain
  authoritative and are reused by the projection.
- The projection is non-mutating, nonpersistent, and reconstructed after
  save/load; save version remains `1`.
- Existing resolver validation still governs stale or invalid attempted actions.

## Verification

- Official-interpreter preflight and canonical-record validation passed.
- Focused contextual projection and affected movement, conversation,
  investigation, discovery, clue presentation, narration, and save/load tests
  passed.
- The full deterministic repository suite passed in bounded batches; commit,
  evidence, and package-review archive validation remain the review preparation.
