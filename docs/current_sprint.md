# Current Sprint

## Sprint 10.20 — Persistent Located Evidence-Trace Representation

Status: Active.

## Goal

Establish sparse persistent World State evidence traces with stable identity,
opaque content identity, exact Region Pack location, defensive reads, and
version-1 candidate-load normalization.

## Expected Files

`engine/evidence_traces.py`, `engine/world_state.py`, `engine/save_system.py`,
`engine/region_validator.py`, focused tests, ADR/documentation, and canonical
package and sprint records.

## Acceptance Criteria

- Every persisted trace has unique stable `trace_id`, opaque `evidence_id`, and
  one exact Region Pack `location_id` in deterministic order.
- Validation is strict and Region-aware; reads are defensive.
- Save version remains `1`; legacy candidate loads may normalize only a missing
  collection and malformed candidate loads fail safely.
- No player-facing trace projection exists.

## Verification

Focused evidence-trace tests, affected World State/save-load/Region Pack
regressions, canonical manifest agreement, and `git diff --check`.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.20","title":"Persistent Located Evidence-Trace Representation","type":"bounded-feature","mode":"capability-package-internal","status":"active","goal":"Establish one sparse persistent World State evidence-trace representation with stable trace identity, exact Region Pack location, opaque content identity, deterministic ordering, strict Region-aware validation, defensive copies, and version-1 legacy-load normalization only.","platform":{"official_interpreter":".\\.venv\\Scripts\\python.exe"},"expected_files":{"likely_modified":["engine/world_state.py","engine/save_system.py","engine/region_validator.py","docs/architecture.md","docs/decisions.md","docs/roadmap.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/current_capability_package.md","TASK.md"],"likely_created":["engine/evidence_traces.py","test_evidence_traces.py"]},"acceptance_criteria":["World State owns a sparse evidence_traces collection whose records have stable non-empty trace_id, opaque non-empty evidence_id, and one exact Region Pack location_id.","Validation is deterministic, Region-aware, rejects malformed or duplicate identities, and all public reads are defensive.","Save version remains 1; missing evidence_traces normalizes only during candidate loading and malformed candidate loads fail without changing live state.","No trace projection enters scene, perception, narration, dialogue, targeting, CLI, or gameplay behavior."],"verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_evidence_traces.py"],"required_regressions":["World State, save/load, history, region validation, and engine regressions"],"manifest_commands":["JSON/YAML/Markdown deep comparison","git diff --check"],"closeout_commands":["Focused representation tests, affected regressions, Region Pack validation, save/load checks, and checkpoint validation"]},"execution_phases":[{"id":"setup"},{"id":"implementation"},{"id":"verification"},{"id":"closeout"}],"governance":["Exactly one sprint is active.","Part of accepted Evidence Trace Foundations package.","Save version remains 1.","Do not begin Sprint 10.21 until Sprint 10.20 is complete."],"closeout":{"allowed_terminal_statuses":["complete","blocked"],"verification_result":null,"next_sprint":"10.21"}}}
```
<!-- CANONICAL-MANIFEST-END -->
