# AI RPG — Core Gameplay Domains: Cross-Domain Contract Design V1

**Phase:** Design, Stage A  
**Date:** October 25, 2026  
**Status:** Owner-accepted October 25, 2026 (CD-01–CD-09 and the four consolidated architectural directions); Design only  
**Origin:** Approved *Core Gameplay Domains — Research → Design Handoff* (October 25, 2026)  
**Repository:** `Mixelplux/AI-RPG`  
**Scope:** General contracts among World Simulation, Character System, Action & Resolution, and Actors & Social Dynamics. No implementation or Git publication authorized.

## 1. Purpose and inherited authority

The target is a persistent, open-ended AI RPG whose gameplay domains cooperate coherently without becoming tailored to an initial traversal test. The accepted **Integrated Gameplay Architecture V1** (IG-01–IG-18, IG-20–IG-23; IG-19 excluded) already governs situated undertaking coordination, selective domain-owned dependencies, accepted consequences, continuity, and integrity. This document **specializes those contracts for core gameplay domains**; it does not create another coordinator, truth authority, or transaction system.

Authoritative inherited design:

- `docs/design/integrated-gameplay-architecture-v1.md` and its implementation plan;
- `docs/design/information-foundation-functional-design-v1.md` (D1–D16) and `information-grounded-adjudication-v1.md` (D-A1–D-A6);
- `docs/design/f05-authorized-activities-and-player-control.md` and `f01-truthful-presentation-and-epistemic-fidelity.md`;
- `docs/design/systems/README.md`, `system-map.md`, and the individual system manifests;
- the owner-approved Research handoff, including T-R1–T-R11.

Accepted strategic direction: D&D **2024 revised fifth-edition core mechanics** provide the mechanical foundation, with explicit justified adaptations; PCs and NPCs share relevant rule-facing semantics at different levels of representation detail; physical traversal is the first integration *validation* capability. Current experimental implementations are evidence, not normative architecture.

**Status convention:** The *requirements* above and CD-01–CD-09 were accepted by the owner on October 25, 2026. They are not claims about current runtime coverage or a demand for separate modules, services, databases, model calls, or schemas. Later domain-focused detail remains separately reviewable Design.

## 2. Contract map — semantic authorities

| Meaning | Owning authority | Relevant consumers / constraint |
|---|---|---|
| Authored setting foundations, creature and item definitions, rules reference material | Scenario & Authored Content / Information Foundation for provision; accepted rules/adaptations govern interpretation | The content source does not decide live attempts or rewrite accepted campaign state. |
| Current external reality: places, environment, time, physical objects, location/attachment/possession relationships and consequences | World Simulation | Does not decide player intent, actor intentional choices, or action success independently. |
| Creature-specific capability, conditions/resources associated with a creature, equipment use and legitimate informational access/retention | Character System | Supplies rule-facing facts for PC and NPC alike; cannot conjure physical means or objective world truth. |
| Attempt eligibility, applicable mechanics, uncertainty, costs and accepted attempt result | Action & Resolution | Applies actual rules and context; proposed external effects are accepted by relevant owners. |
| Intentional NPC/faction choices, social commitments, meaningful dispositions and relationships | Actors & Social Dynamics | May propose NPC acts, not choose outcomes of contested or mechanically governed attempts. |
| Executable scope and continuation of player undertakings | F05 and Integrated Gameplay coordination | Neither constitutes an outcome-owning fifth domain. |
| Saved/restored consequential meaning and compatibility | Persistence | Storage does not acquire the semantic authority of the records it stores. |
| Character-safe meaning and expression | F01 / Narrative Experience / Player Presentation | Internal truth does not automatically become character knowledge; narration has no consequential authority. |

One occurrence may affect several owners. For example, a successful climb can change world position, consume a character resource, advance fictional time and create a mechanically accepted result. **Multiple owners of different meanings do not require multiple separately visible or partially accepted outcomes.**

## 3. Proposed Stage A contracts

### CD-01 — Authoritative fact ownership and access

