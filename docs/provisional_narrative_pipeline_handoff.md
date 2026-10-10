# Provisional narrative pipeline implementation handoff

October 10, 2026. Elevated. Owner-accepted implementation on
`codex/provisional-narrative-pipeline` in
`D:/AI RPG/.artifacts/provisional-narrative-pipeline`. Protected baseline and
required direct parent: `942504a7d7019eb94f81f6db6d281ffa779367a2`. The owner
separately authorized final offline verification, staging and one implementation
commit. Merge and push require separate authorization.
The original dirty Sprint 10.82 checkout and protected main are preserved.

## Implemented slice

A newly resolved failed `follow withdrawal signs` attempt at North Gate now
flows through accepted foundation input, content preparation and stateless
realization before one CLI presentation. All other results and repeated commands
retain their established presentation. Failure in either stage uses the established
deterministic outcome with its hour cost. The following scene still supplies
updated choices and other material changes without repeating the search result.

Revised A selects the failed search, hour cost and useful uncertainty qualifier.
Previously known guard reports, Mara's account and limited inferences remain
context with their status. No-discovery, no-travel, agency and knowledge limits
remain boundaries rather than mandatory prose. Mechanical competence labels and
the no-capture/threat inventory are absent from the local passage.

Preparation and realization receive copied player-safe data, never engine/state
handles. Revised A checks belong to those adapters. An alternate pair using a
different representation passes the same engine/CLI interface test. No universal
schema, narrative memory, simulation mechanism or persistence field was added.

Normal gameplay uses local adapters and makes no new provider calls. The optional
provider pair uses the existing model/transport policy, with separate fresh
Requests, zero retries, store=false, 4096 preparation and 2048 realization output
token caps. Stage two receives only the validated intermediate. Callables can
be supplied to `GameEngine.get_resolved_narration` or `play_game.main`; no live
adapter was invoked against a provider during implementation. The owner later
authorized and accepted one bounded live smoke; further paid use requires authorization.

## Verification and review

Passed syntax checks for all changed Python files; ten new offline integration
checks in `test_resolved_narration.py`; these 17 affected regression scripts:

- Narration context, request, prompt, source, output, pipeline, OpenAI fake transport,
  and bounded narration input foundation (8 scripts).
- Player scene route, pressure narration, scene context, character competence,
  West Road predicament, scene relevance, presentation, save/load and market theft
  (9 scripts).

Passed preflight (19 passes, two expected warnings), lifecycle validator (7 passes),
diff whitespace checks and an offline interactive-loop smoke. The legacy tokenizer
test initially lacked its cache in the sandbox TEMP location; pointing
`TIKTOKEN_CACHE_DIR` to the existing
`C:/Users/Richard/AppData/Local/Temp/data-gym-cache` resolved it without downloading
dependencies or calling a provider. An existing presentation assertion was updated
for the newly integrated hour wording; all its other behavior checks remain.

Targeted architecture review: only recorded results are read; no calls resolve
actions, draw RNG, advance time or save from narration. Hostile generated prose
cannot change gameplay, discoveries, NPC knowledge, location, history or saves.
Full version-1 save data is equal before/after narration, and saved bytes round-trip
unchanged. Preparation failure stops realization; source/realization failures and
malformed output reveal no raw error material. Serialized fake transports confirm
separate stateless calls and exclusion of private scene/debug/history fields,
engine result IDs, raw player input, source and review metadata from realization.

## Limits

Only a failed TRACK result is integrated. Partial/full results, other investigations,
dialogue, generic scenes and additional simulation remain outside scope.
The provider pair is wired and fake-transport tested; the owner also accepted one
live sample, which establishes no universal narration-reliability claim.
Local smoke verifies the gameplay presentation and integration, not generated
selection quality. Structural output validation cannot detect all fabricated or
misattributed prose; the adversarial prose test intentionally demonstrates that
such prose can pass structural validation while having no simulation authority.
Semantic fidelity of future live output requires separately authorized evaluation
and owner experience review. No new semantic validator framework was introduced.

## Owner experiential smoke

From the isolated worktree root, run:

```powershell
.\.venv\Scripts\python.exe tools/play_provisional_narration_smoke.py
```

This sets up the existing withdrawal situation through real engine commands,
fixes only the smoke draw to failure, blocks provider construction and redirects
any smoke save to `.artifacts/provisional_smoke_save.json`.
Enter `follow withdrawal signs`. Assess whether this feels like a concise failed
investigation that costs an hour, stays at North Gate, introduces no new knowledge
and avoids replaying prior reports or mechanical labels. Then enter `quit`.
Routine regressions have already been automated; the owner need only assess the
player experience.

Expected local passage:

> You spend an hour at North Gate searching the churned snow, but cannot pick out
> a trail you can follow. The watchers' names and destination beyond this stretch
> of road remain unknown.

## Changed files

- `engine/resolved_narration.py`: slice source, adapter-private Revised A contract,
  local/provider preparation and realization, fail-closed orchestration.
- `engine/narration_source.py`: reusable bounded stateless text transport; existing
  preview packet/source identity and configuration retained.
- `engine/game_engine.py`: read-only accepted-result narration entry point.
- `play_game.py`: one fresh result presentation with deterministic fallback.
- `test_resolved_narration.py`, `test_west_road_presentation.py`: new integration
  coverage and directly affected presentation expectation.
- `tools/play_provisional_narration_smoke.py`: offline experiential launcher.
- Package/sprint Markdown, lifecycle JSON, architecture map and this handoff.

## Acceptance and finalization

The owner accepted Revised A preparation, stateless realization, the failed
`follow withdrawal signs` path, fallback, existing CLI presentation, simulation
authority and version-1 save compatibility. Accepted live evidence:
`C:/tmp/AI-RPG-Provisional-Narrative-Live-20261010-01a1277d/report.md`.
That smoke used two authorized requests and displayed the generated passage once.
Finalization remains offline; no further provider calls are authorized.

Final verification passed: all ten provisional integration checks, all 17
affected regression scripts listed above, syntax checks for all seven changed
Python files, maintained GitWorkflowTools verification and diff checks. Preflight:
19 passes, two expected warnings (PowerShell 5.1 and pending worktree changes),
zero failures or blocks. Lifecycle validation: seven passes. Tests ran with
network connections blocked and no network attempts. Existing tokenizer cache
was reused; no dependencies were downloaded. No runtime source correction was
needed during finalization.

Scope review against the protected baseline found only the files listed above.
Preparation and realization remain replaceable, generated data is presentation
only, and no experimental evaluation metadata is a runtime dependency. No
simulation/persistence implementation, doctrine, foundational system or unrelated
presentation design is changed. Lifecycle is complete and idle; next_sprint
remains null. No next package is selected.

Broader scenario coverage, interactive latency, presentation voice and repetitive
uncertainty phrasing, Scene Construction, natural-language player intent and
future specialized or trained narration models remain deferred.
