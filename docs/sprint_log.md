# Sprint Log

## Sprint 10.2 Planning and Staging

- Status: Defined and staged; implementation not started.
- Selected capability: Persistent Scoped Pressure Representation.
- Architecture review: Complete; pressure representation was selected over unresolved-thread representation or a combined generic abstraction.
- Ownership decision: current pressure state belongs in `world_state`; Region Packs provide immutable new-game seeds only.
- Persistence decision: loaded games retain persisted pressure state; legacy saves without pressures normalize to an empty collection and are not retroactively seeded.
- Boundary: representation, validation, persistence, and read-only copy-safe inspection only.
- Contract clarification: Region Pack seeds use the exact optional top-level `initial_pressures` list, and Region Pack provenance must match the containing `region_id`.
- Facade clarification: exact methods are `GameEngine.get_pressures()` and `GameEngine.get_pressure(pressure_id)`, with defensive deep copies and `None` for unknown IDs.
- CLI clarification: `pressures` is required and routes only through `GameEngine.get_pressures()`.
- Legacy clarification: canonical runtime state requires `pressures`; copied version-1 legacy saves missing the field normalize to empty during loading only, while malformed present values fail validation.
- Added ADR-036: Scoped Pressures Are Persistent Current State.
- Canonical Sprint 10.2 Markdown, YAML, JSON, and handoff files staged and synchronized.
- Application code and tests were not modified; implementation verification was not run.
- Sprint 10.3 was not defined or started.

## Sprint 10.1 Closeout
- Status: Complete.
- Files created: `test_interaction_history.py`.
- Files modified: `engine/world_update.py`.
- Implemented behavior: successful conversation commands now create one durable `player_conversation` history entry only when current-scene target resolution identifies a resolved entity.
- Resolved-entity requirement: stable target identity comes from deterministic target resolution, not raw player text.
- Durable fields recorded: deterministic summary, current location, current durable time, `target_entity_id`, `target_display_name`, and the existing engine-owned `history_id`.
- No-history failure cases: failed, unresolved, ambiguous, and non-actor conversation targets do not create history.
- Save/load preservation: conversation history and identifiers survive save/load without reuse or regeneration.
- No time advancement: conversation does not move the player, advance time, or mutate unrelated world state.
- No new top-level world-state field: none was added.
- Save version unchanged: confirmed.
- Verification passed with the official project virtual environment: `test_interaction_history.py`, `test_history_query.py`, `test_history_context.py`, `test_narration_context.py`, `test_save_load.py`, `test_narration_pipeline.py`, and `-m json.tool docs/current_sprint.json`.
- Parsed JSON/YAML deep comparison passed.
- Scripted smoke result: covered North Gate start, `talk to captain`, Captain Darvin Grey resolution, history display, `history type player_conversation`, repeated conversations with distinct history IDs, unresolved/ambiguous/non-actor no-history cases, save/load preservation, movement, wait, destination resolution, skill check, narration preview, reset, and quit.
- Non-interactive launch note: `play_game.py` rendered the opening scene and then reached the expected `EOFError` in the non-interactive terminal session.
- Bundled Python status: not used for verification.
- Pressure work and Sprint 10.2 were not started.

## Sprint 10.1 Setup and Review-Record Maintenance
- Status: Complete.
- Promoted the Sprint 10.1 planning package into the canonical sprint and handoff files under `docs/`.
- Confirmed the playable vertical-slice review result: movement and waiting are remembered, but resolved conversations are not yet durable history.
- Recorded the decision to begin Phase 2B with persistent resolved conversation memory before persistent scoped pressures.
- Updated the roadmap to reflect Sprint 9 completion, the post-Sprint-9 architecture review, the playable vertical-slice review, and the deferred provider integration stance.
- Confirmed Sprint 10.1 is defined but implementation has not started.
- No application code was changed.

