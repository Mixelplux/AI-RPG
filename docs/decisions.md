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

---

## ADR-014

**Title:** Skill Checks Start Deterministic

**Status:** Accepted

Sprint 8 skill checks begin as deterministic structured checks. The first implementation should establish the interface and routing path before adding dice randomness, character advancement, proficiency, equipment modifiers, combat integration, or AI adjudication.

This keeps the skill system immediately testable and prevents premature expansion into a full tabletop rules engine.


## ADR-015

**Title:** Skill Check Commands Route Through Interaction Kernel

**Status:** Accepted

Skill-check-style player commands should enter the engine through the same command-processing path as other gameplay actions.

The Interaction Kernel may identify explicit, narrow skill-check command patterns and return structured interaction results that the `GameEngine` can route to the deterministic skill-check resolver.

This preserves `GameEngine` as the gameplay facade and prevents `play_game.py` from becoming a collection of direct subsystem calls.

This decision does not introduce broad natural-language parsing, dice randomness, character sheets, proficiency, inventory modifiers, combat rules, or AI adjudication.


---

## ADR-016

**Title:** Target Resolution Is Deterministic and Scene-Bound First

**Status:** Accepted

Player commands often refer to things by natural names, such as "guard", "gate", or "north". These references should be resolved by a deterministic target-resolution layer before future systems consume them.

The first implementation is intentionally limited to the current scene: visible entities and available exits. Missing or ambiguous targets must return structured unresolved results instead of guessing.

This decision does not introduce pathfinding, destination travel, fast travel, off-scene lookup, NPC memory, inventory objects, fuzzy matching libraries, LLM interpretation, combat rules, or broad natural-language understanding.

`GameEngine` remains the gameplay-facing facade. Player-facing front ends must not call the resolver directly.


---

## ADR-017

**Title:** Destination Resolution Identifies Places Before Travel Exists

**Status:** Accepted

Player commands may refer to non-current destinations, such as "blacksmith", "inn", or "market". These references should be resolved deterministically into known location identifiers before future travel systems consume them.

Sprint 8.4 is intentionally limited to destination identification. It does not move the player, compute paths, perform fast travel, advance time, interrupt travel, consult NPC memory, invoke AI interpretation, or expand the region pack into a full production setting.

Unknown or ambiguous destinations must return structured unresolved results instead of guessing.

`GameEngine` remains the gameplay-facing facade. Player-facing front ends must not call the destination resolver directly.

---

## ADR-018

**Title:** Simulation Owns Truth and AI Expresses Perception

**Status:** Accepted

The simulation determines objective world truth. AI narration may express, summarize, dramatize, and clarify what the player character can perceive, hear, infer, or be told, but it must not invent persistent facts or override simulation truth.

If a detail can affect future simulation, it must be represented or approved by the simulation. If a detail only enriches present expression and does not create durable truth, AI narration may provide it as neutral ambience.

Salient cues that imply hidden meaning, invite player action, or suggest future consequence should be grounded in simulation truth, actor knowledge, observable evidence, or player-character perception.

This decision preserves the simulation-first architecture and prevents the AI layer from becoming the authority over reality.

---

## ADR-019

**Title:** Phase 2 Focuses on World Evolution Foundations

**Status:** Accepted

After Sprint 8, the next major development phase should focus on World Evolution Foundations rather than combat or feature systems.

Phase 1 established representation of the world. Phase 2 should establish the minimum simulation structures required for the world to remember, evolve, and present meaningful opportunities without relying on AI invention.

Initial Phase 2 implementation should be broken into small capability sprints. Each sprint should add one durable concept, one narrow behavior, and one verification path.

Combat, full NPC AI, companions, faction warfare, economy simulation, and full travel simulation are deferred until the underlying history, time, pressure, knowledge, affordance, and opportunity foundations exist.

---

## ADR-020

**Title:** Simulation Model Guides Future Systems Without Premature Implementation

