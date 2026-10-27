"""Climbing-owned rules, effects, evidence and continuity premises for schema 4.

This adapter composes World, Character and Resolution; it never publishes a root.
"""
from dataclasses import dataclass, replace

from engine.character_rules import CharacterRules, CreatureRules
from engine.domain_campaign import Contribution
from engine.domain_state import Domains, validate_domains
from engine.gameplay_coordination import AcceptedStep
from engine.information_adjudication import Unresolved
from engine.physical_world import (WorldPhysics, CausalRecord, FallOccurrence, TautProtection,
    Surface, TraversalLink, PhysicalObject, PhysicalRelation, ClimbCircumstances, natural, reference)
from engine.traversal_resolution import (ClimbRequest, ClimbRuling, ClimbResult, TraversalResolution,
    validate_climb_request, FallDependencies, FallResult, climb_result, fall_result, die)


@dataclass(frozen=True)
class ClimbPlan:
    duration_seconds: int
    time_basis: str
    ruling: ClimbRuling


@dataclass(frozen=True)
class ClimbOptions:
    means: tuple[str, ...] = ()
    use_climb_speed: bool = False
    distance_feet: int | None = None


@dataclass(frozen=True)
class TraversalConsequence:
    kind: str
    position: str
    fall: FallOccurrence | None = None
    injury: FallResult | None = None


@dataclass(frozen=True)
class ClimbUpdate:
    surfaces: tuple[Surface, ...] = ()
    links: tuple[TraversalLink, ...] = ()
    objects: tuple[PhysicalObject, ...] = ()
    relationships: tuple[PhysicalRelation, ...] | None = None
    circumstances: tuple[ClimbCircumstances, ...] = ()
    characters: tuple[CreatureRules, ...] = ()
    elapsed_seconds: int = 0


@dataclass(frozen=True)
class _Command:
    request: ClimbRequest
    run: bool | None


@dataclass(frozen=True)
class _Scope:
    duration_seconds: int
    ruling: ClimbRuling
    authorization: object
    checkpoint: object


def owners(domains):
    return WorldPhysics(domains.world), CharacterRules(domains.character_revision, domains.characters)
def movement_charge(result):
    return (result.assessment.movement_cost if result.success
            else result.assessment.ruling.failure_movement_cost)


def movement_meaning(command, result, duration, consequence=None):
    if consequence is None or consequence.kind == 'arrived':
        destination = 'the next established position' if command.run is not None else 'the chosen destination'
        effect = f'You climb {command.request.distance_feet} feet to {destination}.'
    elif consequence.kind == 'supported_no_progress':
        effect = 'You do not make progress; you remain on the existing footing.'
    elif consequence.kind == 'grip_lost_protected':
        effect = 'You lose your grip; the taut protection supports you in place.'
    elif consequence.kind == 'fell':
        damage = consequence.injury.bludgeoning_damage
        c = consequence.injury.dependencies.character
        # Observation ends at loss of consciousness. No landing name, hidden
        # cause, subsequent fact or omniscient diagnosis enters the receipt.
        injured = CharacterRules('receipt', (c,)).apply_fall_damage(c.id, damage) if damage else c
        if injured.vitality is not None and (injured.vitality.dead or 'unconscious' in injured.conditions):
            effect = 'You lose your grip and fall; awareness ends at the impact.'
        else:
            effect = 'You lose your grip and fall.'
            if damage:
                effect += f' You take {damage} Bludgeoning damage and are Prone.'
    else:
        raise ValueError('unsupported physical consequence')
    return (f'{effect} {duration} seconds pass; '
            f'{movement_charge(result)} feet of movement are spent.')


def safe_receipt(command, result, duration, consequence=None):
    text = movement_meaning(command, result, duration, consequence)
    return AcceptedStep(command.request.attempt, ('movement',), 'complete', (('movement', text),))


