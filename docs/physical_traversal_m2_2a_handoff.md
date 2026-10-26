# Physical Traversal Core V1a — M2-2a acceptance and publication-readiness report

**Owner accepted M2-2a October 26, 2026**, including all three corrected P2 invariants.
Risk: Elevated. This is an unstaged, uncommitted working-diff handoff, not a final
committed review candidate. No live providers, staging, commits, push or merge.

## Repository and authorized boundary

- Repository: Mixelplux/AI-RPG.
- Published baseline and unchanged HEAD: `62058d3fbed65b01827802c789cbc86a3bd05a42`.
- Branch: `codex/physical-traversal-v1a-m2-2a`.
- Isolated worktree: `C:\Users\Richard\.codex\worktrees\physical-traversal-v1a-m2-2a\AI RPG`.
- Source scope: World, Character, Resolution, common Runtime/Coordinator integration,
  existing persistence and directly affected tests/documentation.
- Lifecycle is complete/idle: no active package or sprint; latest completed is
  M2-2a; next_sprint is null. Overall Physical Traversal V1a remains incomplete.
  No later milestone/package is selected or started.

Preflight verified the exact published commit, original dirty checkout and existing
worktrees. The app created this new isolated checkout. Its sandbox context initially
prevented Git status; a narrow authorized escalation verified the clean checkout,
created the feature branch and exposed the existing approved Windows environment
through an ignored `.venv` junction to `D:\AI RPG\.venv`. No environment was
recreated, no package installed and no ACL or shared-tool modification performed.
Initial preflight: 21 passed, zero warnings/blocks/failures. Shared GitWorkflowTools
state tooling ran read-only with the established profile; it still targets the
original checkout, so isolated validation used explicit roots.

## Implemented behavior and ownership

The [pre-source model](physical_traversal_m2_2a_design.md) reconciles PT-D1–9,
CD-01–09, IG, F01/F05, manifests, ADR-063 and M1/M2-1 handoffs. No material Design
conflict was found. CD-02 contextual rulings supply check stakes where core rules
leave them open; this does not introduce a universal numerical fall rule.

World fixes meaningful support during the check, exposure, landing/drop/medium,
assistance, protection and unresolved material bindings. Resolution requires a
matching explicit contextual ruling: failed progress on load-bearing footing or
failure to maintain grip during a grip-dependent attempt. Character supplies real
check statistics, conditions, movement, readiness and legitimate route access.
Fixtures supply these premises, not success, failure, fall damage or post-roll
supports. No named scenario branch is present.

After the mechanical objective result, World independently composes supported no
progress, grip loss held by verified taut protection, or an actual fall to the
already established landing. The currently supported protection arrangement requires
intact rope/harness/anchor,
anchor secured to a place, rope secured to anchor and attached to harness,
harness attached to creature, taut/load-bearing premises and Character readiness.
A carried rope or a convenient invented support cannot prevent a fall.

F05 gates intent, restrictions, means and choices. Grip-dependent uncertainty also
requires the exact established risk reference in scoped answered choices. Read-only
assessment never samples; execution samples once after branch sufficiency. The
contextual ruling explicitly fixes failed-attempt movement effort before sampling;
success uses actual climbing cost. The scoped World duration is fixed separately.
Failure is not automatically free or automatically charged the whole route.

An actual solid-ground fall records capped d6 damage. Character applies temporary
HP, current HP, Prone, Unconscious/Incapacitated, immediate massive-damage death or
explicit monster-style instant death, and the minimum immediate damage-at-zero
state. World accepts the landing/fall/time and required drops of held objects;
independent attachments survive. Zero-HP/dead/Prone ordinary climbing is unavailable
in schema 2. No subsequent death-save turn or recovery executor exists.

The same immutable Campaign root and common Runtime remain authoritative. All owner,
receipt, reference and aggregate checks precede a final captured-root comparison
and one publication. Stale or invalid proposals publish no failure, damage, time,
expenditure or partial result. Safe receipts describe accessible effects without
hidden causes, internal fall geometry or facts arising after loss of awareness.
Exact typed accepted retries return saved receipts before owner reads or draws.

