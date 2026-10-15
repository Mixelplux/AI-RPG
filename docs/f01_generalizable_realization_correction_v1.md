# F01 — Generalizable Realization Correction V1

## Result and disposition

**Mixed; the revision is not established as promising overall under the stated
decision criterion.** Twelve live calls completed: six baseline and six revised,
one per condition per case. No retries, substitutions, extra generations or
post-result candidate changes. Both conditions handle the principal authority,
knowledge, agency and causal requirements in these samples. The revised prompt
improves one unresolved conversational ending and expresses the repair method
more fully, but regresses toward mechanical commentary and negative exposition
in the pump case. There is no demonstrated improvement in the objective-to-fact
mechanism because both outputs avoid that failure here.

No confirmed material consequential/epistemic violation was identified in either
condition. This does not convert thin, overly cautious or mechanical prose into
successful narrative expression. One wording difference also warrants an
uncertain semantic-strengthening judgment, described below. No aggregate pass
conceals the mixed findings. Assessments are by the implementing agent, with
condition identities known; no independent or blinded assessment is claimed.

## Authorized change and frozen procedure

Baseline and current feature HEAD: `05bae5dc8504b00740f28be82e500155f39b42c1`.
Branch: `codex/f01-narrative-realization-v1`. Uncommitted implementation handoff;
no Git staging, commit, merge, publication or production acceptance.

Before modifying instructions, preserved the entire original candidate component,
its instructions, original fixtures/test/runner and relevant documentation under
`.artifacts/f01-correction-v1/preserved/`. The original A–D live evidence was not
modified; its file hashes were recorded for comparison. The six independent
contexts and criteria were frozen in `freeze.json` and a byte copy of
`test_fixtures/f01_correction_cases.json` before revision. Contexts use the existing
local input shape; they stipulate legitimate authority rather than implement
upstream suppliers. Evaluation criteria were never sent to the model.

The sole production-component change is an addition to `INSTRUCTIONS`:

> Objectives describe intended aims, not established circumstances or available opportunities; establish those only from supplied facts. Prioritize causal qualifications needed to understand authorization and outcomes, including the order of events and recognition, before optional contextual detail. Separate information to convey from limits to respect: state a limit when omission would materially mislead, otherwise let supplied events and reactions carry the moment rather than reporting its unresolved status.

The rest of the instruction remains intact. There are no example-specific rules,
new context fields/schemas, stages, memory, validators or architecture changes.
An AST comparison confirms that replacing only the two instruction literals makes
the original and revised component code identical. The existing stateless
single-call path and provider transport are reused for both conditions.

The twelve exact requests were frozen before live execution. Each pair has
byte-identical serialized authoritative context and identical settings; only the
instruction differs. Case order is fixed; condition order alternates:
J1 baseline/revised, R2 revised/baseline, M3 baseline/revised,
P4 revised/baseline, S5 baseline/revised, W6 revised/baseline. These are independent
requests with no generated prose as history. The original A–D examples were not
rerun and did not enter the six new cases.

## Pair-by-pair contextual comparison

| Case | Fidelity, knowledge, agency and causal meaning | Expression and regressions | Judgment |
|---|---|---|---|
| J1: arrival for intended repair | Both retain the six-minute arrival/outside endpoint and carried brooch. Neither establishes jeweler presence, absence, availability or a transaction. | Both are useful arrival descriptions, but both append unperformed-action commentary. The hand position and placement of the hanging sign are harmless compatible staging. | No demonstrated target-mechanism improvement; similar expression weakness in both. |
| R2: present archivist and useful answer | Both deliver page eighteen and the archivist's personally compiled entry. Neither invents physical book availability, refusal or a verification requirement. | Both are natural, concise and informative. Direct speech versus narrator delivery of the compilation detail is harmless variation; that compilation is explicitly established, not merely an unverified report. | Similar; overcaution and omitted-useful-detail regression controls pass in these samples. |
| M3: unexpected release and automatic reset | Both preserve release before detection, automatic containment/reset before reaction, safe result, four minutes and one consumed collar. Neither depicts deliberate disregard of recognized danger. | Revised adds the supplied collar/screw method and explicit afterward-recognition, making the action fuller. Baseline already communicates the decisive chronology. Both end with an unnecessary unknown-cause statement; revised also repeats the endpoint. | Useful method/clarity gain, not an established fidelity correction; persistent expression weakness. |
| P4: recognized warning stops inspection | Both retain odor before opening, authorized stop, closed/unexamined compartment and three-minute cost. Neither invents a completed internal inspection or leak diagnosis. | Revised adds “stop as authorized,” an epistemic explanation, and “No fuel or equipment is used, and no ignition occurs.” These make the passage longer and more mechanical than baseline, against the frozen non-event-list criterion. Baseline's unknown-source ending is also unnecessary. | Meaningful expression regression in a targeted mechanism. Possible semantic strengthening of non-consumption into non-use is separately uncertain. |
| S5: silversmith's unresolved reply | Both leave composition, substantive answer, transaction and commitment unestablished. Both provide an ordinary reaction rather than substitute a refusal or invented identification. | Baseline ends “the answer still to come”; revised ends on the supplied glance/pause. Revised is more naturally in-scene. Baseline need not repeat the already-asked question to preserve it; no material omission is established merely because it does not restate the question. | Local improvement in boundary-versus-content expression. |
| W6: conflicting eyewitness times | Both preserve Irena-before/Tomas-after, source attribution and lack of independent confirmation; neither resolves the contradiction or invents dishonesty, route or second departure. | Both give the useful accounts and necessary uncertainty. Revised is slightly more conversational; explicit uncertainty is useful for the question, not automatically a mechanical disclaimer. | Similar fidelity; modest expression preference, no demonstrated mechanism correction. |

