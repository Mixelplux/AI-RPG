# Roadmap

## Authored Resolved-Thread Actor Relocation — Complete

The Bryn Shander west-road thread now has one bounded durable world reaction: successful clue presentation sends the declared guard to the West Gate. Save version remains 1; no next package is selected.

## Completed Foundation

- Authored Actor-Knowledge Conversation Response — complete pending package review.

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

## Phase 2 — World Evolution Foundations

### Goal

Establish the minimum simulation structures required for the world to remember, evolve, and present meaningful opportunities without relying on AI invention.

Phase 1 taught the engine to represent the world.

Phase 2 teaches the engine to remember and evolve the world while preserving simulation-owned truth.

### Phase 2.0 — Simulation Model Baseline ✅

Completed through the post-Sprint-8 Project Review and Simulation Design Summit.

Established:

- `docs/simulation_model.md`
- Updated simulation principles
- AI/simulation authority boundaries
- Phase 2 direction
- Governance that conceptual design does not become implementation until scheduled

### Phase 2A — World Memory and Safe Narration Foundations ✅

Completed through Sprint 9.13.

#### World memory and time

- Sprint 9.1 — World History Skeleton ✅
- Sprint 9.2 — Time Advancement Operation ✅
- Sprint 9.3 — Read-Only History Query ✅
- Sprint 9.4 — Bounded History Query Guardrails ✅
- Sprint 9.5 — Stable History Entry Identity ✅
- Sprint 9.6 — Bounded History Context Packet ✅

#### Safe narration boundaries

- Sprint 9.7 — Narration Context Boundary ✅
- Sprint 9.8 — Narration Output Contract ✅
- Sprint 9.9 — Deterministic Narration Pipeline Stub ✅
- Sprint 9.10 — Deterministic Narration Candidate Source Boundary ✅
- Sprint 9.11 — Deterministic Narration Request Packet Contract ✅
- Sprint 9.12 — Deterministic Narration Prompt Packet Contract ✅
- Sprint 9.13 — Strict Narration Source Result Validation Contract ✅

Sprint 9 is complete. No Sprint 9.14 is required.

---

## Current Transition

Sprint 9 is complete as **World Memory and Safe Narration Foundations**.

The post-Sprint-9 architecture review is complete.

The playable vertical-slice review is complete. It confirmed that movement and waiting are remembered, and Sprint 10.1 confirmed that resolved conversations are now remembered as durable world history.

Phase 2B has begun with **Persistent Resolved Conversation Memory** complete as Sprint 10.1.

The architecture and scope review selected persistent scoped pressure representation as Sprint 10.2. Sprint 10.2 is complete and closed out. Sprint 10.3, explicit atomic pressure-level change with durable history, is complete and closed out. Sprint 10.4, causally referenced pressure transition, is complete and closed out. Sprint 10.5, one declared resolved-conversation pressure consequence, is complete and closed out. Sprint 10.6, read-only applicable pressures for one location, is complete and closed out. Sprint 10.7, one declared elapsed-hour threshold pressure consequence, is complete and closed out.

Phase 2B now includes one deterministic gameplay event automatically causing one linked pressure consequence and one canonical scope-aware read boundary for pressures applicable to an exact location. The next action is an architecture and scope review; no next capability or sprint has been selected.

Real AI provider integration remains deferred. It is not required for the next simulation capabilities and should not lead the roadmap merely because the provider-neutral narration boundary exists.

---

## Proposed Phase 2B - Reactive World State Foundations

**Status:** In progress

### Goal

Teach accepted events and elapsed time to produce persistent, scoped, simulation-owned change.

### Proposed capability sequence

This sequence is directional, not a sprint commitment. The playable vertical-slice review may adjust the first implementation choice.

1. **Persistent resolved conversation memory**
   - Complete in Sprint 10.1.
   - The world records that a resolved conversation occurred without inventing dialogue or changing unrelated state.

