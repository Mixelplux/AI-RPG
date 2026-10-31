"""Owner-authorized six-call diagnostics. No gameplay progression or authority."""
import argparse
from contextlib import ExitStack
import json
from pathlib import Path
import re
import sys
import time
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.domain_persistence import export
from engine.local_intent_provider import LocalIntentProvider, LocalInterpretationUnavailable
from engine.player_intent import normalize, request_for, IntentHandoff, InvalidInterpretation
from engine.watchhouse import WatchhouseSession
from engine.watchhouse_intent import WatchhouseIntentDomain, bind_meaning

# Same six original inputs. No prompt/schema/provider changes or post-call tuning.
CASES = (
    ("account", "I ask Mara for her account.", "report"),
    ("access", "I persuade Mara to let me examine the ledger.", "access"),
    ("physical-search", "I search the ledger for physical signs of tampering.", "search"),
    ("notation-study", "I study the ledger notation.", "study"),
    ("unsupported", "I cast Charm Person on Mara.", "spell"),
    ("no-promise", "I request ledger access by explaining my investigation, without making a promise.", "access"),
)
# Frozen diagnostic examples, never gameplay matching or a general interpreter.
MEANINGS = {
    "report": {"ask for account", "ask mara for her account", "ask the custodian for her account"},
    "access": {"request ledger access", "request permission to examine the ledger", "request access to the ledger",
               "persuade mara to let me examine the ledger", "persuade mara to grant ledger access"},
    "search": {"search ledger for physical signs", "search the ledger for physical signs of tampering",
               "search the ledger for physical evidence", "examine the ledger for signs of tampering"},
    "study": {"study ledger notation", "study the ledger notation", "decipher the ledger notation"},
    "spell": {"cast charm person on mara", "cast charm person"},
}
METHOD_MEANINGS = {"report": {"persuasion", "ordinary questioning", "ask directly", "politely ask"},
    "access": {"persuasion", "explain investigation", "explaining my investigation", "persuade"},
    "search": {"physical examination", "perception", "search for physical evidence"},
    "study": {"decipher notation", "investigation", "study notation"},
    "spell": {"cast charm person", "charm person", "spellcasting"}}
NEGATIVE_PROMISE = {"without making a promise", "without making any promises", "do not make a promise",
                    "no promises", "without promises", "not making any promises"}
# Preserve the research scorer's original target vocabulary independently of
# executable binding aliases. A binder correction must not improve its scores.
FROZEN_TARGET_NAMES = {"mara": "custodian", "custodian": "custodian", "the custodian": "custodian",
    "ledger": "dispatch-ledger", "the ledger": "dispatch-ledger", "dispatch ledger": "dispatch-ledger",
    "the dispatch ledger": "dispatch-ledger", "ledger notation": "dispatch-ledger"}


def key(text):
    return " ".join(text.casefold().strip().rstrip(".").split())


def sanitized(value):
    """Bounded interpretation fields only; exclude unknown/envelope/diagnostic keys."""
    fields = {"id", "mode", "commitment", "activity", "goal", "targets", "method", "source",
              "constraints", "conditions", "stop_at", "context_refs", "candidate_domains"}
    def text(v):
        if re.search(r"sk-|bearer\s|api[_ -]?key|password|secret|credential|https?://[^/\s]+@", v, re.I):
            return "[REDACTED]"  # Entire string, never partially disclose a credential.
        return "".join(c for c in v if ord(c) >= 32 or c in "\n\t").encode("utf-8", "replace").decode("utf-8")[:1024]
    def item(v, allowed):
        if type(v) is not dict:
            return {"diagnostic": "wrong_object_type"}
        result = {}
        for k in sorted(allowed & v.keys()):
            x = v[k]
            if type(x) is str:
                result[k] = text(x)
            elif type(x) is list:
                result[k] = [text(s) if type(s) is str else "[WRONG_TYPE]" for s in x[:16]]
        return result
    result = {}
    if type(value) is dict:
        for name, allowed, limit in (("intentions", fields, 8),
                ("relationships", {"type", "from", "to"}, 32),
                ("ambiguities", {"intentions", "issue"}, 8)):
            if type(value.get(name)) is list:
                result[name] = [item(v, allowed) for v in value[name][:limit]]
    return result


