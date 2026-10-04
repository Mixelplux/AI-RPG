# Sprint 10.79 implementation handoff

## Reconciliation

October 4, 2026. The candidate branch was `codex/west-road-market-causality`,
directly based on protected baseline
`8d52ab0ef763846c598af8af29236475d34f42be`
(`feat: add character competence v1`); `main` still pointed to that baseline
before integration. Owner smoke changed `saves/savegame.json`, which is runtime
state and is excluded from the Sprint 10.79 package. The owner accepted Sprint
10.79 after the projection correction and successful re-smoke. Sprint 10.78's
historical handoff is unchanged; `next_sprint` remains null.

## Exact causal semantics

Existing guard allocation is represented by the West-Road phase, not a numeric
guard field. Only `observers_withdrew` and `withdrawal_route_found` explicitly
keep other approaches thin. The patrol's initial one-hour resolution runs
before its reduced allocation is established. Timing starts at the accepted
`observers_withdrew` outcome, after that hour. This preserves the requested
identical survey starting conditions and one-hour tactical headroom.

The specific authoritative `world_state.west_road_market_theft` record contains:

- `coverage_started_elapsed_hours`: start of the active qualifying interval,
  or null when normal coverage is restored;
- `theft_history_id`: reference to the one established incident, or null.

Current elapsed time minus the interval start gives qualifying duration.
Pursuit and a full competence result keep the same interval running; they do
not reset it. The existing `restore coverage` decision clears the start. It is
available in `observers_withdrew`, including after partial/failed investigations,
but not after a full survey/pursuit reaches `withdrawal_route_found`. No new
restoration path or command was introduced.
Restoration is terminal in the existing phase graph: there is no valid second
guard-diversion command within one playthrough. The review verifies that the
allocation helper sets a fresh start on a new normal-to-reduced transition and
keeps it unchanged during continued reduction, in isolation. That helper check
does not claim a playable restart branch or authorize one.

Every existing engine time transition passes through the time candidate
preparation hook. If `previous_elapsed < start + 2 <= new_elapsed`, the candidate
records exactly one `market_approach_theft` event, at elapsed `start + 2`, even
when a single transition advances farther. Its backward source reference is
the crossing `time_advanced` event; its location is `market_square`. The record
points to that incident. The phase controls qualifying allocation, not the
command name, competence tag, observation or narration. Already-established
incidents cannot retrigger, including after restoration.

## Revelation and presentation

Market Square derives a copied local location description containing the
teamster, supply sled, cut lashing, missing lamp-oil crate, and watchman's account
of thin patrol coverage. Region Pack content is unchanged. Before occurrence,
that description contains no incident. After occurrence, scene rebuilding,
perception, current-scene projection and deterministic narration reveal the
same established facts. Repeated reads and visits do not mutate incident state.
Away from the market the incident is absent from scene/narration context;
clues, actor knowledge and the resume summary do not acquire it automatically.
Simulation history remains available through the existing explicit world-history
diagnostics; those diagnostics are not an automatic fiction/knowledge projection.

The local narration context adds the explicit independence/unknown-identity/no
quest constraint to its existing drift guardrail. No thief, motive, observer
connection, faction connection or conspiracy is established. No discovery,
actor-knowledge membership, quest or thread is created by the theft.

Directly touched competence presentation omits status/command labels and
engine-only narration rules from playable prose, removes repeated finding text,
and gives failed investigations concrete wording. Internal layered statuses and
evidence limits remain available to tests/debug/narration context. Other
presentation and West-Road behavior are preserved.

## Persistence and transaction review

Save version stays 1. New saves persist the interval start and incident reference
with the existing history. Mid-interval reload continues from the saved start;
post-event reload retains the same event and cannot double-apply it.

For an older version-1 save missing the additive record, only the copied loaded
payload is normalized. Normal-coverage saves receive an empty record. An
already-reduced allocation starts monitoring at saved elapsed time: its older
unrecorded duration is not inferred, and no past theft is invented. Historical
completed pursuit remains valid. Missing record with an existing theft event
rejects rather than erasing it. Prototype saves still reject under existing policy.

