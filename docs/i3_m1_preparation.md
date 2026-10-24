> Acceptance, October 24, 2026: the owner accepted the bounded I3-M1 implementation
> and its limitations after structural and experiential verification. The
> [implementation handoff](i3_m1_handoff.md) supersedes historical preparation/pending
> status below. Only acceptance recording and exact publication preparation are
> authorized now; no source correction, Git commit/merge/push or follow-on work.

> Implementation authorization, October 24, 2026: the owner approved this revised
> assessment and its representation/version/seconds contracts and authorized source
> implementation and Elevated offline verification. Historical preparation-only
> stop language below is superseded by that authorization, not deleted.
> No migration, live providers or Git publication; owner acceptance remains separate.

# I3-M1 — implementation preparation

Prepared October 23, 2026; reconciled October 24, 2026 with the owner's
**I3-M1 Additional Owner Clarifications**. **Proposal for owner review; no source
implementation authorized or performed.** Waiting semantics and canonical integer
seconds are owner-approved architectural requirements; remaining representation,
format and implementation proposals retain their review boundaries.
Selected package: **I3 — Continuing Gameplay Integrity V1**.
First milestone: **I3-M1 — Durable Consequential Continuity and Safe Resumption**.
Risk: **Elevated** (persistent semantics, restoration and cross-system continuity).

## Authority and verified state

The owner's Design → Implementation Preparation Handoff authorizes package selection,
architecture assessment, an isolated worktree and first-milestone lifecycle staging.
It expressly stops source work until this report has been reviewed. Selection is
not acceptance of the proposed persistence model, save format or migration.

- Repository: `Mixelplux/AI-RPG`, origin `https://github.com/Mixelplux/AI-RPG.git`.
- Baseline and preparation HEAD: `a4a9874d0576c353c9c6738f7c9091f8555891ea`.
  Local main, origin/main and read-only `git ls-remote origin refs/heads/main` agree.
- Worktree: `C:\Users\Richard\.codex\worktrees\i3-m1-continuity-preparation\AI RPG`.
- Branch: `codex/i3-m1-continuity-preparation`; initially clean, now an uncommitted
  four-document preparation diff with an empty index. No commit or publication authority.
- Baseline JSON validated complete/idle: no active sprint/package or next sprint;
  latest completed activity I2-M1. This report stages I3-M1 preparation only.
- Original `D:\AI RPG` remains at `618ad922c15d78d9d413cde73420fe1b0ce686fe`
  on `codex/bounded-ai-narrative-realization-v1-10.82`, preserving its dirty
  experiment, owner saves and unrelated worktrees.
- App-managed creation initially used detached HEAD; the feature branch was created
  explicitly. Approved execution outside the sandbox was needed for Git/worktree
  writes. No ACLs changed. The ignored `.venv` junction reuses `D:\AI RPG\.venv`;
  no environment was recreated or substitute interpreter used.
- Shared GitWorkflowTools state tool ran with the established AINarrativeRPG profile.
  That profile reports the original checkout by design; direct worktree checks
  establish this preparation's state. Candidate/evidence/merge operations do not apply.

## Accepted requirements and assessment basis

The [integrated decisions](design/integrated-gameplay-architecture-v1.md) and
[implementation plan](design/integrated-gameplay-architecture-v1-implementation-plan.md)
govern I3: IG-09, IG-11–IG-15 and recovery/save-load IG-21, with IG-16–IG-18
applying throughout. IG-01–IG-08, IG-10 and IG-20–IG-23 remain obligations of
the common I1/I2 runtime. **IG-19 remains excluded.** This milestone is bounded
evidence, not completion of every I3 or upstream gameplay requirement.

Also reviewed: [Information Foundation](design/information-foundation-functional-design-v1.md)
D1–D16, [adjudication](design/information-grounded-adjudication-v1.md) D-A1–D-A6,
[F05](design/f05-authorized-activities-and-player-control.md) D1–D6,
[F01](design/f01-truthful-presentation-and-epistemic-fidelity.md) D1–D10,
[system map](design/systems/system-map.md), [shared doctrines](design/systems/README.md),
[Persistence manifest](design/systems/persistence.md), relevant
[runtime architecture](architecture.md), ADR-011/012/013/025,
[engineering posture](engineering_posture.md), applicable architecture/persistence
[procedures](conditional_procedures.md), and the accepted
[I1](i1_m1_handoff.md)/[I2](i2_m1_handoff.md) handoffs.
Research and previous experiments supply evidence, not new authority.

## Existing implementation: reuse, adaptation and replacement

