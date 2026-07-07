from engine.game_engine import GameEngine
from engine.save_system import save_game, load_game


REGION_PATH = "data/regions/bryn_shander.json"
SAVE_PATH = "saves/test_save.json"


def main():
    engine = GameEngine(REGION_PATH)

    starting_location = engine.get_world_state()["player"]["current_location_id"]
    print(f"Starting location: {starting_location}")

    engine.process_command("go south")

    moved_location = engine.get_world_state()["player"]["current_location_id"]
    print(f"Moved location: {moved_location}")

    save_game(engine, SAVE_PATH)

    loaded_engine = load_game(SAVE_PATH)
    loaded_world_state = loaded_engine.get_world_state()

    loaded_location = loaded_world_state["player"]["current_location_id"]
    print(f"Loaded location: {loaded_location}")

    assert loaded_location == moved_location
    assert loaded_world_state["weather"] == engine.get_world_state()["weather"]
    assert loaded_world_state["time"] == engine.get_world_state()["time"]

    print("Save/load test passed.")


if __name__ == "__main__":
    main()