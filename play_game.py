import sys
import re

from engine.game_engine import GameEngine
from engine.scene_continuity import SceneContinuity
from engine.scene_context import select_scene_sections


REGION_PATH = "data/regions/bryn_shander.json"
SAVE_PATH = "saves/savegame.json"


def configure_stdout() -> None:
    """Use UTF-8 for interactive output when the active stream can configure it."""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None and sys.stdout.encoding != "utf-8":
        reconfigure(encoding="utf-8")


def print_clue_presentation(presentation: dict) -> None:
    print(
        presentation.get("response_text") or "You cannot present that clue here."
    )


def print_narration(narration: dict, previous: dict | None = None,
                    result: dict | None = None) -> bool:
    description = narration["description"]
    sections = narration.get("scene_sections")
    if sections:
        selected = select_scene_sections(narration, previous, result)
        parts = [text for key in ("orientation", "conditions", "presence", "situation", "evidence", "choices", "other")
                 for text in (selected.get(key, []) if key in ("conditions", "evidence") else [selected.get(key)])
                 if text]
        if not parts:
            return False
        description = "\n\n".join(parts)
    print("\n=== SCENE ===\n")

    print(narration["title"])
    print()
    print(description)
    print()

    if narration.get("player_prompt"):
        print(narration["player_prompt"])
    return True


def print_composed_scene(engine, narration, previous=None, result=None, *, preparer=None, realizer=None):
    packet = engine.get_scene_narration(previous, result, preparer=preparer, realizer=realizer)
    if not packet["accepted"]:
        return print_narration(narration, previous, result)
    parts = [packet["display_text"]] if packet["display_text"] else []
    parts.extend(packet["guidance"][key] for key in ("choices", "other") if key in packet["guidance"])
    if not parts:
        return False
    return print_narration({"title": narration["title"], "description": "\n\n".join(parts)})


def print_scene_experience(engine: GameEngine, player_input: str,
                           continuity=None, stage="expand") -> None:
    """Present validated prose through the existing read-only narration boundary."""
    presentation = (continuity.presentation(engine.get_scene_snapshot(), player_input, stage)
                    if continuity is not None else None)
    packet = engine.get_narration_preview(player_input, presentation=presentation)
    if not packet["accepted"]:
        # Provider failure must be visible, without dumping grounding or errors.
        print("\nScene narration is unavailable. You can retry with 'look'.")
        return
    if continuity is not None:
        continuity.remember(packet["display_text"],
                            packet["narration_context"]["scene_context"]["conditions"])
    print_narration({
        "title": engine.get_scene_snapshot()["location"]["name"],
        "description": packet["display_text"],
    })


def travel_presentation(result, engine):
    """Compress only completed routine routes; preserve other result messages."""
    message = result.get("message", "")
    if (result["success"] and result["intent"] == "movement"
            and result.get("movement_hops")
            and re.fullmatch(r"(?:You move [a-z]+\.\s*)+", message)):
        name = engine.get_scene_snapshot()["location"]["name"]
        return f"You make your way to {name}."
    return message


def print_help() -> None:
    print("\nAvailable commands:")
    print("- save: Save the current game.")
    print("- load: Load the saved game.")
    print("- reset: Start a fresh game session.")
    print("- pressures: Show current scoped pressure state.")
    print("- clues: Recall discovered clues.")
    print("- present <clue title> to <actor>: Present a discovered clue.")
    print("- history: Show recent recorded world history.")
    print("- history recent <count>: Show recent world history.")
    print("- history type <event_type>: Show history by event type.")
    print("- history location <location_id>: Show history by location.")
    print("- history id <history_id>: Show one history entry by id.")
    print("- history context: Show a bounded history context packet.")
    print("- history context <count>: Show a bounded history context packet.")
    print("- narration context <player input>: Show narration context.")
    print("- narration output: Inspect the narration output contract.")
    print("- narration output invalid: Check a rejected mutation sample.")
    print("- narration preview <player input>: Show a fixed narration preview.")
    print("- wait: Let 1 hour pass.")
    print("- check <name>: Run a deterministic skill check.")
    print("- head to <place>: Identify a known destination without traveling.")
    print("- go to <place>: Travel along a known local route.")
    print("- investigate: Search the current area for clues.")
    print("- advocate patrol / continue investigation: Choose at the North Gate after reporting evidence to Elin.")
    print("- pursue observers / restore coverage: Follow up after patrol action.")
    print("- protect supply stop / locate raiders: Follow up after further investigation.")
    print("- follow withdrawal signs / reconstruct local observation circuit / arrange guarded local survey: Follow the watchers' tracks, compare their positions, or coordinate a search with Grey and Elin.")
    print("- help: Show this help message.")
    print("- quit or exit: End the game.")
    print("- Any other input is treated as a player action.")


