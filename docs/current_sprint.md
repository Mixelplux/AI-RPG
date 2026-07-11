# Current Sprint

## Sprint 10.3 - Explicit Atomic Pressure-Level Change with Durable History

Status: Complete.

## Goal

Add one deterministic, engine-owned operation that sets the exact level of one existing persistent pressure and records each material change in durable world history. The operation must validate input, preserve pressure identity, scope, type, and provenance, prepare the complete transition against a copied candidate world state, and commit pressure and history together only after the complete operation succeeds.

This sprint is a bounded atomic-transition sprint.

## Design Intent

Sprint 10.3 proves the first explicit transition of persistent reactive world state. It changes only the level of an existing pressure. It does not create pressures, derive changes from gameplay, advance time, project pressure into scenes or narration, or introduce generalized transaction or event infrastructure.

## Accepted ADR

**ADR-037 - Pressure-Level Changes Are Atomic Current-State Transitions**

An exact pressure-level change is prepared against a copied candidate world state. Pure pressure validation and record mutation remain in or near `engine/pressure_state.py`. `GameEngine` owns orchestration, durable history creation, final validation, and the single commit to `GameEngine.world_state`. A material change commits the pressure value and one `pressure_changed` history entry together. Any validation, mutation, history-construction, or final-validation failure commits neither. Setting the existing level is a successful no-op and creates no history.

## Operation Contract

The exact gameplay-facing method is:

```python
GameEngine.set_pressure_level(
    pressure_id: str,
    new_level: int,
) -> dict
```

Input rules:

- `pressure_id` must identify exactly one pressure already present in `world_state.pressures`.
- Unknown pressure IDs raise `ValueError`.
- `new_level` must be an integer from `0` through `100`, inclusive.
- Booleans are invalid even though Python treats them as integers.
- Non-integers raise `ValueError`.
- Values below `0` or above `100` raise `ValueError`.
- Do not clamp values.
- Do not interpret the input as a delta.

Result shape:

```json
{
  "changed": true,
  "pressure_id": "bryn_shander_winter",
  "previous_level": 65,
  "new_level": 70,
  "history_id": "history_000001"
}
```

No-op result shape:

```json
{
  "changed": false,
  "pressure_id": "bryn_shander_winter",
  "previous_level": 65,
  "new_level": 65,
  "history_id": null
}
```

## Pure Pressure-Mutation Boundary

Pure pressure-state logic must remain in or near `engine/pressure_state.py`.

That logic must:

- Validate the exact requested level.
- Require the targeted pressure to exist.
- Change only the targeted record’s `level`.
- Preserve `pressure_id`.
- Preserve `pressure_type`.
- Preserve `scope_type`.
- Preserve `scope_id`.
- Preserve the complete existing `provenance` object without replacement or alteration.
- Preserve every non-targeted pressure without material change.
- Operate on copied candidate data rather than live durable state.
- Return sufficient deterministic change data for `GameEngine` orchestration.
- Create no history.
- Read or advance no time.
- Access no scene, narration, player, or Region Pack mutation authority.

## Atomicity Contract

`GameEngine` owns the complete operation.

For a material change:

1. Validate the request through the narrow pressure mutation boundary.
2. Prepare the operation against a defensive candidate copy of current `world_state`.
3. Apply the level change only to the candidate.
4. Read the current durable time without changing it.
5. Add the corresponding history entry to the candidate through the existing engine-owned history mechanism.
6. Validate the completed candidate state as appropriate.
7. Assign the completed candidate to `GameEngine.world_state` exactly once.
8. Return the copy-safe result packet.

Do not assign partially changed state to `self.world_state`.

A pressure-validation, mutation, history-construction, or completed-candidate validation failure must leave both the durable pressure dictionary and durable history unchanged.

Propagate the bounded failure rather than swallowing it or returning a partial-success result.

Do not introduce:

- A transaction class
- A transaction manager
- Rollback infrastructure
- An event bus
- A command bus
- A scheduler
- Dependency injection
- Generic mutation registration

