# Sprint 10.73 - Representative Bryn Shander Traversal Region and Topology Integrity

Status: Ready for Independent Review.

## Goal

Create a representative canon-informed Bryn Shander macro traversal graph that
can be deterministically traversed and inspected for local topology integrity.

## Expected Files

- `data/regions/bryn_shander.json`
- `engine/region_validator.py`
- `test_interaction_kernel.py`
- `test_region_topology.py`
- `test_navigation_projection.py`
- `test_contextual_action_projection.py`
- `test_discovery_gated_conversation_affordance.py`
- `test_discovery_gated_relocated_actor_response.py`
- `test_one_hour_west_road_exit_traversal.py`
- `test_delayed_watch_discovery_actor_recall.py`
- `test_discovery.py`
- `test_resolved_thread_evidence_trace_consequence.py`
- `docs/bryn_shander_topology.md`
- `docs/current_capability_package.md`
- `docs/current_sprint.md`
- `docs/current_sprint.json`

## Acceptance Criteria

- The approved representative anchors, gates, civic area, commercial area, and
  minimal connective geography form one reachable local graph.
- Every ordinary connection is explicitly reciprocal; the validator rejects
  missing targets, self-links, duplicate targets, missing reverse edges, and
  unreachable locations.
- The graph contains loops and equal-hop alternate routes whose deterministic
  selection follows the Sprint 10.72 authored connection ordering.
- Route selection remains static-topology-only, `movement_hops` remains
  transient, save version remains `1`, and no provider request occurs.

## Verification

Topology validation and deterministic routing tests; the full script-based
regression suite including movement, save/load, narration-context, and
provider-safe regressions; official interpreter preflight; canonical record
validation; `git diff --check`; and a validated package-review packet.