def print_pressures(pressures: dict[str, dict]) -> None:
    print("\n=== PRESSURES ===")

    if not pressures:
        print("No active pressures.")
        return

    for pressure_id in sorted(pressures):
        pressure = pressures[pressure_id]
        provenance = pressure["provenance"]
        print(
            f"{pressure_id}: type={pressure['pressure_type']}; "
            f"scope={pressure['scope_type']}:{pressure['scope_id']}; "
            f"level={pressure['level']}; "
            f"provenance={provenance['kind']}:{provenance['source_id']}"
        )


def print_known_clues(clues: list[dict[str, str]]) -> None:
    print("\n=== KNOWN CLUES ===")
    if not clues:
        print("You have not discovered any clues.")
        return
    for clue in clues:
        print(f"- {clue['title']}: {clue['text']}")


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


def print_narration_output_contract(
    contract: dict,
    validation_result: dict | None = None,
    validation_error: str | None = None
) -> None:
    print("\n=== NARRATION OUTPUT CONTRACT ===")
    print(f"schema: {contract['schema']}")
    print(f"version: {contract['version']}")
    print(f"type: {contract['type']}")
    print(f"rule: {contract['rule']}")
    print(f"authority: {contract['authority']}")
    print(f"drift limit: {contract['drift_limit']}")
    print(f"example: {contract['atmosphere_example']}")
    print("required fields:")
    for field_name in contract["required_fields"]:
        print(f"- {field_name}")

    if validation_result is not None:
        print("sample validation: accepted")
        print(f"sample text: {validation_result['narration_text']}")

    if validation_error is not None:
        print("sample validation: rejected")
        print(f"reason: {validation_error}")


def print_narration_preview(packet: dict) -> None:
    print("\n=== NARRATION PREVIEW ===")
    print(f"schema: {packet['schema']}")
    print(f"version: {packet['version']}")
    print(f"accepted: {packet['accepted']}")
    print(f"source: {packet['source']}")
    print(f"display text: {packet['display_text']}")
    print(
        "context history entries: "
        f"{len(packet['narration_context']['history_context']['history_entries'])}"
    )

    if packet.get("error"):
        print(f"error: {packet['error']}")


def parse_narration_output_command(player_input: str) -> dict:
    normalized_input = player_input.strip().lower()

    if normalized_input == "narration output":
        return {"sample": "valid"}

    if normalized_input == "narration output invalid":
        return {"sample": "invalid"}

    return {
        "error": "Usage: narration output or narration output invalid."
    }


def parse_narration_preview_command(player_input: str) -> dict:
    prefix = "narration preview"
    stripped_input = player_input.strip()

    if stripped_input.lower() == prefix:
        return {
            "error": "Usage: narration preview <player input>."
        }

    if not stripped_input.lower().startswith(f"{prefix} "):
        return {
            "error": "Usage: narration preview <player input>."
        }

    return {
        "player_input": stripped_input[len(prefix):].strip()
    }


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


