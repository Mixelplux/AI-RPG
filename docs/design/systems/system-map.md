# System responsibility and relationship map

Reviewed October 5, 2026 at `51f595b5c8516ef242a4fffeb246c0e143acc9b3`.
This is the current conceptual ownership model, subject to evidence and revision.
It is neither a call graph nor a list of runtime modules. See the separate
[runtime architecture](../../architecture.md) and [shared doctrines](README.md).
The World Simulation baseline is preserved. [Character System](character-system.md)
was reviewed October 6, 2026 at documentation baseline
`89f135834eb85cb995facb0b7126a3c5f58b7a6a`.
[Action & Resolution](action-resolution.md) was finalized October 6, 2026 at
accepted milestone `63f1a3db8b8996efe0f8245ad21d22ddb234dcbc`;
[Actors & Social Dynamics](actors-social-dynamics.md) was finalized October 6,
2026 at accepted milestone `ecd3ed246a8c989990d1411582438b58369d3c84`;
[Narrative Experience](narrative-experience.md) was finalized October 6, 2026
at accepted milestone `da362a53a704c27709a137b1d0e363368b49a044`.
[Scenario & Authored Content](scenario-authored-content.md) has an October 6,
2026 review candidate based on protected baseline
`da362a53a704c27709a137b1d0e363368b49a044`.
Persistence and Player Presentation have no manifests yet.

## Responsibility hierarchy

| Group | Systems and responsibilities |
|---|---|
| Core Gameplay | **World Simulation:** external reality and legitimate change. **Character System:** character capability, perspective, and memory. **Action & Resolution:** adjudication of attempted action. **Actors & Social Dynamics:** meaningful intentional NPC/faction decisions. |
| Experience | **Narrative Experience:** selective, context-aware expression of authoritative truth and outcomes, preserving epistemic meaning and continuity. **Player Presentation:** player input/display and interaction surface. |
| Content | **Scenario & Authored Content:** authored foundations, constraints, and bounded declarations. |
| Cross-Cutting | **Persistence:** durable storage, restoration, and compatibility. |
| Supporting Infrastructure | **Narrator Provider / Model Adapter:** untrusted model transport and adaptation. **Verification / Evaluation:** evidence and checks. **Runtime / Tooling:** execution and development support. |

Storage in `world_state` does not transfer all conceptual ownership to World
Simulation. `GameEngine` currently orchestrates multiple responsibilities. The
hierarchy does not require splitting either into new modules.

## Dependencies and information flow around World Simulation

| From → To | Information / dependency | Current status |
|---|---|---|
| Scenario & Authored Content → World Simulation | Initial weather/time, macro locations/connections, authored constraints and effect declarations | Implemented for supported Region Pack fields; broader authoring interfaces provisional |
| Player Presentation → Action & Resolution → World Simulation | Declared intent, validated interactions, accepted external consequences | Implemented bounded engine path; a general action model is unsettled |
| Character System → Action & Resolution | Capability and recognition affect applicable actions and resolution | Implemented bounded West-Road competence; broader interface provisional |
| World Simulation → Character System | Observable world facts constrain perception and access; world truth alone does not grant knowledge | Partial: existing perception/discovery boundaries; ordinary lived familiarity remains design direction |
| World Simulation ↔ Actors & Social Dynamics | Circumstances inform intentional decisions; executed actions return external consequences | Provisional conceptual interface; declared relocation/report effects are implemented, autonomous decisions are not |
| World Simulation → Narrative Experience → Player Presentation | Local facts, conditions, and safe outcomes become scene context and expression | Implemented bounded projections and Sprint 10.80 context; generalized context selection deferred |
| Narrator Provider / Model Adapter → Narrative Experience | Untrusted candidate expression through validated, fail-closed boundaries | Implemented narration path; no reverse authority flow into simulation |
| World Simulation ↔ Persistence | Validated runtime state saved/restored; scenes rebuilt from state plus content | Implemented version-1 envelope; storage atomicity limitation in manifest |
| Verification / Evaluation, Runtime / Tooling → supported systems | Checks and execution support | Infrastructure relationships, not fictional authority |

