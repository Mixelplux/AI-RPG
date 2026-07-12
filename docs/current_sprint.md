# Sprint 10.27 — Region Pack Discovery Declarations

Status: Active.

## Goal

Add strict immutable Region Pack discovery declarations with exact authored player-facing text for existing evidence traces.

## Expected Files

- data/regions/bryn_shander.json
- engine/region_validator.py
- test_discovery.py
- docs/current_sprint.md
- docs/current_sprint.yaml
- docs/current_sprint.json
- docs/next_chat_handoff.md
- docs/sprint_log.md

## Acceptance Criteria

- Region Packs own strict discovery declarations, trace references, exact locations, and authored player-facing text.
- Declarations remain immutable and do not expose opaque trace identifiers to the player.
- No World State, history, investigation command, or save-version behavior is introduced.

## Verification

- Focused declaration validation and evidence-trace regression.
- Canonical manifests parse and deeply agree; git diff --check passes.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.27","title":"Region Pack Discovery Declarations","type":"bounded-feature","mode":"capability-package-internal","status":"active","goal":"Add strict immutable Region Pack discovery declarations with exact authored player-facing text for existing evidence traces.","platform":{"official_interpreter":".\\.venv\\Scripts\\python.exe"},"expected_files":{"likely_modified":["data/regions/bryn_shander.json","engine/region_validator.py","test_discovery.py","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/next_chat_handoff.md","docs/sprint_log.md"],"likely_created":[]},"acceptance_criteria":["Region Packs own strict discovery declarations, trace references, exact locations, and authored player-facing text.","Declarations remain immutable and do not expose opaque trace identifiers to the player.","No World State, history, investigation command, or save-version behavior is introduced."],"verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_discovery.py"],"required_regressions":[".\\.venv\\Scripts\\python.exe test_evidence_traces.py"],"manifest_commands":["JSON/YAML/Markdown parse and deep comparison","git diff --check"],"closeout_commands":["Focused declaration validation and evidence-trace regression"]},"execution_phases":[{"id":"implementation"}],"governance":["Exactly one sprint is active.","Sprint 10.27 is the third internal milestone of Deterministic Local Investigation and Evidence Discovery.","Sprint 10.28 remains unstaged."],"closeout":{"allowed_terminal_statuses":["complete"],"verification_result":"Pending.","next_sprint":null}}}
```
<!-- CANONICAL-MANIFEST-END -->
