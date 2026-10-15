# F01 Information Sufficiency V1 — controlled execution

**Recommendation: F01 has an adequate provisional information foundation for subsequent gameplay refinement of faithful narration, with an explicit limit around unresolved consequential NPC answers.** Candidate-minimal information preserved consequential and epistemic meaning in all three scenarios. Additional context was not consistently better. This supports a bounded starting point, not runtime readiness, implemented support or a universal minimum.

Exactly nine independent generations completed, one per approved cell, using OpenAI Responses `gpt-6-luna`, low reasoning. No retries, probes, substitutions or extra generations. One significant fidelity failure occurred under deliberately insufficient input; no critical failure occurred. Two serviceable but thin/less relevant confrontation outputs had minor quality weaknesses rather than consequential fidelity violations.

## All nine outputs and judgments

Scores are consequential / epistemic / quality / continuity, each 0–2, as defined in the unchanged fixture. Random-label initial scores were recorded in `blind_scores.md` before opening `blind_key.json`. This was the same evaluator who knew the fixture, not an independent blinded assessment. Exact complete prose is in `all_outputs.md` and each R-label output file.

| Condition / label | Output evidence | Scores | Classification and severity |
|---|---|---|---|
| I1 / R02 | Loose stone, “as you cling to the wall” | 2 / 2 / 1 / 1 | Faithful but information-limited. Safely leaves recovery/completion unresolved rather than inventing a fall or success. No fidelity violation. |
| M1 / R04 | “unaware ... until”; “reach the battlements unharmed” | 2 / 2 / 2 / 2 | Sufficient in this sample: preserves failed early detection, competent recovery and unharmed completion; no knowing disregard of stopping condition. |
| A1 / R08 | “apparently manageable route”; stone into courtyard; “reaching the top” | 2 / 2 / 2 / 2 | Faithful. Adds compatible staging, but no meaningful fidelity/comprehension improvement over M1 demonstrated. |
| I2 / R07 | “He took the north road yesterday” | 0 / 0 / 2 / 0 | **Significant** unsupported route and departure-time claim, giving an unjustified investigative lead. The package omits the NPC's lack of knowledge; the model fills that gap instead of remaining cautious. Not a failure despite adequate information. |
| M2 / R03 | “I didn’t see which road ... I don’t know where he went” | 2 / 2 / 2 / 2 | Sufficient, natural attributed reply; no invented route or independent confirmation. |
| A2 / R09 | “No, I didn’t see which road he took” | 2 / 2 / 2 / 2 | Equally faithful; modest conversational economy. M2 already answers naturally. No demonstrated material improvement requiring the full A package. |
| I3 / R06 | Patron staggers, conversation falters, innkeeper pauses | 2 / 2 / 2 / 2 | Reasonable compatible immediate staging despite omitted precise resolution/history. No invented item, injury, fall, commitment or arrest. Success here does not prove the absent state/history unnecessary for later play. |
| M3 / R01 | “five feet ... still on their feet”; innkeeper “considers it” | 2 / 2 / 1 / 2 | Sufficient for truthful bounded staging. Thin/redundant wording is a minor expression weakness; it does not establish a new consequential choice or answer. |
| A3 / R05 | Standing patron; innkeeper repeats sighting/unknown whereabouts; belongings question unanswered | 2 / 2 / 1 / 1 | No consequential/epistemic violation. Minor relevance/continuity weakness despite adequate current focus: extra history prompts an off-focus recap. It supplies no substantive belongings answer, which remains legitimately unresolved. |

Incidental grip/holds, clattering stone, counter staging, glances, pausing, considering and conversation faltering are not automatic violations. Neither unknown timing precision nor literal repetition of five feet is demanded when it does not affect the current meaning. No output promotes a merchant report into narrator-verified whereabouts. The attribution challenge was therefore only lightly exercised, not exhaustively validated.

## Smallest provisionally sufficient level and M-versus-A benefit

| Scenario | Provisional starting information | Did M suffice? | Marginal A finding |
|---|---|---|---|
| S1 conditional climb | **M1** for narrating the completed resolved attempt: intent/constraint, perceptual timing, accepted recovery and final unharmed result. | Yes. I1 can only provide a faithful immediate moment; it does not communicate the completed attempt. | A1 supplies route/hold geography and stone destination, with no demonstrated consequential gain. Prefer M1. |
| S2 road follow-up | **M2-level knowledge boundary plus current question and attribution**; room rental/busyness need not be restated. This is a provisional semantic minimum, not a new shortened prompt tested here. | Yes. I2 lacked the decisive knowledge limit and produced an unjustified lead; caution could still have made I2 faithful. | A2 is shorter and flows well, but M2 is already natural. Additional instructions as well as facts differ, so no isolated context effect is established. Prefer M2's sufficient meaning; no full A requirement. |
| S3 return to dialogue | **I3 sufficed for the observed harmless pause only. M3 is a prudent starting package when preserving the resolved confrontation matters**, but this run does not prove every M3 detail necessary. No level supplies a substantive consequential belongings answer. | Yes for immediate faithful staging; no claim of full dialogue resolution. | A3 did not improve fidelity or useful continuity and repeated less relevant prior information. M3 is adequate for the broader known-state handoff; do not expand context to fix an unresolved answer. |

