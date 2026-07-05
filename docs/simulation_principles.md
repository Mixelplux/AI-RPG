# Simulation Principles

This document defines how the simulated world should make decisions.

These principles guide design direction. They are not implementation requirements until a sprint explicitly schedules them.

---

## Principle Status Levels

Use these labels to keep important ideas without prematurely building systems.

- **Idea:** Worth keeping, not yet accepted as a project rule.
- **Principle:** Accepted as design direction.
- **Approved:** Ready to influence architecture when a sprint needs it.
- **Scheduled:** Assigned to a current or future sprint.
- **Implemented:** Represented in code and tests.

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
- current simulation needs

This prevents the world from feeling scripted while also avoiding the impossible task of simulating every minor action.

### Design Use

Use this principle when discussing delayed consequences, investigation, rumors, witnesses, faction response, discovery, or world-state escalation.

Do not add evidence fields, thread systems, attention scores, or investigation logic until a sprint requires them.

### Example

The player steals an object from an isolated shack.

The world does not automatically start a quest or response.

A response becomes possible only if someone later has a reason and opportunity to notice the missing object, care about it, connect it to the player, and act on that knowledge.

---

## Evidence Before Consequence

**Status:** Idea

Consequences should usually arise from evidence, witnesses, memory, or world pressure rather than direct authorial reaction.

The simulation should prefer: player action creates a trace, an actor encounters the trace, the actor interprets it, then the actor responds.

This principle supports emergent consequences without making the world feel omniscient.

---

## Locality of Knowledge

**Status:** Idea

NPCs and factions should not know things simply because they happened in the simulation.

Knowledge should spread through perception, reports, rumors, travel, investigation, magic, or other plausible channels.

---

## Bounded Simulation

**Status:** Principle

The engine should simulate enough of the world to create believable play, but not attempt full reality.

Systems should be scoped around what improves play, supports emergence, and remains testable.
