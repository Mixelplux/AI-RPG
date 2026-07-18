# Sprint 10.73 - Representative Bryn Shander Topology

This is a deliberately limited local traversal graph, not a complete Bryn
Shander Region Pack or a regional travel policy. It uses the owner-approved
canon-informed anchors: North Gate, East Gate, Southwest Gate, Market Square,
Northlook, Blackiron Blades, Rendaril's Emporium, House of the Triad, Council
Hall, Town Hall, and Speaker's Palace.

## Authored Connective Geography

The following locations are project-authored connective geography rather than
claims of established Forgotten Realms canon:

- `bryn_shander_main_street` is the macro-scale link from North Gate to the
  commercial lanes.
- `outside_tundra_route_north` is the immediate Northern Gate Approach only;
  it is not a wilderness routing model.
- `outside_trade_road_west` is the immediate Southwest Trade Road approach
  only; it preserves the existing one-hour traversal fixture and does not
  establish regional routing.
- `outside_eastway_east` is the immediate Eastway Gate Approach only; it is
  deliberately local and does not establish regional routing.

Existing IDs are retained for save compatibility. In particular,
`bryn_shander_gate_west` now presents the approved physical identity
**Southwest Gate**.

## Topology Contract

Every connection is authored explicitly in both directions. The validator does
not manufacture reverse links. It rejects missing targets, self-links,
duplicate targets from one origin, unpaired connections, and locations that
cannot be reached from the entry location.

`connected_locations` order is intentional. From Main Street, Northlook
precedes Blackiron Blades; both lead to Market Square in two hops, so the
Sprint 10.72 breadth-first resolver deterministically chooses the Northlook
route. The graph also contains longer civic and commercial loops for cross-town
movement.
