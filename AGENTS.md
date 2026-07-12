# AGENTS.md

## Purpose

Codex is the implementation agent. Its default unit of work is one complete coherent sprint run, not a sequence of mandatory micro-passes.

## Responsibilities

- Read the canonical project documentation.
- Perform Startup Review and environment preflight.
- Stage only the explicitly accepted sprint in the canonical manifests.
- Implement only that sprint.
- Run proportionate implementation checks and one complete closeout verification cycle.
- Complete required documentation, ADR work, and sprint closeout after successful verification.
- Report results and stop without defining or beginning the next sprint.

A normal bounded sprint may stage, implement, document, verify, close out, and report in one medium-reasoning run. Separate runs are allowed when they materially improve safety, but are not the default.

## Required Reads

- `AGENTS.md`
- `PROJECT.md`
- `WORKFLOW.md`
- `TASK.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`

Read other canonical architecture and project documents required by `TASK.md` or the active sprint.

## Startup Gate

Before editing:

- confirm branch, full HEAD, and working-tree status;
- stop for unexpected user changes or a materially contradictory dirty tree;
- confirm the prior sprint is complete;
- confirm `next_sprint` is `null` or matches the explicitly accepted sprint;
- confirm exactly one sprint will be active;
- confirm `docs/current_sprint.md` contains Goal, Expected Files, Acceptance Criteria, and Verification; and
- confirm the canonical Markdown, JSON, and YAML manifests materially agree.

The JSON and YAML manifests must both parse successfully, represent the same data types, contain the same keys and nesting, preserve equivalent ordered list values, and deeply agree after parsing. JSON syntax validation alone is insufficient.

For a combined sprint run, stage the accepted sprint in all canonical manifests and verify their agreement before changing implementation code. Then continue directly unless a stop condition in `WORKFLOW.md` is encountered. Never stage more than one sprint.

## Reasoning Routing

Use the lowest reasoning level capable of completing the entire coherent task safely. Do not divide one coherent task into many runs solely to obtain a lower reasoning setting.

- Low: genuinely mechanical edits, established validation, package generation, archive inspection, Git evidence, and deterministic cleanup.
- Medium: a normal bounded sprint from startup and staging through implementation, documentation, verification, closeout, and reporting.
- High: architecture or scope review, systemic or unclear failures, ownership conflict, persistence or atomicity design, and material contradictions.

## Architecture Review

Require full review at meaningful subsystem and capability-cluster boundaries, including new persistent domains or schemas, save compatibility changes, ownership-boundary changes, autonomous behavior, projection policy, generic infrastructure, material architectural contradictions, and the beginning or end of a meaningful capability cluster.

An accepted review may cover a small sequence, but every sprint must remain explicitly staged, independently bounded, and testable. Review again when the sequence ends, implementation diverges, a stop condition occurs, or the next capability crosses an architecture boundary. Cluster approval does not authorize speculative work.

## Verification

During implementation, run focused tests, directly affected regressions, and necessary syntax or static checks. Do not rerun the full official suite after every small edit.

At closeout, run one complete workflow-required verification cycle. If a later repair is documentation-only, rerun only manifest/governance validation, `git diff --check`, and directly affected checks. If implementation changes after the full cycle, rerun affected tests and the required final suite according to `WORKFLOW.md`.

Treat application failures and tooling/runtime failures differently. Application failures and other unresolved required failures block closeout. Blocked commands are not passes.

## Canonical Windows Environment

- Work from the repository root in PowerShell on Windows.
- The only official Python interpreter is `.\.venv\Scripts\python.exe`.
- Invoke small Python probes with `-c` and substantial logic from checked-in or generated script files. Do not pipe multiline Python through stdin.
- Do not substitute bundled, system, Windows Store, alternate, `uv`, or fallback Python.
- Run environment preflight before implementation and closeout.
- Record each required command, exit code, outcome, and concise output.

If Codex cannot launch the official interpreter, preserve the exact command, exit code, and error. Classify access-denied or process-creation failure as an execution-context limitation, not evidence that `.venv` is unhealthy. Provide copy-safe commands for the repository owner. Clearly identified user-executed evidence using the same official interpreter may satisfy verification; alternate interpreters remain prohibited.

## Closeout and Commit Control

Before marking a sprint complete, confirm all canonical manifests parse and deeply agree. Synchronize them during staging and closeout, and again only if a repair changes sprint-record content. Closeout must not define the following sprint.

Do not create a Git commit unless the task prompt explicitly authorizes it. Without authorization, report the exact changed files and a recommended commit title.

## Packaging and Project Invariants

- Create a handoff ZIP only at an environment or architecture-review boundary, for a formal milestone, or when explicitly requested.
- Use PowerShell `Compress-Archive` and independently validate archive entries.
- Create generated content only under `.build\`, `.artifacts\`, or `handoffs\` according to repository policy.
- Packaging success is independent from application-test success.
- Preserve provider neutrality, deterministic behavior, simulation-owned truth, exactly one active sprint, and unrelated user changes.
