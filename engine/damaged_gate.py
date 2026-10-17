"""Disposable damaged-gate evaluation; bounded suppliers, no campaign save API.

Fixture values stand in for missing upstream owners, not narrator inventions.
One copied candidate composes their distinct responsibilities. F05 alone decides
continuation at the supplied checkpoints. F01 receives safe accepted meaning.
"""
from copy import deepcopy
from dataclasses import dataclass
import re

from engine.activity_control import (
    ActivityAuthorization, ActivityCheckpoint, ActivityDevelopment,
    decide_activity_control,
)
from engine.narrative_realization import validate_context, realize


# Existing gate restriction policy, shared by initial and resumed execution.
RESTRICTION_CONFLICTS = ("no_damage",)


@dataclass(frozen=True)
class GateFixture:
    lift: str = "success"
    lever: str = "success"
    repair: str = "success"
    development: str = "choice"  # ordinary, choice, none
    carpenter: bool = True
    helper: bool = True
    timber: bool = True
    tools: bool = True

    def __post_init__(self):
        if any(value not in {"success", "failure"} for value in (self.lift, self.lever, self.repair)):
            raise ValueError("Unsupported controlled outcome")
        if self.development not in {"choice", "ordinary", "none"}:
            raise ValueError("Unsupported development")
        if any(type(getattr(self, key)) is not bool for key in ("carpenter", "helper", "timber", "tools")):
            raise ValueError("Expected explicit supplier flags")


