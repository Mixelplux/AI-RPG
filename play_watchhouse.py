"""Offline Watchhouse M1 player entry point; no legacy save or provider access."""
import argparse
from pathlib import Path

from engine.game_session import GameSession
from engine.save_system import save_game
from engine.watchhouse import OPENING, WatchhouseSession


def main():
    parser = argparse.ArgumentParser(description='Watchhouse Records M1')
    parser.add_argument('--load', type=Path, help='Restore a Watchhouse V3 save')
    parser.add_argument('--save', type=Path, default=Path('.artifacts/watchhouse-player.json'))
    args = parser.parse_args()
    try:
        session = WatchhouseSession(GameSession.load(str(args.load))) if args.load else WatchhouseSession()
    except (OSError, ValueError):
        print('The Watchhouse save could not be restored. No campaign was adopted.')
        return
    print(OPENING)
    print("Use 'help' for examples, 'save' to save, 'review findings' to recall results, or 'quit' to leave.")
    while True:
        try:
            text = input('> ')
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if text.strip().casefold() == 'quit':
            return
        if text.strip().casefold() == 'help':
            print('Examples: Could I examine the ledger? / I ask Mara for her account / '
                  'I persuade Mara to let me examine the ledger / '
                  'I search the ledger for signs of tampering / I study the ledger notation. '
                  'Describe one action at a time. Unclear methods return control to you.')
            continue
        if text.strip().casefold() == 'save':
            # User-selected destination, independent of the legacy owner save.
            if args.save.resolve() == Path('saves/savegame.json').resolve():
                print('Choose a separate Watchhouse save destination.')
                continue
            try:
                args.save.parent.mkdir(parents=True, exist_ok=True)
                save_game(session.runtime, str(args.save))
                print('Saved.')
            except (OSError, ValueError):
                print('Save failed. The in-memory investigation is preserved.')
            continue
        print(session.process(text).message)


if __name__ == '__main__':
    main()
