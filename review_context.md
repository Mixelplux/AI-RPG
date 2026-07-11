# AI Narrative RPG Engine - Phase 2B Architecture Review Record

## Review Status

Complete.

The focused architecture and scope review selected **Persistent Scoped Pressure Representation** as Sprint 10.2. Sprint 10.2 is defined and staged but implementation has not started.

## Decision

A pressure is a bounded ongoing force whose current level is mutable simulation-owned truth. Current pressure state belongs in `world_state`, not solely in history. Region Packs may contain immutable initial pressure seeds. New-game construction validates and deep-copies those seeds into persistent state; loading uses persisted state.

The first capability is representation-only. It uses a dedicated pressure model rather than combining pressures with unresolved threads, quests, conditions, opportunities, or a generic ongoing-condition framework.

## Initial Boundary

- Persistent storage: `world_state.pressures`, a dictionary keyed by stable `pressure_id`.
- Supported scopes: region and location.
- Region Pack seed field: exact optional top-level `initial_pressures` list; absence means no seeds.
- Supported provenance: `region_pack` with `source_id` exactly equal to the containing `region_id`.
- Level: integer from 0 through 100; booleans rejected.
- Read boundary: exact defensive-copy methods `GameEngine.get_pressures()` and `GameEngine.get_pressure(pressure_id)`, returning `None` when unknown.
- CLI boundary: required `pressures` command routed through `get_pressures()` without direct durable-state access.
- Legacy saves: during loading only, copied version-1 data missing pressure state normalizes to an empty dictionary before strict runtime validation and is not retroactively seeded; malformed present values fail.
- Save version: preserve version 1.

## Deferred Work

Pressure mutation, pressure-change history, event-driven change, time drift, world ticks, scene/perception/narration projection, AI-created pressures, unresolved threads, actor state and knowledge, evidence, consequences, opportunities, quests, travel execution, combat, economy, and faction simulation remain outside Sprint 10.2.

## Repository State at Staging Start

- Branch: `main`
- Starting HEAD: `be799540c2d6688cf10e6b46c8a6e270c0e7bd5c`
- Starting working tree: clean
- Latest product sprint: Sprint 10.1, complete at `5feb28ed2de47334189458747ae1d597e4ba79d8`
- Latest maintenance task: ENV-HARDENING-001, complete at starting HEAD

## Next Activity

Run the mandatory Startup Review, then implement only Sprint 10.2 from the synchronized canonical manifests. Do not define or begin Sprint 10.3.
