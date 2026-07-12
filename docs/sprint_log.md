# Sprint Log

## Sprint 10.17 Closeout

- Status: Complete.
- Capability delivered: explicit atomic addition of one opaque knowledge identifier to one stable static actor, with one durable `actor_knowledge_added` history entry for each material change.
- Preserved ownership: World State remains simulation truth; Region Pack data remains immutable; duplicate additions leave World State and Scene Snapshot live objects untouched; save version remains 1.
- Preserved non-goals: no knowledge projection, source, certainty, truth, provenance, evidence, dialogue, propagation, loss, or autonomous behavior.
- Verification: focused and required regressions, complete root inventory, Region Pack validation, manifest agreement, preflight, launch and save/load atomicity smokes, packet validation, and diff check passed through the official interpreter.

## Sprint 10.16 Closeout

- Status: Complete.
- Capability delivered: sparse persistent current knowledge membership for stable static actors, initialized by deep-copying validated immutable Region Pack `knowledge` arrays for new games.
- Ownership and compatibility: `world_state.actor_knowledge` stores only actor-to-identifier membership. Version-1 saves missing it normalize to empty membership during loading and do not receive new authored seeds.
- Validation and inspection: malformed membership, duplicates, empty values, unknown actors, and spawned or ephemeral identities fail closed. `GameEngine.get_actor_knowledge(...)` returns an immutable tuple.
- Boundary: no knowledge mutation, history, player-facing command, scene/perception/narration/prompt projection, dialogue effect, target-resolution change, or autonomous behavior was added.
- Verification: focused actor-knowledge coverage and all 23 root test scripts passed through the official interpreter; save/load, malformed live-load atomicity, and boundary checks passed. ADR-045 records the ownership decision.
- Governance: no gameplay playtest requested, no commit created, and Sprint 10.17 was not defined or started.

## Sprint 10.12 Closeout

- Status: Complete.
- Capability delivered: one optional immutable Region Pack declaration can relocate one seeded named static actor after a successful resolved conversation with one exact trigger actor.
- Fixture behavior: speaking with Captain Darvin Grey moves Guard Elin Voss from the North Gate to Main Street. The rebuilt scene immediately removes Elin from North Gate perception, targeting, and later conversation routing.
- Atomicity: the accepted conversation, pressure consequence when material, actor override, causally linked `actor_moved` history, final validation, and one rebuilt scene are prepared before one live commit. Repeated Captain conversations create genuine conversation history but no duplicate movement event.
- Persistence: save version remains 1; the actor override and backward causal history survive save/load, while Region declaration policy remains immutable content.
- Verification: focused relocation, actor-location, conversation-pressure, and save/load tests passed; all 20 root test scripts passed through the official interpreter. Final workflow evidence is recorded in the canonical manifest.
- ADR determination: no new ADR. ADR-035, ADR-038, ADR-039, and ADR-043 already establish the required conversation, causal-history, atomic-consequence, actor-location, and scene-consumer boundaries.
- Scope: no commands, schedules, autonomous movement, pathfinding, multiple declarations, spawned-instance persistence, or generic consequence infrastructure. Sprint 10.13 remains undefined and unstarted.

## Sprint 10.11 Closeout

- Status: Complete.
- Capability delivered: sparse persistent location overrides for seeded named static actors plus one explicit atomic `set_actor_location` operation.
- Ownership: Region Packs retain immutable actor identity, description, classification, and baseline location; World State owns only runtime location differences keyed by existing `entity_id`.
- Projection: moved actors naturally disappear from old perception and target resolution and appear at the destination; spawned templates are unchanged.
- Atomicity: material override preparation, one `actor_moved` history entry, completed-state validation, and candidate scene construction succeed before one live World State and scene commit. Same-location moves preserve exact scene identity and create no history.
- Persistence: save version remains 1; missing legacy override data normalizes to `{}`, and material overrides survive save/load.
- Verification: focused actor-location and save/load tests passed; all 19 root test scripts passed with the official project interpreter. Final workflow checks are recorded in the canonical sprint manifest.
- Governance: ADR-043 accepted. No commands, schedules, autonomous movement, pathfinding, spawned-instance persistence, or generic actor components were added. Sprint 10.12 remains undefined and unstarted.

## Sprint 10.6 Closeout

