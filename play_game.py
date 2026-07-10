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
    print("- history: Show recent recorded world history.")
    print("- history recent <count>: Show recent world history.")
    print("- history type <event_type>: Show history by event type.")
    print("- history location <location_id>: Show history by location.")
    print("- history id <history_id>: Show one history entry by id.")
    print("- history context: Show a bounded history context packet.")
    print("- history context <count>: Show a bounded history context packet.")
    print("- narration context <player input>: Show narration context.")
    print("- wait: Let 1 hour pass.")
    print("- check <name>: Run a deterministic skill check.")
    print("- head to <place>: Identify a known destination without traveling.")
    print("- help: Show this help message.")
    print("- quit or exit: End the game.")
    print("- Any other input is treated as a player action.")


def print_history(history: list[dict]) -> None:
    print("\n=== HISTORY ===")

    if not history:
        print("No history recorded yet.")
        return

    for index, entry in enumerate(history, start=1):
        context = []
        if entry.get("location"):
            context.append(f"location: {entry['location']}")
        if entry.get("time"):
            context.append(f"time: {entry['time']}")
        if entry.get("previous_time"):
            context.append(f"previous time: {entry['previous_time']}")
        if entry.get("new_time"):
            context.append(f"new time: {entry['new_time']}")

        suffix = f" ({'; '.join(context)})" if context else ""
        history_id = f"{entry['history_id']} " if entry.get("history_id") else ""
        print(
            f"{index}. {history_id}[{entry['event_type']}] "
            f"{entry['summary']}{suffix}"
        )


def print_history_context(packet: dict) -> None:
    print("\n=== HISTORY CONTEXT ===")
    print(f"schema: {packet['schema']}")
    print(f"version: {packet['version']}")
    print(
        "limit: "
        f"{packet['limit']} "
        f"(default {packet['default_limit']}, max {packet['max_limit']})"
    )
    print(f"current time: {packet['current_time']}")
    print(
        "current location: "
        f"{packet['player']['current_location_id']}"
    )

    history_entries = packet["history_entries"]

    if not history_entries:
        print("No history entries in context.")
        return

    print("entries:")
    for index, entry in enumerate(history_entries, start=1):
        context = []
        if entry.get("location"):
            context.append(f"location: {entry['location']}")
        if entry.get("time"):
            context.append(f"time: {entry['time']}")

        suffix = f" ({'; '.join(context)})" if context else ""
        history_id = f"{entry['history_id']} " if entry.get("history_id") else ""
        print(
            f"{index}. {history_id}[{entry['event_type']}] "
            f"{entry['summary']}{suffix}"
        )


def print_narration_context(packet: dict) -> None:
    print("\n=== NARRATION CONTEXT ===")
    print(f"schema: {packet['schema']}")
    print(f"version: {packet['version']}")
    print(f"player input: {packet['player_input']}")
    print(f"current time: {packet['current_time']}")
    print(
        "current location: "
        f"{packet['player']['current_location_id']}"
    )
    print(f"scene id: {packet['scene_snapshot']['scene_id']}")
    print(
        "scene location: "
        f"{packet['scene_snapshot']['location']['location_id']}"
    )
    print(
        "history context entries: "
        f"{len(packet['history_context']['history_entries'])}"
    )
    print(f"boundary: {packet['boundary']['rule']}")
    print(f"drift guardrail: {packet['boundary']['drift_guardrail']}")

    history_entries = packet["history_context"]["history_entries"]

    if not history_entries:
        print("No history entries in narration context.")
        return

    print("history entries:")
    for index, entry in enumerate(history_entries, start=1):
        history_id = f"{entry['history_id']} " if entry.get("history_id") else ""
        print(
            f"{index}. {history_id}[{entry['event_type']}] "
            f"{entry['summary']}"
        )


def parse_narration_context_command(player_input: str) -> dict:
    prefix = "narration context"
    stripped_input = player_input.strip()

    if stripped_input.lower() == prefix:
        return {
            "error": "Usage: narration context <player input>."
        }

    if not stripped_input.lower().startswith(f"{prefix} "):
        return {
            "error": "Usage: narration context <player input>."
        }

    return {
        "player_input": stripped_input[len(prefix):].strip()
    }


