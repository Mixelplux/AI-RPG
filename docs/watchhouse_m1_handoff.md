# Watchhouse Records V1 — M1 implementation handoff

## Status and authority

Owner separately authorized M1 implementation October 28, 2026 after staging.
Owner accepted M1 October 29, 2026 and authorized staging and committing this
exact implementation. At acceptance, merge and push were not yet authorized.
The owner separately authorized strict fast-forward merge and normal push on
October 29, 2026; the implementation was published at
`014c1b84efbedef742e0cc23d737c4ef2d0020ec`. Provider calls remain unauthorized.
Lifecycle is idle using the existing complete state: latest completed is
`watchhouse-records-v1-m1`, active sprint/package and next sprint are null.
Broader Watchhouse V1 is not complete. No M2 is staged.

Published implementation: `014c1b84efbedef742e0cc23d737c4ef2d0020ec`.
Exact parent and pre-publication main baseline:
`a5649fa191b2f1d989491d18b5d1e9bb5cd86c58`.

Branch: `codex/watchhouse-records-v1-m1-stage-20261028`.
Worktree: `C:\Users\Richard\.codex\worktrees\watchhouse-records-v1-m1-stage-20261028\AI RPG`.
The original `D:\AI RPG` dirty checkout and its index are preserved. At initial
handoff, only the candidate commit was authorized; subsequent publication
authorization is recorded above. Model/provider requests remain unauthorized.

The external Design handoff was unavailable during staging; the owner's bounded
scope, accepted foundational Design and existing ownership contracts govern.

## Submitted behavior and ownership review

### Final corrections and acceptance boundary — October 29, 2026

The owner adjusted M1 acceptance to require a safe interpreted-intention interface,
not actual LLM language understanding. This does not alter accepted foundational
F05/F01 Design. Genuine contextual language understanding remains required for
early API integration before substantial expansion into additional gameplay
domains. Neither actual LLM understanding nor AI narration quality is verified.
The existing CLI is a deterministic scenario harness; its phrase recognizer and
fixed prose are not evidence of those capabilities. No next milestone is staged.

Influence no longer substitutes existing permission for the outcome of a new
urging. An established grant followed by intimidation records a refusal, preserves
the earlier grant and adds only the established exchange time. A different hesitant
approach requires its own roll even after access was granted; failed same-way
urging still has its wait. No hostility or automatic revocation is introduced.

`test_new_urging_after_permission_is_independent_and_retry_safe` checks accepted
outcomes/history, retained permission, cooldown, actual disk save/load and exact
retry with no repeated time, dice or effects. `test_controlled_interpretations_use_existing_coordinator_and_owner`
feeds controlled `Interpretation` values to existing `Coordinator`/`CoordinatedDomain`
interfaces. Inquiry/preparation, ambiguous intent, wrong target/approach and missing
ledger permission cannot publish consequences; a valid commitment reaches real
owning-domain checks and common acceptance. Existing forged-result tests retain
the proof that the interpreter cannot authoritatively choose an outcome.
No new framework, action schema, phrase pattern or production interface was needed.

Final correction verification, before publication: 25 Watchhouse tests, 21
cross-domain compatibility/recovery regressions, legacy save/load, 8 lifecycle
checks and 29 PowerShell workflow checks passed. Worktree-bound GitWorkflowTools
verification passed (20 preflight passes and the expected dirty-working-tree
warning). Logs use `.artifacts/watchhouse-final-*`; the unrelated full suite was
not rerun. Only the Watchhouse owner, focused tests and package/sprint/handoff
records changed for these corrections. Architecture/manifests and accepted
Design needed no further edits at that point: existing interfaces and ownership
were unchanged; only the M1 acceptance boundary was clarified. Both indexes were
empty; original checkout and save boundaries were preserved. No API/provider
calls occurred. Git publication had not yet happened at final-correction
verification; it was separately authorized and completed afterward on October
29, 2026 at `014c1b84efbedef742e0cc23d737c4ef2d0020ec`. Actual LLM
understanding and AI narration quality remain unverified.

The owner accepted the corrected permission/intimidation behavior October 29,
2026. Scripted smoke is not evidence for AI language or narration quality.

- `engine/watchhouse.py` creates an independent schema-4 campaign, one physical
  custodian and one ledger. It interprets complete bounded natural-language
  utterances. Questions, proposed actions ending in a question mark, unsupported
  methods, compound requests and unowned commitments cannot silently execute.
