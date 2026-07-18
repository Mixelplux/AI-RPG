# Sprint 10.68 - One Unambiguous Two-Hop Local Destination Traversal

Status: Ready for Independent Review.

Capability: Deterministic Abstract Local Destination Traversal.

Sprint 10.68 is implemented and ready for independent review. `next_sprint`
is `null`; no following sprint or capability is authorized or staged.

## Goal

From a current location A, resolve `go to C` or `move to C` through exactly
one uniquely eligible authored local route A -> B -> C, reusing the existing
per-hop movement semantics and ending at canonical location C.

## Authorized Scope

- Resolve only a route with exactly one intermediate location and exactly one
  eligible two-hop route to the named destination.
- Validate the complete two-hop route before the first movement mutation.
- Execute each hop through the existing immediate local movement semantics.
- Preserve direct and immediate movement behavior.
- Keep route resolution transient and derived from existing authored local
  connections.
- Preserve save version `1` and the existing persistence architecture;
  save/load must preserve the resulting canonical location.
- Handle cycles and unrelated connections deterministically and within the
  bounded two-hop search.

## Boundaries

- No arbitrary-length or general pathfinding, route ranking, or tie-breaking.
- No new movement command forms, LLM intent interpretation, narrative
  generation, interruptions, encounters, generated routes, spatial detail,
  destination knowledge/discoverability, or category-based destination
  seeking.
- A missing or ambiguous eligible two-hop route fails deterministically with
  no movement mutation.
- No persistence, migration, parser expansion, or save-version change. Save
  version remains `1` and `next_sprint` remains `null`.

## Completion

The implementation moves A -> B -> C only when `go to C` or `move to C`
identifies one eligible two-hop local route and the entire route validates
before movement begins. Direct and immediate behavior is unchanged; failure
and ambiguity leave movement state unchanged. Focused traversal and affected
movement, route, save/load, narration-context, and provider-safe regressions
pass. No live provider request occurs. The committed candidate is ready for
independent review, with save version `1` and `next_sprint` still `null`.
