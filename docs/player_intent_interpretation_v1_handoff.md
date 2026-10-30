# Player Intent Interpretation V1 — implementation handoff

October 30, 2026. **Implementation candidate ready for owner review; not accepted
or published.** Baseline and current HEAD:
`870d1080e67c2f943d12a7bd74952d26ed56b5d2`.
Branch: `codex/player-intent-interpretation-v1`.
Worktree: `D:/AI RPG/.artifacts/player-intent-interpretation-v1`.
The candidate is an **uncommitted working diff**, with empty index. The original
dirty checkout, owner saves, prior experiments and external research artifacts
remain preserved. No Git staging, commit, push, merge or further package is
authorized. Lifecycle remains active pending owner acceptance; `next_sprint` is null.

## Exact changed-file inventory

| File | Change |
|---|---|
| `engine/player_intent.py` | New V1 contract, immutable canonical form, strict bounded normalization, provider request and handoff records. |
| `engine/gameplay_coordination.py` | Explicit provider/binder handoff; commitment and boundary preservation; context checks; existing progression reused. |
| `engine/game_engine.py` | Explicit `process_player_intent` entry, no fallback or implicit production provider. |
| `test_player_intent.py` | New contract, meaning-preservation fixtures and Coordinator/GameEngine containment tests. |
| `test_player_intent_integration.py` | New production Watchhouse/common acceptance and independent-owner integration checks. |
| `docs/design/player-intent-interpretation-v1.md` | Accepted handoff semantics, exact wire choices, integration obligations and research limits. |
| `docs/design/README.md` | Design record index. |
| `docs/architecture.md` | Runtime seam and retained authority, candidate status. |
| `docs/design/systems/player-presentation.md` | Input, clarification and operational failure behavior, bounded status. |
| `docs/design/systems/system-map.md` | Interpretation → Coordinator → installed owner relationships. |
| `docs/current_capability_package.md` | Stage only the authorized interpretation package and boundaries. |
| `docs/current_sprint.json` | Sole machine lifecycle: active interpretation milestone, Elevated, provider calls forbidden. |
| `docs/current_sprint.md` | Scope, implementation readiness and acceptance boundary. |
| `docs/player_intent_interpretation_v1_handoff.md` | This report, inventory, evidence, limitations and recommendation. |

Ignored local setup/evidence is under the worktree's `.artifacts/`; `.venv` is a
junction to the original official environment, not a recreated interpreter.
The shared GitWorkflowTools profile is unchanged. Its ignored worktree-bound
copy changes only repository path and the required expected-root argument.

## Contract and integration

The [contract](design/player-intent-interpretation-v1.md) records all field types,
nullability, canonical serialization, bounds and structural rejection rules.
Unknown/executable/outcome keys, inconsistent commitments, invalid relationships,
duplicate IDs/keys, fabricated context references, malformed or oversized output
are rejected. Model text remains non-authoritative even when structurally valid.
Optional omissions never add restrictions. Source excerpts, natural-language
methods, constraints, conditions, stops and context references remain distinct.

A replaceable provider receives exact player input and only trusted accessible
context. The existing Coordinator receives validated meaning, original input and
trusted situated context, then an installed read-only owning capability binder
maps supported meaning to existing internal target/method IDs. Unsupported or
ambiguous meaning returns control. No keyword replacement, second general
interpreter, production model selection or provider SDK dependency is introduced.

The Coordinator derives commitment itself from validated V1, preventing an owner
binder from promoting inquiry/preparation assessment to execution. All expressed
restrictions carry forward; conditions require owner-established satisfaction,
and stops require owner support. Fresh context, availability, F05, single-use
permission, domain reassessment and common acceptance remain authoritative.
Domain hints confer no routing or adjudication authority. No model-generated
outcome, cost, permission or dependency list is accepted as truth.

Multiple intentions, including related ones, return clarification before binding;
none are selected, executed or queued. Single coherent undertakings retain
existing ordinary situated progression. Invalid/technical rejection invalidates
old pending permission without changing fictional time/resources/campaign state.
Earlier accepted results survive failures; retries use existing accepted-step
and Runtime receipt recognition. Persistence records/codecs are unchanged.

## Verification

All commands use PowerShell 7.6.5 and `.\.venv\Scripts\python.exe` from this
exact worktree. No inference, live provider, model evaluation or owner-save access.

- **Passed:** syntax compilation of all three changed runtime Python files and
  both new test scripts before behavioral execution.
