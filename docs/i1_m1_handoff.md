# I1-M1 — Common Coordination Runtime: implementation handoff

## Status and repository

Owner authorized bounded implementation October 23, 2026 after preparation.
The owner accepted I1-M1, its correction and documented limits after successful
experiential smoke October 23, 2026, and separately authorized Git publication.
Risk: **Elevated** for authorization, access and cross-system coordination.

- Publication parent: `ab3014357759a522d7a281325da9c5bc64ac636c`.
- Branch: `codex/i1-m1-coordination-foundation`.
- Worktree: `D:\AI RPG\.artifacts\i1-m1-coordination-foundation`.
- Publication authority: exactly the 12 handoff files, one verified commit,
  strict fast-forward merge to main and push; no additional source changes.
- Original dirty checkout, owner saves, existing worktrees and shared tools are preserved.
- Official `.\.venv\Scripts\python.exe` uses the established junction to the
  existing environment; no unofficial environment was installed.

JSON remains the sole machine authority. The authorized I1-M1 scope is complete
and idle: active_sprint, active_capability_package and next_sprint are null.
Latest completed activity and sprint.id are
`i1-situated-gameplay-coordination-foundation-v1`; the title identifies I1-M1.
This closes only the authorized milestone scope, not later I1 work, I2 or I3.
IG-19 remains excluded.

## Owner acceptance and publication record

The owner accepted the common coordinator, narrow GameEngine integration,
domain-supplied results, situated continuation, natural non-leading boundaries,
accepted-result/F05 safeguards and the documented fixture/language/domain limits.
Successful owner experiential smoke occurred October 23, 2026. Separate explicit
authorization covers staging exactly the 12 inventory files, one candidate commit,
verified strict fast-forward merge and push from parent
`ab3014357759a522d7a281325da9c5bc64ac636c`.

Publication makes no source/test/tool changes. Their five file contents are pinned
before documentation reconciliation and checked again before commit. Existing
230-test, F01, script, compatibility and four-smoke evidence remains valid and is
reused under WORKFLOW.md. Required publication checks cover official Windows/
interpreter preflight, lifecycle/JSON, whitespace, exact inventory, mutation-safe
verification, committed parent/tree and clean worktree/index. Final Git identities
and actual remote agreement are reported in the publication response rather than
creating a self-referential commit field or extra lifecycle-only commit.

Nonblocking owner observation: `search west` currently implies movement. Future
integration must distinguish reasonable movement inherent in an authorized
undertaking from movement or method choices requiring separate authorization.
No I1-M1 source correction is required or made. This observation remains attached
to this accepted handoff; it neither selects nor authorizes I2/I3 work.
## Owner correction — situated progression and result presentation

Owner authorized this Elevated I1-M1 correction after experiential smoke on
October 23, 2026. The owner accepted the corrected implementation and separately authorized publication.

**Root cause:** the fixture receipt projected only generic completion text, and
`Coordinator.process` returned after one accepted step without assessing current
continuation. Every F05 control stop used one clarification/menu presentation,
conflating ambiguity with a natural exploration decision point.

**Corrected behavior:** receipts preserve the domain's explicit positive, negative,
incomplete, unresolved or complete meaning and its immutable Character-safe result
projection. A domain may supply newly accepted information which could not have
been in pre-execution context. Missing result text is not interpreted as no findings.
Results are projected separately in `coordination.results` and in the response
message; internal receipt identities and hidden premises remain private.

After each accepted activity, the coordinator gets current context and a fresh
F05/domain assessment. It advances only ordinary authorized, unambiguous supported
steps of the same undertaking, each with a fresh single-use permit and owner
acceptance. It stops at the next actual boundary without a redundant command.
A defensive per-call ceiling of 16 accepted steps reports an unresolved domain
boundary if an owner supplies an unbounded stream. It retains all accepted results,
with no speculative action queue, scheduler, rollback or universal transaction API.

A natural `decision` boundary presents the domain's accessible circumstances and
no automatic menu or leading question. Explicit `clarification` remains available
for material ambiguity and bounded confirmation. Trusted domain steps can supply
exact free-form response phrases mapped to disclosed choice keys. These are
context-bound, match only imperative activity wording, and cannot bypass changed
means, risks, constraints or stale scope. The fixture supports `search east` and
`search west`; this is not general language interpretation or navigation.

The common smoke now produces, directly after `search castle`:

> You finish examining the hall. No useful signs turn up in the areas examined.
> One passage leads east, while another continues west.

These negative findings and passages are explicitly fixture-owned. Refining to
`search castle carefully` presents the boundary without another hall acceptance.
`search west` then accepts the supplied western-passage activity with the new
constraint. Prior costs, results, references and original execution constraints
remain unchanged. With one supported route, the next ordinary activity executes
in the same call; with several, the coordinator chooses no direction.

