"""Model-independent V1 meaning, never gameplay authorization or world truth.

Only JSON text crosses the untrusted output seam. Canonical JSON is kept as an
immutable value; callers receive fresh decoded copies. No provider is installed,
selected, retried or called implicitly by this module.
"""
from dataclasses import dataclass
import json
import re


MAX_OUTPUT_BYTES = 32768
MAX_INPUT_CHARS = 8192
MAX_INTENTIONS = 8
MAX_RELATIONSHIPS = 32
MAX_AMBIGUITIES = 8
MAX_ITEMS = 16
MAX_TEXT = 1024
DOMAINS = frozenset({"world", "character", "resolution", "actors"})
RELATIONSHIPS = frozenset({"precedes", "depends_on", "alternative", "together", "independent"})
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}\Z")
_REQUIRED = {"id", "mode", "commitment", "activity"}
_TEXTS = {"goal", "method", "source"}
_LISTS = {"targets", "constraints", "conditions", "stop_at", "context_refs", "candidate_domains"}

INSTRUCTIONS = """Identify player meaning only. Return one JSON object, no prose or code fence:
{"version":1,"intentions":[],"relationships":[],"ambiguities":[]}.
Each intention requires id (unique ASCII identifier), mode (inquiry, statement,
preparation, action), commitment (none, now, conditional), activity (natural text).
Optional goal/method/source are nonempty strings; source is a verbatim excerpt of
the player input. Optional targets/constraints/conditions/stop_at/context_refs/
candidate_domains are arrays of unique nonempty strings. Null is never allowed.
context_refs may use only supplied context ids. candidate_domains may contain
world, character, resolution, actors; these are advisory, never final routing.
Relationships are {"type":TYPE,"from":ID,"to":ID}; TYPE is precedes,
depends_on, alternative, together, independent. Ambiguities are
{"intentions":[ID,...],"issue":"material unresolved meaning"}; [] means global.
Inquiry/statement have commitment none. Action has now or conditional.
Preparation may have none, now or conditional. Conditional commitment requires
conditions. Now cannot have conditions: express such authorization as conditional.
Inquiry/statement may carry hypothetical conditions without authorizing action.
Preserve affirmatively requested acts, methods, restrictions and stop boundaries.
In-world questioning is an action when the player commits to speaking to an NPC.
Omissions do not imply prohibitions: running toward a cart does not forbid arrival.
Use proportionate specificity: examining a ledger need not name its hidden parts.
Preserve separate intentions and their expressed relationships, never an execution
queue. Preserve continuation/retry meaning and supplied references without deciding
whether prior mechanics repeat. Do not invent methods, references, prerequisites,
permissions, facts, NPC decisions, costs, checks, outcomes or narration. Material
ambiguity is about meaning; domain information gaps need not make intent ambiguous.
Domains discover their own dependencies; any suggested gaps are not exhaustive.
At most 8 intentions, 32 relationships, 8 ambiguities, 16 strings per optional
array, 1024 characters per text, 64 per id, 32768 UTF-8 bytes total.
"""


class InvalidInterpretation(ValueError):
    """Technical structural rejection, never a fictional failure."""


def _reject():
    # Do not echo untrusted output, hidden context or provider diagnostics.
    raise InvalidInterpretation("Invalid V1 interpretation")


def _text(value, limit=MAX_TEXT):
    if type(value) is not str or not value.strip() or len(value) > limit:
        _reject()
    try:
        value.encode("utf-8")
    except UnicodeError:
        _reject()
    if any(ord(c) < 32 and c not in "\n\r\t" for c in value):
        _reject()
    return value.strip()


def _identifier(value):
    if type(value) is not str or not _ID.fullmatch(value):
        _reject()
    return value


def _strings(value, *, limit=MAX_ITEMS, identifier=False):
    if type(value) is not list or len(value) > limit:
        _reject()
    result = [(_identifier(v) if identifier else _text(v)) for v in value]
    if len(set(result)) != len(result):
        _reject()
    return result


def _object(value, required, optional=frozenset()):
    if type(value) is not dict or not required <= value.keys() or value.keys() - required - optional:
        _reject()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _reject()
        result[key] = value
    return result


def _constant(value):
    _reject()


@dataclass(frozen=True)
class InterpretationV1:
    """Immutable canonical representation; construction alone grants no trust."""
    json: str

    def to_dict(self):
        return json.loads(self.json)


