from typing import Any


def derive_conversation_actor_knowledge_response(
    region: dict[str, Any],
    target_entity_id: str | None,
    command_start_knowledge: tuple[str, ...],
) -> dict[str, str] | None:
    """Return the exact authored response for one eligible conversation."""

    declaration = region.get("conversation_actor_knowledge_response")
    if (
        declaration is None
        or target_entity_id != declaration["target_entity_id"]
        or declaration["required_knowledge_id"] not in command_start_knowledge
    ):
        return None
    return {"text": declaration["response_text"]}