def interpret(text, *, repair_started=False):
    """Small scenario vocabulary; ambiguity returns control, never another method."""
    text = re.sub(r"\s+", " ", text.lower().replace("’", "'")).strip()
    constraints = []
    for pattern, constraint in (
        (r"\b(?:alone|without (?:any |the )?(?:help|assistance|guard)|with no help)\b", "alone"),
        (r"\b(?:without (?:using )?(?:the )?timber|no timber|don't use (?:the )?timber)\b", "no_timber"),
        (r"\b(?:without (?:further )?(?:damage|damaging)|don't damage)\b", "no_damage"),
    ):
        if re.search(pattern, text):
            constraints.append(constraint)
            text = re.sub(pattern, " ", text)
    if re.search(r"\b(?:stop|abandon|leave it|give up|never mind|don't (?:lift|repair|pry|raise))\b", text):
        return "withdraw", None, tuple(constraints)
    # Conditional programs and extra consequential acts are deliberately unclaimed.
    if re.search(r"\b(?:if|unless|until|only|then|while|burn|break|smash|steal|bribe|promise|magic|spell|rope|horse|pay|secretly|attack|kill|threaten|explosives)\b", text):
        return "unsupported", None, tuple(constraints)
    text = re.sub(r"\b(?:the )?guard and i\b", "we", text)
    if " and " in text or re.search(r"\b(?:without|don't|must|never|but)\b|\b(?:do not|with no)\b", text):
        return "unsupported", None, tuple(constraints)
    # Only the existing repair can give these phrases a definite referent.
    # Full matches keep questions, proposals, extra acts and unfamiliar means
    # out of this authorization path. A bare "brace" remains ambiguous.
    if repair_started:
        instruction = re.sub(r"^(?:please |i |we |let's )", "", text).strip(" .!")
        if re.fullmatch(
            r"(?:brace (?:the )?(?:gate|hinge|it)(?: with (?:the )?timber)?|"
            r"use (?:the )?timber to brace(?: (?:the )?(?:gate|hinge|it))?|"
            r"finish(?: (?:the )?repair)? with (?:the |a )?timber brace)", instruction
        ):
            return "resume", "repair", tuple(constraints)
        # Here "with repair" names the activity, not a supplied resource.
        text = re.sub(r"^((?:please |i |we |let's )?(?:continue|resume|carry on)) with (?:the )?repair\b",
                      r"\1 repair", text)
    # Bound consequential means explicitly rather than silently substituting the
    # fixture's tools/helper for an unfamiliar requested resource.
    supplied_means = re.search(r"\b(?:with|using)\s+(.+)", text)
    if supplied_means:
        allowed = {"the", "a", "an", "available", "guard", "help", "assistance", "assisting",
                   "me", "us", "my", "our", "of", "tools", "tool", "timber", "brace", "support",
                   "leverage", "lever", "care", "carpentry", "experience", "knowledge"}
        if any(word not in allowed for word in re.findall(r"[a-z]+", supplied_means[1])):
            return "unsupported", None, tuple(constraints)
    methods = [name for name, pattern in (
        ("lift", r"\b(?:lift|lifting|raise|raising|heave)\b"),
        ("lever", r"\b(?:lever|leverage|pry|prying)\b|\buse (?:the |a )?timber to (?:open|move)\b"),
        ("repair", r"\b(?:repair|repairing|fix|fixing|mend|mending)\b"),
    ) if re.search(pattern, text)]
    inquiry = bool(re.match(r"^(?:can|could|would|should|is|are|what|how|do|does)\b", text) or
                   re.search(r"\b(?:consider|considering|thinking|wonder|might|maybe|plan|planning|want|intend)\b|\bi (?:can|could)\b", text))
    if len(methods) > 1:
        return "unsupported", None, tuple(constraints)
    method = methods[0] if methods else None
    if re.search(r"\b(?:lift|raise|heave|pry|repair|fix|mend) (?:the |a )?(?:cart|guard|timber|wall)\b", text):
        return "unsupported", None, tuple(constraints)
    if method == "lift" and "timber" in text:
        return "unsupported", None, tuple(constraints)
    if inquiry:
        return "inquiry", method, tuple(constraints)
    if re.search(r"\b(?:prepare|ready) to\b", text):
        return "preparation", method, tuple(constraints)
    if re.search(r"\b(?:examine|inspect|study|assess|check)\b", text):
        return "examine", None, tuple(constraints)
    if re.search(r"\b(?:ask|seek|fetch|find)\b.*\b(?:help|guard|assistance)\b", text):
        return "help", None, tuple(constraints)
    if re.search(r"\b(?:get|take|fetch|ready|prepare|pick up)\b.*\b(?:timber|tools)\b", text):
        return "prepare", None, tuple(constraints)
    if re.search(r"\b(?:continue|resume|carry on)\b", text):
        return "resume", method, tuple(constraints)
    if method:
        return "commit", method, tuple(constraints)
    if re.search(r"\b(?:look|observe|gate|cart|hinge|timber)\b", text) and (
            text.startswith(("look", "observe")) or text in {"gate", "cart", "hinge", "timber"}):
        return "observe", None, tuple(constraints)
    return "unsupported", None, tuple(constraints)


