# I2-M1 — Information-Grounded Consequence Integration: preparation report

Publication status, October 23, 2026: owner accepted the implemented milestone and documented limits after successful experiential smoke and separately authorized exact 15-file Git publication. Lifecycle is complete/idle; no later milestone is selected.

Implementation status, October 23, 2026: the owner subsequently approved this direction and authorized source implementation with explicit opt-in continuity/save boundaries. See [the implementation handoff](i2_m1_handoff.md) for actual behavior, verification and limits. Historical preparation wording below records the original review boundary.

Prepared October 23, 2026. **Proposed architecture; source implementation awaits owner review and authorization.** Risk: **Elevated**. Selection and lifecycle staging are authorized; acceptance of this proposal is not presumed.

## Verified repository and authority

- Repository: `Mixelplux/AI-RPG`, origin `https://github.com/Mixelplux/AI-RPG.git`.
- Published baseline: `5567f97506d580c187f9a48cd945500e69562ec4`; read-only `git ls-remote origin refs/heads/main` matched it.
- Isolated worktree: `C:\Users\Richard\.codex\worktrees\i2-m1-consequence-integration\AI RPG`.
- Branch: `codex/i2-m1-consequence-integration`; HEAD remains the baseline. Worktree/index were clean before preparation edits. No commit, index staging, push or merge is authorized or performed.
- Original `D:\AI RPG` remains on `codex/bounded-ai-narrative-realization-v1-10.82` at `618ad922c15d78d9d413cde73420fe1b0ce686fe`, with its rejected experiment, owner saves and unrelated work preserved. Existing worktrees are untouched.
- App-managed worktree creation initially leaves detached HEAD; the feature branch was created explicitly. Git access required approved execution outside the sandbox because the new worktree is outside the original writable workspace. No ACL changes were made.
- Official `.venv` is a junction to `D:\AI RPG\.venv`, following the established worktree practice; no environment was recreated.

Governing records reviewed: PROJECT, AGENTS, WORKFLOW, engineering posture, applicable conditional procedures, the accepted Integrated Gameplay Architecture and I1–I3 plan, Information Foundation, Information-Grounded Adjudication, F01, F05, system map and shared doctrines. IG-19 remains excluded. No conflicting accepted requirement was identified. Concrete runtime ownership and save limitations below are proposals for owner review, not new accepted doctrine.

## Bounded package and first milestone

Select **I2 — Information-Grounded Consequence Integration V1**, with only **I2-M1 — Authoritative In-Memory Consequential Integration** staged. Deliver one reusable extension of I1 through GameEngine: authorized undertaking → domain requirements → selective/iterative retrieval → supported adjudication → current-state validation → coherent authoritative incorporation → character-safe result → later dependent activity.

The first milestone covers all ten owner-requested I2 capabilities within the explicit runtime boundary below. It must not stop at a domain adapter calling a disposable session. Supported operations remain finite: routine attempts, existing d6 competence outcomes, established binding conditions/exception/termination semantics, explicitly authorized resource costs and commitments, and limited incorporation of consequential facts and relationships. Progressive specification must distinguish genuinely unspecified facts from unavailable or conflicting established facts.

Conceptual scope: Action & Resolution, World Simulation, Character capability/access, stipulated Actor consent/commitment inputs, Information Foundation access, and the narrow GameEngine/I1 integration. Narrative work is limited to deterministic accepted accessible result meaning. Persistence is assessed for compatibility; no persistence implementation is selected.

Excluded: general language understanding, new combat/magic/stealth/search/navigation mechanics, autonomous NPC choices, production Region Pack changes, general entity/rules frameworks, graph databases, exhaustive ledgers, unrelated refactors, live providers, save-format changes/migration, cross-session restoration/recovery and I3 implementation. Ordinary supporting movement may remain within an authorized undertaking; meaningful new destination/method/risk choices remain player-owned. No navigation work is included.

## Architecture assessment and reuse decisions

