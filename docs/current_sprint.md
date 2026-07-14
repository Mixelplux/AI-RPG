# Sprint 10.56 - One Derived Discovery-Gated Conversation Affordance

Status: Complete - ready for owner review.

## Goal

Surface one existing Elin Voss discovery-gated conversation as a pure,
repeatable, player-safe affordance while preserving the existing `talk` command
as the sole authority.

## Expected Files

- Region Pack, strict validator, pure affordance derivation, perception
  projection, focused tests, canonical package records, ADR, and one
  package-review archive.

## Acceptance Criteria

- One exact singleton declaration binds the West Gate, static Guard Elin Voss,
  and the existing West-Road Orders discovery to exact authored display text.
- Perception projects only `affordance_id`, `display_text`, `command_text`, and
  `target_display_name` when location, visible targetable actor, and owned
  discovery all match.
- Projection remains repeatable and nonauthoritative with no opportunity state,
  history, acknowledgement, command or parser behavior, persistence, or schema change.
- Existing `talk to Elin` independently applies normal targeting, presence, and
  discovery-gated conversation checks. Save version remains 1.

## Verification

- Focused and full official-interpreter tests, Region Pack validation,
  canonical-record agreement, preflight, diff check, and independent
  package-review archive validation passed.

## Canonical Manifest

<!-- CANONICAL-MANIFEST-START -->
```json
{"schema_version":"1.0.0","document_type":"current_sprint","sprint_count":1,"project":{"name":"AI Narrative RPG Engine","principles":["provider-neutral","deterministic-core","simulation-owned-truth"]},"sprint":{"id":"10.56","title":"One Derived Discovery-Gated Conversation Affordance","type":"capability-package","mode":"capability-package","status":"complete","goal":"Surface one existing Elin Voss discovery-gated conversation as a pure, repeatable, player-safe affordance while preserving the existing talk command as the sole authority.","platform":{"official_interpreter":".\\.venv\\Scripts\\python.exe"},"expected_files":{"likely_modified":["data/regions/bryn_shander.json","engine/perception_builder.py","engine/game_engine.py","engine/region_validator.py","docs/architecture.md","docs/roadmap.md","docs/decisions.md","docs/current_capability_package.md","docs/current_sprint.md","docs/current_sprint.yaml","docs/current_sprint.json","docs/sprint_log.md"],"likely_created":["engine/conversation_affordance.py","test_discovery_gated_conversation_affordance.py","handoffs/discovery-gated-conversation-affordance-<short-head>.zip"]},"acceptance_criteria":["One optional strict singleton Region Pack declaration binds the West Gate, static Guard Elin Voss, and the existing West-Road Orders discovery to one authored display text and no unsupported fields.","Perception derives exactly one record containing affordance_id, display_text, command_text, and target_display_name only when the player is at the declared location, the named static actor is visible and targetable, and the player owns the exact discovery.","Eligible projection may repeat without state, history, acknowledgement, command, parser, persistence, or save-schema changes; existing talk independently revalidates normal conversation eligibility.","Save version remains 1; no multiple affordances, ordering, priority, conditions, action types, lifecycle, consumption, hidden-state eligibility, or following package is staged."],"verification":{"focused_commands":[".\\.venv\\Scripts\\python.exe test_discovery_gated_conversation_affordance.py","Affected perception, narration, conversation, discovery, relocation, Region Pack, and save/load regressions"],"required_regressions":["Complete root test inventory through the official interpreter","Region Pack validation"],"manifest_commands":["JSON/YAML/Markdown deep agreement","git diff --check"],"closeout_commands":["Official preflight","Independent package-review archive validation"]},"execution_phases":[{"id":"contract-and-staging","status":"complete"},{"id":"affordance-projection","status":"complete"},{"id":"verification-and-closeout","status":"complete"}],"governance":["Owner-authorized package: One Derived Discovery-Gated Conversation Affordance.","Excluded: durable opportunities, opportunity history or causal references, acknowledged or once-only display state, commands or parser changes, generic affordance framework, multiple declarations, ordering, priority, scoring, action types, condition language, lifecycle, consumption, hidden-state eligibility, World State additions, save migration, and any following package.","The exact supported fixture is the Elin Voss conversation gated by west_gate_elin_report_trace at the West Gate."],"closeout":{"allowed_terminal_statuses":["complete"],"verification_result":"Focused and full official-interpreter verification passed; Region Pack validation and independent package-review archive validation completed for the committed review candidate.","next_sprint":null}}}
```
<!-- CANONICAL-MANIFEST-END -->
