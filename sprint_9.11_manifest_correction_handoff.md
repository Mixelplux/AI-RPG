# Sprint 9.11 Manifest Correction Handoff

## Task Type

Mechanical documentation correction.

Recommended model: **mini or lighter model with low reasoning**.

A higher-reasoning model is not required because the corrected files and exact validation rule are supplied. Do not implement Sprint 9.12 during this task.

## Problem Being Corrected

The Sprint 9.11 JSON and YAML manifests were both syntactically valid but did not parse to the same structure.

JSON stored verification results at:

`verification.verification_results`

YAML stored them at:

`verification_results`

The YAML result entries also used unquoted colon-space values such as:

`test_narration_request.py: passed`

A YAML parser interpreted those entries as one-key mappings rather than strings.

## Files Supplied

- `current_sprint_9.11_corrected.yaml`
- `WORKFLOW_manifest_consistency_update.md`
- `AGENTS_manifest_consistency_update.md`

## Required Actions

1. Copy `current_sprint_9.11_corrected.yaml` to `docs/current_sprint.yaml`.
2. Replace root `WORKFLOW.md` with the supplied workflow update.
3. Replace root `AGENTS.md` with the supplied agents update.
4. Validate `docs/current_sprint.json`.
5. Parse `docs/current_sprint.json` and `docs/current_sprint.yaml`.
6. Confirm the parsed nested structures are deeply equal.
7. Confirm `docs/current_sprint.md` still materially agrees with the corrected machine-readable manifests.
8. Confirm Sprint 9.11 remains Complete and Sprint 9.12 remains unstarted.
9. Stop.

## Boundaries

- Do not modify application code.
- Do not alter Sprint 9.11 implementation history.
- Do not change recorded verification results.
- Do not promote the Sprint 9.12 planning files.
- Do not begin Sprint 9.12.