**Additional tests:** all four result meanings, missing descriptions, hidden
information, same-command result plus boundary, natural text without menus,
both free-form directions and inquiry non-commitment, prospective constraints,
constraint conflicts, automatic single-route progression, changed means, stale
phrases, post-acceptance context failure, later operation failure, and bounded
termination. Accepted work survives a later failure without fictionalizing it.
The first focused run exposed old single-step/menu assertions; those were updated
to assert the corrected boundary/results and actual unchanged or advanced costs.

**Correction file scope (11 files, within the existing 12-file candidate):**
`engine/gameplay_coordination.py`, `test_fixtures/coordination_suppliers.py`,
`test_gameplay_coordination.py`, `tools/play_coordination_smoke.py`,
`docs/current_capability_package.md`, `docs/current_sprint.json`,
`docs/current_sprint.md`, `docs/architecture.md`,
`docs/design/systems/system-map.md`, `docs/design/systems/action-resolution.md`,
`docs/design/systems/player-presentation.md`. GameEngine's existing integration
required no correction. The full candidate inventory below remains unchanged.

**Verification:** syntax checks, 230 focused/affected unittest cases, directly
affected player-scene-route and save/load script entry points, ordinary/heard/
hidden/missing-means offline smoke, and maintained lifecycle/JSON/whitespace/scope
checks passed. Network/provider actions remained disabled. Earlier unaffected
projection/F01 script evidence below is retained; it was not needlessly rerun.
No failed or blocked required check remains. Live semantic evaluation is unrun.

**Reconciliation:** architecture, map and Action/Presentation records describe
result projections, immediate continuation and non-leading natural boundaries.
Lifecycle records preserve implementation/correction authority and complete and idle after
owner acceptance. Accepted Design/doctrine/ADRs, F05 policy, saves and upstream systems
need no changes: their ownership and semantics are preserved. Fixture atomicity
and access remain trusted-owner contracts; I2/I3 guarantees are not added.
## Implementation and contracts

`engine/gameplay_coordination.py` supplies one reusable session-local coordinator:

- **Interpretation:** activity, objective, target, method, inquiry/preparation/
  commitment, constraints, independent intentions and material ambiguity. Shape,
  references and mode are validated; interpretation alone never grants execution.
- **Undertaking:** logical identity, coherent objective/target/method, constraints,
  explicitly answered choices and owning-domain accepted-step references. A
  repeated target/activity retains restrictions; accepted references
  are retained. Explicit continuation revalidates current target/method/means.
- **SituatedContext:** owner-supplied revision/location, supported targets/methods,
  available means, geography/routes, actors, conditions, material unavailability
  and separately referenced character-accessible text. It is an immutable local
  handoff, not a universal world schema or new persistent ownership model.
- **CoordinationDecision:** permission for one situated step, clarification,
  inquiry/preparation assessment, conclusion or unresolved status, with internal
  responsibility/undertaking/context references. Only a safe projection is returned
  through GameEngine. It never serializes the internal decision wholesale.

Trusted `domain.assess(undertaking, context)` supplies one `DomainStep` with its
own checkpoint, applicable responsibilities, required means, supported constraints,
accessible result/choice references and stable step identity. The coordinator
arranges these responsibilities and invokes existing F05 policy. It does not
acquire authority over mechanics, information access, truth or NPC decisions.
`domain.execute` owns atomic execution and returns an `AcceptedStep` receipt.
The coordinator retains accepted references; it does not fabricate outcomes.

`GameEngine.process_command` invokes coordination before contextual action,
investigation and legacy dispatch. A claimed result is terminal even when
ambiguous, unsupported or erroneous. Only `None` from an unclaimed raw command
continues. `process_coordination` accepts a supplied interpretation or explicit
continuation, a supplier-supported direction phrase, or one explicit numbered choice through the same runtime. Reset/load clears
session-local coordination state. No save schema/version changes occur.

The production adapter uses existing character-safe local scene projection for
`observe surroundings` (or the supplied current location alias). It does not
claim a general perception/access engine. Its revision includes local visible
context and time, without publishing internal state. Search/door authority is
absent in production, so claimed instructions remain contained.

## Bounded language support and evidence limits

The small explicit offline grammar supports `open TARGET`, `search TARGET`,
`observe TARGET`, optional `using METHOD`, and `quietly`/`carefully` modifiers.
Targets and routine methods come from context, not a scenario-name lookup.
`Can I ...?`, `Could I ...?`, `How can I ...?` are inquiry; `Prepare to ...` is a
read-only preparation assessment, not physical preparation. Independent clauses,
alternatives, tentative/unsupported restrictions and ambiguous targets do not
execute. A bare question does not become commitment. Methods without an
authoritative routine default require player choice.

