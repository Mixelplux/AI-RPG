# Physical Traversal Core V1a — M2-1 accepted implementation handoff

Owner accepted M2-1 October 26, 2026 after integrity corrections and offline
verification. Elevated risk. M2-1 is complete/idle; the overall Physical Traversal
V1a effort is not complete. This accepted implementation remains an uncommitted,
unpublished working diff. Publication and M2-2 require separate authorization.

## Architecture and ownership

The common consequential `Runtime` now has an explicit new-domain mode, created
through `GameSession.start_domains(Campaign(...))`. Its immutable Campaign root
contains World current physical truth, Character capability/expenditure, scoped
F05 authorization/checkpoints and accepted Action units. There is no legacy
GameEngine world in this mode and no independent traversal truth store.

World owns positions, seconds, physical instances/relationships and causes.
Character owns selected speed, relevant conditions, readiness, legitimate route
access and movement spent. Action owns mechanics and accepted attempt identity.
The existing Coordinator enforces control boundaries over typed input. Domain
preparation and validation confer no new authority on coordination or storage.
See [the pre-write model](physical_traversal_m2_1_design.md) and
[ADR-063](decisions.md#adr-063--opt-in-core-domain-campaign-aggregate).

Acceptance prepares M1 mechanics, dependent position/time/expenditure, accepted
recognition and a safe receipt. Independent receipt validation, complete aggregate
validation and a final captured-root identity comparison precede one publication.
Exact request structure/types are checked before retry matching. Exact accepted
retries return the recorded receipt before current-position reads;
changed meaning under a used identity rejects. New identities still need current
eligibility and authorization. Inert proposals cannot publish themselves.

M1 P3 disposition: deterministic movement no longer requires Strength, Athletics,
proficiency, HP or an unused speed. Named ClimbDependencies replace durable climb
premise tuples. Fall dependency tuples remain provisional, outside the v3 accepted
vocabulary; they must be reconciled before consequential fall integration.

## Consequential evidence

Production `process_increment` tests demonstrate a 5-foot climb moving the creature
from base to middle, advancing World time from 17 to 28 seconds and Character
movement spent from 0 to 10, with stable object/attachment identity and a causal
attempt reference in the same root. A second valid link reaches end at 39 seconds
and 20 movement spent. Real return followed by a new attempt on the same route is
distinct from retrying the first accepted attempt.

Unauthorized, restricted, choice-bearing, unavailable, wrong-position, stale,
forged-cost/result/destination and malformed-receipt attempts publish nothing.
Tests vary authoritative time, position, surface, expenditure and coordination
capacity between preparation and publication. A faulty receipt producer cannot
leave accepted effects behind a Coordinator technical failure. Exact answered
choice keys do not waive missing means or other restrictions. Inquiry/preparation
are read-only. Hidden unavailable bindings block without disclosing their cause.

Independent actor/locality/distance/terrain/special-speed variations yield costs
8, 21, 6 and 16 from the actual M1 rules, without scenario dispatch or scripted
outcomes. Sparse deterministic creatures omit check statistics legitimately.

Version-3/domain-schema-1 save/load preserves World/Character state, object and
relationship identities, scoped authorization, accepted costs/time/results and
retry recognition. Strict finite decoding plus pure reconstruction validates
complete restored meaning before adoption, with no draw or consequence replay.
Corrupt references, state/receipt tampering, unknown versions/types/fields,
duplicate v3 JSON keys at every object depth and truncated JSON reject. Separate
checkpoint resolution reuse is unsupported; non-null `resolution_ref` rejects
before initial adoption, restoration or execution, even for a real accepted ID.
Failed restoration leaves the existing root intact.
Injected encoding, fsync and atomic-replace failures preserve the previous save
and current root and leave no temporary file. Existing v1/v2 behavior is retained;
there is no automatic conversion or invention of missing traversal state.

## Verification

- Approved Windows interpreter exposed by an ignored worktree `.venv` junction to
  `D:\AI RPG\.venv`; no recreated environment, installation or copied interpreter.
- Initial isolated preflight: 23 passed, zero warnings/failures/blocks.
- Ten-file AST syntax passed before broad changed-code execution.
- 331 tests passed after integrity corrections: 31 acceptance/persistence tests,
  including six correction regressions, 54 M1 traversal tests and
  the established 246-test coordination/consequence/continuity/information group.
- Thirteen additional established gameplay scripts passed with socket connections
  blocked: save/load, world update, player scene routing, time/pressure, time/actor
  relocation, time/evidence, actor location/knowledge, evidence traces, interaction
  history, character competence, F01 fidelity and F05 independent activity.
- Project/lifecycle validator: eight checks passed. Its fixture suite: 16 passed,
  including valid v1/v2/v3 records and invalid versions/types/lifecycle states.
- Final ten-file Python syntax, all 25 changed files UTF-8/whitespace, local
  documentation links, exact inventory, scope/save boundary, empty index and
  `git diff --check`: passed. Original implementation preflight: 22 passed, one expected
  dirty-working-tree warning, zero failures/blocks. Summary retained in ignored
  `.artifacts/m2_1_preflight.txt`.

The first focused run exposed four legacy assertions expecting now-irrelevant
Strength/Athletics dependencies. Tests were reconciled to require those inputs for
checks and to invalidate deterministic movement on a material expenditure change.
Subsequent runs passed. Lifecycle staging initially used object IDs where the
validator requires strings; corrected before implementation. The validator's
version allowlist and stale fixture expectations were extended for authorized v3.
Fixtures now use the approved generated directory with bounded cleanup, rather
than temporary directories outside the repository's player-save validation context.

## Targeted architecture review and remaining risks

Reviewed CD/PT/IG ownership, premise sufficiency, hidden information, F05 scope,
receipt/publication ordering, accepted identity, recovery and legacy compatibility.
No material conflict with accepted Design identified. The one publication protocol
uses root identity and owner validation; the finite semantic payload/codec currently
supports climbing. Future methods require supported method records/validators,
not a second root or a different publication protocol. Cross-method generalization
is not demonstrated by this milestone.

Current local tuple scans, full snapshot saves, initial historical validation
premises and repeated growing-history reconstruction scans are implementation
limits. Reconstruction is not linear in accepted-unit count; repeated validation
during play also scans prior consequential units. Performance evaluation remains
deferred; no optimization or persistence redesign is part of these corrections.
Stable IDs and named selected dependencies permit future indexes, selective owner
reads and storage changes without changing fictional ownership. No production
multi-pack compiler, general authored-revision reconciliation, graph database or
exhaustive event ledger was added. Suppliers must already compose applicable
material bindings; unresolved established inputs fail closed.

Execution assumes one synchronous session. No thread/process arbitration,
cross-branch exactly-once guarantee, autosave journal or directory-level power-loss
durability is claimed. Accepted unsaved play remains subject to explicit saving.
No known required verification failure remains.

## Independent review corrections — October 26, 2026

The independent final review identified one P2 blocker and two bounded integrity
weaknesses. The owner authorized these corrections within M2-1; that correction
authorization did not close lifecycle or grant Git publication authority.

- **Checkpoint references (P2):** M2-1 has no separately resolved but unexecuted
  checkpoint result to reuse. All non-null checkpoint resolution references now
  explicitly reject in complete campaign validation and execution authorization.
  This covers dangling IDs, another activity's accepted result and an actual
  same-activity accepted ID whose checkpoint-reuse semantics are unsupported.
  No result is invented. Null checkpoints and exact accepted-command retries
  remain supported through the existing accepted-unit history.
- **Retry types:** shared exact request validation precedes accepted-identity
  lookup without reading current position or rules. Float distance, integer
  Boolean, mutable means and string subclasses cannot pass by Python equality.
  Process, preparation and direct acceptance reject malformed retries without
  changing the live root; valid exact retries retain the receipt without charge.
- **Duplicate keys:** the v3 file decoder detects duplicates throughout nested
  objects, including identical keys and conflicting version entries in either
  order. A v3 version cannot be hidden by a later v1/v2 duplicate. Legacy v1/v2
  last-key-wins decoding is preserved; their full regression checks also pass.

Six new focused tests bring the acceptance/persistence group from 25 to 31.
Subcases exercise initial validation, direct restore adoption, encoded restore,
file load, invalid typed retries at every entry point and nested duplicate keys.
Rejected restoration/retry cases retain the exact live root; malformed file loads
preserve the existing good save and the input bytes. A good save still restores
with stable retry recognition. The complete 331-test group, 13 gameplay scripts,
eight lifecycle checks and 16 lifecycle fixtures pass after correction.
Correction preflight also passes: 22 checks, one expected working-diff warning,
zero failures or blocks. Syntax, UTF-8/whitespace, local documentation targets,
25-file inventory, save boundary and empty-index checks pass.

A separate in-memory invariant recheck reproduced and rejected the original
dangling/cross-activity references, malformed equal-valued retries and duplicate
keys. It verified exact receipt reuse without owner reads, legitimate new attempts,
legacy nested-key behavior and rejection when the root changes during validation.
No additional acceptance blocker was found. The resulting recommendation for
bounded M2-1 acceptance was accepted by the owner October 26, 2026.
Scaling/generalization and later M2 gameplay limitations remain nonblocking and
unimplemented here.

Correction files (within the unchanged 25-file candidate inventory):
`engine/domain_campaign.py`, `engine/traversal_resolution.py`,
`engine/save_system.py`, `test_domain_acceptance.py`, `docs/architecture.md`,
`docs/decisions.md`, `docs/design/systems/action-resolution.md`,
`docs/design/systems/persistence.md`, `docs/physical_traversal_m2_1_design.md`
and this handoff. No new candidate path or subsystem was introduced.

## Explicit limitations and subsequent M2 dependencies

Consequential execution supports deterministic full directed links between
established meaningful positions, with explicit grounded duration. Partial-link
endpoints, uncertain/failed climbing consequences, exposed/protected/near-ground
failure integration, actual falls/injury, changed physical setup during progress,
interrupted multi-increment continuation and broad owner-playable/CLI integration
remain subsequent M2 work. Unsupported checks stop before sampling so technical
rejection cannot silently become safe failure or a free reroll.

The accepted realistic failure matrix remains binding for subsequent M2. Future
contributions must preserve the same coherent root, identity, owner, F05, receipt
and persistence contracts. No swimming, jumping, combat, progression, World Forge,
provider call, narration or general natural-language interpretation is included.
No production content or player saves were changed. No M2-2 has begun.

## Documentation reconciliation

Updated runtime architecture, World/Character/Action/Persistence manifests,
manifest index and relationship map, current package/sprint records, the M2-1
model/handoff and the durable representation decision. Those implementation-review
descriptions preceded owner acceptance; the closure records below establish the
current accepted status. Canonical CD/PT/IG, F01/F05, Information Foundation and Region
Pack Design remain unchanged because their accepted semantics are preserved.
Historical M1 handoffs and ADR-062 remain historical; no rewrite is needed.
Roadmap, unrelated actor/narration/content manifests and deferred-finding register
need no change: no new package, actor agency, narration or authored content is
introduced, and the M1 P3 dispositions and remaining requirements are recorded here.
Correction reconciliation updates the model, handoff, architecture, ADR-063 and
Action/Persistence manifests. Other manifests and package/sprint records need no
further edit during correction: ownership, scope, schema/version and the then-active
review-pending lifecycle were unchanged. The scaling wording records growing-history scans
without claiming linear reconstruction or introducing a performance overhaul.

## Owner acceptance closure and publication preparation — October 26, 2026

Owner acceptance covers deterministic consequential climbing between established
meaningful positions, coherent World/Character/Action acceptance, exact typed retry
recognition, F05 and safe receipts, complete validation and opt-in version-3/domain-
schema-1 persistence. V1/v2 compatibility is preserved without migration. The three
reviewed integrity findings are corrected and no known acceptance blocker remains.

Only M2-1 is closed. Uncertain climbing, hazardous failure/falls, injury,
interruptions/resumption, partial-link traversal and broader playable integration
remain future work. The P3 growing-history reconstruction/scalability concern
remains for later assessment; no performance redesign or M2-2 work is authorized.

Closure changes only this handoff, `docs/current_capability_package.md`,
`docs/current_sprint.md` and `docs/current_sprint.json`, all already in the original
25-file inventory below. The other 21 candidate files, including all runtime code,
tests and validation tools, remain byte-for-byte unchanged from the accepted diff.
Technical model/architecture/manifests retain their reviewed semantic descriptions;
earlier candidate labels describe their pre-acceptance review state. These closure
records establish acceptance without changing those semantics or widening scope.
Canonical design, historical records, roadmap and deferred-finding register need
no edit because this task changes only acceptance/lifecycle/publication readiness.

Retain the successful 331-test and 13-script offline evidence above. No executable
content changes in closure; gameplay tests are not rerun for record-only edits.
Lifecycle validation, documentation links, syntax, whitespace, exact inventory,
save boundary and preservation checks verify publication readiness. Publication
itself is not authorized: stop before Git staging, commit, merge or push. No formal
committed candidate or review packet is created by this preparation.

Closure validation passed: eight lifecycle/project checks, 16 fixtures, AST syntax
for all ten candidate Python files, UTF-8/whitespace and local documentation-link
targets, `git diff --check`, exact 25-file inventory, empty index and player-save
publication boundary. Session comparisons verified that only the four closure
records changed and the other 21 candidate files are byte-for-byte unchanged.
Published parent/branch remain the values below. No blocker remains for requesting
separate publication authorization; no Git publication action has been performed.

## Exact changed-file inventory

- `docs/architecture.md`
- `docs/current_capability_package.md`
- `docs/current_sprint.json`
- `docs/current_sprint.md`
- `docs/decisions.md`
- `docs/design/systems/README.md`
- `docs/design/systems/action-resolution.md`
- `docs/design/systems/character-system.md`
- `docs/design/systems/persistence.md`
- `docs/design/systems/system-map.md`
- `docs/design/systems/world-simulation.md`
- `docs/physical_traversal_m2_1_design.md`
- `docs/physical_traversal_m2_1_handoff.md`
- `engine/character_rules.py`
- `engine/consequence_integration.py`
- `engine/domain_campaign.py`
- `engine/domain_persistence.py`
- `engine/game_session.py`
- `engine/save_system.py`
- `engine/traversal_coordination.py`
- `engine/traversal_resolution.py`
- `test_domain_acceptance.py`
- `test_physical_traversal.py`
- `tools/test_project_records.ps1`
- `tools/validate_project_records.ps1`

## Repository and lifecycle status

Repository: Mixelplux/AI-RPG. Worktree:
`D:\AI RPG\.artifacts\physical-traversal-v1a-m2-1`.
Branch: `codex/physical-traversal-v1a-m2-1`.
HEAD/baseline: `4399e57bfcaf604b83c7079da63c0a62024d6f8c`, matching local main
and origin/main. Original dirty checkout, player saves, shared tools and unrelated
worktrees were preserved. Shared workflow state tooling ran read-only; its profile
still targets the original checkout, so isolated checks used explicit roots.

All listed changes are unstaged/uncommitted; the index is empty. No commit, merge,
push or publication was performed. M2-1 owner acceptance is recorded October 26,
2026. JSON lifecycle is complete/idle: active sprint and package are null, latest
completed is `physical-traversal-v1a-m2-1`, and next_sprint is null. The original
25-file accepted inventory is preserved. No next capability is selected or staged.
Ready for separate Git publication authorization; stop here without publication
or M2-2. Closure of M2-1 does not claim completion of Physical Traversal V1a.
