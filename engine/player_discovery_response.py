from typing import Any


def derive_conversation_player_discovery_response(
    region: dict[str, Any], target_entity_id: str | None,
    command_start_discoveries: tuple[str, ...],
) -> dict[str, str] | None:
    declaration = region.get("conversation_player_discovery_response")
    if (declaration is None or target_entity_id != declaration["target_entity_id"]
            or declaration["required_discovery_id"] not in command_start_discoveries):
        return None
    return {"text": declaration["response_text"]}
