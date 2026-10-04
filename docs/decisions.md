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

See also: `docs/simulation_principles.md`.

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

---

## ADR-034

**Title:** Sprint 9 Closes as World Memory and Safe Narration Foundations

**Status:** Accepted

Sprint 9 is complete and no Sprint 9.14 is required.

The milestone is named **World Memory and Safe Narration Foundations**. It established durable accepted-event history, stable history identity, bounded history access and context, explicit simulation-owned time advancement, and a deterministic fail-closed narration preview boundary.

Sprint 9 completed important World Evolution prerequisites but did not complete World Evolution Foundations as a whole. Persistent pressures or threads, pressure change, time-based drift, runtime actor state, actor knowledge, evidence, consequences, schedules, affordances, opportunity surfacing, and travel execution remain future capabilities.

The existing narration context, request, prompt, source, source-result, output, and preview boundaries are sufficient for the current deterministic fixed-source preview. Narration infrastructure should not expand further until a real provider or other immediate bounded consumer demonstrates a concrete need. Real AI provider integration is deferred and is not a prerequisite for simulation-owned world evolution.

The immediate next project activity is a focused playable vertical-slice review. After that review, the next feature work should begin a new milestone within Phase 2, proposed as **Phase 2B - Reactive World State Foundations**, rather than extending Sprint 9. Persistent scoped pressures or unresolved threads are the leading next implementation candidate, subject to the vertical-slice findings.

**Consequences**

- The roadmap must mark Sprint 9 complete and remove language stating that Sprint 9 is undefined.
- No following sprint is defined by this decision.
- The active Sprint 9.13 manifests remain closed and are not replaced until a future sprint is explicitly staged.
- Provider integration, provider registries, retries, streaming, semantic narration validation, and additional narration packet layers remain deferred.
- Documentation should distinguish immutable Region Pack seeds from mutable runtime state before actor knowledge, schedules, or regional-state mutation are implemented.

**Alternatives Considered**

- Continue with Sprint 9.14 narration infrastructure. Rejected because the deterministic preview is already fail-closed and further work lacks an immediate consumer.
- Add a real AI provider next. Rejected because generated prose would improve presentation without advancing simulation-owned world evolution.
- Declare all World Evolution Foundations complete. Rejected because the engine still lacks reactive pressures, knowledge, evidence, consequences, schedules, affordances, and opportunity surfacing.
- Begin a pressure sprint immediately. Rejected in favor of first conducting a focused playable vertical-slice review so the next bounded capability is selected from observed gameplay needs.

---

## ADR-035

**Title:** Resolved Conversations Become Durable Accepted Events

**Status:** Accepted

A conversation becomes durable history only after the normal gameplay path accepts the command and deterministic current-scene target resolution identifies a resolved entity.

The resulting history event records the occurrence and grounded target identity only. It stores the existing engine-owned history identifier, the current location, the current durable time, `target_entity_id`, and `target_display_name`. It does not establish dialogue, topics, claims, promises, actor knowledge, beliefs, relationships, emotional state, consequences, pressures, or time advancement.

Failed, unresolved, ambiguous, and non-actor conversation targets do not create history.

Conversation history remains inside the existing durable history system and keeps the same bounded history context, narration context, persistence, and save/load ownership boundaries. Conversation does not grant narration authority.

---

## ADR-036

**Title:** Scoped Pressures Are Persistent Current State

**Status:** Accepted

Current scoped pressure state is simulation-owned mutable truth and belongs in `world_state`. A pressure is not represented solely as a history event. History may later record accepted pressure changes, but history does not replace the current pressure value.

Region Packs may provide immutable initial pressure seeds through the exact optional top-level field `initial_pressures`. When present it is a list of exact pressure records, and Region Pack provenance `source_id` must equal the containing pack's exact `region_id`. New-game construction validates and deep-copies those seeds into persistent `world_state.pressures`.

