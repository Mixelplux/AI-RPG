# Roadmap

## Completed Foundation

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

The architecture and scope review selected persistent scoped pressure representation as Sprint 10.2. Sprint 10.2 is complete and closed out.

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
   - One deterministic engine-owned operation changes one pressure.
   - The accepted change is recorded in durable history.

4. **Pressure change from one accepted gameplay event**
   - One bounded player or simulation action affects one known pressure.

5. **Narrow time-based pressure drift**
   - One explicitly configured pressure can increase, decay, or remain stable after elapsed time.
   - No generalized scheduler or world tick framework.

6. **Pressure projection into scene or perception**
   - Relevant scoped pressure state becomes observable where the simulation permits it.

7. **Runtime actor-state baseline**
   - Establish persistent ownership for mutable actor location or state without implementing full NPC AI.

8. **Actor knowledge baseline**
   - One actor can know, not know, or hold an outdated or false belief about a referenced event.

9. **Evidence and consequence chain**
   - One bounded action leaves one persistent trace that one eligible actor can discover and respond to.

10. **Opportunity surfacing**
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

Active sprint definitions must include:

- Goal
- Expected Files
- Acceptance Criteria
- Verification

Work on only one sprint at a time. Do not begin the next sprint automatically.

