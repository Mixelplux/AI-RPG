"""Session-only agenda for one North-Gate exchange; never world or save truth."""
from copy import deepcopy

from engine import west_road_predicament as west
from engine.scene_composition import prepare_scene_revised_a, realize_scene_locally


class NorthGateDiscussion:
    """Accept player controls, resolve outside facts afresh, retire only local focus."""
    MAX_RECENT_EVENTS = 4
    CONTROLS = {"discuss patrol with Elin", "resume patrol discussion", "cancel patrol discussion"}

    def __init__(self):
        self._record = None

    def snapshot(self):
        return deepcopy(self._record)

    @staticmethod
    def _current(engine):
        world = engine.get_world_state()
        scene = engine.get_scene_snapshot()
        supported = west.enabled(engine.region)
        investigating = supported and world["west_road_predicament"]["phase"] == "investigating"
        here = world["player"]["current_location_id"] == west.GATE
        present = west.ELIN in scene["entities"]["static"]
        return world, scene, investigating and here and present

    def control(self, engine, command):
        """Only explicit bounded player commands establish or retire an agenda."""
        command = command.strip().casefold()
        if command == "cancel patrol discussion":
            if self._record is None:
                return "There is no patrol discussion to cancel."
            self._record = None
            return "You leave the patrol discussion unfinished. Reports and accepted decisions remain unchanged."
        if command not in {"discuss patrol with elin", "resume patrol discussion"}:
            raise ValueError("Unsupported discussion control.")
        _, _, available = self._current(engine)
        if not available:
            if self._record is not None:
                self._record["status"] = "suspended"
            return "The patrol discussion cannot continue now. Elin must be at the North Gate and the patrol response must still be undecided."
        if command == "resume patrol discussion":
            if self._record is None:
                return "No session discussion is pending. Use 'discuss patrol with Elin' to begin a new exchange."
            self._record["status"] = "pending"
            return "You resume the patrol discussion with Elin, using the reports and circumstances as they stand now."
        if self._record is not None:
            return ("The discussion is suspended. Talk to Elin or use 'resume patrol discussion' to continue it."
                    if self._record["status"] == "suspended" else "Your patrol discussion with Elin is already open.")
        self._record = {"participant_id": west.ELIN, "focus": "patrol_response",
                        "status": "pending", "recent_event_refs": []}
        return "You open a patrol discussion with Elin. Your focus is reviewing the road reports before choosing a response."

    def refresh(self, engine):
        if self._record is None:
            return None
        _, _, available = self._current(engine)
        if not available and self._record["status"] != "suspended":
            self._record["status"] = "suspended"
            return "Your patrol discussion is suspended. Its question remains open; return to Elin and talk to her when circumstances permit."
        return None

    def observe(self, engine, result, previous_history_count):
        """Follow successful engine events, never generated prose or adapter output."""
        if self._record is None:
            return None
        if result.get("success"):
            new_events = engine.get_history()[previous_history_count:]
            refs = self._record["recent_event_refs"]
            self._record["recent_event_refs"] = list(dict.fromkeys(
                refs + [event["history_id"] for event in new_events]))[-self.MAX_RECENT_EVENTS:]
            outcome_id = result.get("narrative_action_id")
            if result.get("intent") == "west_road_decision" and outcome_id:
                event = engine.get_history_entry_by_id(outcome_id)
                world = engine.get_world_state()
                if (event and event["event_type"] == "west_road_outcome"
                        and world["west_road_predicament"]["last_outcome_history_id"] == outcome_id):
                    self._record = None
                    return "The accepted response concludes this patrol discussion. The wider West-Road threat remains unresolved."
        if (result.get("success") and result.get("intent") == "conversation"
                and result.get("target_resolution", {}).get("identifier") == west.ELIN
                and self._record["status"] == "suspended" and self._current(engine)[2]):
            self._record["status"] = "pending"
            return "You pick up the unfinished patrol discussion with Elin."
        return self.refresh(engine)

    def relevant_progress(self, engine, result):
        """Only a report exchange with Elin merits extra focused follow-through.

        Ordinary talk already receives the same authoritative contextual reply.
        Unrelated actions and a suspended topic need no repeated status.
        """
        if (self._record is None or self._record["status"] != "pending"
                or not self._current(engine)[2] or not result.get("success")
                or result.get("intent") != "clue_presentation"):
            return False
        target = engine.resolve_target(result["action"].get("target") or "")
        return target.get("identifier") == west.ELIN and bool(result.get("presentation", {}).get("changed"))

    def interrupt(self, reason):
        if self._record is None:
            return None
        self._record = None
        return (f"The session-only patrol discussion is interrupted by {reason}; its focus is not saved. "
                "No discussion is marked resolved. World facts follow the session you next play.")

    def focus_text(self, engine):
        """A fresh relevance projection; receipts and eligibility remain engine-owned."""
        if self._record is None:
            return None
        world, scene, available = self._current(engine)
        if self._record["status"] == "suspended" or not available:
            return ("The unfinished exchange can resume when you talk to Elin; "
                    "'resume patrol discussion' is also available." if available else
                    "That exchange cannot continue here under the current circumstances. You can cancel it without changing the world.")
        response = west.actor_response(engine.region, world, west.ELIN, scene)
        return "Elin: " + response["text"] if response else None

    def present(self, engine, *, preparer=None, realizer=None):
        """Use copied scene source and existing realization; deterministic fallback."""
        text = self.focus_text(engine)
        if text is None:
            return None
        # A suspended exchange has no remote speech or narration adapter invocation.
        if self._record["status"] == "suspended" or not self._current(engine)[2]:
            return text
        chosen = preparer or prepare_scene_revised_a
        def focused(source):
            source["selected_facts"] = [{"text": text, "status": "accepted session dialogue focus with current engine prerequisites"}]
            return chosen(source)
        packet = engine.get_scene_narration(preparer=focused, realizer=realizer or realize_scene_locally)
        return packet["display_text"] if packet["accepted"] else text
