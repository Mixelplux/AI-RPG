"""World/Character aggregate and joint reference closure, without action semantics."""
from dataclasses import dataclass

from engine.character_rules import CharacterRules, CreatureRules
from engine.physical_world import PhysicalFrame, WorldPhysics


@dataclass(frozen=True)
class Domains:
    world: PhysicalFrame
    character_revision: str
    characters: tuple[CreatureRules, ...]


def validate_domains(domains):
    if type(domains) is not Domains:
        raise ValueError('domain state')
    world = WorldPhysics(domains.world)
    characters = CharacterRules(domains.character_revision, domains.characters)
    frame = world.frame
    if set(frame.creatures) != {c.id for c in characters.creatures}:
        raise ValueError('creature reference closure')
    if set(dict(frame.positions)) != set(frame.creatures):
        raise ValueError('campaign position closure')
    objects = {o.id for o in frame.objects}
    routes = {r.id for r in frame.links}
    for c in characters.creatures:
        if not set(c.ready_equipment).issubset(objects) or not set(c.known_routes).issubset(routes):
            raise ValueError('character reference closure')
