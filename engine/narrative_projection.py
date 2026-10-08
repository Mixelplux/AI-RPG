"""Explicit narration serialization and accepted West-Road read models.

This is a bounded presentation contract, not a general knowledge/access model.
Only public authored local grounding and already accepted scenario records enter.
"""

from copy import deepcopy
from math import isfinite

from engine import character_competence as competence
from engine import west_road_predicament as west
from engine.west_road_presentation import CURRENT_CIRCUMSTANCES, ROUTE_FOLLOWTHROUGH


WEATHER_TEXT = {"type"}
WEATHER_NUMBERS = {"severity", "temperature_c", "wind_speed_kmh", "visibility_m"}
TIME_TEXT = {"current_date", "season", "time_of_day"}
TIME_NUMBERS = {"elapsed_hours"}
PERSPECTIVE_LAYERS = {"observations", "recognition", "findings"}
ACTION_KEYS = {"action", "competence_basis", "outcome", "result", "cost_hours",
               "consequences", "actor_responses", "remaining_uncertainty"}


def _object(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError("Narrative projection has unsupported fields.")


def _texts(value):
    if not isinstance(value, list) or any(not isinstance(s, str) for s in value):
        raise ValueError("Narrative projection requires a text list.")


def project_conditions(conditions):
    result = {}
    for section, text, numbers in (("weather", WEATHER_TEXT, WEATHER_NUMBERS),
                                   ("time", TIME_TEXT, TIME_NUMBERS)):
        source = conditions.get(section, {})
        result[section] = {k: deepcopy(source[k]) for k in sorted(text | numbers) if k in source}
    validate_conditions(result)
    return result


def validate_conditions(value):
    _object(value, {"weather", "time"})
    for section, text, numbers in (("weather", WEATHER_TEXT, WEATHER_NUMBERS),
                                   ("time", TIME_TEXT, TIME_NUMBERS)):
        fields = value[section]
        if not isinstance(fields, dict) or set(fields) - (text | numbers):
            raise ValueError("Narrative conditions contain unsupported fields.")
        for key, item in fields.items():
            if key in text and not isinstance(item, str):
                raise ValueError("Narrative condition must be text.")
            if key in numbers and (type(item) not in (int, float) or not isfinite(item)):
                raise ValueError("Narrative condition must be a finite number.")


def project_perspective(source):
    if not source:
        return {}
    result = {layer: [{"text": item["text"], "status": item["status"]}
                      for item in source.get(layer, [])] for layer in sorted(PERSPECTIVE_LAYERS)}
    result["approaches"] = [{k: item[k] for k in ("command", "cost_hours", "uncertain", "specialist")}
                            for item in source.get("approaches", [])]
    result["accepted_outcomes"] = [{k: item[k] for k in ("command", "result", "cost_hours", "text")}
                                   for item in source.get("accepted_outcomes", [])]
    result["limits"] = list(source.get("limits", []))
    validate_perspective(result)
    return result


def validate_perspective(value):
    if value == {}:
        return
    _object(value, PERSPECTIVE_LAYERS | {"approaches", "accepted_outcomes", "limits"})
    for layer in PERSPECTIVE_LAYERS:
        _records(value[layer], {"text", "status"})
    for layer, fields in (("approaches", {"command", "cost_hours", "uncertain", "specialist"}),
                          ("accepted_outcomes", {"command", "result", "cost_hours", "text"})):
        if not isinstance(value[layer], list):
            raise ValueError("Narrative perspective requires records.")
        for item in value[layer]:
            _object(item, fields)
            for key in fields - {"cost_hours", "uncertain", "specialist"}:
                if not isinstance(item[key], str):
                    raise ValueError("Narrative perspective requires text.")
            _cost(item["cost_hours"])
            if layer == "approaches" and any(type(item[k]) is not bool for k in ("uncertain", "specialist")):
                raise ValueError("Narrative perspective requires flags.")
    _texts(value["limits"])


def _records(value, fields):
    if not isinstance(value, list):
        raise ValueError("Narrative projection requires records.")
    for item in value:
        _object(item, fields)
        if any(not isinstance(v, str) for v in item.values()):
            raise ValueError("Narrative record requires text.")


def _cost(value):
    if type(value) is not int or value < 0:
        raise ValueError("Narrative cost must be a nonnegative integer.")


def accepted_action(region, world, action_id):
    """Read an engine-issued outcome reference; never execute an action.

    Explicit references retrieve recorded results independently of current scene
    eligibility. Local context is filtered separately by build_projection.
    Historical actor replies use the accepted phase, and competence basis uses
    the accepted attempt rather than current tags. References remain internal.
    """
    if action_id is None:
        return {}
    if not isinstance(action_id, str) or not action_id:
        raise ValueError("Narration requires an accepted West-Road outcome reference.")
    events = {e["history_id"]: e for e in world["history"]}
    event = events.get(action_id)
    if not event or event["event_type"] not in {"west_road_outcome", "west_road_competence_result"}:
        raise ValueError("Narration requires an accepted West-Road outcome reference.")
    responses = []
    consequences = []
    if event["event_type"] == "west_road_outcome":
        source = events[event["source_history_id"]]
        command = source["command"]
        cost = 1 if event["time_history_id"] else 0
        outcome = region["west_road_predicament"]["phase_text"][event["phase"]]
        result, basis = "accepted commitment", "Established decision; no competence check."
        response_event = event
    else:
        attempt = event["attempt"]
        source = events[event["source_history_id"]]
        command = source["command"]
        cost, result = attempt["cost_hours"], attempt["result"]
        outcome = competence.outcome_text(region, command, attempt)
        basis = ("Established " + competence.OPERATIONS[command][0].replace("_", " ") + " competence informed this attempt." if attempt["specialist"]
                 else "Ordinary competence informed this attempt.")
        if command == "arrange guarded local survey":
            basis += " Grey and Elin supplied the already committed guards; the survey was deterministic."
        else:
            basis += " The engine resolved an uncertain investigation."
        followup = next((e for e in world["history"] if e["event_type"] == "west_road_commitment"
                         and e.get("source_history_id") == source["history_id"]), None)
        response_event = next((e for e in world["history"] if followup and e["event_type"] == "west_road_outcome"
                               and e.get("source_history_id") == followup["history_id"]), None)
        if response_event:
            # The accepted finding already carries the route discovery. Reuse the
            # existing presentation of its continuing consequence without repeating it.
            consequences.append(ROUTE_FOLLOWTHROUGH)
    if response_event:
        for actor, speaker in ((west.GREY, "Grey"), (west.ELIN, "Elin")):
            if actor in response_event["witness_entity_ids"]:
                responses.append({"speaker": speaker, "text": region["west_road_predicament"]["actor_responses"][actor][response_event["phase"]]})
    packet = {"action": command, "competence_basis": basis, "outcome": outcome,
              "result": result, "cost_hours": cost, "consequences": consequences,
              "actor_responses": responses, "remaining_uncertainty": [competence.LIMIT if event["event_type"] == "west_road_competence_result"
                  else "The observers' identities and the broader threat remain unresolved."]}
    validate_action(packet)
    return packet


def validate_action(value):
    if value == {}:
        return
    _object(value, ACTION_KEYS)
    for key in ("action", "competence_basis", "outcome", "result"):
        if not isinstance(value[key], str):
            raise ValueError("Narrative action requires text.")
    _cost(value["cost_hours"])
    _texts(value["consequences"])
    _texts(value["remaining_uncertainty"])
    _records(value["actor_responses"], {"speaker", "text"})


def build_projection(region, world, public_scene, pressure_cue, action_id=None):
    local = west.scene_relevant(region, world)
    information = []
    # Acquired information is selected locally, not a dump of the character ledger.
    if local:
        for d in region.get("discovery_declarations", []):
            if d["discovery_id"] in world["player_discoveries"]:
                report = d["discovery_id"] in {"west_road_merchant_account", "west_road_driver_account"}
                inference = d["discovery_id"] in {"west_road_tracks", "west_road_patrol_signs", "west_road_staging_area", "west_road_observation_overlap", "west_road_sign_direction"}
                information.append({"text": d["text"], "status": "attributed report" if report else "limited inference" if inference else "established finding"})
    packet = {
        "current_situation": CURRENT_CIRCUMSTANCES[world["west_road_predicament"]["phase"]] if local else "",
        "presence": [{"display_name": a["display_name"]} for a in public_scene["entities"]["actors"]],
        "groups": [{"display_name": g["display_name"], "count": g["count"]} for g in public_scene["entities"]["groups"]],
        "routes": [{"orientation": e["orientation"], "destination_name": e["destination_name"]} for e in public_scene["exits"]],
        "acquired_information": information,
        "familiarity": {"profile": "unspecified", "basis": "No ordinary local familiarity supplied.", "public_features": []},
        "accepted_action": accepted_action(region, world, action_id),
        "pressure_cue": {"text": pressure_cue["text"]} if pressure_cue else {},
    }
    validate_projection(packet)
    return packet


def validate_projection(value):
    _object(value, {"current_situation", "presence", "groups", "routes", "acquired_information", "familiarity", "accepted_action", "pressure_cue"})
    if not isinstance(value["current_situation"], str):
        raise ValueError("Narrative situation must be text.")
    _records(value["presence"], {"display_name"})
    _records(value["routes"], {"orientation", "destination_name"})
    _records(value["acquired_information"], {"text", "status"})
    if not isinstance(value["groups"], list):
        raise ValueError("Narrative groups require records.")
    for group in value["groups"]:
        _object(group, {"display_name", "count"})
        if not isinstance(group["display_name"], str) or type(group["count"]) is not int or group["count"] < 1:
            raise ValueError("Narrative group is malformed.")
    familiar = value["familiarity"]
    _object(familiar, {"profile", "basis", "public_features"})
    if familiar["profile"] != "unspecified" or not isinstance(familiar["basis"], str):
        raise ValueError("Narrative familiarity is malformed.")
    _texts(familiar["public_features"])
    if familiar["public_features"]:
        raise ValueError("Runtime familiarity is not supported.")
    validate_action(value["accepted_action"])
    cue = value["pressure_cue"]
    if cue:
        _object(cue, {"text"})
        if not isinstance(cue["text"], str):
            raise ValueError("Narrative pressure cue requires text.")
    elif cue != {}:
        raise ValueError("Narrative pressure cue must be an object.")
