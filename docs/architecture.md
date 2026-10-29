# System Architecture

## Purpose

This document is a concise map of the current AI Narrative RPG Engine architecture.

Detailed architectural decisions belong in `docs/decisions.md`. Package-specific requirements belong in the current capability package.

Implementation descriptions were reconciled October 12, 2026 against published
baseline `a6ff316473ce2bafc58be4718479261602f5e3ac`, covering accepted work
through October 11. Prior research is indexed separately in the non-authoritative
[architecture comprehension review](architecture_comprehension_review.md).

Living responsibility models and shared design doctrines are indexed in
[System design manifests](design/systems/README.md). Their
[system map](design/systems/system-map.md) separates conceptual ownership from
the runtime flow and storage boundaries described here.

Do not add sprint history, full schemas, test inventories, or implementation walkthroughs here.

## Watchhouse Records M1 — owner accepted and published October 29, 2026

`play_watchhouse.py` opens a separate schema-4 Runtime through `engine.watchhouse`.
Full-utterance, bounded natural-language interpretation preserves inquiry and
returns control for unclear/compound methods. `watchhouse_domain` composes one
custodian's duty-grounded Influence responses, legitimate ledger access and
Search/Study findings; `watchhouse_rules` owns explicit scoped Character skill
inputs and pure 2024 checks. No legacy climbing statistics or gate mechanics
govern these actions. Existing Coordinator/F05 and common acceptance publish one
root with time, causal history, accepted evidence and Character-safe receipts.

Permission, refusal timing and findings derive from validated accepted units;
there is no parallel mutable social store. Versioned scenario and Character
declarations use existing inert scope payloads. Envelope V3 and schema 4 are
unchanged, as are historical schemas 1–3 and V1/V2 routes. Receipt/evidence
reconstruction and atomic disk replacement reuse the existing paths. No provider
or general social/spell system is added; ordinary `play_game.py` is unchanged.
M1 was owner accepted and published October 29, 2026 at `014c1b84efbedef742e0cc23d737c4ef2d0020ec`. See [handoff](watchhouse_m1_handoff.md).

## Cross-Domain Coupling Correction V1 — implementation awaiting acceptance

The schema-4 common campaign/activity boundary now uses scoped identity,
authorization, meaningful target stages, inert owner payload/evidence, validated
progression and character-safe receipts. `domain_dispatch` reuses Coordinator/F05;
`domain_owners` selects installed semantic owners without mechanical verb branches.
`climbing_domain` composes existing World/Character/Resolution climbing mechanics.
Common acceptance and continuity do not interpret distance, climbing costs,
falling, injury or climbing risk stakes. Owners declare the relevant decision
premises; common history preserves occurrence, scope, restrictions and answers,
checking those premises after every accepted increment during acceptance and
restoration. Climbing independently checks receipt meaning against validated
evidence and character access limits. Common acceptance enforces the applicable
Coordinator receipt contract, including unique public references, before publication.
One captured-root check/publication remains authoritative across all effects.

Envelope V3 retains schemas 1–3 through explicit historical evaluators and a finite
schema-specific codec; they share Runtime and the common publication boundary.
New schema 4 is opt-in, with no migration or rewriting of historical saves. An
independent non-movement mechanical fixture exercises the same common runtime,
continuity and disk paths; it adds no gameplay subsystem. See the
[implementation handoff](cross_domain_coupling_v1_handoff.md) for evidence and
limits. Owner acceptance and all Git publication remain separate. Historical
milestone descriptions below retain their original version-specific scope.

## Physical Traversal Core V1a — owner-accepted M1 foundations

Owner accepted M1 foundations October 26, 2026 after blocking corrections. World-owned local
physical views (`physical_world.py`) separate stable objects/attachments and
position/time/causes from sparse PC/NPC capabilities (`character_rules.py`).
`traversal_resolution.py` discovers owner dependencies, computes actual 2024
climbing costs/checks and separate established-fall damage, and rejects missing,
unsupported or stale premises. Results are provisional, with no save publication.

`traversal_coordination.py` exercises the existing I1 Coordinator/F05 assessment
interface. It refuses consequential execution pending M2 common-runtime aggregate
integration. The CLI and GameEngine do not yet route climb commands here. The
finite d6 adjudicator is not reused as a climbing rule. Existing v1/v2 saves and
accepted gameplay remain unchanged. See [M1 design](physical_traversal_m1_design.md)
and [handoff](physical_traversal_m1_handoff.md) for exact limits and compatibility.