The existing `search for ...` phrase family stays unclaimed by this grammar and
retains established investigation handling. No general rule-based language engine,
synonym coverage or LLM interpretation reliability is claimed.

Natural decision points describe established circumstances and yield control without
questions or automatic menus. Supplier-supported phrases express fixture directions.
Explicit clarification may expose numbered IDs and accessible text; internal
choice/risk keys remain private. One explicit choice can be answered per call.
An answer is bound to its disclosed context, not a blanket waiver. Previously
answered choices prevent redundant questions while applicable. Changed context,
missing prerequisites or changed methods cannot be waived by stale answers.

## Reuse and replacement decisions

- Reused `activity_control.py` unchanged for F05 continuation, interruption,
  completion and accepted resolution references; no competing control policy.
- Adapted GameEngine narrowly for context, dispatch, public integration and
  reset/load retirement. Existing owning-state publication operations are unchanged.
- Reused scene/world/perception components for supported observation. Explicit
  fixture access covers unavailable upstream systems, not inferred general access.
- Preserved contextual action/investigation and legacy handling for unclaimed
  commands. Their bounded parsers do not become general interpretation authority.
- Retained InformationAccess for future I2 integration; no full retrieval integration.
  The disposable adjudication session and damaged-gate interpreter were excluded
  as general coordination implementations; their tests provide regression evidence.

## Fixture suppliers and situated evidence

`test_fixtures/coordination_suppliers.py` provides explicit World/Character/Action/
Actor authority for offline validation. It supplies a hall, routes, targets,
methods, means, perceptible or hidden circumstances, access, checkpoints and
accepted results. One fixture minute per accepted activity is stipulated test
data, not an invented game rule. It publishes its own tiny state atomically only
after checks; failure injection precedes publication. It never mutates campaign
world state or reads a scenario ID to pick an outcome.

The same coordinator and GameEngine run these cases:

| Required situation | Evidence |
|---|---|
| Ordinary local action | One authorized owner step/receipt; no coordinator resolution. |
| Inquiry | Description without domain execution, cost or accepted undertaking. |
| Broad castle search | One local activity in the supplied current hall, then route choice; no automatic itinerary. |
| Quiet/careful search | Same activity/undertaking with constraints and Character participation; conflicts/unsupported constraints stop. |
| Door with guard circumstances | Empty scene uses World/Action; actors add Actor participation; heard objectionable-risk development returns control, hidden development does not disclose/interrupt. |
| Method ambiguity | Multiple methods without a routine default require choice; an unavailable method cannot execute. |
| Independent undertakings | Neither activity executes; player chooses one. |
| Changed geography/means | No route blocks, one stipulated route permits ordinary next activity, several routes return choice; missing means stop. Changed location/opaque IDs use the same runtime. |

Negative coverage includes malformed/inconsistent interpretation/context/checkpoint,
unauthorized method/constraint/choice, multiple answers, hidden public references,
known-unavailable material context, supplier faults, stale context/domain steps,
forged/reused permits, changed risk and continuation prerequisites, constraint
retention, and claimed unresolved input reaching legacy. The tests assert no
unauthorized domain activity, fixture cost, campaign mutation, time or resolution.

## Failure containment and targeted Elevated review

Permission is bound to the exact pending decision object and consumed on attempted
execution. Fresh context and read-only domain reassessment must equal the approved
premises/step before calling the owner. Reset, another decision or an attempted
execution retires the permit. Accepted-step references prevent accidental repeats
within the supported undertaking; owners retain their own acceptance checks.

Player output contains fixed safe messages plus references explicitly in the
accessible projection. Raw input, exception text, hidden premise/revision, internal
responsibilities, step references and private choice keys are not serialized.
Interpretation, routing, authorization, context, domain and technical failure
categories remain distinct. Errors/rejections assert no fictional outcome.

The targeted review checked input-versus-authority separation, current-state
checks, F05 reuse, disclosure, constraints, single-use execution and session reset.
It corrected target/method revalidation on continuation, stale choice answers,
numbered public choices, rephrasing constraints and the existing investigation
phrase overlap. No new architectural ownership or persistence decision was needed.

**Trust limit:** context/Character/domain adapters are trusted gameplay owners,
not arbitrary untrusted executable code. They must be read-only during assessment,
include material changes in context/step identity, publish atomically, and validate
their receipts before publication. I1 contains their reported failures and rejects
malformed receipts, but does not roll back a nonconforming owner that mutates and
then throws or returns an invalid receipt. That is not a demonstrated I2
transaction/recovery guarantee. Production observation has no such mutation;
fixture failure tests explicitly occur before publication.