1. Every consequential meaning has a responsible semantic owner. A composite record may carry facts owned by several domains, but one field or relationship must not acquire contradictory competing authorities simply because several systems store or project it.
2. An authoritative read identifies the subject(s), relevant present or historical scope, applicable source or basis, and whether the information is established, inferred, unresolved, or not currently available. Identity and temporal meaning remain stable across consumers.
3. Domain consumers request only facts needed for their responsibility, including direct and relationship-based dependencies. The Information Foundation retrieves; the domain determines relevance and application. A material established fact that cannot be obtained blocks the affected decision internally, not through an invented replacement or leaked hint.
4. Contextual new facts enter the same owner as equivalent authored or previously accepted facts; no special “AI truth” store or separate factual status remains after legitimate acceptance.

**Boundary test:** A hidden surface hazard may constrain a climb without entering character-facing knowledge. If its record is established but unavailable, the attempt remains unresolved; if no condition was established, the World Simulation may establish a plausible condition before mechanical resolution under CD-03.

### CD-02 — Shared rule applicability and mechanical semantics

1. The resolution authority determines whether an undertaking is permissible, deterministic under known conditions, or governed by a check or another mechanic. Consequential uncertainty is resolved according to the applicable D&D 2024 rule and any explicitly accepted adaptation. Competence alone cannot replace an applicable consequential check.
2. A rules applicability decision uses, as relevant: authorized actor/method/target; current world and scene state; creature capabilities and conditions; possessed and usable means; governing rule definitions; effects, exceptions and binding circumstances; and already accepted attempt history.
3. The rule basis must be identifiable: **accepted adaptation, applicable 2024 rule, scoped authored feature/effect, or contextual ruling delegated or left open by those rules**. An authored property may create a valid exception within its declared scope, but an unexplained contradiction between rules or authored foundations is not quietly resolved by retrieval order.
4. The outcome must distinguish rule application, randomness, contextual establishment and final accepted consequence. A die result alone is not a complete fictional outcome. Critical results apply where the governing mechanic supplies them; do not invent universal natural-1 consequences.
5. PC and NPC uses of the same relevant rule have equivalent mechanics and semantic inputs. A creature can be represented sparsely if the information sufficient for its actual action is supplied, without constructing an exhaustive PC sheet.

**Deferred:** The precise canonical rules corpus, adaptation register entries, complete character statistics, full movement/combat/spell catalogs, and rule-implementation algorithms belong to later domain-focused work. This contract does not authorize copying or importing third-party content.

### CD-03 — Pre-resolution establishment of governing circumstances

1. Before resolving an outcome, each relevant owner establishes the minimum material circumstances its decision actually needs, using existing truth, contextual judgment, and where justified independent uncertainty. Do not invent unnecessary detail or universally require a coordinate/physics representation.
2. Distinguish (a) previously established facts, including hidden ones; (b) genuinely unspecified details that may be established now; (c) facts established but temporarily unavailable; and (d) genuine uncertainty appropriately resolved under rules or legitimate judgment.
3. Material facts newly established for a decision must be fixed *before* the uncertain attempt is resolved. They cannot be retrospectively selected to explain a preferred success or failure. Established facts and scope must be incorporated through the owning boundary if future action depends on them.
4. Contextual establishment is constrained by authored foundations, existing geography, causal history, actor capabilities and commitments, and the world’s actual fictional time. Arbitrary compensating obstacles or convenient favorable details are not valid substitutes for grounding.
5. Facts with merely incidental expressive significance need not all be registered or persisted. A detail becomes consequential when it materially governs an option, cost, risk, evidence, relationship, or later continuity.

**Boundary test:** The condition and availability of handholds are settled before deciding an uncertain climb. Failure cannot subsequently manufacture rotten stone merely to justify injury; success cannot retrospectively create a ladder or ledge not otherwise grounded.

### CD-04 — Coherent cross-domain consequence acceptance

