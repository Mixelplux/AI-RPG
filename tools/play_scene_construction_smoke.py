"""Offline owner smoke from an unbriefed start; saves only in .artifacts.

The fixed failed draw belongs only to this launcher. Gameplay rules/RNG are
unchanged. The owner may converse, leave, or follow the suggested test route.
"""
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import play_game
from engine import character_competence


def main():
    print("Offline Scene Construction smoke: start at North Gate without prior briefing.")
    print("You may engage or leave. The launcher fixes only an investigation draw to failure.")
    with patch.object(play_game, "SAVE_PATH", ".artifacts/scene_construction_smoke_save.json"), \
         patch.object(character_competence, "draw_d6", return_value=1), \
         patch("engine.narration_source.OpenAI", side_effect=RuntimeError("Offline smoke")), \
         patch("socket.create_connection", side_effect=RuntimeError("Offline smoke")), \
         patch("socket.socket.connect", side_effect=RuntimeError("Offline smoke")):
        play_game.main()


if __name__ == "__main__":
    main()
