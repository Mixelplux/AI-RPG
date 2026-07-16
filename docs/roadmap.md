# Strategic Roadmap

## Role

This document is the authoritative strategic roadmap for architecture review
and review-packet context. It describes direction, priorities, and deferrals;
the current project records own package and sprint state, and
`docs/conditional_procedures.md` owns triggered process detail.

## Current Capability Position

The engine has a deterministic, simulation-owned core with immutable authored
Region Packs and durable World State. It supports a bounded playable vertical
slice with scene construction, structured interaction, movement and elapsed
time, durable history, authored discoveries and clue presentation, scoped
world reactions, actor knowledge, and player-safe projections.

Persistent changes use copied candidate state, validation, derived-scene
construction, and one publication. Causal history is durable and referenceable.
Save compatibility remains version 1. Narration is an explicit, untrusted,
provider-neutral preview boundary rather than simulation authority.

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