## Post-Sprint-9 Architecture Review
- Status: Complete.
- Reviewed the canonical architecture, decisions, roadmap, simulation model, simulation principles, Sprint 9 documentation, implemented history/time/narration modules, gameplay facade, persistence path, command routing, Region Pack, and focused tests.
- Determined that Sprint 9 is complete and that no Sprint 9.14 is required.
- Named the completed milestone **World Memory and Safe Narration Foundations**.
- Confirmed that `world_state`, save/load ownership, `GameSession`, and the `GameEngine` facade remain coherent and do not require a major refactor.
- Confirmed that the narration preview boundary is sufficiently fail-closed for its current deterministic source and should stop expanding until an immediate bounded consumer exists.
- Deferred real AI provider integration because it is not required for simulation-owned world evolution.
- Confirmed that World Evolution Foundations remain incomplete: pressures or threads, pressure change, drift, runtime actor state, actor knowledge, evidence, consequences, schedules, affordances, opportunity surfacing, and travel execution remain unimplemented.
- Selected a focused playable vertical-slice review as the next project-level activity.
- Proposed **Phase 2B - Reactive World State Foundations** as the next implementation milestone after that review, with persistent scoped pressures or unresolved threads as the leading candidate rather than a committed sprint.
- Added ADR-034 to record the phase-completion and transition decision.
- No application code was changed, no sprint manifests were staged, and no following sprint was defined or started.

## Sprint 9.12 - Deterministic Narration Prompt Packet Contract
- Status: Complete.
- Implemented `engine/narration_prompt.py` and `test_narration_prompt.py` for the deterministic, copy-safe, provider-neutral narration prompt packet contract.
- Updated `engine/narration_source.py` and `engine/narration_pipeline.py` so preview flow now sequences narration context, narration request, narration prompt, fixed source, and narration-output validation before display.
- Preserved the fixed sample prose: `The street remains quiet.`
- Preserved fail-closed behavior for prompt construction, prompt validation, source exceptions, malformed source results, and invalid candidates.
- Preserved state isolation: no world-state mutation, no time advancement, no history creation, no scene-state mutation, no history-identifier mutation, and no narration-artifact persistence.
- Files created: `engine/narration_prompt.py`, `test_narration_prompt.py`.
- Files modified: `engine/narration_source.py`, `engine/narration_pipeline.py`, `test_narration_source.py`, `test_narration_pipeline.py`.
- Verification passed with the official project virtual environment: `test_narration_prompt.py`, `test_narration_request.py`, `test_narration_source.py`, `test_narration_pipeline.py`, `test_narration_output.py`, `test_narration_context.py`, `test_history_context.py`, `test_history_query.py`, `test_save_load.py`, and `-m json.tool docs/current_sprint.json`.
- Launch check rendered the opening scene and then hit expected `EOFError` in the non-interactive session.
- Scripted `play_game.main()` smoke passed through narration context, narration output, repeated narration preview, and quit.
- Bundled Python was not used.
- Sprint 9.13 was not started.

## Sprint 9.13 - Strict Narration Source Result Validation Contract
- Status: Complete.
- Implemented `validate_narration_source_result_packet(...)` and tightened the narration preview pipeline so source results are validated immediately after source invocation.
- Enforced the exact source-result schema, version, source identity, top-level fields, matched prompt, object-shaped candidate, and exact metadata contract.
- Preserved the fixed sample prose: `The street remains quiet.`
- Preserved fail-closed behavior with `source_result_validation` for malformed source-result envelopes, bounded diagnostics, empty display text, empty candidate, and empty source-result inspection data.
- Preserved the separate `candidate_validation` stage for invalid candidate prose.
- Preserved state isolation: no world-state mutation, no time advancement, no history creation, no scene-state mutation, no history-identifier mutation, and no narration-artifact persistence.
- Files created: None.
- Files modified: `engine/narration_source.py`, `engine/narration_pipeline.py`, `test_narration_source.py`, `test_narration_pipeline.py`.
- Verification passed with the official project virtual environment: `test_narration_source.py`, `test_narration_pipeline.py`, `test_narration_prompt.py`, `test_narration_request.py`, `test_narration_output.py`, `test_narration_context.py`, `test_history_context.py`, `test_history_query.py`, `test_save_load.py`, `-m json.tool docs/current_sprint.json`, parsed YAML/JSON deep comparison, and a scripted `play_game.main()` smoke flow through `narration preview look around` and quit.
- Launch check rendered the opening scene and then hit expected `EOFError` in the non-interactive session.
- Bundled Python was not used.
- Sprint 9.13 was closed out after verification, and no following sprint was started.

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