- Status: Complete.
- Capability delivered: one canonical, deterministic, read-only operation for pressures applicable to one exact Region Pack location.
- Files changed: `engine/pressure_state.py`, `engine/game_engine.py`, `test_pressure_applicability.py`, and the required closeout documentation.
- Ownership: `engine/pressure_state.py` validates and filters exact pressure scopes; `GameEngine` resolves and validates locations through the public facade `GameEngine.get_applicable_pressures(location_id=None)`.
- Ordering and copying: results are deep defensive copies ordered by sorted `pressure_id`; valid level `0` records remain included.
- Failure behavior: non-string, empty, unknown, and malformed-state reads fail closed without modifying durable or derived runtime state.
- Focused coverage: region and location applicability, omitted-location movement behavior, level `0`, stable ordering, defensive copies, failure preservation, existing read contracts, helper/facade agreement, and save/load equivalence passed.
- Persistence: save version remains `1`, no persistence fields were added, and save/load preserves applicability results.
- Official verification: all 15 required focused and regression commands passed through `.\.venv\Scripts\python.exe`; JSON parsing and YAML/JSON deep agreement passed.
- Environment: preflight reported 15 passes, 2 warnings, 3 blocked restricted-context probes, and 0 failures. No alternate, bundled, system, fallback, or live-AI environment was used.
- Launch: direct launch reached the initial scene and then encountered expected non-interactive EOF; the scripted `play_game.main()` smoke passed with exit code 0.
- Hardening: 20 checks passed with 0 failures; `git diff --check` passed.
- Governance: ADR-040 was accepted. No scene, perception, narration, visibility, ranking, mutation, or runtime-effect integration was added. Sprint 10.7 was not defined.

## Sprint 10.3 Closeout

- Status: Complete.
- Implementation and verification completed using the official project environment.
- Selected capability: Explicit Atomic Pressure-Level Change with Durable History.
- Architecture review: Complete; pressure mutation was selected as the next bounded Phase 2B capability after persistent scoped pressure representation.
- Ownership decision: exact pressure-level changes remain in or near `engine/pressure_state.py`; `GameEngine` owns orchestration and history creation.
- Atomicity decision: material changes commit pressure and history together, and no-op updates create no history.
- Persistence decision: loaded games retain the changed pressure and pressure-change history; save version remains unchanged.
- Boundary: exact-level validation, candidate-based mutation, durable history creation, and copy-safe result reporting only.
- Contract clarification: `GameEngine.set_pressure_level(pressure_id, new_level)` is the gameplay-facing method; exact levels are required and deltas are rejected.
- History clarification: material changes record `pressure_changed` entries with the pressure identity, type, scope, time, previous level, and new level.
- Facade clarification: there is no pressure-mutation CLI command.
- Added ADR-037: Pressure-Level Changes Are Atomic Current-State Transitions.
- Canonical Sprint 10.3 Markdown, YAML, JSON, and handoff files staged and synchronized.
- Application code and tests were updated for Sprint 10.3.
- Corrected verification passed with the official project environment: environment preflight, package validator, every required focused and regression test, Region Pack validator, canonical manifest parse and three-way deep-agreement checks, and `git diff --check`.
- Sprint 10.4 was not defined or started.

## Sprint 10.4 Architecture Review

- Status: Accepted and staged.
- Review result: Causally Referenced Pressure Transition was selected as the next bounded Phase 2B capability.
- Scope decision: one pressure consequence may reference one already accepted durable history event by stable history ID.
- Boundary decision: the source event remains read-only and is not part of the pressure/history atomic commit.
- Staging decision: Sprint 10.4 was staged only after explicit acceptance.
- Implementation status: complete and closed out.

## Sprint 10.4 Closeout

