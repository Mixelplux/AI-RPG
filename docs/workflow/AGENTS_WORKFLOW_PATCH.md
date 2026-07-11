# AGENTS and Workflow Patch Guide

Merge these sections into the repository's existing `AGENTS.md` and workflow documentation. Preserve existing instructions unless they conflict with this sprint's explicit toolchain policy. Do not replace either file wholesale.

## Merge procedure

1. Locate the nearest existing sections for environment setup, testing, packaging, generated files, sprint governance, and handoff.
2. Insert or reconcile the snippets below in those sections.
3. Replace duplicate rules with one unambiguous rule.
4. Keep repository-specific test arguments and paths where they are already canonical.
5. Do not weaken the official-interpreter or one-sprint requirements.
6. Run the package validator and preflight after merging.

If the repository has no applicable `AGENTS.md`, create a root `AGENTS.md` from the AGENTS snippet below after confirming that equivalent instructions are not stored under another repository-specific filename.

## AGENTS.md replacement snippet

```markdown
## Canonical Windows Environment

- Work from the repository root in PowerShell on Windows.
- The only official Python interpreter is `.\.venv\Scripts\python.exe`.
- Invoke small Python probes with `-c` and substantial logic from checked-in or generated script files. Do not pipe multiline Python programs through stdin.
- Do not substitute bundled, system, Windows Store, or alternate Python for setup, tests, validation, or closeout evidence.
- If Codex cannot launch the official interpreter, preserve the exact command, exit code, and error. An access-denied/process-creation failure is an agent execution-context limitation, not evidence that `.venv` is unhealthy.
- Provide copy-safe commands for the owner; clearly identified user-executed output using the same official interpreter may satisfy verification. Label it user-executed and never substitute another interpreter.
- Run `pwsh -NoProfile -File .\tools\preflight.ps1 -RepoRoot .` before implementation and closeout.

## Verification Evidence

- Use the repository's canonical test command with `.\.venv\Scripts\python.exe` as the executable.
- Record each required command, exit code, pass/fail/blocked status, and concise output.
- Never represent a fallback run as official verification.
- A failed required check prevents successful closeout. A Codex-blocked check requires passing user-executed evidence from the same official interpreter before closeout.

## Packaging

- Use PowerShell `Compress-Archive` for Windows package creation unless the repository defines a stricter canonical command.
- Create generated content only under `.build\`, `.artifacts\`, or `handoffs\` according to repository policy.
- Validate archive entries and expected files after creation.
- Packaging success is independent from application-test success.

## Project Invariants

- Keep the engine provider-neutral; environment work must not introduce a provider dependency.
- Preserve deterministic runtime and validation behavior.
- Maintain exactly one active sprint. Do not start or define another sprint during implementation or closeout.
- Preserve unrelated user changes and avoid destructive repository operations.
```

## Workflow document replacement snippet

```markdown
## Environment Gate

Every sprint phase begins from the repository root. Before implementation, run the package validator and environment preflight. Resolve failures narrowly and record unsupported capabilities explicitly.

1. Validate sprint manifests and PowerShell syntax:
   `pwsh -NoProfile -File .\tools\validate_hardening_package.ps1 -PackageRoot .`
2. Validate the Windows development environment:
   `pwsh -NoProfile -File .\tools\preflight.ps1 -RepoRoot .`
3. Run every root `test_*.py` file directly, in sorted order, with the official interpreter and record each exit code. These are standalone assertion scripts, not unittest-discoverable modules.
4. Record exact commands, exit codes, outcomes, and artifact paths.

No alternate Python may satisfy steps 2 or 3. PowerShell packaging is allowed as a separate operation and must be independently validated.

## Sprint State Synchronization

`docs/current_sprint.md`, `docs/current_sprint.yaml`, and `docs/current_sprint.json` describe one active sprint and must remain structurally identical. Update them together, then run the package validator. Closeout may set the sprint to `complete` or `blocked`; it may not define the next sprint.
```

## Optional ignore-file snippet

Add only entries compatible with the repository's existing artifact policy:

```gitignore
.build/
.artifacts/
```

Do not ignore `handoffs\` if handoff records are version-controlled. If only ZIP outputs inside `handoffs\` are disposable, use a narrow archive pattern instead of ignoring the directory.

## Repository-specific fields to resolve

Before closeout, replace these placeholders in existing workflow text:

- A sorted PowerShell loop that invokes each root `test_*.py` file directly with `.\.venv\Scripts\python.exe` and aggregates exit codes.
- Any package entry expectations with the repository's actual packet layout.
- Any relocated sprint-document paths with the chosen canonical paths in all three manifests.

The official interpreter itself is not a placeholder and must remain `.\.venv\Scripts\python.exe`.