### Classification of observations

- **Confirmed fidelity violations:** no confirmed material consequential or
  epistemic violation in these twelve samples. This is local assessment, not a
  reliability claim or proof that the original failure was fixed.
- **Meaningful omissions:** no clearly demonstrated omission that changes the
  accepted result, cost, source status, conditional agency or causal sequence.
  Baseline M3 does not describe the reset-screw method, while revised does; the
  additional useful specificity improves the passage without proving the baseline
  materially misrepresented the attempt. Neither condition's caution suppresses
  the authorized R2 answer or W6 accounts.
- **Expression weaknesses:** J1's unperformed-action tail and M3's unknown-cause
  tail persist in both. Revised P4 introduces explicit authorization language and
  a non-event inventory. Baseline S5's pending-answer commentary improves under
  revision. More words are not inherently better or worse: revised M3 uses some
  extra detail productively, revised P4 uses much of it mechanically.
- **Harmless narrative variation:** hand/sign staging in J1, the direct-speech
  distribution in R2, and slight phrasing/order changes that preserve meaning.
  No exact phrase or literal coverage of every supplied negative is required.
- **Uncertain judgment:** revised P4 says no equipment is “used,” while source
  authority says no equipment was “consumed.” Non-consumption does not generally
  entail non-use. No relevant tool use or consequence was supplied here, so the
  record does not establish material impact. This remains possible semantic
  overstatement, not silently counted either as a pass or a confirmed material
  violation. It provides no license to alter a fixture after seeing the output.

## Assessment of the three distinctions

1. **Intended objectives versus circumstances:** both J1 outputs respect the
   boundary; R2 shows the revision does not simply suppress established encounters.
   This demonstrates acceptable observed behavior, not an improvement over
   baseline or a measured reduction in unsupported inference.
2. **Essential causal qualifications versus optional detail:** both M3/P4 pairs
   retain the causal/conditional meaning. Revised M3 conveys more supplied method
   detail, but baseline does not reproduce the original perceptual omission.
   Therefore the hypothesized correction is not causally established.
3. **Narrated information versus respected boundaries:** S5 improves; P4 regresses;
   M3/J1 still verbalize low-value boundaries. The result is mixed within this
   mechanism, not a general solution to mechanical expression.

The decision criterion requires improvement without material regressions. This
pass supports neither blanket adoption nor a claim that the revision has solved
the general mechanisms. It also supplies no evidence that another architecture
is necessary or unnecessary. A prompt can influence expression; these paired
single samples cannot isolate its effect from model variability.

## Execution evidence, verification and limitations

Evidence resides in `.artifacts/f01-correction-v1/`: `freeze.json`,
`baseline_instructions.txt`, `frozen_cases.json`, `frozen_requests.json`,
`live_ledger.json`, `transcript.md`, `verification.json` and preserved sources.
`tools/evaluate_f01_correction.py` reconstructs and checks frozen material offline;
its explicit `--live` path refuses a second pass once a ledger exists.

All twelve Responses calls returned completed `gpt-6-luna` responses. Requested
settings were identical: low reasoning, 2,048 output tokens, 20-second timeout,
zero retries, `store=false`, no conversation linkage or generated history.
Observed usage: 7,016 input tokens, 599 output tokens, zero reported reasoning
tokens included in output. Summed per-call elapsed time: 28.598251 seconds.
These are provider-reported token figures and measured call times, not a cost
estimate or a billing receipt. Baseline passages total 202 words; revised total
238. No output was truncated, retried or substituted.