| Existing responsibility | Assessment and proposed treatment |
|---|---|
| `engine/gameplay_coordination.py` | Reuse interpretation validation, undertaking boundaries, fresh context checks, single-use permits, finite ordinary progression and safe AcceptedStep output. Its serial references, undertaking and pending choices are coordinator-lifetime state. Adapt it to obtain durable undertaking identity/progress from the owning runtime; never serialize pending execution permits. |
| `engine/consequence_integration.py` | Reuse domain discovery, actual-read freshness validation, candidate construction, coherent root replacement and exact-request receipts. State currently holds SessionState, facts, identities, relationships, grants and receipts only in memory. Config contains a callable information supplier/draw and finite declarations. Adapt its aggregate, not a parallel scenario runtime; copying its dataclasses alone would omit authoritative base premises and configuration meaning. |
| `engine/information_adjudication.py` | Reuse finite requirements/binding effects, routine/existing d6, accepted mechanics, costs, commitments and proposal validation. SessionState.history holds private Accepted/Assessment/context objects; replace direct object persistence with explicit domain records. `prepare_candidate` remains a preparation function, not a restoration validator. Attempt.identity and I2 Request equality differ: define durable identity explicitly rather than deriving it from either transient tuple. |
| `engine/information_resolution.py` | Reuse identities, provenance, periods, epistemic/availability distinctions, constraints, Character access and selective queries. It has no campaign export or restoration contract. Adapt InformationView to expose retained history correctly: current I2 puts owned records in the current layer and delegates constraints to its base supplier. Restoring only that overlay would lose hidden terms/dependencies. |
| `engine/activity_control.py` | Reuse F05 decisions: missing means, conflicts, restart_required, resolved reference, meaningful perceived developments and answered choices. It deliberately owns no progress, mechanics or persistence. A restart flag is not a spell mechanic; no unsupported restart rules will be added. |
| `engine/game_engine.py` | Reuse the facade/common I1 path and isolated reconstruction pattern. I2 constructs a fresh Domain/Coordinator per request and guards save/load/reset/adoption and legacy dispatch. Adapt the opt-in path to restore complete owner state and durable activities; retain refusal of unsupported mixed legacy mutation. Audit direct mutators, including advance_time, so they cannot create a second I3 time/truth owner. |
| `engine/save_system.py`, `engine/game_session.py` | Reuse explicit load lifecycle, copied parsing and separate engine construction. Version 1 stores only region_path/world_state; it does not persist I2 or reconstruct Config. Replace direct destination truncation for the new path with validated same-directory atomic file replacement; do not mistake engine reconstruction for atomic disk writing. |
| `engine/world_state.py` and history helpers | Reuse domain validation, stable history IDs and source_history_id links, copied state and bounded history queries. Current history is not a complete acceptance ledger; do not infer receipts, obligations or mechanical results from summaries. |
| `engine/timekeeper.py`, GameEngine time candidate preparation | Retain the owner-prepared candidate/publication contract; adapt general elapsed-time handling to canonical seconds only after source authorization. Existing helpers and dispatch assume hours and the candidate helper invokes scenario owners; do not adopt that bundle as production time policy. Independently assess supported domain transitions, preserving fixture contracts. I2 SessionState.at must not remain a second clock. |
| `engine/scene_continuity.py`, scene/history projections | Presentation memory is ephemeral prose/conditions, not accepted progress or a recovery log. Exclude it from durable truth; rebuild scene/perception and accessible projections from restored owners. Keep the existing historical/current distinction in projections. |

No graph database, universal entity framework, serializer of arbitrary Python objects,
event-sourced campaign, distributed transaction engine or broad refactor is justified.
The concrete gap is complete accepted-state preservation and safe continuation.

## Recommended milestone and integration boundary

Keep I3-M1 as one vertical milestone. A supported authorized undertaking accepts
a meaningful increment, incurs its legitimate costs/time and establishes a fact
and/or commitment; interruption preserves those records. Save, discard the engine,
restore into a new engine, recognize the accepted increment, assess fresh
circumstances, resume the remaining authorized work and retrieve the earlier
consequence in subsequent gameplay. Use the same GameEngine → coordinator →
owning-domain acceptance path throughout, with finite supported suppliers.

Allowed implementation subsystems, after separate approval: common coordination
and activity control; consequence/adjudication/information owners; World State,
history/time and supported causal transitions; persistence/session reconstruction;
safe derived presentation; directly necessary fixtures/tests and documentation.
No general parser, actor agency, unsupported mechanics or production content.

