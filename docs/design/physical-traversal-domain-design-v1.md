# AI RPG — Physical Traversal Domain Design V1

**Phase:** Design, Stage B — domain-focused capability design  
**Prepared:** October 25, 2026  
**Status:** Owner-accepted October 25, 2026 (PT-D1–PT-D9 and consolidated Stage B direction); Design only  
**Primary gameplay capability:** Physical traversal  
**First implemented method proposed:** Climbing; subsequent generalization through swimming and jumping  
**Repository:** `Mixelplux/AI-RPG`

## 1. Goal, inherited design and boundary

Establish the **minimum genuine gameplay semantics** needed for rule-grounded physical traversal in a persistent open-ended RPG. This is the first domain-focused Design after the owner accepted the Core Gameplay Domains Cross-Domain Contract Design V1 (CD-01–CD-09) on October 25, 2026.

Inherited contracts include D&D 2024 core mechanics with explicit justified adaptations; accepted T-R1–T-R11; F01, F05, Information Foundation D1–D16, Information-Grounded Adjudication D-A1–D-A6, Integrated Gameplay Architecture IG-01–IG-18 and IG-20–IG-23; the shared Specificity, Authority Composition and Causal Continuity doctrines; and existing persistence/integrity requirements.

Design target is **not** a climbing scenario, map-specific handler, or miniature disposable runtime. The capability must become a reusable part of World Simulation, Character System and Action & Resolution. Actors & Social Dynamics participates when consequential NPC intention is relevant; it is not compulsory for a solitary climb. The existing reusable coordination/integration runtime is a candidate for implementation reuse, but it does not define intended mechanics or dictate domain design.

This document establishes intended semantic behavior and validation evidence. It does **not** select modules, database schemas, precise APIs, prompt structure, rules import source, publication process, or a scheduled implementation package.

## 2. Grounded 2024 rules baseline

The following are paraphrased working premises from the official **2024 D&D Free Rules**. The published core rules and their applicable errata, not this paraphrase, remain the reference if a wording dispute matters.

| Rules area | Relevant foundation | Domain implication |
|---|---|---|
| Movement | A creature's movement is constrained by its Speed and applicable special speeds in turn-based play. Modes can be combined; difficult terrain changes movement cost. | Character supplies movement statistics/traits; World supplies physical terrain; Resolution computes applicable movement consumption. |
| Climbing | Ordinary climbing has additional movement cost. Climb Speed removes that climbing surcharge. The DM may require a DC 15 Strength (Athletics) check for slippery surfaces or those with few handholds. | **Not every climb requires a roll.** A precarious climb can require one even for a skilled creature. World circumstances govern applicability. |
| Ability checks | Checks address uncertain consequential tasks; ability, proficiency and other valid modifiers apply to the selected DC. | Resolution decides check applicability before drawing, not by verb or character competence alone. |
| Swimming | Ordinary swimming has additional movement cost; Swim Speed removes it. Rough water can call for a Strength (Athletics) check. | Second method reuses general movement and check responsibilities with different environmental predicates. |
| Jumping | Normal long/high jump limits depend on Strength, running start and movement spent; specific obstacle or landing checks may apply. | Third method validates more deterministic geometry/capability relations without turning all movement into generic DC rolls. |
| Falling | Falling has separate hazard/damage rules *when a fall actually occurs*. | Failure of another check does not itself establish falling; physical circumstances and the declared attempt determine what the result means. |

Official references:

