"""World-owned local physical premises. Immutable views, no acceptance authority.

None means a material established input is unavailable, never a default fact.
These views are not an additional saved campaign or a global spatial model.
"""
from dataclasses import dataclass, replace

from engine.information_adjudication import Unresolved


def natural(value):
    return type(value) is int and value >= 0


def reference(value):
    return isinstance(value, str) and bool(value.strip())


@dataclass(frozen=True)
class Place:
    id: str
    locality: str


@dataclass(frozen=True)
class Surface:
    id: str
    climbable: bool | None
    slippery: bool | None
    few_handholds: bool | None
    difficult: bool | None
    basis: str
    unresolved_bindings: tuple[str, ...] = ()


@dataclass(frozen=True)
class TraversalLink:
    id: str
    origin: str
    destination: str
    surface: str
    distance_feet: int | None
    blocked: bool | None
    basis: str


@dataclass(frozen=True)
class PhysicalObject:
    id: str
    definition: str
    intact: bool | None


@dataclass(frozen=True)
class PhysicalRelation:
    object: str
    kind: str  # held, carried, attached, secured, located
    target: str
    basis: str


@dataclass(frozen=True)
class CausalRecord:
    id: str
    at_seconds: int
    subjects: tuple[str, ...]
    cause: str


@dataclass(frozen=True)
class FallOccurrence:
    id: str
    creature: str
    origin: str
    landing: str
    distance_feet: int | None
    landing_medium: str | None
    cause: str


@dataclass(frozen=True)
class TautProtection:
    rope: str
    harness: str
    anchor: str
    position: str
    taut: bool | None
    load_bearing: bool | None
    basis: str


@dataclass(frozen=True)
class ClimbCircumstances:
    id: str  # stable reference for the exact established risk commitment
    route: str
    footing: str | None  # load_bearing or grip_dependent during this check
    landing: str | None
    drop_feet: int | None
    landing_medium: str | None
    protection: TautProtection | str | None  # explicit 'none', never inferred
    assistance: str | None
    basis: str
    unresolved_bindings: tuple[str, ...] = ()


@dataclass(frozen=True)
class PhysicalFrame:
    revision: str
    at_seconds: int
    places: tuple[Place, ...]
    creatures: tuple[str, ...]
    positions: tuple[tuple[str, str], ...]
    surfaces: tuple[Surface, ...] = ()
    links: tuple[TraversalLink, ...] = ()
    objects: tuple[PhysicalObject, ...] = ()
    relationships: tuple[PhysicalRelation, ...] = ()
    history: tuple[CausalRecord, ...] = ()
    falls: tuple[FallOccurrence, ...] = ()
    climb_circumstances: tuple[ClimbCircumstances, ...] = ()


