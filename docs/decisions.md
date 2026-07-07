# Architecture Decisions

## ADR-006

**Title:** GameEngine Orchestrates Engine Layers

**Status:** Accepted

Gameplay front ends interact with GameEngine instead of individual engine layers.

---

## ADR-007

**Title:** Interaction Result Is the Simulation Interface

**Status:** Accepted

The Interaction Kernel converts player language into structured actions consumed by the simulation.

---

## ADR-008

**Title:** World Attention Budget Guides Future Consequence Systems

**Status:** Accepted

The world should not react to every player action. Player actions may leave evidence or unresolved threads, but only evidence that intersects with actor goals, proximity, world pressures, faction interests, danger or value, narrative opportunity, or current simulation needs should become active.

This decision preserves emergent storytelling while avoiding the impossible task of simulating every minor action.

See also: `docs/simulation_principles.md` and `docs/future_design.md`.

---

## ADR-009

**Title:** Region Packs Validate on Engine Startup

**Status:** Accepted

GameEngine validates Region Packs during initialization and fails fast if any connected location references are invalid. Placeholder locations are preferred over removing intended world connectivity during early development.

---

## ADR-010

**Title:** World State Owns Runtime Weather

**Status:** Accepted

Region Pack weather is an initial value, not runtime state.

During engine startup, initial weather is copied into `world_state.weather`. Scene Builder reads weather from `world_state.weather` when building Scene Snapshots.

This keeps mutable world-level state in one persistent runtime object without introducing weather simulation, clocks, seasons, random weather, save/load, or additional persistence systems.

---

## ADR-011

**Title:** World State Owns Runtime Time

**Status:** Accepted

Region Pack time is an initial local value, not runtime state.

During engine startup, initial time is copied into `world_state.time`. Scene Builder reads time from `world_state.time` when building Scene Snapshots.

This keeps mutable runtime state in one persistent object without introducing clock advancement, calendar simulation, schedules, NPC routines, or realm-level world files prematurely.


---

## ADR-012

**Title:** Save Files Persist World State Only

**Status:** Accepted

Save files serialize only World State. Region Packs are immutable assets. Scene Snapshots, Player Perception, and Narration are regenerated after load.

---

## ADR-013

**Title:** GameSession Owns Session Lifecycle

**Status:** Accepted

`GameSession` constructs new, loaded, and reset gameplay sessions. `GameEngine` remains the public gameplay orchestration facade and delegates lifecycle construction to the session layer.