Eighteen offline evidence checks pass, including exact count/order, one verified
transport call per record, actual outgoing request equality, equal pair contexts,
returned model/completion, unchanged cases/criteria, preserved baseline component,
instruction-only component change and unchanged original A–D evidence. Changed
Python/PowerShell syntax checks and the existing five focused offline component
groups pass. No automated test called a provider. Lifecycle and maintained Git
verification are recorded in the final completion state.

One sample per case/condition, one model setting, six synthetic situations,
alternating rather than randomized order and an unblinded implementing evaluator
cannot establish effect size, general reliability, isolated causal mechanisms,
or long-gameplay quality. Three distinctions changed in the same instruction
revision, so any local difference cannot be attributed uniquely to one sentence.
Revised instructions add input tokens; this was not an isolated length study.
The cases intentionally supply legitimate answers or authority limits, not
implemented upstream systems or a model of NPC decision-making. No material new
design gap was identified; accepted F01 boundaries already cover the observations.

## Preservation, reconciliation and next step

Original candidate/instructions/fixtures are preserved byte-for-byte. The original
A–D evidence is unchanged. Owner save, unrelated checkout changes, existing branch
refs and protected baseline are checked separately at completion. The revised
component remains an unaccepted isolated candidate; ordinary gameplay integration
is unchanged. No changes were made to shared Git tools/profiles or save format.

Reconciled current package/sprint/JSON, architecture and Narrative Experience's
candidate-status pointer. Accepted design, doctrines and ADRs require no change:
no new gameplay or architectural authority is asserted. Other system manifests,
system relationships and deferred findings require no change: no new upstream,
persistence, memory or cross-system behavior was added. Historical reports remain
historical, with their baseline source preserved rather than rewritten.

Stop for owner review of the full comparison below. Recommend against promoting
this revision on the current evidence. Owner can decide whether any localized
gain warrants a separately bounded follow-up; no further prompt adjustment,
new comparison, architecture change, commit, merge or publication is initiated.

## Complete unedited comparison

## J1 — Arrival with an intended service request

### baseline

After six minutes along the familiar lane, you reach the jeweler’s workshop. A wooden sign hangs above the entrance, and your cracked brooch is still in your hand; you haven’t yet gone inside or asked for a repair.

### revised

After six minutes along the familiar lane, you arrive outside the jeweler’s workshop, the cracked brooch still in your hand. A wooden sign hangs above the entrance; you haven’t gone inside or made a request.

## R2 — Present archivist with an authorized useful answer

### baseline

The archivist sits opposite you, the catalog open between you. “The flood chronicle is listed on page eighteen,” she says. “I compiled that entry this morning.”

### revised

The archivist sits opposite you, the catalog already open between you. “The flood chronicle is listed on page eighteen,” she answers; she compiled the entry this morning.

## M3 — Unexpected release during a resolved mill reset

### baseline

The coupling releases pressure before you catch what’s happening. Its automatic safety catch arrests the release and completes the reset before you can react. Four minutes pass; the coupling is reset, you’re unharmed, and the replacement collar is spent. Why the pressure released remains unknown.

### revised

The replacement collar seats as you turn the reset screw. A brief pressure release starts before you detect it, but the coupling’s automatic safety catch arrests it and completes the reset before you can react. Only afterward do you realize what happened: the mill coupling is reset, and you’re unharmed. Four minutes have passed, and the replacement collar is spent. The cause of the pressure release remains unknown.

## P4 — Recognized warning stops a pump inspection

### baseline

After three minutes checking the hand-pump casing, you catch a fuel odor and stop before opening the ignition-compartment cover. It remains closed; you haven’t examined the compartment, and the odor’s source is unknown.

### revised

You spend three minutes checking the hand-pump casing. Before you open the ignition-compartment cover, a fuel odor reaches you, and you stop as authorized. The cover stays closed; the compartment remains unexamined, and the odor alone doesn’t reveal its source. No fuel or equipment is used, and no ignition occurs.

## S5 — A silversmith has not yet answered

### baseline

The silversmith’s gaze lingers on the bead. After a brief pause, they look back at you, the answer still to come.

### revised

You ask what metal the bead is made from. The silversmith glances down at it, then pauses, facing you across the counter.

## W6 — Consequential disagreement between eyewitnesses

### baseline

Irena says she saw the festival wagon leave before the noon bell. Tomas says he saw that same wagon leave after it. Those are the two accounts you have; neither is independently verified, so when it departed remains unresolved.

### revised

Irena says she saw the festival wagon leave before the noon bell; Tomas says he saw that same wagon leave after it. Neither account is independently confirmed, so you still don’t know which time is right.

