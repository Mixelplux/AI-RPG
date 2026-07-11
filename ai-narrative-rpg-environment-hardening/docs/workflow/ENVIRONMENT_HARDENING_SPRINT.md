# ENV-HARDENING-001: Windows Development Environment Hardening

## Sprint contract

This is one bounded maintenance sprint for the AI Narrative RPG Engine. Its purpose is to make the current Windows development environment observable, repeatable, and honest about failures. It does not authorize product development, architecture changes, or a repository rebuild.

## Objective

Establish a canonical PowerShell workflow that validates the repository and its official `.\.venv\Scripts\python.exe` interpreter before implementation, uses deterministic file-based checks, provides an approved packaging route, and leaves reproducible evidence for subsequent Codex tasks.

## Non-negotiable constraints

- Exactly one sprint is active.
- Official Python verification uses `.\.venv\Scripts\python.exe` only.
- Python code is invoked with `-c` for small probes or from a script file; no multiline programs are piped through stdin.
- Bundled, system, Windows Store, or alternate Python may not substitute for official verification.
- `Compress-Archive` is the canonical Windows packaging command for this sprint.
- A packaging success does not imply Python verification success.
- Provider-neutral interfaces and deterministic runtime behavior are preserved.
- Existing user changes are preserved.
- Broad security-control disabling is outside scope.

## Work breakdown

### Setup

- Record repository root, branch, HEAD, and working-tree status.
- Identify existing AGENTS, workflow, test, packaging, and sprint conventions.
- Preserve current sprint and handoff history before replacement.
- Run `tools\validate_hardening_package.ps1` before relying on package content.
- Run `tools\preflight.ps1` and record every result without substituting tools.

### Implementation

- Install the sprint manifests, preflight, validator, prompts, and workflow documentation.
- Merge policy snippets into existing guidance rather than replacing unrelated content.
- Ensure `.build\`, `.artifacts\`, and `handoffs\` are approved generated-file locations.
- Update ignore rules only where generated content should not be versioned, following existing repository policy.
- Resolve environment failures with the smallest correction supported by evidence.
- Keep application and provider code unchanged.

### Verification

- Validate all three sprint manifests for exact structural agreement.
- Parse all included PowerShell scripts with the PowerShell language parser.
- Run the preflight from the repository root.
- Resolve and execute the repository's canonical test command through `.\.venv\Scripts\python.exe`.
- Validate each generated ZIP by listing entries and checking expected paths.
- Record the exact command, exit code, status, and concise output for every required check.

### Closeout

- Reconcile all documentation with actual behavior.
- Set sprint status to `complete` only if all required checks pass; otherwise use `blocked` and describe the remaining condition.
- Update all three manifests together and validate them again.
- Update `next_chat_handoff.md` with evidence and remaining risks.
- Do not create or route a second sprint.

## Acceptance criteria

The authoritative acceptance criteria are in the three `current_sprint` manifests. In practical terms, completion requires:

- exact manifest agreement;
- clean PowerShell parsing;
- a passing official-interpreter preflight;
- passing repository-defined official tests;
- merged AGENTS and workflow policies;
- no product, provider, or deterministic behavior changes; and
- complete verification evidence.

## Stop conditions

Pause implementation and record the issue if:

- another active sprint would be overwritten;
- the repository conventions materially conflict with the package layout;
- unexpected user changes overlap a file being edited;
- the official interpreter remains blocked after a narrowly scoped diagnosis; or
- completion would require disabling security controls or changing application behavior.

A stop condition does not authorize a fallback interpreter. It changes the sprint outcome to blocked until the repository owner chooses a safe next action.