M1 includes the minimum history, temporal applicability, controlled re-entry and
structured failure attribution needed by this sequence. Later I3 work may complete
richer retrospective developments, wider domain coverage, campaign history
selection and diagnostics across paths not exercised here. No later milestone is
selected, staged or authorized. Storage-only or receipt-only demonstrations would
miss the restoration/resumption interaction and are not suitable substitutes.

## Proposed authoritative state and ownership contract

Subject to owner approval, use **one engine-owned campaign root** for the opt-in
runtime, with logical owner sections. It includes the existing supported World State
and a bounded continuing-gameplay section; sharing storage transfers no domain authority.
All fallible preparation occurs off-root; one validated replacement publishes
dependent state and acceptance recognition together.

| Section | Minimum retained consequential meaning |
|---|---|
| Campaign identity and revisions | Stable campaign namespace, record schema marker, accepted revision and non-colliding undertaking/attempt/increment identity allocation. Identity survives process restarts and does not depend on coordinator serials, list positions or prose. |
| World/Character/Actor owner records | Relevant authored definition references and supported current/retained facts, identities, meaningful relationships, binding terms, availability, epistemic kind, holder and Character grants. Include accepted mutable supplier premises, not only I2-generated effects. Actor consent/commitments remain supplied owner facts; no actor-choice algorithm is created. |
| Resources and conditions | Current balances, accepted expenditures, ended/revoked conditions, obligations and their applicable subjects/terms; one owner per mutable value. |
| Undertakings and increments | Actor, objective, activity/target, method, constraints, authorized scope, accepted increment IDs, unresolved next boundary, accepted resolution references, legitimate interruption/status and any still-valid specifically answered choices. Accommodate waiting defined by duration or an authoritative stopping condition, with accepted elapsed progress and unresolved condition basis. Do not persist raw input as authorization or invent a stopping deadline. General event-conditioned waiting execution is deferred. |
| Accepted recognition and history | Immutable request binding, accepted outcome/mechanical result/draw when applicable, costs/time, effect IDs, relevant premise/causal references, acceptance revision and validated safe receipt. Retain enough historical basis to explain accepted commitments and outcomes without replaying them. |
| Fictional time | One canonical integer-seconds timeline with explicit origin for current circumstances, accepted duration, period boundaries, causal history and receipts. Supported input units require explicit conversion at their boundary; no independently mutable hours clock. |
| Runtime exclusions | Pending proposals/permits, callable suppliers, provider objects/credentials, raw model payloads, transient coordinator caches, generated prose and diagnostics are not campaign truth. |

Logical IDs are stable references, not an obligation to register incidental entities.
No semantic rewrite on reload: same IDs, term scope, source/holder, periods and
relationships refer to the same accepted meaning. Referential closure validation
checks all owned and referenced supported records, including hidden constraints
and active-effect definitions. Unavailable established material information stays
unavailable/unresolved; it cannot become an empty or unspecified default.

Finite method/effect declarations and trusted input snapshots must be reconstructible.
Persist supported declarative values and their schema/definition identity; rebind
only known installed domain code. Never import a module, deserialize a callable
or execute a supplier named by a save. Validate the relevant content contract
against installed referenced content; fail closed on material mismatch. Freezing
the relevant supplied declarations/premises avoids relying on whatever a callback
happens to return after restart. This is a bounded snapshot contract, not a new
Region Pack composition or revision-migration system.

## Persistence, compatibility and restoration proposal

**Decision requested, not implemented:** opt-in I3 uses a **version-2 JSON save**
with the existing region reference and World State envelope, adding the explicitly
versioned continuing-gameplay owner section inside World State. Version 1 remains
the existing default production format/path. A separate sidecar would risk
mismatched state/receipts and is rejected for this milestone. Keeping version 1
while silently broadening its meaning is also unsuitable.

ADR-012 says saves persist World State only; the proposed owned section stays in
that state envelope and excludes derived scenes/prose. ADR-013 retains GameSession
construction. Do not alter either accepted decision by implication. Record the
approved durable section/version policy in an ADR before implementing it; if owner
review chooses an external aggregate instead, resolve ADR-012 explicitly first.

