# F01 — Information Sufficiency Experiment V1

Status: Design experiment fixture, prepared for review. No implementation or live-model execution authorized by this artifact.

## Purpose and boundaries

Compare three information conditions (I: deliberately insufficient; M: candidate minimal; A: additional relevant context) for each of three gameplay scenarios. The underlying authoritative scenario truth is fixed within each trio. Do not assume M is sufficient or A is beneficial. Assess consequential fidelity, natural narrative quality, and marginal value of additional context. A narrator may make ordinary compatible incidental inferences. Contextual adjudication of consequential new developments is an open, separately proposed clarification, not a settled F01 rule. This experiment must not settle the architecture or demand exhaustive simulation.

## Method

For each case, an evaluator retains the hidden truth ledger, the player's declared action or conversational focus, and the information package presented to the narrator. The narrator receives only the specified package and a common instruction: "Describe the next moment in concise, natural second-person RPG prose, preserving supplied facts, reported claims, player intent and resolved results. Do not invent a result for an unresolved player action. Ordinary compatible scene texture is welcome. Do not add explanatory disclaimers unless needed for understanding." Keep the prompt, model and generation settings equivalent between conditions. Exclude previous generated narrative prose as an independent input variable; supply only factual or semantic continuity. Randomize package labels for blind evaluation. Preserve exact prompts, outputs and notes. One pass per cell, with limited repeats only for ambiguous findings.

A deliberately insufficient package tests a known omission; a narrator that prudently avoids unsupported specificity may be faithful but less useful. Score that as information-limited rather than a fidelity failure. Never require hallucination to pass a test.

## S1 — Conditional castle-wall climb

### Hidden truth ledger (evaluator only)

- The player declared an attempt to climb a castle wall, stopping if it became too dangerous.
- The character did not recognize crumbling mortar before a stone broke loose beneath their boot (failed danger observation).
- Their climbing competence was sufficient to regain purchase and continue; the climb succeeds and the character reaches the battlements unharmed.
- No adverse persistent consequence, fall, injury or time cost is established.
- The stone fell into the courtyard. This is a transient scene event, not established damage to a person or a triggered alarm.

### I1 — Insufficient

"The player climbs a castle wall. A stone breaks loose beneath their boot. Describe the result." 

*Deliberately omitted:* stopping condition, failed perception, successful recovery and final state. An invented fall, injury or abandonment would be unsupported; an unresolved description may be appropriately cautious.

### M1 — Candidate minimal

"Player intent: climb the castle wall, stopping if the wall becomes too dangerous. Resolved: the character fails to notice crumbling mortar before a stone breaks loose underfoot; sufficient climbing skill prevents a fall; the character climbs past the danger and reaches the battlements unharmed. No adverse consequence is established. Describe the completed attempt." 

### A1 — Additional relevant context

"Player intent: climb the castle wall, stopping if the wall becomes too dangerous. At first, the visible route appears climbable. Mortar is degraded in one section but the character does not recognize the danger before a stone dislodges. The stone falls into the courtyard. The character remains capable of finding secure holds beyond the damaged section. The stopping condition is not knowingly disregarded; climbing competence overcomes the danger. No fall, injury, alarm or other adverse consequence is established. Describe the completed attempt without implying that the player chose to ignore a known danger." 

*Additional information tested:* relevant environmental context and perceptual timing, without prescribing the narrator’s choreography. Avoid counting mechanical disclaimers in the prose as quality.

### Evaluation anchors

Must preserve: failed early detection; successful climb; no injury; stop condition not knowingly disregarded. Test whether A adds useful staging or merely repeats the result.

## S2 — Innkeeper report and follow-up

### Hidden truth ledger (evaluator only)

- The player is speaking with the innkeeper about a traveling merchant.
- The innkeeper says they saw the merchant at the inn yesterday and that the merchant rented a room.
- The innkeeper does not know where the merchant went afterward.
- These are the innkeeper's statements; independent verification of the merchant's stay and later destination is not established.
- The player asks: "Did you see which road the merchant took?"
- The innkeeper cannot truthfully provide a road from the available knowledge.
- No special motive, lie, or hidden knowledge is established.

### I2 — Insufficient

"At an inn, the player asks the innkeeper which road a merchant took. The innkeeper saw the merchant yesterday. Write the reply." 

*Deliberately omitted:* limits of knowledge, room-rental report and verification status. A specific road would be an unsupported invention.

### M2 — Candidate minimal

