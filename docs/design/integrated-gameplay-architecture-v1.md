# Integrated Gameplay Architecture V1

**Phase: Design. Status: owner-accepted decisions; documentation candidate for
owner review.** Consolidated October 23, 2026 from the owner's reconstructed
Accepted Decision Source for Documentation Consolidation. This is the canonical
Design consolidation of IG-01–IG-18 and IG-20–IG-23. The decision headings and
descriptions below preserve that accepted source with line wrapping only.

**IG-19 is not accepted and is excluded.** No contents or substitute decision
are inferred for it. Acceptance of the 22 decisions is distinct from review and
publication of this documentation candidate and from acceptance of implementation.

Verified preparation baseline: local and remote `main`
`ed3bdbe782a6e4f0e0f636207724795ffe8f33e7`. Research, Design and Implementation
remain distinct. Existing implementation is evidence and a possible resource,
not authority over accepted design. This record selects no package, changes no
lifecycle state and authorizes no implementation, Git publication, save-version
change, migration or live-provider execution. [WORKFLOW.md](../../WORKFLOW.md)
retains those authorization boundaries.

## Governing contracts and purpose

Integrated Gameplay Architecture coordinates coherent player undertakings
across the existing gameplay responsibilities. It connects interpretation,
domain participation, information sufficiency, authoritative acceptance and
continuing play without introducing competing authority over outcomes.

