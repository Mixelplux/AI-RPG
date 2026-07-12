from copy import deepcopy
from typing import Dict, Any


def build_perception(
    scene_snapshot: Dict[str, Any],
    pressure_cues: list[Dict[str, str]] | None = None,
    unresolved_thread_evidence: list[Dict[str, str]] | None = None,
) -> Dict[str, Any]:
    """
    Convert a Scene Snapshot into a Perception Snapshot.

    v0.1 rules:
    - Everything in the current scene is visible.
    - Local environment is perceivable.
    - No narration.
    - No mutation of input.
    """

    location = scene_snapshot.get("location", {})
    entities = scene_snapshot.get("entities", {})
    local_state = scene_snapshot.get("local_state", {})

    location_id = location.get("location_id") or location.get("id")

    return {
        "perception_id": f"{scene_snapshot.get('scene_id', 'unknown_scene')}_perception",

        "observer": {
            "location": location_id
        },

        "visible": {
            "location": {
                "id": location_id,
                "name": location.get("name"),
                "type": location.get("type"),
                "description_seed": location.get("description_seed"),
                "state": deepcopy(location.get("state", {}))
            },

            "entities": {
                "static": deepcopy(entities.get("static", [])),
                "spawned": deepcopy(entities.get("spawned", []))
            }
        },

        "environment": deepcopy(local_state),

        "audible": [],

        "hidden": [],

        "pressure_cues": deepcopy(pressure_cues or []),

        "unresolved_thread_evidence": deepcopy(unresolved_thread_evidence or [])
    }
