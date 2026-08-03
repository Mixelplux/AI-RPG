# Sprint 10.74 - Canonical Lifecycle Authority and Behavioral Verification Gate

Status: Ready for Independent Review.

Review state: Candidate Prepared.

## Lifecycle Summary

`docs/current_sprint.json` is the sole machine-readable lifecycle authority.
This readable package record supplies scope, rationale, acceptance criteria,
and status. Its duplicated lifecycle values must agree with JSON.

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

- Establish explicit lifecycle authority.
- Validate all material duplicated lifecycle state.
- Remove obsolete YAML authority requirements.
- Add one mandatory complete offline behavioral verification command.

## Authorized Scope

- Update only active operational lifecycle guidance and the current package
  and sprint records.
- Expand the repository-owned project-record validator and add focused idle,
  active, and disagreement fixtures.
- Add one repository-owned command that runs project-record validation and the
  complete stable offline `test_*.py` behavioral suite through the official
  interpreter.
- Keep save version `1`, provider requests forbidden, and `next_sprint` null.

## Exclusions

- No engine or gameplay behavior changes.
- No region or authored-content changes.
- No save-format or save-write changes.
- No provider changes or live API use.
- No dependency additions or replacements.
- No external GitWorkflowTools changes.
- No Codex configuration, sandbox, ACL, ownership, or Git-configuration
  changes.

## Acceptance Criteria

- JSON is explicitly the sole machine-readable lifecycle authority, while
  Markdown remains the readable scope and status record and cannot override
  contradictory JSON active-state fields.
- Every intentionally duplicated material lifecycle field is normalized and
  compared with exact conflicting fields and source files reported.
- Active operational guidance and validation contain no obsolete YAML
  lifecycle-authority requirement.
- One fail-fast command runs current-record validation, its complete fixture
  suite, and every stable root `test_*.py` script without a live provider
  request or alternate Python interpreter.
- Workflow guidance distinguishes focused implementation checks, mandatory
  pre-candidate offline verification, separately authorized live smoke, and
  post-merge lifecycle reconciliation.

## Stop Conditions

Stop if current records cannot be reconciled without changing historical
meaning; the existing suite has no stable definition; a required behavioral
test fails for an unrelated pre-existing reason; a dependency change is
required; or scope would extend into save behavior, provider behavior, or
external tools.

## Completion Boundary

The focused and complete offline verification passed. A single immutable
candidate commit and review-evidence export are authorized; merge remains
unauthorized. No following package is authorized.
