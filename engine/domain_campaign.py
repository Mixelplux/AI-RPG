"""Domain-owned aggregate preparation/validation for the common Runtime.

This module owns no live root. Proposals and restored candidates are inert values.
Only Runtime publishes. Unsupported consequence semantics fail before resolution.
"""
from dataclasses import dataclass, replace

from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, decide_activity_control
from engine.character_rules import CharacterRules, CreatureRules
from engine.gameplay_coordination import AcceptedStep, SituatedContext, validate_context
from engine.information_adjudication import Unresolved
from engine.physical_world import PhysicalFrame, WorldPhysics, CausalRecord, FallOccurrence, TautProtection, natural, reference
from engine.traversal_resolution import (
    ClimbRequest, ClimbRuling, ClimbResult, TraversalResolution, validate_climb_request,
    FallDependencies, FallResult, climb_result, fall_result, die,
)


@dataclass(frozen=True)
class Domains:
    world: PhysicalFrame
    character_revision: str
    characters: tuple[CreatureRules, ...]


@dataclass(frozen=True)
class ActivityScope:
    id: str
    actor: str
    target: str
    authorization: ActivityAuthorization
    checkpoint: ActivityCheckpoint
    duration_seconds: int
    time_basis: str
    ruling: ClimbRuling


@dataclass(frozen=True)
class Increment:
    activity: str
    request: ClimbRequest


@dataclass(frozen=True)
class TraversalConsequence:
    kind: str
    position: str
    fall: FallOccurrence | None = None
    injury: FallResult | None = None


@dataclass(frozen=True)
class AcceptedUnit:
    command: Increment
    result: ClimbResult
    duration_seconds: int
    receipt: AcceptedStep
    consequence: TraversalConsequence | None = None


@dataclass(frozen=True)
class Campaign:
    id: str
    actor: str
    origin: Domains
    current: Domains
    activities: tuple[ActivityScope, ...]
    accepted: tuple[AcceptedUnit, ...] = ()
    revision: int = 0
    schema: int = 1


@dataclass(frozen=True)
class Proposal:
    base: Campaign
    unit: AcceptedUnit


def owners(domains):
    return WorldPhysics(domains.world), CharacterRules(domains.character_revision, domains.characters)


def validate_domains(domains):
    if type(domains) is not Domains:
        raise ValueError('domain state')
    world, characters = owners(domains)
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


def validate_increment(command):
    if (type(command) is not Increment or type(command.activity) is not str
            or not reference(command.activity)):
        raise ValueError('explicit increment required')
    validate_climb_request(command.request)


def validate_resolution_reference(checkpoint):
    # M2-1 accepts resolution and execution together, not separate reusable
    # checkpoint resolutions. Exact accepted retries use Campaign.accepted.
    if checkpoint.resolution_ref is not None:
        raise ValueError('checkpoint resolution references are unsupported in M2-1')


def scope_for(campaign, command, *, execution=True):
    validate_increment(command)
    scope = next((a for a in campaign.activities if a.id == command.activity), None)
    r = command.request
    if scope is None or (scope.actor, scope.target, scope.authorization.method) != (r.creature, r.route, 'climb'):
        raise Unresolved('authorization', 'activity_scope')
    if r.creature != campaign.actor:
        raise Unresolved('authorization', 'controlling_actor')
    # No constraints are silently claimed as supported by this bounded method.
    if scope.authorization.constraints:
        raise Unresolved('authorization', 'unsupported_constraints')
    validate_resolution_reference(scope.checkpoint)
    control = decide_activity_control(scope.authorization, scope.checkpoint)
    if execution and control.status != 'continue':
        raise Unresolved('authorization', 'return_control')
    return scope


def prior(campaign, command):
    validate_increment(command)
    accepted = next((a for a in campaign.accepted
                     if a.command.request.attempt == command.request.attempt), None)
    if accepted is not None and accepted.command != command:
        raise Unresolved('acceptance', 'identity_conflict')
    return accepted


def movement_charge(result):
    return (result.assessment.movement_cost if result.success
            else result.assessment.ruling.failure_movement_cost)


def movement_meaning(command, result, duration, consequence=None):
    if consequence is None or consequence.kind == 'arrived':
        effect = f'You climb {command.request.distance_feet} feet to the chosen destination.'
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