def normalize(raw, *, context_ids=(), player_input=None):
    """Strict bounded JSON -> canonical V1. No inferred methods or semantic repair.

    Unknown fields at every level are rejected (including executable/outcome
    fields). Free text is a description of intent, never an accepted fact.
    Structural validation cannot certify that the model understood the player.
    """
    if type(raw) is not str:
        _reject()
    try:
        if len(raw) > MAX_OUTPUT_BYTES or len(raw.encode("utf-8")) > MAX_OUTPUT_BYTES:
            _reject()
        value = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_constant)
    except (ValueError, TypeError, UnicodeError, RecursionError):
        _reject()
    _object(value, {"version", "intentions", "relationships", "ambiguities"})
    if type(value["version"]) is not int or value["version"] != 1:
        _reject()
    for field, bound in (("intentions", MAX_INTENTIONS), ("relationships", MAX_RELATIONSHIPS),
                         ("ambiguities", MAX_AMBIGUITIES)):
        if type(value[field]) is not list or len(value[field]) > bound:
            _reject()
    ids = set()
    for intention in value["intentions"]:
        _object(intention, _REQUIRED, _TEXTS | _LISTS)
        identity = _identifier(intention["id"])
        if identity in ids:
            _reject()
        ids.add(identity)
        if (type(intention["mode"]) is not str
                or intention["mode"] not in {"inquiry", "statement", "preparation", "action"}
                or type(intention["commitment"]) is not str
                or intention["commitment"] not in {"none", "now", "conditional"}):
            _reject()
        intention["activity"] = _text(intention["activity"])
        for field in _TEXTS & intention.keys():
            intention[field] = _text(intention[field])
        for field in _LISTS & intention.keys():
            intention[field] = _strings(intention[field], identifier=field == "context_refs")
        if not set(intention.get("candidate_domains", ())) <= DOMAINS:
            _reject()
        if not set(intention.get("context_refs", ())) <= set(context_ids):
            _reject()
        mode, commitment = intention["mode"], intention["commitment"]
        conditions = intention.get("conditions", ())
        if (mode in {"inquiry", "statement"} and commitment != "none"
                or mode == "action" and commitment == "none"
                or commitment == "conditional" and not conditions
                or commitment == "now" and conditions):
            _reject()
        if "source" in intention and player_input is not None and intention["source"] not in player_input:
            _reject()
    seen, graph, pair_types = set(), {i: set() for i in ids}, {}
    for relation in value["relationships"]:
        _object(relation, {"type", "from", "to"})
        kind, left, right = relation["type"], relation["from"], relation["to"]
        if (type(kind) is not str or kind not in RELATIONSHIPS
                or _identifier(left) not in ids or _identifier(right) not in ids or left == right):
            _reject()
        pair = tuple(sorted((left, right)))
        key = (kind, *(pair if kind in {"alternative", "together", "independent"} else (left, right)))
        if key in seen:
            _reject()
        seen.add(key)
        pair_types.setdefault(pair, set()).add(kind)
        if kind == "precedes":
            graph[left].add(right)
        if kind == "depends_on":
            graph[right].add(left)
    for kinds in pair_types.values():
        if ("alternative" in kinds and kinds & {"precedes", "depends_on", "together"}
                or {"together", "independent"} <= kinds):
            _reject()

    def visit(node, path):
        if node in path:
            _reject()
        for child in graph[node]:
            visit(child, path | {node})
    for node in graph:
        visit(node, set())
    seen = set()
    for ambiguity in value["ambiguities"]:
        _object(ambiguity, {"intentions", "issue"})
        affected = _strings(ambiguity["intentions"], limit=MAX_INTENTIONS, identifier=True)
        if not set(affected) <= ids:
            _reject()
        ambiguity["issue"] = _text(ambiguity["issue"])
        key = (tuple(sorted(affected)), ambiguity["issue"])
        if key in seen:
            _reject()
        seen.add(key)
    return InterpretationV1(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                       separators=(",", ":"), allow_nan=False))


@dataclass(frozen=True)
class InterpretationRequest:
    player_input: str
    context: tuple[tuple[str, str], ...]
    instructions: str = INSTRUCTIONS


@dataclass(frozen=True)
class IntentHandoff:
    interpretation: InterpretationV1
    player_input: str
    context: object  # Original trusted SituatedContext, never the provider's copy.


def request_for(player_input, context):
    """Only the supplied accessible projection crosses the model input seam."""
    _text(player_input, MAX_INPUT_CHARS)
    # Keep the exact original input. No normalization of player wording.
    for ref, text in context.accessible:
        _identifier(ref)
        _text(text, MAX_INPUT_CHARS)
    if len(context.accessible) > 64:
        _reject()
    return InterpretationRequest(player_input, context.accessible)
