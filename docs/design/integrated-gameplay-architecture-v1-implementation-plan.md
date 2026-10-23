# Integrated Gameplay Architecture V1 — Implementation Plan

**Phase: Design. Status: documentation candidate for owner review.** Prepared October 23,
2026 against verified local and remote `main`
`ed3bdbe782a6e4f0e0f636207724795ffe8f33e7`. This plan records the owner's
three bounded implementation milestones for the accepted
[Integrated Gameplay Architecture V1](integrated-gameplay-architecture-v1.md).
That canonical record preserves IG-01–IG-18 and IG-20–IG-23; IG-19 is not accepted
and supplies no implementation requirement. This plan does not replace the decisions.

This document selects no capability package, stages no milestone or sprint,
and authorizes no implementation, publication or live-provider execution.
[WORKFLOW.md](../../WORKFLOW.md) governs separate package authorization,
lifecycle staging, implementation acceptance and Git authority.

## Common runtime and retained contracts

I1, I2 and I3 extend one common reusable runtime. Later milestones build on the
same interpretation, undertaking, context and acceptance responsibilities rather
than constructing isolated scenario implementations. Scenario-specific fixtures
supply missing upstream contracts; scenario identity must not select an outcome.
Existing code is evidence and a candidate for reuse, not design authority.