The World Simulation manifest describes its [inputs, outputs, and
relationships](world-simulation.md#inputs). This map leaves future interfaces
open rather than designing the other systems prematurely.

## Dependencies and information flow around Character System

The [Character System manifest](character-system.md) refines capability,
perspective, and memory into capability/constraints, informational access, and
selective retention/continuity. This working decomposition remains provisional.
World Simulation supplies what exists and its externally observable properties;
Character System supplies character-specific capability, perspective, and
constraints or basis relevant to access. Accessible views may be derived jointly
from both rather than independently established by Character System.

| From → To | Information / dependency | Current status |
|---|---|---|
| Scenario & Authored Content → Character System | Supported seeds, evidence descriptions, clue/report text and bounded interpretation declarations | Implemented bounded slices; biography/profile/familiarity interfaces provisional |
| World Simulation → Character System | What exists and its externally observable properties, including position, local evidence, and conditions | Partial: accessible views depend jointly on world conditions and character-specific constraints; ordinary lived familiarity remains design direction |
| Character System → Action & Resolution | Authoritative competence, limited recognition and retained information relevant to attempts | Implemented West-Road slice; capability does not adjudicate outcomes or create evidence |
| Action & Resolution → Character System / World Simulation | Accepted findings and attempts preserve character continuity; external consequences update world truth | Implemented fixed atomic candidate path; attempt records span responsibilities |
| Character System ↔ Actors & Social Dynamics | Individual informational access constrains intentional decisions and reports | Provisional general interface; static-actor membership and declared sharing/responses are bounded implementations |
| Character System → Narrative Experience / Player Presentation | Character-specific capability, perspective, and access basis inform the jointly derived safe view, reports, recognition/findings, and retained clue review | Partial: current local views also depend on world conditions; narration cannot establish or expand informational access |
| Character System ↔ Persistence | Validated supported competence, discoveries, actor membership and attempt continuity | Implemented version-1 slices; no general character identity/replacement or belief storage model |

These relationships neither relocate fields out of `world_state` nor prescribe
new module boundaries. Player intention remains external input; session-only
presentation continuity has no authority over persistent character state.

## Dependencies and information flow around Action & Resolution

The [Action & Resolution manifest](action-resolution.md) uses three provisional
responsibilities: frame an executable attempt, determine outcome/cost, and commit
and preserve the accepted result. These describe conceptual authority, not a new
pipeline or module split. Acceptance of a command differs from fictional success.

| From → To | Information / dependency | Current status |
|---|---|---|
| Player Presentation → Action & Resolution | Declared intent to interpret as a supported operation | Partial: fixed parsing and scenario commands; descriptive scene intention is not consequential execution, and general action framing remains open |
| World Simulation / Character System → Action & Resolution | External facts and resources; character capability, recognition/access basis and retained information | Implemented bounded premises; neither input owner independently adjudicates the attempt |
| Scenario & Authored Content → Action & Resolution | Supported prerequisites, evidence, declared costs/effects and bounded resolution material | Implemented narrow declarations plus engine policy; no authority to predetermine arbitrary player outcomes |
| Actors & Social Dynamics ↔ Action & Resolution | Intentional actor choices as inputs; adjudicated contested outcomes as results | Provisional: no general contest or autonomous decision mechanism; resolution does not choose actor intentions |
| Action & Resolution → World Simulation / Character System | Accepted immediate effects, applicable costs and evidence-grounded information legitimately yielded, committed with owning systems | Implemented bounded candidate paths; external truth/time and later causality remain World Simulation responsibilities, acquired information retains character continuity |
| Action & Resolution → Narrative Experience / Player Presentation | Safe approaches, uncertainty, costs, accepted results and evidence limits | Implemented bounded projections; provider expression cannot roll, waive costs or repair failure |
| Action & Resolution ↔ Persistence | Accepted draw/result, basis, cost, findings and causal references survive restoration | Implemented West-Road attempt replay without reroll/recharge/republish; no universal attempt ledger or anti-save-scumming guarantee |

An action's time cost may cross a World Simulation threshold within the same
candidate. Shared publication does not transfer downstream causal authority to
Action & Resolution. The fixed theft follows guard allocation and elapsed time,
not a competence result band or narrator choice.

## Dependencies and information flow around Actors & Social Dynamics

The [Actors & Social Dynamics manifest](actors-social-dynamics.md) refines
meaningful intentional NPC/faction decisions into social continuity, decision
basis, and intentional choice. This decomposition and broader social-state
interfaces remain provisional. Individual informational state/access belongs to
Character System; using it for a choice does not create a second knowledge model.
Consequential relationships and commitments may need continuity without numeric
meters, a general character sheet, or continuously simulated actors.

| From → To | Information / dependency | Current status |
|---|---|---|
| Scenario & Authored Content → Actors & Social Dynamics | Identity, roles, relationship/motivation foundations and bounded behavior declarations | Partial: profiles, numeric relationship foundations and faction objectives exist as content; fixed scenario behavior does not evaluate them as general decision policy |
| World Simulation → Actors & Social Dynamics | Circumstances, effective locations, pressures and relevant consequences | Implemented bounded premises; general intentional reaction interface provisional |
| Character System ↔ Actors & Social Dynamics | Legitimate information/access and capability constrain choices; accepted sharing establishes acquired information | Partial: report membership gates West-Road choices and authored responses; no general belief or propagation model |
| Actors & Social Dynamics ↔ Action & Resolution | Actor choices frame attempts; adjudicated outcomes inform further response | Provisional general interface; no general social contest or autonomous decision mechanism |
| Actors & Social Dynamics → World Simulation | Executed intentional action yields external consequences and relevant causal provenance | Fixed authored effects and guard commitments implemented; independent intentional offscreen choice deferred |
| Actors & Social Dynamics → Narrative Experience / Player Presentation | Safe behavior, attributed reports and eligible interactions | Partial authored replies and scenario projections; expression cannot create consequential choices, relationships or knowledge |
| Actors & Social Dynamics ↔ Persistence | Established social meaning and causal continuity survive technical boundaries | Partial: supported identity references, reports, location overrides and scenario history persist; general goals/relationships/group-state representation remains open |

Ordinary routines and background maintenance need no individual actor simulation.
Meaningful deliberate offscreen obstruction by an established antagonist would
require actor authority; its external result belongs to World Simulation. This
design distinction does not implement a scheduler or select a future package.

## Dependencies and information flow around Narrative Experience

The [Narrative Experience manifest](narrative-experience.md) proposes three
responsibilities: context selection, framing and continuity, and expression.
These refine expression of authoritative truth rather than adding fictional
authority. Selection does not establish informational access or erase omitted
truth. Compatible incidental texture remains non-authoritative; a model is one
expression mechanism alongside authored and deterministic text.

| From → To | Information / dependency | Current status |
|---|---|---|
| World Simulation → Narrative Experience | Accessible external facts, conditions and legitimate changes | Partial: bounded local scene and causal projections; provider snapshot still contains internal fields, not a universal safe view |
| Character System → Narrative Experience | Character-specific access basis, capability, recognition and retained findings, jointly constrained by world conditions | Partial: local competence layers; no general perception/familiarity engine; expression cannot grant knowledge |
| Action & Resolution → Narrative Experience | Accepted results, costs, findings and uncertainty limits | Implemented bounded outcomes; no general outcome stream or permission to repair failure |
| Actors & Social Dynamics → Narrative Experience | Accepted behavior, attributed reports and established social meaning | Partial authored/scenario behavior; expressive manner cannot invent consequential intentions, promises or disclosures |
| Scenario & Authored Content → Narrative Experience | Location grounding, dialogue, tone foundations and supported constraints | Implemented bounded content; authored wording remains constrained by live state |
| Player Presentation ↔ Narrative Experience | Declared focus/presentation context in; selected expressive content out | Partial CLI integration; parsing, widgets and safe display mechanics remain presentation responsibilities |
| Narrator Provider / Model Adapter → Narrative Experience | Untrusted candidate language | Implemented validated fail-closed path; structural acceptance is not proof of factual prose |
| Persistence → Narrative Experience | Restored supported fictional state from which scenes and recap are rebuilt | Implemented bounded recap; current-scene prose cache is session-only and not saved; no new storage interface selected |

Persistent truth need not be mentioned every turn. Current Scene Context and
bounded descriptive continuity support this direction without semantic repetition
suppression or authoritative provider memory. Technical resets can require
reorientation without creating fictional discontinuity. General context selection,
incidental-detail promotion and long-term narrative continuity remain unsettled.

## Dependencies and information flow around Scenario & Authored Content

The [Scenario & Authored Content manifest](scenario-authored-content.md) proposes
foundations, declarations and narrative material as three responsibilities.
Content supplies intentional starting material; supported runtime interpreters
establish applicability and consequences. Legitimate live campaign changes take
precedence over affected canonical/default facts. Current overlays implement this
only for supported state, not every authored field.

| From → To | Information / dependency | Current status |
|---|---|---|
| Scenario & Authored Content → World Simulation | Initial conditions, geography, supported constraints and effects | Implemented bounded seeds/declarations; no universal live override or generic effect language |
| Scenario & Authored Content → Character System | Supported actor knowledge seeds, identity foundations and evidence material | Partial: new-game membership and bounded clues/recognition; biography and canonical lore do not automatically grant access or competence |
| Scenario & Authored Content → Action & Resolution | Supported prerequisites, costs and result material | Partial: declaration interpretation plus code-defined West-Road eligibility/costs/results; option text cannot grant success |
| Scenario & Authored Content → Actors & Social Dynamics | Roles, relationship/motivation foundations, replies and bounded behavior | Partial: fixed behavior and profile representation; numeric relationships/faction objectives are not general decision policy |
| Scenario & Authored Content → Narrative Experience | Grounding, dialogue, tone foundations and scenario framing | Implemented bounded material; current truth/access constrain expression, with no universal semantic reconciliation |
| Scenario & Authored Content → Player Presentation | Names, labels, clue titles and eligible option wording | Implemented bounded projections; parsing and UI mechanics remain outside content ownership |
| Scenario & Authored Content ↔ Persistence | Stable references connecting source material and saved campaign state | Partial: saves reload a region path and validate supported references; content revision compatibility/pinning remains unsettled |

Canonical lore conceptually supplies foundations, not a campaign reset or a
character knowledge grant. Current source labels are not a lore-ingestion system.
Active Bryn Shander content is distinct from test-only legacy declarations, and
some authored scenario behavior/text remains in code. This separation suggests
future portability without establishing a general modding or scenario framework.