- `engine/watchhouse_domain.py` owns the scoped custodian's duty/knowledge-based
  responses and access. Mara offers her public account, hesitates over supervised
  examination, refuses to surrender the ledger and rejects bullying. She did
  not witness departure; her belief in the copy cannot become witnessed truth.
  This is an independent campaign identity, not a rewrite of the ordinary pack.
- `engine/watchhouse_rules.py` computes checks from explicit Character-owned
  ability scores, proficiency/ranks and exhaustion. No climbing or gate statistic
  determines these mechanics. Custodian Intelligence and attitude are explicit.
- The installed owner composes these inputs through existing Coordinator/F05,
  common schema-4 acceptance and one root publication. World time/cause records,
  safe receipts and accepted evidence advance coherently. Social permission,
  refusal time and Character findings derive from validated history, with no
  parallel mutable social store. Forged evidence/receipts, invalid dice, stale
  roots and unsupported effects cannot confer permission or knowledge.
- Search requires supervised access and resolves a physical sign; Study resolves
  a cipher-like notation. The safe result distinguishes observed reopening signs,
  Mara's attributed claim, an uncertain interpretation and the unrevealed actual
  departure. The culprit remains unspecified. No narration invents an identity.
- Recognized request IDs reuse exact receipts; conflicting IDs reject. Completed
  examinations recall past results without more time or dice. Failed Influence
  retains the same-urging wait across saves; another explicitly chosen supported
  approach is a new attempt. A failed examination completes that examination
  without manufacturing a discovery.

