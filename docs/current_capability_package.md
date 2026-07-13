# Authored Resolved-Thread Actor Relocation

Status: Complete — ready for owner review.

## Value and Scope

The successful authored clue-presentation resolution for the Bryn Shander west-road report now sends the declared stable guard to the West Gate as durable World State. The package is limited to one optional strict Region Pack declaration, one declared resolved thread, one stable static actor, and one valid destination.

## Ownership and Decisions

Region Pack data owns the immutable declaration and rejects an effect identity that conflicts with any other supported Region Pack effect. World State remains the sole owner of runtime actor-location overrides and thread state. The existing clue-presentation candidate composes source history, resolution, one material relocation and its causal history, validates once, builds one Scene Snapshot, and publishes both together. The public result is only `None`, `{"status": "applied"}`, or `{"status": "no_op"}`; simulation identities remain internal. An already-at-destination actor is a successful no-op with no location history. Save version remains 1.

## Exclusions and Rollback

No generic effects, reaction engine, dialogue framework, scheduling, elapsed-time movement, actor knowledge, evidence, pressure change, spawned actors, or save migration is introduced. Rollback is confined to this feature branch.

## Completion

Focused declaration, atomicity, no-op, repeat, scene, target, perception, save/load, and failure-isolation coverage passed. The full official inventory, manifest agreement, preflight, and packet validation are recorded in the final review archive. No next package is staged.
