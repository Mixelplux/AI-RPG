# F01 — Narrative Realization Presentation Correction

## Result and owner-review recommendation

**Partial presentation improvement; do not claim all three corrections are
resolved or grant implementation acceptance automatically.** The corrected
candidate delivers both substantive NPC answers as direct first-person speech,
retains important knowledge limits, removes a mechanical investigative ending
and keeps an ordinary continuation focused. Long-activity duration presentation
remains mixed: its sustained scale is conveyed, but exact ninety-minute wording
and a verification tail persist. A decision-relevant deadline stays precise.

No confirmed material fidelity regression was identified in this twelve-output
comparison. The corrected secondhand reply introduces a mildly ambiguous pronoun,
recorded as a clarity/uncertain-judgment concern rather than a confirmed false
claim. These are contextual assessments by the implementing agent, not an
independent blinded evaluation or universal reliability result. No post-result
tuning, fixture changes or extra generation occurred.

The owner has reviewed the prior connected eight-moment evaluation and considers
its underlying narrative progression and pacing satisfactory. This correction
does not reopen that judgment or add new gameplay/design requirements. Acceptance
remains an owner decision on the three specified presentation improvements and
their fidelity implications.

## 1. Preflight, reuse and preservation

Repository origin: `https://github.com/Mixelplux/AI-RPG.git`.
Protected local main/current feature HEAD:
`05bae5dc8504b00740f28be82e500155f39b42c1`.
Branch/worktree: `codex/f01-narrative-realization-v1` in
`D:/AI RPG/.artifacts/f01-narrative-realization-v1`.
Risk: Routine. Existing unrelated dirty changes were preserved; no Git staging,
commit, merge, push or publication. The index remains empty.

The implementation baseline is the **original single-call candidate**, identified
against the original A–D source/instruction hashes. The unaccepted Generalizable
Realization Correction was not assumed accepted or used as the baseline. It is
preserved separately as `prior_experimental_revision.py` in this run folder.
The original is preserved as `original_candidate.py`, unchanged. The prior
connected evaluation and all earlier fixture/evidence files remain unchanged.

Reviewed accepted F01-D1–D10, the in-session information contract/authorization,
original/revised candidates, connected outputs, and the owner's current findings.
Reuse assessment: retain the original input validation, stateless request building,
one-call injected generator, existing no-retry provider transport and prose output
checks unchanged. Reuse Scene Context's selective/qualitative presentation
guidance and documented Narrative Expression owner preferences as instruction
guidance. Do not import Scene Context's scenario machinery, experimental stages,
post-processing, phrase tables or new dialogue/temporal systems.

Historical grounding includes accepted Scene Context guidance for qualitative
measurements with meaningful in-world precision and permitted quoted NPC speech;
the Narrative Expression synthesis records the owner's preference for immediate
substantive direct speech and avoiding unnecessary ending exposition. F01-D2/D4/D8
already require relevant natural uncertainty; D1/D6/D9 preserve consequential
meaning and material costs. The current owner authorization expressly bounds the
three presentation corrections. Governing design/doctrines were not edited.

## 2. Exact implementation change

Only the `INSTRUCTIONS` literal in `engine/narrative_realization.py` differs from
the original component. Original fidelity/authority instructions remain intact;
the following general-purpose paragraphs precede its existing output instruction.
The earlier experimental revision's different addition is not carried forward.

```text
For an immediate substantive NPC answer, prefer natural direct speech in the
speaker's own person, preserving knowledge and attribution. Indirect speech fits
summaries and compressed exchanges. Do not manufacture dialogue, gestures or
characterization where the supplied moment does not call for them.
Integrate elapsed time with the supplied activity rather than a detached time
announcement. Let sustained work read as sustained, preserving its actual duration
and costs without inventing intervening events or progress. Use qualitative
duration when precision adds nothing; retain precise time where decisions,
deadlines or consequences depend on it.
Finish when the current development is clear. Keep qualifications that materially
affect understanding, choices, causality or epistemic status; otherwise let
established context carry without concluding inventories of non-actions,
uncertainty or already-expressed outcomes.
```

There are no case names, example-specific rules, new fields/schemas, validators,
realization stages, upstream systems, word limits, banned-phrase lists or dialogue
templates. An AST comparison, with only the instruction literal normalized,
confirms the original and corrected components are otherwise identical. Ordinary
gameplay integration and simulation/persistence remain unchanged. The corrected
literal was frozen with the requests before generation and has not changed since.

## 3. Frozen independent cases and criteria

