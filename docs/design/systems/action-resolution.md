# Action & Resolution — Design Manifest

## Status

- Overall: **Partial** — bounded deterministic operations and persistent
  competence attempts, contextual investigation and declared material handling exist;
  general player-action adjudication does not.
- Last materially reviewed: October 6, 2026, repository baseline
  `d0dba1f5f1da391216cdb8fb8e4dabf8485705c8` (`docs: refine character system authority`).
- Relevant milestones: [10.77 reference predicament](../../sprint_10_77_handoff.md),
  [10.78 Character Competence V1](../../sprint_10_78_handoff.md),
  [10.79 causal follow-through](../../sprint_10_79_handoff.md), and
  [10.80 Scene Context](../../sprint_10_80_handoff.md).

This living responsibility model uses the [shared structure and vocabulary](README.md).
It is a documentation review candidate, not implementation authorization or a
new action framework. Conceptual ownership does not require separate modules.

Implementation reconciliation: October 12, 2026 at published baseline
`a6ff316473ce2bafc58be4718479261602f5e3ac`, through October 11 accepted work.
Later evidence: [Contextual Investigation V1](../../contextual_investigation_v1_handoff.md),
[Contextual Action & Consequence V1](../../contextual_action_consequence_v1_handoff.md)
and its [structural correction](../../contextual_action_structural_correction.md).
The October 6 review identity above remains historical.

## Physical Traversal M1 — owner accepted October 26, 2026

`engine/traversal_resolution.py` implements bounded 2024 climb movement and
circumstance-justified Athletics checks, with proficiency/condition/trait effects,
and a distinct dry-ground fall-damage contribution. Failed objectives do not
manufacture falling, injury, a safe final position or a movement charge.
Assessments/results are unaccepted; stale and unavailable premises reject.
`traversal_coordination.py` reuses common I1/F05 assessment and refuses execution
until M2 coherent acceptance is integrated. This neither replaces existing
accepted gameplay nor routes climbing through the finite d6 policy.
The owner's October 26 clarification makes coordination a prerequisite of climbing,
independently of whether a check is needed; Resolution consumes Character's general
capability instead of imposing a Stunned Speed restriction. Fall sampling validates
against a captured immutable frame. Grounded exposed/protected/near-ground failure
consequences remain required M2 validation. See [M1 handoff](../../physical_traversal_m1_handoff.md).

## Physical Traversal M2-2a — owner accepted October 26, 2026

A supported uncertain climb requires fixed World circumstances and an explicit
contextual ruling for failed progress versus failure to maintain grip, plus the
failed-attempt movement commitment. Resolution records controlled check and fall
rolls; World and Character validate their consequences in the existing acceptance
unit. World validates generated identities and the supported protection branches
before sampling, so a known invalid failure cannot selectively discard an unfavorable
roll. Read-only assessment never draws. Pure recorded-result evaluation validates
history without invoking resolution, drawing or publishing again. There is no
universal fall-chance rule, automatic safe failure or natural-1/20 check override.
See [model](../../physical_traversal_m2_2a_design.md) and
[handoff](../../physical_traversal_m2_2a_handoff.md). Owner accepted the bounded milestone October 26, 2026;
Git publication remains separate and overall system status remains Partial.

## Physical Traversal M2-2b — owner accepted October 27, 2026

One retained undertaking can advance over multiple meaningful established links.
Each increment applies current domain premises and the scoped contextual ruling;
previously accepted mechanics/receipts are reused without new dice or costs.
A failed attempt may permit a distinct legitimate new attempt, but a new identity
does not waive eligibility or F05. Internal choice contexts retain the establishing
owner occurrence, declared meaningful stages and reconstructed climbing risk/rule
stakes. Changed contextual stakes can be supplied before the next resolution; a
materially changed scoped decision needs a fresh identity and appropriate answer.
Unchanged choices survive unrelated World revisions. Checkpoint result references remain unsupported; accepted
increment identity is validated during execution and historical reconstruction.
See [model](../../physical_traversal_m2_2b_design.md) and
[handoff](../../physical_traversal_m2_2b_handoff.md). This uncommitted bounded
implementation was owner accepted October 27, 2026. Git publication remains separately unauthorized; overall classification stays Partial.

## Purpose

