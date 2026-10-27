"""Meaningful activity continuity; mechanical dependencies remain domain-owned."""
from dataclasses import dataclass, replace

from engine.activity_control import ActivityCheckpoint, decide_activity_control
from engine.domain_campaign import (ActivityStage, ActivityRun, ChoiceContext, ActivityUpdate,
    ActivityResponse, AcceptedUnit, Increment, Contribution, domain_owner, receipt_message)
from engine.domain_state import validate_domains
from engine.information_adjudication import Unresolved
from engine.physical_world import CausalRecord, WorldPhysics, natural, reference


@dataclass(frozen=True)
class ActivityOutcome:
    status: str
    message: str
    receipts: tuple = ()


def successful_units(campaign, activity):
    return tuple(u for u in campaign.accepted if type(u) is AcceptedUnit
                 and u.command.activity == activity and u.progressed)


def effective_scope(campaign, activity):
    scope = next((a for a in campaign.activities if a.id == activity), None)
    if scope is None:
        raise Unresolved('authorization', 'activity_scope')
    checkpoint, authorization, notices = scope.checkpoint, scope.authorization, scope.notices
    contexts, plan, index = scope.choice_contexts, list(scope.stages), 0
    for event in campaign.accepted:
        if type(event) is AcceptedUnit and event.command.activity == activity and event.progressed:
            index += 1
        elif type(event) is ActivityUpdate and event.activity == activity:
            if event.stage is not None:
                plan[index] = event.stage
            if event.checkpoint is not None:
                checkpoint, notices, contexts = event.checkpoint, event.notices, event.choice_contexts
        elif type(event) is ActivityResponse and event.activity == activity:
            authorization = replace(authorization, answered_choices=tuple(dict.fromkeys(
                authorization.answered_choices + event.choices)))
    active = {c.key for c in contexts if index < len(plan) and index in c.stages}
    keys = {c.key for c in contexts}
    checkpoint = replace(checkpoint, developments=tuple(d for d in checkpoint.developments
        if d.choice_key not in keys or d.choice_key in active))
    original = {c.key for c in scope.choice_contexts}
    current_keys = (set(scope.authorization.answered_choices) - original) | {
        d.choice_key for d in checkpoint.developments if d.choice_key is not None}
    return replace(scope, stages=tuple(plan), index=index,
        authorization=replace(authorization, answered_choices=tuple(
            key for key in authorization.answered_choices if key in current_keys)),
        notices=tuple(n for n in notices if n[0] in active),
        choice_contexts=tuple(c for c in contexts if c.key in active),
        checkpoint=replace(checkpoint, complete=checkpoint.complete or index == len(plan)))


def validate_run(run):
    from engine.domain_campaign import typed
    typed(run)
    if type(run) is not ActivityRun or not all(reference(v) for v in (run.id, run.activity)):
        raise ValueError('typed activity run required')


def validate_notices(checkpoint, notices):
    visible = tuple(d for d in checkpoint.developments if d.perceived and d.opportunity_to_respond
                    and (d.kind == 'player_choice' or d.kind == 'increased_discovery_risk'
                         and d.potentially_objectionable))
    keys = tuple(d.choice_key for d in checkpoint.developments if d.choice_key is not None)
    if any(not reference(d.choice_key) for d in visible) or len(set(keys)) != len(keys):
        raise ValueError('recognizable decisions need unique identities')
    visible_keys = {d.choice_key for d in visible}
    if (type(notices) is not tuple or any(type(n) is not tuple or len(n) != 2
            or not all(type(v) is str and reference(v) for v in n) or n[0] not in visible_keys for n in notices)
            or len(dict(notices)) != len(notices) or set(dict(notices)) != visible_keys):
        raise ValueError('each recognizable decision needs its legitimate accessible notice')


