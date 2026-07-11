# Current Sprint

## Sprint 10.5 - One Declared Resolved-Conversation Pressure Consequence

Status: Planned.

## Goal

Add one strict Region Pack declaration that maps a successful conversation with one exactly resolved entity to one exact level for one existing seeded pressure.

For a matching material effect, the `player_conversation` source event, pressure mutation, and linked `pressure_changed` consequence must be prepared in one candidate world state and committed atomically.

## Design Intent

Sprint 10.5 completes the first deterministic gameplay-event-to-world-consequence path by reusing the conversation, pressure, exact-mutation, durable-history, and causal-reference seams already implemented.

It adds one conversation-specific declaration shape. It does not add a generic rule engine, multiple effects, autonomous simulation, or pressure projection.

## Expected ADR

**ADR-039 - One Region-Declared Resolved Conversation and Its Pressure Consequence Commit Atomically**

Region-specific effect policy belongs in strict immutable Region Pack data. `GameEngine` owns lookup and candidate-state orchestration. The existing Sprint 10.4 public linked-transition method retains its already-durable-source contract.

## Region Declaration

```json
{
  "conversation_pressure_effects": [
    {
      "effect_id": "north_gate_captain_scrutiny",
      "target_entity_id": "captain_darvin_grey",
      "pressure_id": "bryn_shander_gate_scrutiny",
      "new_level": 25
    }
  ]
}
```

The canonical Bryn Shander pack should also seed `bryn_shander_gate_scrutiny` as a location-scoped `guard_attention` pressure at level 10. Do not misuse the existing winter pressure for this conversation consequence.

## Successful Material Path

1. Resolve a successful conversation with Captain Darvin Grey.
2. Copy current durable world state.
3. Add the normal `player_conversation` source entry to the candidate.
4. Capture its engine-owned `history_id`.
5. Match the one strict declaration.
6. Prepare the exact pressure transition in the same candidate.
7. Add one `pressure_changed` entry referencing the source.
8. Validate the completed candidate.
9. Build the required candidate scene.
10. Commit world state once and replace the scene only after all preparation succeeds.

## Unmatched and No-Op Behavior

A successful conversation with no declaration keeps the existing source-only behavior.

A repeated matching conversation at the declared level still commits its new `player_conversation` entry, but creates no `pressure_changed` entry. Its result reports `changed: false`, `history_id: null`, and the new `source_history_id`.

## Ownership

- Region Pack owns immutable exact policy.
- Region validation owns strict shape and cross-reference validation.
- Interaction Kernel remains policy-free.
- World Update constructs the conversation source event.
- Pressure State remains history-free and policy-free.
- World State retains stable IDs and backward-only causal validation.
- `GameEngine` composes and commits the matched source and consequence.
- Save/load persists results but neither persists nor replays declarations.

## Expected Files

Likely modified:

- `engine/game_engine.py`
- `engine/world_update.py`
- `engine/region_validator.py`
- `data/regions/bryn_shander.json`
- `test_conversation_pressure_effect.py`
- `test_interaction_history.py`
- `test_save_load.py`
- Canonical architecture, ADR, roadmap, sprint-log, sprint-manifest, and handoff files

Possibly modified only for a concrete bounded need:

- `engine/pressure_state.py`
- `test_pressure_state.py`
- Existing focused Region Pack validation tests
- `engine/scene_loader.py`

## Acceptance Criteria

The canonical machine manifest below is the complete acceptance contract. Core requirements include:

- Strict optional declaration validation.
- One exact Captain Darvin Grey effect and one credible seeded gate-scrutiny pressure.
- Source-first causal history ordering.
- One candidate state and one final durable assignment for a material matched effect.
- Source-only unmatched behavior.
- Source-committing consequence no-op behavior.
- Fail-closed state and scene atomicity.
- Save/load preservation without replay.
- Sprint 10.3 and 10.4 pressure APIs preserved.
- No rule engine, autonomous progression, projection, narration coupling, or Sprint 10.6 work.

## Verification

Use the official project interpreter only. Run every command in the canonical manifest, including focused conversation-effect, interaction-history, pressure, save/load, target, world-update, time, history, narration, Region Pack, manifest, and diff checks.

