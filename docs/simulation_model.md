# Simulation Model

## Purpose

This document describes the conceptual model for how the AI Narrative RPG Engine's world behaves.

It is not an implementation specification. It should guide future sprint planning, architecture decisions, and Codex implementation work without requiring premature systems.

The model exists to preserve the project's direction after Sprint 8 and before Phase 2 implementation.

---

## Status

**Status:** Baseline

This document captures the accepted direction from the post-Sprint-8 Project Review and Simulation Design Summit.

Concepts here are design guidance. They do not become implementation requirements until a sprint explicitly schedules them.

---

## Core Model

Resolved authored investigations may have one explicit durable world reaction when an approved Region Pack declaration binds that exact resolution to a stable actor location. Such a reaction is simulation state, not narration, and remains bounded to its authored transition rather than implying general autonomous behavior.

The engine should distinguish between:

- objective world truth
- actor knowledge
- public belief
- player-character perception
- AI narration

The simulation owns truth. The AI expresses what the player character can perceive, hear, infer, or be told.

```text
Objective Truth
    ↓
Evidence / Observable Traces
    ↓
Actor Knowledge or Interpretation
    ↓
Public Belief / Rumor / Lie / Myth
    ↓
Player-Character Perception
    ↓
AI Narration
```

The narrator should not bypass this pipeline by revealing hidden truth as flavor.

---

## 1. Objective Truth

Objective truth is what is actually true in the world.

Examples:

- The prince was murdered.
- The dragon is alive.
- The northern bridge collapsed yesterday.
- The stolen relic is hidden beneath the chapel.

Objective truth can exist even if no actor knows it.

The simulation owns objective truth. AI narration must not alter it for convenience, drama, pacing, or surprise.

---

## 2. Knowledge Is Not Truth

Knowledge is an actor's understanding of reality.

Knowledge can be:

- true
- false
- incomplete
- outdated
- inferred
- rumored
- deliberately deceptive

The world may contain truth without knowledge, and knowledge without truth.

Examples:

- A dragon lairs in the distant hills, but no one has seen it yet.
- Villagers believe a dragon is killing livestock, but a secret group is staging the attacks.
- A story says an abandoned keep contains treasure, but the keep was looted decades ago.

False belief can still produce real consequences. If people believe there is a dragon, caravans may avoid the road even if no dragon exists.

---

## 3. Actor Knowledge

Actors should not know things merely because they happened in the simulation.

Knowledge should require a plausible access path, such as:

- direct observation
- conversation
- written records
- rumors
- reports
- investigation
- inference
- magical means
- cultural knowledge
- professional expertise

Knowledge resolution should short-circuit when access fails.

Example:

```text
Question: Did anyone leave by the north gate last night?

Was the guard there?
  No → The guard cannot know from direct observation.

  Yes → Did anyone leave?
      No → The guard may truthfully say no if they observed the gate.

      Yes → Did the guard notice?
          No → The guard does not know.

          Yes → Does the guard remember?
              No → The guard cannot reliably answer.

              Yes → Is the guard willing to answer?
                  No → The guard may withhold, evade, or lie.

                  Yes → The guard answers according to what they know.
```

This is a conceptual access model, not a required implementation algorithm.

---

## 4. Public Belief, Rumor, Myth, and Lies

Presented knowledge does not have to be objectively true.

Rumors, myths, lies, propaganda, superstition, and mistaken interpretation may enter the player's experience as things actors believe or say.

Examples:

- "A dragon stalks the mountain pass."
- "The old keep contains treasure."
- "The prince was killed by foreign assassins."

These statements may be true, false, incomplete, manipulated, or outdated.

The simulation should distinguish the existence of a belief from the truth of the belief.

---

## 5. Evidence and Observable Cues

Evidence is what objective truth leaves behind or what actor behavior reveals.

Examples:

- footprints in snow
- a broken lock
- a missing heirloom
- trembling hands
- contradictory testimony
- livestock carcasses
- unusual silence in a forest

Evidence should not automatically become consequence. It becomes meaningful only if an actor can plausibly encounter it, interpret it, care about it, and act.

### Salient Cues

A salient cue is narration that invites player attention or implies hidden meaning.

Examples:

- "A nervous-looking servant hurries past."
- "The guard watches you too closely."
- "The merchant flinches when you mention the prince."

Salient cues should be grounded in simulation truth, actor knowledge, or player-character perception. They should not be invented by the AI as casual flavor.

Neutral ambience may be AI-generated if it does not create durable truth or imply hidden significance.

---

## 6. Passive and Active Perception

The engine should distinguish passive recognition from active investigation.

### Passive Recognition

A character may notice meaningful cues without explicit prompting if their skills, background, attention, knowledge, or circumstances make the cue salient.

Example:

A court-trained bard may passively notice that a servant is moving too quickly for court protocol.

### Active Investigation

If a cue is not passively noticed, the player may still actively inspect, question, follow, listen, compare, or infer.

