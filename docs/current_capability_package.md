# Review Packet Profiles and Fail-Closed Validation

Status: Complete — accepted by owner.

## Purpose and Owner-Visible Value

Ensure that a packet intended to support an architecture decision cannot be
mistaken for compact package-completion evidence. New packets declare their
purpose, preserve authoritative-source boundaries, and fail validation when
required decision context is absent.

## Included Internal Milestones

1. Sprint 10.40 — Packet Profile and Manifest Contract — complete.
2. Sprint 10.41 — Independent Assembly and Validation Tooling — complete.
3. Sprint 10.42 — Fixture Tests, Workflow Integration, and Package Closeout — complete and accepted.

The package is complete and accepted after the owner-requested corrections. No
engine capability or following package is staged.

## Scope, Ownership, and Compatibility

- This package changes workflow records, packet documentation, and PowerShell
  tooling only. It does not change engine, Region Pack, World State, narration,
  persistence, save/load, or save version behavior.
- `docs/architecture.md`, `docs/simulation_model.md`,
  `docs/simulation_principles.md`, `docs/roadmap.md`, and `docs/decisions.md`
  remain repository authorities. Packet-local synthesis is review convenience
  only and must pin its authoritative sources.
- New packets use only the approved profiles: `package-review`,
  `post-package-architecture-review`, and `phase-architecture-review`.
- Existing archives remain legacy, unprofiled historical artifacts. They are
  neither rebuilt nor required to meet the new contract.

## Exclusions

No game behavior, game data, generic document platform, next game capability,
roadmap selection, commit, merge, save migration, or historical archive rewrite
is included.

## Expected Files and Systems

- `docs/review_packet_profiles.md`
- `tools/assemble_review_packet.ps1`
- `tools/validate_review_packet.ps1`
- `tools/test_review_packet.ps1`
- `WORKFLOW.md`, `AGENTS.md`, and `docs/architecture_review_template.md`
- canonical package, sprint, architecture, decision, roadmap, sprint-log, and
  handoff records as required for closeout

## Architecture Decisions and Stop Conditions

Role-based packet membership, artifact-kind distinction, source-pinned
synthesis, independent archive validation, and legacy-only validation are
workflow boundaries for this package. Stop for a need to alter existing
architecture authority, create a generic documentation platform, change engine
behavior, or enter any `WORKFLOW.md` stop condition.

## Verification, Completion, and Rollback

Focused PowerShell fixture tests, valid and expected-failure packet validation,
legacy validation, official preflight, the full root test inventory, manifest
deep agreement, `git diff --check`, and independent final-archive validation
passed after the corrective validator, matrix, workflow, and packet evidence
work. The corrective boundary explicitly covers profile-specific
role/kind rules, Git identity consistency, substantive required content,
complete portable-path checks, and all independently identified malformed
fixtures. It also covers role-specific phase dependency, ADR-index, and
unresolved-decision-context contracts so a generic map cannot satisfy a phase
review packet.
Owner acceptance authorizes the final commit and fast-forward merge only; it
does not define or start a following package. The rollback boundary is this feature branch's workflow and tooling changes;
there is no data migration or runtime behavior to reverse.