## Sprint 9.8 - Narration Output Contract
- Status: Complete.
- Added `engine/narration_output.py` with a deterministic, read-only narration output contract.
- Added `GameEngine.get_narration_output_contract()` and `GameEngine.validate_narration_output(...)`.
- Added CLI/debug commands `narration output` and `narration output invalid`.
- Added `test_narration_output.py` covering prose-only acceptance, structured mutation rejection, copy safety, and no world-state mutation.
- Preserved narration context behavior, history context behavior, history query behavior, history id lookup, save/load behavior, and gameplay flow.
- Documented that narration output is presentational only and is not accepted world truth.
- Verified with the official project virtual environment: `test_narration_output.py`, `test_narration_context.py`, `test_history_context.py`, `test_history_query.py`, `test_save_load.py`, `-m json.tool docs/current_sprint.json`, `play_game.py` startup, and a scripted `play_game.main()` smoke flow.
- Bundled Python was not used for Sprint 9.8 verification.

## Sprint 9.9 - Deterministic Narration Pipeline Stub
- Status: Complete.
- Added `engine/narration_pipeline.py` with a deterministic, read-only narration pipeline stub.
- Added `GameEngine.get_narration_preview(...)` to bridge narration context and narration output through a fixed sample candidate.
- Added the CLI/debug command `narration preview <player input>`.
- Added `test_narration_pipeline.py` covering deterministic preview packets, invalid candidate rejection, copy safety, and no world-state mutation.
- Preserved narration context behavior, narration output contract behavior, history context behavior, history query behavior, history id lookup, save/load behavior, and gameplay flow.
- Documented that the preview path validates fixed sample prose before display and does not make narration world truth.
- Verified with the official project virtual environment: `test_narration_pipeline.py`, `test_narration_output.py`, `test_narration_context.py`, `test_history_context.py`, `test_history_query.py`, `test_save_load.py`, `-m json.tool docs/current_sprint.json`, `play_game.py` startup, and a scripted `play_game.main()` smoke flow.
- Bundled Python was not used for Sprint 9.9 verification.

## Sprint 9.10 - Deterministic Narration Candidate Source Boundary
- Status: Complete.
- Added `engine/narration_source.py` as the deterministic fixed-sample narration candidate source.
- Updated `engine/narration_pipeline.py` to obtain narration candidates through the source boundary before output validation.
- Preserved the fixed prose sample, copy-safe packet behavior, and fail-closed handling for malformed source results, source exceptions, and invalid candidates.
- Preserved CLI compatibility for `narration context`, `narration output`, and `narration preview`.
- Verified with the official project virtual environment: `test_narration_source.py`, `test_narration_pipeline.py`, `test_narration_output.py`, `test_narration_context.py`, `test_history_context.py`, `test_history_query.py`, `test_save_load.py`, `-m json.tool docs/current_sprint.json`, `play_game.py` startup, and a scripted `play_game.main()` smoke flow covering narration context, narration output, repeated narration preview, and quit.
- Bundled Python was not used for Sprint 9.10 verification.
- Sprint 9.11 was not started.

## Sprint 9.11 - Deterministic Narration Request Packet Contract
- Status: Complete.
- Added `engine/narration_request.py` and `test_narration_request.py` for the deterministic request packet contract.
- Updated `engine/narration_pipeline.py` to build and validate a narration request before candidate-source invocation.
- Updated `engine/narration_source.py` to consume the request packet instead of raw narration context.
- Preserved the fixed sample prose, copy-safe preview packets, and fail-closed handling for malformed context, malformed request, request-construction failure, source exceptions, malformed source results, and invalid candidates.
- Preserved CLI compatibility for `narration context`, `narration output`, and `narration preview`.
- Verified with the official project virtual environment: `test_narration_request.py`, `test_narration_source.py`, `test_narration_pipeline.py`, `test_narration_output.py`, `test_narration_context.py`, `test_history_context.py`, `test_history_query.py`, `test_save_load.py`, `-m json.tool docs/current_sprint.json`, `play_game.py` startup, and a scripted `play_game.main()` smoke flow covering narration context, narration output, repeated narration preview, and quit.
- Bundled Python was not used for Sprint 9.11 verification.
- Sprint 9.12 was not started.
