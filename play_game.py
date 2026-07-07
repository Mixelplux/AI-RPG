from engine.game_engine import GameEngine


REGION_PATH = "data/regions/bryn_shander.json"
SAVE_PATH = "saves/savegame.json"


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


def print_help() -> None:
    print("\nAvailable commands:")
    print("- save: Save the current game.")
    print("- load: Load the saved game.")
    print("- reset: Start a fresh game session.")
    print("- help: Show this help message.")
    print("- quit or exit: End the game.")
    print("- Any other input is treated as a player action.")


def main() -> None:
    engine = GameEngine.start_new(REGION_PATH)

    print("\n=== AI Narrative RPG ===")
    print("Type 'help' for commands.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        narration = engine.get_narration()

        print_narration(narration)

        player_input = input("\n> ").strip()
        normalized_input = player_input.lower()

        if normalized_input in ["quit", "exit"]:
            print("\nGoodbye.")
            break

        if normalized_input == "help":
            print_help()
            continue

        if normalized_input == "save":
            engine.save(SAVE_PATH)
            print("\nGame saved.")
            continue

        if normalized_input == "load":
            try:
                engine.load(SAVE_PATH)
                print("\nGame loaded.")
            except FileNotFoundError:
                print("\nNo saved game found.")
            except ValueError as error:
                print(f"\nCould not load saved game: {error}")
            continue

        if normalized_input == "reset":
            engine.reset()
            print("\nGame reset.")
            continue

        interaction_result = engine.process_command(player_input)

        if interaction_result.get("message"):
            print()
            print(interaction_result["message"])

        print(f"\n[Intent: {interaction_result['intent']}]")


if __name__ == "__main__":
    main()
