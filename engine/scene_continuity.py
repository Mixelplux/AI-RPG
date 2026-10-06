"""Bounded CLI presentation memory; never world truth or save data."""

from copy import deepcopy
import re


MAX_DETAILS = 24
MAX_DETAIL_CHARS = 4000
MAX_TOTAL_CHARS = 8000
STAGES = {"orient", "expand", "follow", "narrow"}


class SceneContinuity:
    def __init__(self):
        self.clear()

    def clear(self):
        self.location_id = None
        self.details = []
        self.conditions = {}

    def enter(self, location_id):
        if location_id != self.location_id:
            self.clear()
            self.location_id = location_id

    def presentation(self, scene, player_input, stage):
        self.enter(scene["location"]["location_id"])
        return {
            "stage": stage if self.details else "orient",
            "focus": player_input,
            "established_details": list(self.details),
            "previous_conditions": deepcopy(self.conditions),
        }

    def remember(self, text, conditions):
        # Sentence excerpts retain concrete claims without another model call or
        # lossy semantic guessing. No player transcript, provider payload or ledger.
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
            if sentence and len(sentence) <= MAX_DETAIL_CHARS and sentence not in self.details:
                self.details.append(sentence)
        # Keep the initial orientation plus recent resolution within a fixed cap.
        self.details = self.details[:4] + self.details[4:][-(MAX_DETAILS - 4):]
        while sum(map(len, self.details)) > MAX_TOTAL_CHARS:
            # Prefer retaining orientation and the newest discovery. If those
            # alone fill the budget, discard the oldest description.
            self.details.pop(4 if len(self.details) > 5 else 0)
        self.conditions = deepcopy(conditions)


def validate_scene_presentation(value):
    if not isinstance(value, dict) or set(value) != {
        "stage", "focus", "established_details", "previous_conditions",
    }:
        raise ValueError("Scene presentation is malformed.")
    details = value["established_details"]
    if (value["stage"] not in STAGES or not isinstance(value["focus"], str)
            or not isinstance(details, list) or len(details) > MAX_DETAILS
            or any(not isinstance(s, str) or len(s) > MAX_DETAIL_CHARS for s in details)
            or sum(map(len, details)) > MAX_TOTAL_CHARS
            or not isinstance(value["previous_conditions"], dict)):
        raise ValueError("Scene presentation is malformed.")
