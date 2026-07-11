# Codex Prompt 01: Setup

Use this prompt from the AI Narrative RPG Engine repository root.

```text
Execute only the setup phase of sprint ENV-HARDENING-001. This is the sole active sprint.

First read every applicable AGENTS.md file, the repository workflow guidance, README_HARDENING.md, current_sprint.md/yaml/json, next_chat_handoff.md, and docs/workflow/ENVIRONMENT_HARDENING_SPRINT.md. Inspect the existing repository before editing anything.

Preserve all user changes. Record the repository root, current branch, HEAD commit, and working-tree status. Identify the canonical test command, package command, sprint/archive locations, generated-file policy, and existing virtual-environment guidance. If repository conventions require relocating package files, identify every reference that would need to change; do not relocate yet.

Run the package validator from the repository root:
pwsh -NoProfile -File .\tools\validate_hardening_package.ps1 -PackageRoot .

Run the preflight from the repository root:
pwsh -NoProfile -File .\tools\preflight.ps1 -RepoRoot .

For Python checks, use only .\.venv\Scripts\python.exe. Do not invoke bundled, system, Windows Store, or alternate Python. Do not pipe Python code through stdin. If the official interpreter fails, capture the exact command, exit code, and error and mark official verification blocked.

Do not change product code, dependencies, providers, game behavior, manifests, AGENTS.md, workflow files, ignore rules, or environment settings in this phase.

Finish with a setup report containing:
- repository baseline and pre-existing changes;
- discovered canonical commands and paths;
- package-validation result;
- each preflight result;
- conflicts or path adaptations required;
- narrowly scoped implementation actions; and
- explicit confirmation that no implementation edits were made.

Stop after the setup report. Do not begin implementation or define another sprint.
```
