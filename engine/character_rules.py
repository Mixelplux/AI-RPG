"""Sparse shared creature rules and access. Physical disposition stays World-owned."""
from dataclasses import dataclass

from engine.information_adjudication import Unresolved
from engine.physical_world import natural, reference


@dataclass(frozen=True)
class StrengthTrait:
    definition: str
    advantage: bool


@dataclass(frozen=True)
class CreatureRules:
    id: str
    speed: int | None
    climb_speed: int | None  # 0 explicitly means no Climb Speed; None is unavailable
    strength: int | None
    proficiency_bonus: int | None
    athletics_rank: int | None  # 0 untrained, 1 proficient, 2 expertise
    conditions: tuple[str, ...] = ()
    exhaustion: int = 0
    traits: tuple[StrengthTrait, ...] = ()
    ready_equipment: tuple[str, ...] = ()
    known_routes: tuple[str, ...] = ()
    hit_points: int | None = None
    movement_spent: int | None = None  # accepted turn expenditure; missing is not zero
    unresolved_rules: tuple[str, ...] = ()


@dataclass(frozen=True)
class PhysicalCapability:
    """Character facts; Resolution determines what the chosen technique requires.

    Coordination follows the owner's October 26, 2026 clarification, distinct
    from the 2024 condition's movement allowance and action-economy effects.
    """
    speed: int
    climb_speed: int
    coordinated_movement: bool
    actions: bool
    bonus_actions: bool
    reactions: bool


class CharacterRules:
    def __init__(self, revision, creatures):
        if not reference(revision) or type(creatures) is not tuple or any(type(c) is not CreatureRules for c in creatures):
            raise ValueError('character rules view')
        if len({c.id for c in creatures}) != len(creatures):
            raise ValueError('duplicate creature')
        for c in creatures:
            if (not reference(c.id) or any(v is not None and not natural(v)
                    for v in (c.speed, c.climb_speed, c.proficiency_bonus, c.hit_points, c.movement_spent))
                    or c.strength is not None and (type(c.strength) is not int or not 1 <= c.strength <= 30)
                    or c.athletics_rank is not None and (type(c.athletics_rank) is not int or c.athletics_rank not in {0, 1, 2})
                    or not natural(c.exhaustion) or c.exhaustion > 6):
                raise ValueError('creature statistics')
            for refs in (c.conditions, c.ready_equipment, c.known_routes, c.unresolved_rules):
                if type(refs) is not tuple or not all(reference(r) for r in refs) or len(set(refs)) != len(refs):
                    raise ValueError('character references')
            if (type(c.traits) is not tuple or any(type(t) is not StrengthTrait
                    or not reference(t.definition) or type(t.advantage) is not bool for t in c.traits)
                    or len({t.definition for t in c.traits}) != len(c.traits)):
                raise ValueError('scoped Strength traits')
        self.revision, self.creatures = revision, creatures

    def creature(self, creature):
        profile = next((c for c in self.creatures if c.id == creature), None)
        if profile is None:
            raise Unresolved('retrieval', 'creature_rules_unavailable')
        return profile

    def _physical_profile(self, creature):
        c = self.creature(creature)
        if c.unresolved_rules:
            raise Unresolved('retrieval', 'creature_rule_effect_unavailable')
        supported = {'poisoned', 'grappled', 'restrained', 'incapacitated', 'paralyzed', 'stunned', 'unconscious'}
        if not set(c.conditions).issubset(supported):
            raise Unresolved('rules', 'unsupported_condition')
        return c

    def physical_capability(self, creature):
        c = self._physical_profile(creature)
        if c.speed is None or c.climb_speed is None:
            raise Unresolved('retrieval', 'creature_rules_unavailable')
        conditions = set(c.conditions)
        dead = c.exhaustion == 6
        immobile = dead or bool(conditions & {'grappled', 'restrained', 'paralyzed', 'unconscious'})
        speed = 0 if immobile else max(0, c.speed - 5 * c.exhaustion)
        climb_speed = 0 if immobile else max(0, c.climb_speed - 5 * c.exhaustion)
        coordinated = not (dead or conditions & {'stunned', 'paralyzed', 'unconscious'})
        incapacitated = dead or bool(conditions & {'incapacitated', 'stunned', 'paralyzed', 'unconscious'})
        return PhysicalCapability(speed, climb_speed, coordinated,
                                  not incapacitated, not incapacitated, not incapacitated)

    def climb_inputs(self, creature, means=()):
        c = self._physical_profile(creature)
        if any(v is None for v in (c.speed, c.climb_speed, c.strength, c.proficiency_bonus,
                                    c.athletics_rank, c.movement_spent)):
            raise Unresolved('retrieval', 'creature_rules_unavailable')
        if not set(means).issubset(c.ready_equipment):
            raise Unresolved('eligibility', 'equipment_not_ready')
        return c

    def knows_route(self, creature, route):
        return route in self.creature(creature).known_routes
