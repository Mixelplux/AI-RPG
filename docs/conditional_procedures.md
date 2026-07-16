# Conditional Procedures

Load a procedure in this document only when its trigger applies. `AGENTS.md`,
`PROJECT.md`, and `WORKFLOW.md` remain the standing execution contract; this
router adds only the source set and narrow rules unique to each situation.

## Architecture Review

**Trigger:** The owner requests an architecture review, or a completed package
raises a material ownership, boundary, persistence, or phase-level question.

**Load:** `docs/architecture.md`, `docs/decisions.md`,
`docs/simulation_model.md`, `docs/simulation_principles.md`, the current
package and sprint records, and `docs/architecture_review_template.md` when
preparing an owner review.

**Rules:** Use the lightest review type that answers the question. Bind the
review to an exact branch and HEAD, separate decision-relevant technical
evidence from the owner brief, and end with one owner decision request. A
recommendation does not authorize staging or starting a capability.

## Capability Sequencing and Planning Horizon

**Trigger:** The owner asks for a next-capability recommendation, a planning
horizon, or a phase dependency decision.

**Load:** `PROJECT.md`, `WORKFLOW.md`, `docs/architecture.md`,
`docs/roadmap.md`, `docs/decisions.md`, `docs/simulation_model.md`,
`docs/simulation_principles.md`, and the current package and sprint records.

**Rules:** Recommend only bounded candidates justified by player or project
value and established dependencies. Preserve the one-active-sprint rule; do
not define, branch, stage, or implement a recommendation until separately
authorized by the owner.

## Review-Packet Assembly and Validation

**Trigger:** `WORKFLOW.md` or the active package requires a formal review
candidate or packet.

**Load:** `docs/review_packet_profiles.md`, the current package and sprint
records, package verification evidence, and
`tools/assemble_review_packet.ps1` plus `tools/validate_review_packet.ps1`.

**Rules:** Select the profile before assembling evidence. Assemble only from a
committed, clean candidate, bind packet Git evidence and source pins to its
exact branch and HEAD, and validate the completed archive with the repository
root. Existing legacy archives remain legacy; do not rewrite them to satisfy a
new profile.

## Environment and Interpreter Recovery

**Trigger:** `tools/preflight.ps1` reports a failure or block, especially for
the official interpreter or workspace root.

**Load:** `AGENTS.md`, `WORKFLOW.md`, `tools/preflight.ps1`,
`tools/validate_project_records.ps1`, and the current package and sprint
records.

**Rules:** Use only `./.venv/Scripts/python.exe` as the official interpreter.
Correct the workspace context and rerun the focused preflight; do not recreate
the environment, change permissions, run as Administrator, or substitute a
different Python executable. Stop when the required preflight remains
unresolved.

## Live-Provider Execution

**Trigger:** The owner explicitly authorizes an opt-in live provider smoke or
the active package explicitly permits one.

**Load:** The active package and sprint records, the narration boundary in
`docs/architecture.md`, the applicable decisions in `docs/decisions.md`, and
`tools/run_openai_responses_live_smoke.py`.

**Rules:** Keep automated tests provider-safe. Run only the authorized smoke,
never expose credentials or raw provider material, and record only sanitized
pass/fail evidence. Provider output remains untrusted and must not create or
mutate simulation truth.

## Migration and Save-Version Changes

**Trigger:** Work proposes a save-version change, a compatibility migration,
or a persistence-model change.

**Load:** `AGENTS.md`, `WORKFLOW.md`, `docs/architecture.md`,
`docs/schemas/savegame_schema.md`, the applicable ADRs in
`docs/decisions.md`, and the directly affected save/load implementation and
tests.

**Rules:** Stop for owner authorization before implementation. Define the
version transition, compatibility behavior, atomicity, and verification before
changing persisted state; preserve existing saves unless an explicitly
authorized migration supersedes that requirement. Do not introduce a generic
migration framework without separate approval.
