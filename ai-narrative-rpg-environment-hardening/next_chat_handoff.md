# Next Chat Handoff: ENV-HARDENING-001

## Current state

The active work is one bounded maintenance sprint: Windows Development Environment Hardening. The package was prepared in a separate Codex workspace because the AI Narrative RPG Engine repository was not attached to that task. The next Codex task must inspect the real repository before merging files.

Sprint status: `ready`

## Objective

Install and execute the hardening package so environment failures are detected at startup, official verification always uses `.\.venv\Scripts\python.exe`, Windows packaging is documented and validated, and provider-neutral deterministic project behavior remains unchanged.

## Authoritative files

- `current_sprint.md`
- `current_sprint.yaml`
- `current_sprint.json`
- `docs\workflow\ENVIRONMENT_HARDENING_SPRINT.md`
- `README_HARDENING.md`

The three sprint manifests must normalize to exactly the same structure.

## Required invariants

- Keep exactly one sprint active.
- Preserve all unrelated user changes.
- Do not rebuild or migrate the repository as part of this sprint.
- Use PowerShell on Windows.
- Use `.\.venv\Scripts\python.exe` as the only Python executable for official checks.
- Do not pipe Python programs through stdin.
- Do not use bundled, system, Store, or alternate Python to convert a blocked check into a pass.
- Preserve provider neutrality and deterministic behavior.
- Keep packaging evidence separate from test evidence.

## Start here

1. Read repository-level and nested `AGENTS.md` files.
2. Inspect existing sprint, workflow, test, package, handoff, ignore, and tool conventions.
3. Record branch, HEAD, and working-tree state; do not modify unrelated changes.
4. Read `README_HARDENING.md` and the bounded sprint definition.
5. Run `docs\codex_prompts\01_setup.md` from the repository root.
6. Continue through implementation, verification, and closeout prompts only when each phase's exit criteria are met.

## Required verification evidence

For every required check, record:

- exact command;
- exit code;
- pass, fail, or blocked;
- concise relevant output; and
- artifact path, when applicable.

At minimum, evidence must cover manifest agreement, PowerShell syntax, preflight, the repository's canonical tests through the official interpreter, and archive inspection if a package is produced.

## Closeout rule

Set the sprint to `complete` only if every required check passes. Otherwise use `blocked`, record the exact remaining condition, keep all three manifests synchronized, and do not define another sprint.

## Evidence log

Populate this section during execution.

| Check | Command | Exit code | Status | Evidence |
| --- | --- | ---: | --- | --- |
| Package validation | Pending | Pending | Pending | Pending |
| Environment preflight | Pending | Pending | Pending | Pending |
| Repository tests | Pending | Pending | Pending | Pending |
| Package inspection | Not yet required | N/A | Pending | Pending |

## Changed files

Populate during implementation. Distinguish package files, merged policy edits, and pre-existing user changes.

## Remaining risks

- Repository-specific paths and the canonical test arguments must be resolved in the actual repository.
- A failure of the official interpreter remains a blocker even if PowerShell packaging succeeds.
