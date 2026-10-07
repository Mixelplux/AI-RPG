# Scenario & Authored Content — Design Manifest

## Status

- Overall: **Partial** — Region Packs supply foundations and supported declarations;
  runtime interpretation is bounded and several scenario rules remain code-defined.
- Last materially reviewed: October 6, 2026, protected implementation/documentation
  baseline `da362a53a704c27709a137b1d0e363368b49a044`.
- Relevant milestones: ADR-043/045/049–057 and ADR-059–061 in the
  [decision ledger](../../decisions.md), plus [10.79](../../sprint_10_79_handoff.md)
  and [10.80](../../sprint_10_80_handoff.md).

This living responsibility model follows the [manifest framework](README.md).
It records evidence and direction, not implementation authorization or a new
content format. The five existing manifests retain their authority boundaries.

## Purpose

Supply intentional setting and scenario material from which owning gameplay
systems can establish a coherent beginning, interpret supported declarations,
and express play. Authored foundations enrich the world without becoming a
second source of arbitrary runtime outcomes.

## Player-facing goal

Begin among recognizable places, people, circumstances and opportunities;
discover information through legitimate access; and see choices change a world
that remembers those changes. Richness should not require an exhaustive database
or a predetermined sequence of player successes.

## Authority

Content owns authored identity, baseline geography and descriptions, supported
initial/default values, and the material of bounded declarations: evidence,
constraints, replies, possible consequences and scenario framing. Canonical
setting foundations conceptually belong here. Runtime systems decide whether a
declaration is supported, applicable and legitimately consequential.

Content may define a fixed bounded rule, transition, declaration or supported
result material. The authorized runtime interpreter or owning gameplay system
determines whether it applies and establishes any consequential outcome. Current
West-Road behavior is such a bounded rule, not evidence that arbitrary outcome
prose is executable. Authored content has no independent adjudication or
intentional-actor authority; deterministic authored scenario transitions remain
supported. The contractual boundary remains simulation authority: providers and
presentation cannot mutate gameplay truth, and state changes retain their
owning-system validation and publication.

## Explicit non-authority

Content does not own current external truth or time advancement; current character
capability/access/retention; adjudication; general intentional actor choice;
narrative selection; input parsing or UI mechanics; or save compatibility.
It cannot grant success, discovery, resources or future cooperation merely by
describing them. It cannot reset campaign divergence to a canonical/default fact.
Its immutable source is not the complete campaign save.

## Governing principles

