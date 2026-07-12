# Architecture

Version: 0.10.10

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

## Narration Preview Boundary

The implemented deterministic preview path is:

```text
Bounded Narration Context
    ↓
Validated Narration Request
    ↓
Validated Provider-Neutral Prompt
    ↓
Untrusted Candidate Source
    ↓
Strict Source-Result Validation
    ↓
Independent Candidate-Output Validation
    ↓
Preview Display Text
```

This is a presentation-only path. It has no simulation authority, does not persist narration artifacts, and does not replace normal deterministic gameplay narration.

## Source of Truth

`world_state` is the persistent runtime source of truth for mutable state.

Currently owned by `world_state`:

- Player current location
- Current weather
- Current time
- World history entries
- Persistent scoped pressures
- Runtime actor-location overrides
- Persistent open unresolved threads
- Persistent actor knowledge membership for stable static actors

Region Packs provide static world data and initial values only.

Region Pack fields that appear mutable in meaning, including entity state, entity knowledge, relationships, economy, security, and population, remain immutable seeds or static data until a future sprint explicitly migrates their runtime ownership into `world_state` or another persistent simulation-owned structure. They must not be treated as mutable runtime truth merely because they are projected into a Scene Snapshot.

Scene Snapshots are derived views built from Region Pack data plus `world_state`. Scene Snapshots are not persistent state.



## Simulation Model Boundary

`docs/simulation_model.md` describes how the world should conceptually behave. It is the behavioral counterpart to this architecture document.

Architecture describes implemented or scheduled software structure.

Simulation model describes conceptual world behavior such as truth, knowledge, pressures, affordances, time, perception, routine abstraction, and AI responsibility.

Concepts in `docs/simulation_model.md` do not become implementation requirements until scheduled by a sprint.

## Phase 2 Direction

Phase 2 remains **World Evolution Foundations**.

Phase 1 established world representation. Sprint 9 completed the first Phase 2 milestone by establishing durable world memory, explicit simulation-owned time advancement, bounded historical context, and safe narration boundaries.

Sprint 9 is closed as **World Memory and Safe Narration Foundations**. It completed history and time prerequisites but did not complete World Evolution Foundations as a whole. Persistent unresolved threads, time-based pressure drift, runtime actor state, actor knowledge, evidence, consequences, schedules, affordances, and opportunity surfacing remain future capabilities.

Sprint 10.1 closed the first Phase 2B capability: **Persistent Resolved Conversation Memory**. The subsequent architecture and scope review selected **Persistent Scoped Pressure Representation** as Sprint 10.2. Sprint 10.2 is complete and closed out.

The implementation keeps the existing `GameEngine` command path intact: `Interaction Kernel -> GameEngine -> current-scene target resolution -> World Update -> world_state.history`. A successful resolved conversation becomes a durable accepted event only when the normal command path succeeds and target resolution returns a resolved entity with stable identity.

Major feature systems such as combat, companions, economy simulation, faction warfare, full NPC AI, and full travel simulation remain deferred until the underlying world-evolution foundations exist.

Sprint 10.2 establishes a representation-only ownership boundary. Current pressure state belongs in a persistent `world_state.pressures` dictionary keyed by stable pressure identity. `initial_pressures` is the exact optional top-level Region Pack field for immutable seeds. If present, it is a validated list of exact pressure records; Region Pack provenance must identify the containing pack's exact `region_id`. Seeds are deep-copied only during new-game construction.

Canonical runtime World State always requires the pressure dictionary. During loading only, copied version-1 legacy save data missing `pressures` normalizes to an empty dictionary before strict validation and engine construction. This normalization does not modify or reapply Region Pack seeds. A present malformed pressure value fails validation, and save version 1 remains unchanged.

The initial pressure contract supports region and location scopes, an integer level from 0 through 100, and Region Pack provenance. The exact read boundary is `GameEngine.get_pressures()` for the complete keyed dictionary and `GameEngine.get_pressure(pressure_id)` for one copied record or `None`. Both return defensive deep copies without state, time, history, or scene-rebuild effects. The required `pressures` CLI command routes through `get_pressures()` and never accesses durable state directly. Mutation, history of pressure changes, time drift, projection, AI creation, unresolved-thread representation, and generic ongoing-condition frameworks remain outside Sprint 10.2.

