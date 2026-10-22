# Information-Grounded Adjudication V1 — implementation handoff

October 22, 2026. Elevated risk. **Owner-accepted, including the inquiry correction
and experiential smoke; publication explicitly authorized.**
This acceptance/publication record is included in the implementation publication
commit. Its exact identity and parent are verified by the official Git workflow.
Implementation baseline/publication parent: `5f493e48d28f1c8591ec22aa8afeb040fc7738e2`.
Branch: `codex/information-grounded-adjudication-v1`.
Worktree: `D:\AI RPG\.artifacts\information-grounded-adjudication-v1`.

## Functional behavior

`engine/information_adjudication.py` implements one disposable, in-memory owning
boundary over V1a `InformationAccess`. It takes explicitly supplied actor, action,
chosen method/means, target, location, related subjects, time, capability facts,
constraints and F05 authorization. Explicit one-edge relationship retrieval can
expand the constraint scope. Applicable hidden bindings are retrieved internally.
No fixture/scenario identity selects an outcome.

Supported requirements and binding terms govern eligibility, effects and an
authorized ending. Eligible uncertain methods use the existing d6 resolver;
routine methods do not draw. The untrusted proposal boundary follows assessment
and precedes acceptance. Proposals cannot alter chosen means/capability, mandatory
mechanics, result, charges, obligations or ending authority. Rejection is a
technical result with no fictional context, cost, knowledge, history or state
publication. It is distinct from an accepted blocked attempt or mechanical failure.

Accepted elapsed effort, resource charges, obligations, ended bindings, assessment
references and safe observations publish together, after F01 context construction.
The session applies ended bindings and retained commitments in later interactions.
Prior consequential history remains intact. F05 controls perceived developments,
inquiry, withdrawal and constraints. Reusing the same accepted attempt requires
the same undertaking and renewed compatible control; it neither redraws nor
recharges. A failed later narration request leaves the accepted result intact.

Bounded inquiry now follows F05's return of control for `intent="inquiry"` when
the request identifies that character's own previously accepted undertaking.
`step` returns `status="inquired"` and a read-only F01 context: the earlier safe
observation, explicitly historical, plus legitimately granted character facts.
Without additional knowledge it states that the observation alone does not
establish its cause. Inference/report qualifications, attribution and retained
knowledge limits remain intact. Inquiry never assesses a new attempt, calls the
proposal supplier, draws, charges, advances time, writes knowledge or appends an
accepted result. No internal constraint query or diagnostic enters its response.

## Assessment and architecture/reuse decisions

- Reuse V1a's public identity, direct/relationship fact retrieval, applicable hidden
  constraint retrieval and character-grant projection. Its representation and
  retrieval implementation are unchanged. The session overlays its accepted ended
  binding IDs during applicability evaluation; it does not mutate the snapshot.
- Reuse `activity_control.py` unchanged for F05 permission at supplied checkpoints.
  It does not decide gameplay outcomes. Current developments are checked before
  replaying an accepted result.
- Reuse `character_competence.resolve` unchanged for its existing d6 interpretation:
  ordinary 1–2 failure, 3–4 partial, 5–6 full; specialist 1–2 partial, 3–6 full.
  A trusted method selects whether that mechanical policy applies. No new combat,
  casting or skill system is claimed.
- Assess `contextual_action.py` and `material_state.py`: retain their production
  candidate transaction and finite material declarations unchanged. Their authored
  domains are not a general ward/agreement substrate. Generalizing them would
  expand production/persistence scope unnecessarily.
- Adapt the disposable copied-candidate/one-publication pattern of `damaged_gate.py`,
  without reusing its gate parser or preselected lift/repair outcomes. Session
  consequences belong to the existing conceptual World/Character/Actors owners;
  orchestration does not transfer that authority to retrieval or providers.
- Reuse `narrative_realization.validate_context` and its request/realization seam
  unchanged. Only accepted observations, legitimately granted retained information,
  and safe historical meaning enter that boundary. Hidden assessment/provenance is
  never serialized for narration. Deterministic meaning is the smoke presentation;
  no generated prose or live semantic-fidelity claim is made.

