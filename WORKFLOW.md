# WORKFLOW.md

## Sprint Lifecycle

## Environment Gate

Every sprint phase begins from the repository root in PowerShell. Before implementation and closeout:

1. Validate sprint manifests and PowerShell syntax with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\validate_hardening_package.ps1 -PackageRoot .` when `pwsh` is unavailable.
2. Validate the Windows environment with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\preflight.ps1 -RepoRoot .` when `pwsh` is unavailable.
3. Run the repository's documented test files with `.\.venv\Scripts\python.exe` only.
4. Record exact commands, exit codes, outcomes, and artifact paths.

No alternate Python may satisfy environment or test verification. PowerShell packaging is a separate operation and must be independently inspected. The canonical sprint files under `docs/` must remain synchronized; closeout may set the sole sprint to `complete` or `blocked` and may not define another sprint.

### Manual Verification Bridge

Codex must attempt each official `.\.venv\Scripts\python.exe` command first. If its execution context denies process creation, Codex records the exact command, exit code, and error, classifies the result as an agent execution-context limitation rather than an unhealthy virtual environment, and provides copy-safe commands for the repository owner. User-provided output may satisfy the check when it clearly shows the same official interpreter path, command result, and exit status where applicable. Closeout must label this evidence as user-executed, not Codex-executed. System, bundled, Store, `uv`, or other Python installations may not substitute.

1. Define the next sprint without beginning implementation.
2. ChatGPT prepares temporary, sprint-numbered planning files:
   - `current_sprint_<sprint>.md`
   - `current_sprint_<sprint>.yaml`
   - `current_sprint_<sprint>.json`
   - `next_chat_handoff_<sprint>.md`
3. Codex performs a setup/staging pass:
   - Copy the sprint-numbered planning content into the canonical documentation files.
   - Confirm the Markdown, YAML, and JSON sprint manifests materially agree.
   - Confirm the canonical JSON and YAML sprint manifests both parse successfully, represent the same data types, contain the same keys and nesting, preserve equivalent ordered list values, and deeply agree after parsing. JSON syntax validation alone is not sufficient.
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

### Zip Handoff Handling

When a sprint handoff arrives as a zip archive, Codex handles the archive directly:

1. Inspect the archive contents.
2. Extract any required staging files into the workspace if needed.
3. Promote the staged content into the canonical repository files.
4. Validate the promoted files using the normal workflow checks.
5. Keep the user out of manual unzip and file-copy work unless a specific archive is malformed or blocked by tooling.

Do not require the user to extract sprint handoff zip files manually when Codex can process them in the workspace.

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
3. Confirm the canonical JSON and YAML sprint manifests both parse successfully, represent the same data types, contain the same keys and nesting, preserve equivalent ordered list values, and deeply agree after parsing. JSON syntax validation alone is not sufficient.
4. Validate:

```powershell
.\.venv\Scripts\python.exe -m json.tool docs/current_sprint.json
```

5. Confirm all four canonical files exist.
6. Delete the temporary sprint-numbered files only after all prior steps succeed.
7. Stop and report a blocker if promotion or validation fails. Do not begin implementation from partially promoted manifests.

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
- Manual verification using the same official interpreter is authoritative for sprint closeout when the returned evidence identifies the interpreter, command, result, and exit status where applicable.
- Record it explicitly as user-executed verification; do not relabel it as Codex-executed.
- Do not modify application code to work around tooling limitations.

## Documentation First

No sprint may begin unless `docs/current_sprint.md` contains:

- Goal
- Expected Files
- Acceptance Criteria
- Verification

The Markdown, YAML, and JSON current-sprint manifests must materially agree before implementation begins.
The canonical JSON and YAML current-sprint manifests must both parse successfully, represent the same data types, contain the same keys and nesting, preserve equivalent ordered list values, and deeply agree after parsing. JSON syntax validation alone is not sufficient.

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

## Sprint-Transition Review Packet

When a sprint closes and the next chat needs broader context than the compact handoff provides, Codex should create one standardized upload package for the next review chat.

This package should be created once per transition and should be the primary artifact used to start the next ChatGPT review conversation.

### Immediate Packaging Rule

The preferred handoff between sprint closeout and the next review chat is a single ZIP file generated by Codex.

