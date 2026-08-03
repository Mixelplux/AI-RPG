# Sprint 10.74 - Canonical Lifecycle Authority and Behavioral Verification Gate

Status: Ready for Independent Review.

Review state: Candidate Prepared.

## Lifecycle Summary

`docs/current_sprint.json` is the sole machine-readable lifecycle authority.
This readable sprint record supplies the authorized goal, exclusions,
acceptance criteria, and current status. Its duplicated lifecycle values must
agree with JSON.

| Lifecycle field | Value |
|---|---|
| `active_sprint` | `10.74` |
| `active_capability_package` | `10.74` |
| `latest_completed_sprint` | `10.73` |
| `latest_completed_status` | `complete` |
| `next_sprint` | `null` |
| `candidate_state` | `created` |
| `merge_state` | `not_merged` |
| `save_version` | `1` |
| `provider_requests` | `forbidden` |
| `official_interpreter` | `.\.venv\Scripts\python.exe` |
| `required_verification_command` | `& .\tools\run_offline_behavioral_verification.ps1` |

## Goal

Establish explicit canonical lifecycle authority, validate all material
duplicated lifecycle state, remove obsolete YAML authority, and add one
mandatory complete offline behavioral verification command.

## Expected Files

- `AGENTS.md`
- `WORKFLOW.md`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`
- `tools/validate_project_records.ps1`
- `tools/test_project_records.ps1`
- `tools/run_offline_behavioral_verification.ps1`

## Acceptance Criteria

- The authority roles and contradiction behavior described in the current
  capability-package record are mechanically enforced.
- Positive idle and active fixtures pass; mismatched active sprint, active
  package, status, next sprint, review/candidate/merge state, save version,
  provider policy, interpreter, verification command, and forbidden YAML
  references fail with exact fields and files.
- `& .\tools\run_offline_behavioral_verification.ps1` fails immediately if the
  official interpreter is missing, runs project-record validation and all
  stable root `test_*.py` scripts, and never invokes live smoke.
- Focused checks and the complete offline suite pass without durable repository
  output or live API use.

## Exclusions and Stop Conditions

The exclusions and stop conditions in `docs/current_capability_package.md`
apply unchanged. Candidate preparation is authorized, but merge remains
unauthorized. Save version remains `1`, provider requests remain forbidden,
and `next_sprint` remains `null`.

## Verification

- During implementation, run the smallest relevant syntax and fixture checks.
- Run `& .\tools\run_offline_behavioral_verification.ps1 -SelfTest` for the
  focused native stdout, stderr, traceback, and exit-code regression matrix.
- Before reporting completion, run the complete project-record fixture suite,
  the official complete offline behavioral verification command, JSON parsing
  through the official interpreter, safe read-only preflight checks, and `git
  diff --check`.
- Do not run live provider smoke.