The session is a bounded integration harness, not a campaign backend or a new
persistent storage architecture. It has no save/load, Region Pack mutation,
provider adapter or production command-route integration.

## Supported condition/effect semantics

Natural language in V1a `BindingTerms` is **not executable**. Suppliers must supply
the following explicit supported tokens; arbitrary prose/unknown tokens return an
unresolved representation result before proposal generation or state publication.
All terms of applicable active bindings are syntax-checked, even if a trigger
would be false. Ordinary trusted method requirements use the same equality checks.

| Token | Meaning |
|---|---|
| `method=<id>`, `action=<id>` | Equality with the explicitly chosen method/action. |
| `means=<id>` | Membership in explicitly chosen, validated available means. |
| `capability=<id>` | Retrieved objective actor `capability:<id>` equals `yes`. |
| `fact=<subject>\|<predicate>\|<value>` | Retrieved current objective scalar equality; attributed claims/beliefs/inferences cannot substitute for truth. The term vocabulary reserves `\|` as a separator. |
| `commitment=<binding>\|<obligation>` | This actor has that accepted retained session obligation. |
| effect `block` | The attempt cannot complete under that method. |
| effect `obligation=<text>` | Retain the supported obligation with actor and binding identity. |

Prerequisites and triggers are conjunctive; empty groups are true. Exclusions and
exceptions are disjunctive; empty groups are false. An effect applies only when
prerequisites and triggers hold, and neither exclusion nor exception holds.
Thus a false agreement prerequisite means its effects do not attach; a prerequisite
that must prevent an attempt belongs in the method requirements or an explicit
blocking binding. False method requirements produce an accepted blocked attempt.
Effects attach to triggered attempts even when blocked/failed; suppliers must
state exclusions when effects should differ. Obligations are idempotently retained
by actor/binding/value and are not automatically discharged by ending a binding.

Termination and revocation are explicit authorized `end_binding` operations. Each
nonempty group is conjunctive; either complete group permits the ending. The
binding must be retrieved in that ending action's subject/action/time scope.
Its own ordinary effects do not veto its authorized ending, but other applicable
bindings and method requirements/mechanics still govern it. Only a full accepted
result ends it. Ordinary attempts do not silently terminate conditions merely
because a termination operand happens to match. Temporal expiry uses V1a's
existing half-open `Period`; no automatic process or natural-language interpreter
is added. This is intentionally limited condition coverage, not universal rules.

Material fact operands must be available, objective facts; unavailable,
unspecified and genuinely uncertain operands produce distinct unresolved retrieval
diagnostics. Equality/group evaluation is order-independent and three-valued:
a known decisive false conjunction or true disjunction can make a missing operand
immaterial. Likewise a known false trigger/prerequisite or true exclusion/exception
can make other missing binding operands irrelevant. This does not permit unknown
term syntax. Tests distinguish an immaterial absent ward exception for a hook
attempt from that same material omission for a triggered levitation attempt.
Current unavailable truth cannot fall back to an authored default.
Upstream authoritative retrieval may supply the missing slot through V1a's current
overlay. Uncertain attempts with known eligibility can use the d6 mechanic;
uncertain material premises remain unresolved in this increment.

Fictional time is the supplied nonnegative integer session timeline; duration is
an explicitly supplied method cost in those units, not campaign calendar time.
Exactly declared consumable costs apply once to accepted attempts, including
accepted blocked/failed attempts. Missing capability/means and unresolved/rejected
attempts do not consume them. Nonconsumed means must still be actually available.

## Provisional mechanical samples and rejected proposals

Review confirmed that mechanical assessment precedes proposal validation, but its
draw/result is provisional until the complete candidate is accepted and published.
A rejected proposal leaves no accepted attempt, cost, elapsed time, fictional
failure, knowledge or recorded roll. If the caller explicitly retries the same
intended attempt, assessment runs again and the supplier may return a different
draw. The supplier's RNG/sample-stream position is not rolled back; sampling is
not an authoritative fictional consequence. There is no automatic retry.

