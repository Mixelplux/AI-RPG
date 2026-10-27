"""Finite version-3 opt-in codec. No executable values or legacy conversion."""
from dataclasses import fields
from typing import get_type_hints

from engine.historical_activity import ActivityStage, ActivityRun, ActivityUpdate, ActivityResponse, ChoiceContext
from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment
from engine.campaign_records import _matches
from engine.character_rules import CreatureRules, StrengthTrait, Vitality
from engine.historical_campaign import Domains, ActivityScope, Increment, AcceptedUnit, Campaign, TraversalConsequence, validate_campaign
from engine.gameplay_coordination import AcceptedStep
from engine.physical_world import (
    Place, Surface, TraversalLink, PhysicalObject, PhysicalRelation, CausalRecord, FallOccurrence, PhysicalFrame,
    TautProtection, ClimbCircumstances,
)
from engine.traversal_resolution import ClimbRequest, ClimbRuling, ClimbDependencies, ClimbAssessment, ClimbResult, FallDependencies, FallResult


RECORDS = {c.__name__: c for c in (
    ActivityStage, ActivityRun, ActivityUpdate, ActivityResponse, ChoiceContext,
    ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment, CreatureRules, StrengthTrait,
    Domains, ActivityScope, Increment, AcceptedUnit, Campaign, AcceptedStep,
    Place, Surface, TraversalLink, PhysicalObject, PhysicalRelation, CausalRecord, FallOccurrence,
    PhysicalFrame, ClimbRequest, ClimbRuling, ClimbDependencies, ClimbAssessment, ClimbResult,
    Vitality, TautProtection, ClimbCircumstances, TraversalConsequence, FallDependencies, FallResult,
)}


def pack(value):
    if type(value) in (str, int, bool, type(None)):
        return value
    if type(value) is tuple:
        return {'tuple': [pack(v) for v in value]}
    if type(value) in RECORDS.values():
        return {'record': type(value).__name__,
                'fields': {f.name: pack(getattr(value, f.name)) for f in fields(value)}}
    raise ValueError('Unsupported domain record')


# Explicit default additions preserve historical schema-1/2 meanings.
LEGACY_DEFAULTS = {
    'CreatureRules': {'vitality': None},
    'PhysicalFrame': {'climb_circumstances': ()},
    'ClimbRuling': {'failure_mode': None, 'failure_movement_cost': None},
    'AcceptedUnit': {'consequence': None},
}


CONTINUITY_DEFAULTS = {
    'ActivityScope': {'objective': None, 'continuations': (), 'supported_constraints': (), 'notices': (), 'choice_contexts': ()},
    'Increment': {'run': None},
}


def unpack(value, *, legacy=False, continuity_legacy=False):
    if type(value) in (str, int, bool, type(None)):
        return value
    if type(value) is not dict:
        raise ValueError('Invalid domain encoding')
    if set(value) == {'tuple'} and type(value['tuple']) is list:
        return tuple(unpack(v, legacy=legacy, continuity_legacy=continuity_legacy) for v in value['tuple'])
    if set(value) != {'record', 'fields'} or type(value['record']) is not str:
        raise ValueError('Invalid domain record')
    cls = RECORDS.get(value['record'])
    if cls is None or type(value['fields']) is not dict:
        raise ValueError('Unknown domain record')
    names = {f.name for f in fields(cls)}
    missing = names - set(value['fields'])
    defaults = dict(LEGACY_DEFAULTS.get(cls.__name__, {})) if legacy else {}
    if continuity_legacy:
        defaults.update(CONTINUITY_DEFAULTS.get(cls.__name__, {}))
    if set(value['fields']) - names or not missing.issubset(defaults):
        raise ValueError('Unknown or incomplete domain record')
    args = {n: unpack(v, legacy=legacy, continuity_legacy=continuity_legacy) for n, v in value['fields'].items()}
    args.update({n: defaults[n] for n in missing})
    hints = get_type_hints(cls)
    if any(not _matches(v, hints[n]) for n, v in args.items()):
        raise ValueError('Invalid domain field type')
    return cls(**args)