Malformed present record shape/types, invalid intervals, overdue unestablished
thresholds, missing/duplicate/mismatched incident references, unsupported event
fields/facts, wrong timestamps or nonqualifying causal sources reject. Engine
validation occurs before publication. The existing candidate-copy/validate/
scene-build/publish boundary covers the event and timing; injected validation,
scene or later discovery failures leave the original world and scene intact.
Failed load preserves the current session and source save bytes. Projection is
read-only. No general scheduler, transaction system or presentation architecture
was introduced; no save migration or new architectural subsystem was needed.
The completion review corrected a malformed-load rejection gap: missing additive
records previously reached unchecked coverage/time/history accesses, and some
malformed current records also reached unchecked coverage/time access. These
could raise AttributeError instead of the ValueError caught by the CLI. Specific
shape/type checks now reject them cleanly without changing valid-save behavior.

## Observed causal cases

| Case | Observed result |
|---|---|
| Ordinary survey | Two qualifying hours; theft established at start + 2. |
| Tactical survey | One qualifying hour; no theft. |
| Tactical survey + wait | Second qualifying hour establishes theft. |
| Composed activities | Partial follow-withdrawal-signs + partial reconstruction, one hour each, establish the same theft. |
| Timed navigation | One-hour investigation + existing one-hour road traversal also establish theft away from the market. |
| Restore before threshold | Partial one-hour investigation, restore, then five hours: no theft. |
| Restore after threshold | Existing incident survives restoration and further time. |
| Nonqualifying allocation | Initial/investigating/continue-investigation phases do not trigger the theft. |
| Large time transition | Five-hour step records occurrence at start + 2, once. |
| Before/after save-load | Timing continues correctly; established incident and restoration round-trip without retriggering. |
| Market observation | Before threshold no theft; after threshold read-only revelation of existing truth. |

## Verification

Syntax checks passed for all six changed engine modules and the new test script.
All thirteen focused groups in `test_west_road_market_theft.py` passed, including
compatibility/malformed saves, failed load, failed commands and publication
rollback, helper restart bounds, automatic knowledge isolation and scripted CLI
ordinary/tactical/restoration comparisons with save/load. Character competence's
seven existing groups in `test_character_competence.py` passed. The listed affected regressions were rerun during
the bounded completion review after the load-rejection correction and passed.

Affected offline regression scripts passed:
`test_west_road_predicament.py`, `test_west_road_presentation.py`,
`test_contextual_action_projection.py`, `test_current_scene_projection.py`,
`test_discovery.py`, `test_actor_knowledge.py`, `test_actor_knowledge_response.py`,
`test_save_load.py`, `test_world_update.py`,
`test_elapsed_time_transition_observation.py`, `test_time_pressure_effect.py`,
`test_time_actor_relocation.py`, `test_time_evidence_trace_effect.py`,
`test_navigation_projection.py`, `test_one_hour_west_road_exit_traversal.py`,
`test_western_trade_road_arrival_discovery.py`, `test_narration_context.py`,
`test_narration_request.py`, `test_narration_prompt.py`,
`test_narration_output.py`, and `test_narration_pipeline.py`.

`test_narration_source.py` and `test_openai_responses_narration.py` passed with
an offline tokenizer stub and fake transport. A separate cache-only probe
confirmed the real tokenizer cache is unavailable without attempting a download.
Exact tokenizer-backed counts/input-limit behavior remain unverified, matching
the accepted baseline limitation. The provider adapter is unchanged; no live
provider was contacted. Full repository gameplay suite was not run.

Maintained GitWorkflowTools verification passed with
`Profiles/AINarrativeRPG.psd1`: official interpreter, preflight, lifecycle JSON,
project record validator, working/index diff checks and unchanged Git state.
The ignored log is `.artifacts/sprint_10_79_git_verification.log`. The initial
branch write was blocked by the sandbox; the narrowly authorized elevated Git
branch creation succeeded without changing ACLs or shared tools. Generated
test files stayed under `.artifacts/` and were cleaned by their owning tests.
The completion-review maintained verification also passed; its ignored log is
`.artifacts/sprint_10_79_completion_review_git_verification.log`. Exact candidate
set comparison, protected HEAD comparison and empty-index checks passed. Both
documented interactive smoke launchers were syntax/startup checked without
creating a smoke save. No live provider was contacted during the review.

