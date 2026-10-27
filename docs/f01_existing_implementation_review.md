# F01 existing implementation review and proposed approach

October 15, 2026. Read-only review of existing implementations and preserved
evidence, measured against accepted F01-D1–D10 and the owner-supplied handoff.
Historical acceptance/rejection identifies provenance, not design fitness.

## Timing and status

The mandatory review instruction arrived after a small uncommitted candidate
had been implemented and offline-tested in the isolated worktree. No live
candidate evaluation, gameplay integration or owner acceptance has occurred.
No further substantive code changes were made while performing this review.
The assessment below precedes any further implementation and treats that new
candidate as provisional alongside the older alternatives.

## Candidate assessment

| Existing component | Disposition | F01 fit and bounded reason |
|---|---|---|
| `narration_source.request_narration_text` | Reuse unchanged | Already supplies one explicit stateless bounded provider call, disabled retries, nonpersistent request and sanitized failures. Suitable for arbitrary validated context/instructions. It provides transport safety, not consequential/epistemic fidelity. |
| `narration_output.validate_narration_output_packet` and output identity constants | Reuse unchanged | Prose-only structural boundary without simulation authority. Explicitly does not establish semantic truth; no new validator framework is justified. |
| `resolved_narration.realize_with_provider` and its instructions | Adapt the realization pattern; reuse transport/output utilities | Already a stateless realization call. Most rules preserve selected meaning, knowledge, agency and costs. Its `intermediate` wrapper and Revised A preparation contract are not required for fixture-supplied already-selected authoritative context. F01-specific conditional intent, temporal/provenance and dialogue limits still need adequate input and evaluation. |
| `resolved_narration.build_track_source`, local preparation and local renderer | Exclude from F01 execution; preserve existing routes | Explicit failed-TRACK/outcome/hour assumptions do not cover four different moments. Generalizing the entire pathway would add upstream/scenario work. Local text manipulation is not demonstrated general realization. |
| Revised A `validate_revised_a` and content/plan representation | Available alternative; do not require a new planning stage | Supports qualified meanings/context/boundaries, but mandatory per-meaning plan references add no demonstrated value when fixtures already supply the current focus and developments. Existing structure can carry F01 semantics in text; its historical acceptance does not make it mandatory. |
| `scene_composition` | Reuse design pattern, exclude scenario machinery | Separates selected facts, relevant information and boundaries, with copied data and fail-closed adapters. Builders depend on scene projections, opportunities and refresh selection unnecessary for upstream-independent fixtures. Local realization mostly joins supplied text; not evidence of flexible natural narration. |
| `scene_narrator`, `narration_context`, `narrative_projection`, request/prompt/preview pipeline | Preserve unchanged; exclude from new fixture path | Useful established player-safe projections and deterministic presentation, but tied to existing world/region/scenario data and packet identities. They do not supply arbitrary fixture NPC knowledge or general accepted outcomes. Reusing the entire pipeline would require adaptation with no demonstrated benefit to this bounded test. |
| `SceneContinuity.remember` and experimental prior-prose memory | Exclude from new path | Retains generated sentence excerpts; presentation comparison can be useful, but it cannot establish character knowledge or truth. Earlier report-to-observation contamination makes generated text a poor authority source. Caller-supplied semantic continuity satisfies this task without general memory. This does not require changing existing gameplay routes. |
| Narrative Expression V1 direct single-call and structured-input experiments | Adapt semantic organization and narrative intent | Established context, current action, new development, character knowledge and boundaries are a close fit. They allow incidental expression without consequential authority and avoid prior generated prose as truth. The scripts themselves include experiment-specific freezing, credentials, snapshots and campaign logistics; copying whole runners would not produce a smaller reusable runtime component. |
| Historical multi-sample evaluation tooling | Reuse evidence lessons and exact-input preservation; exclude campaign machinery | Inputs/outputs and provenance must be inspectable. Blind labels, comparison arms, scoring campaigns, extra samples and model sweeps are not required for the single A–D candidate evaluation. |
| New uncommitted `narrative_realization.py` | Retain provisionally as the small direct-call candidate | Uses the reusable transport/output utilities above. Its local field checks are shape checks, not an accepted universal schema or proof that every field must always be separately stored. It has no demonstrated semantic or narrative-quality advantage yet. |

## Evidence inspected and implications

