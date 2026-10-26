# System design manifests

System manifests record the best current model based on design, implementation,
and play evidence. They preserve reasoning, authority boundaries, and system
relationships. They are not hard constraints against justified change and should
be revised when new evidence demonstrates a better model.

This directory adds a living responsibility model to the existing flat
documentation collection. It does not replace the [runtime architecture
map](../../architecture.md), [ADRs](../../decisions.md), [simulation
principles](../../simulation_principles.md), [simulation model](../../simulation_model.md),
or [Story-First Design Doctrine](../../story_first_design_doctrine.md).
Those retain their decisions and historical reasoning. Manifests link evidence
and distinguish present implementation from future design; they do not authorize
new implementation or override [workflow](../../../WORKFLOW.md) and lifecycle.
Only genuine contractual rules, such as simulation authority and fail-closed
provider behavior, should be presented as contracts.

## M2-2a owner-accepted implementation — October 26, 2026

[Consequential uncertain climbing and falling](../../physical_traversal_m2_2a_handoff.md)
extends the published M2-1 common aggregate across World, Character, Resolution and
Persistence. The [bounded model](../../physical_traversal_m2_2a_design.md) records
pre-check grounding, explicit effort, immediate injury and schema compatibility.
The owner accepted the corrected bounded implementation October 26, 2026. M2-2a
is complete/idle; Git publication remains separate and the systems remain Partial.
Ordinary climbing remains mechanical without unnecessary equipment detail; the
documented meaningful-activity requirements and deferred capabilities are preserved.

## Navigation and status vocabulary

- [Responsibility hierarchy and information flow](system-map.md)
- [Reusable manifest template](system-manifest-template.md)
- [Information-Grounded Adjudication V1](../information-grounded-adjudication-v1.md)
  — Owner-accepted D-A1–D-A6 and bounded implementation. Retains existing
  system authority and F01/F05 contracts; implementation separately authorized.
  The [October 22 bounded implementation](../../information_grounded_adjudication_v1_handoff.md)
  is owner-accepted with its inquiry correction; finite conditions, offline acceptance and session
  continuity are implemented without production/persistence integration.
- [Information Foundation Functional Design V1](../information-foundation-functional-design-v1.md)
  — Accepted design; bounded V1a implementation accepted following final code-level review.
  See the [V1a handoff](../../information_resolution_core_v1a_handoff.md).
  Cross-system information contracts,
  Region Pack scope, continuity, validation scenarios, rationale and accepted
  gameplay-evaluated risks; existing conceptual ownership is preserved.
- [World Simulation](world-simulation.md) — Partial; individual review complete October 5, 2026
- [Character System](character-system.md) — Partial; individual review complete October 6, 2026
- [Action & Resolution](action-resolution.md) — Partial; finalized October 6, 2026
- [Actors & Social Dynamics](actors-social-dynamics.md) — Partial; finalized October 6, 2026
- [Narrative Experience](narrative-experience.md) — Partial; finalized October 6, 2026
- [Scenario & Authored Content](scenario-authored-content.md) — Partial; finalized October 6, 2026
- [Persistence](persistence.md) — Partial; finalized October 6, 2026 at
  `56baf51a26c2ca2effeb098b78937bd381e28304`
- [Player Presentation](player-presentation.md) — Partial; finalized October 6, 2026 at
  accepted baseline `f18a9512adcf659facbf9e70ae29bdc4a9146607`

Use **Implemented** for behavior evidenced in runtime and tests, **Partial** for
a responsibility with bounded implementation and material gaps, **Accepted design**
for agreed direction without claiming code, **Provisional** for a revisable model
or unsettled interface, and **Deferred** for capability outside current work.
An accepted direction can also have deferred implementation; state both when
useful. These labels do not replace the historical status vocabulary in
simulation principles or authorize scheduling.

All eight individual manifest reviews are complete, and their Partial
implementation classifications remain unchanged. Cross-system synthesis was
finalized at `9f402a352ca038e35dcc96eb2b1876e7f5b0f171`; the overall System
Manifest completion review was accepted October 7, 2026. No fundamental
architectural contradiction or missing system responsibility was found.
Intentional unresolved questions remain deferred. Completion selects no
implementation package or next milestone. These living manifests and their
responsibility model may be revised when future evidence supports a better model.

