# WORKFLOW.md

## Sprint Lifecycle

1. Define the sprint.
2. Update:
   - current_sprint.md
   - current_sprint.yaml
   - current_sprint.json
3. Codex performs Startup Review.
4. Codex implements only the current sprint.
5. Run documented verification.
6. If verification passes:
   - Update documentation.
   - Perform sprint closeout.
7. Stop. Await the next sprint.

## Verification Policy

### Application Failure
- Code defects
- Test failures
- Unmet acceptance criteria

Result:
- Stop.

### Tool/Runtime Failure
Examples:
- Codex cannot launch the project virtual environment.
- Host runtime restrictions.
- Permission limitations unrelated to repository code.

Result:
- User runs the documented verification manually.
- Manual verification is authoritative for sprint closeout.
- Do not modify application code to work around tooling limitations.

## Documentation First
No sprint may begin unless current_sprint.md contains:
- Goal
- Expected Files
- Acceptance Criteria
- Verification

## Compact Chat Handoff

To reduce repeated full-document processing between ChatGPT planning sessions and Codex implementation sessions, each sprint closeout should produce or update a compact handoff file:

- docs/next_chat_handoff.md

This file is the default handoff artifact for starting a new ChatGPT planning chat. It should be concise and should not replace the full documentation set.

### Required Contents

The handoff file should include:

- Current completed sprint
- What was implemented
- Verification commands and results
- Files changed
- ADRs added or updated
- Current known constraints or unresolved concerns
- Current sprint status
- Whether the next sprint has or has not started
- Recommended next step, if known

### Size Limit

Keep docs/next_chat_handoff.md under 1500 words unless a larger handoff is explicitly needed.

### Default New-Chat Package

For normal sprint planning, attach or paste only:

- AGENTS.md
- PROJECT.md
- WORKFLOW.md
- TASK.md
- docs/next_chat_handoff.md
- docs/current_sprint.md
- docs/current_sprint.yaml
- docs/current_sprint.json

Attach the full docs package only for major architecture reviews, documentation audits, project restructuring, or when the compact handoff is insufficient.

### Rule

The full documentation archive is not the default new-chat handoff. The compact handoff is the default. Full docs remain authoritative but should be consulted only when needed.

## Staging File Cleanup Rule

When ChatGPT provides temporary planning, handoff, or documentation files for Codex to copy into the repository, Codex may delete those staging files only after confirming that their contents have been copied into the correct canonical repository files.

Codex must not delete canonical project documentation.

Examples of staging files that may be deleted after processing:

- current_sprint_9_6.md
- current_sprint_9_6.yaml
- current_sprint_9_6.json
- next_chat_handoff_9_6.md
- sprint_9_6_planning_files.zip

Examples of canonical files that must not be deleted:

- docs/current_sprint.md
- docs/current_sprint.yaml
- docs/current_sprint.json
- docs/next_chat_handoff.md
- docs/architecture.md
- docs/decisions.md
- docs/sprint_log.md
- WORKFLOW.md
- PROJECT.md
- AGENTS.md

Before deleting staging files, Codex must confirm:

1. The staged content has been copied into the intended canonical files.
2. docs/current_sprint.json validates if sprint manifests were changed.
3. The canonical files remain present in docs/.
4. The deletion affects only temporary staging/download files.

If there is uncertainty about whether a file is temporary or canonical, Codex must leave the file in place and report it instead of deleting it.

## Codex Task Routing Rule

Codex work should be split by task type so each run can use the lowest suitable model and reasoning level.

The default workflow should not require one Codex run to copy staging files, implement the sprint, verify behavior, update closeout documentation, and clean up temporary files. Those steps may be separated into smaller runs when doing so improves efficiency or reduces usage.

### Setup / Staging Tasks

Use mini, a lighter model, or low reasoning when available.

Use for:

- Copying sprint planning files into canonical `docs/` files.
- Validating `docs/current_sprint.json`.
- Deleting temporary staging files after validation.
- Simple documentation formatting.
- Confirming expected files are present.

Setup tasks must not implement sprint code.

### Normal Sprint Implementation

Use the standard Codex model with medium reasoning.

Use for:

- Implementing one bounded sprint.
- Adding narrow engine modules.
- Adding or updating tests tied to the current sprint.
- Adding narrow CLI or debug commands.
- Running official verification commands.

Normal implementation tasks must follow the current sprint definition and must not begin the next sprint.

### Closeout Tasks

Use mini, a lighter model, or low reasoning when available.

Use for:

- Updating closeout documentation.
- Updating ADRs.
- Updating `docs/sprint_log.md`.
- Marking current sprint manifests complete.
- Updating `docs/next_chat_handoff.md`.
- Validating `docs/current_sprint.json`.

Closeout tasks must not add new features.

### Debugging / Architecture Investigation

Use high reasoning only when needed.

Use for:

- Failed tests with unclear cause.
- Save/load consistency problems.
- History, time, or state mutation bugs.
- Cross-layer architecture issues.
- Repeated verification failures.

Do not use extra-high reasoning unless the issue remains unresolved after a focused high-reasoning debugging pass.

### Default Routing

If a task is mechanical, use mini or low reasoning.

If a task implements a bounded sprint, use medium reasoning.

If a task diagnoses unclear failures, use high reasoning.

### Preferred Split Workflow

When useful, split Codex work into separate runs:

1. Setup run: copy staged sprint files into canonical docs, validate JSON, delete staging files, then stop.
2. Implementation run: implement only the current sprint and run verification, then stop.
3. Closeout run: update documentation, mark the sprint complete, validate JSON, update handoff, then stop.
4. Debug run, only if needed: investigate failed tests or unclear architecture issues.

Each run should state its task type before beginning and should stop when that task type is complete.