Published M2-1 foundation (historical milestone coverage): the common Runtime's opt-in
domain aggregate accepts deterministic M1 climbing increments through the existing
Coordinator/F05 interface. Named premises, dependent effects and independently
validated safe receipts precede publication. Exact accepted retry recognition
follows strict request-type validation and precedes current-position reads.
Non-null checkpoint resolution references reject: separate checkpoint reuse is
unsupported in M2-1; accepted-command retries use the accepted-unit history.
A distinct attempt needs current eligibility and
authorization. Check-bearing/partial-link execution stops before sampling;
objective failure never implies a safe accepted disposition. Existing M1 uncertain
checks/falls remain provisional. [Model](../../physical_traversal_m2_1_design.md).

Owner-accepted implementation, October 22, 2026: [Information-Grounded Adjudication V1](../../information_grounded_adjudication_v1_handoff.md)
combines supplied authorization, actual means/capability and V1a-retrieved hidden
bindings through one finite evaluator and existing d6 policy. Offline proposals
must agree with supported authoritative conditions/mechanics before acceptance;
unsupported terms remain unresolved. Rejection is technical, with no fictional
failure or mutation. F05 controls resumption without reroll/recharge. This bounded
disposable integration and inquiry correction are accepted; general adjudication remains deferred.

Targeted correction: an inquiry intent can return read-only information about the
character's accepted observable effect, without a new assessment, proposal, roll,
cost or result. Mechanical samples remain provisional until candidate acceptance;
technical rejection stores no roll/result. Explicit retry may sample again, while
accepted-attempt resumption reuses the recorded result. No pending-roll model.

Adjudicate executable attempts from declared intent, authoritative world and
character circumstances, and applicable policy. Establish whether an attempt
can proceed, what resolution it needs, and its accepted immediate result and
cost, with consequences committed through the systems that own the affected truth.

## Player-facing goal

Make attempts intelligible, fair to established circumstances, and consequential.
Ordinary actions need not become checks. Capability can improve understanding,
efficiency, probability, or available approaches without normally gating campaign
continuation. Rejection, failure, limited findings, and success should communicate
different things; none permits narration to repair an unfavorable outcome.

## Authority

Action & Resolution owns adjudication: combining relevant premises to accept or
reject a supported attempt, applying the appropriate deterministic or uncertain
policy, and establishing the accepted outcome and applicable cost. It determines
which evidence-grounded information or result that outcome legitimately yields;
it does not establish external facts or invent informational content. World
Simulation owns external reality and evidence, Character System owns retained
character information and access basis, and Scenario & Authored Content may
provide supported evidence, declarations, and bounded result material. Resolution
determines whether and how that material is yielded. Narrative Experience and
Player Presentation express the accepted result. Eligibility consumes facts owned
elsewhere; adjudication cannot manufacture a target, evidence, capability,
permission, or resource to make an attempt possible. Character recognition may
expose an approach without deciding its outcome.

Acceptance includes a valid commitment of the required immediate effects, not
merely a parsed command or a proposed die result. Outcomes that alter external
truth pass through World Simulation; acquired information passes into established
character-information records. Current GameEngine candidate preparation composes
these responsibilities without a separate outcome/commit API.

The contractual boundary remains engine-owned simulation authority: provider
output cannot choose a draw/result, waive a cost, mutate state, or establish
success. The narrower responsibility map explains who decides what within that
boundary; it does not weaken validation or atomic publication safeguards.

## M2-M1 inspection connection — owner-accepted bounded implementation

Owner accepted October 24, 2026 after successful interactive smoke and handoff
review, including documented limitations. Git publication remains separate.

The [M2-M1 handoff](../../m2_m1_handoff.md) connects bounded ordinary input to the
existing I1 coordinator and domain-owned I2/I3 acceptance. Situated suppliers
declare visible targets, method availability and means; finite method declarations
still own capability, requirements, existing routine/d6 mechanics, cost, duration
and result observations. Interpretation never resolves an outcome. Material
unavailable information stays unresolved; a known failed prerequisite can produce
an accepted blocked attempt with its declared cost, preserving existing semantics.
F05 checks durable continuation and current restrictions. Final acceptance also
checks current supplied context; retry reuses accepted mechanics and costs.
No new inspection/search rules, universal durations or production content are added.

