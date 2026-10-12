# Architecture comprehension review — research precedent index

Non-authoritative working index, reconciled October 12, 2026. Runtime claims use
published baseline `a6ff316473ce2bafc58be4718479261602f5e3ac`, covering accepted
implementation through October 11. October 12 A/B and Option C research is indexed
as experimental evidence only. This document discovers precedent; it creates no
doctrine, framework requirement, architecture acceptance or next milestone.

Read the directly relevant source before investigating again. [Architecture Review
guidance](conditional_procedures.md#architecture-review) supplies the lightweight
precedent check. [Runtime architecture](architecture.md), [system ownership map](design/systems/system-map.md),
[ADRs](decisions.md), [principles](simulation_principles.md), [Simulation Model](simulation_model.md)
and [Story-First doctrine](story_first_design_doctrine.md) retain their own authority
and historical scope. [Deferred findings](deferred_findings.md) retain stable IDs.

## Questions and existing precedent

| Architectural question | Established direction / accepted implementation | Research precedent and genuine remaining gap |
|---|---|---|
| What is the minimum sufficient resolution detail when uncertainty matters? | [Routine Until Meaningful](simulation_principles.md#routine-until-meaningful), [Resolution Follows Meaningful Uncertainty](simulation_principles.md#resolution-follows-meaningful-uncertainty), [Specificity Doctrine](design/systems/README.md#specificity-doctrine), [minimum detail](story_first_design_doctrine.md#minimum-sufficient-detail), ADR-059 and [Action Resolution depth](design/systems/action-resolution.md#resolution-depth) already establish the principle. Accepted competence and material handling demonstrate bounded deterministic/uncertain outcomes. | R1 wall probes distinguish assessment, preparation, commitment, partial progress and stopping. R2/R3 test risk disclosure and revalidation; R4 tests outcome-constrained explanation. These are candidate mechanisms and controlled fixtures, not the origin of the principle or proof of generalized physics, perception or extended action. |
| How should interpretation and contextual grounding differ from gameplay feasibility? | [Investigation V1](contextual_investigation_v1_handoff.md) and [material handling](contextual_action_consequence_v1_handoff.md) propose stable frames; owning policies revalidate access, method, restrictions, presence, risk/cost and accepted consequences. Input and narration cannot establish truth. | R5 demonstrates collisions when both contextual purposes coexist. R6 separates shared interpretation/grounding from specialized validation/execution for two purposes. General language grounding, ambiguity and dropped-purpose prevention remain unproven; see DF-002. |
| Which rules belong to a purpose, and which mechanisms can be common? | [Authority Composition](design/systems/README.md#authority-composition) and [Action Resolution](design/systems/action-resolution.md) distinguish common candidate publication, causal history and d6 primitives from inquiry access, material feasibility and actor policy. Shared storage does not transfer meaning. | R5 A/B retain specialized parsers and add ownership decisions; neither simplifies overall runtime. R6 replaces those parsers with structured instructions while retaining purpose rules. A common interpreter is a hypothesis, not a requirement to centralize all gameplay policy. |
| What information should a structured handler contract preserve? | Accepted transient `ActionFrame` and `HandlingFrame` carry bounded operation, stable subject, method/objective and restrictions. [Structural correction](contextual_action_structural_correction.md) distinguishes inspection/possible repair from authorization. [Material persistence](design/systems/persistence.md#later-accepted-material-continuity) retains accepted effects, not unsaved proposals. | R2/R3 use exact target/method/objective/stopping condition and separate risk recognition, communication and commitment. R6 removes raw-input handler overloads in the experiment. General compound intents, stopping conditions and richer contracts are not accepted production capabilities. |
| How do consistency, simplicity and extensibility compare? | Existing [system manifests](design/systems/README.md) remain revisable responsibility models; bounded reuse must preserve simulation authority and compatibility. Investigation's test depot and material's archive fixture establish specific reuse. | R5 A/B are completed negative simplification experiments: they repair tested routing collisions but add complexity. R6 is promising for two-purpose consistency and handler simplicity, with modest global complexity change and real source movement. Third-purpose extension effort and real-player clarification frequency were not demonstrated. |
| How should multiple systems coordinate open-ended action? | [Causal Continuity](design/systems/README.md#causal-continuity), [World Simulation](design/systems/world-simulation.md), [Actors & Social Dynamics](design/systems/actors-social-dynamics.md) and existing transactions preserve ownership. North-Gate [working context](north_gate_working_context_v1_handoff.md) is session focus; accepted material preparation/time/outcomes share one candidate. | R1/R4 keep physical success separate from observation, attribution and explanatory detail; R5/R6 test two-purpose routing. General compositions, arbitrary actor intervention and extended contests remain open. DF-003/004/005 retain evidence, causal-scene and propagation gaps. No scene manager or universal action planner is selected. |
| Does the evidence support refactoring or rebuilding? | Accepted candidate publication, discovery/report transactions, finite material state and save-version-1 compatibility are working seams. [Workflow](../WORKFLOW.md) requires separately authorized bounded implementation. | R5 supports retaining current architecture rather than layering B's router. R6 explores a bounded replacement of two interpretation pipelines, not rebuilding simulation. A smaller lexical refactor was not tested against C. No measured rebuild benefit, completed migration or general extensibility advantage is established. |

## Evidence locator and status

All R1–R6 evidence below is local under `C:/tmp`, outside durable repository
documentation. Paths were checked for this review; availability on another machine
is not guaranteed. Consult the reports and their linked final ledgers/patches rather
than duplicating reports here. Counts are historical claims, not checks rerun here.

| ID | Local evidence | What it establishes and limits |
|---|---|---|
| R1 | `C:/tmp/AI-RPG-Action-Resolution-Experiment-A/evidence_report.md` | Initial fixture block is retained; the appended completed/resumed results supersede its initial blocked status. Wall assessment/preparation/commitment/stopping/disclosure probes show bounded production gaps and a supplied reference evaluator, not production climbing or general physical validation. |
| R2 | `C:/tmp/AI-RPG-Action-Resolution-Experiment-A/A1/evidence_report.md` | Completed disclosure/authorization comparison. Pending confirmation is one tested policy, not the only safe policy; full action re-entry also satisfies the stipulated boundary. |
| R3 | `C:/tmp/AI-RPG-Action-Resolution-Experiment-A/A2/evidence_report.md` | Completed six-case revalidation study using A.1's disposable evaluator. Current feasibility/identity/risk revalidation preserves intent and prior accepted effects; fixture success is not a production feature. |
| R4 | `C:/tmp/AI-RPG-Outcome-First-Research/evidence_report.md` | Six supplied climbing/tracking outcomes, manually reviewed explanations and one continuity follow-up distinguish explanation from unauthorized effects/information. No provider generations, automatic semantic verifier or production mechanic was established. |
| R5 | `C:/tmp/AI-RPG-Action-Routing-20261012-01a12fd0/comparative_report.md` | Completed A/B negative simplification experiments at `549fd848…`: A adds cross-purpose exclusion; B adds a router while retaining specialized interpretation. Both repair demonstrated combined-fixture collisions, but neither reduces overall runtime complexity. These are different experiments from R1's similarly named wall study. |
| R6 | `C:/tmp/AI-RPG-Option-C-20261012-01a12fd0/option_c_report.md` | Promising bounded replacement experiment at `549fd848…`: shared interpretation, structured instructions and specialized execution replace the two raw-input pipelines. Handler separation improves; overall complexity changes little. Not accepted production architecture; third-purpose extensibility and general composition are hypotheses. |

Earlier narrative evidence remains discoverable via the accepted
[provisional pipeline handoff](provisional_narrative_pipeline_handoff.md),
[Scene Construction acceptance/findings](scene_construction_v1_handoff.md#acceptance-and-deferred-findings),
[North-Gate correction](north_gate_working_context_v1_correction.md), and
[investigation acceptance](contextual_investigation_v1_handoff.md).
The [10.82 closure](sprint_10_82_closure.md) records rejected narrator fidelity;
it does not describe the accepted later integration. A bounded successful smoke,
structural validation or manually tagged explanation study cannot establish general
semantic fidelity. A/B's negative simplification result and C's promising replacement
result address different hypotheses; neither silently adopts a new architecture.
