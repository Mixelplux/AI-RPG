# Sprint 10.63 - One-Time Consequence-Bearing Conversation Response

Status: Ready for independent review.

Review state: Candidate prepared.

## Goal

Correct the repeated Elin consequence-bearing response found in playtesting.
The response may occur once after its qualifying discovery and must record the
declared patrol-dispatch consequence as canonical history so it cannot recur.

## Authorized Scope

- Reuse canonical World State history to establish whether the declared West
  Gate patrol-dispatch consequence has already occurred.
- Apply that declared consequence atomically with the first eligible Elin
  conversation, and suppress the special response and its affordance after it.
- Preserve ordinary conversations, deterministic behavior, save version `1`,
  save/load behavior, and the player-safe derived projection boundary.
- Add focused coverage for first use, repeat prevention, no duplicate
  consequence, and save/load persistence.

## Boundaries

- Do not add a generic dialogue-consumption flag or system.
- Do not change parsing, region-pack scope beyond the one declaration, save
  schema/version, providers, or contextual-cue wording.
- Do not start another package; `next_sprint` remains `null`.

## Completion

Focused conversation, discovery, evidence, thread-resolution, relocation,
travel, contextual-action projection, narration-preview, and save/load
regressions pass. A committed review candidate and required review packet are
prepared on a feature branch; merge remains owner-authorized.