- `D:/AI-RPG-Archive/2026-10-22-housekeeping/files/C/tmp/AI-RPG-Sprint-10.82-Live-20261008-01a118fb/evaluation_report.md`
  (originally `C:/tmp/AI-RPG-Sprint-10.82-Live-20261008-01a118fb/evaluation_report.md`;
  archived October 22; location corrected October 27 without changing findings):
  21 structurally valid outputs with unchanged state nevertheless included one
  critical and eight additional significant fidelity violations. Guard reports
  became observation; uncertain watcher positions became fact. Deterministic
  core plus generated restatement also duplicated material. Neither hybrid
  display nor unchanged simulation proves truthful player understanding.
- `C:/tmp/AI-RPG-Narrative-Expression-V1/remote_review_report.md` and
  `...-Continuous/remote_review_report.md`: direct generation supports readable
  prose and connected supplied semantic history, with remaining material/minor
  failures, tense changes and unnecessary uncertainty/end-state summaries.
- `C:/tmp/AI-RPG-Narrative-Expression-V1-Structured-Input/`: inspected execution
  source, exact request, contexts 1 and 8, report/comparison and moment-8 prose.
  The report describes eight completed calls, four relative improvements, three
  similar moments and one regression. These are local judgments, not proof
  structured inputs always improve output. Moment 8 put a previously handled
  glove back on the ground and introduced vanishing tracks. Separating facts
  from boundaries and excluding prior prose did not eliminate continuity errors.
- `C:/tmp/AI-RPG-Narrative-Expression-V1-Synthesis-20261009-01a1235d/`:
  owner summary and relevant synthesis sections support objective, knowledge,
  resolved progression/outcome and consequences as useful input. They establish
  neither individual field necessity nor an exclusive architectural cause.
- `C:/tmp/AI-RPG-Narrative-Expression-V1-Input-Reduction-Live-20261010-01a1256b/report.md`:
  the runner decoded UTF-8 requests as cp1252, so its exact-instruction comparison
  failed. Its exploratory outputs cannot justify an exact-protocol conclusion
  that reduced inputs outperform full inputs. Explicit UTF-8/exact serialized
  request preservation is appropriate; no rerun is part of this task.
- `D:/AI RPG/.artifacts/narrator_eval/F01-controlled-20261015/`: completed
  sufficiency report, all nine outputs, verification and provenance assessment
  examined. Explicit knowledge limits made M2 faithful in that sample; I2
  invented a north-road lead. Additional A context did not consistently help.
  S3 supplied no legitimate substantive belongings answer at any level. The
  evaluation supports stipulated sufficient context, not new NPC authority.
- Production source inspected includes context/projection, request/prompt,
  pipeline, transport/output, resolved realization, scene composition/narrator
  and continuity. Original dirty-checkout pipeline/prompt were also compared.
  No historical evidence or existing implementation was modified by this review.

## Proposed bounded implementation approach

Use one stateless realization call with explicit, already-selected authoritative
fixture context. Reuse existing transport and output validation unchanged.
Adapt the experiments' meaningful separation of new developments, relevant
semantic history, character knowledge and boundaries. Preserve player intent,
method, authorization, constraints, results/costs and consequential provenance
in the supplied meaning. Do not infer a need for a universal schema from the
local Python shape or these experiments.

For this first candidate, omit a preparatory model call, persistent memory,
scene-selection system, semantic judge, retry framework and hybrid duplicate
result layer. This is a provisional choice, not a finding that these alternatives
are unnecessary. Reusing the entire examined implementation would
bring scenario and pipeline dependencies without supplying missing authority.
Reuse of individual utilities and the direct-call realization pattern is the
least complex fit found in the reviewed evidence. This is a bounded technical
choice, not a new accepted design requirement or a claim of superior fidelity.

The owner accepted this assessment as a provisional implementation choice, not
a final architectural decision. Alternatives remain available if evaluation
exposes material limits. The existing small candidate remains provisional.
Continue only with the authorized A–D sequence and checks. Inspect actual output
against costs, conditional intent, source chains, known/unknown distinctions,
causal continuity, relevance, naturalness and unnecessary repetition. Do not
add samples or tune the candidate after evaluating its first pass. Four live
calls required separate explicit provider authorization, subsequently granted
and fully used. See [the completed evaluation](f01_narrative_realization_v1_evaluation.md).
Offline doubles are not evidence of narrative quality. No scope expansion or
new material design decision was identified by this review.