The [official 2024 Rules Glossary](https://www.dndbeyond.com/sources/dnd/br-2024/rules-glossary/)
was checked for Influence, Search and Study. Willing/unwilling responses require
no check; hesitant Influence uses the higher of DC 15 and NPC Intelligence,
attitude advantage/disadvantage and the failed-urging wait. Search/Study use their
appropriate ability/skill. Natural 1/20 do not automatically decide ability checks.
Search DC 12, Study DC 13 and 60/300-second examination durations are explicit
scenario rulings, not universal 2024 rules. Social exchanges take 60 seconds.

## Persistence and compatibility

No save-version, codec field, record registry or historical schema change.
Existing inert scope tuples carry versioned local declarations and scoped
Character/NPC premises; accepted evidence records dice, outcome and original
time. Installed v1 owner code retains the fixed authored ledger meaning.
Existing envelope V3/schema 4 reconstructs every accepted result without dice
before adoption. Unknown/corrupt meaning rejects; old saves are not rewritten.
Finite historical schemas 1–3, original defaults and V1/V2 routes are unchanged.
The existing same-directory atomic writer preserves the earlier save on failure.

## Verification

All Python changes passed `py_compile` before behavioral execution.

- `test_watchhouse.py`: **25 passed**, including the live CLI loop with mocked
  player input, on-disk V3 round trip, safe recall, retry/cooldown persistence,
  failed replacement, corrupt adoption, unsupported effects, explicit methods,
  attitude/DC handling and single-root rejection cases. Socket connections are
  denied during these tests.
- `test_cross_domain_coupling.py`: **21 passed**, including schema-4 climbing
  equivalence, independent owner contracts, historical schemas 1–3, unfinished
  activities, atomic writes, corruption and choice-history integrity.
- `test_save_load.py`: **passed**, preserving the legacy save/load route.
- Worktree-bound GitWorkflowTools verification: **passed**, including syntax of
  lifecycle JSON, lifecycle checks, preflight and both diff checks; repository
  state unchanged by verification. The copied profile changes only required
  worktree bindings; shared tools/profile remain untouched.
- PowerShell workflow fixtures: **29 passed** in the approved execution context,
  including 16 lifecycle cases in each whitespace layout. The sandbox run could
  not complete the legacy-shell guard assertion; the explicit approved-context
  rerun passed without modifying checks.
- Earlier supplementary full offline runner: **interrupted**, not passed. It reached
  `test_narration_source.py`, where unavailable tokenizer data caused an attempted
  static encoding-asset fetch that failed DNS resolution. Automatic approval
  review rejected a proposed approved-context narration rerun because it might
  cause an unauthorized external download. That path was not retried or bypassed.
  The later authorized local-cache recovery below resolves that individual test.
  Logs are ignored in `.artifacts/watchhouse-offline.log`; the passing clean
  baseline's 77 commands/75 behavioral scripts are historical baseline evidence,
  not a passing post-implementation full-suite result. The owner clarified that
  unrelated full-suite coverage is not an additional acceptance requirement.

No independent reviewer was requested or used. Focused checks, the compatibility
suite and code/ownership review were performed in this chat; commands ran as
separate processes. Required affected-system checks are passed, including the
recovered narration regression below. No post-recovery full-suite pass is
claimed. No model/provider generation occurred.

### Authorized tokenizer recovery — October 28, 2026

Existing source:
`C:\Users\Richard\AppData\Local\Temp\data-gym-cache\fb374d419588a4632f3f557e76b4b70aebbca790`.
The 3,613,922-byte asset is `o200k_base.tiktoken`, whose upstream URL is
`https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken`.
The installed `tiktoken_ext/openai_public.py` pins its SHA-256 to
`446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d`.
Both the existing source and the copied worktree asset matched that pin.

The verified copy is in `.artifacts/tokenizer-cache/` under tiktoken's expected
URL-derived cache key above. No network retrieval, additional dependency,
shared environment modification or rejected-action bypass was needed.
`TIKTOKEN_CACHE_DIR` was set only for the verification process and restored
afterward. `test_narration_source.py` **passed** through the official Python
interpreter with `socket.socket.connect` patched to reject outbound connections.
The test's injected fake narration response remained in use; no live model/API
request occurred. Evidence: `.artifacts/watchhouse-tokenizer-recovery.log`.

No gameplay, save contract or architectural change was made for recovery.

## Files and documentation reconciliation

New runtime files: `engine/watchhouse.py`, `engine/watchhouse_domain.py`,
`engine/watchhouse_rules.py`, `play_watchhouse.py`. Existing `engine/domain_owners.py`
registers the installed owner; common acceptance, codec and historical modules
are unchanged. New behavioral evidence: `test_watchhouse.py`.

Updated documentation: current package/sprint JSON and Markdown, architecture,
the eight affected system manifests and their system map, plus this handoff.
They distinguish submitted implementation from accepted behavior and preserve
the legacy paths. Accepted F01, F05, Information Foundation, doctrine and ADRs
are unchanged: this implementation realizes bounded behavior without changing
those requirements or selecting a new architectural/persistence model.
`PROJECT.md`, `AGENTS.md`, workflow/tooling and Region Pack data require no change.

## Owner smoke and limits

From this worktree root, run:

```powershell
.\.venv\Scripts\python.exe play_watchhouse.py
```

1. Ask `Could I examine the ledger?` and confirm no attempt occurs.
2. Say `I ask Mara for her account`; her reply remains attributed and qualified.
3. Choose `I persuade Mara to let me examine the ledger`. Success permits only
   supervised examination. Failure preserves the refusal and same-approach wait.
   Other explicit supported approaches are shown by the language adapter, e.g.
   `I request permission to examine the ledger by performing a song` or
   `I request permission to examine the ledger by claiming I am an inspector`.
4. If permitted, say `I search the ledger for signs of tampering` and
   `I study the ledger notation`. Checks may fail; successful findings must not
   become proof of a culprit or actual departure time.
5. Use `save`, quit, then run with
   `--load .artifacts/watchhouse-player.json`; `review findings` retains accepted
   meaning, while recalled examinations do not repeat time or random outcomes.
6. Propose a compound promise/payment or ask to surrender the ledger. The former
   returns control; the latter is refused without transferring the object.

The language adapter is finite and conservative, not arbitrary-language coverage.
Unrecognized wording asks for clarification. It has no general wait/time-advance,
social freeform planner, changed NPC goals or ongoing spell effects. A failed
same-way urging cannot be spammed; only the existing legitimate clock boundary
or another supported chosen approach can permit a new attempt. Unsupported
ongoing Character effects fail closed. The independent CLI is deliberate; the
ordinary `play_game.py` flow is not integrated or claimed to be extended.

Charm Person, expiry, later NPC/faction developments, combat, general stealth,
tactical movement, companion control, broad rule catalogs, universal engines,
migration, broad refactoring and live providers remain excluded/deferred.
Do not begin another milestone or publish this diff automatically.