The focused retry test supplies 1 then 6 to the same intended d6 attempt. A proposal
contradicting the initial failure is rejected with the entire session unchanged.
Retry accepts draw 6, records exactly one result and charges the declared rope
cost once. Subsequent accepted-attempt reuse neither samples again nor recharges.
This preserves D-A5's acceptance boundary and F05's accepted-result continuity;
neither promises retention of an unaccepted technical sample. No pending-roll
storage, new persistence or broader retry machinery is justified or introduced.

## Predetermined suppliers and limits

The focused test module supplies authored foundations, current facts, complete
relevance/relationship scope, coherent term tokens, explicit method declarations,
actor capability, available inventory, controlled draws, F05 developments and
legitimate character grants. The smoke imports those same test suppliers. The
accepted agreement fixture stipulates existing consent/authority; no NPC consent
or agency is inferred. Safe method observations are supplied for each result.
Returned inference/claim records are explicitly stipulated as legitimately
accessible and retain their epistemic status and attribution, rather than being
derived by a new knowledge system.

`propose_assessed` is a predetermined offline proposal supplier. Tests replace it
with invalid responses and failures. It is not an implemented AI model. The
bounded acceptance mechanism verifies proposed contextual conclusions against
supported retrieved premises and mechanics; it does not validate arbitrary prose,
invent facts or allow unconstrained creative consequence proposals. Mechanical
assessment and contextual binding application remain distinct in the trace.

Unimplemented: natural-language authorization, general contextual interpretation,
automatic relevance/completeness discovery, source authentication, comprehensive
magic/physics/rules, inference derivation, arbitrary consequences, agreement
negotiation/discharge, general NPC agency, spatial movement simulation, autonomous
time evolution, campaign persistence and production integration. Location is a
supplied relevance scope, not a simulated character pose/path. Sequential fixture
interactions exercise application of terms and accepted session consequences;
they do not prove full traversal/casting execution or campaign playability.
Safe observation suppliers must themselves preserve the access contract. Test
success establishes this finite coverage, not general AI semantic fidelity.

## Verification evidence and targeted Elevated review

All commands use the worktree's `.\.venv\Scripts\python.exe`, a junction to the
existing official environment. No replacement environment was installed.

- Syntax: new engine, focused test and smoke script compile.
- Focused: `test_information_adjudication.py` — **48 tests passed**, with socket
  connections forbidden. Controlled changes to exceptions, triggers, prerequisites,
  effects, physical facts, current availability, opaque IDs and scope govern the
  shared mechanism. Both hook/levitation orders, ward removal, retained history,
  agreement ending/revocation and subsequent commitment enforcement are exercised.
- Regressions: V1a information, F05 control, independent activity and damaged gate
  — **61 tests passed**. Contextual action/consequence — **24 tests passed**.
  Total: **133 unittest cases**, plus the following script checks. The correction
  reran the 48 focused and 61 information/F05/gate regressions; the 24 contextual
  action regressions remain recorded prior results.
- F01 realization script assertion groups passed with injected suppliers; the
  seven competence script groups (including atomic time/state and compatibility
  rejection) and save/load roundtrip passed under a socket-denial wrapper.
- Scripted offline gameplay smoke passed for ward, agreement and mundane control;
  technical rejection produces no fictional failure. No provider was invoked.
- Lifecycle/preflight, final maintained-workflow verification and whitespace/scope
  checks are recorded with the completion handoff; no repository-wide suite is
  claimed. Generated saves/bytecode/profile are ignored in approved locations.
  The maintained verifier used a generated copy of the official AINarrativeRPG
  profile with only repository/preflight-root paths specialized for this worktree;
  the installed profile and shared tools were not changed. Result: PASS, repository
  state unchanged. A final targeted review corrected immaterial availability
  handling; focused tests and syntax were rerun after that correction.