The owner's October 26 clarification separates movement allowance from physical
coordination and action economy through Character's general PhysicalCapability
view. Resolution requires coordination for climbing even without a check; Stunned
alone never sets Speed to zero or establishes a fall. Fall validation captures an
immutable starting frame, including when suppliers reuse mutable view wrappers.
M2 must ground actual consequences for exposed, protected and near-ground failures;
provisional objective failure neither asserts safety nor automatically causes falling.

## Physical Traversal M2-2a — owner accepted October 26, 2026

World supplies fixed support/exposure, landing geometry, assistance and verified
physical protection before an uncertain attempt. Resolution validates explicit
contextual check stakes and failed-effort commitment, then records d20/d6 draws.
World distinguishes supported no progress, grip loss held by a taut system, and
an actual fall. Character owns HP/temporary HP, Prone, Unconscious, immediate death
and the minimum immediate zero-HP state. World drops held objects while preserving
independent attachments. No universal secondary fall-chance rule is introduced.
Generated causal/fall IDs are checked against the complete World identity namespace
before sampling. The supported local anchor/worn harness configuration rejects
contradictory dispositions; explicit harness locations follow accepted movement,
and extended rope connections remain permitted. Damage taken at zero HP uses the
2024 damage-at-zero threshold independently of temporary-HP absorption.

Ordinary climbing remains mechanical without equipment or protection detail unless
consequential circumstances require it. TautProtection is one supported arrangement,
not the definition of all protected climbing. Other arrangements can extend the
owning World/Character/Resolution contributions, finite codec and safe projection
without changing the common acceptance unit or root-publication semantics.

These contributions extend the same common root and final publication check.
Assessment is read-only; all possible failure branches and F05 risk commitments
must be supported before sampling. Technical rejection publishes nothing. Safe
receipts expose accepted felt effects, without hidden causes, internal landing
geometry or facts arising after loss of awareness. Exact retries reuse the receipt.

Opt-in domain schema 2 under envelope v3 persists these semantics. Schema 1 retains
its historical deterministic meaning, including a finite explicit legacy-default
decode for previously saved bytes. Historical validation recomputes mechanics from
recorded rolls and owner premises without invoking resolution or randomness.
Whole-state comparison precedes adoption; v1/v2 and atomic file writes are preserved.
See [the model](physical_traversal_m2_2a_design.md) and
[handoff](physical_traversal_m2_2a_handoff.md) for accepted scope, closure and publication readiness.
M2-2a was accepted and published before the current baseline. The separately
authorized M2-2b implementation below was owner accepted October 27, 2026; broader
limitations remain.

## Physical Traversal M2-2b — owner accepted October 27, 2026

The historical schema-3 activity contract adds bounded continuity within the existing Campaign/Runtime.
One immutable objective/method/restriction scope may cover several established
World links. Each accepted increment preserves actual position, time, Character
expenditure, mechanics and consequences; progression derives from accepted units,
not percentages or descriptive narration. Ordinary execution continues until an
F05 boundary, unavailable prerequisite, failed attempt or completion.

World/Character suppliers contribute typed changed facts and access-qualified
checkpoint notices through the same coherent root publication. Schema-3 recognizable
decisions require unique response keys and complete access-qualified notices.
Internal `ChoiceContext` records bind each keyed decision to its establishing
owner occurrence and explicit existing stage occurrences. Pure history validation
binds the relevant remaining-stage climbing circumstances and rule stakes too;
notice-text equality is never proof of unchanged consequential meaning. A stable
occurrence may span stages, survive unrelated World changes and retain its answer.
A different occurrence, expanded scope or changed scoped risk/stakes requires a new
key and appropriate fresh response. Completed-stage facts do not revoke remaining
permission. Original bare answers retain only established original mechanical-risk
scope. Explicit situated responses retain original restrictions and bind to the
current revision and accessible notice. Context/risk provenance remains internal;
only access-qualified notices cross the presentation boundary. Current owner
inputs and rules are reassessed before each new increment; historical receipts precede owner reads
on exact retries. No checkpoint result references are supported in any schema.

Envelope v3/domain schema 3 opts into continuity and ordered fact/control changes.
Schemas 1/2 keep their historical meanings through finite default decoding; v1/v2
remain unchanged. Pure historical reconstruction validates every increment/update
and the final aggregate before adoption, without randomness or repeated effects.
The [model](physical_traversal_m2_2b_design.md) and [handoff](physical_traversal_m2_2b_handoff.md)
state supported interfaces and limits. Implementation was owner accepted October 27, 2026 and remains uncommitted; Git publication requires separate authorization; no CLI/narrator, other traversal method or general simulation
is added. Overall systems remain Partial.