## Randomness, persistence and compatibility

The runtime owns a controlled die supplier (injectable offline, SystemRandom by
default); accepted units record check and damage dice. Pure evaluators validate
recorded die count/type/bounds, modifiers, totals, objective result, World disposition,
fall mechanics, Character effects and receipts against historical domain state.
Validation does not invoke the sampling resolver or use a replaying random callback.
Full reconstructed-state comparison precedes adoption. Stale adoption also rejects.

Envelope v3 remains; domain schema 2 explicitly opts into the new vocabulary.
Schema 1 retains prior deterministic meaning. Its finite legacy decoder supplies
only newly added default fields; schema 2 requires complete records. An intentional
fixture was produced with the unchanged published M2-1 codec, including a sparse
zero-HP premise that was historically valid in schema 1. Restoration preserves that
historical meaning; schema 2 enforces current injury eligibility. There is no silent
promotion, migration or invented traversal state. V1/v2 remain unchanged.

Same-directory flush/fsync/atomic replacement is reused. Corrupt files, unsupported
schemas/records, missing new fields, forged mechanical/consequence/receipt fields
and incoherent current state reject without adopting a candidate. Save failure
preserves the previous bytes and root. Accepted retries after load repeat no draw,
damage, time or expenditure. Validation establishes internal coherence, not
cryptographic authenticity against a comprehensively rewritten coherent save.

## Owner-authorized independent-review corrections — October 26, 2026

The independent read-only review identified three confirmed P2 findings. The owner
separately authorized these bounded corrections, preserving accepted Design, the
existing implementation scope, all 24 candidate paths and unstaged/uncommitted state.
All three defects were reproduced before editing:

| Original reproduction | Before correction | Corrected evidence |
|---|---|---|
| Existing object `attempt:one:fall`; repeat the same attempt with dice 1/3/4 then 20 | Failure technically rejected after d20/d6/d6; the same ID then accepted success | Both requests and direct preparation reject with zero draws and unchanged root; fall and causal IDs tested against all eight World identity groups |
| Anchor secured at base but explicitly located at the landing 20 feet below | Accepted `grip_lost_protected`; contradictory state could restore | Local anchor/worn-harness disposition conflicts reject before sampling and during restoration, including forged accepted history; live root preserved |
| HP 0, maximum 10, temporary HP 10, damage 10 | Alive with one failure after temporary HP absorbed all HP loss | Immediate death at equality uses damage taken; tests cover below/equal/above threshold, zero damage, temporary HP 0/9/10/100, stability and prior counters |

World now checks every proposed causal ID and every possible actual-fall ID against
places, creatures, surfaces, links, objects, history, falls and climb circumstances
before sampling. IDs for a fall that cannot occur are not unnecessarily reserved.
No identity reservation store or publication path was added.

Protection contradiction checks are specific to the supported local fixed-anchor
and worn-harness roles. A rope may retain physically coherent connections to several
places. Coherent explicit anchor/harness locations survive both outcomes; a worn
harness's explicit location follows accepted movement. The possible protected arrival
is checked before drawing, so unsupported retained handling (for example, moving
while still holding the fixed point-anchor) cannot filter out a sampled success.
No release/handling executor or general attachment physics was added.

Character preserves temporary-HP absorption and positive-HP massive-damage overflow.
For an already-zero creature, damage taken supplies the immediate-death threshold,
independently of temporary HP. Nonzero damage still records one immediate death-save
failure, clears stability and kills on the third failure. Tests cover equality,
neighbouring thresholds, zero damage, PC/NPC treatment and unchanged positive-HP rules.
No later death-save gameplay is introduced.

