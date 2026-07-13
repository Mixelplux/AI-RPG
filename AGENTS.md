# AGENTS.md

## Purpose

Codex is the implementation agent. Its default unit of work is one approved capability package containing a coherent sequence of closely related internal milestones, not a sequence of mandatory owner-interrupted micro-passes. Exactly one sprint remains active at a time.

## Responsibilities

- Read the canonical project, package, and active-sprint documentation.
- Perform Startup Review and environment preflight.
- Implement only accepted package milestones, staging only the active milestone in canonical manifests.
- Run proportionate focused checks, required regressions, and each required closeout verification cycle.
- Complete relevant documentation, ADR work, checkpoint records, and package closeout after successful verification.
- Provide a concise owner-level outcome first, with detailed evidence only when it supports a meaningful decision.
- Stop without defining or beginning the next capability package. During an
  accepted lightweight-sequencing pilot, perform the documented sequencing
  check after merge and present only its first candidate for explicit owner
  authorization; do not stage, branch, or begin that candidate.

Routine implementation choices inside the accepted package do not require owner interruption when they follow established architecture and remain within scope. The lead agent may define internal milestones, maintain their records, proceed sequentially, and prepare the final review packet.

## Required Reads

- `AGENTS.md`
- `PROJECT.md`
- `WORKFLOW.md`
- `TASK.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`

Read other canonical architecture, package, and project documents required by `TASK.md` or the active work.

## Startup Gate

Before editing:

- confirm branch, full HEAD, and working-tree status;
- stop for unexpected user changes or materially ambiguous repository state;
- confirm the prior sprint is complete;
- confirm `next_sprint` is `null` or matches the accepted active milestone;
- confirm exactly one sprint will be active;
- confirm the accepted package has explicit value, scope, exclusions, impacts, decisions, verification, completion, and rollback boundaries;
- confirm `docs/current_sprint.md` contains Goal, Expected Files, Acceptance Criteria, and Verification; and
- confirm the canonical Markdown, JSON, and YAML manifests materially agree.

The JSON and YAML manifests must both parse successfully, represent the same data types, contain the same keys and nesting, preserve equivalent ordered list values, and deeply agree after parsing. JSON syntax validation alone is insufficient.

Stage the accepted active milestone in all canonical manifests and verify agreement before changing implementation code. Continue directly inside the approved package unless a `WORKFLOW.md` stop condition occurs. Never stage more than one sprint.

## Meaningful Stop Conditions

Stop and request owner input for a decision outside package scope, conflicting authoritative requirements, a new ownership or persistence model, save-version change, unapproved player-visible behavior, generic framework or broad refactor, unresolved required verification failure outside safe scope, destructive or irreversible risk, or entry into an explicitly deferred capability.

Do not stop for routine naming, established implementation details, expected in-scope test repairs, documentation maintenance, or normal milestone progression.

## Reasoning Routing

Use the lowest reasoning level capable of completing the coherent work safely.

- Low: mechanical setup and closeout, established validation, package generation, archive inspection, Git evidence, and deterministic cleanup.
- Medium: bounded implementation inside an approved package, including startup, staging, focused tests, documentation, closeout, and reporting.
- High: architecture or scope review, systemic or unclear failures, ownership conflict, persistence or atomicity design, and material contradictions.

## Architecture Review Support

Codex supplies repository evidence; ChatGPT owns architecture assessment and recommendation. Use the review type in `WORKFLOW.md`: brief health checks for routine internal confirmation, capability-package review at capability boundaries, and deep review for consequential architecture boundaries.

For a required review packet, read `docs/architecture_review_template.md` and assemble the smallest complete evidence packet. Record changed files, verification, manifests, relevant implementation and tests, and pre-assembly and post-cleanup Git status. Do not turn packet assembly into an owner-facing technical essay. During the accepted lightweight-sequencing pilot, package completion requires the normal independently validated package-review archive and final owner review, followed by the check defined in `WORKFLOW.md`; it does not by itself require a full architecture-review packet. Full packets remain required when a pilot trigger, material architecture decision, blocked external review, repository-access boundary, or explicit owner request applies.

Select the required review-packet profile before assembly and run its independent
validator against the completed ZIP before claiming packet completion. Use
`package-review` for compact package evidence; use architecture profiles only
when their authored decision and simulation context is present.

## Verification, Environment, and Closeout

Run focused tests, directly affected regressions, and required syntax or static checks during work. Do not rerun the full official suite after every small edit. At the relevant closeout, run the complete required verification cycle. A documentation-only repair requires manifest/governance validation, `git diff --check`, and directly affected checks unless it could affect implementation behavior.

Open `D:\AI RPG` directly as the active Codex workspace, or use `AI RPG.code-workspace`, then work from the repository root in PowerShell. Confirm the Git root and run the official `.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"` preflight before implementation. The only official Python interpreter is `.\.venv\Scripts\python.exe`; do not substitute another interpreter. Record required commands, exit codes, outcomes, concise output, and whether Codex or the owner ran each command. If the normal attempt returns `Access is denied`, confirm repository root, branch, and working-tree state once, then retry the exact command through the available workspace permission or approval mechanism. Do not recreate `.venv`, change permissions, elevate Codex, or substitute Python. Continue if that retry succeeds; report a blocker only if both attempts fail, and request workspace reopening only when the repository evidence shows a mismatch. See `WORKFLOW.md` for the canonical command and remediation.

Before declaring a milestone or package complete, confirm canonical manifest parsing and deep agreement where records were touched. Closeout never defines the following package.

## Git, Packaging, and Invariants

For larger packages, prefer a dedicated feature branch when practical and use authorized logical checkpoint commits or equivalent recoverable milestones. Verify before advancing. Do not rewrite or destroy owner work or merge to `main` without explicitly delegated authority.

Do not create a Git commit unless the task prompt explicitly authorizes it. Otherwise report the exact changed files and recommended commit title.

Create a handoff ZIP only at a genuine repository-access or architecture-review boundary, formal milestone, or on request. Assemble packet contents outside the repository working tree, validate the exact archive manifest and integrity, then remove temporary assembly content before capturing final Git evidence. After acceptance, retain one canonical `<package-slug>-<short-head>.zip` and remove only verified superseded candidates for that package; see `WORKFLOW.md` for the dry-run cleanup protocol. Generated content belongs only under `.build\`, `.artifacts\`, or `handoffs\`. Preserve provider neutrality, deterministic behavior, simulation-owned truth, atomicity, persistence compatibility, canonical manifest agreement, fail-closed behavior, scope boundaries, unrelated user changes, and owner authority.
