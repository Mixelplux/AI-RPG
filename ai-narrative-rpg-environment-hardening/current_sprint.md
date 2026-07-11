# Current Sprint: Windows Development Environment Hardening

This file is the human-facing view of the single active maintenance sprint. The JSON block below is canonical machine data and must remain structurally identical to `current_sprint.json` and `current_sprint.yaml`.

The `.yaml` manifest intentionally uses JSON syntax. JSON is valid YAML 1.2, which allows exact validation with built-in PowerShell and no bootstrap dependency on Python or a YAML package.

<!-- CANONICAL-MANIFEST-START -->
```json
{
  "schema_version": "1.0.0",
  "document_type": "current_sprint",
  "sprint_count": 1,
  "project": {
    "name": "AI Narrative RPG Engine",
    "principles": [
      "provider-neutral",
      "deterministic-core",
      "reproducible-verification"
    ]
  },
  "sprint": {
    "id": "ENV-HARDENING-001",
    "title": "Windows Development Environment Hardening",
    "type": "bounded-maintenance",
    "mode": "single-sprint",
    "status": "ready",
    "objective": "Make repository setup, validation, packaging, and Codex execution predictable on Windows without changing game behavior or provider abstractions.",
    "platform": {
      "operating_system": "Windows",
      "shell": "PowerShell",
      "official_interpreter": ".\\.venv\\Scripts\\python.exe",
      "python_invocation_policy": "Direct executable calls using -c or checked-in script files; no Python programs supplied through stdin.",
      "packaging_command": "Compress-Archive"
    },
    "governance": [
      "Exactly one sprint is active.",
      "Do not add product features or change runtime game behavior.",
      "Do not substitute bundled, system, Windows Store, or alternate Python for official verification.",
      "A packaging fallback may change implementation only when artifact contents are unchanged and independently validated.",
      "Preserve provider-neutral interfaces and deterministic project behavior.",
      "Do not close the sprint with unverified required checks."
    ],
    "in_scope": [
      "Add and document a canonical Windows toolchain and invocation policy.",
      "Add a PowerShell preflight that checks the repository, official interpreter, Git, writable artifact locations, required documents, and ZIP support.",
      "Validate the Markdown, YAML, and JSON sprint manifests for exact structural agreement.",
      "Define approved generated-file locations: .build, .artifacts, and handoffs.",
      "Patch AGENTS.md and workflow guidance with official verification and failure-handling rules.",
      "Create setup, implementation, verification, and closeout prompts.",
      "Record evidence and prepare a deterministic handoff."
    ],
    "out_of_scope": [
      "Gameplay, narrative, model-provider, UI, content, or persistence features.",
      "Dependency upgrades unrelated to making the existing environment runnable.",
      "A destructive repository rebuild or migration.",
      "Disabling antivirus, endpoint protection, or Windows security controls broadly.",
      "Changing canonical tests to accommodate an alternate interpreter.",
      "Starting or defining a second sprint."
    ],
    "deliverables": [
      {
        "path": "README_HARDENING.md",
        "purpose": "Step-by-step installation and execution guide."
      },
      {
        "path": "current_sprint.md",
        "purpose": "Human-readable canonical sprint manifest with embedded machine data."
      },
      {
        "path": "current_sprint.yaml",
        "purpose": "YAML 1.2-compatible canonical sprint manifest."
      },
      {
        "path": "current_sprint.json",
        "purpose": "JSON canonical sprint manifest."
      },
      {
        "path": "next_chat_handoff.md",
        "purpose": "Continuation contract for the next Codex task."
      },
      {
        "path": "docs/workflow/ENVIRONMENT_HARDENING_SPRINT.md",
        "purpose": "Bounded maintenance sprint definition."
      },
      {
        "path": "docs/workflow/AGENTS_WORKFLOW_PATCH.md",
        "purpose": "Merge instructions and replacement policy snippets."
      },
      {
        "path": "docs/codex_prompts/01_setup.md",
        "purpose": "Setup-phase Codex prompt."
      },
      {
        "path": "docs/codex_prompts/02_implementation.md",
        "purpose": "Implementation-phase Codex prompt."
      },
      {
        "path": "docs/codex_prompts/03_verification.md",
        "purpose": "Verification-phase Codex prompt."
      },
      {
        "path": "docs/codex_prompts/04_closeout.md",
        "purpose": "Closeout-phase Codex prompt."
      },
      {
        "path": "tools/preflight.ps1",
        "purpose": "Official environment preflight."
      },
      {
        "path": "tools/validate_hardening_package.ps1",
        "purpose": "No-dependency package, manifest, and PowerShell syntax validator."
      }
    ],
    "acceptance_criteria": [
      "The three current_sprint manifests normalize to the same data structure.",
      "The manifest declares exactly one bounded maintenance sprint.",
      "The preflight invokes only .\\.venv\\Scripts\\python.exe for Python checks.",
      "Direct interpreter, -c, and file-based Python probes pass in the target repository.",
      "Git status, required workflow files, writable generated-file locations, JSON support, and Compress-Archive are checked.",
      "PowerShell syntax validation reports no parser errors for package scripts.",
      "Repository-defined tests run through the official interpreter and their exact commands and results are recorded.",
      "No product behavior, provider binding, or deterministic runtime behavior changes.",
      "AGENTS.md and workflow documentation contain the official verification and fallback policies.",
      "Closeout records failures honestly and leaves no required check represented as passed when it did not run."
    ],
    "verification": {
      "commands": [
        {
          "id": "package_validation",
          "command": "pwsh -NoProfile -File .\\tools\\validate_hardening_package.ps1 -PackageRoot .",
          "required": true
        },
        {
          "id": "environment_preflight",
          "command": "pwsh -NoProfile -File .\\tools\\preflight.ps1 -RepoRoot .",
          "required": true
        },
        {
          "id": "project_tests",
          "command": ".\\.venv\\Scripts\\python.exe <arguments from the repository's canonical test command>",
          "required": true,
          "resolve_before_execution": true
        }
      ],
      "evidence": [
        "Exact command line",
        "Exit code",
        "Pass, fail, or blocked status",
        "Relevant output summary",
        "Artifact path when applicable"
      ],
      "failure_policy": [
        "If the official interpreter cannot launch, official verification is blocked.",
        "Do not use another Python executable to turn a blocked check into a pass.",
        "Diagnose and record the exact failure before changing the environment.",
        "Packaging may use documented PowerShell behavior, but the archive must be independently inspected and validated.",
        "A required blocked or failed check prevents successful sprint closeout."
      ]
    },
    "execution_phases": [
      {
        "id": "setup",
        "goal": "Baseline the repository and confirm package integrity before merging files.",
        "exit_criteria": "Existing work is preserved, package validation passes, and preflight failures are captured without substitution."
      },
      {
        "id": "implementation",
        "goal": "Merge the hardening assets and policy into the repository with minimal scoped changes.",
        "exit_criteria": "Required files and policy sections exist, paths match repository conventions, and no product code changed."
      },
      {
        "id": "verification",
        "goal": "Run syntax, manifest, preflight, and repository-defined checks using the canonical toolchain.",
        "exit_criteria": "Every required check has recorded evidence and no alternate Python was used."
      },
      {
        "id": "closeout",
        "goal": "Reconcile documentation and handoff state without opening another sprint.",
        "exit_criteria": "All three manifests agree, the handoff is current, and the sprint status accurately reflects verification."
      }
    ],
    "closeout": {
      "allowed_terminal_statuses": [
        "complete",
        "blocked"
      ],
      "requirements": [
        "Update all three current_sprint manifests together.",
        "Re-run package validation after status or evidence changes.",
        "Summarize changed files and retained user changes.",
        "Record exact verification evidence in next_chat_handoff.md.",
        "Do not define a next sprint during this maintenance sprint."
      ],
      "next_sprint": null
    }
  }
}
```
<!-- CANONICAL-MANIFEST-END -->
