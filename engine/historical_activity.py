"""Bounded activity continuity over owner facts in the common campaign root.

No scheduler, rules resolver, live root or narration authority lives here. Update
records are trusted upstream owner contributions, not player/provider proposals.
"""
from dataclasses import dataclass, replace

from engine.activity_control import ActivityCheckpoint, decide_activity_control
from engine.character_rules import CreatureRules
from engine.information_adjudication import Unresolved
from engine.physical_world import Surface, TraversalLink, PhysicalObject, PhysicalRelation, ClimbCircumstances, CausalRecord, natural, reference
from engine.traversal_resolution import ClimbRuling, ClimbRequest


@dataclass(frozen=True)
class ActivityStage:
    route: str
    duration_seconds: int
    time_basis: str
    ruling: ClimbRuling


@dataclass(frozen=True)
class ActivityRun:
    id: str
    activity: str
    means: tuple[str, ...] = ()
    use_climb_speed: bool = False


@dataclass(frozen=True)
class ChoiceContext:
    key: str
    source: str  # this activity's original scope or the first offering update
    stages: tuple[int, ...]  # existing stage occurrences, never implicit expansion


@dataclass(frozen=True)
class ActivityUpdate:
    id: str
    activity: str
    basis: str
    surfaces: tuple[Surface, ...] = ()
    links: tuple[TraversalLink, ...] = ()
    objects: tuple[PhysicalObject, ...] = ()
    relationships: tuple[PhysicalRelation, ...] | None = None
    circumstances: tuple[ClimbCircumstances, ...] = ()
    characters: tuple[CreatureRules, ...] = ()
    checkpoint: ActivityCheckpoint | None = None
    elapsed_seconds: int = 0
    ruling: ClimbRuling | None = None
    notices: tuple[tuple[str, str], ...] = ()
    choice_contexts: tuple[ChoiceContext, ...] = ()


@dataclass(frozen=True)
class ActivityResponse:
    id: str
    activity: str
    choices: tuple[str, ...]
    at_revision: int


@dataclass(frozen=True)
class ActivityOutcome:
    status: str
    message: str
    receipts: tuple = ()


def stages(scope):
    return (ActivityStage(scope.target, scope.duration_seconds, scope.time_basis, scope.ruling),) + scope.continuations


def successful_units(campaign, activity):
    from engine.historical_campaign import AcceptedUnit
    return tuple(u for u in campaign.accepted if type(u) is AcceptedUnit
                 and u.command.activity == activity and u.result.success)


def effective_scope(campaign, activity):
    scope = next((a for a in campaign.activities if a.id == activity), None)
    if scope is None:
        raise Unresolved('authorization', 'activity_scope')
    if campaign.schema != 3:
        return scope
    checkpoint, authorization, notices = scope.checkpoint, scope.authorization, scope.notices
    contexts = scope.choice_contexts
    stage_index, rulings = 0, {}
    from engine.historical_campaign import AcceptedUnit
    for event in campaign.accepted:
        if type(event) is AcceptedUnit and event.command.activity == activity and event.result.success:
            stage_index += 1
        if type(event) is ActivityUpdate and event.activity == activity and event.ruling is not None:
            rulings[stage_index] = event.ruling
        if type(event) is ActivityUpdate and event.activity == activity and event.checkpoint is not None:
            checkpoint, notices, contexts = event.checkpoint, event.notices, event.choice_contexts
            # Stable choice meaning is validated before acceptance. Retain prior
            # answers to that same decision even when its checkpoint is replaced.
        elif type(event) is ActivityResponse and event.activity == activity:
            authorization = replace(authorization, answered_choices=tuple(dict.fromkeys(
                authorization.answered_choices + event.choices)))
    index = len(successful_units(campaign, activity))
    plan = stages(scope)
    stage = plan[min(index, len(plan) - 1)]
    active = {c.key for c in contexts if index < len(plan) and index in c.stages}
    context_keys = {c.key for c in contexts}
    checkpoint = replace(checkpoint, developments=tuple(d for d in checkpoint.developments
        if d.choice_key not in context_keys or d.choice_key in active))
    notices = tuple(n for n in notices if n[0] in active)
    contexts = tuple(c for c in contexts if c.key in active)
    # Original context-bound answers expire outside that declared scope too.
    # Only legacy-style original mechanical risk answers keep their old scope.
    original_context_keys = {c.key for c in scope.choice_contexts}
    current_keys = (set(scope.authorization.answered_choices) - original_context_keys) | {
        d.choice_key for d in checkpoint.developments if d.choice_key is not None}
    authorization = replace(authorization, answered_choices=tuple(
        key for key in authorization.answered_choices if key in current_keys))
    return replace(scope, target=stage.route, duration_seconds=stage.duration_seconds,
                   time_basis=stage.time_basis, ruling=rulings.get(index, stage.ruling), authorization=authorization,
                   notices=notices, choice_contexts=contexts,
                   checkpoint=replace(checkpoint, complete=checkpoint.complete or index == len(plan)))



