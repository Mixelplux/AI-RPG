# Sprint 10.70 - One Hop-Count-Agnostic Unambiguous Local Destination Route Resolver

Status: Ready for Independent Review.

Sprint 10.70 is implemented and ready for independent review; `next_sprint`
is `null`.

## Goal

Derive and prevalidate exactly one authored simple local route of any hop
length for `go to <location>` and `move to <location>`, then compose existing
immediate movement transitions.

## Boundaries

Routes are transient and unranked. Repeated locations are excluded from a
candidate route, making cycles finite without a hop limit. No route ranking,
persistence, save migration, parser expansion, generated content, encounters,
or significance system is introduced.

## Completion

Unique routes of any authored length succeed; zero or multiple routes fail
without mutation. Existing immediate, two-hop, and three-hop behavior and save
version `1` remain compatible. The candidate is unmerged pending review.
