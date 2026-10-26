"""Finite version-3 opt-in codec. No executable values or legacy conversion."""
from dataclasses import fields
from typing import get_type_hints

from engine.activity_control import ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment
from engine.campaign_records import _matches
from engine.character_rules import CreatureRules, StrengthTrait
from engine.domain_campaign import Domains, ActivityScope, Increment, AcceptedUnit, Campaign, validate_campaign
from engine.gameplay_coordination import AcceptedStep
from engine.physical_world import (
    Place, Surface, TraversalLink, PhysicalObject, PhysicalRelation, CausalRecord, FallOccurrence, PhysicalFrame,
)
from engine.traversal_resolution import ClimbRequest, ClimbRuling, ClimbDependencies, ClimbAssessment, ClimbResult


RECORDS = {c.__name__: c for c in (
    ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment, CreatureRules, StrengthTrait,
    Domains, ActivityScope, Increment, AcceptedUnit, Campaign, AcceptedStep,
    Place, Surface, TraversalLink, PhysicalObject, PhysicalRelation, CausalRecord, FallOccurrence,
    PhysicalFrame, ClimbRequest, ClimbRuling, ClimbDependencies, ClimbAssessment, ClimbResult,
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


def unpack(value):
    if type(value) in (str, int, bool, type(None)):
        return value
    if type(value) is not dict:
        raise ValueError('Invalid domain encoding')
    if set(value) == {'tuple'} and type(value['tuple']) is list:
        return tuple(unpack(v) for v in value['tuple'])
    if set(value) != {'record', 'fields'} or type(value['record']) is not str:
        raise ValueError('Invalid domain record')
    cls = RECORDS.get(value['record'])
    if cls is None or type(value['fields']) is not dict or set(value['fields']) != {f.name for f in fields(cls)}:
        raise ValueError('Unknown or incomplete domain record')
    args = {n: unpack(v) for n, v in value['fields'].items()}
    hints = get_type_hints(cls)
    if any(not _matches(v, hints[n]) for n, v in args.items()):
        raise ValueError('Invalid domain field type')
    return cls(**args)


def export(campaign):
    validate_campaign(campaign)
    return {'save_version': 3, 'domain_campaign': pack(campaign)}


def restore(envelope):
    if (type(envelope) is not dict or set(envelope) != {'save_version', 'domain_campaign'}
            or type(envelope['save_version']) is not int or envelope['save_version'] != 3):
        raise ValueError('Unsupported domain envelope')
    return validate_campaign(unpack(envelope['domain_campaign']))