Canonical runtime World State requires `pressures`. During loading only, a copied version-1 legacy save missing the field normalizes to an empty dictionary before strict validation and engine construction; it is not seeded from the Region Pack. A present malformed value fails validation. Save version 1 is preserved without a general migration framework.

The initial persistent collection is a dictionary keyed by stable `pressure_id`. Each exact record contains pressure identity and type, a region or location scope, an integer level from 0 through 100, and Region Pack provenance. Read access is exposed exactly through copy-safe `GameEngine.get_pressures()` and `GameEngine.get_pressure(pressure_id)`, with unknown identifiers returning `None`. The required `pressures` CLI command routes through `get_pressures()` and has no direct state access or mutation authority.

Sprint 10.2 is representation-only. Pressure mutation, pressure-change history, time drift, projection into scene or narration, AI-created pressures, unresolved threads, and generic ongoing-condition frameworks remain future capabilities.

Sprint 10.2 implementation and verification completed successfully in the official project environment, and the closeout preserved the representation-only boundary.

---

## ADR-037

**Title:** Pressure-Level Changes Are Atomic Current-State Transitions

**Status:** Accepted

An exact pressure-level change is prepared against a copied candidate world state. Pure pressure validation and record mutation remain in or near `engine/pressure_state.py`. `GameEngine` owns orchestration, durable history creation, final validation, and the single commit to `GameEngine.world_state`. A material change commits the pressure value and one `pressure_changed` history entry together. Any validation, mutation, history-construction, or final-validation failure commits neither. Setting the existing level is a successful no-op and creates no history.

Sprint 10.3 is complete and closed out. The next feature work should move to the next bounded Phase 2B capability without introducing a generic mutation framework, rollback layer, or pressure CLI command.

---

## ADR-038

**Title:** Pressure Consequences Reference One Accepted Source Event by Stable History ID

**Status:** Accepted

A linked pressure consequence references exactly one already durable history entry through a stable `source_history_id`. The source entry must already exist, must be a non-empty stable history identifier, and must precede the new consequence in durable history. Self references, forward references, malformed references, and dangling references fail closed.

Existing durable history without `source_history_id` remains valid, including the unlinked Sprint 10.3 pressure history. Narrow referential-integrity validation belongs in `engine/world_state.py`. `GameEngine` owns source resolution, candidate-state orchestration, linked history construction, completed-candidate validation, and the final atomic commit. `engine/pressure_state.py` remains unaware of history.

The pressure mutation and the new linked `pressure_changed` consequence entry commit atomically. The already accepted source event is read-only and is not part of that transaction. This decision does not introduce automatic event effects, a causal graph, reverse references, replay, effect policy, narration behavior, or combined event-acceptance and consequence atomicity.

---

## ADR-039

**Title:** One Region-Declared Resolved Conversation and Its Pressure Consequence Commit Atomically

**Status:** Accepted

The engine already had durable resolved-conversation events, persistent scoped pressures, exact atomic pressure mutation, and stable backward causal references. It lacked one automatic deterministic path from an accepted gameplay event to a persistent pressure consequence.

Region-specific effect policy belongs in strict immutable Region Pack data. Sprint 10.5 supports one conversation-specific declaration shape mapping one exactly resolved entity to one existing seeded pressure and one exact target level. `GameEngine` owns runtime declaration lookup and candidate-state orchestration. It prepares the accepted conversation source first and any material linked pressure consequence in one candidate world state, validates the completed state, and builds the candidate scene before committing world state once. The source precedes the consequence and both become durable only after preparation succeeds.

The public Sprint 10.4 `set_pressure_level_from_event(...)` operation retains its already-durable-source contract. A private non-committing helper provides bounded internal reuse. Unmatched conversations remain source-only. A matching pressure no-op commits the new conversation source but creates no consequence history. Save/load persists resulting state and causal history without persisting or replaying declarations.

**Consequences**

