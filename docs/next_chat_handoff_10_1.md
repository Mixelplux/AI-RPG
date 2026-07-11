# Sprint 10.1 Handoff

## Status

Sprint 10.1 is complete and closed out. Sprint 10.2 has not been defined or started.

## What Changed

- Implemented persistent resolved conversation memory as durable history.
- Conversation history now records resolved entity identity, current location, current durable time, and the existing engine-owned history ID.
- Failed, unresolved, ambiguous, and non-actor conversation targets do not create history.

## Files Changed

- `engine/world_update.py`
- `test_interaction_history.py`
- `docs/architecture.md`
- `docs/decisions.md`
- `docs/roadmap.md`
- `docs/sprint_log.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`
- `docs/next_chat_handoff.md`

## Verification

Passed with the official project virtual environment:

- `.\.venv\Scripts\python.exe test_interaction_history.py`
- `.\.venv\Scripts\python.exe test_history_query.py`
- `.\.venv\Scripts\python.exe test_history_context.py`
- `.\.venv\Scripts\python.exe test_narration_context.py`
- `.\.venv\Scripts\python.exe test_save_load.py`
- `.\.venv\Scripts\python.exe test_narration_pipeline.py`
- `.\.venv\Scripts\python.exe -m json.tool docs/current_sprint.json`
- Parsed JSON/YAML deep comparison

The scripted smoke flow covered North Gate start, `talk to captain`, Captain Darvin Grey resolution, history display, `history type player_conversation`, repeated conversations with distinct history IDs, unresolved/ambiguous/non-actor no-history cases, save/load preservation, movement, wait, destination resolution, skill check, narration preview, reset, and quit.

The launch check rendered the opening scene and then reached the expected non-interactive `EOFError` in the terminal session. Bundled Python was not used for verification.

## ADR-035

Resolved conversations become durable accepted events only after the normal gameplay path accepts the command and current-scene target resolution identifies a resolved entity.

## Current Constraints

- Provider integration remains deferred.
- Persistent scoped pressures or unresolved threads are the likely next capability.
- Conversation does not advance time or grant narration authority.
- No new top-level world-state field was introduced.
- Save version remained unchanged.