def main(*, narration_preparer=None, narration_realizer=None,
         scene_preparer=None, scene_realizer=None) -> None:
    configure_stdout()
    engine = GameEngine.start_new(REGION_PATH)

    print("\n=== AI Narrative RPG ===")
    print("Type 'help' for commands.")
    print("Type 'quit' or 'exit' to stop.\n")

    last_presented_narration = None
    continuity = SceneContinuity()
    scene_player_input = "look"
    scene_stage = "expand"
    last_interaction_result = None
    while True:
        narration = engine.get_narration()
        continuity.enter(engine.get_scene_snapshot()["location"]["location_id"])

        if narration != last_presented_narration:
            if engine.get_scene_snapshot()["location"]["location_id"] == "market_square":
                print_scene_experience(engine, scene_player_input, continuity, scene_stage)
            else:
                print_composed_scene(engine, narration, last_presented_narration, last_interaction_result,
                                     preparer=scene_preparer, realizer=scene_realizer)
            last_presented_narration = narration
            last_interaction_result = None

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
                continuity.clear()
                print("\nGame loaded.")
                for line in engine.get_resume_summary():
                    print(line)
                last_presented_narration = None
                last_interaction_result = None
                scene_player_input = "look"
            except FileNotFoundError:
                print("\nNo saved game found.")
            except ValueError as error:
                print(f"\nCould not load saved game: {error}")
            continue

        if normalized_input == "reset":
            engine.reset()
            continuity.clear()
            print("\nGame reset.")
            last_presented_narration = None
            last_interaction_result = None
            scene_player_input = "look"
            continue

        if normalized_input == "pressures":
            print_pressures(engine.get_pressures())
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

        if normalized_input == "narration output" or normalized_input.startswith(
            "narration output "
        ):
            narration_output_query = parse_narration_output_command(
                player_input
            )

            if narration_output_query.get("error"):
                print()
                print(narration_output_query["error"])
                continue

            contract = engine.get_narration_output_contract()
            valid_sample = {
                "schema": contract["schema"],
                "version": contract["version"],
                "narration_text": "The street remains quiet."
            }

            if narration_output_query["sample"] == "valid":
                try:
                    print_narration_output_contract(
                        contract,
                        validation_result=engine.validate_narration_output(
                            valid_sample
                        )
                    )
                except ValueError as error:
                    print_narration_output_contract(
                        contract,
                        validation_error=str(error)
                    )
            else:
                invalid_sample = {
                    **valid_sample,
                    "world_state": {
                        "player": {
                            "inventory": ["gloves"]
                        }
                    }
                }
                try:
                    validation_result = engine.validate_narration_output(
                        invalid_sample
                    )
                    print_narration_output_contract(
                        contract,
                        validation_result=validation_result
                    )
                except ValueError as error:
                    print_narration_output_contract(
                        contract,
                        validation_error=str(error)
            )
            continue

        if normalized_input == "narration preview" or normalized_input.startswith(
            "narration preview "
        ):
            narration_preview_query = parse_narration_preview_command(
                player_input
            )

            if narration_preview_query.get("error"):
                print()
                print(narration_preview_query["error"])
                continue

            print_narration_preview(
                engine.get_narration_preview(
                    narration_preview_query["player_input"]
                )
            )
            continue

        interaction_result = engine.process_command(player_input)
        last_interaction_result = interaction_result
        if interaction_result["success"]:
            scene_player_input = player_input
            scene_stage = "narrow" if interaction_result["intent"] == "conversation" else "follow"
        if interaction_result["success"] and interaction_result["intent"] in {
            "observation", "player_intention",
        }:
            stage = "expand" if normalized_input in {"look", "look around", "look here"} else "follow"
            print_scene_experience(engine, player_input, continuity, stage)
            continue
        actor_knowledge_response = interaction_result.get("actor_knowledge_response")
        if actor_knowledge_response is not None:
            print(actor_knowledge_response["text"])
        player_discovery_response = interaction_result.get("player_discovery_response")
        if player_discovery_response is not None:
            print(player_discovery_response["text"])
        specific_conversation_response = (
            interaction_result.get("intent") == "conversation"
            and (actor_knowledge_response is not None or player_discovery_response is not None)
        )
        if interaction_result.get("intent") == "clue_recall":
            print_known_clues(interaction_result["known_clues"])
        specific_response_printed = False
        if interaction_result.get("intent") == "clue_presentation" and "presentation" in interaction_result:
            presentation = interaction_result["presentation"]
            print_clue_presentation(presentation)
            specific_response_printed = True
        if interaction_result.get("intent") == "investigation" and "investigation" in interaction_result:
            investigation = interaction_result["investigation"]
            if investigation.get("changed"):
                print(investigation["text"])
            else:
                print("You find no new clues here.")
            specific_response_printed = True

        if interaction_result.get("message") and not specific_response_printed and not specific_conversation_response:
            print()
            if interaction_result.get("intent") == "west_road_decision" and not interaction_result["success"]:
                print(engine.get_narration().get("current_choice_hint", interaction_result["message"]))
            elif interaction_result.get("intent") == "west_road_decision":
                response = interaction_result["scene_response"]
                print(response["outcome"])
                print("Grey: " + response["grey"])
                print("Elin: " + response["elin"])
            elif interaction_result.get("intent") == "west_road_competence" and interaction_result["success"]:
                if interaction_result.get("changed"):
                    packet = engine.get_resolved_narration(
                        interaction_result["narrative_action_id"],
                        preparer=narration_preparer, realizer=narration_realizer,
                    )
                    if packet["accepted"]:
                        print(packet["display_text"])
                    else:
                        hours = interaction_result["accepted_outcome"]["cost_hours"]
                        print(("An hour passes." if hours == 1 else f"{hours} hours pass.") + "\n" + interaction_result["message"])
                else:
                    print("That approach has already been resolved. " + interaction_result["message"])
            else:
                print(travel_presentation(interaction_result, engine))

        if interaction_result.get("skill_check"):
            check_result = interaction_result["skill_check"]
            outcome = "succeeded" if check_result["succeeded"] else "failed"
            print(
                f"Skill check '{check_result['check_name']}' {outcome}: "
                f"result {check_result['result_value']} against "
                f"difficulty {check_result['target_difficulty']}."
            )

        if (interaction_result["success"] and interaction_result["intent"] == "conversation"
                and engine.get_scene_snapshot()["location"]["location_id"] == "market_square"):
            print_scene_experience(engine, player_input, continuity, "narrow")
            last_presented_narration = engine.get_narration()

        if interaction_result.get("time_advancement") and interaction_result.get("intent") not in {"west_road_decision", "west_road_competence"}:
            time_advancement = interaction_result["time_advancement"]
            print(
                "Time advanced: "
                f"{time_advancement['new_time'].get('elapsed_hours', 0) - time_advancement['previous_time'].get('elapsed_hours', 0)} hour."
            )

        target_resolution = interaction_result.get("target_resolution")
        if (
            target_resolution
            and target_resolution["status"] == "resolved"
            and interaction_result["intent"] != "movement"
            and not specific_conversation_response
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



if __name__ == "__main__":
    main()
