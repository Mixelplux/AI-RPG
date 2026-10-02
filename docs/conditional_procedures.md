# Conditional Procedures

Load a procedure in this document only when its trigger applies. `AGENTS.md`,
`PROJECT.md`, and `WORKFLOW.md` remain the standing execution contract; this
router adds only the source set and narrow rules unique to each situation.

## Architecture Review

**Trigger:** The owner requests an architecture review, or a completed package
raises a material ownership, boundary, persistence, or phase-level question.

**Load:** The directly relevant architecture sections and ADRs; simulation
sources only if the question needs them. The review template is optional for
ordinary reviews and remains required only for formal architecture packets.

**Rules:** Routine work uses focused scope/diff review. Elevated work may need
a targeted review of ownership, compatibility, or cross-system rules.
Critical work may justify deep adversarial review; choose depth by concrete
consequence and recovery difficulty. A new persistent domain or compatibility
change needs explicit design and owner authority, but does not automatically
require a full architecture audit. Access/tooling failures use recovery, not
automatic architecture escalation. Identify the reviewed baseline and diff;
formal candidates bind to exact branch/HEAD. Recommendations do not authorize
new capability selection, staging, or implementation.

## Capability Sequencing and Planning Horizon

**Trigger:** The owner asks for a next-capability recommendation, a planning
horizon, or a phase dependency decision.

**Load:** `PROJECT.md`, `docs/roadmap.md`, current package/sprint records, and
only architecture, simulation, or decision sections needed for the question.

**Rules:** Use observed player friction and completed capability evidence to
recommend the next small coherent package. A short planning horizon is optional
context with no fixed package-count limit or automatic full-review reset.
Only one bounded implementation task proceeds at a time. Do not run sequencing
or select the next package automatically after merge. The owner separately
authorizes each new package before staging and implementation. Escalate a
material dependency, authority conflict, or architectural risk on its merits,
not because a correction count or planning horizon was exhausted.

## Review-Packet Assembly and Validation

**Trigger:** The owner explicitly requests a formal packet, or the agreed
risk boundary specifically requires one. An ordinary committed review
candidate alone does not trigger packet assembly.

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
different Python executable. Apply the known Windows fallback below if its
trigger matches. Otherwise stop when required preflight remains unresolved;
report an environment blocker rather than a product defect.

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

**Rules:** Obtain owner authorization before implementation if the accepted
package does not already authorize this persistence or compatibility change.
Classify as Elevated, or Critical for credible destructive/data-loss risk.
Define the version transition, compatibility behavior, atomicity, and verification before
changing persisted state; preserve existing saves unless an explicitly
authorized migration supersedes that requirement. Do not introduce a generic
migration framework without separate approval.
