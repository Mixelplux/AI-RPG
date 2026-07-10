# Sprint Log

## Sprint 7.2
- Integrated save/load commands into CLI.
- Verified deterministic persistence.
- Adopted permanent Definition of Done.
- Standardized sprint closeout workflow.

## Sprint 7.3
- Added public save and load operations to `GameEngine`.
- Routed CLI persistence commands through the engine facade.
- Preserved the existing save format and World State schema.
- Verified movement, save, load, restored location, and continued gameplay using the project virtual environment.

## Sprint 7.4
- Introduced `GameSession` as the owner of new, loaded, and reset session construction.
- Kept `GameEngine` as the gameplay-facing orchestration facade.
- Added a fresh-session reset command without changing save, load, movement, or interaction behavior.
- Verified new game, save, restart, load, continued gameplay, and reset through the documented manual flow.

## Sprint 8.1
- Added deterministic skill-check resolution with structured results.
- Routed skill checks through the `GameEngine` gameplay facade.
- Added the CLI command `check <name>` with deterministic result reporting.
- Preserved movement, interaction, save, load, and reset behavior.
- Verified the documented gameplay flow manually using the project virtual environment after Codex encountered a host execution restriction.


## Sprint 8.2
- Completed structured skill-check command routing through the existing gameplay command path.
- Updated `engine/interaction_kernel.py`, `engine/game_engine.py`, and `play_game.py`.
- Preserved deterministic Sprint 8.1 skill checks as the only resolver.
- Verified documented `.venv` gameplay flow manually.
- Confirmed facade-boundary checks and closeout consistency.

## Sprint 8.3
- Completed deterministic current-scene target resolution.
- Added `engine/target_resolver.py` and routed supported target references through the existing command path.
- Preserved `GameEngine` as the gameplay-facing facade.
- Verified documented `.venv` gameplay flow manually.
- Confirmed closeout, facade-boundary, resolver-status, and no-8.4 checks.

## Sprint 8.4
- Added deterministic resolution for known location names, identifiers, and derived aliases.
- Added structured resolved, unresolved, and ambiguous destination results without guessing.
- Routed explicit `head to <place>` and `go to <place>` commands through `GameEngine` while keeping the CLI independent of the lower-level resolver.
- Confirmed destination resolution identifies places without moving the player, computing routes, advancing time, or triggering travel events.
- Preserved scene targets, skill checks, directional movement, save, load, continued gameplay, and reset behavior.
- Verified the documented gameplay flow manually using the project virtual environment after Codex encountered a host execution restriction.

## Project Review and Simulation Design Summit
- Conducted post-Sprint-8 architecture and simulation review before defining Sprint 9.
- Confirmed the current architecture remains healthy and does not require major refactor before Phase 2.
- Established Phase 2 direction as World Evolution Foundations rather than combat or feature systems.
- Created `docs/simulation_model.md` as the conceptual counterpart to `docs/architecture.md`.
- Updated simulation principles to clarify truth, knowledge, AI responsibility, persistent world continuity, routine abstraction, uncertainty, affordances, and narrative depth.
- Recorded ADRs for simulation-owned truth, Phase 2 direction, and simulation-model governance.
- Sprint 9 remains undefined until the Phase 2.0 documentation baseline is accepted.

## Sprint 9.1 — World History Skeleton
- Status: Complete.
- Added durable `world_state.history` support for minimal world-history entries.
- Recorded successful player movement as a history event with event type, summary, location, and time when available.
- Exposed history through `GameEngine` and added a CLI `history` review command without letting `play_game.py` mutate history internals.
- Preserved history through the existing save/load path while keeping scene snapshots, perception, and narration as derived views.
- Preserved non-goals: no world evolution, pressures, rumors, actor knowledge, autonomous NPC behavior, combat, procedural quest generation, or broad refactor.
- Verified the documented `.venv` gameplay flow manually after Codex encountered host execution and save-directory permission restrictions.

## Sprint 9.2 - Time Advancement Operation
- Status: Complete.
- Added an explicit simulation-owned time advancement operation through `GameEngine`.
- Added the narrow CLI command `wait`, which advances durable elapsed time by one fixed hour.
- Recorded time advancement in `world_state.history` with event type, summary, location, previous time, and new time.
- Preserved advanced time and time-advancement history through save/load.
- Preserved movement-created history, history review, movement, skill-check routing, target resolution, destination resolution, and reset behavior.
- Confirmed destination resolution still identifies destinations without moving the player or advancing time.
- Preserved non-goals: no world evolution, pressures, pressure drift, rumors, actor knowledge, autonomous NPC behavior, schedules, travel duration, recovery, healing, decay, escalation, opportunity loss, combat, procedural quest generation, or destination travel execution.
- Verified the documented gameplay flow and `test_save_load.py` manually using the project virtual environment after Codex encountered host execution restrictions.

## Sprint 9.3 - Read-Only History Query
- Status: Complete.
- Added a read-only history query facade through `GameEngine`.
- Supported recent-count, event-type, and location-filtered history queries while preserving existing history-entry structure.
- Added narrow CLI review commands for recent, type-filtered, and location-filtered history.
- Added focused automated coverage in `test_history_query.py`.
- Preserved movement-created history, time-advancement history from `wait`, save/load history and time persistence, movement, skill-check routing, target resolution, destination resolution, and reset behavior.
- Confirmed destination resolution still identifies destinations without moving the player or advancing time.
- Preserved non-goals: no world evolution, pressures, pressure drift, rumors, actor knowledge, autonomous NPC behavior, schedules, travel duration, evidence detection, consequence selection, opportunity surfacing, procedural quests, combat, AI interpretation of history, campaign-history summarization, or generated facts from history queries.
- Verified `test_history_query.py`, `test_save_load.py`, and the documented gameplay flow manually using the project virtual environment after Codex encountered host execution restrictions.