- The first deterministic player-event-to-world-consequence path is complete using existing conversation, pressure, history, and causal-reference seams.
- Candidate-state composition provides an atomic source-and-consequence pattern without a transaction framework.
- Immutable content policy remains outside generic engine code.
- The declaration is intentionally conversation-specific, supports one consequence per target, and uses exact levels rather than deltas or expressions.
- Scene projection, autonomous progression, and general effect infrastructure remain deferred. A second genuine effect family may justify later review, but no generalized framework is approved now.

**Alternatives Considered**

- Hardcode Captain-specific policy in `GameEngine`. Rejected because immutable region policy belongs in Region Pack data.
- Commit the conversation and then call the public Sprint 10.4 method. Rejected because a failure could leave a partial durable commit.
- Add a generic rule engine, event or command bus, or transaction framework. Rejected as premature infrastructure.
- Add pressure projection or time-based progression first. Rejected because the simpler atomic composition seam was the immediate bounded capability.
- Add persistent unresolved threads in parallel. Rejected as a separate future subsystem.

---

## ADR-040

**Title:** Pressure Applicability Is a Pure Scope-Aware Read Boundary

**Status:** Accepted

Pressure applicability is determined only by exact scope membership: region-scoped pressure records apply when their `scope_id` exactly equals the loaded Region Pack `region_id`, and location-scoped records apply when their `scope_id` exactly equals the requested canonical location identifier.

Applicability does not imply perceptibility, activity, importance, visibility, escalation eligibility, or narration eligibility. Scene, perception, narration, visibility, and runtime-effect policy remain separate concerns.

The canonical operation is deterministic, read-only, and copy-safe. It validates pressure state before filtering, returns defensive copies, and orders results by sorted `pressure_id`. Future consumers must use this canonical boundary instead of reimplementing pressure-scope filtering.
# ADR-041 - One Elapsed-Hour Threshold May Cause One Atomic Pressure Consequence

Status: Accepted.

One immutable Region Pack declaration may target one existing pressure and exact level. It is evaluated only during accepted time advancement using `previous_elapsed_hours < trigger_elapsed_hours <= new_elapsed_hours`. The source event and any material consequence commit atomically with time and the rebuilt scene. One-shot behavior is inferred from durable elapsed time; no persisted fired flag is required. This decision introduces no scheduler, recurring drift, world tick, or generic effect engine.
# ADR-042 - Pressure Applicability Does Not Grant Perceptibility; Authored Observation Policy Does

Status: Accepted.

Applicability is necessary but insufficient for perception. One strict immutable Region Pack declaration grants perceptibility. Observation is derived and non-persistent; raw pressure state remains simulation-owned. The Scene Snapshot does not own pressure cues, perception receives only a validated authored cue, and narration gains no authority. No general visibility, player-knowledge, or observation-history system is introduced.

# ADR-043 - Authored Actors Retain Immutable Identity and Description While World State Owns Mutable Runtime Location

Status: Accepted.

Region Packs own immutable named static actor identity, description, and authored baseline location. The existing `entity_id` is the sole runtime ownership key. World State stores only sparse location overrides; absence means the authored location, and returning to that baseline removes the override. Spawned template entities are excluded because they have no stable instance identity.

Scene Snapshot construction is the canonical projection boundary that merges authored actor data with effective runtime location. Perception, target resolution, conversations, and narration consume the Scene Snapshot rather than override state. Version-1 saves remain compatible by normalizing a missing mapping to empty. A material move prepares its override, one `actor_moved` history entry, validation, and rebuilt scene before committing World State and scene atomically.

# ADR-044 - One Declared Unresolved Thread Is Sparse Persistent State with Derived Local Evidence

Status: Accepted.

One unresolved situation may be declared immutably in a Region Pack and triggered by one resolved conversation with one static actor. Immutable content owns its identity, description, trigger, applicable perception locations, and evidence text. `world_state.open_threads` owns only whether that declaration has been created, its sole supported `open` status, and the stable history identifier of the source conversation.

