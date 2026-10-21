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

## Tech Stack

- Python 3.13
- CLI gameplay interface
- JSON Region Packs for authored world content
- Version-1 World State saves
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
Contextual material action → contextual investigation → legacy fallback
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