The ZIP should include a compact review summary plus only the files needed for the next review scope. The goal is to avoid manual file picking in ChatGPT while still keeping the package bounded and explainable.

### Package Modes

Use one of two package modes:

- **Normal sprint packet**
  - For routine sprint transitions, implementation follow-ups, and compact planning chats.
  - Keep this small and focused on the current sprint plus the minimal dependency chain.

- **Architecture review packet**
  - For phase reviews, milestone reviews, documentation audits, or scope decisions.
  - Include the current architecture and decision context needed to evaluate the next direction.

The active mode should be named explicitly in the package manifest so the next chat knows why the packet was assembled.

### Required Packet Contents

Every review packet should include:

- A `review_context.md` file that explains the completed sprint or review state, the clean-tree or closeout status, what changed, what was verified, what remains deferred, and what the next decision needs to answer.
- `docs/next_chat_handoff.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`

The rest of the packet depends on the mode:

- **Normal sprint packet**
  - `docs/architecture.md`
  - `docs/decisions.md`
  - `docs/roadmap.md`
  - Files changed in the completed sprint
  - Tests changed in the completed sprint
  - Direct dependencies of the current sprint scope

- **Architecture review packet**
  - `docs/architecture.md`
  - `docs/decisions.md`
  - `docs/roadmap.md`
  - `docs/sprint_log.md`
  - `docs/simulation_model.md`
  - `docs/simulation_principles.md`
  - `docs/future_design.md`
  - `docs/project_structure.md`
  - Files changed in the most relevant recent sprint or milestone
  - Direct dependency files needed to evaluate the next architectural choice
  - Focused tests relevant to the decision under review
  - Relevant data files when mutable state ownership or region representation is under review

### Codex Selection Logic

Codex should choose packet contents by starting with the actual change set and then expanding only as needed.

Recommended selection order:

1. Read the most recent sprint diff and changed-file list.
2. Include the files directly modified in that sprint.
3. Include the lowest-level ownership and persistence files touched by those changes.
4. Include the immediate facade or coordinator files that route those changes.
5. Include focused tests that prove the behavior or protect the boundary.
6. Add documentation files needed for the review goal.
7. Add data files only when they materially affect the next architectural choice.

The packet should explain any additional file that was added beyond the immediate diff so the next chat can see why it matters.

The simplest reliable source for selection is the Git diff plus direct imports or ownership dependencies. Codex should not default to whole-repository uploads.

### Review Context File

`review_context.md` should be the human-readable entry point for the packet.

It should summarize:

- Completed sprint or milestone
- Git commit or clean-tree status
- What was implemented or reviewed
- What was verified
- Files included in the packet
- Open architectural questions
- Deferred systems
- Recommended next step
- Whether the next sprint has already started

This file should make the next chat usable even before the rest of the packet is opened.

### Default Next-Chat Package

For routine sprint planning, the next chat should usually receive only:

- `AGENTS.md`
- `PROJECT.md`
- `WORKFLOW.md`
- `TASK.md`
- `docs/next_chat_handoff.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`

Use the larger review packet only when the next chat is doing architecture review, milestone selection, documentation audit, or another decision-heavy transition.

### Long-Term Automation Plan

The review packet should eventually be generated by a repository script instead of assembled manually.

Target script:

- `tools/build_review_packet.py`

Suggested modes:

- `--mode sprint`
- `--mode architecture`

Suggested responsibilities:

1. Read the current Git diff and repository metadata.
2. Select the appropriate files based on packet mode.
3. Copy or bundle the selected files into a deterministic output directory or ZIP.
4. Create `review_context.md` from the sprint log, handoff, roadmap, and verification results.
5. Write a manifest listing every included file and why it was included.
6. Validate that all required canonical files are present.
7. Produce a repeatable package name that reflects the sprint or review focus.

Suggested longer-term workflow:

- Sprint closeout refreshes the review packet automatically.
- The next chat consumes the packet as the default upload.
- The packet generator becomes the normal place to encode packaging rules, not ad hoc chat instructions.
- The workflow document remains the policy source for what belongs in each mode.

The long-term goal is to make sprint transitions largely self-serve: Codex closes the sprint, generates the packet, and the next chat starts from one archive plus the standard small handoff files.

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
