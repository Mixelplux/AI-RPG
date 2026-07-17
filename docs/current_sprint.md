# Sprint 10.64 - One Derived Player-Safe Elapsed-Time Transition Observation

Status: Ready for independent review.

Review state: Independent review pending.

`next_sprint` remains `null`.

## Goal

For one accepted one-hour `wait`, derive deterministic player-safe presentation
from authoritative command-start and completed player-visible state: communicate
that an hour passed and, when applicable, one material authored-actor presence
change such as a previously visible actor no longer being present.

## Expected Files

- `engine/game_engine.py`
- `engine/elapsed_time_transition_observation.py`
- `test_elapsed_time_transition_observation.py`
- `test_time_actor_relocation.py`
- `test_save_load.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- A successful accepted one-hour `wait` returns `An hour passes.`; a qualifying
  actor absence appends `{actor display name} is no longer at the {location
  name}.` Exact wording is deterministic and bounded to this transition.
- When one material authored actor was visible at wait start and is no longer
  present at the same player location after the accepted transition, the output
  includes only that actor's player-safe display name and current-location
  absence in fixed deterministic selection order.
- The observation derives only from command-start and completed player-visible
  scene state; it neither changes World State nor adds history, save data,
  narration context, or simulation authority.
- No hidden cause, trigger, history identifier, pressure, evidence, internal
  consequence identifier, or other simulation-only state is disclosed.
- No qualifying visible change produces no actor-change clause; travel and
  non-wait transitions remain outside this sprint. Save version remains `1` and
  `next_sprint` remains `null`.

## Verification

- Official-interpreter preflight, syntax checks, canonical-record validation,
  and `git diff --check` passed.
- Focused transition-observation coverage passed for baseline wording,
  qualifying actor absence, no qualifying change, deterministic selection,
  non-mutation, hidden-state non-disclosure, and save/load non-persistence.
- Time actor-relocation, time-pressure, time-evidence-trace, interaction-history,
  save/load, narration-context, narration-pipeline, and fake-transport OpenAI
  Responses regressions passed. No live provider request occurred.