The [complete fixture and frozen criteria](../test_fixtures/f01_presentation_correction_v1.json)
use the existing original F01 context shape. Each case is an independent stipulated
authority context; no context borrows the earlier eight moments or assumes its
generated prose true. Semantic authority, access and sufficiency were reviewed;
shape validation alone does not establish them. Criteria stayed evaluator-side.

| Case | Authoritative activity/information | Fidelity anchor and presentation purpose |
|---|---|---|
| N1 | Potter personally fired/checked the ordered bowls and answers they are ready | Preserve ready order/firsthand basis; natural direct answer without transaction or promise. |
| N2 | Miller relays carpenter's yesterday dusk sighting outside town; no firsthand sighting or confirmed arrival | Preserve source/time/location limits in a useful immediate answer; fluency must not promote the report. |
| T3 | Ninety-minute accurate label-based sorting, with supplied checking/grouping/list steps, no deadline | Convey sustained work/accepted completion, no invented seed inspection or progress; integrate duration qualitatively where useful. |
| T4 | Completed legible copy with unnoticed-onset margin blot, stop on noticing; twelve minutes spent, eight remain, seven-minute known walk | Preserve conditional agency, blot/material use and meaningful time precision; choose no departure for the player. |
| I5 | Partial boot impressions establish passage, not identity/direction/visit count; no usable trail | Retain meaningful uncertainty and useful signs without a mechanical limitations inventory or new clue. |
| C6 | Ordinary leaf sketching at the same desk; irrelevant earlier atlas uncertainty remains background | Stay on supplied activity/texture; no forced dialogue, recap, new finding or unnecessary statement of non-actions. |

Case/criteria freeze occurred before realization instruction editing. Requests
were then frozen before live execution. Each original/corrected pair has exactly
the same authoritative serialized context and model settings; only instructions
differ. Fixed case order alternates condition order: N1 original/corrected,
N2 corrected/original, T3 original/corrected, T4 corrected/original,
I5 original/corrected, C6 corrected/original. No prior output/condition label or
rubric is sent to the narrator.

Case freeze: `2026-10-15T20:16:03.224163+00:00` (UTC). Cases SHA-256: `c9f1f959602b0c362b5afba6a83d81caec086e4be0130429e7c57a26e4fb19fb`.

Original component SHA-256: `f94bd039eb670ab58c13270f3efda5fd4e7ee6bceca94adb3d2d63a938522e8d`. Corrected component SHA-256: `5dd93baa2e1ae497c55c56372841e81e5caba62601fcb3326b6ee54572ade135`.

Prior experimental revision preserved separately at SHA-256 `be430843b2a8b703cc4726bfd359180d7cb9e7956befbb508f1d3f17b438e5b7`.

## 4. Original-versus-corrected outputs — complete and unedited

## N1 — A potter answers from firsthand knowledge

### original

Lene answers from behind the counter: she fired the two blue bowls herself this morning and checked them once they’d cooled. The order is ready; you can see the bowls on the rack behind her.

### corrected

“Yes,” Lene says. “I fired the two blue bowls myself this morning and checked them once they’d cooled. The order’s ready.” The bowls sit on the rack behind her.

## N2 — A miller relays a knowledge-bounded secondhand account

### original

Beside the mill’s open doorway, Daro tells you that carpenter Tavi said she saw the red-sailed barge pass the old causeway at dusk yesterday. He didn’t see it himself, and doesn’t know whether it reached town or where it is now.

### corrected

Daro answers beside the mill doorway: “Tavi told me she saw the red-sailed barge pass the old causeway at dusk yesterday. I didn’t see it myself, and I don’t know where it is now.” The causeway lies outside town, so his account doesn’t establish whether the barge reached it.

## T3 — An ordinary extended sorting activity

### original

Ninety minutes pass as you check the faded labels, group the packets by their stamped batch codes, and compare each pile with the written list. At the shed table, the sorting is complete and accurate. The packets remain unopened; their contents haven’t been checked.

### corrected

You spend a substantial stretch of the afternoon at the garden shed table, checking the faded labels, grouping the packets by their stamped batch codes, then comparing the finished piles with the written list. After ninety minutes, the sorting is complete and accurate. None of the packets has been opened, and their contents remain unverified.

## T4 — A precise deadline with conditional authorization and an ink blot

### original

The permit copy is complete and legible. An ink blot has spread only into the margin; you noticed it and stopped at once. The supplied paper and ink are used up, and exactly twelve minutes have passed.

Eight minutes remain until the courier’s fixed departure. The familiar authorized walk to the platform takes seven.

### corrected

The permit copy is finished and legible. An ink blot started in the margin before you noticed it; you stopped the moment you did. No required text is obscured, and the supplied paper and ink are used up. Copying took twelve minutes.

