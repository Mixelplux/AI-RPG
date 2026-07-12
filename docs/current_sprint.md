# Current Sprint

## Sprint 10.9 - One Declared Pressure Observation Cue

Status: Complete. Implemented, verified, and closed out without defining Sprint 10.10.

## Goal

Derive one authored player-perception cue when one applicable pressure meets its declared minimum level.

## Expected Files

Region Pack, validation, observation helper, perception orchestration, focused tests, and closeout documentation.

## Acceptance Criteria

- Strict zero-or-one declaration.
- Applicability plus threshold controls the cue.
- Derived, read-only, copy-safe, non-persistent perception only.
- No scene or narration projection.

## Verification

Run focused and required regressions through the official project interpreter.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{
  "schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,
  "project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},
  "sprint":{"id":"10.9","title":"One Declared Pressure Observation Cue","phase":"Phase 2B - Reactive World State Foundations","type":"bounded-feature","mode":"single-sprint","status":"complete",
  "goal":"Derive one authored player-perception cue when one applicable pressure meets its declared minimum level.",
  "source_state":{"branch":"main","commit":"a3717f894227a2a59f14e132641d13293265105f","predecessor_sprint":"10.8","predecessor_status":"complete"},
  "platform":{"operating_system":"Windows","shell":"PowerShell","official_interpreter":".\\.venv\\Scripts\\python.exe"},
  "architectural_decision":{"adr":"ADR-042","title":"Pressure Applicability Does Not Grant Perceptibility; Authored Observation Policy Does","status_during_sprint":"accepted"},
  "acceptance_criteria":["One strict optional Region Pack declaration.","Cue requires canonical applicability and level at or above threshold.","Perception exposes cue identity, pressure identity, and authored text only.","Observation is deterministic, derived, read-only, copy-safe, and non-persistent.","Scene and narration boundaries remain unchanged.","Save version remains 1."],
  "expected_files":{"likely_modified":["data/regions/bryn_shander.json","engine/region_validator.py","engine/pressure_observation.py","engine/perception_builder.py","engine/game_engine.py","test_pressure_observation.py","docs/architecture.md","docs/decisions.md","docs/roadmap.md","docs/sprint_log.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/next_chat_handoff.md"]},
  "non_goals":["multiple cues","raw pressure display","scene pressure projection","narration integration","persistence","knowledge systems","recurring drift","generic visibility or effect framework","Sprint 10.10 planning"],
  "verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_pressure_observation.py"],"environment_commands":["powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\preflight.ps1 -RepoRoot .","powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\validate_hardening_package.ps1 -PackageRoot ."],"manifest_commands":["JSON/YAML/Markdown deep comparison","git diff --check"]},
  "execution_phases":[{"id":"setup","goal":"Stage and validate Sprint 10.9."},{"id":"implementation","goal":"Implement the bounded cue."},{"id":"verification","goal":"Run focused and required regressions."},{"id":"closeout","goal":"Close without defining Sprint 10.10."}],
  "governance":["Exactly one sprint is active.","Do not substitute bundled, system, Windows Store, or alternate Python.","Do not define Sprint 10.10.","Do not commit."],
  "closeout":{"allowed_terminal_statuses":["complete","blocked"],"actual_files_changed":["data/regions/bryn_shander.json","engine/region_validator.py","engine/pressure_observation.py","engine/perception_builder.py","engine/game_engine.py","test_pressure_observation.py","test_pressure_state.py","docs/architecture.md","docs/decisions.md","docs/roadmap.md","docs/sprint_log.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/next_chat_handoff.md"],"verification_result":"Focused and all 17 repository tests passed through the official .venv; final workflow checks completed.","non_goals_preserved":"No multiple cues, raw pressure display, scene or narration projection, persistence, knowledge, recurring drift, generic framework, or Sprint 10.10 planning.","next_sprint":null}}}
```
<!-- CANONICAL-MANIFEST-END -->
