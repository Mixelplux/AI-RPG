# North-Gate Working Context V1 correction handoff

Routine, October 11, 2026. Corrected owner-smoke findings within the existing
milestone; owner accepted the corrected smoke on October 11, 2026. Lifecycle is
complete/idle and no next milestone is selected. Git publication remains pending. Branch: codex/north-gate-working-context-v1.
HEAD/protected baseline: c0d75f0cd4b026eba0326f7f6cafc5348c6b70ca.
Uncommitted working diff; index empty; no commit, merge or push.

## Exact corrections

- engine/west_road_predicament.py: bounded Elin dialogue now selects acknowledgements
  from authoritative zero/one/two report receipts while investigating. Both-receipt
  dialogue uses current decision availability when a scene is supplied. Accepted
  phases retain existing witnessed outcome responses. No state mutation.
- engine/game_engine.py: supplies the current scene to that existing response
  projection for ordinary conversation; transition/resolution code is unchanged.
- engine/north_gate_discussion.py: uses the same dialogue projection for focused
  exchanges, naturally resumes a suspended valid topic on a successful resolved
  Elin conversation, and identifies changed report exchanges for focused feedback.
  Return alone and unrelated/failed conversation do not resume it.
- play_game.py: prints focused follow-through only for relevant changed report
  exchanges; ordinary talk delivers its contextual NPC reply once. Existing
  suspension/resumption/conclusion notices occur on transitions, rather than
  replaying unchanged status after unrelated commands.
- test_north_gate_discussion.py: receipt matrix, ordinary/focused consistency,
  natural resumption without disclosure, absent/invalid-topic checks, non-repetition
  and updated fallback/comparison expectations; fourteen focused tests total.
- docs/architecture.md, current_capability_package.md, current_sprint.md,
  current_sprint.json, north_gate_working_context_v1_handoff.md and this correction
  handoff: accurate current behavior and verification; lifecycle is complete/idle after acceptance.

The smoke launcher is unchanged from the initial milestone. No authored content,
report discovery/sharing, eligibility, time, knowledge ownership, outcome, save
version, doctrine or wider predicament mechanics changed. Owner checkout/saves
and earlier research/implementation evidence remain preserved.

## Verification

All five corrected runtime/test Python files passed AST checks before execution.
Fourteen focused tests pass. All ten directly affected regression scripts pass:
Scene Construction, West-Road predicament, competence, save/load, presentation,
resolved narration, player scene route, market theft, current-scene projection
and contextual-action projection. The guard recorded zero network attempts.
Focused and isolated routes still produce identical authoritative save payloads.
Fallback, cancellation, interruptions, exactly-once receipts/decision/cost and
version-1 save/restart boundaries remain tested. No provider evaluation occurred.

Actual before/after transcripts, pre-correction source copies, concise comparison
and per-suite logs: C:/tmp/AI-RPG-North-Gate-Working-Context-V1/correction-20261011.
Previous evidence files were not overwritten.

## Actual concise before/after

```text
Tracks received, Mara account not yet received:
Before Elin: Bring me the tracks and the merchant account. Immediate patrols cost other coverage; further investigation takes an hour while traffic remains exposed.
After Elin: I've received your report about the tracks. I still need Mara's account before we choose a response.

Travel -> unrelated investigation/Mara conversation -> return -> talk to Elin:
Before repeated paused notices: 7
After suspension notices: 1
After natural resumption notices: 1

Both receipts, decision still open:
Elin: I have your track report and Mara's account. We can weigh an immediate patrol against another hour of investigation. A patrol draws guards from other approaches; waiting leaves road traffic exposed. The choice is still yours.

After accepted patrol decision:
Elin: Those guards are still off their ordinary circuit. Follow the signs, or bring them back?
```

The later follow-up question belongs to the continuing predicament; it does not
reopen the concluded report-and-patrol-decision exchange. Starting or resuming
that old topic after an accepted decision is rejected.

## Remaining limits

Only this Elin topic and existing resolved conversation command are supported.
No automatic evidence sharing, interviews, information-disclosure mechanics,
general natural-language intent, NPC autonomy or new scenes were added. Focus
is session-only and not restored across load/reset/exit; failed load preserves
it, and saving alone keeps it in the running session. Structural validation
still does not certify arbitrary generated prose. The owner accepted the corrected
conversational experience on October 11, 2026. Authored advance knowledge of
Mara/tracks and fixed report prerequisites are accepted testing limitations.
See [deferred findings](deferred_findings.md); no further V1 correction is authorized.

## Short owner smoke

From the isolated worktree root, run:

```powershell
.\.venv\Scripts\python.exe tools/play_north_gate_discussion_smoke.py
```

```text
discuss patrol with Elin
go to Southwest Trade Road
investigate
talk to Mara
go to North Gate
talk to Elin
present Repeated Watch Tracks to Elin
talk to Elin
present Mara's Account to Elin
talk to Elin
advocate patrol
talk to Elin
quit
```

Check one suspension notice, no return-only resumption, natural resumption on
talk, receipt-appropriate replies, one local conclusion and an outcome-aware
later reply. To check the other one-report branch, present Mara's account first
on a fresh run. `resume patrol discussion` remains optional. Cancellation and
load/reset/exit can be checked using the original interruption route.

No commit/staging/merge/push authority has been granted. Owner acceptance is recorded;
Git publication remains pending. Lifecycle is complete/idle; no next milestone starts.
