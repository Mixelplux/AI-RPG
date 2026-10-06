import re
from collections import deque
from typing import Any, Dict


def process_player_input(
    player_input: str,
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]] | None = None,
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

        immediate_route_result = resolve_immediate_destination_route(
            action,
            scene_snapshot,
            locations or [],
        )
        if immediate_route_result is not None:
            return immediate_route_result

        if _is_go_to_destination_command(cleaned_input):
            return resolve_local_destination_route(action, scene_snapshot, locations or [])

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
        if not action["parameters"].get("clue_title") or not action.get("target"):
            return build_interaction_result(
                success=False,
                intent=intent,
                message="Usage: present <clue title> to <actor>",
                action=action,
            )
        return build_interaction_result(success=True, intent=intent, message="You present a clue.", action=action)

    if intent == "movement":
        immediate_movement_result = resolve_movement(
            action,
            scene_snapshot,
            locations or [],
        )
        if (
            immediate_movement_result["success"]
            or not _is_move_to_destination_command(cleaned_input)
            or _matching_named_connections(
                scene_snapshot.get("location", {}).get("connected_locations", []),
                action.get("target") or "",
                locations or [],
            )
        ):
            return immediate_movement_result

        return resolve_local_destination_route(action, scene_snapshot, locations or [])

    if intent == "observation":
        return build_interaction_result(
            success=True,
            intent=intent,
            message="You take a closer look.",
            action=action
        )

    if intent == "player_intention":
        return build_interaction_result(
            success=True, intent=intent, message="", action=action
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
    if lowered.startswith("present"):
        return "clue_presentation"

    # Within-scene first-person movement is narration intent, not a route.
    # Keep explicit go/head/move-to and directional commands on their old path.
    if re.match(r"^i\s+(?:walk|move|wander|stroll)\s+(?:through|around|about|among|along)\b", lowered):
        return "player_intention"

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
    if intent == "player_intention":
        return {
            "type": "narrate_intention", "target": None,
            "parameters": {}, "confidence": 1.0,
        }

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
        match = re.fullmatch(r"present\s+(.+?)\s+to\s+(.+?)", player_input.strip(), re.IGNORECASE)
        clue_title, actor = (match.group(1).strip(), match.group(2).strip()) if match else (None, None)
        return {"type": "present_clue", "target": actor or None, "parameters": {"clue_title": clue_title or None}, "confidence": 1.0}

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
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]],
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
            return _resolved_movement(action, connection)

    named_connections = _matching_named_connections(
        connected_locations,
        target,
        locations,
    )
    if len(named_connections) == 1:
        return _resolved_movement(action, named_connections[0])

    return build_interaction_result(
        success=False,
        intent="movement",
        message="You cannot go that way.",
        action=action
    )


def resolve_immediate_destination_route(
    action: Dict[str, Any],
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]],
) -> Dict[str, Any] | None:
    """Resolve a destination phrase only when it names one immediate route.

    Returning ``None`` preserves the destination resolver's existing
    nonmoving loaded-region identification behavior.
    """

    target = action.get("target")
    if not isinstance(target, str) or not target:
        return None

    connected_locations = scene_snapshot.get("location", {}).get(
        "connected_locations", []
    )
    named_connections = _matching_named_connections(
        connected_locations,
        target,
        locations,
    )
    if len(named_connections) == 1:
        movement_action = {
            **action,
            "type": "move",
        }
        return _resolved_movement(movement_action, named_connections[0])
    if len(named_connections) > 1:
        return build_interaction_result(
            success=False,
            intent="destination",
            message="That immediate route is ambiguous.",
            action=action,
        )
    return None


