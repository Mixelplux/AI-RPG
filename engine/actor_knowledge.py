from copy import deepcopy
from typing import Any


def build_initial_actor_knowledge(region: dict[str, Any]) -> dict[str, list[str]]:
    """Deep-copy non-empty authored knowledge seeds for static actors."""

    return {
        entity["entity_id"]: deepcopy(entity["knowledge"])
        for entity in region.get("entities", [])
        if isinstance(entity, dict)
        and entity.get("persistence") == "static"
        and entity["knowledge"]
    }


def validate_actor_knowledge(
    actor_knowledge: Any,
    region: dict[str, Any] | None = None,
) -> None:
    """Validate sparse persisted membership for supported static actors."""

    if not isinstance(actor_knowledge, dict):
        raise ValueError("World State actor_knowledge must be a dictionary.")

    static_actor_ids = None
    if region is not None:
        static_actor_ids = {
            entity.get("entity_id")
            for entity in region.get("entities", [])
            if isinstance(entity, dict) and entity.get("persistence") == "static"
        }

    for actor_id, knowledge_ids in actor_knowledge.items():
        if not isinstance(actor_id, str) or not actor_id:
            raise ValueError("Actor knowledge actor_id must be a non-empty string.")
        if static_actor_ids is not None and actor_id not in static_actor_ids:
            raise ValueError("Actor knowledge actor_id must reference a static actor.")
        if not isinstance(knowledge_ids, list):
            raise ValueError("Actor knowledge membership must be a list.")
        if not knowledge_ids:
            raise ValueError("Actor knowledge sparse membership must not be empty.")
        if any(not isinstance(knowledge_id, str) or not knowledge_id
               for knowledge_id in knowledge_ids):
            raise ValueError(
                "Actor knowledge identifiers must be non-empty strings."
            )
        if len(set(knowledge_ids)) != len(knowledge_ids):
            raise ValueError("Actor knowledge identifiers must be unique per actor.")


def get_actor_knowledge(
    actor_knowledge: dict[str, list[str]],
    actor_id: str,
) -> tuple[str, ...]:
    """Return immutable current membership for one validated actor."""

    return tuple(actor_knowledge.get(actor_id, []))
