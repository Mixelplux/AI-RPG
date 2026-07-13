# Sprint 10.48 — Authored Resolved-Thread Actor Relocation

## Goal

Resolve one authored clue-presentation thread and atomically relocate one declared stable actor.

## Expected Files

- Region Pack, GameEngine, Region Pack validator, relocation test, package records, ADR, and final review archive.

## Acceptance Criteria

- A strict Region Pack declaration moves only its declared stable actor at its declared thread-resolution transition.
- Source-first causal history, no-op and repeat safety, save/load, scene projection, target resolution, perception, and failure isolation hold.
- No generic consequence framework, save migration, or next package is introduced.

## Verification

- Focused and full official-interpreter tests, Region Pack validation, preflight, three-way manifest agreement, diff check, and independent package-review validation.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.48","title":"Authored Resolved-Thread Actor Relocation","type":"capability-package-internal","mode":"capability-package-internal","status":"complete","goal":"Resolve one authored clue-presentation thread and atomically relocate one declared stable actor.","platform":{"official_interpreter":".\\.venv\\Scripts\\python.exe"},"expected_files":{"likely_modified":["data/regions/bryn_shander.json","engine/game_engine.py","engine/region_validator.py","docs/architecture.md","docs/simulation_model.md","docs/roadmap.md","docs/decisions.md","docs/current_capability_package.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/sprint_log.md"],"likely_created":["test_conversation_actor_relocation.py","handoffs/authored-resolved-thread-actor-relocation-<short-head>.zip"]},"acceptance_criteria":["One valid declared resolution atomically resolves its thread and materially relocates its declared stable actor.","No-op, repeat, save/load, scene, target-resolution, perception, causal-history, and failure-isolation behavior are verified.","The declaration is strict Region Pack policy and no generic consequence framework is introduced."],"verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_conversation_actor_relocation.py","Relevant unresolved-thread, actor-location, save/load, and conversation regressions"],"required_regressions":["Complete root test inventory through the official interpreter","Region Pack validation"],"manifest_commands":["JSON/YAML/Markdown deep agreement","git diff --check"],"closeout_commands":["Official preflight","Independent package-review archive validation"]},"execution_phases":[{"id":"contract-and-composition-boundary","status":"complete"},{"id":"atomic-relocation-integration","status":"complete"},{"id":"scenario-persistence-and-closeout","status":"complete"}],"governance":["Approved package: Authored Resolved-Thread Actor Relocation.","No next capability package is staged."],"closeout":{"allowed_terminal_statuses":["complete"],"verification_result":"Focused and full verification passed; final packet validation pending final commit.","next_sprint":null}}}
```
<!-- CANONICAL-MANIFEST-END -->
