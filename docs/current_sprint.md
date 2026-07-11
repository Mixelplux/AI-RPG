# Current Sprint

## Sprint 9.13 - Strict Narration Source Result Validation Contract

Status: Complete

## Goal

Add a deterministic, exact, copy-safe validation and sanitization boundary for untrusted narration source-result packets after source invocation and before candidate extraction, narration-output validation, or preview exposure. The pipeline must accept only the documented fixed-source result shape, verify that it corresponds to the validated narration prompt, and fail closed without copying raw invalid source output into preview packets or display text.

## Design Intent

Sprint 9.12 completed the deterministic pre-source path from bounded narration context through validated request and prompt packets. The remaining narrow gap is the return envelope from the untrusted candidate source. The current pipeline checks selected source-result fields while extracting the candidate, but it has no dedicated strict source-result validator and may retain raw malformed source-result content in preview inspection data. Sprint 9.13 closes that existing boundary before any provider integration. The fixed source remains deterministic and continues returning only 'The street remains quiet.' The pipeline must validate the complete source-result packet against the originating validated prompt, expose only a validated copy, then separately validate the candidate through the existing narration-output contract. This sprint hardens the present preview path only; it does not add generation, a provider, semantic prose analysis, or simulation authority.

The governing rules remain:

> The narrator can describe. The engine decides what is true.

> Narration candidate sources and their return envelopes are untrusted.

> Raw invalid source output must not cross into preview inspection data or display text.

The intended preview sequence is:

1. Build bounded narration context.
2. Build and validate the narration request packet.
3. Build and validate the narration prompt packet.
4. Invoke the deterministic fixed candidate source.
5. Validate the complete source-result packet against the originating validated prompt.
6. Extract the candidate only from the validated source result.
7. Validate the candidate through the narration-output contract.
8. Expose display text only after successful validation.

## Expected ADR

Add **ADR-033: Narration Source Results Are Untrusted Until Strictly Validated** during closeout.

Every narration source-result envelope is untrusted. After source invocation, the pipeline must validate the exact supported source-result schema, version, source identity, echoed prompt, candidate object, and bounded metadata before candidate extraction or preview exposure. The echoed prompt must match the originating validated prompt. Unsupported, malformed, or mismatched source results fail closed with empty display text, bounded diagnostics, and no copied raw source payload. A validated source-result envelope does not validate the candidate prose; the candidate must still pass independently through the narration-output contract.

## Expected Files

Likely created:

- None.

Likely modified:

- `engine/narration_source.py`
- `engine/narration_pipeline.py`
- `test_narration_source.py`
- `test_narration_pipeline.py`
- `docs/architecture.md`
- `docs/decisions.md`
- `docs/sprint_log.md`
- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`
- `docs/next_chat_handoff.md`

Possibly modified only if required by the existing facade or CLI:

- `engine/game_engine.py`
- `play_game.py`

## Acceptance Criteria

- A dedicated narration source-result validation function exists in the narration-source boundary.
- The existing source-result schema remains ai_rpg.narration_source_result.
- The existing source-result version remains 1.
- The validator accepts only an object with the exact supported top-level fields: schema, version, source, source_prompt, candidate, and metadata.
- Missing required source-result fields are rejected deterministically.
- Unsupported extra source-result fields are rejected deterministically.
- The source-result schema, version, and source identity must match the supported fixed source.
- The source_prompt field must be an object accepted by the existing narration-prompt validator.
- The validated source_prompt must equal the originating validated prompt supplied to the source.
- A substituted, stale, mutated, or otherwise mismatched source_prompt is rejected.
- The metadata field must be an object with the exact supported metadata keys.
- Metadata must preserve candidate_trust as untrusted.
- Metadata must preserve generation as fixed_sample_only.
- Missing, extra, or altered metadata is rejected.
- The candidate field must be an object before it can be extracted.
- Source-result validation does not treat the candidate as trusted narration output.
- The candidate still passes independently through validate_narration_output_packet(...) before display.
- The source-result validator returns a deep copy and exposes no live mutable reference from its input.
- Equivalent valid source results produce equivalent validated source-result packets.
- Source-result validation does not mutate the supplied source result or originating prompt.
- The narration pipeline validates the complete source result immediately after source invocation.
- Candidate extraction occurs only from the validated source-result packet.
- An accepted preview packet exposes only a validated, copy-safe source-result packet.
- A source-result validation failure returns an unsuccessful preview packet with empty display text.
- Source-result validation failure uses a distinct bounded failure stage such as source_result_validation.
- A failed source-result validation does not copy the raw source result into preview inspection fields.
- A failed source-result validation does not copy a raw candidate into preview inspection fields.
- Failure diagnostics remain bounded and do not include raw unvalidated narration prose or arbitrary source payload content.
- Candidate-output validation failure remains distinct from source-result validation failure.
- The fixed narration source remains deterministic.
- The fixed narration source continues returning only The street remains quiet.
- The fixed source continues receiving only a validated copy-safe narration prompt packet.
- Existing narration context, request, prompt, and output contracts remain materially compatible.
- GameEngine.get_narration_preview(...) remains the gameplay-facing preview entry point.
- Existing CLI syntax narration preview <player input> remains supported.
- No new player-facing source-result command is added.
- Normal gameplay output is not replaced or altered.
- Source-result validation and narration preview do not mutate world state.
- Source-result validation and narration preview do not advance time.
- Source-result validation and narration preview do not create history or alter history identifiers.
- Narration prompts, source results, candidates, validated output, and preview text are not persisted.
- No AI model, external service, provider SDK, or network call is used.
- Documentation describes strict validation and sanitization of untrusted source-result envelopes.
- ADR-033 is added during closeout.
- Sprint 9.13 is marked complete only after all documented verification passes.
- No following sprint is defined or started.

## Verification

Primary automated checks:

```powershell
.\.venv\Scripts\python.exe test_narration_source.py
.\.venv\Scripts\python.exe test_narration_pipeline.py
.\.venv\Scripts\python.exe test_narration_prompt.py
.\.venv\Scripts\python.exe test_narration_request.py
.\.venv\Scripts\python.exe test_narration_output.py
.\.venv\Scripts\python.exe test_narration_context.py
.\.venv\Scripts\python.exe test_history_context.py
.\.venv\Scripts\python.exe test_history_query.py
.\.venv\Scripts\python.exe test_save_load.py
```

Launch check:

```powershell
.\.venv\Scripts\python.exe play_game.py
```

Manifest and regression checks:

```powershell
.\.venv\Scripts\python.exe -m json.tool docs/current_sprint.json
.\.venv\Scripts\python.exe -c "import json, yaml; from pathlib import Path; j=json.loads(Path('docs/current_sprint.json').read_text(encoding='utf-8')); y=yaml.safe_load(Path('docs/current_sprint.yaml').read_text(encoding='utf-8')); assert j == y"
```

Manual or scripted checks:

1. Confirm narration context <player input> still works.
2. Confirm narration output still works.
3. Confirm narration preview <player input> still displays the validated fixed sample.
4. Repeat the same preview and confirm deterministic output.
5. Confirm a valid source result is accepted only after complete source-result validation.
6. Confirm an unexpected top-level source-result field fails closed.
7. Confirm missing or wrong source-result schema, version, or source identity fails closed.
8. Confirm a malformed or mismatched source_prompt fails closed.
9. Confirm missing, extra, or altered source metadata fails closed.
10. Confirm a non-object candidate fails at source-result validation.
11. Confirm invalid candidate output still fails separately at candidate validation.
12. Confirm raw invalid source-result fields and raw candidate prose are absent from failure inspection fields and display text.
13. Confirm accepted preview inspection data contains only a validated copy-safe source result.
14. Confirm preview does not alter time, history, scene state, history identifiers, or saved state.
15. Confirm normal gameplay output remains unchanged.
16. Run the established scripted play_game.main() smoke flow through narration preview and quit.

## Actual Files

Created:

- None

Modified:

- `engine/narration_source.py`
- `engine/narration_pipeline.py`
- `test_narration_source.py`
- `test_narration_pipeline.py`

## Verification Results

- `test_narration_source.py`: passed
- `test_narration_pipeline.py`: passed
- `test_narration_prompt.py`: passed
- `test_narration_request.py`: passed
- `test_narration_output.py`: passed
- `test_narration_context.py`: passed
- `test_history_context.py`: passed
- `test_history_query.py`: passed
- `test_save_load.py`: passed
- `-m json.tool docs/current_sprint.json`: passed
- Parsed YAML/JSON deep comparison: passed
- Scripted `play_game.main()` smoke through `narration preview look around` and `quit`: passed
- `play_game.py`: rendered the opening scene and then hit expected `EOFError` in the non-interactive session

Sprint 9.13 is complete and closed out. No following sprint has been started.

## Non-Goals

- Do not call an AI model.
- Do not add an external API, SDK, or network dependency.
- Do not add provider implementations, provider selection, a provider registry, or a plugin framework.
- Do not add provider-specific request or response payloads.
- Do not add API keys, secrets, environment-variable loading, model configuration, or provider configuration.
- Do not add prompt rendering for a specific provider.
- Do not add model names, temperature, top-p, seed, token settings, token budgets, context-window management, or cost tracking.
- Do not add retries, timeouts, streaming, asynchronous execution, fallback providers, or caching.
- Do not generate prose from narration context, request data, or prompt data.
- Do not change the fixed sample prose.
- Do not replace normal gameplay narration.
- Do not persist narration artifacts.
- Do not treat a validated source envelope, source metadata, candidate prose, or preview text as world truth.
- Do not add semantic hallucination detection, lore verification, embeddings, relevance scoring, or prose fact extraction.
- Do not broaden narration context or pass full durable history to the prompt or source.
- Do not add a new player-facing source-result inspection command.
- Do not implement world evolution, pressures, rumors, actor knowledge, schedules, evidence, consequences, opportunities, quests, combat, inventory, conditions, or travel execution.
- Do not add or repair dependency-management files or development-environment documentation unless an implementation blocker is discovered and reported first.
- Do not refactor unrelated systems.
- Do not define or begin a following sprint.

## Closeout Requirement

Closeout has been completed for Sprint 9.13. The canonical current-sprint manifests record the sprint as complete, the actual files and verification results are recorded, and no following sprint has been defined or started.

## Closeout State

Sprint 9.13 is complete and closed out.

## Codex Task Routing

### Run 1 - Setup / Staging

Recommended: **mini or lighter model with low reasoning**

Promote the four Sprint 9.13 numbered staging files into the canonical docs paths. Confirm the Markdown, YAML, and JSON sprint definitions materially agree. Parse the canonical JSON and YAML with the official project runtime and confirm exact deep agreement on keys, nesting, data types, ordered lists, values, and complete structure. Validate docs/current_sprint.json, confirm all four canonical files exist, delete only the temporary Sprint 9.13 staging files after successful promotion and validation, then stop. Do not modify application code or tests and do not begin implementation.

### Run 2 - Bounded Sprint Implementation

Recommended: **standard Codex with medium reasoning**

Perform Startup Review, implement only Sprint 9.13, update the focused source and pipeline tests, run every documented official .venv verification command, report results, then stop. Do not perform closeout and do not begin another sprint.

### Run 3 - Closeout Documentation

Recommended: **mini or lighter model with low reasoning**

Only after implementation verification passes, update architecture documentation, add ADR-033, update the sprint log, record actual files and verification results, mark all canonical Sprint 9.13 manifests complete, update the compact handoff, validate JSON, deep-compare parsed YAML and JSON, confirm no following sprint has started, then stop. Do not add features.

### Run 4 - Debugging If Needed

Recommended: **high reasoning only after a focused medium-reasoning pass fails**

Use only for an unclear verification failure involving source-result exact-shape validation, prompt correspondence, raw-payload sanitization, candidate-stage separation, copy safety, or state isolation. Keep investigation within Sprint 9.13 scope.