Apply the [shared doctrines](README.md#shared-doctrines), especially Specificity,
Sparse Epistemic State and Authority Before Presentation, with Story-First Part I
and ADR-059. The following summarize that direction, not new runtime guarantees:

- **Foundations are not perpetual truth.** Supported starting facts yield to
  legitimate live changes for the affected fact; other compatible grounding remains.
- **Declarations require an owner.** A field matters mechanically only through a
  supported interpreter and its validation, eligibility and consequence rules.
- **Canon is a baseline constraint, not a campaign reset.** Canonical/authored
  foundations can constrain an unestablished part of the setting when it first
  becomes relevant or is resolved; this is not limited to new-game initialization.
  Legitimate established campaign state and campaign-caused divergence override
  the affected canonical/default fact. Canonical lore is not automatically
  character knowledge. This does not establish lore ingestion, claim-level
  provenance, or continuous canon reconciliation.
- **Unspecified is not nonexistent.** Leave ordinary detail open where inference
  suffices; consequential action still needs legitimate grounding and resolution.
- **Prose is not mechanics.** Text supplies expression and meaning, not an
  independent mutation path or proof that its implications were adjudicated.
- **Stable references support continuity.** Preserve supported identity without
  turning every noun, anonymous person or lore fact into a simulated entity.

## Current model

Three **Provisional** conceptual responsibilities are sufficient. They are not
new modules, mandatory schema partitions or a generalized authoring API.

| Responsibility | Material and present support |
|---|---|
| Foundations | Setting, places/connections, named actors, baseline placement, conditions and supported seeds. Canonical grounding is represented; canonical provenance and general social foundations are incomplete. |
| Declarations | Supported evidence, effects, cues and response conditions, interpreted by runtime owners. Current scenario eligibility, transitions and costs also live in code. |
| Narrative material | Names, descriptions, exact replies, clue/report wording and framing. Selection must preserve current truth, access and uncertainty; semantic consistency is not universally checked. |

The same record can serve several responsibilities. A clue has a reference,
eligibility inputs and text; that does not make its text an acquisition rule.

## Resolution depth

Author explicit structure when executable references, consequential constraints,
information access, repeatable outcomes or continuity depend on it. Examples are
macro connections, named actor IDs, the trace needed for an investigation and the
supported cost of a traversal. Exact dialogue is appropriate for a bounded reply.

Normal furnishings, incidental passersby, ordinary commerce and connective
background detail need not all be records. Market Square supplies spatial and
normal-activity grounding; current conditions constrain its expression. Attention
can reveal ordinary detail without inventing a clue, secret, vendor inventory or
independent actor. A named institution does not automatically need a decision loop.

Inference → lazy resolution → explicit persistent state → active simulation is
design guidance, not implemented content promotion machinery. A new consequential
detail or independent choice still needs its owning system. Region Packs need not
enumerate every alley or conceivable route; current executable travel nevertheless
uses the authored graph, not arbitrary inferred geometry.

## State and lifecycle

### Initial foundations and live overlays

**Implemented:** `GameEngine` reads a pack, validates recognized content, then
creates new state or validates/copies supplied state before building a scene.
New games deep-copy weather/time and supported pressure/actor-knowledge seeds;
discoveries, history and player competences start empty. Current West-Road code
also initializes its phase/incident record and one tracks trace. The active pack's
three static actors all have empty knowledge arrays; richer knowledge seeding is
demonstrated by the legacy fixture, not active starting knowledge.

| Fact | Initial source and subsequent authority |
|---|---|
| Player start | First location in the pack, unless an explicit engine entry override is supplied. `simulation_hooks.entry_location` is validated for topology but is not what the default initializer reads. They agree in the active pack. |
| Weather/time | Copied into World State, then read from there. Elapsed hours advance; the current timekeeper does not advance the calendar, time-of-day label or weather. |
| Pressures | Supported initial records copied; runtime setters/declared consequences own changes. A winter-pressure increase is not a weather-record mutation. |
| Static actor position | Sparse World State override wins; absence falls back to authored location. Returning to that baseline removes the override. |
| Actor knowledge | New-game seeds only; runtime membership subsequently wins. Missing legacy saved membership normalizes empty, never reseeds from current content. |
| Geography, profiles and local source fields | Loaded from content. No general mutable topology, profile, relationship, faction, gate-open or location-condition overlay exists. |
| Scene grounding | Authored description plus bounded runtime-derived additions. The market incident is appended only after occurrence; current weather/time and effective actor placement feed the scene. |

Scene construction still reads economy, security and population from the pack.
Location `state` fields and relationship numbers do not thereby become live
simulation. Spawns are rebuilt deterministically from `count` or the floored
midpoint of `count_range`; their template records have no stable individual
ownership. This is not a population model, schedule or persistent crowd.

### Content evolution and canonical foundations

**Accepted design:** content supplies canonical locations, named people, factions,
history, institutions, geography, cultural facts and setting constraints where
relevant. The [lore initialization principle](../../simulation_principles.md#world-initialization-from-lore)
supports coherent beginnings and compatible completion where lore is silent.
“Fully realized” should be read with minimum sufficient detail, not as exhaustive
precomputation. Live campaign changes supersede the affected initial truth.

**Partial representation:** current content identifies Icewind Dale, Forgotten
Realms, a date, named places/institutions and Town Watch foundations. `canon_source`
is a source label, not a citation registry or verified claim-level provenance.
Named content may combine setting anchors with authored scenario inventions;
this review does not certify every person, date or geographic assertion as canon.
The pack's `event_history` is not copied into new campaign history. There is no
general lore import, historical/cultural fact store or canonical conflict resolver.

**Implemented limit:** saves carry runtime state and a region path, not a frozen
copy or content hash. Loading uses the content currently at that path. Supported
saved changes persist, but edited source-only names, descriptions and declarations
can affect the rebuilt scene or make references invalid. Actor baseline changes
also affect actors with no override. The common pack `version` value does not
guarantee compatible meaning: active and legacy content both say `0.5`.

Stable references and preservation of accepted campaign meaning are the desired
interface to Persistence. Content revision pinning, reconciliation and migrations
are unresolved and **Deferred** here. ADR-060 deliberately rejects old prototype
saves lacking the required West-Road record; it is not an automatic conversion.

## Inputs

- Intentional authoring and setting sources, expressed in supported Region Pack
  fields and bounded scenario code; source claims are not automatically verified.
- Existing gameplay contracts defining interpretable references, effects and text.
- For runtime use, owning systems supply current state, access, eligibility and
  accepted outcomes to select applicable content. They do not rewrite source JSON.
- Future imported/generated material would require an authorized acceptance path;
  no model output or arbitrary content field currently has general mutation authority.

## Outputs

Supported initialization values, stable references, geography, evidence and
effect/response declarations, plus names, descriptions, reports and scenario text.
These are inputs to owning systems, not already adjudicated live results. Selected
exact authored text can be player-facing without constituting a new state change.

## Relationships

See the [information-flow map](system-map.md#dependencies-and-information-flow-around-scenario--authored-content).

| System | Boundary |
|---|---|
| [World Simulation](world-simulation.md) | Content supplies external foundations, geography and supported effects. World Simulation owns current truth, time and legitimate external change. |
| [Character System](character-system.md) | Content supplies supported identity/information seeds and evidence material. Character System owns current capability and informational access/retention, jointly constrained by world conditions; biography grants no competence. |
| [Action & Resolution](action-resolution.md) | Content supplies bounded prerequisites, costs and result material. Resolution determines applicability and yield; it cannot invent evidence to satisfy an authored outcome. |
| [Actors & Social Dynamics](actors-social-dynamics.md) | Content supplies roles, relationship/motivation foundations, dialogue and intentional bounded behavior rules. General meaningful choices belong to actor authority, not personality prose. |
| [Narrative Experience](narrative-experience.md) | Content supplies grounding, tone foundations, dialogue and framing. Narrative selection/expression remains constrained by live truth and legitimate access. |
| Player Presentation | Names/options/text feed display. Parsing, widgets and executable command routing remain presentation/runtime responsibilities. |
| Persistence | Preserves supported live state and compatibility. The interface for future content evolution remains provisional; authored source is not a save. |

## Player-facing projection

A baseline location description can establish ordinary features, but cannot
resurrect a legitimately destroyed door. This is an authority example, not a
claim that door destruction or general description reconciliation is implemented.
Market activity already demonstrates the narrower distinction: ordinary daytime
commerce in grounding does not override a current severe blizzard.

Separate evidence existence, access, interpretation and acquisition. Active tracks
exist before discovery; local investigation acquires a supported declaration.
Talking to Mara yields her attributed account through a fixed path. Sharing a
retained clue with Elin records receipt before initial decisions become available.
It does not certify the observers' identity or force an actor's general agreement.
Competence interpretation can reveal limited direction/overlap without a complete
route, and a failed check adds no finding. Text should preserve those distinctions.

Authored responses are legitimate bounded dialogue. Legacy response rules consult
command-start membership or discovery/history conditions; new membership from the
same conversation does not retroactively satisfy the knowledge-response predicate.
Active Grey/Elin replies instead use phase and, after the initial phase, recorded
witnesses. Conversation acceptance is not general persuasion or autonomous intent.
Exact text is not semantically checked against every possible live contradiction.

Opportunity text is advisory. Current projection reuses supported eligibility for
talking, investigating, clue presentation, West-Road choices and competence
approaches. Execution checks its own predicates. Displaying an option does not
grant its result, and arbitrary instructions embedded in text do not create a
new executable action. Clean display projections hide internal IDs, but the
provider's scene snapshot still contains internal fields; it is not a universal
safe information view (see Narrative Experience).

## Current implementation

### Active content, legacy mechanisms and representation

| Material | Classification and evidenced limit |
|---|---|
| Current ordinary play | **Implemented:** `play_game.py` selects `data/regions/bryn_shander.json`: 15 locations, three static actors, one faction, eight discovery declarations and the fixed West-Road predicament. |
| Actor foundations | **Partial:** Grey/Elin have role/state and numeric relationship material; Mara has identity, location and description. No runtime consumer interprets trust, loyalty, respect, alertness or faction objectives as general decisions. No general biography/motivation schema exists; motivations appear chiefly in scenario prose. |
| Factions/institutions | **Partial representation:** Town Watch identity, influence, player stance, readiness, morale and objectives exist; scenes list faction IDs. No mutable faction state, institutional knowledge or faction AI follows from these fields. |
| Geography/locations | **Implemented bounded graph:** references, reciprocal local edges and reachability are validated. Named routes use authored adjacency; location prose and `state.open` do not independently establish executable paths or movement blocking. |
| Legacy fixture | **Implemented test coverage only:** `test_fixtures/bryn_shander_legacy.json` retains superseded conversation, thread, relocation, trace, response and affordance declarations. These mechanisms remain in runtime, but are not the current reference story. |
| Earlier packs | **Historical prototypes:** `bryn_shander_v0_2.json` and `bryn_shander_v0_3.json` each contain three locations/two actors; both internally label version `0.2`. `run_scene_test.py` still points at v0_2. Presence on disk is not current gameplay endorsement or evidence of current validator compatibility. |
| Metadata | **Representation only:** `setting`, `canon_source`, source `event_history`, `simulation_hooks.current_phase` and `allowed_systems` do not form a generic lore/runtime feature switch. Actual supported commands and current scenario phase are engine-owned. |

### Declarations and their interpreters

| Declaration/material | Runtime meaning and authority |
|---|---|
| Current pressure/time declarations | Initial winter/gate pressures seed state. Crossing the declared first elapsed hour sets winter pressure to 70. The separately declared observation cue requires applicable pressure at its threshold. It does not alter weather or grant global perceptibility. |
| Current traversal cost | One strict declaration binds the Southwest Gate → Southwest Trade Road edge to exactly one hour. Engine prepares time/effects/movement and publishes the validated candidate. Other graph edges have no authored general travel-cost semantics. |
| Discoveries | Strict records supply IDs, location/trace matching, title and text, with optional evidence ID. Local investigation chooses the first eligible undiscovered declaration; text alone creates neither trace nor acquisition. West-Road outcomes also acquire specified findings through explicit code paths. |
| West-Road predicament | Pack contains premise, seven phase texts and Grey/Elin phase replies. Code owns six commands, seven phases, required evidence/reports, actor/location gates and phase-to-discovery mapping. Either initial choice costs one hour; ordinary fixed follow-ups add no hour. This intentionally bounded behavior is not a universal quest/state-machine language. |
| Competence resolution | Pack supplies observation/recognition and clue wording. Runtime owns three tags/operations, d6 policy, failure/partial/full yield, resources, replay and costs: uncertain approaches cost one hour, guarded survey two or one with tactical competence. Changing prose cannot choose a draw, discount or successful result. |
| Market consequence | Fixed code tracks two qualifying reduced-coverage hours and establishes one theft; authored-style incident prose also lives in code. It is not a pack-defined event scheduler, general theft rule or evidence of a named faction's choice. |
| Legacy effects | Recognized declarations can set pressure, relocate static actors, add opaque actor knowledge, create traces, open/resolve one thread or recall an actor after clue presentation. Conversation, elapsed-time, resolution and arrival paths prepare their supported consequences through GameEngine and state validators. They are separate bounded mechanisms, not generic effect dispatch. |
| Legacy replies/affordances | Exact text is gated by specified actor membership or player discovery/history conditions. A derived suggestion neither executes the action nor guarantees a social outcome. |

Time cost is an input to resolution where applicable; authoritative time/world
change belongs to World Simulation. Effect declarations do not bypass their
owners because they reside in data. Existing candidate validation/build/publish
protects supported material transitions; this does not imply disk-write guarantees.

### Validation and identity limits

`load_region` only parses JSON. `GameEngine` then calls `validate_region` before
initialization/restoration and scene construction. There is no separate general
Region Pack schema/version dispatcher. Validation covers topology/static identity,
knowledge shape, pressures, and named optional declarations. An absent optional
mechanism is normally allowed; a present recognized declaration often requires an
exact key set, nonempty text, valid references and restricted values. West-Road
presence activates additional exact shape, phase, actor and evidence requirements.

Tests assert rejection of extra/missing declaration fields, invalid pressure
values/thresholds, unknown or spawned actor references, invalid locations, selected
effect-ID conflicts and malformed saved membership. One-hour traversal rejects
other endpoints/durations. Candidate failure tests preserve existing state/scene
rather than publish partial consequences. Loading builds a replacement engine
before replacing a live session. There is no supported partial-pack activation.

**Partial validation, not universal fail-closed content semantics:** unknown
top-level fields are not blanket-rejected and have no generic executor. Many
descriptive/profile/spawn fields lack exhaustive shape or semantic validation;
malformed structure can raise ordinary lookup/type errors later. Validators do
not prove authored prose truthful, validate all faction/relationship references,
or impose one global entity namespace. These are implementation limits, not a
promise that arbitrary malformed input is safely accepted or usefully diagnosed.

Location IDs, static `entity_id`, pressure/discovery/trace/effect/thread IDs and
history references have specific consumers. Knowledge IDs are opaque membership,
not a canonical lore catalog. Faction IDs currently reach scene lists; spawned
templates have no stable instance identity. Internal keys can survive display-name
changes: `inn_four_candles` displays “Northlook,” `traders_hall` displays
“Rendaril's Emporium,” and west-gate/road IDs display southwest names. Names/titles
also serve bounded command matching; neither names nor stable keys establish a
universal canonical identifier system.

## Accepted decisions

Immutable authored sources plus validated mutable campaign state; supported
initial seeds rather than repeated reseeding; sparse actor overrides; explicit
discovery/access boundaries; bounded declared consequences; minimum sufficient
detail; and untrusted narration are existing direction. ADR-060 supersedes the
prototype's ordinary-play scenario, while preserving its test-only mechanisms.
ADR-061 distinguishes evidence text from competence and accepted resolution.

Canonical grounding is **Accepted design**, with **Partial** current content
representation and **Deferred** general ingestion/completion machinery. Campaign
truth taking precedence is accepted in the World Simulation manifest, implemented
only for supported runtime fields rather than every conceivable authored fact.

## Provisional decisions

Foundations / declarations / narrative material is the smallest useful working
decomposition. Broader actor foundations, canonical provenance, safe content
evolution and cross-setting interfaces remain provisional. File boundaries do
not fully match ownership: scenario code contains authored behavior/text as well
as interpretation. No module extraction or new authoring format is prescribed.

## Deferred capabilities

General lore ingestion/conflict resolution, content migrations, modding/plugin
formats, universal effects/quests, generalized conditions, autonomous actor/faction
AI, mutable relationship systems, broad biography-derived knowledge/capability,
exhaustive world databases and automatic promotion of prose into state. A region
path and data-driven foundations suggest separation useful to other settings;
hardcoded West-Road IDs/rules and market logic limit portability. Generalizing
those requires separately authorized evidence and scope, not this manifest.

## Known tensions / open questions

- **Source revision versus campaign continuity:** content is reloaded by path;
  source-only changes and missing references can affect an existing campaign.
  What minimum compatibility policy preserves established meaning without copying
  the whole setting into each save? This belongs with later Persistence work.
- **Baseline versus live prose:** generic description replacement/reconciliation
  does not exist. Current overlays and market activity are narrow; even exact
  authored replies can become inappropriate under combinations of live changes.
  Semantic review is not supplied by structural validation.
- **Validation coverage:** exact supported declarations coexist with loosely
  checked metadata/profiles. Determine needed checks from actual authoring risks;
  do not infer a general trusted schema from successful pack loading.
- **Initialization mismatch:** the topology entry hook and first-location start
  are different mechanisms, currently aligned by content. This is an implementation
  quirk to resolve if authoring needs diverge, not a permanent authoring rule.
- **Doctrine wording drift:** Simulation Model's “Once concretized” persistence
  wording is broader than later ADR-059 and accepted incidental narration.
  Ordinary expressive detail does not automatically become durable canon. Older
  actor-knowledge exclusions also describe earlier slices, not later supported
  reporting/response paths. Protected manifests already preserve these limits.
- **Canonical provenance and portability:** source labels do not separate canonical
  facts from scenario invention, and scenario semantics are partly hardcoded.
  Neither issue authorizes a lore database or generic framework now.

No contradiction requiring an edit to a protected manifest was found. These are
bounded implementation gaps, historical wording and provisional interfaces; they
do not transfer runtime authority to authored prose.

## Evidence

Runtime and test assertions below were inspected. Gameplay suites and providers
were not run for this documentation review; historical acceptance is not a new
verification result. Documentation checks are reported in the review handoff.

| Evidence | Supports |
|---|---|
| [Framework](README.md), [map](system-map.md), five linked manifests | Responsibility boundaries and shared doctrine |
| [Architecture](../../architecture.md), [principles](../../simulation_principles.md), [model](../../simulation_model.md), [Story-First](../../story_first_design_doctrine.md), [ADRs](../../decisions.md) | Immutable content/live state, lore initialization, specificity and bounded historical contracts |
| [Active pack](../../../data/regions/bryn_shander.json), [legacy fixture](../../../test_fixtures/bryn_shander_legacy.json), [fixture scope](../../../test_fixtures/README.md), [v0_2](../../../data/regions/bryn_shander_v0_2.json), [v0_3](../../../data/regions/bryn_shander_v0_3.json) | Actual representations and active/legacy distinction |
| [CLI](../../../play_game.py), [old scene runner](../../../run_scene_test.py), [loader](../../../engine/scene_loader.py), [region validator](../../../engine/region_validator.py) | Selected pack, scene reconstruction, validation and its limits |
| [World State](../../../engine/world_state.py), [knowledge](../../../engine/actor_knowledge.py), [pressures](../../../engine/pressure_state.py), [time](../../../engine/timekeeper.py), [save system](../../../engine/save_system.py), [session](../../../engine/game_session.py) | Seeds, sparse overlays, current conditions and content reload behavior |
| [GameEngine](../../../engine/game_engine.py), [eligibility](../../../engine/action_eligibility.py), [opportunities](../../../engine/contextual_action_projection.py) | Declaration interpretation, gated acquisition/actions and candidate publication |
| [Predicament](../../../engine/west_road_predicament.py), [competence](../../../engine/character_competence.py), [theft](../../../engine/west_road_market_theft.py) | Fixed scenario/causal rules, engine costs/results and authored material in code |
| [Knowledge reply](../../../engine/actor_knowledge_response.py), [discovery reply](../../../engine/player_discovery_response.py), [affordance](../../../engine/conversation_affordance.py), [Scene Context](../../../engine/scene_context.py) | Bounded response predicates, advice and conditions-constrained description |
| [Topology tests](../../../test_region_topology.py), [knowledge tests](../../../test_actor_knowledge.py), [discovery tests](../../../test_discovery.py), [response tests](../../../test_actor_knowledge_response.py) | Reference rejection, seeding/load distinction, access and command-start ordering |
| [Pressure effects](../../../test_conversation_pressure_effect.py), [relocation](../../../test_conversation_actor_relocation.py), [time relocation](../../../test_time_actor_relocation.py), [traversal](../../../test_one_hour_west_road_exit_traversal.py) | Strict optional declarations and bounded atomic mechanisms exercised with legacy content |
| [Predicament tests](../../../test_west_road_predicament.py), [competence tests](../../../test_character_competence.py) | Active prerequisites, fixed outcomes, malformed evidence rejection and retained attempts |

## Revision history

- October 6, 2026: initial review candidate; distinguish foundations, interpreted
  declarations and narrative material, with explicit active/legacy classification,
  live-state precedence and limits on validation, canonical provenance and evolution.
