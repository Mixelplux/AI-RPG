# Next Chat Handoff: ENV-HARDENING-001

## Current state

The active work is one bounded maintenance sprint: Windows Development Environment Hardening. The package was prepared in a separate Codex workspace because the AI Narrative RPG Engine repository was not attached to that task. The next Codex task must inspect the real repository before merging files.

Sprint status: `complete`

## Objective

Install and execute the hardening package so environment failures are detected at startup, official verification always uses `.\.venv\Scripts\python.exe`, Windows packaging is documented and validated, and provider-neutral deterministic project behavior remains unchanged.

## Authoritative files

- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`
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
| Package validation | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\validate_hardening_package.ps1 -PackageRoot .` | 0 | Pass | 32 passed, 0 failed; manifests deeply agree and both scripts parse. `pwsh` is not installed, so the documented Windows PowerShell fallback was used. |
| Official interpreter identity | `.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"` | 0 | Pass (user-executed) | Repository-owner PowerShell output identifies `D:\AI RPG\.venv\Scripts\python.exe`, Python 3.13.14. This proves `.venv` is healthy and must not be recreated. |
| Environment preflight | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\preflight.ps1 -RepoRoot .` | 0 | Pass (user-executed) | 18 passed, 2 warnings, 0 blocked, 0 failures. Direct, `-c`, and file probes all used `D:\AI RPG\.venv\Scripts\python.exe`; the warnings were PowerShell 5.1 preference and the preserved dirty working tree. |
| Incorrect unittest discovery attempt | `.\.venv\Scripts\python.exe -m unittest discover -p "test_*.py"` | 5 | Invalid evidence (user-executed) | The command ran through the official interpreter but found zero tests. Repository tests are standalone assertion scripts, so this exposed and corrected a hardening command-resolution defect; it is not a game-test failure. |
| Repository standalone test suite | Sorted direct execution of every root `test_*.py` with `.\.venv\Scripts\python.exe` | 0 | Pass (user-executed) | All 12 standalone test files reported exit 0; aggregate `TEST_EXIT=0`. No alternate Python was used. |
| Package inspection | Not produced | N/A | Not applicable | No ZIP was produced during this bounded merge; packaging evidence remains separate from test evidence. |

## Changed files

- Package/policy files: `README_HARDENING.md`, `tools/preflight.ps1`, `tools/validate_hardening_package.ps1`, `docs/workflow/*`, `docs/codex_prompts/*`, `AGENTS.md`, `WORKFLOW.md`, and `.gitignore`.
- Canonical sprint/handoff files: `docs/current_sprint.md`, `.yaml`, `.json`, and `docs/next_chat_handoff.md`.
- Archived prior completed state: `docs/current_sprint_10_1.md`, `.yaml`, `.json`, and `docs/next_chat_handoff_10_1.md`.
- Pre-existing user changes preserved: the existing `WORKFLOW.md` modification, untracked `review_context.md`, and untracked `ai-narrative-rpg-environment-hardening/` staging directory.
- No product, provider, persistence, gameplay, or test code was changed.

## Manual verification bridge

Run these commands from `D:\AI RPG` in the repository owner's normal PowerShell session and return their complete output:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\preflight.ps1 -RepoRoot .
"PREFLIGHT_EXIT=$LASTEXITCODE"

$testExit = 0
Get-ChildItem -File -Filter "test_*.py" | Sort-Object Name | ForEach-Object {
    & .\.venv\Scripts\python.exe $_.FullName
    $fileExit = $LASTEXITCODE
    "TEST_FILE=$($_.Name) EXIT=$fileExit"
    if ($fileExit -ne 0) { $testExit = $fileExit }
}
"TEST_EXIT=$testExit"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\validate_hardening_package.ps1 -PackageRoot .
"PACKAGE_VALIDATION_EXIT=$LASTEXITCODE"
```

The package validator includes exact manifest agreement and PowerShell syntax validation, so no additional syntax/manifest command is required.

## Closeout

- ENV-HARDENING-001 is complete. Required Python checks passed as explicitly labeled user-executed verification through the same official interpreter after Codex recorded an agent execution-context limitation.
- `.venv` is healthy and was not deleted or recreated.
- The incorrect unittest-discovery attempt remains recorded as invalid evidence and was replaced by sorted direct execution of the repository's 12 standalone test scripts.
- Final package validation passed after closeout synchronization.
- No second sprint has been defined or started.

## Remaining risks

- Codex may still be unable to create the official Python process in its restricted execution context. Future tasks should use the documented manual-verification bridge rather than treating this as a broken `.venv`.


