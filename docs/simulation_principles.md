# Simulation Principles

This document defines high-level principles for how the simulated world should behave.

These principles guide design direction. They are not implementation requirements until a sprint explicitly schedules them.

Detailed world-behavior modeling belongs in `docs/simulation_model.md`.

---

## Principle Status Levels

Use these labels to keep important ideas without prematurely building systems.

- **Idea:** Worth keeping, not yet accepted as a project rule.
- **Principle:** Accepted as design direction.
- **Approved:** Ready to influence architecture when a sprint needs it.
- **Scheduled:** Assigned to a current or future sprint.
- **Implemented:** Represented in code and tests.

---

## Bounded Simulation

**Status:** Principle

The engine should simulate enough of the world to create believable play, but not attempt full reality.

Systems should be scoped around what improves play, supports emergence, and remains testable.

The engine should favor meaningful change over exhaustive detail.

---

## Simulation Owns Truth

**Status:** Principle

The simulation determines objective reality.

AI narration may express, summarize, dramatize, or clarify what the player character can perceive, but it must not invent persistent facts, override simulation truth, or decide reality because it would be convenient for pacing or drama.

The AI performs the expressive role of a tabletop DM, not the authority-over-reality role.

### Design Use

Use this principle when discussing AI narration, dialogue, hidden information, action resolution, and persistent world state.

---

## Knowledge Is Not Truth

**Status:** Principle

The world may contain truth without knowledge, and knowledge without truth.

Actors may believe things that are false, incomplete, outdated, inferred, rumored, mythologized, or deliberately deceptive.

Rumors, lies, myths, public beliefs, and mistaken interpretations may produce real consequences without being objectively true.

### Examples

- A dragon lairs in distant hills, but no one knows it yet.
- Villagers believe a dragon is killing livestock, but a secret group is staging the attacks.
- A story says the abandoned keep contains treasure, but the treasure may be gone, false, misunderstood, or real.

---

## Locality of Knowledge

**Status:** Principle

NPCs and factions should not know things simply because they happened in the simulation.

Knowledge should spread through plausible channels such as perception, reports, rumors, travel, investigation, records, magic, inference, or direct communication.

### Design Use

Use this principle when discussing witnesses, secrets, rumors, false belief, investigation, NPC dialogue, faction response, and delayed consequence.

### Implementation Note

Sprint 10.16 establishes persistent membership of authored knowledge identifiers for stable static actors. It does not yet implement any channel that changes or projects that membership.

---

## Evidence Before Consequence

**Status:** Principle

Consequences should usually arise from evidence, witnesses, memory, knowledge, or world pressure rather than direct authorial reaction.

The simulation should prefer:

```text
player action
    ↓
evidence / trace / memory
    ↓
discovery or interpretation
    ↓
response
```

This principle supports emergent consequences without making the world feel omniscient.

---

## World Attention Budget

**Status:** Principle

The world cannot react to everything, so it should spend its attention where the greatest combination of plausibility, consequence, and opportunity exists.

Player actions may create evidence, traces, or unresolved threads, but most evidence fades without consequence.

Evidence should only become active when it intersects with one or more meaningful pressures:

- actor goals
- proximity
- world events
- faction interests
- danger or value
- narrative opportunity
- player engagement
- current simulation needs

This prevents the world from feeling scripted while also avoiding the impossible task of simulating every minor action.

### Design Use

Use this principle when discussing delayed consequences, investigation, rumors, witnesses, faction response, discovery, world-state escalation, and simulation scope.

Do not add evidence fields, thread systems, attention scores, or investigation logic until a sprint requires them.

---

## Narrative Depth Follows Sustained Engagement

**Status:** Principle

The world continues broadly, but sustained player engagement determines where the current campaign receives deeper simulation and narrative focus.

Player engagement does not rewrite objective reality. It directs discovery, attention, and depth, not truth.

### Example

If the player spends months investigating a royal murder, the court intrigue should receive more depth than unrelated events far away. Those distant events may still continue, but they should not compete equally for the current campaign's focus.

---

## Persistent World Over Persistent Character

**Status:** Principle

The persistent entity is the world, not any individual player character.

Characters may die, retire, disappear, ascend, be imprisoned, or be replaced while the world history continues.

A campaign may span multiple protagonists, descendants, companions, successors, or unrelated new characters while preserving the consequences of earlier characters.

---

## Routine Until Meaningful

**Status:** Principle

Routine actions should remain abstract unless circumstances make them meaningful.

The simulation should not force the player to micromanage mundane logistics unless a constraint, risk, uncertainty, scarcity, or consequence makes those details important.

### Examples

- Retrieving a stabled horse can be summarized unless the horse is missing, injured, stolen, unavailable, or socially contested.
- Buying supplies can be summarized unless supplies are scarce, expensive, dangerous, restricted, or inadequate for the intended journey.
- Climbing a low fence can be narrated unless guards, injury, noise, time pressure, or other uncertainty matters.

---

## Resolution Follows Meaningful Uncertainty

**Status:** Principle

The simulation should adjust its level of detail according to the current level of meaningful uncertainty.

Some actions are atomic and can resolve immediately. Others are extended situations that unfold through new information, changing risk, and additional decisions.

Uncertainty can increase, decrease, disappear, or reappear.

### Design Use

Use this principle when discussing skill checks, stealth, travel, investigation, negotiation, climbing, infiltration, and other actions where success may involve multiple kinds of uncertainty.

---

## Affordances Guide Possibility

**Status:** Principle

Places, objects, actors, groups, and situations naturally support certain kinds of interactions, occupants, and developments.

World evolution should select among plausible possibilities based on affordances, pressures, actors, time, history, and current constraints rather than inventing arbitrary developments.

### Examples

- A cave may plausibly support shelter, animal dens, bandit hideouts, hidden passages, or ruins.
- A royal court may plausibly support intrigue, etiquette, gossip, alliances, secrets, and spies.
- A road may plausibly support trade, travel, ambush, patrols, migration, and rumors.

---

## Moral Agency and Narrative Restraint

**Status:** Principle

The simulation does not impose a universal morality score on player actions.

Actions should be evaluated through the perspectives of cultures, factions, laws, beliefs, and individual actors within the world.

Players may roleplay a wide range of characters, including antagonistic or villainous ones, within the intended scope of the game experience.

However, narration should emphasize outcomes, consequences, and meaning rather than gratuitous or graphic depiction of harm.

---

## World Initialization From Lore

**Status:** Principle

The player enters an existing world; they do not cause it to begin.

A region should begin in a plausible, fully realized state derived from canonical lore where available and procedurally completed where necessary.

Lore provides anchor points, constraints, major truths, important people, historical events, and significant places. The engine may complete connective tissue where lore is silent.

This is procedural completion, not arbitrary procedural generation.

---

## Open Design Questions

The following ideas are important but not fully settled:

- how abstract truths become concrete
- how pressures drift over time
- how world attention is applied in practice
- how false beliefs and rumors propagate mechanically
- how player-facing opportunities surface without becoming procedural quests
- how long campaigns compress history while preserving meaning

These questions should remain open until implementation experience gives better evidence.
