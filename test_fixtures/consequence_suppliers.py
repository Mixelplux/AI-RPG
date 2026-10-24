"""I2 premises/finite method declarations; no scenario outcome selector."""
import json
from dataclasses import replace
from pathlib import Path

from engine.consequence_integration import Config, Request
from engine.game_engine import GameEngine
from engine.information_adjudication import Method
from engine.information_resolution import (
    BindingTerms, Constraint, Fact, Foundation, Identity, InformationSnapshot,
    Relationship, Source,
)

REGION = 'data/regions/market_passage_v1.json'
LOCATION = json.loads(Path(REGION).read_text())['locations'][0]['location_id']
AUTHORED = Source('supported-foundation', 'authored')
HIDDEN = 'SECRET-BINDING-CAUSE'


class Premises:
    def __init__(self):
        self.facts = (
            Fact('capability', 'actor', 'capability:lift', 'yes', AUTHORED),
            Fact('manageable', 'target', 'manageable', 'yes', AUTHORED),
            Fact('permit', 'actor', 'permit', 'no', AUTHORED),
        )
        self.identities = tuple(Identity(s) for s in ('actor', 'target', LOCATION, 'wedge', 'agreement'))
        self.constraints = ()
        self.relationships = ()
        self.calls = []

    def change(self, predicate, value, **changes):
        self.facts = tuple(replace(f, value=value, **changes) if f.predicate == predicate else f for f in self.facts)

    def snapshot(self):
        snapshot = InformationSnapshot((Foundation('foundation', 'setting', 'era', self.identities,
            self.facts, self.relationships, self.constraints),))
        owner = self
        class Access:
            def identity(self, subject):
                owner.calls.append(('identity', subject))
                return snapshot.identity(subject)
            def resolve(self, query):
                owner.calls.append(('resolve', query.subjects))
                return snapshot.resolve(query)
            def applicable_constraints(self, query):
                owner.calls.append(('constraints', query.subjects))
                return snapshot.applicable_constraints(query)
            def for_character(self, *args):
                return snapshot.for_character(*args)
        return Access()

    def ward(self):
        self.constraints = (Constraint(HIDDEN, (LOCATION,), ('open',), BindingTerms(
            ('block',), exceptions=('fact=actor|permit|yes',),
            termination=('fact=actor|permit|yes',)), AUTHORED),)

    def agreement(self):
        self.constraints = (Constraint('agreement-terms', ('agreement',), ('open',),
            BindingTerms(('obligation=return the wedge',)), AUTHORED),)


def methods():
    return (Method('lift', 'open', 'lift', ('wedge',), (('wedge', 1),),
        requirements=('fact=target|manageable|yes',), mechanic='d6', duration=2,
        observations=(('full', 'You lift the obstruction and establish an opening.'),
                      ('partial', 'You establish a foothold but leave the obstruction in place.'),
                      ('failure', 'The obstruction does not move.'),
                      ('blocked', 'You cannot complete the chosen lift.'))),
        Method('use', 'open', 'lift', requirements=('fact=gap|usable|yes',),
            observations=(('full', 'You pass through the established opening.'),
                          ('partial', 'You remain partway through.'),
                          ('failure', 'You remain at the opening.'),
                          ('blocked', 'You cannot use this opening.'))),
        Method('depart', 'open', 'lift', requirements=('commitment=agreement-terms|return the wedge',)),
        Method('remove', 'open', 'lift', operation='end_binding'))


def engine(premises=None, *, effects=(), draw=None, grants=(), method_rules=None):
    premises = premises or Premises()
    return GameEngine(REGION, consequence_config=Config(premises.snapshot,
        methods() if method_rules is None else method_rules, 'actor',
        (('target', tuple(m.id for m in (methods() if method_rules is None else method_rules))), ('gap', ('use',))),
        (('actor', 'wedge', 1),),
        grants, effects, draw or (lambda: 6)))


def request(identity='increment-1', **changes):
    return replace(Request(identity, 'actor', 'open', 'target', 'lift', ('wedge',)), **changes)