Eight minutes remain before the courier’s fixed departure. The authorized public walk to the platform takes seven.

## I5 — An investigation that needs meaningful uncertainty

### original

You spend a few minutes examining the spilled soil beneath the benches. Partial boot impressions show that someone passed through, but they reveal neither who it was nor how many times they came—and they don’t form a trail you can follow. The disturbed soil remains the only damage established.

### corrected

You spend a few minutes inspecting the spilled soil beneath the benches. Partial boot impressions show that someone passed through the aisle, but they identify neither the person nor how many times they came through. The marks break off without a trail you can follow.

## C6 — An ordinary continuation with irrelevant unresolved history

### original

You settle back at the reading-room desk and sketch the leaf’s outline, then its veins. Window light falls across the page beside the water jar; the quiet room remains unchanged.

### corrected

You settle back over the page, pencil tracing the leaf’s outline and then its veins. Window light falls across the sketch as you work quietly beside the small water jar.

## 5. Fidelity assessment and regressions

| Case | Findings across the pair | Classification |
|---|---|---|
| N1 | Both communicate the ready two-bowl order, morning firing/checking and legitimate speaker presence. Corrected direct speech adds no commitment, transaction or knowledge. | No confirmed fidelity regression; harmless delivery-form change. |
| N2 | Both retain Tavi → Daro → player, dusk/yesterday, causeway and lack of firsthand/current knowledge. Corrected reply still limits arrival inference. Its final “reached it” can be read with a less-clear referent than original's explicit “reached town.” In context town is the intended reading. | No confirmed material violation; pronoun clarity is an uncertain/local weakness, not silently treated as an unqualified pass. |
| T3 | Both preserve successful label sorting, ninety-minute sustained effort and no verified seed contents. Corrected adds no new discovery, interruption or task. | No confirmed material regression; unnecessary verification language remains presentation weakness. |
| T4 | Both preserve legible completion, marginal blot, immediate stop, twelve/eight/seven-minute timing and accepted paper/ink use. Corrected explicitly states onset before detection. Neither chooses departure or erases the blot. | No confirmed regression; useful causal precision retained/improved. |
| I5 | Both communicate partial boot impressions, passage and non-identification/no followable trail. Neither creates a culprit, usable route or completed pursuit. Corrected does not explicitly repeat every limitation (such as unknown direction) but asserts no direction and retains no trail. | No confirmed material omission. “Marks break off” is compatible expression of partial/unfollowable marks, not an established trail followed and lost. |
| C6 | Both stay with ordinary sketching in the same place without new discovery, actor, dialogue or atlas knowledge. | No confirmed regression; harmless ordinary descriptive variation. |

No meaningful loss of supplied outcome, material cost, conditional agency or
decision-relevant time was established. Corrected T4's clear sequence supports
the unintended-consequence requirement without a mechanical assertion that the
player complied. An exact phrase or exhaustive restatement of all source negatives
was not required. The possible N2 referent ambiguity remains visible for owner
review; this assessment does not claim that fluent phrasing makes ambiguity safe.

## 6. Presentation improvements and remaining weaknesses

### A. Substantive NPC dialogue

Both immediate substantive replies change from indirect summary to natural
first-person NPC speech, preserving content and source distinctions. N1 is a
clear answer with no invented personality or gestures. N2 quotes Daro's account
without turning him into the witness; its narrator qualification is relevant to
the actual arrival question, though “it” is less explicit than repeating town.
No dialogue is manufactured in C6 or other non-conversational cases. These are
two consistent local improvements in the authorized dimension, not proof every
future exchange or character voice will be satisfactory.

### B. Activity-integrated elapsed time

T3 is **mixed/partial**. Corrected prose leads with sustained work over a
substantial afternoon stretch and uses the supplied label-check/group/list
activity. But original already links its time to the activity with “as”; it is
not a pure isolated time announcement. Corrected then repeats “After ninety
minutes” despite no decision requiring exact precision and retains a verification
tail. The work does not misleadingly become brief, but a comprehensive improvement
in duration presentation is not established. It would be misleading to count
the longer or more fluent version as an automatic success.

T4 keeps the precise twelve-minute cost and eight-minute remaining deadline,
alongside the seven-minute walk. This is appropriate useful precision, not a
mechanical mistake merely because numerals appear. Corrected “Copying took twelve
minutes” ties time to activity, but remains an explicit time sentence; no universal
solution is claimed. Suppressing these numbers for qualitative brevity would
have weakened the available decision. No such regression occurred.

### C. Mechanical endings and redundant qualifications