def stamp(campaign, current, event, scope):
    revision, world = campaign.revision + 1, current.world
    cause_id = f'{campaign.id}:accepted:{revision}'
    WorldPhysics(world).require_new_identities((cause_id,))
    world = replace(world, revision=f'{campaign.id}:world:{revision}',
        history=world.history + (CausalRecord(cause_id, world.at_seconds, (scope.actor,), event.id),))
    return replace(current, world=world, character_revision=f'{campaign.id}:character:{revision}')


def validate_choice_history(campaign, addition=None, *, handlers=()):
    """Bind occurrence/scope plus domain-declared consequential decision premises.

    Domain evidence is compared structurally, never inferred from notice text or
    an unrelated aggregate revision. Reconstruct without random draws.
    """
    probe = replace(campaign, current=campaign.origin, accepted=(), revision=0)
    meanings, active = {}, {}
    preauthorized = {(a.id, k) for a in campaign.activities for k in a.authorization.answered_choices}

    def signature(activity, context):
        scope = effective_scope(probe, activity)
        owner = domain_owner(scope, handlers)
        return tuple((i, scope.stages[i].target, owner.decision_basis(probe, scope, i)) for i in context.stages)

    def remaining(activity, facts):
        return tuple(f for f in facts if f[0] >= effective_scope(probe, activity).index)

    def observe(scope, checkpoint, notices, contexts, source, initial=False):
        validate_notices(checkpoint, notices)
        needed = {d.choice_key for d in checkpoint.developments if d.kind != 'ordinary' and d.choice_key is not None}
        if (type(contexts) is not tuple or any(type(c) is not ChoiceContext for c in contexts)
                or len({c.key for c in contexts}) != len(contexts) or {c.key for c in contexts} != needed):
            raise ValueError('each keyed decision needs its authoritative context')
        by_key, text = {c.key: c for c in contexts}, dict(notices)
        for c in contexts:
            if (not all(reference(v) for v in (c.key, c.source)) or not c.stages
                    or not all(natural(i) and i < len(scope.stages) for i in c.stages)
                    or len(set(c.stages)) != len(c.stages) or scope.index not in c.stages):
                raise ValueError('decision context must cover the current established stage')
        for d in checkpoint.developments:
            key = d.choice_key
            if key is None:
                continue
            identity = (scope.id, key)
            classification = (scope.authorization.method, d.kind, d.potentially_objectionable)
            context, notice = by_key.get(key), text.get(key)
            facts = signature(scope.id, context) if context is not None else None
            old = meanings.get(identity)
            if context is not None and old is None and context.source != source:
                raise ValueError('decision context must name its actual establishing occurrence')
            if not initial and identity in preauthorized and (old is None or old[1] is None and notice is not None):
                raise ValueError('original answer cannot authorize newly introduced choice meaning')
            if old is not None:
                if ((old[0], old[2]) != (classification, context)
                        or context is not None and remaining(scope.id, old[3]) != remaining(scope.id, facts)
                        or old[1] is not None and notice is not None and old[1] != notice):
                    raise ValueError('choice identity must retain its authoritative context')
                notice = old[1] if notice is None else notice
                facts = old[3]
            meanings[identity] = (classification, notice, context, facts)
        active[scope.id] = contexts

    for a in campaign.activities:
        allowed = {c.key for c in a.choice_contexts} | set(domain_owner(a, handlers).initial_choices(probe, a))
        if not set(a.authorization.answered_choices).issubset(allowed):
            raise ValueError('original answers require an established choice meaning')
        observe(a, a.checkpoint, a.notices, a.choice_contexts, a.id, initial=True)
    for event in campaign.accepted + (() if addition is None else (addition,)):
        scope = effective_scope(probe, event.command.activity if type(event) is AcceptedUnit else event.activity)
        owner = domain_owner(scope, handlers)
        if type(event) is AcceptedUnit:
            current = owner.evaluate(probe, event.command, scope, event.evidence).current
        else:
            current = owner.update(probe, event, scope) if type(event) is ActivityUpdate else probe.current
            current = stamp(probe, current, event, scope)
        probe = replace(probe, current=current, accepted=probe.accepted + (event,), revision=probe.revision + 1)
        if type(event) is ActivityUpdate and event.checkpoint is not None:
            observe(effective_scope(probe, event.activity), event.checkpoint, event.notices,
                    event.choice_contexts, event.id)
        for activity, contexts in active.items():
            for context in contexts:
                if remaining(activity, meanings[(activity, context.key)][3]) != remaining(activity, signature(activity, context)):
                    raise ValueError('changed decision stakes require a fresh choice identity')


