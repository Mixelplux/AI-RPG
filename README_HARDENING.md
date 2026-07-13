# AI Narrative RPG Engine Environment Hardening

This package is a repository overlay for one bounded Windows maintenance sprint. It establishes repeatable environment checks without rebuilding the repository, changing game behavior, or binding the engine to a model provider.

## What is included

- Three structurally identical `current_sprint` manifests.
- A bounded sprint definition and next-task handoff.
- A PowerShell preflight that uses only `.\.venv\Scripts\python.exe` for Python checks.
- A no-dependency package validator.
- AGENTS and workflow merge snippets.
- Four Codex prompts for setup, implementation, verification, and closeout.

The `.yaml` file uses JSON syntax deliberately. JSON is valid YAML 1.2, so PowerShell can validate exact structural agreement before the project's Python environment is trusted.

## Step-by-step execution

### 1. Preserve the repository state

Open PowerShell in the AI Narrative RPG Engine repository. Review `git status` and make sure all current work is committed or otherwise backed up. Do not discard unrelated or uncommitted work for this maintenance sprint.

### 2. Keep this package outside the repository initially

Extract the ZIP into a temporary folder. Run the package validator from the extracted package root:

```powershell
pwsh -NoProfile -File .\tools\validate_hardening_package.ps1 -PackageRoot .
```

If `pwsh` is not installed but Windows PowerShell is available, the same script can be run with:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\validate_hardening_package.ps1 -PackageRoot .
```

The validator must report that all three manifests agree, required files exist, policy invariants hold, and both PowerShell scripts parse.

### 3. Confirm that this is the only sprint

Review the repository's existing sprint files. Archive the prior completed sprint according to the repository's existing workflow. Do not combine this maintenance sprint with feature work and do not define a second sprint.

If another sprint is active, finish or explicitly pause it before installing these manifests.

### 4. Merge the overlay into the repository root

Copy the package contents into the repository while preserving the directory structure. Treat these cases differently:

- New `tools` and `docs` files can be added at their listed paths.
- Existing `docs/current_sprint.md`, `docs/current_sprint.yaml`, and `docs/current_sprint.json` must be archived together, then replaced together.
- Existing `docs/next_chat_handoff.md` must be archived according to the repository workflow before replacement.
- Do not replace `AGENTS.md` or a workflow file wholesale. Merge the snippets in `docs\workflow\AGENTS_WORKFLOW_PATCH.md`.
- Keep this README as `README_HARDENING.md` during the sprint; it can be archived with closeout evidence later.

### 5. Adapt only path conventions

If the repository stores sprint or workflow files in a dedicated directory, relocate the files consistently and update every referenced path in all three manifests, prompts, handoff, and scripts. Then re-run the package validator.

Do not alter the official interpreter path:

```text
.\.venv\Scripts\python.exe
```

### 6. Merge the policy snippets

Follow `docs\workflow\AGENTS_WORKFLOW_PATCH.md`. Add the canonical toolchain rules to the nearest relevant sections in `AGENTS.md` and the repository workflow document. Avoid duplicate or contradictory policy sections.

### 7. Validate the installed package

From the repository root, run:

```powershell
pwsh -NoProfile -File .\tools\validate_hardening_package.ps1 -PackageRoot .
```

This does not use Python.

### 8. Run the environment preflight

Open `D:\AI RPG` directly as the active Codex workspace, or open `D:\AI RPG\AI RPG.code-workspace`. From the repository root, confirm the active Git root and run:

```powershell
git rev-parse --show-toplevel
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\preflight.ps1 -RepoRoot .
```

To require project-specific imports, add each import name explicitly:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\preflight.ps1 -RepoRoot . -RequiredPythonModule yaml,pydantic
```

The preflight path-normalizes the Git root, runs the official interpreter with the required minimal `-c` probe, and never searches for or substitutes another Python executable.

### 9. Resolve failures narrowly

For each failed check, record the check name, exact error, and proposed correction. Repair only the failing capability. Do not broadly disable Windows security controls and do not use another Python to claim official verification passed.

If the official interpreter is blocked, do not begin sprint implementation or treat packaging as a substitute for Python verification. Resolve the workspace-context preflight first.

Treat an access-denied or process-creation error from the official interpreter as a Codex workspace-context failure, not proof that `.venv` is unhealthy. Do not recreate `.venv`, change permissions, run Codex as Administrator, or substitute another interpreter. Reopen `D:\AI RPG` directly as the Codex workspace, or open `AI RPG.code-workspace`, then rerun the startup gate. Stop only while that preflight remains blocked; do not repeatedly ask the owner to approve the same diagnosis. Record whether validation was run by Codex or the owner and never claim blocked validation passed.

### 10. Execute the four Codex phases

Use these prompts in order:

1. `docs\codex_prompts\01_setup.md`
2. `docs\codex_prompts\02_implementation.md`
3. `docs\codex_prompts\03_verification.md`
4. `docs\codex_prompts\04_closeout.md`

Each prompt assumes the repository root is the working directory and the hardening sprint is the only active sprint.

### 11. Close accurately

Set the sprint to `complete` only if every required acceptance criterion and repository-defined official test passes. Use `blocked` when a required capability remains unavailable. Update all three manifests together, update `docs/next_chat_handoff.md` with exact evidence, and run the validator one final time.

Do not create the next sprint during this closeout.

## Expected result

After successful closeout, Codex can run a single preflight at the start of work and receive a precise capability report. Python verification always uses the project virtual environment, packaging uses a documented Windows-native path, and deterministic provider-neutral project rules remain unchanged.


