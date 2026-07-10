# Current Sprint

## Sprint 9.8 - Narration Output Contract

Status: Complete

## Goal

Define a deterministic, read-only contract for future narration output before any AI model is called.

The contract should specify what a narration response may contain, reject structured attempts to mutate world state or history, and document narration drift limits.

This prepares for AI-assisted narration while preserving the rule that the engine owns truth and narration owns presentation.

## Design Intent

Sprint 9.7 created the narration context boundary: what a future narrator may see.

Sprint 9.8 defines the other side of that boundary: what a future narrator may return.

This is not AI integration and not final narration generation. It is a schema and validation foundation so future narrator output is treated as presentational prose only, not simulation authority.

The design rule remains:

> The narrator can describe. The engine decides what is true.

Sprint 9.8 adds:

> Narration output may be shown later, but it is not accepted world truth.

## Expected Files

Likely created:

- `engine/narration_output.py`
- `test_narration_output.py`

Likely modified:

- `engine/game_engine.py`
- `play_game.py`
- `docs/architecture.md`
- `docs/decisions.md`
- `docs/sprint_log.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`
- `docs/next_chat_handoff.md`

Possibly modified:

- `engine/narration_context.py`
- `test_narration_context.py`

## Acceptance Criteria

- A narrow narration output contract exists in an engine module.
- The contract defines narration output as presentational prose only.
- The contract includes schema/version metadata.
- The contract requires narration text to be a string.
- The contract can accept a simple valid narration output object for future use.
- The contract rejects narration output that contains structured world-state mutations.
- The contract rejects narration output that contains structured history mutations.
- The contract rejects narration output that attempts to advance time.
- The contract rejects narration output that attempts to create quests, rumors, pressures, actor knowledge, NPC schedules, evidence, or consequences.
- The contract rejects narration output that attempts to add new entities, locations, exits, inventory, player conditions, or NPC relationship state.
- The contract does not attempt to fully prove whether freeform prose contains invented details.
- Documentation explicitly states that freeform narration drift is controlled by context limits, prompt rules, output contract, and later review/validation layers, not by this sprint alone.
- Documentation includes an example: narration may describe a blizzard if the context contains a blizzard, but should not mention gloves unless gloves are present in context.
- GameEngine exposes a narrow method for validating or wrapping narration output without mutating world state.
- A narrow CLI/debug command is available for inspecting the narration output contract or validating a fixed sample output.
- Narration output validation does not mutate world state.
- Narration output validation does not advance time.
- Narration output validation does not create history entries.
- Narration output validation does not alter history identifiers.
- Narration output validation does not call an AI model.
- Existing narration context behavior still works.
- Existing history context behavior still works.
- Existing history query and history id behavior still work.
- Save/load behavior remains unchanged.
- Documentation explains that narration output is not accepted world truth.

## Verification

Run:

```powershell
.\.venv\Scripts\python.exe play_game.py
```

Run:

```powershell
.\.venv\Scripts\python.exe test_narration_output.py
```

Regression checks:

```powershell
.\.venv\Scripts\python.exe test_narration_context.py
.\.venv\Scripts\python.exe test_history_context.py
.\.venv\Scripts\python.exe test_history_query.py
.\.venv\Scripts\python.exe test_save_load.py
```

Validate JSON:

```powershell
.\.venv\Scripts\python.exe -m json.tool docs/current_sprint.json
```

Manual verification should confirm:

1. Start a new game with .\.venv\Scripts\python.exe play_game.py.
2. Create at least one movement history entry.
3. Use wait to create a time-advancement history entry.
4. Inspect narration context to confirm Sprint 9.7 behavior still works.
5. Inspect the narration output contract or run the fixed sample validation debug command.
6. Confirm valid prose-only narration output is accepted by the contract.
7. Confirm structured mutation attempts are rejected by the contract.
8. Confirm narration output validation does not advance time.
9. Confirm narration output validation does not create history entries.
10. Confirm normal history, history context, history id, and narration context commands still work.
11. Confirm normal gameplay still works after the debug command.

## Non-Goals

- Do not call an AI model.
- Do not generate final AI narration.
- Do not replace existing gameplay output with AI narration.
- Do not implement a full natural-language hallucination detector.
- Do not implement semantic prose analysis.
- Do not implement embeddings.
- Do not implement world evolution.
- Do not implement pressures or pressure drift.
- Do not implement rumors.
- Do not implement actor knowledge.
- Do not implement autonomous NPC behavior.
- Do not implement schedules.
- Do not implement evidence detection.
- Do not implement consequence selection.
- Do not implement opportunity surfacing.
- Do not implement procedural quests.
- Do not implement combat.
- Do not implement inventory, equipment, clothing, exposure, fatigue, or condition systems.
- Do not pass full durable history into narration output validation.
- Do not allow narration output to mutate world state.
- Do not allow narration output to create durable facts.
- Do not begin Sprint 9.9.

## Closeout

Sprint 9.8 is complete.

Official `.venv` verification passed.

Bundled Python was not used.

Sprint 9.9 has not started.

`docs/architecture.md` and `docs/decisions.md` record the narration output contract and ADR-028.

`docs/sprint_log.md`, `docs/current_sprint.yaml`, `docs/current_sprint.json`, and `docs/next_chat_handoff.md` were updated to reflect completion.
