# Player Presentation — Design Manifest

## Status

- Overall: **Partial** — a working CLI receives commands and displays bounded
  scenes, opportunities and results; discoverability, safe display and recovery
  are uneven across routes.
- Last materially reviewed: October 6, 2026, protected baseline
  `56baf51a26c2ca2effeb098b78937bd381e28304`.
- Current documentation review candidate. Relevant milestones:
  [10.77 presentation](../../sprint_10_77_handoff.md),
  [10.78 competence](../../sprint_10_78_handoff.md),
  [10.79 local consequences](../../sprint_10_79_handoff.md), and
  [10.80 ordinary player route](../../sprint_10_80_handoff.md).

This living model uses the [shared framework and vocabulary](README.md).
It authorizes no runtime, parser, help, content, persistence or provider changes.
The seven protected manifests retain their boundaries. Repository lifecycle
remains idle; this standalone documentation task selects no capability package.

## Purpose

Own the interaction surface between the human player and the game: receive
intent, make supported play legible, and surface narrative, result and operational
feedback. Preserve the distinction between what the player can type or see and
what the owning game systems establish as true or consequential.

## Player-facing goal

Understand the current situation, discover supported interaction, make an
informed choice, and understand what happened and what remains possible.
Recoverable input or technical problems should leave an understandable way to
continue. A suggested opportunity should help the player choose without choosing
for them or promising success.

## Authority

Own interaction grammar, normalization, aliases, routing mechanics and prompts;
display placement, section structure, spacing and mechanical refresh; and the
surface for supplied choices, results, costs and status/error messages. These
are conceptual responsibilities across terminal, desktop, web or other surfaces,
not permanent CLI architecture or a proposed GUI.

Presentation can map a supported command form to an operation and request its
execution through the engine. Owning gameplay systems determine applicability
and execute it. Projection can join already supported facts and reuse owning
predicates to derive affordances; it must not establish a separate eligibility
policy or epistemic authority. A displayed option never grants an outcome.

Narrative Experience selects and frames expressive content and its meaning.
Presentation arranges how that content reaches the player. Choosing to print a
result before a scene is display sequencing; choosing which consequence matters
or how an actor's report should be understood is narrative selection/framing,
subject to gameplay truth and character access. Current code mixes these concerns
in `GameEngine`, projection helpers and the CLI without settling module boundaries.

Simulation authority and fail-closed providers are existing contracts. The
decomposition below and broader presentation direction are revisable design.

## Explicit non-authority

Presentation cannot establish world facts, character knowledge/capability,
fictional success or costs, NPC willingness/intentions, time passage, scenario
progression, or accepted consequential change. It cannot repair an unavailable
action, infer successful discovery from detailed observation, or invent narrative
content to fill a display. Save/load commands do not own storage semantics.

The human controls protagonist intent. Suggested or prominent options do not
authorize automatic commitment, disclosures, purchases, threats or other
meaningful choices. Display caches, omission and technical transitions neither
advance fiction nor erase retained information. Provider prose has no mutation
path into simulation; acceptance for display does not certify factual prose.

## Governing principles