"Active dialogue: the player asks the innkeeper about a merchant. The innkeeper reports seeing the merchant at the inn yesterday and says the merchant rented a room, but does not know where the merchant went afterward. These are the innkeeper's claims, not independently verified world facts. Player follow-up: 'Did you see which road the merchant took?' Write the innkeeper's natural response without inventing a road or implying firsthand knowledge they lack." 

### A2 — Additional relevant context

"Setting: a moderately busy roadside inn, with the player speaking directly to the innkeeper. In the active exchange, the innkeeper has already reported seeing the merchant yesterday, renting a room, and not knowing the subsequent route. This remains an attributed report, not independent confirmation. The player now asks, 'Did you see which road the merchant took?' The innkeeper has no established information about the route. Respond naturally in the innkeeper's voice; do not repeat the entire earlier answer or invent an alibi, motive, route, witness or new lead." 

*Additional information tested:* active-dialogue continuity and environment; no prior narrative prose is supplied. Do not mistake optional natural wording for a new factual disclosure.

### Evaluation anchors

Must preserve: innkeeper report attribution; lack of route knowledge; no invented specific road. Test whether additional relevant dialogue context improves conversational flow.

## S3 — Confrontation and return to dialogue

### Hidden truth ledger (evaluator only)

- The player has been asking an innkeeper about a merchant; the innkeeper has reported a sighting, but no independently verified merchant whereabouts are established.
- A patron nearby asks why the player is asking about the merchant. The patron obstructs the player's route.
- The player tries to pass without fighting; the attempt is blocked, with no injury.
- The player then shoves the patron. Applicable resolution establishes the shove succeeds and moves the patron five feet. The patron stays standing; no damage is established.
- The player turns to ask the innkeeper: "Did the merchant leave anything behind?"
- The innkeeper's answer, knowledge of left-behind items and willingness to engage are not predetermined by the ledger.
- The scene may include ordinary compatible reactions. New consequential facts (such as a left-behind ledger, a promise to cooperate or an arrest) are not pre-authorized as resolved outcomes. The contextual-adjudication boundary is observed and flagged, not adjudicated by this test.

### I3 — Insufficient

"In an inn, the player has shoved a patron and asks the innkeeper whether a merchant left anything behind. Continue the scene." 

*Deliberately omitted:* outcome of shove, current positions, preceding exchange and absence of established knowledge about belongings. The response should avoid claiming a known item was left behind.

### M3 — Candidate minimal

"At an inn, the player was asking about a merchant. A patron challenged the questions and blocked the player's path. The player tried to pass without fighting, but was blocked. The player then shoved the patron; the shove succeeded, moving the patron five feet without knocking them down or causing established injury. The player turns back to the innkeeper and asks, 'Did the merchant leave anything behind?' The innkeeper's knowledge and answer have not been determined. Continue with compatible immediate staging, but do not assert an inventory discovery, firm NPC commitment, arrest or other resolved consequential outcome." 

### A3 — Additional relevant context

"Current scene: a moderately busy roadside inn, the innkeeper behind the counter, a patron nearby. The innkeeper previously reported seeing a merchant yesterday and said they did not know where the merchant went afterward. A patron who overheard the exchange demanded to know why the player was asking, then blocked the player's way. The player tried to get past without fighting and failed; no injury occurred. The player shoved the patron successfully, displacing them five feet; the patron remains standing, with no established damage. The player now turns back toward the counter and asks, 'Did the merchant leave anything behind?' The innkeeper's knowledge of any belongings, willingness to answer and subsequent consequential choices are undetermined. Use the active confrontation and dialogue history to write a natural continuation. Compatible small reactions are allowed. Do not invent a verified item, commitment, successful arrest or new outcome of a player action." 

*Additional information tested:* spatial staging, overheard conversation, dialogue continuity and response relevance. The test is not a demand for NPC psychology simulation.

### Evaluation anchors

Must preserve: patron remains standing; player shove succeeded; no injury; merchant report not verified; no invented factual answer about belongings. Observe whether plausible innkeeper reactions can be expressed without pretending a consequential choice was already settled.


## Information provenance and support assessment (design addition, October 15)

For **each information element that materially affects an output**, record the following independent judgments. Do not infer the need for a mechanical subsystem merely from narrative importance or consequence.

| Field | Values / interpretation |
|---|---|
| Narrative necessity | Essential for faithful playable narration / useful improvement / dispensable / distracting |
| Source of authority | Rules-resolved attempt or cost; established world/character fact; attributed actor report; contextual AI-GM judgment; unresolved |
| Design support | Accepted responsibility in governing design / proposed or ambiguous responsibility / absent or unresolved |
| Implementation support | Verified present / verified partial / verified absent / not assessed |
| Evidence | Specific output difference or fidelity failure, plus the fact that explains it |

