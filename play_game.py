from engine.game_engine import GameEngine


REGION_PATH = "data/regions/bryn_shander.json"


def print_narration(narration: dict) -> None:
    print("\n=== SCENE ===\n")

    print(narration["title"])
    print()
    print(narration["description"])
    print()

    if narration.get("visible_entities"):
        print("Visible:")
        for entity in narration["visible_entities"]:
            print(f"- {entity}")
        print()

    print(narration["player_prompt"])


def main() -> None:
    engine = GameEngine(REGION_PATH)

    print("\n=== AI Narrative RPG ===")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        narration = engine.get_narration()

        print_narration(narration)

        player_input = input("\n> ").strip()

        if player_input.lower() in ["quit", "exit"]:
            print("\nGoodbye.")
            break

        interaction_result = engine.process_command(player_input)

        if interaction_result.get("message"):
            print()
            print(interaction_result["message"])

        print(f"\n[Intent: {interaction_result['intent']}]")


if __name__ == "__main__":
    main()