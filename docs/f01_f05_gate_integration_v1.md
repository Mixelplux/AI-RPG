# F01–F05 gate integration V1 — implementation report

**Owner acceptance (October 17, 2026):** the bounded integration, corrections,
independent activity validation, API tooling and associated tests/documentation
are structurally accepted. The [acceptance and publication proposal](f01_f05_integration_v1_acceptance.md)
supersedes pending-acceptance statements below. These dated implementation and
evaluation accounts retain their original judgments. Staging, commit, merge and
push remain unauthorized during preparation.

**Latest validation follow-up:** the owner reports gate structural smoke passed
after SR-01. The separately authorized [independent activity validation](f05_independent_activity_validation.md)
adds only a test-local supplier sequence and evidence; gate behavior and all
production runtime remain unchanged by that task. Package acceptance and
publication remain separate owner decisions. Dated accounts below are historical.

**Current disposition (October 17):** [final structural reconciliation](f01_f05_final_structural_reconciliation.md)
supersedes the current-status summaries below while preserving their historical
judgments. Both live budgets are exhausted. Owner now classifies the original pin
omission as minor in this scenario; style remains deferred. Existing bracing
recognition is corrected. That review found SR-01: a recognized restriction was
not checked consistently on resumption. The subsequent owner-authorized
[SR-01 correction](f01_f05_sr01_restriction_correction.md) now supplies the existing
conflict consistently; structural acceptance remains pending owner review/smoke.
The historical final review changed documentation only; this follow-up changes
the gate checkpoint supplier and its focused regression.

## Preflight and boundary

**Current follow-up:** the API environment repair and eight completed live samples
supersede the initial environment blocker recorded below. Live Case 5 omitted a
committed pin at a player decision. The separately owner-authorized
[offline instruction correction](f01_consequential_fidelity_correction.md) now
targets that failure, without changing accepted design, scenario state or F05
control. Original live evidence is unchanged. The live budget is exhausted;
revised generated fidelity and owner experiential quality remain unverified.
Earlier implementation/verification descriptions below retain their dated scope.

October 16, 2026: local main, origin/main and actual remote main independently
matched `d2ededee58294002f522cef5ab61577270311997`. The shared workflow state
tool confirmed the original dirty checkout; it remains untouched. Created
`codex/f01-f05-bounded-playable-integration-v1` at that baseline under
`D:/AI RPG/.artifacts/f01-f05-bounded-playable-integration-v1`.
The isolated checkout uses a junction to the existing official virtual environment;
no environment was recreated. First milestone staged and lifecycle validation
passed 7 checks before code changes. Preflight: 20 pass, one dirty-tree warning.

Governing sources: PROJECT/WORKFLOW/AGENTS; Story-First Part I; canonical F01
D1–D10 and F05 D1–D6; system manifest shared doctrines and responsibility map;
relevant Action & Resolution, World Simulation, Character System, Actors & Social
Dynamics, Narrative Experience, Scenario and Player Presentation authority;
accepted F01/F05 implementation/acceptance records; DF-009. The supplied owner
request authorizes this scenario only, superseding its previously deferred status.

| Component | Disposition |
|---|---|
| `engine/activity_control.py` | Reuse unchanged: authorization and return of control over explicit checkpoints. |
| `engine/narrative_realization.py` and provider/output boundary | Reuse unchanged: accepted stateless F01, explicit safe meaning/provenance/access, single call, fail closed. |
| Existing material handling / competence | Exclude from gate execution: cart-specific declarations and West-Road-only tags/bands do not define gate gameplay. Reuse their copied-candidate and accepted-result principles locally. |
| Ordinary CLI / campaign save / region loader | Exclude: standalone unsaved scenario avoids campaign schema, historical experiments and unrelated gameplay changes. |
| Missing upstream suppliers | Explicit bounded scenario fixtures for competence, means, guard choice, physical development and controlled outcome. No general systems claimed. |