Sprint 10.2 is complete. The verified implementation covered the representation-only boundary, the Region Pack seed contract, load-only legacy normalization, and read-only pressure inspection.

Sprint 10.3 adds the exact gameplay-facing operation `GameEngine.set_pressure_level(pressure_id, new_level)`. It accepts an exact level rather than a delta. Pure pressure mutation remains in or near `engine/pressure_state.py`, while `GameEngine` prepares a copied candidate world state, adds exactly one engine-identified `pressure_changed` history entry for a material change, validates the completed candidate, and commits pressure and history together through one final assignment. Validation or history failure commits neither. A no-op creates no history and does not replace durable state. The entry records current durable time without advancing it and records pressure scope rather than player location. The operation does not rebuild scene state or invoke narration.

Sprint 10.4 adds the linked pressure-transition operation `GameEngine.set_pressure_level_from_event(pressure_id, new_level, source_history_id)`. The source history entry is already durable, is referenced by stable `history_id`, and remains read-only outside the pressure-consequence commit. `engine/world_state.py` performs narrow backward-only referential-integrity validation for `source_history_id`, while `GameEngine` resolves the source entry, orchestrates copied candidate state, reuses the exact pressure-mutation boundary, constructs the linked `pressure_changed` history entry, validates the completed candidate, and commits once. A material change mutates one pressure and records one linked consequence atomically. A validated no-op confirms the source reference, returns without durable mutation, and creates no history. Existing unlinked history, including Sprint 10.3 pressure history, remains valid through save/load. Pressure state still remains unprojected into scenes, perception, narration, and autonomous simulation.

Sprint 10.5 adds the strict optional Region Pack field `conversation_pressure_effects`. Each exact declaration maps one `target_entity_id` that resolves to exactly one Region Pack entity to one existing seeded `pressure_id` and one integer `new_level` from 0 through 100. Region Pack data owns this immutable policy; Region validation owns exact shape, uniqueness, identifier, range, and cross-reference validation before gameplay. The Interaction Kernel, World Update, Pressure State, and World State remain unaware of effect policy.

For a matching resolved conversation, `GameEngine` copies durable world state, adds the normal `player_conversation` source first, captures its engine-owned `history_id`, resolves the one declaration, and uses a private non-committing form of the Sprint 10.4 linked-transition logic to prepare the exact pressure mutation and linked `pressure_changed` consequence in the same candidate. It validates the completed candidate and builds the required candidate scene before assigning live world state once and replacing `scene_snapshot`. An unmatched conversation remains source-only. A matching same-level conversation commits its new source but creates no consequence history. Save version 1 persists the resulting pressure and causal history without persisting or replaying Region Pack declarations.

This first automatic gameplay-event-to-pressure-consequence path remains deliberately bounded. It does not add generic effect rules, multiple consequences, deltas, predicates, ordering, event replay, schedulers, autonomous progression, pressure projection, narration coupling, runtime pressure creation, actor state, unresolved threads, or new commands.

Sprint 10.6 adds the canonical read-only pressure-applicability boundary. `engine/pressure_state.py` owns the pure operation: it validates the pressure collection, filters only records whose region scope exactly matches the loaded Region Pack `region_id` or whose location scope exactly matches the requested location, deep-copies the results, and orders them by sorted `pressure_id`. It remains independent of player movement, Region Pack scenes, history, narration, perception, and runtime effects.

`GameEngine.get_applicable_pressures(location_id=None)` is the gameplay facade. It resolves an omitted identifier from the player's durable current location, rejects non-string, empty, and non-canonical explicit locations, delegates scope filtering to the pressure-domain operation, and returns the copy-safe result without modifying world state, pressure state, history, time, weather, Region Pack data, player location, or the scene snapshot. Applicability is scope membership only; it does not imply activity, visibility, perceptibility, importance, narration eligibility, or escalation eligibility.

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
- Narration pipeline stub
- Deterministic narration candidate-source boundary
- Deterministic narration request packet contract
- Deterministic narration prompt packet contract
- Strict narration source-result validation contract
- Deterministic structured skill checks
- Structured skill-check command routing
- Scene-bound target resolution
- Known-destination resolution without travel execution
- Persistent scoped pressure representation
- Explicit atomic pressure-level change with durable history
- Causally referenced pressure transition

