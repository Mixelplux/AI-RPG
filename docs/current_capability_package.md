# Sprint 10.64 - One Derived Player-Safe Elapsed-Time Transition Observation

Status: Planned.

Review state: Staged for bounded implementation.

## Goal

For the existing accepted one-hour `wait` transition, derive one deterministic,
nonpersistent, player-safe observation that says an hour passed and, when
applicable, names one material change in the presence of an authored actor
visible at the command start.

## Authorized Scope

- Operate only on the accepted one-hour `wait` transition and preserve its
  existing simulation-owned candidate-state transition.
- Compare only command-start and completed player-visible scene state to derive
  one presentation result after the transition has been accepted.
- Emit deterministic, bounded wording: `An hour passes.` followed, when
  applicable, by `{actor display name} is no longer at the {location name}.`
  for one visible actor's material absence from the current location.
- Keep the observation derived, non-mutating, nonpersistent, and reconstructible
  from the transition inputs; it must not become World State, history, save
  data, or narration context.
- Preserve existing actor-location authority, player-safe projection boundaries,
  save/load compatibility, and save version `1`.

## Boundaries

- Do not add a generic scene-diff, World State comparison, transition, or
  elapsed-time narration framework.
- Do not add persistent World State fields, history event types, observation
  history, parser or command changes, migrations, or save-version changes.
- Do not reveal cause, trigger, history identifier, pressure, evidence,
  internal consequence identifier, or other simulation-only information.
- Do not cover travel transitions, automatic investigation or discovery, later
  discovery/use presentation, AI/provider-generated prose, provider changes,
  or unrelated Sprint 10.60 findings.
- `next_sprint` remains `null`; no following package is authorized.

## Completion

The bounded implementation must prove deterministic one-hour wording, one
eligible visible-actor absence observation, no observation when no qualifying
visible change occurs, non-mutation and non-persistence, and affected wait,
actor-relocation, save/load, interaction, narration-preview, and provider-safe
regressions. A separately authorized review candidate is required after
implementation; staging alone does not authorize implementation or review.