No material design gap found: ordinary lifting/leverage, character-grounded
examination, repair, meaningful changed means and routine non-interruption fit
accepted design. Local scenario quantities and text are authored evaluation
circumstances, not new doctrine. Repair retains a secured hinge and one accepted
resolution across control return; continuing with a newly needed timber brace
requires the player's choice. Duration alone never creates an interruption.

Routine risk: isolated disposable session; no campaign persistence or core
time/causality changes. No inn/trail implementation, generalized parser, scheduler,
progress meter, NPC framework, save migration or broad refactor. Separate chat
authorization permits up to eight live generations; automated tests remain offline.

## Implemented behavior and observed limits

- Ordinary lift with the guard: three minutes; controlled success clears the
  cart but leaves a damaged hinge and re-jammed gate. Controlled failure keeps
  the blockage and paid effort. Timber leverage: five minutes; success commits
  timber to holding the opening, failure splits/spends it. Both retain damage.
- Examining takes two minutes once. Stipulated carpentry supports identifying a
  repair using tools and a pin; a novice sees the bent hinge without gaining
  specialist knowledge. Neither result proves the guard's tampering suspicion.
- Repair uses one pin and thirty minutes total under ordinary/no development,
  with no intermediate decision. Controlled failure retains paid effort, used
  pin and damage. A support-shift variant stops after ten minutes with the hinge
  secured. Explicit renewed authorization for a timber brace spends five more
  minutes plus the remaining twenty. The accepted result is reused, not rerolled.
- Withdrawal and changed approach preserve costs, findings and accepted work.
  A different explicitly chosen approach can clear the cart. If that uses the
  timber, resuming repair then finds the support unavailable. A previously stated
  no-timber restriction persists until the player explicitly renews that choice.
- Natural variants distinguish inquiry, tentative proposals, examination,
  preparation, commitment, help, stopping and continuation. Unsupported methods,
  unrecognized restrictions, mixed methods and some compound requests return
  contextual unavailability without silently selecting another method or target.
  This remains a finite scenario interpreter: it does not claim unrestricted
  language understanding. Compound phrasing may need a simpler restatement.
- F01 receives established source/status/time/access meaning records, explicit
  intent/constraints, unknown cause and historical continuity. Initial guard
  suspicion stays reported and unverified. Current projection reflects completed
  cooperation/cleared cart rather than replaying a helper agreement. A candidate
  construction failure publishes nothing; presentation failure cannot replay,
  refund or erase an accepted action. Generated claims never enter state.

`GateFixture` is the explicit supplier boundary: success/failure for each method,
choice/ordinary/no development, carpentry, helper, timber and tools. Defaults
provide a competent character and the meaningful repair interruption. Outcomes
are controlled fixtures, not a general probabilistic skill or physical model.
The session intentionally has no campaign save/load or restoration guarantee;
closing it ends the disposable evaluation. Within-session continuity is tested.

## Verification and evaluation

- Python syntax/static compile passed before execution using the official
  `.\.venv\Scripts\python.exe`.
- `test_damaged_gate.py`: 19 offline tests pass. Coverage includes A/B/C, natural
  variants, missing means, restrictions, failure costs, target/method preservation,
  preparation vs commitment, explicit constraint renewal, current-means resumption,
  result reuse, authoritative state/provenance, atomic failure and provider isolation.
- Accepted `test_activity_control.py`: 11 tests pass, including its real handling
  integration, copied-candidate isolation and existing save restoration checks.
- `test_narrative_realization.py`: five offline groups pass. Three adjacent scripts
  pass: `test_narration_output.py`, `test_narration_source.py`, and
  `test_openai_responses_narration.py` (fake transport). The initial adjacent run
  encountered a missing tokenizer cache at the sandbox default path. Recovery
  pointed `TIKTOKEN_CACHE_DIR` at the existing public-tokenizer cache in the user's
  local Temp directory; the rerun passed with DNS/socket access denied. No
  dependency installation, provider connection or accepted-code change was made.
