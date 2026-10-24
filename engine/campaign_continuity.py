"""I3 owner-state validation and preparation for the existing consequential runtime.

No alternate adjudicator, scheduler, provider or command parser. All effects still
pass Runtime.accept; these functions prepare/validate its complete campaign root.
"""
from copy import deepcopy
from dataclasses import dataclass, replace
from hashlib import sha256
import json
from uuid import uuid4

from engine.campaign_records import (
    Activity, Blueprint, Boundary, CampaignData, Inputs, WaitingIntent, pack, unpack,
)
from engine.consequence_integration import Config, Runtime, State, InformationView
from engine.information_adjudication import SessionState, Unresolved
from engine.information_resolution import InformationSnapshot, Period, Query
from engine.scene_loader import build_scene
from engine.world_state import add_history_entry, validate_world_state


@dataclass(frozen=True)
class Root:
    data: CampaignData
    world: dict
    scene: dict


def hours_to_seconds(hours):
    if type(hours) is not int or hours < 0:
        raise ValueError("Explicit nonnegative authored hours required")
    return hours * 3600


def snapshot(inputs):
    if type(inputs) is not Inputs:
        raise ValueError("Explicit declarative information required")
    return InformationSnapshot(inputs.foundations, identities=inputs.identities,
        current=inputs.current, history=inputs.history, relationships=inputs.relationships,
        constraints=inputs.constraints)


