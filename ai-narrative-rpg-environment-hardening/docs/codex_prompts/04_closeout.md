# Codex Prompt 04: Closeout

Use this prompt only after a complete verification report exists.

```text
Execute only the closeout phase of sprint ENV-HARDENING-001. Do not define or start another sprint.

Read the setup, implementation, and verification evidence. Inspect the final working tree. Re-run a required check only if evidence is missing, stale, or affected by a closeout edit.

Determine the terminal status honestly:
- complete only if every required acceptance criterion and repository-defined official check passed;
- blocked if any required check failed, could not run, used an unauthorized interpreter, or lacks evidence.

Update current_sprint.md, current_sprint.yaml, and current_sprint.json together so they remain structurally identical. Update status only to complete or blocked. If the repository schema includes evidence fields, add the same normalized evidence to all three. Keep next_sprint null and do not route future feature work.

Update next_chat_handoff.md with:
- terminal sprint status;
- exact command, exit code, and outcome for every required check;
- changed files, including merged AGENTS/workflow sections;
- pre-existing user changes that were preserved;
- generated artifact paths and archive inspection result;
- unresolved blocker and safest next action, if blocked; and
- residual risks or testing gaps.

Run the package validator one final time:
pwsh -NoProfile -File .\tools\validate_hardening_package.ps1 -PackageRoot .

If final validation fails, correct only the hardening documentation or manifest synchronization issue and re-run it. Do not use alternate Python. Do not mark complete while validation is failing.

Finish with a concise closeout report containing the terminal status, solution summary, changed-file summary, verification evidence, preserved user work, artifact locations, and any blocker. Explicitly confirm that no second sprint was created.
```
