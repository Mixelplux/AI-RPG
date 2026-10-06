# World Simulation — Design Manifest

## Status

- Overall: **Partial** — bounded authoritative state and causal transitions exist.
- Last materially reviewed: October 5, 2026, implementation baseline
  `51f595b5c8516ef242a4fffeb246c0e143acc9b3` (`feat: add scene context v1`).
- Relevant milestones: [10.79 causal follow-through](../../sprint_10_79_handoff.md),
  [10.80 Scene Context](../../sprint_10_80_handoff.md), ADR-059 through ADR-061
  in the [decision ledger](../../decisions.md).

This is a living model under the [shared documentation rule](README.md).
Accepted design and provisional decomposition do not claim generalized runtime
support or authorize implementation.

## Purpose

Maintain authoritative external reality: what is true now and how that truth can
legitimately change.

## Player-facing goal

Enable coherent places, travel, conditions, continuity, and intelligible
consequences that persist beyond the scene currently being played. The world
can respond without manufacturing drama or requiring exhaustive bookkeeping.

## Authority

Accepted responsibility includes current external world truth, fictional time,
environmental conditions, location and spatial relationships, physical and
accessibility state, resulting external consequences, non-intentional causal
processes, ordinary offscreen reconciliation, and material history/provenance
where future reasoning requires it. These responsibilities have different
implementation depths, recorded below.

Simulation authority over consequential truth is an existing contractual
boundary. AI/provider output is untrusted and has no simulation authority.
Persistent transitions preserve the established validation and publication
boundary; the persistence implementation limitation below remains explicit.

Canonical/authored content defines initial or normal conditions. Once legitimate
campaign change occurs, live campaign state is authoritative over original
canonical/default state for that campaign. This is implemented for supported
mutable fields and overlays, not as a universal content override mechanism.

## Explicit non-authority

World Simulation does not own player intent; player-character capability or
memory; meaningful intentional NPC/faction decisions; action adjudication
requiring Action & Resolution; narration/presentation; or authored player
outcomes. Meaningful intentional NPC/faction decisions belong to Actors & Social
Dynamics under the current responsibility model.
Once an actor's action occurs, its resulting external truth belongs here.
This distinction holds even though no separate autonomous actor subsystem exists.

## Governing principles