def validate_run(run):
    if (type(run) is not ActivityRun or not all(type(v) is str and reference(v) for v in (run.id, run.activity))
            or type(run.means) is not tuple or not all(type(m) is str and reference(m) for m in run.means)
            or len(set(run.means)) != len(run.means) or type(run.use_climb_speed) is not bool):
        raise ValueError('typed activity run required')


def validate_notices(checkpoint, notices):
    """Only legitimate perceptible choice projections may cross this interface.

    Text is supplied by the trusted joint World/Character access owner, like the
    common Coordinator's accessible context; it is never model-generated truth.
    """
    visible = tuple(d for d in checkpoint.developments if d.perceived and d.opportunity_to_respond
                    and (d.kind == 'player_choice' or d.kind == 'increased_discovery_risk'
                         and d.potentially_objectionable))
    keys = tuple(d.choice_key for d in checkpoint.developments if d.choice_key is not None)
    if (any(type(d.choice_key) is not str or not reference(d.choice_key) for d in visible)
            or len(set(keys)) != len(keys)):
        raise ValueError('recognizable decisions need unique response-addressable identities')
    visible_keys = {d.choice_key for d in visible}
    if (type(notices) is not tuple or any(type(n) is not tuple or len(n) != 2
            or not all(type(v) is str and reference(v) for v in n) or n[0] not in visible_keys for n in notices)
            or len(dict(notices)) != len(notices) or set(dict(notices)) != visible_keys):
        raise ValueError('each recognizable decision needs its legitimate accessible notice')


def validate_choice_history(campaign, addition=None):
    """Reconstruct decision occurrences and their scoped risk/stakes, without rolls.

    Context is internal owner authority, independent of presentation wording.
    No current revision, elapsed time, unrelated owner fact or access flag is a
    decision identity. An occurrence may explicitly span established stages.
    """
    from engine.historical_campaign import AcceptedUnit
    scopes = {a.id: a for a in campaign.activities}
    plans = {a.id: stages(a) for a in campaign.activities}
    indices = {a.id: 0 for a in campaign.activities}
    risks = {x.route: x for x in campaign.origin.world.climb_circumstances}
    rulings = {}
    preauthorized = {(a.id, key) for a in campaign.activities for key in a.authorization.answered_choices}
    meanings, active = {}, {}

    def signature(activity, context):
        # Bind exact failure circumstances and rule stakes for this decision's
        # declared stage occurrences. Do not couple it to the entire mutable World root.
        return tuple((i, stage.route, risks.get(stage.route),
            (r.require_check, r.failure_mode, r.failure_movement_cost))
            for i, stage in enumerate(plans[activity]) if i in context.stages
            for r in (rulings.get((activity, i), stage.ruling),))

    def remaining(activity, facts):
        return tuple(fact for fact in facts if fact[0] >= indices[activity])

    def observe(activity, checkpoint, notices, contexts, source, *, initial=False):
        validate_notices(checkpoint, notices)
        needed = {d.choice_key for d in checkpoint.developments
                  if d.kind != 'ordinary' and d.choice_key is not None}
        if (type(contexts) is not tuple or any(type(c) is not ChoiceContext for c in contexts)
                or len({c.key for c in contexts}) != len(contexts)
                or {c.key for c in contexts} != needed):
            raise ValueError('each keyed decision needs its authoritative context')
        by_key = {c.key: c for c in contexts}
        for c in contexts:
            if (not all(type(v) is str and reference(v) for v in (c.key, c.source))
                    or type(c.stages) is not tuple or not c.stages
                    or not all(natural(v) and v < len(plans[activity]) for v in c.stages)
                    or len(set(c.stages)) != len(c.stages)
                    or indices[activity] not in c.stages):
                raise ValueError('decision context must cover the current established stage')
        text = dict(notices)
        for development in checkpoint.developments:
            key = development.choice_key
            if key is None:
                continue
            identity = (activity, key)
            classification = (scopes[activity].authorization.method,
                              development.kind, development.potentially_objectionable)
            context = by_key.get(key)
            facts = signature(activity, context) if context is not None else None
            notice = text.get(key)
            old = meanings.get(identity)
            if context is not None and old is None and context.source != source:
                raise ValueError('decision context must name its actual establishing occurrence')
            if (not initial and identity in preauthorized
                    and (old is None or old[1] is None and notice is not None)):
                raise ValueError('original answer cannot authorize newly introduced choice meaning')
            if old is not None:
                if ((old[0], old[2]) != (classification, context)
                        or context is not None and remaining(activity, old[3]) != remaining(activity, facts)
                        or old[1] is not None and notice is not None and old[1] != notice):
                    raise ValueError('choice identity must retain its authoritative context')
                notice = old[1] if notice is None else notice
                facts = old[3]
            meanings[identity] = (classification, notice, context, facts)
        active[activity] = contexts

    def check_active():
        for activity, contexts in active.items():
            index = indices[activity]
            for context in contexts:
                if any(stage >= index for stage in context.stages):
                    if remaining(activity, meanings[(activity, context.key)][3]) != remaining(activity, signature(activity, context)):
                        raise ValueError('changed decision risk/stakes require a fresh choice identity')

    for activity in campaign.activities:
        context_keys = {c.key for c in activity.choice_contexts}
        original_risks = {x.id for x in campaign.origin.world.climb_circumstances
                          if x.route in {stage.route for stage in plans[activity.id]}}
        if not set(activity.authorization.answered_choices).issubset(context_keys | original_risks):
            raise ValueError('original answers require an established decision or original mechanical risk')
        observe(activity.id, activity.checkpoint, activity.notices, activity.choice_contexts,
                activity.id, initial=True)
    for event in campaign.accepted + (() if addition is None else (addition,)):
        if type(event) is AcceptedUnit and event.result.success:
            indices[event.command.activity] += 1
        elif type(event) is ActivityUpdate:
            risks.update((x.route, x) for x in event.circumstances)
            if event.ruling is not None:
                rulings[(event.activity, indices[event.activity])] = event.ruling
            if event.checkpoint is not None:
                observe(event.activity, event.checkpoint, event.notices, event.choice_contexts, event.id)
        check_active()