Eleven focused regression methods were added to the existing test file. They include
ordinary schema-2 climbing with no equipment/protection model and supported uncertain
climbing with no gear, plus coherent extended-rope connections and restoration/retry
without drawing. All original 33 climbing tests still pass. The full prior 372-test
affected suite plus these additions passes (383 total); no unexpected changes to
previously tested accepted mechanics/results were found. Intentionally contradictory
states reject rather than being normalized or migrated.

### Simplicity and future protection arrangements

No material architectural rigidity requiring redesign was found. Ordinary climbing
continues without protection records or equipment detail unless consequential facts
require them. TautProtection is one currently supported arrangement, not a universal
definition of protected climbing. A future bounded arrangement would add its World
premises/disposition validation, applicable Character readiness and Resolution rules,
and finite codec/receipt vocabulary as necessary. The same accepted unit and common
root publication remain applicable; the coordinator gains no outcome authority.
The present finite record types and taut-specific receipt wording require an explicit
extension for another arrangement; they are not claimed as already generalized.
No individual handholds, piton placement, additional protection method or general
physics system was implemented.

## Verification results

| Check | Result |
|---|---|
| Changed Python AST before execution and final syntax review | 10 files passed |
| Final affected-domain/coordination/continuity/information/F01/F05 suite | 383 tests passed across 12 modules |
| Included M2-2a coverage | 44 tests passed, including 11 correction regressions |
| Traversal/aggregate group | 129 tests passed (included above) |
| Established legacy gameplay scripts | 11 passed |
| Lifecycle/project validator | 8 checks passed |
| Lifecycle validator fixtures | 16 passed |
| UTF-8/whitespace, local documentation targets, exact inventory, scope/index/save boundary | Passed |
| Correction preflight and git diff --check | Passed; 20 preflight passes, one expected 24-path working-diff warning |

All gameplay verification blocked socket connections. The 11 standalone scripts
cover save/load, world update, player scene routing, time/pressure, time/actor
relocation, time/evidence, actor location, actor knowledge, evidence traces,
interaction history and character competence. Eight F01/F05 tests ran through
unittest discovery and are included in the 383-test total. No live-provider smoke.

New tests cover unsecured elevated failures, verified taut protection and missing
attachment edges, load-bearing near-ground failure, short harmless actual falls,
damage cap, success/failure, PC/NPC parity and independent World/Character variation,
training/expertise, advantage/disadvantage/cancellation, Exhaustion, Climb Speed,
no natural-1/20 override, explicit effort, unknown/unsupported premises, F05 risk/
intent/restrictions, HP/temporary HP/Prone/zero HP/death, attached versus loose held
items, exact retries/new attempts, stale dependencies/root replacement, malformed
receipts/dice/results, published schema-1 bytes, no-draw restoration, corrupt new
schema files and injected fsync/replace failure preservation.

Resolved execution issues: lifecycle staging values were corrected to the existing
active/string-ID contract before source implementation; one fixture's effort was
updated when its terrain changed; a runpy harness found zero F01 tests and was
replaced with proper unittest discovery; Windows default text decoding interrupted
documentation editing, so those edits were reapplied from exact baseline UTF-8.
These are recorded as corrected issues, not claimed as initially passing checks.
No known required verification failure remains.

## Targeted architectural review and limitations

Reviewed the final diff for domain ownership, pre-roll branch sufficiency, genuine
mechanics, F05 risk scope, hidden access, atomic publication, identity, historical
validation, strict decoding and legacy compatibility. The original implementation
self-review was followed by an independent review finding three P2 issues. The
owner-authorized corrections above are implementation-verified and the bounded
corrected implementation is now owner accepted. No additional independent review or
undocumented experiential smoke is claimed.

- Check stakes and failed effort are trusted contextual rulings constrained by
  actual support; suppliers must compose every applicable material binding and
  preserve risk-reference meaning. This package supplies no general world-content
  compiler, natural-language adjudicator or source-authentication layer.
- Supported protection is a verified already taut load-bearing system. Slack
  catches, dynamic rope forces, uncertain protection, helpers/assistance, mitigation,
  liquid landings/reactions and unresolved effects block before draws.