The matching conversation source, one open-thread record, and one causally linked `unresolved_thread_opened` history entry are prepared in the existing candidate transition and committed only after completed-state validation and scene construction succeed. A thread identifier is unique in the runtime dictionary, so repeated trigger conversations do not create a second instance or a second opening event. Version-1 saves missing the field normalize to an empty dictionary only on load.

Perception derives authored evidence text for an open declared thread at an applicable location. It does not create a quest log, objective, marker, player-knowledge record, resolution mechanism, generic trigger engine, or ongoing-condition framework.

# ADR-045 - Actor Knowledge Seeds Initialize Sparse Persistent Membership

Status: Accepted.

Immutable Region Pack `knowledge` arrays belong to authored static actors and serve only as validated new-game seeds. `world_state.actor_knowledge` owns current sparse membership keyed by the same stable static `entity_id`; absent keys mean no current membership. The runtime structure stores only unique non-empty knowledge identifiers and does not add truth, certainty, provenance, timestamps, categories, beliefs, or behavior semantics.

New games deep-copy non-empty seeds. Version-1 saves missing the field normalize to empty membership only while loading, and loading never reseeds from changed Region Pack content. Region-aware validation excludes unknown, spawned, and ephemeral identities. `GameEngine.get_actor_knowledge(actor_id)` is a copy-safe inspection boundary only; no scene, perception, narration, prompt, target-resolution, dialogue, acquisition, loss, propagation, or autonomous behavior is authorized.

# ADR-046 - Explicit Actor-Knowledge Addition Commits Membership and History Atomically

Status: Accepted.

`GameEngine.add_actor_knowledge(actor_id, knowledge_id)` is the sole Sprint 10.17 gameplay-facing addition boundary. It accepts exactly one stable static actor identity and one non-empty knowledge identifier. The engine copies World State, creates sparse membership only when absent, appends once in call order, records one `actor_knowledge_added` history entry with current durable time, validates the completed candidate against the active Region Pack, and assigns live World State once. It does not rebuild or replace the Scene Snapshot.

Duplicates are successful no-ops: they add no history and do not replace World State or the Scene Snapshot. Material entries contain only the engine-owned history identity, event type, exact summary, time, actor identity, and knowledge identity. They remain durable and history-queryable but narration context excludes them as lifecycle records.

This decision preserves save version 1 and introduces no source linkage, certainty, truth, provenance, reason, evidence, dialogue, perception, target resolution, loss, propagation, or autonomous behavior.

# ADR-047 - Causally Referenced Actor-Knowledge Addition

Status: Accepted.

`GameEngine.add_actor_knowledge_from_event(actor_id, knowledge_id, source_history_id)` may add one opaque knowledge identifier to one stable static actor while referencing one already accepted durable history entry. The source identifier must be non-empty, resolve in current history, and be backward from the new entry. The linkage is structural only: it does not establish semantic eligibility, witnessing, understanding, evidence, truth, certainty, reliability, or provenance.

A material addition prepares copied World State, appends absent membership once, constructs one `actor_knowledge_added` history entry with `source_history_id`, validates the completed Region-aware candidate including backward history integrity, and commits World State exactly once. The source entry remains unchanged and outside the commit. Duplicates still validate the source but create no membership, history, World State replacement, or Scene Snapshot rebuild.

Source-free Sprint 10.17 entries remain valid through save/load. This decision preserves save version 1, stable static actor ownership, narration-context exclusion, and all non-projection boundaries. It introduces no automatic trigger, source-event type restriction, causal graph, generic transaction system, knowledge loss, propagation, or player-facing behavior.

# ADR-048 - Evidence Traces Are Sparse World State Records

Status: Accepted.

World State owns deterministic ordered evidence-trace records. Each has one
stable `trace_id`, opaque `evidence_id`, and exact immutable Region Pack
`location_id`. No trace is a Region Pack seed or a player-facing object.
Version-1 saves persist the records; only a missing legacy field normalizes to
an empty list during candidate loading. Records and inspection results are
defensively copied. Identical identities are no-ops while conflicting reuse
fails.

