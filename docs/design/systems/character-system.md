# Character System — Design Manifest

## Status

- Overall: **Partial** — authoritative competence and selective information
  records exist in bounded slices; a general character model does not.
- Last materially reviewed: October 6, 2026, repository baseline
  `89f135834eb85cb995facb0b7126a3c5f58b7a6a` (`docs: establish world simulation manifest`).
- Relevant milestones: [10.77 reference predicament](../../sprint_10_77_handoff.md),
  [10.78 Character Competence V1](../../sprint_10_78_handoff.md),
  [10.79 local causal projection](../../sprint_10_79_handoff.md), and
  [10.80 Scene Context](../../sprint_10_80_handoff.md).

This living model applies the [shared doctrines and status vocabulary](README.md).
Conceptual ownership does not select storage, require new runtime modules, or
authorize implementation. The framework and World Simulation baseline remain
unchanged apart from manifest navigation and relationship-map integration.

## Purpose

Establish what a character can do, what information they can legitimately access,
and what character-specific continuity matters to future play. Supply these
constraints to action adjudication and presentation without copying external
reality into character memory or giving narration authority over either.

## Player-facing goal

Enable characters to recognize different possibilities, understand evidence at
different resolutions, and carry meaningful experience forward. Ordinary lived
experience should support believable play without requiring every street visit
or conversation to have appeared in the transcript. Specialist capability may
provide understanding, efficiency, or alternate paths without becoming the only
way to continue a campaign.

## Authority

The current responsibility model covers authoritative character capability,
character-relative informational access, and selectively retained information.
It distinguishes a character's actual capability from a narrated description,
and the fact that they encountered or believe a report from whether the report
is true. These are character-specific truths established by owning gameplay
systems, within the existing contractual simulation-authority boundary.

Character System supplies capability and recognition constraints; Action &
Resolution combines them with world evidence, circumstances, resources, and
attempt policy to establish eligibility, costs, and outcomes. Their current
implementation shares a fixed competence authority and GameEngine orchestration.
This conceptual separation does not move existing code or divide its validator.

For NPCs, individual informational access is relevant character state, while
meaningful intentional decisions and social responses belong to Actors & Social
Dynamics. Treat a shared character-information responsibility across player and
NPC records as **Provisional**: the current map and code do not settle a general
NPC profile interface or the ownership of every social/relational state field.

## Explicit non-authority

Character System does not own external reality, fictional time, physical traces,
scenario phase, action-outcome adjudication, intentional NPC/faction decisions,
narration, the player's actual intentions, or authored future outcomes. A
character's belief cannot make its content world truth. Familiarity cannot
create a building, and competence cannot create absent evidence.

Persistence owns durable storage/restoration and compatibility; Player
Presentation owns input/display. Character-specific access restrictions still
apply to their consumers. A human player's campaign knowledge and a narrator's
context are not authoritative character knowledge.

## Governing principles