def apply_update(campaign, event, *, handlers=()):
    if not all(reference(v) for v in (event.id, event.activity)):
        raise ValueError('activity event identity')
    scope = effective_scope(campaign, event.activity)
    current = campaign.current
    if type(event) is ActivityResponse:
        if (not natural(event.at_revision) or event.at_revision != campaign.revision or not event.choices
                or len(set(event.choices)) != len(event.choices)
                or not all(reference(c) for c in event.choices)):
            raise ValueError('situated response required')
        validate_notices(scope.checkpoint, scope.notices)
        if (not set(event.choices).issubset(dict(scope.notices))
                or set(event.choices).intersection(scope.authorization.answered_choices)):
            raise ValueError('response must answer a current recognizable choice')
    else:
        if not reference(event.basis):
            raise ValueError('owner development basis')
        if scope.index >= len(scope.stages):
            raise ValueError('completed activity cannot receive continuation developments')
        if event.stage is not None and event.stage.target != scope.target:
            raise ValueError('a development cannot replace the chosen target')
        if event.checkpoint is not None:
            cp = event.checkpoint
            if ((cp.purpose, cp.method) != (scope.id, scope.authorization.method)
                    or cp.complete or cp.restart_required or cp.resolution_ref is not None):
                raise ValueError('development cannot rewrite objective or completion')
            decide_activity_control(scope.authorization, cp)
        elif event.notices or event.choice_contexts:
            raise ValueError('notices and contexts require their checkpoint')
        owner = domain_owner(scope, handlers)
        current = owner.update(campaign, event, scope)
        if event.stage is not None:
            plan = list(scope.stages)
            plan[scope.index] = event.stage
            owner.validate_scope(campaign, replace(scope, stages=tuple(plan)))
    current = stamp(campaign, current, event, scope)
    validate_domains(current)
    validate_choice_history(campaign, event, handlers=handlers)
    return replace(campaign, current=current, accepted=campaign.accepted + (event,), revision=campaign.revision + 1)


def run_receipts(campaign, run):
    return tuple(u.receipt for u in campaign.accepted if type(u) is AcceptedUnit and u.command.run == run)


def advance(runtime, run, refresh=None):
    validate_run(run)
    if not runtime.domain_mode or runtime.campaign.schema != 4:
        raise ValueError('explicit continuity campaign required')
    history = [u for u in runtime.campaign.accepted if type(u) is AcceptedUnit
               and u.command.run is not None and u.command.run.id == run.id]
    if any(u.command.run != run for u in history):
        raise Unresolved('acceptance', 'identity_conflict')
    receipts = [u.receipt for u in history]

    def outcome(status, message):
        return ActivityOutcome(status, ' '.join([receipt_message(r) for r in receipts] + [message]), tuple(receipts))
    if history and not history[-1].progressed:
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
        command = Increment(f'{run.id}:stage:{scope.index}', run.activity, scope.index, run.payload, run)
        decision = runtime.process_increment(command)
        if decision.status != 'accepted':
            return outcome('control' if decision.status == 'clarification' else 'unresolved', decision.message)
        unit = next(u for u in runtime.campaign.accepted if type(u) is AcceptedUnit and u.command == command)
        receipts.append(unit.receipt)
        if not unit.progressed:
            return outcome('failed', 'The attempt did not complete the activity.')
