# Workflow: Proportional Engineering

## Governing Rule

Work on one owner-authorized, small, coherent capability package or maintenance
task at a time. Finish authorized reversible work without repeated approval.
Use credible consequence and recovery difficulty to choose rigor; Routine is
the default. `docs/engineering_posture.md` defines the three risk levels and
architectural safeguards that apply to all work.

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