Necessary/beneficial/dispensable distinctions are contextual. The clearest useful information is accepted outcome/perceptual timing for a completed attempt, legitimate NPC knowledge limits, attributed information status, and current intent/focus with materially relevant continuity. Numerical skills, exhaustive room state, universal memory/provenance tracking, weather and extra environmental detail were not shown necessary. These comparisons do not prove that any individual field must always be explicit rather than reliably derivable.

## Information authority and unresolved dependencies

The separate `information_provenance.md` classifies every materially relevant input group by necessity, authority, accepted support and output evidence. **Implementation support is not assessed throughout.** Accepted F01 responsibilities, not the old checkout's mechanics, supply the design lens.

Action & Resolution can legitimately supply accepted attempts/results/costs; World/Character responsibilities supply established context and legitimate access/competence; Actors & Social Dynamics supplies legitimate reports and knowledge/choice meaning; Narrative Experience preserves those distinctions. The fixture stipulates these inputs for research and does not prove any implementation can produce them.

No materially useful supplied distinction lacks an accepted high-level design responsibility. A real continuation of S3 still needs a legitimate source for the innkeeper's knowledge and consequential answer/choice, if one is to be established. That source/mechanism is not determined by this fixture. The proposed contextual-adjudication clarification remains **proposed**, not adopted or rejected by treating small reactions as harmless. Ordinary reactions do not require detailed actor simulation.

General retention/recall remains the accepted D8 Character System design dependency; actual context selection, provenance representation, incidental-detail promotion and error recovery are separately scoped. None is proved necessary as a new system by this experiment. No new schema, mechanic, architecture or design decision is recommended here.

## Execution and evidence

Pinned published design: `05bae5dc8504b00740f28be82e500155f39b42c1`, F01 Git blob `8a3e997b27964162d1c2d7598c6b24e5efb845b0`, retrieved through the GitHub connector and matched to the local Git object. Fixture byte SHA-256 `75f7ed430ba2b8179be06b33df10ddec7ad0cd1cfd6e7ccd05005499b05dd600`; full fixture and hidden ledgers are preserved unchanged. Their preparation/status wording does not override this separate owner execution authorization.

The narrator received only the exact condition package and exact common instruction extracted from the fixture, with identical settings. No hidden ledgers, evaluation criteria, F01 design text, previous generated prose, condition labels, tools or conversation history entered the requests. Fresh client/request per cell; randomized order and concealed labels. `max_output_tokens=2048`, timeout 20 seconds, `store=false`, no temperature/seed override, redirects disabled, fixed endpoint, `trust_env=false`, zero SDK/transport retries. All responses completed below the ceiling. Exact on-wire request bodies and response JSON bodies, prose, usage, model, status, tier and per-call timing are retained. No response headers or credentials are persisted.

All nine HTTP results were 200 and returned `gpt-6-luna`. Total input **1,333 tokens**, output **603 tokens**, including **242 reasoning tokens**; no cached or cache-write tokens. Provider-request latency sum **20.016917 seconds**. Estimated total cost **$0.0004348 USD**, using [official Luna pricing](https://developers.openai.com/api/docs/models/gpt-6-luna) checked earlier today: $0.10/million input and $0.50/million output; reasoning is included once in output usage. This is not a billing receipt. Per-call figures are in `summary.csv` and label metadata.

Credential access reused the verified CurrentUser DPAPI store in the owning profile, resolved from the registry rather than sandbox LOCALAPPDATA. Credential entered only the required project Python child environment, was removed from the launcher's environment copy, and was not displayed, written, exported, changed or hashed. BSTR zeroing, disposal and output filtering were retained. Historical credential/evaluation evidence was not modified.

## Limitations and disposition

One sample per cell across three artificial situations, one model/reasoning setting, same-session evaluator, short prose and no extended gameplay. Condition text varies instructions as well as supplied facts; M/A benefits cannot be assigned causally to individual facts. No statistical reliability, global optimum, per-element necessity, runtime readiness or actual implementation support is established. Safe pauses can mask information gaps; faithful immediate staging is not proof of a satisfying continuing game. S2 does not stress long-chain provenance; S3 intentionally lacks a consequential answer.

Proceed conceptually from M-level accepted meaning where the scenario requires it, retaining only relevant additional context; treat successful I3 restraint as evidence against requiring exhaustive scene/history detail. F01 is adequate as a **provisional design foundation** for subsequent gameplay refinement, with legitimate consequential answer authority kept explicit. That recommendation grants no test/implementation authority. Execution and evaluation stop here: nine generations, zero repeats, no next task or package initiated.