def validate_receipt(unit):
    receipt = unit.receipt
    if (type(receipt) is not AcceptedStep or receipt.ref != unit.command.request.attempt
            or receipt.public_refs != ('movement',) or receipt.outcome != 'complete'
            or receipt.accessible != (('movement', movement_meaning(
                unit.command, unit.result, unit.duration_seconds, unit.consequence)),)):
        raise Unresolved('receipt', 'invalid_safe_receipt')
    validate_context(SituatedContext('receipt', 'receipt', accessible=receipt.accessible))


def inspect(campaign, command, *, execution=True):
    """Read-only branch sufficiency, applicability and authorization; never draw."""
    scope = scope_for(campaign, command, execution=execution)
    world, characters = owners(campaign.current)
    r = command.request
    if not characters.knows_route(r.creature, r.route):
        raise Unresolved('access', 'route_not_legitimately_known')
    if campaign.schema == 2 and characters.creature(r.creature).hit_points == 0:
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
        if campaign.schema != 2:
            raise Unresolved('resolution', 'consequence_adjudication_required')
        circumstances = world.failure_inputs(r.creature, r.route)
        expected = 'no_progress' if circumstances.footing == 'load_bearing' else 'loss_of_grip'
        if scope.ruling.failure_mode != expected:
            raise Unresolved('rules', 'unsupported_failure_classification')
        if (not natural(scope.ruling.failure_movement_cost)
                or scope.ruling.failure_movement_cost > assessment.movement_cost):
            raise Unresolved('rules', 'failure_expenditure_unestablished')
        if circumstances.footing == 'grip_dependent':
            if circumstances.id not in scope.authorization.answered_choices and execution:
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
    if campaign.schema == 1:
        if damage_rolls:
            raise ValueError('unexpected damage rolls')
        return None
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