| Input / action | Proposed supported behavior |
|---|---|
| Existing valid version-1 save | Continue loading through legacy/default reconstruction with established copied-load normalization. Never silently claim I3 receipts/progress were restored. Existing owner files remain untouched. |
| Version-1 input requested as I3 | Refuse unsupported promotion with a safe compatibility error. No inferred prior acceptance, campaign conversion or synthetic mechanics. Conversion needs separate migration authority. |
| Complete supported version-2 save | Restore all required sections and dependencies into the opt-in common runtime. No accepted section may be missing while reporting successful restoration. |
| Missing/malformed I3 section, unknown version/type, broken IDs, receipt/effect mismatch, unsupported declarations/content | Reject before live adoption. Do not normalize loss into an empty campaign, replay effects to repair state or downgrade to version 1. |
| New I3 save/write failure | Preserve the previous complete destination and live state; report technical failure, not saved success or fictional failure. |
| Reset, rollback or export | Explicit separate operation; not resumption or receipt repair. No cross-branch/global exactly-once guarantee and no automatic reset. |

The proposed version-2 temporal section must declare seconds and campaign origin;
all retained deadlines, periods, accepted timestamps and activity progress must be
consistent before adoption. Missing temporal or condition basis is not permission
to invent a deadline or default to one hour. This refines the representation
proposal; the clarification does not approve the save format or migration.

Version 2 also requires a narrowly approved update to the lifecycle platform
validator, which currently requires exactly save_version 1, and compatibility
checks for both supported runtime modes. **This preparation leaves runtime
SAVE_VERSION, lifecycle platform.save_version and the validator at 1.** No migration
is included. Legacy reader/writer semantics must be regression checked; changes
to them beyond this boundary require review.

Proposed write sequence: capture one consistent accepted root (reject reentrant
capture), validate every owner section, encode fully, write/flush a same-directory
temporary file, then atomically replace the destination. Clean up only the
operation's temporary file. Failure before replacement preserves old bytes.
Specify platform flush/fsync behavior and test injected serialization/write/replace
failures; do not promise power-loss durability beyond demonstrated guarantees.
A save captures accepted progress at its snapshot boundary, not later unsaved play.

Proposed load sequence: parse/version-check → validate representations and reference
closure → validate relevant content/declarations and receipt/effect consistency →
construct isolated owners and derived scene → validate the complete runtime →
publish one prepared root. Prepare all copies and fallible projections before
adoption; current successive _replace_runtime_state assignments alone are insufficient
for the stronger opt-in guarantee. Refuse adoption while an acceptance is running.
Source save bytes and existing live root/scene remain unchanged on any earlier
failure. Rebuild fresh coordinator adapters without executable pending permits.
Loading performs no adjudication, roll, consequence replay, re-entry update or time advance.

Durability means recognition within a successfully saved/restored campaign snapshot.
A crash before explicit successful save may lose unsaved play; automatic journaling,
multi-file commits, cloud sync, concurrent writers and branch reconciliation are excluded.

## Activity, retry and resumption contracts

1. Give undertaking, attempt and accepted increment distinct durable identities.
   Scope accepted-request IDs by campaign. Same ID with a different semantic
   request is an identity conflict, not a fresh attempt. Define a canonical request
   binding including actor/action/target/method/constraints/means/binding scope;
   passage of time alone does not change that accepted request.
2. Receipt lookup precedes current resource/method eligibility for **recognition
   only**. Returning a prior safe result never executes, advances time, charges or
   rolls, even if the resource is now exhausted or a method has become unavailable.
   Historical receipt text is identified as prior acceptance, not current applicability.
3. Continuing unresolved work is a separate assessment: reconstruct undertaking
   scope, retrieve fresh location/means/terms/capability/access/developments,
   enforce initial restrictions and F05, then offer only the next ordinary authorized
   increment. A prior receipt or answered risk is never blanket permission.
4. Restore accepted findings/physical effects, incurred costs, elapsed time,
   commitments and resolved mechanics. Presentation interruption does not resolve
   anything new or confer a new checkpoint. Never reroll an accepted resolution.
5. Reassess changed material circumstances, including hidden terms, lost means,
   access and material risk. Return control where a meaningful choice is required
   and legitimately perceptible; internal hidden causes do not become clarification.
   Specifically answered choices require a matching current circumstance basis.
6. A legitimate new attempt has a fresh identity and renewed applicable authorization;
   preserve the previous result/cost even when trying again. A restart-required
   checkpoint returns control; demonstrate it through an existing supported
   domain rule only. No new spell/search/stealth mechanics to fill a fixture gap.
7. Accept each independently justified increment with its progress and receipt in
   the same root as effects/cost/time. Later rejected/stale proposals preserve prior
   increments and do not create durable permits, results or false fictional failure.
8. Keep current safe display derivation separate from hidden acceptance basis.
   Loss of presentation after acceptance cannot erase truth or cause a second charge.