def replace_named(current, changes, cls, key='id'):
    if type(changes) is not tuple or any(type(x) is not cls for x in changes):
        raise ValueError('typed owner facts required')
    supplied = {getattr(x, key): x for x in changes}
    existing = {getattr(x, key): x for x in current}
    if len(supplied) != len(changes) or not set(supplied).issubset(existing):
        raise ValueError('existing owner identity required')
    return tuple(supplied.get(getattr(x, key), x) for x in current)


def apply_update(campaign, event):
    """Validate fact/control contributions without resolving a gameplay answer."""
    from engine.historical_campaign import validate_domains, validate_resolution_reference
    if campaign.schema != 3 or type(event) not in (ActivityUpdate, ActivityResponse):
        raise ValueError('continuity requires domain schema 3')
    if not all(type(v) is str and reference(v) for v in (event.id, event.activity)):
        raise ValueError('activity event identity')
    scope = effective_scope(campaign, event.activity)
    current = campaign.current
    revision = campaign.revision + 1
    world = current.world
    if type(event) is ActivityResponse:
        if (not natural(event.at_revision) or event.at_revision != campaign.revision
                or type(event.choices) is not tuple or not event.choices
                or len(set(event.choices)) != len(event.choices)
                or not all(type(c) is str and reference(c) for c in event.choices)):
            raise ValueError('situated response required')
        validate_notices(scope.checkpoint, scope.notices)
        available = set(dict(scope.notices))
        if (not set(event.choices).issubset(available)
                or set(event.choices).intersection(scope.authorization.answered_choices)):
            raise ValueError('response must answer a current recognizable choice')
    else:
        if not reference(event.basis) or not natural(event.elapsed_seconds):
            raise ValueError('owner development basis/time')
        if event.ruling is not None:
            r = event.ruling
            if (type(r) is not ClimbRuling or type(r.require_check) is not bool or not reference(r.basis)
                    or r.failure_mode not in {None, 'no_progress', 'loss_of_grip'}
                    or r.failure_movement_cost is not None and not natural(r.failure_movement_cost)):
                raise ValueError('current contextual ruling required')
        if event.checkpoint is not None:
            cp = event.checkpoint
            if (type(cp) is not ActivityCheckpoint or (cp.purpose, cp.method) !=
                    (scope.id, scope.authorization.method) or cp.complete or cp.restart_required):
                raise ValueError('development cannot rewrite objective or accepted completion')
            decide_activity_control(scope.authorization, cp)
            validate_resolution_reference(cp)
        elif event.notices or event.choice_contexts:
            raise ValueError('notices and contexts must accompany their situated checkpoint')
        # Changing the exact established risk requires a fresh risk identity.
        old_risks = {x.route: x for x in world.climb_circumstances}
        historical_risks = {x.id: x for x in campaign.origin.world.climb_circumstances}
        for accepted in campaign.accepted:
            if type(accepted) is ActivityUpdate:
                historical_risks.update((x.id, x) for x in accepted.circumstances)
        for x in event.circumstances:
            if x.id in historical_risks and historical_risks[x.id] != x:
                raise ValueError('risk identity must retain historical meaning')
            old = old_risks.get(x.route)
            if old is not None and x != old and x.id == old.id:
                raise ValueError('changed risk requires a fresh identity')
        risks = dict(old_risks)
        if len({x.route for x in event.circumstances}) != len(event.circumstances):
            raise ValueError('unique risk contribution')
        risks.update((x.route, x) for x in event.circumstances)
        links = replace_named(world.links, event.links, TraversalLink)
        for before, after in zip(world.links, links):
            if (before.origin, before.destination) != (after.origin, after.destination):
                raise ValueError('a development cannot replace the chosen route endpoints')
        world = replace(world,
            surfaces=replace_named(world.surfaces, event.surfaces, Surface), links=links,
            objects=replace_named(world.objects, event.objects, PhysicalObject),
            relationships=world.relationships if event.relationships is None else event.relationships,
            climb_circumstances=tuple(risks.values()), at_seconds=world.at_seconds + event.elapsed_seconds)
        characters = replace_named(current.characters, event.characters, CreatureRules)
        # Supplier facts may change capacity/readiness/conditions/access. Accepted
        # costs, HP and vitality are consequences, not fixture-supplied answers.
        for before, after in zip(current.characters, characters):
            if (before.movement_spent, before.hit_points, before.vitality) != (
                    after.movement_spent, after.hit_points, after.vitality):
                raise ValueError('development cannot overwrite accepted character consequences')
        current = replace(current, world=world, characters=characters)
    cause_id = f'{campaign.id}:accepted:{revision}'
    from engine.physical_world import WorldPhysics
    WorldPhysics(world).require_new_identities((cause_id,))
    world = replace(world, revision=f'{campaign.id}:world:{revision}',
        history=world.history + (CausalRecord(cause_id, world.at_seconds, (scope.actor,), event.id),))
    current = replace(current, world=world, character_revision=f'{campaign.id}:character:{revision}')
    validate_domains(current)
    validate_choice_history(campaign, event)
    return replace(campaign, current=current, accepted=campaign.accepted + (event,), revision=revision)


