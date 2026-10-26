"""Sparse shared creature rules and access. Physical disposition stays World-owned."""
from dataclasses import dataclass

from engine.information_adjudication import Unresolved
from engine.physical_world import natural, reference


@dataclass(frozen=True)
class StrengthTrait:
    definition: str
    advantage: bool


@dataclass(frozen=True)
class Vitality:
    maximum_hp: int
    temporary_hp: int = 0
    zero_hp_rule: str = 'death_saves'  # same explicit treatment for PCs and NPCs
    dead: bool = False
    stable: bool = False
    death_successes: int = 0
    death_failures: int = 0


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
    vitality: Vitality | None = None


@dataclass(frozen=True)
class PhysicalCapability:
    """Character facts; Resolution determines what the chosen technique requires.

    Coordination follows the owner's October 26, 2026 clarification, distinct
    from the 2024 condition's movement allowance and action-economy effects.
    """
    speed: int | None
    climb_speed: int | None
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
            v = c.vitality
            if v is not None:
                if (type(v) is not Vitality or not natural(v.maximum_hp) or v.maximum_hp == 0
                        or not natural(v.temporary_hp) or type(v.dead) is not bool or type(v.stable) is not bool
                        or v.zero_hp_rule not in {'death_saves', 'instant_death'}
                        or not natural(v.death_successes) or v.death_successes > 2
                        or not natural(v.death_failures) or v.death_failures > 3
                        or c.hit_points is None or c.hit_points > v.maximum_hp
                        or v.dead and (c.hit_points != 0 or v.stable)
                        or v.stable and (c.hit_points != 0 or v.death_successes or v.death_failures)
                        or c.hit_points > 0 and (v.dead or v.stable or v.death_successes or v.death_failures)
                        or v.death_failures == 3 and not v.dead
                        or c.hit_points == 0 and not v.dead and v.zero_hp_rule == 'instant_death'
                        or c.hit_points == 0 and not v.dead and not {'unconscious', 'incapacitated', 'prone'}.issubset(c.conditions)):
                    raise ValueError('coherent Character vitality required')
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
        supported = {'poisoned', 'grappled', 'restrained', 'incapacitated', 'paralyzed', 'stunned', 'unconscious', 'prone'}
        if not set(c.conditions).issubset(supported):
            raise Unresolved('rules', 'unsupported_condition')
        return c

    def physical_capability(self, creature, *, require_speed=True, require_climb_speed=True):
        c = self._physical_profile(creature)
        if require_speed and c.speed is None or require_climb_speed and c.climb_speed is None:
            raise Unresolved('retrieval', 'creature_rules_unavailable')
        conditions = set(c.conditions)
        dead = c.exhaustion == 6 or c.vitality is not None and c.vitality.dead
        immobile = dead or bool(conditions & {'grappled', 'restrained', 'paralyzed', 'unconscious'})
        speed = None if c.speed is None else 0 if immobile else max(0, c.speed - 5 * c.exhaustion)
        climb_speed = None if c.climb_speed is None else 0 if immobile else max(0, c.climb_speed - 5 * c.exhaustion)
        coordinated = not (dead or conditions & {'stunned', 'paralyzed', 'unconscious'})
        incapacitated = dead or bool(conditions & {'incapacitated', 'stunned', 'paralyzed', 'unconscious'})
        return PhysicalCapability(speed, climb_speed, coordinated,
                                  not incapacitated, not incapacitated, not incapacitated)

    def climb_inputs(self, creature, means=(), *, require_check=True, use_climb_speed=False):
        c = self._physical_profile(creature)
        if 'prone' in c.conditions or c.vitality is not None and c.hit_points == 0:
            raise Unresolved('eligibility', 'ordinary_climb_not_available')
        required = (c.climb_speed if use_climb_speed else c.speed, c.movement_spent)
        if require_check:
            required += (c.strength, c.proficiency_bonus, c.athletics_rank)
        if any(v is None for v in required):
            raise Unresolved('retrieval', 'creature_rules_unavailable')
        if not set(means).issubset(c.ready_equipment):
            raise Unresolved('eligibility', 'equipment_not_ready')
        return c

    def knows_route(self, creature, route):
        return route in self.creature(creature).known_routes

    def injury_inputs(self, creature):
        c = self._physical_profile(creature)
        if c.hit_points is None or c.vitality is None:
            raise Unresolved('retrieval', 'injury_premises_unavailable')
        if c.vitality.dead or c.exhaustion == 6:
            raise Unresolved('rules', 'dead_creature_injury_unsupported')
        return c

    def apply_fall_damage(self, creature, damage):
        """Character-owned immediate injury. No death-save turn or recovery executor."""
        from dataclasses import replace
        c = self.injury_inputs(creature)
        if not natural(damage):
            raise ValueError('fall damage')
        v = c.vitality
        absorbed = min(v.temporary_hp, damage)
        remaining = damage - absorbed
        hp = max(0, c.hit_points - remaining)
        v = replace(v, temporary_hp=v.temporary_hp - absorbed)
        conditions = list(c.conditions)
        if damage and 'prone' not in conditions:
            conditions.append('prone')
        if damage and hp == 0:
            if c.hit_points == 0:
                v = replace(v, stable=False, death_successes=0 if v.stable else v.death_successes,
                            death_failures=(0 if v.stable else v.death_failures) + 1)
            # Damage taken at zero HP is distinct from the overflow that
            # reduced positive HP to zero. Temporary HP buffer HP loss, not
            # damage taken for the already-zero death threshold.
            lethal_amount = damage if c.hit_points == 0 else remaining - c.hit_points
            dead = (v.zero_hp_rule == 'instant_death'
                    or lethal_amount >= v.maximum_hp or v.death_failures >= 3)
            v = replace(v, dead=dead)
            if not dead:
                for condition in ('unconscious', 'incapacitated', 'prone'):
                    if condition not in conditions:
                        conditions.append(condition)
        result = replace(c, hit_points=hp, vitality=v, conditions=tuple(conditions))
        CharacterRules('injury:validated', (result,))
        return result