| Boundary | Evidence and findings |
|---|---|
| Representation | Invalid foundations are rejected by V1a; unsupported material term/effect syntax remains unresolved, including in an otherwise inapplicable trigger group. |
| Retrieval | Hidden location/relationship bindings reach adjudication; a deliberately shallow query has detectable expected omissions. Suppliers still own completeness. Unknown, unavailable and uncertain facts remain distinct. |
| Adjudication | Common equality/group semantics apply changed premises across ward/agreement/mundane cases and opaque identity permutations. Existing d6 policy applies with controlled inputs. |
| Acceptance | Binding bypass, unauthorized means/method/resources/capability, invented obligations/ending, stale or malformed proposal and mechanical contradiction all reject atomically; no fictional context. Defensive copies and reentry guard preserve session ownership. |
| Presentation | F01 serialization excludes hidden cause/diagnostics; granted inference/report retains qualification. A safe-context construction failure rolls back publication; later generator failure preserves an already accepted result. |

Targeted architecture review found no new ownership transfer, campaign mutation,
save format or migration. Accepted state is published once after complete proposal
and safe-context checks; unresolved/rejected paths publish nothing. Compatibility
is established by unchanged production code/content plus affected integrity and
save/load regressions, not by saving this disposable session. No unresolved
required verification failure or architectural blocker remains. No independent
audit or live model evaluation was performed or claimed.

## Documentation reconciliation and exact inventory

Updated runtime architecture, both information Design implementation-status
annotations, system index/map, and Action/Resolution, World, Character, Narrative
and Authored Content manifests. These now record owner acceptance of the bounded
implementation and inquiry correction without changing accepted Design contracts.
Package/sprint records close the accepted milestone as complete and idle.

Meaningful no-change decisions: PROJECT, WORKFLOW, AGENTS, doctrine and ADRs retain
their commitments. Persistence and Player Presentation have no new production
route/storage behavior. Actors/Social retains intentional agency: the already
accepted agreement and authority are stipulated rather than newly simulated.
Existing F01/F05 canonical requirements and modules need no revision. No new
deferred finding is needed; remaining gaps are documented accepted risks and
explicit exclusions. Historical handoffs and unrelated original files are intact.

Exact changed-file inventory (17 paths, all relative to this worktree):

1. `engine/information_adjudication.py` — new bounded integration.
2. `test_information_adjudication.py` — new offline suppliers and tests.
3. `tools/play_information_adjudication_smoke.py` — new disposable smoke.
4. `docs/information_grounded_adjudication_v1_handoff.md` — this report.
5. `docs/architecture.md`.
6. `docs/design/information-grounded-adjudication-v1.md`.
7. `docs/design/information-foundation-functional-design-v1.md`.
8. `docs/design/systems/README.md`.
9. `docs/design/systems/system-map.md`.
10. `docs/design/systems/action-resolution.md`.
11. `docs/design/systems/world-simulation.md`.
12. `docs/design/systems/character-system.md`.
13. `docs/design/systems/narrative-experience.md`.
14. `docs/design/systems/scenario-authored-content.md`.
15. `docs/current_capability_package.md`.
16. `docs/current_sprint.md`.
17. `docs/current_sprint.json`.

## Owner gameplay smoke and repository disposition

From the worktree root run:

```powershell
.\.venv\Scripts\python.exe tools/play_information_adjudication_smoke.py
```

Choose `ward`: try `float`, `status`, `inquire` (or `look`), `status`, `invalid`,
`remove`, `float`. Inquiry recalls the observed effect without identifying its
hidden cause; the two status readings have identical costs/time/history counts.
Run again with `--informed`, choose `ward`, and try `float`, `inquire`: the response
also includes a legitimately supplied qualified inference and attributed guide
report. These are supplied character knowledge, not newly discovered secrets.
The chosen
methods differ; rejection changes nothing; accepted removal changes later
applicability without disclosing the hidden cause. Choose `agreement`: `hook`,
`revoke`, `leave`; revocation prevents new agreement effects but retains the
existing departure obligation. Choose `mundane`: `lift`; the controlled d6 gives
partial progress with no magical explanation. Use `status` for costs/history count,
`quit` to discard the session. `--scripted` runs the three demonstrations offline;
`--scripted --informed` also exercises the supplied-knowledge inquiry variant.

