"""Run from repository root with the official interpreter. Offline by default."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.damaged_gate import DamagedGate, GateFixture
from engine.narrative_realization import generate_with_provider


def main():
    parser = argparse.ArgumentParser(description="Standalone damaged-gate evaluation; session is not saved.")
    parser.add_argument("--development", choices=("choice", "ordinary", "none"), default="choice")
    parser.add_argument("--failure", choices=("lift", "lever", "repair"))
    parser.add_argument("--novice", action="store_true")
    parser.add_argument("--live", action="store_true", help="Explicit opt-in provider realization, at most eight calls per session")
    args = parser.parse_args()
    settings = dict(development=args.development, carpenter=not args.novice)
    if args.failure:
        settings[args.failure] = "failure"
    gate = DamagedGate(GateFixture(**settings))
    print("Damaged gate evaluation. Unsaved session. Type quit to end.")
    print("Describe your approach naturally. Examining, asking, attempting and stopping have different effects.")
    calls = 0

    def display(turn):
        nonlocal calls
        if args.live and calls < 8:
            calls += 1
            result = gate.present(turn, generate_with_provider)
            if result["status"] == "candidate":
                print(result["text"])
                return
            print("Narration unavailable. The accepted action stands; authoritative account follows.")
        records = turn["context"]["developments"]
        # The full current projection remains available to F01; deterministic
        # display uses it for observation rather than reciting it after each act.
        if turn["intent"] == "observe":
            records = [r for r in records if r["source"] == "Current observable gate projection" or r["status"] == "reported"]
        else:
            records = [r for r in records if r["source"] != "Current observable gate projection"]
        print(" ".join(item["meaning"] for item in records))

    display(gate.step("look"))
    while True:
        try:
            command = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if command.lower() in {"quit", "exit"}:
            break
        if command:
            display(gate.step(command))


if __name__ == "__main__":
    main()
