# Sprint 10.78 - Character Competence V1

## Status
Complete and owner-accepted October 4, 2026. Sprint 10.78 is frozen on
`codex/character-competence-v1`; baseline: `d9c0cb9056007b938902dc4f1a439130763179b2`.
No next package is selected; `next_sprint` remains null.

## Scope
Authoritative player competences: tactical_assessment, outdoor_tracking, surveillance_analysis.
One bounded West-Road authority projects and executes follow withdrawal signs (1 hour,
uncertain), reconstruct local observation circuit (1 hour, uncertain), and arrange guarded
local survey (2 hours; tactical competence reduces to 1). Existing guard assistance is a
prerequisite, never competence. Preserve ordinary pursuit and all initial/follow-up paths.
An engine-owned d6 yields failure/partial/full at 1-2/3-4/5-6 without competence;
with competence, 1-2 partial and 3-6 full. Routine recognition is deterministic.
Persist accepted attempts, draw, result, costs, findings and causal references; no reroll
or repeat cost. Use copied candidate transactions and existing discoveries.

## Persistence
Retain save version 1 using established additive copied-load normalization. Missing new
fields normalize empty; malformed present fields reject. Preserve prototype rejection,
source saves, active session on failure, and historical completed pursuit.

## Exclusions
No classes, attributes, biography parsing, leveling, inventory, broad skills/modifiers,
generic checks/investigations/migrations, new locations, quests, combat, provider calls,
or automatic next package. No unsupported identity, affiliation or destination claims.

## Verification and completion
Injected deterministic draws; profiles, evidence, eligibility/projection agreement,
full/partial/failure, idempotence, alternate approaches, guard prerequisites, time,
rollback, save/load and malformed states; affected discovery/action/scene/perception/
narration and existing West-Road regressions. Filesystem tests use `.artifacts/`.
Focused verification and owner smoke passed; owner accepted Character Competence V1
on October 4, 2026. Real tokenizer-backed narration token counting remains unverified
because the tokenizer cache was unavailable; the offline narration contract passed,
the provider adapter is unchanged, and the limitation is non-blocking.

## Implementation handoff
See `docs/sprint_10_78_handoff.md` for repository reconciliation, semantics,
verification, and the accepted tokenizer limitation.