**Do not equate implementation status with design status.** For this design experiment, implementation support defaults to **not assessed** unless separately verified against the implementation baseline. The contextual-adjudication clarification is **proposed, not accepted**. Its unresolved boundary should be flagged without assuming a new adjudication mechanism.

### Initial provenance inventory (hypotheses to verify against outputs)

| Scenario | Information element | Likely source | Design-support assessment |
|---|---|---|---|
| Climb | Player's stopping condition | Player-declared constraint, carried into action adjudication | Accepted responsibility |
| Climb | Failed danger observation and successful recovery | Action & Resolution, informed by character competence | Accepted responsibility |
| Climb | Loose mortar and falling stone | Established event/context, potentially ordinary contextual adjudication | Mixed: event accepted for fixture; general origin depends on context |
| Climb | Additional lighting, weather or physical detail | Established world context **if supplied**, otherwise compatible incidental expression only | Conditional; not mechanically required by default |
| Innkeeper | Merchant sighting and rented-room statement | Attributed NPC report | Accepted attribution requirement; actor's consequential statements require legitimate adjudication |
| Innkeeper | Unknown departure route | NPC knowledge boundary, as adjudicated | Accepted epistemic constraint |
| Innkeeper | Busy room or ordinary mannerisms | Contextual description | Permissible when compatible; no dedicated mechanics implied |
| Confrontation | Failed attempt to pass, successful shove and five-foot displacement | Action & Resolution | Accepted responsibility; precise movement is fixture-specific |
| Confrontation | Previous questions and patron obstruction | Relevant scene/dialogue continuity | Accepted continuity responsibility |
| Confrontation | Innkeeper's immediate manner or ordinary bystander response | Contextual expression or contextual AI-GM judgment depending on consequence | Boundary-dependent; do not preempt proposed clarification |
| Confrontation | Whether merchant left an item, a new promise or an arrest | Consequential adjudication, not narrative realization alone | Source and authority need explicit determination if test depends on them |

**Evaluation output:** Report (a) smallest sufficient information for each case, (b) provenance of each materially useful element, (c) whether accepted design can legitimately supply it, and (d) any genuine unresolved design dependency. Do not recommend a new system merely because additional detail sounds better.

## Blind scoring sheet

Score each dimension 0–2 with a brief cited example from the output:

- **Consequential fidelity:** 0 material contradiction/invention; 1 ambiguity or consequentially misleading omission; 2 preserves known meaning.
- **Epistemic fidelity:** 0 material source/knowledge confusion; 1 unclear attribution or uncertainty; 2 appropriate attribution and knowledge bounds.
- **Narrative quality:** 0 incoherent/unusable; 1 serviceable but awkward or thin; 2 natural, coherent and playable.
- **Continuity:** 0 contradicts prior events; 1 incomplete or awkward carry-forward; 2 relevant prior context used appropriately.
- **Information efficiency:** qualitative: indispensable / useful / redundant / distracting; judge only after unblinding.

Record whether the output is **faithful but information-limited**, **narrator failure despite adequate information**, **reasonable contextual inference**, or **potential consequential adjudication boundary**. A score of 2 is not proof of general sufficiency. Record the smallest specific missing or extra fact that changed the assessment.

## Decision rules after evaluation

1. Prefer M over A when both are acceptable and A gives no meaningful benefit.
2. Prefer A only where added context demonstrably improves fidelity, coherence or useful continuity enough to justify its cost.
3. If I succeeds, examine whether the omitted information was inferable, unnecessary or merely avoided by cautious narration; do not automatically declare it sufficient.
4. If M fails, distinguish missing authoritative information from the narrator mishandling available information before expanding requirements.
5. If all conditions fail, do not conclude that additional simulation is required; inspect the case, prompt, model and unresolved design boundaries.
6. Treat contextual consequential developments as observations for the separate proposed clarification, not automatic failures or automatic permissions.
7. Record a provisional starting information level for each function, then refine through extended gameplay under F01-D10.

## Deliverables of an eventual authorized run

Nine preserved inputs and outputs, blinded evaluation sheet, information-provenance and design-support matrix, failure classifications, comparison of M vs A marginal value, provisional starting information levels and a short list of deferred questions. No production code, persistent schema, runtime controls or universal optimality claim.