def prepare(campaign, command, *, execution=True, draw=None):
    scope, world, characters, assessment, circumstances = inspect(campaign, command, execution=execution)
    if not execution:
        # Caller must use inspect for inquiries. No random result exists yet.
        raise ValueError('read-only assessment has no execution proposal')
    result = TraversalResolution(lambda: world, lambda: characters).resolve(assessment, draw)
    damage_rolls = ()
    if not result.success:
        _, _, fall = world.failed_climb(command.request, circumstances)
        if fall is not None:
            damage_rolls = tuple(die(draw, 6) for _ in range(min(20, fall.distance_feet // 10)))
    consequence = consequence_for(campaign, command, result, circumstances, damage_rolls)
    args = (command, result, scope.duration_seconds)
    receipt = safe_receipt(*args) if campaign.schema == 1 else safe_receipt(*args, consequence)
    return Proposal(campaign, AcceptedUnit(*args, receipt, consequence))


def validate_unit(campaign, unit):
    """Recompute from historical owners and dice evidence, without sampling."""
    scope, world, characters, assessment, circumstances = inspect(campaign, unit.command)
    expected_result = climb_result(assessment, unit.result.rolls)
    rolls = unit.consequence.injury.rolls if (type(unit.consequence) is TraversalConsequence
                                             and type(unit.consequence.injury) is FallResult) else ()
    expected_consequence = consequence_for(campaign, unit.command, expected_result, circumstances, rolls)
    if (unit.result != expected_result or unit.duration_seconds != scope.duration_seconds
            or unit.consequence != expected_consequence):
        raise Unresolved('validation', 'unit_meaning_mismatch')
    validate_receipt(unit)


def apply_unit(campaign, unit):
    """Pure owner validation and composition. Never publish or sample randomness."""
    if type(unit) is not AcceptedUnit or prior(campaign, unit.command) is not None:
        raise ValueError('unique consequential unit required')
    validate_unit(campaign, unit)
    state = campaign.current
    r, result = unit.command.request, unit.result
    frame = state.world
    revision = campaign.revision + 1
    consequence = unit.consequence
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
        at_seconds=frame.at_seconds + unit.duration_seconds,
        falls=falls, relationships=relationships,
        positions=tuple((actor, position if actor == r.creature else place)
                        for actor, place in frame.positions),
        history=frame.history + (CausalRecord(f'{campaign.id}:accepted:{revision}',
            frame.at_seconds + unit.duration_seconds, (r.creature, r.route), r.attempt),))
    characters = tuple(replace(creature, movement_spent=c.movement_spent + movement_charge(result))
                       if c.id == r.creature else c for c in state.characters)
    current = Domains(world, f'{campaign.id}:character:{revision}', characters)
    validate_domains(current)
    return replace(campaign, current=current, accepted=campaign.accepted + (unit,), revision=revision)


def validate_campaign(campaign):
    """Validate the complete supported aggregate, including accepted causal meaning."""
    from engine.domain_persistence import pack, unpack
    # Exact recursive field typing also protects live construction from bool/int
    # equality and mutable values smuggled into nominally frozen records.
    unpack(pack(campaign))
    if (type(campaign) is not Campaign or not reference(campaign.id)
            or not reference(campaign.actor) or type(campaign.schema) is not int or campaign.schema not in {1, 2}
            or not natural(campaign.revision) or type(campaign.activities) is not tuple
            or type(campaign.accepted) is not tuple):
        raise ValueError('domain campaign envelope')
    if campaign.schema == 1:
        if (any(d.world.climb_circumstances or any(c.vitality is not None for c in d.characters)
                for d in (campaign.origin, campaign.current))
                or any(a.ruling.failure_mode is not None or a.ruling.failure_movement_cost is not None
                       for a in campaign.activities)
                or any(u.consequence is not None for u in campaign.accepted)):
            raise ValueError('new consequence semantics require domain schema 2')
    validate_domains(campaign.origin)
    validate_domains(campaign.current)
    if campaign.actor not in campaign.origin.world.creatures:
        raise ValueError('controlling actor reference')
    ids = []
    for a in campaign.activities:
        if (type(a) is not ActivityScope or not reference(a.id)
                or a.actor not in campaign.origin.world.creatures
                or a.target not in {l.id for l in campaign.origin.world.links}
                or type(a.authorization) is not ActivityAuthorization
                or type(a.checkpoint) is not ActivityCheckpoint
                or (a.authorization.purpose, a.checkpoint.purpose) != (a.id, a.id)
                or a.authorization.method != a.checkpoint.method
                or not natural(a.duration_seconds) or not a.duration_seconds
                or not reference(a.time_basis) or type(a.ruling) is not ClimbRuling
                or type(a.ruling.require_check) is not bool or not reference(a.ruling.basis)
                or a.ruling.failure_mode not in {None, 'no_progress', 'loss_of_grip'}
                or a.ruling.failure_movement_cost is not None and not natural(a.ruling.failure_movement_cost)):
            raise ValueError('activity ownership, timing and references')
        decide_activity_control(a.authorization, a.checkpoint)
        validate_resolution_reference(a.checkpoint)
        ids.append(a.id)
    if len(set(ids)) != len(ids):
        raise ValueError('activity identity')
    rebuilt = replace(campaign, current=campaign.origin, accepted=(), revision=0)
    for unit in campaign.accepted:
        rebuilt = apply_unit(rebuilt, unit)
    if rebuilt != campaign:
        raise ValueError('incoherent accepted aggregate')
    return campaign


def accept(runtime, proposal):
    """One root publication in the existing consequential Runtime, no second store."""
    if runtime.running:
        raise Unresolved('acceptance', 'reentrant')
    runtime.running = True
    try:
        if type(proposal) is not Proposal:
            raise ValueError('explicit proposal')
        from engine.domain_persistence import pack, unpack
        unpack(pack(proposal.unit))
        root = runtime.campaign
        old = prior(root, proposal.unit.command)
        if old is not None:
            if proposal.unit != old:
                raise Unresolved('acceptance', 'identity_conflict')
            return old.receipt
        if root is not proposal.base:
            raise Unresolved('acceptance', 'stale_premises')
        candidate = apply_unit(root, proposal.unit)
        validate_campaign(candidate)
        receipt = proposal.unit.receipt
        if runtime.campaign is not root:
            raise Unresolved('acceptance', 'stale_premises')
        runtime.campaign = candidate
        return receipt
    finally:
        runtime.running = False


def restore_into(runtime, candidate):
    if runtime.running:
        raise Unresolved('persistence', 'reentrant')
    root = runtime.campaign
    validate_campaign(candidate)
    if runtime.campaign is not root:
        raise Unresolved('persistence', 'stale_premises')
    runtime.campaign = candidate
