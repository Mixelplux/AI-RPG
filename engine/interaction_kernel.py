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

    if intent == "skill_check":
        check_name = action.get("target")
        if not check_name:
            return build_interaction_result(
                success=False,
                intent=intent,
                message="Usage: check <name>",
                action=action
            )

        return build_interaction_result(
            success=True,
            intent=intent,
            message=f"You attempt a {check_name} check.",
            action=action
        )

    if intent == "destination":
        destination_text = action.get("target")
        if not destination_text:
            return build_interaction_result(
                success=False,
                intent=intent,
                message="Usage: head to <destination>",
                action=action
            )

        return build_interaction_result(
            success=True,
            intent=intent,
            message=f"You identify {destination_text} as a destination.",
            action=action
        )

    if intent == "wait":
        return build_interaction_result(
            success=True,
            intent=intent,
            message="You wait for 1 hour.",
            action=action
        )
    if intent == "investigation":
        return build_interaction_result(success=True, intent=intent, message="You investigate the area.", action=action)
    if intent == "clue_recall":
        return build_interaction_result(success=True, intent=intent, message="You recall the clues you have found.", action=action)
    if intent == "clue_presentation":
        return build_interaction_result(success=True, intent=intent, message="You present a clue.", action=action)

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
    words = lowered.split()

    if lowered == "check" or lowered.startswith("check "):
        return "skill_check"

    destination_prefixes = ["head to", "go to"]
    if any(
        lowered == prefix or lowered.startswith(f"{prefix} ")
        for prefix in destination_prefixes
    ):
        return "destination"

    if lowered == "wait":
        return "wait"
    if lowered in {"investigate", "search for clues"}:
        return "investigation"
    if lowered in {"clues", "known clues"}:
        return "clue_recall"
    if lowered.startswith("present ") and " to " in lowered:
        return "clue_presentation"

    movement_words = ["go", "walk", "move", "travel", "enter", "leave"]
    look_words = ["look", "inspect", "examine", "search", "study"]
    talk_words = ["talk", "speak", "ask", "greet", "tell"]
    action_words = ["take", "grab", "open", "close", "use", "push", "pull"]

    if any(word in words for word in movement_words):
        return "movement"

    if any(word in words for word in look_words):
        return "observation"

    if any(word in words for word in talk_words):
        return "conversation"

    if any(word in words for word in action_words):
        return "action"

    return "unknown"


def build_action(player_input: str, intent: str) -> Dict[str, Any]:
    if intent == "skill_check":
        return {
            "type": "skill_check",
            "target": player_input[5:].strip() or None,
            "parameters": {},
            "confidence": 1.0
        }

    if intent == "destination":
        return {
            "type": "resolve_destination",
            "target": extract_destination_target(player_input),
            "parameters": {},
            "confidence": 1.0
        }

    if intent == "wait":
        return {
            "type": "advance_time",
            "target": None,
            "parameters": {
                "duration_hours": 1
            },
            "confidence": 1.0
        }
    if intent == "investigation":
        return {"type": "investigate", "target": None, "parameters": {}, "confidence": 1.0}
    if intent == "clue_recall":
        return {"type": "recall_clues", "target": None, "parameters": {}, "confidence": 1.0}
    if intent == "clue_presentation":
        clue, actor = player_input[8:].rsplit(" to ", 1)
        return {"type": "present_clue", "target": actor.strip() or None, "parameters": {"clue_title": clue.strip()}, "confidence": 1.0}

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

    words = player_input.strip().split()
    if words and words[0].lower() in ["talk", "speak", "ask", "greet", "tell"]:
        target_words = words[1:]
        if target_words and target_words[0].lower() == "to":
            target_words = target_words[1:]
        return " ".join(target_words) or None

    return None


def extract_destination_target(player_input: str) -> str | None:
    lowered = player_input.lower()
    for prefix in ["head to", "go to"]:
        if lowered == prefix or lowered.startswith(f"{prefix} "):
            target = player_input[len(prefix):].strip()
            if target.lower().startswith("the "):
                target = target[4:].strip()
            return target or None
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
