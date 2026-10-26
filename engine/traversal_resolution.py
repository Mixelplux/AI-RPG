"""D&D 2024 climbing/falling with owner-clarified physical coordination limits.

The common acceptance owner must bind a result to an authorized attempt and
publish dependent World/Character effects together. Sampling is not acceptance.
"""
from dataclasses import dataclass, replace

from engine.information_adjudication import Unresolved
from engine.physical_world import natural, reference
from engine.physical_world import TraversalLink, Surface, PhysicalObject, PhysicalRelation
from engine.character_rules import CreatureRules


@dataclass(frozen=True)
class ClimbRequest:
    attempt: str
    creature: str
    route: str
    distance_feet: int
    use_climb_speed: bool = False
    means: tuple[str, ...] = ()


def validate_climb_request(request):
    """Check exact request types without reading present physical premises."""
    if (type(request) is not ClimbRequest
            or not all(type(v) is str and reference(v) for v in
                       (request.attempt, request.creature, request.route))
            or not natural(request.distance_feet) or request.distance_feet == 0
            or type(request.use_climb_speed) is not bool
            or type(request.means) is not tuple
            or not all(type(v) is str and reference(v) for v in request.means)
            or len(set(request.means)) != len(request.means)):
        raise ValueError('explicit typed climb request required')


@dataclass(frozen=True)
class ClimbRuling:
    require_check: bool
    basis: str  # trusted contextual ruling, not player/model text


@dataclass(frozen=True)
class ClimbDependencies:
    world_revision: str
    at_seconds: int
    character_revision: str
    link: TraversalLink
    surface: Surface
    equipment: tuple[tuple[PhysicalObject, tuple[PhysicalRelation, ...]], ...]
    character: CreatureRules


@dataclass(frozen=True)
class ClimbAssessment:
    request: ClimbRequest
    ruling: ClimbRuling
    status: str  # deterministic, check, unavailable
    reason: str | None
    movement_cost: int
    speed: int
    modifier: int
    advantage: int  # -1 disadvantage, 0 normal/cancelled, +1 advantage
    dc: int | None
    dependencies: ClimbDependencies


@dataclass(frozen=True)
class ClimbResult:
    assessment: ClimbAssessment
    success: bool
    rolls: tuple[int, ...]
    total: int | None
    destination: str | None
    # Failed progress does not establish final position, movement charge or a fall.
    disposition: str


@dataclass(frozen=True)
class FallResult:
    occurrence: str
    creature: str
    landing: str
    rolls: tuple[int, ...]
    bludgeoning_damage: int
    prone: bool
    dependencies: tuple


def die(draw, sides):
    value = draw(sides)
    if type(value) is not int or not 1 <= value <= sides:
        raise Unresolved('resolution', 'invalid_die')
    return value


