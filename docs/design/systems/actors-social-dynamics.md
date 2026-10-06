# Actors & Social Dynamics — Design Manifest

## Status

- Overall: **Partial** — stable actors and bounded authored social behavior exist;
  general intentional decision-making does not.
- Last materially reviewed: October 6, 2026, documentation baseline
  `63f1a3db8b8996efe0f8245ad21d22ddb234dcbc`.
- Review candidate; relevant milestones: [10.77 predicament](../../sprint_10_77_handoff.md),
  [10.78 competence](../../sprint_10_78_handoff.md),
  [10.79 consequences](../../sprint_10_79_handoff.md).

This living responsibility model follows the [manifest framework](README.md).
It distinguishes accepted direction from a provisional decomposition and deferred
mechanisms. It authorizes no implementation, persistence model, or new package.

## Purpose

Own meaningful intentional non-player choices and the consequential social
continuity needed to make those choices coherent. This includes individuals and,
conceptually, organized groups, institutions, and factions when their agency
matters. It does not require treating a group as one large NPC.

## Player-facing goal

People can have intelligible reasons, limited knowledge, relationships, and
commitments that matter beyond one exchange. Their cooperation, resistance, and
independent activity can produce lasting consequences without universal NPC
simulation or narrator-invented decisions. Player intent remains player authority.

## Authority

The accepted map assigns meaningful intentional NPC/faction decisions here.
An intentional decision establishes what an actor chooses to do, withhold, pursue,
or commit to under the circumstances. Cooperation, refusal, deliberate deception,
warning, sharing, deliberate relocation, and reactions to pressure can qualify
when their meaning affects play. A proposed choice is not an accomplished action.

The working refinement includes consequential relationships, motivations, and
commitments needed to support such choices. Their representation and interfaces
remain **Provisional**; the review does not adopt a new mutable social schema.
Actors may choose deterministically: authority does not require an AI planner,
randomness, or a continuously running agent.

The existing contractual boundary is engine-owned simulation authority. Provider
output is untrusted; narration cannot establish consequential intentions,
knowledge, allegiances, promises, or actions. Any future AI-proposed choice needs
owning gameplay acceptance before expression or effects can treat it as settled.
No such general proposal/acceptance mechanism is claimed here.

## Explicit non-authority

- World Simulation owns external circumstances, effective positions, resulting
  external changes, time, and later non-intentional causal progression.
- Character System owns capability and character-specific informational state
  and access basis. This system consumes those inputs, not a duplicate knowledge store.
- Action & Resolution adjudicates attempts, costs, uncertainty, and contests;
  it does not independently choose another actor's wants or commitments.
- Scenario & Authored Content establishes foundations and supported bounded
  behavior declarations. Authored personality prose alone is not executable policy.
- Narrative Experience expresses accepted behavior; Player Presentation handles
  input and safe display. Neither has authority to complete a consequential choice.
- Persistence stores/restores established meaning and compatibility. Storage in
  `world_state` does not assign all conceptual ownership to World Simulation.

The protagonist is not an autonomous NPC. Relationship state may connect the
protagonist to others without selecting player goals, consent, or responses.

## Governing principles

