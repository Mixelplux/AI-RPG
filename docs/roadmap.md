# Roadmap

## Completed Foundation

- Sprint 1 ✅ Foundation
- Sprint 2 ✅ Perception
- Sprint 3 ✅ Narrator
- Sprint 4 ✅ Interaction
- Sprint 5 ✅ Simulation
- Sprint 6 ✅ Character / Engine Stabilization
- Sprint 7 ✅ Save / Load and Session Lifecycle
- Sprint 8 ✅ Skills, Target Resolution, and Destination Resolution
  - Sprint 8.1 — Deterministic Skill Check Foundation ✅
  - Sprint 8.2 — Structured Skill Check Command Routing ✅
  - Sprint 8.3 — Current-Scene Target Resolution ✅
  - Sprint 8.4 — Destination Resolution ✅

---

## Current Transition

Sprint 8 is complete.

Sprint 9 is not yet defined.

The project is currently in a post-Sprint-8 review and Phase 2 design transition.

---

## Phase 2 — World Evolution Foundations

### Goal

Establish the minimum simulation structures required for the world to remember, evolve, and present meaningful opportunities without relying on AI invention.

Phase 1 taught the engine to represent the world.

Phase 2 should teach the engine to evolve the world.

---

## Phase 2.0 — Simulation Model Baseline

**Status:** Recommended before Sprint 9

Purpose:

- Create `docs/simulation_model.md`.
- Update `docs/simulation_principles.md`.
- Record ADRs that protect the AI/simulation boundary and Phase 2 direction.
- Preserve summit outcomes without beginning implementation prematurely.

No implementation code should be generated during Phase 2.0 unless a later sprint explicitly schedules it.

---

## Candidate Phase 2 Implementation Sequence

This sequence is directional, not a sprint commitment.

Each sprint should introduce one durable concept, one narrow behavior, and one verification path.

### 2.1 — World History Skeleton

Capability:

- The world can record that something happened.

Possible scope:

- player action creates a history entry
- history persists through save/load
- no autonomous world evolution yet

### 2.2 — Time Advancement as Operation

Capability:

- Time can advance intentionally and be recorded.

Possible scope:

- wait-like or travel-like command advances time
- history records when events occur
- save/load preserves time

### 2.3 — Abstract Threads / Pressures Skeleton

Capability:

- The world can track an unresolved or ongoing condition.

Possible examples:

- winter pressure
- local unrest
- missing caravan
- livestock attacks

Initial scope should be representation only. No global simulation sweep.

### 2.4 — Pressure Change Through Player Action

Capability:

- Player action can change a local or scoped pressure.

Possible examples:

- reduce local danger
- worsen local suspicion
- increase unrest

### 2.5 — Time-Based Pressure Drift

Capability:

- Some pressures can decay, intensify, or remain stable when time passes.

Initial scope should be narrow and explicitly modeled.

### 2.6 — Knowledge / Belief Skeleton

Capability:

- The engine distinguishes objective truth from known, believed, rumored, or false information.

Initial scope should support simple public belief or actor knowledge without full rumor propagation.

### 2.7 — Affordance Baseline

Capability:

- Locations or entities can express what kinds of developments they plausibly support.

Initial scope should be representational, not generative.

### 2.8 — Player-Facing Opportunity Surfacing

Capability:

- Relevant world state can surface to the player when it intersects with location, knowledge, relationship, and sustained engagement.

This is not procedural quest generation.

---

## Deferred Systems

The following systems remain important but should not lead Phase 2:

- combat
- full NPC AI
- companion systems
- faction warfare
- economy simulation
- full travel simulation
- detailed survival mechanics
- settlement management
- large-scale rumor networks
- procedural quest generation

These are future applications of Phase 2 foundations, not the foundations themselves.

---

## Sprint Rule

Active sprint definitions must include:

- Goal
- Expected Files
- Acceptance Criteria
- Verification

Do not begin the next sprint automatically.