## Tech Stack

M2-1 is the published accepted foundation. The common consequential
`Runtime` also accepts an explicit `domain_campaign.Campaign` root, created through
`GameSession.start_domains`. This mode has no legacy GameEngine world alongside
it. `domain_campaign` prepares and validates domain-owned consequences; Runtime
publishes one root containing World/Character state, scoped authorization and
accepted-unit recognition. The existing Coordinator/F05 adapter manages typed
climb input. All required receipt checks precede publication.
Request types are checked before retry recognition. Separate checkpoint result
reuse is unsupported: non-null resolution references reject before adoption or execution.

Version 3 stores this opt-in aggregate through a finite codec; v1/v2 retain their
existing routes and JSON decoding behavior. V3 rejects duplicate JSON keys,
including nested records. Pure complete-aggregate validation precedes restore adoption;
the existing atomic writer preserves earlier files on pre-replacement failure.
That baseline supports deterministic full-link climbing. Published M2-2a adds
uncertain consequences; M2-2b adds activity continuity across meaningful established
links. Arbitrary positions inside a link and CLI integration remain deferred. See [M2-1 model](physical_traversal_m2_1_design.md) and
[ADR-063](decisions.md#adr-063--opt-in-core-domain-campaign-aggregate).

- Python 3.13
- CLI gameplay interface
- JSON Region Packs for authored world content
- Default version-1 World State saves; opt-in version-2 and version-3 campaigns
- OpenAI Responses narration preview behind provider-neutral engine boundaries

## Directory Map

```text
/
├─ engine/          Simulation, interaction, state, projection, persistence, narration
├─ data/regions/    Immutable authored Region Packs
├─ docs/            Architecture, ADRs, workflow, package, and sprint records
├─ tools/           Validation, preflight, and review-packet tooling
├─ handoffs/        Review and handoff artifacts
├─ .artifacts/      Temporary evaluation evidence
├─ play_game.py     CLI entry point
└─ test_*.py        Automated tests
```

## Runtime Flow

```text
Player input
    ↓
CLI intercepts applicable session controls → session handling / feedback
    ↓ gameplay input
GameEngine.process_command() — gameplay orchestration
    ↓
Explicit I3 with situated activity supplier → bounded player input → common I1/I2/I3 owners
(terminal routing: unsupported input cannot enter legacy mutation)
    or default version-1 runtime:
Bounded coordination → contextual material action → contextual investigation → legacy fallback
(next route only if input is unclaimed)
    ↓
    ├─ Read-only assessment / result → player-facing presentation
    └─ Consequential operation
           ↓
       Prepare candidate state + consequences
           ↓
       Validate candidate → build required scene
           ↓
       Publish state/scene once → authoritative state/result
           ↓
       Derived player-safe views → result / scene / narration presentation
```

`GameEngine` is the gameplay-facing orchestration boundary. Player-facing code must not directly mutate lower-level state.

## M2-M1 player input — owner-accepted bounded implementation

Owner accepted October 24, 2026 after handoff review and successful interactive
smoke (45 seconds, two lamp units remaining, three accepted increments).
Documented bounded limitations remain; Git publication requires separate authority.

`engine/player_activity.py` connects bounded ordinary inspection/search instructions
to `process_consequence`, the I1 coordinator/F05 policy and existing domain-owned
I2/I3 acceptance. Current legitimate suppliers return situated targets, visible
aliases, available methods/means and accessible descriptions. Interpretation chooses
no outcome. Inquiry/preparation are read-only; unsupported language/constraints
return control. Each committed instruction authorizes one finite supported increment.
`continue` uses durable undertaking scope and current restrictions; a completed
undertaking does not reroll. No legacy fallback is available on this opt-in path.

Opaque request/undertaking references distinguish retry from a new attempt. Explicit
retry recognition uses saved accepted receipts before current eligibility, requiring
no installed supplier result. New attempts require fresh domain information and
F05 checks. A supplied context is rechecked at execution and immediately before
acceptance; the existing owning read/root checks still protect dependent effects.

Services are installed explicitly on fresh restoration; callbacks and parser state
are not saved. Existing-engine load retains its installed context service, called
with the restored engine. I3's version-2 format/ownership and version-1/default/I2
boundaries are unchanged. Production CLI/content, general language and domain rules
remain deferred. See the [M2-M1 handoff](m2_m1_handoff.md) for support and trust limits.

## I2-M1 consequential integration — owner-accepted bounded implementation

The [I2-M1 handoff](i2_m1_handoff.md) records an explicit GameEngine
`consequence_config` opt-in and `process_consequence` path through the existing
I1 coordinator/F05 contracts. Trusted suppliers declare controlled actor and
target/method scope, authoritative premises, finite supported methods/effects,
character grants and existing mechanics. The domain discovers direct, linked
and binding-term dependencies selectively and iteratively; retrieval owns no
outcome. The bounded adjudicator prepares copied candidates without owning
integrated truth.

One engine-held authoritative aggregate publishes dependent I2 resources/time,
conditions, commitments, new facts/identities/relationships/grants and acceptance
receipts together after candidate/safe-receipt validation and final premise
rechecks. A matching accepted logical identity reuses its receipt before new
eligibility or resolution, across reconstructed domain/coordinator objects.
Later activities retrieve accepted owning-domain records rather than prose.
Legacy world is a read-only premise here; coupled legacy/I2 mutations are not
supported. Private diagnostics and Character-safe results remain separate.

This is synchronous, non-reentrant, one-engine in-memory continuity, not I3
recovery or save restoration. Opt-in save/load rejects before file I/O; reset,
adoption and legacy command dispatch also refuse to discard/mix this state.
Default version-1 production save/load and dispatch remain unchanged. No new
rules, general language/actor implementation, production content or permanent
storage doctrine is introduced. Owner accepted the implementation and documented limits after successful smoke October 23, 2026;
conceptual ownership and Partial classifications remain unchanged.

## Bounded I1-M1 coordination — owner-accepted bounded implementation

`engine/gameplay_coordination.py` adds one common session-local runtime with
interpretation, undertaking, situated-context and coordination-decision contracts.
GameEngine tries this path before contextual/legacy dispatch. Claimed ambiguous,
unsupported and erroneous requests are terminal; only unclaimed raw commands
continue. Existing `search for ...` investigation phrasing remains unclaimed.

Owner-supplied domain checkpoints identify applicable responsibilities and the
next bounded activity. Existing F05 policy decides continuation/control/completion;
coordination does not resolve mechanics, invent methods/means, choose NPC intent
or own consequential truth. Permissions are single-use and require fresh matching
context and domain assessment. Accepted references and constraints remain in the
logical undertaking; explicit continuation rechecks current prerequisites.

Public results use fixed messages and character-accessible references, with
numbered choices for explicit clarification instead of hidden keys. Internal context, diagnostics and raw
exceptions stay out of player output. The small offline grammar covers explicit
open/search/observe forms, inquiry/preparation/commitment and limited modifiers;
it is not validated general language understanding. Production observation uses
existing safe scene projection. Missing search/door/actor capabilities are
explicit owning-domain fixtures exercising this same GameEngine runtime.

Suppliers own read-only assessment, accurate material revisions and atomic domain
execution. No universal transaction engine, I2 consequential integration or I3
persistence/recovery is implemented. Runtime replacement clears session-local
coordination. Save version 1 and existing owning publication operations are
unchanged. See [the I1-M1 handoff](i1_m1_handoff.md) for validation and trust limits.
Owner-authorized I1-M1 correction, October 23: accepted receipts now carry explicit
domain result meaning and a Character-safe result projection. The common runtime
immediately assesses the next current boundary and continues ordinary supported
steps only under fresh F05 permission and domain acceptance. A natural decision
point describes established accessible circumstances without leading questions or
automatic menus. Explicit ambiguity can still require clarification. Exact
supplier-supported direction phrases provide bounded free-form choice; they are
not general navigation or language interpretation. Refinements preserve accepted
work and apply constraints prospectively. A later failure retains earlier accepted
results/costs. See the [correction handoff](i1_m1_handoff.md) for the finite per-call
bound and trusted supplier limits; no I2/I3 or new gameplay mechanics are claimed.
## Sources of Truth

### World State

`world_state` owns mutable persistent simulation truth, including accepted runtime state such as:

- player location, time, and weather;
- durable history;
- pressures and thread state;
- actor location changes;
- actor knowledge;
- evidence traces and player discoveries;
- player competence tags and accepted attempts for the bounded West-Road slice;
- the fixed west-road reference predicament phase and causal outcome reference;
- optional declared material conditions, cooperation and causal handling/development
  records for the opt-in material scenario.

### Region Packs

Region Packs are immutable authored content.

They define locations, connections, actors, descriptions, initial values, and bounded authored declarations.

Runtime state may use Region Pack policy, but Region Packs themselves do not become mutable state.

### Derived Projection

Scene Snapshots, player perception, affordances, and narration context are derived from authoritative state and authored content.

They do not own persistent simulation state.

## Persistent Transitions

Material state changes use the established candidate-state pattern:

```text
Copy current state
    ↓
Prepare source event and consequences
    ↓
Validate completed candidate
    ↓
Build required derived scene
    ↓
Publish once
```

Failures must not leave partial durable mutation.

Durable causal references use stable backward `history_id` references.

Save envelope version remains `1`. Revised Bryn Shander content deliberately rejects prototype saves missing `west_road_predicament`; loading does not invent a branch or alter the existing file/session. See ADR-060. Other content retains its own validated state requirements.

Character Competence V1 uses one local authority for evidence applicability,
recognition, eligibility, costs and d6 interpretation. Accepted West-Road attempts
persist their draw/result and backward causal references; full results reuse the
existing pursuit outcome in the same candidate transaction. Missing additive
competence fields normalize empty only in a copied loaded payload. Projection
and narration receive player-safe layers, never authority to resolve attempts.

## Character Information and Spatial Projection

Keep these concepts separate:

- **World truth:** what is actually true.
- **Perception:** what the character can currently observe.
- **Familiarity:** broad background understanding.
- **Acquired information or belief:** selectively retained information encountered during play.

Player-facing projection must not expose hidden causes or information merely because the engine knows it.

Use minimum sufficient world detail:

- author important structure;
- resolve incidental detail only when needed;
- persist it only when future gameplay materially depends on it.

The authored map represents macro spatial relationships, not every possible traversal path. Spatial presentation should favor natural orientation over a raw compass-direction grid.

See ADR-059 for governing detail.

## Narration Boundary

F01 Narrative Realization V1 provides an owner-accepted bounded component in
`engine/narrative_realization.py`; ordinary gameplay routes are unchanged.
It validates explicit caller-supplied context, serializes it to one injected
generator and applies the existing prose output validator. The opt-in provider
adapter reuses `narration_source.request_narration_text`; no provider is called
by default. Relevant semantic continuity is supplied by the caller, with no stored
transcript, memory policy or simulation references. Shape validation does not
authenticate authority, prove sufficiency or certify prose fidelity.

The accepted implementation is the original candidate with the instruction-only
[presentation correction](f01_presentation_correction_v1_report.md), covering direct
substantive NPC speech, activity-integrated time and relevance-sensitive
qualifications. Input shape, single-call stateless execution, transport and output
validation are unchanged. No new gameplay or persistence authority is established.
See [owner acceptance and limitations](f01_narrative_realization_v1_acceptance.md).

The owner-accepted damaged-gate integration includes an **instruction-only
correction** after live Case 5 omitted a committed pin at a player decision.
It prioritizes consequential understanding of the next choice, including earlier
accepted work/costs, while allowing irrelevant known context to carry implicitly.
Input shape, the single-call mechanism, structural validation, provider settings
and gameplay authority are unchanged. This is guidance, not semantic enforcement
or a guarantee of generated fidelity. Four later samples provide limited
comparison evidence; see the historical [correction report](f01_consequential_fidelity_correction.md)
and current [acceptance and limitations](f01_f05_integration_v1_acceptance.md).

The [first A–D evaluation](f01_narrative_realization_v1_evaluation.md), mixed
[generic correction comparison](f01_generalizable_realization_correction_v1.md)
and [original connected evaluation](f01_connected_experience_v1_report.md) remain
historical evidence. The generic revision is not the accepted runtime. The owner
found connected progression/pacing satisfactory and accepted remaining presentation
limitations; unrestricted fidelity and single-call adequacy are not established.
Alternative architectures remain available for separately authorized work.

```text
Bounded Narration Context
    ↓
Validated Provider-Neutral Request
    ↓
Validated Prompt
    ↓
Untrusted Candidate Source
    ↓
Source-Result Validation
    ↓
Narration-Output Validation
    ↓
Preview Display
```

The provider source is OpenAI Responses through the existing preview boundary.
Accepted ordinary CLI routes also request it for Market Square automatic display
and broad observation/descriptive intention. The request mode still says `preview`;
that label does not mean all narration is a diagnostic-only command.

Narration remains read-only, untrusted, nonpersistent and without simulation
authority. Source/output validation permits display; it does not certify semantic
fidelity. Internal context retains a scene snapshot, but the provider prompt
serializes explicit Scene Context and bounded narrative projection, not that raw
snapshot or the full history. This is not a general character-access model.

Failures preserve deterministic gameplay. The bounded local composition routes
below retain deterministic result/scene fallback; broad provider-backed observation
still returns only an unavailable/retry notice on failure ([DF-008](deferred_findings.md#df-008--narration-unavailable-deterministic-fallback-experience)).

The provisional failed `follow withdrawal signs` gameplay slice also uses a
read-only accepted-result route: recorded result -> accepted player-safe input
foundation -> replaceable content preparation -> stateless realization -> existing
output validation -> one CLI outcome. Revised A is private to the initial
narration adapters; a replacement pair may use a different handoff representation.
Normal gameplay uses local adapters. Provider adapters must be explicitly supplied
under separate live-call authorization. Failure retains the established deterministic
outcome and scene delta. Prose and intermediate content are never persisted or
used to resolve gameplay. Structural validation does not prove semantic fidelity.

Scene Construction V1 composes the bounded North Gate / Southwest Trade Road
views through the same preparation/realization pattern using local adapters.
It joins existing accessible context, public actor roles, and derived opportunities
with the shared scene-section refresh selection. The adapter source is a narrow
read-only handoff, not a universal scene schema; Revised A remains adapter-private.
CLI command guidance stays derived, including on choice-only refreshes. No scene
authority, encounter flag, narrative persistence, gameplay rule or save field is
added. Other locations and explicit preview/observation routes retain their
existing behavior. See [Scene Construction V1](scene_construction_v1_handoff.md) for verification and limits.

## Bounded Contextual Action & Consequence V1

`engine.contextual_action` proposes immutable `HandlingFrame` instructions for
declared stabilize, adjust and reposition methods, plus assessment and bounded
cooperation. It runs before investigation and legacy dispatch; specialized
interpreters still own their own language grounding. A proposal is not authority.
Inspection/possible repair is assessment, not commitment. Consequential handling
discloses method, risk and one-hour effort before contextual confirmation; execution
rechecks target, conditions, helper presence/refusal, restrictions and disclosure.

Routine preparation, elapsed-time effects, re-assessment, the supported d6 result
and material consequences share one validated candidate publication. If preparation
changes feasibility, its accepted effects/cost remain and the remaining action stops
without a draw. Unchanged completed attempts do not obtain a free redraw. Optional
`material_conditions` retain finite stability/fitting/position/integrity, cooperation
and causal references; one declared time development per target is supported.
Missing required material state is rejected on load, not reseeded. Save version is 1.

Engine-owned `ActionFocus` retains one unsaved focus/proposal; travel suspends focus
and changed basis invalidates authorization. Load/reset replaces that context;
accepted consequences remain in World State/history. The opt-in `--scenario market`
uses deterministic material scenes and observations; the independent archive fixture
uses the same production path. This is not general physics, repair, NPC planning,
inventory, conditional planning or a shared general interpreter. See the
[handoff](contextual_action_consequence_v1_handoff.md) and accepted
[structural correction](contextual_action_structural_correction.md).

## Bounded F05 activity control — owner accepted

`engine/activity_control.py` provides a deterministic continuation policy over
one caller-framed immediate purpose and chosen method. Explicit intent, limits,
available means, completion and owning-system developments determine whether to
continue or return control. Perceived increased discovery risk for a potentially
objectionable activity and independent consequential choices can return control
when the character has an opportunity to respond; routine or inaccessible
developments alone do not. Previously answered choices apply only by their
specific supplied reference.

The policy receives authority; it neither infers character access or coherent
natural-language intent nor authenticates its caller. It does not execute work,
advance time, roll, retain progress or store outcomes. Accepted resolution
references are opaque owning-system inputs: reuse and restart-required decisions
do not themselves perform a replay or fresh attempt.

The existing material-handling post-preparation checkpoint calls this policy
with its current feasibility assessment. Its candidate publication, one-hour
cost, prerequisites, draws, replay rules and save version remain unchanged.
Discovery/social/restart suppliers are stipulated in offline test fixtures;
general activity execution, NPC observation, inventory/perception systems and
playable F01–F05 integration are not implemented by this binding.

The ten situations in `test_fixtures/f05_activity_control.json` supply explicit
F01-compatible meaning, provenance and access. Structural compatibility is not
a live narration or semantic-fidelity evaluation. F01 runtime/instructions remain
unchanged. See the [coverage, verification and limitations](f05_implementation_preflight.md).
Owner accepted this bounded implementation on October 16, 2026 after Market
scenario review; see [acceptance and limits](f05_authorized_activities_v1_acceptance.md).
Discovery, dialogue, restart and broader playable integration remain outside this
package's implemented scope.

## Damaged-gate F01–F05 evaluation — accepted bounded integration

`engine/damaged_gate.py` is a standalone, unsaved evaluation session, reached
through `tools/play_damaged_gate.py`; ordinary campaign routes are unchanged.
Explicit bounded fixtures stand in for world circumstances, character competence,
means, guard cooperation and controlled resolution. Copied candidate state is
published only after F01 context construction succeeds. Accepted F05 policy
decides continuation, meaningful control return and conclusion. Accepted F01
realization receives supplied meaning, source, status, time, access and continuity;
provider prose never drives execution or state. F05 policy and F01 realization
mechanics remain unchanged; F01 instructions include the accepted correction above.
Routine repair steps run together; changed support needs return control
while accepted work/cost/result survive renewed authorization under current means.
There is no save/load API, general activity framework or upstream system claim.
The bounded interpreter now recognizes explicit bracing instructions in an already
started repair; unclear continuation leaves the new timber commitment undecided.
It reuses the existing F05 resumption path, not a new resolution mechanism. See
[interaction correction](f01_f05_interrupted_repair_correction.md).
See [implementation, validation and limits](f01_f05_gate_integration_v1.md).
The [final structural review](f01_f05_final_structural_reconciliation.md) records
a gate checkpoint-supplier omission: a recognized restriction conflict was checked
on initial execution but not repair resumption. The [SR-01 correction](f01_f05_sr01_restriction_correction.md)
now shares the same existing conflict tuple across both checkpoints. Restriction
semantics and accepted F05 policy are unchanged. The owner structurally accepted
this bounded implementation, including independent test-local activity validation
and API readiness tooling; see [acceptance](f01_f05_integration_v1_acceptance.md).

## Read-only Information Resolution Core V1a — accepted bounded implementation

`engine/information_resolution.py` supplies an independent immutable information
snapshot and storage-independent access operations over composed authored inputs,
supplied current/history records, relationships and binding constraints. Character
views require explicit owning-system access grants; internal constraint retrieval
includes hidden information. This module accepts supplied authority, authenticates
no source and adjudicates no outcome. It is not connected to production gameplay,
Region Packs, World State, F01/F05 or saves. See the [interface, verification and
limitations](information_resolution_core_v1a_handoff.md). Owner acceptance followed
final code-level review on October 21, 2026; the implementation remains uncommitted.

## Information-Grounded Adjudication V1 — owner-accepted bounded implementation

The October 22, 2026 [implementation handoff](information_grounded_adjudication_v1_handoff.md)
adds `engine/information_adjudication.py`, a disposable session consuming V1a's
public InformationAccess operations. Supplied authorized methods/capability/means,
retrieved facts and hidden bindings govern finite condition evaluation and existing
d6 mechanics. An offline untrusted proposal must match the owning assessment before
one publication of costs, time, retained obligations, ended bindings and safe history.
Technical rejection publishes neither state nor fictional failure. F05 controls
continuation/resumption; F01 receives only accepted accessible meaning. Later
interactions apply accepted endings/commitments without erasing earlier results.

The targeted inquiry correction supplies a read-only F01 response when F05 returns
control for inquiry about that character's accepted observation. It uses only the
safe historical observation and legitimately granted character facts, preserving
inference/report status and attribution; it does not query internal bindings,
execute an action or publish state. A mechanical draw preceding proposal validation
is provisional: rejection discards it, an explicit retry can sample again, and
only accepted attempts gain F05 result continuity. No pending-roll storage is added.

The owner accepted this implementation and inquiry correction on October 22,
2026 and authorized publication through the official strict fast-forward workflow.
Suppliers own relevance,
coherent supported terms, authorization, capability and legitimate character access.
The handoff defines the finite equality/group/effect semantics and their limits.
No general language/rules interpreter, production route, campaign state/schema,
save API, Region Pack or provider change is included. This follows the existing
damaged-gate disposable candidate pattern; conceptual authority remains unchanged.

## Context Loading

Do not read this file for every routine implementation turn.

Read it when:

- the current task affects an architectural boundary;
- ownership or persistence is unclear;
- the capability package explicitly references it;
- a material architecture conflict must be resolved.

For ordinary bounded work, use the current capability package, current sprint, and specifically named ADRs.

## North-Gate session working context

The CLI owns one optional `NorthGateDiscussion` per running session. Explicit
player commands accept a patrol-response focus with Elin; its record contains
only participant/focus, pending or suspended status, and at most four accepted
history references. It is not World State, narrator memory or save data.
Current public context, report receipts and action prerequisites are read afresh.
A copied source passes through existing local scene preparation/realization;
malformed adapters fall back to the deterministic focused text.

Travel/presence loss suspends the exchange; returning never automatically resumes
it. A successful ordinary conversation with Elin or the optional explicit resume
control revalidates Elin's presence, location and undecided response.
Existing predicates still adjudicate report sharing and decisions. An accepted
response concludes the immediate exchange, not the West-Road predicament.
Cancellation retires local focus without changing world records. Successful load,
reset and exit visibly interrupt it; failed load preserves it and saving alone
retains it. New processes start without unsaved agendas. Prose never establishes
local acceptance and structural validation makes no semantic fidelity guarantee.

Elin's bounded ordinary and focused dialogue share the same receipt-aware
projection. Zero/one/two receipts determine her acknowledgement and remaining
question; accepted phases use existing witnessed outcome responses. Unrelated
commands do not replay focus/status. Report exchanges receive current dialogue,
while suspension, resumption and conclusion are communicated at transitions.


## Bounded Contextual Investigation V1

`engine.contextual_investigation` interprets one survey, examination, supported
question or selective report into an immutable transient `ActionFrame`. A small
West-Road policy derives accessible candidates from current local traces, actor
presence and the initial inquiry phase. Candidates and copied focus are internal
selection data; presentation receives only sanctioned cues and existing qualified
results. A survey grants attention without acquiring findings or writing history.

The engine revalidates stable target identity, method, restrictions and recipient
before dispatching to selected `investigate`, the supported Mara account, or
existing `present_clue` transactions. Selected acquisition is independent of
content order and replays only that finding. Simulation retains discovery,
history, recipient knowledge, costs and decision authority. Interpretation never
runs a list of legacy commands or chooses a consequential branch.

One unsaved focus holds a frame, location and at most four subject/event references.
Travel suspends it; resumption and new input recheck current subjects and execute
nothing automatically. Successful load/reset and exit retire it; failed load keeps
it. Findings and receipts remain in existing owners. Save version 1 and its shape
are unchanged. The test-only depot supplies a second concrete policy through the
same engine seam; no production region, registry or saved lead structure is added.

## Durable consequential runtime — owner-accepted bounded implementation

The explicit I3 campaign configuration extends the existing GameEngine →
Coordinator → consequential Runtime.accept path. One prepared root couples domain
state, declarative Information Foundation inputs, undertaking progress and receipt
recognition with World State and its derived scene. World/Character/Action/Actor
owners retain their semantics. Legacy I2 remains memory-only; default gameplay
and version-1 persistence retain their existing behavior.

campaign_records defines a finite, non-executable record vocabulary; campaign_continuity
validates reference closure, accepted mechanics/costs/time/effects/progress and safe
receipt meaning, and prepares complete roots. Authoritative elapsed time is integer
seconds. Trusted owners supply current input/checkpoint changes; initial and resumed
increments enforce F05 and fresh dependencies. Waiting retains duration-or-condition
intent without a general waiting executor or scheduler.

Version-2 saves place the continuing-gameplay section inside World State. The writer
validates/encodes before a same-directory flushed/fsynced atomic file replacement.
GameSession builds an independent validated engine before a single adoption. Load
never draws, adjudicates, advances time or replays consequences. Version-1 promotion,
unsupported legacy scenario time owners and material content revisions fail closed.
Historical bases contain selected accepted premises; diagnostics remain private,
bounded and non-authoritative. Pending permits and generated/private presentation
contexts are rebuilt, not serialized.

See [ADR-062](decisions.md#adr-062--opt-in-durable-consequential-campaign-continuity)
and the [I3 implementation handoff](i3_m1_handoff.md) for supported boundaries and
compatibility/recovery evidence. The owner accepted the bounded implementation October 24, 2026; Git publication remains separately authorized.