## Changed files and owner smoke

Implementation: `engine/west_road_market_theft.py`, `engine/game_engine.py`,
`engine/world_state.py`, `engine/save_system.py`, `engine/scene_loader.py`,
`engine/character_competence.py`. Verification: `test_west_road_market_theft.py`.
Records: `docs/current_capability_package.md`, `docs/current_sprint.md`,
`docs/current_sprint.json`, and this handoff. Scene-loader integration is directly
necessary for the already-approved local revelation; no Region Pack was changed.

Ordinary owner smoke from a new CLI session (`.\.venv\Scripts\python.exe play_game.py`):

```text
go to Southwest Trade Road
investigate
talk to Mara
go to North Gate
present Repeated Watch Tracks to Elin
present Mara's Account to Elin
advocate patrol
arrange guarded local survey
go to Market Square
```

For an interactive comparison with an initial tactical profile, run the following
PowerShell fixture from the repository root. It uses the existing initial-world-
state interface and only substitutes CLI startup; no profile UI or gameplay
command is added. Use `ordinary` or `tactical_assessment` as the final argument.
Smoke saves go to separate approved `.artifacts/` paths instead of the ordinary
session save. Quit and relaunch for each fresh comparison; do not use reset to
select a profile.

```powershell
$smokeScript = @'
import sys
from unittest.mock import patch
import play_game
from engine.game_engine import GameEngine
profile = sys.argv[1]
state = GameEngine(play_game.REGION_PATH).get_world_state()
state["player"]["competences"] = [] if profile == "ordinary" else ["tactical_assessment"]
session = GameEngine(play_game.REGION_PATH, initial_world_state=state)
play_game.SAVE_PATH = ".artifacts/sprint_10_79_owner_smoke_" + profile + ".json"
with patch.object(GameEngine, "start_new", return_value=session):
    play_game.main()
'@
& .\.venv\Scripts\python.exe -c $smokeScript tactical_assessment
```

Read the people, evidence and dialogue in each scene; avoid world-history/debug
commands for these fiction comparisons. Follow the common setup above through
`advocate patrol`, then use these short paths:

| Path | Commands and expected playable result |
|---|---|
| Ordinary | `arrange guarded local survey`, `save`, `load`, `go to Market Square`: teamster, cut lashing and missing lamp oil. Save/load again: same incident. |
| Tactical | `arrange guarded local survey`, `save`, `load`, `go to Market Square`: no theft scene yet. The market visit creates nothing. |
| Tactical headroom spent | From that market, `wait`: the teamster scene now appears. Save/load: it remains established. Alternatively wait at the gate first, then visit the market to reveal the already-existing event. |
| Restore early | Fresh ordinary run after `advocate patrol`: `wait`, `restore coverage`, `save`, `load`, `wait`, `wait`, `go to Market Square`: no theft from the ended interval. |

The composed two-activity path is verified with deterministic partial draws in
the focused regression; owner smoke does not rely on an uncontrolled draw.

## Findings and status

Required before initial owner smoke: malformed-load rejection correction completed;
no outstanding implementation or verification correction.
Recommended: owner smoke/review of the uncommitted slice; real-tokenizer
verification when its existing cache is available.
No action: observer identity/faction, quest creation, broader town simulation,
new restoration choices, save-version changes or next-package work.

The initial eleven-file handoff passed bounded completion review after the
load-validation correction. The owner-smoke correction below supersedes its
initial READY FOR OWNER SMOKE status. This remains an uncommitted implementation
handoff, not a committed candidate or owner acceptance. Sprint 10.79 stays active.

## Owner-smoke scene-projection correction