- [2024 Free Rules — Playing the Game](https://www.dndbeyond.com/sources/dnd/br-2024/playing-the-game) (D20 tests, proficiency, movement and difficult terrain)
- [2024 Free Rules — Rules Glossary](https://www.dndbeyond.com/sources/dnd/br-2024/rules-glossary/) (Climbing, Climb Speed, Swimming, Swim Speed, Jumping and Falling)

No new house rule or automatic success/failure band is adopted. Any necessary adaptation must be explicit, justified by gameplay, and recorded separately under the accepted rule foundation rather than being smuggled in as a traversal implementation convenience.

## 3. Proposed traversal design decisions

### PT-D1 — One authorized traversal undertaking, several semantic methods

Physical traversal is movement of a creature through established space under a specified or legitimately inferred ordinary method. Walking, climbing, swimming and jumping differ in method-specific rules; the architecture does not force them into one roll or one movement cost formula.

The input meaning must distinguish objective, destination or extent, method, target/route, constraints (such as careful or quiet), inquiry versus preparation versus commitment, relevant available means, and whether an unresolved material choice remains player-owned. F05 permits ordinary situated steps but not silent selection of materially distinct methods, consumables or risks.

A simple instruction such as “climb that wall” authorizes ordinary physical execution within capability, means and scene circumstances. It does not automatically authorize using a scarce potion, constructing an elaborate apparatus, exposing the character to a newly recognized grave risk, or choosing a different route when the selected method becomes impossible.

### PT-D2 — Minimum genuine World Simulation traversal state

World Simulation must be able to establish and preserve, when consequential:

- **Place and relation:** Creature's meaningful current position; intended reachable destination; established traversable relationship or obstacle; relative height, distance, direction or adjacency when a rule or consequence needs it.
- **Surface/environment:** Relevant stability, handholds, slope, terrain, water, weather, visibility, hazards, supports and changing conditions. These are established, inferred, or legitimately resolved at relevance, not invented after a roll to fit its result.
- **Physical objects:** Stable identity and actual disposition/condition of ropes, anchors, harnesses or other material means; distinct held, attached, secured, located and usable relationships. Physical possession is not proof of a successful attachment.
- **Time and causal state:** Fictional elapsed time, accepted physical progress, changes in conditions, causal history sufficient for retries, return visits and subsequent activity.

These are *logical information requirements*, not a demand for exact universal coordinates, 3D physics, a tile map, global object catalog or constant background simulation. Exact distance or elevation is required only when it materially affects a rule, option or result; otherwise a stable semantic spatial relation can suffice. Important identities and relationships must survive later retrieval and restoration.

World Simulation owns external reality, including whether an attachment holds and where a creature actually ended an accepted movement. It does not choose the player's method or determine check success by fiat.

### PT-D3 — Minimum genuine Character System traversal semantics

For any PC or NPC undertaking a supported method, Character System must supply relevant rule-facing facts: ordinary and special movement speeds; applicable ability score/modifier, proficiency and relevant traits; current mechanically relevant conditions and resources; creature size or other physical capacity when applicable; relevant equipment readiness, ability to use established means, and legitimate knowledge/observation.

Do not require an entire leveled PC sheet or complete monster stat block when the supported action needs fewer facts. Conversely, the system must not fabricate omitted material bonuses, capabilities or supplies. Both PC and NPC attempts consume the same types of rule-facing input, with different richness where sufficient.

Equipment mechanics and creature-specific readiness belong here; the physical rope or harness instance, its attachment and its actual position remain World-owned. Available use depends on both. A creature may hold gear without it being suitable, ready, intact, attached or authorized for the contemplated attempt.

### PT-D4 — Resolution distinguishes feasibility, rules, uncertainty and consequence

Action & Resolution must distinguish:

1. **Not authorized / method unresolved:** Return player control without an attempt or fictional cost.
2. **Material information unavailable:** Seek legitimate internal retrieval; if not available, leave the affected action unresolved without hidden disclosure.
3. **Physically or mechanically unavailable:** An established obstacle or missing means may make the intended method impossible. Distinguish mere feasibility assessment from a player-committed attempted action that legitimately consumes time or resources before discovering the obstacle.
4. **Deterministic permissible movement:** Apply required movement costs and consequences without a gratuitous die roll.
5. **Consequential uncertain movement:** Select the applicable check, modifiers, DC or other rule using established governing circumstances, then resolve once. Report exactly the result the rule and circumstances support.

Consequence determination is not a second independent “story repair” pass. The relevant failure possibilities, material risk, existing supports, physical causes, progress and costs must be grounded before or during legitimate adjudication, not post hoc inventions favoring a roll. The final rule result and World/Character/Actor-owned effects enter one coherent acceptance unit when dependent (CD-04).

### PT-D5 — Failed attempt is not synonymous with falling

Failure means the attempted objective was not achieved to the extent established by the applied mechanic. A failed precarious-climb check may mean no progress, an interrupted approach, a forced retreat, a loss of grip with a support preventing a fall, or an actual fall **only when the applicable rule and established physical circumstances justify that consequence**.

Do not impose automatic injury, fall, broken rope, progress meter reset, or a new mandatory roll merely because the check failed. Conversely, do not preserve a favorable safe position when the established physical conditions and relevant effects require otherwise. Falling, if genuinely established, invokes its own rules rather than being treated as a generic failure label.

The player-facing result should distinguish failed progress from physical injury, lost equipment and other independent consequences. Details that materially determine options or risk must be accepted through owning domains before narration.

### PT-D6 — Movement extent, time and progress are meaningful, not microscopic

For turn-based combat or similarly exact timing, the applicable movement and action economy governs. Outside that context, a coherent traversal activity may cover meaningful distance over an appropriate amount of fictional time, without imposing a universal six-second accounting loop on every climb.

Represent the extent and precision necessary for the actual stakes: arrival at a ledge, halfway up a wall, secured at an anchor, stuck on a surface, safely returned to ground, etc. A universal percentage-complete field is not required. Time spent, resource cost, accepted physical position, resolved mechanics and changed conditions survive interruption and session boundaries.

Later attempts may be permitted, disallowed or governed by changed conditions and previously accepted resolution. Repetition must not create an automatic free reroll or blanket prohibition on trying again. An already accepted check is not rerolled merely because its fictional presentation was interrupted.

### PT-D7 — Object and relationship continuity

A consequential rope remains the *same object* when acquired, secured to a railing, attached to a harness, tensioned, cut, dropped and recovered. Multiple compatible physical relationships may coexist. The state must not make it both exclusively held by one actor and independently held by another unless shared handling is actually supported; it also must not use a generic single location to erase simultaneous rope attachments.

The relevant physical state and accepted setup effects constrain future uses. Routine knots/adjustments may be assumed when legitimately within a chosen method and means; a successful secure attachment cannot be conjured when the anchor, materials, preparation or risk is consequentially in doubt. Changing the material setup requires an appropriate authorized action and accepted state update.

No exhaustive catalog of mundane props is needed. Incidental descriptive items become authoritative instances only when their consequential use makes identity and continuity necessary.

### PT-D8 — NPC participation is conditional and rule-facing

A solitary climb does not invoke Actors & Social Dynamics merely to meet a four-domain quota. When an NPC meaningfully decides to assist, withhold aid, sabotage or attempt the same obstacle, their choice comes from Actors & Social Dynamics under legitimate knowledge, motive and circumstance. Character supplies their mechanical capability; Action & Resolution resolves applicable rules; World records external effects.

The first genuine traversal implementation need not produce a general autonomous NPC planner. A later relevant validation can exercise an independently established NPC choice and a genuine shared rules mechanism (for example, the 2024 Help action where its prerequisites apply). A fixture-supplied NPC intention is acceptable only as an explicit missing-supplier boundary and **must not be claimed as implemented general actor agency**.

### PT-D9 — Continuity, visibility and generalization gates

Consequential movement must pass through the accepted cross-domain acceptance, identity, epistemic access and persistence contracts. The player may learn the felt effect of slipping without discovering a hidden sabotage source; later inspection may change that access legitimately.

The same common gameplay runtime must accept a changed state after save/load without duplicating movement, cost, damage, checks or object changes. Rejected proposals, stale dependencies and failed restoration remain technical outcomes, not fictional setbacks.

Climbing can establish the first vertical capability but not generalization. A sufficiently different method (recommended: swimming; then jumping) must reuse domain information/acceptance contracts while applying genuinely different mechanics. A method-specific implementation may be appropriate; a **scenario-specific integration path** or a rule engine that requires a shared-contract rewrite for every new movement type is not sufficient evidence.

## 4. Semantic interaction example — one climb

The following is illustrative, not a predetermined outcome or required function-call sequence:

1. **F05 / coordination:** Player commits to climb the established stone wall, by hand, without taking a materially different approach. The character's target and current position are legitimate accessible context.
2. **World:** The wall is established as wet and sparse in handholds, with its relative height and nearby support known as needed. A hidden causal condition, if previously established and binding, must be retrieved internally.
3. **Character:** The creature's movement/special speeds, Strength, Athletics proficiency, conditions and legitimate equipment are supplied. A rope is not assumed available if absent.
4. **Resolution:** Apply the actual 2024 climbing/movement rules and determine whether the optional difficult-climb check is appropriate in this particular circumstance. Fix governing risk before resolving uncertainty. Do not use a universal “climb always rolls” shortcut.
5. **Acceptance:** Accept the legitimate result and dependent current position/time/resources/physical changes, or reject a stale/invalid unit entirely. Preserve stable attempt recognition.
6. **Continuation:** Use fresh facts to decide ordinary continued climbing or a meaningful return of control. F01 expresses only accessible results, with no invented fall or hidden explanation.

Different equipment, climb speed, surface, actor, difficulty or established history should change the applicable premises and behavior without changing the coordinator's job or creating a named scenario branch.

## 5. Minimum implementation evidence after separate authorization

The proposed future bounded package is **Physical Traversal Core V1a**, not full World Simulation or Character System. It should establish reusable, genuine capabilities in three core domains and integrate them into the existing accepted runtime where that is architecturally justified.

| Work area | Minimum genuine delivery | Explicitly not claimed |
|---|---|---|
| World Simulation | Stable local traversal relation/obstacle, meaningful position, conditions, fictional time, one persistent physical-object identity and compatible attachments | Universal coordinates, global pathfinding, physics, all hazards |
| Character System | Shared PC/NPC rule-facing movement/capability view, one or more applicable conditions/traits, equipment use versus physical presence, legitimate access | Full character generator, complete creature database, general memory model |
| Action & Resolution | 2024 ordinary climb and consequential difficult-climb mechanics, relevant speed/proficiency/condition handling, legitimate failure semantics, controlled checks and costs | Universal rule interpreter, combat, spell engine, every climb variant |
| Cross-domain runtime | Coherent dependent acceptance; meaningful resumption; object/attempt recognition; F01-safe outputs; save/load of supported state; invalid proposal rejection | New universal transaction engine, event sourcing, independent prototype runtime |
| Actors & Social Dynamics | Contract conformance for optional explicit NPC intention, plus genuine rule-facing participation if a bounded NPC case is selected | Autonomous NPC agency or schedules |

The primary implementation path should deliver actual gameplay functionality. Contract-conforming fixtures can supply missing authored world material and actor intent; they must not supply preselected climb answers or bypass authoritative state and rules.

### Validation groups

**A. Rules and variation**

- Ordinary climb with no consequential check; a difficult climb with an applicable Strength (Athletics) check; the same condition with a creature's actual Climb Speed or changed proficiency/condition.
- Controlled relevant mechanical input variation demonstrates a changed result or applicability where rules require it. Verify rules-conforming DC and modifier use and no invented natural-1/20 ability-check behavior.
- World conditions vary independently of the named test location or map. Failure does not automatically cause falling or injury. Where actual falling occurs, separate falling rules govern.

**B. Material and activity continuity**

- Established rope and anchor, genuine setup and multi-attachment identity; then detach, transfer, damage or lose the means. Later access must reflect physical truth, not obsolete inventory text.
- Accepted partial progress, time, costs and changed circumstances survive interruption and resumption. A resolved check does not reroll due solely to presentation pause.
- A genuine new attempt follows current means, authorization, rules and accepted history, without automatic free repetition or impossible blanket prohibition.

**C. Integrity and access**

- Concurrently dependent state changes publish coherently or not at all. Reject stale premises, unavailable material established facts, impossible equipment and unsupported untrusted proposals with no fictional effects.
- Save/load retains real position, rope identity and relationships, costs, resolved attempt recognition, time and restrictions; failed restoration does not damage the active state.
- Hidden material conditions internally govern action without automatic player knowledge. Presentation error repair never repeats accepted resolution.

**D. Generalization**

- After climbing is validated, introduce swimming under ordinary and rough-water conditions to test the same movement/context/acceptance boundaries with different speed and uncertainty rules.
- Introduce jumping or at least a focused design-and-contract conformance test for its different deterministic length/height, running-start and obstacle/landing semantics.
- Report new method-specific logic separately from changes to shared contracts. Unexpected general-contract rewrites, duplicated authoritative facts or inability to preserve common object/character continuity trigger architecture review.

Automated checks should establish structural and rules integrity; owner experiential play should assess believable continuity, meaningful control and pacing. No live-provider call is required merely to validate deterministic traversal mechanics. Model use is justified only when genuine contextual interpretation/adjudication behavior is under investigation and is separately authorized.

## 6. Implementation sequencing proposed, not yet authorized

**B1 — Complete design and rule-reference mapping.** Confirm which 2024 movement, check and relevant equipment/condition rules are in the first supported set. Specify semantic minimums; document deliberate exclusions. This Stage B document is the current candidate.

**B2 — Domain foundations.** Implement genuine World/Character/Action capabilities against CD-01–CD-09. Workstreams may proceed independently or in parallel once their shared interfaces are accepted; a coordinating integration owner guards semantic changes. Implementation requires a separate capability authorization and workflow staging.

**B3 — Continuing climb integration.** Exercise one production-capable general runtime and save boundary with varied climbing circumstances and real domain outcomes. Existing code is assessed for fitness, not retained by default because it exists.

**B4 — Cross-method generalization.** Extend to swimming (and then jumping as warranted), measuring how much is genuinely new method logic versus a flaw in general contracts. Reconcile architecture before expanding scope if a material mismatch is found.

These steps are development sequencing, not separate arbitrary owner-acceptance gates. The owner needs to decide materially changed rules, gameplay semantics, authority, architecture, risk, scope or implementation authorization, not every ordinary design detail.

## 7. Consolidated Design review

The main proposed design commitments are:

1. **Begin with genuine climb semantics, including both ordinary and uncertain climbing.** Avoid a universal roll or automatic-fall outcome; follow the applicable 2024 rules and material circumstances.
2. **Implement minimum real World, Character and Action foundations together for an end-to-end capability.** Do not claim that any one partial foundation is a complete core system or that supplied fixtures implement absent upstream domains.
3. **Retain a relevance-based NPC boundary.** Actors & Social Dynamics need not be implemented as an autonomous system for the first solo climb. NPC participation, when used, requires actual choice authority and shared applicable rules.
4. **Use a second substantially different method as the generalization gate.** Swimming is recommended first, with jumping adding deterministic spatial-rule contrast later.

**Acceptance:** The owner accepted the consolidated Stage B direction, including PT-D1–PT-D9, and authorized preparation of the Design → Implementation handoff on October 25, 2026. This does not itself authorize source edits, implementation package selection/staging, provider usage, save migration or Git publication.
