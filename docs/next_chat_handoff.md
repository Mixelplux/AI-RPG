# Next Chat Handoff: Sprint 10.5 Staging

## Current State

- Sprint 10.4 - Causally Referenced Pressure Transition is complete, closed out, and committed.
- The post-Sprint 10.4 architecture review is complete.
- The recommendation was explicitly accepted.
- Sprint 10.5 - One Declared Resolved-Conversation Pressure Consequence is defined for staging.
- Sprint 10.5 implementation has not started.
- Sprint 10.6 is undefined and has not started.

## Accepted Architecture Decision

The first automatic reactive-world path should be one strict Region Pack declaration connecting a successful conversation with one exact resolved entity to one exact pressure level.

Expected ADR:

**ADR-039 - One Region-Declared Resolved Conversation and Its Pressure Consequence Commit Atomically**

The declaration shape is:

```json
{
  "effect_id": "north_gate_captain_scrutiny",
  "target_entity_id": "captain_darvin_grey",
  "pressure_id": "bryn_shander_gate_scrutiny",
  "new_level": 25
}
```

The canonical Bryn Shander pack should seed `bryn_shander_gate_scrutiny` as a location-scoped `guard_attention` pressure at level 10. The existing winter pressure must not be used as the consequence of initiating a conversation.

## Critical Atomicity Boundary

For a matching material conversation:

```text
resolved conversation
    -> candidate player_conversation source entry
    -> candidate exact pressure mutation
    -> candidate linked pressure_changed consequence
    -> completed-state validation
    -> required candidate-scene construction
    -> one live world-state commit
```

The source event must precede the consequence in candidate history, but neither becomes durable until the full matched operation succeeds.

The existing public `GameEngine.set_pressure_level_from_event(...)` keeps its Sprint 10.4 contract requiring an already durable source. Reuse should occur through a non-committing internal candidate helper, not by chaining two public commits.

## Staging Pass

**Task type:** Setup/staging
**Recommended:** mini or lighter model with low reasoning

Promote:

- `current_sprint_10_5.md` -> `docs/current_sprint.md`
- `current_sprint_10_5.yaml` -> `docs/current_sprint.yaml`
- `current_sprint_10_5.json` -> `docs/current_sprint.json`
- `next_chat_handoff_10_5.md` -> `docs/next_chat_handoff.md`

During staging:

1. Confirm the repository is at the committed Sprint 10.4 source state.
2. Confirm the four temporary Sprint 10.5 files are present.
3. Confirm the three manifests materially agree before promotion.
4. Promote them into the canonical paths.
5. Parse canonical JSON and YAML with the official `.venv` interpreter and confirm exact deep agreement.
6. Confirm the Markdown canonical block exactly matches the machine manifests.
7. Validate `docs/current_sprint.json`.
8. Update `docs/roadmap.md` narrowly to record the accepted conversation-to-pressure consequence as the next Phase 2B capability.
9. Add a concise post-Sprint 10.4 architecture-review decision entry to `docs/sprint_log.md`.
10. Do not add ADR-039 during staging unless an existing repository convention explicitly requires planned ADR text before implementation. The expected default is to add and accept ADR-039 during successful closeout.
11. Confirm all four canonical files remain present.
12. Delete only the four temporary Sprint 10.5 staging files after successful promotion and validation.
13. Stop before implementation.

Do not modify application code or tests during staging.

## Implementation Boundary

**Task type:** Bounded implementation
**Recommended:** standard model with medium reasoning

Primary expected files:

- `engine/game_engine.py`
- `engine/world_update.py`
- `engine/region_validator.py`
- `data/regions/bryn_shander.json`
- `test_conversation_pressure_effect.py`
- `test_interaction_history.py`
- `test_save_load.py`

`engine/pressure_state.py` may change only to expose a concrete non-committing reuse seam. `engine/world_state.py`, Interaction Kernel, target resolution, save format, scene projection, perception, and narration should remain materially unchanged unless a focused acceptance requirement proves otherwise.

## Required Behavior

- Captain Darvin Grey conversation: source entry plus one linked material pressure consequence.
- Elin Voss conversation: existing source-only behavior.
- Repeated Captain conversation at level 25: new source entry, no consequence history, `changed: false`.
- Failed or unresolved conversation: no source and no consequence.
- Any matched preparation failure: no partial world-state or scene commit.
- Save/load: preserve result, do not replay effect, do not reuse history IDs.

## Verification

Run all commands recorded in the canonical Sprint 10.5 manifest through:

```powershell
.\.venv\Scripts\python.exe
```

Treat application failures and agent execution-context limitations according to `WORKFLOW.md`. Do not substitute another Python.

## Routing

- Setup/staging: mini or lighter, low reasoning.
- Bounded implementation: standard model, medium reasoning.
- Closeout documentation: mini or lighter, low reasoning.
- High reasoning: only for an architecture conflict or unclear focused failure.

## Stop Conditions

Staging must stop after promotion, narrow roadmap/sprint-log maintenance, validation, and cleanup.

Do not:

- Begin Sprint 10.5 implementation during staging.
- Add a generic effect framework.
- Add another event type or multiple effects.
- Add time progression, projection, narration coupling, unresolved threads, or AI mutation.
- Repair packet-generation workflow as part of this sprint.
- Define Sprint 10.6.
- Commit unless the repository owner explicitly requests it.
