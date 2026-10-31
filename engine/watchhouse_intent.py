"""Finite Watchhouse-owned V1 binding, delegating all mechanics to installed owners.

The public vocabulary names supported meanings, not internal commands. Unknown
descriptions fail closed. This is deliberately not a general language interpreter.
"""
from dataclasses import replace
import re

from engine.activity_control import ActivityCheckpoint
from engine.domain_activity import effective_scope
from engine.domain_campaign import Increment, prior
from engine.domain_dispatch import CoordinatedDomain
from engine.gameplay_coordination import Coordinator, DomainStep, Interpretation, SituatedContext, Target
from engine.watchhouse import OPENING, WatchhouseSession
from engine.watchhouse_domain import DOMAIN, TARGETS, knowledge, permitted, units


ACTIVITIES = {"ask for account": "report", "request ledger access": "access",
              "request ledger surrender": "remove", "search ledger for physical signs": "search",
              "study ledger notation": "study"}
METHODS = {"persuasion": "persuasion", "explain investigation": "persuasion",
           "claim to be an inspector": "deception", "threaten to report her": "intimidation",
           "perform a song": "performance", "physical examination": "perception",
           "decipher notation": "investigation"}
TARGET_NAMES = {"mara": "custodian", "custodian": "custodian", "the custodian": "custodian",
                "ledger": "dispatch-ledger", "the ledger": "dispatch-ledger",
                "dispatch ledger": "dispatch-ledger", "the dispatch ledger": "dispatch-ledger",
                "dispatch-ledger": "dispatch-ledger", "the dispatch-ledger": "dispatch-ledger",
                "ledger notation": "dispatch-ledger", "dispatch ledger notation": "dispatch-ledger",
                "the dispatch ledger notation": "dispatch-ledger",
                "the ledger notation": "dispatch-ledger", "dispatch notation": "dispatch-ledger",
                "the dispatch notation": "dispatch-ledger"}
CAPABILITIES = ("Supported meanings include asking Mara for her account, requesting permission to examine "
    "the dispatch ledger, requesting its surrender, searching it for physical evidence, and studying its notation. "
    "Describe player meaning naturally; targets and methods may be stated within the activity. "
    "Mara/the custodian and the dispatch ledger (dispatch-ledger) are the installed targets. "
    "Supported chosen approaches include persuasion, explaining an investigation, claiming to be an inspector, "
    "threatening to report her, performing a song, physical examination and deciphering notation. "
    "Routine asking for an account needs no special approach. Do not invent a lie, threat, song, "
    "promise or approach. Generic ledger examination does not choose physical search versus notation study: "
    "preserve it as general examination or material ambiguity. Keep all restrictions/conditions/stops. "
    "Inquiry about possibilities remains uncommitted. Unsupported activities remain unsupported descriptions.")


def _key(text):
    return " ".join(text.casefold().strip().rstrip(".").split())


# Full descriptions, not keyword searches: a lie, promise, extra action or
# boundary in an unmatched suffix must never disappear during binding.
_MARA = r"(?:mara|(?:the )?custodian)"
_LEDGER = r"(?:the )?(?:dispatch[- ]ledger|ledger)"
_NOTATION = r"(?:the )?(?:ledger|dispatch(?: ledger)?) notation"
_APPROACH = r"(?:persuasion|explaining (?:my |the )?investigation|claiming i am an inspector|threatening to report her|performing a song)"
_PATTERNS = (
    ("report", rf"ask {_MARA} (?:for her account|what she knows(?: about (?P<subject>(?:the )?(?:missing )?dispatch))?)", None),
    ("access", rf"persuade {_MARA} to (?:let me examine {_LEDGER}|grant (?:me )?ledger access)", "persuasion"),
    ("access", rf"(?:request|ask for) (?:ledger access|(?:permission|access) to examine {_LEDGER}|access to {_LEDGER})(?: by (?P<approach>{_APPROACH}))?", None),
    ("remove", rf"persuade {_MARA} to surrender {_LEDGER}", "persuasion"),
    ("remove", rf"request (?:ledger surrender|surrender of {_LEDGER})", None),
    ("search", rf"(?:search|examine|inspect) {_LEDGER} for (?:physical signs(?: of tampering)?|signs of tampering|physical evidence(?: of tampering)?)", None),
    ("study", rf"(?:study|decipher|examine) {_NOTATION}", None),
)
_METHOD_ALIASES = {
    "explain my investigation": "persuasion", "explaining my investigation": "persuasion",
    "explaining the investigation": "persuasion", "explaining investigation": "persuasion",
    "claiming i am an inspector": "deception", "threatening to report her": "intimidation",
    "performing a song": "performance",
}


