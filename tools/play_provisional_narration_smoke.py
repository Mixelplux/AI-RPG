"""Provider-free experiential smoke, with a real engine-resolved failed search.

Run from repository root. Fixtures and fixed draw are smoke-only; normal gameplay
retains its original rules/RNG. Saves stay in the generated-artifact directory.
"""
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import play_game
from engine import character_competence
from engine.game_engine import GameEngine


def main():
    engine = GameEngine(play_game.REGION_PATH)
    for command in ("go to Southwest Trade Road", "investigate", "talk to Mara",
                    "go to North Gate", "present Repeated Watch Tracks to Elin",
                    "present Mara's Account to Elin", "advocate patrol"):
        if not engine.process_command(command)["success"]:
            raise RuntimeError("Smoke setup did not reach the existing withdrawal situation.")
    print("Offline narrative smoke: at North Gate after the guards' patrol.")
    print("Enter 'follow withdrawal signs' to experience the resolved failed search, then 'quit'.")
    with patch.object(play_game.GameEngine, "start_new", return_value=engine), \
         patch.object(play_game, "SAVE_PATH", ".artifacts/provisional_smoke_save.json"), \
         patch.object(character_competence, "draw_d6", return_value=1), \
         patch("engine.narration_source.OpenAI", side_effect=RuntimeError("Offline smoke")):
        play_game.main()


if __name__ == "__main__":
    main()
