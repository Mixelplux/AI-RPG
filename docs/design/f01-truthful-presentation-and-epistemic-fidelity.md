# F01 — Truthful Presentation and Epistemic Fidelity

## Status and scope

**Accepted design; consolidation proposed for owner review.** This is the
single authoritative Design record for F01-D1–D10. D1–D5 retain their original
owner-accepted wording. D6–D10, including revised D10 and the accepted D8/D9
clarifications, reproduce the owner-supplied accepted text with line wrapping
only. This documentation consolidation awaits owner review and grants no
publication authority.

These are intended gameplay requirements, not a claim of implemented behavior
or authorization to implement them. They apply to presentation of established
meaning without selecting authored, deterministic, generated or hybrid mechanisms.
Existing sources retain their stated status and historical scope.

## Player-facing goal

Preserve the player's understanding of established information and actual
outcomes so that choices, investigations and commitments remain meaningful.
Natural expression and harmless incidental invention remain compatible with
that goal; narration is expected to offer reasonable fidelity, not perfection.

## Governing context

Read these decisions with [Story-First Part I](../story_first_design_doctrine.md#part-i--established-design-doctrine),
[Simulation principles](../simulation_principles.md), the relevant accepted
[ADRs](../decisions.md#adr-059---character-information-and-spatial-projection-use-minimum-sufficient-world-detail)
and [shared doctrines](systems/README.md#shared-doctrines), including the
[Specificity Doctrine](systems/README.md#specificity-doctrine) and
[Context Carry-Forward](systems/README.md#context-carry-forward).

Simulation owns consequential truth and accepted outcomes. AI/provider output
remains untrusted and has no simulation authority; provider behavior fails
closed. F01 preserves these boundaries. It neither revises existing doctrines,
principles or ADRs nor converts provisional descriptions into architecture.

## Accepted decisions

### F01-D1 — Consequential meaning

Narration preserves established consequential meaning.

Significance is assessed contextually, considering immediate and plausible
later effects on player understanding, choices, risks, knowledge, commitments
and consequences.

Harmless incidental expressive invention remains permissible.

This is a reasonable-fidelity expectation, not a guarantee of perfect narration.

### F01-D2 — Attribution and uncertainty

Information sources, verification status and uncertainty remain clear when
consequential.

Initial attribution may carry naturally through context.

Repeat or clarify attribution when omission would materially mislead the
player, especially during consequential decisions or investigations.

Avoid repetitive disclaimers and mechanical exposition.

Apply the existing [Specificity Doctrine](systems/README.md#specificity-doctrine).

### F01-D3 — Character-grounded interpretation

Narration may communicate interpretations supported by the character's
established observations, knowledge, experience and competence.

The narrator should not independently provide additional hints or solve
problems for the player.

Ordinary contextual inference remains permissible when appropriately grounded.

Optional hint assistance is deferred until gameplay establishes a need.

### F01-D4 — Investigative outcome precision

Narration must preserve the actual investigative result.

Distinguish:

- No tracks found.
- Tracks or signs found, but no usable trail.
- An established trail subsequently lost.

These are materially different outcomes.

Relevant established circumstances may explain an outcome naturally.

Do not invent findings, causes, progress or explanations unsupported by the
accepted result and available context.

Do not routinely add statements explaining what a failed search does not prove.

### F01-D5 — Historical continuity

Previously established information may be referenced naturally.

Preserve temporal and access distinctions when materially relevant.

Do not automatically imply that historical information remains currently
actionable.

Equally, do not manufacture uncertainty or require re-verification merely
because time has passed.

Players may act on historical knowledge and accept the associated uncertainty.

### F01-D6 — Minimum Sufficient Information Principle

Narrative Experience must have sufficient authoritative information to
preserve the consequential meaning of what it communicates.

The necessary information is determined contextually by the player's
situation, available character knowledge, current activity and plausible
consequences.

Meaningful distinctions must be available explicitly or reliably derivable
from authoritative information.

Ordinary incidental detail does not require exhaustive representation.

Where required information is unavailable, narration must not invent
consequential meaning to compensate.

F01 establishes these information requirements and their ownership boundaries
without prescribing a universal representation, storage mechanism or narrative
pipeline.

### F01-D7 — Grounded Contextual Interpretation

Narrative Experience may communicate interpretations reasonably supported by
the character's established observations, knowledge, familiarity, experience
and competence.

Ordinary contextual inference may be expressed without separate adjudication
when its meaning is adequately grounded in available information.

Interpretations that establish consequential new knowledge, resolve meaningful
uncertainty or materially alter the player's available understanding require
sufficient authority from the responsible gameplay systems.

Where multiple explanations remain plausible, narration may convey supported
possibilities without presenting one as established fact.

Interpretation should support the character's competence and the player's
understanding without independently solving investigations or introducing
unearned hints.

### F01-D8 — Selective Consequential Provenance

The game must preserve sufficient information about the origin, evidential
basis, verification and temporal relevance of consequential information to
support faithful interpretation and narration.

Provenance requirements are proportional to their significance for player
understanding, decisions, investigations and future consequences.

Narrative Experience must distinguish established facts from reports, beliefs,
hypotheses and interpretations when those distinctions matter.

Repeated transmission of a claim does not independently verify it. New
evidence may strengthen, weaken or contradict a claim according to what that
evidence actually establishes.

Information retains its historical meaning even when its current applicability
changes.

Attribution and uncertainty should be communicated naturally, with explicit
clarification when omission would materially mislead the player.

**Accepted D8 clarification — Retention and recall**

Use significance-based retention and relevance-based recall as the working
design direction.

Information not mentioned is not necessarily forgotten. Consequential
information should remain available when necessary for meaningful decisions
and continuity. Ordinary information may be supplied through relevant context,
familiarity or reasonable inference.

Do not introduce universal provenance expiration, detailed memory decay or
exhaustive memory tracking without demonstrated gameplay need.

Specific memory retention and recall behavior remains a Character System
design dependency.

### F01-D9 — Consequence-Sensitive Fidelity and Recovery

Narrative fidelity is assessed according to whether expression preserves
consequential meaning, including established facts, outcomes, character
knowledge, attribution, uncertainty, temporal context and materially relevant
costs.

Harmless expressive variation is acceptable.

Narration that materially distorts established meaning or introduces
unsupported consequential information must be rejected or corrected.

Fidelity assessment considers the context and plausible effects on player
understanding and subsequent choices rather than requiring literal
reproduction of source information.

When a material error reaches the player, the game must provide an appropriate
correction while preserving authoritative gameplay state.

Recovery should be proportional to the significance of the error and minimize
unnecessary interruption to play.

Where a player has already acted in reliance on incorrect narration, the
discrepancy must be considered in subsequent gameplay reconciliation.

**Accepted D9 clarification — Proportional safeguards**

Prioritize reliable gameplay without introducing extensive preventative
controls before demonstrated need.

Harmless expressive variation does not require exhaustive verification.

Additional validation, recovery mechanisms or control layers require evidence
of meaningful gameplay failures.

Player reliance on incorrect narration remains a gameplay fairness principle.
It does not mandate an automated reconciliation system in advance.

### F01-D10 — Gameplay-Centered Fidelity Validation

F01 is evaluated through representative gameplay situations and extended
gameplay testing, assessing consequential accuracy, epistemic fidelity,
character-grounded interpretation, continuity and narrative quality.

Focused automated checks, fidelity harnesses and controlled experiments may be
used to identify failures, characterize their causes and prevent regressions.
These validation mechanisms need not become player-facing runtime systems.

Actual gameplay is an ongoing source of design evidence. Observed failures may
justify changes to narration, supporting systems, evaluation methods or
accepted design assumptions.

Validation should prioritize meaningful gameplay consequences and recurring
weaknesses over superficial imperfections. Additional runtime safeguards and
architectural complexity should be justified by demonstrated need rather than
hypothetical production requirements.

F01 does not require a fixed release-quality threshold or comprehensive
player-facing recovery infrastructure.

## Cross-system requirements and deferred dependencies

These requirements identify the meaning each responsibility must supply or
preserve. They select no interface, mechanism or implementation prerequisite.
The linked manifests retain their implementation classifications and authority.

| Responsibility | F01 requirement and retained boundary |
|---|---|
| [Narrative Experience](systems/narrative-experience.md) | Receive sufficient authoritative information, explicit or reliably derivable, and express accessible context faithfully; preserve consequential meaning, attribution, grounded interpretation, actual results and historical continuity. Selection and emphasis do not establish truth or access. |
| [Action & Resolution](systems/action-resolution.md) | Supply actual accepted findings, outcomes, material costs and limits so attempts and their consequences remain intelligible. Narration cannot invent progress, waive costs or repair failure. |
| [World Simulation](systems/world-simulation.md) | Supply established external circumstances, legitimate changes and consequential causal continuity. Presentation error does not authorize a world-state change or new offscreen causal policy. |
| [Character System](systems/character-system.md) | Supply legitimate informational access, experience, competence and relevant retained continuity to ground interpretation and recall. World truth and narrator context alone do not grant knowledge. General retention/recall is deferred below. |
| [Actors & Social Dynamics](systems/actors-social-dynamics.md) | Supply accepted behavior and reports with consequential source/verification distinctions. Expression establishes no new actor knowledge, intention, commitment or propagation. |
| [Scenario & Authored Content](systems/scenario-authored-content.md) | Supply grounding and supported evidence/result material consistent with established campaign meaning. Authored wording alone grants neither current truth, access nor an outcome. |
| [Player Presentation](systems/player-presentation.md) | Display sufficient supplied context, choices, results and material corrections intelligibly; preserve the distinction between technical failure and fictional outcome. F01 selects no layout or input mechanism. |
| [Persistence](systems/persistence.md) | Preserve supported accepted meaning and selectively required provenance across restoration. Gameplay owners determine retention needs; storage does not choose relevance, grant access or establish new facts. |

[F05 — Authorized Activities and Player Control](f05-authorized-activities-and-player-control.md)
now records the accepted authorization, interruption and resumption boundaries.
F01's information contract remains unchanged: realization cannot execute actions
or create consequential progress. Future bounded F01–F05 playable situations and
their [separately authorized evaluation](../deferred_findings.md#df-009--bounded-f01f05-playable-scenario-evaluation)
must satisfy that contract even with predetermined fixtures; no full upstream
system or integration milestone is authorized by this cross-reference.

**Deferred Character System dependency:** the
[accepted D8 clarification](#f01-d8--selective-consequential-provenance) supplies
significance-based retention and relevance-based recall as the working design
direction. Specific memory retention and recall behavior remains deferred to
Character System design. Character informational continuity differs from
authoritative campaign history and a narrator's transcript or cache. Existing
bounded records do not establish a general memory capability; this consolidation
selects no expiration, decay, storage or retrieval mechanism.

Scene/context selection, incidental-detail promotion, consequential provenance
representation and recovery procedures remain separately scoped dependencies.
They need no general solution for this documentation consolidation. Validation
can exercise bounded or stipulated character/context inputs if their limits are
explicit; doing so does not claim that deferred systems are implemented.

## Development and validation posture

This is a personal, single-player project intended to evolve through an extended
beta. Pursue useful, coherent gameplay with reasonable fidelity and iterative
improvement from observed failures. Apply the existing
[proportional engineering posture](../engineering_posture.md); credible
consequence and recovery difficulty determine rigor.

Focused offline fidelity harnesses, representative scenario fixtures, controlled
comparisons and owner play evaluation are compatible with this posture when
separately authorized. Their purpose is to reveal meaningful gameplay failures
and guide the smallest justified improvement. A harness may need explicit source
and result material for assessment without requiring that structure in every
runtime response.

F01 mandates no speculative semantic validator, runtime monitoring/control
framework, universal automated judge, retry/fallback architecture or release gate.
Add controls only when observed need and consequence justify separately scoped
work. Existing simulation authority, untrusted provider boundaries, fail-closed
provider behavior, atomicity and save-compatibility obligations remain intact.
This posture does not authorize live provider calls or evaluation in this task.

## Research context and implementation boundary

The completed external [protocol verification](<C:/tmp/AI-RPG-F01-Protocol-Verification-20261014/f01_protocol_verification.md>)
and [focused review](<C:/tmp/AI-RPG-F01-Focused-Review-20261014/f01_focused_review.md>)
provide historical research context and limitations. They prepared consideration
of F01 before the original five decisions were accepted. Their open alternatives
are not additional accepted requirements. Research evidence remains separate from
the accepted Design decisions above and establishes no general reliability claim.

F01 selects no narrator model or prompt, schema or validator, narrative pipeline,
information storage or retrieval mechanism, actor simulation, action interpretation
mechanism, or implementation milestone. Existing technical descriptions remain
bounded implementation evidence or provisional models according to their own
status. This record schedules no capability package, advances no lifecycle state
and does not begin F02.

## Revision history

- October 14, 2026: record the five owner-accepted F01 gameplay decisions and
  relevant cross-system implications; documentation integration proposed for
  owner review and publication, with implementation requiring separate authorization.
- October 14, 2026: consolidate accepted D6–D9 and revised D10; preserve D1–D5;
  record deferred Character System retention/recall, cross-system requirements
  and the personal-project extended-beta validation posture. Use owner-supplied
  accepted D6–D10 and D8/D9 clarifications with line wrapping only; documentation
  proposed for owner review; no implementation, research or lifecycle advancement.
