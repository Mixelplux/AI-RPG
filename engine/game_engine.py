from typing import Any, Dict

from engine.scene_loader import load_region, build_scene
from engine.perception_builder import build_perception
from engine.scene_narrator import narrate_scene
from engine.interaction_kernel import process_player_input
from engine.world_update import apply_interaction
from engine.region_validator import validate_region
from engine.world_state import (
    create_initial_world_state,
    get_player_location_id,
    set_player_location_id
)


class GameEngine:
    """
    Orchestrates the core AI Narrative RPG Engine pipeline.

    Runtime flow:
    Player Input
        -> Interaction Kernel
        -> Interaction Result
        -> World Update
        -> World State
        -> Scene Builder
        -> Scene Snapshot
        -> Narration / UI
    """

    def __init__(self, region_path: str, entry_location_id: str | None = None):
        self.region_path = region_path
        self.region = load_region(region_path)

        validate_region(self.region)

        self.world_state = create_initial_world_state(self.region)

        if entry_location_id is not None:
            self.world_state = set_player_location_id(
                self.world_state,
                entry_location_id
            )

        self.scene_snapshot = build_scene(
            self.region,
            self.world_state
        )

    def get_scene_snapshot(self) -> Dict[str, Any]:
        """
        Return the current Scene Snapshot.
        """

        return self.scene_snapshot

    def get_player_perception(self) -> Dict[str, Any]:
        """
        Build and return the current Player Perception.
        """

        return build_perception(self.scene_snapshot)

    def get_narration(self) -> Dict[str, Any]:
        """
        Build and return the current Narration Output.
        """

        perception = self.get_player_perception()
        return narrate_scene(perception)

    def process_command(self, player_input: str) -> Dict[str, Any]:
        """
        Process a player command.

        Returns the Interaction Result.
        """

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