## Bounded I1-M1 implementation — owner accepted

October 23, 2026: [I1-M1](../../i1_m1_handoff.md) adds a common GameEngine
coordination runtime with untrusted interpretation, undertaking/context contracts
and existing F05 control. Owning domain suppliers establish applicable
responsibilities, prerequisites and accepted results. Coordination authorizes
only the next situated step and rechecks current context before execution;
it neither resolves mechanics nor replaces domain acceptance. Search/door/guard
responsibilities are explicitly supplied offline fixtures; production observation
is read-only. General adjudication, I2 integration and I3 durability remain deferred.
The overall Partial classification and Action & Resolution authority are unchanged.
Owner-authorized I1-M1 correction, October 23: accepted receipts now carry explicit
domain result meaning and a Character-safe result projection. The common runtime
immediately assesses the next current boundary and continues ordinary supported
steps only under fresh F05 permission and domain acceptance. A natural decision
point describes established accessible circumstances without leading questions or
automatic menus. Explicit ambiguity can still require clarification. Exact
supplier-supported direction phrases provide bounded free-form choice; they are
not general navigation or language interpretation. Refinements preserve accepted
work and apply constraints prospectively. A later failure retains earlier accepted
results/costs. See the [correction handoff](../../current_sprint.md) for the finite per-call
bound and trusted supplier limits; no I2/I3 or new gameplay mechanics are claimed.
## Explicit non-authority

- **World Simulation:** external facts, physical evidence, positions, actual time
  advancement, resulting external truth, and later causal progression.
- **Character System:** authoritative capability, character-specific access basis,
  recognition and retained information. Current access can be jointly derived
  from character constraints and external conditions.
- **Actors & Social Dynamics:** meaningful intentional NPC/faction decisions.
  Adjudicating a contested interaction does not decide what an actor wants or
  independently chooses; a general contest mechanism is not implemented.
- **Scenario & Authored Content:** bounded circumstances, evidence, constraints,
  costs/effects and resolution material. Its declarations need supported engine
  interpretation; they are not permission to predetermine arbitrary player outcomes.
- **Narrative Experience / Player Presentation:** expression, input/display,
  attention and communication of safe choices/results. Descriptive intention is
  not an accepted consequential action.
- **Persistence:** storage, restoration and compatibility. Action & Resolution
  identifies the accepted meaning that must survive, not the disk-storage design.

## Governing principles

