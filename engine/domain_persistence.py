"""Finite envelope-v3 codec with explicit campaign-schema interpretation."""
from dataclasses import fields
from typing import get_type_hints

from engine import historical_persistence as historical
from engine.campaign_records import _matches
from engine import domain_campaign as common
from engine.climbing_domain import ClimbPlan, ClimbOptions, ClimbUpdate, TraversalConsequence

LEGACY_DEFAULTS = historical.LEGACY_DEFAULTS
CONTINUITY_DEFAULTS = historical.CONTINUITY_DEFAULTS
_HISTORICAL_COMMON = {'Campaign', 'ActivityScope', 'Increment', 'AcceptedUnit', 'ActivityStage',
    'ActivityRun', 'ActivityUpdate', 'ActivityResponse', 'ChoiceContext', 'TraversalConsequence'}
RECORDS = {k: v for k, v in historical.RECORDS.items() if k not in _HISTORICAL_COMMON}
RECORDS.update({c.__name__: c for c in (
    common.Campaign, common.ActivityScope, common.Increment, common.AcceptedUnit,
    common.ActivityStage, common.ActivityRun, common.ActivityUpdate, common.ActivityResponse,
    common.ChoiceContext, ClimbPlan, ClimbOptions, ClimbUpdate, TraversalConsequence)})


def pack(value):
    if type(value) in (str, int, bool, type(None)):
        return value
    if type(value) is tuple:
        return {'tuple': [pack(v) for v in value]}
    if type(value) in RECORDS.values():
        return {'record': type(value).__name__, 'fields': {f.name: pack(getattr(value, f.name)) for f in fields(value)}}
    return historical.pack(value)


def unpack(value, *, schema=None, legacy=False, continuity_legacy=False):
    if schema is None and type(value) is dict and value.get('record') == 'Campaign':
        schema = value.get('fields', {}).get('schema')
    if schema in {1, 2, 3}:
        return historical.unpack(value, legacy=legacy or schema == 1,
                                 continuity_legacy=continuity_legacy or schema in {1, 2})
    if schema not in {None, 4}:
        raise ValueError('unsupported campaign schema')
    if type(value) in (str, int, bool, type(None)):
        return value
    if type(value) is not dict:
        raise ValueError('invalid domain encoding')
    if set(value) == {'tuple'} and type(value['tuple']) is list:
        return tuple(unpack(v, schema=4) for v in value['tuple'])
    if set(value) != {'record', 'fields'} or type(value['record']) is not str:
        raise ValueError('invalid domain record')
    cls = RECORDS.get(value['record'])
    if cls is None or type(value['fields']) is not dict or set(value['fields']) != {f.name for f in fields(cls)}:
        raise ValueError('unknown or incomplete domain record')
    args = {n: unpack(v, schema=4) for n, v in value['fields'].items()}
    hints = get_type_hints(cls)
    if any(not _matches(v, hints[n]) for n, v in args.items()):
        raise ValueError('invalid domain field type')
    return cls(**args)


def export(campaign, *, handlers=()):
    common.validate_campaign(campaign, handlers=handlers)
    return {'save_version': 3, 'domain_campaign': pack(campaign)}


def restore(envelope, *, handlers=()):
    if (type(envelope) is not dict or set(envelope) != {'save_version', 'domain_campaign'}
            or type(envelope['save_version']) is not int or envelope['save_version'] != 3):
        raise ValueError('unsupported domain envelope')
    value = envelope['domain_campaign']
    if type(value) is not dict or value.get('record') != 'Campaign' or type(value.get('fields')) is not dict:
        raise ValueError('campaign encoding required')
    schema = value['fields'].get('schema')
    if type(schema) is not int or schema not in {1, 2, 3, 4}:
        raise ValueError('unsupported campaign schema')
    return common.validate_campaign(unpack(value, schema=schema), handlers=handlers)
