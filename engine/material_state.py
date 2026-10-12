"""Optional finite material conditions; existing World State/history own truth.

Three handling operations and one elapsed-time development are supported. This
is not an arbitrary property writer, expression language, or scene simulator.
"""
from copy import deepcopy

from engine import character_competence

STATE_KEY = "material_conditions"
OPERATIONS = {"stabilize", "adjust", "reposition"}
CONSTRAINTS = {"preserve_integrity", "no_talk", "no_move", "no_adjust", "assess_only"}
EVENTS = {"material_preparation", "material_outcome", "material_cooperation", "material_development"}


def declarations(region):
    return region.get("material_targets", [])


def target(region, identity):
    return next((item for item in declarations(region) if item["target_id"] == identity), None)


def validate_declarations(region):
    items = declarations(region)
    if not isinstance(items, list):
        raise ValueError("material_targets must be a list.")
    locations = {item["location_id"] for item in region.get("locations", [])}
    actors = {item["entity_id"] for item in region.get("entities", []) if item.get("persistence") == "static"}
    seen = set()
    fields = {"target_id", "location_id", "label", "aliases", "conditions", "methods", "cooperation", "development"}
    for item in items:
        if not isinstance(item, dict) or set(item) != fields:
            raise ValueError("Invalid material declaration shape.")
        identity = item["target_id"]
        if not isinstance(identity, str) or not identity or identity in seen:
            raise ValueError("Material target identities must be unique.")
        seen.add(identity)
        if item["location_id"] not in locations or not isinstance(item["label"], str) or not item["label"]:
            raise ValueError("Invalid material target location or label.")
        if not isinstance(item["aliases"], list) or not item["aliases"] or any(not isinstance(a, str) or not a.strip() for a in item["aliases"]):
            raise ValueError("Material aliases must name target features.")
        domains = item["conditions"]
        if not isinstance(domains, dict) or set(domains) != {"stability", "fitting", "position", "integrity"}:
            raise ValueError("Only the four bounded material dimensions are supported.")
        for name, declaration in domains.items():
            if not isinstance(declaration, dict) or set(declaration) != {"initial", "values", "transitions"}:
                raise ValueError("Invalid material domain declaration.")
            values = declaration["values"]
            if not isinstance(values, dict) or not values or any(not isinstance(k, str) or not k or not isinstance(v, str) or not v for k, v in values.items()) or declaration["initial"] not in values:
                raise ValueError("Invalid material domain values.")
            transitions = declaration["transitions"]
            if not isinstance(transitions, list) or any(not isinstance(edge, list) or len(edge) != 2 or any(v not in values for v in edge) for edge in transitions):
                raise ValueError("Invalid material transitions.")
        cooperation = item["cooperation"]
        if cooperation is not None and (not isinstance(cooperation, dict) or set(cooperation) != {"actor_id", "refuse_when", "offer", "refusal"} or cooperation["actor_id"] not in actors):
            raise ValueError("Invalid bounded cooperation declaration.")
        if cooperation is not None:
            _validate_conditions(item, cooperation["refuse_when"])
            if any(not isinstance(cooperation[k], str) or not cooperation[k] for k in ("offer", "refusal")):
                raise ValueError("Cooperation responses must be authored text.")
        methods = item["methods"]
        if not isinstance(methods, list) or not methods:
            raise ValueError("Material methods must be declared.")
        method_ids = set()
        for method in methods:
            expected = {"method_id", "operation", "label", "when", "brace", "cooperate", "risk", "conflicts", "outcomes"}
            if not isinstance(method, dict) or set(method) != expected or method["operation"] not in OPERATIONS:
                raise ValueError("Invalid bounded handling method.")
            if not isinstance(method["method_id"], str) or not method["method_id"] or method["method_id"] in method_ids:
                raise ValueError("Handling method identity must be unique.")
            method_ids.add(method["method_id"])
            if type(method["brace"]) is not bool or type(method["cooperate"]) is not bool or method["cooperate"] and cooperation is None:
                raise ValueError("Invalid handling preparation.")
            if any(not isinstance(method[k], str) for k in ("label", "risk")) or not isinstance(method["conflicts"], list) or not set(method["conflicts"]) <= CONSTRAINTS:
                raise ValueError("Invalid handling risk or restrictions.")
            _validate_conditions(item, method["when"], lists=True)
            if method["brace"] and "braced" not in domains["stability"]["values"]:
                raise ValueError("Bracing needs an authored braced stability value.")
            outcomes = method["outcomes"]
            if not isinstance(outcomes, dict) or set(outcomes) != {"full", "partial", "failure"}:
                raise ValueError("All three outcomes must be authored.")
            for outcome in outcomes.values():
                if not isinstance(outcome, dict) or set(outcome) != {"effects", "text"} or not isinstance(outcome["text"], str) or not outcome["text"]:
                    raise ValueError("Invalid handling outcome declaration.")
                _validate_conditions(item, outcome["effects"])
            # A claimed preservation method must preserve integrity on every draw.
            if "preserve_integrity" not in method["conflicts"] and any("integrity" in o["effects"] for o in outcomes.values()):
                raise ValueError("Integrity-changing methods must declare the preservation conflict.")
        development = item["development"]
        if not isinstance(development, dict) or set(development) != {"after_hours", "when", "effects", "text"} or type(development["after_hours"]) is not int or development["after_hours"] <= 0 or not isinstance(development["text"], str):
            raise ValueError("Invalid material timed development.")
        _validate_conditions(item, development["when"], lists=True)
        _validate_conditions(item, development["effects"])


