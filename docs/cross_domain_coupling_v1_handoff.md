# Cross-Domain Coupling Correction V1 — implementation handoff

October 27, 2026. Owner-authorized implementation; owner acceptance pending.
Publication, staging, commits, merge and push are not authorized.

## Repository and authority

- Published `origin/main` and local accepted baseline:
  `6d4216eff053b4a08d667e457ea8be787c695eeb` (read-only remote verification).
- Implementation root: `D:\AI RPG\.artifacts\cross-domain-coupling-correction-v1`.
- Branch: `codex/cross-domain-coupling-correction-v1`; HEAD remains that baseline.
- Original dirty checkout, owner saves, other worktrees and shared tools preserved.
- Elevated risk. One active package; no subsequent package or sprint selected.

Preflight reconciled CD-01–CD-09, PT-D1–PT-D9, F01/F05, Information Foundation,
Information-Grounded Adjudication, Integrated Gameplay Architecture and its plan,
applicable World/Character/Resolution/Persistence manifests, ADR-062/063 and the
published M2 acceptance/continuity/persistence models. Actual dependencies were
inspected in Runtime, Coordinator, GameSession, save_system and consumers. No
material conflict with accepted Design was identified. The owner instruction
explicitly authorizes schema 4, selective replacement and a contract fixture;
it does not authorize a new movement method or a save-envelope change.

## R1 — representation and replacement boundary

Schema-4 Campaign retains a single immutable World/Character aggregate, original
premises, activity authorizations, accepted recognition and revision. Common
ActivityScope owns identity, actor, responsible-domain identity, objective,
authorization/checkpoint, meaningful stages, restrictions, notices and scoped
choice occurrences. A stage has a target and inert owner payload; a run has
identity, activity and inert options. Increment has explicit identity, activity,
stage occurrence, owner options and optional run association.

AcceptedUnit records that command, domain evidence, owner-validated progression
and its validated character-safe receipt. No common unit requires a climbing
request, ruling, distance, speed selection, success/fall field or movement charge.
Domain Contribution composes the validated next World/Character state, evidence,
progression and safe receipt. Common acceptance checks exact types, authorization,
identity, historical reconstruction, whole-state closure and captured-root
freshness before one publication. No fallible operation follows publication.

`domain_dispatch` uses the existing Coordinator/F05 interface for all schema-4
owners. `domain_owners` composes the built-in owner and explicitly installed trusted
contract suppliers. This is a bounded adapter seam, not a universal action engine,
provider proposal router, scheduler or executable persistence registry. Unknown or
competing owners fail closed. Suppliers/code are never persisted. Missing owners
must be explicitly reinstalled to restore their supported campaigns.

## R2 — climbing ownership and gameplay

`climbing_domain` now owns ClimbPlan, ClimbOptions, ClimbUpdate and physical result
composition. It uses the unchanged `traversal_resolution`, `physical_world` and
`character_rules` mechanics. Domain assessment establishes all possible branches,
means, rule applicability, failure stakes, generated identity availability and
F05 exposure commitment before drawing. Recorded evidence is independently
recomputed without sampling. World accepts position/time/falls/relationships;
Character accepts expenditure, damage and immediate vitality effects.

Common progression and choice history ask owners for the relevant decision basis.
Climbing supplies the remaining stages' physical failure circumstances and rule
stakes. The common code binds occurrence, source, scope, perception/opportunity and
stable meaning without interpreting climbing. Changed stakes need a fresh choice;
unrelated revisions do not revoke an answer. Current capacity, access, means and
original restrictions are rechecked before each increment. Accepted identity
recognition precedes new owner assessment. F01 receives only validated accessible
receipts/notices, including loss-of-awareness limits; technical failure is not a
fictional setback.

## R3 — compatibility and integrity

Save envelope remains V3. Schemas 1–3 use finite historical record definitions,
mechanical interpretation, original explicit default additions and ordered
continuity validation in `historical_campaign`, `historical_activity` and
`historical_persistence`. They continue through the same Runtime and common root
publication boundary. The historical modules have no separate publication or
save-file writer. Schema selection occurs before interpreting colliding record
names; new schema-4 fields are required and old meanings are never promoted.