Apply the [shared doctrines](README.md#shared-doctrines),
[Simulation Principles](../../simulation_principles.md),
[Simulation Model](../../simulation_model.md), and accepted
[Story-First Part I](../../story_first_design_doctrine.md#part-i--established-design-doctrine).

- Agency requires authority; narrative plausibility alone is not acceptance.
- Named existence does not justify goal stacks, schedules, relationship scores,
  belief graphs, memory ledgers, or autonomous processing.
- Knowledge constrains decisions. World truth or provider context does not grant
  access; plausible ordinary access need not become exhaustive epistemic simulation.
- Relationships deserve persistence when future reasoning needs them, not because
  every social exchange requires an affinity update.
- Actor life exceeds the transcript. Ordinary routines can remain inferred;
  established consequential facts constrain later inference.
- Decisions and consequences have distinct owners even in one atomic transition.

## Current model

Three **Provisional** conceptual responsibilities are sufficient for this review;
they are not runtime modules or a required pipeline.

| Responsibility | Meaning and present grounding |
|---|---|
| Social continuity | Identify the same participant and retain only consequential stance, relationships, motivations, commitments, and prior decisions. Stable authored identity and bounded history exist; mutable social continuity is largely future work. |
| Decision basis | Combine relevant external circumstances, legitimate informational access, capability, authored constraints, and established social continuity. Consume Character System information without copying it into a social model. Present basis is fixed scenario eligibility. |
| Intentional choice | Establish a meaningful response or independent action and pass attempts/consequences to their owners. Present behavior is bounded authored policy; general decision selection and independent activity remain deferred. |

Identity is a continuity requirement across systems, not a demand for a general
character sheet. Informational basis is an input, not a fourth knowledge subsystem.
Independent activity is a context for choices, not inherently another scheduler.

## Resolution depth

Use **Inference → Lazy resolution → Explicit persistent state → Active simulation**.
These are design levels, not implemented promotion/demotion machinery.

| Level | Actor application and limit |
|---|---|
| Inference | An incidental shopkeeper's ordinary work can follow role, place, time, and context. Naming them does not require tracking their day. Compatible incidental expression cannot establish a consequential sale, promise, or disclosure. |
| Lazy resolution | Later relevance may justify determining whether someone plausibly heard a public event or is normally available. Respect last established facts and legitimate access; hidden information and consequential deliberate choices require stronger justification and the proper owner. |
| Explicit persistent state | Established hostility, debt, allegiance, an unresolved commitment, or a goal may need continuity when later play depends on it. These are conceptual examples, not implemented fields or mandatory numeric meters. |
| Active simulation | A consequential objective may justify stronger tracking when timely independent action materially changes play. It does not automatically justify continuous ticking, complete schedules, or simulating every participant. |

Direct player relationships, repeated interaction, ongoing conflict, persistent
investment, responsibility for material change, or relevant institutional leadership
can earn specificity. A title or faction membership alone does not. Explicit
routine/schedule state is justified when timing, interception, availability,
deviation, or consequences matter; normal life otherwise remains inferential.

## State and lifecycle

**Implemented:** static `entity_id` connects authored identity to sparse location
overrides, knowledge membership, and supported history. Authored name, type,
description and baseline location are loaded from content. Returning to the
baseline location removes an override; the fictional person remains the same.
Spawned guards have template/location/display data without stable instance IDs;
they are not individually persistent agents. Fictional identity is more than the
current storage key, but no general actor creation/replacement lifecycle exists.

Conversation history records accepted occurrence and grounded target, not a
transcript, promise, relationship, or inferred understanding. West-Road phase and
causal outcome history preserve bounded commitments and reports. Guard allocation
is represented by phase, not a roster or separate social state. Scoped pressure
levels are external conditions, not actor emotions or dispositions.

**Accepted design:** established consequential social meaning must survive save/load,
model calls, UI changes, and technical sessions. This includes known information,
relationships, unresolved commitments/goals, meaningful decisions, and necessary
causal provenance where actually established. It is not a claim that those general
records exist. Dormancy does not erase a commitment or require offscreen ticking.

The minimum useful history answers which participant made a material choice,
what was committed or changed, and the causal basis/reference needed by later
play. Retain timing or informational provenance when consequential. This is a
retention criterion, not a new event schema or exhaustive life log. Existing
structural source references alone do not establish witnessing or semantic truth.

### Offscreen action

Ordinary background change can be inferred or lazily reconciled by World
Simulation without instantiating an intentional individual. A meaningful
offscreen choice by an established actor belongs here; resulting external truth
belongs to World Simulation, with Action & Resolution involved when adjudication
is needed. Offscreen does not weaken authority or informational constraints.

**Design example, not implemented:** ordinary maintenance may explain a sealed
sewer without simulating a worker. An established antagonist deliberately ordering
it sealed to obstruct the player requires authoritative intentional choice and
enough retained causal provenance to distinguish obstruction from maintenance.
Neither requires an exhaustive worker schedule. Lazy resolution may not rewrite
already established history to invent convenient motives or connections.

## Inputs

Relevant world circumstances and history; character capability and legitimate
informational access; authored identity, roles, motivations, relationships and
bounded declarations; established social commitments; player requests/actions and
accepted resolution results. A request to cooperate is not cooperation itself.
Untrusted model suggestions, if ever supported, remain proposals.

## Outputs

Authoritatively accepted intentions/responses and relevant commitments; attempts
requiring resolution; accepted effects for World Simulation and legitimate
information acquisition for Character System; enough continuity/provenance for
future reasoning; player-safe behavior and attributed reports for expression.
These general interfaces are **Provisional**, grounded by the narrow paths below.

## Relationships

See the [system map](system-map.md#dependencies-and-information-flow-around-actors--social-dynamics).

| Other responsibility | Boundary |
|---|---|
| World Simulation | Circumstances inform choices; executed actions establish external consequences there. Non-intentional progression does not need a newly invented actor. |
| Character System | Owns information/access and capability; this system uses that basis to choose whether to disclose, conceal, cooperate, or act. Actual acquisition updates the existing informational responsibility. The general NPC interface remains provisional. |
| Action & Resolution | Actor intention/response supplies premises; resolution determines a contested or uncertain attempt's outcome. That outcome can inform a later choice without automatically deciding willingness or motivation. A social interaction need not require a check. |
| Scenario & Authored Content | Supplies actors, roles, relationship/motivation foundations, dialogue material and supported behavior constraints. Fixed transitions can encode bounded behavior without a general motivation engine. |
| Narrative Experience | Expresses accepted behavior and appropriately attributed claims. Expressive tone cannot silently create hostility, trust, deception, allegiance, or commitments with future consequences. |
| Player Presentation | Accepts player intent and displays eligible interactions, reports and outcomes. Displaying an option does not choose it or grant success; internal social/informational state need not be shown. |
| Persistence | Preserves supported state and references; does not select fictional intentions or reset them at technical boundaries. Future social storage/compatibility decisions need separate authorization. |

## Player-facing projection

A visible departure does not disclose its motive. A spoken report is not proof
of its content, and a refusal need not expose private goals. Player-safe views
should communicate intelligible behavior and usable choices while preserving
truth, belief/report, and inference distinctions. Current authored replies and
safe scenario projections supply bounded examples; no general social perspective
filter or believable-dialogue guarantee is implemented.

## Current implementation

| Capability | Classification and evidenced limit |
|---|---|
| Actor identity/location | **Implemented, bounded:** authored static IDs, sparse overrides, scene-based targeting and durable movement history. Explicit, conversation-resolution, and elapsed-time relocation mechanisms exist; movement effects do not establish freely selected travel intentions. |
| Informational membership | **Implemented, bounded:** nonempty authored static-actor seeds copied at new game; unique opaque IDs, explicit additions, optional backward source links and declared conversation/resolution additions. No general truth, belief, certainty, loss, access reasoning or propagation model. |
| Knowledge affecting behavior | **Partial:** generic authored response checks command-start membership. Current West-Road report membership gates initial choices; revised phase responses use phase and recorded witnesses. These are different paths, despite the shared result name `actor_knowledge_response`. Neither is general knowledge-driven planning. |
| Reports/sharing | **Implemented, bounded:** presenting an encountered clue to present Grey/Elin records recipient-specific `west_road_received:` membership and a sharing source. Elin must receive both initial reports before the first decision. Fixed later outcome preparation records new reports to both witnesses. Duplicate reports do not reapply membership; no general NPC-to-NPC rumor network. |
| Conversation/social interaction | **Partial:** accepted local target/occurrence history, exact authored replies, Mara's bounded account discovery, and declared effects. Conversation success means accepted interaction, not persuasion, agreement, a lie, or an open dialogue policy. No general social contest exists. |
| Pressure/reaction | **Implemented declared effects; broader reaction deferred:** a matching conversation can set an exact pressure level; explicit elapsed-time thresholds can trigger supported changes. These are deterministic content/effect rules, not appraisal of fear, trust, hostility, or actor goals. |
| Motivations/decisions | **Partial authored behavior:** Grey's concern and Elin's evidence/coverage tradeoff appear in premise and phase text. Fixed commands select seven-phase transitions, commitments and outcomes. No general runtime goal stack, motivation evaluator, deliberation or autonomous planner. |
| Guard behavior | **Implemented scenario abstraction:** named coordination at the gate, phase-based coverage, and committed assistance for guarded survey. Tactical competence changes survey time, not willingness. Spawned watch guards are scene groups, not individually assigned patrol agents. |
| Relationships | **Partial content only:** Grey has authored trust/alertness and Watch authority/loyalty; Elin has authored respect/authority toward Grey. No inspected runtime consumer turns these numeric foundations into mutable trust, reputation, obligation or cooperation policy. Conversation/report history is not a relationship model. |
| Factions/groups | **Partial representation only:** Town Watch content includes identity, influence, player stance, readiness, morale and objectives; scene construction lists faction IDs. No mutable faction decision process, institutional knowledge, group goal execution or faction persistence overlay is implemented. |
| Offscreen consequence | **Implemented fixed world rule:** two qualifying reduced-coverage hours establish one market theft independently of observation. Thief/motive/affiliation remain unknown; it does not instantiate a thief or evidence autonomous antagonist planning. |
| Persistence/continuity | **Partial:** version-1 state stores supported membership, overrides, history, scenario phase and outcomes; load rebuilds scenes and does not reseed missing legacy knowledge. Authored profiles/relationships/factions are reloaded content, not saved mutable social state. No general persisted stance/goals/relationship model. |

The revised ordinary-play pack supersedes prototype declarations; legacy mechanism
tests use the explicitly test-only fixture. Do not describe every historical
conversation, recall, pressure or relocation declaration as active Bryn Shander play.

## Accepted decisions

Meaningful intentional non-player agency belongs here, with player intent reserved
to the player. Knowledge is not world truth; informational access constrains
choices. Agency and consequence require simulation authority, downstream expression,
minimum sufficient detail, and continuity independent of technical sessions.
ADRs 035, 039, 043–047, 051–054 and 059–061 establish bounded occurrence/effect,
identity, knowledge, response, relocation, specificity and scenario contracts;
they do not collectively authorize a general social AI system.

## Provisional decisions

The three-part decomposition, consequential social-state responsibility, general
NPC information interface, and individual/group decision interfaces remain
revisable. Motivation and relationship persistence should follow demonstrated
continuity needs. No universal scalar representation, actor scheduler, promotion
policy, new schema, or module split is selected.

## Deferred capabilities

General autonomous actors, offscreen intentional decision machinery, goal stacks,
schedules, social checks, relationship/reputation systems, belief/rumor propagation,
dynamic actor promotion, faction AI, and general history compression remain outside
this review. Accepted independent-agency direction does not schedule these mechanisms.

## Known tensions / open questions

- **Representation versus behavior:** numeric relationship/personality fields and
  faction objectives already exist as content. Their presence is not acceptance
  of universal meters or proof of executable semantics. Future use needs a real
  player-facing case and an authorized contract.
- **Information gap:** opaque membership and backward links do not establish all
  semantic access. West-Road sharing and witnesses enforce a narrow basis; a future
  decision mechanism must not generalize that into omniscience.
- **Identity gap:** static keys preserve current continuity, while spawned actors
  lack stable instance identity. When an incidental person earns persistence, the
  identity/ownership and promotion contract remains open.
- **Agency depth:** what minimum state and activation conditions support an actor's
  consequential independent objective without continuous simulation? Ordinary
  schedules and goals should not become mandatory by default.
- **Group responsibility:** how should institutional commitments and information
  differ from a leader's private knowledge or personal goals? The scope includes
  both without selecting a shared representation or implying perfect consensus.
- **Causal retention:** which social choices require durable provenance beyond
  existing occurrence/report history, and how can older history be reduced while
  preserving unresolved obligations and invested relationships?
- **Historical terminology:** Simulation Model's World Evolution includes actor
  goals under a broad umbrella. The responsibility map separates intentional
  choice from resulting reality; this does not require editing protected manifests.

No fundamental contradiction requiring changes to the three protected manifests
was found. These are implementation gaps and unsettled future interfaces.

## Evidence

Runtime, authored content and test assertions were inspected at the baseline.
Tests listed here were read, not executed for this documentation-only review.
Handoff verification and owner smoke are historical evidence, not new test results.

| Evidence | Supports |
|---|---|
| [Architecture](../../architecture.md), [principles](../../simulation_principles.md), [model](../../simulation_model.md), [doctrine](../../story_first_design_doctrine.md), [ADRs](../../decisions.md) | Authority, locality, continuity, minimum detail and historical decisions |
| [World](world-simulation.md), [Character](character-system.md), [Action](action-resolution.md) manifests | Protected responsibility boundaries and current limitations |
| [Current content](../../../data/regions/bryn_shander.json), [legacy fixture](../../../test_fixtures/bryn_shander_legacy.json), [fixture note](../../../test_fixtures/README.md) | Named actor profiles, authored relationships/faction objectives, fixed behavior and historical mechanism separation |
| [World State](../../../engine/world_state.py), [scene loader](../../../engine/scene_loader.py), [location tests](../../../test_actor_location.py) | Stable identity, effective positions, spawned groups, faction IDs and continuity |
| [Knowledge](../../../engine/actor_knowledge.py), [knowledge tests](../../../test_actor_knowledge.py), [response](../../../engine/actor_knowledge_response.py), [response tests](../../../test_actor_knowledge_response.py) | Sparse membership, command-start response gating, no general belief or relationship model |
| [GameEngine](../../../engine/game_engine.py), [interaction kernel](../../../engine/interaction_kernel.py), [conversation knowledge tests](../../../test_conversation_actor_knowledge.py), [pressure tests](../../../test_conversation_pressure_effect.py), [relocation tests](../../../test_conversation_actor_relocation.py) | Accepted interaction, fixed effect composition, idempotence, failure isolation and source references |
| [Predicament](../../../engine/west_road_predicament.py), [predicament tests](../../../test_west_road_predicament.py), [10.77](../../sprint_10_77_handoff.md) | Reports, witnesses, phase ownership, all branches, rollback and saved continuity |
| [Competence tests](../../../test_character_competence.py), [10.78](../../sprint_10_78_handoff.md) | Guard coordination, eligibility, existing assistance and bounded resolution |
| [Theft rule](../../../engine/west_road_market_theft.py), [theft tests](../../../test_west_road_market_theft.py), [10.79](../../sprint_10_79_handoff.md) | Consequence without invented actor identity, local revelation and persistence |
| [Save system](../../../engine/save_system.py), [Scene Context](../../../engine/scene_context.py), [10.80](../../sprint_10_80_handoff.md) | Stored versus derived state, authority limits and technical presentation continuity |

## Revision history

- October 6, 2026: initial review candidate; refine intentional agency and social
  continuity while distinguishing authored representations, fixed scenario behavior,
  informational ownership and deferred autonomous simulation.