Active investigation lowers abstraction and may reveal more, but it can also create consequences:

- time passes
- someone notices the player
- the subject reacts
- the opportunity disappears
- suspicion increases

### Perception Pipeline

```text
Objective Truth
    ↓
Observable Cues
    ↓
Player-Character Capability / Attention / Context
    ↓
Passive or Active Recognition
    ↓
Narration
```

---

## 7. Abstract Truth and Just-in-Time Concretization

The simulation should not fully construct every detail of the world before it matters.

The world may contain unresolved truths that are real but not fully specified.

Example:

```text
World truth:
- The prince was murdered.

Servant state:
- connected_to: prince_murder
- exposure: partial
- emotional_state: anxious
- knowledge_detail: unresolved
```

This is enough to justify observable cues without deciding every detail of the servant's knowledge.

If the player engages, the unresolved truth may become concrete:

```text
Concrete knowledge:
- The servant overheard Lord Veyr arguing with the prince shortly before the murder.
- The servant did not see the killing.
- The servant fears punishment if he speaks.
```

Once concretized, details become persistent canon.

### Consequence Envelope

Unresolved truths need enough constraints to produce coherent consequences.

Example:

```text
Regional thread:
- mountain_livestock_attacks
- scope: northern mountain frontier
- intensity: moderate
- apparent_cause: dragon
- actual_cause: unresolved
- public_belief: dragon
- domains affected:
  - travel danger
  - livestock loss
  - trade disruption
  - refugee movement
```

The simulation can use this to produce abstract consequences without yet deciding the exact cause.

Working rule:

> Abstract truths may drive abstract consequences. Concrete consequences require concrete causes.

---

## 8. History

History is what has happened in the world.

History is not the same as knowledge.

A city may have fallen three hundred years ago. That is history. A scholar may know the cause, a farmer may know only a legend, and a cult may believe a false version.

The engine should eventually distinguish:

- recent events
- durable facts
- unresolved threads
- summarized history
- legacy across characters

The campaign's persistent entity is the world, not any single character.

Characters may die, retire, disappear, or be replaced while the world history continues.

---

## 9. Time

Time is a primary force of world change.

Time should eventually support:

- travel duration
- delay
- decay
- healing
- recovery
- escalation
- schedule
- rumor spread
- opportunity loss
- long-term world adaptation

Time is not merely a displayed clock. It is a driver of state evolution.

---

## 10. Geography, Travel, and Scale

Geography should matter.

Distance affects:

- travel time
- information spread
- trade
- migration
- isolation
- danger
- military response
- access to opportunity

The engine does not need meter-by-meter simulation. It needs meaningful spatial relationships.

A region, journey, road, pass, settlement, or wilderness area may be enough depending on context.

Travel should eventually combine:

- intent
- destination or direction
- route plausibility
- time
- preparation abstraction
- risk
- interruption opportunity
- information contact

Routine travel can remain abstract until uncertainty or consequence makes it meaningful.

---

## 11. Routine Until Meaningful

Routine actions should remain abstract unless circumstances make them meaningful.

Examples:

- buying ordinary supplies
- retrieving a horse from a stable
- crossing a familiar street
- climbing a low fence
- eating a normal meal

These should not require micromanagement.

The simulation should bring detail forward when the routine breaks:

- supplies are scarce
- the horse is missing
- the street is under curfew
- the fence is guarded
- the food is poisoned

Working rule:

> Simulate decisions and meaningful constraints. Abstract routine bookkeeping.

---

## 12. Resolution and Uncertainty

Resolution should follow the uncertainty of the situation, not the granularity of the player's command.

Some actions are atomic:

- pick up a mug
- open an unlocked door
- step over a low obstacle

Other actions are extended situations:

- climb a cliff
- cross a desert
- investigate a murder
- negotiate a treaty
- infiltrate a castle

The engine should adjust detail according to meaningful uncertainty.

Uncertainty can increase, decrease, disappear, or reappear.

Examples:

- Interrogation may collapse into routine if the thief immediately talks.
- Buying provisions may become meaningful if supplies are unavailable.
- Climbing may become extended if weather worsens or a patrol appears.

Working rule:

> The simulation should continuously adjust its level of detail according to the current level of meaningful uncertainty.

---

## 13. Pressures and Threads

A pressure is an ongoing force pushing some part of the world in a direction.

Examples:

- winter pressure
- food shortage
- political unrest
- livestock attacks
- bandit activity
- dragon scare
- cult influence

A thread is an unresolved situation that may continue, fade, concretize, or become relevant later.

Pressures and threads should initially be represented minimally.

They should not require full simulation of every actor, resource, and consequence.

Working rule:

> Record many things briefly, promote only some into durable state, and let most decay.

---

## 14. Affordances

An affordance is what a place, object, actor, group, or situation naturally supports.

Examples:

A cave may support:

- shelter
- animal den
- temporary camp
- bandit hideout
- hidden passage
- ruins

A royal court may support:

- intrigue
- etiquette
- servants
- gossip
- alliances
- spies
- secrets

A road may support:

- travel
- trade
- ambush
- patrols
- migration
- rumors

World evolution should not invent arbitrary developments. It should select among plausible developments based on affordances, pressures, actors, time, history, and current constraints.

---

## 15. World Evolution

Phase 2 should teach the world to evolve.

World Evolution is the engine capability that answers:

> Given the current world state and the passage of time, what naturally changes?

World Evolution should prefer transformation of existing state over arbitrary invention.

Sources of change may include:

- existing actors pursuing goals
- pressures increasing or fading
- time passing
- resources changing
- relationships shifting
- knowledge spreading
- opportunity appearing through contact
- natural processes
- rare new phenomena when justified

The exact mechanism is intentionally open.

---

## 16. World Attention and Narrative Depth

The world is vast, but simulation attention is finite.

The engine should not simulate everything everywhere at the same level of detail.

Attention should consider:

- proximity
- current situation
- current journey
- relationships
- active pressures
- actor goals
- player engagement
- likely consequence
- opportunity for meaningful play

### Simulation Breadth

The world continues broadly. Distant events may progress at low detail or remain abstract until they intersect with the player, another actor, or a pressure.

### Narrative Depth

Sustained player engagement determines where the current campaign receives deeper simulation and narrative focus.

The player does not rewrite objective reality by caring about something. Engagement directs depth, not truth.

---

## 17. Player Role

The player is the protagonist of the experience, not the center of objective reality.

The player differs from other actors because their intent originates outside the simulation.

The simulation should respond to the player's chosen path and invest depth where sustained engagement shows the campaign currently lives.

The player may pursue many lives across a persistent world:

- adventurer
- courtier
- explorer
- criminal
- ruler
- merchant
- companion successor
- descendant
- unrelated new character

The world persists across character death, retirement, disappearance, or succession.

---

## 18. Player-Facing Opportunity

The engine should not generate traditional procedural quests.

Instead, opportunities should surface when the player's location, knowledge, relationships, intent, and ongoing world state intersect.

Examples:

- a rumor reaches the player through a traveler
- a blacksmith's need exposes a larger resource problem
- a refugee carries news from a distant conflict
- a companion receives a letter
- an investigation reveals a hidden connection

Opportunity should not guarantee importance, reward, or correctness.

A cave may be empty. A noble may be innocent. A rumor may be false.

---

## 19. AI Responsibilities

AI may:

- interpret natural language within simulation boundaries
- narrate known or perceived reality
- express tone and sensory detail
- phrase dialogue
- summarize routine or extended events
- present uncertainty without revealing hidden truth

AI must not:

- invent durable facts
- override objective truth
- decide success or failure when the simulation owns resolution
- reveal hidden truth as flavor
- promote ambience into canon without simulation approval
- create salient cues without grounding

Working rule:

> If something can affect future simulation, it must be represented or approved by the simulation. If something only improves present expression, the AI may generate it as narration.

---

## 20. Implemented Knowledge Membership Baseline

Static actors now have persistent current knowledge membership in World State, seeded once from immutable authored identifiers when a new game starts. Explicit engine operations may durably add an opaque knowledge identifier with a matching lifecycle history record; the causally referenced form may point structurally to one earlier accepted durable event. That reference does not establish witnessing, understanding, truth, evidence, certainty, reliability, or semantic eligibility. Knowledge remains outside dialogue content, perception, narration context, and automatic behavior. Acquisition policy, loss, propagation, and interpretation remain future work.

---

## 21. Authored Actor-Knowledge Conversation Response

One present static actor may return exact Region Pack-authored text after a
successful conversation only if it held the required opaque membership at
command start. The response repeats for later eligible conversations, creates
no player knowledge or simulation state, and is neither dialogue nor a truth,
belief, or propagation model.

---

## 22. Open Questions

The following questions are intentionally unresolved:

- How exactly does unresolved truth become concrete?
- How does world attention select which threads continue evolving?
- How should rumors, lies, and mistaken beliefs propagate?
- How should affordances be represented in data?
- How should pressures drift, decay, or escalate over time?
- How should player-facing opportunities surface without becoming procedural quests?
- How should ephemeral AI flavor be promoted into simulation state, if ever?
- How should long campaigns compress history without losing meaning?

Sprint 10.19 adds one authored, deterministic bridge from an accepted resolved conversation to opaque current actor-knowledge membership. The durable source records that the declared transition caused the membership change; it does not decide what was said, heard, understood, true, believed, or reliable. Player-facing discovery and interpretation remain separate future concerns.

These questions should be answered through future design sessions and implementation experience, not solved prematurely.

## Declared Elapsed-Time Evidence

One explicit accepted time advancement may cross one authored strict elapsed-hour threshold and create one hidden, location-bound evidence trace. It remains simulation truth until the player explicitly investigates at the matching location; it creates no continuous ticking, schedules, recurring evidence, passive cue, or automatic discovery.
