# System responsibility and relationship map

Reviewed October 5, 2026 at `51f595b5c8516ef242a4fffeb246c0e143acc9b3`.
This is the current conceptual ownership model, subject to evidence and revision.
It is neither a call graph nor a list of runtime modules. See the separate
[runtime architecture](../../architecture.md) and [shared doctrines](README.md).
The World Simulation baseline is preserved. [Character System](character-system.md)
was reviewed October 6, 2026 at documentation baseline
`89f135834eb85cb995facb0b7126a3c5f58b7a6a`.
[Action & Resolution](action-resolution.md) has an October 6, 2026 review candidate
at baseline `d0dba1f5f1da391216cdb8fb8e4dabf8485705c8`;
[Actors & Social Dynamics](actors-social-dynamics.md) has an October 6, 2026 review
candidate at baseline `63f1a3db8b8996efe0f8245ad21d22ddb234dcbc`;
later systems have no manifests yet.

## Responsibility hierarchy

| Group | Systems and responsibilities |
|---|---|
| Core Gameplay | **World Simulation:** external reality and legitimate change. **Character System:** character capability, perspective, and memory. **Action & Resolution:** adjudication of attempted action. **Actors & Social Dynamics:** meaningful intentional NPC/faction decisions. |
| Experience | **Narrative Experience:** expression of authoritative truth and outcomes. **Player Presentation:** player input/display and interaction surface. |
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
