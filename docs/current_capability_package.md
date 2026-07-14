# One Derived Discovery-Gated Conversation Affordance

Status: Complete - ready for owner review.

## Value and Scope

One existing meaningful Elin Voss conversation becomes visibly actionable when
the player is at the West Gate, Elin is visibly present and targetable, and the
player already owns the West-Road Orders discovery. The affordance is a derived
player-safe perception fact, not an opportunity entity or command authority.

## Included Milestones

1. Stage the canonical Sprint 10.56 record and validate one exact optional
   `conversation_affordance` Region Pack declaration.
2. Derive one exact player-safe affordance record from player location, scene
   actor presence, and player discovery membership, and add it to perception.
3. Prove repeatability, hidden-state isolation, independent existing-talk
   revalidation, save/load reconstruction, documentation, ADR, and package-review
   closeout.

## Decisions and Impacts

The declaration contains only an affordance identity, location, static target,
required discovery, and display text. Projection contains only `affordance_id`,
`display_text`, deterministic `command_text`, and `target_display_name`. No
World State, history, causal reference, persistence, acknowledgement, or
once-only presentation state is introduced. Save version remains 1.

## Exclusions and Rollback

No durable opportunity, multiple affordances, ordering, priority, scoring,
generic condition language, action type, lifecycle, consumption, command or
parser change, actor knowledge, evidence, pressure, history, future-effect,
hidden-intent eligibility, generic framework, or save migration is permitted.
Removing the declaration or projection returns perception to its prior shape;
no durable rollback is needed.

## Verification and Completion

Focused and full official-interpreter verification, Region Pack validation,
canonical-record agreement, preflight, diff check, and independent
package-review archive validation passed. No following package is staged.
