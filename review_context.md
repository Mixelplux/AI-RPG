# AI Narrative RPG Engine - Next Review Context

## Review Purpose

Conduct a focused architecture and scope review for the next Phase 2B capability before defining Sprint 10.2.

The leading candidate is persistent scoped pressures or unresolved threads. This is a candidate only; Sprint 10.2 has not been defined or started.

## Repository Status

- Completed sprint: Sprint 10.1 - Persistent Resolved Conversation Memory
- Sprint status: Complete and closed out
- Git status: Working tree is not clean
- Commit hash: `5feb28ed2de47334189458747ae1d597e4ba79d8`
- Active development sprint: None
- Sprint 10.2 status: Not defined or started

## Current Phase

- Sprint 9 milestone: World Memory and Safe Narration Foundations
- Current phase: Phase 2B - Reactive World State Foundations
- Completed Phase 2B capability: Persistent resolved conversation memory
- Leading next capability: Persistent scoped pressures or unresolved threads

## Sprint 10.1 Outcome

A successful conversation with a deterministically resolved current-scene entity now creates exactly one durable world-history event.

The event uses:

- `event_type`: `player_conversation`
- Existing engine-owned `history_id`
- Deterministic summary
- Current player location
- Current durable time
- Stable `target_entity_id`
- Resolved `target_display_name`

Stable target identity comes from deterministic current-scene target resolution, not raw player input.

Failed, unresolved, ambiguous, and non-actor conversation targets create no history. Repeated accepted conversations create distinct events with distinct history identifiers.

## Deliberate Sprint 10.1 Limits

The durable event records only that conversation was initiated. It does not establish:

- Dialogue content or topics
- Claims or promises
- Actor knowledge or beliefs
- Relationships, trust, disposition, or emotional state
- Consequences or evidence
- Pressures or unresolved threads
- Rumors, quests, schedules, or opportunities
- Time advancement

Sprint 10.1 added no top-level `world_state` field and did not change the save version.

## Sprint 10.1 Files

Created:

- `test_interaction_history.py`

Modified for implementation:

- `engine/world_update.py`

Updated during closeout:

- `docs/architecture.md`
- `docs/decisions.md`
- `docs/roadmap.md`
- `docs/sprint_log.md`
- `docs/next_chat_handoff.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`

`engine/game_engine.py` and `engine/target_resolver.py` required no changes because the existing command path already supplied successful resolution status, target kind, stable identity, and display name before world update.

## Verification Record

The following focused checks passed:

- `test_interaction_history.py`
- `test_history_query.py`
- `test_history_context.py`
- `test_narration_context.py`
- `test_save_load.py`
- `test_narration_pipeline.py`
- Canonical sprint JSON validation
- Canonical JSON/YAML parsing and exact deep comparison

The scripted smoke flow covered:

- Starting at the Bryn Shander North Gate
- Resolving `talk to captain` to Captain Darvin Grey
- Creating and querying `player_conversation` history
- Repeated conversations with distinct history identifiers
- No-history behavior for unresolved, ambiguous, and non-actor targets
- Save/load preservation and post-load history-ID continuity
- No conversation-driven movement or time advancement
- Movement, waiting, destination resolution, skill checks, narration preview, reset, and quit

The CLI launch rendered the opening scene successfully. It then reached `EOFError` at the input prompt because the verification terminal was non-interactive.

## Accepted Architecture Decisions

ADR-035 - Resolved Conversations Become Durable Accepted Events:

- A conversation becomes durable only after the normal gameplay path accepts it and deterministic current-scene target resolution identifies an entity.
- The event records occurrence and grounded target identity only.
- Failed, unresolved, ambiguous, and non-actor targets do not create history.
- The event does not establish dialogue, knowledge, beliefs, relationships, promises, consequences, or emotional state.
- Conversation does not advance time or grant narration authority.

Existing governing principles remain in force:

- The simulation owns truth.
- World state owns persistent mutable runtime truth.
- Region Packs are immutable authored assets unless a later bounded decision explicitly migrates a field into runtime state.
- Narration is presentational and non-authoritative.
- Untrusted and future provider-facing boundaries fail closed.
- Provider integration remains deferred until there is a bounded consumer.

## Implemented Foundations Relevant to the Review

- Region Packs and region validation
- Scene construction and player perception
- Interaction Kernel and GameEngine gameplay facade
- GameSession lifecycle and save/load
- Persistent player location, weather, time, and history
- Explicit simulation-owned time advancement
- Stable engine-owned history identifiers
- Read-only and bounded history queries
- History lookup by identifier
- Bounded history and narration contexts
- Scene-bound target resolution
- Known-destination resolution without travel execution
- Persistent resolved conversation memory
- Fail-closed narration request, prompt, source-result, output, and preview boundaries

