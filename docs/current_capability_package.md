# Sprint 10.71 - One Hop-Count-Agnostic Sequential Local Destination Traversal

Status: Ready for Independent Review.

Sprint 10.71 executes the ordered transient `movement_hops` supplied by the
existing Sprint 10.70 resolver as sequential authoritative movement
transitions. `next_sprint` is `null`.

## Goal

For a resolved finite local route, validate, build the scene for, and publish
each completed hop before beginning the next hop.

## Boundaries

Route plans remain provisional and transient. Completed hops remain
authoritative if a later hop fails. The existing resolver, route model,
directionality, parser, save version, and persistence model are unchanged.
No interruption, dynamic-route, narration, or provider behavior is added.

## Completion

Routes of four or more hops execute in order; timed intermediate movement
retains its existing duration and consequences; one-, two-, and three-hop
behavior remains compatible. Save version remains `1`, `movement_hops` remains
transient, and a clean committed review candidate is prepared without staging
a following package. Verification passed; no live provider request occurred.
