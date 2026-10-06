# Sprint 10.80 - Scene Context V1

## Status and authority
Owner-accepted and complete October 5, 2026. Protected baseline:
`dad93cea3a6b38aa5cd6b9852f44340676be241f`. Branch:
`codex/scene-context-v1`. Routine risk. `next_sprint` remains null.

Owner-authorized October 4, 2026. Routine risk: derived narration inputs and
instructions only. Protected baseline: `dad93cea3a6b38aa5cd6b9852f44340676be241f`.
Branch: `codex/scene-context-v1`. Sprint 10.79 is complete and frozen.

## Scope
Extend the existing narration boundary with a small derived Scene Context:
stable Market Square grounding, current weather/severity and time, bounded
expected activity, declared player intention and existing local competence.
Explicitly permit incidental low-consequence concretization compatible with
authoritative facts and conditions. Preserve consequential authority, local
causal filtering, competence semantics, fail-closed providers and save behavior.
Use selective experiential narration instructions without fixed prose templates.

Owner-authorized player-path correction: connect the existing narration boundary
to Market Square presentation and observation commands in `play_game.py`, and
route bounded first-person within-scene movement intentions to narration while
preserving explicit navigation. No generalized parser redesign or new state.

Owner-authorized October 5 correction: provisional runtime narrator is
`gpt-6-luna` with reasoning effort `low`, centrally configured in the existing
Responses adapter. House narration is second person; system measurements
normally become qualitative lived language, with exact numbers only for a
supplied credible in-world reason. Retain incidental freedom and consequential
authority limits. No elevated narration mode or provider routing redesign.

## Exclusions and authority
October 5 owner-authorized continuity/progression correction adds bounded,
session-only current-scene presentation continuity and attention stages to the
existing narration boundary, plus CLI compression of routine destination-hop
messages. Preserve low-consequence invention, authority, local competence and
causal locality. Reset continuity on location transition or successful load/reset;
no save changes, long-term memory, model selection or spatial redesign.

No generic scene generator, population/schedule/economy simulation, generated
inventories, incidental persistence or NPC promotion, new competence tags,
causal mechanics, investigation closure, prompt framework, UI work or save
changes. Automated verification remains offline. The owner separately authorized
only the focused Luna-low evaluator validation: five named cases, three repetitions
each, when an API key is available. Preserve `saves/savegame.json` as owner runtime
state and keep all five evaluator files unchanged and unstaged. The owner accepted
the final live narrator smoke and authorized one Sprint 10.80 commit. No push or
merge is authorized. No remote configured.
The known tokenizer-cache limitation remains non-blocking and out of scope.

## Verification and completion
Prove ordinary activity, severe-blizzard suppression, intention propagation,
competence interpretation without truth changes, incidental permission and
consequence protection. Run affected narration, competence and causal-locality
regressions offline, applicable static checks, lifecycle validation, maintained
Git verification, diff check and exact changed-file review. Owner acceptance was
completed October 5, 2026 after the Luna-low three-turn live narrator smoke.
Finalization is one committed review candidate. Preserve save version 1 and keep
`next_sprint` null.