def structural_reason(raw, request):
    """Explanation only after V1 rejection; not an alternative validator."""
    if type(raw) is not str or len(raw.encode("utf-8", "replace")) > 32768:
        return "output_type_or_size", None
    duplicate = False
    def pairs(entries):
        nonlocal duplicate
        d = {}
        for k, v in entries:
            duplicate |= k in d
            d[k] = v
        return d
    try:
        v = json.loads(raw, object_pairs_hook=pairs)
    except (ValueError, RecursionError):
        return "json_syntax", None
    if duplicate:
        return "duplicate_json_key", v
    if type(v) is not dict or set(v) != {"version", "intentions", "relationships", "ambiguities"}:
        return "top_level_fields", v
    if type(v["version"]) is not int or v["version"] != 1:
        return "version", v
    for field, limit in (("intentions", 8), ("relationships", 32), ("ambiguities", 8)):
        if type(v[field]) is not list or len(v[field]) > limit:
            return "collection_type_or_bound", v
    ids = set()
    for i in v["intentions"]:
        if type(i) is not dict or not {"id", "mode", "commitment", "activity"} <= i.keys():
            return "intention_required_fields", v
        if any(type(i[k]) is not str for k in ("id", "mode", "commitment", "activity")):
            return "intention_field_type", v
        if i["id"] in ids:
            return "duplicate_intention_id", v
        ids.add(i["id"])
        if i["mode"] not in {"inquiry", "statement", "preparation", "action"} or i["commitment"] not in {"none", "now", "conditional"}:
            return "mode_or_commitment_enum", v
        if (i["mode"] in {"inquiry", "statement"} and i["commitment"] != "none"
                or i["mode"] == "action" and i["commitment"] == "none"
                or i["commitment"] == "now" and i.get("conditions")
                or i["commitment"] == "conditional" and not i.get("conditions")):
            return "commitment_condition_consistency", v
        refs = i.get("context_refs", [])
        if type(refs) is list and any(type(r) is not str or r not in dict(request.context) for r in refs):
            return "unknown_context_reference", v
        if "source" in i and (type(i["source"]) is not str or i["source"] not in request.player_input):
            return "source_not_verbatim", v
    return "other_v1_constraint", v


def semantic_checks(value, action, *, no_promise=False, conditions=(), relationships=(), count=1):
    """Binding-independent finite checks; unfamiliar phrasing requires human review."""
    items = value["intentions"]
    checks = {"intention_count": "pass" if len(items) == count else "fail"}
    if len(items) != count or not items:
        return dict(status="incorrect", checks=checks)
    i = items[0]
    checks["mode"] = "pass" if all(x["mode"] == "action" for x in items) else "fail"
    checks["commitment"] = "pass" if all(x["commitment"] == ("conditional" if conditions else "now") for x in items) else "fail"
    activity = key(i["activity"])
    checks["activity_meaning"] = ("pass" if activity in MEANINGS[action] else
        "fail" if any(activity in examples for a, examples in MEANINGS.items() if a != action) else "review")
    target = "custodian" if action in {"report", "access", "spell"} else "dispatch-ledger"
    targets = i.get("targets", [])
    checks["target_meaning"] = "pass" if len(targets) == 1 and FROZEN_TARGET_NAMES.get(key(targets[0])) == target else "review"
    method = key(i["method"]) if "method" in i else None
    checks["method_meaning"] = ("pass" if method in METHOD_MEANINGS[action] else
        "pass" if method is None and action in {"report", "search", "study"} and checks["activity_meaning"] == "pass" else "review")
    constraints = tuple(key(s) for s in i.get("constraints", []))
    checks["restriction_polarity"] = ("pass" if len(constraints) == 1 and constraints[0] in NEGATIVE_PROMISE else
        "fail" if not constraints or constraints == ("make a promise",) else "review") if no_promise else (
        "pass" if not constraints else "review")
    checks["conditions_and_polarity"] = "pass" if tuple(key(s) for s in i.get("conditions", [])) == tuple(key(s) for s in conditions) else "review"
    checks["stopping_boundaries"] = "pass" if not i.get("stop_at") else "review"
    mapping = {x["id"]: n for n, x in enumerate(items)}
    actual = {(r["type"], mapping[r["from"]], mapping[r["to"]]) for r in value["relationships"]}
    checks["relationships_and_direction"] = "pass" if actual == set(relationships) else "fail"
    checks["material_ambiguity"] = "pass" if not value["ambiguities"] else "review"
    status = "incorrect" if "fail" in checks.values() else "requires_review" if "review" in checks.values() else "matches_frozen_checks"
    return dict(status=status, checks=checks, limitation="Finite checks; human semantic review remains required.")


def binding_probe(domain, validated, text, context):
    """Probe current Watchhouse binding only, never authorization or execution.

    Semantic scoring stays independent and frozen. Historical evidence is not
    rescored; this probe shares only the current owning adapter's grounding.
    """
    value = validated.to_dict()
    if len(value["intentions"]) != 1 or value["ambiguities"]:
        return dict(category="not_probed_count_or_ambiguity")
    i = value["intentions"][0]
    if context != domain.context():
        return dict(category="stale_context")
    if i["mode"] == "statement":
        return dict(category="statement_no_authorization", runtime_route="statement_no_authorization", proposal=None)
    reason, expected = bind_meaning(i, context)
    try:
        proposal = domain.bind_intent(IntentHandoff(validated, text, context))
    except Exception:
        return dict(category="binder_exception")
    if (proposal is None) != (expected is None):
        return dict(category="diagnostic_binder_disagreement")
    route = "statement_no_authorization" if i["mode"] == "statement" else "uncommitted" if i["commitment"] == "none" else "requires_coordinator_and_domain"
    return dict(category=reason, runtime_route=route, proposal=None if proposal is None else
                dict(activity=proposal.activity, target=proposal.target, method=proposal.method))


