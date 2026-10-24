# M2-M1 — Integrated Player Input and Consequential Execution

October 24, 2026. **Owner-accepted after successful interactive smoke and handoff
review, including documented bounded limitations.** Risk: Elevated. Current owner
authorization covers acceptance recording, lifecycle closeout and publication
preparation only. Accepted runtime/test/fixture/tool contents are frozen. No Git
staging, commit, merge or push is authorized.

## Repository and scope

Repository: Mixelplux/AI-RPG. Published/local main and starting HEAD verified at
`f93988958385ec77dc012e0e5ecf8d0af068f893`; no baseline reconciliation was needed.
Branch: `codex/m2-m1-player-input`.
Worktree: `C:\Users\Richard\.codex\worktrees\m2-m1-player-input\AI RPG`.
The original dirty `D:\AI RPG` checkout, player saves and unrelated worktrees were
preserved. The ignored `.venv` junction reuses the official Windows environment.
No source was copied from the rejected experiment in the original checkout.

The accepted Integrated Gameplay Architecture, I1–I3 plan/handoffs, F01/F05,
Information Foundation and Information-Grounded Adjudication were reviewed.
JSON was staged/validated before implementation. Lifecycle is now complete/idle:
active_sprint and active_capability_package null, latest completed M2-M1 and
next_sprint null. This closes only the accepted bounded milestone.

## Implemented capability and ownership

An explicit I3 campaign can install `player_activity_context=callable(engine)`.
The legitimate World/Character/Action supplier returns the existing validated
SituatedContext: current location/revision, supported targets with visible aliases,
method availability/defaults, means and Character-safe descriptions. Suppliers
own accurate completeness, legitimate access and read-only behavior. No hidden
internal record is turned into a visible alias or instruction suggestion.

`GameEngine.process_command` accepts supplied search targets and ordinary
`inspect`/`examine` spellings, optional `the`, explicit `using METHOD`, and I1's
`can I`/`could I`/`how can I` inquiry and `prepare to` assessment forms. A supplied
routine method can make an ordinary instruction actionable; otherwise the player
must choose a method. Interpretation has no outcome authority. Compound/ambiguous
input and unsupported methods/constraints are contained. Carefulness/quietness
have no implemented finite mechanics here and are refused rather than dropped.

Inquiry/preparation creates no activity, costs, roll or accepted information.
Commitment builds a structured Request and durable undertaking through existing
I3 operations, then uses the same I1 coordinator, F05 policy, dependency discovery,
finite adjudication and Runtime.accept as structured I2/I3 play. A known failed
factual prerequisite can yield an accepted blocked attempt with declared costs;
missing capability, unavailable material information and technical rejection do
not become fictional outcomes. No new mechanics or authority are introduced.

The new situated context participates in I1's execution freshness checks and a
final equality guard immediately before the existing owning read/root revalidation.
Changed methods, scope, means or context revision cannot publish a stale candidate.
Existing domain information checks still apply. Accepted information, mechanics,
costs, seconds, history and receipts publish in the existing single campaign root.
Later comparison actually retrieves the accepted finding and current target premise.

Each ordinary instruction commits one declared meaningful finite increment and
returns control. `continue` selects the sole durable undertaking or an explicit
`undertaking_id`, preserves method/constraints and enforces current F05 boundaries.
Completed undertakings do not reroll on `continue`; a fresh instruction is a new
attempt. With multiple undertakings the caller must identify which to continue.
There is no invented multistep plan, universal search duration or outcome table.

`process_command(text, request_id=..., undertaking_id=...)` carries opaque transport
references; response `player_activity` returns them. Without a supplied request ID,
a committed instruction is a new attempt with a generated identity. Reusing an
accepted ID with matching interpreted scope returns the saved result. Conflicting
reuse refuses. Explicit `retry` plus the accepted request ID recognizes its receipt
before current eligibility/context lookup, even if services currently fail. The
client must retain transport IDs for reliable replay; repeated text alone is not
an idempotency key. A same-text replay requiring unavailable aliases/context should
use explicit `retry`. New attempts always require current authorization/adjudication.

Rejected first attempts discard only their implementation-created, unaccepted
activity when the campaign root is still exactly that prepared root. Accepted
increments and intervening legitimate owner revisions are never rolled back.
Previously accepted progress survives interruption, failed later steps and display
failure; the existing safe receipt remains the retry authority.

## Persistence and bounded limitations

No save codec, record shape, version or ownership contract changed. Existing
version-2 activities/results/receipts preserve identity and continuation requirements.
Independent `load_game` reconstruction requires explicit current service installation
with `set_player_activity_context`; callbacks, aliases, parser/session state and
unaccepted proposals are not saved. Existing-engine load retains its installed
service and passes the restored engine to it. Supplier revisions must cover every
material situational premise. No concurrent writer guarantee is added.

