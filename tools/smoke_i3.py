"""Offline I3 owner smoke: declarative fixtures through the common GameEngine."""
import argparse
from pathlib import Path

from engine.campaign_records import Boundary
from engine.save_system import load_game
from test_fixtures.continuity_suppliers import Draws, engine, request, start


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripted", action="store_true")
    args = parser.parse_args()
    current = engine(draws=Draws(3, 6))
    undertaking = start(current)
    path = Path(".artifacts/i3-owner-smoke.json")
    print("Development fixture: finite inspection, four wedges, existing d6 mechanics.")
    print("Commands: progress, interrupt, save, restore, retry, resume, continue, depend, status, quit.")
    script = iter(("progress", "interrupt", "save", "restore", "retry", "resume", "continue", "depend", "status", "quit"))
    while True:
        command = next(script) if args.scripted else input("> ").strip().lower()
        if args.scripted:
            print("> " + command)
        if command == "quit":
            break
        if command == "progress":
            print(current.process_consequence(request(undertaking))["message"])
        elif command == "interrupt":
            current.revise_campaign(undertaking=undertaking, boundary=Boundary(blocked=True))
            print("Fixture supplies an interruption requiring reassessment. Accepted progress retained.")
        elif command == "save":
            current.save(str(path))
            print("Complete version-2 campaign saved.")
        elif command == "restore":
            current = load_game(str(path), campaign_draw=Draws(6))
            undertaking = current.get_campaign_state().activities[0].id
            print("Original engine discarded; fresh owners reconstructed from the file.")
        elif command == "retry":
            print(current.process_consequence(request(undertaking))["message"])
        elif command == "resume":
            result = current.process_consequence(request(undertaking, "next"))
            print(result["message"])
            if args.scripted:
                assert result["coordination"]["status"] != "accepted"
        elif command == "continue":
            current.revise_campaign(undertaking=undertaking, boundary=Boundary())
            print("Fixture supplies current circumstances in which the interruption no longer applies.")
            print(current.process_consequence(request(undertaking, "next"))["message"])
        elif command == "depend":
            dependent = current.begin_undertaking("search", "finding", "use")
            print(current.process_consequence(request(dependent, "dependent",
                target="finding", method="use", means=()))["message"])
        elif command != "status":
            print("Choose one listed fixture command.")
        state = current.get_campaign_state()
        print(f"Accepted seconds: {state.state.adjudication.at}; wedges: {state.state.adjudication.inventory[0][2]}; "
              f"receipts: {len(state.state.receipts)}; first undertaking effort: {state.activities[0].progress_seconds}s.")
    if args.scripted:
        state = current.get_campaign_state()
        assert state.state.adjudication.at == 69
        assert state.state.adjudication.inventory == (("actor", "wedge", 2),)
        assert len(state.state.receipts) == 3
        print("Offline smoke passed: progress, interruption, fresh restore, recognition, current-state continuation and dependency.")


if __name__ == "__main__":
    main()