## In Progress

- Phase 2 - World Evolution Foundations

## Post-Sprint-9 Architecture Review

The post-Sprint-9 architecture review reached these decisions:

- Sprint 9 is complete. Do not assume or define Sprint 9.14.
- The completed milestone is **World Memory and Safe Narration Foundations**.
- The narration context, request, prompt, source, source-result, output, and preview boundaries are sufficient for the current deterministic preview.
- Narration infrastructure should remain frozen except for defect correction or changes required by an immediate bounded consumer.
- Real AI provider integration is deferred. It is not required for history, time, pressures, actor state, evidence, consequences, schedules, travel, or other simulation-owned capabilities.
- The immediate next project activity is a focused playable vertical-slice review, not a feature sprint.
- After that review, the next implementation should begin a new Phase 2B milestone rather than extending Sprint 9. Persistent scoped pressures or unresolved threads are the leading candidate, subject to the vertical-slice findings.

`GameEngine` remains the appropriate gameplay-facing facade. Its command routing should continue to grow only through bounded capabilities. Do not introduce a command bus, provider registry, plugin framework, dependency-injection framework, or broad handler abstraction without an immediate consumer.

## Known Architectural Debt

The following issues are real but do not block later bounded reactive-world capabilities:

- The untrusted narration candidate and the enriched validated narration result currently use the same narration-output schema and version despite having different supported shapes. Separate or version these contracts before real provider integration.
- Narration preview packets repeat substantial context through request, prompt, source-result, candidate, validated-output, and display fields. Preserve the current tested boundary for now and simplify only when a real provider or runtime consumer demonstrates the required shape.
- Request and prompt validation are not uniformly exact at every nested level. Reassess exact-field behavior before external packet producers are introduced.
- Runtime ownership of actor state, actor knowledge, relationships, economy, security, and population remains unresolved. Resolve ownership before implementing actor knowledge, schedules, or pressure-driven mutation of those values.
- The current elapsed-hours clock is sufficient for narrow deterministic pressure drift but not for schedules, calendar-sensitive behavior, or substantive travel duration.

## Architecture Boundary

Architecture describes systems that exist now or are scheduled for implementation.

Broader world-behavior ideas belong in `docs/simulation_principles.md`.

Ideas that are important but not ready for implementation belong in `docs/future_design.md`.


## Persistence

Only `world_state` is persisted. Region Packs remain immutable assets. Scene Snapshots, Perception, and Narration are regenerated after loading.

Sprint 10.15 hardens the existing unresolved-thread boundary without changing its ownership or save version. Region-aware World State validation now requires each persisted open thread to match the singular active declaration, a prior `player_conversation` targeting that declaration's trigger actor, and exactly one later `unresolved_thread_opened` record with matching identity, `open` status, and source history identifier. Malformed state fails before engine replacement or candidate commit. Lifecycle records remain durable and engine-queryable, but the narration-context projection excludes them alongside existing internal pressure and actor consequence records; location-aware perception remains unchanged.

Sprint 10.16 establishes `world_state.actor_knowledge` as sparse current membership keyed only by stable static actor identity. Immutable Region Pack `knowledge` arrays are validated new-game seeds and are deep-copied only during new-game construction. Version-1 saves missing the field normalize to empty membership during loading and never reseed from Region Pack content. Region-aware validation rejects malformed membership, unknown or unsupported actor identities, duplicate identifiers, and nested metadata. `GameEngine.get_actor_knowledge(actor_id)` returns an immutable tuple without adding knowledge to scenes, perception, narration, prompts, targeting, dialogue, or behavior.

Sprint 10.17 adds the exact `GameEngine.add_actor_knowledge(actor_id, knowledge_id)` transition. It prepares a copied candidate, validates the static actor and non-empty identifier, appends one absent identifier to sparse membership, adds one `actor_knowledge_added` durable history entry, validates the completed candidate against the active Region Pack, and assigns World State once. Duplicate additions are no-ops that preserve live World State and the Scene Snapshot. The history record remains queryable but is excluded from narration context; this transition does not project knowledge or introduce acquisition policy, source, certainty, truth, provenance, evidence, dialogue, or behavior.