class WorldPhysics:
    """Validate composed runtime premises and discover local physical dependencies.

    Suppliers replace a whole validated frame after legitimate World acceptance.
    Constructing/replacing a view does not itself accept any gameplay effect.
    """
    def __init__(self, frame):
        if type(frame) is not PhysicalFrame or not reference(frame.revision) or not natural(frame.at_seconds):
            raise ValueError('physical frame')
        groups = ((frame.places, Place), (frame.surfaces, Surface),
                  (frame.links, TraversalLink), (frame.objects, PhysicalObject),
                  (frame.relationships, PhysicalRelation), (frame.history, CausalRecord),
                  (frame.falls, FallOccurrence), (frame.climb_circumstances, ClimbCircumstances))
        if any(type(items) is not tuple or any(type(i) is not cls for i in items)
               for items, cls in groups):
            raise ValueError('typed immutable physical records required')
        ids = [i.id for items, cls in groups if cls is not PhysicalRelation for i in items]
        if (type(frame.creatures) is not tuple or not all(reference(c) for c in frame.creatures)
                or not all(reference(i) for i in ids)
                or len(set(ids + list(frame.creatures))) != len(ids) + len(frame.creatures)):
            raise ValueError('unique physical identity')
        places = {p.id: p for p in frame.places}
        surfaces = {s.id: s for s in frame.surfaces}
        objects = {o.id: o for o in frame.objects}
        if any(not reference(p.locality) for p in frame.places):
            raise ValueError('locality')
        if (type(frame.positions) is not tuple or any(type(p) is not tuple or len(p) != 2
                or p[0] not in frame.creatures or p[1] not in places for p in frame.positions)
                or len(dict(frame.positions)) != len(frame.positions)):
            raise ValueError('one World position per creature')
        for s in frame.surfaces:
            if (not reference(s.basis) or any(v is not None and type(v) is not bool
                    for v in (s.climbable, s.slippery, s.few_handholds, s.difficult))
                    or type(s.unresolved_bindings) is not tuple
                    or not all(reference(r) for r in s.unresolved_bindings)):
                raise ValueError('surface premises')
        for link in frame.links:
            if (link.origin not in places or link.destination not in places
                    or link.origin == link.destination or link.surface not in surfaces
                    or places[link.origin].locality != places[link.destination].locality
                    or not reference(link.basis)
                    or link.distance_feet is not None and (not natural(link.distance_feet) or not link.distance_feet)
                    or link.blocked is not None and type(link.blocked) is not bool):
                raise ValueError('local traversal relationship')
        for obj in frame.objects:
            if not reference(obj.definition) or obj.intact is not None and type(obj.intact) is not bool:
                raise ValueError('physical object')
        targets = set(places) | set(objects) | set(frame.creatures)
        edges = set()
        for edge in frame.relationships:
            key = (edge.object, edge.kind, edge.target)
            if (edge.object not in objects or edge.target not in targets or edge.object == edge.target
                    or edge.kind not in {'held', 'carried', 'attached', 'secured', 'located'}
                    or not reference(edge.basis) or key in edges
                    or edge.kind in {'held', 'carried'} and edge.target not in frame.creatures
                    or edge.kind == 'located' and edge.target not in places
                    or edge.kind == 'secured' and edge.target in frame.creatures):
                raise ValueError('physical relationship')
            edges.add(key)
        for oid in objects:
            carriers = {e.target for e in frame.relationships if e.object == oid and e.kind in {'held', 'carried'}}
            locations = {e.target for e in frame.relationships if e.object == oid and e.kind == 'located'}
            if len(carriers) > 1 or len(locations) > 1 or carriers and locations:
                raise ValueError('incompatible exclusive disposition')
        for event in frame.history:
            if (not natural(event.at_seconds) or event.at_seconds > frame.at_seconds
                    or type(event.subjects) is not tuple or not event.subjects
                    or not set(event.subjects).issubset(targets | set(surfaces) | {l.id for l in frame.links})
                    or not reference(event.cause)):
                raise ValueError('causal continuity')
        for fall in frame.falls:
            if (fall.creature not in frame.creatures or fall.origin not in places or fall.landing not in places
                    or fall.origin == fall.landing or not reference(fall.cause)
                    or fall.distance_feet is not None and not natural(fall.distance_feet)
                    or fall.landing_medium not in {None, 'solid', 'liquid'}):
                raise ValueError('fall occurrence')
        routes = {r.id: r for r in frame.links}
        if len({x.route for x in frame.climb_circumstances}) != len(frame.climb_circumstances):
            raise ValueError('unique route circumstances')
        for x in frame.climb_circumstances:
            if (x.route not in routes or not reference(x.basis)
                    or x.footing not in {None, 'load_bearing', 'grip_dependent'}
                    or x.landing is not None and x.landing not in places
                    or x.drop_feet is not None and not natural(x.drop_feet)
                    or x.landing_medium not in {None, 'solid', 'liquid'}
                    or x.assistance is not None and not reference(x.assistance)
                    or type(x.unresolved_bindings) is not tuple
                    or not all(reference(v) for v in x.unresolved_bindings)):
                raise ValueError('climb circumstance premises')
            protection = x.protection
            if protection is not None and protection != 'none':
                if (type(protection) is not TautProtection
                        or len({protection.rope, protection.harness, protection.anchor}) != 3
                        or not {protection.rope, protection.harness, protection.anchor}.issubset(objects)
                        or protection.position not in places or not reference(protection.basis)
                        or any(v is not None and type(v) is not bool for v in
                               (protection.taut, protection.load_bearing))):
                    raise ValueError('physical protection premises')
                # This supported configuration has a local fixed anchor and a
                # worn harness. The rope may legitimately span several places;
                # attachment endpoints do not define its exclusive location.
                positions = dict(frame.positions)
                for edge in frame.relationships:
                    if edge.object == protection.anchor:
                        place = (edge.target if edge.kind in {'located', 'secured'} and edge.target in places
                                 else positions.get(edge.target) if edge.kind in {'held', 'carried'} else None)
                        if place is not None and place != protection.position:
                            raise ValueError('contradictory protection anchor disposition')
                wearers = {edge.target for edge in frame.relationships
                           if edge.object == protection.harness and edge.kind == 'attached'
                           and edge.target in frame.creatures}
                known_places = {positions[actor] for actor in wearers if actor in positions}
                known_places.update(edge.target if edge.kind == 'located' else positions.get(edge.target)
                                    for edge in frame.relationships if edge.object == protection.harness
                                    and edge.kind in {'located', 'held', 'carried'})
                known_places.discard(None)
                if len(known_places) > 1:
                    raise ValueError('contradictory protection harness disposition')
        self.frame = frame

    def require_new_identities(self, proposed):
        """Reserve no state; prove all prospective branch IDs are available."""
        existing = set(self.frame.creatures)
        for records in (self.frame.places, self.frame.surfaces, self.frame.links,
                        self.frame.objects, self.frame.history, self.frame.falls,
                        self.frame.climb_circumstances):
            existing.update(record.id for record in records)
        if len(set(proposed)) != len(proposed) or existing.intersection(proposed):
            raise Unresolved('validation', 'world_identity_conflict')

    def relocate_worn_protection(self, creature, position, relationships):
        """Keep an explicitly located worn harness coherent with its wearer."""
        worn = {edge.object for edge in relationships
                if edge.kind == 'attached' and edge.target == creature}
        harnesses = {x.protection.harness for x in self.frame.climb_circumstances
                     if type(x.protection) is TautProtection} & worn
        return tuple(replace(edge, target=position) if edge.object in harnesses and edge.kind == 'located'
                     else edge for edge in relationships)

    def validate_protected_arrival(self, creature, position):
        """Prove the success branch preserves this supported protection setup."""
        positions = tuple((actor, position if actor == creature else place)
                          for actor, place in self.frame.positions)
        relationships = self.relocate_worn_protection(creature, position, self.frame.relationships)
        WorldPhysics(replace(self.frame, positions=positions, relationships=relationships))

    def climb_inputs(self, creature, link_id, means=()):
        link = next((l for l in self.frame.links if l.id == link_id), None)
        if link is None or creature not in self.frame.creatures:
            raise Unresolved('retrieval', 'physical_identity_unavailable')
        position = dict(self.frame.positions).get(creature)
        if position is None:
            raise Unresolved('retrieval', 'position_unavailable')
        if position != link.origin:
            raise Unresolved('eligibility', 'not_at_route_origin')
        surface = next(s for s in self.frame.surfaces if s.id == link.surface)
        if surface.unresolved_bindings:
            raise Unresolved('retrieval', 'surface_binding_unavailable')
        if any(v is None for v in (link.distance_feet, link.blocked, surface.climbable,
                                    surface.slippery, surface.few_handholds, surface.difficult)):
            raise Unresolved('retrieval', 'established_unavailable')
        equipment = []
        for oid in means:
            obj = next((o for o in self.frame.objects if o.id == oid), None)
            if obj is None:
                raise Unresolved('eligibility', 'missing_physical_means')
            if obj.intact is None:
                raise Unresolved('retrieval', 'object_condition_unavailable')
            relations = tuple(e for e in self.frame.relationships if e.object == oid)
            # M1 supports direct handling, not inferred access through arbitrary chains.
            if not obj.intact or not any(e.kind in {'held', 'carried'} and e.target == creature for e in relations):
                raise Unresolved('eligibility', 'means_not_available')
            equipment.append((obj, relations))
        return link, surface, tuple(equipment)

    def fall_inputs(self, occurrence):
        fall = next((f for f in self.frame.falls if f.id == occurrence), None)
        if fall is None or fall.distance_feet is None or fall.landing_medium is None:
            raise Unresolved('retrieval', 'fall_unavailable')
        return fall

    def failure_inputs(self, creature, route):
        """Establish all supported failure branches before an uncertain attempt."""
        x = next((x for x in self.frame.climb_circumstances if x.route == route), None)
        if (x is None or x.unresolved_bindings or x.footing is None
                or x.protection is None or x.assistance is None):
            raise Unresolved('retrieval', 'failure_circumstances_unavailable')
        if x.assistance != 'none':
            raise Unresolved('rules', 'assistance_not_supported')
        link = next(l for l in self.frame.links if l.id == route)
        if x.footing == 'load_bearing':
            if x.protection != 'none':
                raise Unresolved('rules', 'unsupported_combined_support')
            return x
        if (x.landing is None or x.drop_feet is None or x.landing_medium is None):
            raise Unresolved('retrieval', 'fall_geometry_unavailable')
        if (x.drop_feet == 0 or x.landing == link.origin
                or next(p.locality for p in self.frame.places if p.id == x.landing)
                   != next(p.locality for p in self.frame.places if p.id == link.origin)):
            raise Unresolved('validation', 'fall_geometry_incoherent')
        if type(x.protection) is TautProtection:
            p = x.protection
            objects = {o.id: o for o in self.frame.objects}
            edges = {(e.object, e.kind, e.target) for e in self.frame.relationships}
            if (p.taut is not True or p.load_bearing is not True or p.position != link.origin
                    or any(objects[o].intact is not True for o in (p.rope, p.harness, p.anchor))
                    or not {(p.anchor, 'secured', p.position), (p.rope, 'secured', p.anchor),
                            (p.rope, 'attached', p.harness), (p.harness, 'attached', creature)}.issubset(edges)):
                raise Unresolved('validation', 'protection_not_established')
        return x

    def failed_climb(self, request, circumstances):
        """World-owned physical disposition, after separately validated loss of grip."""
        link = next(l for l in self.frame.links if l.id == request.route)
        if circumstances.footing == 'load_bearing':
            return 'supported_no_progress', link.origin, None
        if type(circumstances.protection) is TautProtection:
            return 'grip_lost_protected', circumstances.protection.position, None
        fall = FallOccurrence(request.attempt + ':fall', request.creature, link.origin,
                              circumstances.landing, circumstances.drop_feet,
                              circumstances.landing_medium, request.attempt)
        return 'fell', fall.landing, fall

    def drop_held(self, creature, position):
        """Unconscious creature drops held objects; independent attachments survive."""
        held = {e.object for e in self.frame.relationships if e.kind == 'held' and e.target == creature}
        edges = tuple(e for e in self.frame.relationships
                      if not (e.object in held and e.target == creature and e.kind in {'held', 'carried'}))
        attached = {e.object for e in edges if e.kind in {'attached', 'secured'}}
        return edges + tuple(PhysicalRelation(o, 'located', position, 'unconscious:drop')
                             for o in sorted(held - attached))
