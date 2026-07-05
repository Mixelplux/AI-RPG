# Architecture

Version: 0.6.3

## Current Engine Pipeline

Player Input
↓
Interaction Kernel
↓
Interaction Result
↓
World Update
↓
World State
↓
Scene Builder
↓
Scene Snapshot
↓
Perception Builder
↓
Player Perception
↓
Narrator / UI

## Source of Truth

`world_state` is the persistent runtime source of truth for mutable state.

Currently owned by `world_state`:

- Player current location
- Current weather
- Current time

Region Packs provide static world data and initial values only.

Scene Snapshots are derived views built from Region Pack data plus `world_state`. Scene Snapshots are not persistent state.

## Completed

- Region Pack
- Scene Loader / Scene Builder
- Perception Builder
- Narrator
- Interaction Kernel
- World Update
- GameEngine
- Playable CLI Loop
- Deterministic movement
- Region validation
- Persistent player location
- Persistent weather ownership
- Persistent time ownership

## In Progress

- Persistent world state

## Architecture Boundary

Architecture describes systems that exist now or are scheduled for implementation.

Broader world-behavior ideas belong in `docs/simulation_principles.md`.

Ideas that are important but not ready for implementation belong in `docs/future_design.md`.