def validate_receipt(receipt, command, result, duration, consequence):
    """Validate supported, grounded and character-accessible meaning independently.

    Recompute from checked evidence rather than trusting the receipt producer.
    movement_meaning bounds observation at loss of awareness and excludes hidden
    causes, landing identities and subsequent facts.
    """
    if (type(receipt) is not AcceptedStep or receipt.ref != command.request.attempt
            or receipt.public_refs != ('movement',) or receipt.outcome != 'complete'
            or receipt.accessible != (('movement', movement_meaning(
                command, result, duration, consequence)),)):
        raise Unresolved('receipt', 'invalid_safe_receipt')



def inspect(campaign, command, scope, *, execution=True):
    """Read-only branch sufficiency, applicability and authorization; never draw."""
    world, characters = owners(campaign.current)
    r = command.request
    if not characters.knows_route(r.creature, r.route):
        raise Unresolved('access', 'route_not_legitimately_known')
    if characters.creature(r.creature).hit_points == 0:
        raise Unresolved('eligibility', 'ordinary_climb_not_available')
    resolution = TraversalResolution(lambda: world, lambda: characters)
    assessment = resolution.assess(r, scope.ruling)
    if assessment.status == 'unavailable':
        raise Unresolved('eligibility', assessment.reason)
    if r.distance_feet != assessment.dependencies.link.distance_feet:
        raise Unresolved('resolution', 'established_endpoint_required')
    circumstances = None
    proposed_ids = [f'{campaign.id}:accepted:{campaign.revision + 1}']
    if scope.ruling.require_check:
        circumstances = world.failure_inputs(r.creature, r.route)
        expected = 'no_progress' if circumstances.footing == 'load_bearing' else 'loss_of_grip'
        if scope.ruling.failure_mode != expected:
            raise Unresolved('rules', 'unsupported_failure_classification')
        if (not natural(scope.ruling.failure_movement_cost)
                or scope.ruling.failure_movement_cost > assessment.movement_cost):
            raise Unresolved('rules', 'failure_expenditure_unestablished')
        if circumstances.footing == 'grip_dependent':
            hidden_boundary = any(
                d.choice_key == circumstances.id and (not d.perceived or not d.opportunity_to_respond)
                for d in scope.checkpoint.developments)
            if circumstances.id not in scope.authorization.answered_choices and execution and not hidden_boundary:
                raise Unresolved('authorization', 'unanswered_fall_risk')
            if type(circumstances.protection) is TautProtection:
                p = circumstances.protection
                if not {p.rope, p.harness}.issubset(characters.creature(r.creature).ready_equipment):
                    raise Unresolved('eligibility', 'protection_not_ready')
                world.validate_protected_arrival(r.creature, assessment.dependencies.link.destination)
            else:
                if circumstances.landing_medium != 'solid':
                    raise Unresolved('rules', 'unsupported_landing')
                if circumstances.drop_feet >= 10:
                    characters.injury_inputs(r.creature)
                proposed_ids.append(r.attempt + ':fall')
    world.require_new_identities(proposed_ids)
    return scope, world, characters, assessment, circumstances


def consequence_for(campaign, command, result, circumstances, damage_rolls):
    """Pure owner composition over fixed circumstances and recorded randomness."""
    if result.success:
        if damage_rolls:
            raise ValueError('unexpected damage rolls')
        return TraversalConsequence('arrived', result.destination)
    world, characters = owners(campaign.current)
    kind, position, fall = world.failed_climb(command.request, circumstances)
    injury = None
    if fall is not None:
        deps = FallDependencies(world.frame.revision, world.frame.at_seconds, characters.revision,
                                fall, characters.creature(command.request.creature))
        injury = fall_result(deps, damage_rolls)
    elif damage_rolls:
        raise ValueError('damage without a fall')
    return TraversalConsequence(kind, position, fall, injury)