A situated search can use contract-conforming I1 supplier checkpoints for searched
areas, findings and disturbances, with existing routine/d6 resolution supplied by
Action & Resolution. Search layout, capability and accepted effect declarations
must be explicit owner inputs. Neither a scenario title nor an arbitrary progress
counter selects an outcome. If no existing rule supports a proposed restart example,
record that fixture limit rather than implement a new mechanic.

## Historical, temporal and offscreen boundary

Retain accepted event/result identity, origin, applicable period, consequential
prior facts and causal references. Preserve relevant ended terms/obligations and
accepted mechanical basis even after current applicability changes. Information
retrieval must distinguish historical query from current query; expired truth
is not erased or automatically treated as presently actionable. Existing history
IDs and source links remain stable; I3 acceptance IDs are distinct linked identities,
not regenerated summaries. No exhaustive transcript or per-incidental-event ledger.

### Canonical elapsed time and timed developments

The October 24 owner clarification supersedes the earlier hours-based proposal.
Use **integer seconds** for authoritative elapsed time, with an explicit campaign
origin. Domain durations, period boundaries, history/causal timestamps, accepted
cost-time records and receipts use this same timeline. Preserve exact integer
values across persistence; reject invalid types (including booleans), invalid
ranges and incompatible units before adoption. Runtime views derive from one
owner clock. Wall-clock passage, process restarts and save/load do not advance it.

This resolution does not require per-second simulation. An authorized temporal
advance may cross an interval in one operation, with relevant consequential
boundaries established by their owners and accepted consistently with fictional
time and F05. Do not skip a meaningful interruption merely because the player
authorized a longer wait. Second-level representation implies no tick frequency.

Distinguish three responsibilities:

- **Established duration/expiration rules:** the applicable owner supplies start,
  duration/deadline, applicability and consequential expiration effects. Persist
  sufficient basis and accepted effects/recognition; restoration cannot apply
  consequences again.
- **Established condition-governed developments:** evaluate actual supported
  predicates and authoritative dependencies. A condition need not imply a known
  deadline or guaranteed occurrence.
- **Contextually adjudicated offscreen developments:** establish necessary
  developments through gameplay owners at natural re-entry, respecting causes,
  commitments, elapsed seconds and legitimate access before affected interaction.
  General retrospective adjudication remains later I3 work.

A bounded M1 re-entry fixture may use an already supported declared transition
with explicit timing/condition basis and a retained commitment. After an authorized
elapsed-time increment, current conditions govern re-entry while prior findings
and causal history remain intact; restore/re-entry cannot trigger accepted
consequences twice. Reuse applicable domain contracts selectively. No particular
West Road relocation, market theft, gate/cart behavior or threshold is a production
requirement. Also vary Period/current applicability while preserving historical
consequences. Save/load/rebuild/history queries perform no temporal development
or condition resolution themselves.

### Waiting intent, interruption and persistence

Waiting is a player-authorized undertaking defined by a duration or stopping
condition: for example, a specified duration, dawn, guards leaving, fire ending
or a spell ending. These are semantic examples, not new mechanics implemented
or mandated in M1. Legacy bare wait = one hour is not general gameplay policy;
the coordinator cannot choose an arbitrary stop time or promise an event.

Accommodate duration-based versus condition-based intent in the undertaking
contract. Retain authorized scope/method/constraints, start and accepted elapsed
progress, duration or stopping-condition reference and its legitimate information
basis, accepted increments/resolutions and unresolved continuation boundary.
A condition reference is declarative owner data, not executable code from a save.
Do not invent a deadline when its time is unknown.

F05 meaningful developments, changed circumstances, interruption and player-owned
choices apply during waiting. For event-conditioned waiting, responsible domains
establish relevant circumstances and Character supplies legitimate information:
hidden engine truth alone cannot imply that the character knows the stopping
event occurred. If the needed event/observation capability is unsupported or
established information unavailable, retain an unresolved boundary without invented
timing, knowledge or success.

Restoration preserves this intent and accepted progress, but does not execute
waiting, advance time, resolve a condition or confer continuation permission.
Reassess current circumstances and authorization at the supported continuation
boundary. General event-conditioned waiting implementation is not required for
I3-M1; no new waiting mechanic or scheduler is introduced by this correction.

### General dependencies versus development fixtures

The dependency review separates architecture from accepted development evidence:

