# Information Resolution Core V1a — implementation handoff

Status: implemented, verified and owner-accepted following final code-level review,
October 21, 2026. Implementation remains uncommitted and unpublished.
Risk: Routine. No persistence, Region Pack or major ownership boundary was crossed.
Baseline and HEAD: `cd6de8be40407f504aba1438b6d12f8828b81dde`.
Branch: `codex/information-resolution-core-v1a`.
Worktree: `D:\AI RPG\.artifacts\information-resolution-core-v1a`.
The original dirty checkout and all pre-existing worktrees remain preserved.
No staging, commit, merge, push, publication or live provider calls occurred.

## Final code-level review and acceptance

The owner accepted V1a subject to a final code-level review. A manual review of
the complete implementation and focused tests found no blocking defects and
required no code corrections. This was an in-thread review, not an independent
review or a committed candidate review. HEAD remains the baseline above; the
review covers this worktree's uncommitted V1a implementation.

Review covered foundation composition/conflicts, identity and layer separation,
current/history selection, deterministic bounded traversal, binding scope and
availability, character grants and hidden-information diagnostics, immutable
public values and storage-independent consumer operations. Fresh syntax checks
and all 26 focused tests passed. Additional public-interface probes passed for
half-open time boundaries, identical character results with and without hidden
current changes, unavailable binding terms, all-action constraints and foundation
permutations. The earlier regression results below remain recorded results;
the final review did not rerun the unchanged production regression suite.

The acceptance condition is satisfied. Lifecycle is complete and idle, with no
next package selected. Acceptance does not authorize staging, commits, merge,
push or publication. No runtime code or tests changed during final review.

Limits remain explicit: conflict detection covers matching scalar slots rather
than semantic prose; suppliers own completeness and legitimate grants; binding
conditions are returned for an owning adjudicator; production integration,
authentication, mutation and persistence remain deferred. Review and fixture
success do not establish those capabilities or generalized gameplay correctness.

## Scope and component assessment

The owner authorized the reusable read-only increment of accepted Information
Foundation Functional Design V1, not general gameplay, mutation or persistence.
The package's single milestone was staged and validated before implementation.

Assessment completed before coding:

- Reused conceptual ownership, stable opaque identities/source references,
  immutable input/result patterns and standalone offline unittest conventions.
- Excluded `world_state`, `history_context`, actor-knowledge membership, Region
  Pack validation, saves and `GameEngine` from modification. Their bounded
  dictionaries, tail-history queries and membership lists cannot provide general
  composition, epistemic distinctions and cross-domain retrieval without expanding
  current runtime or persistence contracts. No replacement was warranted.
- Retained F01 realization and F05 activity control unchanged. They already consume
  supplied authority. This increment supplies information retrieval, not prose,
  sufficiency certification or continuation decisions.
- Added `engine/information_resolution.py`, independent of existing campaign
  structures. No existing production component was adapted or replaced.

## Functional architecture and public operations

`InformationSnapshot` validates supplied immutable dataclasses and builds private
subject, outgoing-relationship and constraint-scope indexes. Identities contain
only an opaque ID, subject/definition/instance distinction and optional definition
reference. Facts, relationships and binding terms carry meaning separately; this
is an information handoff vocabulary, not a universal entity or Region Pack schema.

Consumers use the four operations defined by `InformationAccess`:

| Operation | Contract |
|---|---|
| `identity(subject_id)` | Trusted lookup of minimal identity metadata; unknown returns None. Definitions never establish an instance, presence or capability. |
| `resolve(Query)` | Trusted internal direct or explicitly bounded outgoing relationship retrieval over supplied current/history and authored grounding. |
| `applicable_constraints(ConstraintQuery)` | Trusted internal retrieval of every constraint matching any supplied subject and action/time scope, including hidden constraints. |
| `for_character(query, character_id, grants)` | Character-accessible facts/edges or constraints, requiring explicit Character System grants with legitimate basis and time bounds. |

All operations return immutable values in deterministic record-ID order.
`Result` contains the request, selected records, source/basis, traversal paths,
selection reasons, temporal relevance and availability. `missing_expected(ids)`
reports test-expected omissions; it is not a runtime completeness oracle.

