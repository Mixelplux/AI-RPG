"""Disposable offline gameplay smoke using the focused test suppliers.

No campaign files, saves, providers or natural-language interpretation. Menus
select stipulated contexts/methods; the common engine still computes outcomes.
"""
import argparse
from dataclasses import replace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.information_adjudication import propose_assessed
from engine.information_resolution import AccessGrant, BindingTerms, Constraint
from test_information_adjudication import (
    ACCESS, AUTHORED, HIDDEN, agreement, attempt, fact, premises, session, ward,
)


def make_session(domain, *, informed=False):
    if domain == "ward":
        if informed:
            inference = fact("actor", "inference", "The effect may depend on the chosen method.",
                             epistemic="inference", holder="actor")
            report = fact("actor", "report", "A guide reports that old barriers once stood here.",
                          epistemic="claim", holder="actor")
            return session(facts=(*premises(), inference, report), constraints=(ward(),),
                           grants=tuple(AccessGrant(f.id, "actor", ACCESS) for f in (inference, report)))
        return session(constraints=(ward(),))
    if domain == "agreement":
        retained = Constraint("departure-obligation", ("place",), ("leave",), BindingTerms(
            ("block",), prerequisites=("commitment=agreement-terms|pay one silver on departure",)), AUTHORED)
        return session(constraints=(agreement(), retained),
                       grants=(AccessGrant("agreement-terms", "actor", ACCESS),))
    return session(draw=3)  # controlled ordinary partial d6 result, not selected by engine domain


def act(s, command):
    if command == "status":
        print(f"Elapsed effort: {s.state.at}; accepted interactions: {len(s.state.history)}")
        print("Available: " + ", ".join(f"{n} {r}" for a, r, n in s.state.inventory))
        return
    if command in {"look", "inquire"}:
        prior = next((a for a in reversed(s.state.history) if a.attempt.actor == "actor"), None)
        if prior is None:
            print("No accepted observation is available to inquire about.")
            return
        request = replace(prior.attempt, at=s.state.at,
                          authorization=replace(prior.attempt.authorization, intent="inquiry"))
        reply = s.step(request)
        if reply["context"] is None:
            print("The inquiry response is unavailable; no action or consequence was published.")
        else:
            for record in reply["context"]["developments"]:
                print(record["meaning"])
        return
    method = {"remove": "unweave", "leave": "depart", "invalid": "float"}.get(command, command)
    if method not in {"hook", "float", "unweave", "revoke", "depart", "lift"}:
        print("Choose a listed method.")
        return
    kwargs = {"binding": HIDDEN} if method == "unweave" else {"binding": "agreement-terms"} if method == "revoke" else {}
    request = attempt(s, method, **kwargs)
    proposal = (lambda a: replace(propose_assessed(a), costs=(("potion", 99),))) if command == "invalid" else propose_assessed
    result = s.step(request, proposal)
    if result["context"] is not None:
        for record in result["context"]["developments"]:
            print(record["meaning"])
    else:
        print(f"Technical/control response: {result['status']}. No fictional action or consequence was published.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripted", action="store_true")
    parser.add_argument("--informed", action="store_true", help="Supply legitimate retained inference/report in the ward context")
    args = parser.parse_args()
    if args.scripted:
        for domain, commands in (("ward", ("hook", "float", "inquire", "status", "invalid", "remove", "float")),
                                 ("agreement", ("hook", "revoke", "leave")),
                                 ("mundane", ("lift",))):
            print("\n" + domain.upper())
            s = make_session(domain, informed=args.informed)
            for command in commands:
                print("> " + command)
                act(s, command)
        return
    print("Offline supplied contexts; d6 is controlled, all state is disposable.")
    domain = input("Context [ward/agreement/mundane]: ").strip().lower()
    if domain not in {"ward", "agreement", "mundane"}:
        parser.error("Choose ward, agreement or mundane")
    s = make_session(domain, informed=args.informed)
    print("Methods: hook, float, remove, revoke, leave, lift; invalid, inquire/look, status, quit.")
    while True:
        command = input("> ").strip().lower()
        if command in {"quit", "exit"}:
            return
        act(s, command)


if __name__ == "__main__":
    main()
