"""Declarative I3 development suppliers; existing finite routine/d6, no scenario engine."""
from dataclasses import replace
import json
from pathlib import Path

from engine.campaign_records import Blueprint, Inputs, Boundary, WaitingIntent
from engine.consequence_integration import FactEffect, Request
from engine.game_engine import GameEngine
from engine.information_adjudication import Method
from engine.information_resolution import (
    Source, Identity, Fact, Foundation, Constraint, BindingTerms, Period, AccessGrant,
)

REGION = "data/regions/market_passage_v1.json"
LOCATION = json.loads(Path(REGION).read_text())["locations"][0]["location_id"]
HIDDEN = "PRIVATE-BINDING-CAUSE"
AUTHORED = Source("fixture-foundation", "authored")
CHARACTER = Source("fixture-access", "character", ("Explicit supplied knowledge",))


class Draws:
    def __init__(self, *values):
        self.values = list(values or (6,))
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return self.values.pop(0) if len(self.values) > 1 else self.values[0]


def declarations(*, effects=True, duration=31):
    facts = (Fact("capability", "actor", "capability:search", "yes", AUTHORED),
             Fact("available", "target", "manageable", "yes", AUTHORED))
    identities = tuple(Identity(s) for s in ("actor", "target", LOCATION, "wedge", "agreement"))
    promise = Constraint("terms", ("target",), ("search",), BindingTerms(
        ("obligation=return the wedge",)), AUTHORED)
    inputs = Inputs((Foundation("fixture", "setting", "era", identities, facts, constraints=(promise,)),))
    methods = (Method("inspect", "search", "search", ("wedge",), (("wedge", 1),),
        requirements=("fact=target|manageable|yes",), mechanic="d6", duration=duration),
        Method("use", "search", "search", requirements=(
            "fact=finding|searched|yes", "commitment=terms|return the wedge"), duration=7),
        Method("hold", "wait", "search", duration=0))
    effect = (FactEffect("inspect", "finding", "searched", "yes", result="partial",
                    identity=Identity("finding"), relation_from="target", relation="governs", visible=True),
              FactEffect("inspect", "opening", "usable", "yes",
                    identity=Identity("opening"), relation_from="target", relation="governs", visible=False)) if effects else ()
    blueprint = Blueprint("actor", (("target", ("inspect", "hold")), ("finding", ("use",))),
        methods, (("actor", "wedge", 4),),
        grants=(AccessGrant("terms", "actor", CHARACTER),), effects=effect)
    return blueprint, inputs


def engine(*, draws=None, effects=True, duration=31):
    b, i = declarations(effects=effects, duration=duration)
    return GameEngine(REGION, campaign_config=(b, i), campaign_draw=draws or Draws(3, 6))


def start(e):
    return e.begin_undertaking("search", "target", "inspect")


def request(undertaking, id="first", **changes):
    return replace(Request(id, "actor", "search", "target", "inspect", ("wedge",),
                           undertaking=undertaking), **changes)


def changed_inputs(e, *, capable=True, blocked=False, expires=None):
    data = e.get_campaign_state()
    foundation = data.inputs.foundations[0]
    facts = tuple(replace(f, value="no") if f.id == "capability" and not capable else f
                  for f in foundation.facts)
    bindings = foundation.constraints
    if blocked:
        bindings += (Constraint(HIDDEN, (LOCATION,), ("search",), BindingTerms(("block",)),
                                AUTHORED, Period(0, expires)),)
    return replace(data.inputs, foundations=(replace(foundation, facts=facts, constraints=bindings),))
