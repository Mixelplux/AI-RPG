# Sprint 10.53 — One Declared Delayed-Watch Discovery Actor Recall

## Goal

Give the existing delayed-watch discovery one authored player use: presenting it to Captain Grey at the West Gate returns him durably to the North Gate.

## Expected Files

- Region Pack, validator, GameEngine, focused tests, affected authority, package records, and package-review archive.

## Acceptance Criteria

- One strict optional declaration, exact pair selection, atomic relocation, and version-1 no-op semantics.

## Verification

- Focused and full official-interpreter tests, Region Pack validation, canonical agreement, preflight, diff check, and independent package-review validation.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.53","title":"One Declared Delayed-Watch Discovery Actor Recall","type":"capability-package","mode":"capability-package","status":"complete","goal":"Give the existing delayed-watch discovery one authored player use: presenting it to Captain Grey at the West Gate returns him durably to the North Gate.","platform":{"official_interpreter":".\\.venv\\Scripts\\python.exe"},"expected_files":{"likely_modified":["data/regions/bryn_shander.json","engine/game_engine.py","engine/region_validator.py","test_time_evidence_trace_effect.py","docs/architecture.md","docs/roadmap.md","docs/decisions.md","docs/current_capability_package.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/sprint_log.md"],"likely_created":["test_delayed_watch_discovery_actor_recall.py","handoffs/delayed-watch-discovery-actor-recall-<short-head>.zip"]},"acceptance_criteria":["One optional strict singleton declaration binds The Delayed Watch Mark, Captain Grey, the North Gate, and exact authored response text.","The existing present command selects the west-road and delayed-watch paths by exact discovery/target pair without ordering or precedence.","A material recall atomically creates one clue-presented source and one causal actor-moved entry, validates once, rebuilds one Scene Snapshot, and publishes once.","Existing-location recall is an exact relocation no-op; save version remains 1 and no discovery is consumed."],"verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_delayed_watch_discovery_actor_recall.py","Affected time, discovery, presentation, relocation, save/load, narration, and Region Pack regressions"],"required_regressions":["Complete root test inventory through the official interpreter","Region Pack validation"],"manifest_commands":["JSON/YAML/Markdown deep agreement","git diff --check"],"closeout_commands":["Official preflight","Independent package-review archive validation"]},"execution_phases":[{"id":"contract-and-staging","status":"complete"},{"id":"exact-pair-recall-transition","status":"complete"},{"id":"verification-and-closeout","status":"complete"}],"governance":["Owner-authorized package: One Declared Delayed-Watch Discovery Actor Recall.","Excluded: generic presentation systems, precedence, discovery consumption, new persistence, save migration, autonomous movement, and the workflow-horizon update.","No next package is staged; next_sprint is null."],"closeout":{"allowed_terminal_statuses":["complete"],"verification_result":"Focused and full official-interpreter verification passed; package-review archive validation pending committed review candidate.","next_sprint":null}}}

```
<!-- CANONICAL-MANIFEST-END -->
