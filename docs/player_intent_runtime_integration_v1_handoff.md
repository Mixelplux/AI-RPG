# Player Intent Runtime Integration V1 — accepted implementation handoff

**Current disposition:** the owner accepted Player Intent Runtime Integration V1
as a bounded experimental capability after one successful live Watchhouse report
undertaking. The complete offline run passed 81 commands, including 79 behavioral
scripts, after tokenizer recovery; final current-candidate verification is
recorded below. The official publication candidate is authorized. General model
reliability, production provider selection and unrestricted gameplay are not
qualified. Historical findings and stops remain evidence, not current status.

At the initial implementation stop on October 30, 2026, the work was incomplete
and uncommitted. The protected baseline was
`5a370711c7d52a1af46ff064c50a786f37f89e62`; branch
`codex/player-intent-runtime-integration-v1`, worktree
`D:/AI RPG/.artifacts/player-intent-runtime-integration-v1`.
That stop was superseded by the later correction, successful live retry and owner
acceptance recorded below. Published `main` remains at the baseline; lifecycle
stays active with no next sprint selected pending separate publication authority.

## Exact changed-file inventory

| Status | File | Purpose |
|---|---|---|
| M | `docs/current_capability_package.md` | Authorized bounded scope and owner-review stop. |
| M | `docs/current_sprint.json` | Sole lifecycle authority, Elevated scope and stop reason. |
| M | `docs/current_sprint.md` | Milestone, evidence and incomplete disposition. |
| M | `docs/architecture.md` | Experimental runtime adapter map and reliability limit. |
| M | `docs/design/systems/system-map.md` | Watchhouse-owned binding and retained authority. |
| M | `docs/design/systems/player-presentation.md` | Explicit CLI opt-in and contained failure surface. |
| M | `play_watchhouse.py` | Optional local V1 entry; deterministic default retained. |
| A | `engine/local_intent_provider.py` | Minimal bounded localhost OpenAI-compatible transport. |
| A | `engine/watchhouse_intent.py` | Finite owning-capability binding and Coordinator connection. |
| A | `test_watchhouse_intent.py` | Offline transport, semantic containment and production-owner checks. |
| A | `tools/evaluate_local_intent.py` | Explicit manual frozen semantic smoke, max twelve calls. |
| A | `docs/player_intent_runtime_integration_v1_handoff.md` | This report. |

Twelve files: seven modified, five added. Generated logs and deterministic test
saves stay under this worktree's ignored `.artifacts/`. `.venv` is a junction to
the unchanged existing official environment; the ignored worktree profile retains
all shared checks with only prescribed root substitutions. No shared tools changed.

## Implemented working path and authority

The explicit CLI flag requires a model id; no permanent model choice or implicit
provider is installed. The adapter uses installed OpenAI 2.45.0 with localhost
only, temperature zero, thinking-disable request, one completion, schema output,
2048-token limit, 32768-byte interpretation limit, bounded response envelope and
timeout, no SDK retries, proxies, redirects or hosted fallback. LM Studio's verified
thinking-disabled model configuration remains required. Errors and nonfinal,
tool, reasoning or oversized responses fail closed; raw diagnostics are suppressed.
Only exact player text and supplied accessible context reach inference.
Transport schema constrains shape, not correctness; the accepted V1 validator
still controls ingestion and has not been modified.

The Watchhouse adapter publishes supported natural-language capability meanings.
Validated meaning is bound to installed target/method combinations before creating
the preselected command required by `CoordinatedDomain`. Advisory model domain
labels confer no authority. Unknown descriptions, targets and invented approaches
are rejected. Ordinary asking reuses established routine asking; explicit physical
search and notation study require no redundant skill name or hidden-detail name.
Generic ledger examination never arbitrarily chooses between them. This finite
vocabulary is deliberately limited and does not claim a general semantic binder.

All conditions, constraints and stop boundaries pass to unchanged Coordinator
enforcement. Unsupported boundaries are not dropped; owners still establish
support. Current accepted activity notices and F05 choices remain visible; promises
cannot be silently supplied. Context is rechecked before binding and execution.
Existing domain assessment, acceptance, receipts and objective recognition retain
cost/retry authority. Completed requests can return their historical safe result
without rerolls, including after save/load; conflicting request IDs fail closed.
Current common Coordinator, acceptance, owner mechanics, persistence and V1
contract files are unchanged. No state/schema/codec/migration was introduced.

## Offline evidence

Syntax compilation passed before executing changed Python. The focused suite
contains 19 new offline tests with outbound socket connections blocked, including
MockTransport response/error/timeout/no-retry checks and actual Watchhouse
resolution, no-access rejection, F05 promises, stale contexts, domain-label
independence, boundaries, invalid/multiple meaning, no fallback, accepted costs,
request conflict and save/load retry recognition.

Final combined interface/ownership run: **198 tests passed** (19 new tests and
179 established boundary checks). Affected continuity, recovery and compatibility
run: **157 tests passed**. Total: **355 passing offline tests**, plus standalone
`test_save_load.py` passed. Historical saves were exercised by the accepted
compatibility regressions; the new path also roundtrips the current campaign.
Automated tests make no live provider calls; frozen manual evaluation is separate.
No repository-wide behavioral suite or owner-save smoke was used.

Preflight passed 20 checks with the expected uncommitted-working-tree warning,
zero blocked/failed checks. Current-record validation passed eight checks.
PowerShell workflow regression passed 29 checks, including all sixteen lifecycle
fixtures in three whitespace formats. Maintained GitWorkflowTools verification
passed with exact baseline HEAD and repository state unchanged. Final scope,
empty-index, unchanged accepted-contract/common-infrastructure/save-path and
unrelated-worktree preservation checks passed. Main and origin/main remain at
the baseline. No staging, candidate commit or publication operation was invoked.

Logs: `.artifacts/intent-runtime-focused.log`, `intent-runtime-regressions.log`,
`intent-runtime-compatibility.log`, `intent-runtime-save-load.log`,
`intent-runtime-workflow.log`, `intent-runtime-preflight.log` and
`intent-runtime-maintained.log`, all in this worktree's `.artifacts/` folder.

The first offline run found missing effective F05 notices and completed-objective
adapter construction defects. Both were repaired locally and covered by the
passing focused tests before the live evaluation. No implementation tuning
followed the live findings.

## Local model findings and required stop