Lifecycle entries may structurally reference an earlier durable source history
entry, without asserting truth, reliability, discovery, interpretation, belief,
or causation semantics beyond the declared transition. Traces remain distinct
from history, unresolved threads, actor knowledge, perception, and narration.

## Sprint 10.19 ADR Determination

No new ADR is required. Sprint 10.19 directly composes ADR-035 resolved conversation history, ADR-039 declared conversation consequences, ADR-045 actor-knowledge ownership, ADR-046 atomic explicit addition, and ADR-047 causal linkage. It creates no new persistent domain, ownership boundary, save compatibility rule, or generic consequence mechanism.

## ADR-049 - Deterministic Local Discovery Is Authored Policy with Sparse Player Membership

**Status:** Accepted

Region Packs own immutable discoverability declarations and exact player-facing
text. World State owns only unique discovery identifiers. Investigation examines
only the current location, considers only present opaque traces matched by an
authored declaration, and deterministically selects the first undiscovered
declaration. A material discovery and one player_discovery_added history entry
validate and commit together; exhausted eligibility is a successful no-op.
Missing version-1 legacy membership normalizes to empty on load. Discovery and
trace internals do not enter Scene Snapshots, perception, narration, dialogue,
targeting, actor knowledge, quests, inventories, interpretation, or generic
frameworks.

## ADR-050 - Authored Clue Presentation Resolves One Open Thread Atomically

**Status:** Accepted

Region Packs own the one strict resolution declaration, authored clue title,
exact response, and resolved observation. World State owns sparse
`resolved_threads`; an entry contains only the thread identity, `resolved`
status, and the presentation history identity. Missing legacy version-1 state
normalizes empty only during loading.

The engine accepts a presentation only when the player already knows the exact
authored clue, the declared static actor is currently present, and the required
thread is explicitly open. It prepares presentation history, removes the open
state, creates resolved state, adds causally linked resolution history,
validates, rebuilds the scene, and commits once. Repeats are non-mutating;
resolved threads cannot reopen through their original trigger. This adds no
dialogue system, semantic interpretation, branching, quests, or generic state
machine.

## Authored Resolved-Thread Observation and Integrity ADR Determination

No new ADR is required. ADR-050 already owns sparse resolved-thread state,
authored observation text, atomic presentation, and version-1 compatibility.
Sprints 10.37 through 10.39 only strengthen validation of that established
state and derive one local non-persistent presentation from it. History and
Region Pack declarations remain validation inputs rather than a second runtime
authority; no generic consequence or projection framework is introduced.

## ADR-051 - Actor-Knowledge Conversation Response Is a Non-Persistent Projection

**Status:** Accepted

One exact-keyed immutable Region Pack declaration may supply one response for
one stable static actor and one required durable membership identifier. After a
successful current-scene conversation, the engine derives the response from the
actor's command-start membership only after the existing candidate transition,
final validation, candidate scene construction, and single live commit all
succeed. The response is exact authored player-facing text and may repeat on
every eligible conversation.

This creates no World State, save, migration, history, scene, perception,
narration, player-knowledge, dialogue, rule-framework, or response-history
ownership. Failure publishes neither candidate state nor response.

## ADR-052 - One Resolved Thread May Relocate One Authored Static Actor

**Status:** Accepted

An optional Region Pack-owned declaration may bind one already declared resolved thread to one stable static actor and one valid destination. Its singleton `effect_id` must not conflict with any supported authored effect identity in the same Region Pack. Eligibility is trigger-specific: it exists only during the successful authored clue-presentation resolution. The candidate creates the clue-presentation source before both lifecycle and material actor-location history, validates the complete state, builds one Scene Snapshot, and publishes state and scene together. Public result output is restricted to `None`, `{"status": "applied"}`, or `{"status": "no_op"}`; identifiers remain internal. Already-at-destination is a successful no-op with no location history. Version-1 saves continue unchanged. This is not a generic consequence, reaction, rule, condition, dispatcher, or scheduler framework.