- Accepted falls here arise from supported climb grip loss. No autonomous external
  hazard scheduler or separate environmental-fall command is added.
- Full-link increments only. Interruption/resumption, changed setup during progress,
  partial-link progress and M2-2b are excluded. Owner acceptance covers this bounded
  model; fairness of supplied contextual stakes/effort remains a content/owner responsibility.
  Cross-method generalization is not demonstrated; other movement methods remain deferred.
- Death-save counters preserve immediate necessary state, including Character's
  damage-at-zero contribution; no subsequent death saves, healing, stabilization,
  revival, combat or full condition/effect engine is implemented.
- No production CLI, narration, interpretation, swimming, jumping, World Forge or
  generalized NPC agency is claimed.
- The known growing-history reconstruction scans, whole snapshots and tuple scans
  remain. No scaling redesign, thread/process arbitration, autosave journal or
  directory-level power-loss guarantee. Provisional draws rejected technically
  remain unaccepted, consistent with prior accepted semantics; no pending-roll store.

## Documentation reconciliation

Updated architecture, the World/Character/Action/Persistence manifests, manifest
index and relationship map, ADR-063's implementation extension, package/sprint
records, the pre-source model and this handoff. These descriptions distinguish
the bounded owner-accepted implementation from Git publication and preserve Partial
system classifications. No new ownership or general transaction decision is made.

No changes to canonical PT/CD/IG, F01/F05, Information Foundation, Region Pack design,
shared doctrines, PROJECT/WORKFLOW/AGENTS, roadmap or unrelated manifests are needed:
the accepted authority is preserved, no next package is selected and no authoring,
actor/narration subsystem or general framework is implemented. Historical M1/M2-1
models/handoffs remain historical. Existing deferred scaling and later gameplay
remain documented here rather than being silently resolved or rescheduled.

Correction reconciliation updated this handoff, the implementation model, runtime
architecture and World/Character/Action manifests. Source changes are confined to
`engine/physical_world.py`, `engine/domain_campaign.py`, `engine/character_rules.py`
and the existing `test_consequential_climbing.py`: ten previously inventoried paths
changed during correction. Persistence codec, save versions, ADR-063, system-map and
manifest index need no additional changes: the record vocabulary, semantic owners,
acceptance contract and compatibility policy are unchanged. At the correction handoff,
package/sprint records pointed here for pending review and lifecycle JSON was unchanged.
The separately authorized acceptance closure below changes lifecycle/status records only.
Accepted Design and unrelated historical records remain unchanged. No new architecture
decision or doctrine change was needed.

## Exact file inventory — 24 files

Nine runtime files:

- `engine/physical_world.py`
- `engine/character_rules.py`
- `engine/traversal_resolution.py`
- `engine/domain_campaign.py`
- `engine/domain_persistence.py`
- `engine/consequence_integration.py`
- `engine/traversal_coordination.py`
- `engine/game_session.py`
- `engine/save_system.py`

Two test files/artifacts:

- `test_consequential_climbing.py`
- `test_fixtures/physical_traversal_m2_1_schema1.json`

Thirteen documentation/lifecycle files:

- `docs/physical_traversal_m2_2a_design.md`
- `docs/physical_traversal_m2_2a_handoff.md`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`
- `docs/architecture.md`
- `docs/decisions.md`
- `docs/design/systems/README.md`
- `docs/design/systems/system-map.md`
- `docs/design/systems/world-simulation.md`
- `docs/design/systems/character-system.md`
- `docs/design/systems/action-resolution.md`
- `docs/design/systems/persistence.md`

The save-system draw-injection seam and published-codec compatibility fixture are
directly necessary additional paths within the authorized persistence/testing
subsystems. No production content or player save is part of this diff.

## Preservation and owner action

The original dirty checkout and its player save were not written. Its final
HEAD/status were compared with the initial observation; unrelated worktrees retain
their original HEADs. Existing shared tools and the approved environment were reused.
Generated test outputs remain in ignored `.artifacts/`. Dedicated M2-2a temporary
saves are removed by their tests; established legacy regression outputs remain in
that approved ignored directory. The old published worktree was used read-only to produce
the intentional compatibility fixture in this new checkout.

This isolated index is empty and HEAD remains the exact published baseline. All
24 files remain unstaged/uncommitted. The owner accepted bounded M2-2a October 26,
2026 after the three P2 corrections. Acceptance does not grant Git publication authority.

## Acceptance closure and publication readiness — October 26, 2026

**Owner decision:** M2-2a accepted. Its lifecycle is complete/idle: active package
and active sprint are null, latest completed is `physical-traversal-v1a-m2-2a`, and
`next_sprint` is null. Overall Physical Traversal V1a is not complete. M2-2b remains
unselected and unauthorized.

**Exact accepted contents:** the 24-file inventory above is unchanged (nine runtime,
two test/fixture, thirteen documentation/lifecycle paths). Closure changes only those
thirteen existing documentation/lifecycle records. All nine runtime files, the test
file and the schema-1 compatibility fixture are preserved byte-for-byte from the
accepted corrected candidate. The World identity pre-draw invariant, supported
protection contradiction checks/attachment continuity and corrected damage-at-zero
threshold are unchanged. No player saves or production content are included.

**Meaningful activity and remaining limits:** CD-06, PT-D6 and F05 remain binding.
Traversal extent, contextual effort and time reflect meaningful activity; ordinary
climbing does not acquire mandatory gear, individual handholds, pitons or a universal
six-second loop. Accepted costs, results, object relationships and identity survive;
future interruption/resumption must preserve those requirements without free rerolls.
Interruption/resumption/M2-2b, additional protection arrangements, unsupported fall/
mitigation mechanics, subsequent death-save gameplay, cross-method generalization
and the documented reconstruction/scaling/session limitations remain deferred.
TautProtection is one supported arrangement, not the universal definition of protection.

**Verification evidence:** the successful offline 383-test suite (including all 44
climbing tests and the 11 correction regressions) and 11 legacy gameplay scripts are
retained. No executable content changed during closure, so those tests were not rerun.
The existing v1/v2/v3 compatibility, atomic-write/recovery and no-redraw evidence remains
applicable. Closure verification passed: lifecycle/project validator 8/8, lifecycle
fixtures 16/16, AST syntax for ten Python files, fixture JSON, UTF-8/whitespace,
355 local documentation links across twelve Markdown records, no stale links to
renamed M2-2a headings, exact 24-path scope, empty index, unchanged branch/base/main,
no player-save paths and preservation checks. Runtime/test/fixture and index bytes
match the closure-start snapshot; only the thirteen existing documentation/lifecycle
records changed. This closure did not rerun or relabel the retained gameplay tests.

**Publication readiness and blockers:** this is the accepted, bounded working-diff
handoff, not a committed/frozen candidate. No implementation blocker is known. Staging,
commit, merge and push are not authorized. After separate Git authorization, the
established GitWorkflowTools candidate/verification and strict fast-forward procedures
must be used against the exact accepted worktree and published base. The installed
`AINarrativeRPG.psd1` profile still targets the original dirty `D:\AI RPG` checkout;
future publication must resolve that target through the supported workflow before
any stage-all operation. The shared profile/tools were not changed and no candidate
creation, staging, commit, merge, push or live-provider operation was invoked.

**Preservation:** original checkout status/HEAD, player-save metadata, unrelated
worktree heads, ignored environment target and empty index match the closure-start
snapshot. The original dirty checkout and accepted implementation remain separate.
Shared tooling was read-only. No additional file or substantive implementation change
was needed. The remaining publication blockers are absent Git publication authority
and resolution of the installed profile's target before future candidate creation;
there is no outstanding implementation or closure-verification blocker.

**Stop after acceptance closure and publication preparation. No M2-2b or next package
begins automatically. Git publication requires separate owner authorization.**
