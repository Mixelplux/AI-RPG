# Strategic Roadmap

## Role

This document describes strategic direction, priorities, and deferrals.
Use observed player experience to choose small coherent capabilities under
`docs/engineering_posture.md`; routine planning needs no formal review packet
or full architecture review. `docs/current_sprint.json` alone owns
machine-enforced lifecycle state; Markdown package/sprint records explain it, and
`docs/conditional_procedures.md` owns triggered process detail.

## Current Capability Position

The engine has a deterministic, simulation-owned core with immutable authored
Region Packs and durable World State. It supports a bounded playable vertical
slice with scene construction, structured interaction, movement and elapsed
time, durable history, authored discoveries and clue presentation, scoped
world reactions, actor knowledge, and player-safe projections.

Persistent changes use copied candidate state, validation, derived-scene
construction, and one publication. Causal history is durable and referenceable.
Save compatibility remains version 1. Through October 11 accepted work at published
baseline `a6ff3164`, bounded contextual investigation supports selected examination,
questions and reporting; optional declared material handling supports disclosed
authorization, preparation, outcomes, cooperation and causal conditions. The opt-in
Market passage and independent test fixtures do not establish general action,
physics, social agency or multi-system composition.

Narration remains untrusted and non-authoritative. Bounded accepted result/scene
composition uses replaceable preparation and stateless realization with local
adapters; ordinary provider preview routes coexist. North-Gate working focus is
session-only. General narration selection/fidelity and the broad-observation
fallback experience remain incomplete. See the [runtime architecture](architecture.md),
[deferred findings](deferred_findings.md) and non-authoritative
[research index](architecture_comprehension_review.md). Research candidates,
including Option C, do not select or authorize the next capability.

## Strategic Directions

### Player-Facing Coherence

Strengthen the player’s understanding of place, available action, visible
change, and consequence. Favor clear spatial orientation, meaningful local
affordances, and authored information that supports natural next actions
without exposing hidden simulation state.

### World Evolution Through Bounded Causality

Extend world change only where a specific authored event, elapsed time, or
player action has a clear simulation-owned effect. New behavior should compose
with existing candidate-state, causal-history, validation, and projection
boundaries rather than introduce broad reaction machinery.

### Information, Evidence, and Social Continuity

Develop the distinction among objective truth, evidence, actor knowledge,
public belief, and player perception when a bounded player experience needs
it. Information should remain selective, causally grounded, and player-safe;
detail earns persistence only when future gameplay depends on it.

### Authored Vertical-Slice Depth

Use compact authored situations to evaluate how discovery, conversation,
movement, time, and consequences form coherent player loops. Prioritize
observed player friction and continuity over speculative subsystem breadth.

### Safe Narration Evolution

Keep provider-backed narration optional, cost-bounded, validated, and
nonpersistent. Any future expansion must preserve simulation authority,
provider failure closure, and deterministic gameplay without provider access.

## Important Deferrals

- Generic consequence, condition, effect, reaction, transaction, or dispatch
  frameworks.
- Broad autonomous schedules, world simulation sweeps, or background NPC
  behavior.
- Universal belief, familiarity, semantic-memory, or knowledge-graph systems.
- General travel duration, pathfinding, exhaustive local geometry, and
  procedural spatial simulation.
- Combat, economy simulation, faction warfare, companions, and procedural
  quest generation until a concrete player need justifies a bounded design.
- Provider-authored world mutation, provider authority over truth, and
  narration-dependent core gameplay.

## Architectural and Product Priorities

- Preserve simulation-owned truth, immutable authored content, and
  player-safe derived projection.
- Prefer the minimum persistent detail that supports meaningful player
  experience; avoid modeling possibilities merely because they are plausible.
- Keep material transitions atomic, causally traceable, validated, and
  compatible with existing saves unless an explicitly authorized change says
  otherwise.
- Use focused evidence from completed work to choose the next bounded
  capability; this roadmap does not authorize, stage, or start one.
- Scale verification to Routine, Elevated, or Critical consequence and recovery
  difficulty; preserve focused tests without routine enterprise-style ceremony.