## ADR-053 - One Declared Elapsed-Time Threshold May Add One Hidden Evidence Trace

**Status:** Accepted

An optional strict Region Pack declaration may bind one positive elapsed-hour threshold to one stable trace, opaque evidence identity, matching discovery declaration, and location. The existing explicit time transition creates its source history first, then prepares pressure, actor relocation, and trace consequences in a fixed order against one copied candidate before validation, scene construction, and publication. Exact existing traces are no-ops; conflicting identities reject. The trace remains hidden until existing local explicit investigation finds its matching declaration. This preserves save version 1 and does not create a scheduler, generic effect registry, transaction framework, passive cue, or automatic discovery.

## ADR-054 - One Declared Delayed-Watch Discovery May Recall Captain Grey Atomically

**Status:** Accepted

The existing `present` interaction already resolves a local actor and an exact
player discovery. One optional strict Region Pack declaration binds only the
delayed-watch discovery, Captain Grey as target and relocated actor, the North
Gate, and one exact authored response.

`GameEngine.present_clue` selects this path solely by local target identity and
exact discovery identity. The west-road path uses another discovery, so no list,
ordering, or precedence policy is needed. The candidate adds `clue_presented`,
prepares material `actor_moved` history with a backward source reference,
validates, rebuilds the scene, and publishes once. At the North Gate relocation
is a no-op with no duplicate move history. Discovery is not consumed, save
version remains 1, and no generic consequence or presentation framework exists.

## ADR-055 - One Declared One-Hour West-Road Exit Traversal Is Atomic

**Status:** Accepted

One optional strict Region Pack declaration may name only the existing directed
West Gate to Western Trade Road connection and a duration of exactly one hour.
The existing local movement command remains the player entry point; every other
route stays instantaneous. This is not general travel-duration metadata.

The engine prepares elapsed time and its `time_advanced` source history from
the command-start West Gate before changing player location. Existing threshold
consequences are then prepared with their required backward references to that
source history. Completed `player_movement` history follows those records and
uses the final time and destination. No in-transit state, departure/arrival
history kind, source scene, or post-time/pre-movement scene exists.

The complete candidate validates and builds one destination Scene Snapshot
before it replaces live World State and scene. Any preparation, history,
validation, or scene-build failure publishes neither elapsed time, consequence,
movement, nor partial scene. Existing state and history structures preserve
save version 1 compatibility. General travel, bidirectional inference,
pathfinding, encounters, schedules, and route frameworks remain deferred.

## ADR-056 - One Declared Western Trade Road Arrival May Make One Hidden Trace Discoverable

**Status:** Accepted

One optional strict Region Pack declaration may bind only the accepted directed
West Gate to Western Trade Road one-hour traversal to one unique trace, opaque
evidence identity, and matching discovery declaration at the Western Trade
Road. It represents evidence created, exposed, or made locally discoverable by
that completed arrival. Arbitrary pre-existing roadside evidence must not be
modeled as physically caused by player movement.

The existing outer traversal candidate prepares elapsed time, existing crossed
time consequences, completed `player_movement`, and then the absent trace. The
new `evidence_trace_added` record references the completed movement history,
not `time_advanced`. Validation and one destination Scene Snapshot construction
precede one live publication. Existing traces are no-ops, while normal time and
movement still complete.

The trace and opaque identity remain hidden from movement output, destination
scenes, narration, perception, targeting, conversation, actor knowledge, and
ordinary diagnostics. Existing explicit local investigation is the sole
discovery boundary. This preserves save version 1 and introduces no general
arrival-effect mechanism, route hook, encounter system, generic effect
dispatch, automatic discovery, or travel generalization.

## ADR-057 - One Discovery-Gated Conversation Affordance Is a Pure Player-Safe Projection

**Status:** Accepted