- Status: Complete.
- Implemented capability: `GameEngine.set_pressure_level_from_event(pressure_id, new_level, source_history_id)` for a linked pressure consequence that records one stable source history ID.
- Ownership boundary: `engine/world_state.py` validates backward-only `source_history_id` integrity; `GameEngine` resolves the source entry, prepares the candidate state, constructs the linked consequence, validates the finished candidate, and commits once.
- History-reference semantics: the source entry is already durable, read-only, and outside the atomic commit; legacy history and unlinked Sprint 10.3 pressure history remain valid.
- Atomicity behavior: one material change commits exactly one pressure mutation and one linked `pressure_changed` entry together; invalid source references, invalid pressure inputs, or injected validation/history failures commit nothing.
- No-op behavior: a validated same-level call resolves the source entry, returns `changed: false`, and creates no durable history.
- Save/load compatibility: linked history and `source_history_id` survive the existing save/load path, save version remains 1, and malformed loaded references fail closed.
- Focused files changed: `engine/game_engine.py`, `engine/world_state.py`, `test_pressure_state.py`, `test_save_load.py`, `docs/architecture.md`, `docs/decisions.md`, `docs/roadmap.md`, `docs/sprint_log.md`, `docs/current_sprint.md`, `docs/current_sprint.yaml`, `docs/current_sprint.json`, `docs/next_chat_handoff.md`.
- Verification results: the hardening package validator passed, the environment preflight passed, `test_pressure_state.py` passed, `test_save_load.py` passed, `test_interaction_history.py` passed, `test_history_query.py` passed, `test_history_context.py` passed, `test_narration_context.py` passed, `test_narration_pipeline.py` passed, the region validator passed, `python -m json.tool docs/current_sprint.json` passed, the JSON/YAML/Markdown deep-agreement check passed, and `git diff --check` passed.
- Restricted execution-context issue: the initial official `.venv` launch hit the documented access-denied process-creation limitation, then the same official interpreter was rerun successfully outside the restricted context.
- Excluded systems: automatic pressure effects, causal graphs, replay, schedulers, event buses, narration projection, scene projection, unresolved threads, actor systems, and new CLI commands were not added.
- Sprint 10.5 status: undefined and not started.

## Sprint 10.5 Architecture Review

- Status: Accepted and staged.
- Review result: One Declared Resolved-Conversation Pressure Consequence was selected as the next bounded Phase 2B capability.
- Scope decision: one strict Region Pack declaration may map one exactly resolved conversation target to one seeded pressure and one exact resulting level.
- Boundary decision: the source conversation event, linked pressure consequence, and resulting commit stay atomic inside one candidate world state.
- Staging decision: Sprint 10.5 was staged only after the declaration package was verified and promoted.

## Sprint 10.5 Closeout

- Status: Complete.
- Goal: implement one strict Region Pack declaration mapping one exactly resolved conversation target to one existing seeded pressure and one exact resulting level.
- Files changed: `data/regions/bryn_shander.json`, `engine/game_engine.py`, `engine/region_validator.py`, `test_conversation_pressure_effect.py`, `test_interaction_history.py`, `test_pressure_state.py`, `test_save_load.py`, and the required closeout documentation.
- Region content: added location-scoped `bryn_shander_gate_scrutiny` at level 10 and `north_gate_captain_scrutiny`, which maps Captain Darvin Grey to level 25 without repurposing the winter pressure.
- Atomicity: `GameEngine` prepares the source conversation, exact pressure mutation, linked consequence, completed-state validation, and candidate scene before one live world-state assignment and scene replacement.
- Behavior: the first Captain conversation creates source plus consequence; Elin Voss remains source-only; a repeated Captain conversation commits a new source but no consequence history and preserves the pressure record.
- Compatibility: the Sprint 10.4 public linked-transition API retains its already-durable-source material and no-op contracts through a private non-committing candidate helper.
- Persistence: save version 1 preserves pressure state, source and consequence entries, stable IDs, and `source_history_id` without persisting or replaying declarations; legacy pressure normalization remains intact.
- Review correction: entity cross-reference validation originally used set membership and could accept duplicate entities sharing one identifier. The correction counts matching entity IDs and requires exactly one; focused coverage also proves declaration-extraction atomicity, exact source preservation, and complete no-op pressure-record preservation.
- Verification: hardening validation passed 20 checks with 0 failures. Preflight exited 1 with 15 passes, 2 warnings, 3 restricted-context interpreter probes blocked, and 0 application failures; the approved official interpreter subsequently ran all required available tests successfully.
- Official checks passed: `test_conversation_pressure_effect.py`, `test_interaction_history.py`, `test_pressure_state.py`, `test_save_load.py`, `test_interaction_kernel.py`, `test_world_update.py`, `test_history_query.py`, `test_history_context.py`, `test_narration_context.py`, `test_narration_pipeline.py`, `engine/region_validator.py`, JSON validation, canonical manifest deep agreement, and `git diff --check`.
- Missing files: `test_target_resolver.py` and `test_time_advance.py` do not exist and were not reported as failures. Target resolution is covered by conversation-effect and interaction-history tests; time preservation is covered by conversation-effect, interaction-history, save/load, and history-context tests.
- Execution context: PowerShell 5.1 and the intentionally dirty review tree produced warnings; restricted preflight probes were tooling limitations rather than application failures. No alternate Python was used.
- Governance: ADR-039 was accepted, Sprint 10.6 remains undefined and not started, and no next capability was selected.

