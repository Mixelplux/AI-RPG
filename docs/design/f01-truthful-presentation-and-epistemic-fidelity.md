# F01 — Truthful Presentation and Epistemic Fidelity

## Status and scope

**Accepted design.** Recorded October 14, 2026 from the five owner-accepted
F01 decisions supplied in the documentation integration authorization.
This is the single authoritative Design record for those decisions. The
proposed documentation integration awaits owner review and publication.

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

## Cross-system implications

These relationships track where faithful presentation matters. They do not
make adjacent capabilities prerequisites or select interfaces or mechanisms.

| Responsibility | F01 implication and retained boundary |
|---|---|
| [Narrative Experience](systems/narrative-experience.md) | Preserve consequential meaning, attribution, grounded interpretation, actual results and relevant historical distinctions in expression. Selection and emphasis do not establish truth or access. |
| [Action & Resolution](systems/action-resolution.md) | Actual investigative outcomes and their supported findings constrain narration. F01 selects no action interpretation or resolution mechanism. |
| [World Simulation](systems/world-simulation.md) | Established circumstances and legitimate changes constrain present and historical claims. F01 adds no actor simulation, offscreen progression or new causal policy. |
| [Character System](systems/character-system.md) | Interpretations remain grounded in established character observations, knowledge, experience and competence. General discovery, familiarity and access mechanisms remain separately scoped. |
| [Actors & Social Dynamics](systems/actors-social-dynamics.md) | Reports retain consequential source and verification distinctions. Their expression establishes no new actor knowledge, motive, choice or propagation. |
| [Player Presentation](systems/player-presentation.md) | Display of supplied narrative and results preserves their consequential meaning. F01 selects no interaction surface, parsing mechanism or display layout. |
| [Persistence](systems/persistence.md) | Historical reference preserves relevant temporal and access meaning. F01 selects no information storage, retrieval, retention, save-version change or migration. |

Scene content selection, information discovery/access, actor knowledge and
memory/history remain relevant separately scoped questions. No general solution
to them is required by this documentation integration.

## Research context and implementation boundary

The completed external [protocol verification](<C:/tmp/AI-RPG-F01-Protocol-Verification-20261014/f01_protocol_verification.md>)
and [focused review](<C:/tmp/AI-RPG-F01-Focused-Review-20261014/f01_focused_review.md>)
provide historical research context and limitations. They prepared consideration
of F01 before the five decisions were accepted; their open alternatives are
not additional accepted requirements. Research evidence remains separate from
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
