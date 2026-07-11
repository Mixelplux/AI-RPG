# Current Sprint

## Sprint 10.1 - Persistent Resolved Conversation Memory

Status: Complete

Phase: Phase 2B - Reactive World State Foundations

## Goal

Record a successful conversation initiation with a deterministically resolved current-scene actor as one durable, simulation-owned history event. The event must preserve the resolved actor identity, display name, current location, and current durable time through the existing history and save/load systems without creating dialogue content, actor knowledge, relationship changes, time advancement, or AI narration.

## Design Intent

The post-Sprint-9 playable vertical-slice review found that the engine can resolve a conversation target but does not remember that the interaction occurred. Sprint 10.1 closes that smallest player-facing gap and begins Phase 2B. It must reuse the existing Interaction Kernel -> GameEngine -> World Update -> World State path and the existing durable history system. The accepted fact is only that the player initiated a conversation with a resolved actor. The sprint must not infer what was said, what either participant learned, whether trust changed, or whether the actor agreed to anything.

The accepted fact is deliberately narrow:

> The player initiated a conversation with this resolved current-scene actor.

It does not establish what was said, learned, promised, believed, or changed.

## Expected ADR

Add **ADR-035: Resolved Conversations Become Durable Accepted Events** during closeout.

A conversation becomes durable history only after the existing gameplay path accepts the command and deterministic current-scene target resolution identifies an actor. The resulting history entry records only the occurrence and grounded target identity. Raw narration, invented dialogue, actor knowledge, relationships, dispositions, and consequences remain outside this event. Failed, unresolved, ambiguous, or non-actor conversation targets do not create history.

## Expected Files

Likely created:

- `test_interaction_history.py`

Likely modified:

- `engine/game_engine.py`
- `engine/world_update.py`
- `docs/architecture.md`
- `docs/decisions.md`
- `docs/roadmap.md`
- `docs/sprint_log.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`
- `docs/next_chat_handoff.md`

Possibly modified only if required by the existing target identity or regression path:

- `engine/target_resolver.py`
- `test_target_resolver.py`
- `play_game.py`
- `test_history_query.py`
- `test_history_context.py`
- `test_narration_context.py`
- `test_save_load.py`

## Acceptance Criteria

- The existing conversation command path remains Interaction Kernel -> GameEngine target resolution -> World Update -> World State.
- A successful conversation command creates history only when current-scene target resolution returns one resolved actor or entity target.
- The durable event type is player_conversation.
- Exactly one history entry is created for each accepted resolved conversation command.
- The history entry receives its history_id through the existing engine-owned history identifier mechanism.
- The history entry contains a deterministic summary stating that the player initiated a conversation with the resolved actor.
- The history entry records the current player location.
- The history entry records the current durable world time.
- The history entry records a stable target_entity_id copied from deterministic target resolution rather than inferred from raw player text.
- The history entry records the resolved target_display_name.
- If the current target-resolution result does not expose enough stable entity identity to meet this contract, it is extended narrowly without broadening target resolution beyond the current scene.
- The event records only that conversation was initiated; it does not record invented dialogue, topics, claims, promises, outcomes, knowledge changes, relationship changes, or emotional state.
- Failed conversation commands do not create history.
- Unresolved conversation targets do not create history.
- Ambiguous conversation targets do not create history.
- A resolved exit or other non-actor target does not create a conversation history entry.
- Repeated accepted conversations create separate history entries with distinct stable history_id values.
- Recording a conversation does not advance time.
- Recording a conversation does not move the player.
- Recording a conversation does not change weather, actor state, knowledge, relationships, schedules, pressures, evidence, consequences, or other world state.
- The new history entry is returned through existing history queries, including event_type filtering.
- The new history entry appears naturally in existing bounded history context and narration context when it falls within the selected history window.
- Conversation history survives save/load without regenerating or altering its history_id.
- New history created after loading does not reuse an existing history_id.
- No new top-level world_state field is introduced.
- The existing save version remains unchanged and existing saves without conversation events remain valid.
- Existing movement history and wait-created time history remain materially unchanged.
- Existing destination resolution, skill checks, narration context, narration preview, and normal deterministic scene narration remain materially unchanged.
- No new player-facing command is required.
- The existing history command can display the conversation event through its event type and deterministic summary.
- No AI model, provider, SDK, external service, or network call is added.
- Documentation records the playable vertical-slice review result, Phase 2B transition, the bounded conversation-memory rule, and ADR-035.
- Sprint 10.1 is marked complete only after all documented verification passes.
- No Sprint 10.2 work is defined or started during implementation or closeout.

## Verification

Primary automated checks:

```powershell
.\.venv\Scripts\python.exe test_interaction_history.py
.\.venv\Scripts\python.exe test_history_query.py
.\.venv\Scripts\python.exe test_history_context.py
.\.venv\Scripts\python.exe test_narration_context.py
.\.venv\Scripts\python.exe test_save_load.py
.\.venv\Scripts\python.exe test_narration_pipeline.py
```

Launch check:

```powershell
.\.venv\Scripts\python.exe play_game.py
```

