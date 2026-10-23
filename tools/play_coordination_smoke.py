"""Offline I1 smoke through GameEngine, with explicit test-owned domain suppliers.

No campaign mutation or search/stealth/navigation mechanic is implemented here.
"""
import argparse
from dataclasses import replace
from pathlib import Path
import socket
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.game_engine import GameEngine
from test_fixtures.coordination_suppliers import SituatedAuthority, context


def denied(*args, **kwargs):
    raise RuntimeError("This smoke is offline")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripted", action="store_true")
    parser.add_argument("--guards", choices=("none", "heard", "hidden"), default="none")
    parser.add_argument("--no-means", action="store_true")
    args = parser.parse_args()
    socket.create_connection = socket.socket.connect = socket.socket.connect_ex = denied
    current = context()
    if args.guards != "none":
        current = replace(current, actors=("fixture-guard",),
                          conditions=("footsteps" if args.guards == "heard" else "hidden-footsteps",))
    if args.no_means:
        current = replace(current, means=())
    authority = SituatedAuthority(current)
    engine = GameEngine("data/regions/market_passage_v1.json",
                        coordination_context=authority.supply, coordination_domain=authority)
    print("I1 common GameEngine runtime; hall, routes and domain results are stipulated offline fixtures.")
    print("Open the door | Can I open the door? | Prepare to open the door | Search the castle carefully")
    print("Search east or search west expresses a fixture-supported direction. Explicit clarification may offer numbers. Quit exits.")
    commands = iter(("Can I open the door?", "Prepare to open the door", "Search the castle",
                     "Search the castle carefully", "search west", "Open the door")) if args.scripted else None
    while True:
        if commands is not None:
            command = next(commands, None)
            if command is None:
                break
            print("> " + command)
        else:
            command = input("> ").strip()
        if command.casefold() == "quit":
            break
        if command == "continue":
            result = engine.process_coordination(resume=True)
        elif command.isdigit():
            result = engine.process_coordination(resume=True, answers=(command,))
        else:
            result = engine.process_command(command)
        print(result["message"])
        for choice in result.get("coordination", {}).get("choices", ()):
            print(choice["id"] + ": " + choice["text"])
    print(f"Stipulated domain totals: {len(authority.accepted)} accepted steps; {authority.minutes} fixture minutes.")
    print("Campaign world/save state is unchanged by these supplied fixture activities.")


if __name__ == "__main__":
    main()
