# Current Sprint

## Sprint 10.15 - Strict Unresolved-Thread Integrity and Narration Isolation

Status: Complete.

## Goal

Enforce Region-aware identity and causal integrity for persisted open unresolved threads and isolate internal lifecycle history from narration context.

## Expected Files

Thread validation, narration isolation, focused regression tests, closeout documentation, and the required review packet.

## Acceptance Criteria

- Persisted open threads match declaration, trigger conversation, and exactly one opening record.
- Malformed state fails before live replacement.
- Lifecycle history remains engine-visible and narration-excluded.
- Save version 1 and location-aware evidence remain intact.

## Verification

Focused and all 22 repository tests passed; final smoke, manifest deep comparison, diff check, and review packet validation completed.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.15","title":"Strict Unresolved-Thread Integrity and Narration Isolation","type":"bounded-hardening","mode":"single-sprint","status":"complete","goal":"Enforce Region-aware identity and causal integrity for persisted open unresolved threads and isolate internal lifecycle history from narration context.","platform":{"official_interpreter":".\\.venv\\Scripts\\python.exe"},"expected_files":{"likely_modified":["engine/unresolved_threads.py","engine/world_state.py","engine/narration_context.py","test_unresolved_thread.py","test_interaction_history.py","docs/architecture.md","docs/roadmap.md","docs/sprint_log.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/next_chat_handoff.md"]},"acceptance_criteria":["Persisted open threads match declaration, trigger conversation, and exactly one opening record.","Malformed state fails before live replacement.","Lifecycle history remains engine-visible and narration-excluded.","Save version 1 and location-aware evidence remain intact."],"verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_unresolved_thread.py"],"manifest_commands":["JSON/YAML/Markdown deep comparison","git diff --check"]},"governance":["Exactly one sprint is active.","Do not define Sprint 10.16.","Do not commit."],"closeout":{"allowed_terminal_statuses":["complete","blocked"],"verification_result":"Focused and all 22 repository tests passed.","next_sprint":null}}}
```
<!-- CANONICAL-MANIFEST-END -->
