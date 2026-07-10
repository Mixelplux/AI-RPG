# Architecture

Version: 0.9.8

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
- World history entries

Region Packs provide static world data and initial values only.

Scene Snapshots are derived views built from Region Pack data plus `world_state`. Scene Snapshots are not persistent state.



## Simulation Model Boundary

`docs/simulation_model.md` describes how the world should conceptually behave. It is the behavioral counterpart to this architecture document.

Architecture describes implemented or scheduled software structure.

Simulation model describes conceptual world behavior such as truth, knowledge, pressures, affordances, time, perception, routine abstraction, and AI responsibility.

Concepts in `docs/simulation_model.md` do not become implementation requirements until scheduled by a sprint.

## Phase 2 Direction

After Sprint 8, the recommended next major phase is World Evolution Foundations.

Phase 1 established world representation. Phase 2 should establish the minimum structures required for the world to remember, evolve, and present meaningful opportunities without relying on AI invention.

Major feature systems such as combat, companions, economy, and faction warfare are deferred until the underlying world-evolution foundations exist.

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
- Durable world history skeleton
- Explicit time advancement operation
- Read-only world history query
- Bounded history query defaults
- Stable history entry identity
- Bounded history context packet
- Narration context boundary
- Narration output contract
- Deterministic structured skill checks
- Structured skill-check command routing
- Scene-bound target resolution

## In Progress

- Persistent world state

## Architecture Boundary

Architecture describes systems that exist now or are scheduled for implementation.

Broader world-behavior ideas belong in `docs/simulation_principles.md`.

Ideas that are important but not ready for implementation belong in `docs/future_design.md`.


## Persistence

Only `world_state` is persisted. Region Packs remain immutable assets. Scene Snapshots, Perception, and Narration are regenerated after loading.

`GameEngine` exposes save and load operations to gameplay front ends. Persistence serialization and reconstruction remain implemented by the save system behind that engine API.

`world_state.history` stores durable records of events the simulation has accepted as having happened. Each new history entry receives a stable `history_id`, plus an event type and summary, with location and time recorded when available. History identifiers are assigned by the engine when the entry is created, stored directly on the durable entry, and preserved through save/load. Loading a save must not regenerate existing history identifiers.

History is persistent world state; scene snapshots, perception, and narration remain derived views and do not own history truth. History identifiers make accepted events referenceable by future systems, but they do not interpret history, summarize history, or turn durable history into active memory.

History can be queried through a read-only `GameEngine` facade by recent count, event type, and location. A single history entry can also be looked up by `history_id` through a narrow read-only `GameEngine` facade. Querying or looking up history returns existing durable entries without mutating `world_state.history`, advancing time, creating history entries, or triggering world evolution.

Normal history access is bounded by default using a single safe recent-entry count. Plain CLI history review and filtered history review use this bounded query path unless an explicit smaller or larger count is provided through a supported command. Durable history remains persisted simulation truth, but it is not active memory and should not be passed casually into narration or future simulation context.

`GameEngine.get_history_context(...)` exposes a deterministic, read-only, bounded history context packet for future handoff boundaries. Sprint 9.6 packet shape is:

- `schema`: `ai_rpg.history_context_packet`
- `version`: `1`
- `limit`: the bounded entry limit used for the packet
- `default_limit`: the normal safe history-query default
- `max_limit`: the maximum supported history-context count
- `current_time`: a copy of current durable world time
- `player.current_location_id`: current player location from durable world state
- `history_entries`: bounded recent accepted history entries, including stable `history_id` values

The context packet defaults to the same safe recent history count as normal bounded history queries and rejects explicit counts above its documented maximum. It never returns full durable history by default. Included entries preserve existing event type, summary, location, time, and other accepted entry fields without interpretation, summarization, relevance scoring, or AI narration. The packet is a copy-safe handoff structure; callers cannot mutate durable `world_state.history` through it.

`GameEngine.get_narration_context(...)` exposes a deterministic, read-only narration context packet for future narration handoff boundaries. Sprint 9.7 packet shape is:

- `schema`: `ai_rpg.narration_context_packet`
- `version`: `1`
- `player_input`: the raw player input supplied for context construction
- `current_time`: a copy of current durable world time
- `player.current_location_id`: current player location from durable world state
- `scene_snapshot`: a copy of the current derived scene snapshot
- `history_context`: the bounded Sprint 9.6 history context packet
- `boundary`: the read-only narration input rule and drift guardrail

The narration context packet defines what a future narrator may see. It is not narration output, not an AI call, not simulation authority, and not world evolution. Building the packet does not advance time, create history entries, alter history identifiers, summarize history, reinterpret events, rank relevance, or mutate durable world state.

Future narration may use known scene facts for grounded atmospheric description, but atmospheric prose must not become durable world truth unless the engine records it. For example, if the scene contains a blizzard, narration may describe cold weather, but may not mention the player's gloves unless gloves are present in player state or context. The narrator can describe; the engine decides what is true.

`GameEngine.validate_narration_output(...)` exposes a deterministic, read-only contract for future narration output. Sprint 9.8 packet shape is:

- `schema`: `ai_rpg.narration_output_packet`
- `version`: `1`
- `narration_text`: presentational prose string
- `contract`: a copy of the narration output contract, including authority and drift limits

