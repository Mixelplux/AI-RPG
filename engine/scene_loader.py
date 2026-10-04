import json
import math
from copy import deepcopy
from typing import Dict, Any

from engine.world_state import get_effective_actor_location, get_weather, get_time
from engine import west_road_market_theft


def resolve_spawn_count(rule: Dict[str, Any]) -> int:
    """
    Deterministic spawn resolution:
    - If count exists → use it
    - If count_range exists → midpoint (floor)
    """
    if "count" in rule:
        return rule["count"]

    if "count_range" in rule:
        min_v, max_v = rule["count_range"]
        return math.floor((min_v + max_v) / 2)

    return 0


def load_region(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_location(region: Dict[str, Any], location_id: str) -> Dict[str, Any] | None:
    for loc in region["locations"]:
        if loc["location_id"] == location_id:
            return loc
    return None


def get_static_entities(
    region: Dict[str, Any], world_state: Dict[str, Any], location_id: str
):
    static = []
    for entity in region.get("entities", []):
        if entity.get("persistence") == "static" and get_effective_actor_location(
            region, world_state, entity["entity_id"]
        ) == location_id:
            static.append(entity)
    return static


def resolve_spawns(location: Dict[str, Any]):
    spawned = []

    spawn_rules = location.get("spawn_rules", {})

    for template_name, rule in spawn_rules.items():
        count = resolve_spawn_count(rule)

        for _ in range(count):
            entity = {
                "template": rule["template"],
                "location": location["location_id"]
            }
            if isinstance(rule.get("display_name"), str) and rule["display_name"].strip():
                entity["display_name"] = rule["display_name"].strip()
            spawned.append(entity)

    return spawned


def build_scene(
    region: Dict[str, Any],
    world_state: Dict[str, Any],
    entry_location_id: str | None = None
):
    # STEP 1: resolve entry
    entry = entry_location_id or world_state["player"]["current_location_id"]

    location = find_location(region, entry)

    if location is None:
        raise ValueError(f"Location not found in Region Pack: {entry}")

    incident_text = west_road_market_theft.visible_text(world_state, entry)
    if incident_text:
        location = deepcopy(location)
        location["description_seed"] += " " + incident_text

    # STEP 2: static entities
    static_entities = get_static_entities(region, world_state, entry)

    # STEP 3: spawned entities
    spawned_entities = resolve_spawns(location)

    # STEP 4: factions
    factions = region.get("factions", [])

    # STEP 5: local state projection
    local_state = {
        "weather": get_weather(world_state),
        "time": get_time(world_state),
        "economy": region["region_state"]["economy_state"],
        "security": region["region_state"]["security_state"],
        "population": region["region_state"]["population_state"]
    }

    # STEP 6: scene snapshot
    exits = location.get("connected_locations", [])
    scene = {
        "scene_id": f"{entry}_0001",
        "tick": 0,
        "location": location,
        "exits": exits,
        "entities": {
            "static": [e["entity_id"] for e in static_entities],
            "spawned": spawned_entities
        },
        "factions": [f["faction_id"] for f in factions],
        "local_state": local_state,
        "debug": {
            "resolved_entry": entry,
            "spawn_counts": {
                k: resolve_spawn_count(v)
                for k, v in location.get("spawn_rules", {}).items()
            }
        }
    }

    return scene


def print_scene(scene: Dict[str, Any]):
    print("\n=== SCENE SNAPSHOT ===\n")

    loc = scene["location"]
    print(f"You are at: {loc['name']}")
    print(loc["description_seed"])
    print()

    weather = scene["local_state"]["weather"]
    print(f"Weather: {weather['type']} (severity {weather['severity']})")
    print(f"Wind: {weather['wind_speed_kmh']} km/h")
    print()

    time = scene["local_state"]["time"]
    print(f"Time: {time['current_date']} — {time['time_of_day']}")
    print()

    print("Entities present:")

    for e in scene["entities"]["static"]:
        print(f" - STATIC: {e}")

    for e in scene["entities"]["spawned"]:
        print(f" - SPAWNED: {e['template']}")

    print("\n======================\n")


def print_perception(perception: Dict[str, Any]):
    print("\n=== PERCEPTION SNAPSHOT ===\n")

    visible_location = perception["visible"]["location"]
    print(f"Visible location: {visible_location['name']}")
    print(f"Location ID: {visible_location['id']}")
    print()

    weather = perception["environment"]["weather"]
    print(f"Perceived weather: {weather['type']} (severity {weather['severity']})")
    print()

    print("Visible entities:")

    for e in perception["visible"]["entities"]["static"]:
        print(f" - STATIC: {e}")

    for e in perception["visible"]["entities"]["spawned"]:
        print(f" - SPAWNED: {e['template']}")

    print()
    print(f"Audible: {perception['audible']}")
    print(f"Hidden: {perception['hidden']}")

    print("\n===========================\n")


def print_narration(narration: Dict[str, Any]):
    print("\n=== NARRATION ===\n")

    print("Title:")
    print(narration["title"])
    print()

    print("Description:")
    print(narration["description"])
    print()

    print("Visible Entities:")
    for entity in narration["visible_entities"]:
        print(f" - {entity}")

    print()
    print("Prompt:")
    print(narration["player_prompt"])

    print("\n=================\n")


def print_llm_prompt(prompt: str):
    print("\n=== LLM PROMPT ===\n")
    print(prompt)
    print("\n==================\n")


if __name__ == "__main__":
    from engine.world_state import create_initial_world_state

    region = load_region("data/regions/bryn_shander_v0_3.json")
    world_state = create_initial_world_state(region)
    scene = build_scene(region, world_state)
    print_scene(scene)
