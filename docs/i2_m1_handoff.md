# I2-M1 — Authoritative In-Memory Consequential Integration: implementation handoff

October 23, 2026. **Owner-accepted following review and successful experiential smoke.** Risk: Elevated. The owner approved the preparation direction and authorized bounded source implementation, offline verification, necessary corrections and documentation reconciliation. Separate owner authorization now covers verified publication of exactly the 15 inventory files: staging, one commit, strict fast-forward merge and push. No further source work, live providers, migration or I3 authority is granted.

## Repository and lifecycle

Publication parent: `5567f97506d580c187f9a48cd945500e69562ec4` (previously verified published main). Branch: `codex/i2-m1-consequence-integration`. Worktree: `C:\Users\Richard\.codex\worktrees\i2-m1-consequence-integration\AI RPG`. The accepted implementation is frozen for exact-inventory publication; final commit and remote agreement are reported in the publication response rather than self-referential lifecycle fields. Original dirty checkout, owner saves, unrelated worktrees and shared tools are preserved.

Lifecycle JSON is complete/idle: active_sprint, active_capability_package and next_sprint are null. Latest completed activity identifies this authorized I2-M1 scope only. No later milestone is selected. The preparation report is the accepted direction, subject to the implementation authorization's clarifications; this handoff records actual behavior and limits.

## Implemented architecture and authority

`GameEngine(..., consequence_config=Config(...))` explicitly opts into I2. `process_consequence(Request(...))` binds the supplied structured instruction to the existing I1 Coordinator, F05 decisions and AcceptedStep path. Every call reconstructs the domain/coordinator; authoritative consequences stay in the engine-held Runtime. This deliberately exercises recognition outside adjudication/coordinator object lifetimes. Default GameEngine behavior remains on its accepted production routes.

Trusted Config suppliers declare the controlled actor, supported target/method scopes, finite supported methods, current InformationAccess, initial resources, character grants, controlled existing d6 draws and finite FactEffect declarations. Request cannot grant actor control, target availability, capability or a new method. Fixtures supply these missing upstream responsibilities and explicit premises, never a scenario-name outcome table. Unsupported constraints remain unresolved rather than being ignored; this increment does not infer arbitrary instruction meaning or constraint semantics.

Action & Resolution owns requirements, finite binding semantics, mechanics and proposal validation. `prepare_candidate` reuses the accepted bounded evaluator against a copied trusted state to prepare a result; its disposable state is never the integrated authority. World Simulation owns incorporated external facts/relationships/conditions, Character owns capability/access and resources as supplied, Actor suppliers own consent/commitment premises, and shared aggregate storage does not transfer conceptual authority. Narrative receives accepted accessible meaning only.

The immutable aggregate root holds the copied adjudication state (resources, explicit I2 time, conditions, commitments and accepted mechanics), incorporated identities/facts/relationships/grants, and logical acceptance receipts. Public state reads are defensive copies. The legacy world supplies location/scene premises but is not charged or mutated by the I2 consequential path. I2 resources/time are explicitly supplied for this opt-in runtime, never a mirrored legacy inventory or clock. Coupled legacy/I2 mutations are not supported or claimed. Legacy command dispatch is refused in this mode to prevent a mixed authoritative gameplay path.

## Discovery, incorporation and access

The owning domain starts with actor, target, location, explicit means and related subjects. It selectively follows supported `active_effect`, `definition`, `governs` and `equipment` relationships, instance-definition identity references and fact references in applicable binding terms. This iterative traversal is cycle-safe with a 64-subject ceiling; exhaustion is unresolved. Direct innate capability and linked effect/definition premises use the same adjudication path. Supported binding terms remain the existing finite equality/commitment, block, obligation and legitimate ending semantics; no combat, magic, navigation or other new rules are added.

Read-only InformationView composes base authoritative inputs with accepted domain records, including relationship paths crossing the two sources. It preserves source/temporal/access distinctions. Character traversal cannot follow a hidden internal edge merely because adjudication used it. Material unavailable information stays unresolved; genuinely unspecified facts are distinct from existing, unavailable, uncertain or conflicting information.

