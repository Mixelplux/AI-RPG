# Information-Grounded Adjudication V1

**Phase: Design. Status: owner-accepted D-A1–D-A6; consolidation for owner review.**
Consolidated October 22, 2026 from the owner's accepted decision handoff.
This is the canonical Design record for those decisions and qualifications.
Reference publication: `68a3ce6a2c712ffddfa6304fb0e35b0b2beca5ff`
(accepted Information Resolution Core V1a). Local and remote `main` matched
that reference at preparation; no subsequent publication was identified.

This record preserves Research → Design → Implementation. Existing code and
research are evidence and possible resources, not design authority. It selects
no package, stages no sprint, and authorizes no implementation or publication.
[WORKFLOW.md](../../WORKFLOW.md) retains lifecycle and authorization authority.

## Governing contracts and purpose

Consequential gameplay must depend on applicable authoritative information,
including hidden binding conditions. Retrieval supplies context; the owning
gameplay authority adjudicates using relevant mechanics and legitimate judgment.
Validation must demonstrate that changing relevant retrieved information changes
its application and, where consequential, the result, rather than replaying a
predetermined scenario answer.

Read with the accepted [Information Foundation Functional Design V1](information-foundation-functional-design-v1.md),
especially D7 and D10–D16, its functional authority contracts and accepted risks;
[F01](f01-truthful-presentation-and-epistemic-fidelity.md) for consequential meaning,
access, attribution and continuity; and
[F05](f05-authorized-activities-and-player-control.md) for authorized methods,
available means, interruption and preserved results. Those contracts are retained
without revision. The [system map](systems/system-map.md) and
[shared doctrines](systems/README.md#shared-doctrines) retain conceptual ownership,
Specificity, Authority Composition and Causal Continuity.

## Functional requirements and owner qualifications

### D-A1 — Information-grounded adjudication

Consequential decisions account for applicable authoritative facts, including
hidden binding conditions. Information retrieval does not independently decide
outcomes. The owning gameplay authority applies relevant mechanics and legitimate
contextual judgment. Demonstrate dependence on retrieved information rather than
hard-coded scenario answers.

### D-A2 — Adjudication responsibility

Action & Resolution determines applicable conditions, mechanics and authorized
resolution. AI proposals remain untrusted until accepted by the appropriate
gameplay authority. World Simulation owns accepted consequential world truth;
Character System governs capability and legitimate informational access; F01
narrates accepted, accessible results. Shared retrieval, orchestration, storage
or presentation does not transfer these responsibilities.

### D-A3 — Context and authorized methods

Relevance depends on the complete gameplay context, not solely the latest player
text: authorized action/method, actor, equipment, location, target, related
subjects and applicable hidden conditions. Retrieve proportionately to that
decision without omitting a material established condition.

Do not silently select materially different methods or consume unspecified
resources. Possession of both a levitation scroll and potion does not authorize
choosing between them when intention is ambiguous. Return a player-owned method
choice when needed, preserving F05. Predetermined fixtures may supply correctly
authorized context while general interpretation remains unimplemented.

### D-A4 — Unavailable established information

Preserve the distinction between unspecified information, established-but-unavailable
information and genuine uncertainty. Material established-but-unavailable
conditions require internal authoritative retrieval or an unresolved outcome;
missing context never permits invented replacement facts. Do not reveal hidden
conditions through player-facing clarification. This is a materiality requirement,
not a demand for exhaustive world information before ordinary gameplay proceeds.

### D-A5 — Acceptance of consequential adjudication

Generation alone confers no authority. Before acceptance, the owning gameplay
boundary proportionately checks relevant established conditions, mechanics,
authorization and state. Accepted consequences govern subsequent gameplay and
meaningful continuity. Rejected proposals must not mutate authoritative state or
be presented as fictional failures. Technical rejection and an accepted fictional
failure remain distinct.

This requirement selects neither a universal acceptance protocol nor an extra
provider call. Use the minimum sufficient checks justified by the supported
consequence and observed need, preserving fail-closed provider behavior,
atomic state publication and save compatibility.

### D-A6 — Bounded integration and validation

Demonstrate reusable information-grounded resolution for a hidden ward and
authorized exceptions, distinct grappling-hook and levitation methods,
observations and later removal; a binding agreement; a mundane obstruction;
and deliberately invalid AI proposals. The criteria below cover consequential
continuity, player-safe access, existing mechanics, state integrity and
cross-domain applicability.

Narrative quality remains deferred provided outputs are meaningful and faithful.
World magic remains causally grounded and meaningful: consider applicable
existing rules before inventing consequential magical abilities. Original world
magic is permissible when warranted; arbitrary magical manifestations must not
be routinely inserted.

## Responsibilities and authority boundaries

| Responsibility | Required contribution and retained boundary |
|---|---|
| [Scenario & Authored Content](systems/scenario-authored-content.md) | Supply coherent foundations, binding terms and supported circumstances. Fixtures may stipulate premises and authorization, but cannot substitute a scenario answer for adjudication. |
| Information retrieval | Supply relevant authoritative current/history information and binding terms, including hidden conditions for internal use; preserve availability, epistemic and source distinctions. Returning terms does not evaluate them. |
| [Action & Resolution](systems/action-resolution.md) | Combine authorized context, capability, conditions and mechanics; evaluate supported attempts and consequential proposals through the owning gameplay boundary. Do not manufacture missing prerequisites or bypass binding terms. |
| [World Simulation](systems/world-simulation.md) | Own accepted external reality, resulting changes and supported subsequent causal continuity. Rejection cannot publish proposed consequences. |
| [Character System](systems/character-system.md) | Supply capability and legitimate access/basis. Internal knowledge does not grant character knowledge; observable effects do not automatically disclose their hidden cause. |
| [Actors & Social Dynamics](systems/actors-social-dynamics.md) | Retain meaningful intentional NPC choices and commitments; agreement adjudication does not independently invent an actor's consent or knowledge. |
| [Narrative Experience](systems/narrative-experience.md) / [F01](f01-truthful-presentation-and-epistemic-fidelity.md) | Express accepted accessible results faithfully, including material limits and uncertainty. Do not repair outcomes, create costs or turn technical rejection into fictional failure. |
| [Player Presentation](systems/player-presentation.md) / [F05](f05-authorized-activities-and-player-control.md) | Preserve input/display and player control boundaries; a method choice cannot expose hidden internal premises. Neither owns consequential truth. |
| [Persistence](systems/persistence.md) | Retain storage/restoration and compatibility responsibility. Gameplay continuity requirements do not select a new save model or establish full campaign persistence. |

## Representative validation and acceptance criteria

These are required validation situations, not prescribed scenario mechanics.
Use explicitly established terms, supported rules and authorized methods;
determine expected results from those premises. Fixtures may provide missing
upstream contracts, including controlled untrusted AI proposals, without live calls.

| Situation | Acceptance criteria |
|---|---|
| Hidden ward, methods and exception | Retrieve the applicable hidden terms from full context. Evaluate grappling-hook and levitation methods distinctly under their actual conditions and existing mechanics. Exercise an authorized exception and its absence. Do not infer immunity or prohibition from the method name alone, silently substitute methods, or choose a scroll/potion without authorization. |
| Observations and legitimate later removal | Present only legitimately observable/accessible findings, preserving hidden causes. An accepted removal changes current applicability for a later attempt; consequential prior results/history retain their meaning. Removal itself must have legitimate authority. |
| Binding agreement | Retrieve and apply relevant prerequisites, exclusions and termination conditions, with the applicable effects and scope. Vary those terms/current circumstances to demonstrate that agreement adjudication follows them, including after legitimate termination. Preserve consequential obligations and accepted results in subsequent interactions. |
| Mundane obstruction control | Resolve an ordinary obstruction using established physical circumstances, capability, authorized means and applicable mechanics. Do not invent a ward, curse or other magical explanation to justify the result. |
| Invalid AI proposals | Deliberately propose bypassing a binding condition, an unauthorized method/resource, an unsupported capability or a result inconsistent with current state/mechanics. Reject each through the owning boundary: no proposed mutation, resource expenditure, acquired knowledge or fictional failure is published merely because it was proposed. |
| Availability and access controls | A material known-but-unavailable condition prompts internal retrieval or remains unresolved without replacement invention or hidden disclosure. Distinguish unspecified and uncertain information. Ordinary immaterial omissions do not block play. |

Across these situations, acceptance requires:

- Reuse of the resolution approach across ward, agreement and mundane domains;
  fixture/scenario identity must not select the answer. Controlled changes to
  relevant authoritative premises demonstrate the resulting differences; where
  uncertainty mechanics apply, control their inputs sufficiently to assess this.
- Evidence distinguishing representation, retrieval, adjudication/acceptance and
  presentation failures. Assess the retrieved premises and their application,
  not just whether output matches a scenario's expected prose.
- Existing relevant mechanics, costs, eligibility and F05 authorization remain
  respected. Accepted costs, elapsed time, findings and consequences carry into
  subsequent supported gameplay; presentation interruption does not reroll or
  erase an accepted result.
- Player-safe information remains separate from trusted internal context.
  Rejected/unresolved proposals preserve authoritative state; accepted changes
  publish coherently through existing integrity boundaries. Any claimed save/load
  behavior must be independently exercised within authorized compatibility scope.
- Meaningful, faithful output is sufficient for this increment; expressive quality
  is not an additional gate. Passing fixtures proves only their bounded coverage.

## Dependencies and explicit implementation exclusions

The accepted [V1a handoff](../information_resolution_core_v1a_handoff.md) describes
a reusable read-only information core, not an adjudicator or production integration.
Its historical pre-publication branch/HEAD/status statements describe that handoff;
the published reference for this design is the commit recorded above.
V1a's public operations are candidates for reuse. Suppliers still own completeness,
relevant query scope, authoritative inputs and legitimate character grants.
The core cannot infer omitted established facts without supplied information,
certify relevance sufficiency or evaluate returned binding terms.

Eventual bounded implementation may use predetermined, contract-conforming
suppliers for unimplemented context/authorization, foundations, current/history,
capability/access and proposal generation. Identify every stipulated input and
its limits. Adjudication must still depend on retrieved premises.

This design does not claim or require general natural-language interpretation,
automatic relevance discovery, comprehensive rules interpretation or full campaign
persistence without independent implementation and validation. It prescribes no
scenario-specific mechanic, graph database, universal entity schema, new save
format, exhaustive ledger or autonomous simulation. General actor agency,
offscreen reconciliation, Region Pack production/import and memory/access
derivation remain separately scoped dependencies. No model, prompt, provider
configuration, live call, generic framework or broad refactor is selected.

## Accepted residual risks and deferred questions

Information Foundation's [accepted R1–R4](information-foundation-functional-design-v1.md#accepted-residual-risks)
remain applicable: retrieval omission, adjudication misapplication, historical
under-persistence and excessive complexity. Evaluate observed gameplay failures
proportionately; these risks do not mandate speculative infrastructure.

Remaining implementation questions are bounded supplier/query completeness,
supported condition/rule coverage, proportionate proposal checks, and the minimum
continuity needed for the chosen slice. General interpretation, relevance discovery,
semantic rules coverage, durable retention and production integration remain
deferred; fixture success cannot settle them. F01 narrative quality remains
deferred here subject to meaningful fidelity. No additional risk waiver or new
material design decision is introduced by this consolidation.

## Design → Implementation readiness and bounded handoff

**Ready for owner consideration of a bounded implementation package.** D-A1–D-A6
provide sufficient functional direction and acceptance criteria without selecting
a new representation, persistence model or universal protocol. No unresolved
design conflict was identified in consolidation. Readiness is not package
selection, staging, implementation authorization or implementation acceptance.

Recommended objective: demonstrate reusable information-grounded adjudication
over supplied authorized context and V1a-compatible authoritative information,
with owning-boundary acceptance, player-safe results and consequential continuity
across the ward, agreement, mundane control and invalid-proposal scenarios above.
Keep missing upstream capabilities explicit through contract-conforming suppliers.
Reuse existing mechanics and integrity boundaries where appropriate; assess code
as evidence against this design before choosing integration points.

The separately authorized package must state its supported operations, suppliers,
integration/state boundary, continuity scope and exclusions before implementation.
Apply the [engineering posture](../engineering_posture.md) to actual consequences;
meaningful cross-system or persisted consequences warrant Elevated verification.
Focused offline cases, directly affected regressions, integrity/compatibility
checks where affected and owner gameplay evaluation should demonstrate the criteria
above. No production integration or persistence expansion is pre-authorized here.

Stop for owner review of this consolidation. Package selection, lifecycle staging,
execution and Git publication retain their separate workflow authorizations.