def _activity(text):
    text = _key(text)
    if text.startswith("i "):
        text = text[2:]
    if text in ACTIVITIES:
        action = ACTIVITIES[text]
        return action, action != "report", None, None
    for action, pattern, method in _PATTERNS:
        match = re.fullmatch(pattern, text)
        if match:
            approach = match.groupdict().get("approach")
            return action, True, _METHOD_ALIASES.get(approach, approach) if approach else method, match.groupdict().get("subject")
    return None, False, None, None


def _method(text, action):
    text = _key(text)
    if action == "report":
        # An explicit tactical method cannot be inferred from ordinary asking.
        return "persuasion" if text in {"ordinary questioning", "ask directly", "ask mara directly",
                                         "ask the custodian directly", "politely ask"} else None
    method = METHODS.get(text) or _METHOD_ALIASES.get(text)
    if method is not None:
        return method
    if action == "search" and (text in {"perception", "search for physical evidence"}
                              or re.fullmatch(rf"search {_LEDGER}", text)):
        return "perception"
    if action == "study" and text in {"investigation", "study notation", "deciphering notation"}:
        return "investigation"
    return None


def bind_meaning(item, context):
    """Read-only Watchhouse meaning/grounding check, also used by diagnostics.

    A proposal is not an execution permit. Coordinator retains commitment and
    every boundary; installed owners/F05 must still authorize and accept it.
    """
    action, embedded_target, activity_method, subject = _activity(item["activity"])
    if action is None:
        return "unsupported_activity", None
    targets = [TARGET_NAMES.get(_key(t)) for t in item.get("targets", ())]
    if action == "report" and subject is not None:
        # The dispatch is the topic of testimony, never a second action target.
        topic = _key(subject).removeprefix("the ")
        targets = ["subject" if _key(t).removeprefix("the ") == topic else target
                   for t, target in zip(item.get("targets", ()), targets)]
    # Access/surrender can name both the custodian and the object of the request.
    allowed = ({"custodian", "dispatch-ledger"} if action in {"access", "remove"} else
               {"custodian", "subject"} if action == "report" and subject is not None else {TARGETS[action]})
    if any(t not in allowed for t in targets) or not (targets or embedded_target):
        return "unsupported_target", None
    supported = [t for t in context.targets if (t.activity, t.ref) == (action, TARGETS[action])]
    if len(supported) != 1:
        return "unavailable_activity", None
    method = _method(item["method"], action) if "method" in item else activity_method
    if "method" in item and method is None:
        return "unsupported_method", None
    if activity_method is not None and method != activity_method:
        return "conflicting_method", None
    if method is None:
        method = {"report": "persuasion", "search": "perception", "study": "investigation"}.get(action)
    if method is not None and method not in supported[0].methods:
        return "method_not_supported_for_activity", None
    reason = "missing_method" if method is None else "compatible"
    return reason, Interpretation(action, item["activity"], TARGETS[action], method)


