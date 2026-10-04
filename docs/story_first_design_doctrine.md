# Story-First Design Doctrine v0.2

**Status: Provisional living document**

This document is authoritative as a design-evaluation lens. Part I records
accepted design doctrine; Part II describes a provisional AI-GM reasoning
model; Part III records hypotheses requiring experimentation. Provisional
mechanisms and hypotheses are not implementation mandates, software components,
schemas, or new engine contracts. They do not authorize implementation or
supersede `WORKFLOW.md` and its owner-controlled task boundaries.

Revise this document when playtesting or experiments provide better evidence.
Do not expand implementation merely to conform to hypothetical future
architecture. Apply the [proportional engineering posture](engineering_posture.md)
to the experience actually being enabled.

## Part I — Established design doctrine

### Story and player experience are the product

The story and the player's experience of it are the product. Systems,
structures, rules, simulation, persistence, AI, and architecture exist to
enable that experience.

Systems earn complexity only when they materially improve meaningful choice,
consequence, character engagement, discovery, tension/uncertainty, continuity,
agency, believable world response, or long-term narrative development.
Technical elegance, completeness, generality, and theoretical future usefulness
are not sufficient justification.

### Campaigns and story structure

- A campaign is persistent history and evolving world context, not a
  predetermined plot. Plan trajectories, not the player's future scenes.
- NPCs, antagonists, and factions may form plans; the campaign does not plan
  the player's actions. Epic campaigns can emerge from persistent long-term
  intentions, pressures, relationships, discoveries, setbacks, and consequences.
- Major arcs should be scarce. Prefer one rich foreground major arc over
  several simultaneous epic threats competing for attention. Other large
  concerns may remain latent or in the background until relevance changes.
- Not all situations should connect to the major arc. Independent novelty
  makes the world feel larger than the player's current history.
- Long-term coherence comes from persistent causality, not plot predetermination.

### Player agency and world momentum

- The player is central to the experience, not necessarily to causality.
  Relevance is negotiated between player attention and world momentum.
  Intentions and commitments signal relevance but do not control reality.
- Players may abandon, ignore, or redirect away from situations and apparent
  major arcs. Changing direction does not erase choices or commitments:
  promises, threats, investments, alliances, failures, and abandoned
  responsibilities may carry consequences forward.
- Other actors can act without the player. Ignored situations may improve,
  worsen, resolve, transform, or remain dormant. Unchosen opportunities do not
  automatically fail.
- The world must not freeze while unobserved, and it must not fully simulate
  everything. Preserve consequential truth at sufficient resolution.

### Failure and consequence

- The protagonist is not guaranteed success. The narrative owes meaningful
  agency and intelligible consequences, not eventual victory.
- Bad decisions must be allowed to remain bad decisions. Consequences should
  be causal rather than punitive; failure should usually transform the
  campaign rather than invalidate it.
- Antagonists and opposing forces must be capable of meaningful success.
  Success and failure may be partial or mixed rather than binary.
- Major consequences resist casual reversal. Reversal requires credible
  causality and usually meaningful cost. Established history constrains
  future creativity.

### Relevance and attention

- Relevance is relational, not geographic. Do not formalize local/regional/world
  tiers. Geography is one factor alongside relationships, identity, obligations,
  history, reputation, goals, consequences, knowledge, and sustained player interest.
- Player attention should increase resolution before objective significance.
  Importance, urgency, and immediacy are distinct; active arcs may remain offscreen.
- "No new major situation" is a valid AI-GM outcome. Quiet play, recovery,
  ordinary conversation, and breathing room are valid. Do not flood play with content.
- Explicit player disinterest should usually reduce repeated attempts to
  foreground the same material unless causal circumstances make it relevant again.

### Minimum sufficient detail

- Worlds, characters, organizations, and arcs begin with only enough detail
  to support meaningful play. Add specificity when player attention makes it
  useful or causal integrity requires it: **specificity is earned by relevance
  or causal necessity.**
- Undefined history is possibility, not permission for convenient retroactive
  plot connections. AI-generated details should often be mundane, unrelated,
  or remain unresolved.
- Resolve offscreen developments at the lowest level of detail sufficient to
  preserve consequential truth.

### Character history and knowledge

- Characters begin as meaningful outlines rather than complete biographies.
  Player-authored, AI-expanded, and AI-generated foundations are all possible.
- Character background history, campaign history, and world history are
  distinct. Campaign continuity belongs to the world and survives protagonist
  retirement, death, or replacement.
- A replacement character inherits the world, not the previous character's
  private knowledge, relationships, or motivations.
- Track character knowledge only where it materially affects play. Do not
  build a detailed player-knowledge ledger. If a human player uses campaign
  knowledge unavailable to the character, a simple DM-style ruling is enough:
  "Your character does not know that." No elaborate in-world explanation is required.

### Truth, belief, and information

Preserve distinctions between authoritative world truth, actor belief/report,
and player/character inference. A clue does not automatically prove its interpretation.

Information may arrive through conversation, observation, documents, rumor,
correspondence, travel, investigation, relationships, or later developments.
A stable truth may have multiple plausible discovery routes. Do not force
discovery merely because a fact belongs to an important arc.

### World developments and playable situations

A world development is something that becomes true. A playable situation is
a development or condition instantiated so the player can meaningfully engage
with it. Many developments should never become player-facing situations.

New unrelated situations and people may originate independently of existing
arcs. Connections should develop only when actual causality supports them.
Do not maximize connectivity or draw everything into the "Main-Quest Magnet."

### Progressive narrative commitment