def _validate_conditions(item, changes, *, lists=False):
    if not isinstance(changes, dict) or set(changes) - set(item["conditions"]):
        raise ValueError("Undeclared material dimension.")
    for name, value in changes.items():
        values = value if lists else [value]
        if not isinstance(values, list) or not values or any(not isinstance(v, str) or v not in item["conditions"][name]["values"] for v in values):
            raise ValueError("Undeclared material condition value.")


def initial_record(item, elapsed):
    return {"conditions": {k: d["initial"] for k, d in item["conditions"].items()},
            "cooperation": "unasked" if item["cooperation"] else "not_required",
            "started_elapsed_hours": elapsed, "last_history_id": None, "development_history_id": None}


def initialize(region, world):
    if declarations(region):
        world[STATE_KEY] = {d["target_id"]: initial_record(d, world["time"].get("elapsed_hours", 0)) for d in declarations(region)}


def matches(conditions, requirements):
    return all(conditions[k] in values for k, values in requirements.items())


def routine_steps(method):
    steps = ["approach the accessible target"]
    if method["brace"]: steps.append("brace the target")
    if method["cooperate"]: steps.append("request and coordinate the declared helper's cooperation")
    return steps + [method["label"]]


def changed_conditions(item, before, effects):
    _validate_conditions(item, effects)
    after = deepcopy(before)
    for name, value in effects.items():
        previous = before[name]
        if previous != value and [previous, value] not in item["conditions"][name]["transitions"]:
            raise ValueError("Unsupported material transition.")
        after[name] = value
    return after


def transition(region, world, identity, event_type, effects, *, cooperation=None, extra=None, source_id=None, summary=""):
    """Prepare a finite condition transition in a private outer candidate only."""
    from engine.world_state import add_history_entry
    item = target(region, identity)
    record = world[STATE_KEY][identity]
    before = deepcopy(record["conditions"])
    after = changed_conditions(item, before, effects)
    current = record["cooperation"]
    following = cooperation or current
    payload = {"target_id": identity, "before": before, "after": after,
               "cooperation_before": current, "cooperation_after": following, **(extra or {})}
    if source_id is not None:
        payload["source_history_id"] = source_id
    updated = add_history_entry(world, event_type, summary, item["location_id"], deepcopy(world["time"]), payload)
    record = updated[STATE_KEY][identity]
    record.update(conditions=after, cooperation=following, last_history_id=updated["history"][-1]["history_id"])
    if event_type == "material_development":
        record["development_history_id"] = record["last_history_id"]
    return updated


def advance_candidate(region, world, previous_time, new_time, source_id):
    from engine.world_state import get_effective_actor_location
    for item in declarations(region):
        record = world[STATE_KEY][item["target_id"]]
        development = item["development"]
        threshold = record["started_elapsed_hours"] + development["after_hours"]
        if record["development_history_id"] is None and previous_time.get("elapsed_hours", 0) < threshold <= new_time["elapsed_hours"]:
            policy = item["cooperation"]
            present = policy is None or get_effective_actor_location(region, world, policy["actor_id"]) == item["location_id"]
            applied = present and matches(record["conditions"], development["when"])
            world = transition(region, world, item["target_id"], "material_development",
                               development["effects"] if applied else {}, source_id=source_id,
                               extra={"applied": applied, "threshold": threshold},
                               summary=development["text"] if applied else "The bounded development no longer applies.")
    return world


