"""Schema-4 coherent acceptance. Domains own mechanics and safe projections.

Historical schemas are evaluated by their frozen contract; publication is shared.
No handler, callable or executable object is stored in a campaign.
"""
from dataclasses import dataclass, replace

from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, decide_activity_control
from engine.domain_state import Domains, validate_domains
from engine.domain_owners import domain_owner
from engine.gameplay_coordination import AcceptedStep
from engine.information_adjudication import Unresolved
from engine.physical_world import natural, reference


@dataclass(frozen=True)
class ActivityStage:
    target: str
    payload: tuple


@dataclass(frozen=True)
class ChoiceContext:
    key: str
    source: str
    stages: tuple[int, ...]


@dataclass(frozen=True)
class ActivityScope:
    id: str
    actor: str
    domain: str
    objective: str
    authorization: ActivityAuthorization
    checkpoint: ActivityCheckpoint
    stages: tuple[ActivityStage, ...]
    supported_constraints: tuple[str, ...] = ()
    notices: tuple[tuple[str, str], ...] = ()
    choice_contexts: tuple[ChoiceContext, ...] = ()
    index: int = 0

    @property
    def target(self):
        return self.stages[min(self.index, len(self.stages) - 1)].target

    @property
    def payload(self):
        return self.stages[min(self.index, len(self.stages) - 1)].payload


@dataclass(frozen=True)
class ActivityRun:
    id: str
    activity: str
    payload: tuple = ()


@dataclass(frozen=True)
class Increment:
    id: str
    activity: str
    stage: int
    payload: tuple = ()
    run: ActivityRun | None = None


@dataclass(frozen=True)
class AcceptedUnit:
    command: Increment
    evidence: tuple
    progressed: bool
    receipt: AcceptedStep


@dataclass(frozen=True)
class ActivityUpdate:
    id: str
    activity: str
    basis: str
    payload: tuple = ()
    stage: ActivityStage | None = None
    checkpoint: ActivityCheckpoint | None = None
    notices: tuple[tuple[str, str], ...] = ()
    choice_contexts: tuple[ChoiceContext, ...] = ()


@dataclass(frozen=True)
class ActivityResponse:
    id: str
    activity: str
    choices: tuple[str, ...]
    at_revision: int


@dataclass(frozen=True)
class Campaign:
    id: str
    actor: str
    origin: Domains
    current: Domains
    activities: tuple[ActivityScope, ...]
    accepted: tuple[AcceptedUnit | ActivityUpdate | ActivityResponse, ...] = ()
    revision: int = 0
    schema: int = 4


@dataclass(frozen=True)
class Proposal:
    base: Campaign
    unit: AcceptedUnit | ActivityUpdate | ActivityResponse


@dataclass(frozen=True)
class Contribution:
    current: Domains
    evidence: tuple
    progressed: bool
    receipt: AcceptedStep


def model(campaign):
    """Version selection, never method or mechanical interpretation."""
    from engine import historical_campaign
    if type(campaign) is historical_campaign.Campaign:
        return historical_campaign
    if type(campaign) is not Campaign:
        raise ValueError('explicit campaign required')
    import sys
    return sys.modules[__name__]


def typed(value):
    from engine.domain_persistence import pack, unpack
    unpack(pack(value), schema=4)


def identity(unit):
    return unit.command.id if type(unit) is AcceptedUnit else unit.id


def receipt_message(receipt):
    return ' '.join(text for _, text in receipt.accessible)


def validate_increment(command):
    typed(command)
    if (type(command) is not Increment or not all(reference(v) for v in (command.id, command.activity))
            or not natural(command.stage)):
        raise ValueError('explicit increment identity and stage required')
    if command.run is not None:
        from engine.domain_activity import validate_run
        validate_run(command.run)
        if (command.run.activity != command.activity or command.run.payload != command.payload
                or command.id != f'{command.run.id}:stage:{command.stage}'):
            raise ValueError('run and increment association')


def prior(campaign, command):
    validate_increment(command)
    old = next((u for u in campaign.accepted if identity(u) == command.id), None)
    if old is not None and (type(old) is not AcceptedUnit or old.command != command):
        raise Unresolved('acceptance', 'identity_conflict')
    return old


def event_prior(campaign, event):
    if type(event) not in (ActivityUpdate, ActivityResponse) or not reference(event.id):
        raise ValueError('typed activity change required')
    old = next((u for u in campaign.accepted if identity(u) == event.id), None)
    if old is not None and old != event:
        raise Unresolved('acceptance', 'identity_conflict')
    return old


def scope_for(campaign, command, *, execution=True, handlers=()):
    from engine.domain_activity import effective_scope
    validate_increment(command)
    scope = effective_scope(campaign, command.activity)
    if scope.actor != campaign.actor or command.stage != scope.index:
        raise Unresolved('authorization', 'activity_scope')
    if not set(scope.authorization.constraints).issubset(scope.supported_constraints):
        raise Unresolved('authorization', 'unsupported_constraints')
    if command.run is not None and any(type(u) is AcceptedUnit and u.command.run is not None
            and u.command.run.id == command.run.id and u.command.run != command.run for u in campaign.accepted):
        raise Unresolved('acceptance', 'identity_conflict')
    if execution and decide_activity_control(scope.authorization, scope.checkpoint).status != 'continue':
        raise Unresolved('authorization', 'return_control')
    domain_owner(scope, handlers).validate_command(campaign, command, scope)
    return scope