For a no-op:

- Validate the pressure ID and level normally.
- Detect that `new_level` equals the current level.
- Create no history.
- Do not replace or otherwise materially mutate durable world state.
- Return the no-op result with `history_id: null`.

## History Contract

Each material change creates exactly one durable history entry with:

- `history_id`
- `event_type`
- `summary`
- `time`
- `pressure_id`
- `pressure_type`
- `scope_type`
- `scope_id`
- `previous_level`
- `new_level`

Use:

```json
{
  "event_type": "pressure_changed",
  "summary": "Pressure bryn_shander_winter changed from 65 to 70."
}
```

The exact deterministic summary template is:

```text
Pressure {pressure_id} changed from {previous_level} to {new_level}.
```

History rules:

- Use the existing engine-owned history ID mechanism.
- Do not accept a caller-supplied history ID.
- Use a defensive copy of the current durable world time.
- Do not advance time.
- Do not attach the player’s current location.
- The pressure’s explicit `scope_type` and `scope_id` are the relevant spatial data.
- Do not record provenance in the history entry.
- Do not add a reason, cause, causal event reference, mutation provenance, taxonomy, or `updated_at` field.
- A no-op creates no history.
- Invalid requests and failed operations create no history.

## Persistence and Immutability

- The changed pressure and new history entry must survive the existing save/load path.
- Preserve save version 1.
- Do not add a migration.
- Do not change legacy pressure normalization.
- Do not reapply Region Pack seeds during loading.
- `data/regions/bryn_shander.json` remains an immutable initialization input.
- Runtime mutation must not alter `region["initial_pressures"]` or any nested seed data.
- No `engine/save_system.py` change is expected because it already persists the complete world state.

## Expected Files

Likely modified during implementation:

- `engine/pressure_state.py`
- `engine/game_engine.py`
- `test_pressure_state.py`
- `test_save_load.py`
- `docs/architecture.md`
- `docs/decisions.md`
- `docs/roadmap.md`
- `docs/sprint_log.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`
- `docs/next_chat_handoff.md`

Not expected to require modification:

- `engine/world_state.py`
- `engine/world_update.py`
- `engine/save_system.py`
- `engine/region_validator.py`
- `data/regions/bryn_shander.json`
- `play_game.py`

A file from the second list may be changed only if implementation reveals a concrete bounded necessity. Any such change must be reported and justified. Do not expand the sprint to refactor those files.

## Acceptance Criteria

1. `GameEngine.set_pressure_level(pressure_id, new_level)` exists with the exact gameplay-facing name and parameters.
2. A valid material change succeeds.
3. Exactly one existing pressure is targeted.
4. Only the targeted pressure’s `level` changes.
5. Every other field of the targeted pressure remains unchanged.
6. Existing provenance remains exactly unchanged.
7. Region Pack seed data remains exactly unchanged.
8. Every non-target pressure remains exactly unchanged.
9. Exactly one `pressure_changed` history entry is created for a material change.
10. The history entry receives a stable engine-owned history ID.
11. The operation result returns that history ID.
12. The history entry contains current durable time.
13. Durable time is not advanced.
14. The entry records previous and new levels.
15. The entry records pressure identity, type, and scope.
16. The entry does not automatically include player location.
17. Save/load preserves the changed pressure and its history entry.
18. Unknown pressure IDs raise `ValueError`.
19. Boolean levels raise `ValueError`.
20. Non-integer levels raise `ValueError`.
21. Values below `0` or above `100` raise `ValueError`.
22. Validation failures commit no pressure mutation and no history.
23. An injected history-construction failure commits no pressure mutation and no history.
24. A completed-candidate validation failure, where practically testable without broad infrastructure, commits no partial state.
25. Setting the existing level returns `changed: false`.
26. A no-op returns `history_id: null`.
27. A no-op creates no history.
28. Returned operation data cannot mutate durable state.
29. Player location remains unchanged.
30. Weather remains unchanged.
31. Current scene snapshot remains unchanged.
32. Narration behavior and narration data remain unchanged.
33. Unrelated world state remains unchanged.
34. Existing movement, waiting, conversation history, history queries, history context, narration context, narration pipeline, target resolution, destination resolution, and save/load behavior remain materially unchanged.
35. Sprint 10.3 closes only after every required verification passes.
36. Sprint 10.4 remains undefined and not started.