def compose(campaign, command, result, duration, consequence):
    state = campaign.current
    r = command.request
    frame = state.world
    revision = campaign.revision + 1
    position = result.destination if consequence is None else consequence.position
    falls = frame.falls + ((consequence.fall,) if consequence is not None and consequence.fall is not None else ())
    profiles = CharacterRules(state.character_revision, state.characters)
    creature = profiles.creature(r.creature)
    if consequence is not None and consequence.injury is not None and consequence.injury.bludgeoning_damage:
        creature = profiles.apply_fall_damage(r.creature, consequence.injury.bludgeoning_damage)
    drops = ('unconscious' in creature.conditions or creature.vitality is not None and creature.vitality.dead)
    physical = WorldPhysics(frame)
    relationships = physical.drop_held(r.creature, position) if drops else frame.relationships
    relationships = physical.relocate_worn_protection(r.creature, position, relationships)
    # World validates the new position/time/cause; Character validates expenditure.
    world = replace(frame, revision=f'{campaign.id}:world:{revision}',
        at_seconds=frame.at_seconds + duration,
        falls=falls, relationships=relationships,
        positions=tuple((actor, position if actor == r.creature else place)
                        for actor, place in frame.positions),
        history=frame.history + (CausalRecord(f'{campaign.id}:accepted:{revision}',
            frame.at_seconds + duration, (r.creature, r.route), r.attempt),))
    characters = tuple(replace(creature, movement_spent=c.movement_spent + movement_charge(result))
                       if c.id == r.creature else c for c in state.characters)
    current = Domains(world, f'{campaign.id}:character:{revision}', characters)
    validate_domains(current)
    return current



def replace_named(current, changes, cls, key='id'):
    if type(changes) is not tuple or any(type(x) is not cls for x in changes):
        raise ValueError('typed owner facts required')
    supplied = {getattr(x, key): x for x in changes}
    existing = {getattr(x, key): x for x in current}
    if len(supplied) != len(changes) or not set(supplied).issubset(existing):
        raise ValueError('existing owner identity required')
    return tuple(supplied.get(getattr(x, key), x) for x in current)


