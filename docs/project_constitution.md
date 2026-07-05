# Project Constitution

## Project Vision

Build a single-player AI-driven narrative RPG that recreates the experience of playing with an exceptional tabletop Dungeon Master.

The project emphasizes:

* Emergent storytelling
* A persistent, simulated world
* Natural language interaction
* Canonical lore as the foundation
* AI-assisted narration
* Story before mechanics

---

# Core Principles

## 1. Simulation Determines Truth

The simulation defines reality.

The narrator only describes reality.

---

## 2. The World Exists Independently of the Player

Time passes.

NPCs continue living.

Weather changes.

Trade continues.

The player participates in the world but is not its center.

---

## 3. Simulation Principles Are Design Commitments

Simulation principles describe how the world should behave before those ideas become code.

They guide design direction but do not imply implementation until scheduled in a sprint.

Detailed principles belong in `docs/simulation_principles.md`.

---

## 4. Canon Is the Foundation

Canonical lore is considered true until altered by simulation or player action.

AI must never invent or contradict established canon without explicit project direction.

---

## 5. Player Perception Is Limited

The player only receives information that could reasonably be perceived.

Hidden information never reaches the narrator.

---

## 6. Small Vertical Slices

Every sprint must produce something runnable.

Avoid expanding systems until the previous system works.

---

## 7. Stable Layers

The engine is built from independent layers.

Region Pack
↓
Scene Loader
↓
Scene Snapshot
↓
Perception Builder
↓
Narrator
↓
Player

Each layer consumes one object and produces one object.

---

## 8. No Premature Systems

Do not introduce new systems unless implementation proves they are necessary.

Combat, romance, quests, factions, economy, etc. are added only when required.

---

## 9. Repository Is The Source Of Truth

The repository stores:

* documentation
* architecture
* code
* data

Chats assist development but are never considered permanent project memory.
