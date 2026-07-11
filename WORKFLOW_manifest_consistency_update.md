# WORKFLOW.md

## Sprint Lifecycle

1. Define the next sprint without beginning implementation.
2. ChatGPT prepares temporary, sprint-numbered planning files:
   - `current_sprint_<sprint>.md`
   - `current_sprint_<sprint>.yaml`
   - `current_sprint_<sprint>.json`
   - `next_chat_handoff_<sprint>.md`
3. Codex performs a setup/staging pass:
   - Copy the sprint-numbered planning content into the canonical documentation files.
   - Confirm the Markdown materially agrees with the machine-readable manifests, and confirm the YAML and JSON manifests parse to deeply equivalent structures.
   - Validate `docs/current_sprint.json`.
   - Confirm the canonical files remain present.
   - Delete only the temporary staging files after successful promotion and validation.
4. Codex performs Startup Review using the canonical repository files.
5. Codex implements only the current sprint.
6. Run documented verification.
7. If verification passes:
   - Update documentation.
   - Perform sprint closeout.
8. Stop. Await the next sprint.

## Canonical and Staging File Rule

The permanent authoritative sprint paths are:

- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`
- `docs/next_chat_handoff.md`

ChatGPT planning packages must not use these permanent filenames as direct-download replacements unless the user explicitly requests a direct replacement workflow.

The default planning-package filenames must include the sprint number:

- `current_sprint_<sprint>.md`
- `current_sprint_<sprint>.yaml`
- `current_sprint_<sprint>.json`
- `next_chat_handoff_<sprint>.md`

These numbered files are temporary staging artifacts. Codex promotes their contents into the canonical files during the setup/staging pass.

The canonical files keep stable names so all tools know where to find the active sprint. The sprint-numbered files exist only to make handoff intent explicit and prevent accidental ambiguity.

Before changing file naming, packaging, promotion, validation, or cleanup behavior, consult this workflow and the most recent prior sprint handoff. Do not silently replace an established handoff procedure with a new one.

## Planning Package Promotion Rule

Before sprint implementation begins, Codex must:

1. Copy:
   - `current_sprint_<sprint>.md` to `docs/current_sprint.md`
   - `current_sprint_<sprint>.yaml` to `docs/current_sprint.yaml`
   - `current_sprint_<sprint>.json` to `docs/current_sprint.json`
   - `next_chat_handoff_<sprint>.md` to `docs/next_chat_handoff.md`
2. Confirm the three sprint manifests materially agree.
3. Validate:

```powershell
.\.venv\Scripts\python.exe -m json.tool docs/current_sprint.json
```

4. Confirm all four canonical files exist.
5. Delete the temporary sprint-numbered files only after all prior steps succeed.
6. Stop and report a blocker if promotion or validation fails. Do not begin implementation from partially promoted manifests.

## Sprint Manifest Structural Equivalence Rule

`docs/current_sprint.json` and `docs/current_sprint.yaml` are machine-readable twins. They must parse to the same nested data structure, including:

- the same keys and nesting;
- the same list ordering;
- the same scalar types;
- the same string values;
- the same status, files, acceptance criteria, verification commands, verification results, non-goals, and task-routing data.

JSON syntax validation alone is not sufficient. YAML validity alone is not sufficient.

YAML values containing a colon followed by a space must remain strings when the JSON value is a string. They must be safely quoted or emitted by a serializer so entries such as `test_name.py: passed` do not become unintended YAML mappings.

The preferred method is to generate JSON and YAML from one shared canonical data structure. If either file is edited independently, both must be parsed and deeply compared before promotion, implementation, or closeout may proceed.

`docs/current_sprint.md` remains the human-readable manifest. It must materially represent the same sprint number, status, goal, expected and actual files, acceptance criteria, verification, non-goals, and next-sprint boundary, but it is not required to have the same structural shape as JSON and YAML.

A structural mismatch blocks staging promotion and sprint closeout. Do not report that the manifests agree until the deep comparison succeeds.

## Verification Policy

### Application Failure

Examples:

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

No sprint may begin unless `docs/current_sprint.md` contains:

- Goal
- Expected Files
- Acceptance Criteria
- Verification

The Markdown current-sprint manifest must materially agree with the machine-readable manifests, and the YAML and JSON current-sprint manifests must parse to deeply equivalent structures before implementation begins.

## User-Effort Minimization Rule

The workflow should minimize repeated user instructions and unnecessary manual file handling.

When ChatGPT or Codex identifies a repeated process instruction that is:

- safe;
- consistent with existing architecture and governance;
- broadly applicable to future sprints;
- unlikely to create ambiguity; and
- suitable for automation or permanent documentation,

the instruction should be added to the appropriate canonical workflow or governance document instead of requiring the user to repeat it in future prompts.

Examples include:

- stable planning-package naming;
- staging-file promotion and cleanup;
- standard verification commands;
- recurring handoff contents;
- model/task routing conventions;
- repeated documentation checks.

Do not permanently change the workflow for:

- one-time preferences;
- sprint-specific implementation details;
- ambiguous instructions;
- unverified assumptions;
- changes that weaken safety, verification, or architecture boundaries.

When a proposed workflow improvement would materially change project governance or create risk, present it for user approval before adopting it.

ChatGPT should default to the lowest-burden safe process and should not ask the user to repeat information already recorded in project documentation.

## Compact Chat Handoff

To reduce repeated full-document processing between ChatGPT planning sessions and Codex implementation sessions, each sprint closeout should produce or update a compact handoff file:

- `docs/next_chat_handoff.md`

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

Keep `docs/next_chat_handoff.md` under 1500 words unless a larger handoff is explicitly needed.

### Default New-Chat Package

For normal sprint planning, attach or paste only:

- `AGENTS.md`
- `PROJECT.md`
- `WORKFLOW.md`
- `TASK.md`
- `docs/next_chat_handoff.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`

Attach the full docs package only for major architecture reviews, documentation audits, project restructuring, or when the compact handoff is insufficient.

### Rule

The full documentation archive is not the default new-chat handoff. The compact handoff is the default. Full docs remain authoritative but should be consulted only when needed.

## Staging File Cleanup Rule

When ChatGPT provides temporary planning, handoff, or documentation files for Codex to copy into the repository, Codex may delete those staging files only after confirming that their contents have been copied into the correct canonical repository files.

Codex must not delete canonical project documentation.

Examples of staging files that may be deleted after processing:

- `current_sprint_<sprint>.md`
- `current_sprint_<sprint>.yaml`
- `current_sprint_<sprint>.json`
- `next_chat_handoff_<sprint>.md`
- `sprint_<sprint>_planning_files.zip`

Examples of canonical files that must not be deleted:

- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`
- `docs/next_chat_handoff.md`
- `docs/architecture.md`
- `docs/decisions.md`
- `docs/sprint_log.md`
- `WORKFLOW.md`
- `PROJECT.md`
- `AGENTS.md`

