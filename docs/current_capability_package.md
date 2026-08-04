# Sprint 10.75 - Risk-Proportional Workflow Simplification

This is an explanatory package record. `docs/current_sprint.json` is the only
machine-enforced lifecycle authority.

## Status

Implementation is complete and the immutable Routine candidate awaits owner
review. Candidate acceptance and merge authorization are owner decisions, not
lifecycle fields.

## Goal

Simplify the maintained workflow to Critical and Routine levels; remove
redundant lifecycle gates and Markdown duplicate authority.

## Authorized Scope

- Governance guidance and lifecycle records.
- Project-record validator behavior and directly relevant fixtures.

## Exclusions

- Engine or gameplay behavior, movement, saves or save schema, Region Packs,
  provider code, dependencies, external GitWorkflowTools, `AINarrativeRPG.psd1`,
  and the offline behavioral test selection.

## Acceptance Criteria

- Critical work is limited to saves, migrations, Region Pack integrity,
  destructive mutation, movement semantics, security/provider boundaries, and
  repository/data-loss risk; it requires frozen scope, a feature branch,
  relevant integration verification, independent review, and owner-authorized
  strict-fast-forward merge.
- Routine work requires concise scope, a feature branch, targeted verification,
  and owner review and merge authorization. Independent review and evidence
  packets are optional unless requested.
- JSON is the only machine-enforced lifecycle authority; Markdown is
  explanatory and does not duplicate JSON lifecycle checks.
- Candidate and merge lifecycle states are removed. Normal merge needs no
  separate lifecycle-closeout package.
- Clerical corrections receive correction-only verification; non-contract
  hardening and style concerns are backlog items; one bounded correction cycle
  precedes an owner classification request.

## Required Verification

- Lifecycle validator tests and project-record fixtures.
- JSON parsing and save-version assertion through `\.venv\Scripts\python.exe`.
- `git diff --check`, changed-scope inspection, and final clean-state check.

No merge or push is authorized by this record.