def content_digest(region):
    # Public authored content only. Never inspect/hash player data or credentials.
    return sha256(json.dumps(region, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def combined(inputs, state):
    return InformationSnapshot(inputs.foundations,
        identities=(*inputs.identities, *state.identities),
        current=(*inputs.current, *state.facts), history=inputs.history,
        relationships=(*inputs.relationships, *state.relationships),
        constraints=inputs.constraints)


def config_for(blueprint, information, draw=None):
    if draw is None:
        from random import randint
        draw = lambda: randint(1, 6)
    return Config(information, blueprint.methods, blueprint.actor, blueprint.targets,
                  blueprint.inventory, blueprint.grants, blueprint.effects, draw)


def integer(value):
    if type(value) is not int or value < 0:
        raise ValueError("Nonnegative integer seconds required")
    return value


def text(value):
    if type(value) is not str or not value.strip():
        raise ValueError("Campaign identity required")
    return value


def records(inputs):
    return tuple(r for f in inputs.foundations for r in (*f.facts, *f.relationships, *f.constraints)) + (
        *inputs.current, *inputs.history, *inputs.relationships, *inputs.constraints)


def validate(data, world, region):
    """Validate retained meaning, never roll, adjudicate or replay a consequence."""
    if type(data) is not CampaignData or data.schema != 1 or type(data.schema) is not int or data.unit != "seconds":
        raise ValueError("Unsupported campaign schema or timeline")
    text(data.id)
    integer(data.revision)
    b, s = data.blueprint, data.state
    if b.rules != "finite-adjudication-v1":
        raise ValueError("Unsupported domain declarations")
    text(b.origin)
    integer(b.start_seconds)
    integer(s.adjudication.at)
    if data.content_digest != content_digest(region) or world["time"] != {"elapsed_seconds": s.adjudication.at}:
        raise ValueError("Campaign time/content mismatch")
    if s.adjudication.at < b.start_seconds:
        raise ValueError("Campaign time precedes origin")
    validate_world_state(world, region)
    base = snapshot(data.inputs)
    # Constructor validates finite methods, target scope, costs, effects, inventory.
    Runtime(config_for(b, lambda: base))
    view = combined(data.inputs, s)
    all_records = (*records(data.inputs), *s.facts, *s.relationships)
    if len({r.id for r in all_records}) != len(all_records):
        raise ValueError("Duplicate campaign records")
    record_ids = {r.id for r in all_records}
    for grant in (*b.grants, *s.grants):
        if grant.record_id not in record_ids or view.identity(grant.character_id) is None:
            raise ValueError("Dangling character access")
        from engine.information_resolution import _source
        _source(grant.source)
        if grant.source.owner != "character" or not grant.source.basis:
            raise ValueError("Invalid character access source")
        integer(grant.period.start)
        if grant.period.end is not None and integer(grant.period.end) <= grant.period.start:
            raise ValueError("Invalid access period")
    for item in all_records:
        integer(item.period.start)
        if item.period.end is not None:
            integer(item.period.end)
    activity_ids = set()
    for a in data.activities:
        text(a.id)
        if a.id in activity_ids or a.actor != b.actor or a.method not in dict(b.targets).get(a.target, ()):
            raise ValueError("Invalid undertaking identity/scope")
        activity_ids.add(a.id)
        if a.action != next(m.action for m in b.methods if m.id == a.method):
            raise ValueError("Undertaking method mismatch")
        integer(a.started_seconds)
        integer(a.progress_seconds)
        if a.started_seconds > s.adjudication.at:
            raise ValueError("Undertaking starts in future")
        from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, decide_activity_control
        decide_activity_control(ActivityAuthorization(a.action, a.method, constraints=a.constraints),
            ActivityCheckpoint(a.action, a.method, blocked=a.boundary.blocked,
                missing_means=a.boundary.missing_means, restart_required=a.boundary.restart_required,
                developments=a.boundary.developments))
        if a.boundary.not_after_seconds is not None:
            integer(a.boundary.not_after_seconds)
        if a.waiting is not None:
            w = a.waiting
            if (w.duration_seconds is None) == (w.condition is None) or a.action != "wait":
                raise ValueError("Waiting needs exactly duration or stopping condition")
            if w.duration_seconds is not None:
                if integer(w.duration_seconds) == 0 or a.progress_seconds > w.duration_seconds:
                    raise ValueError("Invalid waiting duration/progress")
            else:
                text(w.condition)
                if not w.basis or not set(w.basis).issubset(record_ids):
                    raise ValueError("Missing stopping-condition information basis")
    history = s.adjudication.history
    if len(history) != len(s.receipts) or len(history) != len(data.bases):
        raise ValueError("Incomplete acceptance history")
    remaining = {(a, r): n for a, r, n in b.inventory}
    obligations, ended, request_ids = set(), set(), set()
    at = b.start_seconds
    effects, identities, relationships, grants = [], [], [], []
    for index, (accepted, receipt, basis) in enumerate(zip(history, s.receipts, data.bases)):
        request, assessment, attempt = receipt.request, accepted.assessment, accepted.attempt
        # Domain declarations are immutable throughout this bounded campaign.
        method = next((m for m in b.methods if m.id == request.method), None)
        if (method is None or request.id in request_ids or request.intent != "commit"
                or request.actor != b.actor or request.method not in dict(b.targets).get(request.target, ())
                or request.undertaking not in activity_ids or attempt != assessment.attempt
                or (attempt.id, attempt.actor, attempt.action, attempt.method, attempt.target, attempt.means,
                    attempt.binding, attempt.authorization.constraints) !=
                   (request.id, request.actor, request.action, request.method, request.target, request.means,
                    request.binding, request.constraints)
                or attempt.at != at or assessment.revision != index
                or assessment.costs != method.costs or assessment.capability != method.capability
                or receipt.step.ref != request.id):
            raise ValueError("Acceptance identity/declaration mismatch")
        if request.action != method.action or request.means != method.means:
            raise ValueError("Accepted method/means mismatch")
        a = next(a for a in data.activities if a.id == request.undertaking)
        if (a.actor, a.action, a.target, a.method, a.constraints) != (
                request.actor, request.action, request.target, request.method, request.constraints):
            raise ValueError("Accepted undertaking mismatch")
        request_ids.add(request.id)
        info = snapshot(basis)
        known = {r.id for r in records(basis)} | {r.id for r in effects + relationships}
        if not set(assessment.premise_ids).issubset(known):
            raise ValueError("Missing accepted causal basis")
        if info.identity(attempt.location) is None:
            raise ValueError("Unknown accepted location")
        if assessment.result not in {"full", "partial", "failure", "blocked"}:
            raise ValueError("Invalid accepted outcome")
        if len(set(assessment.obligations)) != len(assessment.obligations) or any(
                len(o) != 2 or o[0] not in known or not isinstance(o[1], str) or not o[1]
                for o in assessment.obligations):
            raise ValueError("Invalid retained commitments")
        if assessment.draw is not None:
            from engine.character_competence import resolve
            specialist = False
            if method.specialist:
                found = info.resolve(Query((request.actor,), attempt.at, (method.specialist,)))
                specialist = any(f.value == "yes" for f in found.facts)
            if assessment.mechanical_result != resolve(assessment.draw, specialist):
                raise ValueError("Recorded mechanics contradict accepted basis")
            if type(assessment.draw) is not int or not 1 <= assessment.draw <= 6 or method.mechanic != "d6":
                raise ValueError("Invalid retained mechanics")
            if assessment.result != assessment.mechanical_result or assessment.result == "blocked":
                raise ValueError("Retained mechanics/result mismatch")
        elif assessment.mechanical_result is not None or (
                method.mechanic == "d6" and assessment.result != "blocked"):
            raise ValueError("Missing retained mechanics")
        expected_outcome = {"full": "complete", "partial": "incomplete", "failure": "negative", "blocked": "negative"}[assessment.result]
        if (receipt.step.outcome != expected_outcome or receipt.step.public_refs != ("result",)
                or len(receipt.step.accessible) != 1 or receipt.step.accessible[0][0] != "result"):
            raise ValueError("Invalid safe acceptance receipt")
        text(receipt.step.accessible[0][1])
        for resource, cost in method.costs:
            key = (request.actor, resource)
            if key not in remaining or remaining[key] < cost:
                raise ValueError("Inconsistent accepted expenditures")
            remaining[key] -= cost
        obligations.update((request.actor, binding, value) for binding, value in assessment.obligations)
        ended.update(assessment.ended)
        if not set(assessment.applied_bindings + assessment.ended).issubset(known):
            raise ValueError("Dangling accepted binding")
        # Validate safe meaning with read-only presentation of accepted authority.
        # No attempt adjudication, sampling or consequence application occurs here.
        from engine.information_adjudication import AdjudicationSession
        prefix = State(SessionState(at=attempt.at, inventory=tuple((a, r, n) for (a, r), n in remaining.items()),
            ended=tuple(ended), obligations=tuple(obligations)), tuple(identities),
            tuple(effects), tuple(relationships), tuple(grants))
        reads = InformationView(info, prefix)
        evaluator = AdjudicationSession(reads, b.methods, grants=(*b.grants, *prefix.grants), time_unit="seconds")
        candidate = replace(prefix.adjudication, at=at + method.duration)
        safe = evaluator._presentation(attempt, method, assessment, candidate)
        if Runtime._receipt(request, assessment.result, safe) != receipt.step:
            raise ValueError("Receipt contradicts accepted accessible meaning")
        at += method.duration
        # Check effect/receipt coupling without running gameplay or inventing outcomes.
        from engine.information_resolution import Fact, Source, Relationship, AccessGrant
        for number, effect in enumerate(b.effects):
            if (effect.method, effect.result) != (request.method, assessment.result):
                continue
            fact_id = f"{request.id}:fact:{number}"
            source = Source(request.id, "world_simulation", ("Accepted supported domain effect",))
            effects.append(Fact(fact_id, effect.subject, effect.predicate, effect.value, source, Period(at)))
            if effect.identity and effect.identity not in identities and info.identity(effect.identity.id) is None:
                identities.append(effect.identity)
            if effect.relation:
                relationships.append(Relationship(f"{request.id}:relation:{number}", effect.relation_from,
                    effect.relation, effect.subject, source, Period(at)))
            if effect.visible:
                grants.append(AccessGrant(fact_id, request.actor,
                    Source(request.id, "character", ("Legitimately observed accepted result",)), Period(at)))
    if (at != s.adjudication.at or dict(((a, r), n) for a, r, n in s.adjudication.inventory) != remaining
            or len(s.adjudication.inventory) != len(remaining)
            or set(s.adjudication.obligations) != obligations or set(s.adjudication.ended) != ended
            or tuple(effects) != s.facts or tuple(identities) != s.identities
            or tuple(relationships) != s.relationships or tuple(grants) != s.grants):
        raise ValueError("Incomplete consequential state")
    for a in data.activities:
        receipts = tuple(r.request.id for r in s.receipts if r.request.undertaking == a.id)
        progress = sum(next(m.duration for m in b.methods if m.id == r.request.method)
                       for r in s.receipts if r.request.undertaking == a.id)
        if a.accepted != receipts or a.progress_seconds != progress:
            raise ValueError("Incomplete undertaking progress")
    events = [e for e in world["history"] if e.get("event_type") == "campaign_increment"]
    if len(events) != len(history) or any(
            (e.get("attempt_id"), e.get("increment_id"), e.get("time")) !=
            (r.request.id, f"{data.id}:increment:{r.request.id}",
             {"elapsed_seconds": h.attempt.at + next(m.duration for m in b.methods if m.id == h.attempt.method)})
            for e, r, h in zip(events, s.receipts, history)):
        raise ValueError("Missing campaign causal history")


def prepare_root(data, world, region):
    validate(data, world, region)
    return Root(data, deepcopy(world), build_scene(region, world))


def attach(engine, blueprint, inputs, draw=None):
    if type(blueprint) is not Blueprint or type(inputs) is not Inputs:
        raise ValueError("Explicit I3 declarations required")
    if any(k in engine.world_state for k in ("west_road_predicament", "material_state")):
        raise ValueError("Legacy scenario time owner requires an explicit adapter")
    holder = []
    def information():
        return snapshot(holder[0].campaign.data.inputs if holder else inputs)
    runtime = Runtime(config_for(blueprint, information, draw))
    data = CampaignData(str(uuid4()), 0, blueprint, inputs,
        State(SessionState(at=blueprint.start_seconds, inventory=blueprint.inventory)), (), (),
        content_digest(engine.region))
    world = engine.get_world_state()
    world["time"] = {"elapsed_seconds": blueprint.start_seconds}
    runtime.campaign = prepare_root(data, world, engine.region)
    holder.append(runtime)
    return runtime


def activity(runtime, request):
    a = next((a for a in runtime.campaign.data.activities if a.id == request.undertaking), None)
    if a is None or (a.actor, a.action, a.target, a.method, a.constraints) != (
            request.actor, request.action, request.target, request.method, request.constraints):
        raise Unresolved("authorization", "undertaking_scope")
    if a.waiting is not None:
        raise Unresolved("routing", "waiting_executor_unavailable")
    return a


def acceptance_basis(reads, inputs, grants):
    """Retain actually accessed base premises and reference closure, not the world."""
    record_ids = {g.record_id for g in grants}
    subjects = {g.character_id for g in grants}
    for operation, args, value in reads.values:
        if operation == "identity":
            if value is not None:
                subjects.add(value.id)
            continue
        record_ids.update(r.id for r in (*value.facts, *value.relationships, *value.constraints))
    available = snapshot(inputs)
    selected = [r for r in records(inputs) if r.id in record_ids]
    from engine.information_resolution import Fact, Relationship, Constraint
    for r in selected:
        if isinstance(r, Fact):
            subjects.add(r.subject)
            if r.holder:
                subjects.add(r.holder)
        elif isinstance(r, Relationship):
            subjects.update((r.subject, r.target))
        else:
            subjects.update(r.subjects)
    # Definition closure is data, not an exhaustive relationship traversal.
    for subject in tuple(subjects):
        identity = available.identity(subject)
        while identity is not None and identity.definition_id:
            subjects.add(identity.definition_id)
            identity = available.identity(identity.definition_id)
    foundations = tuple(replace(f,
        identities=tuple(i for i in f.identities if i.id in subjects),
        facts=tuple(r for r in f.facts if r.id in record_ids),
        relationships=tuple(r for r in f.relationships if r.id in record_ids),
        constraints=tuple(r for r in f.constraints if r.id in record_ids))
        for f in inputs.foundations)
    return Inputs(foundations, tuple(i for i in inputs.identities if i.id in subjects),
        tuple(r for r in inputs.current if r.id in record_ids),
        tuple(r for r in inputs.history if r.id in record_ids),
        tuple(r for r in inputs.relationships if r.id in record_ids),
        tuple(r for r in inputs.constraints if r.id in record_ids))


def accepted_root(runtime, state, request, engine, basis):
    root = runtime.campaign
    a = activity(runtime, request)
    duration = state.adjudication.at - root.data.state.adjudication.at
    updated = replace(a, accepted=(*a.accepted, request.id), progress_seconds=a.progress_seconds + duration)
    data = replace(root.data, revision=root.data.revision + 1, state=state,
        activities=tuple(updated if item.id == a.id else item for item in root.data.activities),
        bases=(*root.data.bases, basis))
    world = deepcopy(root.world)
    world["time"] = {"elapsed_seconds": state.adjudication.at}
    world = add_history_entry(world, "campaign_increment", "Accepted consequential increment.",
        world["player"]["current_location_id"], world["time"],
        {"attempt_id": request.id, "increment_id": f"{data.id}:increment:{request.id}"})
    return prepare_root(data, world, engine.region)


def export(engine):
    runtime = engine._consequences
    if runtime.running:
        raise ValueError("Cannot capture running acceptance")
    root = runtime.campaign
    if runtime.config != config_for(root.data.blueprint, runtime.config.information, runtime.config.draw):
        raise ValueError("Campaign declaration mismatch")
    validate(root.data, root.world, engine.region)
    world = deepcopy(root.world)
    world["continuing_gameplay"] = pack(root.data)
    return {"save_version": 2, "region_path": engine.region_path, "world_state": world}


def restore(payload, *, draw=None):
    from engine.game_engine import GameEngine
    if set(payload) != {"save_version", "region_path", "world_state"} or type(payload["save_version"]) is not int or payload["save_version"] != 2:
        raise ValueError("Unsupported campaign envelope")
    world = deepcopy(payload["world_state"])
    if type(world) is not dict or "continuing_gameplay" not in world:
        raise ValueError("Incomplete campaign")
    data = unpack(world.pop("continuing_gameplay"))
    # Build separate owners; no callbacks or saved code names are executed.
    engine = GameEngine(payload["region_path"], initial_world_state=world)
    root = prepare_root(data, world, engine.region)
    holder = []
    def information():
        return snapshot(holder[0].campaign.data.inputs if holder else data.inputs)
    runtime = Runtime(config_for(data.blueprint, information, draw))
    runtime.campaign = root
    holder.append(runtime)
    engine._consequences = runtime
    # Restore only accepted safe meaning for later F01 continuity, never private context.
    rebuilt = []
    for accepted, receipt in zip(data.state.adjudication.history, data.state.receipts):
        context = {"developments": []}
        # _presentation only reads the development list; receipt is Character-safe.
        context["developments"] = [dict(id=receipt.request.id, meaning=receipt.step.accessible[0][1],
            authority="Action & Resolution", status="resolved", source="Previously accepted result",
            time=f"Elapsed {accepted.attempt.at + next(m.duration for m in data.blueprint.methods if m.id == accepted.attempt.method)} seconds",
            access="Accepted character-safe receipt")]
        rebuilt.append(replace(accepted, context=context))
    state = replace(data.state, adjudication=replace(data.state.adjudication, history=tuple(rebuilt)))
    runtime.campaign = replace(root, data=replace(data, state=state))
    runtime.note("restoration", reason="validated")
    return engine


def begin(engine, action, target, method, *, constraints=(), waiting=None):
    runtime = engine._consequences
    if runtime is None or runtime.campaign is None or runtime.running:
        raise ValueError("Idle I3 campaign required")
    root = runtime.campaign
    a = Activity(str(uuid4()), root.data.blueprint.actor, action, target, method, constraints,
                 root.data.state.adjudication.at, waiting=waiting)
    data = replace(root.data, revision=root.data.revision + 1, activities=(*root.data.activities, a))
    runtime.campaign = prepare_root(data, root.world, engine.region)
    return a.id


def revise(engine, *, inputs=None, undertaking=None, boundary=None, location=None):
    """Trusted World/Character/checkpoint supplier boundary, not player input."""
    runtime = engine._consequences
    if runtime is None or runtime.campaign is None:
        raise ValueError("I3 required")
    root = runtime.campaign
    activities = root.data.activities
    if undertaking is not None:
        if boundary is None or type(boundary) is not Boundary or undertaking not in {a.id for a in activities}:
            raise ValueError("Explicit supported checkpoint required")
        activities = tuple(replace(a, boundary=boundary) if a.id == undertaking else a for a in activities)
    data = replace(root.data, revision=root.data.revision + 1,
                   inputs=inputs if inputs is not None else root.data.inputs, activities=activities)
    world = deepcopy(root.world)
    if location is not None:
        world["player"]["current_location_id"] = location
    runtime.campaign = prepare_root(data, world, engine.region)



def check_continuation(runtime, request):
    from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, decide_activity_control
    a = activity(runtime, request)
    method = next(m for m in runtime.config.methods if m.id == request.method)
    boundary = a.boundary
    crossing = (boundary.not_after_seconds is not None
                and runtime._state.adjudication.at + method.duration > boundary.not_after_seconds)
    control = decide_activity_control(
        ActivityAuthorization(a.action, a.method, request.intent, a.constraints),
        ActivityCheckpoint(a.action, a.method, blocked=boundary.blocked or crossing,
            missing_means=boundary.missing_means, conflicting_constraints=method.conflicts,
            restart_required=boundary.restart_required, developments=boundary.developments))
    if control.status != "continue":
        raise Unresolved("authorization", control.reason)