The narration output contract defines what a future narrator may return before any AI model is called. It accepts only schema/version metadata and a `narration_text` string, then returns a copy-safe packet with contract metadata. It rejects unsupported structured fields and structured attempts to mutate world state, mutate history, advance time, create quests, create rumors, create pressures, update actor knowledge, add NPC schedules, add evidence, add consequences, add entities, add locations, add exits, alter inventory, add player conditions, or update NPC relationship state.

Narration output is presentational prose only. It is not accepted world truth, not simulation authority, not history, not time advancement, not world evolution, and not AI integration. Validating narration output does not mutate durable world state, advance time, create history entries, alter history identifiers, call an AI model, or make freeform prose durable.

This contract is structural rather than semantic. It does not attempt to fully prove whether freeform narration contains invented details. Freeform narration drift is controlled by context limits, prompt rules, this output contract, and later review or validation layers. For example, narration may describe a blizzard if the context contains a blizzard, but should not mention gloves unless gloves are present in context. Narration output may be shown later, but it is not accepted world truth.

`world_state.time` can be advanced by an explicit simulation-owned operation. Sprint 9.2 supports a narrow fixed-duration `wait` command that increments durable elapsed time by one hour and records the previous and new time in history. This operation does not trigger world evolution, pressures, schedules, travel duration, recovery, decay, escalation, opportunity loss, or autonomous NPC behavior.

## Session Lifecycle

`GameSession` owns construction of new, loaded, and reset gameplay sessions. `GameEngine` remains the gameplay-facing orchestration facade and delegates lifecycle construction to the session layer.


## Command Routing

Player-facing commands should enter through the existing gameplay command path. The Interaction Kernel converts supported player input patterns into structured interaction results. `GameEngine` remains responsible for routing those results to the appropriate engine behavior.

Sprint 8.2 extends this principle to explicit skill-check commands. The CLI may display skill-check results, but it must not bypass `GameEngine` by calling `engine.skill_check` directly.

Sprint 9.2 extends this principle to the explicit `wait` command. The Interaction Kernel recognizes the narrow command shape, and `GameEngine` performs the time advancement through the gameplay-facing facade.

Sprint 9.3 exposes narrow history review commands through the CLI, while keeping the query behavior behind the `GameEngine` facade. Front ends may request recent, event-type, or location-filtered history, but they do not interpret history or mutate history internals.

Sprint 9.4 requires normal history review paths to use bounded query defaults. Full durable history access may remain available for internal inspection, but it is not the default gameplay or CLI review path.

Sprint 9.5 adds stable history entry identity. The CLI may expose a narrow `history id <history_id>` review command, but front ends still do not assign, alter, reinterpret, or mutate history identifiers.

Sprint 9.6 adds a narrow `history context` review path for the bounded history context packet. Front ends may display the packet for manual review, but they must not treat it as full memory, reinterpret history, summarize history, omit identifiers, or trigger world evolution.

Sprint 9.7 adds a narrow `narration context <player input>` review path for the narration context packet. Front ends may inspect the packet for debugging, but they must not treat it as final narration, create durable facts from atmospheric prose, call an AI model, validate generated narration, add equipment or exposure mechanics, or trigger world evolution.

Sprint 9.8 adds a narrow `narration output` review path for the narration output contract and fixed sample validation. Front ends may inspect the contract or confirm that a structured mutation sample is rejected, but they must not call an AI model, generate final AI narration, replace existing gameplay output with narration output, create durable facts from prose, implement semantic prose analysis, or trigger world evolution.

## Skills

The skill system begins with deterministic check resolution. `engine.skill_check` returns structured results containing the check name, target difficulty, deterministic result value, and success state. `GameEngine.perform_skill_check` is the gameplay-facing entry point.

Skill-check commands should be routed through the normal command-processing flow. The Interaction Kernel may identify explicit skill-check command patterns and produce structured interaction results; `GameEngine` then resolves the check.

The current implementation does not include dice rolling, character progression, inventory modifiers, combat rules, broad natural-language parsing, or AI adjudication. Front ends depend on `GameEngine`, not the lower-level skill-check module.


## Target Resolution

Target resolution is a deterministic support layer between parsed player intent and simulation behavior. Its first scope is current-scene resolution only: visible entities and available exits.

The resolver should answer what current-scene thing the player appears to be referring to, not decide whether an action succeeds, perform travel, search off-scene locations, consult NPC memory, or invoke AI interpretation.

`GameEngine` remains the gameplay-facing facade. Front ends should not call lower-level target-resolution modules directly.

Sprint 8.3 introduces this layer narrowly so future systems such as conversation, examination, interaction, and destination travel can share one deterministic target-resolution boundary.


## Destination Resolution

Destination resolution is a deterministic support layer for player commands that refer to places, such as "head to the blacksmith" or "go to the inn".

Sprint 8.4 scopes this layer to identifying known locations from loaded region data. Destination resolution produces structured results that say whether a destination was resolved, ambiguous, or unknown.

Destination resolution does not execute travel. It must not move the player, calculate a route, perform fast travel, advance time, trigger encounters, or narrate a journey. Those behaviors belong to later travel and world-simulation systems.

`GameEngine` remains the gameplay-facing facade. Front ends should not call lower-level destination-resolution modules directly.
