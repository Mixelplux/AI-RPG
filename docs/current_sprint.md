# Current Sprint Record

No sprint is currently active. The most recent terminal sprint record is
retained below for identity and closeout context.

## Most Recent Terminal Sprint

# Sprint 10.65 - One Player-Safe Local Route Guidance Projection

Status: Complete.

Review state: Merged.

`next_sprint` is `null`. No following sprint is authorized, staged, or
started.

## Goal

Derive one deterministic, player-safe presentation of the current scene's
immediate traversable connections as natural local route cues, without turning
navigation into a compass grid or destination-routing system.

## Expected Files

- `engine/navigation_projection.py`
- `engine/game_engine.py`
- `engine/perception_builder.py`
- `engine/scene_narrator.py`
- `test_navigation_projection.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- Route cues describe only immediate, traversable connections from the current
  player scene; they do not describe the relative position of non-adjacent or
  merely known destinations.
- Cues are deterministic, player-safe, and phrased as natural local routes,
  for example `Main Street continues south into town.`
- Local orientation may be included only where it meaningfully describes an
  immediate route; the result is not a raw compass grid.
- Structural connectivity remains authoritative and separate from the derived
  presentation projection; movement behavior is unchanged.
- The projection adds no World State, history, save data, narration context,
  provider authority, migration, or save-version change. `next_sprint` remains
  `null`.

## Verification

- Official-interpreter preflight, syntax checks, canonical-record validation,
  and `git diff --check` pass.
- Focused local-route projection coverage proves immediate-only selection,
  deterministic cue wording and order, optional-orientation boundaries,
  non-persistence, and non-disclosure of nonlocal destination relationships.
- Affected navigation, movement, scene, save/load, narration-context, and
  provider-safe regressions pass. No live provider request occurred.
- The accepted candidate was strict-fast-forward merged into `main`; no
  following sprint is active or authorized, save version remains `1`, and
  `next_sprint` remains `null`.
