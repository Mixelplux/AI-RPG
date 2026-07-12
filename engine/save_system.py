import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

from engine.game_engine import GameEngine
from engine.world_state import copy_world_state, validate_world_state


SAVE_VERSION = 1


def build_save_data(engine: GameEngine) -> Dict[str, Any]:
    """
    Build a deterministic save payload.

    Save files persist runtime World State only.
    Scene Snapshots, perception, and narration are derived and are not saved.
    """

    world_state = engine.get_world_state()
    validate_world_state(world_state)

    return {
        "save_version": SAVE_VERSION,
        "region_path": engine.get_region_path(),
        "world_state": copy_world_state(world_state)
    }


def save_game(engine: GameEngine, save_path: str) -> None:
    save_data = build_save_data(engine)

    path = Path(save_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(save_data, file, indent=2)


def load_save_data(save_path: str) -> Dict[str, Any]:
    path = Path(save_path)

    with path.open("r", encoding="utf-8") as file:
        loaded_data = json.load(file)

    save_data = deepcopy(loaded_data)

    if save_data.get("save_version") != SAVE_VERSION:
        raise ValueError(
            f"Unsupported save version: {save_data.get('save_version')}"
        )

    if "region_path" not in save_data:
        raise ValueError("Save file is missing region_path.")

    if "world_state" not in save_data:
        raise ValueError("Save file is missing world_state.")

    if not isinstance(save_data["world_state"], dict):
        raise ValueError("Save file world_state must be a dictionary.")

    if "pressures" not in save_data["world_state"]:
        save_data["world_state"]["pressures"] = {}
    if "actor_location_overrides" not in save_data["world_state"]:
        save_data["world_state"]["actor_location_overrides"] = {}
    if "open_threads" not in save_data["world_state"]:
        save_data["world_state"]["open_threads"] = {}
    if "actor_knowledge" not in save_data["world_state"]:
        save_data["world_state"]["actor_knowledge"] = {}
    if "evidence_traces" not in save_data["world_state"]:
        save_data["world_state"]["evidence_traces"] = []

    validate_world_state(save_data["world_state"])

    return save_data


def load_game(save_path: str) -> GameEngine:
    save_data = load_save_data(save_path)

    return GameEngine(
        region_path=save_data["region_path"],
        initial_world_state=save_data["world_state"]
    )