1. A contemplated outcome has a proposed, unaccepted meaning. The relevant owners validate authorization, rule applicability, required premises, domain invariants, and the consequences they own. The coordinator arranges this, not adjudicates it.
2. Consequences that are logically dependent form **one coherent acceptance unit**. Either the valid unit becomes authoritative across affected meanings or none of its effects becomes fictional truth. Examples include a location change paired with elapsed time, expended resources, damaged gear and an accepted mechanical result.
3. Acceptance must verify that material premises still apply to the current authoritative state. A stale or technically rejected proposal cannot publish effects, consume resources, expose hidden truth, or be narrated as a fictional failure.
4. Accepted results receive stable recognition so later calls, retries, resumed presentation, and save/load do not repeat a charge, draw, result, or physical change. A future legitimate new attempt is distinct and must follow the rules and current authorization.
5. **Actual incremental progress** may be separately accepted at a meaningful boundary and persist even if a later proposed increment fails. Technical partial publication of an unaccepted unit is prohibited.
6. Acceptance establishes fictional result and causal order; the particular transaction, lock, revision, storage, or in-process implementation mechanism is not prescribed. Failed write/recovery must preserve or recover coherent accepted meaning, not silently reconstruct contradictory facts.

**Boundary test:** If a rope-supported climb advances one accepted segment, later inability to continue preserves that segment and any cost. If a single segment’s proposed position change is rejected because its supporting attachment became invalid, its dependent time/resource/position update is not partially published as though successful.

### CD-05 — Physical-object identity and cross-domain relationships

1. Consequential physical objects retain stable identity through location, carrying, holding, securing, attaching, transfer, damage, repair, dropping and recovery. An item definition and an individual world object instance are distinct, and neither its name nor a temporary inventory slot is its identity.
2. World Simulation owns the object’s external existence, material condition, spatial disposition and physical relationships; Character System establishes creature capability, relevant equipment-readiness/use and resource semantics. Definitions and applicable effects remain retrievable from authored/rules information.
3. Represent **relationships**, not just an object's single location label. One rope may simultaneously connect a railing to a harness while being carried or manipulated; those statements must be mutually physically coherent. Exclusive relationships (if applicable) are checked against actual conditions, not imposed universally on all object types.
4. Physical possession, legal/social ownership, immediate ability to use, attached position and currently equipped status are distinct meanings. Changing one does not silently imply all others. Ownership or obligations may require Actors & Social Dynamics; possession does not create consent.
5. All accepted object relationship changes participate in CD-04 coherence and subsequent retrieval. No global object registration for incidental descriptions is required until consequential identity or continuity is needed.

**Boundary test:** Dropping the only climbing rope removes its held relationship while preserving any still-valid attachment, location, condition, and later recoverability. The character cannot use the rope merely because an outdated inventory summary lists it.

### CD-06 — Meaningful activity, interruption and temporal order

1. F05 controls the authorized undertaking, chosen method, constraints, ordinary constituent execution, meaningful interruption and resumption. A broad objective may permit situated progress, but not materially different methods or new risk commitments chosen by the DM.
2. Resolution granularity follows meaningful activities and actual mechanics. Movement need not be decomposed into hand- and foothold operations merely for completeness. The accepted state records only progress, spent time/resources, resolved checks, changed conditions and restrictions needed for future integrity.
3. Fictional time belongs to World Simulation. Ordering records enough to distinguish establishment, attempt, consequence, perceptible development, opportunity to respond and continuation. Rules-specific ordering (such as an encounter mechanic when relevant) may refine that sequence; there is no universal scheduler mandate.
4. On resumption, the relevant owners re-evaluate current circumstances, available means, previously accepted mechanics/results, and the original method and restrictions. An interruption is not a free reroll, state rollback or automatic forfeiture of established progress. A true restart or new attempt follows the nature and governing rule.
5. Meaningful NPC actions, including offscreen ones, require legitimate intentional choice before their attempts are resolved and their external effects accepted. Routine world evolution can be inferred or lazily established without instantiating every worker or actor.
6. At natural re-entry, necessary offscreen developments are resolved before affected play using elapsed fictional time, history and causal commitments. They must not be engineered backwards to match unexpressed player plans.

**Boundary test:** During a climb, a newly perceptible change in fall risk or hostile observation may require a player decision if continuation would exceed prior authorization. A hidden, unperceived development does not automatically expose its cause or force a clarifying question.

### CD-07 — NPC parity, intention and resolution separation