class DamagedGate:
    def __init__(self, fixture=None):
        self.fixture = fixture or GateFixture()
        self._state = dict(minutes=0, pins=2, timber_used=False, prepared=False, tools_prepared=False,
                           gate="jammed", damaged=True, cart_passed=False,
                           repair_stage="untouched", attempts={}, examined=False,
                           history=[], turn=0, repair_constraints=())

    @property
    def state(self):
        return deepcopy(self._state)

    def _scene(self, state):
        if state["cart_passed"]:
            opening = "The supply cart has passed through."
        else:
            opening = "The gate is jammed partly closed, blocking a supply cart."
        condition = "The hinge is repaired." if not state["damaged"] else "The hinge remains damaged."
        means = []
        if self.fixture.helper and not state["cart_passed"]:
            means.append("The guard is willing to help lift it.")
        if self.fixture.timber and not state["timber_used"]:
            means.append("A stout timber lies beside the wall, available for leverage or support.")
        if self.fixture.tools:
            pins = state["pins"]
            means.append(f"Repair tools and {pins} spare hinge {'pin is' if pins == 1 else 'pins are'} available.")
        return " ".join([opening, condition, *means])

    def _record(self, state, text, authority, status="established", source=None):
        record = dict(id=f"gate-{len(state['history'])}", meaning=text,
                      authority=authority, status=status,
                      source=source or "Bounded gate fixture and accepted session transition",
                      time=f"Established at elapsed minute {state['minutes']}",
                      access="Character present: direct observation or expressly supplied knowledge")
        state["history"].append(record)
        return record

    def _control(self, method, constraints=(), *, resolution_ref=None, **checkpoint):
        return decide_activity_control(
            ActivityAuthorization("clear_gate", method, constraints=tuple(constraints)),
            ActivityCheckpoint("clear_gate", method, resolution_ref=resolution_ref, **checkpoint))

    def step(self, text="look"):
        state = self.state
        start = len(state["history"])
        intent, method, constraints = interpret(text, repair_started=state["repair_stage"] != "untouched")
        control = None
        message, authority, status = self._apply(state, intent, method, constraints, text)
        if isinstance(message, tuple):
            message, control = message
        self._record(state, message, authority, status)
        # A current projection is derived from physical truth, never old helper prose.
        self._record(state, self._scene(state), "World Simulation / Actors & Social Dynamics",
                     source="Current observable gate projection")
        if not state["turn"]:
            self._record(state, "The guard says he suspects someone tampered with the hinge. This is his unverified belief, not an established cause.",
                         "Actors & Social Dynamics", "reported", "Guard's firsthand statement of his suspicion")
        state["turn"] += 1
        current = state["history"][start:]
        context = validate_context(dict(
            moment=f"Damaged gate: exchange {state['turn']}", focus="The player's current gate interaction",
            player_intent=dict(objective=text or "Observe the gate", method=method or intent,
                               authorization=intent, constraints=list(constraints)),
            developments=current, continuity=state["history"][:start],
            knowledge_limits=["The cause of the hinge damage is unknown. The guard's suspicion has not been verified.",
                              "Carpentry experience is stipulated." if self.fixture.carpenter else "No specialist carpentry knowledge is stipulated."],
            unresolved=["The cause of the original hinge damage remains unresolved."] +
                       (["Hinge damage remains."] if state["damaged"] else []),
            boundaries=["No new actions, agreements, resources, outcomes or progress may be established by narration.",
                        "Continuity records are historical: current physical projection takes precedence."]))
        self._state = state  # publish only after contract construction succeeds
        return dict(text=message, context=context, control=control, intent=intent)

    def _apply(self, s, intent, method, constraints, raw):
        ar = "Action & Resolution"
        if intent == "withdraw":
            return "You stop working on the gate. Established work, spent supplies and elapsed time remain.", ar, "established"
        if intent == "observe":
            return "You take in the obstruction and available means.", "Character System", "established"
        if intent == "preparation":
            return "You get ready beside the gate. No new attempt, elapsed work or supply cost is applied. Prior work and costs remain.", ar, "established"
        if intent == "unsupported":
            prior = ("The hinge remains secured and the repair is paused; prior work, elapsed time and the committed pin remain. Choose whether to use timber as a brace." if s["repair_stage"] == "secured" else
                     "Accepted results, elapsed time and spent supplies remain." if s["attempts"] else
                     "No attempt has begun; describe one approach using the means here.")
            return "That instruction is not clear enough to apply in this gate scenario. No new work or cost is applied. " + prior, ar, "established"
        if intent == "help":
            reply = ("The guard agrees to lend a hand with lifting the gate." if self.fixture.helper else
                     "The guard cannot leave his post to help with the gate.")
            return reply + " No new gate attempt begins; prior work and costs remain.", "Actors & Social Dynamics", "established"
        if intent == "prepare":
            tools = "tools" in raw.lower()
            available = self.fixture.tools if tools else self.fixture.timber and not s["timber_used"] and "no_timber" not in constraints
            resource, flag = ("tools", "tools_prepared") if tools else ("timber", "prepared")
            if not available:
                return f"You have no available {resource} to prepare under those conditions. No gate attempt begins.", ar, "established"
            if not s[flag]:
                s["minutes"] += 1
                s[flag] = True
                return f"You ready the available {resource} beside the gate, taking one minute. No new move or repair attempt begins; prior work and costs remain.", ar, "resolved"
            return f"The {resource} is already ready; no further preparation or time is spent.", ar, "established"
        if intent == "examine":
            if s["examined"]:
                return "You recall your examination: the hinge is bent; that does not establish how it was damaged.", "Character System", "established"
            s["minutes"] += 2
            s["examined"] = True
            finding = ("Your carpentry experience identifies the bent hinge and how the available tools and a spare pin could repair it." if self.fixture.carpenter else
                       "You can see the bent hinge, but cannot confidently judge a repair with your present knowledge.")
            return finding + " Examination takes two minutes. It does not establish tampering.", "Action & Resolution / Character System", "resolved"
        if intent == "inquiry":
            options = {"lift": "Lifting with the guard can clear the cart in a short attempt; the damaged hinge may still jam afterward. Success is uncertain.",
                       "lever": "Using the available timber as leverage can hold an opening for the cart. It commits the timber and may fail; it does not repair the hinge.",
                       "repair": "A repair uses carpentry knowledge, tools and one spare pin, taking about half an hour. It may fail. A newly needed support would require your choice."}
            unavailable = ((method is not None and "no_damage" in constraints) or
                           (method == "lift" and (not self.fixture.helper or "alone" in constraints)) or
                           (method == "lever" and (not self.fixture.timber or s["timber_used"] or "no_timber" in constraints)) or
                           (method == "repair" and (not self.fixture.carpenter or not self.fixture.tools or s["pins"] < 1)))
            answer = "That approach is not currently feasible with your means and conditions." if unavailable else options.get(method, "You can consider the available means shown here, examine the hinge, or ask the guard for help. An attempt needs a chosen approach.")
            return answer + " You have not authorized an attempt.", ar, "established"
        if intent == "resume":
            if s["repair_stage"] != "secured" or method not in {None, "repair"}:
                return "There is no paused activity matching that request. Accepted results remain unchanged.", ar, "established"
            method = "repair"
            previous_constraints = set(s["repair_constraints"])
            wants_support = bool(re.search(r"\b(?:timber|brace|support)\b", raw.lower()))
            if wants_support and "no_timber" not in constraints:
                previous_constraints.discard("no_timber")  # explicitly renewed means choice
            constraints = tuple(sorted(set(constraints) | previous_constraints))
            if "no_timber" in constraints or not wants_support:
                return "The hinge remains secured. Continuing now needs a timber brace; choose whether to use it or change approach. No more work or cost is applied.", ar, "established"
            decision = self._control(method, constraints, resolution_ref="repair",
                                     conflicting_constraints=RESTRICTION_CONFLICTS,
                                     missing_means=() if self.fixture.timber and not s["timber_used"] else ("timber",))
            if decision.status != "continue":
                reason = ("The repair cannot continue under that restriction. No further work or cost is applied."
                          if decision.reason == "authorization_constraint" else "The needed timber is unavailable.")
                return (reason + " The secured hinge, accepted repair result and spent costs remain.", decision), ar, "established"
            s["timber_used"] = True
            s["minutes"] += 5
            self._record(s, "You commit the timber to the brace, taking five minutes to fit the support before continuing the repair.", ar, "resolved")
            finished = self._finish_repair(s, 20)
            return (finished, self._control(method, constraints, resolution_ref="repair", complete=True)), ar, "resolved"
        if s["cart_passed"] and method != "repair":
            return "The cart has already passed. That goal needs no further attempt or cost; the current hinge condition remains.", ar, "established"
        if method in s["attempts"]:
            return "That attempt already has an accepted result. No new resolution or cost is applied. A secured repair needs an explicit continuation with its newly required support.", ar, "established"
        missing = []
        if method == "lift" and (not self.fixture.helper or "alone" in constraints):
            missing.append("assistance")
        if method == "lever" and (not self.fixture.timber or s["timber_used"] or "no_timber" in constraints):
            missing.append("timber")
        if method == "repair":
            if not self.fixture.carpenter:
                missing.append("repair knowledge")
            if not self.fixture.tools or s["pins"] < 1:
                missing.append("tools and pin")
        decision = self._control(method, constraints, missing_means=tuple(missing),
                                 conflicting_constraints=RESTRICTION_CONFLICTS)
        if decision.status != "continue":
            return ("This approach cannot proceed under your conditions with the available means. No attempt, cost or substitute method is applied.", decision), ar, "established"
        if method == "repair" and not s["damaged"]:
            return "The hinge is already repaired; no further repair or cost is needed.", ar, "established"
        s["attempts"][method] = getattr(self.fixture, method)
        if method == "repair":
            s["repair_constraints"] = constraints
            s["pins"] -= 1
            s["minutes"] += 10
            s["repair_stage"] = "secured"
            self._record(s, "Ten minutes of competent routine work secures the hinge and commits one spare pin. The repair is not yet finished.", ar, "resolved")
            development = self.fixture.development
            events = (() if development == "none" else
                      (ActivityDevelopment("player_choice" if development == "choice" else "ordinary"),))
            unavailable = development == "choice" and (not self.fixture.timber or s["timber_used"] or "no_timber" in constraints)
            decision = self._control(method, constraints, resolution_ref="repair", developments=events,
                                     missing_means=("timber support",) if unavailable else ())
            if decision.status == "control":
                detail = ("No timber is available under your current conditions; the repair cannot continue this way." if unavailable else
                          "Using the available timber as a brace would commit it to the repair; choose whether to use it, change approach, or stop.")
                return ("As you expose the mounting, its support shifts. Finishing now needs a timber brace. The hinge stays secured. " + detail, decision), "World Simulation / F05", "established"
            if development == "ordinary":
                self._record(s, "The guard shifts his stance as you keep working.", "Actors & Social Dynamics")
            finished = self._finish_repair(s, 20)
            return (finished, self._control(method, constraints, resolution_ref="repair", complete=True)), ar, "resolved"
        s["minutes"] += 3 if method == "lift" else 5
        cost = "three minutes" if method == "lift" else "five minutes"
        if method == "lever":
            s["timber_used"] = True
        if s["attempts"][method] == "failure":
            return (f"Your {'assisted lift' if method == 'lift' else 'timber leverage attempt'} fails after {cost}. The gate remains jammed and the cart blocked. " + ("The timber splits and is spent." if method == "lever" else "The effort does not clear the obstruction."), self._control(method, constraints, resolution_ref=method, complete=True)), ar, "resolved"
        s["cart_passed"] = True
        s["gate"] = "jammed" if method == "lift" else "held_open"
        return (f"With {'the guard assisting your lift' if method == 'lift' else 'the timber providing leverage'}, you clear the supply cart in {cost}. " + ("After you lower it, the gate jams again; the hinge remains damaged." if method == "lift" else "The timber remains committed to holding the opening; the hinge remains damaged."), self._control(method, constraints, resolution_ref=method, complete=True)), ar, "resolved"

    def _finish_repair(self, s, minutes):
        s["minutes"] += minutes
        s["repair_stage"] = "finished"
        if s["attempts"]["repair"] == "failure":
            return "You finish the remaining twenty minutes of work, but the replacement pin will not hold and is spent. The hinge remains damaged; the gate keeps its prior opening and any cart already cleared stays cleared."
        cart = "The supply cart has already passed." if s["cart_passed"] else "The supply cart passes through."
        s.update(gate="working", damaged=False, cart_passed=True)
        return "After twenty more minutes of work, the repair holds and the gate operates. " + cart + " The spare pin is spent."

    def present(self, turn, generate):
        """Expression follows publication; failures cannot undo or replay the turn."""
        return realize(deepcopy(turn["context"]), generate)
