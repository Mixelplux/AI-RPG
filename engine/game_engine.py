from typing import Any, Dict

from engine.scene_loader import load_region, build_scene
from engine.perception_builder import build_perception
from engine.scene_narrator import narrate_scene
from engine.interaction_kernel import process_player_input
from engine.world_update import apply_interaction
from engine.region_validator import validate_region
from engine.world_state import (
    create_initial_world_state,
    set_player_location_id,
    copy_world_state,
    validate_world_state
)


class GameEngine:
    """
    Orchestrates the core AI Narrative RPG Engine pipeline.
    """

    def __init__(
        self,
        region_path: str,
        entry_location_id: str | None = None,
        initial_world_state: Dict[str, Any] | None = None
    ):
        self.region_path = region_path
        self.region = load_region(region_path)

        validate_region(self.region)

        if initial_world_state is None:
            self.world_state = create_initial_world_state(self.region)
        else:
            validate_world_state(initial_world_state)
            self.world_state = copy_world_state(initial_world_state)

        if entry_location_id is not None:
            self.world_state = set_player_location_id(
                self.world_state,
                entry_location_id
            )

        self.scene_snapshot = build_scene(
            self.region,
            self.world_state
        )

    @classmethod
    def start_new(
        cls,
        region_path: str,
        entry_location_id: str | None = None
    ) -> "GameEngine":
        from engine.game_session import GameSession

        return GameSession.start_new(region_path, entry_location_id)

    def get_region_path(self) -> str:
        return self.region_path

    def get_world_state(self) -> Dict[str, Any]:
        return copy_world_state(self.world_state)

    def get_scene_snapshot(self) -> Dict[str, Any]:
        return self.scene_snapshot

    def get_player_perception(self) -> Dict[str, Any]:
        return build_perception(self.scene_snapshot)

    def get_narration(self) -> Dict[str, Any]:
        perception = self.get_player_perception()
        return narrate_scene(perception)

    def save(self, save_path: str) -> None:
        """
        Persist the current engine state using the save system.

        Import is local to avoid a circular import:
        save_system depends on GameEngine for load reconstruction.
        """

        from engine.save_system import save_game

        save_game(self, save_path)

    def load(self, save_path: str) -> None:
        """
        Load saved engine state into this GameEngine instance.
        """

        from engine.game_session import GameSession

        loaded_engine = GameSession.load(save_path)

        self._replace_runtime_state(loaded_engine)

    def reset(self) -> None:
        """Replace the current runtime state with a fresh session."""

        from engine.game_session import GameSession

        fresh_engine = GameSession.reset(self.region_path)

        self._replace_runtime_state(fresh_engine)

    def _replace_runtime_state(self, other: "GameEngine") -> None:
        """Adopt canonical and derived runtime state from another engine."""

        self.region_path = other.region_path
        self.region = other.region
        self.world_state = other.get_world_state()
        self.scene_snapshot = other.get_scene_snapshot()

    def process_command(self, player_input: str) -> Dict[str, Any]:
        interaction_result = process_player_input(
            player_input,
            self.scene_snapshot
        )

        self.world_state = apply_interaction(
            self.world_state,
            interaction_result
        )

        self.scene_snapshot = build_scene(
            self.region,
            self.world_state
        )

        return interaction_result