## Accepted design integration

[F01](../f01-truthful-presentation-and-epistemic-fidelity.md) and
[F05 — Authorized Activities and Player Control](../f05-authorized-activities-and-player-control.md)
are canonical accepted Design records. Their
[integration boundaries](system-map.md#f01f05-design-integration-boundaries)
refine intended gameplay without changing the manifests' implementation status,
selecting modules or extending the shared doctrines below. The subsequent
separately authorized [bounded F05 implementation](../../f05_implementation_preflight.md)
was [owner accepted](../../f05_authorized_activities_v1_acceptance.md) October 16, 2026;
its policy/material checkpoint and offline fixture coverage do not complete the
Partial systems or begin the deferred playable integration milestone.

## Core gameplay domain design — October 25, 2026

The owner-accepted [cross-domain contracts CD-01–CD-09](../core-gameplay-domains-cross-domain-contract-design-v1.md)
and [physical traversal PT-D1–PT-D9](../physical-traversal-domain-design-v1.md)
specialize the accepted Integrated Gameplay Architecture and existing F01/F05,
Information Foundation and responsibility contracts. See the
[system-map reconciliation](system-map.md#core-gameplay-domains-and-physical-traversal--accepted-design).
These are intended semantics, including shared relevant PC/NPC mechanics and
World-owned physical-object relationships with Character-owned equipment use.
The manifests' Partial implementation classifications and shared doctrines remain
unchanged. Proposed traversal implementation and sequencing require separate
authorization; this incorporation selects no package or lifecycle transition.

The separately authorized [Physical Traversal M1 implementation handoff](../../physical_traversal_m1_handoff.md)
records owner acceptance of bounded World/Character/rule foundations on October 26, 2026. Common
assessment is exercised; consequential integration and new-domain persistence
remain M2. M1 is closed. The separately owner-authorized
[M2-1 foundation](../../physical_traversal_m2_1_design.md) is published: coherent
domain acceptance and opt-in v3 persistence with deterministic full-link climbs.
The accepted M2-2a extension above adds bounded hazardous failure and immediate
injury; interruption/resumption and broader playable integration remain deferred.
Overall systems remain Partial; no next package is selected.

## Shared doctrines

Current bounded implementation evidence: [damaged-gate F01–F05 integration](../../f01_f05_gate_integration_v1.md),
structurally owner-accepted October 17, 2026; see [acceptance and scope](../../f01_f05_integration_v1_acceptance.md).
Explicit fixtures do not upgrade general system
implementation classifications or revise the shared doctrines below.

These centrally recorded doctrines apply across responsibilities. Existing
accepted reasoning is in Story-First Part I and ADR-059; the rules below express
that direction and the owner-supplied System Manifest Review foundation.
They are design guidance unless an existing authority/integrity rule is
explicitly contractual. They do not imply generalized runtime support.

### Specificity Doctrine

Use the lowest level of specificity capable of producing a coherent, meaningful
result. Default escalation:

**Inference → Lazy resolution → Explicit persistent state → Active simulation**

Specificity is earned by relevance, attention, interaction, consequence,
persistent investment, or independent agency. It determines resolution depth,
not system ownership. Do not simulate ordinary background activity merely
because it could plausibly occur.

A random worker discovering and sealing a sewer entrance normally need not be
individually simulated. If the entrance matters months later, its current
condition can be lazily reconciled from elapsed time, normal maintenance/activity,
concealment, prior traces, and relevant conditions. This is a design example,
not a current engine capability.

### Context Carry-Forward

Persistent truth does not require persistent mention. Established weather,
social atmosphere, injury, darkness, danger, or another persistent condition
normally carries implicitly in later narration. Re-express it when it materially
changes, affects the current action, produces a new observable consequence,
becomes newly relevant, or concise reorientation is needed after a meaningful
transition. This addresses repeated restatement of an unchanged blizzard.
Sprint 10.80 provides a bounded presentation mechanism, not universal continuity.

### Attention / Relevance Drives Detail

For presentation, attention increases descriptive resolution, not significance.
For systems, relevance increases systemic specificity, not necessarily importance.
Looking harder at an ordinary shack can reveal more ordinary detail without
creating a secret.

### Authority Before Presentation

The owning gameplay system establishes truth; Narrative Experience presents it.
Narration must not independently determine consequential world truth, actor
decisions, character capability, or action outcomes. This preserves the existing
contractual simulation/provider authority boundary. Compatible incidental
expression does not become durable truth merely by being narrated.

### Authority Composition

Orchestration, storage, projection, persistence, or shared publication does not
transfer conceptual authority. Each system retains authority over the meaning
it establishes, even when `world_state` stores it, `GameEngine` orchestrates it,
one candidate transition publishes several systems' changes, Persistence saves
it, or Narrative Experience and Player Presentation project it. This revisable
responsibility guidance preserves the contractual simulation/provider boundary;
it does not require separate modules, containers, or publication APIs.

Authored identities, foundations, motivations, declarations, fixed bounded rules,
replies, constraints, and possible consequence material can support runtime
behavior. They do not automatically grant Scenario & Authored Content general
actor decision authority. Actors & Social Dynamics owns meaningful consequential
intentional non-player choice; Action & Resolution adjudicates supported attempts
where needed; World Simulation owns resulting external reality and its subsequent
legitimate causal progression. Existing fixed bounded authored scenario behavior
remains valid through its supported runtime interpretation.

### Causal Continuity

Accepted consequences arise from authoritative state, choices, adjudicated
outcomes, elapsed fictional time, and supported causal processes. Narrative
interest alone is not a cause. Initiating or publishing a consequence does not
transfer downstream progression from its appropriate owning system.

Persistence and history should preserve enough provenance when future reasoning
requires established causal meaning, including relevant unresolved consequences
or commitments. Retention follows story relevance and consequential need under
the Specificity Doctrine; ordinary background activity needs no exhaustive log.
This is revisable guidance, not a universal provenance schema, event-sourcing
requirement, continuous simulation, generalized causal engine, or scheduler.
Existing bounded causal records do not establish those broader mechanisms.

### Fictional Continuity Is Independent of Technical Boundaries

Save/load, model calls, UI transitions, process restarts, and technical sessions
do not themselves create fictional discontinuities. A presentation cache reset
does not reset fictional reality or advance time.

### Character Life Exceeds Played Transcript

Played scenes are selective. Sustained circumstances imply reasonable ordinary
lived experience. A month living in Bryn Shander may justify familiarity with
major streets, public businesses, and normal routines even if those experiences
were never played. This does not grant hidden information or automatic knowledge
of recent changes; ADR-059 preserves potentially stale familiarity.

### Sparse Epistemic State

Derive ordinary knowledge. Persist exceptional informational access only when
access itself matters and cannot be reconstructed reliably.

- Exposure establishes breadth.
- Attention establishes detail.
- Interaction establishes consequential specificity.

Hidden, private, unusual, contested, or consequential information requires
stronger provenance. Do not create a shadow copy of World State inside Character
Knowledge. Existing actor knowledge membership and player discovery IDs are
bounded records, not a universal knowledge model.

World Simulation establishes what exists and its externally observable properties.
Character System establishes character-specific capability, informational
access/basis, and relevant retained continuity. A legitimate accessible view may
be derived jointly from these inputs. Narrative Experience selects and frames
information within that view; Player Presentation displays it. Character System
does not independently own all perception, and world truth alone does not grant
character knowledge. General familiarity/access mechanisms remain unimplemented.

## Intentional unresolved questions

The manifests preserve these deferred design questions. This synthesis selects
no mechanism or implementation package to resolve them:

- Topology/destination knowledge versus character familiarity.
- When reliance on incidental narrative detail requires authoritative acceptance.
- NPC informational state versus social/relationship state at their shared interface.
- Source-content revision versus established saved-campaign meaning.
- Future competence changes versus the historical basis of accepted attempts.
- Minimum durable provenance for unresolved consequences, obligations, or commitments.
