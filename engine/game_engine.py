from copy import deepcopy
from typing import Any, Dict

from engine.scene_loader import load_region, build_scene
from engine.perception_builder import build_perception
from engine.scene_narrator import narrate_scene
from engine.interaction_kernel import process_player_input
from engine.world_update import apply_interaction
from engine.region_validator import validate_region
from engine.destination_resolver import (
    DestinationResolution,
    resolve_destination,
)
from engine.skill_check import SkillCheckResult, resolve_skill_check
from engine.target_resolver import TargetResolution, resolve_scene_target
from engine.timekeeper import advance_time_by_hours
from engine.history_context import build_history_context_packet
from engine.narration_context import build_narration_context_packet
from engine.world_state import (
    DEFAULT_HISTORY_QUERY_COUNT,
    add_history_entry,
    create_initial_world_state,
    get_history,
    get_history_entry_by_id,
    get_player_location_id,
    get_time,
    query_history,
    set_player_location_id,
    set_time,
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

    def get_history(self) -> list[Dict[str, Any]]:
        return get_history(self.world_state)

    def query_history(
        self,
        count: int | None = None,
        event_type: str | None = None,
        location: str | None = None
    ) -> list[Dict[str, Any]]:
        return query_history(
            self.world_state,
            count=count,
            event_type=event_type,
            location=location
        )

    def get_default_history_query_count(self) -> int:
        return DEFAULT_HISTORY_QUERY_COUNT

    def get_history_entry_by_id(
        self,
        history_id: str
    ) -> Dict[str, Any] | None:
        return get_history_entry_by_id(self.world_state, history_id)

    def get_history_context(
        self,
        count: int | None = None
    ) -> Dict[str, Any]:
        return build_history_context_packet(self.world_state, count=count)

    def get_narration_context(
        self,
        player_input: str,
        history_count: int | None = None
    ) -> Dict[str, Any]:
        return build_narration_context_packet(
            self.world_state,
            self.scene_snapshot,
            player_input,
            history_count=history_count
        )

    def advance_time(self, duration_hours: int = 1) -> Dict[str, Any]:
        previous_time = get_time(self.world_state)
        new_time = advance_time_by_hours(previous_time, duration_hours)
        location_id = get_player_location_id(self.world_state)

        self.world_state = set_time(self.world_state, new_time)
        self.world_state = add_history_entry(
            self.world_state,
            event_type="time_advanced",
            summary=f"Player waited for {duration_hours} hour.",
            location=location_id,
            time=new_time,
            extra={
                "previous_time": previous_time,
                "new_time": new_time
            }
        )
        self.scene_snapshot = build_scene(
            self.region,
            self.world_state
        )

        return {
            "duration_hours": duration_hours,
            "previous_time": previous_time,
            "new_time": new_time
        }

    def get_scene_snapshot(self) -> Dict[str, Any]:
        return deepcopy(self.scene_snapshot)

    def get_player_perception(self) -> Dict[str, Any]:
        return build_perception(self.scene_snapshot)

    def get_narration(self) -> Dict[str, Any]:
        perception = self.get_player_perception()
        return narrate_scene(perception)

    def perform_skill_check(self, check_name: str) -> SkillCheckResult:
        """Resolve a gameplay-facing check using deterministic placeholders."""

        return resolve_skill_check(
            check_name=check_name,
            target_difficulty=10,
            result_value=12,
        )

    def resolve_target(self, target_text: str) -> TargetResolution:
        """Resolve text against entities and exits in the current scene."""

        return resolve_scene_target(
            target_text,
            self.scene_snapshot,
            self.region.get("entities", []),
        )

    def resolve_destination(
        self,
        destination_text: str,
    ) -> DestinationResolution:
        """Identify a known region location without moving the player."""

        return resolve_destination(
            destination_text,
            self.region.get("locations", []),
        )

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

        if (
            interaction_result["intent"] == "skill_check"
            and interaction_result["success"]
        ):
            check_name = interaction_result["action"]["target"]
            interaction_result["skill_check"] = self.perform_skill_check(
                check_name
            )

        if (
            interaction_result["intent"] == "destination"
            and interaction_result["success"]
        ):
            destination_text = interaction_result["action"]["target"]
            destination_resolution = self.resolve_destination(
                destination_text
            )
            interaction_result["destination_resolution"] = (
                destination_resolution
            )
            interaction_result["success"] = (
                destination_resolution["status"] == "resolved"
            )
            if destination_resolution["status"] == "ambiguous":
                interaction_result["message"] = (
                    "That destination is ambiguous in the loaded region."
                )
            elif destination_resolution["status"] == "unresolved":
                interaction_result["message"] = (
                    "No known destination matches that name."
                )

        if (
            interaction_result["intent"] == "wait"
            and interaction_result["success"]
        ):
            duration_hours = interaction_result["action"]["parameters"][
                "duration_hours"
            ]
            interaction_result["time_advancement"] = self.advance_time(
                duration_hours
            )

        target_text = interaction_result["action"].get("target")
        if target_text and interaction_result["intent"] in {
            "conversation",
            "movement",
        }:
            target_resolution = self.resolve_target(target_text)
            interaction_result["target_resolution"] = target_resolution

            if (
                interaction_result["intent"] == "conversation"
                and target_resolution["status"] != "resolved"
            ):
                interaction_result["success"] = False
                if target_resolution["status"] == "ambiguous":
                    interaction_result["message"] = (
                        "That target is ambiguous in the current scene."
                    )
                else:
                    interaction_result["message"] = (
                        "No matching target is present in the current scene."
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
