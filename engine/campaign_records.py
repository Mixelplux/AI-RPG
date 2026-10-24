"""Finite I3 campaign records and codec. No arbitrary object/callable restoration."""
from dataclasses import dataclass, fields
from types import UnionType
from typing import get_args, get_origin, get_type_hints

from engine.activity_control import ActivityAuthorization, ActivityDevelopment
from engine.gameplay_coordination import AcceptedStep
from engine.information_resolution import (
    Source, Period, Identity, Fact, Relationship, BindingTerms, Constraint, Foundation, AccessGrant,
)
from engine.information_adjudication import Method, Attempt, Assessment, Accepted, SessionState
from engine.consequence_integration import Request, FactEffect, Receipt, State


@dataclass(frozen=True)
class Inputs:
    foundations: tuple[Foundation, ...]
    identities: tuple[Identity, ...] = ()
    current: tuple[Fact, ...] = ()
    history: tuple[Fact, ...] = ()
    relationships: tuple[Relationship, ...] = ()
    constraints: tuple[Constraint, ...] = ()


@dataclass(frozen=True)
class Blueprint:
    actor: str
    targets: tuple
    methods: tuple[Method, ...]
    inventory: tuple = ()
    grants: tuple[AccessGrant, ...] = ()
    effects: tuple[FactEffect, ...] = ()
    origin: str = "campaign-start"
    start_seconds: int = 0
    rules: str = "finite-adjudication-v1"


@dataclass(frozen=True)
class WaitingIntent:
    duration_seconds: int | None = None
    condition: str | None = None
    basis: tuple[str, ...] = ()


@dataclass(frozen=True)
class Boundary:
    blocked: bool = False
    missing_means: tuple[str, ...] = ()
    restart_required: bool = False
    developments: tuple[ActivityDevelopment, ...] = ()
    not_after_seconds: int | None = None


@dataclass(frozen=True)
class Activity:
    id: str
    actor: str
    action: str
    target: str
    method: str
    constraints: tuple[str, ...]
    started_seconds: int
    accepted: tuple[str, ...] = ()
    progress_seconds: int = 0
    boundary: Boundary = Boundary()
    waiting: WaitingIntent | None = None


@dataclass(frozen=True)
class CampaignData:
    id: str
    revision: int
    blueprint: Blueprint
    inputs: Inputs
    state: State
    activities: tuple[Activity, ...]
    bases: tuple[Inputs, ...]
    content_digest: str
    unit: str = "seconds"
    schema: int = 1


# Fixed supported domain vocabulary, not a public serialization extension registry.
_RECORDS = {c.__name__: c for c in (
    Source, Period, Identity, Fact, Relationship, BindingTerms, Constraint, Foundation,
    AccessGrant, Method, Attempt, Assessment, Accepted, SessionState, Request, FactEffect,
    Receipt, State, ActivityAuthorization, ActivityDevelopment, AcceptedStep, Inputs,
    Blueprint, WaitingIntent, Boundary, Activity, CampaignData,
)}


def _matches(value, annotation):
    if annotation is object:
        return False
    if annotation is type(None):
        return value is None
    origin, args = get_origin(annotation), get_args(annotation)
    if origin is UnionType:
        return any(_matches(value, a) for a in args)
    if annotation is tuple or origin is tuple:
        if type(value) is not tuple:
            return False
        return not args or (all(_matches(v, args[0]) for v in value) if args[-1] is Ellipsis
                            else len(value) == len(args) and all(_matches(v, a) for v, a in zip(value, args)))
    return type(value) is annotation


def pack(value):
    if type(value) in (str, int, bool, type(None)):
        return value
    if type(value) is tuple:
        return {"tuple": [pack(v) for v in value]}
    if type(value) in _RECORDS.values():
        # Accepted presentation context is derived from the stored safe receipt.
        names = [f.name for f in fields(value) if not (type(value) is Accepted and f.name == "context")]
        return {"record": type(value).__name__, "fields": {n: pack(getattr(value, n)) for n in names}}
    raise ValueError("Unsupported campaign value")


def unpack(value):
    if type(value) in (str, int, bool, type(None)):
        return value
    if type(value) is not dict:
        raise ValueError("Invalid campaign encoding")
    if set(value) == {"tuple"} and type(value["tuple"]) is list:
        return tuple(unpack(v) for v in value["tuple"])
    if set(value) != {"record", "fields"} or type(value["record"]) is not str:
        raise ValueError("Invalid campaign record")
    cls = _RECORDS.get(value["record"])
    if cls is None or type(value["fields"]) is not dict:
        raise ValueError("Unknown campaign record")
    names = {f.name for f in fields(cls)} - ({"context"} if cls is Accepted else set())
    if set(value["fields"]) != names:
        raise ValueError("Incomplete campaign record")
    args = {n: unpack(v) for n, v in value["fields"].items()}
    hints = get_type_hints(cls)
    if any(not _matches(v, hints[n]) for n, v in args.items()):
        raise ValueError("Invalid campaign field type")
    if cls is Accepted:
        args["context"] = {"developments": []}
    return cls(**args)
