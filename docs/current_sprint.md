# Sprint 10.67 - Immediate Local Travel Phrase Alignment

Status: Ready for Independent Review.

Review state: Candidate prepared.

`next_sprint` is `null`. This is the active, owner-authorized capability
package; no following sprint is authorized or staged.

## Goal

Align `go to <location>` and `head to <location>` with the existing immediate
local movement result, without converting nonlocal destination identification
into travel.

## Expected Files

- `engine/interaction_kernel.py`
- `test_interaction_kernel.py`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- `go to Main Street` and `head to Main Street` from North Gate move only
  because Main Street is a uniquely named immediately traversable connection;
  their destination and movement behavior match `go south` and `move to Main
  Street`.
- Non-adjacent names retain existing nonmoving destination-identification
  behavior; they do not invoke travel, pathfinding, or multi-step routing.
- Ambiguous or invalid immediate names fail closed without player movement,
  history, or other state change.
- The interaction kernel resolves only immediate scene candidates; the
  destination resolver remains the fallback for nonmoving loaded-region
  identification when no immediate unique match exists.
- No persistence, history model, parser framework, provider behavior,
  migration, or save-version change is introduced. Save version remains `1`
  and `next_sprint` remains `null`.

## Verification

- Official-interpreter preflight, syntax checks, canonical-record validation,
  and `git diff --check` pass.
- Focused phrase-alignment coverage proves local `go to` and `head to`
  equivalence, non-adjacent nonmoving fallback, ambiguity refusal, invalid
  refusal, and no state change on failed movement.
- Affected interaction-kernel, movement, navigation-projection, save/load,
  narration-context, and provider-safe regressions pass. No live provider
  request occurred.
- The bounded candidate is committed and ready for independent review; save
  version remains `1` and `next_sprint` remains `null`.
