from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.game_engine import GameEngine


class GameSession:
    """Creates engine instances for new, loaded, and reset sessions."""

    @staticmethod
    def start_new(
        region_path: str,
        entry_location_id: str | None = None
    ) -> "GameEngine":
        from engine.game_engine import GameEngine

        return GameEngine(
            region_path=region_path,
            entry_location_id=entry_location_id
        )

    @staticmethod
    def load(save_path: str) -> "GameEngine":
        from engine.save_system import load_game

        return load_game(save_path)

    @staticmethod
    def reset(region_path: str) -> "GameEngine":
        return GameSession.start_new(region_path)