| Dependency | Assessment for later authorized implementation |
|---|---|
| timekeeper.advance_time_by_hours and GameEngine.advance_time/_prepare_time_advance_candidate | Shared hour-shaped interfaces/elapsed_hours arithmetic need explicit adaptation or isolation from canonical seconds. The candidate helper also invokes scenario owners; its call bundle is not a universal world-evolution contract. |
| interaction_kernel wait dispatch | Bare wait creates duration_hours = 1 and one-hour prose. Preserve legacy test value while excluding that default from general waiting policy; no parser/behavior change in this correction. |
| Information Resolution Period/query.at, adjudication Method.duration/SessionState.at and I2 acceptance periods | Integer time is representable, but values need an explicit common seconds contract at the I3 boundary. Never silently relabel existing fixture ticks as seconds or hours. |
| Region validation/declarations, material timing and West Road thresholds/history | trigger_elapsed_hours, duration_hours, after_hours and scenario coverage timing have existing bounded contracts. Keep meaningful hourly fixtures/tests; selectively adapt explicitly needed inputs, not geography, mechanics or thresholds into production policy. |

A known hourly duration may map exactly to seconds at an explicitly declared
fixture/input boundary (hours times 3600), including relevant origin, periods and
thresholds. Do not round sub-hour times through a legacy helper or write back a
truncated authoritative hour value. An incompatible legacy-only interface stays
unsupported until a lossless adapter or isolated path is reviewed. New I3 seconds
records do not silently reinterpret existing version-1 saves or unsaved I2 sessions;
no save conversion or migration is authorized.

This validates supported causal continuity at re-entry, **not general retrospective
offscreen adjudication**. That wider I3 responsibility remains later work requiring
its own bounded authorization. No autonomous scheduler, continuous simulation or
outcome selected to favor an unexpressed intention. New unmet temporal mechanics
remain unresolved, not invented.

## Structured diagnostics and failure containment

Use lightweight correlated records for consequential operations: operation/campaign,
undertaking/attempt/increment, stage, safe reason code, acceptance revision/receipt,
relevant internal premise references and persistence phase. Link interpretation →
responsibility selection → retrieval → adjudication → validation → acceptance →
save/restore → presentation; include authorization and distinguish the earliest
failure from any subsequent containment failure. Existing short I2 diagnostic
tuples and coordinator failure fields are a starting point, not full coverage.

Bounded in-memory or explicitly enabled development output is sufficient. Extensive
payload capture, profiling and durable diagnostic logs are optional; ordinary play
does not require them. Mandatory runtime authorization, validation and acceptance
checks remain enabled. Diagnostics never restore truth or decide a fictional result.

Internal references/premises remain private; public responses use approved safe
reason categories and Character-authorized results only. Never log credentials,
raw provider inputs/outputs or hidden premise values to player output. Failures
before acceptance/adoption preserve the old root; failures after acceptance retain
the receipt and permit safe redisplay/retry. No fallible diagnostics callback
between final validation and publication. Save failure leaves live accepted play
intact but explicitly unsaved; load failure leaves the old campaign intact.

## Fixture contracts and validation matrix

Fixtures supply explicit coherent foundations/IDs, mutable owner premises,
relationships/terms, Character access/capability, actor consent, supported
method/effect declarations, geography/checkpoints, interruption/development basis,
controlled existing d6 draws and untrusted proposals. They do not supply scenario
answers, migrate real saves, bypass validation or create mechanics. Fresh restoration
must reconstruct these declared inputs without retaining the original engine,
closure, coordinator, evaluator or access object.

Vary relevant premises independently of wording: capability, equipment, relation
definition, hidden restriction/exception, resource, period, location and elapsed
time. Inspect authoritative owner records and retrieval/application, not merely
matching public prose. Use direct deterministic files under ignored `.artifacts/`,
not TemporaryDirectory, and block network/provider use.

