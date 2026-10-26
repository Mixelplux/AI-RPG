# Workflow: Proportional Engineering

## Governing Rule

Work on one owner-authorized, small, coherent capability package or maintenance
task at a time. Finish authorized reversible work without repeated approval.
Use credible consequence and recovery difficulty to choose rigor; Routine is
the default. `docs/engineering_posture.md` defines the three risk levels and
architectural safeguards that apply to all work.

## Windows Automation Environment

Supported Windows development, verification and publication automation requires
PowerShell 7+ (Core), invoked explicitly as `pwsh.exe -NoProfile`. The verified
baseline is installed PowerShell 7.6.5; prefer the 7.6 LTS line. Do not install or
upgrade a working environment merely to meet a preferred patch version.
Windows PowerShell 5.1 is unsupported; mandatory preflight fails on it, and other
repository PowerShell entry points require version 7 before executing.
No demonstrated repository legacy exception requires 5.1.

Confirm shell selection with
`pwsh.exe -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'`.
Codex commands must select `pwsh.exe` explicitly where shell selection matters;
the repository VS Code terminal profile also selects it without loading a user
profile. Do not alter system shell defaults or user profiles.

From the intended repository/worktree root, use the existing official Windows
Python environment at `.\.venv\Scripts\python.exe` and run:

```powershell
pwsh.exe -NoProfile -File .\tools\preflight.ps1 -RepoRoot . -ExpectedRepoRoot (Get-Location).Path
pwsh.exe -NoProfile -File .\tools\validate_project_records.ps1 -ProjectRoot .
pwsh.exe -NoProfile -File .\tools\test_powershell_workflow.ps1 -ProjectRoot .
pwsh.exe -NoProfile -File .\tools\run_offline_behavioral_verification.ps1 -ProjectRoot .
```

The workflow regression covers all 16 lifecycle fixtures in formatted, compact
and legacy-style JSON whitespace. Mutations operate on exact JSON properties
and check their expected source values; lifecycle validation and the intended
negative assertions remain unchanged. These checks make no live provider calls.

The shared `Profiles\AINarrativeRPG.psd1` is AI RPG specific. Its mandatory
preflight and lifecycle commands use `pwsh.exe`; other projects' profiles and
shared scripts are unchanged. Its default repository is the original
`D:\AI RPG` checkout: do not run stage-all, verification or publication against
that dirty checkout when the candidate is in another worktree.

For an isolated candidate, use the established worktree-bound profile-copy
procedure: preserve the shared profile and create a new ignored copy under that
worktree's `.artifacts/`. Change only the copy's `RepositoryPath` to the exact
candidate root and add `-ExpectedRepoRoot "<candidate root>"` to its preflight
command, retaining every original check, argument and protected-branch value.
Invoke the shared state and standalone verification tools with that explicit
copy via `pwsh.exe -NoProfile -File`. Do not repoint the shared profile, drop
checks or replace GitWorkflowTools.

Any owner-required independent verification must identify the same candidate
worktree, exact HEAD, empty index, file scope, shell version, lifecycle and offline
regressions, shared-profile scope and repository-mutation detection. Report
whether verification used a separate fresh process or an independent reviewer;
a process check does not substitute for an explicitly required reviewer.
An uncommitted handoff cannot satisfy committed-candidate evidence-export
preconditions; do not invoke candidate or merge tools without Git authorization.

If `pwsh.exe` is unavailable or resolves to an unexpected version, correct shell
selection before proceeding; do not fall back to `powershell.exe`. A linked
worktree can expose its files while sandbox access to Git metadata fails,
producing `must be run in a work tree`, `Permission denied`, or the validator's
`Could not verify the player-save publication boundary`. Confirm root/HEAD and
the name-only `git diff --name-only HEAD -- saves` in the intended worktree using
the approved execution context. Preserve the save check and existing ACLs and
environment. See `docs/conditional_procedures.md` for environment recovery.

## Verify and Define Scope

Before editing, verify repository root, branch, full HEAD, and working-tree
and index status; identify the accepted Git baseline and preserve unrelated
changes. Read the task-start files specified by `AGENTS.md`. Confirm the
authorized capability, allowed architectural subsystems, exclusions, risk,
and completion condition. Expected files are guidance, not an immutable list.

A directly necessary additional file within an approved subsystem may change
without another approval if it does not broaden product scope. Report it at
completion. Crossing into another architectural subsystem requires owner
review. Do not introduce unapproved behavior, persistence or ownership models,
migrations, save-version changes, broad refactors, or deferred capabilities.

Use a feature branch for implementation and maintenance edits. Owner
authorization is required to select/open a new capability package; stage its
first sprint before implementation. Record its risk in lifecycle JSON.
An explicitly authorized standalone documentation/process maintenance task
may proceed while lifecycle is idle without replacing the completed sprint
or staging a future package.

`docs/current_sprint.json` is the sole machine-enforced lifecycle authority.
Markdown package and sprint records explain scope and status; stale prose
cannot override JSON. Zero or one sprint may be active. Historical handoffs
are context, not authorization. Do not create a YAML lifecycle representation
or select, stage, or start the next package automatically. Keep `next_sprint`
null until separately authorized package selection under existing lifecycle
mechanics; validate staged records with the established validator.

