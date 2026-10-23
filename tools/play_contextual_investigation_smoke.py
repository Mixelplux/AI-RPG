"""Offline owner smoke; disposable saves stay under the checkout .artifacts directory."""
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import play_game


def blocked(*args, **kwargs):
    raise RuntimeError("Offline contextual investigation smoke")


def main():
    evidence = Path(__file__).resolve().parents[1] / ".artifacts" / "contextual-investigation-smoke"
    evidence.mkdir(parents=True, exist_ok=True)
    print("Contextual investigation smoke. Saves use .artifacts; providers are blocked.")
    with patch.object(play_game, "SAVE_PATH", str(evidence / "owner-smoke-save.json")), \
         patch("engine.narration_source.OpenAI", side_effect=blocked), \
         patch("socket.create_connection", side_effect=blocked), \
         patch("socket.socket.connect", side_effect=blocked), \
         patch("socket.socket.connect_ex", side_effect=blocked):
        play_game.main()


if __name__ == "__main__":
    main()