## Verification

Official focused commands:

```powershell
.\.venv\Scripts\python.exe test_pressure_state.py
.\.venv\Scripts\python.exe test_save_load.py
.\.venv\Scripts\python.exe test_interaction_history.py
.\.venv\Scripts\python.exe test_history_query.py
.\.venv\Scripts\python.exe test_history_context.py
.\.venv\Scripts\python.exe test_narration_context.py
.\.venv\Scripts\python.exe test_narration_pipeline.py
.\.venv\Scripts\python.exe engine/region_validator.py
.\.venv\Scripts\python.exe -m json.tool docs/current_sprint.json
.\.venv\Scripts\python.exe -c "import json, yaml; from pathlib import Path; j=json.loads(Path('docs/current_sprint.json').read_text(encoding='utf-8')); y=yaml.safe_load(Path('docs/current_sprint.yaml').read_text(encoding='utf-8')); assert type(j) is type(y) and j == y"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\validate_hardening_package.ps1 -PackageRoot .
git diff --check
```

The implementation verification plan must also include:

- A direct API smoke flow for one material pressure change.
- A no-op pressure change.
- Invalid pressure ID and invalid-level checks.
- Save/load of the changed pressure and history.
- Existing movement, wait, conversation, history review, target resolution, destination resolution, narration preview, reset, and quit smoke coverage.
- No CLI pressure-mutation command.

## Documentation Closeout Checks

Completed documentation closeout results:

1. Pressures were added to the current `world_state` ownership list in `docs/architecture.md`.
2. The stale statement that Sprint 10.2 had not started was corrected.
3. The architecture version was updated to `0.10.3`.
4. The Sprint 10.2 closeout record was retained with a corrected closeout heading rather than being replaced by Sprint 10.3.

These bounded checks were completed during Sprint 10.3 closeout correction.

## Non-Goals

- Runtime pressure creation
- Runtime pressure deletion
- Delta-based adjustment as the primitive API
- Automatic clamping
- Gameplay-event coupling
- Interaction Kernel pressure commands
- Player-facing pressure mutation
- Debug pressure mutation
- Time-based drift
- Escalation policy
- Decay policy
- Pressure consequences
- Pressure projection
- Scene rebuilding
- Narration integration
- AI-generated pressure behavior
- Causal event references
- Change-reason taxonomies
- Mutation provenance fields
- `updated_at`
- Persistent unresolved threads
- Opportunities
- Actor state
- Actor knowledge
- Evidence systems
- Generic transactions
- Event buses
- Schedulers
- Command buses
- Dependency-injection infrastructure
- Broad cleanup
- Sprint 10.4 planning

## Canonical Manifest

The JSON block below is canonical machine data and must remain structurally identical to `docs/current_sprint.json` and `docs/current_sprint.yaml`. The YAML file intentionally uses JSON syntax, which is valid YAML 1.2.

