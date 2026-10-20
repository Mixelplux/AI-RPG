# Information Foundation Functional Design V1

**Status: Accepted design; implementation deferred.** Consolidated October 20,
2026 from the owner-supplied accepted design handoff. This is the canonical
functional design record for D1–D16, their qualifications and reconciliation
clarifications, representative validation scenarios, rationale, and accepted
residual risks. It records design acceptance, not implementation acceptance.

This design follows the [Story-First Design Doctrine](../story_first_design_doctrine.md)
and preserves the [system responsibility map](systems/system-map.md) and
[shared doctrines](systems/README.md#shared-doctrines). Research, design and
implementation remain distinct under [WORKFLOW.md](../../WORKFLOW.md).
Existing implementation is evidence and a potential resource, not authority
over this target design. This record selects no package, changes no lifecycle
state, and authorizes no implementation, Region Pack creation or data changes,
save-format changes, or revision of F01/F05 contracts.

Information Foundation is a cross-system functional design, not an additional
outcome-deciding system. The authority contracts below retain existing conceptual
ownership. Player Presentation continues to own input/display mechanics under
its [manifest](systems/player-presentation.md), without fictional authority.
The AI-GM's authorized contextual adjudication operates through the appropriate
owning gameplay boundary; acceptance of provider language for display alone
cannot establish consequential truth. No general acceptance protocol or new
storage, persistence, or ownership model is selected here.

## Purpose and direction

### Purpose

The Information Foundation provides sufficient reliable information for coherent, consequential gameplay across authored world content, evolving circumstances, meaningful history, actor knowledge, relationships and binding constraints.

It must support open-ended gameplay without exhaustive world modeling, continuous simulation or detailed tracking of every possible fact.

The accepted direction combines composable authored foundations, shared authoritative current information, meaningful historical continuity, consequential relationships, reliable operational information access and selective graph-capable retrieval.

Graph-capable does not mean a graph database is required.

The foundation supports existing gameplay responsibilities rather than establishing a separate outcome-deciding authority.

### D1 — Information scope and applicability

Foundations apply according to relevance to the gameplay situation, not solely geographic location.

A foundation may concern geography, a deity, faction, culture, organization, historical subject or another coherent information domain.

Multiple foundations may apply simultaneously.

### D2 — Foundation composition and reconciliation

Applicable authored foundations compose into one coherent setting and era.

Compatible information accumulates. Contradictory canonical authored information must be reconciled before gameplay.

Greater specificity does not automatically override broader information.

Apparent exceptions require explicit legitimate explanations in the authored information, such as local exceptions, secret defiance, competing beliefs or historical distinctions.

An unexplained contradiction must be corrected rather than resolved through automatic precedence.

Changes legitimately established during gameplay are not authored-foundation conflicts.

### D3 — Stable consequential identity

Important authored entities require stable identities so information and consequences consistently refer to the same entity.

Incidental entities acquire stable identity when consequential gameplay requires it.

Universal registration of every incidental person, object or detail is unnecessary.

### D4 — Minimum sufficient authored detail

Foundations provide sufficient detail for meaningful gameplay without exhaustively specifying the world.

Additional specificity may be established progressively when relevance or causal necessity warrants it.

Separate Region Packs must provide meaningful informational depth rather than fragmenting content into trivial units.

Basic information about Lolth may belong in a broader Forgotten Realms foundation. A dedicated Lolth foundation becomes appropriate when substantial additional information justifies it.

### D5 — Authoritative current circumstances

Authored foundations supply initial conditions and constraints.

Accepted gameplay developments may legitimately change those circumstances.

Subsequent gameplay respects authoritative current truth.

A character's claim, belief or speculation does not independently change objective reality.

### D6 — Meaningful historical continuity

Preserve past events and circumstances when they materially affect subsequent gameplay.

For example, a guard who accepted a bribe and was subsequently promoted may retain consequential history despite changes in role or location.

Exhaustive event recording is unnecessary.

Historical retention follows consequential relevance.

### D7 — Progressive specification and established truth

Distinguish establishing previously unspecified information from changing an established fact.

Previously unspecified details may be resolved through legitimate contextual adjudication.

Established facts constrain subsequent adjudication and cannot be silently rewritten to accommodate desired outcomes.

### D8 — Retrospective offscreen adjudication

The world may evolve independently of player observation without continuously simulating every actor and location.

When unattended circumstances become relevant again, adjudicate necessary developments at natural re-entry, before the player can interact with the affected circumstances.

Respect established history, elapsed fictional time, commitments and causal conditions.

The adjudication must respect the appropriate fictional time and must not retroactively select outcomes to favor player intentions, including intentions not yet expressed in gameplay.

### D9 — Contextual actor knowledge

NPC knowledge derives from legitimate informational access, role, experience and circumstances.

Ordinary knowledge may be inferred without exhaustive individual knowledge records.

Secrets, unusual disclosures, meaningful misconceptions and consequential informational differences must be preserved.

An NPC does not automatically know everything the engine knows.

### D10 — Objective truth, belief, claims and uncertainty

Distinguish objective facts, actor beliefs, reported claims, character inferences and genuinely unresolved information.

Claims are not automatically true. Confidence does not establish objective reality.

Unestablished facts may be adjudicated when required, subject to existing constraints and applicable mechanics.

### D11 — Consequential relationships and commitments

Preserve relationships, obligations, promises, loyalties, hostilities and other social conditions when they materially influence gameplay.

These may constrain future decisions, informational access or actor behavior.

An exhaustive social graph is unnecessary.

### D12 — Binding conditions

Conditions governing consequential outcomes must preserve sufficient meaning for consistent application.

As applicable, this includes scope, subjects, prerequisites, triggering conditions, exclusions, exceptions, effects, expiration, termination and revocation.

A magical ward or binding agreement cannot be reduced to a vague description when its specific terms govern gameplay.

No particular rules language, schema or domain-specific language is mandated.

### D13 — Direct and relationship-based information access

Support direct access to relevant information and selective access through meaningful relationships.

For example, information about a temple may lead to applicable doctrine concerning Lolth.

Exhaustive relationship traversal or loading every potentially related foundation is unnecessary.

### D14 — Applicable hidden constraints

Material authoritative constraints must be considered during adjudication even when hidden from the player or absent from the player's request.

An established ward preventing levitation must constrain a levitation attempt regardless of whether the player knows about it.

Such constraints must be available to adjudication, but their application does not authorize revealing hidden information.

### D15 — Proportional information retrieval

Retrieve the minimum sufficient information for the current gameplay decision.

Retrieval depth reflects relevance, consequence and applicable conditions.

Proportional retrieval must not omit an established binding constraint that materially governs the attempted action.

Exhaustive retrieval is not required.

No specific retrieval algorithm or context architecture is mandated.

### D16 — Information availability and uncertainty

Distinguish:

**Unspecified information:** May be established through legitimate contextual adjudication when needed.

**Established but unavailable information:** Must be retrieved from authoritative information when material. Missing context does not authorize inventing a replacement.

**Genuinely uncertain information:** Resolve through applicable mechanics, contextual adjudication or supported uncertainty.

Established-but-unavailable information must not be treated as unspecified.

## Region Pack requirements

A Region Pack represents a coherent region of information, not necessarily geography.

Examples include:

- Geographic hierarchy: Forgotten Realms → The North → Icewind Dale → Bryn Shander.
- Cross-cutting domains: deities, factions, organizations, cultures and other setting information.

Packs may overlap and reference shared identities.

All composed authored information belongs to one coherent setting and era, with canonical contradictions reconciled before gameplay.

Pack boundaries follow meaningful informational depth, not arbitrary atomization.

Pack creation, schemas, validation tools, packaging formats and storage choices remain deferred.

## Functional authority contracts

The Information Foundation supports existing conceptual responsibilities.

**Scenario & Authored Content:** Supplies canonical authored foundations and initial constraints.

**World Simulation:** Owns authoritative current circumstances and accepted consequential developments.

**Character System:** Establishes legitimate character capability and informational access.

**Actors & Social Dynamics:** Governs consequential NPC behavior within established knowledge and circumstances.

**Action & Resolution:** Applies relevant conditions, mechanics and uncertainty to attempted actions.

**Persistence:** Preserves consequential established meaning across sessions.

**Narrative Experience:** Expresses accepted, character-accessible information without independently deciding consequential truth.

The AI-GM may introduce reasonable consequential developments through authorized contextual adjudication. Once accepted, those developments become authoritative.

Provider output remains untrusted until accepted through the appropriate gameplay boundary.

Narration cannot independently modify accepted outcomes.

Shared storage, retrieval, orchestration or presentation does not transfer conceptual authority.

## Representative validation scenarios

### A — Guard identity and history

A guard accepts a bribe, changes assignment and is later promoted.

The foundation preserves consequential identity and history without requiring exhaustive biography or event simulation.

### B — Matron Veyr's competing interests

An NPC has obligations, objectives, limited legitimate knowledge and conflicting interests.

Adjudication must respect these circumstances rather than manufacture convenient concessions to accommodate the player.

### C — Warded tower

An established hidden magical ward prevents levitation.

The ward applies despite player ignorance.

Legitimate later removal changes current circumstances and subsequent adjudication.

### D — Binding agreement

An agreement has defined prerequisites, exclusions, effects and termination conditions.

Applicable terms govern adjudication even when the player does not explicitly mention them.

### E — Cross-domain information

A temple, its factional affiliation and its deity's doctrine are represented across composed foundations.

Relevant information is accessed selectively while maintaining coherent identity, canonical consistency and legitimate character knowledge.

Validation must distinguish representation failures, retrieval failures and adjudication failures.

Conceptual representability is not proof of runtime reliability.

## Accepted residual risks

The owner explicitly accepts four risks for evaluation through gameplay:

**R1 — Retrieval omission:** Material information may be omitted during retrieval.

**R2 — Adjudication misapplication:** Retrieved information may be applied incorrectly.

**R3 — Historical under-persistence:** A fact initially considered minor may later prove consequential.

**R4 — Excessive complexity:** Information and history tracking may become unnecessarily elaborate.

These risks do not block design acceptance.

Investigate observed failures and refine the system proportionately.

Do not introduce speculative preventive infrastructure solely because these failures are possible.

## Design rationale and tradeoffs

The following rationale preserves the reasoning behind the accepted choices. It is explanatory, not an additional set of requirements.

### Composable foundations rather than isolated Region Packs

The game requires coherent information across geography, factions, deities, cultures and evolving circumstances.

Treating each Region Pack as a self-contained world would duplicate shared information and risk contradictory accounts of the same entities or setting.

Composable foundations allow meaningful separation of authored content while preserving one coherent authoritative setting.

This also explains why pack boundaries should reflect useful informational depth rather than arbitrary granularity.

### Relevance rather than geography

Geography alone cannot determine which information applies to a gameplay situation.

A deity's doctrine, faction obligation or historical commitment may remain relevant across many locations.

Relevance-based composition permits information from different domains to govern the same consequential situation.

### Meaningful history rather than exhaustive simulation

Consequential gameplay requires continuity, not a complete record of everything that occurred.

Retaining meaningful developments supports causal consistency while avoiding the complexity of exhaustive event sourcing or continuous simulation.

Selective retrospective adjudication allows the world to evolve without requiring every offscreen event to be computed in advance.

### Stable identity and graph-capable relationships

Consequential history and relationships require consistent references to important entities.

Relationships also allow information to be found across domains, such as a temple's connection to its deity.

These capabilities do not inherently require a graph database or universal registration of every entity.

The functional need is reliable identity and relationship-based access; storage technology remains an implementation choice.

### Selective retrieval rather than exhaustive context

Consequential adjudication requires the applicable information, not every fact in the world.

Retrieving everything would create unnecessary processing complexity and potentially obscure what matters.

Selective retrieval is therefore accepted, provided material binding constraints are not omitted.

The risk of retrieval failure is recognized and intentionally reserved for gameplay-based validation rather than speculative preventive infrastructure.

### Contextual adjudication rather than exhaustive authored truth

An open-ended RPG cannot reasonably pre-author every person, object, circumstance and development.

The AI-GM must be able to establish plausible previously unspecified information when gameplay requires it.

However, contextual adjudication cannot silently replace established facts, bypass binding conditions or rewrite outcomes to favor the player.

This preserves flexibility without sacrificing consequential continuity.

### Gameplay validation rather than premature safeguards

The design recognizes possible failures in retrieval, adjudication, historical retention and system complexity.

The owner accepts these risks because their actual gameplay significance is not yet demonstrated.

The project can use extended gameplay and targeted testing to refine systems when failures become material.

This avoids building elaborate safeguards against hypothetical problems before evidence justifies them.

## Implementation freedoms

The accepted design does not prescribe:

- Graph databases or particular storage technology.
- Universal entity schemas.
- Exhaustive event sourcing.
- Region Pack file formats.
- Retrieval algorithms or caching architectures.
- Continuous offscreen simulation.
- Exhaustive individual knowledge or relationship ledgers.

Implementation mechanisms must satisfy the functional requirements, but current implementation limitations do not define the target design.

Bounded implementation and predetermined fixtures remain acceptable when upstream systems are absent, provided fixtures conform to accepted information contracts.

This documentation task does not authorize implementation.