## Targeted code-review correction

The previous inquiry path returned F05 control without an informational response;
accounting-only `look` did not satisfy inquiry coverage. The minimum correction
adds the read-only accepted-observation response described above. It shares the
existing character-safe fact projection with accepted-result presentation and
reuses unchanged F01/F05 contracts. Seven focused tests cover inquiry without
knowledge, granted knowledge/inference/report, expired/other-character grants,
own-observation restrictions, safe failure, historical inquiry after ward removal,
and provisional draw rejection/retry/accepted reuse.

Fresh correction verification: syntax for all three Python files; 48 focused tests;
61 information/F05/independent-activity/gate regressions; F01 script assertion
groups under network denial; uninformed and informed scripted gameplay smokes;
maintained Git/lifecycle/preflight and whitespace checks. Prior contextual-action,
competence and save/load results remain recorded above; those unchanged production
subsystems were not rerun for this read-only correction.

Correction touched 10 existing candidate paths: `engine/information_adjudication.py`,
`test_information_adjudication.py`, `tools/play_information_adjudication_smoke.py`,
this handoff, `docs/architecture.md`, `docs/current_capability_package.md`,
`docs/current_sprint.md`, and the Action/Resolution, Character and Narrative
manifests. Overall candidate inventory remains the same 17 files. No new lifecycle
package or JSON transition was needed. Design contracts, ownership, persistence,
World/Actors/Player Presentation boundaries and other documentation remain valid;
no ADR/doctrine or new deferred-finding record is warranted.

Remaining inquiry limits: explicit accepted-attempt references, own observed
effects, supplied relevance scope and legitimately granted fact records. This is
not general natural-language questioning, investigation, new inference derivation
or automatic explanation from internal binding terms. No provider or new
consequential authority was introduced. No unresolved correction blocker remains.

## Owner acceptance and authorized publication

The owner accepted this bounded implementation and its targeted inquiry correction,
including experiential smoke, on October 22, 2026. The subsequent publication
instruction explicitly authorizes staging only the 17 listed paths, one publication
commit, strict fast-forward merge to main and push through the official workflow.
No runtime/test/smoke source changed during publication; reconciliation is limited
to acceptance, lifecycle and publication records within the authorized inventory.

Fresh publication verification passed all 133 unittest cases (48 focused, 61
information/F05/gate and 24 contextual-action regressions), F01 assertions, seven
competence groups, save/load compatibility, syntax and both ordinary/informed
inquiry smoke variants. Automated behavioral verification denied socket network
access; no live provider calls occurred. This re-exercises hidden-condition
application, read-only inquiry, rejection atomicity, provisional draw disposal,
accepted-result reuse, resource integrity, F01/F05 and compatibility boundaries.

The maintained GitWorkflowTools candidate tool runs standardized interpreter,
preflight, lifecycle/JSON and whitespace validation with repository-mutation
detection. Exact staged inventory/diff and parent/tree identity are checked before
commit. The official merge tool permits only strict fast-forward from the expected
baseline. Publication completion verifies local main, origin/main and actual
remote main agree, with clean publication worktrees/indexes; exact SHA and parent
are reported by the publication operation rather than self-referencing this file.

Lifecycle is complete and idle at Elevated risk: active_sprint,
active_capability_package and next_sprint are null; latest completed activity is
Information-Grounded Adjudication V1. No separate lifecycle-only commit or next
package is needed. Original dirty checkout, owner save and unrelated worktrees
remain preserved. The unused clean managed checkout created during implementation
preflight was archived; the accepted source worktree remains the `.artifacts`
path above. No extra artifacts, provider configuration, owner save or unrelated
file belongs to the publication commit.

Stop after publication. No next capability package is selected or begun.
