# Workflow: Task Execution

## Governing Rule

The normal unit of work is one owner-authorized capability package or maintenance task.

Codex proceeds through the phases below without routine owner interruption.

Advance only when the current phase passes. Stop when `AGENTS.md` requires it, the package defines a stop condition, required verification cannot be completed safely, scope would expand, or owner review/merge authorization is required.

---

# Phase 1: Verify

**Goal:** Confirm authority, repository state, scope, and a usable baseline before editing.

## 1.1 Repository State

From the repository root:

- confirm Git root;
- confirm branch and full HEAD;
- confirm working-tree and index status;
- run the approved environment/interpreter preflight.

Stop for unexpected user changes, repository mismatch, or unresolved preflight failure.

## 1.2 Task Authority

Read the task-start files defined in `AGENTS.md`.

Confirm:

- the package or maintenance task is owner-authorized;
- any active sprint belongs to the authorized package; zero active sprints is valid while idle;
- once a first sprint or milestone is staged, it defines its goal, expected files, acceptance criteria, and verification;
- scope, exclusions, and completion conditions are defined.

Do not invent missing scope.

## 1.3 Canonical Records

When sprint/package records are used:

- validate canonical Markdown/JSON/YAML agreement with the established validator;
- inspect duplicate structured manifests directly only when validation fails or the task concerns them.

Update only the authorized package or sprint state.

## 1.4 Targeted Inspection and Baseline

Before modifying code:

- locate relevant files;
- inspect only the smallest relevant implementation area;
- read additional ADRs, architecture sections, or conditional procedures only when required;
- run proportionate baseline checks for the affected behavior.

Do not automatically run the full project suite unless the package requires it or the baseline is uncertain.

---

# Phase 2: Modify

**Goal:** Implement the smallest change that satisfies the authorized task.

## 2.1 Targeted Changes

- Change only files needed for the authorized scope.
- Prefer existing architecture and established patterns.
- Do not introduce a generic framework, new ownership model, persistence change, or unrelated refactor unless explicitly authorized.

### Approved External Region Pack Artifact Imports

An owner-approved external Region Pack artifact must have a recorded SHA-256 before repository import. Repository integration must verify the external source against that approved SHA-256, import the artifact by byte-preserving file copy without text decoding or re-encoding, and verify the repository destination against the same SHA-256 before any subsequent repository-side content edits or test updates.

Use the repository import utility for this transfer. It verifies the source before
copying, writes only a same-directory temporary byte copy, verifies that copy, and
atomically replaces the destination only after both hashes match. Do not pass the
artifact through a text editor, parser, serializer, or newline-normalizing tool as
part of the import.

## 2.2 Immediate Checks

After a meaningful code edit:

1. run the smallest appropriate syntax/static check;
2. run the focused test for the changed behavior when practical.

Repair directly caused, in-scope defects without owner interruption.

Follow `AGENTS.md` failure limits. Do not loop on repeated failures.

## 2.3 Internal Milestones

A capability package may contain multiple accepted internal milestones.

Codex may progress through them sequentially when each remains in scope, required focused verification passes, and no meaningful stop condition occurs.

Do not request routine continuation approval between milestones.

---

# Phase 3: Validate

**Goal:** Prove the completed change satisfies the package without known regressions.

Run, as applicable:

1. syntax/static checks;
2. focused tests;
3. directly affected regressions;
4. package-specific acceptance checks;
5. required broader regression or official suite;
6. canonical manifest agreement where records changed;
7. `git diff --check`.

Specialized checks are required only when relevant to the package.

For documentation-only changes, run documentation/governance validation and directly affected checks unless behavior could be affected.

Never report failed, skipped, or blocked verification as passed.

If validation finds a directly caused, bounded defect requiring no new architecture or scope, correct it once within the package and rerun the affected verification. Otherwise stop.

For player-visible packages, provide a short owner playtest procedure. Do not require manual owner validation of invisible internals already covered by automated verification.

---

# Phase 4: Prepare Review Candidate

**Goal:** Produce one auditable candidate for final review.

