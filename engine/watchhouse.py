"""Bounded natural-language entry point for the Watchhouse investigation.

No provider, command queue, inferred promises, offscreen developments or legacy
GameEngine state. Unknown or compound instructions return player control.
"""
import re
from dataclasses import dataclass

from engine.activity_control import ActivityAuthorization, ActivityCheckpoint
from engine.character_rules import CreatureRules
from engine.domain_campaign import Campaign, ActivityScope, ActivityStage, Increment, Domains
from engine.game_session import GameSession
from engine.physical_world import PhysicalFrame, Place, PhysicalObject, PhysicalRelation
from engine.watchhouse_domain import DOMAIN, WATCHHOUSE, METHODS, TARGETS, knowledge, units
from engine.watchhouse_rules import INVESTIGATOR, validate_profile


@dataclass(frozen=True)
class Reply:
    status: str
    message: str


def new_campaign(*, profile=INVESTIGATOR, intelligence=12, attitude='indifferent'):
    """Authored bootstrap; scoped skill facts are owned Character inputs.

    All scopes share the same explicit immutable Character/NPC premises. They
    reside in existing inert owner payloads, not new save fields or a new schema.
    """
    validate_profile(profile)
    world = PhysicalFrame('watchhouse:world:0', 0, (Place('watchhouse', 'town'),),
        ('investigator', 'custodian'), (('investigator', 'watchhouse'), ('custodian', 'watchhouse')),
        objects=(PhysicalObject('dispatch-ledger', 'bound dispatch ledger', True),),
        relationships=(PhysicalRelation('dispatch-ledger', 'located', 'watchhouse', 'custodial desk'),))
    characters = tuple(CreatureRules(actor, None, None, None, None, None) for actor in world.creatures)
    state = Domains(world, 'watchhouse:character:0', characters)
    scopes = []
    for action, methods in METHODS.items():
        for method in methods:
            identity = f'watchhouse:{action}:{method}'
            scopes.append(ActivityScope(identity, 'investigator', DOMAIN, f'{action} at the Watchhouse',
                ActivityAuthorization(identity, method), ActivityCheckpoint(identity, method),
                (ActivityStage(TARGETS[action], ('watchhouse-m1-v1', action, method,
                                               profile, intelligence, attitude)),)))
    return Campaign('watchhouse-m1', 'investigator', state, state, tuple(scopes))


OPENING = ('Mara, the Watchhouse custodian, sits beside a bound dispatch ledger. '
           'The ledger stays at her desk; examination requires her permission. '
           'You can ask for her account, choose an approach to request access, '
           'and examine accessible evidence. What do you do?')
CLARIFY = ('Describe one immediate action and your approach. You retain control '
           'of promises, payments, threats, disclosures and changes of method. '
           'No attempt has been made.')


def interpret(text):
    """Finite, full-utterance patterns: never truncate a consequential suffix."""
    if type(text) is not str or not text.strip():
        return None
    t = ' '.join(text.casefold().strip().rstrip('.?!').split())
    if t in ('look', 'look around', 'where am i'):
        return ('look', None)
    if t in ('what have i learned', 'review my findings', 'review findings'):
        return ('knowledge', None)
    if re.match(r'^(can|could|would|what|how|is|does|may)\b', t):
        return ('inquiry', None)
    if text.strip().endswith('?'):
        return None  # A proposed first-person action is not unambiguous commitment.
    if re.fullmatch(r'(?:i )?ask (?:mara|the custodian) (?:for her account|what she knows about the dispatch)', t):
        return ('report', 'persuasion')
    if re.fullmatch(r'(?:i )?(?:search|examine) (?:the )?ledger for (?:physical signs|signs of tampering)', t):
        return ('search', 'perception')
    if re.fullmatch(r'(?:i )?(?:study|decipher) (?:the )?(?:ledger notation|dispatch notation)', t):
        return ('study', 'investigation')
    verbs = {'persuade': 'persuasion', 'deceive': 'deception', 'intimidate': 'intimidation',
             'entertain': 'performance'}
    m = re.fullmatch(r'(?:i )?(persuade|deceive|intimidate|entertain) (?:mara|the custodian) '
                     r'to (let me examine the ledger|give me her account|surrender the ledger)', t)
    if m:
        action = {'let me examine the ledger': 'access', 'give me her account': 'report',
                  'surrender the ledger': 'remove'}[m[2]]
        # Deception, threats and performance require a specified player-owned
        # approach. No imaginary lie, threat or performance is supplied here.
        return ('clarify-method', None) if m[1] != 'persuade' else (action, verbs[m[1]])
    m = re.fullmatch(r'(?:i )?request permission to examine the ledger by '
                     r'(explaining my investigation|claiming i am an inspector|threatening to report her|performing a song)', t)
    if m:
        return ('access', dict(zip(('explaining my investigation', 'claiming i am an inspector',
            'threatening to report her', 'performing a song'),
            ('persuasion', 'deception', 'intimidation', 'performance')))[m[1]])
    return None


class WatchhouseSession:
    def __init__(self, runtime=None, *, draw=None):
        self.runtime = runtime if runtime is not None else GameSession.start_domains(new_campaign(), draw=draw)
        if not getattr(self.runtime, 'domain_mode', False):
            raise ValueError('explicit Watchhouse campaign required')
        root = self.runtime.campaign
        if (root.schema != 4 or not root.activities
                or any(a.domain != DOMAIN for a in root.activities)):
            raise ValueError('explicit Watchhouse campaign required')

    def process(self, text, *, request_id=None):
        parsed = interpret(text)
        if parsed is None or parsed[0] == 'clarify-method':
            return Reply('clarification', CLARIFY)
        action, method = parsed
        if action == 'look':
            return Reply('observation', OPENING)
        if action == 'knowledge':
            return Reply('knowledge', ' '.join(knowledge(self.runtime.campaign)) or 'No findings have been established yet.')
        if action == 'inquiry':
            return Reply('inquiry', 'No attempt has been made. ' + OPENING)
        identity = f'watchhouse:{action}:{method}'
        if request_id is not None and (type(request_id) is not str or not request_id.strip()):
            return Reply('clarification', CLARIFY)
        attempt = request_id or f'watchhouse-command:{self.runtime.campaign.revision + 1}'
        command = Increment(attempt, identity, 0)
        # Preserve exact identity conflict detection even when an objective has
        # already completed. An automatic historical response is explicitly past.
        old_id = next((u for u in units(self.runtime.campaign) if u.command.id == attempt), None)
        if old_id is None:
            prior = next((u for u in reversed(units(self.runtime.campaign))
                          if u.command.activity == identity and u.progressed), None)
            if prior is not None:
                return Reply('recorded', 'Previously: ' + ' '.join(t for _, t in prior.receipt.accessible)
                             + ' No new attempt or elapsed time is recorded.')
        decision = self.runtime.process_increment(command)
        if decision.status == 'unresolved':
            return Reply('unresolved', 'The action could not be resolved. Established results remain intact.')
        if decision.status == 'clarification':
            # Coordinator exposes only access-qualified notices, never owner
            # diagnostics. Preserve a meaningful pending player-owned choice.
            return Reply('clarification', decision.message + ' No new attempt has been made.')
        return Reply(decision.status, decision.message)