## Sprint 9.4 - Bounded History Query Guardrails
- Status: Complete.
- Added a single safe default history query count.
- Routed `GameEngine.query_history(...)` through the safe default when no explicit count is provided.
- Routed plain CLI `history` through the bounded query path instead of dumping full durable history.
- Preserved explicit `history recent <count>` review and bounded event-type and location filters.
- Preserved read-only query behavior: history queries do not mutate history, advance time, create history entries, or trigger world evolution.
- Preserved save/load history and time persistence, movement-created history, and `wait` time-advancement history.
- Documented that durable history is not active memory and normal history access is bounded by default.
- Preserved non-goals: no world evolution, pressures, rumors, actor knowledge, autonomous NPC behavior, combat, history pruning, history summarization, semantic memory, embeddings, memory archive tiers, active memory management, AI interpretation of history, or passing full history into narration or simulation context.
- Verified `test_history_query.py`, `test_save_load.py`, and the documented gameplay flow manually using the project virtual environment after Codex encountered host execution restrictions.

## Sprint 9.5 - Stable History Entry Identity
- Status: Complete.
- Added stable engine-owned `history_id` values to newly recorded durable history entries.
- Preserved identifiers through save/load without regenerating them on load.
- Ensured new history after load receives a non-reused identifier.
- Returned identifiers through existing read-only history query results.
- Added a narrow read-only `GameEngine.get_history_entry_by_id(...)` lookup.
- Added a narrow CLI review path: `history id <history_id>`.
- Preserved bounded history query defaults from Sprint 9.4 and existing `history`, `history recent <count>`, `history type <event_type>`, and `history location <location_id>` commands.
- Preserved read-only history behavior: query and lookup do not mutate history, advance time, create history entries, or trigger world evolution.
- Updated documentation to clarify that history identifiers make accepted events referenceable, not interpreted.
- Codex supplemental verification passed with the bundled Python runtime: `test_history_query.py`, `test_save_load.py`, and a scripted CLI smoke test.
- Verified the documented gameplay flow, `test_save_load.py`, and `test_history_query.py` manually using the project virtual environment after Codex encountered a runtime access restriction launching `.\.venv\Scripts\python.exe`.
- Runtime blocker resolved after closeout: Windows 11 App execution aliases for `python` / `Python 3` were interfering with Python resolution. Turning off the Python and Python 3 App execution aliases in Windows Settings allowed Codex to run official project verification through `.\.venv\Scripts\python.exe test_save_load.py`. Bundled Python should remain supplemental only unless the official `.venv` command is blocked and the `WORKFLOW.md` runtime-blocker rule is invoked.

## Sprint 9.6 - Bounded History Context Packet
- Status: Complete.
- Added a deterministic, read-only, bounded history context packet through `GameEngine.get_history_context(...)`.
- Added `engine/history_context.py` with a stable Sprint 9.6 packet shape, schema marker, version, default limit, maximum limit, current time, player location, and bounded accepted history entries.
- Preserved stable `history_id` values and existing history-entry fields without interpretation, summarization, relevance scoring, AI narration, or world evolution.
- Added CLI review commands `history context` and `history context <count>`.
- Preserved existing history commands: `history`, `history recent <count>`, `history type <event_type>`, `history location <location_id>`, and `history id <history_id>`.
- Added `test_history_context.py` covering default bounded packets, explicit counts, maximum-count validation, copy safety, no history/time mutation, save/load behavior, and CLI parser support.
- Updated architecture documentation with the bounded history context packet contract.
- Added ADR-026: Future Consumers Receive Bounded History Context Packets.
- Verified with the official project virtual environment: `test_history_context.py`, `test_history_query.py`, `test_save_load.py`, JSON manifest validation, and a scripted CLI smoke flow invoking `play_game.main()`.
- Bundled Python was not used for Sprint 9.6 verification.

## Sprint 9.7 - Narration Context Boundary
- Status: Complete.
- Added a deterministic, read-only narration context packet through `GameEngine.get_narration_context(...)`.
- Added `engine/narration_context.py` with schema/version metadata, raw player input, current time, current player location, current scene snapshot, bounded history context, and a narration drift guardrail.
- Added CLI review command `narration context <player input>`.
- Preserved bounded history context and stable `history_id` values inside narration context without interpretation, summarization, relevance scoring, AI narration, or world evolution.
- Documented the boundary between grounded facts and safe atmospheric description, including the blizzard/gloves example.
- Preserved non-goals: no AI narration, narration validator, equipment system, exposure mechanics, semantic history interpretation, history summarization, state mutation, or Sprint 9.8 work.
- Verified with the official project virtual environment: `test_narration_context.py`, `test_history_context.py`, `test_history_query.py`, `test_save_load.py`, JSON manifest validation, and a scripted CLI smoke flow invoking `play_game.main()`.
- Bundled Python was not used for Sprint 9.7 verification.