1. Actor intention and willingness are established by Actors & Social Dynamics from authored motivations, current relevant circumstances, legitimate informational access, capability and consequential prior relationships. They are not narration inventions, and a DM cannot choose the player’s intentions in parallel.
2. An NPC's decision to assist, obstruct, warn, withdraw, attack or negotiate is not its automatic mechanical success. Where rules require it, Action & Resolution applies the same relevant rule-facing semantics as for the PC; World Simulation accepts external consequences.
3. Sparse NPC records may supply only the attributes, proficiencies, conditions, equipment, movement, senses or other inputs actually needed. Missing material information must be sourced or legitimately established, rather than granting an NPC arbitrary capability by narrative fiat.
4. An actor's beliefs and known facts are not a copy of omniscient world state. Retain exceptional secrets, misconceptions, commitments and accesses where future play depends on them; ordinary familiarity can be inferred under existing doctrine.

**Boundary test:** An NPC holding the same rope may help a climber only if they choose and are able to do so; any relevant assistance mechanic is adjudicated, and resulting position/rope state changes are accepted coherently.

### CD-08 — Character-facing access and truthful presentation

1. An accepted internal outcome must be projected through legitimate character access: relevant observation, senses, attention, competence, knowledge, historical basis, and available evidence. Accepted hidden causes do not become automatically known from their effects.
2. Keep objective truth, observed effect, report, interpretation, uncertainty, and established historical versus current applicability distinguishable where consequential. Narrative Experience expresses that meaning naturally and cannot add costs, opportunities, causal claims, actor decisions, or physical success.
3. A technical unresolved/rejected proposal is not a fictional obstacle or failed attempt. A successful mechanical resolution can still yield limited or no information where legitimate evidence is absent.
4. If narration fails after acceptance, the gameplay result remains accepted. Presentation repair may correct the player-facing account without repeating the mechanics or mutating authoritative truth. The F01 reliance/reconciliation principle remains proportional, not a requirement for a generalized compensation subsystem.

**Boundary test:** A hidden magical effect impedes a climb. The player learns only the accessible obstruction or result unless an authorized observation or investigation legitimately reveals the magical cause.

### CD-09 — Persistence, compatibility and scaling invariants

1. Saving and restoring must retain the consequential meaning needed for later play: stable object/actor/place identities, current facts, accepted attempts/costs, activity status and restrictions, meaningful relationships/commitments, fictional time, applicable history and the recognition required to prevent duplicate acceptance.
2. A restored campaign is validated as a coherent whole within its supported scope. Missing material references, invalid cross-domain relationships, incompatible meanings or unresolved accepted-unit corruption cannot be silently normalized into contradictory fictional facts. Failed restoration must not damage the live campaign.
3. Consequential current truth and historically valid claims are distinct. Authored references, campaign overrides, and past states require enough context to interpret them correctly after content updates; the general content-revision compatibility policy remains a separate open design problem.
4. Selective direct, relationship and history access is a functional requirement. Stable identifiers, scoped facts, relevant links and bounded retrieval should allow future indexing, partitioning, storage evolution and migration without changing gameplay semantics.
5. No graph database, exhaustive event ledger, universal entity framework, full-scene snapshot for each turn, autonomous world ticker or particular save format is prescribed. Growth should be evaluated using representative larger state and queries before selecting technology.

**Boundary test:** After save/load, a rope remains attached to the same rail and harness, a climber has the correct position and expended resources, and an accepted check is not rerolled simply because the display or process restarts.

## 4. Cross-domain collaboration for one meaningful action

The following is a **semantic contract sequence**, not a fixed runtime pipeline or required model-call count. Steps may be combined or omitted if not relevant, so long as the same guarantees hold:

1. **Understand the player's undertaking:** F05/coordination determines inquiry, preparation or commitment, method, constraints and next situated step.
2. **Identify responsible meanings and dependencies:** relevant domains declare necessary rules, world state, creature capability, objects, actors and hidden conditions; Information Foundation retrieves.
3. **Establish missing governing reality:** responsible owners resolve genuinely unspecified material facts before adjudication; remain unresolved if material established information is unavailable.
4. **Decide intentions and mechanics:** Actor authority supplies meaningful NPC choices where relevant; Action & Resolution chooses and applies legitimate rules for attempts without manufacturing prerequisites.
5. **Validate and accept dependent consequences:** relevant domains validate the complete effect unit against current premises, record accepted result/recognition and publish coherent effects.
6. **Continue or return control:** F05 uses fresh situation and retained activity semantics; save/persistence preserves the accepted meaning; F01 receives only legitimate player-facing projection.