- Scripted CLI smoke checked inquiry → assisted lift, repair → choice → plain
  resume refusal → explicit timber continuation → observation, and ordinary
  repair completion. It exposed overlong repeated scene recaps; deterministic
  display now uses the current projection for observation and expresses only new
  action developments on other exchanges. Full current truth stays in F01 input.
- Live F01 evaluation is **blocked**, not passed: neither the process nor user
  environment has `OPENAI_API_KEY` configured. Zero live generations attempted;
  the separately authorized allowance of eight is unused. No credential files
  were inspected, copied or modified. No model/prompt tuning was performed.
- Final lifecycle validation passed 7/7; shared GitWorkflowTools verification
  passed with unchanged repository state during its checks. Its canonical profile
  was copied only to ignored `.artifacts/gate-verification/` to bind checkout root,
  expected preflight root and evidence directory; shared tooling/profile unchanged.
  Log: `.artifacts/gate-verification/workflow.log`. Final syntax and 19 gate tests
  passed after the last input-boundary corrections. Tracked/index diff checks,
  new-file whitespace and changed-document links passed; the 13-path scope was
  reviewed and accepted F01/F05/persistence source remains unchanged.

Mechanical correctness and explicit information fidelity have offline evidence.
Injected/canned prose and structural F01 validation do not establish generated
semantic fidelity. Live narrative quality and owner experiential quality remain
unverified. No full repository suite or universal semantic-safety claim is made.

## Limited owner smoke

Current follow-up: [October 17 interaction correction and verified offline smoke](f01_f05_interrupted_repair_correction.md).
The original eight-request evaluation and subsequent four-request comparison
budgets are exhausted. Use the default offline launcher below; `--live` is not
authorized. The original implementation account below is historical; this
follow-up supersedes its live-evaluation blocker and smoke disposition.

From this isolated checkout, run:

```powershell
.\.venv\Scripts\python.exe tools/play_damaged_gate.py
```

Try a question about lifting, then an assisted lift. Start another disposable
session, authorize repair, and decide about the timber when support changes.
For ordinary non-interruption, run with `--development ordinary` and repair.
Optional `--failure lift`, `--failure lever` or `--failure repair` supplies the
controlled unfavorable outcome; `--novice` changes stipulated competence.
`--live` explicitly uses accepted F01/provider realization with a configured
process credential, capped at eight calls per session; the current task's total
authorized evaluation budget is eight, not eight per repeated run.

Owner review needs only whether approaches feel natural, ordinary attempts are
appropriately paced, the repair decision is meaningful, and consequences remain
clear. Technical retesting is not requested. Offline authoritative accounts are
usable now; generated experience still needs the blocked live evaluation.

## Documentation reconciliation and handoff

Updated architecture, system relationship map, Action & Resolution and Narrative
Experience manifests, manifest index, DF-009 and current package/sprint records.
These identify the unaccepted gate route and explicit fixture limits. DF-009's
other themes and older Market observations remain deferred; no historical
material was reconciled. Additional paths are directly necessary within the
authorized scenario/integration and documentation scope.

Meaningful no-change determinations: F01/F05 accepted Design, doctrine, ADRs,
AGENTS/PROJECT/WORKFLOW and accepted F01/F05 runtime stay unchanged: this adds no
new doctrine or durable architecture. World/Character/Actors/Scenario/Presentation
manifest general classifications remain Partial: their general implementations
and ordinary routes are unchanged; fixture suppliers are described centrally in
the map/report. Persistence manifest/save version need no change because this
session has no persistence integration. No region, campaign data or owner save
changed. No dependencies added.

Baseline/HEAD remains `d2ededee58294002f522cef5ab61577270311997`; changes are an
uncommitted implementation handoff on the feature branch, with an empty index.
Lifecycle stays active pending review and blocked live evaluation. No acceptance,
Git staging, commit, merge, push, publication or next package is implied.
