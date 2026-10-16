# F05 Extended Activity & Control V1 — acceptance and closeout

Owner accepted the bounded implementation on October 16, 2026 after experiential
review of the Market scenario, and separately authorized staging, commit,
strict fast-forward merge and publication. The problem → observation → action →
completion sequence was satisfactory for this implementation stage.

Protected starting baseline and expected publication parent:
`342b9a4670131a22535a3b436e323684c6ab74b3`.
Feature branch: `codex/f05-authorized-activities-v1`. Risk: Routine.
Package/sprint ID remains `f05-authorized-activities-v1`; the display title does
not create a second package.

## Accepted implementation and identity

The owner accepted the existing deterministic control policy and its narrow
material-handling checkpoint binding. No runtime, test or fixture changes are
made during closeout. Canonical Git blob identities pinned before closeout:

| Path | Accepted Git blob |
|---|---|
| `engine/activity_control.py` | `34a1d12212f6ed984b8eef4856a833e12fc0395d` |
| `engine/contextual_action.py` | `22c37370bc97a3b81b3c56edc1915a414ea03869` |
| `test_activity_control.py` | `6ca0c812604aba784246f72b5cb7016f6aa3d518` |
| `test_fixtures/f05_activity_control.json` | `bae92869821bc6a332f2940fd2d1285b7a9fedc6` |

The policy consumes owning-system authorization, circumstances and result
references, returning continuation/control decisions. Existing contextual input,
candidate publication, costs, draws, replay and save-version-1 semantics remain.
Discovery, consequential dialogue and restart inputs are authoritative offline
fixtures; their general suppliers and playable F01–F05 integration are not
implemented by this package. Neither references nor context shape validation
authenticate gameplay authority or prove semantic fidelity.

Accepted [F05 D1–D6](design/f05-authorized-activities-and-player-control.md),
[F01 information requirements](design/f01-truthful-presentation-and-epistemic-fidelity.md),
shared doctrines and system ownership are unchanged. See the
[implementation and verification report](f05_implementation_preflight.md) for
decision coverage, source disposition, assertion investigation and prior stop.

## Verification and publication scope

Final offline prepublication rerun passed 77 tests (11 F05, 51 adjacent handling,
15 investigation) and four narration scripts. Changed Python syntax passed.
Network access was blocked; investigation reported zero network attempts.
Owner experiential review covered inquiry, action proposal, authorization,
resolution and continuity.

Publication additionally requires unchanged accepted source blobs, the exact
bounded path set, closed lifecycle, preserved Design/ADRs/governance, ignored
generated material, whitespace/record/preflight checks, mutation-protected shared
workflow verification, a clean committed candidate with the expected sole parent,
and exact strict fast-forward and remote identity checks. Final commit identity
and execution outcome are reported by the publication workflow and task report;
this record does not claim unrun publication operations succeeded.

Exact publication paths:

- Runtime: `engine/activity_control.py`, `engine/contextual_action.py`.
- Tests: `test_activity_control.py`, `test_fixtures/f05_activity_control.json`.
- Runtime/system reconciliation: `docs/architecture.md`,
  `docs/design/systems/README.md`, `docs/design/systems/action-resolution.md`,
  `docs/design/systems/system-map.md`.
- Closeout: `docs/current_capability_package.md`, `docs/current_sprint.md`,
  `docs/current_sprint.json`, `docs/f05_implementation_preflight.md`,
  this acceptance record and `docs/deferred_findings.md`.

Generated execution logs, local workflow profile copies and preservation metadata
remain ignored under this worktree's `.artifacts/f05-publication/`; they are
not publication content. No credentials, saves, historical experiments, raw
provider material or rejected Sprint 10.82 implementation are included.

## Accepted limitations and deferred observations

The owner reported these non-blocking observations for subsequent integration
evaluation; no fix is authorized in this closeout:

- `look at the cart` produces a generic fallback while `assess the cart` works.
- The post-action scene can describe Tessa agreeing to help after she has already
  completed the action.

They are preserved under [DF-009](deferred_findings.md#df-009--bounded-f01f05-playable-scenario-evaluation).
Existing bracing can establish support while reporting interruption; full-result
repeat commands can be unavailable while preserving the result. The verified
matching-condition replay uses a partial result. No universal replay, general
discovery/dialogue/restart support, upstream simulation or broader integration
claim follows from acceptance.

## Documentation reconciliation, lifecycle and preservation

Architecture, Action & Resolution manifest, system map/index and package records
now describe this bounded implementation as owner accepted. Deferred findings
retain the two observations without scheduling work. Accepted Design, doctrines,
ADRs, F01 runtime and other system implementation classifications need no change:
there is no new gameplay decision, ownership, storage, provider or save contract.

Lifecycle JSON records F05 complete, zero active packages/sprints, latest completed
F05 and `next_sprint: null`. No follow-on package or integration milestone is
selected. This acceptance supersedes earlier pending-review/authorization language
in historical preflight descriptions.

Preserve the original dirty `D:\AI RPG` checkout, owner saves and credentials,
historical experiments, unrelated worktrees and rejected Sprint 10.82 code.
Only the F05 feature and existing clean publication-main worktrees participate.
No history rewrite or force push is authorized. Stop after successful publication.