def diagnostic_case(provider, case):
    name, text, action = case
    def forbidden(*args, **kwargs):
        raise AssertionError("Diagnostic execution forbidden")
    session = WatchhouseSession(draw=forbidden)
    runtime = session.runtime
    original, encoded = runtime.campaign, export(runtime.campaign)
    domain = WatchhouseIntentDomain(session)
    context = domain.context()
    request = request_for(text, context)
    record = dict(case=name, input=text, expected_action=action, interpretation=None,
                  structural=dict(valid=False, category="unavailable"), semantic=None, binding=None, executed=False)
    start = time.monotonic()
    with ExitStack() as guards:
        for method in ("prepare_increment", "accept_increment", "process_increment", "prepare_activity_change"):
            guards.enter_context(patch.object(runtime, method, side_effect=forbidden))
        for method in ("assess", "execute"):
            guards.enter_context(patch.object(domain, method, side_effect=forbidden))
        try:
            raw = provider(request)  # Exactly one call. No Coordinator/progression path.
            record["operational"] = dict(getattr(provider, "last_diagnostic", None) or {"category": "completion_received"})
            try:
                validated = normalize(raw, context_ids=tuple(k for k, _ in request.context), player_input=text)
            except InvalidInterpretation:
                reason, decoded = structural_reason(raw, request)
                record["structural"]["category"] = reason
                record["operational"]["v1_valid"] = False
                record["interpretation"] = sanitized(decoded)
            else:
                value = validated.to_dict()
                record["operational"]["v1_valid"] = True
                record.update(interpretation=sanitized(value), structural=dict(valid=True, category="valid_v1"),
                    semantic=semantic_checks(value, action, no_promise=name == "no-promise"),
                    binding=binding_probe(domain, validated, text, context))
        except LocalInterpretationUnavailable as error:
            record["structural"]["category"] = "provider_unavailable"
            record["operational"] = dict(error.diagnostic)
        except Exception:
            record["structural"]["category"] = "diagnostic_exception"
    if runtime.campaign is not original or export(runtime.campaign) != encoded:
        raise AssertionError("Diagnostic campaign mutation")
    record.update(state_unchanged=True, latency_seconds=round(time.monotonic() - start, 3))
    return record


def private_evidence(record):
    """Metadata-only persisted view: no input, source, context or response text.

    Descriptive fields may be examined in memory by diagnostic checks but never
    cross this evidence boundary. Preserve existing earlier evidence unchanged.
    """
    result = {k: record[k] for k in ("structural", "semantic", "binding", "operational",
              "executed", "state_unchanged", "latency_seconds") if k in record}
    result["case"] = record["case"] if record["case"] in {c[0] for c in CASES} else "verification"
    projected = record.get("interpretation") or {}
    items = projected.get("intentions", [])
    result["interpretation_summary"] = {"count": len(items), "items": [dict(
        mode=i.get("mode") if i.get("mode") in {"action", "inquiry", "statement", "preparation"} else "invalid_or_absent",
        commitment=i.get("commitment") if i.get("commitment") in {"now", "none", "conditional"} else "invalid_or_absent",
        targets_count=len(i.get("targets", [])), constraints_count=len(i.get("constraints", [])),
        conditions_count=len(i.get("conditions", [])), stops_count=len(i.get("stop_at", [])),
        method_present="method" in i, source_present="source" in i) for i in items]}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--enable-local-diagnostic", action="store_true")
    parser.add_argument("--model", required=True)
    args = parser.parse_args()
    if not args.enable_local_diagnostic or args.model != "qwen3.5-2b":
        parser.error("Six-call diagnostic requires explicit flag and unchanged qwen3.5-2b model")
    path = Path(".artifacts/intent-diagnostic-v1/six-case-evidence.jsonl")
    with path.open("x", encoding="utf-8") as evidence:
        provider = LocalIntentProvider(model=args.model, timeout=30)
        for case in CASES:
            record = diagnostic_case(provider, case)
            evidence.write(json.dumps(private_evidence(record), ensure_ascii=True) + "\n")
            evidence.flush()
            print(json.dumps(dict(case=record["case"], structural=record["structural"],
                semantic=record["semantic"]["status"] if record["semantic"] else None,
                binding=record["binding"], state_unchanged=record["state_unchanged"])), flush=True)
            if record["structural"]["category"] in {"provider_unavailable", "diagnostic_exception"}:
                break  # Stop environmental failures, never retry.


if __name__ == "__main__":
    main()