2. **Persistent scoped pressure representation**
   - Complete as Sprint 10.2.
   - The world can store a pressure with identity, region or location scope, bounded level, and Region Pack provenance.
   - Initial seeds use the exact optional top-level Region Pack field `initial_pressures`; provenance identifies the containing `region_id`.
   - Canonical runtime state requires `pressures`; version-1 legacy saves receive load-only empty normalization rather than retroactive seeding.
   - Initial implementation is representational, persistent, validated, and read-only through exact `GameEngine` methods plus the required `pressures` inspection command.
   - No global simulation sweep or AI-generated pressure creation.
   - Unresolved threads remain a distinct future concept rather than part of a generic combined abstraction.

3. **Explicit pressure change operation**
   - Complete as Sprint 10.3.
   - One deterministic engine-owned operation changes one pressure.
   - The accepted change is recorded in durable history.

4. **Causally referenced pressure transition**
   - One pressure consequence references one already accepted durable history event by stable history ID.
   - The source event is read-only and remains outside the pressure/history atomic commit.
   - Complete as Sprint 10.4.

5. **One declared resolved-conversation pressure consequence**
   - One strict Region Pack declaration maps one exactly resolved conversation target to one seeded pressure and one exact resulting level.
   - The source conversation event, linked pressure consequence, and resulting state commit atomically in one candidate world state.
   - Complete as Sprint 10.5.

6. **Read-only applicable pressures for one location**
   - Exact region and requested-location scope membership is exposed through one deterministic, copy-safe gameplay facade.
   - Complete as Sprint 10.6.

7. **Narrow time-based pressure drift**
   - One explicitly configured pressure can increase, decay, or remain stable after elapsed time.
   - No generalized scheduler or world tick framework.

7. **Pressure projection into scene or perception**
   - Relevant scoped pressure state becomes observable where the simulation permits it.

8. **Runtime actor-state baseline**
   - Establish persistent ownership for mutable actor location or state without implementing full NPC AI.

9. **Actor knowledge baseline**
   - One actor can know, not know, or hold an outdated or false belief about a referenced event.

10. **Evidence and consequence chain**
   - One bounded action leaves one persistent trace that one eligible actor can discover and respond to.

11. **Opportunity surfacing**
   - Relevant world state can become player-facing without being converted into a procedural quest.

## Prerequisites and Ownership Decisions

Before actor knowledge, schedules, or pressure-driven mutation of economy, security, population, relationships, or actor activity:

- Distinguish immutable Region Pack seeds from mutable runtime state.
- Define persistent runtime ownership for the affected data.
- Define save compatibility and default initialization for every new persisted field.

Before NPC routines or schedules:

- Add a canonical clock representation beyond elapsed hours.
- Establish persistent actor location and activity ownership.

Before real AI provider integration:

- Separate or version untrusted candidate-output and enriched validated-output shapes.
- Reassess exact request and prompt validation for external producers.
- Introduce a bounded provider adapter rather than generalizing the fixed-sample source contract prematurely.

---

## Narration Infrastructure Policy

The current deterministic narration preview boundary is complete enough for now.

Do not add another narration infrastructure sprint solely to introduce:

- provider registries
- plugin frameworks
- provider-specific payloads
- model configuration
- retries or fallback providers
- streaming
- caching
- token or cost accounting
- semantic hallucination detection
- additional packet layers

Narration infrastructure may resume when a real provider or another immediate bounded consumer is explicitly selected.

---

## Deferred Systems

The following systems remain important but should not lead the current Phase 2 transition:

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

These are future applications of World Evolution Foundations, not the foundations themselves.

---

## Sprint Rule

Deterministic Local Investigation and Evidence Discovery is complete through
the reconciled 10.27 through 10.30 package closeout. No following sprint or
capability package is selected.

Sprint 10.7 completed one declared elapsed-hour threshold pressure consequence with atomic causal history and no new persistent schema or generic scheduling infrastructure.

Sprint 10.8 completed the wait single-commit atomicity correction. Sprint 10.9 completed the first bounded pressure projection into perception through one authored observation cue. Sprint 10.10 carried that cue into deterministic player-facing narration without exposing raw pressure state or adding provider integration. Recurring or continuous pressure drift remains a distinct future capability.