Finite FactEffect declarations describe legitimate consequences of supported methods/results. The outcome still comes from capability, retrieved conditions and existing mechanics. On the matching accepted result, new facts require an unspecified slot, valid owner/provenance, subject identity, explicit period and any declared relationship. New identity and relationship references are validated. Existing consequential slots cannot be silently overwritten. Optional visible effects receive explicit Character grants. Later activities obtain facts through fresh authoritative access, not earlier narrative text or a disposable session cache.

## Acceptance and retry integrity

A logical Request.id is distinct from the single-use coordinator permission and authoritative Receipt. Acceptance records actual immutable information reads, including missing/available slots, relationships, binding scope, identity and character projections. It prepares complete costs/time/result/conditions/commitments, incorporated facts/relationships/grants and a safe receipt before publication.

Immediately before publication it rechecks current owning reads, the aggregate root, configuration and copied legacy world premises. Changed relevant facts, relationships, conditions, authorization configuration, resources or legacy premises cause rejection. Supplier failure during final revalidation cannot publish. With the supported synchronous, non-reentrant owner contract, one final aggregate replacement publishes dependent effects and retry recognition together. There is no fallible presentation operation between final freshness validation and that replacement, no distributed transaction layer, and no cross-thread/concurrent-writer guarantee.

Accepted identity plus matching Request returns its existing receipt before new-attempt time/resource/method eligibility, without a new proposal, roll, charge or effect. Conflicting reuse is rejected. Public retry text explicitly labels the earlier accepted result. New logical identities require current authorization/means and new adjudication. Earlier independent accepted increments survive later rejection or technical failure. Accepted blocked/failed attempts can carry legitimate method costs; these differ from invalid or stale proposals, which publish nothing.

Safe receipt construction/validation happens before acceptance. Rejected/technical failures expose no internal reason or hidden cause as a fictional outcome. Structured private diagnostics identify retrieval, adjudication/proposal, validation, receipt or acceptance stages. A later display failure returns a safe presentation-unavailable result; already accepted truth remains recognized on retry. The bounded deterministic projections preserve accessible result meaning and explicitly supplied attribution/limits. No live-generated prose quality claim is made.

## Continuity and save/load

Guaranteed: subsequent supported activities and coordinator/adjudicator reconstruction within the same live engine recognize accepted facts, balances, time, conditions, commitments and receipts. No process restart, engine replacement, save restoration, unattended history or broader I3 recovery is implemented.

Opt-in saves reject in `build_save_data` before destination opening/writing; engine load rejects before file reading or state replacement. Reset/adoption and legacy command dispatch are likewise refused rather than silently dropping I2 consequences. The limit is identified in errors and the smoke tool. Default version-1 save/load continues unchanged and is regression-tested. No save schema, version or migration changed. Stable identities, owner access, periods, provenance and receipts leave a replacement/backing persistence representation available to separately authorized I3 work.

## Verification evidence

- Syntax: changed source, fixture, focused test and smoke tool compiled with the official `.\.venv\Scripts\python.exe` before execution.
- Focused I2: **59 tests passed**, with provider/socket guards. Coverage includes mundane and changed premises, hidden/expired/removed conditions, exceptions and method/actor/target authority, linked definitions and cycles, unavailable/uncertain material facts, cost/time/commitments, new fact/identity/relationship incorporation, fresh later access, composed provenance/access, invalid/stale proposals, resource owner changes, retry conflicts/current-time/exhausted-means/current-method eligibility, partial progress and later rejection, defensive reads, supplier/proposal/validation/receipt/final-acceptance/display faults, reentrancy, save/load rejection before I/O, and default save/command behavior.
- Affected regression scripts: **13 passed**. Their unittest counts are I1 55, F05 policy 11, independent-activity 1, Information Resolution 26, Information-Grounded Adjudication 48, F01 7, material consequence 24 and contextual investigation 15: **187 tests**. Combined with I2: **246 unittest cases**.
- Five additional standalone regression scripts passed: narrative realization (five named boundary checks), Scene Construction (14 offline checks), current-scene projection, player-scene route and save/load. These are reported separately from unittest counts.
- Scripted owner-smoke sequences passed for mundane, hidden-binding and authorized-exception supplied premises. They demonstrate retry counters, a later dependent activity and save refusal, not production language coverage. The owner separately completed successful experiential smoke October 23, 2026 and accepted the implementation and documented limits.
- Regression logs and a script/exit-code summary are ignored artifacts under `.artifacts/i2-*`; no provider was invoked. Final official preflight: 20 passes, one expected dirty-worktree warning, zero blocks/failures. Lifecycle validator: 7 passes. JSON, all affected local documentation links, strict UTF-8, whitespace, exact 15-path inventory, verbatim preserved I1 handoff and empty-index checks passed. The established shared GitWorkflowTools state operation ran with the AINarrativeRPG profile; focused worktree checks ran directly. The subsequent exact-inventory publication uses the official candidate and strict fast-forward tools, with worktree-specific copies of the established profile; shared tools/profile remain unchanged. Accepted source/test/tool files are pinned before publication-only documentation updates and verified unchanged. Existing successful test evidence is reused; mechanical and mutation-safe publication checks are required.