def advance(runtime, run, refresh=None):
    """Execute ordinary permitted increments; stop at a real control boundary.

    refresh is a missing-upstream-supplier seam returning an inert ActivityUpdate
    before the next increment. It never returns rolls, outcomes or player answers.
    Accepted updates survive save/load; the callable is never persisted.
    """
    from engine.historical_campaign import Increment, AcceptedUnit
    validate_run(run)
    if not runtime.domain_mode or runtime.campaign.schema != 3:
        raise ValueError('explicit continuity campaign required')
    history = [u for u in runtime.campaign.accepted if type(u) is AcceptedUnit
               and u.command.run is not None and u.command.run.id == run.id]
    if any(u.command.run != run for u in history):
        raise Unresolved('acceptance', 'identity_conflict')
    receipts = [u.receipt for u in history]

    def outcome(status, message):
        accepted = [dict(r.accessible)['movement'] for r in receipts]
        return ActivityOutcome(status, ' '.join(accepted + [message]), tuple(receipts))
    if history and not history[-1].result.success:
        return outcome('failed', 'The recorded attempt did not complete the activity.')
    while True:
        root = runtime.campaign
        scope = effective_scope(root, run.activity)
        control = decide_activity_control(scope.authorization, scope.checkpoint)
        if control.status == 'complete':
            return outcome('complete', 'The authorized activity is complete.')
        if refresh is not None:
            event = refresh(root, scope)
            if runtime.campaign is not root:
                raise Unresolved('acceptance', 'stale_premises')
            if event is not None:
                if type(event) is not ActivityUpdate or event.activity != run.activity:
                    raise ValueError('upstream suppliers contribute facts, not decisions')
                runtime.accept_increment(runtime.prepare_activity_change(event))
                root = runtime.campaign
                scope = effective_scope(root, run.activity)
                control = decide_activity_control(scope.authorization, scope.checkpoint)
        if control.status != 'continue':
            visible = [text for key, text in scope.notices if key not in scope.authorization.answered_choices]
            return outcome('control', ' '.join(visible + ['The activity cannot continue as authorized.']))
        index = len(successful_units(root, run.activity))
        link = next(l for l in root.current.world.links if l.id == scope.target)
        command = Increment(run.activity, ClimbRequest(f'{run.id}:stage:{index}', scope.actor,
            scope.target, link.distance_feet, run.use_climb_speed, run.means), run)
        decision = runtime.process_increment(command)
        if decision.status != 'accepted':
            # Never turn missing material information or technical rejection into
            # a fictional setback. Eligibility failures are player control.
            return outcome('control' if decision.status == 'clarification' else 'unresolved', decision.message)
        unit = next(u for u in runtime.campaign.accepted if type(u) is AcceptedUnit
                    and u.command.request.attempt == command.request.attempt)
        receipts.append(unit.receipt)
        if not unit.result.success:
            return outcome('failed', 'The attempt did not complete the activity.')