Apply the [shared doctrines](README.md#shared-doctrines),
[Simulation Principles](../../simulation_principles.md),
[Simulation Model](../../simulation_model.md),
[Story-First Part I](../../story_first_design_doctrine.md#part-i--established-design-doctrine),
and ADR-027–033, 049–051 and 055–061 in the [decision ledger](../../decisions.md).

- **Input is intent, not truth.** Assumptions inside player wording require an
  authoritative basis; `search the burned inn` establishes neither a fire nor a
  discovery. The current broad observation route sends that wording as focus.
- **Eligibility precedes executable affordance.** Reuse supported owning-system
  predicates where practical, and revalidate on execution. Advisory text need
  not be an exact command or a guarantee that a social request will be fulfilled.
- **Presentation does not adjudicate.** Parser acceptance, supported execution,
  accepted fictional failure/partial/full result, and unchanged state differ.
- **Explain material choice consequences.** Preserve supplied cost, uncertainty,
  evidence limits and meaningful alternatives. Immersion does not require hiding
  an intentional one-hour cost or the command needed to act.
- **Keep internal identifiers internal in ordinary play.** Display useful names
  and qualified meaning rather than phase/discovery/actor IDs or status tags.
  Current diagnostics and raw dice options are explicit implementation limits.
- **Technical failure stays technical.** Parser rejection, provider failure and
  file errors are distinct from a resolved fictional failure.
- **UI state is not world state.** Formatting, suppression and continuity hints
  have no fictional authority; persistent truth need not be mentioned every turn.

These principles synthesize existing authority, agency and comprehension direction.
They do not claim every current route satisfies the intended experience.

## Current model

Three **Provisional** responsibilities are sufficient; no new modules or general
screen/interaction state machine are implied.

| Responsibility | Question and present grounding |
|---|---|
| Input and intent capture | What did the human request, and which supported route receives it? CLI control commands, bounded kernel grammar and explicit engine scenario dispatch exist. General natural-language action interpretation does not. |
| Interaction projection | What supplied state, operations and choices help the player act now? Safe names/exits, advisory contextual actions, retained clues and exact West-Road choices exist. General discovery, access and visibility policy remain incomplete. |
| Feedback and display | How should narrative, results, costs, errors and status be surfaced coherently? Scene sections, result printers, recap placement and mechanical refresh suppression exist. Unified feedback/recovery and richer presentation remain incomplete. |

Intent capture does not frame or adjudicate a novel consequential attempt.
Interaction projection does not choose actor cooperation or informational access.
Feedback/display does not select narrative meaning. Each consumes the appropriate
owner's accepted material even when functions are presently co-located.

## Resolution depth

Use the [Specificity Doctrine](README.md#specificity-doctrine) for sufficient
interaction detail: orientation, then detail warranted by attention, a choice,
accepted consequence or transition. A repeated look can deepen ordinary
description without creating significance or discovery. A meaningful cost or
unsupported operation may need explicit feedback even in restrained prose.

Do not turn inference → lazy resolution → persistent state → active simulation
into a UI-state storage ladder. Greater focus does not justify menus for every
noun, a transcript ledger, persistent display history or automatic player choices.
Current stages help narration; they are not a general progression mechanic.

## State and lifecycle

| Kind | Present behavior and authority |
|---|---|
| Interaction loop | `main()` starts a new engine, prints introductory help guidance, and reads stripped text synchronously. Control commands continue the loop; quit/exit end it. No modal choice queue or automatic choice exists. |
| Display bookkeeping | `last_presented_narration` compares complete deterministic narration dictionaries. `scene_player_input` and `scene_stage` supply subsequent presentation focus/stage. These variables are ephemeral and not saved. |
| Current-scene descriptive continuity | `SceneContinuity` holds location, prior accepted-for-display sentence excerpts and previous conditions: at most 24 excerpts, 4,000 characters each and 8,000 total. It preserves initial orientation plus recent detail; it is neither verified truth, character memory nor a transcript. |
| Fictional/persistent state | Engine-owned location/time, discoveries, reports, phase, competence and accepted attempts have their gameplay owners and existing saves. Projection and display do not alter their semantics. |

`SceneContinuity.enter` clears descriptive memory when location changes; successful
load/reset clears it explicitly. Empty memory forces `orient`; broad look normally
uses `expand`, focused observation/intention `follow`, and conversation `narrow`.
Only accepted narration is remembered. An unavailable provider result adds no
descriptive claim. Process restart retains none of this presentation memory.

First display and material deterministic scene changes show a scene; identical
deterministic output suppresses automatic redisplay. Explicit observation/intention
still calls narration even when that dictionary is unchanged. This is mechanical
suppression, not semantic comparison of generated language. After unavailable
automatic market narration, the loop still records the deterministic dictionary
as last presented; it does not automatically retry unchanged scenes. `look` can
request another call. Neither suppression nor retry changes fictional state.

Successful load prints status, then supplied `Previously:`, then refreshed scene.
Reset requests an intentional fresh game and refreshes; a cache reset by itself
does not reset fiction. Failed caught load preserves the running session/cache.
Re-entry reorients rather than restoring a saved location prose record.

## Inputs

- Raw human text, stripped by the CLI; lowercased copies for routing while original
  wording reaches descriptive context. Input assumptions remain untrusted.
- Supported engine results, locally derived perception/scene projections,
  navigation cues, eligible approaches and accepted outcome/cost material.
- Character capability/access constraints and retained clue title/text surfaces;
  world conditions and actor presence arrive through supported engine interfaces.
- Authored names, labels, replies and option material with supported interpretation.
  Arbitrary authored wording is not executable UI behavior.
- Accepted narration packets, operational status/errors and resume summaries.
  Provider infrastructure remains behind the narration boundary in ordinary play.

## Outputs

Declared intent or a requested supported operation to the engine; descriptive
focus/stage and untrusted continuity hints to Narrative Experience; and displayed
scene, opportunities, results, retained information, costs and technical status.
No authoritative world mutation, outcome, knowledge grant or actor decision is an
output of this responsibility. Current APIs can return internal metadata that
ordinary printers ignore; merely receiving it does not authorize disclosure.

## Relationships

See the [Player Presentation information flow](system-map.md#dependencies-and-information-flow-around-player-presentation).

| System | Interface and ownership retained elsewhere |
|---|---|
| [World Simulation](world-simulation.md) | Supplies supported local state, route execution and consequences. Presentation names destinations and displays travel/arrival; it does not move the character, advance time or establish external truth. |
| [Character System](character-system.md) | Supplies capability/access and retained information. Presentation exposes supported views and clues without granting knowledge, certifying a report or reacquiring it. |
| [Action & Resolution](action-resolution.md) | Receives declared intent/requested operation; supplies eligibility, approaches, costs and accepted results. Labels and parser `success` do not adjudicate. General action-framing interfaces remain provisional. |
| [Actors & Social Dynamics](actors-social-dynamics.md) | Supplies accepted behavior/reports and supported interaction. Targetability permits requesting conversation, not guaranteed willingness, disclosure or cooperation. |
| [Narrative Experience](narrative-experience.md) | Receives focus and ephemeral presentation context; returns selected/framed expression. Semantic relevance and repetition policy belong there; section placement and redundant redisplay mechanics belong here. |
| [Scenario & Authored Content](scenario-authored-content.md) | Supplies supported names, labels, clues and choices. Engine interpretation establishes applicability; text alone adds no command or consequence. |
| [Persistence](persistence.md) | Receives explicit save/load/reset requests and returns success/failure/restored session. Presentation displays status and reorientation; it does not validate storage compatibility or invent restoration. |
| Narrator Provider / Model Adapter | Normally reached through Narrative Experience, not interpreted directly by presentation. Unavailability is a technical presentation failure; configuration, retries and fallback policy are not chosen by this manifest. |

## Player-facing projection

### Input, declared intent and executable operation

Three distinctions are useful without prescribing three runtime objects:
an interface command controls interaction/session behavior; declared fictional
intent expresses what the human wants; a recognized executable operation has a
supported engine path with its own prerequisites. Recognition alone is not
successful execution. A text command may contain both control syntax and intent.

| Current route | Actual meaning and limit |
|---|---|
| `help`, save/load/reset, quit/exit | Exact normalized CLI commands invoke supported interface/session operations. Startup does not auto-load; quit does not save. Paths are fixed in the CLI. |
| `go`/walk/move/travel/enter/leave forms | Keyword classification plus bounded direction/name extraction proposes movement. Engine validates/executes supported graph hops. This is no general language or spatial-intent parser. |
| `head to <place>`, `go to <place>`, `move to <place>` | Immediate named connections can execute movement. Non-immediate `go to`/`move to` use a shortest authored graph route; non-immediate `head to` identifies a loaded-region destination without traveling. The help's blanket nontravel description of `head to` is inaccurate. |
| `look`/inspect/examine/search/study | Broad observation retains original text as narration focus; the structured action has no resolved object target. It neither investigates traces nor adds discovery/time by itself. Successful observations use the provider boundary at any location, unlike automatic non-market scene display. |
| First-person `I walk/move/wander/stroll through/around/about/among/along ...` | Narrow pattern routes descriptive within-scene intention to narration. It changes no position, time or consequential state. Explicit navigation remains separate; arbitrary descriptive intention is not generally supported. |
| `investigate`, `search for clues` | Distinct deterministic local discovery operation: first eligible undiscovered authored declaration with a present matching trace. Exhaustion is an accepted no-op. This differs from broad `search ...` observation. |
| talk/speak/ask/greet/tell forms | Request a bounded current-scene conversation target. There is no general dialogue-topic or freeform speech interpretation. Authored/scenario replies and effects follow engine rules. |
| `clues`/`known clues`, `present <title> to <actor>` | Recall retained information or request supported sharing/presentation. Recall uses declaration order and does not reacquire clues; exact case-insensitive clue title and local actor matching constrain presentation. |
| Six fixed West-Road choices; three competence operations | Exact stripped/lowercased command dispatch precedes the generic kernel. Eligibility, time, phase change and accepted result are engine-owned; the UI selects none automatically. |
| `check <name>`; take/grab/open/close/use/push/pull | Check is a constant-result scaffold, not character competence. Generic actions can return acceptance/attempt text without object or inventory mutation. They do not prove playable open-ended execution. |
| Empty/unrecognized text | Empty input rejects with a message; unknown input reports that the player is unsure how to do it. Help's “Any other input” wording does not establish general natural-language support. |

Kernel classification has precedence and checks words/prefixes, not full semantic
understanding. Movement direction extraction uses substring matches with fixed
aliases (including inside/outside); ordinary whitespace/case handling varies by
helper. Immediate route matching uses normalized authored display names; named
graph routing chooses fewest hops with authored connection order as tie-break.
Destination identification separately normalizes punctuation/articles and uses
exact aliases before single-word alias matches. Scene target resolution normalizes
case, underscores and whitespace, then exact aliases before whole alias words;
ambiguity is not fuzzy disambiguation. Conversation extraction special-cases
`guard`/`captain`, otherwise strips an initial verb and optional `to`. These are
bounded matching conveniences, not a general natural-language parser.

### Discoverability, choice and transparency

Contextual action projection reuses investigation and clue-presentation predicates,
visible uniquely resolvable static actors, West-Road availability and competence
assessment. It emits advisory prose in fixed construction order: speaking,
investigation, clue presentation, legacy conversation hint, fixed choices and
competence approaches. Current legacy affordance exposes a command separately,
but deterministic scene formatting uses its display text. Execution checks current
conditions again; stale displayed opportunities have no retained authority.

At relevant gate/road scenes, deterministic narration groups exact choices under
`What now?`, followed by compact `Other actions` and routes. Evidence/report hints
guide prerequisites when choices are unavailable. Text compaction consumes derived
opportunities; it does not determine eligibility. Narrative emphasis cannot make
a suggested option mandatory, successful or the only possible player intention.

Help exposes session controls, clue use, named travel and fixed choices, but omits
broad look/observation, ordinary conversation syntax, directional movement, the
three competence commands and several aliases. Local actors/routes and exact
competence choices help compensate; no universal discoverability guarantee exists.
Automatic Market Square provider display prints only title and accepted prose,
not the deterministic navigation/opportunity arrays or `What do you do?` prompt.
Their presence in internal packets is not proof they reach that display.

Initial West-Road choices explicitly show one-hour cost and allocation/exposure
tradeoffs. Competence options show hours, uncertainty or committed guard assistance,
and raw ordinary/specialist d6 bands. Accepted results pay their established cost
even on failure; partial information remains qualified. No general resource-use,
travel-cost preview or uncertainty explanation is implemented. CLI prints singular
`time_advancement` deltas after actions; multi-hop results can carry plural
`time_advancements`, which the loop does not print as an aggregate. Engine costs
still apply. Hiding route-hop chatter must not be mistaken for waived cost.

Meaningful cost/uncertainty should remain understandable. Existing raw dice bands
are a **current implementation tension** with the Narrative Experience direction
to avoid internal mechanics in ordinary prose, not a new accepted UI design.
Status tags in competence packets are not printed as such; the separate diagnostic
check command intentionally displays its constant result/difficulty.

### Feedback, transitions and safe information

`print_narration` owns the scene header, title/description spacing and optional
prompt. Deterministic composition supplies local description, weather, presence,
routes, opportunities and scenario framing. Provider-backed presentation supplies
accepted prose and a location title. Narrative Experience owns that wording and
semantic selection; the UI owns how the resulting sections appear.

The loop prints authored replies, discovery text, clue recall/presentation and
operation messages before the next material scene refresh. Fixed choice feedback
prints the player's chosen command instead of the engine's long outcome/reply
message; the refreshed deterministic scene carries current circumstances. Rejected
fixed choices prefer the current choice hint. Competence feedback uses accepted
outcome text, with costs from the engine; its `success=True` can accompany
`accepted_outcome.result="failure"`. No new clue and already accepted replay are
different no-op meanings. General `success`/`changed` flags are not a universal
feedback taxonomy, and parsed clue presentation may still return unchanged.

Routine completed multi-hop messages consisting solely of `You move ...` become
one destination sentence. Failed or nonroutine messages remain intact. Compression
changes output only: hops execute sequentially and have no whole-route rollback
guarantee. Arrival/re-entry shows the destination scene; local consequences appear
only when established and legitimately projected. A suppressed scene changes no
world state, and semantic repetition guidance remains with Narrative Experience.

Retained `clues` show authored titles/text even away from the originating scene.
Local scene omission does not delete them. Review is remembered information,
not proof it is still current or objectively true; no aging/staleness display
mechanism exists. `Previously:` is engine-derived, chiefly phase/discovery/report
based, and precedes the post-load scene. It is not exact replay of generated prose
or a complete cost/attempt summary; its route-found wording can blur survey versus
following, as already recorded by Narrative Experience and Persistence.

Clean scene/navigation/contextual projections use names, labeled groups and text,
excluding supported hidden identifiers/fields. Printers can receive discovery IDs,
history references, target identifiers or competence status metadata without
displaying them. They should consume safe interfaces rather than independently
read raw state and decide character entitlement. Current engine projection uses
world/content predicates; that shared implementation does not give presentation
an independent knowledge model.

**Partial safety:** provider context still contains the fuller scene snapshot;
structural output checks do not prove prose factuality. Generic deterministic
entity formatting can derive a label from an ID. Explicit `pressures`, `history`,
history/narration context and preview/contract diagnostics expose internal IDs,
schema/status/error material through the same CLI/help. They are not a uniformly
character-safe journal or ordinary-play information contract. Naming that gap
does not authorize removing diagnostics or filtering truth in the UI.

### Errors and failure semantics

| Situation | Current feedback/recovery and meaning |
|---|---|
| Parser/target rejection | Missing movement/check/presentation arguments, invalid route and ambiguous/absent named conversation target have bounded messages. Unknown text does not resolve a fictional attempt. Missing conversation target can still be accepted as a no-op and print conversation text or trigger market narrowing; no consistent missing-target prompt exists. |
| Gameplay unavailability | Owning prerequisites reject fixed decisions/competence operations; CLI can display a current choice hint or supplied reason. No roll is required to reject an unsupported attempt. |
| Accepted fictional failure/partial result | Competence outcome text reports the finding limits; supplied time still applies. Command acceptance is not victory, and failure is not a provider outage. Other approaches and ordinary continuation can remain. |
| Provider/configuration/network/validation failure | Ordinary scene path reports narration unavailable and suggests `look`. It omits grounding, raw errors and rejected candidate prose; no rich automatic fallback/model switch/retry loop exists. The command loop can continue. A preceding gameplay operation remains committed; narration failure does not roll it back or turn it into fictional failure. |
| Persistence failure | Missing load reports no save; caught `ValueError` prints the load error. Success status follows engine completion. CLI exposes no filename arguments, so malformed user save paths are not an implemented input case; engine callers can supply paths. Storage/restoration failures belong to Persistence. |
| Other infrastructure/internal failure | Startup, save/reset, load errors outside the two caught types, and ordinary command exceptions lack a uniform recoverable display boundary. EOF/keyboard interruption has no dedicated loop handling. Diagnostics and tracebacks may reach the terminal; a friendly-error guarantee is absent. |

Basic headings, readable names, explicit hints, UTF-8 stdout configuration and
some recoverable messages are **Implemented** ergonomics. No evidence establishes
a broader accessibility program, screen-reader audit, localization, configurable
contrast or graphical interaction system. Record legibility/recovery limits
without inventing such a program.

## Current implementation

| Capability | Classification and evidenced limit |
|---|---|
| Input/routing | **Partial:** exact CLI controls, keyword kernel, aliases/target matching and explicit scenario bypasses work. Generic action acceptance and descriptive focus do not supply general executable intent. |
| Opportunity/choice display | **Implemented, bounded:** read-only local opportunities and exact eligible West-Road/competence commands; stale affordances revalidate. **Partial** discoverability across help and provider displays. |
| Results and mechanical transparency | **Partial:** supplied outcome text, clue acquisition/recall, choice hints and explicit costs; mixed acceptance/no-op flags, raw dice, route-time reporting and scaffold language remain uneven. |
| Scene/narration integration | **Implemented, bounded:** deterministic non-market automatic scenes, provider-backed market automatic scenes, successful observation/intention at any location and market conversation narrowing. No universal narrative/display pipeline. |
| Refresh/continuity | **Implemented, bounded:** deterministic dictionary equality suppression, scene stages/cache, load/reset/re-entry reorientation and routine hop compaction. Semantic suppression and persistent presentation memory are absent. |
| Failure/status surfaces | **Partial:** selected parser/load errors and narration-unavailable feedback; no complete infrastructure recovery or fallback experience. |
| Information safety | **Partial:** clean projections and selective printing exist; fuller provider snapshots and explicit diagnostic routes prevent a blanket safe-display claim. No independent presentation epistemic authority. |
| Interface portability | **Provisional:** responsibilities remain meaningful beyond CLI; commands/print functions are current evidence, not a selected future UI framework. |

## Accepted decisions

Simulation authority, fail-closed providers, character access limits, player agency,
minimum sufficient detail, and fictional continuity independent of technical
boundaries are existing direction. ADR-049–051/057 establish bounded acquisition,
presentation and advisory affordances; ADR-055/059 distinguish executed travel
from orientation; ADR-060/061 establish explicit scenario choice and competence
semantics. Accepted 10.77–10.80 evidence supports concise choice/result orientation,
local relevance, progressive attention and routine travel compaction. These are
bounded mechanisms, not approval for general parsing, a GUI or hidden choices.

## Provisional decisions

The three-part responsibility model and cross-interface realization remain working
concepts. A clearer surface distinction among control commands, descriptive intent
and supported operations may improve comprehension; no parser redesign, universal
result schema or new prompt is selected. How much mechanics to expose, how to keep
provider scenes discoverable, and how to separate diagnostics from play require
player evidence and future owner-authorized scope.

## Deferred capabilities

General natural-language intent/action parsing, interactive menus, GUI/web/mobile
implementation, save slots/autosave, retry orchestration, richer fallback narration,
unified error/result frameworks, durable UI memory, semantic repetition detection,
general knowledge/staleness display and broad accessibility infrastructure.
Previously deferred broader presentation refinement remains unscheduled. This
manifest neither implements these nor selects the next package.

## Known tensions / open questions

- **Help versus execution:** immediate `head to` travel contradicts its help
  description; broad input wording overstates supported play. Missing ordinary
  syntax and competence commands limit learning without repository knowledge.
- **Accepted versus accomplished:** generic actions and targetless conversation
  can sound successful without execution. What smallest feedback distinction makes
  acceptance, no-op, unavailable operation and fictional result understandable?
- **Affordance visibility:** deterministic options are eligible/advisory, while
  provider market display does not render those structures separately. How should
  supported interaction remain discoverable without requiring invented prose?
- **Transparency balance:** explicit costs/alternatives aid informed choice;
  raw d6 bands expose rules that ordinary narrative direction seeks to hide.
  Multi-hop cost feedback is incomplete. Reconcile the experience with owner
  evidence rather than removing useful cost information by default.
- **Safe display versus diagnostics:** clean projections do not make every CLI
  or provider input character-safe. Topology-based destination identification has
  no general familiarity gate. Eligibility/access remain owning-system concerns.
- **Failure orientation:** fail-closed generation leaves sparse orientation and
  no automatic retry on unchanged scenes. File/internal exceptions are unevenly
  handled. Neither issue justifies fictional failure or UI repair of gameplay.
- **Continuity and recap:** remembered prose can reinforce an unsupported claim;
  reset/re-entry loses it, and phase recap can blur the exact operation. Narrative
  fidelity belongs to Narrative Experience, placement/reset mechanics here.
- **Historical wording drift:** architecture and ADR-058 retain preview-only/
  no-normal-gameplay descriptions; accepted 10.80 CLI routes invoke the provider.
  Older help also calls preview fixed. Narrative Experience already records this
  drift and the older incidental-detail restrictions; protected records are not
  rewritten in this bounded review.

No new contradiction among the seven protected ownership manifests requires
changing them. The concrete help mismatch and historical architecture/provider
wording conflict with evidenced runtime descriptions; they are reported limits,
not resolved by transferring fictional authority or silently changing behavior.

## Evidence

Source, test assertions and design records were inspected at the stated baseline.
Tests below establish existing coverage; no gameplay/test suite or live provider
was run for this documentation task. Handoff verification and owner acceptance
are historical evidence, not fresh runtime certification.

| Evidence | Supports |
|---|---|
| [Framework](README.md), [template](system-manifest-template.md), [map](system-map.md), seven manifests linked above | Shared structure/status, preserved ownership and final presentation boundary |
| [Architecture](../../architecture.md), [principles](../../simulation_principles.md), [model](../../simulation_model.md), [Story-First](../../story_first_design_doctrine.md), [ADRs](../../decisions.md) | Truth/access/intent, minimum detail, agency, meaningful uncertainty and historical wording drift |
| [CLI](../../../play_game.py), [kernel](../../../engine/interaction_kernel.py), [target resolver](../../../engine/target_resolver.py), [destination resolver](../../../engine/destination_resolver.py), [GameEngine](../../../engine/game_engine.py), [world update](../../../engine/world_update.py) | Actual dispatch, bounded matching, execution versus scaffold, result order, help, session/status/errors and travel compaction |
| [Eligibility](../../../engine/action_eligibility.py), [contextual projection](../../../engine/contextual_action_projection.py), [conversation affordance](../../../engine/conversation_affordance.py), [navigation](../../../engine/navigation_projection.py) | Reused owning predicates, advisory wording, construction order, safe names and independent revalidation |
| [Scene projection](../../../engine/current_scene_projection.py), [scene narrator](../../../engine/scene_narrator.py), [West-Road presentation](../../../engine/west_road_presentation.py), [competence](../../../engine/character_competence.py) | Clean display structures, deterministic content, choice grouping, compaction, limited outcome layers and raw dice options |
| [Scene Context](../../../engine/scene_context.py), [continuity](../../../engine/scene_continuity.py), [narration context](../../../engine/narration_context.py), [pipeline](../../../engine/narration_pipeline.py) | Untrusted focus/claims, stages, bounded cache, fuller provider snapshot, validated display and technical failure |
| [Player route tests](../../../test_player_scene_route.py), [presentation tests](../../../test_west_road_presentation.py) | Real patched CLI loop: orient/expand/follow/narrow, all-location observation boundary, no-op suppression, outcome refresh, recap ordering, rejected-output exclusion and nonroutine message preservation |
| [Kernel tests](../../../test_interaction_kernel.py), [navigation tests](../../../test_navigation_projection.py), [contextual tests](../../../test_contextual_action_projection.py), [projection tests](../../../test_current_scene_projection.py) | Route matching/tie-break, eligibility filtering, read-only projection, redaction and stale-opportunity rejection; several use the test-only legacy fixture |
| [Discovery tests](../../../test_discovery.py), [save/load tests](../../../test_save_load.py), [locality tests](../../../test_west_road_scene_relevance.py) | Authored acquisition/no-op and Unicode printing, restoration, retained clues separate from scene locality |
| [10.77](../../sprint_10_77_handoff.md), [10.78](../../sprint_10_78_handoff.md), [10.79](../../sprint_10_79_handoff.md), [10.80](../../sprint_10_80_handoff.md) | Recorded owner acceptance of explicit choices/competence, correction of remote scene leakage, and final live arrival/look/browsing progression with minor storm repetition accepted |

The final 10.80 acceptance records the three-command owner sequence and findings;
it is not a comprehensive transcript or proof of universal quality/accessibility.
No unrelated narrator evaluation, credential tooling or owner save is evidence
required by this review.

## Revision history

- October 6, 2026: initial Player Presentation review candidate; reconcile actual
  input/display routes with owning-system authority, expose discoverability and
  feedback limits, and distinguish semantic narration from display mechanics.