Apply the [shared doctrines](README.md#shared-doctrines),
[Simulation Principles](../../simulation_principles.md), and
[Story-First Part I](../../story_first_design_doctrine.md#part-i--established-design-doctrine).

- Resolve meaningful uncertainty and consequence, not every verb. Missing
  prerequisites can make an attempt unavailable without a roll or a failure band.
- Capability diversifies play. A specialist advantage is not automatically a
  prerequisite, and ordinary continuation need not reproduce specialist mechanics.
- Findings must have legitimate evidence and access. Success cannot conjure absent
  evidence or prove identity, affiliation or a preferred hypothesis without support.
- Failure may cost time, preserve uncertainty or change circumstances. Do not
  fabricate false factual information, guarantee eventual victory, or create a
  compensatory adventure merely because a check failed.
- Commit consequential results coherently and preserve accepted meaning across
  technical boundaries. Repeated presentation is not another fictional attempt.
- Attribute later consequences to established causes. An action initiating a
  causal chain does not transfer all subsequent world evolution to this system.

The exact d6 bands, one-attempt restriction and survey costs below are accepted
slice rules, not universal versions of these principles.

### F05 authorization and continuity

**Accepted design; not a claim of implemented support:** canonical
[F05 D1–D6](../f05-authorized-activities-and-player-control.md#accepted-decisions)
bounds coherent activity, inquiry/preparation/commitment, resolution and return
of control. Advance only as authorization, rules and circumstances permit;
routine events alone need not interrupt. Competence cannot create prerequisites,
guarantee success or select a materially different or costly method. Mechanical
resolution, fictional execution and durable progress differ: resumption depends
on the activity and current circumstances, and presentation interruption alone
does not justify rerolling an already resolved attempt. Established costs,
elapsed time, findings and consequences remain. This selects no general activity
framework or progress representation; existing bounded replay rules remain scoped.

**Owner-accepted bounded implementation (October 16, 2026):**
`engine/activity_control.py` implements a pure continuation/control policy over
authority-supplied purpose, method, intent, prerequisites, restrictions and
developments. The material-handling post-preparation assessment uses its blocked/
continue decision. Accepted result references remain owned by existing
resolution/history; the policy neither draws, executes, authenticates references
nor persists progress. Discovery, social-choice and restart cases currently use
stipulated offline inputs; this is not general F05 gameplay support. Existing
natural input, candidate publication, costs, replay and save semantics remain
unchanged. See [acceptance and closeout](../../f05_authorized_activities_v1_acceptance.md)
and the [implementation coverage](../../f05_implementation_preflight.md).

## Current model

The structurally owner-accepted [damaged-gate integration](../../f01_f05_gate_integration_v1.md)
adds a disposable session with bounded intent distinctions, controlled attempts,
costs and accepted-result reuse. It invokes the accepted F05 policy at gate
continuation/conclusion points and returns control before committing newly needed
support. It changes no campaign resolution, save semantics or accepted F05 code;
see [acceptance and bounded scope](../../f01_f05_integration_v1_acceptance.md).
Its [bounded interaction correction](../../f01_f05_interrupted_repair_correction.md)
recognizes explicit timber-bracing instructions against an already started repair,
then reuses the existing continuation checks and accepted result. Ambiguous input
retains the pause, progress and costs; this adds no general intent parser.
The [final review](../../f01_f05_final_structural_reconciliation.md) found SR-01:
the gate resumption checkpoint omitted the existing restriction conflict supplied
on initial execution. The [bounded correction](../../f01_f05_sr01_restriction_correction.md)
now supplies the same conflict on both paths. This changes no restriction semantics,
accepted control policy or general constraint-adjudication capability; this
correction is included in the owner's structural acceptance.

The [independent supplier validation](../../f05_independent_activity_validation.md)
adds one test-local archive-lock sequence using the existing footsteps fixture.
It derives checkpoints from retained activity state and current authorization;
this extends integration evidence without adding a production lockpicking route,
general supplier framework or F05 policy change.

Three working responsibilities suffice. This decomposition is **Provisional**;
it describes existing seams and open design work, not new runtime components.

| Responsibility | Current grounding and limit |
|---|---|
| Frame an executable attempt | Interpret input and combine world facts, character access/capability, authored prerequisites and supported operation policy. Fixed parsing, local targets, bounded contextual frames and shared assessment predicates exist; open-ended framing and general possibility judgments do not. |
| Determine outcome and cost | Decide the needed resolution depth and apply bounded rules. Deterministic discovery/decisions, two uncertain competence investigations, a deterministic competence survey and declared material handling exist; there is no general policy selector or stakes/difficulty derivation. |
| Commit and preserve the accepted result | Compose immediate effects with owning systems, validate and publish the candidate, retaining enough result/basis/provenance for continuity. Explicit attempt replay exists for three West-Road operations, not all commands. |

World facts answer whether a trace or actor is present; character state supplies
competence and encountered information; content supplies supported declarations;
resolution combines these premises to decide whether and how the operation runs.
An advisory opportunity list consumes the same eligibility where implemented;
the displayed suggestion itself grants neither availability nor success.

## Resolution depth

**Accepted design:** use the lowest sufficient specificity. Ordinary uncontested
action can succeed without a check; a known operation can have deterministic cost
and result. Consequential uncertainty may justify explicit adjudication, which
need not be random. An impossible or unsupported request is not rescued by a roll.
Longer uncertainty may require further decisions rather than a single check.

Current evidence already spans read-only recognition, deterministic discovery,
fixed decisions, d6 interpretation and deterministic time reduction. It does not
implement a general inference → lazy resolution → persistent state → active
simulation escalation policy. Ordinary actions need no universal attempt ledger;
explicit retention is justified where cost, uncertainty, consequence or replay
integrity requires it. Extended actions and active contests remain deferred.

## State and lifecycle

**Implemented, bounded:** a competence operation first returns an existing
accepted record if present. Otherwise it assesses eligibility, draws only for an
eligible uncertain operation, determines the result, and prepares a copied
candidate with source event, elapsed time/consequences, findings/continuation and
result history. Validation and scene construction precede publication. Invalid
preparation, validation or scene construction leaves live world and scene intact.

`competence_attempts` stores at most one record per supported operation: draw
(null for survey), result, specialist basis, cost, findings, and backward
source/time/outcome references. History mirrors the accepted record. Findings
also enter discoveries and supported physical-trace records; full results reuse
the pursuit continuation. Shared `world_state` storage does not transfer the
adjudication responsibility to World Simulation or Character System.

Replay returns that accepted result, including after later continuation or load,
without drawing, charging, rebuilding or publishing. This is distinct from a
newly unavailable action and from other mechanisms' successful no-ops. Ordinary
conversations may record a new conversation on repetition even when a declared
effect is already satisfied; there is no universal command deduplication.

### Later accepted contextual slices

Investigation interprets survey, selected examination, a supported witness question
or selective reporting into an immutable transient `ActionFrame`. Survey reveals
sanctioned leads without acquiring a finding or history entry; targeted acquisition
and reporting reuse existing discovery, Mara-account and recipient transactions.
Target/method/restrictions/access are revalidated, including resumed unsaved focus.
This contextual lead survey differs from the paid West-Road competence survey.

Material handling interprets a `HandlingFrame` with objective, stable target,
authored method and explicit restrictions. Read-only assessment and questions do
not authorize handling. Disclosed risk/method/one-hour effort precede contextual
confirmation; revalidation cannot silently discard restrictions or retarget a
proposal. Routine preparation, time consequences, re-assessment and accepted
full/partial/failure (or interruption) result publish in one candidate. Stabilization
is deterministic; supported adjustment/reposition uses the existing d6 primitive.
This does not grant specialist modifiers to material handling.

Accepted material conditions and causal history survive save/load. An identical
attempt on unchanged material circumstances cannot redraw; changed circumstances
or another supported method can permit a new disclosed attempt. General extended
actions, autonomous intervention, arbitrary repair and conditional plans remain
deferred. Material interpretation runs first, then investigation, then the legacy
kernel if unclaimed. This sequential dispatch is accepted implementation, not the
shared interpretation replacement explored by Option C in the
[research index](../../architecture_comprehension_review.md).

### Randomness and technical continuity

The reviewed runtime draw is `character_competence.draw_d6`, using Python's
`randint(1, 6)`, called by `GameEngine.attempt_competence`. The gameplay entry
point accepts an operation, not a supplied draw or outcome. Recognition, survey,
ordinary discovery and fixed predicament decisions do not draw. Test-injected
draws demonstrate rule coverage, not a player-facing outcome-selection interface.

Accepted draw/result/cost/findings and their causal references survive save/load.
Loading must preserve these results, not reinterpret them as fresh attempts or
reapply their consequences. Version-1 additive normalization permits missing
competence fields to become empty in a copied older payload; malformed present
records reject. Historical ordinary pursuit needs no invented competence attempt.

No PRNG state or unresolved draw is saved. A draw occurs before candidate
publication; if preparation fails, the draw is not durably accepted and the PRNG
is not rolled back. Loading a save from before an attempt allows a fresh draw;
there is no anti-save-scumming guarantee. Continuity protects results present in
the restored state, not events absent from an older save. No new mechanism is
selected to change this limit.

## Inputs

- Declared player intent through the input surface; parsing proposes a supported
  operation, not truth. Future AI-generated action proposals would remain untrusted.
- World facts: current location/scene, physical traces, phase, actor presence,
  elapsed time and relevant circumstances/resources.
- Character facts: applicable competence, recognition/access basis, discoveries
  and other established constraints; biography or equipment prose grants no modifier.
- Validated authored declarations and existing bounded engine policy.
- Prior accepted attempts and causal references for replay and integrity.

## Outputs

- Rejection/unavailability, accepted operation, or supported no-op, distinct from
  the attempt's fictional failure/partial/full result.
- Bounded result quality, legitimate findings and applicable cost; accepted
  immediate external changes are committed with World Simulation, and acquired
  information with character continuity.
- Validated accepted records/provenance where required for Persistence and later
  reasoning; derived player-safe choices, uncertainty, costs and outcome text for
  presentation. Internal identifiers and hidden causes are not automatic knowledge.

## Relationships

See the [relationship map](system-map.md#dependencies-and-information-flow-around-action--resolution).
[World Simulation](world-simulation.md) supplies external premises and owns the
external result and causal follow-through. [Character System](character-system.md)
supplies capability/access and retains acquired information; neither independently
decides the attempted outcome. Content supplies supported material, while the
engine selects and validates its application. Actors & Social Dynamics owns
intentional choices, including future opposing choices; that interface remains
provisional. Narrative Experience and Player Presentation communicate bounded
results. Persistence restores accepted meaning without introducing a fictional
attempt. None of these relationships requires a storage or module split.

### Costs and causal handoff

Separate a cost mentioned in fiction from a supported executable cost. Current
rules include an authored one-hour directed road traversal, fixed one-hour initial
predicament commitments, one-hour uncertain competence operations, and a two-hour
survey reduced to one by tactical competence. Resolution establishes the applicable
cost; World Simulation advances elapsed hours and applies qualifying consequences
inside the guarded transition. Timekeeper does not advance a calendar or weather.

Committed guard assistance is a bounded survey resource, recorded on the attempt
source; it is not a competence tag, a numeric inventory or a general resource debit.
The predicament phase represents guard allocation. There is no general stamina,
money, equipment-consumption or resource-cost mechanism in these paths. Existing
untimed operations must not acquire invented costs from prose.

Sprint 10.79 illustrates the separation: two hours of reduced guard coverage
establish one market theft. An ordinary survey reaches that threshold; a tactical
survey takes one hour, and a subsequent wait can reach the same threshold. Failed
or partial investigations also consume qualifying time. The incident is a World
Simulation consequence of allocation plus time, not a survey failure, roll penalty,
or narrator reward. It can occur away from the player and is revealed locally;
it establishes no thief identity, motive or observer conspiracy.

## Player-facing projection

Communicate available approaches, established costs, uncertainty and the limits
of accepted findings. Current competence packets separate observation/guard
report, automatic limited recognition, limited inference, supported finding and
accepted outcome. Projection is read-only and locally filtered; hidden causes
and internal records are not thereby available to the character.

The current parser's `success` flag is not a universal fictional-success claim.
An accepted failed competence attempt returns `success=True` with
`accepted_outcome.result="failure"`; an exhausted investigation can be accepted
with `changed=False`. Generic `take`/`open`/`use` language can parse as an action
without any implemented object change. Scene Context can express a narrow
within-scene intention without movement, elapsed time or consequential resolution.
These distinctions must survive future presentation work; CLI vocabulary is not
the intended final action abstraction.

## Current implementation

Information Resolution Core V1a implements accepted read-only binding-constraint retrieval by
subject, action and fictional time, including hidden constraints. Conditions,
exclusions and effects are returned intact for an owning adjudicator; no general
condition evaluation or outcome decision is implemented. See the
[V1a handoff](../../information_resolution_core_v1a_handoff.md).

| Capability | Classification and evidenced limit |
|---|---|
| Intent and executable operation | **Partial:** bounded contextual investigation/material framing precedes fixed kernel parsing, current-scene target resolution, graph routes and scenario commands. Unknown input rejects; generic action acceptance is scaffolding without object/inventory mutation. No general free-text adjudication. |
| Preconditions and recognition | **Implemented, bounded:** local discovery needs a matching present trace and an undiscovered declaration. Competence needs withdrawal phase, encountered tracks, exact physical trace, North Gate and Grey/Elin present; no specialist tag is required to try. Recognition is automatic/read-only on applicable evidence. |
| Deterministic discovery and interaction | **Implemented, bounded:** bare investigation acquires the first eligible local discovery; contextual examination selects and revalidates one supported target without roll/time cost. Lead survey grants neither finding nor cost. Clue presentation and conversations validate local targets and supported requirements, then apply declared history/knowledge/pressure/relocation/trace or thread effects where supported. These are not general investigation, persuasion or actor-decision systems. Older prototype effects have test-only legacy-fixture coverage rather than proving current Bryn Shander play. |
| Fixed predicament decisions | **Implemented, scenario-specific:** phase plus evidence/shared reports and guard coordination determine availability; two initial decisions cost an hour, four follow-ups add none. The accepted engine phase graph applies authored outcomes. This bounded scenario policy is not authority for arbitrary authored future outcomes. |
| Uncertain competence | **Implemented, scenario-specific resolution:** follow withdrawal signs uses outdoor tracking; reconstruct local observation circuit uses surveillance analysis. Each costs one hour. Ordinary d6: 1–2 failure, 3–4 partial, 5–6 full. Relevant specialist: 1–2 partial, 3–6 full. No general difficulty/modifier system. |
| Deterministic survey | **Implemented, scenario-specific resolution:** committed guard assistance yields full result; two hours ordinarily, one with tactical assessment, no draw. Presence/coordination requirements apply; assistance is not inferred from biography. |
| Failure/partial/full semantics | **Implemented, bounded:** failure adds no finding; partial gives supported local direction or overlapping watch-position inference; full reuses the withdrawal-route pursuit outcome. All accepted bands pay cost. Other approaches and ordinary continuation remain after failure/partial. No names, affiliations, distant destinations or capture are inferred. |
| Movement/travel | **Implemented, bounded:** graph validation and named routing select executable hops; World Simulation changes position/history. One directed West-Gate road hop costs an hour with supported consequences; others are instantaneous. Multi-hop routes commit sequentially, not as one transaction. No general travel-risk or interruption resolution. |
| Candidate integrity and replay | **Partial system-wide:** competence source/time/findings/outcome validate and publish together; tests inject preparation/validation/scene failures. Accepted competence repeats do not draw/charge/publish. Other candidate transitions exist, but no universal transaction, attempt identity or replay policy is implemented. |
| Contextual material handling | **Implemented, bounded:** assessment is read-only; stabilization/adjustment/reposition require disclosed contextual authorization. Supported preparation, helper cooperation/refusal, one-hour effort, d6 where applicable and finite material consequences publish atomically. Independent archive fixture demonstrates the shared path, not general repair/physics. |
| General `check` command | **Implemented scaffold only:** `perform_skill_check` compares constant result 12 with difficulty 10 for a supplied name. It does not consult character competence, draw, charge time or establish a general skill system. |
| Scene Context intention | **Implemented presentation boundary:** narrow first-person within-scene movement phrases route to descriptive narration; explicit navigation retains its engine route. Providers have no outcome authority. Broader natural-language action resolution is deferred. |

## Accepted decisions

Simulation owns authoritative outcomes; providers fail closed. Story precedes
mechanical activity, capability diversifies paths, evidence constrains findings,
and consequences follow causes. ADR-049/050/053–056 establish specific discovery,
effect and timed-traversal boundaries; ADR-060/061 establish the fixed predicament
and competence semantics. These are accepted bounded mechanisms alongside broader
design direction, not a mandate to make every action use d6, three bands, a fixed
cost, or a persistent attempt record. Technical boundaries do not reset accepted
fictional meaning. See the [decision ledger](../../decisions.md).

## Provisional decisions

The three-part responsibility model and future interfaces for open-ended intent,
stakes, contests and owning-system effect commitment remain working concepts.
The repository supports reusing the principle of coherent consequential commitment,
not selecting a generic transaction abstraction. Neither a general resolution
algorithm nor a universal success taxonomy, permission model or resource owner is
chosen. Story-First's AI-GM reasoning/proposal model remains provisional.

## Deferred capabilities

General free-text attempt framing, novel-action validation, skills/stats/modifiers,
contests/combat, extended actions, broad travel costs/interruptions, resource
economies, repeat-attempt policy for changed circumstances, and any generalized
resolution/transaction framework. No runtime work, save changes, later manifest,
new sprint or package selection follows from this review.

## Known tensions / open questions

- **Intent gap:** how should open-ended intent become a bounded candidate with
  legitimate targets, approaches and prerequisites? Current parsing and generic
  success wording do not establish execution. When is ordinary inference enough?
- **Policy gap:** how are stakes, cost and uncertainty derived from authoritative
  circumstances for novel actions without narrator authority or a roll for every
  action? Deterministic versus random resolution remains a contextual choice.
- **Scenario boundary:** current fixed outcomes and guard responses are accepted
  proving slices. How can richer attempts and contested actor actions preserve
  agency without letting content predetermine outcomes or resolution choose actor
  intentions? The later Actors & Social Dynamics manifest must address its side.
- **Repeat scope:** operation-name identity suffices for this single predicament.
  What materially changed circumstances justify another attempt elsewhere, and
  what historical basis must remain when competence changes? Current validation
  requires the stored specialist basis to agree with current tags; gain/loss is absent.
- **Atomicity scope:** each movement hop can already commit before a later hop
  fails. Future extended actions need an explicit fictional commitment boundary;
  neither whole-command rollback nor partial completion is universal policy.
- **Access gap:** topology/name matching does not yet implement the character
  familiarity/access direction of ADR-059. Eligibility must not mistake engine
  awareness for character knowledge. The Character System manifest records this gap.
- **Evidence representation:** competence helpers materialize supported trace and
  discovery records during accepted findings. That represents bounded discovery
  grounded in applicable authored withdrawal evidence, not a roll creating arbitrary
  physical facts. Richer evidence/outcome representations remain unresolved.
- **Historical terminology:** `character_competence.py` owns several current rules,
  and `world_state` stores accepted attempts. Names and co-location do not move
  conceptual adjudication into Character System or World Simulation. Architecture's
  older preview-only narration wording predates accepted 10.80 CLI presentation.

No contradiction requiring changes to the protected manifests was found. These
implementation gaps and provisional questions remain visible rather than being
silently resolved by documentation.

## Evidence

Source and tests were inspected at the stated baseline. Test assertions below
are evidence of coverage, not gameplay runs performed for this documentation task.
Handoffs report historical verification and owner play acceptance separately.

| Evidence | Supports |
|---|---|
| [Framework](README.md), [template](system-manifest-template.md), [map](system-map.md), [World Simulation](world-simulation.md), [Character System](character-system.md), [architecture](../../architecture.md) | Accepted responsibility boundaries versus current storage/orchestration |
| [Simulation Principles](../../simulation_principles.md), [Simulation Model](../../simulation_model.md), [Story-First](../../story_first_design_doctrine.md), [ADRs](../../decisions.md) | Meaningful uncertainty, truth/access, ordinary abstraction, failure and continuity; provisional AI-GM proposals are not runtime authority |
| [10.77](../../sprint_10_77_handoff.md), [10.78](../../sprint_10_78_handoff.md), [10.79](../../sprint_10_79_handoff.md), [10.80](../../sprint_10_80_handoff.md) | Accepted branches, competence comparison, causal time consequences and presentation-only intent/continuity |
| [Interaction kernel](../../../engine/interaction_kernel.py), [targets](../../../engine/target_resolver.py), [eligibility](../../../engine/action_eligibility.py), [contextual actions](../../../engine/contextual_action_projection.py), [GameEngine](../../../engine/game_engine.py), [world update](../../../engine/world_update.py) | Parsing versus execution, shared premises, effect composition, guarded publication and sequential route hops |
| [Competence authority](../../../engine/character_competence.py), [competence tests](../../../test_character_competence.py), [predicament](../../../engine/west_road_predicament.py), [authored evidence](../../../data/regions/bryn_shander.json) | All draw bands/profiles, deterministic survey, rejected prerequisites, ordinary continuation, causal records, replay and injected rollback coverage |
| [Discovery tests](../../../test_discovery.py), [conversation-effect tests](../../../test_conversation_pressure_effect.py), [timed traversal tests](../../../test_one_hour_west_road_exit_traversal.py) | Deterministic acquisition, no-ops versus repeated conversation, exact timed-hop commitment and legacy-fixture limits |
| [Timekeeper](../../../engine/timekeeper.py), [theft rule](../../../engine/west_road_market_theft.py), [theft tests](../../../test_west_road_market_theft.py) | Cost versus elapsed-time effects; survey headroom, composed activities, threshold occurrence and independent local revelation |
| [Save system](../../../engine/save_system.py), [competence save/replay tests](../../../test_character_competence.py) | Accepted result restoration, copied-load normalization, invalid basis/reference rejection and failed-load preservation; no persisted PRNG state |
| [Skill scaffold](../../../engine/skill_check.py), [CLI](../../../play_game.py), [player route tests](../../../test_player_scene_route.py) | Constant checks are scaffolding; descriptive intentions and provider failure do not mutate authoritative state |

## Revision history

- October 6, 2026: established the Action & Resolution review candidate from
  runtime, tests and accepted design/play evidence; separated framing, bounded
  adjudication and commitment/continuity without generalizing the West-Road slice.