The default production CLI/content remains version 1. Unconfigured I3 and legacy
I2 retain their existing command refusal; configured I3 never falls through to
legacy mutating paths, including for `look`, `wait`, movement or unsupported language.
Version-1 compatibility and I2 persistence refusal are preserved. No migration,
general natural-language understanding, movement/combat/search mechanics, waiting
execution, offscreen adjudication, autonomous NPCs, Region Pack or live provider
work is included. This is reusable bounded integration, not generalized gameplay.

Fixtures supply inspection premises, finite routine/d6 methods, explicit durations,
lamp-unit costs, effects and legitimate grants. Target name does not select an
outcome. Tests vary names/durations, mechanical draws, factual prerequisites,
capability, hidden restrictions, availability, means and current boundaries through
the same runtime. The fixture comparison requires both retained information and
current target information; no production investigation rules are inferred.
As in the accepted finite incorporation contract, an attempt proposing an effect
for an already occupied consequential slot rejects rather than overwriting it.
New-attempt identity does not waive that rule or guarantee another accepted effect.

## Verification and corrections

- Syntax: all six changed/new Python files compiled in memory with the official
  `.\.venv\Scripts\python.exe` before relevant execution.
- **293 unittest cases passed:** 18 M2 input matrix, 55 I1, 59 I2, 29 I3 and 132
  F05/independent activity, information resolution/adjudication, F01, material
  consequence and contextual investigation cases.
- **13 affected regression entry points passed:** save/load, narrative realization,
  scene construction, player scene route, navigation projection, history context,
  history query, scene context, time/pressure, actor relocation, evidence time,
  contextual action projection and narration input foundation. Their logs are
  ignored `.artifacts/m2-test_*.log`; these are entry-point runs, not 13 extra
  unittest cases. Network/provider guards were active.
- Scripted smoke passed for cargo panel (19-second increments; total 45 seconds)
  and archive slab (13-second increments; total 33 seconds). Both retain two lamp
  units and three accepted receipts after interruption/restoration/retry/continuation
  and dependent comparison. This verifies the shared sequence, not general language.

The first fixture run lacked all required safe observation outcomes. A later run
exposed an omitted current target premise in the comparison supplier and an incorrect
test expectation that a known failed factual requirement should reject rather than
produce a legitimate accepted blocked attempt. Those fixture/test contracts were
corrected without altering adjudication or persistence rules. A save test was
blocked by sandbox filesystem access; it passed with approved execution outside
the sandbox. One regression harness rejected construction of an offline transport
client; a dummy client retained live-call guards while allowing injected transport,
and all remaining regression entry points passed. No unresolved required product
failure remains. Live evaluation is unrun. The owner subsequently completed a
successful interactive smoke and formally accepted M2-M1 on October 24, 2026.

## Owner experiential smoke

From this worktree root:

```powershell
.\.venv\Scripts\python.exe -m tools.smoke_m2
```

Enter `can I inspect the cargo panel?`, `prepare to inspect cargo panel`,
`inspect cargo panel`, `/interrupt`, `continue`, `/save`, `/restore`, `retry`,
`continue`, `/clear`, `continue`, `inspect surface finding`, `/status`, `/quit`.
Inquiry/preparation must do nothing consequential. After the first inspection,
retry must retain 19 seconds, three lamp units and one receipt. Continuation stays
blocked after fresh restoration until the fixture supplies changed circumstances.
The comparison depends on retained information. Final status: 45 seconds, two lamp
units, three receipts. Slash commands supply explicit fixture events or save/load;
ordinary gameplay instructions all use GameEngine.process_command.

For the second circumstance, add `--target "archive slab" --duration 13` and use
that target name; final status is 33 seconds/two lamp units/three receipts.
`--scripted` runs either sequence deterministically. Only ignored `.artifacts/`
test/smoke saves are written; owner saves are not read or changed.

## Changed-file inventory and reconciliation

Runtime (3): engine/game_engine.py, engine/consequence_integration.py,
engine/player_activity.py.

Tests/fixture/tool (3): test_player_activity.py,
test_fixtures/player_activity_suppliers.py, tools/smoke_m2.py.

Documentation/lifecycle (9): docs/architecture.md,
docs/current_capability_package.md, docs/current_sprint.md,
docs/current_sprint.json, docs/m2_m1_handoff.md,
docs/design/systems/system-map.md, docs/design/systems/action-resolution.md,
docs/design/systems/player-presentation.md, docs/design/systems/persistence.md.

