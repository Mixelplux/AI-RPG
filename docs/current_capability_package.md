# Sprint 10.72 - One Deterministic Mundane Multi-Route Local Destination Resolver

Status: Ready for Independent Review.

Sprint 10.72 selects one provisional local mundane route when static authored
topology contains multiple valid simple routes to a resolved destination.
`next_sprint` remains `null`.

## Goal

Prefer the route with the fewest authored connections. For equal hop counts,
use the stable order of the existing authored `connected_locations` lists.

## Boundaries

The resolver reads only static authored topology, preserves authored direction,
and produces the existing transient ordered `movement_hops` for sequential
authoritative traversal. Hop count is not physical distance or travel time.
No edge costs, hidden-state routing, rerouting, route-choice interaction,
regional or wilderness policy, encounter generation, parser expansion,
persistence change, migration, narration, or provider behavior is added.

## Completion

Focused shortest-route, stable tie-break, directionality, failure, traversal,
save/load, narration-context, and provider-safe regressions passed. Save version
remains `1`, route plans remain provisional, `movement_hops` remains transient,
and a clean committed independent-review candidate is prepared without staging
a following package. No live provider request occurred.