- **Passed:** 179 tests with `python -m unittest test_player_intent
  test_player_intent_integration test_activity_control test_gameplay_coordination
  test_domain_acceptance test_cross_domain_coupling test_watchhouse` (using the
  official executable above). Includes **36 new tests** and 143 established
  boundary regressions. Tests block outbound socket connections.
- **Passed:** 157 additional tests with `python -m unittest
  test_activity_continuity test_campaign_continuity test_player_activity
  test_save_load test_consequential_climbing`. Legacy `test_save_load.py` is a
  standalone main rather than a unittest case and is executed separately below.
- **Passed:** standalone `test_save_load.py`, including historical compatibility,
  invalid/corrupt restore rejection and direct ignored artifact files.
- **Passed:** 21 preflight checks; 8 current-record checks; 29 PowerShell workflow
  checks, including all 16 lifecycle fixtures in three whitespace layouts.
  The sandbox initially prevented the expected legacy-shell version diagnostic
  with `AuthorizationManager`; the authorized normal Windows context passed.
  No tooling, ACL or shared configuration was modified.
- **Passed:** maintained `Invoke-GitWorkflowVerification.ps1` with the
  worktree-bound profile; all mandatory commands passed, repository state unchanged.
- **Passed:** `git diff --check`, documentation link/scope review and empty-index
  verification. No formal evidence packet is required for this uncommitted handoff.
- **Not run:** repository-wide behavioral runner, live-model/CLI language smoke,
  new inference experiments. Verification is focused on this Elevated boundary
  and affected compatibility/continuity systems; language qualification is excluded.

New integration checks reuse actual Watchhouse skill/NPC adjudication and the
production Runtime, acceptance, disk and restoration paths. A mechanically
independent existing fixture exercises World time/Character expenditure through
the same boundary. It is contract evidence, not a new game mechanic. Rejection
checks compare exact campaign/root identity and encoding, with no dice consumed;
valid failed social attempts consume domain-owned time and one d20 as expected.
Candidate labels cannot turn failure into permission. A required player promise
still returns F05 control. Save/load exact retries preserve receipts without draws.

## Documentation reconciliation and ownership review

Updated runtime architecture, the Player Presentation manifest, system map,
Design index, exact contract and package/lifecycle records match the submitted
behavior without claiming owner acceptance or a qualified model.

No change needed to other owner manifests: no World, Character, Actor,
Resolution or Narrative mechanics/authority changed. Persistence/save documents
remain correct because no persisted type, schema, codec or migration changed;
conditions/stop support are transient Coordinator data and unsupported at existing
persisted-domain adapters. Governing F05/IG/Information/CD decisions and shared
doctrines require no revision. No material durable architecture decision or new
deferred capability was selected, so no ADR or deferred register update is needed.
Historical handoffs and research evidence remain unchanged.

Targeted review confirms that untrusted output can reach only validation and the
installed trusted capability binder, not a domain command/acceptance API directly.
Context is checked after inference/binding and again before execution. Existing
acceptance owns coherent publication, historical reconstruction and retry identity.
Only the owning domain may establish condition satisfaction and stop support.
Such support must enforce the actual boundary and retain meaningful authorization
through its existing durable scope when needed; this package adds no general
condition evaluator or persistence support for arbitrary natural-language guards.

## Deviations, reliability risks and recommendation

No significant design conflict was found. Exact field shapes, bounds, canonical
JSON, source excerpts and conservative multi-intention clarification are the
implementation choices permitted by the handoff. Multiple ordinary steps within
one authorized undertaking still use existing F05 progression.

This is an explicit integration seam: **no general language binder or production
provider is installed for the CLI**. Trusted production binders must map supported
meaning without choosing consequential methods, trusting domain labels or
discarding boundaries. Unsupported binding/condition/stop support fails closed.
Model transport adapters must supply bounded completion and timeout/cancellation.

Structural validation cannot detect all semantic misreadings, omitted conditions,
invented restrictions, collapsed intentions, wrong targets or authority assertions
embedded in descriptive prose. The binder remains a trusted semantic boundary;
tests use controlled interpretations, not a model-accuracy estimate. Stage A P10
and P03/P07, and Stage B E03/E04 informed regression themes; no experiments were
rerun. Correct model understanding, broader wording, latency and production
reliability remain unqualified. Models may fail semantically while passing schema.

**Recommendation:** ready for owner acceptance review of the bounded V1 contract,
validation and Coordinator interface. Review the exact serialization and binder
obligations and the offline acceptance/recovery examples. Acceptance should not
be represented as model qualification or general natural-language gameplay.
Publication and any further capability or model evaluation remain separate owner
decisions; stop here with the uncommitted candidate.