def resolve_local_destination_route(
    action: Dict[str, Any], scene_snapshot: Dict[str, Any], locations: list[Dict[str, Any]]
) -> Dict[str, Any]:
    """Derive the shortest local route from static authored topology.

    Breadth-first traversal preserves authored connection-list order for equal
    hop-count routes. The resulting route is transient and remains provisional
    until the sequential movement executor completes each hop.
    """
    target = action.get("target")
    if not isinstance(target, str) or not target:
        return build_interaction_result(False, "movement", "Where do you want to go?", action)

    root_location = scene_snapshot.get("location", {})
    root_id = root_location.get("location_id", "__current_location__")
    target_name = _normalize_destination_name(target)
    visited_location_ids = {root_id}
    pending_routes = deque([(root_location, [])])

    while pending_routes:
        location, hops = pending_routes.popleft()
        connections = location.get("connected_locations", [])
        if not isinstance(connections, list):
            continue

        for connection in connections:
            if not isinstance(connection, dict):
                continue
            destination_id = connection.get("location_id")
            if destination_id in visited_location_ids:
                continue

            hop = _resolve_connection_movement(
                connection,
                {"location": location},
                locations,
            )
            if hop is None:
                continue

            next_hops = [*hops, hop]
            if _normalized_location_name(destination_id, locations) == target_name:
                return build_interaction_result(
                    True,
                    "movement",
                    " ".join(route_hop["message"] for route_hop in next_hops),
                    {**action, "type": "move"},
                    {
                        "destination_location_id": hop["destination_location_id"],
                        "movement_hops": next_hops,
                    },
                )

            destination = _location_by_id(destination_id, locations)
            if destination is not None:
                visited_location_ids.add(destination_id)
                pending_routes.append((destination, next_hops))

    return build_interaction_result(
        False,
        "movement",
        "You cannot reach that destination locally.",
        action,
    )


def resolve_two_hop_destination_route(
    action: Dict[str, Any],
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]],
) -> Dict[str, Any]:
    """Resolve one uniquely eligible A -> B -> C local route without mutation."""

    target = action.get("target")
    if not isinstance(target, str) or not target:
        return build_interaction_result(
            success=False,
            intent="movement",
            message="Where do you want to go?",
            action=action,
        )

    source_connections = scene_snapshot.get("location", {}).get(
        "connected_locations", []
    )
    eligible_routes: list[tuple[Dict[str, Any], Dict[str, Any]]] = []
    for first_connection in source_connections if isinstance(source_connections, list) else []:
        if not isinstance(first_connection, dict):
            continue

        intermediate_location = _location_by_id(
            first_connection.get("location_id"), locations
        )
        if intermediate_location is None:
            continue

        intermediate_scene = {"location": intermediate_location}
        intermediate_connections = intermediate_location.get(
            "connected_locations", []
        )
        for second_connection in _matching_named_connections(
            intermediate_connections,
            target,
            locations,
        ):
            first_hop = _resolve_connection_movement(
                first_connection,
                scene_snapshot,
                locations,
            )
            second_hop = _resolve_connection_movement(
                second_connection,
                intermediate_scene,
                locations,
            )
            if first_hop is not None and second_hop is not None:
                eligible_routes.append((first_hop, second_hop))

    if len(eligible_routes) != 1:
        return build_interaction_result(
            success=False,
            intent="movement",
            message=(
                "That local destination is ambiguous."
                if len(eligible_routes) > 1
                else "You cannot reach that destination locally."
            ),
            action=action,
        )

    first_hop, second_hop = eligible_routes[0]
    movement_action = {**action, "type": "move"}
    return build_interaction_result(
        success=True,
        intent="movement",
        message=f"{first_hop['message']} {second_hop['message']}",
        action=movement_action,
        extra={
            "destination_location_id": second_hop["destination_location_id"],
            "movement_hops": [first_hop, second_hop],
        },
    )