Sprint 10.14 adds `world_state.open_threads`, a sparse dictionary keyed by immutable Region Pack thread identity. Each record contains exactly its identity, the sole supported status `open`, and the stable `created_by_history_id` for the accepted conversation that opened it. The reference must resolve to durable history. During loading only, version-1 saves missing `open_threads` normalize to an empty dictionary; authored declarations are not replayed. Region Pack content owns each thread's description, trigger actor, perception locations, and evidence text.

`GameEngine` composes a matching resolved conversation, existing bounded consequences, one open-thread record, and an `unresolved_thread_opened` history event in one candidate state. Validation and scene rebuilding complete before one live commit. Repeating the trigger does not duplicate the record or opening event.

Open-thread perception is derived and read-only: it returns authored evidence only at a declared applicable location. It exposes no objective, completion instruction, map marker, status label, raw runtime record, actor knowledge, or resolution behavior.

Every future persistent world-state expansion must define default initialization and compatibility for saves created before the new field existed. A broad migration framework is not required in advance, but compatibility must be explicit in the sprint that adds the field.

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

`world_state.history` now also records resolved-conversation events when the normal command path succeeds and scene target resolution identifies a resolved entity. Sprint 10.1 conversation entries use the existing engine-owned `history_id`, record the resolved target identity from deterministic target resolution rather than raw player text, and store only the durable fact that a conversation was initiated.

Those entries add `target_entity_id` and `target_display_name` alongside the existing history fields. They do not establish dialogue content, topics, claims, promises, actor knowledge, beliefs, relationships, emotional state, consequences, pressures, or time advancement.

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

`GameEngine.get_narration_preview(...)` exposes a deterministic narration pipeline stub that sequences the narration context and narration output boundaries through a fixed sample candidate. Sprint 9.9 packet shape is:

- `schema`: `ai_rpg.narration_pipeline_packet`
- `version`: `1`
- `accepted`: whether the fixed sample candidate validated successfully
- `source`: `fixed_sample_prose`
- `narration_context`: a copied narration context packet
- `candidate`: the fixed candidate that was validated
- `validated_output`: the validated narration output packet when accepted
- `display_text`: validated text copied from the narration output contract

The pipeline stub consumes narration context, supplies fixed sample prose only, validates that prose through the narration output contract, and returns a dedicated preview/display packet. It does not generate prose from player input or world data, does not call an AI model, does not replace gameplay narration, and does not persist narration output. The preview display is a copy-safe stub boundary, not a narration authority. If the fixed candidate is rejected, the packet reports the failure before any display text is returned.

The preview command may display the validated fixed sample text, but the displayed text is not accepted world truth. It remains presentational only and does not create history, advance time, mutate state, or alter saved data.

`GameEngine.get_narration_preview(...)` now routes candidate production through a deterministic narration candidate-source boundary. Sprint 9.10 packet shape is:

- `schema`: `ai_rpg.narration_pipeline_packet`
- `version`: `1`
- `accepted`: whether the candidate source produced a valid candidate and the output validator accepted it
- `source`: `fixed_sample_prose`
- `narration_context`: a copied narration context packet passed to the source
- `source_result`: the untrusted source result copied from the candidate boundary
- `candidate`: the untrusted narration-output candidate copied from the source result
- `validated_output`: the validated narration output packet when accepted
- `display_text`: validated text copied from the narration output contract, or empty text on failure
- `failure_stage`: bounded failure category when the source or validation fails
- `error`: bounded diagnostic text when the source or validation fails

The candidate source receives narration context rather than mutable world state. Source output is untrusted and must pass through `validate_narration_output_packet(...)` before any display text is returned. Raw source text is never displayed directly. If the source raises, returns a malformed result, or produces an invalid candidate, the pipeline fails closed with empty display text.

Failed candidate production does not mutate state, advance time, create history, persist narration, or interrupt normal deterministic gameplay. The deterministic fixed-sample source remains the only implemented source. No AI provider, prompt system, or external service exists yet.

`GameEngine.get_narration_preview(...)` now also routes the fixed source through a deterministic narration request packet. Sprint 9.11 packet shape is:

- `schema`: `ai_rpg.narration_request_packet`
- `version`: `1`
- `mode`: `preview`
- `narration_context`: a copied narration context packet
- `expected_output`: the expected narration-output schema/version and output contract metadata
- `constraints`: stable machine-readable narration constraints

The request packet is provider-neutral, read-only, and copy-safe. It is built only from the already bounded narration context and fixed contract metadata. It contains no provider-specific system messages, user messages, credentials, or payload formats, and it grants no simulation authority. The pipeline validates request structure before invoking the source, then validates the returned candidate through the existing output contract before display. Request-construction or request-validation failure fails closed with empty display text. The request does not access mutable world state directly, does not add full durable history, and does not persist requests or source results.

`GameEngine.get_narration_preview(...)` now also routes the validated request through a deterministic narration prompt packet before the fixed source. Sprint 9.12 packet shape is:

- `schema`: `ai_rpg.narration_prompt_packet`
- `version`: `1`
- `mode`: `preview`
- `originating_request`: the validated narration-request packet schema, version, and mode
- `expected_output`: the expected narration-output schema/version and prose-only format guidance
- `instructions`: provider-neutral narration rules that preserve simulation authority, prose-only output, and fail-closed behavior
- `deterministic_input`: a copy-safe deterministic representation of the bounded narration request input

The prompt packet sits between the validated narration request and the untrusted fixed source. It is constructed only from the validated request packet, remains copy-safe, and preserves deterministic request data without retaining live mutable references. Prompt validation occurs before source invocation. The fixed source receives the prompt packet rather than raw context, raw world state, or raw request data. The source remains deterministic and continues returning only the existing sample prose.

Prompt construction or validation failure fails closed with empty display text. The source output still passes through `validate_narration_output_packet(...)` before display, so prompt failure and source failure remain distinct from output validation. The preview sequence is therefore:

1. Build bounded narration context.
2. Build and validate the narration request packet.
3. Build and validate the narration prompt packet.
4. Pass the prompt packet to the fixed candidate source.
5. Validate the returned candidate through the narration-output contract.
6. Expose display text only after successful validation.

The prompt packet does not introduce simulation authority, persistence, provider integration, model settings, retries, streaming, or raw world-state access. If the prompt or source path fails, display text stays empty and the preview remains non-authoritative.

`GameEngine.get_narration_preview(...)` now also routes the validated prompt through a strict narration source-result validation boundary before candidate extraction. Sprint 9.13 packet shape is:

- `schema`: `ai_rpg.narration_source_result`
- `version`: `1`
- `source`: `fixed_sample_prose`
- `source_prompt`: the validated narration-prompt packet that was supplied to the source
- `candidate`: the untrusted narration-output candidate copied from the validated source result
- `metadata`: exact fixed metadata containing `candidate_trust: untrusted` and `generation: fixed_sample_only`

The source-result envelope is untrusted until it passes strict validation immediately after source invocation. Validation accepts only the documented top-level fields, rejects unsupported extras, requires the source prompt to validate and match the originating validated prompt, and enforces exact metadata values. Validation returns a deep copy so callers cannot mutate the supplied source result or originating prompt through the validated packet.

Candidate extraction occurs only from the validated source-result packet. That means the pipeline first validates the complete source-result envelope, then extracts the candidate, and only then validates candidate prose through the existing narration-output contract. Source-result validation failure is distinct from candidate-output validation failure.

Failed source-result validation uses a bounded `source_result_validation` stage, returns empty display text, and does not copy malformed raw source payloads into preview inspection fields. Raw invalid candidate prose is not copied into source-result-validation failures. The fixed source remains deterministic and still returns only `The street remains quiet.` The source-result boundary does not add simulation authority, durable facts, provider integration, or world-state mutation.

`world_state.time` can be advanced by an explicit simulation-owned operation. Sprint 9.2 supports a narrow fixed-duration `wait` command that increments durable elapsed time by one hour and records the previous and new time in history. This operation does not trigger world evolution, pressures, schedules, travel duration, recovery, decay, escalation, opportunity loss, or autonomous NPC behavior.

## Session Lifecycle

## Persistent Static Actor Location

