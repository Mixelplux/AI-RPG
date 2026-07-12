# WORKFLOW.md

## Governing Principle

Use the lowest reasoning level capable of completing the entire coherent task safely. Do not divide one coherent task into many runs solely to obtain a lower reasoning setting.

The default unit of work is one complete, coherent sprint run. For a normal bounded sprint, one medium-reasoning Codex run may perform startup review, sprint staging, implementation, focused testing, required documentation and ADR work, full closeout verification, sprint closeout, and final reporting. Separate runs remain allowed when they materially improve safety, but are not required by default for staging, implementation, documentation repair, closeout, or packet generation.

## Sprint Lifecycle

Exactly one sprint may be active at a time. A combined sprint run must:

1. Work from the repository root in PowerShell and run the environment preflight.
2. Read the canonical project and sprint documents and perform Startup Review.
3. Confirm the prior sprint is complete and `next_sprint` is `null` or matches the explicitly accepted sprint.
4. Stage the explicitly accepted sprint in all three canonical manifests before changing implementation code.
5. Confirm the staged Markdown, YAML, and JSON manifests parse and deeply agree.
6. Continue directly into implementation unless a stop condition is encountered.
7. Run focused verification during implementation.
8. Complete required documentation and ADR work.
9. Run one complete closeout verification cycle.
10. Close out the active sprint only after verification succeeds, then report and stop.

A combined run must not stage more than one sprint. Closeout must not define, stage, or begin the following sprint.

## Canonical Sprint Manifests

The permanent sprint paths are:

- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`

Continue maintaining and validating all three. Synchronize them once during staging, once during closeout, and again only when a repair changes sprint-record content. Do not rewrite or repeatedly revalidate them between implementation edits that do not affect sprint metadata.

The JSON and YAML manifests must both parse successfully, use the same data types, contain the same keys and nesting, preserve equivalent ordered list values, and deeply agree after parsing. The embedded Markdown manifest must materially agree with them. JSON syntax validation alone is insufficient.

Temporary sprint-numbered planning files may be promoted into the canonical paths when supplied, then deleted only after successful promotion and validation. Their presence does not require a separate staging run.

Future workflow tooling should choose one structured canonical source, generate the other formats mechanically, and validate that generated files are current. This direction does not change the present three-manifest policy until separately designed and accepted.

## Architecture Review Cadence

A full architecture review is required when:

- introducing a new persistent domain or schema;
- changing save compatibility;
- changing established ownership boundaries;
- adding autonomous simulation or background behavior;
- adding scene, perception, narration, visibility, or other projection policy;
- introducing generic infrastructure;
- resolving a material architectural contradiction; or
- beginning or ending a meaningful capability cluster.

A full architecture review is not automatically required after every small method-sized or closely related capability. An accepted review may authorize a small sequence or capability cluster. Every sprint in that sequence must still be explicitly staged, independently bounded, and testable.

Review again when the accepted sequence is complete, implementation materially diverges from the reviewed architecture, a stop condition is triggered, or the next capability crosses an architecture boundary listed above. Cluster approval never authorizes speculative implementation or more than one staged sprint.

## Model and Reasoning Routing

### Low reasoning

Use for genuinely mechanical work: applying an already approved exact documentation edit, running established validation commands, generating a handoff package, checking archive inventory, collecting Git evidence, or deterministic cleanup.

### Medium reasoning

Use for a normal bounded sprint, including startup review, staging, implementation, focused tests, documentation, closeout, and final verification.

### High reasoning

Reserve for architecture and scope review, unclear or systemic test failures, ownership conflicts, persistence design, atomicity problems, or material contradictions between accepted scope and repository structure.

A run may escalate only when the coherent task genuinely requires it.

## Verification Cadence

### During implementation

Run new focused tests, directly affected regression tests, and syntax or static validation needed for changed files. Do not repeatedly run the entire official suite after every small edit.

### At closeout

Run one complete workflow-required verification cycle, including:

- focused and required regression tests;
- save/load validation where applicable;
- Region Pack validation where applicable;
- canonical manifest parsing and deep agreement;
- environment preflight;
- hardening validation;
- launch check;
- scripted smoke check; and
- `git diff --check`.

If a closeout repair changes only documentation, rerun manifest validation, applicable documentation or governance validators, `git diff --check`, and any check directly affected by the repair. Do not rerun unrelated application tests unless the repair could affect them.

If implementation code changes after the full closeout cycle, rerun affected tests and any required final suite under the existing safety rules. Required failures block closeout. Blocked commands must be reported accurately and never treated as passes.

## Canonical Windows Environment

- Work from the repository root in PowerShell on Windows.
- Run preflight before implementation and closeout.
- Use only `.\.venv\Scripts\python.exe` for Python setup, tests, validation, and closeout evidence.
- Do not substitute bundled, system, Windows Store, alternate, `uv`, or fallback Python environments.
- Record exact verification commands, exit codes, outcomes, and artifact paths.

Codex must attempt each official interpreter command first. If its execution context denies process creation, record the exact command, exit code, and error and classify it as an agent execution-context limitation, not an unhealthy virtual environment. Provide a copy-safe command for the repository owner. Clearly identified user-executed output from the same official interpreter may satisfy the check; alternate interpreters may not.

## Stop Conditions

Stop before implementation or closeout if:

- the repository is unexpectedly dirty;
- canonical sprint manifests materially disagree;
- the sprint is already implemented or conflicts with current state;
- accepted architecture materially contradicts the repository;
- the change requires a new persistent schema not previously approved;
- ownership cannot remain within the accepted boundary;
- atomicity cannot be preserved;
- implementation would require a listed non-goal; or
- required verification exposes an unresolved material failure.

A minor, clearly bounded defect may be repaired in the same run only when it was directly caused by the sprint work, does not broaden scope, requires no new architectural decision, and is recorded in the final report.

## Commit Policy

Codex may stage sprint documentation, implement, verify, and close out in one run. Codex must not create a Git commit unless the task prompt explicitly authorizes it. When authorization is absent, report the exact changed-file list and a recommended commit title.

Do not create separate staging and closeout commits unless the user explicitly requests them, the sprint is unusually large, or an architecture checkpoint requires preserving an intermediate state. An authorized normal sprint may use one atomic commit after all verification passes.

## Handoff and ZIP Policy

A handoff ZIP is required only when moving from Codex to ChatGPT for architecture review, moving to an environment without repository access, creating a formal milestone artifact, or when explicitly requested. Do not create staging ZIPs for normal sprint work or architecture-review ZIPs after minor sprints without a genuine external-review boundary. Within one repository session, continue from the live repository.

When a ZIP is required, use PowerShell `Compress-Archive`, a deterministic inventory, exact archive-membership validation, readability checks, temporary-assembly cleanup, and recorded Git evidence. Generated content must stay under `.build\`, `.artifacts\`, or `handoffs\` according to repository policy. Packaging success remains independent from application-test success.

## Task Prompt Guidance

Normal sprint prompts should reference canonical repository documents instead of repeating stable architecture. They should normally state:

- accepted capability;
- task type and reasoning level;
- required behavior;
- ownership;
- focused tests;
- ADR requirement when applicable;
- explicit non-goals;
- stop conditions; and
- commit authorization.

The prompt should instruct Codex to read the canonical repository documents. Missing sprint details must not be invented.

## Future Mechanical Automation

Future tooling should support commands equivalent to:

```powershell
.\tools\validate_sprint.ps1
.\tools\close_sprint.ps1
.\tools\build_review_packet.ps1
```

It should automate manifest parsing and deep comparison, focused and official regression execution, preflight and hardening checks, Git evidence capture, launch and scripted smoke checks, handoff assembly, exact ZIP inventory validation, and temporary-file cleanup. This section documents direction only; no new script is required by this workflow update.

## Project Invariants

Preserve provider neutrality, deterministic behavior, simulation-owned truth, exactly one active sprint, and unrelated user changes. Never begin the next sprint automatically.