The additional acceptance freshness seam and service-retention load change are
directly necessary within the authorized Action/coordination/persistence boundary.
Affected manifests and relationship/runtime maps describe actual accepted bounded support;
historical I1 links now point to its handoff after lifecycle rotation.
Meaningful no-change determinations: accepted Design/ADRs/doctrine retain their
existing authority/ownership; no new durable decision, record format or policy is
needed. Information Foundation and Character manifests need no revision because
retrieval/access contracts are reused unchanged. Production Region content, CLI,
PROJECT/AGENTS/WORKFLOW and deferred findings remain unchanged because no general
capability or deferred system was implemented. No material Design question remains.

The handoff is an **uncommitted working diff** at the starting HEAD, with an empty
index. No committed candidate, commit, merge or push exists. Stop after publication
preparation for separate owner Git authority; do not select another milestone.

Final mechanical evidence: established GitWorkflowTools verification passed and
reported repository state unchanged during verification. Its ignored profile copy
changes only the worktree root/preflight expected root; shared tools/profile are
unchanged. Direct final preflight: 20 passes, one expected dirty-worktree warning,
zero blocks/failures. Lifecycle validator: eight passes, zero failures. Six Python
syntax checks, 255 local documentation links, strict UTF-8/no BOM, whitespace,
exact 15-path inventory, expected branch/HEAD and empty-index checks passed.
No save/data/content diff is present. Generated evidence stays under `.artifacts/`.

## Owner acceptance and publication preparation — October 24, 2026

The owner formally accepts M2-M1 with its documented bounded limitations after
review of this handoff, 293 passing unittest cases, 13 passing affected regression
entry points, two successful scripted smoke circumstances and successful owner
interactive smoke. No acceptance-blocking defect was identified.

The owner smoke confirmed inquiry/preparation without consequential execution;
accepted inspection results/costs; interruption blocking unauthorized continuation;
saved progress surviving independent restoration; retry without repeated costs or
mechanics; changed legitimate circumstances allowing continuation; a subsequent
activity using accepted information; and unsupported commands executing no gameplay.
Final accounting: **45 seconds, two lamp units remaining, three accepted increments**.

Finite language/domain support, explicit service installation after independent
restoration, fixture limitations and deferred capabilities remain accepted limits.
No narrative polish or generalized gameplay understanding is claimed.

The exact 15-file inventory above remains the intended publication content. This
preparation changes only its nine documentation/lifecycle files. Six accepted
runtime/test/fixture/tool files are pinned before reconciliation and verified
unchanged afterward. Existing accepted gameplay evidence is reused; no gameplay
rerun, live provider or owner-save access is needed for these documentation changes.
Accepted Design, ownership, save formats, production content and deferred work
need no further reconciliation because implementation behavior is unchanged.

Lifecycle JSON is complete/idle with latest completed M2-M1 and next_sprint null.
The intended publication remains an uncommitted diff on the expected published
parent. A file-content manifest is preparation evidence, not a Git commit/tree or
final committed candidate. New-GitWorkflowCandidate is not invoked because it
stages and commits. The established verified strict fast-forward publication
workflow requires separate owner staging/commit and merge/push authorization.
No next capability or milestone is selected.

### Publication-preparation result

Published remote main, local main, origin/main and feature HEAD agree at
`f93988958385ec77dc012e0e5ecf8d0af068f893`. The exact 15-path inventory is unchanged;
only the nine documentation/lifecycle files changed during acceptance recording.
The six implementation files match their task-start SHA-256 pins byte for byte
and compile in memory with the official Windows interpreter. Previously accepted
gameplay evidence is reused; no gameplay or live-provider test was rerun.

Established GitWorkflowTools verification passed with repository state unchanged
during verification; lifecycle validation reports eight passes, zero failures.
Complete/idle semantics, acceptance wording, 255 local documentation links,
strict UTF-8/no BOM, whitespace, scope, baseline/branch and empty-index checks pass.
No required verification is blocked or failing.

Preservation checks confirm unchanged HEAD/status for all 18 unrelated worktrees,
including the original dirty checkout, and unchanged worktree registrations.
Existing ignored generated-file metadata, worktree/original save metadata and
shared-tool metadata are unchanged. No player-save contents were read or hashed;
no save, production-content or unrelated path enters the publication diff.
New preparation evidence uses ignored `.artifacts/m2-acceptance-*` paths, preserving
prior evidence. The final exact-content manifest is
`.artifacts/m2-acceptance-candidate.json`; it is not a committed Git candidate.

**Readiness:** accepted content is ready for separately authorized staging/commit
through GitWorkflowTools. Verified strict fast-forward publication still requires
that committed candidate and separate merge/push authority, with main at the
expected parent. The worktree remains an uncommitted 15-file diff and the index is
empty. No staging, candidate commit, merge, push, source correction, migration,
live provider or next milestone was performed.
