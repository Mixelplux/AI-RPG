from typing import Dict, Any

from engine.scene_loader import load_region, build_scene, print_scene
from engine.perception_builder import build_perception
from engine.scene_narrator import narrate_scene
from engine.llm_prompt_builder import build_narration_prompt


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
    region = load_region("data/regions/bryn_shander_v0_2.json")

    scene = build_scene(region)
    print_scene(scene)

    perception = build_perception(scene)
    print_perception(perception)

    narration = narrate_scene(perception)
    print_narration(narration)

    prompt = build_narration_prompt(narration)
    print_llm_prompt(prompt)