Foundation composition requires one setting/era. Compatible information and its
source references accumulate. Overlapping objective scalar facts with the same
subject/predicate and different available values fail with `CanonicalConflict`.
This supports exact-key contradictions; it does not detect semantic contradictions
in differently worded prose or infer unstated exceptions. No specificity or input
order grants precedence. Explicitly different predicates, historical intervals
and attributed beliefs/claims express supported legitimate distinctions.

Accepted current objective facts overlay their authored subject/predicate slots
at the requested time, including known-but-unavailable placeholders. Claims,
beliefs and inferences never overwrite objective truth. Conflicting available
current values fail closed. Historical records are separate supplied references,
returned only with `include_history=True`; they never become a current fallback.
Future records are excluded. Historical meaning, source, attribution and interval
are preserved, without automatic aging or invented verification requirements.

Time is a caller-owned integer fictional timeline with half-open intervals
`[start, end)`. A snapshot may be rebuilt with a supplied accepted change, such as
ward termination. Construction and queries cannot establish that change.
Relationships and constraints use explicit supplied intervals; no implicit graph
mutation or event replay occurs. Traversal follows requested relation names,
outgoing direction and bounded depth, with deterministic shortest selected paths.

Constraint terms retain prerequisites, triggers, exclusions, exceptions, effects,
termination and revocation. Selection determines subject/action/time applicability
only. The owning adjudicator must evaluate the returned conditions and effects.
An established constraint whose terms are unavailable is returned with
`terms=None` and `established_unavailable`, never silently omitted or invented.
Callers must include relevant locations, participants and rule domains in the
constraint query; hidden constraints require no character grant on internal reads.

An internal absent slot is `unspecified`; supplied placeholders are
`established_unavailable`; genuinely unresolved records are `uncertain`. Claims,
beliefs and inferences retain their epistemic status separately from availability.
Without an authoritative placeholder, the core cannot infer that omitted upstream
information actually exists. Suppliers must preserve that distinction.

Character views require grants for both traversed edges and returned records.
A grant authorizes the entire supplied record, including provenance and time
metadata, so suppliers must make that complete record legitimate for the character.
Internal diagnostics must never be forwarded to presentation. Character absence
is uniformly `not_accessible`, without exposing hidden record existence. Hidden
current developments neither erase retained accessible knowledge nor reveal that
knowledge is stale. Accessible nonhistorical facts are labeled `retained`, which
does not certify current world applicability. Historical recall remains historical.
No grants or ordinary knowledge are inferred merely from the engine knowing truth.
Sources, owners and grants are validated handoff declarations, not authenticated
credentials or proof of legitimate adjudication. Untrusted provider output has
no path into production authority through this module.

## Verification and representative coverage

All checks below passed using the existing official `.\.venv\Scripts\python.exe`.
The isolated worktree links to the existing environment; it does not recreate it.

- Syntax: `-m py_compile engine/information_resolution.py test_information_resolution.py`.
- Focused: `test_information_resolution.py` — 26 unittest cases, including domain
  subtests and foundation permutations; socket connections are forbidden.
- Relevant regressions: `test_activity_control.py` — 11 cases;
  `test_f05_independent_activity.py` — 1; `test_damaged_gate.py` — 23.
- `test_narrative_realization.py` — all script assertion groups passed with injected
  generators/transport; `test_save_load.py` — save/load roundtrip passed.
- Total: 61 unittest cases plus the two script-based regression checks.
- Lifecycle validator, official-interpreter/worktree preflight, Git whitespace and
  scope checks passed. Index remains empty. No repository-wide suite was claimed.

| Accepted scenario | Evidence and practical limit |
|---|---|
| Guard bribe, reassignment, promotion | One stable identity; current rank/assignment replace authored slots; historical bribe and assignment retain source/time/meaning. No mutation or history persistence. |
| Matron Veyr | Competing obligation/objective and attributed belief/claim coexist; legitimate grants exclude faction secrets. No autonomous decision or concession. |
| Hidden levitation ward | Internal scope query returns hidden binding terms even without player knowledge; character result excludes them; a separately supplied accepted removal changes time applicability while history remains retrievable. No casting adjudication/removal execution. |
| Binding agreement | Preserves fee prerequisite, trigger, exclusion, exception, effect, termination and revocation; scope/time/action selection tested. No condition adjudication. |
| Temple, faction, deity | Cross-foundation accumulation and selective multi-edge retrieval with path diagnostics; unrelated shop omitted; traversal requires edge access. No comprehensive lore integration. |
| Reference catalogs | Monster, spell, equipment, deity, faction, organization, rule and condition definitions; explicit monster instance distinct from definition; no inferred scene presence, spell knowledge or casting ability. No comprehensive catalogs. |