| # | Required case | Evidence required from the common runtime |
|---|---|---|
| 1 | Accepted consequence round trip | Independent restored engine retains result, cost, time, fact/commitment and safe receipt together; no proposal persisted. |
| 2 | Retry after restoration | Same canonical request and ID, exhausted resource and later current time: zero extra draws/cost/effects; changed payload conflicts. |
| 3 | Interrupted undertaking | Accepted searched-area/finding/disturbance progress survives engine discard and restore; continue remaining authorized increment. Review the retained waiting duration-or-condition intent contract without claiming an event-wait executor. |
| 4 | Changed circumstances | Change material access, location or supported condition before continuing; fresh domain retrieval changes permission/result without undoing prior progress. |
| 5 | Initial/resumed restrictions | Paired tests enforce identical missing means, capability, binding and constraint rules; answered risk cannot waive them. |
| 6 | Resolved mechanics | Count controlled d6 calls across interrupted display, reload and retry; accepted resolution retained with no reroll. |
| 7 | New attempt/restart | Fresh authorized attempt gets new identity and applicable fresh costs/mechanics; restart-required policy returns control. Unsupported restart mechanics explicitly unclaimed. |
| 8 | Increment then rejection | Accept one increment, reject/stale the next, round trip; first remains, second has no effect or receipt. |
| 9 | Subsequent dependency | Fresh coordinator/domain retrieves restored accepted fact and commitment through owning information, changing subsequent applicability. |
| 10 | Identity/relationship closure | New consequential identity, active effect/definition reference, source, temporal/access meaning and relation targets remain stable; duplicate/dangling IDs reject. |
| 11 | Recovery/compatibility | Valid v1 remains legacy; v1→I3 promotion refuses; malformed/truncated/unknown/incomplete v2, content mismatch, receipt mismatch and injected reconstruction/adoption-preparation faults leave live root/scene and source bytes unchanged. Inject write/replace failures and preserve old destination. |
| 12 | Technical boundaries | Canonical seconds round trip exactly, including non-hour-aligned timestamps/periods; save/load/rebuild/history query/presentation do not advance time, resolve a waiting condition, draw, charge or replay acceptance. Reject incompatible temporal units/basis. |
| 13 | Controlled natural re-entry | Explicit supported duration/expiration or condition-governed fixture and accepted commitment/causal basis survive restore; developments follow the responsible owner and elapsed seconds before affected interaction, with no repeated trigger or scenario policy promoted to production. General retrospective adjudication unclaimed. |
| 14 | History versus current | Ended/expired condition or prior fact remains historically retrievable with accepted effects while current queries enforce actual applicability and F01 distinctions. |
| 15 | Attribution/access | Inject failures at each consequential stage, including post-acceptance presentation; correlate earliest failure/containment, retain state and reveal no hidden markers/terms through display/errors. |

Later implementation verification: first official-interpreter syntax/static checks
for changed Python, then focused new continuity/persistence tests and directly
affected regressions: `test_consequence_integration.py`,
`test_gameplay_coordination.py`, `test_activity_control.py`,
`test_information_adjudication.py`, `test_information_resolution.py`,
`test_save_load.py`, history/query/context tests, affected F01/F05 and
elapsed-time/material transition tests. Add compatibility/write/recovery fault
injection and an offline owner smoke of the whole sequence. Existing I2 save-refusal
tests need mode-aware qualification, not blanket removal. Profile invariants,
lifecycle/docs/whitespace checks complete Elevated verification. No gameplay tests
were run for this preparation; this matrix is proposed evidence, not passed tests.

## Scaling, exclusions and owner decisions

Snapshot JSON and tuple copies are sufficient for bounded M1, but whole-root copies,
linear receipt/history scans, per-query InformationSnapshot construction and full-file
rewrites will grow with campaign size. Stable IDs, explicit owner sections,
schema/definition versions and bounded selective queries keep logical meaning
independent of those choices. Later indexed storage, paging or migration must
preserve the same meaning; no database backend or performance claim is made here.
Do not garbage-collect receipts needed for retries, unresolved obligations or
causal history merely to meet a cap. Retention/compaction needs demonstrated need
and separate semantic review.

Principal risks: dropping supplier-owned terms/dependencies on restore; conflating
receipt redisplay with renewed authorization; dual clocks/truth owners; incomplete
root adoption; mutable referenced content; historical access leakage; unbounded
linear histories. The contracts and matrix address concrete M1 failure modes
without promising complete upstream systems or large-campaign performance.

Owner decisions required before dependent implementation:

1. Approve this M1 bound, owned campaign-root/continuing-gameplay representation,
   durable activity/acceptance identity contract and declarative input reconstruction.
2. Explicitly approve the version-2 opt-in format, dual-version compatibility policy,
   narrow validator/ADR updates and refusal of v1 promotion. **No migration requested
   or authorized**; choose separately if conversion of existing campaigns is desired.
3. Review remaining bounded re-entry/history/traceability and explicit legacy
   input-adaptation choices. Integer seconds, duration-or-condition waiting intent
   and fixture/production distinctions are already owner-approved clarifications;
   general event-conditioned waiting and retrospective development remain deferred.
4. Separately authorize source implementation and offline Elevated verification.
   Git staging/commit/push/merge and live providers remain separate and unauthorized.

Excluded: IG-19, general language understanding, new gameplay mechanics, actor
simulation, production Region Packs, generic entity/transaction/serialization
frameworks, exhaustive history, provider execution, migration, publication and
subsequent milestones. Approval of this preparation alone must not be inferred.

