# Current Sprint

## Sprint 10.8 - Wait Command Single-Commit Atomicity

Status: Complete. Implemented, verified, and closed out without defining Sprint 10.9.

## Goal

Return successful wait commands immediately after the shared atomic time-advancement boundary.

## Expected Files

`engine/game_engine.py`, `test_time_pressure_effect.py`, and sprint documentation.

## Acceptance Criteria

- Successful wait bypasses generic interaction application.
- Wait performs exactly one validation, scene build, and commit boundary.
- Direct and command wait transitions remain equivalent.
- Failures preserve live World State and exact scene identity.

## Verification

Run the focused test, affected regressions, and complete workflow closeout verification through the official `.venv`.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{
  "schema_version": "1.0.0",
  "document_type": "current_sprint",
  "sprint_count": 1,
  "project": {"name": "AI Narrative RPG Engine", "principles": ["provider-neutral", "deterministic-core", "simulation-owned-truth"]},
  "sprint": {
    "id": "10.8", "title": "Wait Command Single-Commit Atomicity", "phase": "Phase 2B - Reactive World State Foundations", "type": "bounded-feature", "mode": "single-sprint", "status": "complete",
    "goal": "Return successful wait commands immediately after the shared atomic time-advancement boundary.",
    "source_state": {"branch": "main", "commit": "d36118228979e319f201f65df01b1344a6ad22c1", "predecessor_sprint": "10.7", "predecessor_status": "complete"},
    "platform": {"operating_system": "Windows", "shell": "PowerShell", "official_interpreter": ".\\.venv\\Scripts\\python.exe"},
    "architectural_decision": {"adr": "ADR-041", "title": "Conformance correction to the accepted single-commit atomicity boundary", "status_during_sprint": "accepted-no-new-adr"},
    "ownership": {"game_engine": "Successful wait command orchestration returns after advance_time."},
    "acceptance_criteria": ["Successful wait invokes generic apply_interaction zero times.", "Wait invokes world-state validation exactly once and scene construction exactly once.", "Direct and command wait transitions are equivalent.", "Preparation, validation, and scene failures preserve live World State and exact scene identity."],
    "expected_files": {"likely_modified": ["engine/game_engine.py", "test_time_pressure_effect.py", "docs/architecture.md", "docs/roadmap.md", "docs/sprint_log.md", "docs/current_sprint.md", "docs/current_sprint.yaml", "docs/current_sprint.json", "docs/next_chat_handoff.md"]},
    "non_goals": ["new persistent fields", "rollback framework", "transaction infrastructure", "generic command dispatcher", "new effect rules", "new pressure projection", "Sprint 10.9 planning"],
    "verification": {"focused_commands": [".\\.venv\\Scripts\\python.exe test_time_pressure_effect.py"], "environment_commands": ["powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\preflight.ps1 -RepoRoot .", "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\validate_hardening_package.ps1 -PackageRoot ."], "manifest_commands": ["JSON/YAML/Markdown deep comparison", "git diff --check"]},
    "execution_phases": [{"id": "setup", "goal": "Stage and validate Sprint 10.8."}, {"id": "implementation", "goal": "Apply the bounded early-return correction."}, {"id": "verification", "goal": "Run focused and required regressions."}, {"id": "closeout", "goal": "Close out without defining Sprint 10.9."}],
    "governance": ["Exactly one sprint is active.", "Do not substitute bundled, system, Windows Store, or alternate Python.", "Do not define or begin Sprint 10.9.", "Do not commit."],
    "closeout": {"allowed_terminal_statuses": ["complete", "blocked"], "actual_files_changed": ["engine/game_engine.py", "test_time_pressure_effect.py", "docs/architecture.md", "docs/roadmap.md", "docs/sprint_log.md", "docs/current_sprint.md", "docs/current_sprint.yaml", "docs/current_sprint.json", "docs/next_chat_handoff.md"], "verification_result": "Focused and all 16 repository tests passed through the official .venv; final environment and governance checks passed with documented preflight blocks.", "non_goals_preserved": "No persistence, rollback framework, transaction infrastructure, generic dispatcher, new effects, projection, or Sprint 10.9 planning was added.", "next_sprint": null}
  }
}
```
<!-- CANONICAL-MANIFEST-END -->