Read with [F05 — Authorized Activities and Player Control](f05-authorized-activities-and-player-control.md),
[F01 — Truthful Presentation and Epistemic Fidelity](f01-truthful-presentation-and-epistemic-fidelity.md),
[Information Foundation Functional Design V1](information-foundation-functional-design-v1.md),
[Information-Grounded Adjudication V1](information-grounded-adjudication-v1.md),
the [system responsibility map](systems/system-map.md) and
[shared doctrines](systems/README.md#shared-doctrines).
These records retain their authoritative contracts and implementation statuses.
The [implementation plan](integrated-gameplay-architecture-v1-implementation-plan.md)
describes three bounded milestones over a common reusable runtime; it starts none
of them.

## Accepted decisions

### IG-01 — Coherent Coordinated Gameplay Undertaking

A player instruction may authorize one coherent gameplay undertaking containing
multiple ordinary constituent actions.

The coordinator distinguishes an overarching objective, immediate objective,
method and constituent steps. Multiple intentions may be recognized without
automatically executing all of them.

Independent materially distinct undertakings do not become one authorized
undertaking merely because the player combines them in one message or gives
them a common strategic objective.

### IG-02 — Contextual Intent Interpretation

Interpret natural-language instructions in their complete gameplay context.

Identify the activity, objective, target, specified method, constraints,
inquiry versus preparation versus commitment, continuation and relevant
ambiguity.

Interpretation does not independently authorize or resolve an activity.

Clarification is appropriate when material meaning remains unresolved. The DM
may explain obstacles, offer plausible possibilities or ask an open-ended
question without choosing the player's method.

### IG-03 — Capability-Based Responsibility Selection

Select gameplay responsibilities according to the activity's meaning and
circumstances, not simple verb matching.

The coordinator identifies applicable gameplay domains and arranges their
participation. It does not acquire their authority.

Conceptual responsibilities need not correspond to separate modules, services
or AI calls.

### IG-04 — Responsibility-Driven Information Discovery

Owning gameplay domains determine what authoritative information is necessary
for their decisions.

The coordinator facilitates requests and information flow. The Information
Foundation retrieves information but does not decide outcomes.

Information requirements derive from applicable gameplay semantics and
circumstances.

### IG-05 — Iterative Context Sufficiency

Retrieve sufficient relevant information for the current consequential
decision, including material relationships and dependencies.

Additional information may be requested when earlier retrieval establishes a
relevant dependency.

Avoid exhaustive world retrieval.

Material established-but-unavailable information must be retrieved or leave the
affected outcome unresolved. Missing information cannot be replaced through
invention.

### IG-06 — Controlled Information Disclosure

Distinguish authoritative internal adjudication information, legitimately
character-accessible information and presentation information.

Hidden conditions may govern outcomes without becoming player knowledge.

Narration and player-facing clarification must not disclose information solely
because it was available internally.

These distinctions do not require separate physical information stores.

### IG-07 — Coherent Consequence Acceptance

Mutually dependent consequential changes must be validated and accepted
coherently.

An unsuccessful or rejected proposal must not accidentally publish part of its
intended changes.

Legitimate partial success or incremental progress is permitted when
independently adjudicated and accepted.

### IG-08 — Domain-Owned Consequence Validation

The responsible gameplay domains validate applicable mechanics, established
conditions, authorization and consequential changes.

The coordinator organizes validation and acceptance but does not replace domain
authority.

AI-generated proposals remain untrusted until accepted through the appropriate
gameplay boundary.

### IG-09 — Durable Progress and Interruption Boundaries

Extended undertakings may progress through multiple meaningful accepted
increments.

Interruptions preserve legitimately accepted progress, costs, outcomes and
resolved mechanics.

Unaccepted proposals must not become durable state.

Interruption must not cause an already resolved action to be rerolled solely
because its presentation or continuation was paused.

### IG-10 — Authoritative Fact Incorporation

Previously unspecified consequential facts may be proposed through legitimate
contextual adjudication.

Before becoming authoritative, they must be validated and incorporated into the
appropriate owning domain, preserving relevant identity, meaning, scope,
temporal applicability and relationships.

Accepted facts must be retrievable for later gameplay.

Incidental descriptive details need not all be persisted.

### IG-11 — Durable Consequential State

Preserve world, character, actor, relationship, activity and historical
information to the extent necessary for meaningful future gameplay.

Retain consequential commitments, unresolved conditions and relevant
developments.

Do not require exhaustive recording of every incidental event or detail.

### IG-12 — Activity Continuity and Resumption

Preserve sufficient undertaking context across interactions, interruptions and
sessions.

This includes applicable authorization, method, constraints, accepted progress,
resolved decisions and requirements for resumption.

Resumption must account for changed circumstances and enforce the same
applicable restrictions as initial execution.

Already accepted costs and results must not be duplicated.

### IG-13 — Temporal and Offscreen Continuity

Distinguish current authoritative circumstances from meaningful historical
truth.

The world may evolve outside the player's observation.

When unattended circumstances become relevant again, establish necessary
developments at natural re-entry, before affected interaction occurs.

Respect established causes, commitments and elapsed fictional time. Do not
retroactively tailor developments to unexpressed player intentions.

Continuous exhaustive simulation is not required.

### IG-14 — Scalable, Storage-Independent Continuity

Support stable consequential identities, selective retrieval, meaningful
relationships, history and durable preservation across potentially large
campaigns.

Logical continuity requirements must remain independent of a particular storage
technology.

The design must permit appropriate future scaling and migration without
changing established gameplay meaning.

Neither a graph database nor an exhaustive event ledger is mandated.

### IG-15 — Gameplay Decision Traceability

Provide sufficient structured diagnostic traceability to understand
consequential gameplay decisions.

Relevant stages include interpretation, responsibility selection, information
retrieval, adjudication, validation, acceptance, persistence and presentation.

Diagnostic records do not independently establish campaign truth.

The scope and availability of additional diagnostic instrumentation may be
configurable.

### IG-16 — Failure Attribution and Containment

Identify the earliest relevant failure and any subsequent failure to contain
it.

Distinguish interpretation, routing, retrieval, authorization, adjudication,
validation, persistence, presentation and technical failures.

Rejected proposals and technical errors must not be converted into fictional
outcomes.

Failure handling must preserve authoritative state and prevent
hidden-information disclosure.

### IG-17 — Integrated Contract Validation

Validate individual responsibilities, cross-system boundaries and their
operation in continuing gameplay.

Testing must cover consequential interactions, activity continuation,
persistence and restoration, information access and coherent acceptance.

Prefer a common reusable runtime over isolated disposable demonstrations when
validating already accepted architecture.

Automated structural verification and owner experiential assessment serve
complementary purposes.

Runtime validation remains part of the actual game and cannot be disabled
merely to simplify testing.

### IG-18 — Proportionate Development, Testing and Model Use

Use deterministic fixtures, structural checks and offline testing where they
provide sufficient evidence.

Use live models when model behavior is the subject of investigation, selecting
the lowest-cost model adequate for the required capability.

Conceptual gameplay stages do not mandate individual provider calls.

Avoid unnecessary standalone playable slices when accepted contracts can be
validated through a continuing integrated framework.

This decision concerns development and evaluation discipline, not permission to
bypass gameplay validation.

### IG-20 — Domain-Owned Dependency Discovery

Applicable gameplay domains own the requirements for identifying and obtaining
the information needed to perform their responsibilities.

For example, combat requirements may include attacker and defender statistics,
equipment, armor, applicable rules, conditions and effects.

An innate creature immunity may be directly established in its definition. An
active magical protection may be represented by an effect on the creature
instance referencing an applicable spell definition.

Both are ordinary domain-relevant dependencies, not exceptional AI discoveries.

The Information Foundation supplies direct and relationship-based retrieval.

AI interpretation may identify an unusual activity and its applicable
responsibilities, but a separate general-purpose AI dependency-discovery engine
is not required.

Failure to obtain an applicable established material dependency is a
correctness defect. An unresolved material dependency must not be silently
ignored.

### IG-21 — Authoritative Acceptance Integrity

Distinguish proposed consequential changes from accepted authoritative truth.

Validate mutually dependent changes coherently and ensure that material
assumptions remain valid against current authoritative state.

Support safe retries, idempotent recognition of accepted results and durable
continuity through recovery and save/load.

Technical failures must not cause partial, duplicate or fictionalized
consequences.

Owning domains retain authority. The design specifies logical guarantees
without mandating a particular transaction engine or database.

### IG-22 — Proportionate, Scene-Grounded Coordination

Coordinate gameplay responsibilities and processing in proportion to the actual
activity, context and potential consequences.

Authoritative scene circumstances—including relevant location, geography,
actors, environment, time and ongoing conditions—inform activity
interpretation, responsibility selection and adjudication.

An apparently routine action may become consequential because of its scene
context.

For example, opening a door in an empty hallway differs from opening it while
evading nearby guards.

Avoid rigid universal complexity categories and unnecessary mandatory
processing stages.

Direct or combined execution paths are permissible when they preserve
applicable authorization, domain authority, information requirements,
mechanics, acceptance and persistence.

No conceptual stage requires its own model call.

### IG-23 — Situated Progression and Progressive Specificity

A broad player undertaking may authorize ordinary situated progression without
requiring the player to specify every constituent action or a complete plan.

The coordinator determines what is currently actionable using the established
objective, method, constraints, authorization and authoritative scene
circumstances.

A castle search can begin in the character's current hall without choosing an
entire exploration route.

Where relevant world details are genuinely unspecified, responsible gameplay
domains may establish sufficient additional specificity for the next meaningful
decision, subject to established facts and applicable mechanics.

Consequential new facts become authoritative through the accepted incorporation
contract.

Extended undertakings progress through situated activities and developments
rather than being automatically collapsed into one resolution.

Coordination may advance ordinary authorized steps where continuation is
determined or unambiguous. It returns control when a meaningful direction,
method, risk commitment or independent undertaking requires the player's
choice.

Established geography, spatial relationships, discoveries and temporal
developments must remain causally consistent.

Additional constraints such as carefulness, quiet movement or avoiding
detection modify the undertaking without necessarily creating a different
activity category.

World Simulation and relevant domains establish circumstances and outcomes.
Coordination manages the undertaking and its boundaries without independently
becoming a world simulator.

## Contract reconciliation and responsibility relationships

These cross-references explain how the accepted decisions compose with existing
contracts; they do not restate or replace those contracts.

| Accepted IG decisions | Canonical contract and retained boundary |
|---|---|
| IG-01–IG-03, IG-09, IG-12, IG-22–IG-23 | [F05 D1–D6](f05-authorized-activities-and-player-control.md#accepted-decisions) governs coherent authorization, preparation versus commitment, available means, meaningful return of control and resumption. Coordination interprets and manages executable undertaking scope; ordinary steps need no unnecessary clarification, while materially independent undertakings remain player choices. |
| IG-04–IG-06, IG-20 | [Information Foundation D13–D16](information-foundation-functional-design-v1.md#d13--direct-and-relationship-based-information-access) governs selective access, hidden constraints, sufficiency and unavailable established information. Domains own dependency requirements, including ordinary direct and relationship-based dependencies; retrieval and coordination confer no outcome authority. |
| IG-07–IG-08, IG-21 | [Information-Grounded Adjudication D-A2–D-A5](information-grounded-adjudication-v1.md#d-a2--adjudication-responsibility) retains owning-domain adjudication and acceptance. IG specifies coherent dependent acceptance, current-state validity, retry safety and durable recognition without selecting a transaction engine. Rejected proposals differ from accepted fictional failure or independently accepted partial progress. |
| IG-10, IG-22–IG-23 | [Information Foundation D3–D7](information-foundation-functional-design-v1.md#d3--stable-consequential-identity) and the [Specificity Doctrine](systems/README.md#specificity-doctrine) govern stable identity, authoritative circumstances and progressive specification. Scene state is authoritative contextual information from its appropriate owners. Established geography constrains situated progression; genuinely unspecified detail may gain sufficient specificity through those domains and the accepted incorporation contract. |
| IG-06, IG-10–IG-13 | [F01 D1–D10](f01-truthful-presentation-and-epistemic-fidelity.md#accepted-decisions) governs faithful expression of accepted accessible meaning, attribution and temporal distinctions. Internal context, diagnostics and incidental expression do not independently establish consequential truth, character knowledge or accepted progress. |
| IG-11–IG-14, IG-21 | [Information Foundation D6–D12](information-foundation-functional-design-v1.md#d6--meaningful-historical-continuity), [F05 D6](f05-authorized-activities-and-player-control.md#d6--preserve-established-results-and-consequences) and [Persistence responsibilities](systems/persistence.md) preserve relevant history, commitments, restrictions, accepted results and restoration meaning. IG extends the target for continuing gameplay; it does not claim that existing bounded implementations already provide full durable integration. |
| IG-15–IG-18 | [F01 validation and proportional safeguards](f01-truthful-presentation-and-epistemic-fidelity.md#development-and-validation-posture) and the [engineering posture](../engineering_posture.md) retain proportionate development testing and experiential assessment. Mandatory core runtime validation remains enabled; additional diagnostic instrumentation may be configurable and establishes no campaign truth. |

Under [Authority Composition](systems/README.md#authority-composition),
World Simulation retains external reality and legitimate causal progression;
Character System retains capability and legitimate informational access;
Action & Resolution retains adjudication of attempts; Actors & Social Dynamics
retains meaningful intentional NPC decisions. Scenario & Authored Content supplies
foundations and supported declarations; Narrative Experience and Player
Presentation express and display legitimate accessible results; Persistence
preserves accepted meaning. Coordination arranges their participation and manages
undertaking boundaries without acquiring those authorities.

IG-20 makes domain-owned dependency discovery the normal mechanism. An innate
capability supplied directly and an active effect linked to its definition are
ordinary inputs under that domain's requirements. Iterative retrieval supports
these requirements without a separate general-purpose AI dependency engine.
Information Foundation's accepted retrieval and adjudication risks remain
gameplay-evaluated risks; they do not make omission of an applicable established
material dependency correct.

IG-22–IG-23 preserve situated exploration and player control together. Starting
a castle search in the current hall does not authorize a whole itinerary or
collapse the undertaking into a single result. The responsible domains supply
circumstances and any legitimate new specificity; coordination advances ordinary
authorized steps and returns meaningful unresolved direction, method and risk
choices. Quietness or carefulness can modify the same undertaking. No new search,
stealth, combat or other mechanic is established by these examples.

## Implementation and validation boundary

The [three-milestone plan](integrated-gameplay-architecture-v1-implementation-plan.md)
covers I1 coordination, I2 consequential integration and I3 continuing gameplay
integrity. All extend the same reusable runtime. Contract-conforming fixtures may
supply unavailable upstream capabilities without claiming their implementation
or replacing adjudication with scenario answers.

Conceptual boundaries do not mandate separate modules, processing stages or AI
calls. Preserve scalability, stable consequential identity and storage-independent
meaning without prescribing a graph database, universal entity framework,
exhaustive event ledger or fixed model architecture. A future scaling or migration
capability does not authorize a migration in this task.

The existing bounded implementations retain their stated limits. Full production
coordination, general actor agency, domain rules coverage and campaign persistence
are not claimed by documentation consolidation. Any later implementation must be
separately authorized and staged under the existing workflow, with supported
mechanics, suppliers, integration boundaries and proportionate validation explicit.

## Revision history

- October 23, 2026: consolidate the owner's reconstructed accepted source for
  IG-01–IG-18 and IG-20–IG-23 with wording preserved and IG-19 explicitly excluded;
  cross-reference existing contracts and the bounded implementation plan.
  Documentation candidate only; no implementation or publication authorized.
