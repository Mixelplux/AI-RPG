"""Offline owner experience of ordinary input through the common GameEngine.

Slash controls supply fixture events and persistence, never fictional outcomes.
"""
import argparse
from pathlib import Path

from engine.campaign_records import Boundary
from engine.save_system import load_game
from test_fixtures.continuity_suppliers import Draws
from test_fixtures.player_activity_suppliers import InspectionSuppliers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripted", action="store_true")
    parser.add_argument("--target", default="cargo panel")
    parser.add_argument("--duration", type=int, default=19)
    args = parser.parse_args()
    suppliers = InspectionSuppliers(args.target, duration=args.duration, draws=Draws(3, 6))
    engine = suppliers.engine()
    path = Path(".artifacts/m2-owner-smoke.json")
    sequence = iter((f"can I inspect the {args.target}?", f"prepare to inspect {args.target}",
        f"inspect {args.target}", "/interrupt", "continue", "/save", "/restore", "retry",
        "continue", "/clear", "continue", "inspect surface finding", "/status", "/quit"))
    print(f"Inspection target: {args.target}. Enter ordinary supported instructions.")
    print("Fixture controls: /interrupt /clear /save /restore /status /quit. Retry repeats the latest accepted request.")
    while True:
        text = next(sequence) if args.scripted else input("> ").strip()
        if args.scripted:
            print("> " + text)
        data = engine.get_campaign_state()
        if text == "/quit":
            break
        if text in {"/interrupt", "/clear"}:
            if not data.activities:
                print("Begin an inspection first.")
                continue
            engine.revise_campaign(undertaking=data.activities[0].id,
                                   boundary=Boundary(blocked=text == "/interrupt"))
            print("Fixture supplied a current interruption." if text == "/interrupt" else
                  "Fixture supplied circumstances permitting continuation.")
        elif text == "/save":
            engine.save(str(path))
            print("Saved the accepted campaign snapshot.")
        elif text == "/restore":
            # Independent engine and services; no session-local parser/ID cache.
            engine = load_game(str(path), campaign_draw=Draws(6))
            suppliers = InspectionSuppliers(args.target, duration=args.duration)
            engine.set_player_activity_context(suppliers.context)
            print("Independently restored; current domain services installed.")
        elif text == "/status":
            print(f"{data.state.adjudication.at} seconds; {data.state.adjudication.inventory[0][2]} lamp units; "
                  f"{len(data.state.receipts)} accepted increments.")
        else:
            kwargs = {}
            if text == "retry" and data.state.receipts:
                kwargs["request_id"] = data.state.receipts[-1].request.id
            result = engine.process_command(text, **kwargs)
            print(result["message"])
            if args.scripted:
                status = result["coordination"]["status"]
                if text == "retry" or text.startswith("inspect ") or text == "continue" and not data.activities[0].boundary.blocked:
                    assert status == "accepted", result
                elif text == "continue":
                    assert status != "accepted", result
    if args.scripted:
        data = engine.get_campaign_state()
        assert data.state.adjudication.at == 2 * args.duration + 7
        assert data.state.adjudication.inventory == (("actor", "lamp", 2),)
        assert len(data.state.receipts) == 3
        print("Scripted integrated sequence passed.")


if __name__ == "__main__":
    main()
