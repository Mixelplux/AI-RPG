from typing import Any, Dict


def process_player_input(
    player_input: str,
    scene_snapshot: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process raw player input and return a structured Interaction Result.

    This function validates actions but does not mutate world state.
    """

    cleaned_input = player_input.strip()

    if not cleaned_input:
        return build_interaction_result(
            success=False,
            intent="unknown",
            message="No input provided.",
            action={
                "type": "none",
                "target": None,
                "parameters": {},
                "confidence": 1.0
            }
        )

    intent = classify_intent(cleaned_input)
    action = build_action(cleaned_input, intent)

    if intent == "movement":
        return resolve_movement(action, scene_snapshot)

    if intent == "observation":
        return build_interaction_result(
            success=True,
            intent=intent,
            message="You take a closer look.",
            action=action
        )

    if intent == "conversation":
        return build_interaction_result(
            success=True,
            intent=intent,
            message="You begin a conversation.",
            action=action
        )

    if intent == "action":
        return build_interaction_result(
            success=True,
            intent=intent,
            message="You attempt the action.",
            action=action
        )

    return build_interaction_result(
        success=False,
        intent=intent,
        message="You are not sure how to do that.",
        action=action
    )


def classify_intent(player_input: str) -> str:
    lowered = player_input.lower()

    movement_words = ["go", "walk", "move", "travel", "enter", "leave"]
    look_words = ["look", "inspect", "examine", "search", "study"]
    talk_words = ["talk", "speak", "ask", "greet", "tell"]
    action_words = ["take", "grab", "open", "close", "use", "push", "pull"]

    if any(word in lowered for word in movement_words):
        return "movement"

    if any(word in lowered for word in look_words):
        return "observation"

    if any(word in lowered for word in talk_words):
        return "conversation"

    if any(word in lowered for word in action_words):
        return "action"

    return "unknown"


def build_action(player_input: str, intent: str) -> Dict[str, Any]:
    if intent == "movement":
        return {
            "type": "move",
            "target": extract_movement_target(player_input),
            "parameters": {},
            "confidence": 0.5
        }

    if intent == "observation":
        return {
            "type": "look",
            "target": None,
            "parameters": {},
            "confidence": 1.0
        }

    if intent == "conversation":
        return {
            "type": "talk",
            "target": extract_conversation_target(player_input),
            "parameters": {},
            "confidence": 0.5
        }

    if intent == "action":
        return {
            "type": "use",
            "target": None,
            "parameters": {},
            "confidence": 0.3
        }

    return {
        "type": "unknown",
        "target": None,
        "parameters": {},
        "confidence": 0.0
    }


def resolve_movement(
    action: Dict[str, Any],
    scene_snapshot: Dict[str, Any]
) -> Dict[str, Any]:
    target = action.get("target")

    if not target:
        return build_interaction_result(
            success=False,
            intent="movement",
            message="Where do you want to go?",
            action=action
        )

    location = scene_snapshot.get("location", {})
    connected_locations = location.get("connected_locations", [])

    for connection in connected_locations:
        if connection.get("direction") == target:
            destination_id = connection.get("location_id")

            return build_interaction_result(
                success=True,
                intent="movement",
                message=f"You move {target}.",
                action=action,
                extra={
                    "destination_location_id": destination_id
                }
            )

    return build_interaction_result(
        success=False,
        intent="movement",
        message="You cannot go that way.",
        action=action
    )


def extract_movement_target(player_input: str) -> str | None:
    lowered = player_input.lower()

    direction_aliases = {
        "north": "north",
        "south": "south",
        "east": "east",
        "west": "west",
        "up": "up",
        "down": "down",
        "inside": "in",
        "outside": "out",
        "in": "in",
        "out": "out",
    }

    for word, canonical_direction in direction_aliases.items():
        if word in lowered:
            return canonical_direction

    return None


def extract_conversation_target(player_input: str) -> str | None:
    lowered = player_input.lower()

    if "guard" in lowered:
        return "guard"

    if "captain" in lowered:
        return "captain"

    return None


def build_interaction_result(
    success: bool,
    intent: str,
    message: str,
    action: Dict[str, Any],
    extra: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    result = {
        "success": success,
        "intent": intent,
        "message": message,
        "action": action,
        "world_changes": []
    }

    if extra:
        result.update(extra)

    return result