Generative freedom exists before commitment. Once accepted, facts constrain
future generation. Delay unnecessary specificity when flexibility is useful;
once accepted evidence or consequences depend on hidden structure, commit
enough hidden truth to keep causality honest.

Do not retroactively determine core mystery facts merely to match the player's
theory. Do not rescue weak or contradictory AI proposals by inventing additional
unsupported facts to justify them.

Conceptual shorthand, not a new implementation protocol:

**propose → check → commit minimum necessary truth → persist → constrain future generation**

### Deterministic engine and AI GM

The established authority boundary remains: the deterministic engine owns
authoritative truth and persistence, including World State, accepted actions,
committed consequences, history, discoveries, integrity constraints, and
canonical constraints. AI/provider output is untrusted and non-authoritative;
provider behavior fails closed. Persistent changes preserve atomicity and
save compatibility under existing project safeguards.

Within that boundary, the AI GM may judge relevance, develop trajectories,
originate independent developments, propose opportunities, instantiate candidate
situations, propose plausible actor behavior and information delivery, and
narrate accepted outcomes. This describes permissible reasoning, not a claim
that these capabilities exist or authorization to build them.

The AI must not silently rewrite history, contradict canonical truth, expose
hidden truth as character knowledge, directly mutate authoritative World State,
connect unrelated arcs merely for neatness, or repair legitimate player failure.

### Proportional GM quality

The goal is not an objectively perfect AI GM. Human GMs are imperfect, biased,
inconsistent, and sometimes railroad; ordinary imperfect judgment is acceptable.
Prevent or reduce systemic failures that damage agency, causality, continuity,
consequence, or campaign credibility. Do not engineer machinery for every
possible bad GM decision. Add review/validation complexity only when
demonstrated failure modes justify it.

### Anti-patterns

| Anti-pattern | Failure to avoid |
|---|---|
| Main-Quest Magnet | Pulling all encounters and discoveries into the apparent main arc. |
| Campaign Rail Recovery | Steering the player back onto an abandoned planned path. |
| Protagonist-Centered Reality | Making world events depend on the protagonist's presence or needs. |
| Universal Simulation | Modeling everything regardless of consequential relevance. |
| Premature Generalization | Building reusable machinery before repeated evidence warrants it. |
| AI Authority Leakage | Treating generated proposals as authoritative state or history. |
| False Certainty | Presenting belief, rumor, or inference as established truth. |
| Content Flooding | Crowding out attention and quiet play with continual new situations. |
| Architecture as Product | Valuing technical completeness over the experience enabled. |
| Convenient Overconnection | Linking independent material without causal support. |
| Consequence Reset | Casually undoing established losses, commitments, or outcomes. |
| Proposal Rescue by Unsupported Facts | Inventing facts to justify a weak or contradictory proposal. |
| Major-Arc Proliferation | Stacking epic threats that compete for foreground attention. |

### Decision tests for future designs

- [ ] What player-facing story problem does this solve?
- [ ] What demonstrated situation requires it?
- [ ] Can existing mechanisms solve it honestly with less complexity?
- [ ] Does it improve agency, consequence, continuity, character engagement,
      discovery, or coherence?
- [ ] Are we modeling something because it matters or merely because it exists?
- [ ] Are we preserving flexibility or prematurely committing future content?
- [ ] Does it respect established truth/history?
- [ ] Would it remain useful if the player abandoned the apparent main arc?
- [ ] Are we generalizing after repeated evidence or from one example?
- [ ] Is implementation complexity proportional to the experience enabled?

## Part II — PROVISIONAL AI-GM reasoning model and context

### Working reasoning jobs

These are reasoning responsibilities, **not authorized software components**:

1. **Interpret relevance:** What deserves attention now?
2. **Develop trajectories:** What plausibly changes independently of direct
   player involvement?
3. **Originate independent novelty:** What plausible new people, events, or
   situations might arise without connection to existing arcs?
4. **Decide whether anything should become player-facing:** "Nothing new" is valid.
5. **Instantiate a bounded situation:** Generate only enough participants,
   facts, uncertainty, stakes, approaches, and possible consequences to support play.

### PROVISIONAL bounded context

Likely context includes the current character outline, relevant character
knowledge, consequential recent campaign history, current circumstances,
relevant authoritative world truth, relevant hidden GM truth, only trajectories
that deserve consideration, recent player engagement/disinterest, and necessary
canonical constraints. Hidden GM truth does not thereby become character knowledge.

Reject the assumption that every AI call should receive full campaign history,
every NPC, every active or dormant threat, all lore, or an exhaustive character
biography. Context selection itself affects narrative quality. The useful
selection and limits remain provisional and require experiments.

## Part III — Working hypotheses requiring experimentation

### Proposal self-critique

Current hypothesis for ordinary AI world-development proposals:

**proposal → brief self-critique → structural/integrity checks → commit**

Higher-consequence developments may deserve a deeper reconsideration pass.
Test whether this improves play and integrity before adding machinery. Do not
introduce a separate reviewer architecture yet. This is a conceptual proposal
discipline, not authorization for new validation code or a new acceptance pipeline.

Before accepting a proposal, ask conceptually:

- Does it contradict established truth?
- Does it depend on knowledge the actor does not have?
- Is the magnitude proportionate to the cause?
- Does it connect independent material merely for convenience?
- Does it make the world revolve around the protagonist?
- Does it protect the player from legitimate failure?
- Does it introduce another major arc unnecessarily?
- Could the fact remain less specific until needed?
- Does anything actually need to happen now?
- Am I inventing additional facts merely to rescue a weak proposal?

Experiments should establish whether the reasoning jobs, context choices, and
self-critique depth help actual play. Their packaging, frequency, and software
realization remain open; no future architecture follows from these hypotheses.
