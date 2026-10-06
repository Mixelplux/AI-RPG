# Narrative Experience — Design Manifest

## Status

- Overall: **Partial** — bounded context, deterministic expression, provider
  validation and scene continuity exist; general selective narration does not.
- Last materially reviewed: October 6, 2026, protected repository baseline
  `ecd3ed246a8c989990d1411582438b58369d3c84`.
- Relevant milestones: [10.77 predicament](../../sprint_10_77_handoff.md),
  [10.78 competence](../../sprint_10_78_handoff.md),
  [10.79 locality](../../sprint_10_79_handoff.md), and
  [10.80 Scene Context](../../sprint_10_80_handoff.md).

This living review candidate uses the [shared manifest structure and status
vocabulary](README.md). It refines responsibility, not implementation authority.
No new module, persistence model, prompt change, sprint or provider run follows
from it.

## Purpose

Turn authoritative, legitimately accessible material into coherent, selective,
context-aware expression. Own what to foreground, how to preserve its meaning,
and how to say it. Narrative Experience governs authored, deterministic,
generated and hybrid expression; it is not synonymous with the language model.

## Player-facing goal

Help the player understand where they are, what their action actually achieved,
what remains uncertain, and what matters to their current attention. Preserve
continuity without repeating a state inventory. Close an ordinary or unsuccessful
observation honestly, and let ordinary places remain ordinary.

## Authority

Within supplied truth and access constraints, select, omit, order, contextualize,
describe and emphasize information; choose wording and supported expressive tone;
maintain continuity of expression; make already justified implications legible.
Selection changes the response, not the underlying fact or its availability to
other legitimate views. An explicit clue review may show retained information
that an unrelated location's scene description properly omits.

Compatible incidental detail may enrich expression without becoming gameplay
truth. This freedom has the consequential limits below. Structural acceptance
for display never promotes provider language into an authoritative fact.
Simulation authority and fail-closed provider behavior are existing contracts;
the proposed responsibility decomposition is revisable design.

## Explicit non-authority

Narrative Experience cannot independently determine success, failure, costs,
findings, NPC choices, private motives, relationships, promises, knowledge,
evidence, actor locations, time passage or causal consequences. It cannot turn
speculation into fact, compensate for failure, supply missing prerequisites,
or invent escalation because pacing would benefit. Emotional framing and
salience are expressive choices, not causes of world change or permission to
assign the player's emotions and intentions.

Player Presentation captures input and owns parsing/display mechanics. Action &
Resolution handles supported consequential execution. Descriptive acknowledgement
of intention is not execution: an intention to search does not establish a
successful search, and an intention mentioning a burned inn does not establish
that the inn burned. Current instructions allow ordinary connective movement or
examining within the scene; they do not authorize arrival elsewhere, purchases,
helping, threats, disclosures, accepting offers, danger or abandonment of a goal.

## Governing principles

