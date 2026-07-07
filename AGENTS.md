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

## Verification
Treat application failures and tooling/runtime failures differently.

Application failures block the sprint.

If the only blocker is Codex's inability to execute the project's local runtime, request manual verification from the user. A successful manual verification is sufficient for sprint closeout.