Historical deterministic/uncertain attempts, unfinished schema-3 activities,
exact retry receipts, corruption rejection and default compatibility remain
covered. Historical files reconstruct without dice or rewriting owner files.
Schema 4 also reconstructs every command/update/response and compares the entire
aggregate before adoption. Unknown records/fields/schema/owners, incomplete
contexts, incoherent costs/effects, mismatched decisions and forged receipts
reject. Existing duplicate-JSON-key rejection and same-directory atomic writer
remain in place. V1/V2 save routes are unchanged. There is no migration API or
production conversion of historical campaigns to schema 4.

## R4 — independent contract validation

`test_cross_domain_coupling.IndependentOwner` is explicitly a mechanical contract
fixture, not implemented repair gameplay. It uses capability less fatigue to
validate changes to established object condition, elapsed time and character
fatigue. It needs no traversal link, surface, climb speed, movement expenditure,
ClimbRequest, ClimbRuling, falling or random draw. Movement attributes remain
unavailable in its premises. Changing capability changes the independently
computed result; fixture code does not supply a canned accepted answer.

The fixture uses production Coordinator, Runtime, common authorization,
acceptance, decision binding, continuity, save_game/load_game, finite codec and
historical reconstruction. It implements only domain mechanics/validation, not
an alternative acceptance, publication or persistence path. Tests cover success,
failed costs, multi-stage progress, interruption, fresh response, restoration,
exact retries, changed stakes, hidden control boundaries, unavailable premises,
stale/forged proposals, atomic-write failure and corrupt-load isolation.

## R5 — verification

Final results:

- Syntax checks passed for changed production Python and tests before execution.
- Focused/affected-system run: 363 tests passed (before three additional final
  schema-4 checks; the final complete run includes all 17 replacement tests).
- Replacement tests: 17 passed, including 23 paired baseline/new climbing cases
  comparing full World/Character state, receipts and draw consumption, plus
  schema-4 corruption, F05/changed-capacity and historical compatibility checks.
- Full established offline runner: **77 commands passed; all 75 root behavioral
  scripts passed**, including V1/V2 persistence and all historical climbing tests.
- PowerShell workflow regression: **29 passed**, including all 16 lifecycle
  fixtures in each of three JSON layouts and intentional 5.1 rejection checks.
- Worktree-bound shared GitWorkflowTools verification: **PASS** at exact baseline
  HEAD; repository mutation detection reported **unchanged**. Mandatory preflight
  and lifecycle validation passed. Index and save-publication checks passed.
- Final diff/whitespace review and exact inventory reconciliation passed.

The first complete offline attempt encountered an unrelated missing tokenizer
cache because the runner uses isolated TEMP paths. A pre-existing local tokenizer
asset was copied into this worktree's ignored artifacts and loaded with network
access blocked; the final complete run used that explicit local cache. No package
installation, dependency change or live provider was needed. The first sandboxed
PowerShell negative-shell check hit AuthorizationManager before its version guard;
the unchanged workflow passed in the approved execution context. No ACLs changed.
These were recovered environment failures, not passed checks on the failed runs.

AST checks prohibit climbing-specific types, mechanical fields and mechanical
imports in common campaign/activity/dispatch/Runtime modules. Finite persistence
vocabulary includes domain payload records without interpreting their mechanics.

## R6 — independent-review integrity corrections

The owner authorized only the three confirmed findings. R1–R5 direction and
scope are retained; no contract redesign, gameplay expansion, schema migration,
candidate, Git staging, commit, merge or push is included.

- **R6.1:** `domain_campaign.apply_unit` now applies the Coordinator's reference
  validator before publication, in addition to typed receipt identity/outcome,
  accessible projection and complete disclosure checks. Duplicate public refs
  cannot survive set comparison and fail in Coordinator after root publication.