## Verification

- **Passed:** official interpreter syntax checks for coordinator, GameEngine,
  fixture supplier, focused tests and smoke tool before broad execution.
- **Passed:** 55 focused coordination tests: 31 structural tests, 3 bounded
  language groups, 7 integrated GameEngine tests and 14 progression/result corrections.
- **Passed:** combined focused/affected-system command: **230 unittest cases**
  across coordination, F05 control, independent activity, damaged gate, material
  consequence/structural/owner corrections, investigation, action projection,
  information resolution and adjudication.
- **Passed:** interaction-kernel, current-scene projection, scene-context,
  narrative-realization, player-scene-route and save/load script entry points;
  F01 consequential fidelity separately passed **7 unittest cases**.
- All behavioral checks ran with network connections denied. Legacy fake-transport
  checks used an inert SDK client; no live provider invocation occurred.
- Initial focused test assumed `help` reached legacy, but established handling
  claims it; corrected the test. Regression exposed `search for ...` overlap;
  narrowed grammar and reran affected tests successfully. A verification wrapper
  initially blocked even fake transport construction; corrected to an inert client.
  These were resolved failures, not blocked or omitted checks.
- **Passed:** scripted offline smoke with ordinary, heard-guard, hidden-guard and
  missing-means inputs: fixture totals were respectively 3, 0, 3 and 0 accepted
  activities. Automated tests separately exercise accepting a disclosed heard risk.
  Fixture authority supplies results; the coordinator uses the same runtime.
- **Passed:** final lifecycle/JSON, whitespace, official workflow with mutation
  detection, and exact 12-file scope/index checks after documentation reconciliation.
  The generated official profile copy specializes only repository/preflight root.
  Nonblocking warnings are PowerShell 5.1 preference and the expected working diff.
  No formal review packet is required.
- **Unrun:** live semantic/model evaluation, general language accuracy, production
  search/stealth/navigation/NPC validation, I2 acceptance integration and I3 durable
  restore/recovery. These are outside this implementation, not passed checks.

## Exact changed-file inventory and documentation reconciliation

1. `engine/gameplay_coordination.py` — new common contracts/coordinator and read-only observation adapter.
2. `engine/game_engine.py` — narrow runtime integration/context/reset.
3. `test_gameplay_coordination.py` — structural, bounded language and GameEngine checks.
4. `test_fixtures/coordination_suppliers.py` — explicit trusted offline domain suppliers.
5. `tools/play_coordination_smoke.py` — offline experiential smoke using the same GameEngine runtime.
6. `docs/current_capability_package.md` — implementation authority/scope and owner acceptance/publication authority.
7. `docs/current_sprint.json` — existing lifecycle schema, implementation authority and verification scope.
8. `docs/current_sprint.md` — this completion report.
9. `docs/architecture.md` — implemented bounded dispatch/contracts and authority limits.
10. `docs/design/systems/system-map.md` — implementation relationships, unchanged conceptual owners.
11. `docs/design/systems/action-resolution.md` — bounded coordination status and retained outcome authority.
12. `docs/design/systems/player-presentation.md` — claimed/unclaimed dispatch and safe numbered choices.

No changes to accepted Design decisions, doctrines, ADRs, Region Packs, save schema,
provider adapters, or unrelated manifests are necessary: this realizes the accepted
coordination boundary without implementing those systems or changing their owners.
No new deferred finding is introduced; I2/I3 and general semantic evaluation are
already deferred in the accepted plan. Generated bytecode, verification profile,
save-test outputs and any local captures stay ignored under approved locations.

## Owner experiential smoke and stop

From the worktree root:

```powershell
.\.venv\Scripts\python.exe tools/play_coordination_smoke.py
.\.venv\Scripts\python.exe tools/play_coordination_smoke.py --scripted
```

Optional `--guards heard`, `--guards hidden`, or `--no-means` varies supplied
premises through the same runtime. Try inquiry, preparation, `search castle`, `search castle carefully`,
`search west` (or `search east`), and `open door`. The first search already
returns its result and the next natural boundary. Numbered answers remain available
for explicit clarification; they are not required for ordinary exploration. The console makes
fixture ownership explicit; it is not another scenario engine or playable campaign.
Production `GameEngine.process_command("Observe surroundings")` exercises existing
safe projection without fixture gameplay or campaign mutation.

Stop after verified publication. Do not call a model, select another package or
begin another milestone. I2 preparation is handled separately after the owner
reviews the publication result.