## Known Architectural Questions

The next review should determine:

1. Whether the next capability should model pressures, unresolved threads, or one deliberately narrow combined concept.
2. Whether the first implementation should be representation-only or include one explicit deterministic state-change operation.
3. What minimum identity, scope, state, status, and provenance fields are required.
4. Whether scope should initially be limited to a location or region rather than actors, factions, or arbitrary targets.
5. Whether history identifiers should provide provenance for creation and later changes.
6. Whether definitions should be authored in Region Packs, created at runtime, or support a bounded combination of both.
7. How a new persistent collection should initialize for existing saves.
8. Whether the existing save version can remain unchanged.
9. Whether pressure or thread state should remain query-only initially or appear in scene, perception, or narration context.
10. Whether mutable-looking Region Pack fields such as economy, security, population, entity state, and faction objectives can remain untouched.
11. Which layer should own construction, mutation, queries, and gameplay orchestration.
12. Whether any current documentation or technical debt materially blocks the first bounded capability.

## Candidate Approaches

The architecture review should compare:

- Persistent pressure representation only
- Persistent unresolved-thread representation only
- One combined minimal ongoing-condition structure
- Representation plus one explicit deterministic change operation
- Connecting one existing accepted event directly to a pressure
- Delaying pressure work to establish runtime actor or regional-state ownership first

For each serious option, assess prerequisites, persistence and save/load effects, coupling risk, premature abstraction risk, player-facing value, testability, sprint size, and the next concrete consumer it enables.

## Review Boundaries

Do not:

- Define or begin Sprint 10.2 before completing the review
- Modify code or project documentation during the review
- Add an AI provider or AI-generated pressures
- Add autonomous global simulation sweeps
- Add faction warfare, economy simulation, schedules, rumor networks, quests, or opportunity generation
- Migrate all mutable-looking Region Pack data into world state
- Introduce a generic event bus, rule engine, plugin framework, or world-simulation framework
- Redesign durable history
- Assume pressure drift belongs in the first capability

## Recommended Review Output

The review should provide:

1. Executive assessment
2. Confirmation or rejection of pressure/thread work as the next direction
3. Persistence and state-ownership analysis
4. Candidate comparison
5. Recommended terminology and first capability
6. Proposed minimal persistent data shape
7. Initialization and save/load compatibility approach
8. GameEngine and lower-layer ownership recommendation
9. Decision on representation-only versus one mutation operation
10. Explicit non-goals
11. Technical risks and debt
12. Verification strategy
13. Short future capability sequence
14. Decision on whether Sprint 10.2 should be defined
15. Final decision statement suitable for project documentation

## Suggested Packet Contents

This file is the front page of the architecture review packet. The packet should also include the canonical project documents, relevant persistence and orchestration modules, focused tests, and representative region data listed in its manifest.

At minimum, include:

- `AGENTS.md`
- `PROJECT.md`
- `WORKFLOW.md`
- `TASK.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`
- `docs/next_chat_handoff.md`
- `docs/architecture.md`
- `docs/decisions.md`
- `docs/roadmap.md`
- `docs/sprint_log.md`
- `docs/simulation_model.md`
- `docs/simulation_principles.md`
- `docs/future_design.md`
- `docs/project_structure.md`
- `engine/world_state.py`
- `engine/world_update.py`
- `engine/game_engine.py`
- `engine/save_system.py`
- `engine/game_session.py`
- `engine/timekeeper.py`
- `engine/history_context.py`
- `engine/narration_context.py`
- `engine/interaction_kernel.py`
- `engine/target_resolver.py`
- `engine/scene_loader.py`
- `engine/region_validator.py`
- `play_game.py`
- `test_interaction_history.py`
- `test_history_query.py`
- `test_history_context.py`
- `test_save_load.py`
- `test_narration_context.py`
- `test_narration_pipeline.py`
- `data/regions/bryn_shander.json`

## Final Handoff Statement

Sprint 10.1 is complete, closed out, and committed. The working tree is not clean at the moment of this packet because `WORKFLOW.md` has local changes and this review packet file is new. Sprint 10.1 established durable memory for successful conversations with deterministically resolved current-scene entities while deliberately avoiding dialogue, actor-state, consequence, pressure, and provider work. Phase 2B is active, but Sprint 10.2 has not been defined or started. The next activity is a focused architecture and scope review of persistent scoped pressures or unresolved threads.