## Sprint 10.2 Closeout

- Status: Complete.
- Implementation and verification completed using the official project environment.
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
- Application code and tests were unchanged during closeout.
- Final validations passed: manifest parse/deep-agreement check, package validator, and `git diff --check`.
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
# Sprint 10.7 - One Declared Elapsed-Hour Pressure Threshold Consequence

- Status: Complete.
- Added strict validation for one optional immutable `elapsed_time_pressure_effect` Region Pack declaration.
- Added exact elapsed-hour threshold crossing during accepted time advancement.
- Atomically prepares and commits time, source history, material pressure change, causal history, and scene.
- Preserved same-level no-op behavior, direct/wait equivalence, save version 1, and replay prevention from durable time.
- Added `test_time_pressure_effect.py` and updated history expectations for the new causal consequence.
- Accepted ADR-041. Sprint 10.8 was not defined.

# Sprint 10.8 - Wait Command Single-Commit Atomicity

- Status: Complete.
- Added the immediate successful-wait return after the shared `advance_time` boundary.
- Successful wait now bypasses generic interaction application, validation, scene construction, and final assignment.
- Focused tests prove exactly one validation and scene build, direct/wait equivalence, and command-path failure atomicity.
- This is a conformance correction to ADR-041; no new ADR or architecture boundary was introduced.
- Sprint 10.9 was not defined or started.
# Sprint 10.9 - One Declared Pressure Observation Cue

- Status: Complete.
- Added one strict immutable Region Pack observation declaration and ADR-042.
- Derived one copy-safe cue from canonical applicability and current pressure level on perception reads.
- Preserved Scene Snapshot, narration, persistence, save version 1, and raw pressure ownership boundaries.
- Sprint 10.10 was not defined or started.

# Sprint 10.10 - Deterministic Pressure Cue Narration Projection

- Status: Complete.
- Carried zero or one perception-owned authored pressure cue through narration context, request, and prompt packets.
- Deterministically composed the exact cue into accepted preview display text at most once after source-result and candidate validation.
- Excluded pressure-change history records from narration context so raw levels, scope internals, and causal identifiers do not enter narration.
- Preserved empty-cue behavior, copy safety, determinism, failure atomicity, save version 1, and the fixed provider-neutral source.
- ADR-042 plus ADR-029 through ADR-033 already establish the ownership and fail-closed boundaries; no new ADR was required.
- Focused tests and all 18 repository tests passed through the official project interpreter.
- Sprint 10.11 was not defined or started.

# Sprint 10.13 - One Declared Elapsed-Time Actor Relocation Consequence

- Status: Complete.
- Added one strict immutable Region Pack declaration that moves Captain Darvin Grey from the North Gate to the West Gate on the first elapsed-hour threshold crossing.
- One candidate transition prepares time, source history, any pressure consequence, actor relocation, causal links, validation, and rebuilt scene before one live commit.
- ADR-035, ADR-038, ADR-039, and ADR-043 were sufficient; no new ADR was required. Save version remains 1.
- Focused tests and all 21 repository tests passed through the official project interpreter. Sprint 10.14 is undefined and unstarted.

# Sprint 10.14 - One Declared Conversation-Triggered Unresolved Thread

- Status: Complete.
- Adds one immutable Bryn Shander declaration triggered by a successful Captain Darvin Grey conversation.
- The candidate transition creates one sparse `open_threads` record and one causally linked `unresolved_thread_opened` history event without duplicate creation.
- Player perception projects only authored local evidence at the North Gate; it adds no quest-facing interface, objective, or marker.
- ADR-044 records the new persistent-domain ownership and compatible version-1 load normalization.
- Sprint 10.15 follow-up hardening validates persisted thread causality and excludes lifecycle history from narration context without changing player-facing evidence.
- Focused coverage and all 22 repository tests passed; scripted save/load and direct launch-close smoke checks passed through the official interpreter.
