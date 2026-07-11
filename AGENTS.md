# AGENTS.md

## Purpose
Codex is the implementation agent.

### Responsibilities
- Read project documentation.
- Perform Startup Review.
- Implement only the current sprint.
- Run verification.
- Perform sprint closeout after successful verification.
- Never begin the next sprint automatically.

## Required Reads
- AGENTS.md
- PROJECT.md
- WORKFLOW.md
- TASK.md
- docs/current_sprint.md
- docs/current_sprint.yaml
- docs/current_sprint.json

## Startup Gate
Stop if current_sprint.md does not contain:
- Goal
- Expected Files
- Acceptance Criteria
- Verification
Also confirm the canonical current-sprint JSON and YAML manifests both parse successfully, represent the same data types, contain the same keys and nesting, preserve equivalent ordered list values, and deeply agree after parsing.

## Verification
Treat application failures and tooling/runtime failures differently.

Application failures block the sprint.

If the only blocker is Codex's inability to execute the project's local runtime, request manual verification from the user. A successful manual verification is sufficient for sprint closeout.

## Closeout
Before marking a sprint complete, confirm the canonical current-sprint JSON and YAML manifests both parse successfully, represent the same data types, contain the same keys and nesting, preserve equivalent ordered list values, and deeply agree after parsing. JSON syntax validation alone is not sufficient.

## Canonical Windows Environment
- Work from the repository root in PowerShell on Windows.
- The only official Python interpreter is `.\.venv\Scripts\python.exe`.
- Invoke small Python probes with `-c` and substantial logic from checked-in or generated script files. Do not pipe multiline Python programs through stdin.
- Do not substitute bundled, system, Windows Store, or alternate Python for setup, tests, validation, or closeout evidence.
- If the official interpreter cannot launch in Codex, preserve the exact command, exit code, and error. Classify an access-denied/process-creation failure as an agent execution-context limitation, not evidence that `.venv` is unhealthy.
- After such a limitation, provide copy-safe commands for the repository owner to run with the same official interpreter. User-provided output may satisfy verification when it identifies the official interpreter, command, result, and exit status where applicable; label that evidence user-executed.
- Run the environment preflight before implementation and closeout.

## Verification Evidence
- Run repository tests with `.\.venv\Scripts\python.exe` and record each command, exit code, outcome, and concise output.
- Never represent a fallback run as official verification.
- A failed required check prevents successful sprint closeout. A Codex-blocked check may be satisfied by clearly recorded user-executed evidence using the same official interpreter; alternate interpreters remain prohibited.

## Packaging and Project Invariants
- Use PowerShell `Compress-Archive` for Windows package creation and validate archive entries independently.
- Create generated content only under `.build\`, `.artifacts\`, or `handoffs\` according to repository policy.
- Packaging success is independent from application-test success.
- Preserve provider neutrality, deterministic behavior, exactly one active sprint, and unrelated user changes.
