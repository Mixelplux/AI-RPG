# Sprint 10.80 - Scene Context V1

## Status
Complete and owner-accepted October 5, 2026 after the final live narrator smoke.
Routine risk. Branch: `codex/scene-context-v1`. Protected baseline:
`dad93cea3a6b38aa5cd6b9852f44340676be241f`.
Sprint 10.80 is complete; `next_sprint` remains null.

## Milestone
Implement and verify the smallest derived Scene Context proving slice within
the existing narration boundary. Scope, exclusions, authority and completion
are in `docs/current_capability_package.md`. No persistent state changes;
automated checks remain offline. The final live narrator smoke used the real
`gpt-6-luna` narrator with reasoning `low`; the owner accepted the result and
said “accepted, continue.” The smoke sequence was travel to Market Square, look,
and focused browsing. Progressive scene resolution, continuity, intent handling,
second-person narration and consequential-fact boundaries were accepted. Minor
storm-condition prose repetition is accepted narrative refinement.

Implementation and the owner-requested player-path correction passed focused
offline verification. The working-diff handoff is READY FOR OWNER RE-SMOKE;
see `docs/sprint_10_80_handoff.md` for the route correction and verification.
The known real tokenizer-cache limitation is unchanged; provider transport tests
use an offline tokenizer stub and fake transport. The latest correction and
verification evidence is recorded in the handoff. No further live call is needed.

The owner-smoke continuity/progression correction was implemented and staged.
Current-scene descriptive claims, previous conditions and
orient/expand/follow/narrow attention reach the existing validated prompt path.
Routine destination-hop messages are compressed in the CLI. Offline focused and
affected regressions passed; the owner then re-smoked and accepted the result.
The exact accepted scope and separation are recorded in the latest handoff section.

Finalization: one Sprint 10.80 commit is authorized. No push or merge is
authorized; `next_sprint` remains null. Save version 1 is preserved.