**Status:** Accepted

`docs/simulation_model.md` records the conceptual model for how the simulated world behaves.

The simulation model is design guidance, not an implementation specification. Concepts in the model do not become implementation requirements until a sprint explicitly schedules them.

This decision allows the project to preserve important design direction while maintaining the existing sprint discipline and avoiding premature systems.

---

## ADR-021

**Title:** World History Is Durable World State

**Status:** Accepted

World history entries are stored in `world_state.history` and are persisted through the existing save/load path.

The first durable history structure is intentionally minimal. Entries record an event type and summary, with location and current time included when available. This establishes that the simulation can remember that something happened without introducing world evolution, pressures, rumors, actor knowledge, autonomous NPC behavior, combat, procedural quest generation, or AI-owned truth.

`GameEngine` remains the gameplay-facing facade for exposing history to front ends. Front ends may review history through engine APIs, but they must not directly mutate history internals.

Scene snapshots, player perception, and narration remain derived views. They may express or display history, but they do not own historical truth.

---

## ADR-022

**Title:** Explicit Time Advancement Is Simulation-Owned

**Status:** Accepted

World time advances only through explicit engine operations until a future sprint schedules broader time behavior.

Sprint 9.2 introduces a narrow `wait` command that advances persistent `world_state.time` by one fixed hour using durable elapsed time. `GameEngine` owns the operation through the gameplay-facing facade, and the operation records a durable history entry with event type, summary, location when available, previous time, and new time.

This decision establishes time advancement as simulation-owned truth. AI narration may display or describe the result, but it does not decide that time advanced.

The first time-advancement operation must not trigger world evolution, pressures, pressure drift, rumors, actor knowledge, autonomous NPC behavior, schedules, travel duration, recovery, healing, decay, escalation, opportunity loss, combat, procedural quest generation, or destination travel execution.

---

## ADR-023

**Title:** Read-Only History Query Is a Simulation Support Boundary

**Status:** Accepted

History query capability reads durable `world_state.history` entries through the `GameEngine` gameplay-facing facade.

Sprint 9.3 supports narrow filtering by recent count, event type, and location when location is present. Query results preserve existing history-entry structure and are returned as copies so callers cannot mutate durable world history through the query result.

This boundary exists to let future simulation systems inspect accepted events without making history interpretation a narration responsibility.

History queries must not advance time, create new history entries, trigger world evolution, create pressures, generate rumors, update actor knowledge, run autonomous NPC behavior, surface quests or opportunities, summarize campaign history, or invent new facts from past events.

---

## ADR-024

**Title:** History Queries Are Bounded by Default

**Status:** Accepted

Normal history query access should return a bounded recent slice of durable `world_state.history` unless an explicit supported count is provided.

Sprint 9.4 defines one safe default count for history queries and routes normal gameplay and CLI history review through that bounded query behavior. Plain `history`, event-type-filtered history, and location-filtered history use the default recent slice instead of dumping the full durable history log.

Full durable history may remain available for internal inspection through explicit APIs, but it is not the default gameplay, narration, or simulation context path.

This decision keeps history durable without treating the full history log as active memory. It does not introduce history pruning, summarization, semantic memory, embeddings, archive tiers, active memory management, AI interpretation, world evolution, pressures, rumors, actor knowledge, autonomous NPC behavior, or combat.

---

## ADR-025

**Title:** Durable History Entries Have Stable Engine-Owned Identity

**Status:** Accepted

Each new durable `world_state.history` entry should receive a stable engine-owned identifier when the accepted event is recorded.

History identifiers are stored on the history entry itself and persist through save/load. Loading a save must not regenerate or rewrite existing identifiers, and creating additional history after load must not reuse an existing identifier.

The identifier makes accepted events safely referenceable by future systems. It does not add history interpretation, summarization, semantic memory, embeddings, active memory management, world evolution, pressures, rumors, actor knowledge, autonomous NPC behavior, or AI-owned truth. Narration and front ends may display identifiers, but they do not assign or alter them.