## Implement and Verify

Make routine local decisions, repair directly caused defects, and complete
in-scope milestones and review corrections without arbitrary correction-count
limits. Stop only for scope departure, destructive/irreversible action,
materially different architecture or risk, missing provider/live-action
authorization, conflicting authoritative requirements, or an unresolved blocker.

Verification follows risk and the actual affected behavior:

- **Routine:** relevant syntax/static checks, focused behavior tests, directly
  relevant nearby regressions, `git diff --check`, and scope/diff review.
  Arrange owner smoke when behavior is player-visible.
- **Elevated:** add affected-system regressions, targeted architecture review,
  compatibility checks, and migration/recovery checks where relevant.
- **Critical:** agree explicit approval boundaries and verification appropriate
  to the high-consequence boundary; deep adversarial review, broad verification,
  or evidence capture may be justified.

Validate affected lifecycle/record contracts. For wording-only corrections,
use affected record checks and diff review; do not repeat unrelated tests.
Routine work does not default to independent audit, repository-wide suites,
formal packets, ADRs, exact file manifests, multiple gates, or broad architecture
revalidation. Write an ADR only when a material durable architectural decision
needs recording. Optional hardening and style suggestions do not block
completion unless they violate accepted behavior or a core invariant.

Environment/tooling failures are verification blockers, not proof of product
failure. Report checks as passed, failed, blocked, or unrun accurately. Use the
established Windows recovery procedure after one confirmation of its known
sandbox/ACL failure. Never loop on blocked paths or modify ACLs without new,
narrowly scoped evidence. Live-provider actions require explicit authorization;
automated tests remain offline.

## Documentation Reconciliation

Complete documentation reconciliation for every implementation before
presenting it for owner acceptance or publication, including after corrections
that affect documentation. Identify documentation affected by the actual
changes and update relevant runtime architecture documentation, system
manifests, relationship maps, architectural decisions, deferred findings, and
package records where warranted. Do not require every document to change at
every milestone or reconcile unrelated historical documentation.

Preserve distinctions between implemented behavior, accepted design,
provisional research, and deferred capabilities; documentation must not imply
owner acceptance of an unaccepted implementation. Verify affected documentation
against the implemented behavior and accepted design so that it accurately
represents the implementation submitted for acceptance and, before publication,
the accepted implementation. Record the documentation updates and meaningful
no-change determinations, with brief reasons, in the existing completion report.

Routine reconciliation is part of authorized implementation scope and needs no
separate owner authorization. Stop for owner input only if reconciliation
introduces a material new architectural decision, doctrine change, or otherwise
exceeds authorized scope. Use proportionate documentation/record checks and
diff review; this adds no mandatory report, approval gate, or formal review packet
and does not change lifecycle or acceptance authority.

## Git, Review, and Completion

Continue using `D:\Codex Tools\GitWorkflowTools` with
`Profiles\AINarrativeRPG.psd1`; do not invent a replacement Git workflow.
Use its state tool near task start, run focused checks directly, and use its
verification, candidate, evidence, and merge operations when applicable and
authorized. Profile checks are mechanical invariants, not a requirement for
repository-wide gameplay testing. Do not modify shared tools for a package.

An uncommitted working diff is a valid implementation handoff when commits
are not authorized. Report baseline, changed files, verification, and blockers.
Only prepare a final review candidate when staging/commit authority is granted:
commit authorized changes on the feature branch, bind review to its exact HEAD
and parent, and confirm clean working tree and index. Formal evidence packets
are used only when explicitly requested or required for the agreed risk boundary.

Owner smoke evaluates player experience; acceptance evaluates the result.
Neither authorizes Git staging, commit, push, or merge. Obtain appropriate
Git authorization separately. Routine owner review may use a concise diff and
verification report; independent review is not a default requirement.

When merge is explicitly authorized, use the established strict fast-forward
tool, verify expected `main` parent and candidate HEAD, and report final `main`
HEAD and cleanliness. Never rewrite accepted history without authorization.
A normal merge needs no lifecycle-closeout package or extra lifecycle-only
commit. Do not add ephemeral candidate/merge-state fields to lifecycle JSON.

## Approved External Region Pack Artifact Imports

An approved external artifact needs a recorded SHA-256. Use the existing
repository import utility to verify source bytes, create and verify a
same-directory temporary byte copy, and atomically replace the destination.
Verify destination against the approved hash before repository content edits
or test updates. Do not decode, re-encode, or normalize the artifact during
import. This integrity check is specific to external imports, not routine
package file scope.

## Handoffs and Conditional Procedures

Handoffs identify one bounded objective, baseline/branch, granted authority,
material constraints, completion condition, and focused verification. Prefer
canonical pointers to copied logs. Distinguish execution context, review,
escalation, and owner decisions; transport does not grant authority. Escalate
material omissions, not harmless ones.

Load `docs/conditional_procedures.md` only for an applicable architecture or
planning question, requested packet, environment recovery, authorized live
provider action, or migration/save-version work.
