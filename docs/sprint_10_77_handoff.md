# Sprint 10.77 accepted closeout

## Repository and authority
Protected parent baseline: `18b69f095a429cf00f83bad597fc381e1e9b03fe`.
Branch: `codex/west-road-predicament-10.77`. Owner smoke and acceptance passed. Finalization authorizes one accepted commit and strict fast-forward merge. Sprint records are complete and the project is idle; no next package is authorized or selected.

## Implementation and state
Existing Bryn Shander content is replaced in place. The sole new persistent record is `west_road_predicament` with `phase` (the seven approved values) and `last_outcome_history_id` (null initially, otherwise a matching causal outcome). Current phase governs eligibility; history validates/explains rather than reconstructs it. Discoveries hold encountered reports; actor knowledge holds actually shared information. Both initial decisions cost one displayed hour. Four follow-ups abstract bounded local operations without additional elapsed time, confrontation or capture. Final outcomes leave the wider threat unresolved.

The accepted presentation correction gives one actor listing, prominent current choices and a concise circumstance paragraph. CLI compares derived narration to suppress unchanged-scene repeats; load/reset explicitly refresh. The deterministic `Previously:` summary is one brief continuity paragraph and the ordinary scene follows it. No recap state is persisted. Canonical scene projection supplies visible names and groups. Optional authored spawn display names are forwarded by scene construction; internal templates are not display fallbacks. Contextual suggestions expose exact commands/costs. Ordinary CLI removes intent diagnostics and raw time dictionaries. Resume is derived, includes initial decision plus follow-up result, and does not offer expired choices.

## Compatibility
Save envelope stays 1. Updated Bryn Shander requires the scenario record and explicitly rejects old prototype saves. It never initializes missing scenario state on load, invents migration decisions, changes the original file, or replaces the active session after failed load. Scenario-aware save construction also rejects inconsistent current state.

## Verification
Six new behavioral groups pass: evidence/prerequisites, all branch outcomes, injected atomic failures, integrity/copies, old-save preservation, and ordinary CLI smoke with save/load on both branches. Every phase round-trips; premature, repeated and opposite-branch commands leave state/time/history unchanged. Malformed phase, causal, time, actor-information and evidence combinations are rejected.

Changed Python AST checks, authored pack validators, JSON/save-version assertions and lifecycle validation pass. Maintained GitWorkflowTools verification passed with repository state unchanged. Preflight: 19 passes, 2 warnings (PowerShell bootstrap version and expected working diff), no blocks/failures. No live provider calls or broad repository certification.

Legacy mechanism tests use an explicit test-only baseline fixture. Windows TemporaryDirectory cleanup failed initially; affected tests now use owning-script-prefixed direct files in `.artifacts/`, per the documented recovery. Obsolete ordinary-play assertions were isolated to the fixture; coverage was retained. The first maintained verification detected a concurrent change to `test_pressure_applicability.py`; that change was preserved and checked, and the settled-tree rerun passed. No shared tools or ACLs were changed.

Focused scripts passed:
- `test_actor_knowledge.py`
- `test_actor_knowledge_response.py`
- `test_actor_location.py`
- `test_contextual_action_projection.py`
- `test_conversation_actor_knowledge.py`
- `test_conversation_actor_relocation.py`
- `test_conversation_pressure_effect.py`
- `test_current_scene_projection.py`
- `test_delayed_watch_discovery_actor_recall.py`
- `test_discovery.py`
- `test_discovery_gated_conversation_affordance.py`
- `test_discovery_gated_relocated_actor_response.py`
- `test_elapsed_time_transition_observation.py`
- `test_evidence_traces.py`
- `test_history_context.py`
- `test_history_query.py`
- `test_interaction_history.py`
- `test_interaction_kernel.py`
- `test_narration_context.py`
- `test_navigation_projection.py`
- `test_one_hour_west_road_exit_traversal.py`
- `test_pressure_applicability.py`
- `test_pressure_narration.py`
- `test_pressure_observation.py`
- `test_pressure_state.py`
- `test_region_topology.py`
- `test_resolved_thread_actor_knowledge_acknowledgment.py`
- `test_resolved_thread_evidence_trace_consequence.py`
- `test_save_load.py`
- `test_time_actor_relocation.py`
- `test_time_evidence_trace_effect.py`
- `test_time_pressure_effect.py`
- `test_unresolved_thread.py`
- `test_western_trade_road_arrival_discovery.py`
- `test_west_road_predicament.py`
- `test_world_update.py`

## Owner smoke
Run `.\.venv\Scripts\python.exe play_game.py` from the repository root.

Common path:
1. Read the problem and speak to Grey/Elin if desired.
2. `go to Southwest Trade Road`
3. `investigate`
4. `talk to Mara`
5. `go to North Gate`
6. `present Repeated Watch Tracks to Elin`
7. `present Mara's Account to Elin`

