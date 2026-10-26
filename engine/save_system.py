import json
import os
from uuid import uuid4
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

from engine.game_engine import GameEngine
from engine.world_state import copy_world_state, validate_world_state
from engine import west_road_market_theft


SAVE_VERSION = 1
CAMPAIGN_SAVE_VERSION = 2
DOMAIN_SAVE_VERSION = 3


def build_save_data(engine: GameEngine) -> Dict[str, Any]:
    """
    Build a deterministic save payload.

    Save files persist runtime World State only.
    Scene Snapshots, perception, and narration are derived and are not saved.
    """

    from engine.consequence_integration import Runtime
    if type(engine) is Runtime and engine.domain_mode:
        from engine.domain_persistence import export
        return export(engine.campaign)
    runtime = engine._consequences
    if runtime is not None and runtime.campaign is not None:
        from engine.campaign_continuity import export
        return export(engine)
    engine.require_persistent_runtime()
    world_state = engine.get_world_state()
    validate_world_state(world_state)
    if "west_road_predicament" in engine.region or "material_targets" in engine.region:
        validate_world_state(world_state, engine.region)

    return {
        "save_version": SAVE_VERSION,
        "region_path": engine.get_region_path(),
        "world_state": copy_world_state(world_state)
    }


def save_game(engine: GameEngine, save_path: str) -> None:
    save_data = build_save_data(engine)

    path = Path(save_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if save_data["save_version"] in (CAMPAIGN_SAVE_VERSION, DOMAIN_SAVE_VERSION):
        runtime = engine._consequences if save_data['save_version'] == CAMPAIGN_SAVE_VERSION else None
        if runtime is not None:
            runtime.note("persistence", reason="capture")
        try:
            # Encoding must complete before opening any destination or temporary file.
            encoded = json.dumps(save_data, indent=2, allow_nan=False)
            atomic_write(path, encoded)
        except Exception:
            if runtime is not None:
                runtime.note("persistence", reason="write_failed")
            raise
        return
    with path.open("w", encoding="utf-8") as file:
        json.dump(save_data, file, indent=2)


def load_save_data(save_path: str) -> Dict[str, Any]:
    path = Path(save_path)

    duplicate_keys = False
    last_object_pairs = ()

    def decode_object(pairs):
        nonlocal duplicate_keys, last_object_pairs
        result = {}
        for key, value in pairs:
            if key in result:
                duplicate_keys = True
            result[key] = value
        # JSON objects are decoded bottom-up: for an object envelope the last
        # callback carries every top-level version entry, before key collapse.
        last_object_pairs = pairs
        return result

    with path.open("r", encoding="utf-8") as file:
        loaded_data = json.load(file, object_pairs_hook=decode_object)

    if (type(loaded_data) is dict and duplicate_keys
            and any(key == 'save_version' and type(value) is int and value == DOMAIN_SAVE_VERSION
                    for key, value in last_object_pairs)):
        # Reject duplicates anywhere in v3, including a version hidden by a
        # later duplicate. Preserve the existing v1/v2 last-key-wins behavior.
        raise ValueError('Duplicate JSON keys in version-3 save')

    save_data = deepcopy(loaded_data)

    if type(save_data) is not dict:
        raise ValueError("Invalid save envelope")
    if type(save_data.get("save_version")) is not int:
        raise ValueError("Invalid save version")
    if save_data.get("save_version") in (CAMPAIGN_SAVE_VERSION, DOMAIN_SAVE_VERSION):
        return save_data  # Strict complete validation in isolated reconstruction.
    if isinstance(save_data.get("world_state"), dict) and "continuing_gameplay" in save_data["world_state"]:
        raise ValueError("Version-2 campaign cannot be downgraded")
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
    if "resolved_threads" not in save_data["world_state"]:
        save_data["world_state"]["resolved_threads"] = {}
    if "actor_knowledge" not in save_data["world_state"]:
        save_data["world_state"]["actor_knowledge"] = {}
    if "evidence_traces" not in save_data["world_state"]:
        save_data["world_state"]["evidence_traces"] = []
    if "player_discoveries" not in save_data["world_state"]:
        save_data["world_state"]["player_discoveries"] = []
    player = save_data["world_state"].get("player")
    if not isinstance(player, dict):
        raise ValueError("Save World State player must be a dictionary.")
    player.setdefault("competences", [])
    save_data["world_state"].setdefault("competence_attempts", {})
    west_road_market_theft.normalize_loaded_state(save_data["world_state"])

    validate_world_state(save_data["world_state"])

    return save_data


def load_game(save_path: str, *, campaign_draw=None, require_campaign=False) -> GameEngine:
    save_data = load_save_data(save_path)
    if save_data['save_version'] == DOMAIN_SAVE_VERSION:
        if require_campaign:
            raise ValueError('Version-3 domains are not a version-2 I3 campaign')
        from engine.domain_persistence import restore
        from engine.game_session import GameSession
        try:
            return GameSession.start_domains(restore(save_data))
        except Exception:
            raise ValueError('Domain campaign restoration failed validation') from None
    if save_data["save_version"] == CAMPAIGN_SAVE_VERSION:
        from engine.campaign_continuity import restore
        try:
            return restore(save_data, draw=campaign_draw)
        except Exception as exc:
            # Public compatibility errors never contain hidden values from the file.
            raise ValueError("Campaign restoration failed validation or reconstruction") from None
    if require_campaign:
        raise ValueError("Version-1 saves cannot restore I3 campaign meaning")
    return GameEngine(
        region_path=save_data["region_path"],
        initial_world_state=save_data["world_state"]
    )


def atomic_write(path: Path, encoded: str) -> None:
    """One same-directory replacement; old destination survives pre-replace failures."""
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        # Cleanup failure must not mask the earliest write/replace error.
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise
