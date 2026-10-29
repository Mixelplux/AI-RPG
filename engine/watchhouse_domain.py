"""One custodian/ledger investigation over the existing schema-4 owner contract.

Social permission and Character findings are sparse derived views of validated
accepted units, not a second mutable truth store. Primitive payloads are inert.
Versioned authored meaning is deliberately local to this scenario.
"""
from dataclasses import replace

from engine.character_rules import CharacterRules
from engine.domain_campaign import AcceptedUnit, Contribution
from engine.domain_activity import stamp
from engine.gameplay_coordination import AcceptedStep
from engine.information_adjudication import Unresolved
from engine.watchhouse_rules import SOCIAL, validate_profile, check

DOMAIN = 'watchhouse-records-v1'
METHODS = {'report': SOCIAL, 'access': SOCIAL, 'remove': SOCIAL,
           'search': ('perception',), 'study': ('investigation',)}
TARGETS = {'report': 'custodian', 'access': 'custodian', 'remove': 'custodian',
           'search': 'dispatch-ledger', 'study': 'dispatch-ledger'}
DURATIONS = {'report': 60, 'access': 60, 'remove': 60, 'search': 60, 'study': 300}
REPORT = ('Mara says the copied entry records a dispatch sent at dusk. '
          'She did not witness its departure and believes the copy is accurate.')
SEAL = ('You notice the wax impression is broken across the ledger seam. '
        'This is a physical sign of reopening; it does not identify who reopened it.')
STUDY = ('You decipher the dispatch notation: the entry was copied from a later '
         'correction. That suggests the recorded departure time may be unreliable; '
         'it does not establish when the dispatch actually left.')
# Objective authored information and access are deliberately separate. Neither
# this unrevealed fact nor an unspecified culprit is a Character finding.
OBJECTIVE_TRUTH = 'The dispatch left after dusk; Mara did not witness it.'


def units(campaign):
    activity_ids = {a.id for a in campaign.activities if a.domain == DOMAIN}
    return tuple(u for u in campaign.accepted if type(u) is AcceptedUnit
                 and u.command.activity in activity_ids)


def permitted(campaign):
    return any(u.evidence[1:3] == ('access', True) for u in units(campaign))


def knowledge(campaign):
    """Only previously accepted, Character-safe observations/attributed claims."""
    return tuple(text for u in units(campaign) for _, text in u.receipt.accessible)


def plan(scope):
    return scope.payload


def willingness(action, method):
    # Mara's duty is custody; she wants accurate public records, but cannot
    # surrender the ledger. Bullying her violates those duties. No attitude meter
    # or persuasion roll can manufacture her witnessing an unseen departure.
    if action == 'remove' or method == 'intimidation':
        return 'unwilling'
    return 'willing' if action == 'report' else 'hesitant'


class WatchhouseDomain:
    id = DOMAIN

    def validate_scope(self, campaign, scope):
        if len(scope.stages) != 1 or scope.actor != 'investigator':
            raise ValueError('bounded Watchhouse scope')
        p = scope.payload
        if type(p) is not tuple or len(p) != 6:
            raise ValueError('Watchhouse v1 declaration')
        version, action, method, profile, intelligence, attitude = p
        if (version != 'watchhouse-m1-v1' or action not in METHODS or method not in METHODS[action]
                or scope.target != TARGETS[action] or scope.authorization.method != method
                or scope.id != f'watchhouse:{action}:{method}'
                or type(intelligence) is not int or not 1 <= intelligence <= 30
                or attitude not in ('friendly', 'indifferent', 'hostile')):
            raise ValueError('Watchhouse method, identity or premises')
        validate_profile(profile)
        for other in campaign.activities:
            if other.domain == DOMAIN and (len(other.stages) != 1 or len(other.payload) != 6
                    or other.payload[3:] != p[3:]):
                raise ValueError('consistent Character/NPC premises required')
        w = campaign.origin.world
        if (not {'custodian', scope.actor}.issubset(w.creatures)
                or not any(o.id == 'dispatch-ledger' and o.intact is True for o in w.objects)
                or not any(r.object == 'dispatch-ledger' and r.kind == 'located'
                           and r.target == 'watchhouse' for r in w.relationships)):
            raise ValueError('grounded custodian and ledger required')

    def validate_command(self, campaign, command, scope):
        if command.payload:
            raise ValueError('Watchhouse methods come from authorized scope')

    def means(self, command):
        return ()

    def assess(self, campaign, command, scope, *, execution):
        self.validate_command(campaign, command, scope)
        _, action, method, _, _, _ = plan(scope)
        w = campaign.current.world
        positions = dict(w.positions)
        if positions.get(scope.actor) != 'watchhouse' or positions.get('custodian') != 'watchhouse':
            raise Unresolved('eligibility', 'watchhouse_not_accessible')
        if not any(o.id == 'dispatch-ledger' and o.intact is True for o in w.objects):
            raise Unresolved('eligibility', 'ledger_unavailable')
        profiles = CharacterRules(campaign.current.character_revision, campaign.current.characters)
        for actor in (scope.actor, 'custodian'):
            c = profiles.creature(actor)
            # This scenario has no supported additional ongoing rule effects.
            if c.conditions or c.unresolved_rules or c.exhaustion >= 6 or c.vitality and c.vitality.dead:
                raise Unresolved('rules', 'watchhouse_character_effect_unavailable')
        if action in ('search', 'study') and not permitted(campaign):
            raise Unresolved('eligibility', 'ledger_permission_required')
        if action == 'access':
            for u in units(campaign):
                old = next(a for a in campaign.activities if a.id == u.command.activity)
                if (old.payload[1:3] == (action, method) and u.evidence[2] is False
                        and w.at_seconds < u.evidence[3] + 86400):
                    raise Unresolved('eligibility', 'same_urging_wait_24_hours')

    def requires_check(self, campaign, scope):
        _, action, method, _, _, _ = plan(scope)
        return action in ('search', 'study') or (action == 'access'
            and willingness(action, method) == 'hesitant')

    def prepare(self, campaign, command, scope, draw):
        rolls = ()
        if self.requires_check(campaign, scope):
            attitude = scope.payload[5]
            count = 2 if scope.payload[2] in SOCIAL and attitude != 'indifferent' else 1
            rolls = tuple(draw(20) for _ in range(count))
        return self.evaluate(campaign, command, scope, (rolls, scope.payload[1], None, None), preparing=True)

    def evaluate(self, campaign, command, scope, evidence, *, preparing=False):
        self.assess(campaign, command, scope, execution=True)
        if type(evidence) is not tuple or len(evidence) != 4 or type(evidence[0]) is not tuple:
            raise ValueError('Watchhouse result evidence')
        if not preparing and (type(evidence[1]) is not str or type(evidence[2]) is not bool
                              or type(evidence[3]) is not int):
            raise ValueError('typed Watchhouse evidence required')
        _, action, method, profile, intelligence, attitude = plan(scope)
        rolls = evidence[0]
        if self.requires_check(campaign, scope):
            c = next(c for c in campaign.current.characters if c.id == scope.actor)
            dc = max(15, intelligence) if action == 'access' else 12 if action == 'search' else 13
            success = check(profile, method, dc, rolls, attitude, c.exhaustion)
        else:
            if rolls:
                raise ValueError('unexpected Watchhouse roll')
            success = action in ('report', 'access', 'remove') and willingness(action, method) == 'willing'
        at = campaign.current.world.at_seconds
        expected = (rolls, action, success, at)
        if not preparing and evidence != expected:
            raise ValueError('Watchhouse result/permission/history mismatch')
        if action == 'report':
            text = REPORT if success else 'Mara refuses to answer that approach. No testimony is established.'
        elif action == 'access':
            text = ('Mara allows you to examine the dispatch ledger here under her supervision. '
                    'She keeps custody of it.') if success else (
                    'Mara refuses access. The ledger remains in her custody. '
                    + ('She will not reconsider the same urging for 24 hours.' if rolls else ''))
        elif action == 'remove':
            text = 'Mara refuses to surrender the ledger: keeping the record here is her duty.'
        elif action == 'search':
            text = SEAL if success else 'You examine the accessible ledger but discern no additional physical sign.'
        else:
            text = STUDY if success else 'You study the accessible notation but cannot establish its meaning.'
        seconds = DURATIONS[action]
        current = replace(campaign.current, world=replace(campaign.current.world, at_seconds=at + seconds))
        current = stamp(campaign, current, command, scope)
        text += f' {seconds} seconds pass.'
        receipt = AcceptedStep(command.id, ('watchhouse-result',), 'complete', (('watchhouse-result', text),))
        # A completed examination can fail to find something. Influence failure
        # retains its cooldown while allowing a later, legitimately new attempt.
        progressed = success or action in ('search', 'study', 'remove')
        return Contribution(current, expected, progressed, receipt)

    def initial_choices(self, campaign, scope):
        return ()

    def decision_basis(self, campaign, scope, index):
        return (scope.stages[index].payload, permitted(campaign), campaign.current.characters)

    def update(self, campaign, event, scope):
        if event.payload or event.stage is not None:
            raise ValueError('Watchhouse owner facts cannot be rewritten by activity control')
        return campaign.current


WATCHHOUSE = WatchhouseDomain()
