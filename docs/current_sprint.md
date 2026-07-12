# Current Sprint

## Sprint 10.18 - Causally Referenced Actor-Knowledge Addition

Status: Complete.

## Goal

Add one deterministic engine-owned operation that atomically adds one exact knowledge identifier to one stable static actor while referencing one already accepted durable source-history event, validates backward causal integrity, preserves duplicate additions as unchanged no-ops, and introduces no automatic acquisition policy or player-facing behavior.

## Expected Files

`engine/game_engine.py`, `test_actor_knowledge.py`, relevant ownership documentation, ADR-047, canonical sprint records, `docs/next_chat_handoff.md`, and the required Sprint 10.18 review packet.

## Acceptance Criteria

- `GameEngine.add_actor_knowledge_from_event(actor_id, knowledge_id, source_history_id)` validates a stable static actor, non-empty knowledge identifier, and existing earlier durable source event without semantic source-event eligibility.
- A material addition appends membership once, records one `actor_knowledge_added` entry containing `source_history_id`, validates the complete candidate, and commits World State once without replacing the Scene Snapshot.
- A duplicate validates the source and returns unchanged with no membership duplication or history.
- Source-free historical entries remain valid, save version remains `1`, and malformed persisted causal links fail atomically during load.
- Lifecycle history is queryable but excluded from narration context; neither membership nor source linkage is projected into player-facing systems.

## Verification

Focused actor-knowledge and narration-context tests, save/load and causal-integrity regressions, the complete root inventory, Region Pack validation, save/load atomicity and launch smokes, hardening validation, canonical manifest comparison, review-packet validation, and `git diff --check` passed or are recorded in closeout evidence.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.18","title":"Causally Referenced Actor-Knowledge Addition","type":"bounded-feature","mode":"single-sprint","status":"complete","goal":"Add one deterministic engine-owned operation that atomically adds one exact knowledge identifier to one stable static actor while referencing one already accepted durable source-history event, validates backward causal integrity, preserves duplicate additions as unchanged no-ops, and introduces no automatic acquisition policy or player-facing behavior.","platform":{"official_interpreter":".\\.venv\\Scripts\\python.exe"},"expected_files":{"likely_modified":["engine/game_engine.py","test_actor_knowledge.py","docs/architecture.md","docs/decisions.md","docs/roadmap.md","docs/simulation_model.md","docs/simulation_principles.md","docs/sprint_log.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/next_chat_handoff.md"],"likely_created":["handoffs/post_sprint_10_18_architecture_review_packet.zip"]},"acceptance_criteria":["GameEngine.add_actor_knowledge_from_event(actor_id, knowledge_id, source_history_id) validates exact stable static actor, knowledge, and source identifiers; requires an existing earlier durable source event; and does not impose source event-type eligibility.","A material addition appends one absent knowledge identifier, creates exactly one actor_knowledge_added history entry with source_history_id and current durable time, validates the completed candidate with backward causal integrity, and assigns World State once without rebuilding the Scene Snapshot.","A duplicate validates all inputs including source_history_id and returns changed false with no history, World State assignment, or Scene Snapshot replacement.","Source-free historical actor_knowledge_added entries remain valid, save version remains 1, and malformed persisted source linkage fails atomically during load.","The lifecycle history remains engine-queryable and excluded from narration context; actor knowledge and source linkage remain absent from scene, perception, narration, prompts, dialogue, targeting, and behavior."],"verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_actor_knowledge.py",".\\.venv\\Scripts\\python.exe test_narration_context.py"],"required_regressions":[".\\.venv\\Scripts\\python.exe test_save_load.py",".\\.venv\\Scripts\\python.exe test_actor_location.py",".\\.venv\\Scripts\\python.exe test_pressure_state.py",".\\.venv\\Scripts\\python.exe test_unresolved_thread.py"],"manifest_commands":["JSON/YAML/Markdown deep comparison","git diff --check"],"closeout_commands":["Complete root test inventory","Region Pack validation","causally referenced knowledge-addition save/load and atomicity smoke","direct-engine launch smoke","hardening validation"]},"execution_phases":[{"id":"setup"},{"id":"implementation"},{"id":"verification"},{"id":"closeout"}],"governance":["Exactly one sprint is active.","Do not substitute bundled, system, Windows Store, or alternate Python.","Save version remains 1.","Do not define or begin Sprint 10.19.","Do not commit."],"closeout":{"allowed_terminal_statuses":["complete","blocked"],"verification_result":"Focused coverage and all 23 root tests passed through the official interpreter; final closeout validation recorded separately.","next_sprint":null}}}
```
<!-- CANONICAL-MANIFEST-END -->