Sprint 10.11 completed the persistent actor-location prerequisite: seeded named static actors can move through sparse durable overrides while retaining immutable Region Pack identity and authored baseline data. Spawned entities, schedules, autonomous behavior, and actor activity remain deferred. Sprint 10.12 is undefined and unstarted.

Sprint 10.12 connected one accepted resolved conversation to one Region-declared persistent actor relocation while preserving one candidate transition, causal history, and Scene Snapshot consumer boundaries. The capability adds no scheduler, autonomous behavior, generic effect framework, or new persistence schema. Sprint 10.13 is undefined and unstarted.

Sprint 10.13 adds one bounded elapsed-time actor relocation through the existing time-transition boundary. It does not introduce a schedule, recurrence, generic dispatcher, autonomous behavior, pathfinding, or a persistence-schema change.

Sprint 10.14 adds one declared conversation-triggered unresolved thread. The engine persists one sparse open record and causal history while projecting only local authored evidence; it adds no resolution, quest interface, objective, timer, or generic trigger system. Sprint 10.15 remains undefined and unstarted.

Sprint 10.15 hardens the declared thread's persisted identity and causal history, and isolates its internal lifecycle record from narration-facing history. It adds no new thread capability, persistence version, or ADR.

Sprint 10.16 establishes sparse persistent actor-knowledge membership for stable static actors. Immutable Region Pack arrays seed new games only; version-1 legacy saves missing the runtime field load empty and are not reseeded. Sprint 10.17 adds one explicit atomic knowledge-addition operation with durable lifecycle history while preserving the non-projection boundary. Sprint 10.18 adds a bounded structural reference from one addition to one already accepted durable source event; it adds no semantic source eligibility, belief model, acquisition policy, or player-facing projection. No following sprint is defined.

Sprint 10.19 composes one strict immutable resolved-conversation declaration with the accepted candidate transition. It may grant one opaque actor-knowledge identifier to one stable static actor using the new conversation entry as a structural causal source. It adds no conversation-text interpretation, knowledge projection, semantic source policy, or generic consequence system. No following sprint is defined.

Authored Resolved-Thread Observation and Integrity completed through Sprints
10.37 through 10.39. Resolved-thread records now require declared causal
lifecycle integrity before acceptance, and one exact authored local observation
is derived from valid resolved state for normal scene narration. No new
persistent field, save-version change, generic consequence system, or following
sprint is defined.

Active sprint definitions must include:

- Goal
- Expected Files
- Acceptance Criteria
- Verification

Work on only one sprint at a time. Do not begin the next sprint automatically.

## Sprint 10.49 - One Declared Elapsed-Time Evidence Trace Consequence

Status: Complete — ready for owner review. One strict elapsed-time threshold now composes a hidden, source-linked evidence trace with existing time pressure and actor relocation in one atomic candidate transition. Save version remains 1; no generic temporal or consequence framework is introduced.

## Sprint 10.52 - One Declared Discovery-Gated Relocated-Actor Response

Status: Complete — ready for owner review. One strict Elin-only discovery
response reads command-start West Gate discovery membership after a normal
local conversation commit. Captain Grey remains unchanged; save version 1,
singleton non-overlap, and hidden-state boundaries are preserved.

## Sprint 10.51 - One Declared Resolved-Thread Evidence Trace Consequence

Status: Complete — ready for owner review. One strict resolved-thread declaration adds a hidden,
source-linked evidence trace at the existing relocated actor's authored
destination during the successful west-road clue presentation. Existing local
investigation remains the sole player-facing discovery boundary; save version
remains 1. A discovery-gated relocated-actor response and all generic
consequence infrastructure remain deferred.

## Sprint 10.53 - One Declared Delayed-Watch Discovery Actor Recall

Status: Complete — ready for owner review. The existing second-hour Delayed
Watch Mark can return Captain Grey from the West Gate to the North Gate through
one exact atomic presentation path. No precedence, discovery consumption, new
persistence, or save-version change was added.