No domain's participation is compulsory solely because it appears in this list. For ordinary uncontested walking, actor intention adjudication may not be needed. An NPC-dependent climb or a contested guarded crossing may need it.

## 5. Integrated validation — traversal tests the design

The initial integration method is climbing, but no climbing-specific handling belongs in the shared cross-domain contract. Representative checks:

| Validation case | Contract pressure | Evidence required |
|---|---|---|
| Ordinary supported climb, low consequence | CD-02, CD-03, CD-06 | Apply applicable movement/rules without micro-checks or needless mandatory domains. |
| Consequential uncertain surface | CD-01–CD-04 | Establish relevant surface/capability first, apply governing rule, and derive a specific result; a failed check does **not** automatically become falling or injury. |
| Rope attached to railing and harness | CD-04, CD-05, CD-09 | One stable object identity; multiple compatible relations; valid resource/time/position changes; persistence. |
| Equipment transfer or loss during progress | CD-04–CD-06 | Subsequent means, constraints, position and accepted costs use fresh truth; no automatic restoration or free retry. |
| Partway progress, interruption, resume | CD-04, CD-06, CD-09 | Meaningful checkpoints retained, original restrictions reapplied, accepted rolls/effects not repeated. |
| NPC assistance or opposition | CD-02, CD-04, CD-07 | NPC independently chooses; shared relevant mechanics apply; accepted effects respect both actors and world. |
| Hidden consequential condition | CD-01, CD-03, CD-08 | Internally applied if established; legitimately observable result only; no causal disclosure without basis. |
| Changed state before acceptance or failed save | CD-04, CD-09 | Stale dependent unit rejected without partial effects; restored campaign coherent and retry-safe. |
| Later swimming, jumping, difficult terrain | All as applicable | Reuse shared contracts with different rules and world circumstances; no architecture-level assumption that traversal means climbing. |

Validation should vary authoritative premises and test changes in resulting applicability, not compare against scenario-specific scripted answers. Structural checks cover ownership, acceptance, causality, save/load and access; the owner evaluates whether the integrated experience is sensible, fair and controllable. No live-provider spend is proposed for Stage A.

## 6. Design boundaries and next phase

**Included now:** Semantic authority matrix, shared rule-facing obligations, governing fact establishment, cross-domain effect coherence, stable physical-object identity, meaningful activity continuity, NPC parity, access projection, and future-facing persistence/scalability invariants.

**Not included now:** Class/API names, schemas, a universal transaction framework, complete 2024 rule encoding, source-license acquisition, creature/spell catalogs, full character progression, autonomous NPC scheduling, universal physics or mapping, content-pack authoring, general migration, narrator tuning, or a climb-focused implementation package.

The next logical work after Stage A acceptance is **domain-focused Design**, identifying a minimum genuine rules-and-world capability for physical traversal and defining its dependencies as reusable contracts. Implementation selection and publication require separate owner authorization under `WORKFLOW.md`.

## 7. Consolidated review points

These are the consequential points for the owner's review; lesser wording/interface details can be refined within this design direction:

1. **Rule precedence and justified adaptations (CD-02):** D&D 2024 remains the governing foundation; accepted adaptations and narrowly scoped authored abilities/effects are explicit, not convenient informal overrides.
2. **Physical-object boundary (CD-05):** World Simulation owns the external object and physical relationships; Character System owns creature-related mechanical use/readiness; neither duplicates an independent contradictory inventory truth.
3. **Acceptance unit and replay recognition (CD-04):** dependent domain effects become authoritative coherently and retain recognition; independently accepted meaningful progress remains durable.
4. **Future scalability (CD-09):** design promises semantic identity, selective access and migration compatibility but does not commit to a particular persistence/storage technology or universal ledger.

**Acceptance:** The owner approved the consolidated Stage A direction and authorized continuing into domain-focused Design on October 25, 2026. This acceptance does not authorize implementation, Git publication, a live provider run, or a storage migration.