One optional strict Region Pack `conversation_affordance` declaration may bind
one affordance identity, location, stable static actor, required player
discovery, and authored display text. The declaration is valid only when the
location and actor are supported by existing actor-location rules and the exact
actor-and-discovery pair already has a declared discovery-gated conversation
response.

Perception derives the singleton only from current player location, visible
targetable static-actor presence, and player discovery membership. Its record
contains only `affordance_id`, `display_text`, deterministic `command_text`,
and `target_display_name`. It does not expose entity, discovery, response,
evidence, actor-knowledge, pressure, history, causal, or eligibility data.

The projection is informational and may repeat whenever the player-safe
perception is rebuilt. It adds no opportunity World State, history, causal
record, acknowledgement, once-only display state, persistence, migration,
transaction, lifecycle, consumption, parser change, or command behavior.
Existing `talk` execution independently resolves the target and revalidates
conversation eligibility. Multiple affordances, priority, ordering, scoring,
condition languages, action types, and generic affordance infrastructure remain
deferred.

## ADR-058 - Provider-Backed Narration Remains Explicit, Untrusted, Cost-Bounded, and Preview-Only

**Status:** Accepted

The explicit narration-preview command may use one adapter-local synchronous
OpenAI Responses source with fixed `gpt-4.1-mini`, a 20-second timeout, zero
retries, no reasoning field, no tools, no streaming, no provider conversation
state, `store=False`, an exact 8,000-token local input ceiling, and a
256-token output ceiling. Provider output is untrusted and must pass the
existing source-result and narration-output validation boundaries before
display. It is nonpersistent and has no simulation authority.

Automated tests use injected fake transport only. One opt-in owner-run live
smoke is allowed and records only a sanitized pass/fail line. Provider failures
fail closed without affecting normal gameplay. This establishes no provider
framework; a later local source may use the same seam.

## ADR-059 - Character Information and Spatial Projection Use Minimum Sufficient World Detail

**Status:** Accepted

The engine models, resolves, and persists only the detail needed for meaningful
player experience. Important world structure and gameplay are authored
explicitly. Detail required by a current action may be realized temporarily,
and becomes durable only when later gameplay materially depends on it. The
engine does not model possibilities merely because they could occur. **Depth
must earn persistence. Complexity must earn implementation. Player experience
is the justification for both.**

World truth is authoritative simulation state and remains distinct from a
character's current perception, broad familiarity, and selectively acquired
information or belief. Perception may project observable changes without
exposing hidden causes: observing Captain Grey leave does not disclose why he
left unless that reason is legitimately known. Familiarity supplies plausible
stable background understanding, not automatic current knowledge. It may
coexist with stale understanding of a place; recent change does not update an
absent character merely because world truth changed. Acquired information or
belief is explicit only when a future simulation, interaction, narration,
inference, or continuity need depends on the character having encountered it.
Information from another source can remain a claim or belief rather than
established truth. Where the timing or provenance of such explicit information
matters, existing causal-history or provenance mechanisms are preferred over a
comprehensive timestamped knowledge ledger.

Information remains at the coarsest useful granularity. It may be selectively
promoted from a broad report, such as fires in part of a city, to a named
building or detailed circumstances only when player interest, simulation
consequence, narrative relevance, or continuity justifies that narrower durable
detail. Incidental events, objects, observations, and location details are not
to be catalogued by default. A categorical location-familiarity direction,
potentially resembling unfamiliar, familiar, and local, is promising but its
levels, names, and semantics are not frozen. Familiarity never automatically
grants current, hidden, recently changed, or otherwise unknown information.

The authored map represents established macro spatial relationships, not every
physical path or complete local geometry. Player-facing movement should project
natural spatial orientation--for example, that Main Street continues south from
the North Gate--while compass directions normally support orientation rather
than define the whole movement abstraction. Projection must respect what the
character can perceive, legitimately knows through familiarity, or has
explicitly learned; engine topology alone never justifies revealing a
destination.

