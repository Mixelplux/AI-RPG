# Project Review and Simulation Design Summit Closeout

## Context

Sprint 8 is complete.

The project is not beginning Sprint 9 yet.

This review consolidates the architectural and simulation-design conclusions reached after Sprint 8 so Phase 2 can begin with a stable direction.

---

## Summit Outcome

The project vision remains stable:

- single-player
- AI-driven
- persistent world
- emergent storytelling
- canonical lore integration
- deterministic simulation beneath AI narration
- incremental sprint-driven development

The summit did not redefine the project. It clarified the next phase.

---

## Phase 1 Summary

Phase 1 established the engine's ability to represent a persistent world.

Current foundations include:

- Region Pack loading
- scene construction
- perception generation
- narration pipeline
- interaction kernel
- deterministic movement
- target resolution
- destination resolution
- deterministic skill check foundation
- persistent world state
- save/load
- session lifecycle
- CLI gameplay loop

The engine now has a stable facade and a clear boundary between persistent state and derived presentation.

---

## Phase 2 Direction

Phase 2 should be:

```text
World Evolution Foundations
```

Phase 2 should teach the world to remember and evolve.

It should not begin with combat, companions, faction warfare, economy, or full NPC AI.

---

## Accepted Outcomes

### Simulation Owns Truth

The simulation determines objective reality. AI narration expresses what the player character can perceive, hear, infer, or be told.

### Knowledge Is Not Truth

Actors may know, believe, misremember, misinterpret, rumor, or lie about things that are not objectively true.

Truth may also exist without being known.

### Persistent World Over Persistent Character

The world is the persistent entity. Player characters may die, retire, disappear, or be replaced while the world history continues.

### Narrative Depth Follows Sustained Engagement

The world continues broadly, but sustained player engagement determines where the current campaign receives deeper simulation and narrative focus.

Engagement directs depth, not objective truth.

### Routine Until Meaningful

Routine actions should be abstracted unless scarcity, risk, uncertainty, or consequence makes them meaningful.

### Resolution Follows Uncertainty

The simulation should adjust detail according to meaningful uncertainty. Some actions resolve atomically; others become extended situations.

### Affordances Guide Possibility

Places, objects, actors, groups, and situations naturally support certain kinds of developments. World evolution should select among plausible possibilities rather than invent arbitrary developments.

### Lore Seeds the World

Region Packs should begin from canonical lore where available and procedurally complete connective tissue where lore is silent.

---

## Open Questions

The following questions should remain open until later design or implementation experience:

- How does unresolved truth become concrete?
- How does world attention select which threads continue evolving?
- How should false beliefs and rumors propagate mechanically?
- How should affordances be represented in data?
- How should pressures drift, decay, or escalate?
- How should opportunities surface without becoming procedural quests?
- How should ephemeral AI flavor become canonical, if ever?
- How should long campaign history be compressed?

---

## Deferred Systems

The following should not lead Phase 2:

- combat
- full NPC AI
- companion system
- faction warfare
- economy
- full travel simulation
- detailed survival mechanics
- settlement management
- large-scale rumor networks

They should be treated as future applications of Phase 2 foundations.

---

## Recommended Next Step

Before defining Sprint 9, complete the Phase 2.0 documentation baseline:

- `docs/simulation_model.md`
- updated `docs/simulation_principles.md`
- updated `docs/roadmap.md`
- ADRs for the AI/simulation boundary and Phase 2 direction

After that, define Sprint 9 as the first small implementation sprint of Phase 2.

Recommended first implementation direction:

```text
World History Skeleton
```

Do not define that sprint until the documentation baseline is accepted.