Apply the [shared doctrines](README.md#shared-doctrines),
[Simulation Principles](../../simulation_principles.md),
[Simulation Model](../../simulation_model.md),
[Story-First Part I](../../story_first_design_doctrine.md#part-i--established-design-doctrine)
and [ADRs](../../decisions.md), especially 027–033 and 058–061.

- Preserve factual and epistemic fidelity before expressive preference.
- Make the accepted result intelligible; concise prose must not conceal a
  material cost, limitation or uncertainty needed to understand that result.
- Preserve context through compatibility, not obligatory repeated mention.
- Attention earns descriptive resolution, not a secret, hook or greater importance.
- Technical boundaries do not create fictional discontinuities.

**Provisional synthesis:** fidelity constrains player comprehension, which guides
continuity/relevance and then style/voice. These are priorities for judgment, not
a scoring algorithm or a newly accepted four-level contract. The repository
clearly establishes the fidelity boundary; the exact ranking among otherwise
faithful choices remains subject to play evidence. Current house instructions
favor second person, restrained concrete prose and qualitative environmental
measurements unless a supplied in-world basis justifies exact numbers.

## Current model

Use three **Provisional** responsibilities, with existing bounded implementations:

| Responsibility | Question and present grounding |
|---|---|
| Context selection | Which accessible facts, accepted results and recent context help now? Scene locality, filtered history, competence layers and Scene Context supply partial support. This does not grant access or choose what is true. |
| Framing and continuity | What does the material establish, what remains uncertain, and what need not be restated? Attributed authored reports, limited findings, scene stages and previous conditions supply partial support. |
| Expression | How can the selected material be conveyed clearly and compatibly? Authored replies, deterministic scene/result text and validated provider prose are implemented mechanisms with different quality limits. |

No separate semantic memory, relevance service or narrative director is implied.
Framing includes epistemic discipline; a fourth belief subsystem is unnecessary.
Continuity constrains all three responsibilities rather than owning another world.

## Resolution depth

Use the [Specificity Doctrine](README.md#specificity-doctrine) without importing
its simulation levels as a prose-storage ladder. Begin with sufficient orientation;
increase description when attention, current choice, a relevant consequence or
a transition makes it useful. Richer description must stay compatible with the
same truth and access limits. An ordinary shack may reveal ordinary construction
detail without becoming a mystery. Repeated inspection does not demand novelty.

`look`, `inspect`, `examine`, `search` and `study` can enter the broad observation
route; supported scenario investigations and competence attempts have separate
engine behavior. The observation route is not a generic object examiner,
perception engine, exhaustive-search adjudicator or automatic discovery policy.
Supplying player intention to a model does not fill those gaps.

### Compatible expressive detail

**Accepted design and implemented prompt permission:** ordinary anonymous motion,
harmless props, mundane goods, sensory texture and low-consequence gestures may
be concretized within location, conditions and activity bounds. Mugs on an
appropriate table, ordinary crowd movement or footsteps accompanying supported
movement need not become inventory, named actors or evidence records. Wind
catching an established cloak need not track the fabric; it must not invent
player-owned clothing contrary to the retained equipment constraint.

The test is what the detail implies in context, not whether it sounds mundane.
Footprints offered as a trail are evidence; a flinch implying concealed guilt is
a salient cue; an apparently casual assurance can be a promise. Those require
the relevant authoritative basis. Neutral texture must not imply hidden identity,
hostility, deception, resources, access, a transaction or a new interaction that
the engine must honor. Known live state constrains authored seeds as well as
generated prose; authored wording is not a license to restore obsolete facts.

Actor speech and visible reaction express accepted behavior and reports. Wording,
rhythm and non-consequential manner may vary when compatible with that basis;
new disclosures, commitments, relationships and deliberate choices may not.
Current authored replies are fixed outputs, not a general generated-dialogue
policy. General expressive latitude for meaningful actors remains **Provisional**.
If a player invests in an incidental detail, any consequential acceptance belongs
to its owning gameplay system; no promotion protocol is selected here.

## State and lifecycle

Separate four kinds of continuity:

| Kind | Present behavior and limit |
|---|---|
| Fictional state | Supported world, character, scenario and accepted-attempt state survives through existing saves. Prose neither stores nor reconstructs its authority. |
| Recent narrative context | CLI `SceneContinuity` carries sentence excerpts and previous conditions for the current location. These are untrusted descriptive claims, not verified facts, player memory or a transcript. |
| Recap/reorientation | `Previously:` is deterministic West-Road summary derived from phase, discoveries and reports; the following scene supplies local detail. It is not replay of prior generated language. |
| Provider conversation context | The adapter sends explicit bounded material per call with no conversation chain and `store=False`. There is no authoritative provider memory. |

**Implemented:** the CLI cache keeps at most 24 sentence excerpts, at most 4,000
characters per excerpt and 8,000 total; it favors initial orientation and recent
description. Exact duplicate sentences are not re-added. It does not semantically
deduplicate paraphrases, verify claims, or retain all intervening command results.
Location changes and successful load/reset clear it. Re-entry therefore orients
again; there is no persisted visited-location narrative memory. Reset starts new
game state through the engine; clearing the presentation cache itself changes no
fictional state. Failed load does not intentionally clear the cache.

**Accepted design:** weather, danger, atmosphere, actor presence, consequences
and established problems normally carry implicitly. Re-express a material change,
effect on the present action, necessary limitation or concise reorientation.
An unchanged blizzard need not open every response. An actor need not be
reintroduced after every command. Suppressing mention does not erase a goal,
remove an actor or reduce simulation state. Current weather/context instructions
support this direction; there is no general danger, goal or social-continuity model.

Initial orientation, re-entry, transition, continuation and consequence reveal
are useful **Provisional** framing distinctions, not required prose templates.
Current stages are `orient`, `expand`, `follow` and `narrow`; absence of remembered
details forces `orient`. They describe presentation intent, not authoritative
attention, elapsed time or a guarantee of generated progression. Save/load and
new model calls may need reorientation without suggesting fictional forgetting.

## Inputs

| Source and owner | Material and limits |
|---|---|
| World Simulation | Established local conditions, position, time, external changes and observable facts. Objective truth alone does not justify disclosure. |
| Character System with world conditions | Legitimate access constraints, recognition, retained findings and relevant capability. Current jointly derived views are bounded; no universal access filter exists. |
| Action & Resolution | Accepted results, costs and evidence limits. Command acceptance differs from fictional success; replayed results do not imply another attempt. |
| Actors & Social Dynamics | Accepted behavior, choices, reports and established social context. A report's existence does not prove its content. |
| Scenario & Authored Content | Descriptions, dialogue, tone foundations and supported constraints. Immutable baseline content must be interpreted with current state. |
| Player Presentation | Declared input/focus and current presentation stage; input remains untrusted intention, not testimony that its assumptions are true. |
| Recent presentation/history | Bounded event context, previous conditions and prior descriptive claims. These have distinct trust and meaning; neither is a complete character memory. |
| Provider instructions | Expression and authority rules supplied by the application, not new fictional facts. |

The live context contains a copied **scene snapshot**, derived Scene Context,
current time/location, raw input, bounded history and at most the first applicable
pressure cue. Recent history is first bounded, then restricted to conversation,
movement and time-advance event types; it is not relevance-ranked or a complete
action-result stream. It does not refill the window after filtering.

The provider path does **not** simply consume the clean current-scene projection.
Its snapshot still contains internal IDs, debug/spawn data, faction IDs and
regional local-state fields. It omits full actor profiles/knowledge and full world
history, but must not be described as a universal knowledge-safe projection.
Prompt constraints and bounded scenario filtering carry part of the burden.

## Outputs

Player-facing scene prose, attributed speech/reports, outcome explanations,
reorientation and ordinary descriptive texture, plus bounded presentation context
for subsequent expression. Existing outputs include structured deterministic
narration, exact authored response text and provider `display_text` accepted by
structural validation. None is a state mutation command or evidence of a new
fact merely because it has been displayed.

## Relationships

See the [system map](system-map.md#dependencies-and-information-flow-around-narrative-experience).

| Responsibility | Boundary |
|---|---|
| [World Simulation](world-simulation.md) | Establishes external reality and legitimate changes. Narrative emphasis does not create causal change, time passage or remote access. |
| [Character System](character-system.md) | Supplies capability and character-specific access basis; accessible views may be jointly derived. Expression preserves this basis without granting knowledge. |
| [Action & Resolution](action-resolution.md) | Establishes accepted outcomes/costs and legitimate yielded information. Expression cannot roll, waive costs, repair failure or overstate bounded success. |
| [Actors & Social Dynamics](actors-social-dynamics.md) | Establishes meaningful intentional choices and social meaning. Expression cannot independently choose motives, promises or consequential reactions. |
| Scenario & Authored Content | Supplies foundations and supported narrative material. Generated, authored and deterministic wording all remain constrained by accepted live truth. |
| Player Presentation | Owns parsing, commands, UI layout, widgets and safe display mechanics. Narrative Experience owns expressive content and selection; both currently share CLI/GameEngine code. |
| Persistence | Owns storage/restoration mechanics. Narrative Experience identifies continuity needs without selecting new durable fields or duplicating storage limitations. |
| Narrator Provider / Model Adapter | Produces untrusted candidate language under supplied bounds. Transport and model configuration are infrastructure, not fictional authority. |

## Player-facing projection

Preserving epistemic distinctions is an explicit Narrative Experience
responsibility, not a new inference or belief engine:

| Supplied meaning | Faithful expression |
|---|---|
| Established accessible fact | State the supported fact without adding identity, cause or scope. |
| Attributed report/belief | Preserve who reports/believes it and material qualification; do not silently make it narrator-certified truth. |
| Supported inference | Preserve its evidence basis and uncertainty; precision of wording does not increase certainty. |
| Unknown or unavailable information | Leave it unknown. A failed search finding nothing useful does not prove nothing is concealed. |
| Accepted limited success | Explain what was learned or achieved and what remains unresolved. Do not turn a local route finding into capture or final resolution. |

For example, the market theft is established and locally observable after the
engine event. The watchman's account of thin patrols remains attributed; the
thief and motive remain unknown. A claim that the Zhentarim did it is unsupported.
Likewise, Grey reporting road danger is not an unrestricted warrant for narrator
knowledge of every actor's affiliation. Remote truth, private knowledge and
unobserved motives must not leak as atmospheric detail.

Success, failure, partial result, cost, uncertainty, acquired findings and unchanged
state deserve distinct expression. A negative observation can be complete for its
focus without claiming exhaustive absence. A downstream consequence may be made
salient only after the owning system establishes it and access permits disclosure.
Preserve relevant costs in understandable language; avoid raw dice bands, phase
names, status tags and internal rules in ordinary prose. Existing explicit command
choices and one-hour costs are intentional aids, not a mandate to hide all mechanics.

## Current implementation

| Capability | Classification and evidenced limit |
|---|---|
| Deterministic scenes and results | **Implemented, bounded:** `scene_narrator` composes authored description, weather, presence, routes and opportunities. GameEngine adds West-Road circumstances, choices and competence outcomes; CLI prints authored replies, discoveries and command messages. Not all output passes through the provider. |
| Scene Context | **Implemented, bounded:** location grounding, weather/time, declared intention and local competence; Market Square derives qualitative activity from conditions. Severe exposure suppresses ordinary commerce. Other location activity is unspecified, not generated population or schedules. |
| Local selection | **Implemented, bounded:** West-Road scene/competence material belongs at road/gate; market theft appears locally only after occurrence. Explicit retained clues and resume remain available. **Partial** overall selection: no general relevance policy. |
| Attention and continuity | **Partial:** scene stages, focus, prior sentences and conditions reach validated prompts. CLI suppresses identical deterministic scene redisplay and compresses routine route-hop messages. No semantic repetition suppressor, general actor reintroduction policy or long-term narrative memory. |
| Outcome/epistemic fidelity | **Partial:** competence packets separate observation/report, limited recognition/inference, findings and accepted outcomes; deterministic prose states failure and remaining unknowns. General freeform factuality is not verified. |
| Provider boundary | **Implemented:** copied context → validated request → validated prompt → untrusted source → source-result validation → output validation → display. No state-application path consumes generated prose. Failure yields no candidate display text. |
| Provider transport | **Implemented, bounded:** provisional Luna-low configuration; synchronous call, no tools/conversation state, no retries, 20-second timeout, 8,000 locally counted input tokens, 256 output tokens and 4,000 output characters. These are implementation limits, not narrative principles. |
| Fallback behavior | **Partial experience:** deterministic narration remains used on ordinary non-market scene paths. Provider-backed scene failure prints an unavailable/retry notice; it does not automatically substitute a rich deterministic scene or another model. Fail-closed state safety is not a complete fallback narrative experience. |
| Pressure composition | **Implemented, narrow:** pipeline removes exact occurrences of the selected cue from candidate text and appends that cue once. This is not semantic deduplication or cross-turn condition suppression. |
| Recap/save-load | **Implemented, bounded:** West-Road `Previously:` derives from saved phase/discoveries/report state. Save/load rebuilds scenes; narration/cache is not saved. It is not a general campaign recap or complete attempt-history summary. |
| Incidental expression | **Accepted design with implemented prompt permission:** compatible ordinary texture is allowed. Continuity remembers descriptive claims, not authoritative props, NPCs, inventories or discoveries. Semantic compliance remains **Partial**. |

Sprint 10.79 corrected irrelevant West-Road material at Market Square without
deleting discoveries, phase or outcomes. This demonstrates selection versus truth.
Sprint 10.80's accepted live arrival/look/browsing smoke demonstrated useful
progression and reduced repetition in that sequence. Minor storm repetition was
accepted. Neither proves universal prose quality or complete information safety.

## Accepted decisions

Simulation authority; untrusted fail-closed providers; read-only bounded narration
contracts; distinction between truth, access, report and inference; minimum
sufficient detail; and continuity independent of technical boundaries are existing
direction. Sprint 10.80 explicitly permits compatible incidental expression and
bounded session continuity. Its later accepted ordinary-player route is material
evidence when reading older preview-only descriptions.

## Provisional decisions

The three responsibilities, practical fidelity/comprehension/continuity/style
ordering, generalized transition framing and meaningful-actor expressive latitude
are review proposals. No universal context schema, tone taxonomy, memory store,
salience score, prose template or semantic judge is selected. The current model
choice is reversible infrastructure configuration, not this system's definition.

## Deferred capabilities

General relevance selection, narrative memory/history compression, generalized
perception and object examination, belief/rumor engines, generated consequential
dialogue, incidental-detail promotion, durable prose continuity, broader authored
activity interpretations and semantic repetition/fidelity enforcement require
separately authorized work. So do autonomous agency, proposal-based world changes
and broader AI-GM reasoning from Story-First's provisional sections. None belongs
to narration merely because a model might generate the language.

## Known tensions / open questions

- **Documentation drift:** architecture says provider narration does not run in
  normal gameplay; ADR-058 retains an explicit-preview framing. Current CLI and
  accepted Sprint 10.80 routes include market presentation and observation/intention
  calls. This is a historical description mismatch, not permission to run providers
  during this review. Canonical architecture/ADR wording needs separate reconciliation.
- **Older restrictive examples:** ADR-027, legacy `llm_prompt_builder` and retained
  atmosphere examples emphasize no unstated specifics; newer accepted Scene Context
  permits ordinary incidental detail. Preserve player-equipment and consequential
  limits while recognizing the later permission. Exact guidance cleanup is outside
  this documentation scope; do not infer that every adjective needs World State.
- **Safety coverage:** clean current-scene projection is not the provider payload.
  Internal snapshot fields remain present, and validators check structure rather
  than every claim. How much further filtering is justified by observed leaks?
- **Descriptive carry-forward:** accepted-for-display prose can contain unsupported
  claims; remembering it may reinforce an error. Instructions prioritize authority,
  but no semantic reconciliation proves compatibility. Determine the smallest useful
  response to observed failures without promoting claims or building a transcript.
- **Uneven selection:** locality fixes are scenario-specific; deterministic weather,
  actor lists and phase text can repeat on refresh, and pressure cues are appended.
  Generated guidance does not make every output path equally selective.
- **Recap precision:** terminal `Previously:` text is keyed chiefly by phase. A
  competence survey reaching `withdrawal_route_found` receives wording about having
  followed the route rather than preserving the exact operation. No general recap
  of partial attempts/costs or unrelated consequences exists. The minimum fidelity
  needed for reorientation merits review without duplicating persistent state.
- **Incidental investment:** when does player reliance on texture require authoritative
  acceptance, and how should unsupported implied affordances be handled? This
  review names the boundary without defining promotion/storage or new behavior.
- **Re-entry and failure experience:** cache resets lose ephemeral description;
  unavailable-provider notices preserve safety but offer little orientation.
  Evidence should determine whether either needs additional continuity/fallback work.

No contradiction requiring changes to the four protected Core Gameplay manifests
was found. The issues above are historical wording drift, bounded implementation
gaps and unresolved expressive interfaces, not grounds to transfer simulation
authority to narration.

## Evidence

Runtime and test assertions were inspected, not executed as gameplay suites for
this documentation review. Handoff smoke/verification findings are historical
evidence, not new live results.

| Evidence | Supports |
|---|---|
| [Framework](README.md), [map](system-map.md), four linked Core Gameplay manifests | Responsibility and authority boundaries; shared doctrines |
| [Architecture](../../architecture.md), [principles](../../simulation_principles.md), [model](../../simulation_model.md), [Story-First](../../story_first_design_doctrine.md), [ADRs](../../decisions.md) | Truth/access distinction, neutral ambience, minimum detail, provider contract and historical drift |
| [Context](../../../engine/narration_context.py), [history](../../../engine/history_context.py), [request](../../../engine/narration_request.py), [prompt](../../../engine/narration_prompt.py) | Copied bounded material, history allowlist, instructions and shape validation |
| [Source](../../../engine/narration_source.py), [pipeline](../../../engine/narration_pipeline.py), [output](../../../engine/narration_output.py) | Transport limits, structural rejection, cue composition and lack of semantic proof |
| [Scene Context](../../../engine/scene_context.py), [continuity](../../../engine/scene_continuity.py), [context tests](../../../test_scene_context.py), [route tests](../../../test_player_scene_route.py) | Activity interpretation, stages, carry-forward, bounded cache, ordinary CLI route and failure display |
| [CLI](../../../play_game.py), [GameEngine](../../../engine/game_engine.py), [kernel](../../../engine/interaction_kernel.py), [scene narrator](../../../engine/scene_narrator.py), [legacy prompt](../../../engine/llm_prompt_builder.py) | Mixed authored/deterministic/generated paths, intention versus execution, observation and old wording |
| [Scene loader](../../../engine/scene_loader.py), [perception](../../../engine/perception_builder.py), [safe scene projection](../../../engine/current_scene_projection.py) | Derived truth, visibility simplification and difference from provider snapshot |
| [Competence](../../../engine/character_competence.py), [predicament](../../../engine/west_road_predicament.py), [presentation](../../../engine/west_road_presentation.py), [theft](../../../engine/west_road_market_theft.py) | Evidence-limited outcomes, authored reports, recap, phase rendering and local causal reveal |
| [Locality tests](../../../test_west_road_scene_relevance.py), [presentation tests](../../../test_west_road_presentation.py), [save/load tests](../../../test_save_load.py) | Local omission without state loss, no-op refresh suppression, save reconstruction |
| [Output tests](../../../test_narration_output.py), [pipeline tests](../../../test_narration_pipeline.py), [adapter tests](../../../test_openai_responses_narration.py) | Structural safety and fake-transport boundary evidence, not generated quality |
| [10.79](../../sprint_10_79_handoff.md), [10.80](../../sprint_10_80_handoff.md) | Owner-observed locality/progression corrections and accepted remaining repetition |

## Revision history

- October 6, 2026: initial review candidate; refine expression into selection,
  framing/continuity and expression, with explicit epistemic and incidental-detail
  limits and a distinction between structural safety and narrative quality.
