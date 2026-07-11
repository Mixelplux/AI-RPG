# Codex Prompt 03: Verification

Use this prompt only after implementation is complete.

```text
Execute only the verification phase of sprint ENV-HARDENING-001. This remains the sole active sprint.

Read the implemented files and inspect the working tree before running checks. Verification must describe the repository as it actually exists; do not edit tests or product behavior to make checks pass.

Run and record these required checks from the repository root:

1. Package and manifest validation:
pwsh -NoProfile -File .\tools\validate_hardening_package.ps1 -PackageRoot .

2. Environment preflight:
pwsh -NoProfile -File .\tools\preflight.ps1 -RepoRoot .

3. The repository's canonical test command, using this executable exactly:
.\.venv\Scripts\python.exe <resolved canonical test arguments>

4. Any repository-defined deterministic validation commands, also using the official interpreter where Python is involved.

5. If a ZIP or handoff packet is created, use the documented PowerShell package command, list the archive entries, and compare them with the expected file set. Packaging evidence is separate from test evidence.

For every check, record the exact command, exit code, pass/fail/blocked status, concise relevant output, and artifact path when applicable.

Never invoke bundled, system, Windows Store, `uv`, or alternate Python for an official check. Do not send Python programs through stdin. Codex must attempt the official command first. If Codex receives an access-denied/process-creation error, record the exact command, exit code, and error as an agent execution-context limitation and provide a copy-safe command for the owner. User-provided output may satisfy the check only when it clearly shows the same official interpreter path, result, and exit status where applicable; label it user-executed. A PowerShell packaging success does not unblock Python checks.

Do not make product-code changes in verification. You may correct a clear typo in hardening documentation or scripts only if you document the edit and re-run every affected check. Do not weaken tests or acceptance criteria.

Finish with a verification report mapping every acceptance criterion to evidence. Clearly distinguish passed, failed, blocked, and not applicable. State whether closeout is eligible for complete or must be blocked.

Stop after the verification report. Do not update terminal sprint status or define another sprint.
```