When formal review is required:

- use the authorized feature-branch workflow;
- commit only authorized package changes;
- record exact branch and full HEAD;
- confirm working tree and index are clean;
- confirm canonical package/sprint status truthfully reflects completed work;
- leave `next_sprint` unchanged unless explicitly authorized.

A final review candidate must be a committed repository state. An archive of uncommitted changes is not sufficient.

Create a review packet only at a required review boundary. Use the established profile, assembler, and validator. The packet must bind to the exact candidate branch and HEAD and pass validation before being reported as valid.

Detailed packet mechanics belong to review-packet tooling and conditional procedure documentation.

---

# Phase 5: Owner Review and Merge

**Goal:** Preserve owner authority at meaningful boundaries.

Final package review may result in acceptance, revision, rejection, or deferral.

Acceptance does not authorize merge unless merge authority is explicitly granted.

When strict fast-forward merge is authorized:

1. verify `main` is at the expected parent;
2. verify the accepted candidate HEAD exactly;
3. verify fast-forward eligibility;
4. perform strict fast-forward only;
5. do not alter the accepted candidate;
6. run safe post-merge verification;
7. confirm final `main` HEAD and clean repository state.

---

# Phase 6: Await Next Direction

After merge or completion:

- report the authoritative repository state;
- preserve `next_sprint` as `null` unless separately authorized;
- do not stage, branch, define, or implement another capability automatically.

After the owner explicitly authorizes selection of a new capability package,
Codex may make that package `current_capability_package` and stage its first
sprint or milestone. Validate its records, scope, exclusions, and completion
conditions; only then may bounded implementation begin. Codex must not make
this transition independently. Package selection authorization, candidate
acceptance, and merge authorization are separate owner decisions; none implies
another.

Architecture or sequencing analysis may recommend a next candidate. Implementation requires separate owner authorization.

---

# Handoff Rules

## Classification and Authority

Classify every handoff by its purpose:

- **Execution handoff (Chat → Codex):** perform one already-authorized bounded objective.
- **Review handoff (Codex → Chat):** independently assess a completed candidate.
- **Escalation (Codex → Chat/owner):** report material ambiguity, missing authority, or a decision that Codex cannot make.
- **Owner action:** a separately identified request for the owner to approve, revise, reject, or authorize something.

The transport destination does not confer decision authority. For example, “copy to new chat” and “copy to Codex” identify where context is sent, not who has owner authority.

A context-transfer block intended for a new chat or Codex contains operational context and instructions only. Do not end it with an approval, rejection, revision, or authorization request unless that recipient is explicitly the decision owner. Put owner-action requests outside the context-transfer block or in a separately labeled **Owner action** section.

For Codex prompts, place the recommended reasoning level immediately below `Project: AI Narrative RPG Engine`.

## Content Discipline

Use a pointer-first, necessity-tested handoff. Include information only when the receiver would realistically be unable to execute, review, or safely stop without it.

Prefer reliable canonical pointers over reproduced history, rationale, or logs: commit SHAs and branches; canonical document paths; ADR, capability-package, or sprint identifiers; file paths; evidence or review-packet references; and line ranges when useful. Do not use a line range as the sole durable identity for important material.

This is a default discipline, not an absolute prohibition: include the context necessary for safe execution or review, but do not duplicate canonical state, long logs, or historical explanation when a reliable pointer is sufficient.

## Receiving-Side Validation

Before acting on a handoff, determine that it provides:

- one bounded objective;
- sufficient information to execute or review that objective;
- clear authority already granted for the requested action;
- explicit material constraints and stop conditions; and
- a testable or observable completion condition.

If material scope, authority, or execution information is missing, stop and escalate rather than infer new scope or authority. Do not escalate for harmless omissions that do not affect safe execution or review.

---

# Conditional Procedures

Load detailed instructions only when the current task requires them:

- review-packet assembly and validation;
- environment/interpreter recovery;
- architecture review;
- capability sequencing or planning-horizon review;
- live-provider execution;
- migration or save-version change.

The current package should identify any conditional procedure required for its work.
