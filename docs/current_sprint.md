# Current Sprint

## Sprint 9.7 - Narration Context Boundary

Status: Complete

## Goal

Create a deterministic, read-only narration context packet that combines player input, current scene state, current time, player location, and bounded history context for future AI-assisted narration.

The packet must define what a future narrator is allowed to see without allowing narration to mutate world state, create history, advance time, summarize history, interpret events, or call an AI model.

## Design Intent

Sprint 9.1 made world history durable. Sprint 9.2 made time advancement explicit. Sprint 9.3 made history queryable. Sprint 9.4 made normal history queries bounded by default. Sprint 9.5 made individual accepted history events safely referenceable with stable identifiers. Sprint 9.6 created a bounded history context packet.

Sprint 9.7 introduces the first safe consumer-facing boundary for that context: a narration context packet.

This is not the narrator, not AI integration, and not world evolution. It is the deterministic input contract that future narration may use.

The rule for this sprint is:

> The narrator can describe. The engine decides what is true.

Narration context may support atmospheric prose, but future narration must not invent unstated specifics. The narrator may describe sensory conditions grounded in known scene facts, but must not invent player equipment, clothing, memories, emotions, physical conditions, owned items, NPC attitudes, relationships, hidden observers, threats, clues, exits, or durable world facts unless those details are present in the narration context.

Sprint 9.7 only defines what future narration may see.

## Expected Files

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

Likely created:

- `engine/narration_context.py`
- `test_narration_context.py`

Possibly modified:

- `engine/history_context.py`
- `test_history_context.py`
- `test_history_query.py`
- `test_save_load.py`

## Acceptance Criteria

- A deterministic narration context builder exists in a narrow engine module.
- GameEngine exposes a read-only narration context method, such as get_narration_context(...).
- The narration context packet includes schema/version metadata.
- The narration context packet includes the raw player input provided for narration context construction.
- The narration context packet includes current player location.
- The narration context packet includes current world time.
- The narration context packet includes the current scene or scene snapshot needed for narration.
- The narration context packet includes a bounded history context packet from Sprint 9.6.
- History entries inside the narration context include stable history_id values.
- Narration context construction is deterministic for the same world state and same player input.
- Narration context construction returns read-only copies and cannot mutate durable world state.
- Narration context construction does not advance time.
- Narration context construction does not create history entries.
- Narration context construction does not alter history identifiers.
- Narration context construction does not trigger world evolution.
- Narration context construction does not summarize, reinterpret, rank, or semantically analyze history entries.
- Narration context construction does not call an AI model or introduce AI-generated narration.
- A narrow CLI/debug command is available for inspecting narration context.
- Existing gameplay commands still work.
- Existing history context CLI commands still work.
- Existing history id lookup still works.
- Save/load behavior remains unchanged.
- Documentation explains that narration context is an input boundary, not narration output and not simulation authority.
- Documentation distinguishes grounded facts from safe atmospheric description.
- Documentation states that future narration must not make atmospheric prose durable world truth.
- Documentation includes an example: if the scene contains a blizzard, narration may describe cold weather, but may not mention the player's gloves unless gloves are present in player state or context.
- Narration context remains an input boundary only.
- No AI narration, narration validator, equipment system, or exposure mechanics are implemented in Sprint 9.7.

## Verification

Run:

```powershell
.\.venv\Scripts\python.exe play_game.py
```

Run:

```powershell
.\.venv\Scripts\python.exe test_narration_context.py
```

Regression checks:

```powershell
.\.venv\Scripts\python.exe test_history_context.py
.\.venv\Scripts\python.exe test_history_query.py
.\.venv\Scripts\python.exe test_save_load.py
```

Manual verification should confirm:

1. Start a new game with .\.venv\Scripts\python.exe play_game.py.
2. Create at least one movement history entry.
3. Use wait to create a time-advancement history entry.
4. Run the narration context debug command with a sample player input.
5. Confirm the packet includes schema/version metadata.
6. Confirm the packet includes the supplied player input.
7. Confirm the packet includes current player location and current world time.
8. Confirm the packet includes current scene context.
9. Confirm the packet includes bounded history context with stable history_id values.
10. Confirm repeated narration context inspection does not advance time.
11. Confirm repeated narration context inspection does not create history entries.
12. Confirm normal history, history context, and history id commands still work.
13. Confirm normal gameplay still works after the debug command.

## Non-Goals

- Do not implement AI model integration.
- Do not generate final AI narration.
- Do not implement a narration validator.
- Do not replace existing command output with narration output.
- Do not implement an equipment system.
- Do not implement exposure mechanics.
- Do not implement world evolution.
- Do not implement pressures.
- Do not implement pressure drift.
- Do not implement rumors.
- Do not implement actor knowledge.
- Do not implement autonomous NPC behavior.
- Do not implement schedules.
- Do not implement evidence detection.
- Do not implement consequence selection.
- Do not implement opportunity surfacing.
- Do not implement procedural quests.
- Do not implement combat.
- Do not implement semantic memory.
- Do not implement embeddings.
- Do not implement history summarization.
- Do not implement history pruning.
- Do not pass full durable history into narration context.
- Do not allow narration context construction to mutate world state.
- Do not allow narration to assign, alter, or reinterpret history identifiers.
- Do not begin Sprint 9.8.

## Closeout Instructions

Sprint 9.7 is complete.

Official `.venv` verification passed:

```powershell
.\.venv\Scripts\python.exe test_narration_context.py
.\.venv\Scripts\python.exe test_history_context.py
.\.venv\Scripts\python.exe test_history_query.py
.\.venv\Scripts\python.exe test_save_load.py
.\.venv\Scripts\python.exe -m json.tool docs/current_sprint.json
```

The primary CLI flow was verified with the official `.venv` using a scripted `play_game.main()` smoke flow covering movement, wait, history, history context, history id lookup, narration context inspection, and quit.

Bundled Python was not used for Sprint 9.7 verification.

Sprint 9.8 has not started.
