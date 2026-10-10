"""Local scene selection/expression helpers; no scene or simulation authority.

Consume existing accessible projections and refresh selection. The source is a
bounded read-only handoff, not a permanent scene schema. Revised A belongs only
to the default adapter pair, as on the accepted resolved-action path.
"""
from copy import deepcopy

from engine.narration_request import build_narration_request_packet
from engine.narration_output import (
    NARRATION_OUTPUT_SCHEMA, NARRATION_OUTPUT_VERSION, validate_narration_output_packet,
)
from engine.resolved_narration import validate_revised_a
from engine.scene_context import select_scene_sections


PUBLIC_ROLES = {"guard_commander": "guard commander", "city_guard": "city guard",
                "caravan_driver": "caravan driver", "merchant": "merchant"}


def build_scene_source(context, narration, opportunities, roles, previous=None, result=None,
                       invitation=""):
    """Compose safe source material without passing internal scene/history data.

    Current opportunities are supplied by existing gameplay predicates. Prior
    presentation is a comparison hint, not truth, access policy or memory.
    """
    safe = build_narration_request_packet(context)["narration_context"]
    scene, public = safe["scene_context"], safe["narrative_projection"]
    selected = select_scene_sections(narration, previous, result)
    if selected is None:
        raise ValueError("No bounded scene sections supplied.")
    prior = previous.get("scene_sections", {}) if previous else {}
    known_situation = bool(prior.get("situation")) and prior["situation"] == public["current_situation"]
    if previous and previous.get("title") != narration["title"]:
        # Reorient to the new place without replaying the same local predicament.
        # Current access is still determined by the supplied projections, not this hint.
        if known_situation:
            selected.pop("situation", None)
        selected["evidence"] = [text for text in selected.get("evidence", [])
                                if text not in prior.get("evidence", [])]
    present = {actor["display_name"] for actor in public["presence"]}
    facts = []
    if selected.get("orientation"):
        facts.append({"text": selected["orientation"], "status": "accessible physical circumstances"})
    if selected.get("conditions"):
        facts.extend({"text": text, "status": "observable condition"}
                     for text in selected["conditions"])
    if selected.get("presence"):
        people = []
        for actor in public["presence"]:
            name = actor["display_name"]
            role = next((item["role"] for item in roles if item["display_name"] == name), "")
            people.append(name + (", the " + role if role else ""))
        people.extend(str(group["count"]) + " " + group["display_name"] for group in public["groups"])
        if people:
            joined = people[0] if len(people) == 1 else ", ".join(people[:-1]) + " and " + people[-1]
            facts.append({"text": "You can see " + joined + ".",
                          "status": "observable presence and public roles"})
    if selected.get("situation"):
        facts.append({"text": selected["situation"], "status": "established public situation"})
    facts.extend({"text": text, "status": "qualified established information"}
                 for text in selected.get("evidence", []))
    if selected.get("orientation") and invitation and not known_situation:
        facts.append({"text": invitation, "status": "voluntary opportunity"})
    return {
        "location": deepcopy(scene["location_facts"]),
        "conditions": deepcopy(scene["conditions"]),
        "presence": deepcopy(public["presence"]),
        "roles": [deepcopy(item) for item in roles if item["display_name"] in present],
        "routes": deepcopy(public["routes"]),
        "information": deepcopy(public["acquired_information"]),
        "current_situation": public["current_situation"],
        "selected_facts": facts,
        "opportunities": list(opportunities),
        "guidance": {key: selected[key] for key in ("choices", "other") if selected.get(key)},
        "boundaries": [
            "Only supplied accessible facts establish the scene; reports and inferences retain their qualifications.",
            "Known information is context, not new discovery. Command names and internal labels establish no knowledge or motive.",
            "Do not resolve actions, invent disclosures, assign responsibility or commit the player.",
            "Opportunities, presence and costs are already derived; do not decide prerequisites or availability.",
            "A refresh follows a separately delivered result; do not replay it or introduce another event.",
            "Reorientation is not a fictional first-ever meeting; no familiarity or encounter history is supplied.",
        ],
    }


def prepare_scene_revised_a(source):
    """Select already justified scene meaning, keeping the representation private."""
    meanings = [{"key": "scene_" + str(index), "text": item["text"],
                 "epistemic_status": item["status"], "knowledge_holder": "player"}
                for index, item in enumerate(source["selected_facts"])]
    return validate_revised_a({
        "representation": "selected_meaning_plan",
        "content": {"meanings": meanings,
                    "plan": [{"meaning_keys": [item["key"]], "delivery": "Convey this supplied scene meaning once."}
                             for item in meanings]},
        "context": [item["status"] + ": " + item["text"] for item in source["information"]]
                   + list(source["opportunities"]),
        "boundaries": list(source["boundaries"]),
    })


def realize_scene_locally(intermediate):
    """Conservative stateless realization of the local selection; no provider."""
    prepared = validate_revised_a(intermediate)
    paragraphs = []
    for meaning in prepared["content"]["meanings"]:
        text = meaning["text"]
        if paragraphs and meaning["epistemic_status"] in {
            "observable condition", "observable presence and public roles",
        }:
            paragraphs[-1] += " " + text
        else:
            paragraphs.append(text)
    return {"schema": NARRATION_OUTPUT_SCHEMA, "version": NARRATION_OUTPUT_VERSION,
            "narration_text": "\n\n".join(paragraphs)}


def narrate_scene_source(source, preparer=prepare_scene_revised_a, realizer=realize_scene_locally):
    """Replaceable two-stage expression; presentation guidance remains engine-owned."""
    stage = "preparation"
    try:
        # A choice-only refresh needs no invented passage or empty Revised A plan.
        if not source["selected_facts"]:
            return {"accepted": True, "display_text": "", "guidance": deepcopy(source["guidance"])}
        intermediate = preparer(deepcopy(source))
        stage = "realization"
        output = validate_narration_output_packet(realizer(deepcopy(intermediate)))
        if not output["narration_text"].strip() or len(output["narration_text"]) > 4000:
            raise ValueError("Empty or overlong scene realization.")
        return {"accepted": True, "display_text": output["narration_text"],
                "guidance": deepcopy(source["guidance"])}
    except Exception:
        return {"accepted": False, "display_text": "", "failure_stage": stage}
