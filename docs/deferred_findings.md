# Deferred findings register

Established October 11, 2026 during accepted North-Gate Working Context V1
closeout. Existing handoff findings and system-manifest questions are consolidated
here by underlying capability; their original records remain historical evidence.
No existing DF identifiers or centralized register were found before creating this
record. IDs are stable and must not be recycled.

These are deferred capability limitations or explicitly identified research
questions, not confirmed defects in accepted V1. Every entry is nonblocking and
unscheduled. Recording a condition for resolution does not authorize a package,
implementation, architecture, persistence model or doctrine change. Owner selection
and bounded scope must precede eventual work; completion requires evidence for the
selected scope, not a claim that an entire general capability has been solved.

Sources: [North-Gate acceptance](north_gate_working_context_v1_handoff.md),
[corrected smoke](north_gate_working_context_v1_correction.md),
[Scene Construction V1 findings](scene_construction_v1_handoff.md#acceptance-and-deferred-findings),
and the linked existing system manifests. No earlier evidence is superseded or overwritten.

## DF-001 — Discovery and information exposure

- Missing capability/limitation: contextual discovery and player/NPC information
  exposure beyond authored public briefing and fixed evidence prerequisites.
- Examples/source: North-Gate V1 smoke names tracks and Mara before investigation;
  Elin's dialogue is grounded in authored prerequisites. Consolidates Scene
  Construction V1's public-prerequisite-guidance/first-heard limitation. This is
  an accepted testing limitation, not unauthorized knowledge introduced by V1.
- Responsible system: [Scenario / Authored Content](design/systems/scenario-authored-content.md),
  [Character System](design/systems/character-system.md) and
  [Player Presentation](design/systems/player-presentation.md).
- Disposition: deferred limitation; no scenario or Elin correction in V1.
- Resolution conditions: separately authorize a bounded discovery/exposure scope;
  establish which authoritative observations, reports or briefings justify exposure,
  and verify that presentation does not grant discoveries, knowledge or receipts.

## DF-002 — Contextual intent interpretation

- Missing capability/limitation: bounded interpretation of reasonable contextual
  player intent beyond currently supported commands.
- Examples/source: broad investigation, intermediate actions, natural reporting and
  selective disclosure raised around North-Gate V1 smoke. They remain future scope;
  ordinary talk resumption is the accepted narrow exception. Consolidates the
  existing Action Resolution manifest's intent gap and access-boundary questions.
- Responsible system: [Action Resolution](design/systems/action-resolution.md),
  [Player Presentation](design/systems/player-presentation.md) and actor knowledge
  ownership for disclosures.
- Disposition: deferred capability/research; no general intent or disclosure system selected.
- Resolution conditions: owner-approved bounded command family, explicit ambiguity
  and confirmation policy where needed, and tests that inferred commands still pass
  current eligibility, disclosure, cost and authority predicates.

## DF-003 — Flexible evidence adjudication

- Missing capability/limitation: contextual evidence sufficiency beyond two
  predetermined report receipts in this authored patrol decision.
- Examples/source: North-Gate V1 requires tracks and Mara's account regardless of
  hypothetical alternative evidence. Consolidates Action Resolution's policy and
  scenario-boundary questions; this is not a defect in accepted prerequisites.
- Responsible system: [Action Resolution](design/systems/action-resolution.md),
  [Scenario / Authored Content](design/systems/scenario-authored-content.md) and
  [Actors & Social Dynamics](design/systems/actors-social-dynamics.md).
- Disposition: deferred capability; current prerequisites stay authoritative.
- Resolution conditions: separately select a bounded alternative-evidence case;
  define authoritative sufficiency and decision rules and demonstrate atomic,
  exactly-once results without narrator-created evidence or NPC decisions.

## DF-004 — General causal-scene continuity

- Missing capability/limitation: causal continuity for temporary physical facts,
  NPC activity, external interruption and scene-local consequences beyond dialogue focus.
- Examples/source: North-Gate V1 deliberately retains only participant/focus/status
  and bounded accepted-event references. The accepted Scene Context Integration
  assessment (C:/tmp/AI-RPG-Scene-Context-Integration/run-ed779548/assessment.md)
  separates this immediate exchange from the wider West-Road predicament.
  Broader examples are research cases, not observed V1 failures.
- Responsible system: [Narrative Experience](design/systems/narrative-experience.md),
  [World Simulation](design/systems/world-simulation.md) and
  [Actors & Social Dynamics](design/systems/actors-social-dynamics.md).
- Disposition: deferred capability/architecture question; no general scene manager selected.
- Resolution conditions: an owner-authorized concrete causal use case must establish
  fact ownership, lifetime, interruption/revalidation and consequence boundaries;
  verify that temporary context never duplicates or overrides authoritative truth.

## DF-005 — Scene-to-world consequence relevance

- Missing capability/limitation: relevant cross-scene consequences and actor knowledge
  propagation beyond current authored world transitions and bounded effects.
- Examples/source: consequential NPC death, propagated actor knowledge, pressures
  and deferred offscreen developments are conceptual cases recorded at North-Gate
  closeout, not executed or failed mechanics. Consolidates existing World Simulation
  and Actors & Social Dynamics questions. Scene Construction V1's stale overdue
  caravan overview after Mara's report is the observed related limitation: modeled
  caravan identity and resolution of that original report are absent.
- Responsible system: [World Simulation](design/systems/world-simulation.md),
  [Actors & Social Dynamics](design/systems/actors-social-dynamics.md), with
  [Scenario / Authored Content](design/systems/scenario-authored-content.md) for caravan identity.
- Disposition: deferred capability/research; no combat, autonomy or offscreen simulation selected.
- Resolution conditions: separately authorize a concrete consequence chain, assign
  state/knowledge ownership and propagation triggers, and verify relevance, causal
  provenance, exactly-once commitment and compatibility for that bounded chain.

## DF-006 — Follow-up action and cost presentation

- Missing capability/limitation: clear presentation of differing action abstraction,
  uncertainty and cost in existing observer follow-ups.
- Examples/source: Scene Construction V1 finding that deterministic pursuit with
  zero additional time could be clearer beside uncertain, paid tracking. Mechanics
  passed; North-Gate closeout introduces no new behavior or claim of failure.
- Responsible system: [Player Presentation](design/systems/player-presentation.md),
  with [Action Resolution](design/systems/action-resolution.md) owning rules/costs.
- Disposition: deferred nonblocking presentation limitation, retained under one stable ID.
- Resolution conditions: owner-authorized bounded presentation scope and smoke
  demonstrating clearer distinctions while preserving authoritative costs/outcomes.

## DF-007 — Load reorientation wording

- Missing capability/limitation: contextual reorientation wording that clearly
  distinguishes recorded attempts from current actions.
- Examples/source: Scene Construction V1's present-tense restatement of a stored
  failed check after load. Restoration performs no new check, draw, cost, discovery
  or receipt; this is not a save/load correctness defect.
- Responsible system: [Player Presentation](design/systems/player-presentation.md),
  with [Persistence](design/systems/persistence.md) retaining restoration authority.
- Disposition: deferred nonblocking presentation limitation.
- Resolution conditions: separately authorize bounded wording work; check loaded
  reorientation and prove it neither executes nor implies a new authoritative attempt.


## DF-008 — Narration-unavailable deterministic fallback experience

- Missing capability/limitation: successful `look` observations use the provider
  preview and, when it is unavailable, offer only a retry notice rather than a
  usable deterministic scene fallback. Provider fail-closed safety remains intact.
- Examples/source: October 11, 2026 Contextual Investigation V1 smoke; controlled
  exact-baseline comparison reproduces first/repeated `look` output:
  "Scene narration is unavailable. You can retry with 'look'." Both protected
  baseline and uncommitted V1 match with missing configuration or the offline
  launcher's blocked constructor. This predates V1 and is not launcher-exclusive.
  Initial/travel deterministic scenes and later clue acquisition remain available;
  `look` changes no authoritative state. Consolidates the existing
  [Player Presentation failure/status limitation](design/systems/player-presentation.md)
  and [Narrative Experience partial fallback](design/systems/narrative-experience.md).
  See [final V1 handoff](contextual_investigation_v1_handoff.md#final-baseline-classification-and-acceptance--october-11-2026)
  and `C:/tmp/AI-RPG-Contextual-Investigation-V1-Final-Verification/classification.md`.
- Responsible system: [Player Presentation](design/systems/player-presentation.md)
  and [Narrative Experience](design/systems/narrative-experience.md).
- Disposition: existing nonblocking baseline experience limitation; deferred and
  unscheduled. No V1 regression, narration redesign or provider work authorized.
  Matching baseline behavior establishes provenance, not fallback desirability.
- Resolution conditions: separately authorize bounded offline/provider-failure
  presentation work; verify usable deterministic reorientation after first/repeated
  observation while preserving simulation authority, costs, discoveries, history,
  receipts and provider fail-closed behavior. Expected provider unavailability and
  fallback experience quality must be evaluated separately.