def parse_history_query(player_input: str) -> dict:
    words = player_input.strip().split()

    if len(words) == 1:
        return {}

    query_type = words[1].lower()

    if query_type == "context":
        if len(words) == 2:
            return {"context": True}

        if len(words) == 3:
            try:
                count = int(words[2])
            except ValueError:
                return {"error": "History context count must be a number."}

            if count < 0:
                return {"error": "History context count must not be negative."}

            return {
                "context": True,
                "count": count
            }

        return {
            "error": (
                "Usage: history context or history context <count>."
            )
        }

    if len(words) < 3:
        return {
            "error": (
                "Usage: history recent <count>, history type <event_type>, "
                "history location <location_id>, history id <history_id>, "
                "or history context <count>."
            )
        }

    query_value = " ".join(words[2:]).strip()

    if query_type == "recent":
        try:
            count = int(query_value)
        except ValueError:
            return {"error": "History recent count must be a number."}

        if count < 0:
            return {"error": "History recent count must not be negative."}

        return {"count": count}

    if query_type == "type":
        return {"event_type": query_value}

    if query_type == "location":
        return {"location": query_value}

    if query_type == "id":
        return {"history_id": query_value}

    return {
        "error": (
            "Usage: history recent <count>, history type <event_type>, "
            "history location <location_id>, history id <history_id>, "
            "or history context <count>."
        )
    }


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

        if normalized_input == "history" or normalized_input.startswith(
            "history "
        ):
            history_query = parse_history_query(player_input)

            if history_query.get("error"):
                print()
                print(history_query["error"])
                continue

            if history_query.get("context"):
                try:
                    print_history_context(
                        engine.get_history_context(
                            count=history_query.get("count")
                        )
                    )
                except ValueError as error:
                    print()
                    print(error)
            elif history_query.get("history_id"):
                history_entry = engine.get_history_entry_by_id(
                    history_query["history_id"]
                )
                if history_entry is None:
                    print("\nNo history entry found for that id.")
                else:
                    print_history([history_entry])
            elif history_query:
                print_history(engine.query_history(**history_query))
            else:
                print_history(engine.query_history())
            continue

        if normalized_input == "narration context" or normalized_input.startswith(
            "narration context "
        ):
            narration_context_query = parse_narration_context_command(
                player_input
            )

            if narration_context_query.get("error"):
                print()
                print(narration_context_query["error"])
                continue

            print_narration_context(
                engine.get_narration_context(
                    narration_context_query["player_input"]
                )
            )
            continue

        interaction_result = engine.process_command(player_input)

        if interaction_result.get("message"):
            print()
            print(interaction_result["message"])

        if interaction_result.get("skill_check"):
            check_result = interaction_result["skill_check"]
            outcome = "succeeded" if check_result["succeeded"] else "failed"
            print(
                f"Skill check '{check_result['check_name']}' {outcome}: "
                f"result {check_result['result_value']} against "
                f"difficulty {check_result['target_difficulty']}."
            )

        if interaction_result.get("time_advancement"):
            time_advancement = interaction_result["time_advancement"]
            print(
                "Time advanced: "
                f"{time_advancement['previous_time']} -> "
                f"{time_advancement['new_time']}."
            )

        target_resolution = interaction_result.get("target_resolution")
        if (
            target_resolution
            and target_resolution["status"] == "resolved"
            and interaction_result["intent"] != "movement"
        ):
            print(f"Target: {target_resolution['display_name']}.")

        destination_resolution = interaction_result.get(
            "destination_resolution"
        )
        if (
            destination_resolution
            and destination_resolution["status"] == "resolved"
        ):
            print(
                f"Destination: {destination_resolution['display_name']}."
            )

        print(f"\n[Intent: {interaction_result['intent']}]")


if __name__ == "__main__":
    main()