Before deleting staging files, Codex must confirm:

1. The staged content has been copied into the intended canonical files.
2. `docs/current_sprint.json` validates if sprint manifests were changed.
3. The canonical files remain present in `docs/`.
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
- Parsing and deeply comparing `docs/current_sprint.json` and `docs/current_sprint.yaml`.
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
- Parsing and deeply comparing `docs/current_sprint.json` and `docs/current_sprint.yaml`.

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

### Planning and Prompt Enforcement

The task-routing rules must be actively applied, not merely documented.

For each new sprint, ChatGPT must determine whether the work should be split into separate setup, implementation, closeout, or debugging runs.

Planning packages and Codex instructions must:

- identify the task type for each proposed run;
- recommend the lowest suitable model or reasoning level;
- keep mechanical setup and closeout work separate from implementation when that reduces usage or avoids unnecessary reasoning;
- use the standard model with medium reasoning for bounded sprint implementation;
- reserve high reasoning for unclear failures, architecture investigation, or repeated verification problems;
- avoid requiring the user to restate this routing preference.

If one combined run is recommended instead, the handoff must state why combining the work is safer or more efficient than splitting it.

This routing requirement applies beginning with the next sprint that has not already started.

### Preferred Split Workflow

When useful, split Codex work into separate runs:

1. Setup run: copy staged sprint files into canonical docs, validate JSON, delete staging files, then stop.
2. Implementation run: implement only the current sprint and run verification, then stop.
3. Closeout run: update documentation, mark the sprint complete, validate JSON, update handoff, then stop.
4. Debug run, only if needed: investigate failed tests or unclear architecture issues.

Each run should state its task type before beginning and should stop when that task type is complete.