`GameEngine` remains the gameplay-facing facade for read-only history access. A narrow lookup by history identifier may return a copy of the durable entry, but it must not mutate history, advance time, create history entries, or trigger world evolution.

---

## ADR-026

**Title:** Future Consumers Receive Bounded History Context Packets

**Status:** Accepted

Future narration or simulation handoff boundaries should receive explicit bounded history context packets rather than full durable `world_state.history`.

Sprint 9.6 defines the first packet as a deterministic read-only structure exposed through `GameEngine`. The packet includes a schema marker, version, bounded limit metadata, current durable world time, current player location, and recent accepted history entries with their stable `history_id` values.

The packet preserves accepted history entry fields without interpretation. It does not summarize history, score relevance or importance, choose events for dramatic value, add AI narration, create semantic memory, manage active memory, or trigger world evolution.

The packet defaults to the normal safe bounded history count and validates explicit count overrides against a documented maximum. This keeps history durable and referenceable without making the full history log a routine narration or simulation input.

---

## ADR-027

**Title:** Narration Context Is a Read-Only Input Boundary

**Status:** Accepted

Future narration should receive an explicit narration context packet rather than direct access to mutable engine state or full durable history.

Sprint 9.7 defines this packet as a deterministic read-only structure exposed through `GameEngine`. It includes schema/version metadata, the raw player input supplied for context construction, current durable world time, current player location, the current scene snapshot, and the bounded Sprint 9.6 history context packet with stable `history_id` values.

The packet is an input boundary only. It is not AI model integration, narration output, simulation authority, world evolution, history summarization, relevance scoring, semantic analysis, actor knowledge, equipment tracking, exposure tracking, or a narration validator.

The narrator can describe. The engine decides what is true.

Future narration may use known scene facts for safe atmospheric prose, but it must not invent unstated specifics. It must not invent player equipment, clothing, memories, emotions, physical conditions, owned items, NPC attitudes, relationships, hidden observers, threats, clues, exits, or durable world facts unless those details are present in the narration context.

Atmospheric prose does not become durable world truth unless the engine records it. If the scene contains a blizzard, narration may describe cold weather, but may not mention the player's gloves unless gloves are present in player state or context.

---

## ADR-028

**Title:** Narration Output Is Presentational, Not Simulation Authority

**Status:** Accepted

Future narration output should pass through an explicit structural contract before it can be shown or otherwise consumed.

Sprint 9.8 defines narration output as presentational prose only. A valid output contains schema/version metadata and a `narration_text` string. The contract rejects unsupported structured fields and structured attempts to mutate world state, mutate history, advance time, create quests, create rumors, create pressures, update actor knowledge, add NPC schedules, add evidence, add consequences, add entities, add locations, add exits, alter inventory, add player conditions, or update NPC relationship state.

This decision preserves the existing rule: the narrator can describe, and the engine decides what is true. Narration output may be shown later, but it is not accepted world truth.

The contract does not attempt to fully prove whether freeform prose contains invented details. Freeform narration drift is controlled by context limits, prompt rules, output contract structure, and later review or validation layers. If the context contains a blizzard, narration may describe cold weather, but should not mention gloves unless gloves are present in context.

This decision does not introduce AI model calls, final AI narration generation, replacement of existing gameplay output, semantic prose analysis, embeddings, world evolution, equipment, clothing, exposure, fatigue, condition systems, or durable facts created by narration output.

---

## ADR-029

**Title:** Narration Must Be Validated Before Display

**Status:** Accepted

Sprint 9.9 introduces a deterministic narration pipeline stub that sits between narration context and preview display.

The pipeline must take a copied narration context packet, supply a fixed prose-only sample, validate that candidate through the narration output contract, and return a preview packet whose display text is copied only from validated narration output. The pipeline does not generate prose from player input or world data, does not call an AI model, does not persist narration, and does not replace gameplay narration.