class ClimbingDomain:
    id = 'physical-climbing-v1'

    def validate_scope(self, campaign, scope):
        if scope.authorization.method != 'climb':
            raise ValueError('climbing method required')
        routes = {l.id: l for l in campaign.origin.world.links}
        previous = None
        for stage in scope.stages:
            if len(stage.payload) != 1 or type(stage.payload[0]) is not ClimbPlan or stage.target not in routes:
                raise ValueError('climbing stage required')
            p = stage.payload[0]
            r = p.ruling
            if (not natural(p.duration_seconds) or not p.duration_seconds or not reference(p.time_basis)
                    or type(r) is not ClimbRuling or type(r.require_check) is not bool or not reference(r.basis)
                    or r.failure_mode not in {None, 'no_progress', 'loss_of_grip'}
                    or r.failure_movement_cost is not None and not natural(r.failure_movement_cost)):
                raise ValueError('climbing timing/ruling required')
            link = routes[stage.target]
            if previous is not None and previous.destination != link.origin:
                raise ValueError('continuous established path required')
            previous = link

    def inputs(self, campaign, command, scope):
        if len(command.payload) != 1 or type(command.payload[0]) is not ClimbOptions:
            raise ValueError('climbing options required')
        options = command.payload[0]
        links = {l.id: l for l in campaign.current.world.links}
        if scope.target not in links:
            raise Unresolved('retrieval', 'route_unavailable')
        distance = links[scope.target].distance_feet if options.distance_feet is None else options.distance_feet
        request = ClimbRequest(command.id, scope.actor, scope.target, distance,
                               options.use_climb_speed, options.means)
        validate_climb_request(request)
        p = scope.payload[0]
        return _Command(request, True if command.run is not None else None), _Scope(
            p.duration_seconds, p.ruling, scope.authorization, scope.checkpoint)

    def validate_command(self, campaign, command, scope):
        self.inputs(campaign, command, scope)

    def means(self, command):
        return command.payload[0].means

    def assess(self, campaign, command, scope, *, execution):
        c, s = self.inputs(campaign, command, scope)
        return inspect(campaign, c, s, execution=execution)

    def prepare(self, campaign, command, scope, draw):
        _, world, characters, assessment, circumstances = self.assess(campaign, command, scope, execution=True)
        c, s = self.inputs(campaign, command, scope)
        result = TraversalResolution(lambda: world, lambda: characters).resolve(assessment, draw)
        rolls = ()
        if not result.success:
            _, _, fall = world.failed_climb(c.request, circumstances)
            if fall is not None:
                rolls = tuple(die(draw, 6) for _ in range(min(20, fall.distance_feet // 10)))
        return self.evaluate(campaign, command, scope, (result, consequence_for(campaign, c, result, circumstances, rolls)))

    def evaluate(self, campaign, command, scope, evidence):
        if len(evidence) != 2 or type(evidence[0]) is not ClimbResult or type(evidence[1]) is not TraversalConsequence:
            raise ValueError('climbing evidence required')
        _, world, characters, assessment, circumstances = self.assess(campaign, command, scope, execution=True)
        c, s = self.inputs(campaign, command, scope)
        supplied, consequence = evidence
        result = climb_result(assessment, supplied.rolls)
        rolls = consequence.injury.rolls if type(consequence.injury) is FallResult else ()
        expected = consequence_for(campaign, c, result, circumstances, rolls)
        if (supplied, consequence) != (result, expected):
            raise Unresolved('validation', 'climbing_meaning_mismatch')
        current = compose(campaign, c, result, s.duration_seconds, expected)
        receipt = safe_receipt(c, result, s.duration_seconds, expected)
        validate_receipt(receipt, c, result, s.duration_seconds, expected)
        return Contribution(current, (result, expected), result.success, receipt)

    def decision_basis(self, campaign, scope, index):
        stage = scope.stages[index]
        risks = {x.route: x for x in campaign.current.world.climb_circumstances}
        r = stage.payload[0].ruling
        return (risks.get(stage.target), r.require_check, r.failure_mode, r.failure_movement_cost)

    def initial_choices(self, campaign, scope):
        routes = {s.target for s in scope.stages}
        return {x.id for x in campaign.origin.world.climb_circumstances if x.route in routes}

    def update(self, campaign, event, scope):
        if not event.payload:
            return campaign.current
        if len(event.payload) != 1 or type(event.payload[0]) is not ClimbUpdate:
            raise ValueError('climbing owner update required')
        update = event.payload[0]
        if not natural(update.elapsed_seconds):
            raise ValueError('owner elapsed time')
        current, world = campaign.current, campaign.current.world
        old_risks = {x.route: x for x in world.climb_circumstances}
        historical_risks = {x.id: x for x in campaign.origin.world.climb_circumstances}
        from engine.domain_campaign import ActivityUpdate
        for accepted in campaign.accepted:
            if type(accepted) is ActivityUpdate and accepted.payload and type(accepted.payload[0]) is ClimbUpdate:
                historical_risks.update((x.id, x) for x in accepted.payload[0].circumstances)
        for x in update.circumstances:
            if x.id in historical_risks and historical_risks[x.id] != x:
                raise ValueError('risk identity must retain historical meaning')
        risks = dict(old_risks)
        if len({x.route for x in update.circumstances}) != len(update.circumstances):
            raise ValueError('unique risk contribution')
        risks.update((x.route, x) for x in update.circumstances)
        links = replace_named(world.links, update.links, TraversalLink)
        for before, after in zip(world.links, links):
            if (before.origin, before.destination) != (after.origin, after.destination):
                raise ValueError('a development cannot replace chosen route endpoints')
        world = replace(world,
            surfaces=replace_named(world.surfaces, update.surfaces, Surface), links=links,
            objects=replace_named(world.objects, update.objects, PhysicalObject),
            relationships=world.relationships if update.relationships is None else update.relationships,
            climb_circumstances=tuple(risks.values()), at_seconds=world.at_seconds + update.elapsed_seconds)
        characters = replace_named(current.characters, update.characters, CreatureRules)
        for before, after in zip(current.characters, characters):
            if (before.movement_spent, before.hit_points, before.vitality) != (
                    after.movement_spent, after.hit_points, after.vitality):
                raise ValueError('development cannot overwrite accepted character consequences')
        result = replace(current, world=world, characters=characters)
        validate_domains(result)
        return result


CLIMBING = ClimbingDomain()
