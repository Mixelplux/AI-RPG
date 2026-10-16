# F05 — Authorized Activities and Player Control

**Phase:** Design — owner-accepted October 16, 2026  
**Reference baseline:** `21a5b1e39b2691e4221967d2029b63ff1cedfc8f`  
**Implementation:** Not authorized by this document.  
**Scope:** Preparation, commitment, changing circumstances, interruption, and continuity of authorized activities.

## Purpose and authority

F05 describes the gameplay boundary of the player's authorization. It determines what the player has chosen to undertake, when continued execution would exceed that authorization, and when control returns. It does not replace Action & Resolution, World Simulation, Character System, Actors & Social Dynamics, or Narrative Experience. Applicable authorities establish outcomes, costs, external developments, actor decisions, and consequential truth; F01 realizes accepted information without independently creating it.

## Accepted decisions

### D1 — Coherent activity

The player may authorize a connected undertaking toward an immediate purpose, including routine constituent steps. This does not authorize an arbitrary queue of separate future decisions. Extended activities may be represented with appropriately abstracted elapsed time; their duration alone does not determine whether they are coherent.

### D2 — Inquiry, preparation, and commitment

Interpret natural language and context to distinguish asking about feasibility, examining circumstances, preparing, and actually committing to an attempt. A broad objective is not automatically permission to choose consequential methods or independently pursue a series of objectives. No special command syntax is required.

### D3 — Resolution boundary

Advance an authorized activity as far as its nature, applicable rules, authorization, and circumstances permit. Return control when it concludes, can no longer proceed as authorized, or would require a meaningful player-owned choice. Ordinary events need not trigger an interruption merely because they occur or affect the activity. Do not impose elaborate future-facing conditional programs on the player.

### D4 — Meaningful and discovery-sensitive interruption

Return control when continuing would make a meaningful choice that belongs to the player and the character has a legitimate opportunity to respond. This includes a character becoming aware of a materially increased possibility that a **potentially objectionable activity** will be observed. The activity is objectionable in context if a reasonable witness could regard it as threatening, prohibited, harmful, or warranting intervention; the term describes the player's activity, not a witness's attitude or reaction.

Approaching footsteps during unauthorized lockpicking can justify interruption before a guard appears or responds. Avoiding personal detection does not establish that evidence of the activity went unnoticed. Do not interrupt continuously for a merely hypothetical observer; a meaningful change in perceptible circumstances matters. Previously authorized methods and accepted risks can already answer some developments. Unperceived events and outcomes without a legitimate opportunity to respond need not interrupt or reveal hidden information.

### D5 — Competent execution within available means

Assume reasonable routine execution of an authorized activity within established capabilities, the chosen method, circumstances, and legitimately available means. Competence does not create missing lockpicks, healing potions, supplies, knowledge, permissions, or other prerequisites; nor does it guarantee success or authorize a materially different or costly approach. Mundane incidental resources may be inferred when context supports them; consequential, scarce, or exceptional prerequisites require stronger justification under the existing Specificity Doctrine.

### D6 — Preserve established results and consequences

Interruption, failure, withdrawal, or technical presentation boundaries do not erase legitimately established elapsed time, resources spent, findings, physical changes, actor responses, accepted results, or other consequences. Distinguish mechanical resolution from fictional execution and from durable changes. Narrative description of partial progress does not necessarily create a separate mechanical checkpoint.

Whether an activity can resume, must restart, or requires a new attempt depends on the activity's nature, applicable rules, accepted resolution, and current circumstances. An already resolved attempt must not receive another roll or resolution merely because its fictional presentation was interrupted. An interrupted spell may require restarting; an interrupted crate search may retain which crates were already searched. Resumption does not restore earlier conditions, erase traces, or imply that an undiscovered character's activity went unnoticed. Renewed authorization to proceed is evaluated in the circumstances then prevailing.

## Dialogue within an activity

Routine conversation can occur as part of a coherent authorized activity without asking the player to approve each exchange. Return control before an independent consequential conversational decision such as paying a bribe, making a promise, threatening someone, disclosing protected information, or changing approach. Narration may express established NPC replies but may not invent consequential agreements, commitments, or disclosures.

## Illustrative boundaries

- **Lockpicking:** With established tools and eligibility, a resolved skill outcome remains the same if footsteps interrupt its fictional execution; do not reroll on resumption solely because narration paused.
- **Warehouse search:** Previously searched crates and disturbances persist. Hiding from a guard may prevent identification without preventing discovery of opened crates; resulting developments affect whether searching can continue.
- **Spellcasting:** An interrupted casting may require a fresh casting attempt under applicable spell rules; preserve any established costs and effects.
- **Merchant inquiry:** Routine questions and answers can be summarized. A demand for payment or consequential disclosure returns control.
- **Travel:** Ordinary delays may be resolved without interruption; a blocked route requiring a new consequential route choice returns control.

## F01 integration and later evaluation

F05 governs authorization and control boundaries; other legitimate game authority establishes attempts, outcomes, costs, developments, knowledge and consequences; F01 narrates only the authoritative, character-accessible information supplied under its accepted information contract. Predetermined scenario fixtures used for implementation and evaluation must conform to that contract, not relax it. Narrative realization must not become a second action execution, create a fresh check, repair failure, establish hidden truth as known, or manufacture consequential progress.

After bounded F05 implementation, evaluate F01–F05 together through scenario-specific playable situations (candidate themes: damaged gate, inn confrontation, disappearing trail). Scenarios may supply bounded interactions and authoritative circumstances without requiring complete upstream systems. Their detailed design remains deferred; this document does not authorize that integration milestone.

## Deferred and excluded

Do not infer requirements for a generalized activity scheduler, universal progress meter, conditional action-programming language, exhaustive inventory simulation, universal morality/alignment system, or general NPC/physics simulation. Potential consequences when actions conflict with a character's established values or oaths are a deferred cross-system possibility, not an F05 mechanic. Broader risks of too many interruptions, missed decisions, knowledge leaks, or timing inconsistencies should be investigated when gameplay evidence makes them material.

## Documentation and implementation status

These are accepted design intentions, **not claims of implemented support**. Existing system manifests, workflow, lifecycle authority, simulation/provider authority, and F01 fidelity requirements remain governing. Repository incorporation, review, commit, publication, and any implementation package selection are separate workflow actions.

## Repository incorporation and governing links

This is the single canonical repository Design record for F05. The supplied
owner-accepted `F05_Accepted_Design_Consolidation.md` is reproduced above
unchanged; repository incorporation is proposed for owner review. Acceptance of
the design on October 16, 2026 does not imply acceptance of an implementation.

Read with [F01's accepted decisions and information requirements](f01-truthful-presentation-and-epistemic-fidelity.md),
the [shared doctrines](systems/README.md#shared-doctrines), and the
[system integration boundaries](systems/system-map.md#f01f05-design-integration-boundaries).
The [deferred evaluation register](../deferred_findings.md#df-009--bounded-f01f05-playable-scenario-evaluation)
records the later playable-scenario evaluation without scheduling it.
[Workflow](../../WORKFLOW.md) and lifecycle authority remain unchanged.