- **R6.2:** `climbing_domain.validate_receipt` independently recomputes supported
  receipt meaning from validated results, duration and physical consequence.
  `evaluate` checks the producer's receipt against that meaning before returning
  its contribution. This retains the historical semantic/access check within
  climbing, including loss of awareness, without common climbing interpretation.
- **R6.3:** `domain_campaign.validate_campaign` validates choice history on the
  complete campaign after ordered unit reconstruction, instead of only on the
  empty rebuilt root. Owner-declared remaining-stage premises are compared after
  each accepted event. Intermediate material changes reject even if the final
  history has completed and the choice has expired; unchanged premises preserve
  answers. Acceptance and restoration share this validation before publication.

Four new regressions in `test_cross_domain_coupling.py` cover:

- duplicate refs from an independent owner through direct acceptance and the
  production Coordinator, preserving the exact root, full state, revision and
  accepted identities on rejection;
- invented accessible information and post-unconsciousness disclosure, with the
  receipt producer deliberately returning the same forged text during acceptance
  and restoration, plus legitimate deterministic/fall receipt roundtrips;
- a non-climbing owner declaring fatigue as a material decision premise across
  two stages, where accepted stage-one effects change the later premise; both
  original answers and explicit responses reject, as do unfinished and completed
  forged histories on direct/encoded restoration;
- an answered multi-stage choice surviving state revisions and restoration when
  accepted effects leave its owner-declared premises unchanged.

R6 verification:

- Syntax checks passed for both changed production modules and the changed test
  module before execution; the common-module mechanical isolation checks pass.
- All **4 new focused regressions passed**. The combined replacement/historical
  run passed **162 tests**: all **21 replacement tests** plus **141 historical
  acceptance, consequential climbing and continuity tests**. Evidence:
  `.artifacts/r6-focused.log`.
- Full established offline runner: **77 commands passed; all 75 root behavioral
  scripts passed**, with live provider smoke excluded. This includes existing
  V1/V2 save behavior, schemas 1–3, V3 envelope compatibility, climbing equivalence,
  corruption rejection and the new R6 regressions. Evidence:
  `.artifacts/r6-offline.log`. It used the existing ignored local tokenizer cache;
  no dependency or tooling changes were needed.
- PowerShell workflow regression: **29 passed**, including intentional Windows
  PowerShell 5.1 rejection and all 16 lifecycle cases in each of three layouts.
  Evidence: `.artifacts/r6-workflow-approved.log`. The first sandboxed attempt
  failed at the known legacy-shell negative check (`.artifacts/r6-workflow.log`);
  the unchanged command passed in the established approved context. No ACL,
  environment installation or workflow changes were made.
- Mandatory worktree-bound preflight: **20 passed, one expected dirty-worktree
  warning, zero blocked/failed**. Lifecycle/record validation: **8 passed**.
- Worktree-bound shared GitWorkflowTools verification output is retained in
  `.artifacts/r6-shared-verification.log`; it checks the exact baseline HEAD,
  protected branch, official interpreter, preflight, lifecycle and repository
  mutation detection using the existing isolated profile copy. The shared
  profile and tools are unchanged.
- Whitespace/diff review passes. The index and save-publication diff remain empty.

Receipt validity and complete choice history now gate the authoritative root;
the R6 regressions verify rejection preserves its exact identity and full state.
No common climbing mechanics, new gameplay or save format is introduced. Existing
limits below still apply: owners must declare complete premises and legitimate
access; this is single-process immutable-root consistency with reconstruction
costs, not provenance authentication or cross-process concurrency. No provider
smoke or experiential owner smoke was run.

R6 edits exactly ten files already in the R1–R5 working diff: two production
modules (`engine/domain_campaign.py`, `engine/climbing_domain.py`), the replacement
test module (`test_cross_domain_coupling.py`) and seven documentation/record files
(`docs/architecture.md`, this handoff, `docs/current_capability_package.md`,
`docs/current_sprint.md`, `docs/current_sprint.json`,
`docs/design/systems/action-resolution.md`, `docs/design/systems/persistence.md`).
No additional tracked or untracked source path is introduced by R6.

