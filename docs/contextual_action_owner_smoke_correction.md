# Contextual Action V1 — owner smoke correction

October 11, 2026. Elevated, focused correction in the existing isolated,
uncommitted candidate. The blocking owner sequence is now demonstrated through
the production CLI. No new package, action capability, persistence contract,
provider behavior or narration design was introduced. Owner acceptance remains
pending; this correction does not grant Git publication authority.

## Root causes and routing trace

1. GameEngine.process_command offers input to contextual handling before
   investigation and the legacy kernel. Handling selected material aliases, so
   the role word driver found the cart but the visible actor's name did not.
   The canonical resolver retained the display-name comma in its tokens, leaving
   the short name Tessa unmatched on the legacy talk route.
2. The handling interpreter selected cooperation from the word ask, without
   distinguishing a needs-help question from an actual offer/request.
3. The acknowledgment grammar omitted confirm and contextual continuations.
   These fell into ordinary intent classification or material target lookup.
4. A parsed equivalent handling request always reached proposal creation with
   authorized=False; it did not compare the method and target with the already
   disclosed pending frame. Rephrasing therefore repeated disclosure indefinitely.

## Correction

- actor_aliases derives whole personal names and established roles from authored
  actor metadata. Legacy resolution and contextual reference binding share it.
  Components are used to recognize references within sentences, without
  promoting generic role words to exact aliases. Full-name spans take precedence
  over contained first-name components; separate names remain ambiguous.
  Optional leading articles resolve consistently. No Tessa identifier or
  scenario-name branch was added to shared code.
- A needs-help inquiry is read-only and distinct from an offer/cooperation request
  and a physical handling objective. Query headings matter: a reason clause such
  as because Tessa needs help cannot turn an imperative shift into an inquiry.
  General talk keeps its legacy route. An identified actor must be the authored
  helper for the selected material target; body targets are not substituted by
  their possessions.
- Confirmation is a bounded semantic control. confirm, yes do it, the existing
  acknowledgment forms and context-qualified continuations identify one pending
  frame. An equivalent raw imperative can confirm the same target/operation/method.
  A different method requires a fresh disclosure. Structured frames remain
  proposals, not conversational authorization.
- Original and added restrictions are retained. Conflicting restrictions remain
  bound to the unsaved goal until it is explicitly canceled. No acknowledgment
  overrides them. Ordinary read-only questions do not create cooperation or spend
  time, and can retain relevant unsaved reference context.
- Immediately before execution, confirmation compares authoritative context,
  participant identity/location and the currently assessed disclosed method,
  risk and cost. Changed context/risk invalidates authorization. The existing
  execute -> copied candidate -> validate -> scene build -> publish-once path is
  reused. Pending context is preserved on injected transaction failure.
- Completion clears the pending proposal. Repeated confirmations cannot create
  another outcome, draw or cost.

An initial alias change promoted guard to an exact alias and broke an existing
ambiguity regression. That defect was directly corrected and the regression now
passes. No ambiguity was papered over with actor-specific branches.

## Evidence and tests

New evidence stays under:
.artifacts/contextual_action_owner_correction/

Before correction: before_owner_cli.txt and before_owner_trace.json reproduce
the exact failures, with zero material outcomes and zero draws.

After correction: corrected_owner_cli.txt and corrected_owner_trace.json capture
the production CLI/main using real engine construction and command execution.
The exact owner inputs now resolve both inquiries and the named talk target,
disclose help driver, execute confirm, and produce one full material outcome,
one draw and one hour. Continued confirmation/rephrasing does not charge again.

A separate real CLI process invokes the normal --scenario market entry point,
reads the exact commands from stdin and uses the actual d6 primitive with a fixed
offline random seed. production_cli_input.txt and production_cli_output.txt
contain that replay. It produces exactly one accepted result and one effort cost.
Network access is blocked; no live provider is used. No owner save is loaded or
written.

Final automated results:
- 14 owner-correction acceptance groups pass, including the exact CLI sequence,
  renamed/shared-first-name actors, role ambiguity, questions/offers/commitments,
  confirmation/rephrasing, retained constraints, stale/new-risk rejection,
  wrong helpers, structured-frame safety and injected publication failure.
- All 24 existing contextual action/consequence acceptance groups pass.
- 13 affected existing regression scripts pass: contextual investigation,
  North Gate discussion, interaction kernel/history, actor location,
  actor-knowledge response, conversation actor knowledge, current-scene projection,
  navigation projection, player scene route, Scene Construction, character
  competence and save/load.
- Changed Python sources parse; lifecycle validation and GitWorkflowTools
  mechanical verification pass. Diff/index checks pass.

The verifier supports a separate output directory under this worktree's
.artifacts and redirects historical investigation evidence and fixed test save
paths. The earlier verification directory and C:/tmp evidence are not rewritten.
The seven existing root save/load evidence files still predate correction start.
The brief initial verification interruption was to prevent reusing their fixed
paths; the save/load test passed after redirection.

Previously established baseline resolved-narration provider-fixture failures
are outside this correction and were not rerun or repaired. Do not interpret
focused passes as a claim that those baseline checks now pass. DF-008 remains
deferred.

## Correction file scope

Production: engine/contextual_action.py, engine/target_resolver.py.
Verification: test_contextual_action_owner_correction.py,
tools/verify_contextual_action.py.
Records: docs/current_capability_package.md, docs/current_sprint.md,
docs/current_sprint.json, docs/contextual_action_consequence_v1_handoff.md,
this correction report.

Material declarations, World State/save schemas, authoritative resolution,
default Region Packs and narration modules were not changed by this correction.

## Repository disposition and limits

Worktree: D:/AI RPG/.artifacts/contextual-action-consequence-v1.
Branch: codex/bounded-contextual-action-consequence-v1.
HEAD/protected main: 09d660af6da8b75f980ac2a32d664ba28d3ba8a0.
Delivery remains an uncommitted working diff with an empty index.
The original experimental checkout, owner saves/worktrees and prior evidence
remain preserved. No staging, commit, merge, push or publication.

Interpretation remains bounded: only the current authored needs-help exchange,
cooperation and handling methods are supported. Tentative/disjunctive controls,
unsupported conditions, missing referents or general NPC questions require
clarification or rejection. A role with several present actors remains ambiguous.
No subsequent consequential objective starts automatically.

Stop with this corrected candidate, awaiting owner acceptance. The exact failed
interaction sequence has been verified before making any renewed readiness claim.