class WatchhouseIntentDomain:
    def __init__(self, session, *, request_id=None):
        self.session, self.runtime, self.request_id = session, session.runtime, request_id
        self.bound = None
        self.historical = None

    def context(self):
        root = self.runtime.campaign
        scopes = tuple(effective_scope(root, a.id) for a in root.activities if a.domain == DOMAIN)
        visible = {"watchhouse": OPENING, "capabilities": CAPABILITIES,
                   "access": "Ledger examination is permitted under supervision." if permitted(root)
                   else "Ledger examination requires permission; it is not established."}
        for i, text in enumerate(knowledge(root)[-16:]):
            visible[f"finding:{i}"] = text
        for scope in scopes:
            for ref, text in scope.notices:
                if ref in visible and visible[ref] != text:
                    raise ValueError("conflicting notice")
                visible[ref] = text
        for u in units(root):
            visible["recorded:" + u.command.activity] = "Previously: " + " ".join(
                dict(u.receipt.accessible)[r] for r in u.receipt.public_refs) + " No new attempt is recorded."
        targets = tuple(Target(TARGETS[action], (TARGETS[action],), action,
            tuple(a.authorization.method for a in scopes if a.payload[1] == action))
            for action in dict.fromkeys(a.payload[1] for a in scopes))
        return SituatedContext(str(root.revision), dict(root.current.world.positions)[root.actor],
                               targets=targets, accessible=tuple(visible.items()))

    def bind_intent(self, handoff):
        self.bound = self.historical = None
        if handoff.context != self.context():
            return None
        value = handoff.interpretation.to_dict()
        if len(value["intentions"]) != 1 or value["ambiguities"]:
            return None
        item = value["intentions"][0]
        if item["mode"] == "statement":
            return None
        _, proposal = bind_meaning(item, handoff.context)
        if proposal is None:
            return None
        intent = "inquiry" if item["mode"] == "inquiry" else "prepare" if item["commitment"] == "none" else "commit"
        proposal = replace(proposal, intent=intent, constraints=tuple(item.get("constraints", ())),
                           conditions=tuple(item.get("conditions", ())), stop_at=tuple(item.get("stop_at", ())))
        action, method = proposal.activity, proposal.method
        if method is None:
            return proposal
        identity = f"watchhouse:{action}:{method}"
        attempt = self.request_id or f"watchhouse-intent:{self.runtime.campaign.revision + 1}"
        if type(attempt) is not str or not attempt.strip():
            return None
        # Reuse established objective recognition; failed urging is not a completed objective.
        old = next((u for u in units(self.runtime.campaign) if u.command.id == attempt), None)
        completed = next((u for u in reversed(units(self.runtime.campaign))
                          if u.command.activity == identity and u.progressed), None)
        command = Increment(attempt, identity, 0)
        if old is None and completed is not None:
            command = completed.command
        self.historical = prior(self.runtime.campaign, command)
        if self.historical is None:
            self.bound = CoordinatedDomain(self.runtime, command)
        return proposal

    def assess(self, undertaking, context):
        if self.historical is not None:
            old = self.historical
            return DomainStep(old.command.id, ActivityCheckpoint(undertaking.ref, undertaking.method, complete=True),
                              (DOMAIN,), public_refs=("recorded:" + old.command.activity,))
        if self.bound is None:
            return None
        step = self.bound.assess(undertaking, context)
        old = prior(self.runtime.campaign, self.bound.command)
        if old is not None:
            step = replace(step, public_refs=("recorded:" + old.command.activity,))
        return step

    def execute(self, undertaking, step, context):
        return self.bound.execute(undertaking, step, context)


class WatchhouseIntentSession:
    """Explicit V1 route. A claimed input never falls back to deterministic parsing."""
    def __init__(self, runtime=None, *, provider, draw=None):
        self.session = WatchhouseSession(runtime, draw=draw)
        self.runtime, self.provider = self.session.runtime, provider

    def coordinator(self, *, request_id=None):
        domain = WatchhouseIntentDomain(self.session, request_id=request_id)
        return Coordinator(domain.context, domain)

    def process(self, text, *, request_id=None):
        return self.coordinator(request_id=request_id).process_intent(text, provider=self.provider)
