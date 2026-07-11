# Codex Prompt 02: Implementation

Use this prompt only after setup evidence is complete.

```text
Execute only the implementation phase of sprint ENV-HARDENING-001. Use the completed setup report and keep this as the sole active sprint.

Inspect the working tree again before editing. Preserve unrelated and overlapping user changes. If a new unexpected change directly conflicts with a required edit, pause and report the conflict instead of overwriting it.

Implement the smallest repository-specific merge of the hardening package:
- place tools/preflight.ps1 and tools/validate_hardening_package.ps1 at their canonical paths;
- install current_sprint.md, current_sprint.yaml, and current_sprint.json together after archiving the prior completed sprint according to repository policy;
- install or update next_chat_handoff.md;
- retain README_HARDENING.md and docs/workflow/ENVIRONMENT_HARDENING_SPRINT.md for this sprint;
- merge docs/workflow/AGENTS_WORKFLOW_PATCH.md into existing AGENTS.md and workflow guidance without replacing unrelated instructions; if no AGENTS.md exists, create a root file from the supplied snippet after checking for an equivalent repository-specific instruction file;
- keep the four phase prompts available at documented paths;
- establish .build, .artifacts, and handoffs as the only approved generated-file locations, adapting ignore rules narrowly to existing policy; and
- replace repository-specific placeholders such as canonical test arguments.

If paths change, update every path reference in all three manifests, README_HARDENING.md, next_chat_handoff.md, workflow guidance, and prompts. Keep the three manifests structurally identical.

Do not modify game, narrative, persistence, UI, model-provider, or deterministic runtime code. Do not upgrade dependencies unless a setup finding proves the existing declared environment cannot be installed and the repository owner has authorized that separate change. Do not rebuild the repository. Do not disable Windows security controls broadly.

For Python, use only .\.venv\Scripts\python.exe. No alternate Python substitution and no Python via stdin.

After edits, run only low-risk structural checks needed to catch editing mistakes, including the package validator. Do not claim full verification in this phase.

Finish with an implementation report containing:
- files added and changed;
- how existing user changes were preserved;
- policy sections merged;
- repository-specific placeholders resolved;
- any deviations from the package layout and all synchronized references;
- package-validator result; and
- remaining verification work.

Stop after the implementation report. Do not close the sprint or define another sprint.
```