| Existing implementation | Assessment and proposed treatment |
|---|---|
| `engine/gameplay_coordination.py` | Reuse interpretation/undertaking/context/DomainStep/AcceptedStep, F05 checks, single-use context-bound permission and immediate situated continuation. Add only the necessary owning-domain adapter. Coordinator must not learn domain dependency rules or become an adjudicator. |
| `engine/game_engine.py` | Reuse common `process_coordination`/command dispatch and injected domain/context seams. Existing `_publish_candidate` validates world and builds scene before publication; use that candidate-before-publication discipline. Its world/scene assignment alone does not atomically accept a separate resource/commitment/receipt store. |
| `engine/information_resolution.py` | Reuse immutable records, InformationAccess, direct/selective relationship retrieval, constraints, periods, provenance and `for_character`. Keep read-only. InformationSnapshot does not certify supplier completeness or discover omitted rule dependencies. Rebuild views from current accepted owners; a frozen initial snapshot is not live truth. |
| `engine/information_adjudication.py` | Adapt finite Method/Attempt/Assessment/Proposal semantics, three-valued material condition checks, existing d6 use, authorized means/cost checks and safe projections. Extract or reshape only what the integration needs; keep accepted bounded-session callers compatible. |
| `AdjudicationSession` / `SessionState` | Exclude as the integrated authoritative store. Its inventory/ended/obligations/history are private disposable state; constructor rejects restoration. Revision is history length, not live supplier validity. `_assess` performs a fixed first relationship expansion, then selected fact reads; it does not provide a general iterative dependency contract. `_step` compares proposal to assessment but does not recheck changing external premises after callback. |
| `engine/activity_control.py` | Reuse F05 policy; domain discovery cannot silently choose another method, consent, resource or risk. Unavailable internal premises do not become player clarification about hidden causes. |
| `engine/world_state.py`, contextual material action and save system | Reuse supported state validation and candidate preparation where representations actually fit. Do not stuff arbitrary bindings/commitments into unrelated version-1 fields or treat narrative/history strings as executable state. Current save serializes world_state only; it cannot restore new I2 runtime state. |

No replacement coordinator or extra orchestration tier is needed. Keep domain discovery/adjudication behind the existing domain interface and put acceptance with simulation ownership, shared by all supported cases. Tests must cross the actual GameEngine interface.

## Proposed authoritative ownership and acceptance contract

**Recommended bounded choice:** one engine-lifetime authoritative I2 runtime aggregate, held by GameEngine independently of Coordinator and adjudication instances. It contains only the supported I2 domain records, resource balances, controlled fictional time, accepted condition changes/commitments, scoped facts/relationships and acceptance receipts. Conceptual ownership remains World/Character/Actors/Action as appropriate; shared storage does not transfer it. There is one owner per mutable field, with immutable/copying reads. This aggregate is authoritative simulation state for the supported I2 activities, not a proposal cache or transcript.

For this milestone, do not charge both legacy world resources/time and a second I2 copy. Fixtures may supply missing resource/capability/actor premises, but accepted I2 changes belong to the engine-held aggregate. Existing legacy world state supplies relevant location/scene premises through an adapter. Bind their current identity/revision to each proposal. The supported consequential path may not publish coupled mutations across two independent roots. If a required supported effect must change legacy world_state too, extend the candidate to one coherent engine-owned publication root before claiming support; do not sequentially publish stores or broaden legacy mutation routes speculatively. Owner review must confirm this bounded runtime arrangement before implementation.

The concrete acceptance operation must:

1. Bind a logical activity/increment identity to actor, objective, target, method, authorized means/constraints and scope. Keep the acceptance identity distinct from a consumed coordinator permit.
2. Read current authoritative owners and domain requirements. Record sufficient immutable premise values/revisions, dependencies, temporal applicability and mechanics basis; history length alone is insufficient.
3. Build an untrusted proposal and a complete candidate, without publishing effects. Domain checks cover capability, terms, mechanics, authorization, available means, costs, supported fact incorporation and actor consent inputs.
4. Validate against current authoritative premises immediately before publication. Detect changed relevant facts, relationships, terms, access/capability, resources, time or authorization even if they changed after initial assessment. Reject stale/invalid proposals without mutation. A conservative whole-owner revision is acceptable initially; selective optimization is unnecessary.
5. Validate the complete candidate and prebuild the immutable safe receipt. Publish dependent result, costs, time, conditions, commitments, incorporated facts/relationships and retry recognition together with one aggregate replacement. No callbacks or fallible presentation work after validation and before replacement. Synchronous, non-reentrant local execution is sufficient; no distributed transaction engine is proposed.
6. Return AcceptedStep carrying only domain-owned accessible meaning. Later presentation failure cannot undo acceptance or charge again. A rejected proposal is technical/domain rejection, distinct from an accepted fictional failure with legitimate costs.