class TraversalResolution:
    """Owner suppliers return validated views. No provider or scenario dispatch.

    Assessments discover dependencies in the owning domains. Reassessment rejects
    changed material premises before sampling. Results remain unaccepted and are
    absent from the v1/v2 codecs. The opt-in domain campaign validates and accepts
    supported consequences; this rules module never publishes campaign state.
    """
    def __init__(self, world, characters):
        self.world, self.characters = world, characters

    def assess(self, request, ruling):
        validate_climb_request(request)
        if (type(ruling) is not ClimbRuling or type(ruling.require_check) is not bool
                or not reference(ruling.basis)):
            raise ValueError('explicit traversal scope and contextual ruling required')
        world, characters = self.world(), self.characters()
        link, surface, equipment = world.climb_inputs(request.creature, request.route, request.means)
        c = characters.climb_inputs(request.creature, request.means,
            require_check=ruling.require_check, use_climb_speed=request.use_climb_speed)
        capability = characters.physical_capability(request.creature,
            require_speed=not request.use_climb_speed, require_climb_speed=request.use_climb_speed)
        # Deliberate omission of unrelated campaign state. Both domain revisions
        # and actually used records must still be valid at the acceptance seam.
        selected = replace(c, hit_points=None)
        selected = (replace(selected, speed=None) if request.use_climb_speed
                    else replace(selected, climb_speed=None))
        if not ruling.require_check:
            selected = replace(selected, strength=None, proficiency_bonus=None,
                               athletics_rank=None, traits=())
        deps = ClimbDependencies(world.frame.revision, world.frame.at_seconds,
                                 characters.revision, link, surface, equipment, selected)
        if ruling.require_check and not (surface.slippery or surface.few_handholds):
            raise Unresolved('rules', 'check_without_supported_circumstance')
        speed = capability.climb_speed if request.use_climb_speed else capability.speed
        multiplier = (2 if surface.difficult else 1) if request.use_climb_speed else (3 if surface.difficult else 2)
        cost = request.distance_feet * multiplier
        reason = None
        if not surface.climbable or link.blocked:
            reason = 'physical_route_unavailable'
        elif request.distance_feet > link.distance_feet:
            reason = 'extent_exceeds_route'
        elif speed == 0 or cost > max(0, speed - c.movement_spent):
            reason = 'movement_unavailable'
        elif not capability.coordinated_movement:
            # The technique requires physical coordination even without a check.
            # Character owns this general capacity, not a climb-specific condition.
            reason = 'coordinated_movement_unavailable'
        modifier = ((c.strength - 10) // 2 + c.proficiency_bonus * c.athletics_rank
                    - 2 * c.exhaustion) if ruling.require_check else 0
        advantage = (int(any(t.advantage for t in c.traits))
                     - int('poisoned' in c.conditions)) if ruling.require_check else 0
        return ClimbAssessment(request, ruling, 'unavailable' if reason else
            'check' if ruling.require_check else 'deterministic', reason, cost,
            speed, modifier, advantage, 15 if ruling.require_check else None, deps)

    def resolve(self, assessment, draw):
        if type(assessment) is not ClimbAssessment:
            raise ValueError('climb assessment required')
        fresh = self.assess(assessment.request, assessment.ruling)
        if fresh != assessment:
            raise Unresolved('validation', 'stale_traversal_assessment')
        if assessment.status == 'unavailable':
            raise Unresolved('eligibility', assessment.reason)
        rolls, total, success = (), None, True
        if assessment.status == 'check':
            rolls = tuple(die(draw, 20) for _ in range(2 if assessment.advantage else 1))
            selected = min(rolls) if assessment.advantage < 0 else max(rolls)
            total = selected + assessment.modifier
            success = total >= assessment.dc
        if self.assess(assessment.request, assessment.ruling) != assessment:
            raise Unresolved('validation', 'stale_traversal_assessment')
        # The origin/destination relation only proves arrival for the full extent.
        link = assessment.dependencies.link
        destination = link.destination if success and assessment.request.distance_feet == link.distance_feet else None
        return ClimbResult(assessment, success, rolls, total, destination,
                           'progress' if success else 'objective_not_achieved')

    def resolve_fall(self, occurrence, draw):
        world, characters = self.world(), self.characters()
        # Capture immutable values, not aliases to replaceable view attributes.
        frame, character_revision = world.frame, characters.revision
        fall = world.fall_inputs(occurrence)
        c = characters.creature(fall.creature)
        if c.unresolved_rules:
            raise Unresolved('retrieval', 'creature_rule_effect_unavailable')
        if fall.landing_medium != 'solid':
            raise Unresolved('rules', 'liquid_landing_requires_reaction_rules')
        if set(c.conditions) - {'poisoned', 'grappled', 'restrained', 'incapacitated',
                                'paralyzed', 'stunned', 'unconscious'}:
            raise Unresolved('rules', 'unsupported_fall_condition')
        deps = (frame.revision, frame.at_seconds, character_revision, fall, c)
        rolls = tuple(die(draw, 6) for _ in range(min(20, fall.distance_feet // 10)))
        # Do not apply HP, death, landing position or Prone here. This is a single
        # mechanical contribution to the later coherent acceptance unit.
        damage = sum(rolls)
        current_world, current_characters = self.world(), self.characters()
        if (current_world.frame != frame or current_characters.revision != character_revision
                or current_characters.creature(fall.creature) != c):
            raise Unresolved('validation', 'stale_fall_assessment')
        return FallResult(fall.id, fall.creature, fall.landing, rolls, damage, damage > 0, deps)