def prepare(campaign, command, *, execution=True, draw=None, handlers=()):
    scope = scope_for(campaign, command, execution=execution, handlers=handlers)
    if not execution:
        raise ValueError('assessment has no execution proposal')
    owner = domain_owner(scope, handlers)
    owner.assess(campaign, command, scope, execution=True)
    contribution = owner.prepare(campaign, command, scope, draw)
    unit = AcceptedUnit(command, contribution.evidence, contribution.progressed, contribution.receipt)
    return Proposal(campaign, unit)


def apply_unit(campaign, unit, *, handlers=()):
    from engine.domain_activity import apply_update
    if type(unit) in (ActivityUpdate, ActivityResponse):
        if event_prior(campaign, unit) is not None:
            raise ValueError('unique activity change required')
        return apply_update(campaign, unit, handlers=handlers)
    if type(unit) is not AcceptedUnit or prior(campaign, unit.command) is not None:
        raise ValueError('unique consequential unit required')
    typed(unit)
    scope = scope_for(campaign, unit.command, handlers=handlers)
    contribution = domain_owner(scope, handlers).evaluate(campaign, unit.command, scope, unit.evidence)
    expected = AcceptedUnit(unit.command, contribution.evidence, contribution.progressed, contribution.receipt)
    if type(contribution) is not Contribution or unit != expected:
        raise Unresolved('validation', 'unit_meaning_mismatch')
    if unit.receipt.ref != unit.command.id or unit.receipt.outcome != 'complete':
        raise ValueError('accepted receipt identity')
    from engine.gameplay_coordination import SituatedContext, validate_context, _refs
    validate_context(SituatedContext('receipt', 'receipt', accessible=unit.receipt.accessible))
    if (not unit.receipt.public_refs or not _refs(unit.receipt.public_refs)
            or set(unit.receipt.public_refs) != set(dict(unit.receipt.accessible))):
        raise ValueError('complete safe receipt required')
    validate_domains(contribution.current)
    return replace(campaign, current=contribution.current,
                   accepted=campaign.accepted + (unit,), revision=campaign.revision + 1)


def validate_campaign(campaign, *, handlers=()):
    backend = model(campaign)
    if backend.Campaign is not Campaign:
        return backend.validate_campaign(campaign)
    typed(campaign)
    if (campaign.schema != 4 or not all(reference(v) for v in (campaign.id, campaign.actor))
            or not natural(campaign.revision)):
        raise ValueError('campaign envelope')
    validate_domains(campaign.origin)
    validate_domains(campaign.current)
    if campaign.actor not in campaign.origin.world.creatures:
        raise ValueError('controlling actor reference')
    ids = []
    for a in campaign.activities:
        if (not all(reference(v) for v in (a.id, a.objective, a.domain))
                or a.actor not in campaign.origin.world.creatures or a.index != 0 or not a.stages
                or (a.authorization.purpose, a.checkpoint.purpose) != (a.id, a.id)
                or a.authorization.method != a.checkpoint.method
                or a.checkpoint.resolution_ref is not None
                or len(set(a.supported_constraints)) != len(a.supported_constraints)
                or not all(reference(c) for c in a.supported_constraints)
                or any(not reference(s.target) for s in a.stages)):
            raise ValueError('activity ownership and scope')
        decide_activity_control(a.authorization, a.checkpoint)
        domain_owner(a, handlers).validate_scope(campaign, a)
        ids.append(a.id)
    if len(set(ids)) != len(ids):
        raise ValueError('activity identity')
    rebuilt = replace(campaign, current=campaign.origin, accepted=(), revision=0)
    from engine.domain_activity import validate_choice_history
    for unit in campaign.accepted:
        rebuilt = apply_unit(rebuilt, unit, handlers=handlers)
    validate_choice_history(campaign, handlers=handlers)
    if rebuilt != campaign:
        raise ValueError('incoherent accepted aggregate')
    return campaign


def accept(runtime, proposal):
    """All supported schemas share this publication boundary."""
    if runtime.running:
        raise Unresolved('acceptance', 'reentrant')
    runtime.running = True
    try:
        root = runtime.campaign
        backend = model(root)
        if type(proposal) is not backend.Proposal:
            raise ValueError('explicit proposal')
        if backend.Campaign is Campaign:
            typed(proposal.unit)
        else:
            from engine.historical_persistence import pack, unpack
            unpack(pack(proposal.unit))
        is_result = type(proposal.unit) is backend.AcceptedUnit
        old = backend.prior(root, proposal.unit.command) if is_result else backend.event_prior(root, proposal.unit)
        if old is not None:
            if proposal.unit != old:
                raise Unresolved('acceptance', 'identity_conflict')
            return old.receipt if is_result else None
        if root is not proposal.base:
            raise Unresolved('acceptance', 'stale_premises')
        kwargs = {'handlers': runtime.domain_handlers} if backend.Campaign is Campaign else {}
        candidate = backend.apply_unit(root, proposal.unit, **kwargs)
        validate_campaign(candidate, handlers=runtime.domain_handlers)
        receipt = proposal.unit.receipt if is_result else None
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
    validate_campaign(candidate, handlers=runtime.domain_handlers)
    if runtime.campaign is not root:
        raise Unresolved('persistence', 'stale_premises')
    runtime.campaign = candidate


def prepare_activity_change(campaign, event, *, handlers=()):
    typed(event)
    if event_prior(campaign, event) is None:
        apply_unit(campaign, event, handlers=handlers)
    return Proposal(campaign, event)