Reference the [shared doctrines](README.md#shared-doctrines), Story-First Part I,
and ADR-059 rather than independently redefining them.

- Offscreen does not mean frozen or continuously simulated. Most mundane
  background activity remains inferred; later relevance can justify lazy resolution.
- Lazy reconciliation begins after the last authoritative established state.
  It may not retroactively contradict observed or otherwise established history.
- The more consequential, specific, or player-established a fact becomes, the
  stronger the causal justification required to change it.
- Causal progression executes established relationships; narrative interest
  alone is not a cause and does not justify inventing a dramatic event.
- Preserve enough provenance for material changes when prior state or cause may
  matter later. Do not prescribe exhaustive event sourcing.

Major destruction, important ownership changes, consequential repairs, exposed
secrets, important relocations, and player-established alterations may justify
history. Routine inventory churn, ordinary maintenance, and moved furniture
normally do not. These examples guide future design, not existing schemas.

## Current model

The following decomposition is **Provisional** conceptual structure, not a claim
that corresponding runtime modules already exist:

| Responsibility | Present grounding |
|---|---|
| Current World State | Validated mutable state and bounded authored overlays |
| Environment & Time | Stored weather/time; elapsed-hour advancement |
| Space & Travel | Authored macro graph and bounded traversal |
| Causal Progression | Declared effects and fixed West-Road follow-through |
| Active Processes / Pressures | Pressure levels and one tracked reduced-coverage interval |
| Material Change History | Durable typed history and backward causal references |
| Dormant-State Reconciliation | Accepted direction; no generalized runtime mechanism |

## Resolution depth

Use inference first, then lazy resolution, explicit persistent state, and active
simulation only as justified by relevance and consequence. An ordinary background
worker does not become an individually simulated actor because their activity
could explain a changed place. Independent intentional agency, if consequential,
still belongs to Actors & Social Dynamics under the current responsibility model,
regardless of detail depth.

**Design example:** a hidden sewer entrance was last established as concealed
and usable. Six months later, relevant inputs could include elapsed time, ordinary
local activity, structural stability, concealment, maintenance, player traces,
and active pressures. Its current condition might be still hidden, discovered,
or sealed, with adequate causal justification and no contradiction of established
history. Do not instantiate the discovering worker unless their individual
intentional action becomes independently consequential. The runtime does not
currently implement this generalized reconciliation.

## State and lifecycle

**Implemented:** new-game state copies supported initial content. Commands
prepare candidate state, apply supported effects, validate, rebuild the scene,
and publish. Read-only projection does not establish the market incident.
Saved state is restored and validated against content; derived scenes are rebuilt.
History records supported events and stable causal references; it is not a
general reconstruction of all world truth.

**Accepted design:** inferred ordinary background activity needs no ledger.
For a matter that has become dormant, the last authoritative established state
remains the reconciliation boundary; later relevance can justify resolving what
has changed since that point. This principle does not prescribe a separate
dormant-state data structure. Persistent material facts constrain
future change. Active processes earn explicit tracking by consequential need.
General inference, dormant reconciliation, and promotion between specificity
levels are not implemented lifecycle machinery.

## Inputs

- Validated Region Packs: initial fields, locations/connections, constraints,
  and supported authored declarations.
- Validated live campaign state and established history.
- Accepted engine interactions and elapsed-time transitions, including bounded
  competence outcomes whose resolution is owned elsewhere.
- Future intentional actor actions: provisional interface, not current
  autonomous decision input. Untrusted narration is not an authoritative input.

## Outputs

- Current external truth and accepted changes with relevant history references.
- Location, conditions, supported evidence/actor positions, and local consequences
  for perception, action eligibility, scenes, and narration context.
- Validated runtime state for persistence. Player-safe projection is derived;
  hidden internal facts are not automatically available to the character.

## Relationships

See the [system map](system-map.md#dependencies-and-information-flow-around-world-simulation).
Scenario & Authored Content provides foundations; Action & Resolution adjudicates
attempts; Character System constrains capability and informational access;
Meaningful intentional NPC/faction decisions belong to Actors & Social Dynamics
under the current responsibility model; Narrative Experience and
Player Presentation express safe facts; Persistence saves/restores state.
Current orchestration and storage cross these conceptual responsibilities without
settling future module boundaries.

## Player-facing projection

Truth, perception, familiarity, and acquired information/belief remain distinct.
World State storage does not imply player knowledge. Sprint 10.79 establishes an
incident independently of observation and reveals it locally at Market Square;
remote West-Road status is filtered from that scene. Explicit clue review remains
separate. Sprint 10.80 consumes authoritative local facts/conditions and permits
compatible low-consequence expression without promoting it into world truth.

Internal route resolution can be finer than narrated travel. Accepted longer-term
Space & Travel direction is origin → destination/traversal intent → valid broad
route → fictional travel cost/time → meaningful interruption if any → destination.
The directional graph is not the intended final spatial abstraction. Rooftop,
sewer, and wilderness traversal do not inherently need exhaustive tiles/nodes.

## Current implementation

| Capability | Classification and evidenced limit |
|---|---|
| World/location state | **Implemented, bounded:** player location, weather/time, history, pressures, actor-location overrides, traces and scenario state. Locations, descriptions and connectivity remain authored. No general mutable physical/accessibility model. |
| Fictional time | **Partial:** positive integer hour advancement updates `elapsed_hours`, records a time event and invokes supported effects. `timekeeper` copies other fields unchanged; it does not advance a calendar, `time_of_day`, or weather. |
| Movement/connectivity | **Implemented, bounded:** directional/named connections and named-destination graph routing; route hops execute sequentially. One declared West-Road exit traversal costs one hour atomically with its supported effects. General travel costs, interruptions and arbitrary local geometry are deferred. |
| Environment/world conditions | **Partial:** initial weather is copied into runtime state, saved, and projected; pressure levels have supported mutations. Economy, security and population in the scene remain authored Region Pack values. No general weather evolution, maintenance or condition simulation. |
| Campaign state over defaults | **Partial:** load retains supported runtime fields; actor-location overrides supersede authored positions; established scenario outcomes and incident alter projection. No universal override for every authored fact. |
| Persistence interface | **Implemented, bounded:** version-1 save envelope stores runtime state plus region path; load validates and rebuilds derived scenes. Missing additive fields have specific normalization, not generalized reconciliation. Revised Bryn Shander prototype state is rejected per ADR-060. Disk write atomicity is not established. |
| Causal follow-through (10.79) | **Implemented, fixed rule:** reduced coverage tracked only in `observers_withdrew` / `withdrawal_route_found`. Crossing two qualifying hours establishes one lamp-oil theft at interval start + 2, with a backward reference to the crossing time event, even in a larger step. Early restoration ends timing; later restoration preserves an existing incident. No thief identity, motive, conspiracy, autonomous actor, or general causal framework. |
| Other time effects | **Implemented, declared slices:** supported threshold declarations can change a pressure, relocate one actor, or add an evidence trace in the existing time transaction. Mechanism tests include a test-only legacy fixture; they do not imply all declarations remain active in revised Bryn Shander play. |
| Scene Context (10.80) | **Implemented projection:** local location facts, copied weather/time, declared intention and locally filtered competence enter validated narration inputs. Market-specific expected activity constrains commerce by conditions; other locations have unspecified compatible activity. This is a presentation bound, not crowds, schedules or economy simulation. |
| Presentation carry-forward (10.80) | **Partial, outside world authority:** bounded session-only descriptive continuity and orient/expand/follow/narrow stages reduce repetition. Location change and successful load/reset clear presentation memory; nothing is saved or promoted to world truth. No universal long-term continuity guarantee. |
| Material history / active processes | **Partial:** typed history with stable IDs and causal links, pressure records and a specific coverage interval exist. No exhaustive event sourcing, generalized scheduler, history summarizer or dormant-process reconciler. |

## Accepted decisions

External truth and legitimate causal change belong to simulation; generated
expression has no consequential authority. Mutable campaign truth takes priority
for supported established changes. Minimum sufficient detail, ordinary offscreen
inference, forward-only reconciliation, material provenance, and stronger
justification for reversing invested facts preserve accepted Story-First and
ADR-059 direction. Existing atomic candidate transitions and save compatibility
remain safeguards. Broader travel abstraction is accepted direction, with
mechanisms unsettled. None of these statements schedules new capability.

## Provisional decisions

The seven-part decomposition and future actor/world interfaces are revisable.
The exact inputs, policy, and representation for dormant reconciliation remain
open; the sewer example does not select an algorithm or persistence schema.
No new history format, condition taxonomy, spatial framework, or ownership
storage split is selected here.

## Deferred capabilities

Generalized lazy reconciliation, autonomous actors/factions, process scheduling,
weather/calendar evolution, broad physical change/repair modeling, general
travel cost/interruption resolution, and broader material-history retention
mechanisms remain outside this documentation task. No other system manifest,
runtime refactor, migration, or save-version change is authorized.

## Known tensions / open questions

- **Terminology:** `world_state` is a shared persistent container, including actor
  knowledge, discoveries and character competence. Its name does not mean World
  Simulation conceptually owns all stored data. This reconciles the runtime map
  with the new responsibility hierarchy without a refactor.
- **Older conceptual scope:** Simulation Model's World Evolution includes actor
  goals alongside processes. Treat this as a broad umbrella; meaningful
  intentional decision ownership is clarified by the system map. Its
  just-in-time concretization examples concern consequential truth; they do not
  require incidental narration detail to become persistent canon. Story-First's
  committed versus undecided truth distinction remains intact.
- **Older narration wording:** Architecture's preview-only/not-automatic summary
  predates Sprint 10.80's explicit CLI presentation/observation paths. The latest
  accepted handoff and implementation evidence describe those paths; narration
  still has no simulation authority. Historical reasoning is preserved.
- **Implementation gap:** elapsed hours can change while authored `time_of_day`
  remains fixed; Scene Context consumes supplied time rather than deriving a
  day/night cycle. No wider environment progression is inferred from that input.
- **Persistence gap:** candidate publication is guarded, but `save_game` directly
  opens the destination for JSON writing. This is not evidence of atomic disk
  replacement. Recording the gap does not authorize runtime repair.
- **Unsettled design:** future reconciliation needs enough provenance to respect
  established truth, without exhaustive logging. This review does not freeze a
  retention policy. No fundamental authoritative design contradiction was found.

## Evidence

Reviewed source and tests at the baseline; no gameplay suites or live providers
were run for this documentation review. Historical handoffs report their own
verification and owner play acceptance.

| Evidence | What it supports |
|---|---|
| [World State](../../../engine/world_state.py), [world update](../../../engine/world_update.py), [save system](../../../engine/save_system.py), [save/load test](../../../test_save_load.py) | Initialization, runtime state, persisted location/time/weather/history, restore limits |
| [Timekeeper](../../../engine/timekeeper.py), [GameEngine](../../../engine/game_engine.py), [interaction kernel](../../../engine/interaction_kernel.py) | Elapsed-hour changes, supported effect composition, graph routing and transition publication |
| [Timed traversal ADRs](../../decisions.md), [traversal test](../../../test_one_hour_west_road_exit_traversal.py), [navigation test](../../../test_navigation_projection.py) | Bounded travel costs and graph presentation |
| [Pressure effect test](../../../test_time_pressure_effect.py), [relocation test](../../../test_time_actor_relocation.py), [trace effect test](../../../test_time_evidence_trace_effect.py) | Narrow declared threshold mechanisms |
| [10.79 handoff](../../sprint_10_79_handoff.md), [theft rule](../../../engine/west_road_market_theft.py), [theft tests](../../../test_west_road_market_theft.py), [local relevance tests](../../../test_west_road_scene_relevance.py) | Threshold, idempotence, restoration, save/load, rollback, independent occurrence and local revelation |
| [10.80 handoff](../../sprint_10_80_handoff.md), [scene loader](../../../engine/scene_loader.py), [Scene Context](../../../engine/scene_context.py), [context tests](../../../test_scene_context.py), [continuity](../../../engine/scene_continuity.py) | Authoritative conditions consumption, compatible incidental freedom and bounded presentation continuity; owner accepted final three-turn smoke with minor weather repetition remaining |
| [Architecture](../../architecture.md), [Simulation Principles](../../simulation_principles.md), [Simulation Model](../../simulation_model.md), [Story-First Doctrine](../../story_first_design_doctrine.md), [ADRs](../../decisions.md) | Authority, minimum detail, truth/knowledge distinctions and preserved design reasoning |

## Revision history

- October 5, 2026: established the first manifest, separating conceptual ownership
  from shared storage and bounded implementation from accepted future direction.
