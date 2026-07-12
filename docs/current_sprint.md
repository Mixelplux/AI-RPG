# Current Sprint

## Sprint 10.12 - One Declared Resolved-Conversation Actor Relocation Consequence

Status: Complete. Implemented, verified, and closed out without defining Sprint 10.13.

## Goal

Apply one optional immutable Region Pack actor-relocation consequence within the atomic successful resolved-conversation transition.

## Expected Files

Region declaration and validation, GameEngine candidate-transition orchestration, focused tests, and closeout documentation.

## Acceptance Criteria

- The exact optional declaration validates all identifiers and references.
- A matching resolved conversation and material actor move commit atomically with causal history.
- Same-location consequences commit only the genuine conversation.
- Scene construction and final validation occur once before one live commit.
- Save version 1 preserves resulting actor location and history.

## Verification

Focused relocation and regression tests and all 20 repository tests passed through the official project interpreter. Final workflow verification completed.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.12","title":"One Declared Resolved-Conversation Actor Relocation Consequence","phase":"Phase 2B - Reactive World State Foundations","type":"bounded-feature","mode":"single-sprint","status":"complete","goal":"Apply one optional immutable Region Pack actor-relocation consequence within the atomic successful resolved-conversation transition.","source_state":{"branch":"main","commit":"acf18f5866432d21511fb73607958876bb44c9ce","predecessor_sprint":"10.11","predecessor_status":"complete"},"platform":{"operating_system":"Windows","shell":"PowerShell","official_interpreter":".\\.venv\\Scripts\\python.exe"},"architectural_decision":{"adr":"ADR-035, ADR-038, ADR-039, and ADR-043","title":"Existing conversation, causal consequence, atomicity, and actor-location boundaries","status_during_sprint":"sufficient; no new ADR required"},"acceptance_criteria":["One exact optional Region Pack declaration validates trigger actor, moved static actor, destination, and exact fields.","A matching successful resolved conversation prepares its source history and optional actor move in one candidate transition.","Material relocation creates one causally linked actor_moved entry; same-location relocation creates none.","Completed World State validation and Scene Snapshot construction occur once before one live commit.","Scene, perception, targeting, and subsequent conversation routing reflect the rebuilt scene without direct override reads.","Version-1 save/load preserves actor relocation and causal history without persisting declaration policy."],"expected_files":{"likely_modified":["data/regions/bryn_shander.json","engine/region_validator.py","engine/game_engine.py","test_conversation_actor_relocation.py","test_conversation_pressure_effect.py","test_interaction_history.py","docs/architecture.md","docs/roadmap.md","docs/sprint_log.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/next_chat_handoff.md"]},"non_goals":["multiple relocation declarations","generic consequence dispatcher or rules engine","player actor-movement command","schedules or autonomous movement","pathfinding or travel duration","spawned actor persistence","broader actor state"],"verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_conversation_actor_relocation.py",".\\.venv\\Scripts\\python.exe test_actor_location.py",".\\.venv\\Scripts\\python.exe test_conversation_pressure_effect.py",".\\.venv\\Scripts\\python.exe test_save_load.py"],"environment_commands":["powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\preflight.ps1 -RepoRoot .","powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\validate_hardening_package.ps1 -PackageRoot ."],"manifest_commands":["JSON/YAML/Markdown deep comparison","git diff --check"]},"execution_phases":[{"id":"setup","goal":"Stage and validate Sprint 10.12."},{"id":"implementation","goal":"Implement one declared conversation actor relocation."},{"id":"verification","goal":"Run focused and official regressions."},{"id":"closeout","goal":"Close without defining Sprint 10.13."}],"governance":["Exactly one sprint is active.","Use existing conversation and actor-location ownership boundaries.","Do not substitute bundled, system, Windows Store, or alternate Python.","Do not define Sprint 10.13.","Do not commit."],"closeout":{"allowed_terminal_statuses":["complete","blocked"],"actual_files_changed":["data/regions/bryn_shander.json","engine/game_engine.py","engine/region_validator.py","test_conversation_actor_relocation.py","test_conversation_pressure_effect.py","test_interaction_history.py","docs/architecture.md","docs/roadmap.md","docs/sprint_log.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/next_chat_handoff.md"],"verification_result":"Focused relocation and regressions passed; all 20 repository tests passed through the official interpreter; final workflow checks completed.","non_goals_preserved":"No multiple declarations, generic dispatcher, commands, schedules, autonomous movement, pathfinding, spawned persistence, or broader actor state.","next_sprint":null}}}
```
<!-- CANONICAL-MANIFEST-END -->