Additional tests cover different opaque identities and domains, exact-key conflict
rejection, source ordering, claims/inferences versus truth, uncertainty/unavailable
states, immutable results, expired access/edges, cycles, bounded traversal and
stable multiple-path selection. Public-operation consumer tests avoid internal
storage, including related-scope constraint retrieval and deterministic rebuilds.

Representation failures raise `RepresentationError` (including supported canonical
conflicts). Retrieval failures are detected by fixture expectations and
`missing_expected`; the tests exercise an intentionally shallow query that omits
known doctrine. Adjudication failures are outside V1a: no retrieved text is treated
as an implemented gameplay decision. Fixture success claims only these mechanisms.

## Storage independence and deferred dependencies

The consumer protocol and immutable result vocabulary expose no index/dictionary
layout, filesystem or World State access. Private indexes are rebuildable from
supplied records. Future storage can implement these operations while preserving
identity, time, provenance, epistemic and availability semantics. No alternate
backend, universal repository, database, persistence format, migration mechanism
or speculative optimization was built or tested. Future adapters and versioned
persistence will require separately authorized integration and compatibility work.

Deferred: production authoring/import, source authentication, ordinary knowledge
and familiarity derivation, access retention/recall, authoritative updates, history
retention/persistence, offscreen adjudication, autonomous actors, general condition
interpretation and actual adjudicator trace instrumentation. Suppliers still own
query scope and completeness. Production Region Packs, saves, F01/F05 behavior,
provider configuration, player agency and gameplay routes are unchanged.

## Documentation reconciliation

Updated runtime architecture, Information Foundation implementation status, system
index/map and the four directly relevant manifests (authored content, world,
character and action/resolution). Final-review reconciliation records bounded
implementation acceptance separately from deferred/full-system behavior and
publication. Updated current package, sprint and lifecycle authority to complete
and idle, with no active package/sprint and `next_sprint: null`.

Meaningful no-change determinations: PROJECT/WORKFLOW/AGENTS and Story-First doctrine
retain their existing scope/authority; no new doctrine was introduced. Existing
ADRs need no revision because no accepted ownership or persistence commitment was
superseded. Persistence, Actors/Social, Narrative and Player Presentation manifests
retain their classifications and contracts; the shared map records the read-only
relationship without claiming integration. F01/F05 design and runtime are unchanged.
No new deferred finding is warranted: remaining dependencies are explicit V1a
exclusions and accepted R1–R4, not newly observed production defects. Historical
handoffs, accepted evidence and original lifecycle files are untouched in their
original checkout/worktrees.

## Exact changed files and repository state

All paths below are relative to this isolated worktree (14 changed files):

- `engine/information_resolution.py` (new)
- `test_information_resolution.py` (new)
- `docs/information_resolution_core_v1a_handoff.md` (new)
- `docs/architecture.md`
- `docs/design/information-foundation-functional-design-v1.md`
- `docs/design/systems/README.md`
- `docs/design/systems/system-map.md`
- `docs/design/systems/world-simulation.md`
- `docs/design/systems/character-system.md`
- `docs/design/systems/scenario-authored-content.md`
- `docs/design/systems/action-resolution.md`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

HEAD remains the baseline above; all changes are uncommitted, index empty.
The three new files are untracked; eleven existing files are modified. Generated
bytecode, preflight outputs, regression saves and the environment junction remain
ignored in approved locations. This is an implementation handoff, not a committed
review candidate. The original checkout remains on its original branch/HEAD and
retains its pre-existing dirty paths, owner save and rejected experiment.

## Review and publication disposition

Review this worktree's three new files and `git diff` for the eleven tracked files.
From its root run `.\.venv\Scripts\python.exe test_information_resolution.py` and,
if desired, the focused regression commands above. Review scope matching, conflict
semantics and character grant obligations against D1–D16 and the scenario table.
No player smoke is required: no production player-facing route changed.

Owner acceptance is complete for this bounded read-only implementation following
final code-level review. No staging/commit/publication authority is implied.
Stop here; do not select or begin V1b automatically.