Preserve [F05](f05-authorized-activities-and-player-control.md),
[F01](f01-truthful-presentation-and-epistemic-fidelity.md),
[Information Foundation](information-foundation-functional-design-v1.md),
[Information-Grounded Adjudication](information-grounded-adjudication-v1.md),
the [system responsibilities](systems/system-map.md) and
[shared doctrines](systems/README.md#shared-doctrines). Their contracts remain
canonical; this plan identifies integration work without reproducing them.

Coordination interprets and manages the executable scope of authorized
undertakings, including ordinary constituent steps and continuation boundaries.
It does not independently establish world facts, mechanical outcomes or NPC
decisions. Scene state supplies authoritative contextual information, including
relevant spatial, temporal, environmental and actor circumstances, through the
appropriate owners. Presentation and internal adjudication retain distinct
information access under F01 and the Information Foundation.

Conceptual responsibilities do not prescribe separate runtime modules,
individual AI calls, a fixed model architecture or a new generic framework.
Retain scalable selective information access and meaningful continuity without
requiring a graph database, universal entity framework, exhaustive event ledger
or continuous world simulation. Use existing applicable mechanics; fixtures
must not invent unsupported gameplay rules.

The milestone allocation below identifies primary delivery responsibility;
cross-cutting contracts apply whenever a milestone exercises the affected behavior.
Partial milestone evidence must not be presented as complete IG implementation.

| Milestone / continuing obligation | Decision coverage |
|---|---|
| I1 — Coordination foundation | IG-01–IG-03, IG-06, IG-22–IG-23 |
| I2 — Consequential integration | IG-04–IG-05, IG-07–IG-08, IG-10, IG-20–IG-21 |
| I3 — Continuing gameplay integrity | IG-09, IG-11–IG-15; complete IG-21 recovery/save-load continuity |
| All milestones — failure containment, integrated validation and proportionate testing/model use | IG-16–IG-18; mandatory applicable runtime validation throughout |

## I1 — Coordination foundation

**Bound:** Interpretation, undertaking boundaries, scene grounding,
responsibility selection and clarification.

Develop the common runtime's ability to interpret inquiry, preparation and
commitment in context; identify the authorized undertaking and routine
constituent steps; select the responsibilities needed for its next situated
activity; and return meaningful choices to the player under F05. Ground this in
current scene circumstances and established geography. Clarification concerns
material player-owned ambiguity, not every ordinary execution detail or an
internal hidden-information gap.

Processing is proportionate to actual scene context, not a rigid universal
complexity category. Opening a door in an empty hall and opening it while evading
nearby guards can require different participation. Direct or combined paths are
permitted when they preserve the applicable contracts. Interpretation alone
neither authorizes nor resolves the activity; plausible possibilities or an
open-ended clarification must leave the method to the player.

Broad undertakings such as searching a castle progress through situated
activity. Starting from the character's current hall does not by itself choose
every later destination, search focus, method or risk. Established layout and
access constrain progression; previously unspecified details follow the existing
Specificity Doctrine. Attention can reveal ordinary detail without creating a
secret or granting new knowledge. Prior player direction and accepted risk may
already answer a continuation question; ask only where a meaningful unresolved
choice belongs to the player.

**Validation:** Exercise inquiry versus commitment, a routine local undertaking,
and a broad castle search beginning in a situated hall. Vary established
location, routes, available means and player direction through the same runtime.
Demonstrate ordinary constituent execution without unnecessary clarification,
and return control before a materially different method, expenditure, risk or
direction would be selected. Exercise known geography and explicitly unspecified
detail without silently replacing established facts. No outcome, NPC consent,
capability or missing prerequisite may be supplied by coordination itself.
Check that one message containing independent undertakings does not authorize
their automatic execution, and that quietness or carefulness can constrain the
same situated undertaking without imposing a separate activity category.

**Completion evidence:** Identify supported interpretation and continuation
boundaries, responsible owners, fixture assumptions and unresolved inputs.
Demonstrate meaningful, player-safe choices and reusable coordination. This
milestone does not claim general language understanding or complete upstream
domain implementations.

## I2 — Consequential integration

**Bound:** Domain-owned information discovery, adjudication, authoritative fact
incorporation and coherent acceptance.

Extend I1 so the responsible domains normally identify their applicable
information requirements. Include relevant relationships, innate capabilities,
equipment, active effects and scene circumstances where applicable. Information
retrieval supplies authoritative premises; the owning gameplay domains determine
their meaning and application. A central coordinator must not become the sole
source of domain dependency knowledge or a second adjudicator.

Combine legitimate authoritative premises with authorized methods and applicable
mechanics through Information-Grounded Adjudication. Respect hidden binding
conditions without granting player knowledge of them. Material established but
unavailable information requires internal retrieval or an unresolved result;
it cannot be invented as if unspecified. Accepted consequential facts must enter
their owning authoritative domains so later activities can depend on them.
Incorporation preserves relevant identity, meaning, scope, temporal applicability
and relationships; narration alone is insufficient.

Dependent consequences require coherent acceptance, current-state validity,
retry safety and durable recognition. Rejected or stale proposals must not
publish partial consequences or masquerade as fictional failure. Acceptance
must preserve the relevant result, costs, time, facts and commitments together
where they depend on one another. Neither proposal generation nor presentation
confers acceptance. Independently adjudicated and accepted partial success or
incremental progress remains legitimate; it differs from accidental partial
publication of an unaccepted proposal. This specifies integrity requirements
without selecting a universal transaction protocol or new persistence representation.
I2 must identify the durability boundary it actually validates; a disposable
session cannot establish I3's cross-session persistence criterion.

**Validation:** Use the common runtime for a hidden binding condition, an
authorized exception, a mundane obstruction and a consequential commitment,
using supported mechanics and explicit premises. Vary retrieved information,
relevant relationships, capabilities, equipment and active effects to demonstrate
domain-owned applicability and consequential dependence. Include invalid proposals,
unavailable established information and changed current state before acceptance.
Exercise iterative retrieval when an earlier result identifies another material
dependency. A directly supplied innate immunity and an active protection linked
to its applicable definition illustrate ordinary domain dependencies; use
contract-conforming inputs without introducing unsupported combat or magic rules.
Exercise rejection without mutation, coherent dependent acceptance, retry without
duplicated costs/effects, and recognition of prior acceptance in the supported
continuity boundary. Later gameplay must retrieve accepted facts from their
owning domains rather than rely on narration or an unaccepted proposal cache.
Verify the identity, scope, temporal meaning and relevant relationships of a
newly incorporated consequential fact, including a legitimate increment that
survives a later rejected proposal.

**Completion evidence:** Distinguish representation, dependency discovery,
retrieval, adjudication, acceptance and presentation failures. Show the same
runtime behavior across cases, state its supported conditions and mechanics,
and identify exactly what recognition and durability have been demonstrated.
Full campaign persistence remains I3 work unless separately authorized earlier.

## I3 — Continuing gameplay integrity

**Bound:** Activity resumption, persistence, temporal continuity and traceability.

Extend I1/I2's common runtime across interruption, changed circumstances,
restoration and later gameplay. Evaluate resumption using current circumstances,
the activity's nature, applicable rules and accepted results under F05. Preserve
legitimate prior costs, elapsed time, findings, traces, commitments and outcomes.
An already resolved attempt is not rerolled because its presentation paused;
a legitimate new attempt follows its applicable rules and renewed authorization.

Persist and restore the supported consequential meaning and acceptance recognition
needed for retry safety. Maintain relevant historical and causal basis so later
gameplay can distinguish what occurred, what was accepted and what remains
unresolved. Retention is proportional to consequential need, not an exhaustive
transcript or event ledger. Fictional time and supported world developments
remain with their existing owners; save/load, model calls, UI transitions and
process restarts do not themselves advance time or reset the fiction.

At natural re-entry, establish necessary unattended developments before the
affected interaction. Respect established causes, commitments and elapsed time,
without retroactively favoring unexpressed player intentions. Current conditions
and meaningful historical truth remain distinct. Continuity covers relevant
world, character, actor, relationship, activity and historical meaning without
requiring every incidental event to be retained.

Provide sufficient structured diagnostic traceability for consequential
interpretation, responsibility selection, retrieval, adjudication, validation,
acceptance, persistence and presentation. Diagnostic records do not establish
campaign truth. Stable identities and selective relationship/history access must
support potentially large campaigns and appropriate future scaling or migration
without altering established meaning; no storage technology is prescribed.

**Validation:** Interrupt and resume a situated search while retaining accepted
findings and disturbances; change a material circumstance before continuation;
exercise legitimate restart where the supported activity's rules require it.
Save and restore representative accepted consequences and dependent commitments,
then retry and continue without duplicated costs, effects or resolution. Check
restoration failure isolation, applicable save compatibility and continuity
through technical boundaries. Trace consequential results back to sufficient
authoritative premises and acceptance basis while keeping hidden information
out of player-facing output. Exercise only supported temporal processes; do not
invent an offscreen scheduler or autonomous actor mechanics to fill fixture gaps.
Verify that resumption enforces applicable initial restrictions against current
state, including after restoration, and that unaccepted proposals never become
durable truth. Include a natural re-entry case with controlled elapsed time and
an established commitment; distinguish current applicability from retained history.

**Completion evidence:** State the actual persistence, compatibility, resumption,
time and traceability guarantees exercised, with any remaining fixture limits.
Any new save representation, migration or version change requires explicit
authorization before implementation; this plan supplies none.

## Fixtures, validation and future implementation handoff

Contract-conforming fixtures may supply foundations, current scene/world state,
capability/access, domain requirements, NPC choices, authorized methods and
controlled untrusted proposals while upstream systems remain unavailable.
Identify supplied assumptions and their limits. Fixtures must exercise common
runtime behavior, preserve F01/F05 and authoritative ownership, and avoid treating
preselected scenario answers as adjudication. Passing them establishes bounded
coverage, not production integration or general gameplay reliability.

Core runtime validation is mandatory for supported authorization, applicable
conditions, authoritative acceptance and integrity boundaries. Additional
diagnostics may be configurable; runtime validation cannot be disabled to
simplify testing. Development testing remains proportionate under
the [engineering posture](../engineering_posture.md); diagnostics and extensive
preventive infrastructure are not prerequisites for all ordinary play.

For each separately authorized implementation boundary, use relevant syntax or
static checks before broad execution, focused tests, directly affected regressions,
documentation reconciliation and scope/diff checks. Meaningful cross-system
consequences and persisted semantics call for Elevated verification, including
targeted architecture and affected compatibility/recovery checks. Keep automated
tests offline; any live evaluation needs separate explicit authorization.
When model behavior is the subject of an authorized investigation, use the
lowest-cost live model adequate for the required capability. Use deterministic
fixtures and structural checks where they provide sufficient evidence.
Automated checks and owner experiential assessment are complementary;
avoid separate playable slices when continuing integrated validation suffices.

In each milestone, identify the earliest relevant failure and any subsequent
containment failure. Distinguish interpretation, routing, retrieval, authorization,
adjudication, validation, persistence, presentation and technical failures.
Exercise rejection/error containment without mutation, hidden disclosure or
conversion into fictional outcomes. Trace relevant boundaries as they are built;
I3 completes continuing diagnostic coverage rather than postponing all failure
attribution until persistence exists.

Review exploration progression, domain-owned dependency discovery and acceptance
integrity together. Verify that scene/geography constraints neither authorize
silent itinerary choices nor force exhaustive modeling; that proportional
retrieval includes applicable material constraints; and that subsequent gameplay
uses coherently accepted facts with their authoritative meaning intact.

A future implementation handoff must identify its bounded capability, supported
domains and mechanics, reusable runtime contribution, fixture suppliers,
integration/durability boundary, risk and validation. Existing components may be
reused, adapted or replaced to satisfy accepted design. Unresolved material
authority, persistence or behavioral conflicts require owner judgment before
dependent implementation. No milestone or subsequent package begins automatically.