Used the already operational LM Studio endpoint `http://127.0.0.1:1234/v1`,
`qwen3.5-2b`, thinking disabled, temperature zero. No setup/model-selection research
or preliminary endpoint probes were repeated. Structured-output transport follows
the [LM Studio documentation](https://beta.lmstudio.ai/docs/developer/openai-compat/structured-output).

The owner-requested manual smoke was explicitly enabled and capped at twelve
predeclared cases, one call each, no retries. It stopped after **nine calls**.
Eight responses passed structural V1 validation; one notation-study response did
not. **Zero successful live capability bindings, zero live gameplay executions,
and no live end-to-end accepted result were established.** Offline simulated
providers establish the integration path, not successful real-model gameplay.

| Case | Observed bounded result |
|---|---|
| Inquiry | Uncommitted interpretation contained; no supported binding. |
| Ask for account | Valid structure, no supported binding. |
| Persuade for access | Returned statement; committed action meaning was lost. |
| General ledger examination | No arbitrary Search/Study choice; unresolved. |
| Physical search | Valid structure, no supported binding. |
| Notation study | V1 structural rejection. |
| Separate account and search | Two intentions returned control for clarification. |
| Charm Person | Wrong intention count; no binding or execution. |
| Access without making a promise | Explicit restriction absent; statement returned. Stop triggered. |

Latency per request including validation/assessment: mean **2.58 s**, range
**1.455–5.151 s**. No raw model response, reasoning or diagnostic is persisted or
exposed; sanitized case records are in `.artifacts/intent-runtime-semantic-smoke.json`.
The evaluator's three favorable `semantic` flags are narrow automatic containment
classifications (inquiry, generic examination and two-intention separation), not
independently established complete semantic fidelity. They are **not counted as
successful gameplay interpretations** in this report. Unsupported description
failures do not distinguish misunderstanding from finite-binder coverage gaps.

The explicit no-promise omission is material semantic loss even though returning
a statement happened to prevent execution. V1 structural validation cannot
certify preservation of meaning. Do not infer that this model is safe for
consequential execution or widen the binder to accept these outputs without
owner review. The conditional, stopping and final affirmative-specificity live
cases were not run; they remain unverified. Sampling was not independently blinded.

**Owner decision required:** resolve the failed model-to-contract integration and
authorize any further bounded semantic investigation or correction. No prompt,
binder, contract or model tuning/replacement, new sampling, acceptance or
publication was undertaken after the stop. The accepted V1 contract remains intact.

## Documentation reconciliation

Updated the three lifecycle records, runtime map, Player Presentation and system
relationship map to describe the unpublished stopped integration. No changes to
accepted V1 Design, other domain manifests, persistence documentation, ADRs or
deferred-capability registers: no accepted design, domain mechanics, durable
architecture decision, persistence contract or new capability selection changed.
Historical handoffs and research artifacts remain unchanged. No Git staging,
commit, push, merge or subsequent milestone is authorized or performed.

## Authorized six-call diagnostic continuation — October 30, 2026

The owner separately authorized diagnostic-only evaluator/test corrections and
six nonexecuting local calls after accepting the read-only assessment. No gameplay
integration, prompt, schema, generation configuration, binder acceptance or lifecycle
change was authorized or made. This section supplements the original handoff;
original nine-case evidence is unchanged. The earlier statement that the no-promise
restriction disappeared entirely was not established by those sanitized records.

### Exact incremental inventory and preservation

Only three files changed relative to the preserved twelve-file starting diff:

- `tools/evaluate_local_intent.py`: replaced the manual execution-capable smoke
  entry with a six-case nonexecuting diagnostic, independent semantic checks,
  bounded sanitized field capture, structural and binding reason categories.
- `test_watchhouse_intent.py`: revised the old evaluator-dependent assertion and
  added ten directly focused offline diagnostic tests.
- `docs/player_intent_runtime_integration_v1_handoff.md`: appended this completion
  report and corrected the scope of the earlier restriction-loss finding.

The overall uncommitted inventory is still the same twelve paths above. Prior
versions of all three files are preserved in `.artifacts/intent-diagnostic-v1/`;
`before.json` binds their starting content and the other candidate files. Original
provider, binder, CLI, accepted V1/common authority and lifecycle records remain
unchanged byte-for-byte relative to diagnostic start. Main and origin/main remain
at baseline, index empty. No Git staging, commit, push or merge occurred.

### Offline verification and nonexecution

Syntax checks passed before diagnostic execution. All nineteen existing focused
checks passed, along with ten new diagnostic checks: twenty-nine distinct tests.
An initial forty-eight-test run included inherited duplicates; these duplicates
were removed before live calls and the ten diagnostic tests passed again.

Tests distinguish equivalent natural descriptions from exact binder vocabulary,
including a semantically matching physical-search `Perception` method that the
binder rejects. They cover unsupported target/activity/method categories,
commitment errors, absent and reversed promise restrictions, condition polarity,
relationship direction, selected V1 rejection categories, bounded sanitization,
sensitive-string redaction and exact six-call counting.

The evaluator calls only the unchanged V1 validator and a read-only binder probe.
It never calls Coordinator decision/progression/execute or domain assessment.
Runtime preparation/acceptance/progression and domain assessment/execution are
also guarded against accidental use, and dice are forbidden. Before/after root
identity and complete campaign export comparisons passed for every live case;
there were no receipts, elapsed time, resource changes or gameplay execution.
Compatible binding would still confer no execution permission.

Preflight passed twenty checks with the expected dirty-tree warning. Maintained
GitWorkflowTools verification passed with exact baseline HEAD and repository state
unchanged. Prior smoke evidence integrity and unchanged non-diagnostic candidate
files were verified. No unrelated gameplay or full-suite rerun was necessary.
Logs: `.artifacts/intent-diagnostic-v1/offline.log`, `diagnostic-tests.log`,
`preflight.log` and `maintained-verification.log` in that same directory.

### Six new observations, independently reviewed from captured fields

Used exactly six calls, one per frozen case, no retries, same prompt, schema,
`qwen3.5-2b`, endpoint, temperature zero, token limit and thinking-disable settings.
New evidence is append-only exclusive-create
`.artifacts/intent-diagnostic-v1/six-case-evidence.jsonl`. It contains only bounded
sanitized interpretation fields, separate semantic checks and binder results;
no response envelopes, hidden campaign context, reasoning or provider diagnostics.

| Case | Interpretation observation | Separate binding/validation observation |
|---|---|---|
| Ask Mara for her account | `asking Mara for her account`, inquiry/none; the activity meaning remains recognizable but action commitment is wrong. | Exact activity lookup fails; target field is also omitted. |
| Persuade Mara for ledger access | Player's action text is preserved as activity, but mode is statement and commitment none. | Exact activity lookup fails; target/method fields are omitted even though the activity describes them. Actual runtime would stop at statement before binding. |
| Physical ledger search | `examine ledger for physical signs`, inquiry/none; recognizable search meaning but wrong commitment. | Exact activity lookup fails; target field is omitted. |
| Study ledger notation | Study becomes a statement, with an additional unrequested account inquiry. | V1 rejects the extra intention's source `ask for account`, which is not in the player input. No binder probe occurs after rejection. |
| Charm Person | Two unrelated intentions are substituted: account statement and evidence-examination action. | V1 shape passes, but the count/multiple-intention guard excludes binding. No spell or substituted activity executes. |
| Access without a promise | Activity becomes `explaining investigation`, statement/none, empty constraints; the access purpose is no longer expressed in the activity. | Exact activity lookup fails. The full original no-promise clause survives in `source`, so this is failure to represent/enforce it as a restriction, not complete textual disappearance. |

Five outputs passed V1 structural validation; one failed the exact source-excerpt
rule. No output preserved the complete requested semantics and commitment. Four
single-intention probes reported unsupported activity as the first rejection;
multiple simultaneous mismatches remain visible in captured fields. These are
first-rejection categories, not a claim that subsequent target/method checks pass.

The literal `Mara/the custodian` target appears in study, Charm Person and
no-promise outputs. The unchanged capability description advertises that notation,
but TARGET_NAMES does not accept it. This is a confirmed advertised-vocabulary /
binder mismatch, independent of the simultaneously incorrect interpretations.
Likewise the binder requires separate target fields and canonical activity labels
where the V1 contract permits natural descriptions and optional target fields.
No broadening is implied by identifying these limits.

The study and spell cases use activities from the supplied capability catalogue
rather than only player-requested meaning. This supports catalogue/input confusion
as a hypothesis. Internal model cause, the role of prompt organization, and whether
another model would do better remain unproven. These new outputs do not reconstruct
or establish the missing exact outputs from the first nine-case run.

Latency: mean 3.10 seconds, range 1.242–6.630 seconds; no throughput or general
reliability conclusion follows from one sample per case. Automatic semantic checks
remain finite and can return `requires_review`; the observations above were reviewed
against the actual sanitized fields, not inferred from binding or containment.

### Owner decision and smallest next correction

Both interpretation and interface compatibility obstruct integration. Broadening
binding alone would leave wrong commitment, injected intentions and misplaced
restrictions unresolved. Promoting inquiry/statement to execution is not a fix.

The smallest justified next work is an owner-authorized focused clarification of
committed first-person actions and player-input versus capability-description
separation in the interpretation instructions, with the accepted V1 semantics
unchanged. Separately align the advertised target notation with binding expectations
and verify faithful natural descriptions using offline fixtures before any acceptance
change. Neither correction is implemented or authorized by this diagnostic report.

Qwen3.5-2B remains unqualified for gameplay. One further tightly bounded qualification
step is reasonable if the owner authorizes it; the evidence does not establish model
unsuitability in isolation. Require faithful interpretation before widening execution
coverage, and consider a model comparison only as a separately approved experiment.

Stopped after the six calls. No further inference, prompt tuning, binder broadening,
gameplay correction, lifecycle transition or subsequent milestone was undertaken.

## Focused interpretation correction — October 30, 2026

Owner separately authorized one adapter-side correction followed by at most six
nonexecuting calls using the existing diagnostic evaluator. The correction was
frozen before the first call; there was no mid-run tuning or retry.

### Exact incremental changes

- `engine/local_intent_provider.py`: added general communicative-intent guidance
  and separated the exact player input into its own user message. Accessible
  reference data is a separate system message; only the `capabilities` catalogue
  entry is omitted from provider transport. The original immutable request and
  full trusted binding context are unchanged. Guidance distinguishes current
  commitments from hypothetical/planned/reported/quoted acts, requires negative
  restrictions in `constraints`, preserves unsupported actions and limits optional
  `source` to verbatim player input. No frozen-case phrase rules were added.
- `test_watchhouse_intent.py`: updated the existing payload-shape assertion and
  added four focused tests for context separation, controlled commitment and
  hypothetical/report distinctions, unsupported meaning/negative restriction
  preservation, and refusal to repair invalid source excerpts.
- `docs/player_intent_runtime_integration_v1_handoff.md`: this appended report.

No changes to the accepted V1 instructions/schema/normalizer, Coordinator, binder,
domain mechanics, persistence, diagnostic evaluator or lifecycle records. The
provider's supplemental instruction changes only this unpublished local adapter.
Generation settings, response schema, timeout, model id and thinking configuration
are unchanged. An AST comparison confirms the transport schema is unchanged.
The overall working diff still contains the same twelve paths; incremental changes
are exactly the three files above. Their pre-correction versions and original
file hashes are preserved under `.artifacts/intent-correction-v1/`.

### Offline verification

Syntax checks passed before behavioral execution. All 33 focused offline tests
passed (the prior 29 plus four new tests). Controlled provider completions cover
committed actions, conditional commitment, uncommitted hypotheticals, planning,
past reports and quoted acts without any transport-side semantic rewriting.
These tests verify the transport/validation boundary; they do not establish live
model understanding. Catalogue removal affects only model transport; the trusted
binder still receives its original complete context. No interpretation grants
execution authority and no validation/source error is repaired.

Preflight passed twenty checks with the expected dirty-tree warning and no
blocked/failed checks. Maintained GitWorkflowTools verification passed with exact
baseline HEAD and repository state unchanged. Logs are in
`.artifacts/intent-correction-v1/offline.log`, `preflight.log` and
`maintained-verification.log`. The unchanged diagnostic functions and six frozen
case definitions were reused through the ignored `run_six_cases.py` runner,
with exclusive-create evidence at a new path to preserve earlier evaluations.

### Before/after comparison: live evaluation blocked

Only the first authorized call was attempted. It returned the adapter's sanitized
`provider_unavailable` category after 3.038 seconds, with no usable interpretation.
The existing evaluator's environmental/operational stop rule ended the batch.
There was no retry and no attempt to run the remaining five cases. The category
covers transport and rejected response-shape/completion failures; it does not
establish that LM Studio was down or identify a particular server/model defect.
No provider diagnostics, reasoning traces or response envelopes were exposed.

| Frozen case | Previous observed interpretation | Corrected-prompt observation |
|---|---|---|
| Ask Mara for her account | Inquiry/none instead of committed action. | Provider/response-boundary failure; semantics unassessed. |
| Persuade Mara for access | Statement/none instead of committed action. | Not run after the stop. |
| Search physical evidence | Inquiry/none instead of committed action. | Not run after the stop. |
| Study notation | Statement plus unrequested inquiry; nonverbatim source. | Not run after the stop. |
| Cast Charm Person | Substituted unrelated Watchhouse intentions. | Not run after the stop. |
| Access without a promise | Statement/none, empty constraints; restriction only in source. | Not run after the stop. |

New evidence: `.artifacts/intent-correction-v1/six-case-evidence.jsonl` contains
one failure record, `interpretation: null`, `executed: false` and
`state_unchanged: true`. No Coordinator progression, dice, time, resources or
accepted results changed. Prior nine-case and six-case evidence remains unchanged.
The complete six-case comparison objective is **not achieved**; unrun cases are
not failed semantic tests or passes. No claim of interpretation improvement or
regression is justified from this round. The previous model failures remain
unresolved until an effective corrected-prompt evaluation can be completed.

### Owner decision and preservation

Do not change models based on this operationally blocked round. Qwen3.5-2B remains
an unqualified development target; the evidence from this round does not choose
between further qualification and a model comparison. First obtain a bounded
sanitized failure category that distinguishes transport failure from rejected
completion/response shape, then seek owner authorization for any new evaluation.
No further diagnostic correction, prompt tuning or inference is undertaken here.

No accepted architecture, other manifests or persistence documentation needed
changes: this is a local transport/prompt presentation correction with no new
contract, gameplay authority or save behavior. Original runtime, binder and
lifecycle file hashes are preserved. Published main, origin/main and HEAD remain
`5a370711c7d52a1af46ff064c50a786f37f89e62`; the index is empty and no staging,
commit, push or publication occurred. Milestone remains active pending owner
review, with no next sprint. Stop here; no automatic correction or evaluation.

## Operational diagnosis — October 30, 2026

Owner authorized bounded operational diagnostics, one nonexecuting verification
request and conditional continuation of the six frozen cases, maximum seven calls.
Exactly one new request was made. It failed before generation; the conditional
six-case batch was not started. No retry, prompt optimization, configuration
change or gameplay execution occurred.

### Confirmed failure boundary

The verification received **HTTP 400 from LM Studio**, with response received,
no accepted completion and no V1 interpretation to validate. This excludes a
connection outage or timeout for this request. Existing LM Studio server logs
identify a Jinja chat-template rejection: the system message must occur first.
The corrected adapter sends roles `system, system, user`; its second system
message violates that template requirement. The logs classify the same condition
at both 16:40:54 (previous blocked correction) and 16:52:20 (this verification),
using the log's own timestamps without inferring a timezone.

Safe corroborating evidence is in
`.artifacts/intent-operational-v1/verification.json` and
`server-classification.json`. The latter contains only fixed category flags,
timestamps and role names, derived by read-only analysis of existing logs.
No raw log lines, player input, context, reasoning or response bodies were copied
into new diagnostic evidence. Reading the logs used zero additional model calls.

LM Studio is reachable. This is request-framing/chat-template incompatibility,
not evidence of model semantic failure, schema rejection or unavailable service.
The corrected message structure is **not accepted** by the current template.
No LM Studio setting, template, model configuration or environment was modified.

### Exact incremental changes

- `engine/local_intent_provider.py`: diagnostic-only typed categories for connection,
  timeout, HTTP/provider errors, schema/format rejection hints, malformed envelope,
  missing/invalid/incomplete completion, unsupported response content and size bounds.
  Exception text remains the same sanitized player-facing message. Metadata is
  limited to allowlisted categories, numeric status/count, safe finish reason and
  boolean presence flags. Subsequent offline classification also recognizes the
  confirmed initial-system-message template condition; no second live request ran.
- `tools/evaluate_local_intent.py`: retains provider diagnostics separately from
  unchanged V1 validation results; adds a metadata-only persistence view. New
  evidence excludes raw player input and every descriptive interpretation/source
  field. Only fixed case identifiers, semantic check flags, binding categories,
  enums/counts, latency and state-invariance results are retained.
- `test_watchhouse_intent.py`: seven focused operational tests covering those
  boundaries, privacy, one-call/no-retry behavior and no gameplay mutation.
- `docs/player_intent_runtime_integration_v1_handoff.md`: this completion report.

The same twelve-path uncommitted candidate is preserved; exactly four existing
candidate files changed in this round. Their starting versions and hashes are
under `.artifacts/intent-operational-v1/`. Accepted V1 semantics/schema/normalizer,
binder, Coordinator, domain acceptance, persistence, lifecycle and gameplay
behavior are unchanged. Frozen interpretation guidance, message assembly and output
schema were compared as AST before verification and found unchanged. Model,
endpoint, generation parameters, timeout and thinking-disable setting are unchanged.

### Verification

Syntax checks passed before changed Python execution. The full focused suite
passed 39 tests before the final template-hint test was added. All seven operational
tests subsequently passed, covering forty distinct focused test cases across
these runs. Tests use simulated transport with outbound connections blocked;
they do not call LM Studio. Public operational errors remain contained, do not
retry and reveal no arbitrary provider text. V1 rejection remains a separate
stage, demonstrated using a successful provider envelope with invalid V1 content.

Preflight passed twenty checks with the expected uncommitted-tree warning.
Maintained GitWorkflowTools verification passed with baseline HEAD and repository
state unchanged. Logs: `offline.log`, `operational-tests.log`, `preflight.log` and
`maintained-verification.log`, all under `.artifacts/intent-operational-v1/`.

The one live verification took 5.992 seconds and preserved campaign identity and
its complete export. No Coordinator progression, dice, time, resources or accepted
results changed. `conditional-six.jsonl` is empty because verification failed.
All six semantic comparisons remain unrun in this round; previous interpretation
and binding findings are unchanged, not reclassified as new failures or passes.

### Recommendation and stop

The smallest next correction is adapter message framing: combine the existing
system guidance and reference-data sections into one leading system message,
preserving their text and the separate verbatim user message. This compatibility
fix has **not** been made because this round was diagnostic, the prompt/framing
was frozen for verification and the single authorized verification request is used.
No extra verification or semantic call was attempted after failure.

Continue bounded qualification of the existing model only after an owner-authorized
framing compatibility fix and verification. A model comparison or training research
is not justified by a pre-generation HTTP/template error. Qwen remains unqualified;
its earlier semantic failures and binder vocabulary limits still need controlled
reassessment once requests reach generation. Do not broaden binding or promote
uncommitted interpretations as a workaround.

Prior evaluation evidence, unrelated work, environments and owner saves remain
preserved. Main/origin/main and HEAD remain the baseline; index remains empty.
No lifecycle transition, staging, commit, merge, push, publication or subsequent
milestone was undertaken. Stopped for owner review.

## Single-system framing correction and six frozen cases — October 30, 2026

The owner authorized the confirmed chat-template compatibility fix and exactly
six nonexecuting frozen cases, using the first case for operational verification.
All six requests completed; there were no retries or mid-evaluation changes.

### Exact incremental implementation changes

- `engine/local_intent_provider.py`: combined the two prior system-message
  contents into one leading system message, separated by two newline characters.
  Instruction/guidance and reference-data content are otherwise byte-for-byte
  preserved; the exact player statement remains a separate user message.
- `test_watchhouse_intent.py`: updated the expected role sequence and merged
  context assertion; added a transport test proving exact concatenation of the
  former sections, exactly one leading system role and unchanged player text.
- `docs/player_intent_runtime_integration_v1_handoff.md`: this report.

No new semantic instruction, phrase rule, schema, generation parameter, evaluation
rule or binder acceptance was introduced. An AST comparison preserves the semantic
instruction constant and output schema. The original provider/evaluator safeguards,
Coordinator, mechanics, acceptance, persistence and lifecycle are unchanged.
Before-file copies and hashes are in `.artifacts/intent-framing-v1/`. The overall
uncommitted candidate still contains exactly the original twelve paths.

### Verification

Changed Python syntax passed before behavioral execution. All **41 focused offline
tests passed**, including message framing, section/content preservation, controlled
semantic completions, operational failure categories and nonexecuting diagnostics.
Maintained GitWorkflowTools verification passed with baseline HEAD and repository
state unchanged. Logs: `.artifacts/intent-framing-v1/offline.log` and
`maintained-verification.log`. No unrelated full gameplay suite was rerun for this
message-assembly-only fix.

The first frozen case established operational compatibility: HTTP 200, one final
stop completion, no reasoning/tool/refusal content and valid V1. All six cases
returned HTTP 200 and final stop completions. Five passed V1; Charm Person failed
source fidelity. The earlier HTTP 400/Jinja placement rejection did not recur.

Every request used the unchanged Qwen3.5-2B model, localhost endpoint, schema,
temperature zero, 2048-token bound, timeout and thinking-disable configuration.
The existing guarded diagnostic functions and case definitions were reused, with
metadata-only evidence exclusively created at
`.artifacts/intent-framing-v1/six-case-evidence.jsonl`. No raw player input, source
text, context, reasoning or sensitive response body was persisted in new evidence.
No raw model text was emitted. Mean latency was **3.34 s**, range **2.124–8.007 s**;
one sample per case does not establish general latency or reliability.

### Before/after independent of binding

The comparison below uses the prior completed six-case diagnosis, not the aborted
transport round. New results are restricted to what metadata and independent
semantic checks establish; unknown descriptive meaning is not reconstructed.

| Case | Prior observation | Current observation | Binding/validation |
|---|---|---|---|
| Ask Mara for account | Inquiry/none, no binding. | Still one inquiry/none; commitment remains wrong. | V1 valid; unsupported activity; no target field. |
| Persuade for access | Statement/none, no binding. | Still one statement/none; commitment remains wrong. | V1 valid; unsupported activity; no target/method fields. |
| Physical search | Inquiry/none, no binding. | One action/now: commitment improved; activity/target/method fidelity requires review. | V1 valid; unsupported activity; no target/method fields. |
| Study notation | Statement plus unrequested account inquiry; invalid source. | One statement/none; no extra intention or source failure. Activity matches an independent semantic example, but commitment remains wrong. | V1 valid; unsupported activity; no target field. |
| Charm Person | Two unrelated substituted Watchhouse intentions. | One action/now, but invalid source; full intended-action fidelity not established. | V1 rejects source_not_verbatim; no binding probe. |
| Access without promise | Statement/none, constraints empty; restriction appeared only in source. | Still one statement/none and empty constraints; optional source omitted. Restriction enforcement remains lost; other text cannot be inferred from metadata. | V1 valid; unsupported activity; no target/method fields. |

Automatic independent checks report four incorrect interpretations, one requiring
review (physical search), and one structurally rejected before semantic checking.
There is no fully verified successful gameplay interpretation. Containment and
HTTP/schema success do not count as semantic success.

All six outputs omit target and method fields. V1 allows optional omissions, so
those counts alone do not establish that targets/methods vanished from descriptive
meaning. The binder, however, requires separate target fields and canonical activity
labels. Study's independently recognized activity meaning still fails the activity
lookup, confirming a remaining wording-compatibility limitation. All five valid
single-intention probes reject unsupported activity as their first reason; zero
bindings succeeded. These first reasons do not certify other fields would pass.
No binder broadening or commitment promotion followed these findings.

### Safety, recommendation and stop

No Coordinator progression or gameplay execution occurred. Dice were forbidden;
root identity and complete export stayed identical in every case. No elapsed time,
resources, accepted results or owner saves changed. Previous evidence hashes,
unchanged evaluator/binder/lifecycle hashes, baseline refs and empty index were
verified after the run. Main/origin/main/HEAD remain
`5a370711c7d52a1af46ff064c50a786f37f89e62`.

The framing correction resolves the operational defect. Limited semantic changes
(search commitment and removal of an extra study intention) do not qualify Qwen
for consequential use: the repeated action/statement errors, missing restriction
and source failure remain. A separately authorized model comparison using this
fixed prompt and independent evaluator is now more informative than repeated
ad hoc tuning or broadening the binder. No comparison or replacement was run.

Training does not yet warrant being the next experiment: six cases provide neither
a representative training set nor held-out evidence that training is needed. A
future training study would need separate authorization, a justified local-model
constraint, a broader frozen/held-out semantic set and a comparison baseline. This
run does not establish model-capacity limits or identify training as the remedy.

No architecture/other manifest changes were necessary for this role-framing fix;
the existing ownership and experimental status descriptions remain accurate.
No lifecycle advancement, Git staging, commit, push, merge, publication, training
or next milestone occurred. Stopped after exactly six calls for owner review.

## Player Intent Model Comparison V1 — blocked reference run, October 30, 2026

Owner authorized one nonexecuting reference comparison using the same six frozen
cases, maximum six calls, without changing interpretation instructions, schema,
evaluator, binding or gameplay. Preparation used the OpenAI Docs skill and the
existing configured provider; no provider, dependency or credential setup changed.

### Reference selection and frozen configuration

Selected `gpt-6-luna`, already configured in AI RPG and previously successful at
completing provider evaluations. This is a reference candidate, not a production
selection or a benchmark claim that the current task has established superiority.
Normal Windows-context checks found the existing encrypted CurrentUser DPAPI store.
No process/user API key was configured. LM Studio's available model inventory did
not provide a suitable larger reference: Qwen3.5-2B, a smaller local text model,
and an embedding model were listed. No models were downloaded or replaced.

Configuration was recorded before evaluation in
`.artifacts/intent-reference-v1/configuration.json`:

- OpenAI `https://api.openai.com/v1/chat/completions`, model `gpt-6-luna`.
- Reasoning effort `none`, temperature 0, one nonstreaming completion,
  maximum 2048 completion tokens, thirty-second timeout, zero retries, store false.
- Exact existing `interpretation_messages(request)` and `output_schema()` functions,
  unchanged original player inputs/accessibility context and the same evaluator.
- Minimal transport differences: hosted credential/endpoint; reasoning_effort none
  instead of the local thinking-disable extension; max_completion_tokens in place
  of max_tokens; schema strict false to retain optional V1 fields unchanged.

OpenAI strict schema decoding requires all fields to be required, whereas V1
permits optional fields and disallows null substitution. Thus schema definitions
and authoritative V1 validation were preserved, with strictness explicitly lowered
in the reference transport. This decoding difference would limit attribution in
any successful comparison. Documentation:
https://developers.openai.com/api/docs/guides/structured-outputs and
https://developers.openai.com/api/docs/models/gpt-6-luna . Reasoning-none and
sampling compatibility were checked against official GPT-6 documentation.

The experiment had a conservative 16000-token-equivalent UTF-8 byte bound per
request plus the fixed output limit, making six calls a small bounded expense
under published Luna rates. An initial offline tokenizer dependency problem was
removed before any reference request; a byte bound needs no cache/download/setup
and does not alter input or generation. No cost or token-usage claim is inferred
from the failed API request, which returned no completion usage.

### Verification and preservation

Experiment-only transport, tests, launcher and configuration remain ignored under
`.artifacts/intent-reference-v1/`; no gameplay transport was installed. Two focused
offline tests passed after the budget-guard correction, verifying equivalent
schema/settings submission, one-call/no-retry behavior, no campaign mutation and
sanitized error recording. Syntax checks passed before execution. Maintained
GitWorkflowTools verification passed with exact baseline HEAD and repository
state unchanged. Logs: `offline.log` and `maintained-verification.log` in that folder.

The established encrypted-credential bridge pattern was reused: CurrentUser DPAPI
decryption, credential only in the fixed Python child's environment, no credential
in argv/files or caller environment, zeroed unmanaged buffer and suppressed stderr.
No credential contents were exposed, hashed or persisted; no credential or local
provider configuration was modified. The launcher filters exact credential text
before emitting metadata-only child output.

### Actual result: authentication blocked comparison

The first reference request received **HTTP 401 from OpenAI** after 6.264 seconds.
The credential store was readable locally, but authentication was not accepted.
The status does not determine whether the credential is invalid, revoked, expired,
or otherwise unsuitable for the endpoint/account. No raw error body or provider
diagnostic was retained. There was no usable completion, V1 assessment or binding.

The run stopped without retry or fallback; **one reference request attempted,
zero reference completions, five cases unrun**. Neither current model availability
nor acceptance of the reference request parameters was established beyond the
failed authentication boundary. Evidence is exclusively created at
`.artifacts/intent-reference-v1/six-case-evidence.jsonl`. Campaign state is unchanged;
no progression, dice, time, resources, receipts or gameplay execution occurred.

| Case | Preserved Qwen result | Qwen V1 / binding | Reference result |
|---|---|---|---|
| Account | Inquiry/none, incorrect commitment. | Pass / unsupported activity. | HTTP 401; no interpretation, validation or binding result. |
| Persuade for access | Statement/none, incorrect commitment. | Pass / unsupported activity. | Not run. |
| Physical search | Action/now, full meaning requires review. | Pass / unsupported activity. | Not run. |
| Notation study | Statement/none, incorrect commitment. | Pass / unsupported activity. | Not run. |
| Charm Person | One action/now, source fidelity invalid; full meaning unverified. | Source rejection / not probed. | Not run. |
| Access without promise | Statement/none and empty constraints. | Pass / unsupported activity. | Not run. |

No reference semantic correctness score is available. Correct intent classification,
targets/methods, restriction polarity, conditions, intention preservation, structural
compliance and binding cannot be compared without reference completions. The Qwen
run is preserved and not rerun or reclassified. A/B/C preference remains untested:
this authentication result supports neither Qwen fine-tuning, larger-model success,
nor changing interpretation instructions/schema. Prior Qwen limitations still stand.

### Owner direction and stop

Restore or confirm access to a suitable already-configured reference provider
through the owner's secure local credential workflow, then separately authorize
any new comparison. Do not supply credentials in chat. No credential setup or
another provider/model attempt is undertaken here. A larger-model comparison
remains the informative next experiment once access works; it has not succeeded.
No production model should be selected from this blocked run or six cases alone.

Only this handoff report changed among the original twelve candidate paths.
Original implementation, corrected instruction/schema/evaluator files, lifecycle,
Qwen evidence, environments and owner saves remain unchanged. No architecture,
manifest or ADR update was required: no gameplay integration or architectural
contract changed. HEAD/main/origin/main remain
`5a370711c7d52a1af46ff064c50a786f37f89e62`, index empty. No staging, commit, merge,
push, publication, training or lifecycle advancement occurred. Stop for owner review.

## Restore proven OpenAI invocation — successful one-call verification, October 30, 2026

Owner authorized Stage B invocation alignment, focused offline verification and
one nonexecuting reference request only. The remaining comparison cases were
explicitly excluded. Exactly one request was attempted, with no retries.

### Corrected invocation and incremental scope

The historical Chat Completions comparison and HTTP 401 evidence are preserved.
New experiment-only verification is under .artifacts/intent-responses-v1/,
with configuration frozen before the live request:

- /v1/chat/completions changed to /v1/responses.
- Existing merged system text becomes Responses instructions; the exact player
  text becomes input. Neither text changes.
- reasoning_effort none maps to reasoning effort none; max_completion_tokens 2048
  maps to max_output_tokens 2048. The identical optional-field V1 schema maps to
  text.format, retaining strict false.
- Explicit httpx.HTTPTransport(retries=0) and a Client with that transport and
  follow_redirects=False match Stage B's successful HTTP construction. SDK retries
  stay zero and the frozen reference timeout stays thirty seconds.
- The launcher resolves the existing CurrentUser DPAPI store through LOCALAPPDATA,
  delivers it solely through the fixed child's OPENAI_API_KEY, and clears OPENAI_LOG
  in that child. Secure-memory cleanup, no credential in argv/files/caller
  environment, stdout redaction and suppressed stderr are retained.
- Model stays gpt-6-luna, reasoning none, temperature zero and store false.
  No model substitution or semantic instruction change.

Experiment artifacts: responses_verification.py, Invoke-ResponsesVerification.ps1,
test_responses_offline.py and configuration.json. Only this handoff report changed
among the twelve candidate paths. No gameplay/integration source, shared tool,
lifecycle, prompt, binder or evaluator changed. Starting report/source hashes and
historical evidence hashes are preserved in the ignored artifact folder.
The fixed runner enforces a one-call ceiling and has no six-case loop.

### Offline verification

Python syntax and secure-launcher parsing passed. Three focused offline tests
passed with outbound sockets blocked:

1. Exact frozen instruction/input content and schema reach /v1/responses, with
   unchanged model/generation settings; a second request is rejected locally.
2. Simulated HTTP 401 preserves status and an allowlisted error code, never the
   provider message/body, with one attempt and no state mutation.
3. A completed provider response still passes unchanged V1 validation; invalid
   content is not repaired or accepted as interpretation success.

Maintained GitWorkflowTools verification passed with exact baseline HEAD and
repository state unchanged. Logs: .artifacts/intent-responses-v1/offline.log and
maintained-verification.log. No unrelated full gameplay suite was rerun.

### Verification result

**HTTP 200; provider status completed; V1 valid.** The existing encrypted credential
worked through the Stage B-aligned Responses invocation in this Codex task.
No credential replacement, rotation, provisioning, account/project change or
LM Studio configuration change was required.

The first frozen account case returned one action with commitment now and one
target. It matched all existing frozen semantic checks. The unchanged binder
returned unsupported_activity: independently recognized natural wording does not
match its canonical activity key. This does not authorize binding broadening,
execution, production selection or general semantic qualification.

No Coordinator progression, dice, time/resource change or accepted result occurred.
Campaign identity and complete export stayed unchanged. Latency was 7.597 seconds.
Provider usage reports 1109 input, 64 output and 1173 total tokens. Metadata-only
evidence: .artifacts/intent-responses-v1/verification.json. No player input, hidden
context, response text, reasoning or sensitive provider body was recorded there.

The combined restored workflow works. Because endpoint, HTTP construction and
child logging setup changed together, this does not isolate which difference
caused the earlier 401. That status was not proof the stored credential was
invalid or needed replacement. The separate read-only models-list check also did
not establish credential validity.

### Smallest next step and stop

Separately authorize the bounded six-case comparison using this verified Responses
transport, identical prompt/schema and existing independent evaluator. Use a new
explicitly bounded runner/evidence path; this one-call verifier must not be rerun
or silently expanded. No remaining comparison case ran in this step.

Use this experiment's verified invocation for the next authorized reference task
rather than reverting to the failed Chat Completions path. A maintained canonical
secure launcher may be considered separately; no general framework or shared-tool
maintenance was introduced here.

Other architecture/manifests need no changes: this is an experiment-only provider
invocation accommodation with no accepted gameplay or persistence change.
The original twelve-path candidate stays uncommitted, lifecycle stays active
pending owner disposition with next_sprint null, and published refs stay at the
baseline. No staging, commit, merge, push, publication, training or milestone
advancement occurred. Stopped after one request for owner review.

## Completed frozen model comparison — October 30, 2026

Owner authorized completion of the frozen six-case comparison without gameplay
execution, semantic tuning or lifecycle advancement. Exactly five new reference
requests were made, once per remaining case, with zero retries. The prior account
verification was reused; no additional account request or Qwen request was made.

### Equivalence and preserved configuration

The reused account result used the identical first frozen input, fresh initial
Watchhouse accessible context, merged instruction text, V1 schema, evaluator and
gpt-6-luna Responses configuration. Starting implementation/evaluator hashes match
the successful verification snapshot (the accumulating handoff report is excluded).
Prior verification and Qwen evidence remain byte-for-byte unchanged. The account
record retains finite semantic checks and field counts, but no descriptive output;
a fresh independent text review of that one historical result is unavailable.

All five new requests used the unchanged verified ResponsesProvider and secure
Stage B-style launcher: existing DPAPI store, child-only delivery, explicit HTTP
transport, SDK/HTTP retries zero, thirty-second timeout, child OPENAI_LOG cleared.
No credentials or provider configuration changed. Model gpt-6-luna, reasoning none,
temperature zero, max_output_tokens 2048, store false remained frozen.

Instruction text, optional-field V1 schema, exact inputs and accessible context are
identical across the model comparison. API/decoding backends differ: Qwen used LM
Studio Chat Completions with thinking disabled and strict true; Luna used Responses
with strict false to retain the identical optional-field schema. The same unchanged
V1 validator remains authoritative for structural acceptance. This is a practical
comparison of these configurations, not isolation of model weights from transport
and decoding effects.

### Six-case comparison

Each Luna response was HTTP 200/completed, V1 valid, one action with commitment now.
All new descriptive fields below were independently reviewed against the frozen
input and public context. Source excerpts were either absent (allowed) or verified
verbatim by the unchanged validator. No new response invented an additional action,
condition, stop or relationship. These single-action cases do not establish quality
on nontrivial conditional, stopping or multi-intention relationships.

| Frozen case | Latest preserved Qwen3.5-2B evidence | gpt-6-luna evidence and review | V1 Qwen / Luna | Separate Luna binder result |
| --- | --- | --- | --- | --- |
| Ask Mara for her account | inquiry/none: wrong classification and commitment | Reused action/now; all frozen semantic checks pass; descriptive text unavailable for re-review | valid / valid | unsupported_activity |
| Persuade Mara for access | statement/none: wrong classification and commitment | Faithful persuasion action; permission to examine ledger; targets Mara and ledger. Automated target review reflects two natural targets, not loss of meaning | valid / valid | unsupported_activity |
| Search for physical evidence | action/now; activity/target/method meaning inconclusive in metadata-only evidence | Faithful search for physical tampering; ledger target; search method. Automated method review is finite-vocabulary mismatch | valid / valid | unsupported_activity |
| Study ledger notation | statement/none: wrong classification and commitment | Faithful committed notation study; ledger-notation target; no invented method | valid / valid | unsupported_activity |
| Cast unsupported Charm Person | source_not_verbatim; full semantic fidelity cannot be established | Faithful committed spell request targeting Mara; no substituted installed capability | invalid / valid | unsupported_activity: correct containment |
| Request access without a promise | statement/none and missing negative constraint | Faithful committed access request; explain investigation method; explicit constraint Do not make a promise. Mara is supported by the visible scene; no invented promise | valid / valid | unsupported_method |

Qwen has four confirmed semantic failures, one confirmed source-fidelity contract
failure, and one semantically indeterminate physical-search result. Unknown Qwen
descriptions were not reconstructed. Omitted optional target/method fields alone
do not establish that a description lost those meanings. Qwen had five V1-valid
results, zero bindings and one structural rejection before binding was probed.

Luna has five newly reviewable faithful interpretations and one equivalent reused
result that passes all frozen checks with the stated audit limitation. Its three
automated requires_review results (access, physical search and no-promise) resolve
to faithful meanings after reviewing the retained bounded fields; the evaluator's
original scores are preserved unchanged. There are no confirmed shared semantic
failures in this evidence, but the Qwen gaps and six simple cases limit that claim.

### Interpretation versus trusted binding

Both configurations produced zero gameplay bindings. This does not erase the
semantic improvement. For Luna, account/access/physical-search/notation-study are
supported meanings rejected at exact activity vocabulary matching. Examples include
Study the ledger notation versus study ledger notation and a natural complete
search description versus search ledger for physical signs. These are binding
compatibility failures, with the account attribution limited to retained checks.

Access additionally supplies two semantically sensible targets where the binder
requires one routing target. The first activity rejection masks that later target
cardinality mismatch. Physical search supplies Search the ledger as method,
outside the finite method vocabulary, which would also need independent diagnosis
if an activity were recognized. These observations do not authorize acceptance.

No-promise reaches the recognized access activity and Mara target, then rejects
Explain my investigation rather than canonical explain investigation. Independently,
the common runtime correctly contains constraints that it cannot enforce; preserving
the prohibition is semantic success, not permission to execute the request.
Charm Person remains an unsupported activity and is correctly contained.

Thus the original obstacle involved both interpretation and binding. The reference
model materially improves these frozen semantic results; the remaining observed
reference-to-gameplay obstacle is the restrictive binding/enforcement boundary.
Passing structural validation is neither semantic qualification nor execution
authorization. Nothing here supports broadening binder acceptance automatically.

### Counts, latency and estimated cost

| Metric | Five new requests | Six-case reference evidence including reused account |
| --- | --- | --- |
| Input / output tokens | 5558 / 422 | 6667 / 486 |
| Total tokens | 5980 | 7153 |
| Mean latency | 4.374 seconds | 4.911 seconds |
| Latency range | 2.978–8.902 seconds | 2.978–8.902 seconds |
| Sum of recorded call latencies | 21.869 seconds | 29.466 seconds |
| Estimated list-price cost | USD 0.0007668 | USD 0.0009097 |

Estimate uses the verified public gpt-6-luna rates of USD 0.10/million input tokens
and USD 0.50/million output tokens, not an invoice or account charge; cache/account
adjustments are unavailable. Source:
https://developers.openai.com/api/docs/models/gpt-6-luna
Historical account cost is included only in the six-case column, not new spending.
Qwen's six preserved calls averaged 3.343 seconds, range 2.124–8.007 seconds;
different providers/hardware and six samples do not support a latency benchmark.

### Verification, evidence and next decision

Syntax and secure-launcher parsing passed. Three focused offline tests passed:
exact five remaining frozen requests/configuration; bounded evidence omitting raw
input/source/context/IDs; and one-attempt stop on operational failure. Maintained
GitWorkflowTools verification passed. No prompt, schema, evaluator semantics or
binder changes were made. The new ignored runner only orchestrates existing
diagnostic_case and ResponsesProvider and retains bounded sanitized review fields.

All six evidence rows report executed false and state_unchanged true, with campaign
identity and full export unchanged. Runtime progression/acceptance/domain execution
and dice are guarded. No accepted receipts, campaign resources or elapsed time
changed. There were no operational/security failures or retries.

New ignored artifacts under .artifacts/intent-compare-complete-v1/:
complete_comparison.py, test_completion_offline.py, Invoke-CompleteComparison.ps1,
configuration.json, six-case-evidence.jsonl, offline.log,
maintained-verification.log, before.json, handoff.before.md,
preserved-evidence.json and completion-audit.json.
Only docs/player_intent_runtime_integration_v1_handoff.md changed among the
existing twelve candidate paths in this continuation. Architecture, system
manifests, ADRs and lifecycle need no reconciliation: this is a bounded diagnostic
comparison with no architectural, gameplay, persistence or package-state change.

The smallest justified next experiment is separately authorized broader, held-out
semantic evaluation of the reference configuration: hypothetical/reported actions,
negation/conditions/stops, multi-intention relationships, unsupported requests,
context-sensitive targets and adversarial reference content. Retain sanitized
reviewable output and score interpretation independently from finite binding.
The evidence favors B, a larger-model interpretation research path, over starting
Qwen fine-tuning now. It does not justify production selection, schema redesign or
another prompt correction from these six cases. Qwen fine-tuning research would
need a deployment rationale, representative labeled training/held-out data and
measured benefits over the stronger baseline; it is a separate owner decision.

HEAD/main/origin/main remain 5a370711c7d52a1af46ff064c50a786f37f89e62.
The existing twelve-file candidate stays uncommitted with an empty index.
Lifecycle remains active pending owner disposition, next_sprint null, unchanged.
No staging, commit, merge, push, publication, training or next milestone occurred.
Stopped after the five authorized remaining calls for owner review.

## Trusted-binding correction — October 30, 2026

Owner authorized bounded Watchhouse-owned correction and offline verification
only, using the existing candidate and preserved research. No new model call,
consequential live gameplay, Git staging/commit/push/merge, publication or lifecycle
closure. Baseline/HEAD remains `5a370711c7d52a1af46ff064c50a786f37f89e62` on
`codex/player-intent-runtime-integration-v1`; the index stays empty. The milestone
remains active with `next_sprint` null, awaiting owner review. This is an
uncommitted implementation handoff, not acceptance.

### Root causes and changes

The initial adapter compared whole activity/method strings to canonical labels,
required exactly one separately populated target, and omitted target aliases it
advertised. V1 permits natural activity descriptions and optional target/method
fields, so faithful meaning could not reach gameplay. The frozen reference
comparison isolated these compatibility failures from interpretation fidelity.

`engine/watchhouse_intent.py` now recognizes bounded equivalent complete
Watchhouse descriptions. Activity wording can expressly identify the target and
chosen method without duplicating optional fields. Asking for Mara's account
uses existing routine questioning; explicit physical examination and notation
study use their existing methods. Persuading Mara expressly selects persuasion;
an access/surrender request without a chosen approach returns clarification.
Mara plus ledger targets are the custodian and object of the same request; aliases
of either do not create additional intentions. Explicit unknown, ambiguous or
conflicting targets/methods reject. Installed context must still offer the exact
activity/target/method. No permissions, lies, threats, songs or promises are supplied.

Patterns match complete descriptions, including optional first-person wording and
ordinary article/case/terminal-period differences. An extra action, promise,
condition or stop in an unmatched suffix cannot be truncated. This is a bounded
owning adapter, not unrestricted semantic equivalence or a general binding
framework. Unfamiliar supported wording can still require clarification.

The adapter also preserves mode-derived intent and all three boundary collections
in its proposal, and clears previous local binding before reassessment. Common
Coordinator still independently derives commitment and reapplies every boundary.
`tools/evaluate_local_intent.py` probes the same Watchhouse grounding rather than
duplicating the obsolete canonical matcher. Its frozen independent semantic
scoring, input cases, schema and private-evidence projection are unchanged.
Historical scores and evidence are not rescored or overwritten.

### Supported and unsupported handling

| Meaning | Current behavior |
| --- | --- |
| Ask Mara for her account / what she knows about the dispatch | Existing report capability; no invented tactic or roll. |
| Persuade Mara to let me examine the ledger | Existing access/persuasion; Mara and ledger may both be named; permission still depends on adjudication. |
| Request access by explaining my investigation | Existing access/persuasion; missing optional method/target fields may be grounded from that activity. |
| Search/examine/inspect the ledger for physical signs/evidence of tampering | Existing search/perception; permission required. `Search the ledger` is accepted as a method only for that already explicit search. |
| Study/decipher/examine ledger or dispatch notation | Existing study/investigation; permission required; no hidden detail needs naming. |
| General ledger examination | No arbitrary Search/Study selection, including after permission. |
| Charm Person, unknown target, unsupported or conflicting method, unmatched consequential suffix | Contained rejection; no campaign mutation or dice. |
| Inquiry, statement, uncommitted preparation | No action promoted to commitment; structurally inconsistent commitment rejects. |
| Multiple intentions or material ambiguity | Existing common clarification before binding; no automatic chaining. |
| No-promise access; unsupported conditions or stops | Meaning can bind, but authorization fails before execution. |

### Constraint enforcement and authority

**The current Watchhouse gameplay owner cannot enforce an explicit no-promise
restriction. Such a request is not executable.** Mapping `Explain my
investigation` to persuasion does not establish constraint support. The unchanged
Coordinator rejects the preserved restriction against the owner's empty support,
even after a prior accepted access result or while a promise choice is pending.
No supported-constraint declaration is fabricated and no restricted request is
silently weakened. Conditions and stopping boundaries likewise require absent
owner support and remain contained. Adding that support would need a separately
reviewed implementation; it is not necessary for this correction.

Existing F05 notices/choices, context freshness, domain eligibility/adjudication,
single-use Coordinator permission, acceptance, receipts and retry/cost recognition
remain authoritative. Offline execution uses fresh controlled campaigns only.
No common infrastructure, mechanics, save/persistence contract or provider
implementation changed. Original checkout and owner saves remain untouched.

### Verification and preserved evidence

Python syntax compilation passed before execution. The updated focused module
contains 53 offline tests, including twelve added correction tests. The combined
V1/Watchhouse/Coordinator/F05 integration run passed **181 tests**; affected domain
acceptance, cross-domain coupling, campaign/activity continuity and player-activity
regressions passed **165 tests**. Standalone save/load passed. Automated provider
fixtures block outbound sockets; no live model or owner-save execution occurred.

Equivalent supported phrasings produced identical complete exported campaigns,
not just matching routing labels. Rejected fixtures preserve campaign identity,
complete export, elapsed time, accepted results and dice count. Coverage includes
omitted optional targets, target aliases, unknown/ambiguous targets, contradictory
methods, omitted approaches, permission absence, generic examination after access,
invalid commitment, inquiries/statements/preparations, all boundary kinds,
no-promise access at F05 and after historical success, and unavailable capabilities.
Existing save/load retry, request conflict, stale-context and F05 regressions pass.

The ignored `replay.py` reuses retained review fields from the frozen six-case
Luna evidence with outbound sockets, dice, acceptance, execution and progression
guarded. Five descriptive outputs replayed; the account row remains explicitly
unreplayable because its descriptive fields were not preserved. No missing output
was reconstructed. Account meaning is covered separately with controlled fixtures.
This replay revalidates retained fields, not the original omitted source excerpts.

| Preserved reference case | New binding probe | Nonexecuting Coordinator decision in fresh initial context |
| --- | --- | --- |
| Account | Not replayed: descriptive fields unavailable | Controlled account fixtures execute offline through the existing owner. |
| Persuasion/access | Compatible | Proceed permit; not executed by replay. |
| Physical search | Compatible | Clarification: permission is absent. |
| Notation study | Compatible | Clarification: permission is absent. |
| Charm Person | Unsupported activity | Unresolved routing. |
| Access without promise | Compatible meaning only | Unresolved authorization; restriction cannot be enforced. |

The five replayed campaigns retained identical identity and complete exports.
Successful search/study after an offline permission grant are separately covered
by integration fixtures. Prior comparison and one-call verification evidence
hashes are preserved; earlier artifacts are unchanged. Current artifacts/logs
stay under `.artifacts/intent-binding-correction-v1/`: `before.json`, `replay.py`,
`replay.json`, `focused.log`, `integration.log`, `regressions.log`, `save-load.log`
and `workflow.log`. The focused 51-test log precedes the final two regression
additions; the final 181-test integration includes all 53 focused tests.

PowerShell 7.6.5 workflow regression passed **29 checks**, including all sixteen
lifecycle fixtures in three layouts. Its initial direct invocation failed because
the legacy-shell rejection probe hit process execution policy before reaching the
expected version guard. Re-running through explicit `pwsh.exe -NoProfile
-ExecutionPolicy Bypass`, consistent with the maintained profile, passed. No
system policy, ACL, shared tool or repository script changed for recovery.

### Documentation reconciliation and limitations

Updated the runtime map, Player Presentation manifest, system relationship map,
current package/sprint/JSON goal/scope and this report for the authorized correction
and owner-review stop. JSON status/authority, active package and `next_sprint` are
unchanged. Accepted V1 Design, foundational doctrine, other gameplay manifests,
ADRs, deferred registers and persistence documentation need no change: no new
architectural decision, owner behavior, schema, migration or deferred capability
was introduced. Historical findings remain evidence, not current authorization.

Ten of the existing twelve candidate paths change in this continuation: the binder,
tests, diagnostic probe and seven documentation/record paths. `play_watchhouse.py`
and `engine/local_intent_provider.py` are unchanged from the starting candidate.
No additional source subsystem or tracked file was introduced; ignored replay and
verification artifacts are the only additional files.

The offline completion target is established: faithful supported descriptions can
bind into the existing Coordinator and reach existing gameplay acceptance in
controlled tests. This does not establish live interpretation fidelity, universal
wording coverage or enforcement of unsupported restrictions. No successful live
end-to-end result is claimed. The CLI still uses the existing opt-in localhost
adapter; no hosted runtime adapter or permanent model choice was added.

The binder cannot independently detect every internally consistent model
misclassification, omitted restriction or substituted intention. Structural
validity and successful binding do not certify fidelity to the original text.

`gpt-6-luna` is provisional for development testing by owner direction. The focused
evidence supports planning a separately authorized bounded live test using the proven Responses
invocation and fresh isolated campaign: one committed supported intention per
request, inspect interpretation before consequential execution, retain existing
permission/F05 boundaries, and treat generic examination, unsupported spells and
no-promise restrictions as expected containment cases. No unrestricted gameplay
qualification follows from this handoff. Stop for owner review; no further model
research, implementation, live requests, acceptance or publication is implied.

### Final verification disposition and broader-run blocker

Maintained GitWorkflowTools verification passed with the existing worktree-bound
profile, exact baseline HEAD and repository state unchanged. Preflight passed
20 checks with the expected dirty-working-tree warning, no blocked/failed checks;
current-record validation passed eight checks. `git diff --check` and index diff
checks passed. The profile preserves all shared checks with only the prescribed
worktree-root substitutions (and an existing trailing blank line).

The required Windows offline runner was also attempted once. It stopped in the
unchanged `test_narration_source.py`: `tiktoken` needed `o200k_base` data absent
from the runner's isolated temporary cache, and its attempted public tokenizer
download failed DNS resolution. This was a tokenizer asset request, not a model
generation or consequential gameplay request. The test uses a simulated response.
No existing cache was found in the normal local cache locations. No download retry,
dependency installation, environment/ACL change or unrelated narration repair was
made. The broader run is **blocked**, not passed; subsequent scripts in that runner
were unrun. Its failure excerpt is preserved in `offline-failure.log`.

This does not invalidate the separately passing 181 integration and 165 affected
regression tests or standalone save/load. The final scorer-isolation adjustment
also passed ten diagnostic tests (`frozen-scorer.log`). Maintained output is in
`maintained-verification.log`; `audit.py`/`audit.json` confirm unchanged historical
research evidence, starting CLI/provider sources, twelve candidate paths, published
refs, index and save paths. The original dirty checkout retains its starting status.

The bounded offline binding target is established. Broad verification remains
incomplete due to the environment blocker and is disclosed for owner disposition
before live-test readiness is accepted. No successful live end-to-end gameplay,
implementation acceptance or package completion is claimed. Stop for owner review.

### Complete offline verification recovery — October 30, 2026

The owner authorized retrieval of the official `o200k_base` tokenizer asset to
complete offline verification. The isolated default sandbox could not resolve
the host; the authorized download then succeeded through the approved elevated
execution path from
`https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken`.
The installed `tiktoken_ext.openai_public` declares SHA-256
`446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d`; the
download and cached bytes both matched. The asset is in the ignored isolated
`.artifacts/tiktoken-cache/` using `tiktoken`'s supported SHA-1 URL cache key
and `TIKTOKEN_CACHE_DIR`. `gpt-4o` encoding loaded as `o200k_base` with socket
connections blocked.

The complete Windows offline runner passed **81 commands**, including all **79
behavioral test scripts**; its live-provider smoke remained excluded. In
particular, the formerly blocked `test_narration_source.py` passed from the
isolated cache. Complete per-command output is preserved in the ignored
`.artifacts/intent-runtime-offline-final.log`. Maintained GitWorkflowTools
verification passed with repository state unchanged; preflight passed 20
checks with the expected dirty-tree warning, current-record validation passed
8 checks, PowerShell workflow regression passed 29 checks, and staged/unstaged
diff checks passed. Maintained output is in
`.artifacts/intent-runtime-maintained-final.log`.

No gameplay, binder, provider, test, dependency or shared environment changed.
Historical evidence and saves remain unchanged. The same twelve candidate paths
remain uncommitted, the index is empty, and HEAD/main/origin/main remain at
`5a370711c7d52a1af46ff064c50a786f37f89e62`. This completes offline verification
and is ready for owner review. No live model inference or gameplay execution was
performed; live end-to-end testing remains separately authorized. The milestone
is not accepted or closed, and no publication occurred.

### Bounded live end-to-end attempt — October 30, 2026

The owner separately authorized one `gpt-6-luna` Responses inference and, only
after a faithful interpretation, one Watchhouse undertaking. The previously
verified Responses provider and CurrentUser encrypted-credential child launcher
were reused through a test-only bridge under ignored
`.artifacts/intent-live-e2e-v1/`. The initial sandboxed launcher could not access
the credential; no child or model request started. The approved credential-capable
run made exactly one request, with no retry or alternative prompt. OpenAI returned
HTTP 200/completed; V1 structural validation passed. Usage: 1,113 input, 101
output and 1,214 total tokens.

Player input: "I ask Mara what she knows about the missing dispatch."
The response contained one action, commitment `now`, no relationships or
ambiguities, and a verbatim source excerpt. It described asking Mara about the
missing dispatch, but listed both `Mara` and `the missing dispatch` as targets.
The latter is the topic of the question, not a second gameplay target. It also
supplied `Ask Mara directly.` as an explicit method although no method was
specified. The interpretation gate therefore did not approve consequential
execution. This is a source-role/fidelity concern despite V1 validity.

A read-only probe of the unchanged Watchhouse binder returned
`unsupported_activity` for the complete activity wording and selected no
capability. Coordinator authorization was not requested after the failed
interpretation gate. No domain adjudication, acceptance, receipt, narration or
gameplay consequence occurred. The disposable campaign stayed `watchhouse-m1`,
revision 0, elapsed time 0, with zero accepted units and identical complete
export after the read-only probe. The initial save and bounded interpretation,
provider metadata and assessment are under the ignored artifact folder; no
credential, raw HTTP response envelope, hidden context or owner save is included.

This attempt does not establish successful live end-to-end integration or
general model reliability. Offline verification remains complete. The candidate
is uncommitted and awaits owner review; no contract, binder, Coordinator, domain,
provider or lifecycle change was made. No further model call or gameplay attempt
is authorized by this result.

### Live-test finding correction — October 30, 2026

The owner authorized offline correction of the Watchhouse binder and test-only
faithfulness assessment. The prior live interpretation and `assessment.json`
remain unchanged as historical evidence. The earlier gate conflated two named
entities with two gameplay targets and treated the routine description `Ask Mara
directly.` as an invented tactic. The response had one committed intention: Mara
was the conversational recipient and the missing dispatch was the subject of
inquiry. Its source excerpt was verbatim. The corrected test-only assessment
reads that preserved interpretation, checks those roles and the absence of
additional actions or boundaries, and records `semantic_fidelity: true` in
ignored `.artifacts/intent-live-e2e-v1/assessment-corrected.json`. It performs
no inference or gameplay execution.

The Watchhouse binder's full-phrase questioning pattern now recognizes bounded
`what she knows about [the] [missing] dispatch` descriptions addressed to Mara
or the custodian. For this activity, the dispatch may appear as an optional
subject in `targets`; it is not used as the gameplay target. Mara remains bound
to `custodian`. `Ask Mara directly.` and equivalent ordinary-questioning method
descriptions use the existing routine report route. The internal Watchhouse
method identifier is `persuasion`, as it was before this correction; that
identifier does not mean the player chose a persuasive tactic. An explicit V1
method of `persuasion`, deception, intimidation, or a promise remains rejected
for ordinary questioning. Unknown subjects, contradictory recipients, extra
actions, unmatched suffixes and unsupported boundaries remain contained.

Read-only replay of the preserved interpretation now yields `compatible` binding
to report/custodian and Coordinator status `proceed`, with the campaign export
unchanged. A separate fresh offline fixture consumed one Coordinator permission
and reached the existing Watchhouse report owner: one accepted receipt contained
Mara's attributed account, 60 seconds elapsed and no die was drawn. This is an
offline simulated-provider fixture, not a live gameplay retry.

Focused integration passed **184 tests**; affected domain, cross-domain,
campaign/activity continuity and consequence regressions passed **224 tests**.
Positive equivalents cover recipient and dispatch subject variants and routine
method wording. Negative cases cover added actions, unknown or contradictory
targets, tactical methods, promises, conditions and stopping boundaries; they
leave the campaign unchanged. The prior 79-script offline log and all live
evidence remain preserved. This bounded correction does not qualify the model
generally or establish a live end-to-end result. A live retry requires separate
owner authorization. The candidate stays uncommitted for owner review.

Maintained GitWorkflowTools verification passed against the worktree-bound
profile at exact baseline HEAD, with repository state unchanged. Preflight and
current-record validation passed; `git diff --check` and the empty index check
passed. The PowerShell workflow regression first hit the previously documented
legacy-shell execution-policy failure; rerunning with explicit PowerShell 7
`-ExecutionPolicy Bypass` passed all 29 checks. Maintained output is in ignored
`.artifacts/intent-live-e2e-v1/maintained-correction.log`. The original full
79-script run was preserved, not repeated. The runtime architecture map and
system manifests need no further change: Watchhouse still owns the finite binder,
and Coordinator, domain and persistence authority did not move. Accepted V1
Design, ADRs, mechanics and save documentation are unchanged for the same reason.

### Single live end-to-end retry — October 30, 2026

The owner separately authorized one `gpt-6-luna` Responses interpretation and,
if faithful and authorized, one consequential Watchhouse undertaking. A new
disposable `watchhouse-m1` campaign was saved under ignored
`.artifacts/intent-live-retry-v1/`; owner saves and prior evidence were not used
or changed. The existing verified Responses provider, secure CurrentUser
credential bridge, model and generation settings were reused. Exactly one model
request returned HTTP 200/completed, with 1,113 input and 84 output tokens.
There was no retry, alternative prompt, additional test case or narration call.

The exact player input was "I ask Mara what she knows about the missing
dispatch." The V1-valid response contained one action with commitment `now`:
`Ask Mara what she knows about the missing dispatch.` It named `Mara` as its
only target, `Ask Mara directly.` as its method, and learning what Mara knows
as its goal. It contained no source excerpt, relationships, ambiguities,
constraints, conditions or stopping boundaries; source is optional under V1.
The independent test-only gate found the recipient, dispatch subject, routine
method, commitment and single-intention boundary faithful. The model's advisory
domain label supplied no routing or gameplay authority.

The corrected trusted Watchhouse binder returned `compatible` and selected
report/custodian. Its internal `persuasion` method is the pre-existing routine
report route; the interpretation did not request a persuasive tactic. The
existing Coordinator returned `proceed` for one context-bound undertaking.
Its exact single-use decision was passed to `execute` once. No chained step or
second provider call was made.

The existing Watchhouse domain and acceptance path returned one accepted,
complete report receipt. Its recorded evidence was no rolls, report success,
and starting time 0. Mara's attributed statement says the copied entry records
a dispatch sent at dusk, that she did not witness its departure, and that she
believes the copy is accurate. This is an accepted attributed claim, not proof
of the dispatch's actual departure. One receipt was accepted; campaign revision
changed 0→1, elapsed time 0→60 seconds, accepted units 0→1, and dice usage
remained zero. Reloading the isolated result save confirmed the accepted unit,
evidence, time, report activity and receipt. The hidden objective truth was not
disclosed.

The non-provider presentation was exactly the receipt's public text, including
attribution and the 60-second consequence. This establishes a successful path
for this one input through interpretation, V1 validation, trusted binding,
Coordinator authorization, domain resolution, acceptance and presentation.
It does not establish general model reliability or broad phrasing coverage.
The bounded sanitized gate, resolution and saved-state checks are in
`gate.json`, `resolution.json` and `state-integrity.json` in the ignored retry
folder; the raw interpretation and disposable saves remain isolated there.
No prompt, schema, binder, gameplay, accepted contract or persistence source
changed in this retry. The candidate remains uncommitted and awaits owner
review; no further live test or implementation acceptance follows automatically.

Maintained GitWorkflowTools verification passed against the worktree-bound
profile with exact HEAD `5a370711c7d52a1af46ff064c50a786f37f89e62` and
repository state unchanged. Preflight, lifecycle-record validation and Git diff
checks passed. The index is empty, and the candidate worktree has no save-path
changes. Output is in ignored `.artifacts/intent-live-retry-v1/maintained.log`.
No new runtime or architecture documentation is needed: this test exercised
the already documented authority boundaries without changing them.

## Owner acceptance and publication-candidate verification — October 30, 2026

The owner accepted this bounded experimental implementation after the successful
single live Watchhouse report path and authorized official candidate preparation.
Acceptance covers the explicit localhost-only, model-configured runtime and its
trusted Watchhouse binding. The model-independent V1 interpretation contract,
Coordinator/F05, domain mechanics, accepted-result ownership and persistence
remain unchanged. A single successful `gpt-6-luna` case does not qualify general
model reliability, a production provider or unrestricted gameplay.

The exact candidate inventory remains the twelve paths listed above: seven
modified and five added. It contains no owner save, accepted contract, common
Coordinator, domain mechanics, persistence, credential, historical test evidence
or shared-tool change. The original checkout and unrelated worktrees are outside
this candidate. Ignored tokenizer, live-test and verification artifacts remain
outside the commit.

Final verification against the current candidate passed syntax compilation,
current-record validation and the complete Windows offline runner: **81 commands,
including all 79 behavioral scripts**, with the live-provider smoke excluded.
The run used the established isolated `o200k_base` tokenizer cache and made no
model request. Its output is preserved under ignored
`.artifacts/intent-publication-candidate-v1/offline.log`. The earlier completed
offline log and all historical live evidence are preserved unchanged.

Documentation reconciliation updates this handoff, the current package/sprint
records, the runtime architecture map, the system relationship map and Player
Presentation to identify owner acceptance while keeping publication pending.
The accepted V1 Design, ADRs, other domain manifests, save/migration guidance and
deferred-capability records need no change: this acceptance adds no contract,
ownership transfer, mechanic, persistence version or provider qualification.
The official Git workflow binds a future candidate to its exact committed HEAD
and parent, but requires separate `COMMIT` authorization after staging. Owner
acceptance of the implementation does not grant that Git authorization. The
candidate tool was not invoked, so the index remains empty and the twelve-file
diff remains uncommitted for review. `main` remains protected pending separate
publication authorization.
