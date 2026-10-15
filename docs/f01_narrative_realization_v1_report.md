# F01 Narrative Realization V1 — first bounded implementation candidate

Owner supplied the complete authorization directly in the Codex conversation on
October 15, 2026. This report records implementation, not owner acceptance.
Baseline/parent HEAD: `05bae5dc8504b00740f28be82e500155f39b42c1`.
Branch: `codex/f01-narrative-realization-v1`. Uncommitted working diff; no Git
staging, commit, merge or publication authorized. Lifecycle remains active.

## Implementation and reuse

`engine/narrative_realization.py` provides a stateless `realize(context, generate)`
entry point. Its explicit local input shape carries focus, intent/method/
authorization/constraints, current developments, relevant semantic continuity,
knowledge limits, unresolved matters and boundaries. Each meaning retains
authority, epistemic status, source, temporal meaning and legitimate access.
This representation implements this bounded seam; it is not a new accepted
universal information contract or a demand for upstream representation changes.

The component builds one request and validates returned prose using the existing
output validator. Provider generation is explicitly injected and reuses the
existing bounded no-retry transport, with 2,048 output tokens for this adapter.
Malformed context/output or generation failure returns an unavailable result
with no fictional outcome, raw exception, retry or state mutation. A successful
result is labeled `candidate`, never semantically accepted. There is no hidden
engine, transcript, world-state access, persistence or default network call.

Existing `resolved_narration.py` was examined: its accepted-result separation and
transport are useful precedents, but its failed-TRACK-only preparation shape is
not reused as a universal architecture. Scene narration was examined; its
perception-snapshot renderer does not cover this input scope. Existing gameplay
routes and experimental historical code are preserved. No upstream adapters or
gameplay integration are claimed.

## Fixtures and information authority

`test_fixtures/f01_connected.json` contains one connected sequence and evaluation
anchors. Each context is predetermined authoritative fixture material, not a
claim of implemented upstream suppliers. A resolves a conditional climb with
failed early hazard recognition, competent recovery, unharmed completion and
two-minute cost. B supplies a guard's report of Mara's yesterday sighting and
explicit lack of onward-route knowledge. C establishes visible scheduled gate
closure, its passage consequence and the guard's explanation. D continues the
same scene with a relevant alternative-exit question and an unresolved answer.

Player actions are explicitly authorized; the fixtures supply no authority to
choose travel, invent routes or make commitments. The guard's pending answer
does not become a refusal or promise. Ordinary expression is permitted without
turning inconsequential texture into consequential knowledge. Relevant semantic
continuity is supplied independently for each moment; generated text is never
promoted into character knowledge.

Governing design: accepted F01-D1–D10 at the baseline. Supporting evidence:
`D:/AI RPG/.artifacts/narrator_eval/F01-controlled-20261015/` — report, all nine
outputs and provenance assessment examined without modification. M-level inputs
were provisionally sufficient in those samples; additional context was not
consistently beneficial. That evidence neither proves current runtime quality
nor authorizes narration to supply missing NPC knowledge.

## Verification and evaluation status

Changed Python syntax checks pass. `test_narrative_realization.py` passes five
focused groups: all four exact context transfers without mutation; malformed
provenance/authorization/extra data rejected before generation; output failures
and sanitized single-attempt provider failure; stateless reuse/copy isolation;
and one-call provider-adapter delegation. All use offline doubles. A deliberate
false prose example passes shape validation, explicitly demonstrating its limits.

Nearby regressions pass: `test_narration_output.py`, `test_narration_source.py`,
`test_openai_responses_narration.py` (fake transport). No full-suite expansion.
Lifecycle validation: 7 passed, 0 failed. Worktree preflight: 20 passed, one
expected dirty-tree warning, no failures. The existing official environment is
exposed through a worktree `.venv` junction; no interpreter replacement or ACL
changes were made.

`tools/evaluate_f01_realization.py` validates and preserves all four exact
requests and anchors under `.artifacts/f01-realization-evaluation/prepared_inputs.json`.
It records baseline, fixture/component SHA-256 and exact instructions/input.
Without `--live` it makes no calls and fabricates no narrative output. With
explicitly authorized `--live`, it permits one A–D pass, refuses overwrite of a
started pass and stops on unavailable output without retry. Successful text is
preserved in `live_ledger.json` for contextual assessment, not auto-scored.

The owner subsequently authorized the planned evaluation. Exactly four calls
completed, one for each moment, with no retries, extra samples or candidate
changes. See the [evaluation findings and complete outputs](f01_narrative_realization_v1_evaluation.md).
Results are mixed: A introduces unsupported guard presence/availability and
leaves early hazard recognition unclear; B preserves the report chain; C conveys
the gate closure; D respects unresolved answer authority but ends mechanically.
No general fidelity or narrative-quality acceptance is claimed.

## Architecture, complexity and limitations

One context-to-generator component and one explicit provider adapter, with no
planner, semantic validator, retry/control framework or new state owner. These
are provisional choices, not findings ruling out alternatives. Routine
risk: isolated read-only presentation, no cross-system gameplay consequences.
Prompt constraints guide generated prose; they cannot ensure semantic fidelity.
Caller data must be legitimately authoritative, player-accessible and sufficient;
shape validation cannot verify these properties. A malicious or mistaken caller
can supply contradictory or unauthorized meaning. No automatic recovery for
player reliance on erroneous prose is implemented or implied.

General memory/recall, context selection, consequential NPC answers, incidental
detail promotion and gameplay reconciliation remain upstream/design dependencies.
They are not prerequisites to this stipulated evaluation. D intentionally tests
honest restraint, not a satisfying resolved NPC response. One short A–D sequence
cannot establish broad reliability or extended-gameplay quality. Owner review
must assess naturalness, useful emphasis, repetition and whether the pending
answer feels appropriate; no automated score substitutes for that experience.

## Documentation reconciliation and preservation

Updated architecture map, Narrative Experience manifest candidate note and current
package/sprint/JSON. Accepted design, doctrines and ADRs need no change: this
candidate selects no new gameplay authority or durable architecture commitment.
System map/other manifests need no change: no new responsibility, relationship,
upstream implementation or persistence capability. Deferred findings need no new
entry: listed limits remain scoped dependencies and existing research limits.

The original checkout, owner save and historical evaluation evidence are
preserved; exact preservation checks are recorded in the ignored preservation
directory. Protected main and candidate HEAD remain at the baseline. No accepted
history, data, save schema, unrelated worktree or shared Git tool/profile changed.
The only intended Git registry addition is this authorized feature worktree and
branch. No next milestone is staged, and no owner acceptance is claimed.

## Next step

The first candidate and authorized A–D evaluation are complete; stop for owner
review. Review A's authority/recognition issues and D's mechanical ending before
considering a bounded correction. No further calls, tuning, second candidate,
architectural expansion, commit, merge or publication is authorized. Lifecycle
remains active awaiting review; no implementation acceptance or closure claimed.