Owner smoke confirmed ordinary/tactical timing, another qualifying hour, early
restoration, pre-threshold market observation and save/load. It exposed remote
West-Road circumstances, findings and resolution hints in Market Square prose.
`GameEngine.get_narration()` used region-wide predicament availability to append
`CURRENT_CIRCUMSTANCES` and `CURRENT_CHOICE_HINTS` at every location.
`character_competence.project()` likewise published persistent findings and
accepted outcomes globally into perception, current-scene and narration-context
packets. Existing observation relevance already distinguished the road evidence
context and North Gate report context; region availability was too broad.

`west_road_predicament.scene_relevant()` now expresses that existing road/gate
boundary for deterministic scene narration and competence projection. Other
locations use the existing generic scene narrator. Explicit clue review, resume,
dialogue, history and authoritative state are unchanged. No threshold, time cost,
allocation, competence resolution, discovery, persistence or save-version change
was made. There is no general narrative-selection framework or prose redesign.

The interrupted new regression had two test defects: `get_player_discoveries()`
returns a tuple of IDs whereas stored discoveries are a list (not enriched clue
records); `pursue observers` advances no time and cannot alone meet the two-hour
theft threshold. The repaired test compares matching ID values and separately
verifies explicit clue titles/text, and exercises pursuit before and after two
qualifying hours. Market arrival rebuilds the scene with `visible_text()` in
its copied description when the incident exists; no investigation is required.
The existing theft regression was updated to require the withdrawal finding in
explicit market clue review, absent from market scene prose, and present once
in North Gate scene prose.

Syntax checks and these offline scripts passed:
`test_west_road_scene_relevance.py`, `test_west_road_market_theft.py`,
`test_character_competence.py`, `test_west_road_predicament.py`,
`test_west_road_presentation.py`, `test_current_scene_projection.py`,
`test_contextual_action_projection.py`, `test_navigation_projection.py`,
`test_one_hour_west_road_exit_traversal.py`,
`test_western_trade_road_arrival_discovery.py`, `test_save_load.py`,
`test_narration_context.py`, `test_narration_request.py`,
`test_narration_prompt.py`, `test_narration_output.py`,
`test_narration_pipeline.py`. The new script checks six causal setups, repeated
read-only projection, exact state preservation on leaving, return to gate/road,
explicit clues and market save/load reconstruction. Maintained Git verification
passed with official interpreter, preflight, lifecycle/project-record validation,
working/index diff checks and unchanged repository state. Its ignored log is
`.artifacts/sprint_10_79_scene_relevance_git_verification.log`.
The final explanatory-record checks are recorded in
`.artifacts/sprint_10_79_scene_relevance_final_git_verification.log`.
The accepted tokenizer-cache limitation remains; no live provider was contacted.

The exact thirteen-file Sprint 10.79 package set is:
`docs/current_capability_package.md`, `docs/current_sprint.json`,
`docs/current_sprint.md`, `docs/sprint_10_79_handoff.md`,
`engine/character_competence.py`, `engine/game_engine.py`,
`engine/save_system.py`, `engine/scene_loader.py`,
`engine/west_road_market_theft.py`, `engine/west_road_predicament.py`,
`engine/world_state.py`, `test_west_road_market_theft.py`,
`test_west_road_scene_relevance.py`.
Modified `saves/savegame.json` is excluded owner runtime state and remains
unstaged. Sprint 10.79 is owner-accepted and complete; `next_sprint` remains
null. The final accepted package is staged on the candidate branch for the
authorized commit and fast-forward integration.

Minimal re-smoke from an ordinary survey-completed session: `go to Market Square`,
`look`, `go to North Gate`. The market should show the established lamp-oil theft
without remote resolution/status; the gate should still show West-Road state.
For existing tactical one-hour/restored comparison sessions, a market read should
show neither theft nor remote status. Reload at the market if desired to confirm
the same projection; fixture paths remain as documented above.

Owner re-smoke passed after the projection correction: Market Square showed the
established theft without remote West-Road status; North Gate again showed the
relevant West-Road state. Look/read remained non-mutating. The owner accepted
Sprint 10.79 on October 4, 2026. Narrative Scenario Quality concerns remain
deferred and are not part of this sprint.