The initial focused run found an invalid provenance owner token and an incorrect rejection expectation for an accepted blocked attempt; both were corrected. Subsequent targeted review added actor/target authority, composed retrieval and current-method retry checks. All final focused checks pass; no unresolved required product failure remains.

## Owner experiential smoke

From this worktree, run:

```powershell
.\.venv\Scripts\python.exe -m tools.smoke_i2
```

Enter `attempt`, `retry`, `use opening`, `save`, then `quit`. Check that the outcome is intelligible, retry is clearly historical, counters do not charge twice, the later activity uses the established opening, and save explains the in-memory limit.

Repeat with `--binding`, then with `--binding --exception`. These flags supply validation premises outside the fiction; player-facing results must not expose their hidden cause. A blocked attempt legitimately spends the declared wedge/effort; retry repeats neither. The blocked case has no established opening, so `use opening` remains unresolved with no added cost. Add `--scripted` for the finite automated sequence. This tool uses explicit contract fixtures and the actual common GameEngine runtime, not a separate gameplay implementation.

## Exact changed-file inventory

Source (4): `engine/consequence_integration.py`, `engine/game_engine.py`, `engine/information_adjudication.py`, `engine/save_system.py`.

Tests/fixtures (2): `test_consequence_integration.py`, `test_fixtures/consequence_suppliers.py`.

Smoke tool (1): `tools/smoke_i2.py`.

Documentation/lifecycle (8): `docs/current_capability_package.md`, `docs/current_sprint.md`, `docs/current_sprint.json`, `docs/i2_m1_preparation.md`, `docs/i2_m1_handoff.md`, `docs/i1_m1_handoff.md`, `docs/architecture.md`, `docs/design/systems/system-map.md`.

Total: **15 paths**, including the four preparation paths already present at implementation start. `docs/i1_m1_handoff.md` preserves the published prior sprint record verbatim so current-sprint rotation does not break I1 architecture links. No source content from the original dirty checkout was imported.

## Documentation reconciliation and remaining limits

Current package/sprint/JSON now record owner acceptance, bounded publication authority and completed/idle lifecycle. The preparation report gains a status note while retaining its historical proposal. Architecture and the system relationship map describe the actual opt-in path, conceptual ownership, freshness/publication and continuity limits. The published I1 handoff is preserved and affected links updated.

No change to accepted Design/IG decisions, ADRs, doctrine, individual system responsibility manifests or deferred-findings register is needed: owners and Partial classifications are unchanged; this is the accepted bounded integration direction, and I3/general mechanics/language remain deferred without a new decision or capability selection. Save documentation in the handoff/architecture distinguishes the opt-in refusal from existing default persistence.

Remaining limits: trusted suppliers own completeness/legitimate grants and finite declarations; actual method/rules and natural language coverage are narrow; constraints beyond the declared policy are unsupported; the 64-subject ceiling fails unresolved; rejected provisional draws are discarded rather than durably retained; later new attempts need new identities. There is no general actor agency, production content integration, durable ledger, cross-session recovery or concurrent writer support. The engine-held aggregate is a bounded implementation choice, not permanent doctrine. No material design conflict remains unresolved.

Owner smoke verified ordinary attempt/retry/dependent activity/save refusal, hidden binding without disclosure, authorized exception, legitimate blocked-attempt costs and no duplicated expenditure/time. The documented limitations are accepted. Stop after authorized publication; do not begin I3 preparation or select a later milestone automatically.
