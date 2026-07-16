# Current Sprint Record

No sprint is currently active. The most recent terminal sprint record is
retained below for identity and closeout context.

## Most Recent Terminal Sprint

# Sprint 10.61 - Derived Player-Safe Navigation Projection

Status: Complete.

Review state: Merged.

`next_sprint` is `null`. No following sprint is authorized, staged, or
started.

## Goal

Project immediate player-perceivable navigation opportunities into natural
scene presentation without giving the projection simulation authority or
changing the established movement path.

## Expected Files

- `engine/navigation_projection.py`
- `engine/perception_builder.py`
- `engine/scene_narrator.py`
- `engine/game_engine.py`
- `test_navigation_projection.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- A direct, authored current-scene route is presented with natural orientation
  and destination language.
- The projection contains no internal identifiers, no non-adjacent geography,
  and no route whose destination cannot be safely presented.
- Repeated projection is deterministic and non-mutating; save/load and the
  existing movement path remain compatible.
- Save version remains `1`; provider/API requests are forbidden; `next_sprint`
  remains `null`.

## Verification

- Official-interpreter preflight and canonical-record validation.
- Focused navigation tests plus affected movement, narration, perception,
  save/load, and provider-safe regressions.
- `git diff --check`, clean committed candidate evidence, and the required
  review-packet validation.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"active_sprint":null,"active_capability_package":null,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.61","title":"Derived Player-Safe Navigation Projection","type":"capability-package","mode":"capability-package","status":"complete","review_state":"merged","goal":"Project immediate player-perceivable navigation opportunities into natural scene presentation without giving the projection simulation authority or changing the established movement path.","predecessor":{"id":"10.60","status":"complete","review_state":"merged"},"platform":{"official_interpreter":".\\.venv\\Scripts\\python.exe","save_version":1,"provider_requests":"forbidden"},"expected_files":{"likely_modified":["engine/perception_builder.py","engine/scene_narrator.py","engine/game_engine.py","docs/current_capability_package.md","docs/current_sprint.md","docs/current_sprint.json"],"likely_created":["engine/navigation_projection.py","test_navigation_projection.py","handoffs/derived-player-safe-navigation-projection-10.61-<short-head>.zip"]},"acceptance_criteria":["A direct, authored current-scene route is presented with natural orientation and destination language.","The projection contains no internal identifiers, no non-adjacent geography, and no route whose destination cannot be safely presented.","Repeated projection is deterministic and non-mutating; save/load and the existing movement path remain compatible.","Save version remains 1; provider/API requests are forbidden; next_sprint remains null."],"verification":{"staging_commands":["Official-interpreter preflight through the established workspace procedure","Canonical record validation","git diff --check"],"focused_commands":["Focused navigation projection tests","Affected movement, scene narration, perception, and save/load regressions","Provider-safe regressions only"],"closeout_commands":["Official-interpreter preflight","Canonical record validation","git diff --check","Clean committed review-candidate Git evidence","Required review-packet assembly and validation"]},"execution_phases":[{"id":"package-and-sprint-staging","status":"complete"},{"id":"derived-projection-and-presentation","status":"complete"},{"id":"focused-verification","status":"complete"},{"id":"review-candidate","status":"complete"}],"governance":["Exactly one active sprint is staged.","The projection is derived from current-scene exits and authored geography; it is not persistent World State.","No parser expansion, movement redesign, provider/API request, or follow-on capability is authorized.","Save version remains 1 and next_sprint remains null."],"closeout":{"allowed_terminal_statuses":["complete","blocked"],"verification_result":"Focused navigation tests and the complete local deterministic regression suite passed. No live provider/API request occurred; provider coverage used fake transport only. The candidate preserves save version 1 and next_sprint null. The accepted candidate was strict-fast-forward merged into main.","next_sprint":null}}}
```
<!-- CANONICAL-MANIFEST-END -->