def resolve_three_hop_destination_route(
    action: Dict[str, Any],
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]],
) -> Dict[str, Any]:
    """Resolve one uniquely eligible A -> B -> C -> D local route."""

    target = action.get("target")
    if not isinstance(target, str) or not target:
        return build_interaction_result(False, "movement", "Where do you want to go?", action)

    source_connections = scene_snapshot.get("location", {}).get("connected_locations", [])
    eligible_routes: list[tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]] = []
    for first_connection in source_connections if isinstance(source_connections, list) else []:
        if not isinstance(first_connection, dict):
            continue
        first_location = _location_by_id(first_connection.get("location_id"), locations)
        if first_location is None:
            continue
        first_scene = {"location": first_location}
        first_hop = _resolve_connection_movement(first_connection, scene_snapshot, locations)
        if first_hop is None:
            continue
        second_connections = first_location.get("connected_locations", [])
        for second_connection in second_connections if isinstance(second_connections, list) else []:
            if not isinstance(second_connection, dict):
                continue
            second_location = _location_by_id(second_connection.get("location_id"), locations)
            if second_location is None:
                continue
            second_scene = {"location": second_location}
            second_hop = _resolve_connection_movement(second_connection, first_scene, locations)
            if second_hop is None:
                continue
            for third_connection in _matching_named_connections(
                second_location.get("connected_locations", []), target, locations
            ):
                third_hop = _resolve_connection_movement(third_connection, second_scene, locations)
                if third_hop is not None:
                    eligible_routes.append((first_hop, second_hop, third_hop))

    if len(eligible_routes) != 1:
        return build_interaction_result(
            False,
            "movement",
            "That local destination is ambiguous." if len(eligible_routes) > 1 else "You cannot reach that destination locally.",
            action,
        )

    first_hop, second_hop, third_hop = eligible_routes[0]
    return build_interaction_result(
        True,
        "movement",
        f"{first_hop['message']} {second_hop['message']} {third_hop['message']}",
        {**action, "type": "move"},
        {
            "destination_location_id": third_hop["destination_location_id"],
            "movement_hops": [first_hop, second_hop, third_hop],
        },
    )


def _resolved_movement(
    action: Dict[str, Any], connection: Dict[str, Any]
) -> Dict[str, Any]:
    direction = connection.get("direction")
    return build_interaction_result(
        success=True,
        intent="movement",
        message=f"You move {direction}.",
        action=action,
        extra={"destination_location_id": connection.get("location_id")},
    )


def _matching_named_connections(
    connected_locations: Any,
    target: str,
    locations: list[Dict[str, Any]],
) -> list[Dict[str, Any]]:
    if not isinstance(connected_locations, list):
        return []
    normalized_target = _normalize_destination_name(target)
    return [
        connection
        for connection in connected_locations
        if isinstance(connection, dict)
        and _normalized_location_name(connection.get("location_id"), locations)
        == normalized_target
    ]


def _location_by_id(
    location_id: Any,
    locations: list[Dict[str, Any]],
) -> Dict[str, Any] | None:
    for location in locations:
        if (
            isinstance(location, dict)
            and location.get("location_id") == location_id
        ):
            return location
    return None


def _resolve_connection_movement(
    connection: Dict[str, Any],
    scene_snapshot: Dict[str, Any],
    locations: list[Dict[str, Any]],
) -> Dict[str, Any] | None:
    direction = connection.get("direction")
    if not isinstance(direction, str) or not direction:
        return None

    hop_result = resolve_movement(
        {"type": "move", "target": direction, "parameters": {}, "confidence": 1.0},
        scene_snapshot,
        locations,
    )
    if (
        not hop_result["success"]
        or hop_result.get("destination_location_id") != connection.get("location_id")
    ):
        return None
    return hop_result


def _is_go_to_destination_command(player_input: str) -> bool:
    lowered = player_input.casefold()
    return lowered == "go to" or lowered.startswith("go to ")


def _is_move_to_destination_command(player_input: str) -> bool:
    lowered = player_input.casefold()
    return lowered == "move to" or lowered.startswith("move to ")


def _is_ambiguous_local_route(result: Dict[str, Any]) -> bool:
    return result.get("message") == "That local destination is ambiguous."


def extract_movement_target(player_input: str) -> str | None:
    lowered = player_input.lower()

    if lowered.startswith("move to "):
        return player_input[len("move to "):].strip() or None

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


def _normalized_location_name(
    location_id: Any,
    locations: list[Dict[str, Any]],
) -> str | None:
    for location in locations:
        if location.get("location_id") != location_id:
            continue
        name = location.get("name")
        if isinstance(name, str) and name.strip():
            return _normalize_destination_name(name)
    return None


def _normalize_name(value: str) -> str:
    return " ".join(value.casefold().split())


def _normalize_destination_name(value: str) -> str:
    normalized = _normalize_name(value)
    return normalized[4:] if normalized.startswith("the ") else normalized


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