## Documentation reconciliation

Updated runtime architecture, relevant World/Character/Action/Persistence
manifests, manifest index, relationship map, ADR-063 implementation reconciliation
and package/sprint records. This handoff documents the replacement and evidence;
all descriptions distinguish implementation awaiting acceptance from accepted
Design and published historical work.

No changes to accepted CD/PT/F01/F05 text, shared doctrines, Scenario/Actors/
Narrative/Player Presentation manifests, deferred findings or roadmap: no new
rules, gameplay capability, authority, disclosure contract, deferred capability
closure or package sequencing decision is introduced. The independent fixture
does not satisfy PT-D9's later gameplay swimming/jumping generalization gate.
No changes to the domain mechanics modules or save envelope/atomic writer were
needed; equivalence and existing integrity behavior were retained.

R6 additionally reconciled this handoff, package/sprint records, the runtime
architecture and Action/Resolution and Persistence manifests. The correction
enforces the existing authority, receipt and continuity design; it introduces
no durable architectural decision, new ownership relationship or gameplay rule.
Accordingly ADR-063, the system map, other manifests, accepted design/doctrine,
deferred findings and roadmap need no further R6 change. Only the descriptive
goal text changes in lifecycle JSON; it remains active with no transition or
new package selection.

## Limits and remaining risks

Single-threaded immutable-root freshness remains an in-process guarantee, not
cross-process concurrency or crash journaling. Whole snapshots and repeated
history reconstruction retain existing scaling costs. Structural consistency is
not cryptographic proof of authentic rolls or authoring provenance. Trusted
upstream owners remain responsible for complete premises, legitimate character
access and decision classification. The new fixture proves common contract
independence, not full non-climbing gameplay or general NPC/rules support.
No live provider or experiential owner smoke was run. CLI integration and new
movement methods remain outside this package.

## Exact changed-file inventory

30 files: 21 modified tracked files and 9 new files. No staged changes.
The three older test modules now explicitly exercise historical contracts; their
behavior assertions are retained. New schema-4 and independent-owner assertions
live in the replacement test module. The historical files retain only the
version-specific evaluation/codec/continuity paths needed by schemas 1–3;
publication is shared.

- `docs/architecture.md`
- `docs/cross_domain_coupling_v1_handoff.md`
- `docs/current_capability_package.md`
- `docs/current_sprint.json`
- `docs/current_sprint.md`
- `docs/decisions.md`
- `docs/design/systems/action-resolution.md`
- `docs/design/systems/character-system.md`
- `docs/design/systems/persistence.md`
- `docs/design/systems/README.md`
- `docs/design/systems/system-map.md`
- `docs/design/systems/world-simulation.md`
- `engine/climbing_domain.py`
- `engine/consequence_integration.py`
- `engine/domain_activity.py`
- `engine/domain_campaign.py`
- `engine/domain_dispatch.py`
- `engine/domain_owners.py`
- `engine/domain_persistence.py`
- `engine/domain_state.py`
- `engine/game_session.py`
- `engine/historical_activity.py`
- `engine/historical_campaign.py`
- `engine/historical_persistence.py`
- `engine/save_system.py`
- `engine/traversal_coordination.py`
- `test_activity_continuity.py`
- `test_consequential_climbing.py`
- `test_cross_domain_coupling.py`
- `test_domain_acceptance.py`

## Lifecycle and Git disposition

Implementation R1–R6 is submitted for owner review as an uncommitted working diff.
`docs/current_sprint.json` remains `active` for this package pending owner
disposition; `latest_completed_sprint` remains Physical Traversal M2-2b and
`next_sprint` is null. No package is automatically selected or staged next.
HEAD is the accepted baseline and the Git index is empty. No publication candidate,
commit, merge or push was created. The isolated worktree remains available for
review; the original dirty checkout and owner save are preserved.