Apply the [shared doctrines](README.md#shared-doctrines),
[Story-First Part I](../../story_first_design_doctrine.md#part-i--established-design-doctrine),
and [ADR-059 / ADR-061](../../decisions.md). Do not redefine them here.

Character history, campaign history, and world history differ. A replacement
character inherits the campaign world, not the former protagonist's private
knowledge, relationships, or motivations. This is **Accepted design**, not an
implemented character-replacement mechanism. The campaign's persistence beyond
a protagonist does not prohibit durable state for the current character.

## Current model

Use three working responsibilities rather than a separate subsystem for every
possible character attribute. This decomposition is **Provisional**.

| Responsibility | Current model and limits |
|---|---|
| Capability and relevant constraints | Authoritative competence plus character-specific advantages/limitations when established. Three competence tags are implemented; general attributes, conditions, equipment effects, and development are not. |
| Perspective and informational access | Distinguish current observation, expertise-based recognition, ordinary lived familiarity, and access through reports or investigation. Local projection exists; general sensory/access and familiarity policy do not. |
| Selective retention and continuity | Preserve consequential acquired information and accepted character-related results where future play depends on them. Discovery membership and attempts are implemented; a universal memory or belief system is not. |

Identity/background can ground all three responsibilities; there is no need yet
for an independent biography subsystem. Capability change and informational
change are lifecycle concerns within them, not proof of separate development or
memory engines. Injury, status, equipment, and relationships may constrain a
character, but their broader ownership and transition rules remain open.

## Resolution depth

**Accepted design:** infer ordinary familiarity from established residence,
occupation, repeated travel, public exposure, or relationships. If necessary,
resolve the relevant ordinary detail lazily against established circumstances.
This is intended engine reasoning, not permission for a narrator to invent
consequential access or a claim that such inference is implemented.

For example, a month in Bryn Shander can justify knowing major streets, public
businesses, and ordinary routines. Traveling a street routinely can justify
knowing where the baker is without a discovery ID. Neither circumstance grants
knowledge of hidden rooms, private ownership arrangements, secret activity,
unusual recent changes, or contested claims. Stronger specificity needs a
credible access path and appropriate provenance.

Persist exceptional access when later choice, inference, interaction, or
continuity depends on the character having encountered it and that access
cannot be reconstructed reliably. A privately received report, specialist
finding, or contested account can warrant explicit retention. An ordinary
currently visible object need not. Where provenance or timing matters, prefer
the existing causal-history direction over an exhaustive timestamped ledger.
Active simulation is justified only by a demonstrated consequential process;
there is no general character process simulator today.

## State and lifecycle

The following field map separates conceptual responsibility from the shared
`world_state` container. It is not a schema redesign.

| Current field / record | Conceptual responsibility and evidenced scope |
|---|---|
| `player.competences` | Character capability: unique supported tags, empty by default. Initial state can supply profiles; no production profile-selection UI or gain/loss operation. |
| `player_discoveries` | Character-specific encountered-information membership despite the historical name. IDs join authored clue text; records can retain reports or limited inferences as well as findings. No detailed human-player knowledge ledger. |
| `actor_knowledge` | Sparse per-static-actor information membership, not external world truth. Character-information grounding exists; the generalized Character System / Actors & Social Dynamics interface is provisional. Opaque IDs have no universal belief or truth semantics. |
| `competence_attempts` | Durable Action & Resolution results with character-specific basis and continuity. Stores draw/result, specialist flag, cost, findings, and source/time/outcome references; its location does not make adjudication Character System authority. |
| Related `history` entries | Campaign event/provenance records supporting acquisition and accepted attempts, not an exhaustive character memory. Structural source links alone do not prove witnessing, understanding, or reliability. |
| `player.current_location_id`, `evidence_traces`, `west_road_predicament`, `west_road_market_theft` | External position/evidence/situation truth owned outside Character System; inputs to access and resolution, not copies inside knowledge. |
| Perception, recognition packets, Scene Context, `SceneContinuity` | Derived access/presentation views or session-only descriptive claims. They are not persistent character truth. |

**Implemented, bounded:** accepted discoveries, actor membership, competence,
and attempts survive travel and version-1 save/load. Successful load rebuilds
derived scenes. Missing additive competence/discovery/knowledge fields have
specific copied-load empty normalization; actor seeds are not reapplied on
load. Malformed state rejects. Revised Bryn Shander still requires its
predicament record under ADR-060; historical pursuit needs no competence attempt.

Recognition is derived without a die draw or acquisition record. Accepted
attempt replay returns the stored result without drawing, charging time, or
republishing, including after load. It is not an anti-save-scumming guarantee.
Attempt validation currently requires its specialist basis to agree with current
tags; future competence gain/loss would need an explicitly authorized design
rather than merely mutating tags around historical attempts.

**Accepted design:** technical boundaries do not cause forgetting, re-learning,
or fictional time passage. Elapsed fictional time may make understanding stale,
but does not automatically rewrite it to match current world truth. There is no
implemented aging/forgetting or stale-belief transition policy. Presentation
continuity resets on location change and successful load/reset; that reset has
no character-memory meaning. A deliberate new-game reset creates fresh state.

## Inputs

- Validated character capability and retained information membership.
- Authoritative local world facts, evidence, position, conditions, and accepted
  events; authored declarations constrain their interpretation.
- Established lived circumstances for future familiarity reasoning; no present
  residence/occupation/familiarity schema is implied.
- Validated acquisition and action results from owning gameplay systems.
- Player-declared attention/intent as a relevance input, never proof of
  capability, observation, success, or private informational access.

Provider prose and arbitrary biography/equipment claims are not authoritative
inputs to competence or knowledge.

## Outputs and relationships

See the [Character System information flow](system-map.md#dependencies-and-information-flow-around-character-system).

Character System provides Action & Resolution with established capability,
limited recognition, and retained informational access relevant to an attempt.
World Simulation supplies the evidence and circumstances; adjudication returns
accepted findings and external consequences through the existing guarded state
transition. Assistance is a situational resource, not a competence tag.

Narrative Experience / Player Presentation receive safe observations, reports,
recognition, qualified findings, available approaches/costs, and accepted
outcomes. They may express precision and confidence appropriate to the supplied
status; they cannot grant competence, improve a failed result, invent evidence,
or turn an uncertain interpretation into fact. Persistence saves/restores
validated supported state without owning its fictional meaning. Scenario &
Authored Content supplies seeds and bounded declarations, not mutable memory.

## Player-facing projection

| Layer | Meaning and current support |
|---|---|
| World truth | What is actually true regardless of who knows it. External reality belongs to World Simulation. |
| Current perception | What can currently be observed or received locally. Derived scene visibility and bounded cues exist; generalized senses, occlusion, and observer-specific limits do not. |
| Recognition / interpretation | What expertise makes apparent from applicable evidence. V1 separates automatic limited recognition from uncertain active investigation and accepted findings. |
| Familiarity | Ordinary background understanding grounded in lived circumstances, potentially stale. Accepted direction; no runtime familiarity model. |
| Acquired information | Selectively retained encounters, including reports and limited findings. Discovery and actor membership exist; they are not a universal factual memory. |
| Belief / inference | Understanding that may be uncertain, incorrect, or stale. Accepted distinction; bounded inference labels exist, but no general belief representation or update policy. |
| Human-player information | What the person has read or remembers. Does not automatically transfer to a character; no exhaustive ledger is intended. |

Local scene relevance is a presentation filter, not forgetting. At Market
Square, remote West-Road observations, recognition, findings, approaches, and
accepted outcomes are suppressed while stored discoveries/attempts remain.
Explicit clue review and resume can still recall accepted information. Conversely,
the market theft can become world truth before observation; seeing it locally
does not disclose a thief's identity or hidden cause and need not add a discovery.

Scene Context's `character_perspective` copies the filtered competence packet.
It is not a general observer model. Attention stages and remembered incidental
prose shape descriptive detail; looking closely need not create a clue or a
persistent informational record.

## Current implementation

| Capability | Classification and evidenced limit |
|---|---|
| Character Competence V1 / 10.78 | **Implemented, bounded:** `tactical_assessment`, `outdoor_tracking`, `surveillance_analysis`; applicability requires the withdrawal phase, known tracks, and matching physical trace. No universal skill/stat framework. |
| Recognition / eligibility | **Implemented, bounded:** recognition uses authored evidence and tags read-only; three operations share projection/execution eligibility. Operations require North-Gate coordination with Grey and Elin. Survey uses committed guard assistance, never a character tag. |
| Attempt resolution and retention | **Implemented, bounded, shared with Action & Resolution:** tracking/circuit cost one hour and use an engine d6. Ordinary draws 1–2 fail, 3–4 partial, 5–6 full; relevant specialist draws 1–2 partial, 3–6 full. Deterministic survey costs two hours, one with tactical competence. At most one accepted record per operation. |
| Findings / consequences | **Implemented, bounded:** failure adds no discovery; partial adds supported direction or overlap inference; full reuses the existing withdrawal-route/pursuit outcome. No identity, affiliation, unverified destination, capture, or universal investigation model. Ordinary continuation remains available. |
| Player acquisition / review | **Implemented, bounded:** local investigate selects the first eligible undiscovered authored trace declaration; revised West-Road paths also retain specific reports/findings. Known-clue review joins membership to authored titles/text. No observation-by-observation memory. |
| Actor knowledge | **Implemented membership; Partial informational model:** static-actor seeds, explicit additions, duplicates as no-ops, backward event linkage, narrow declared conversation/report effects and exact authored responses. No universal witnessing, certainty, loss, rumor propagation, or autonomous reasoning. Legacy mechanism tests do not imply prototype declarations remain active in revised play. |
| Perspective / perception | **Partial:** base perception treats current scene entities/environment as visible. Authored pressure cues and local West-Road/market filtering add bounded access controls; no general sensory or knowledge-dependent visibility model. |
| Character continuity | **Partial:** supported persistent fields restore and attempts replay without reroll. No multiple-protagonist identity model, general development, or informational aging. Disk-save atomic replacement is not established. |
| Familiarity / durable change | **Accepted design / Provisional mechanisms:** ordinary familiarity and selective knowledge continuity are accepted; levels, representation, conditions, relationships, equipment effects, and advancement rules are unsettled and unimplemented. |

## Accepted and provisional decisions

**Accepted design:** minimum sufficient character detail; separate truth,
perception, familiarity, acquired information, and belief; sparse consequential
retention; believable lived experience beyond played scenes; campaign continuity
across protagonists; and capability that diversifies paths. ADR-061 supplies
the accepted bounded competence semantics, not a mandate to generalize them.

**Provisional:** the three-part model, shared player/NPC information interface,
familiarity categories (ADR-059 leaves names and levels open), how character
conditions affect access/capability, and how uncertain/stale understanding is
represented. Residence or repeated exposure might support reasoning without
requiring a new ledger. This review selects no schema or resolution algorithm.

## Deferred capabilities

General skills/stats/classes, character creation/profile UI, advancement,
injury/impairment/recovery, equipment modifiers, social status/relationship
mechanics, universal familiarity/belief/memory, rumor propagation, and
protagonist replacement remain outside this package. These exclusions do not
schedule future implementation or freeze ownership of all those domains.
No runtime refactor, storage split, migration, save-version change, or later
system manifest is authorized here.

## Known tensions / open questions

- **Storage terminology:** architecture and ADRs use World State as the durable
  simulation container. This does not give the narrower World Simulation
  responsibility ownership of competence or encountered-information membership.
  `player_discoveries` serves the current character, not a human knowledge ledger;
  no multi-character reassignment semantics are implemented.
- **Historical scope:** ADR-049's original non-projection exclusions and Simulation
  Model section 20's non-dialogue boundary describe foundational slices. ADR-051,
  ADR-060/061, and later source demonstrate specific authored responses, sharing,
  and safe competence projection. They do not establish general semantic knowledge
  or invalidate the older evidence. The Model's linear information diagram is a
  conceptual access example, not a requirement that all observation pass through
  public rumor or actor knowledge.
- **Projection gap against accepted direction:** base perception assumes scene
  visibility; navigation joins immediate exits to authored destination names,
  and destination resolution searches authored region locations without a
  familiarity/access check. ADR-059 says topology alone must not grant knowledge.
  These bounded shortcuts do not prove universal legitimate access; a future
  package must determine when destination naming needs character grounding.
- **Presentation terminology:** architecture's preview-only/not-automatic summary
  predates the accepted 10.80 CLI presentation paths. Scene continuity's remembered
  descriptive claims are untrusted presentation state, not character memory or
  consequential truth. Owner smoke reports improved attention progression, not a
  persistent epistemic capability.
- **Unsettled authority:** individual NPC access constrains decisions, but how
  Character System and Actors & Social Dynamics share belief/relationship state
  needs a future bounded design. Injury, possession, and status can have external,
  relational, and character-capability aspects; no blanket transfer of ownership
  is justified by this review.
- **Persistence / change gap:** accepted-attempt basis assumes unchanged tags;
  future development must preserve historical meaning. Direct JSON disk writes
  lack demonstrated atomic replacement, as recorded in World Simulation. These
  are implementation limits, not authorization to repair or migrate state.

No conflicting authoritative requirements require a decision for this
documentation task. The access gap and unsettled interfaces remain explicit;
historical documents have not been rewritten to conceal them.

## Evidence

Source/test inspection at the baseline supports the classifications above.
Gameplay suites and live providers were not run for this documentation review.
Historical verification and owner acceptance are reported by the handoffs, not
claimed as checks performed here.

| Evidence | What it supports |
|---|---|
| [Framework](README.md), [World Simulation](world-simulation.md), [system map](system-map.md), [architecture](../../architecture.md) | Shared doctrine, conceptual ownership versus shared storage/runtime orchestration |
| [Simulation Principles](../../simulation_principles.md), [Simulation Model](../../simulation_model.md), [Story-First Doctrine](../../story_first_design_doctrine.md), [ADRs](../../decisions.md) | Knowledge/truth distinctions, world continuity, sparse retention, passive/active access; especially ADR-014/015, 045–049, 051, 059–061 |
| [10.77](../../sprint_10_77_handoff.md), [10.78](../../sprint_10_78_handoff.md), [10.79](../../sprint_10_79_handoff.md), [10.80](../../sprint_10_80_handoff.md) | Accepted bounded slices, historical competence comparison smoke, local causality, and final attention/continuity smoke; ADR-059 also preserves 10.60 play findings |
| [Competence authority](../../../engine/character_competence.py), [GameEngine](../../../engine/game_engine.py), [competence tests](../../../test_character_competence.py), [authored Bryn Shander](../../../data/regions/bryn_shander.json) | Tags, applicable evidence, recognition, eligibility, local results/costs, replay, candidate rollback and save validation |
| [World State](../../../engine/world_state.py), [save system](../../../engine/save_system.py), [save/load tests](../../../test_save_load.py) | Persistent field ownership map, copied-load normalization and restore boundaries |
| [Action eligibility](../../../engine/action_eligibility.py), [discovery tests](../../../test_discovery.py), [player discovery response](../../../engine/player_discovery_response.py), [evidence traces](../../../engine/evidence_traces.py) | Local acquisition versus physical evidence; known clue review and bounded responses |
| [Actor knowledge](../../../engine/actor_knowledge.py), [response](../../../engine/actor_knowledge_response.py), [membership tests](../../../test_actor_knowledge.py), [conversation tests](../../../test_conversation_actor_knowledge.py) | Opaque membership, seeds/additions, structural provenance, save continuity and non-general conversation effects |
| [Perception](../../../engine/perception_builder.py), [navigation](../../../engine/navigation_projection.py), [Scene Context](../../../engine/scene_context.py), [continuity](../../../engine/scene_continuity.py) | Simplified visibility, destination naming gap, locally filtered perspective and non-durable presentation claims |
| [Scene relevance tests](../../../test_west_road_scene_relevance.py), [context tests](../../../test_scene_context.py), [CLI route tests](../../../test_player_scene_route.py), [skill-check scaffold](../../../engine/skill_check.py) | Local suppression without forgetting, safe intent/perspective contracts, presentation resets; deterministic placeholder checks do not establish a character skill model |

## Revision history

- October 6, 2026: established the Character System manifest from bounded
  competence, information-access, persistence, and accepted play/design evidence;
  kept generalized character mechanics and cross-system interfaces unsettled.