def validate_state(world, region=None):
    records = world.get(STATE_KEY)
    events = [e for e in world.get("history", []) if e.get("event_type") in EVENTS]
    if records is None:
        if events or region is not None and declarations(region):
            raise ValueError("Missing authoritative material conditions.")
        return
    if not isinstance(records, dict):
        raise ValueError("Material conditions must be a dictionary.")
    if type(world["time"].get("elapsed_hours", 0)) is not int:
        raise ValueError("Material costs and developments require whole elapsed hours.")
    for record in records.values():
        if not isinstance(record, dict) or set(record) != {"conditions", "cooperation", "started_elapsed_hours", "last_history_id", "development_history_id"}:
            raise ValueError("Invalid material state shape.")
        if not isinstance(record["conditions"], dict) or record["cooperation"] not in {"unasked", "willing", "refused", "not_required"} or type(record["started_elapsed_hours"]) is not int or not 0 <= record["started_elapsed_hours"] <= world["time"].get("elapsed_hours", 0):
            raise ValueError("Invalid material state values.")
    if region is None:
        return
    items = {d["target_id"]: d for d in declarations(region)}
    if set(records) != set(items):
        raise ValueError("Material state must match declared targets.")
    if any(record["started_elapsed_hours"] != region["time"].get("elapsed_hours", 0) for record in records.values()):
        raise ValueError("Material development origin must match authored initialization.")
    reconstructed = {identity: initial_record(item, records[identity]["started_elapsed_hours"]) for identity, item in items.items()}
    prior = {}
    actor_locations = {a["entity_id"]: a["location"] for a in region.get("entities", []) if a.get("persistence") == "static"}
    for event in world.get("history", []):
        kind = event.get("event_type")
        if kind not in EVENTS:
            if kind == "actor_moved":
                actor_locations[event["entity_id"]] = event["new_location_id"]
            prior[event.get("history_id")] = event
            continue
        identity = event.get("target_id")
        if identity not in items:
            raise ValueError("Unknown material event target.")
        item, record = items[identity], reconstructed[identity]
        common = {"history_id", "event_type", "summary", "location", "time", "target_id", "before", "after", "cooperation_before", "cooperation_after"}
        additional = {
            "material_preparation": {"method_id", "constraints", "risk_authorized"},
            "material_outcome": {"method_id", "source_history_id", "time_history_id", "draw", "result"},
            "material_cooperation": {"actor_id"},
            "material_development": {"source_history_id", "applied", "threshold"},
        }
        if set(event) != common | additional[kind] or not isinstance(event["summary"], str):
            raise ValueError("Invalid material event shape.")
        if event.get("location") != item["location_id"] or event.get("before") != record["conditions"] or event.get("cooperation_before") != record["cooperation"]:
            raise ValueError("Material event basis is inconsistent.")
        source = prior.get(event.get("source_history_id"))
        cooperation = record["cooperation"]
        if kind == "material_development":
            d = item["development"]
            threshold = record["started_elapsed_hours"] + d["after_hours"]
            policy = item["cooperation"]
            present = policy is None or actor_locations[policy["actor_id"]] == item["location_id"]
            applied = present and matches(record["conditions"], d["when"])
            if record["development_history_id"] is not None or source is None or source.get("event_type") != "time_advanced" or type(event.get("applied")) is not bool or event["applied"] != applied or event.get("threshold") != threshold or not source["previous_time"].get("elapsed_hours", 0) < threshold <= source["new_time"]["elapsed_hours"]:
                raise ValueError("Invalid material development causality.")
            effects = d["effects"] if applied else {}
            expected_summary = d["text"] if applied else "The bounded development no longer applies."
            record["development_history_id"] = event["history_id"]
        elif kind == "material_cooperation":
            policy = item["cooperation"]
            if policy is None or event.get("actor_id") != policy["actor_id"] or actor_locations[policy["actor_id"]] != item["location_id"]:
                raise ValueError("Invalid material cooperation actor.")
            cooperation = "refused" if policy["refuse_when"] and all(record["conditions"][k] == v for k, v in policy["refuse_when"].items()) else "willing"
            effects = {}
            expected_summary = policy["refusal"] if cooperation == "refused" else policy["offer"]
        else:
            method = next((m for m in item["methods"] if m["method_id"] == event.get("method_id")), None)
            if method is None:
                raise ValueError("Unknown accepted material method.")
            if kind == "material_preparation":
                restrictions = event.get("constraints")
                if not isinstance(restrictions, list) or any(not isinstance(c, str) or c not in CONSTRAINTS for c in restrictions) or len(set(restrictions)) != len(restrictions) or type(event.get("risk_authorized")) is not bool or not event["risk_authorized"]:
                    raise ValueError("Invalid material authorization receipt.")
                conflicts = {"assess_only"} | set(method["conflicts"])
                if method["operation"] == "reposition": conflicts.add("no_move")
                if method["operation"] == "adjust": conflicts.add("no_adjust")
                if method["cooperate"]: conflicts.add("no_talk")
                if set(restrictions) & conflicts:
                    raise ValueError("Material authorization violates a restriction.")
                if not matches(record["conditions"], method["when"]):
                    raise ValueError("Ineligible material preparation.")
                effects = {"stability": "braced"} if method["brace"] else {}
                expected_summary = "Accepted routine preparation: " + "; ".join(routine_steps(method)[:-1]) + "."
                if method["cooperate"]:
                    policy = item["cooperation"]
                    if actor_locations[policy["actor_id"]] != item["location_id"]:
                        raise ValueError("Material cooperation requires presence.")
                    if policy["refuse_when"] and all(record["conditions"][k] == v for k, v in policy["refuse_when"].items()):
                        raise ValueError("Unauthorized cooperation.")
                    cooperation = "willing"
            else:
                result, draw = event.get("result"), event.get("draw")
                time = prior.get(event.get("time_history_id"))
                if source is None or source.get("event_type") != "material_preparation" or source.get("target_id") != identity or source.get("method_id") != method["method_id"] or time is None or time.get("event_type") != "time_advanced" or time.get("source_history_id") != source["history_id"] or time["new_time"]["elapsed_hours"] - time["previous_time"].get("elapsed_hours", 0) != 1:
                    raise ValueError("Invalid material attempt cost/causality.")
                applicable = matches(record["conditions"], method["when"])
                if method["cooperate"]:
                    policy = item["cooperation"]
                    applicable = applicable and actor_locations[policy["actor_id"]] == item["location_id"] and record["cooperation"] == "willing"
                if result == "interrupted":
                    if draw is not None or applicable:
                        raise ValueError("Invalid material interruption.")
                    effects = {}
                    reason = "The current material conditions do not permit that method." if not matches(record["conditions"], method["when"]) else "The required helper is not present."
                    expected_summary = "After preparation and 1 hour of effort, changed circumstances stop the remaining action. " + reason
                else:
                    expected = "full" if method["operation"] == "stabilize" else character_competence.resolve(draw, False)
                    if result != expected or method["operation"] == "stabilize" and draw is not None or not applicable:
                        raise ValueError("Invalid material resolution.")
                    effects = method["outcomes"][result]["effects"]
                    expected_summary = method["outcomes"][result]["text"] + " Effort: 1 hour."
        after = changed_conditions(item, record["conditions"], effects)
        if event.get("after") != after or event.get("cooperation_after") != cooperation or event["summary"] != expected_summary:
            raise ValueError("Material event effects are inconsistent.")
        record.update(conditions=after, cooperation=cooperation, last_history_id=event["history_id"])
        prior[event["history_id"]] = event
    if reconstructed != records:
        raise ValueError("Material state disagrees with accepted causal history.")


def observations(region, world):
    from engine.world_state import get_effective_actor_location
    local = world["player"]["current_location_id"]
    texts = []
    for item in declarations(region):
        if item["location_id"] != local:
            continue
        record = world[STATE_KEY][item["target_id"]]
        texts.extend(item["conditions"][name]["values"][value] for name, value in record["conditions"].items())
        policy = item["cooperation"]
        if policy and get_effective_actor_location(region, world, policy["actor_id"]) == local:
            if record["cooperation"] == "unasked":
                actor = next(a for a in region["entities"] if a["entity_id"] == policy["actor_id"])
                texts.append(actor["name"] + " is attending to the " + item["label"] + ".")
            elif record["cooperation"] == "willing":
                texts.append(policy["offer"])
            elif record["cooperation"] == "refused":
                texts.append(policy["refusal"])
    return texts
