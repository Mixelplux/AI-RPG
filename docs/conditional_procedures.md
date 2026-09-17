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

**Rules:** Select explicitly among a sprint health check for routine internal
confirmation, a capability-package review at a capability boundary, and a
deep architecture review for consequential boundaries. A deep review is
required for a new persistent domain or schema, save-compatibility change,
established ownership change, autonomous simulation, generic infrastructure,
live AI authority, material canonical-lore ownership change, serious
contradiction, or close consequential alternatives. Escalate to a full review
as well when a package is blocked for external review, a repository-access
boundary requires it, or the owner requests one. Bind the review to an exact
branch and HEAD, separate decision-relevant technical evidence from the owner
brief, and end with one owner decision request. A recommendation does not
authorize staging or starting a capability.

## Capability Sequencing and Planning Horizon

**Trigger:** The owner asks for a next-capability recommendation, a planning
horizon, or a phase dependency decision.

**Load:** `PROJECT.md`, `WORKFLOW.md`, `docs/architecture.md`,
`docs/roadmap.md`, `docs/decisions.md`, `docs/simulation_model.md`,
`docs/simulation_principles.md`, and the current package and sprint records.

**Rules:** A full architecture review may establish a horizon of up to three
related runtime packages. The horizon is planning context, not implementation
authority: only one package may be owner-authorized at a time. After every
merged package, run a lightweight sequencing check against the latest
committed evidence; it may retain, replace, or revise the next candidate, but
each candidate still needs explicit owner authorization before staging,
branching, or implementation. Return to a full review before further package
authorization when the horizon is exhausted, direction is uncertain, a deep
review trigger applies, evidence is insufficient, or the check exposes a
material dependency, authority conflict, scope pressure, or loss of atomicity,
causal integrity, hidden-state protection, or save compatibility. A full
review also replaces the lightweight check when a package needs more than one
normal consolidated correction cycle, owner interaction or scope fragmentation
increases, workflow authority becomes ambiguous, or review evidence weakens.
A full review interrupts lightweight sequencing rather than extending it. Do
not fragment one coherent capability merely to extend a horizon.

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

### Windows Codex Sandbox and Temporary Test Files

**Trigger:** A Windows Codex run reports `helper_sandbox_lock_failed`,
`SetNamedSecurityInfoW sandbox dir failed: 5`, or a save/load test fails while
cleaning up a Python `TemporaryDirectory`.

**Rules:** Treat the elevated Windows sandbox setup failure as an external
Codex-environment defect. After one confirmation attempt, use the verified
safe fallback instead of retrying the same blocked setup: the affected local
Codex configuration uses `[windows] sandbox = "unelevated"`. Do not change
`.sandbox-bin`, project ACLs, or Windows ACLs as a workaround.

The save/load regression must use direct deterministic files in the tracked
`.artifacts/` root, not `tempfile.TemporaryDirectory`. Redirecting `TEMP` and
`TMP` only changes the parent directory; it does not prevent a sandbox-created
child directory from receiving a protected ACL that blocks cleanup. Generated
save/load outputs remain ignored under `.artifacts/`.

The repository uses standalone `test_*.py` scripts with the official
interpreter; `pytest` is not an intended development dependency and is not
declared in `requirements.txt`. Do not install it solely to run these tests.

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

**Load:** `AGENTS.md`, `WORKFLOW.md`, `docs/architecture.md`, the applicable
ADRs in `docs/decisions.md`, and the directly affected save/load
implementation and tests.

**Rules:** Stop for owner authorization before implementation. Define the
version transition, compatibility behavior, atomicity, and verification before
changing persisted state; preserve existing saves unless an explicitly
authorized migration supersedes that requirement. Do not introduce a generic
migration framework without separate approval.