The macro graph is not an exhaustive traversal list. Future bounded work may
resolve the local detail necessary for a plausible action such as using an
alley, rooftop, sewer, building, climb, shortcut, or wilderness route, while
remaining consistent with established world truth. The intended layering is
durable authored macro geography, already-authored or play-significant local
facts, and otherwise unresolved local detail temporarily realized for the
action. A temporarily realized local fact becomes persistent only when future
gameplay materially depends on it.

This ADR is architectural direction, not authorization to implement a complete
knowledge graph, universal belief or familiarity system, comprehensive
timestamped knowledge ledger, complete spatial simulation, rooftop graph,
building geometry, procedural spatial simulation, dynamic traversal framework,
or universal world-detail model. Future capability packages must implement only
the smallest subset justified by observed player-facing need. It guides future
solutions to the Sprint 10.60 findings on natural spatial orientation,
meaningful-action discoverability, observable state change, elapsed-time
presentation, and discovery/use presentation.


## ADR-060 - West-Road Reference Predicament Owns One Current Phase

Status: Accepted; Sprint 10.77 owner smoke and acceptance passed.

The revised Bryn Shander reference situation persists only `west_road_predicament.phase` and `last_outcome_history_id`. The fixed seven-phase model owns current progression. Existing discoveries retain encountered information; actor membership records only actually shared reports. History records commitments, elapsed-time sources and outcomes with backward causal links, and validates consistency without reconstructing live phase.

Each accepted decision copies state, prepares all effects (including one hour for either initial approach), validates the candidate, rebuilds its scene and publishes once. Follow-ups abstract bounded local operations without additional time, combat or patrol simulation. Named actors witness/report decisions at the North Gate; responses and opportunities are derived rather than separately persisted.

The existing Bryn Shander prototype declarations are superseded in ordinary play. Their mechanism coverage uses an explicitly test-only legacy fixture. No generic situation, quest, condition, dialogue, migration or event framework is introduced.

Save envelope remains version 1. Revised Bryn Shander content requires the new record; missing state fails before region-aware interpretation of legacy scenario facts. Old files and the active session remain intact. No old decision is invented and no missing record is silently initialized on load.

## ADR-061 - Bounded Character Competence and Accepted West-Road Attempts

Status: Accepted; Sprint 10.78 owner smoke passed and owner acceptance was recorded
October 4, 2026.

`player.competences` is a unique list limited to tactical_assessment,
outdoor_tracking and surveillance_analysis. Classes, biography and equipment
prose supply no authority. The fixed West-Road competence module interprets
applicable authored evidence, deterministic recognition, available approaches,
local d6 results and costs. Named guard coordination retains the existing
North-Gate decision boundary; only guarded survey consumes committed guard
assistance, recorded on its source event. Assistance is never a competence.

`competence_attempts` has at most one accepted record per supported operation.
It stores draw (null for survey), result, accepted specialist basis, cost,
discovery identifiers and source/time/result history references. Uncertain
operations cost one hour; survey costs two, or one with tactical competence.
Partial findings are limited supported information in existing discoveries;
failure adds none. Full results reuse the existing pursuit phase, route,
reporting and causal validation. Preparation uses the existing copied candidate
and time consequences, then validates/builds/publishes once. Replays return the
accepted result without drawing, charging or publishing.

Save version 1 is retained consistently with prior additive field normalization
(e.g. ADR-036). Missing new fields normalize empty in a copied loaded payload;
present malformed fields reject. Required West-Road phase/prototype rejection
from ADR-060 remains intact. Historical completed pursuit needs no attempt.
No general checks, skills, investigations, transactions or migrations arise.

Player-safe packets separate observation/report, automatic limited recognition,
limited inference, confirmed local findings, approaches/costs and accepted
outcomes. Narration preserves uncertainty and explicit limits; it cannot grant
competence/resources or repair failure. No identity, affiliation or unverified
destination is inferred. The original ordinary continuation remains available.
