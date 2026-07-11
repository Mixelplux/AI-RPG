# Next Chat Handoff: Sprint 10.2

## Current State

- Sprint 10.1 - Persistent Resolved Conversation Memory: complete and closed out.
- ENV-HARDENING-001: complete and closed out.
- Architecture and scope review for the next Phase 2B capability: complete.
- Sprint 10.2 - Persistent Scoped Pressure Representation: complete and closed out.
- Sprint 10.3: not defined or started.

## Sprint 10.2 Goal

Add a deterministic, validated, copy-safe, persistent representation of scoped pressures. Region Packs may provide immutable initial seeds for new games. Current pressure state belongs in `world_state`, survives save/load, and is inspectable through narrow read-only `GameEngine` methods.

Sprint 10.2 is representation-only.

## Architecture Decision

ADR-036 establishes that scoped pressures are persistent current state rather than history-only events. Store them in a dictionary at `world_state.pressures`, keyed by stable `pressure_id`. `initial_pressures` is the exact optional top-level Region Pack seed field. Its validated records are deep-copied only for new-game construction, and Region Pack provenance `source_id` must exactly equal the containing pack's `region_id`.

Canonical runtime World State always requires `pressures`. During loading only, copied version-1 legacy save data missing the field normalizes to an empty dictionary before strict validation and is not seeded from `initial_pressures`. A present malformed value fails validation. Save version 1 is preserved.

The initial record is exact and bounded:

```json
{
  "pressure_id": "bryn_shander_winter",
  "pressure_type": "winter",
  "scope_type": "region",
  "scope_id": "icewind_dale_bryn_shander",
  "level": 65,
  "provenance": {
    "kind": "region_pack",
    "source_id": "icewind_dale_bryn_shander"
  }
}
```

Initial scope types are `region` and `location`; provenance kind is `region_pack`; level is an integer from 0 through 100, excluding booleans.

Required read and inspection boundary:

- `GameEngine.get_pressures() -> dict[str, dict]`
- `GameEngine.get_pressure(pressure_id: str) -> dict | None`, returning `None` when unknown
- Defensive deep copies from both methods, including nested provenance
- Required `pressures` CLI command routed only through `GameEngine.get_pressures()`
- No direct CLI access to `world_state`, no individual-pressure command, and no mutation command

## Implementation Boundaries

- Perform Startup Review before writing code.
- Implement only the canonical Sprint 10.2 definition.
- Preserve Region Pack immutability and copy safety.
- Preserve save version 1 and the load-only legacy normalization boundary.
- Do not add mutation, drift, pressure history events, projection, AI generation, unresolved threads, actor state, consequences, schedulers, quests, or broad abstractions.
- Do not define or begin Sprint 10.3.

## Verification

Run every command and smoke step in `docs/current_sprint.md` through the official project environment. Record exact commands, exit codes, outcomes, and concise evidence. The full application test suite was not run during staging.

## Staging Outcome

The canonical Markdown, YAML, and JSON Sprint 10.2 manifests were synchronized and validated. Required Markdown headings are present. Architecture, roadmap, decision, sprint-log, review-context, and handoff records were updated. No application code or tests were modified during closeout, and Sprint 10.2 is complete.