Named static actors remain authored in the Region Pack. World State owns only sparse `actor_location_overrides`, keyed by the existing stable `entity_id`. One canonical resolver chooses the runtime override when present and otherwise the authored location; scene construction uses that boundary so downstream perception and target resolution naturally reflect movement. Spawned templates remain independent derived scene content. Material actor movement and the rebuilt current scene commit together only after candidate validation succeeds.

Sprint 10.12 permits one optional immutable `conversation_actor_relocation_effect` declaration. A matching resolved conversation prepares its durable conversation source, any material actor move and backward causal reference, completed World State validation, and one rebuilt scene before the existing single live commit. A repeated matching conversation remains durable but creates no false movement when the actor is already at the destination. This is a bounded content policy, not a generic consequence dispatcher.

Sprint 10.13 adds one optional immutable `elapsed_time_actor_relocation_effect`. Its exact declaration names one elapsed-hour threshold, one seeded named static actor, and one known destination. The existing `advance_time` candidate transition evaluates the same crossing rule used by elapsed-time pressure consequences, then prepares any material `actor_moved` entry after the pressure consequence and links both to the same `time_advanced` source. Durable elapsed time and effective actor location provide one-shot behavior without a fired flag. Final World State validation, scene construction, and live publication remain singular; `wait` continues using that shared boundary.

## Elapsed-Time Pressure Consequence

## Authored Pressure Observation

Sprint 10.9 adds one derived, non-persistent observation cue. Canonical applicability is necessary but not sufficient: one validated immutable Region Pack declaration names the pressure, minimum level, and authored text. `GameEngine` derives the cue on perception reads and passes only cue identity, pressure identity, and text to perception. Raw pressure state never enters the Scene Snapshot or perception.

Sprint 10.10 carries that already-derived zero-or-one cue through the existing deterministic narration context, request, and prompt boundaries. Perception remains the only authority for applicability, threshold, and perceptibility. Narration packets receive only cue identity, pressure identity, and exact authored text; pressure-change history records are excluded from narration context so raw levels, scope internals, and causal identifiers do not leak through bounded history. After the existing source-result and candidate-output validation succeeds, the engine deterministically composes the exact cue into validated display text exactly once. Empty-cue behavior is unchanged, failure output remains empty, and no narration artifact is persisted.

Sprint 10.7 completes the Sprint 10.5 through 10.7 pressure capability cluster: one declared conversation consequence, canonical read-only pressure applicability, and one declared elapsed-time consequence. One optional immutable Region Pack declaration, `elapsed_time_pressure_effect`, may target one seeded pressure and one exact level. `GameEngine.advance_time` evaluates it only when accepted advancement satisfies `previous_elapsed_hours < trigger_elapsed_hours <= new_elapsed_hours`. Time calculation remains pure in `timekeeper`; declaration validation belongs to `region_validator`; pressure preparation remains in `pressure_state`.

The engine prepares time, the `time_advanced` source record, any material linked `pressure_changed` consequence, validation, and the rebuilt scene against a copied World State before committing World State and scene once. A same-level target is a validated consequence no-op: time and source history commit, but pressure history does not. Durable elapsed time supplies one-shot behavior, so no fired flag or other persistence field exists.

Sprint 10.8 corrects command orchestration to conform to ADR-041: a successful `wait` returns immediately after `advance_time`, so the command performs no generic interaction application and has exactly one validation, one scene build, and one live commit boundary.

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

Sprint 9.9 adds a narrow `narration preview <player input>` review path for the deterministic narration pipeline stub. Front ends may inspect the preview packet or display the fixed sample prose returned by the pipeline, but they must not treat it as generated narration, introduce provider integration, persist narration, or trigger world evolution.

Sprint 9.10 adds a deterministic narration candidate-source boundary beneath the preview path. Front ends may still inspect the preview packet or display the validated fixed sample prose, but source output is now treated as untrusted until the existing narration output contract accepts it. Source failures, malformed results, and invalid candidates fail closed without display text, state mutation, history creation, or time advancement.

Sprint 9.11 adds a deterministic narration request packet between narration context and the candidate source. Front ends may still inspect the preview packet or display the validated fixed sample prose, but the candidate source now receives the request packet rather than raw narration context. Request-construction and request-validation failures fail closed without display text, state mutation, history creation, or time advancement.

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