## Lifecycle, documentation reconciliation and completion evidence

JSON uses the established active state for the selected I3-M1 **preparation**;
scope/goal explicitly stop source work at owner review. active_sprint and
active_capability_package identify only this selected package; latest completed
remains I2 and next_sprint remains null. No unsupported new lifecycle state,
candidate/merge metadata or parallel machine authority is added.

Exact changed-file inventory:

- `docs/current_capability_package.md` — selected I3 package, bounds and authority.
- `docs/current_sprint.md` — I3-M1 preparation stage and stop boundary.
- `docs/current_sprint.json` — sole machine lifecycle authority, Elevated preparation.
- `docs/i3_m1_preparation.md` — architecture assessment, contracts, decisions and matrix.

Meaningful no-change determinations: runtime architecture and system manifests
still describe accepted I1/I2 limitations; proposed I3 is linked from current
package records without claiming implementation. No accepted design/doctrine/ADR
is revised before owner choice. PROJECT/WORKFLOW/AGENTS, runtime, tests, tools,
Region Packs, owner saves and prior handoffs require no preparation changes.
This correction records the approved temporal/waiting clarification in preparation
records; canonical design/doctrine and runtime architecture need no change to claim
an unimplemented capability. An approved implementation must reconcile affected
architecture/manifests and record compatibility and seconds-boundary decisions
before acceptance/publication.

Preparation verification results are recorded below after final checks.
Stop after this preparation handoff; source, migration, providers and publication
remain unauthorized.


### Final preparation verification

- Published baseline confirmed by read-only remote main lookup; worktree branch/HEAD
  confirmed before edits and in final assertions.
- Official initial preflight: 21 passes, zero warnings/blocks/failures.
- Final lifecycle validator: 7 passes, zero failures. An initial active-identifier
  field-shape error was corrected to the existing string contract; no validator
  or schema was changed.
- Final official preflight: 20 passes, one expected warning for the four changed
  preparation paths, zero blocks/failures.
- Official-interpreter JSON lifecycle assertions, strict UTF-8/no BOM, 17 local
  documentation links, all 15 matrix rows, exact four-path inventory and empty
  index checks passed. Git whitespace check passed.
- No source/test/tool/content/save diff. Gameplay tests intentionally unrun.
  No live providers, migration, Git staging, commits, push or merge.
- Environment artifacts remain ignored. The original checkout's status remains
  preserved; no owner save contents were inspected or modified.

## October 24 clarification reconciliation and conflict assessment

| Question | Revised assessment |
|---|---|
| Earlier hours-based recommendation | Material conflict, resolved by this owner's clarification: authoritative elapsed time uses integer seconds. The previous recommendation is superseded, not an additional owner choice. |
| Proposed campaign representation | No structural conflict with one root and domain-owned sections. Refine temporal fields/origin and duration-or-condition undertaking intent; retain accepted progress and unresolved stopping basis without callable behavior. Representation details remain proposals. |
| Persistence/restoration | No conflict with complete snapshots, atomic publication, no replay and no technical time advancement. Require exact seconds/unit/period consistency. Hour-based version-1 records cannot be relabeled or promoted silently. Version-2 policy and later adapter changes still need separate source/format authority; migration remains excluded. |
| Existing architecture and fixtures | ADR-011 retains World State time ownership and does not prescribe hours. Generic hour-shaped helpers/dispatch require later bounded adaptation; fixture mechanics and constants retain test value without production authority. No accepted fixture contract is changed here. |
| Scope | General event-conditioned waiting is accommodated by contracts and remains unimplemented. No waiting, combat, travel, repair, autonomous scheduler or world-evolution mechanics, source, migration, providers or Git publication are added. |

The four preparation documents are reconciled together. Lifecycle stays active
preparation at Elevated risk, with I2 latest-completed, next_sprint null and runtime/
platform save version 1. Approved clarifications do not approve every other
architecture proposal or authorize implementation. Stop for owner review.

### October 24 correction verification

Established lifecycle validator: 7 passes, zero failures. Official worktree
preflight: 20 passes, one expected four-document dirty-worktree warning, zero
blocks/failures. Official-interpreter assertions passed for the revised temporal/
waiting contracts, fixture distinction, superseded hours-policy removal, 15 matrix
rows, 17 local documentation links, strict UTF-8/no BOM, whitespace, unchanged
lifecycle/platform/baseline, exact four-document scope and empty index.
Git diff --check passed. No gameplay tests were run; no source, tests, tools,
content or saves changed. No migration, live provider, Git staging or publication.
