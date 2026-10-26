"""Domain-owned aggregate preparation/validation for the common Runtime.

This module owns no live root. Proposals and restored candidates are inert values.
Only Runtime publishes. Unsupported consequence semantics fail before resolution.
"""
from dataclasses import dataclass, replace

from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, decide_activity_control
from engine.character_rules import CharacterRules, CreatureRules
from engine.gameplay_coordination import AcceptedStep, SituatedContext, validate_context
from engine.information_adjudication import Unresolved
from engine.physical_world import PhysicalFrame, WorldPhysics, CausalRecord, natural, reference
from engine.traversal_resolution import (
    ClimbRequest, ClimbRuling, ClimbResult, TraversalResolution, validate_climb_request,
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
class AcceptedUnit:
    command: Increment
    result: ClimbResult
    duration_seconds: int
    receipt: AcceptedStep


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


def movement_meaning(command, result, duration):
    return (f'You climb {command.request.distance_feet} feet to the chosen destination. '
            f'{duration} seconds pass; {result.assessment.movement_cost} feet of movement are spent.')


def safe_receipt(command, result, duration):
    # Self-proprioception, chosen route and accepted costs only. No surface,
    # causal basis, hidden effect or internal failure text enters this projection.
    text = movement_meaning(command, result, duration)
    return AcceptedStep(command.request.attempt, ('movement',), 'complete', (('movement', text),))


def validate_receipt(unit):
    receipt = unit.receipt
    # Independent of the receipt producer: guarantee everything the common
    # coordinator will validate after execution, plus exact supported F01 meaning.
    if (type(receipt) is not AcceptedStep or receipt.ref != unit.command.request.attempt
            or receipt.public_refs != ('movement',) or receipt.outcome != 'complete'
            or receipt.accessible != (('movement', movement_meaning(
                unit.command, unit.result, unit.duration_seconds)),)):
        raise Unresolved('receipt', 'invalid_safe_receipt')
    validate_context(SituatedContext('receipt', 'receipt', accessible=unit.receipt.accessible))


def prepare(campaign, command, *, execution=True):
    scope = scope_for(campaign, command, execution=execution)
    world, characters = owners(campaign.current)
    r = command.request
    if not characters.knows_route(r.creature, r.route):
        raise Unresolved('access', 'route_not_legitimately_known')
    resolution = TraversalResolution(lambda: world, lambda: characters)
    assessment = resolution.assess(r, scope.ruling)
    if scope.ruling.require_check:
        raise Unresolved('resolution', 'consequence_adjudication_required')
    if r.distance_feet != assessment.dependencies.link.distance_feet:
        raise Unresolved('resolution', 'established_endpoint_required')
    result = resolution.resolve(assessment, lambda sides: (_ for _ in ()).throw(
        AssertionError('deterministic movement must not draw')))
    return Proposal(campaign, AcceptedUnit(command, result, scope.duration_seconds,
                    safe_receipt(command, result, scope.duration_seconds)))


def apply_unit(campaign, unit):
    """Pure owner validation and composition. Never publish or sample randomness."""
    if type(unit) is not AcceptedUnit or prior(campaign, unit.command) is not None:
        raise ValueError('unique consequential unit required')
    expected = prepare(campaign, unit.command).unit
    if unit != expected:
        raise Unresolved('validation', 'unit_meaning_mismatch')
    validate_receipt(unit)
    state = campaign.current
    r, result = unit.command.request, unit.result
    frame = state.world
    revision = campaign.revision + 1
    # World validates the new position/time/cause; Character validates expenditure.
    world = replace(frame, revision=f'{campaign.id}:world:{revision}',
        at_seconds=frame.at_seconds + unit.duration_seconds,
        positions=tuple((actor, result.destination if actor == r.creature else place)
                        for actor, place in frame.positions),
        history=frame.history + (CausalRecord(f'{campaign.id}:accepted:{revision}',
            frame.at_seconds + unit.duration_seconds, (r.creature, r.route), r.attempt),))
    characters = tuple(replace(c, movement_spent=c.movement_spent + result.assessment.movement_cost)
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
            or not reference(campaign.actor) or type(campaign.schema) is not int or campaign.schema != 1
            or not natural(campaign.revision) or type(campaign.activities) is not tuple
            or type(campaign.accepted) is not tuple):
        raise ValueError('domain campaign envelope')
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
                or type(a.ruling.require_check) is not bool or not reference(a.ruling.basis)):
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
    validate_campaign(candidate)
    runtime.campaign = candidate
