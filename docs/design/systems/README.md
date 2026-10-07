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

## Navigation and status vocabulary

- [Responsibility hierarchy and information flow](system-map.md)
- [Reusable manifest template](system-manifest-template.md)
- [World Simulation](world-simulation.md) — Partial; reviewed October 5, 2026
- [Character System](character-system.md) — Partial; reviewed October 6, 2026
- [Action & Resolution](action-resolution.md) — Partial; reviewed October 6, 2026
- [Actors & Social Dynamics](actors-social-dynamics.md) — Partial; reviewed October 6, 2026
- [Narrative Experience](narrative-experience.md) — Partial; finalized October 6, 2026
- [Scenario & Authored Content](scenario-authored-content.md) — Partial; finalized October 6, 2026
- [Persistence](persistence.md) — Partial; finalized October 6, 2026 at
  `56baf51a26c2ca2effeb098b78937bd381e28304`
- [Player Presentation](player-presentation.md) — Partial; current review candidate
  October 6, 2026 at protected baseline `56baf51a26c2ca2effeb098b78937bd381e28304`

Use **Implemented** for behavior evidenced in runtime and tests, **Partial** for
a responsibility with bounded implementation and material gaps, **Accepted design**
for agreed direction without claiming code, **Provisional** for a revisable model
or unsettled interface, and **Deferred** for capability outside current work.
An accepted direction can also have deferred implementation; state both when
useful. These labels do not replace the historical status vocabulary in
simulation principles or authorize scheduling.

All eight planned manifests are now present. Player Presentation is the current
documentation review candidate, not an accepted implementation package. Protected
manifests retain their original review-baseline/status wording; the shared index
and map record subsequent finalization milestones without rewriting those records.

## Shared doctrines

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
