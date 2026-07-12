# Current Sprint

## Sprint 10.16 - Persistent Actor Knowledge Membership Baseline

Status: Complete.

## Goal

Establish persistent simulation-owned knowledge membership for stable authored static actors, seed new games from validated immutable Region Pack actor knowledge, preserve legacy save compatibility through empty-state normalization, and provide copy-safe engine inspection without adding knowledge mutation or player-facing behavior.

## Expected Files

World State, actor-knowledge validation and inspection, save/load compatibility, focused tests, ADR-045, relevant ownership documentation, canonical sprint records, and the required post-sprint review packet.

## Acceptance Criteria

- World State persistently owns sparse current knowledge membership for stable static actor identifiers.
- New games deep-copy validated immutable Region Pack knowledge arrays into runtime membership.
- Version-1 saves missing actor_knowledge normalize to empty runtime membership without reseeding Region Pack content.
- Region-aware validation rejects malformed, duplicate, unknown, spawned, and ephemeral actor knowledge membership.
- GameEngine exposes deterministic copy-safe static actor knowledge inspection without mutation or player-facing projection.
- Actor knowledge does not enter scenes, perception, narration, target resolution, dialogue, or autonomous behavior.

## Verification

Focused actor-knowledge coverage and all 23 repository tests passed through the official interpreter; Region Pack validation, canonical deep comparison, diff check, save/load and malformed-load atomicity smoke, direct-engine launch smoke, and review-packet validation completed.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.16","title":"Persistent Actor Knowledge Membership Baseline","type":"bounded-capability","mode":"single-sprint","status":"complete","goal":"Establish persistent simulation-owned knowledge membership for stable authored static actors, seed new games from validated immutable Region Pack actor knowledge, preserve legacy save compatibility through empty-state normalization, and provide copy-safe engine inspection without adding knowledge mutation or player-facing behavior.","platform":{"official_interpreter":".\\.venv\\Scripts\\python.exe"},"expected_files":{"likely_modified":["engine/world_state.py","engine/region_validator.py","engine/save_system.py","engine/game_engine.py","test_actor_knowledge.py","docs/architecture.md","docs/decisions.md","docs/roadmap.md","docs/simulation_model.md","docs/simulation_principles.md","docs/sprint_log.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/next_chat_handoff.md"],"likely_created":["engine/actor_knowledge.py"]},"acceptance_criteria":["World State persistently owns sparse current knowledge membership for stable static actor identifiers.","New games deep-copy validated immutable Region Pack knowledge arrays into runtime membership.","Version-1 saves missing actor_knowledge normalize to empty runtime membership without reseeding Region Pack content.","Region-aware validation rejects malformed, duplicate, unknown, spawned, and ephemeral actor knowledge membership.","GameEngine exposes deterministic copy-safe static actor knowledge inspection without mutation or player-facing projection.","Actor knowledge does not enter scenes, perception, narration, target resolution, dialogue, or autonomous behavior."],"verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_actor_knowledge.py"],"required_regressions":[".\\.venv\\Scripts\\python.exe test_save_load.py",".\\.venv\\Scripts\\python.exe test_unresolved_thread.py",".\\.venv\\Scripts\\python.exe test_actor_location.py",".\\.venv\\Scripts\\python.exe test_pressure_state.py",".\\.venv\\Scripts\\python.exe test_narration_context.py"],"manifest_commands":["JSON/YAML/Markdown deep comparison","git diff --check"],"closeout_commands":["Complete repository test inventory: 23 passed","Region Pack validation passed","scripted save/load and malformed-load atomicity smoke passed","direct-engine launch smoke passed"]},"governance":["Exactly one sprint is active.","Sprint 10.17 is undefined and unstarted.","Do not commit."],"closeout":{"allowed_terminal_statuses":["complete","blocked"],"verification_result":"Focused actor-knowledge coverage and all 23 repository tests passed through the official interpreter; Region Pack, manifest, diff, save/load atomicity, and launch checks passed.","next_sprint":null}}}
```
<!-- CANONICAL-MANIFEST-END -->