The preview path is intentionally narrow and deterministic. It proves that the context boundary and output contract can be sequenced safely before any provider integration exists. The previewed text remains presentational only and does not become world truth, create history, advance time, or mutate the simulation.

This decision does not introduce model providers, prompts, general narration generation, semantic prose analysis, embeddings, state persistence for narration, or any mechanism that treats preview text as simulation authority.

---

## ADR-030

**Title:** Narration Candidate Sources Are Untrusted and Fail Closed

**Status:** Accepted

Candidate-producing components are not simulation authorities. They receive narration context, produce untrusted source output, and may not bypass narration-output validation.

Only narration accepted by the existing output validator may enter preview display text. Malformed output, invalid candidates, and source failures produce no display text and fail closed.

Narration-source failure does not alter simulation state, advance time, create history, persist narration, or interrupt normal deterministic gameplay.

This decision does not introduce AI providers, prompts, retries, streaming, persistence, or semantic hallucination detection.

---

## ADR-031

**Title:** Narration Requests Are Bounded, Deterministic, and Provider-Neutral

**Status:** Accepted

Narration sources receive a versioned, copy-safe request packet made only from the already bounded narration context and stable contract metadata.

The request contains machine-readable constraints, but no provider-specific system messages, user messages, credentials, or payload formats. It grants no simulation authority.

Request construction and validation fail closed. Request construction and preview do not mutate state, advance time, create history, alter history identifiers, or persist narration artifacts.

This decision does not introduce an AI model, provider SDK, external service, or prompt system.

---

## ADR-032

**Title:** Narration Prompts Are Deterministic Provider-Neutral Contracts

**Status:** Accepted

Narration prompt construction is a distinct validated contract boundary between the narration request packet and the untrusted candidate source.

Prompt packets are built only from validated bounded requests. They are deterministic, copy-safe, and provider-neutral. Candidate sources receive prompt packets rather than raw simulation data or raw narration context. Prompt packets carry no simulation authority and do not expose provider-specific payload formats, model settings, credentials, or environment configuration.

Prompt construction and validation fail closed. Prompt and source failures produce empty display text, and candidate prose remains untrusted until the existing narration-output contract accepts it.

This decision keeps the engine contract provider-neutral without introducing provider payload formats, provider selection, retries, streaming, caching, or an AI model call.

**Alternatives Considered**

- Keep the request packet as the final pre-source boundary. Rejected because the next contract layer needed a distinct prompt representation without expanding source authority.
- Allow provider-specific message payloads in the engine contract. Rejected because it would couple the engine to one provider shape and weaken the deterministic boundary.
- Defer prompt validation until after the source. Rejected because source invocation must stay behind a validated prompt boundary and fail closed before any untrusted output is treated as meaningful.

---

## ADR-033

**Title:** Narration Source Results Are Untrusted Until Strictly Validated

**Status:** Accepted

Every narration source-result envelope is untrusted until the engine validates it against the supported strict source-result contract.

The pipeline validates the exact supported schema, version, source identity, echoed prompt, candidate object, and metadata immediately after source invocation. The echoed prompt must match the originating validated narration prompt. Unsupported, malformed, or mismatched source results fail closed. Raw invalid source payloads are not copied into preview packets or diagnostic inspection fields.

Valid source-result structure does not validate candidate prose. The candidate must still pass independently through the narration-output contract before display. Source-result validation has no simulation authority and creates no durable facts.

**Alternatives Considered**

- Continue partial validation inside candidate extraction. Rejected because it leaves the envelope boundary porous and lets malformed source results reach preview inspection data.
- Copy malformed source results into diagnostic packets. Rejected because raw invalid source payloads should not be surfaced in preview paths.
- Treat a structurally valid source result as implicitly validating its candidate. Rejected because envelope validity and prose validity are separate contracts.
