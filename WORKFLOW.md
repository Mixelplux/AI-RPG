# Workflow: Risk-Proportional Task Execution

## Governing Rule

The normal unit of work is one owner-authorized capability package or
maintenance task. Codex proceeds without routine interruption inside that
boundary, and stops for owner review and merge authorization.

Every package is classified once at staging. If its classification is unclear,
use **Critical** until the owner decides otherwise.

## Risk Levels

### Critical

Classify as Critical when the change affects saves, migrations, Region Pack
integrity, destructive mutation, movement semantics, security or provider
boundaries, or repository/data-loss risk.

Critical packages require:

- frozen scope;
- a feature branch;
- relevant integration verification;
- independent review; and
- owner-authorized strict-fast-forward merge.

### Routine

Routine covers ordinary runtime capabilities, read-only behavior,
documentation, tests, lifecycle records, and workflow metadata.

Routine packages require:

- concise scope;
- a feature branch;
- targeted verification; and
- owner review and merge authorization.

Independent review and evidence packets are optional for Routine work unless
the owner explicitly requests them.

---

## Phase 1: Verify and Stage

Before editing:

- confirm Git root, branch, full HEAD, and clean working tree and index;
- read the task-start files defined by `AGENTS.md`;
- confirm owner authorization, scope, exclusions, and completion condition;
- record the risk level in `docs/current_sprint.json`; and
- inspect only the implementation and tests relevant to the change.

`docs/current_sprint.json` is the only machine-enforced lifecycle authority.
`docs/current_sprint.md` and `docs/current_capability_package.md` are
explanatory records for scope, rationale, and readable status. They are not
parsed as duplicate lifecycle state and cannot override JSON.

Do not create a YAML lifecycle representation. Historical handoffs and logs
are context, not current authorization. `next_sprint` remains `null` until the
owner separately authorizes package selection.

---

## Phase 2: Modify

Change only the authorized scope. Make routine in-scope choices, repair
directly caused defects, and run the smallest useful syntax or static check
after meaningful edits.

Do not introduce a migration, persistence or ownership model, broad refactor,
or player-visible behavior beyond the accepted scope. Preserve unrelated user
changes. Provider output remains untrusted and has no simulation authority.

---

## Phase 3: Validate

Run the verification required by the risk level and package record:

- Critical: relevant integration verification plus focused checks.
- Routine: targeted checks for changed behavior and records.

Always validate changed lifecycle JSON, run `git diff --check`, and inspect
the changed scope. Do not run a broader suite unless the package requires it.
Live-provider execution remains separately owner-authorized.

For a clerical correction that cannot affect behavior, run correction-only
verification: JSON parsing, the lifecycle validator or affected record test,
and `git diff --check`. Do not repeat unrelated verification solely because a
record or wording was corrected.

Non-contract hardening, defensive improvements, and stylistic concerns belong
in the backlog and do not block a candidate unless they violate an accepted
requirement or a core invariant.

---

## Phase 4: Prepare Candidate

Prepare one immutable candidate on the feature branch:

- commit only authorized changes;
- record the exact branch, candidate HEAD, and parent;
- confirm a clean working tree and index; and
- leave `next_sprint` unchanged unless separately authorized.

Lifecycle records describe implementation state only. Do not require or add
candidate-prepared, not-merged, merge-unauthorized, candidate-state, or
merge-state lifecycle fields. A normal merge does not require a separate
lifecycle-closeout package or a post-review lifecycle-only commit.

---

## Phase 5: Review, Correction, and Merge

For a Critical candidate, obtain independent review before owner acceptance.
For a Routine candidate, owner review is sufficient. Evidence packets are
created only when the owner explicitly requests one.

One bounded correction cycle is allowed for review findings that remain within
scope. Re-run only the verification affected by that correction and prepare a
replacement immutable candidate. If a further correction, scope change, or
risk reclassification is needed, stop and request owner classification.

Acceptance and merge authority are separate owner decisions. When the owner
authorizes merge, verify the expected `main` parent and candidate HEAD,
confirm fast-forward eligibility, and perform a strict fast-forward only.
Do not push or merge without that authorization.

After a normal merge, report the final `main` HEAD and clean state. Do not
start, stage, or select another package automatically.

---

## Handoff Rules

### Classification and Authority

Classify handoffs by purpose:

- **Execution handoff (Chat → Codex):** perform one already-authorized bounded objective.
- **Review handoff (Codex → Chat):** assess a completed candidate.
- **Escalation (Codex → Chat/owner):** report material ambiguity, missing authority, or a decision Codex cannot make.
- **Owner action:** a separately identified request to approve, revise, reject, or authorize something.

The transport destination does not confer decision authority. A context
transfer contains operational context only; keep owner-action requests
separately labeled.

### Content Discipline

Use pointer-first, necessity-tested handoffs. Prefer canonical pointers—commit
SHAs and branches, record paths, package identifiers, and focused verification
results—over copied history or logs.

### Receiving-Side Validation

Before acting, confirm the handoff contains one bounded objective, sufficient
execution or review information, granted authority, material constraints, and
a testable completion condition. Stop for a material omission; do not escalate
for harmless omissions.

## Conditional Procedures

Load detailed instructions only when the task requires them: independent
review, environment recovery, architecture review, capability sequencing,
live-provider execution, or migration and save-version work.
