# Sprint 10.62 - Derived Player-Safe Contextual Action Projection

Status: Ready for independent review.

Review state: Independent review pending.

## Value and Scope

Derive a fixed, nonpersistent, player-safe set of contextual action opportunities
from existing authoritative state and authored declarations. The projection is
presentation only and has no simulation authority.

## Authorized Categories

- Speak with a visible, uniquely targetable, named static actor.
- Investigate the current location when an undiscovered declared discovery is
  currently eligible through the existing investigation path.
- Present an already discovered clue to a visible authored target only when the
  existing deterministic clue-presentation path currently accepts it.
- Surface the existing discovery-gated conversation affordance through its
  existing player-safe projection.

## Boundaries

- Reuse or narrowly extract existing investigation and clue-presentation
  eligibility rules; do not duplicate resolver authority.
- Produce deterministic natural-language opportunity text only; never expose
  identifiers, hidden state, command syntax, or eligibility reasons.
- Do not change parsing, action resolution, declarations, Region Packs, save
  data, or save version. Save version remains `1`.
- The projection is derived afresh, non-mutating, and absent from saves.
- No generic action or affordance framework, persistent menu state, provider
  work, or following package is authorized. `next_sprint` remains `null`.

## Completion

Implementation and focused category, negative, non-mutation, stale-action,
save/load, affected-regression, and full deterministic suite coverage passed.
The result is ready for independent review once committed with its validated
package-review archive. `next_sprint` remains `null`.
