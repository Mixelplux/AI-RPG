"""Declared inspection premises. No scenario identity or outcome selector.

The fixture owns availability, visible aliases, requirements and finite method
declarations. Existing routine/d6 rules alone determine results.
"""
from dataclasses import replace

from engine.campaign_records import Blueprint, Inputs
from engine.consequence_integration import FactEffect
from engine.game_engine import GameEngine
from engine.gameplay_coordination import SituatedContext, Target
from engine.information_adjudication import Method
from engine.information_resolution import Foundation, Identity, Fact, Source, Query
from test_fixtures.continuity_suppliers import REGION, LOCATION, Draws

AUTHORED = Source("inspection-premises", "authored")


class InspectionSuppliers:
    def __init__(self, name="cargo panel", *, duration=19, draws=None):
        self.name = name
        self.draws = draws or Draws(3, 6)
        self.duration = duration
        self.available = True
        self.means = ("lamp",)
        self.unavailable = ()

    def declarations(self):
        identities = tuple(Identity(s) for s in ("actor", "target", "lamp", LOCATION))
        facts = (Fact("inspection-capability", "actor", "capability:inspection", "yes", AUTHORED),
                 Fact("surface-access", "target", "accessible", "yes", AUTHORED))
        inputs = Inputs((Foundation("inspection", "setting", "era", identities, facts),))
        inspect = Method("inspection", "search", "inspection", ("lamp",), (("lamp", 1),),
            requirements=("fact=target|accessible|yes",), mechanic="d6", duration=self.duration,
            observations=(("partial", "You examine the exposed surface; the inner markings remain unexamined."),
                          ("full", "You finish inspecting the inner markings."),
                          ("failure", "The inspection establishes no finding."),
                          ("blocked", "You cannot complete the chosen inspection.")))
        review = Method("review", "search", "inspection",
            requirements=("fact=finding|examined|The exposed surface has been examined.",
                          "fact=target|accessible|yes"), duration=7,
            observations=(("full", "You compare the retained surface finding with the current inspection."),
                          ("partial", "The comparison remains incomplete."),
                          ("failure", "The comparison establishes no further finding."),
                          ("blocked", "You cannot complete the comparison.")))
        effects = (FactEffect("inspection", "finding", "examined", "The exposed surface has been examined.", result="partial",
                             identity=Identity("finding"), relation_from="target", relation="governs", visible=True),
                   FactEffect("inspection", "conclusion", "identified", "The inner markings have been identified.",
                             identity=Identity("conclusion"), relation_from="target", relation="governs", visible=True))
        return Blueprint("actor", (("target", ("inspection",)), ("finding", ("review",))),
                         (inspect, review), (("actor", "lamp", 4),), effects=effects), inputs

    def context(self, engine):
        data = engine.get_campaign_state()
        location = engine.world_state["player"]["current_location_id"]
        targets = (Target("target", (self.name,), "search", ("inspection",), "inspection"),) if self.available else ()
        info = engine.get_consequence_information()
        known = info.for_character(Query(("finding",), data.state.adjudication.at, ("examined",)),
                                   data.blueprint.actor, (*data.blueprint.grants, *data.state.grants))
        if known.facts:
            targets += (Target("finding", ("surface finding",), "search", ("review",), "review"),)
        return SituatedContext(str(data.revision), location, targets, self.means,
            unavailable=self.unavailable,
            accessible=(("target", f"The {self.name} is available for the supplied lamp inspection."),
                        ("finding", "The retained surface finding is available for comparison.")))

    def engine(self):
        return GameEngine(REGION, campaign_config=self.declarations(), campaign_draw=self.draws,
                          player_activity_context=self.context)

    def inputs(self, engine, *, accessible="yes", capability="yes", availability="available"):
        current = engine.get_campaign_state().inputs
        foundation = current.foundations[0]
        facts = tuple(replace(f, value=accessible if availability == "available" else None,
                              availability=availability) if f.id == "surface-access"
                      else replace(f, value=capability) if f.id == "inspection-capability" else f
                      for f in foundation.facts)
        return replace(current, foundations=(replace(foundation, facts=facts),))
