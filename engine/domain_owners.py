"""Composition of supported domain owners; no mechanical dispatch rules."""


def domain_owner(scope, handlers=()):
    from engine.climbing_domain import CLIMBING
    matches = [h for h in (CLIMBING, *handlers) if h.id == scope.domain]
    if len(matches) != 1:
        raise ValueError('unsupported or competing domain owner')
    return matches[0]