Manifest checks:

```powershell
.\.venv\Scripts\python.exe -m json.tool docs/current_sprint.json
.\.venv\Scripts\python.exe -c "import json, yaml; from pathlib import Path; j=json.loads(Path('docs/current_sprint.json').read_text(encoding='utf-8')); y=yaml.safe_load(Path('docs/current_sprint.yaml').read_text(encoding='utf-8')); assert j == y"
```

Manual or scripted checks:

1. Start a new game at the Bryn Shander North Gate.
2. Use talk to captain and confirm the conversation target resolves to Captain Darvin Grey.
3. Confirm the accepted command creates exactly one player_conversation history entry.
4. Confirm the entry includes a stable history_id, target_entity_id, target_display_name, current location, and current durable time.
5. Confirm history and history type player_conversation display the new event.
6. Confirm history context includes the event when it falls within the bounded window.
7. Confirm narration context includes the event only through its bounded history context.
8. Repeat the accepted conversation and confirm a second entry with a distinct history_id.
9. Attempt an unresolved or ambiguous conversation and confirm no history entry is created.
10. Confirm conversation does not advance time, move the player, or alter unrelated world state.
11. Save, load, and confirm conversation history and identifiers are preserved.
12. After loading, create another accepted conversation and confirm its history_id is not reused.
13. Confirm movement, wait, destination resolution, skill checks, narration preview, save/load, reset, and quit still work.
14. Run a scripted play_game.main() smoke flow through talk to captain, history, save/load where practical, and quit.

## Non-Goals

- Do not generate or persist dialogue content.
- Do not add dialogue trees, topics, conversation sessions, or turn-taking.
- Do not add AI narration or provider integration.
- Do not update actor knowledge, beliefs, memories, relationships, trust, hostility, disposition, or emotional state.
- Do not add mutable runtime actor state.
- Do not add evidence, consequences, rumors, opportunities, quests, or world pressures.
- Do not add pressure representation, pressure change, or time-based pressure drift.
- Do not advance time for conversation.
- Do not add schedules, autonomous NPC behavior, travel execution, inventory, conditions, combat, or character progression.
- Do not add a generic event bus, command bus, plugin framework, handler registry, or broad interaction framework.
- Do not change narration request, prompt, source-result, output, or pipeline contracts unless a regression defect is discovered and reported.
- Do not change the save version or add a general migration framework.
- Do not persist raw player input as canonical dialogue.
- Do not refactor unrelated systems.
- Do not define or begin Sprint 10.2.

## Closeout State

Sprint 10.1 is complete and closed out.

### Closeout Summary

- Files created: `test_interaction_history.py`
- Files modified: `engine/world_update.py`
- Verification: `test_interaction_history.py`, `test_history_query.py`, `test_history_context.py`, `test_narration_context.py`, `test_save_load.py`, `test_narration_pipeline.py`, `-m json.tool docs/current_sprint.json`
- Parsed JSON/YAML deep comparison: passed
- Scripted smoke flow: passed
- Launch check: rendered the opening scene and then reached the expected non-interactive `EOFError`
- Bundled Python: not used
- Sprint 10.2: not started

## Codex Task Routing

### Run 1 - Setup / Staging and Review-Record Maintenance

Recommended: **mini or lighter model with low reasoning**

Promote the four Sprint 10.1 numbered planning files into the canonical documentation paths. Confirm the Markdown, YAML, and JSON sprint definitions materially agree. Parse the canonical JSON and YAML with the official project runtime and confirm exact deep agreement on keys, nesting, data types, ordered lists, values, and complete structure. Validate docs/current_sprint.json. Update docs/roadmap.md to mark the playable vertical-slice review complete, record persistent resolved conversation memory as the first Phase 2B capability, and place persistent pressures next. Add a concise playable vertical-slice review decision entry to docs/sprint_log.md. Confirm all canonical files exist, delete only the temporary Sprint 10.1 staging files after successful promotion and validation, then stop. Do not modify application code or begin implementation.

### Run 2 - Bounded Sprint Implementation

Recommended: **standard Codex with medium reasoning**

Perform Startup Review and implement only Sprint 10.1. Reuse the existing conversation routing, target resolution, world-update, history, and save/load paths. Add focused tests and run every documented official .venv verification command. Report results, then stop. Do not perform closeout and do not begin pressure work or Sprint 10.2.

### Run 3 - Closeout Documentation

Recommended: **mini or lighter model with low reasoning**

After implementation verification passes, update architecture documentation, add ADR-035, update the roadmap and sprint log with the actual implementation, record actual files and verification results, mark all canonical Sprint 10.1 manifests complete, update the compact handoff, validate JSON, deep-compare parsed YAML and JSON, confirm Sprint 10.2 has not started, then stop. Do not add features.

### Run 4 - Debugging If Needed

Recommended: **high reasoning only after a focused medium-reasoning pass fails**

Use only for unclear failures involving actor-versus-exit target identity, duplicate or missing conversation history, history identifier reuse, save/load preservation, or unintended state/time mutation. Keep investigation within Sprint 10.1 scope.
