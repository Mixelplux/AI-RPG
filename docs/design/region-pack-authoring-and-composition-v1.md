# Region Pack Authoring & Composition Design V1

**Phase: Design. Status: owner-accepted RPA-01–RPA-13; documentation candidate
for owner review.** Consolidated October 25, 2026 from the owner-supplied accepted
design documentation handoff. Acceptance of the design is distinct from acceptance
and publication of this incorporation candidate. No implementation is authorized.

Verified published preparation baseline: local and remote main at
86f0618e81dbfcc09b32233c9ab4c5485c6136dd.
This record selects no capability package, stages no sprint, changes no lifecycle,
source data, rules or save format, and authorizes no Git staging, commit, merge,
push, publication or live-provider execution. [WORKFLOW.md](../../WORKFLOW.md)
retains those authorization boundaries.

## Purpose and governing contracts

Region Packs provide coherent, composable information for one setting and era.
A region is an information domain and need not be geographic. Consequential
information requires appropriate authority and persistence, but does not always
require advance authorship. Compatible information accumulates; contradictions
require legitimate reconciliation, and greater specificity alone never overrides
established truth. Stable identities and selective relationship retrieval support
large persistent campaigns without exhaustive advance modeling.

This record specializes Region Pack authoring and composition. It does not
duplicate, redefine or supersede [Information Foundation D1–D16](information-foundation-functional-design-v1.md),
[Information-Grounded Adjudication D-A1–D-A6](information-grounded-adjudication-v1.md)
or [Integrated Gameplay Architecture IG-01–IG-18 and IG-20–IG-23](integrated-gameplay-architecture-v1.md).
IG-19 remains unaccepted. Read with [F01](f01-truthful-presentation-and-epistemic-fidelity.md),
[F05](f05-authorized-activities-and-player-control.md), the
[shared doctrines](systems/README.md#shared-doctrines) and
[system responsibility map](systems/system-map.md).

Authored content, rules definitions and campaign state have distinct responsibilities.
Legitimate campaign developments can change current circumstances established by
authored foundations. Authorized contextual adjudication may establish genuinely
unspecified details. Established-but-unavailable information cannot be treated as
unspecified; applicable material hidden constraints must govern adjudication
without automatic disclosure. Existing gameplay owners retain their authority.

Current implementation is technical evidence and a possible resource, not design
authority. Scenario-specific and prototype choices do not limit future scalability.
This milestone incorporates accepted Design; it does not conduct new Research,
create production packs or design or implement World Forge.

## Accepted Region Pack decisions

The following RPA-01–RPA-13 preserve the owner's accepted decision text and
qualifications.

### RPA-01 — Information Structure

Distinguish:

- **Information domain:** A coherent category of world knowledge, such as Organizations, Religions, Cultures, History, or Geography.
- **Authored pack:** A managed collection of related authored information.
- **Subject:** An identifiable entity, location, organization, phenomenon, or other topic described by the information.
- **Information assertion:** A fact, relationship, condition, attributed claim, or other meaningful statement about a subject.
- **Retrieval unit:** The relevant portion of information supplied for a particular gameplay need.

A subject may appear across multiple packs without duplicating its identity or higher-level authoritative information.

Retrieval units need not correspond to complete packs. Their boundaries should support selective retrieval while preserving the context necessary to interpret them.

Pack boundaries reflect meaningful informational depth, not arbitrary fragmentation.

### RPA-02 — Hierarchical and Cross-Domain Composition

Higher-level foundations establish common information. More specific packs contribute compatible additional information and legitimate scoped exceptions.

Geographic hierarchies and cross-cutting domains may apply simultaneously.

Examples:

- Forgotten Realms → The North → Icewind Dale → Bryn Shander.
- Forgotten Realms → Organizations → Zhentarim information.
- Forgotten Realms → Religions → deity and religious information.

An individual subject does not automatically require a dedicated pack.

A geographic pack may depend on applicable higher-level organization, religion, culture, or history information.

Sibling packs must not directly depend on one another.

Waterdeep and Neverwinter may independently extend higher-level Zhentarim information without importing each other's local authored content.

Shared identities and appropriate higher-level foundations connect related subjects.

Dependency relationships must be coherent and free of circular requirements.

Do not require all applicable information to fit a single geographic tree.

### RPA-03 — Stable Identity and Attribution

Consequentially important subjects require stable identities across authored foundations, retrieval, campaign developments, and persistence.

Incidental subjects acquire stable identities when consequential continuity requires them.

Universal registration of every object, incidental NPC, or descriptive detail is unnecessary.

Material assertions must preserve sufficient meaning and attribution to distinguish:

- Subject and relevant identity.
- What is asserted.
- Scope and applicability.
- Objective truth versus belief, report, inference, or uncertainty.
- Relevant source or authoring provenance.

This is a logical information contract, not a mandate for a universal entity framework.

### RPA-04 — Composition and Explicit Exceptions

Compatible authored assertions accumulate.

A local addition does not require an exception merely because it adds specificity.

Where information genuinely differs from a higher-level fact or constraint, the exception must be explicitly legitimate and appropriately scoped.

An exception must preserve sufficient information about:

- The general fact or constraint it qualifies.
- Applicable location, subject, circumstances, or fictional time.
- The difference.
- Its legitimate explanation.
- Any consequential mechanical applicability.

Greater specificity does not automatically authorize overriding broader information.

Unexplained contradictions between applicable canonical authored assertions must be corrected before authoritative gameplay use.

Beliefs, reports, historical distinctions, and objective reality must not be conflated.

Legitimate campaign changes are not automatically authored-content contradictions.

### RPA-05 — Pack Applicability

Pack applicability derives from gameplay relevance, not geographic location alone.

Relevant factors include:

- Location and surroundings.
- Involved subjects and stable identities.
- Organizational, cultural, religious, and historical relationships.
- Fictional time.
- Current circumstances.
- The attempted activity, target, and authorized method.
- Applicable binding conditions and exceptions.

Multiple foundations may apply to one consequential decision.

Applicability must support proportional information retrieval without requiring exhaustive setting traversal.

### RPA-06 — Distinct Information Responsibilities

Preserve three logically distinct information responsibilities:

**Authored setting information:** Establishes reusable setting truths, meaningful initial conditions, relationships, circumstances, and supported declarations.

**Mechanical and rules-based definitions:** Establish applicable gameplay mechanics and their interpretation through the responsible gameplay domains.

**Persistent campaign information:** Represents legitimately accepted current conditions, changes, relationships, commitments, and consequential history.

These may describe the same fictional subject without sharing conceptual authority.

The separate Core Gameplay Domains track uses the 2024 tabletop rules foundation with explicit adaptations.

This Region Pack Design must support that direction without designing the entire rules framework.

### RPA-07 — Setting-Specific Phenomena

Authored content may establish phenomena with consequential mechanical effects that are not conventional spells or standard character abilities.

Examples include persistent magical miasma, supernatural environmental conditions, local magical restrictions, and unusual world-specific effects.

Authored information defines the phenomenon's meaningful nature, applicability, boundaries, conditions, and exceptions.

Responsible gameplay systems apply supported mechanics and establish accepted results.

Setting prose alone cannot execute arbitrary mechanical consequences.

Do not force all world magic into the conventional spell system.

Do not create a universal magical-effect framework without demonstrated requirements.

### RPA-08 — Progressive Specification

Authored content does not need exhaustive advance detail.

Distinguish:

- Established and available information.
- Established but currently unavailable information.
- Genuinely unspecified information.
- Genuinely uncertain information.
- Beliefs, claims, and character inferences.

Previously unspecified details may be established through legitimate contextual adjudication when relevant.

Consequential accepted details become persistent campaign truth through the appropriate owning system.

Established facts cannot be silently rewritten to accommodate player intentions or desired outcomes.

Incidental descriptive details do not automatically become persistent authoritative information.

### RPA-09 — Current Circumstances and Historical Truth

Authored foundations provide initial and generally established circumstances.

They are not permanent campaign-reset mechanisms.

Legitimate accepted developments may change affected circumstances.

The current campaign state governs the affected current fact while compatible authored information remains applicable.

Material historical meaning, causal relationships, and consequential commitments must remain available when relevant.

Reusable authored packs are not automatically rewritten by campaign developments.

The architecture must support progressively generated worlds and long-running campaigns without duplicating entire setting foundations into mutable campaign state.

### RPA-10 — Selective Retrieval

Retrieve information at an appropriate granularity below complete packs.

Retrieval may include:

- Identity and distinguishing characteristics.
- Contextual information.
- Relationships and objectives.
- Binding conditions.
- Applicable exceptions.
- Related mechanical definitions.
- Relevant current state and history.

Owning gameplay domains establish their information requirements.

The Information Foundation supports direct and selective relationship-based retrieval but does not independently adjudicate outcomes.

Material applicable hidden conditions must be available internally without automatic character or player disclosure.

Material established-but-unavailable information must be retrieved or leave the affected outcome unresolved.

No particular graph database, embedding system, retrieval algorithm, or caching design is prescribed.

### RPA-11 — Authored Revision and Campaign Compatibility

Distinguish pack identity, authored revision, stable subject references, and accepted campaign meaning.

Updating authored content must not silently invalidate established campaign consequences or history.

Material incompatibility must be detectable and handled deliberately.

The precise mechanisms for content pinning, compatible updates, revision reconciliation, and migration remain deferred.

Preserve the ability to adopt future storage and indexing approaches without changing gameplay meaning.

### RPA-12 — Authoring Provenance and Acceptance

Distinguish:

- Verified canonical information.
- Explicit adaptations.
- Sourced inferences.
- Unverified or generated proposals.
- Legitimately accepted campaign developments.

AI-generated or automatically extracted material is not inherently canonical.

Material source-derived assertions require appropriate source grounding, traceability, conflict evaluation, and authoring review.

Authoring acceptance must occur before proposed material becomes reusable authoritative content.

Validation must cover factual accuracy, structural and compositional integrity, gameplay sufficiency, and cross-system integration.

### RPA-13 — Independent Authoring and Compilation

**Region Pack authoring and comprehensive content validation belong to a standalone tool, separate from AI RPG.**

The tool is tentatively called **World Forge**.

Its responsibilities include:

- Source research and ingestion.
- Authored-content organization.
- Canonical verification.
- Source provenance.
- Stable identity and relationship preparation.
- Composition and exception validation.
- Human review.
- Compilation and versioning of approved content.

AI RPG consumes approved compiled Region Packs through defined interfaces.

AI RPG does not need authoring infrastructure to run.

Runtime responsibilities remain separate:

- Loading and structural integrity checks.
- Applicable information composition and retrieval.
- Mechanical interpretation through owning gameplay systems.
- Authoritative acceptance of consequential changes.
- Persistence and restoration.
- Player-safe presentation.

Runtime gameplay validation remains mandatory. Approval of authored content does not waive validation of consequential gameplay decisions.

The two applications share agreed information contracts, identifiers, and compatibility requirements without requiring shared deployment or implementation.

**This milestone does not authorize designing or implementing World Forge itself.**

## Worked examples

These examples illustrate relationships and authority boundaries, not production
content, verified setting claims, executable formats or newly accepted rules.

### A — Zhentarim, Waterdeep, and Neverwinter

**All local facts and exception terms below are invented illustrations, not
verified Forgotten Realms canon.** A higher-level Organizations foundation gives
the Zhentarim one stable identity and general organizational information. Suppose
it establishes a general internal reporting obligation for recognized local cells.

Waterdeep's pack references that identity and adds local premises, contacts and
circumstances. If one cell has a legitimately granted temporary exemption from
that reporting obligation, its exception identifies the general obligation, the
specific cell, the fictional-time interval, the differing requirement and the
grounded reason for the exemption. Any consequential mechanical applicability
still passes through the responsible gameplay domain.

Neverwinter independently references the same higher-level identity and adds
its own local premises and contacts. It does not import Waterdeep's exemption or
depend on Waterdeep's pack. Waterdeep likewise does not depend on Neverwinter.
A local detail compatible with the general information simply accumulates; it
needs no exception.

A genuinely shared cross-location policy belongs in the appropriate higher-level
or cross-cutting foundation. If gameplay legitimately changes a cell's allegiance
or obligations, accepted campaign state retains that change and relevant history.
Neither sibling pack becomes the other's dependency, and campaign change does
not rewrite the reusable organizational foundation.

### B — Magical Forest Miasma

**Illustrative setting phenomenon; no precise 2024 mechanics are prescribed.**
A geographic foundation establishes a forest and a protected clearing with stable
consequential references. Authored phenomenon information establishes persistent
disorienting miasma, where and when it applies, its meaningful boundaries and the
clearing's protection as an explicitly grounded scoped exception.

| Contribution | Meaning and retained responsibility |
|---|---|
| Authored geography and phenomenon | Supply the forest, spatial anchors, miasma terms, protected clearing and legitimate exception. These are information and supported declarations, not self-executing effects. |
| Mechanical definitions | Responsible gameplay domains supply supported navigation and phenomenon mechanics and interpret applicable terms. A world phenomenon need not be a conventional spell. Unsupported mechanical meaning cannot be invented from evocative prose. |
| Current environment | World Simulation supplies current environmental state, whether the miasma is active and whether the clearing's protection still holds after accepted developments. |
| Character capability and access | Character System supplies established capabilities and legitimate knowledge. Internal access to the miasma's hidden terms does not grant the character that knowledge. |
| Navigation adjudication | Action & Resolution requests applicable geography, conditions, exception, current state, character capability and authorized method. It applies supported mechanics; F05 preserves method choice and F01 expresses only accepted accessible meaning. |
| Accepted change and history | A legitimately adjudicated and accepted event removes the clearing's protection. Owning systems accept the affected changes coherently; Persistence retains the changed condition and material causal history. |

Before removal, the clearing's legitimate exception constrains affected navigation.
After removal, later adjudication uses the changed current condition and applicable
miasma terms. It cannot restore protection merely by rereading the authored
foundation. The reusable pack still describes its authored initial protection;
campaign state carries the accepted removal, relevant time, identity and causal
meaning. Earlier protected experiences remain historically true.

If material established terms are unavailable, retrieve them or leave the affected
outcome unresolved. An internally applied hidden cause need not be disclosed.
Changing an authoritative premise, such as current protection or the exception's
scope, must change its application and any consequent result where relevant.

### C — Progressive Geography

A setting foundation establishes settlements, terrain and a river, including
material spatial anchors, without listing every possible crossing. A previously
established bridge or ford must be retrieved when material, even when omitted
from the latest context. Missing retrieval is not permission to replace it.

Where a crossing is genuinely unspecified, authorized contextual adjudication may
establish sufficient geographic detail before dependent player decisions. It
must respect accepted river geometry, terrain, distances, existing crossings,
fictional time and causal circumstances. It cannot create a convenient ford to
make the player's intended shortcut succeed.

World Simulation owns accepted geography; owning gameplay domains determine
traversability and applicable mechanics. Character System determines what the
character can legitimately observe or know. F01 presents that accessible meaning;
F05 returns any meaningful route or method choice to the player. Establishing a
crossing does not authorize choosing to swim, seek a boat or spend resources.

An accepted consequential crossing acquires the identity and persistent meaning
needed for later retrieval and spatial continuity. A later legitimate flood or
destruction changes current conditions while retaining relevant historical truth.
Incidental scenery does not automatically require persistent records.

## Authoring sufficiency

Authoring sufficiency has three accepted criteria:

1. **Recognition:** Enough distinctive information to portray a subject accurately.
2. **Consequential grounding:** Important circumstances, constraints, objectives, relationships, and pressures.
3. **Contextual extension:** Enough grounding to establish unspecified details without contradiction.

Authorship depth depends on gameplay significance.

Important established constraints, organizations, objectives, spatial anchors, and binding terms may require explicit authoring.

Ordinary inventories, incidental people, exhaustive maps, complete biographies, and every conceivable encounter do not.

Retrievability is a separate operational validation concern; sufficiently authored material is not useful if material applicable information cannot be found.

## Validation approach

Four complementary validation categories apply:

**Factual and provenance validation**
- Canonical accuracy.
- Setting and era coherence.
- Attribution and source grounding.
- Adaptation status.
- Significant conflicts.

**Structural and composition validation**
- Identity/reference integrity.
- Domain and dependency coherence.
- Circular dependencies.
- Duplication of shared authoritative information.
- Legitimate scoped exceptions.
- Contradictory applicable assertions.

**Gameplay sufficiency validation**
- Recognition.
- Consequential grounding.
- Contextual extension.
- Retrieval of applicable material constraints.
- Established-but-unavailable versus genuinely unspecified information.

**Cross-system integration validation**
- Domain-owned information requirements.
- Mechanical interpretation.
- Hidden-information boundaries.
- Authoritative acceptance.
- Campaign changes.
- Historical continuity.
- Persistence and restoration.

Distinguish representation, retrieval, adjudication, acceptance, persistence, and presentation failures.

Tests should demonstrate dependence on changed authoritative premises rather than fixed scenario answers.

Use continuing multi-pack gameplay for later integration validation where appropriate.

No live-provider tests are authorized.

## Scalability and risks

Preserve compatibility with:

- Extensive authored settings.
- Many coherent information domains.
- Shared identities and selective indexes.
- Cross-domain relationships.
- Incremental content additions.
- Progressively generated locations and encounters.
- Large persistent campaigns.
- Future storage and indexing migrations.

Do not select a graph database solely because the information is relational.

Existing Information Foundation risks R1–R4 remain accepted:

- Retrieval omission.
- Adjudication misapplication.
- Historical under-persistence.
- Excessive complexity.

Also identify:

- Authoring conflicts at scale.
- Incorrect exception scoping.
- Authored revision incompatibility.
- Unsupported mechanical phenomena.
- AI-generated canonical inaccuracies.
- Long-campaign performance uncertainties.

Treat them proportionately, preserving existing accepted risk decisions.

## Explicit deferrals

Do not implement or finalize:

- Production Region Packs.
- World Forge architecture or implementation.
- Comprehensive setting databases.
- Canonical ingestion tooling.
- Exact serialization formats.
- Automatic migration.
- General autonomous world simulation.
- Universal magical-effect systems.
- Full spatial maps.
- Graph-database selection.
- Additional provider experiments.
- Core Gameplay Domains mechanics.

Source licensing and import procedures remain separate future considerations.

## Contract reconciliation and implementation boundary

| Existing authority | Region Pack relationship; retained contract |
|---|---|
| [Information Foundation](information-foundation-functional-design-v1.md) | D1–D16 remain unchanged. RPA adds authoring/composition detail, scoped exceptions, provenance and the external-tool boundary. The foundation supplies direct and selective relationship retrieval without adjudicating. |
| [Information-Grounded Adjudication](information-grounded-adjudication-v1.md) | D-A1–D-A6 remain unchanged. Applicable conditions, hidden terms and established-but-unavailable information retain their existing treatment; authoring approval never substitutes for consequential gameplay validation. |
| [Integrated Gameplay Architecture](integrated-gameplay-architecture-v1.md) | Accepted IG decisions remain unchanged. Domains own dependency requirements and validation; coordination acquires no outcome authority. Mutually dependent changes retain coherent acceptance, continuity and recovery requirements. |
| [Scenario & Authored Content](systems/scenario-authored-content.md) | Supplies reusable identity, foundations, initial constraints and supported declarations. Independent World Forge authoring prepares approved content; it creates no new runtime system authority. |
| [World Simulation](systems/world-simulation.md) | Owns authoritative current external circumstances and legitimate changes, including accepted progressive geography. Authored baselines do not reset changed campaign truth. |
| [Action & Resolution](systems/action-resolution.md) | Interprets supported mechanical definitions and applicable phenomenon terms under authorized methods; prose does not execute arbitrary effects. |
| [Character System](systems/character-system.md) and [Actors & Social Dynamics](systems/actors-social-dynamics.md) | Retain capability, legitimate access and meaningful intentional actor decisions. Authored identities, roles and claims grant neither current knowledge nor consent. |
| [Persistence](systems/persistence.md) | Preserves consequential accepted meaning, identity and material history with existing atomicity and compatibility commitments. RPA selects no save version, migration, pinning or revision-reconciliation mechanism. |
| [F01](f01-truthful-presentation-and-epistemic-fidelity.md) and [F05](f05-authorized-activities-and-player-control.md) | Attribution, uncertainty, hidden-information boundaries, player method choice, interruption and preserved accepted results remain unchanged. Narration and input/display gain no fictional authority. |

World Forge is the tentative name of a standalone authoring and comprehensive
content-validation tool. AI RPG consumes approved compiled packs through agreed
contracts and remains responsible for runtime integrity, composition, retrieval,
domain-owned mechanical interpretation and acceptance, persistence/restoration and
player-safe presentation. Shared contracts do not require shared implementation
or deployment. No World Forge architecture or implementation is authorized.

The current bounded runtime, schemas, fixtures, saves and implementation-status
records are unchanged. Full multi-pack composition, production authoring,
scalable retrieval and revision compatibility are accepted design direction,
not claims of completed runtime functionality. Later implementation and gameplay
validation require separately authorized bounded work.