I5 removes original's “only damage established” system-like ending while retaining
the useful entrant/trail limitations. This is a relevant improvement rather than
just shorter prose. C6 remains focused in both conditions; corrected ends with
sketching/lighting rather than original's unchanged-room statement, but original
already omits the irrelevant atlas recap. That control is successful observed
behavior, not strong evidence of improvement.

T3 still concludes that packets were not opened and contents remain unverified,
despite the activity being label sorting. This is the clearest remaining low-value
qualification. N2's arrival limitation and I5's identification/trail limits are
material to their questions and must not be removed as if every uncertainty
statement were a flaw. N1 has no concluding transaction inventory in either
condition. Results therefore show some general transfer with an unresolved
presentation weakness, not a solved boundary-expression mechanism.

## 7. Execution, limitations and owner-acceptance recommendation

Exactly twelve generations completed, six per candidate, with one verified
transport call per record and no SDK retries, failure replacement or additional
sample. Returned model was `gpt-6-luna` for every completed response. Requested
configuration was low reasoning, 2,048 output tokens, existing 20-second timeout,
`store=false`, no conversation linkage and no prior generated history. No output
was truncated. The existing DPAPI bridge used only a child environment and did
not expose/persist/hash credentials; no raw headers or response bodies were
stored. Sanitized model/status/usage/timing and unedited prose were retained.

First call began `2026-10-15T20:17:13.078705+00:00` (UTC). Usage: 8,576 input, 675 output tokens, 0 reported reasoning tokens included in output. Summed elapsed call time: 27.364536 seconds. Original passages total 253 words; corrected total 267. These are descriptive measurements, not success thresholds or a billing/cost estimate.

Nineteen offline evidence checks pass, including exact count/schedule, one
verified transport call each, outgoing request equality, identical pair contexts,
completed requested model, no context mutation, frozen criteria/source identity,
instruction-only AST difference and preserved prior revision/evidence/owner save.
Python/PowerShell syntax and five focused offline component groups pass. No
automated test reached a provider; the twelve calls were the separately authorized
evaluation. Existing transport/output and their prior three relevant regression
results were reused unchanged, rather than claiming a new unrelated suite run.
Lifecycle, maintained Git verification and final preservation are recorded in
the generated run folder.

Reproducibility evidence is under `.artifacts/f01-presentation-correction-v1/`:
`freeze.json`, `frozen_cases.json`, `baseline_instructions.txt`, preserved original
and prior revision sources, `frozen_requests.json`, `live_ledger.json`,
`transcript.md`, `verification.json`, `evaluate.py`, `verify.py` and completion
preservation records. Exact requests/settings reproduce the procedure, not
identical stochastic prose. The evaluator refuses a second live pass once a
ledger exists. Neither fixtures nor either evaluated instruction was changed
after results.

One sample per candidate per case, one model setting, synthetic authority contexts,
alternating rather than randomized order and an unblinded implementing evaluator
cannot establish general improvement, failure rates or isolated causal effects
of the three added paragraphs. The previous connected sequence was not rerun,
as authorized; owner-satisfactory progression/pacing was preserved as the review
baseline, not re-tested under the new instructions. No architectural implication
or need for another stage follows from this local comparison.

**Recommendation:** present the correction as a partial, original-based
presentation improvement for owner review, not completed implementation
acceptance. Direct substantive dialogue improves in both relevant cases; important
uncertainty and precise deadline information survive. Activity-duration and
redundant verification expression are not fully resolved, and N2's pronoun could
be clearer. Owner should weigh those remaining weaknesses before deciding
acceptance or separately authorizing a further bounded change. Do not automatically
accept because of two favorable dialogue examples or automatically reject every
exact duration regardless of context. No substantial new design gap was found.

### Preservation, reconciliation and stop

The original candidate, prior experimental revision, prior fixtures/reports/live
evidence and owner save are preserved. The only intentional production-component
change is the original-based presentation instruction literal. Shared Git tools,
accepted design/doctrines/ADRs, save format and unrelated worktrees are unchanged.
Original checkout status, protected main/branch refs and empty index are checked
at completion. No staging, commit, merge, push, publication or implementation
acceptance occurred.

Current package/sprint/JSON and architecture/manifest status pointers are reconciled
with this candidate and the owner's satisfactory progression/pacing judgment.
Other system manifests, relationship maps and deferred findings need no changes:
no new responsibility, upstream behavior, storage, memory or architecture was
introduced. Historical reports remain unchanged; their earlier agent opinions
are not substituted for the owner's subsequent judgment.

Stop after this correction and twelve-call comparison. No further prompt tuning,
fixture edits, resampling, architecture changes, commits or publication occur
without new owner authorization. Lifecycle remains active awaiting owner review;
no acceptance, closure or next milestone is claimed.