Patrol branch: `advocate patrol`, then `save`, `load`, then `pursue observers` or `restore coverage`.
Investigation branch: `reset`, repeat common path, `continue investigation`, then `save`, `load`, then `protect supply stop` or `locate raiders`.
To compare both follow-ups from a branch, load the branch save again and choose its other follow-up. Verify the differing outcome text, remembered initial decision, distinct discoveries and persistent resumed state. Initial travel to the road already costs an hour; either commitment adds exactly one further hour. Follow-ups add none.

## Scope
Additional directly necessary files include the scenario module/test, scene-loader display labels, test-only authored fixture, Windows test-file helper, architecture/ADR documentation and this handoff. No generalized system or prohibited subsystem was added.

Final accepted 55-path scope (including the preserved observed test change):
- `data/regions/bryn_shander.json`
- `docs/architecture.md`
- `docs/current_capability_package.md`
- `docs/current_sprint.json`
- `docs/current_sprint.md`
- `docs/decisions.md`
- `docs/sprint_10_77_handoff.md`
- `engine/action_eligibility.py`
- `engine/contextual_action_projection.py`
- `engine/game_engine.py`
- `engine/region_validator.py`
- `engine/save_system.py`
- `engine/scene_loader.py`
- `engine/west_road_predicament.py`
- `engine/west_road_presentation.py`
- `engine/world_state.py`
- `play_game.py`
- `test_actor_knowledge.py`
- `test_actor_knowledge_response.py`
- `test_actor_location.py`
- `test_artifact_files.py`
- `test_contextual_action_projection.py`
- `test_conversation_actor_knowledge.py`
- `test_conversation_actor_relocation.py`
- `test_conversation_pressure_effect.py`
- `test_current_scene_projection.py`
- `test_delayed_watch_discovery_actor_recall.py`
- `test_discovery.py`
- `test_discovery_gated_conversation_affordance.py`
- `test_discovery_gated_relocated_actor_response.py`
- `test_elapsed_time_transition_observation.py`
- `test_evidence_traces.py`
- `test_fixtures/README.md`
- `test_fixtures/bryn_shander_legacy.json`
- `test_history_context.py`
- `test_history_query.py`
- `test_interaction_history.py`
- `test_interaction_kernel.py`
- `test_narration_context.py`
- `test_navigation_projection.py`
- `test_one_hour_west_road_exit_traversal.py`
- `test_pressure_applicability.py`
- `test_pressure_narration.py`
- `test_pressure_observation.py`
- `test_pressure_state.py`
- `test_resolved_thread_actor_knowledge_acknowledgment.py`
- `test_resolved_thread_evidence_trace_consequence.py`
- `test_save_load.py`
- `test_time_actor_relocation.py`
- `test_time_evidence_trace_effect.py`
- `test_time_pressure_effect.py`
- `test_unresolved_thread.py`
- `test_west_road_predicament.py`
- `test_west_road_presentation.py`
- `test_western_trade_road_arrival_discovery.py`

## Candidate reusable concepts
Observe explicit commitment, selective information sharing, outcome creating opportunity, witnessed actor response, and a bounded time/consequence transition. None was generalized. Another independently designed situation must demonstrate repeated need before extraction.

## Final reconciliation and acceptance
Owner smoke passed and the owner accepted the current-stage player experience. All six commands, seven phases, explicit sharing, one-hour initial consequences, four persistent follow-ups, deterministic actor responses and concise resume remain within the authorized package. History explains and validates causal outcomes; the scenario phase owns current progression. No provider involvement, generalized framework, save-version change or migration was added.

Scope classification: 10 production paths, 1 authored-content path, 37 directly affected test/fixture paths, 6 lifecycle/documentation paths and 1 Windows test helper. The original 53 paths gained only the narrow presentation module and its focused test. Scene-loader labels expose already-authored group names. ADR-060 records the durable phase/compatibility decision. The fixture preserves baseline authored content (line endings differ), solely for prior mechanism tests. Five accidentally re-encoded Unicode test assertions were restored to baseline wording during final review. No unnecessary paths remain.

The owner's tracked smoke save was preserved byte-for-byte in `.artifacts/sprint_10_77_owner_smoke_save.json`, then the tracked baseline save restored, as separately directed. It is excluded from the candidate.

Final direct checks passed: AST parsing of all 46 changed Python files; revised and legacy authored-pack validation; official-interpreter lifecycle/save-version/provider assertions; scenario behavior (6 groups), presentation/resume (5 groups), discovery, actor-knowledge response, region topology, one-hour traversal, scene projection and save/load scripts; lifecycle validator (7 passes, 0 failures); and `git diff --check`. Prior affected-system regression evidence remains applicable. Maintained GitWorkflowTools candidate creation performs its mutation-protected verification before staging; no broad certification or live provider calls are requested.

## Deferred
- Broader player-facing presentation refinement.
- Future observation of reusable world-development primitives.
- Crash-safe disk-save replacement before longer-form playtesting.