<!-- CANONICAL-MANIFEST-START -->
```json
{
  "schema_version": "1.0.0",
  "document_type": "current_sprint",
  "sprint_count": 1,
  "project": {
    "name": "AI Narrative RPG Engine",
    "principles": [
      "provider-neutral",
      "deterministic-core",
      "simulation-owned-truth"
    ]
  },
  "sprint": {
    "id": "10.3",
    "title": "Explicit Atomic Pressure-Level Change with Durable History",
    "phase": "Phase 2B - Reactive World State Foundations",
    "type": "bounded-feature",
    "mode": "single-sprint",
    "status": "complete",
    "goal": "Add one deterministic, engine-owned operation that sets the exact level of one existing persistent pressure and records each material change in durable world history. The operation must validate input, preserve pressure identity, scope, type, and provenance, prepare the complete transition against a copied candidate world state, and commit pressure and history together only after the complete operation succeeds.",
    "design_intent": "Sprint 10.3 proves the first explicit transition of persistent reactive world state. It changes only the level of an existing pressure. It does not create pressures, derive changes from gameplay, advance time, project pressure into scenes or narration, or introduce generalized transaction or event infrastructure.",
    "platform": {
      "operating_system": "Windows",
      "shell": "PowerShell",
      "official_interpreter": ".\\.venv\\Scripts\\python.exe"
    },
    "architectural_decision": {
      "adr": "ADR-037",
      "title": "Pressure-Level Changes Are Atomic Current-State Transitions",
      "policy": "An exact pressure-level change is prepared against a copied candidate world state. Pure pressure validation and record mutation remain in or near engine/pressure_state.py. GameEngine owns orchestration, durable history creation, final validation, and the single commit to GameEngine.world_state. A material change commits the pressure value and one pressure_changed history entry together. Any validation, mutation, history-construction, or final-validation failure commits neither. Setting the existing level is a successful no-op and creates no history."
    },
    "operation_contract": {
      "method": "GameEngine.set_pressure_level(pressure_id: str, new_level: int) -> dict",
      "result_shape": {
        "changed": true,
        "pressure_id": "bryn_shander_winter",
        "previous_level": 65,
        "new_level": 70,
        "history_id": "history_000001"
      },
      "no_op_result_shape": {
        "changed": false,
        "pressure_id": "bryn_shander_winter",
        "previous_level": 65,
        "new_level": 65,
        "history_id": null
      },
      "input_rules": [
        "pressure_id must identify exactly one pressure already present in world_state.pressures",
        "Unknown pressure IDs raise ValueError",
        "new_level must be an integer from 0 through 100 inclusive",
        "Booleans are invalid even though Python treats them as integers",
        "Non-integers raise ValueError",
        "Values below 0 or above 100 raise ValueError",
        "Do not clamp values",
        "Do not interpret the input as a delta"
      ]
    },
    "pressure_mutation_boundary": {
      "location": "engine/pressure_state.py",
      "requirements": [
        "Validate the exact requested level",
        "Require the targeted pressure to exist",
        "Change only the targeted record's level",
        "Preserve pressure_id, pressure_type, scope_type, scope_id, and provenance",
        "Preserve every non-targeted pressure without material change",
        "Operate on copied candidate data rather than live durable state",
        "Return sufficient deterministic change data for GameEngine orchestration",
        "Create no history",
        "Read or advance no time",
        "Access no scene, narration, player, or Region Pack mutation authority"
      ]
    },
    "atomicity_contract": {
      "material_change_flow": [
        "Validate the request through the narrow pressure mutation boundary.",
        "Prepare the operation against a defensive candidate copy of current world_state.",
        "Apply the level change only to the candidate.",
        "Read the current durable time without changing it.",
        "Add the corresponding history entry to the candidate through the existing engine-owned history mechanism.",
        "Validate the completed candidate state as appropriate.",
        "Assign the completed candidate to GameEngine.world_state exactly once.",
        "Return the copy-safe result packet."
      ],
      "no_partial_assignment": true,
      "failure_property": "A pressure-validation, mutation, history-construction, or completed-candidate validation failure must leave both the durable pressure dictionary and durable history unchanged.",
      "forbidden_infrastructure": [
        "transaction class",
        "transaction manager",
        "rollback infrastructure",
        "event bus",
        "command bus",
        "scheduler",
        "dependency injection",
        "generic mutation registration"
      ],
      "no_op_rules": [
        "Validate the pressure ID and level normally.",
        "Detect that new_level equals the current level.",
        "Create no history.",
        "Do not replace or otherwise materially mutate durable world state.",
        "Return the no-op result with history_id null."
      ]
    },
    "history_contract": {
      "entry_fields": [
        "history_id",
        "event_type",
        "summary",
        "time",
        "pressure_id",
        "pressure_type",
        "scope_type",
        "scope_id",
        "previous_level",
        "new_level"
      ],
      "event_type": "pressure_changed",
      "summary_template": "Pressure {pressure_id} changed from {previous_level} to {new_level}.",
      "rules": [
        "Use the existing engine-owned history ID mechanism",
        "Do not accept a caller-supplied history ID",
        "Use a defensive copy of the current durable world time",
        "Do not advance time",
        "Do not attach the player's current location",
        "The pressure's explicit scope_type and scope_id are the relevant spatial data",
        "Do not record provenance in the history entry",
        "Do not add a reason, cause, causal event reference, mutation provenance, taxonomy, or updated_at field",
        "A no-op creates no history",
        "Invalid requests and failed operations create no history"
      ]
    },
    "persistence_and_immutability": {
      "requirements": [
        "The changed pressure and new history entry must survive the existing save/load path",
        "Preserve save version 1",
        "Do not add a migration",
        "Do not change legacy pressure normalization",
        "Do not reapply Region Pack seeds during loading",
        "data/regions/bryn_shander.json remains an immutable initialization input",
        "Runtime mutation must not alter region[\"initial_pressures\"] or any nested seed data",
        "No engine/save_system.py change is expected because it already persists the complete world state"
      ]
    },
    "expected_files": {
      "likely_modified": [
        "engine/pressure_state.py",
        "engine/game_engine.py",
        "test_pressure_state.py",
        "test_save_load.py",
        "docs/architecture.md",
        "docs/decisions.md",
        "docs/roadmap.md",
        "docs/sprint_log.md",
        "docs/current_sprint.md",
        "docs/current_sprint.yaml",
        "docs/current_sprint.json",
        "docs/next_chat_handoff.md"
      ],
      "not_expected_to_require_modification": [
        "engine/world_state.py",
        "engine/world_update.py",
        "engine/save_system.py",
        "engine/region_validator.py",
        "data/regions/bryn_shander.json",
        "play_game.py"
      ]
    },
    "acceptance_criteria": [
      "GameEngine.set_pressure_level(pressure_id, new_level) exists with the exact gameplay-facing name and parameters.",
      "A valid material change succeeds.",
      "Exactly one existing pressure is targeted.",
      "Only the targeted pressure's level changes.",
      "Every other field of the targeted pressure remains unchanged.",
      "Existing provenance remains exactly unchanged.",
      "Region Pack seed data remains exactly unchanged.",
      "Every non-target pressure remains exactly unchanged.",
      "Exactly one pressure_changed history entry is created for a material change.",
      "The history entry receives a stable engine-owned history ID.",
      "The operation result returns that history ID.",
      "The history entry contains current durable time.",
      "Durable time is not advanced.",
      "The entry records previous and new levels.",
      "The entry records pressure identity, type, and scope.",
      "The entry does not automatically include player location.",
      "Save/load preserves the changed pressure and its history entry.",
      "Unknown pressure IDs raise ValueError.",
      "Boolean levels raise ValueError.",
      "Non-integer levels raise ValueError.",
      "Values below 0 or above 100 raise ValueError.",
      "Validation failures commit no pressure mutation and no history.",
      "An injected history-construction failure commits no pressure mutation and no history.",
      "A completed-candidate validation failure, where practically testable without broad infrastructure, commits no partial state.",
      "Setting the existing level returns changed false.",
      "A no-op returns history_id null.",
      "A no-op creates no history.",
      "Returned operation data cannot mutate durable state.",
      "Player location remains unchanged.",
      "Weather remains unchanged.",
      "Current scene snapshot remains unchanged.",
      "Narration behavior and narration data remain unchanged.",
      "Unrelated world state remains unchanged.",
      "Existing movement, waiting, conversation history, history queries, history context, narration context, narration pipeline, target resolution, destination resolution, and save/load behavior remain materially unchanged.",
      "Sprint 10.3 closes only after every required verification passes.",
      "Sprint 10.4 remains undefined and not started."
    ],
    "non_goals": [
      "Runtime pressure creation",
      "Runtime pressure deletion",
      "Delta-based adjustment as the primitive API",
      "Automatic clamping",
      "Gameplay-event coupling",
      "Interaction Kernel pressure commands",
      "Player-facing pressure mutation",
      "Debug pressure mutation",
      "Time-based drift",
      "Escalation policy",
      "Decay policy",
      "Pressure consequences",
      "Pressure projection",
      "Scene rebuilding",
      "Narration integration",
      "AI-generated pressure behavior",
      "Causal event references",
      "Change-reason taxonomies",
      "Mutation provenance fields",
      "updated_at",
      "Persistent unresolved threads",
      "Opportunities",
      "Actor state",
      "Actor knowledge",
      "Evidence systems",
      "Generic transactions",
      "Event buses",
      "Schedulers",
      "Command buses",
      "Dependency-injection infrastructure",
      "Broad cleanup",
      "Sprint 10.4 planning"
    ],
    "verification": {
      "primary_commands": [
        ".\\.venv\\Scripts\\python.exe test_pressure_state.py",
        ".\\.venv\\Scripts\\python.exe test_save_load.py",
        ".\\.venv\\Scripts\\python.exe test_interaction_history.py",
        ".\\.venv\\Scripts\\python.exe test_history_query.py",
        ".\\.venv\\Scripts\\python.exe test_history_context.py",
        ".\\.venv\\Scripts\\python.exe test_narration_context.py",
        ".\\.venv\\Scripts\\python.exe test_narration_pipeline.py",
        ".\\.venv\\Scripts\\python.exe engine/region_validator.py"
      ],
      "manifest_commands": [
        ".\\.venv\\Scripts\\python.exe -m json.tool docs/current_sprint.json",
        ".\\.venv\\Scripts\\python.exe -c \"import json, yaml; from pathlib import Path; j=json.loads(Path('docs/current_sprint.json').read_text(encoding='utf-8')); y=yaml.safe_load(Path('docs/current_sprint.yaml').read_text(encoding='utf-8')); assert type(j) is type(y) and j == y\"",
        "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\validate_hardening_package.ps1 -PackageRoot .",
        "git diff --check"
      ],
      "smoke_plan": [
        "A direct API smoke flow for one material pressure change.",
        "A no-op pressure change.",
        "Invalid pressure ID and invalid-level checks.",
        "Save/load of the changed pressure and history.",
        "Existing movement, wait, conversation, history review, target resolution, destination resolution, narration preview, reset, and quit smoke coverage.",
        "No CLI pressure-mutation command."
      ]
    },
    "documentation_closeout_checks": [
      "Pressures were added to the current world_state ownership list in docs/architecture.md.",
      "The stale statement that Sprint 10.2 had not started was corrected.",
      "The architecture version was updated to 0.10.3.",
      "The Sprint 10.2 closeout record was retained with a corrected closeout heading rather than being replaced by Sprint 10.3."
    ],
    "execution_phases": [
      {
        "id": "setup",
        "goal": "Perform Startup Review and confirm the synchronized Sprint 10.3 definition before application changes."
      },
      {
        "id": "implementation",
        "goal": "Implement only the bounded atomic pressure-level transition."
      },
      {
        "id": "verification",
        "goal": "Run every documented required check through the official project environment."
      },
      {
        "id": "closeout",
        "goal": "Record actual results, synchronize documentation, and stop without defining Sprint 10.4."
      }
    ],
    "governance": [
      "Exactly one sprint is defined at a time.",
      "Do not substitute bundled, system, Windows Store, or alternate Python for official verification.",
      "Preserve provider neutrality, deterministic behavior, simulation-owned truth, and unrelated user changes.",
      "Do not begin implementation during planning and staging.",
      "Do not define or begin Sprint 10.4."
    ],
    "closeout": {
      "allowed_terminal_statuses": [
        "complete",
        "blocked"
      ],
      "next_sprint": null
    }
  }
}

```
<!-- CANONICAL-MANIFEST-END -->