## Non-Goals

No generic event effects, extra event types, multiple consequences, deltas, predicates, ordering, scripts, transactions, event buses, schedulers, autonomous simulation, time drift, applicability resolver, projection, narration context, runtime pressure creation, actor systems, unresolved threads, evidence, AI mutation, new CLI commands, broad cleanup, packet-workflow repair, or Sprint 10.6 planning.

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
    "id": "10.5",
    "title": "One Declared Resolved-Conversation Pressure Consequence",
    "phase": "Phase 2B - Reactive World State Foundations",
    "type": "bounded-feature",
    "mode": "single-sprint",
    "status": "planned",
    "goal": "Add one strict Region Pack declaration that maps a successful conversation with one exactly resolved entity to one exact level for one existing seeded pressure. When the declaration matches, the player_conversation source event, material pressure mutation, and linked pressure_changed consequence must be prepared in one candidate world state and committed atomically.",
    "design_intent": "Sprint 10.5 completes the first deterministic gameplay-event-to-world-consequence path by reusing the Sprint 10.1 conversation event, Sprint 10.2 persistent pressure state, Sprint 10.3 exact pressure mutation, and Sprint 10.4 stable causal reference. It introduces one conversation-specific declarative effect shape, not a generic rule engine, and does not project pressure into scenes, perception, narration, or autonomous simulation.",
    "platform": {
      "operating_system": "Windows",
      "shell": "PowerShell",
      "official_interpreter": ".\\.venv\\Scripts\\python.exe"
    },
    "architectural_decision": {
      "adr": "ADR-039",
      "title": "One Region-Declared Resolved Conversation and Its Pressure Consequence Commit Atomically",
      "policy": "A strict immutable Region Pack declaration may map one exactly resolved conversation target to one existing seeded pressure and one exact resulting level. GameEngine owns declaration lookup and candidate-state orchestration. For a material match, it prepares the player_conversation source event first, then the linked pressure_changed consequence in the same candidate world state, validates the completed candidate, prepares any required derived scene, and commits runtime state only after all preparation succeeds. The existing public Sprint 10.4 linked-transition method retains its already-durable-source contract. No generic effect engine, multiple-effect ordering, replay, or autonomous behavior is introduced."
    },
    "region_declaration_contract": {
      "field": "conversation_pressure_effects",
      "optional": true,
      "item_shape": {
        "effect_id": "north_gate_captain_scrutiny",
        "target_entity_id": "captain_darvin_grey",
        "pressure_id": "bryn_shander_gate_scrutiny",
        "new_level": 25
      },
      "validation_rules": [
        "The field is absent or is a list.",
        "Each item is a mapping with exactly effect_id, target_entity_id, pressure_id, and new_level.",
        "effect_id is a non-empty string and is unique within the Region Pack.",
        "target_entity_id is a non-empty string and references exactly one Region Pack entity.",
        "At most one declaration targets a given target_entity_id.",
        "pressure_id is a non-empty string and references exactly one initial_pressures entry.",
        "new_level satisfies the existing exact pressure-level contract.",
        "Booleans, non-integers, and values outside 0 through 100 are invalid.",
        "Malformed declarations fail Region Pack validation before gameplay begins."
      ],
      "canonical_region_data": {
        "new_pressure": {
          "pressure_id": "bryn_shander_gate_scrutiny",
          "pressure_type": "guard_attention",
          "scope_type": "location",
          "scope_id": "bryn_shander_gate_north",
          "level": 10,
          "provenance": {
            "kind": "region_pack",
            "source_id": "icewind_dale_bryn_shander"
          }
        },
        "effect": {
          "effect_id": "north_gate_captain_scrutiny",
          "target_entity_id": "captain_darvin_grey",
          "pressure_id": "bryn_shander_gate_scrutiny",
          "new_level": 25
        },
        "reason": "The existing winter pressure must not be misused as a consequence of initiating a conversation. One narrow location-scoped guard-attention pressure provides a credible deterministic demonstration."
      }
    },
    "gameplay_contract": {
      "source_event_type": "player_conversation",
      "match_requirements": [
        "The conversation interaction succeeds.",
        "Current-scene target resolution status is resolved.",
        "The resolved target type is entity.",
        "The resolved stable entity identifier exactly matches one declaration."
      ],
      "material_match_result_shape": {
        "pressure_consequence": {
          "effect_id": "north_gate_captain_scrutiny",
          "changed": true,
          "pressure_id": "bryn_shander_gate_scrutiny",
          "previous_level": 10,
          "new_level": 25,
          "history_id": "history_000002",
          "source_history_id": "history_000001"
        }
      },
      "no_op_match_result_shape": {
        "pressure_consequence": {
          "effect_id": "north_gate_captain_scrutiny",
          "changed": false,
          "pressure_id": "bryn_shander_gate_scrutiny",
          "previous_level": 25,
          "new_level": 25,
          "history_id": null,
          "source_history_id": "history_000003"
        }
      },
      "unmatched_behavior": [
        "A successful resolved entity conversation with no declaration retains the existing source-only behavior.",
        "Exactly one player_conversation entry is created.",
        "No pressure changes and no pressure_changed consequence is created.",
        "The interaction result does not contain pressure_consequence."
      ],
      "failed_resolution_behavior": [
        "Unresolved, ambiguous, non-entity, unsuccessful, and exit targets create neither a conversation source event nor a pressure consequence.",
        "Existing target-resolution messages and behavior remain materially unchanged."
      ]
    },
    "ownership_boundary": {
      "region_pack": [
        "Own immutable conversation-to-pressure effect policy.",
        "Own the seeded pressure that the declaration references.",
        "Declare only exact identifiers and an exact target level.",
        "Own no runtime history and perform no mutation."
      ],
      "region_validator": [
        "Validate the optional declaration field strictly.",
        "Reject unknown entities, unknown pressures, duplicate effect IDs, duplicate target mappings, extra fields, and invalid levels.",
        "Do not implement runtime effect selection or mutation."
      ],
      "interaction_kernel": [
        "Continue to identify conversation intent.",
        "Do not select pressure effects or mutate world state.",
        "Require no modification unless a concrete existing-contract defect is discovered."
      ],
      "world_update": [
        "Continue to construct the durable resolved-conversation source event.",
        "Expose or preserve the candidate source history ID needed by GameEngine orchestration.",
        "Do not read Region Pack effect policy."
      ],
      "pressure_state": [
        "Continue to own exact pressure ID and level validation.",
        "Continue to prepare copied pressure-level changes.",
        "Create no history and read no Region Pack effect declarations."
      ],
      "world_state": [
        "Continue to own engine-generated stable history IDs.",
        "Continue to validate backward-only source_history_id integrity.",
        "Require no new causal schema."
      ],
      "game_engine": [
        "Resolve the conversation target through existing boundaries.",
        "Look up at most one matching declaration.",
        "Prepare the source event and any material consequence in one candidate world state.",
        "Reuse a non-committing candidate form of the Sprint 10.4 linked-transition logic.",
        "Validate completed candidate world state.",
        "Prepare the required candidate scene before live assignment for the matched path.",
        "Commit world_state once and replace scene_snapshot only after all preparation succeeds.",
        "Return copy-safe consequence metadata."
      ],
      "save_system": [
        "Continue to persist complete world state.",
        "Do not persist or replay Region Pack declarations.",
        "Preserve save version 1."
      ]
    },
    "internal_composition_contract": {
      "public_api_compatibility": [
        "GameEngine.set_pressure_level_from_event retains its existing public name, parameters, and already-durable-source behavior.",
        "GameEngine.set_pressure_level retains its existing public contract.",
        "No new general public transaction or effect API is required."
      ],
      "candidate_helper_expectations": [
        "A private or otherwise non-public helper may accept candidate world state, pressure_id, new_level, and source_history_id.",
        "The helper must not assign GameEngine.world_state.",
        "The helper may prepare a no-op or a material linked transition against the candidate.",
        "The helper must preserve Sprint 10.4 history shape, summary, source validation, and copy safety.",
        "The public Sprint 10.4 operation may wrap this helper using a copy of current durable state."
      ]
    },
    "atomicity_contract": {
      "material_match_flow": [
        "Build the normal validated interaction result and exact resolved entity identity.",
        "Copy current world_state.",
        "Apply the conversation to the candidate, creating player_conversation first.",
        "Capture the engine-owned history_id of that source entry.",
        "Resolve exactly one matching Region Pack declaration.",
        "Prepare the exact pressure change in the same candidate.",
        "Add exactly one linked pressure_changed entry with source_history_id equal to the new conversation entry.",
        "Validate the completed candidate world state.",
        "Build the derived candidate scene required by the command path.",
        "Assign completed candidate world state exactly once.",
        "Replace scene_snapshot only after candidate preparation succeeds.",
        "Return a defensive interaction result containing bounded pressure_consequence metadata."
      ],
      "failure_property": "Any source-event construction, declaration resolution, pressure preparation, consequence-history construction, completed-state validation, or required candidate-scene construction failure on the matched path leaves durable history, pressures, time, player location, weather, and scene_snapshot unchanged.",
      "forbidden_infrastructure": [
        "transaction class",
        "transaction manager",
        "rollback framework",
        "generic event-effect engine",
        "event bus",
        "command bus",
        "scheduler",
        "dependency injection",
        "generic predicate language",
        "effect priorities",
        "effect ordering",
        "event replay"
      ]
    },
    "history_contract": {
      "material_order": [
        "player_conversation source entry",
        "pressure_changed consequence entry"
      ],
      "requirements": [
        "The source entry receives its normal engine-owned stable history_id.",
        "The consequence receives the next engine-owned stable history_id.",
        "The consequence source_history_id exactly references the source entry.",
        "The source entry remains unchanged after consequence preparation.",
        "Both entries use current durable time without advancing it.",
        "The conversation source keeps target_entity_id, target_display_name, location, time, summary, and event_type.",
        "The consequence preserves the established pressure_changed fields and deterministic summary.",
        "The consequence does not duplicate conversation data or add prose reasons.",
        "An unmatched successful conversation creates source history only.",
        "A matching no-op creates a new source history entry but no pressure_changed entry.",
        "Invalid and failed interactions create neither entry."
      ]
    },
    "no_op_contract": {
      "behavior": [
        "A matching conversation still occurred and its player_conversation source entry commits.",
        "The declaration and source_history_id are validated normally.",
        "No pressure_changed entry is created when the pressure is already at the declared level.",
        "No pressure level or other durable pressure field changes.",
        "pressure_consequence reports changed false, history_id null, and the new source_history_id."
      ]
    },
    "persistence_and_compatibility": {
      "requirements": [
        "Preserve save version 1.",
        "Add no new top-level world-state collection.",
        "Persist resulting pressure level and both history entries through the existing save path.",
        "Preserve source and consequence history IDs and source_history_id through load.",
        "Do not persist the immutable Region Pack declaration in the save.",
        "Do not replay effects during load.",
        "Do not retroactively apply declarations to old conversation history.",
        "After load, a new matching conversation follows the current Region Pack declaration.",
        "New post-load history IDs do not collide with existing IDs.",
        "Existing saves without the new seeded pressure continue through the established legacy pressure-normalization behavior unless repository validation proves a narrower compatibility adjustment is required."
      ]
    },
    "expected_files": {
      "likely_modified": [
        "engine/game_engine.py",
        "engine/world_update.py",
        "engine/region_validator.py",
        "data/regions/bryn_shander.json",
        "test_conversation_pressure_effect.py",
        "test_interaction_history.py",
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
      "possibly_modified": [
        "engine/pressure_state.py",
        "test_pressure_state.py",
        "test_region_validator.py",
        "engine/scene_loader.py"
      ],
      "not_expected_to_require_modification": [
        "engine/world_state.py",
        "engine/interaction_kernel.py",
        "engine/target_resolver.py",
        "engine/save_system.py",
        "engine/timekeeper.py",
        "engine/perception_builder.py",
        "engine/narration_context.py",
        "engine/narration_pipeline.py",
        "engine/narration_request.py",
        "engine/narration_prompt.py",
        "engine/narration_source.py",
        "engine/narration_output.py",
        "play_game.py"
      ]
    },
    "acceptance_criteria": [
      "Region Packs may contain the optional conversation_pressure_effects list with the exact declared item shape.",
      "Region validation accepts an absent field and a valid declaration list.",
      "Region validation rejects extra item fields, missing fields, invalid identifiers, duplicate effect_id values, multiple effects for one target_entity_id, unknown entity IDs, unknown pressure IDs, booleans, non-integer levels, and levels outside 0 through 100.",
      "The canonical Bryn Shander Region Pack contains the narrow bryn_shander_gate_scrutiny seeded pressure.",
      "The canonical Bryn Shander Region Pack contains exactly one north_gate_captain_scrutiny declaration targeting captain_darvin_grey and setting bryn_shander_gate_scrutiny to 25.",
      "A successful current-scene conversation with Captain Darvin Grey creates one player_conversation source entry followed by one linked pressure_changed consequence.",
      "The consequence source_history_id equals the new conversation history_id.",
      "The source entry remains exactly unchanged after consequence preparation.",
      "Only bryn_shander_gate_scrutiny changes from 10 to 25.",
      "The existing bryn_shander_winter pressure and every unrelated durable field remain unchanged.",
      "Both history entries use current durable time and conversation does not advance time.",
      "The interaction result contains copy-safe pressure_consequence metadata for a matched declaration.",
      "Mutating the returned interaction result cannot mutate world_state, history, pressure state, region data, or scene_snapshot.",
      "A successful resolved conversation with Elin Voss creates only the existing player_conversation entry and no pressure consequence.",
      "A repeated matching Captain conversation at level 25 creates a new player_conversation source entry but no pressure_changed entry.",
      "The repeated matching result reports changed false, history_id null, and the new source_history_id.",
      "Unresolved, ambiguous, unsuccessful, and non-entity conversation targets create neither source history nor consequence history.",
      "The material matched path uses one candidate world state and one final GameEngine.world_state assignment.",
      "Injected source-event, pressure-preparation, consequence-history, completed-state validation, and candidate-scene failures leave world_state and scene_snapshot unchanged.",
      "GameEngine.set_pressure_level_from_event retains its Sprint 10.4 already-durable-source contract and focused tests.",
      "GameEngine.set_pressure_level retains its Sprint 10.3 contract and focused tests.",
      "Save/load preserves the material source/consequence chain and exact resulting pressure level.",
      "Loading does not replay the declaration.",
      "A new post-load event receives a non-colliding history ID.",
      "Existing movement, waiting, target resolution, conversation memory, pressure state, history lookup, bounded history queries, history context, narration context, narration pipeline, and save/load behavior remain materially unchanged.",
      "No pressure state is projected into scenes, perception, narration, or AI behavior.",
      "No generic effect framework or additional gameplay command is added.",
      "Sprint 10.5 closes only after all required verification passes.",
      "Sprint 10.6 remains undefined and not started."
    ],
    "non_goals": [
      "Generic event-effect declarations",
      "Additional source event types",
      "Multiple automatic consequences from one event",
      "Multiple declarations for one conversation target",
      "Pressure deltas",
      "Conditional expressions",
      "Effect priorities or ordering",
      "Scripts, callbacks, or plugins",
      "Generic transactions",
      "Event buses",
      "Command buses",
      "Schedulers",
      "Autonomous simulation loops",
      "Time-based pressure escalation or decay",
      "Pressure applicability resolvers",
      "Pressure queries beyond existing generic pressure reads",
      "Pressure projection into scene construction",
      "Pressure projection into perception",
      "Pressure context for narration",
      "Scene lifecycle redesign",
      "Runtime pressure creation or deletion",
      "Actor knowledge or relationship mutation",
      "Evidence systems",
      "Persistent unresolved threads",
      "Opportunities",
      "Causal graphs",
      "Event replay",
      "AI-controlled world mutation",
      "New CLI commands",
      "Broad Region Pack schema redesign",
      "Packet-generation workflow repair",
      "Broad cleanup or unrelated refactoring",
      "Sprint 10.6 planning"
    ],
    "verification": {
      "environment_commands": [
        "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\validate_hardening_package.ps1 -PackageRoot .",
        "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\preflight.ps1 -RepoRoot ."
      ],
      "primary_commands": [
        ".\\.venv\\Scripts\\python.exe test_conversation_pressure_effect.py",
        ".\\.venv\\Scripts\\python.exe test_interaction_history.py",
        ".\\.venv\\Scripts\\python.exe test_pressure_state.py",
        ".\\.venv\\Scripts\\python.exe test_save_load.py",
        ".\\.venv\\Scripts\\python.exe test_interaction_kernel.py",
        ".\\.venv\\Scripts\\python.exe test_target_resolver.py",
        ".\\.venv\\Scripts\\python.exe test_world_update.py",
        ".\\.venv\\Scripts\\python.exe test_time_advance.py",
        ".\\.venv\\Scripts\\python.exe test_history_query.py",
        ".\\.venv\\Scripts\\python.exe test_history_context.py",
        ".\\.venv\\Scripts\\python.exe test_narration_context.py",
        ".\\.venv\\Scripts\\python.exe test_narration_pipeline.py",
        ".\\.venv\\Scripts\\python.exe engine/region_validator.py"
      ],
      "conditional_commands": [
        "Run an existing focused Region Pack validation test file if the repository contains one.",
        "Run any additional existing movement, scene, or perception test directly affected by the implementation."
      ],
      "manifest_commands": [
        ".\\.venv\\Scripts\\python.exe -m json.tool docs/current_sprint.json",
        ".\\.venv\\Scripts\\python.exe -c \"import json, yaml; from pathlib import Path; j=json.loads(Path('docs/current_sprint.json').read_text(encoding='utf-8')); y=yaml.safe_load(Path('docs/current_sprint.yaml').read_text(encoding='utf-8')); assert type(j) is type(y) and j == y\"",
        "git diff --check"
      ],
      "focused_test_shape": [
        "Validate valid, absent, malformed, duplicate, unknown-reference, extra-field, and invalid-level declarations.",
        "Exercise one Captain Darvin Grey material conversation consequence.",
        "Confirm source-first history ordering and exact causal reference.",
        "Confirm the source entry is unchanged.",
        "Confirm only the declared pressure changes.",
        "Exercise an Elin Voss unmatched source-only conversation.",
        "Exercise a repeated matching no-op conversation.",
        "Exercise unresolved, ambiguous, unsuccessful, and non-entity targets.",
        "Inject failures at every matched candidate-state preparation boundary.",
        "Exercise result copy safety.",
        "Save and load the material chain without replay, then create another event without ID reuse.",
        "Confirm the direct Sprint 10.3 and linked Sprint 10.4 pressure APIs remain unchanged.",
        "Confirm no time advancement, pressure projection, narration coupling, or new CLI behavior."
      ]
    },
    "execution_phases": [
      {
        "id": "setup",
        "goal": "Promote the four numbered Sprint 10.5 planning files, record the accepted post-Sprint 10.4 architecture decision narrowly in roadmap and sprint log, validate canonical manifests, and stop before implementation."
      },
      {
        "id": "implementation",
        "goal": "Perform Startup Review and implement only the one declared resolved-conversation pressure consequence."
      },
      {
        "id": "verification",
        "goal": "Run every documented required check through the official project environment and distinguish application failures from execution-context limitations."
      },
      {
        "id": "closeout",
        "goal": "Record actual implementation and verification, add ADR-039, synchronize documentation, and stop without defining Sprint 10.6."
      }
    ],
    "task_routing": [
      {
        "task_type": "Setup and staging",
        "recommended_model": "mini or lighter model with low reasoning"
      },
      {
        "task_type": "Bounded implementation",
        "recommended_model": "standard model with medium reasoning"
      },
      {
        "task_type": "Closeout documentation",
        "recommended_model": "mini or lighter model with low reasoning"
      },
      {
        "task_type": "Architecture conflict or unclear failure",
        "recommended_model": "high reasoning only when needed"
      }
    ],
    "governance": [
      "Exactly one sprint is defined at a time.",
      "Do not begin implementation during the staging pass.",
      "Do not substitute bundled, system, Windows Store, or alternate Python for official verification.",
      "Preserve provider neutrality, deterministic behavior, simulation-owned truth, and unrelated user changes.",
      "Use one explicit conversation-specific declaration rather than a generic effect framework.",
      "Do not define or begin Sprint 10.6."
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
