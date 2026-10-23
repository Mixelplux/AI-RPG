"""Stipulated owning-domain suppliers for I1 tests and offline smoke only."""
from dataclasses import replace
from engine.activity_control import ActivityCheckpoint, ActivityDevelopment
from engine.gameplay_coordination import AcceptedStep, DomainStep, SituatedContext, Target

def context(**changes):
    initial = SituatedContext(
        "revision-1", "hall-a",
        targets=(Target("door-x", ("door", "door x"), "open", ("handle",), "handle"),
                 Target("site-x", ("castle", "site"), "search", ("survey",), "survey")),
        routes=("east", "west"), means=("hands",),
        accessible=(("scene", "You are in the hall beside a door."),
                    ("routes", "One passage leads east, while another continues west."),
                    ("east", "Search toward the eastern passage."),
                    ("west", "Search toward the western passage."),
                    ("risk", "You hear approaching footsteps. Continue with the chosen approach?")))
    current = replace(initial, **changes)
    if "accessible" not in changes:
        routes = current.routes
        summary = ("One passage leads east, while another continues west." if routes == ("east", "west") else
                   " ".join("A passage leads " + route + "." for route in routes)
                   or "No accessible onward passage is established here.")
        public = tuple((ref, summary if ref == "routes" else text) for ref, text in current.accessible)
        public += tuple((r, "Search toward the " + r + " passage.") for r in routes if r not in dict(public))
        current = replace(current, accessible=public)
    return current


class SituatedAuthority:
    """Trusted fixture supplier with no engine handle and no invented mechanics.

    One minute of activity is stipulated test time, not an implemented rule.
    Failure injection occurs before publication. Receipts name this domain's
    accepted step. World/character access is explicit in context.accessible.
    """
    def __init__(self, current=None):
        self.current = current or context()
        self.accepted = ()
        self.minutes = 0
        self.assess_calls = 0
        self.execute_calls = 0
        self.failure = None
        self.required_means = ("hands",)
        self.conflicts = ()
        self.override = None
        self.result_kind = "negative"
        self.result_text = "You finish examining the hall. No useful signs turn up in the areas examined."
        self.executed_constraints = ()
        self.selected_directions = ()

    def supply(self):
        if self.failure == "context":
            raise RuntimeError("HIDDEN-CONTEXT")
        return self.current

    def assess(self, undertaking, current):
        self.assess_calls += 1
        if self.failure == "assess":
            raise RuntimeError("HIDDEN-DOMAIN")
        if self.override is not None:
            return self.override
        if undertaking.activity not in {"open", "search"}:
            return None
        responsibilities = ("world", "action")
        if current.actors:
            responsibilities += ("actors",)
        if undertaking.constraints:
            responsibilities += ("character",)
        developments, choices = (), ()
        step_ref = undertaking.target + ":" + current.location
        completed = undertaking.activity == "open" and step_ref in undertaking.accepted_steps
        if "footsteps" in current.conditions or "hidden-footsteps" in current.conditions:
            key = "risk:" + current.revision
            developments = (ActivityDevelopment("increased_discovery_risk",
                            perceived="footsteps" in current.conditions,
                            potentially_objectionable=True, choice_key=key),)
            if "footsteps" in current.conditions:
                choices = ((key, "risk"),)
        boundary, responses = "clarification", ()
        public_refs = ("scene",)
        if undertaking.activity == "search" and undertaking.accepted_steps:
            step_ref += ":next"
            boundary = "decision"
            public_refs = ("routes",)
            if len(current.routes) > 1:
                choices = tuple(("route:" + current.revision + ":" + r, r) for r in current.routes)
                responses = tuple(("search " + r, key) for r, (key, _) in zip(current.routes, choices))
                selected = next((key for key, _ in choices if key in undertaking.answered_choices), None)
                developments += (ActivityDevelopment("player_choice", choice_key=selected),)
            completed = step_ref in undertaking.accepted_steps
        if completed:
            public_refs, choices, responses = ("accepted:" + step_ref,), (), ()
        checkpoint = ActivityCheckpoint(undertaking.ref, undertaking.method,
                     complete=completed, blocked=undertaking.activity == "search" and bool(undertaking.accepted_steps) and not current.routes,
                     conflicting_constraints=self.conflicts, developments=developments,
                     resolution_ref=step_ref if completed else None)
        return DomainStep(step_ref, checkpoint, responsibilities,
                          self.required_means, public_refs, choices, ("quietly", "carefully"), boundary, responses)

    def execute(self, undertaking, step, current):
        self.execute_calls += 1
        if self.failure == "execute":
            raise RuntimeError("HIDDEN-EXECUTION")
        # Fixture domain owns atomic acceptance and repeats the current-state check.
        if current != self.current or step.ref in self.accepted:
            raise ValueError("stale or duplicate")
        direction = None
        if undertaking.activity == "search" and undertaking.accepted_steps:
            direction = next((route for route in current.routes
                              if "route:" + current.revision + ":" + route in undertaking.answered_choices), None)
            if direction is None and len(current.routes) == 1:
                direction = current.routes[0]
            if direction is None:
                raise ValueError("No authorized direction")
        text = (self.result_text if direction is None else
                "You finish examining the passage to the " + direction + ". No useful signs turn up there.") if undertaking.activity == "search" else "The door opens into the adjoining room."
        outcome = (self.result_kind if direction is None else "negative") if undertaking.activity == "search" else "positive"
        receipt = AcceptedStep(step.ref, ("result",), outcome, (("result", text),))
        accepted, minutes = self.accepted + (step.ref,), self.minutes + 1
        new_context = replace(current, revision=current.revision + ":accepted:" + step.ref,
                              accessible=current.accessible + (("accepted:" + step.ref, text),))
        self.accepted, self.minutes, self.current = accepted, minutes, new_context
        self.executed_constraints += (undertaking.constraints,)
        if direction is not None:
            self.selected_directions += (direction,)
        return receipt
