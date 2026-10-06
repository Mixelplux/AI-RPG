# System responsibility and relationship map

Reviewed October 5, 2026 at `51f595b5c8516ef242a4fffeb246c0e143acc9b3`.
This is the current conceptual ownership model, subject to evidence and revision.
It is neither a call graph nor a list of runtime modules. See the separate
[runtime architecture](../../architecture.md) and [shared doctrines](README.md).
The World Simulation baseline is preserved. [Character System](character-system.md)
was reviewed October 6, 2026 at documentation baseline
`89f135834eb85cb995facb0b7126a3c5f58b7a6a`; later systems have no manifests yet.

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

| From → To | Information / dependency | Current status |
|---|---|---|
| Scenario & Authored Content → Character System | Supported seeds, evidence descriptions, clue/report text and bounded interpretation declarations | Implemented bounded slices; biography/profile/familiarity interfaces provisional |
| World Simulation → Character System | External facts, position, local evidence and conditions constrain access | Partial local perception/filtering; general sensory and familiarity access checks absent |
| Character System → Action & Resolution | Authoritative competence, limited recognition and retained information relevant to attempts | Implemented West-Road slice; capability does not adjudicate outcomes or create evidence |
| Action & Resolution → Character System / World Simulation | Accepted findings and attempts preserve character continuity; external consequences update world truth | Implemented fixed atomic candidate path; attempt records span responsibilities |
| Character System ↔ Actors & Social Dynamics | Individual informational access constrains intentional decisions and reports | Provisional general interface; static-actor membership and declared sharing/responses are bounded implementations |
| Character System → Narrative Experience / Player Presentation | Safe observations/reports, qualified recognition/findings and retained clue review | Partial: local Scene Context filters do not erase memory; narration cannot establish capability or knowledge |
| Character System ↔ Persistence | Validated supported competence, discoveries, actor membership and attempt continuity | Implemented version-1 slices; no general character identity/replacement or belief storage model |

These relationships neither relocate fields out of `world_state` nor prescribe
new module boundaries. Player intention remains external input; session-only
presentation continuity has no authority over persistent character state.