Receipts are retained authoritative acceptance records with logical identity, immutable result/mechanics basis and safe projection. Same identity and same bound request returns prior acceptance without a roll, cost or mutation, including after coordinator/domain reconstruction. Conflicting reuse is rejected. Retry lookup occurs before new-attempt time/resource eligibility; a later current-time value must not make an accepted retry look like a fresh attempt. New attempts need new identity and current authorization. Rejected proposals create no accepted receipt.

Accepted independent increments survive subsequent rejected increments. Returned public results must retain the earlier accepted meaning even if continuation fails. Coordinator's existing exception containment cannot repair a domain that already published and then threw; validate receipt shape/access before publication and exercise this fault explicitly.

## Domain information-requirement contract

Action & Resolution derives needed subjects, predicates, relevant relationship types, condition scopes, capability/equipment and rule/effect definition references from supported activity semantics. Coordination carries requests; InformationAccess retrieves premises without judging outcomes.

Start with actor/target/location/authorized means and applicable hidden constraints. A retrieved relationship or active-effect reference may introduce another necessary subject/definition; the domain requests it, then reevaluates sufficiency. Direct innate capability and instance → active effect → definition must both work as ordinary dependency cases. Keep traversal selective and cycle-safe. Exhaustion or missing material dependencies returns unresolved, never success by default. No general AI dependency engine is needed.

Supplier contracts state what authoritative scope is complete, distinguish absence from unavailable/uncertain records, preserve meaningful identity/relationships and provide fresh reads or a pinned revision. Relevant actor choices/consent are explicit inputs, not inferred agreement. Validate hidden terms internally. Only Character-authorized facts or legitimately observed accepted outcomes cross to presentation, retaining attribution, uncertainty, temporal meaning and material costs. No internal premise IDs, missing-secret diagnostics or hidden causes appear in clarification or public errors.

New consequential facts require stable identity, owning authority, subject/predicate/value, scope, temporal meaning, provenance and relevant relationships. Validate consistency against established truth and binding terms before incorporation. Subsequent activity retrieves the incorporated record through authoritative access after the adjudicator has been discarded; it cannot consult previous prose or an unaccepted proposal. Meaningfully historical records need only the retention exercised here, not an exhaustive event stream.

## Fixture contracts and validation matrix

Use the existing GameEngine/coordinator path with one consequential domain adapter and common owner/acceptance implementation. Suppliers provide foundations/identities, current premises and revisions, capabilities/resources, character grants, explicit method/consent declarations, controlled d6 draws and controlled untrusted proposals. No scenario name selects a result. Vary premises independently of wording and assert retrieved premises, applied rules, complete authoritative state and public results.

| Case | Controlled authoritative variation | Required evidence |
|---|---|---|
| Mundane obstruction | Established obstruction/capability and routine or existing d6 method | Domain derives requirements and mechanics; no invented magical cause. |
| Hidden binding | Applicable terms present/absent or scoped to another subject/action/time | Legitimate result changes; hidden cause stays private. |
| Authorized exception/method | Exception absent/present; explicit method/resource choice | Terms govern applicability; no substituted method or unspecified expenditure. |
| Ordinary dependency discovery | Direct capability; active-effect relationship referencing a definition | Additional material retrieval follows the reference; changing relationship/definition changes legitimate applicability. No new combat/magic rules. |
| Consequential cost/commitment | Resource count, explicit consent, supported obligation/prerequisite | Cost, time, result and commitment publish together; later activity retrieves them. |
| Progressive fact incorporation | Unspecified detail versus conflicting or unavailable established fact | Only legitimate new fact is incorporated; identity/scope/time/relationships remain retrievable. |
| Later dependent activity | Discard coordinator/adjudicator, retain same GameEngine owner | Fresh domain access recognizes earlier accepted fact, balance, condition or commitment without transcript/session cache. |
| Unavailable/uncertain information | Material unavailable definition/term, then supplier resolves it | Internal retrieval or unresolved; no replacement invention or hidden clarification. Immaterial omissions do not block play. |
| Invalid proposal | Wrong result/cost/method/capability, unsupported fact, missing consent | No partial state, time, cost, knowledge or receipt publication. |
| Stale proposal | Change material fact, relation, resource, condition or authorization after assessment | Current-owner acceptance rejects all dependent changes; existing accepted state retained. |
| Retry | Same accepted identity, changed time, exhausted resource, reconstructed domain; conflicting payload | Prior result reused without charge/draw/effect; conflicting identity rejected. |
| Accepted increment then rejection | Accept a legitimate finding/cost; reject next step | Earlier authoritative progress and accessible result remain intact. |
| Technical faults/access | Supplier/proposal/candidate/safe-receipt error; presentation fault after publication | Earliest stage attributed; pre-publication faults do not mutate, post-publication retry recognizes acceptance; no hidden leakage. |

Focused implementation verification later: syntax/static checks, new integration tests, `test_gameplay_coordination.py`, `test_activity_control.py`, `test_information_resolution.py`, `test_information_adjudication.py`, relevant F01/F05 checks and affected material/save regressions where touched. Keep network/provider guards enabled. Preparation runs only mechanical preflight/record/JSON/whitespace/scope checks; no gameplay tests have been run for this task.

## Continuity, I3 compatibility and owner decisions

The proposed guarantee is authoritative recognition across activities and reconstructed domain/coordinator objects **within the same live engine runtime**. It does not cover process termination, save/load, rollback recovery or engine replacement. In-memory accepted state survives presentation interruption; it is not disk durable. Stable logical identities, explicit time/scope/provenance, owner-controlled queries and coupled receipts/state prepare I3 without implementing it.

**Owner decisions before source work:** approve the bounded engine-held authoritative aggregate and its supported effect set; confirm that in-memory continuity is sufficient for I2-M1; approve the user-facing limit at save/load. Recommendation: expose consequential fixtures only through an explicit opt-in integration runtime until I3, with save/load unavailable there before any file is opened or live state replaced. Default production save/version-1 behavior remains unchanged. Do not silently serialize an incomplete campaign or claim restoration. If production mixed legacy/I2 mutation or save restoration is required now, revise scope/ownership and obtain authority before implementation.

Risks: incomplete supplier scope, finite term semantics, stale relationships, accidental duplicate ownership, malformed post-publication receipts, and language/fixture coverage limits. These are addressed by the matrix and explicit bounded contracts, not general infrastructure. Existing accepted residual retrieval/adjudication/history/complexity risks remain. The proposed aggregate is not accepted merely by lifecycle staging. No owner decision is needed to finish this preparation; implementation awaits the review already required by the request.

## Lifecycle, documentation and verification

`docs/current_sprint.json` alone enforces lifecycle. The established schema offers active/complete/blocked, not a staged state; selection is represented as active I2-M1 preparation with an explicit source-implementation hold in scope. Latest completed I1 remains recorded; next_sprint is null. No later milestone is selected.

Exact preparation inventory: `docs/current_capability_package.md`, `docs/current_sprint.md`, `docs/current_sprint.json`, and this `docs/i2_m1_preparation.md`. No source/test/tool/content/save files change. `.venv` junction and preflight scratch locations are ignored environment artifacts. Prior published I1 handoff remains accessible at baseline Git history; current records now explain the selected preparation.

Documentation reconciliation: update only these package/preparation records. Runtime architecture, system manifests/map, design decisions and ADRs remain unchanged because no runtime behavior or accepted doctrine changed. Their accepted implementation descriptions remain accurate; do not describe this proposal as implemented. No new ADR or deferred capability selection is warranted.

Preparation evidence: initial official preflight passed 21 checks; lifecycle validator passed 7 checks. Final staged-record validation passed 7 checks; JSON lifecycle assertions and documentation links passed. Final preflight passed 20 checks with one expected warning for the four preparation paths, zero failures and zero blocks. Git whitespace and exact inventory/index checks passed; no source, test, save or tool diff exists. Gameplay tests were intentionally unrun. Shared GitWorkflowTools state tool ran with the established AINarrativeRPG profile; its RepositoryPath intentionally reports the preserved original checkout. Focused worktree checks run directly, as WORKFLOW permits. No candidate/evidence/merge operations apply without Git authority.

Stop after this report for owner review. Source implementation, Git publication, live calls, save changes and I3 remain unauthorized.
