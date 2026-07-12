"""Validation and defensive read helpers for persisted evidence traces."""

from copy import deepcopy
from typing import Any


TRACE_FIELDS = {"trace_id", "evidence_id", "location_id"}


def validate_evidence_traces(
    evidence_traces: Any,
    region: dict[str, Any] | None = None,
) -> None:
    """Validate ordered, opaque, location-bound trace records."""

    if not isinstance(evidence_traces, list):
        raise ValueError("World State evidence_traces must be a list.")

    locations = None
    if region is not None:
        locations = {
            location.get("location_id")
            for location in region.get("locations", [])
            if isinstance(location, dict)
        }

    seen_ids: set[str] = set()
    for trace in evidence_traces:
        if not isinstance(trace, dict) or set(trace) != TRACE_FIELDS:
            raise ValueError("Evidence trace fields are invalid.")
        for field in sorted(TRACE_FIELDS):
            if not isinstance(trace[field], str) or not trace[field]:
                raise ValueError(f"Evidence trace {field} must be a non-empty string.")
        if trace["trace_id"] in seen_ids:
            raise ValueError("Evidence trace identities must be unique.")
        if locations is not None and trace["location_id"] not in locations:
            raise ValueError("Evidence trace location_id is unknown.")
        seen_ids.add(trace["trace_id"])


def get_evidence_traces(world_state: dict[str, Any]) -> list[dict[str, str]]:
    """Return a defensive copy in persisted deterministic order."""

    validate_evidence_traces(world_state["evidence_traces"])
    return deepcopy(world_state["evidence_traces"])


def get_evidence_trace(
    world_state: dict[str, Any], trace_id: str
) -> dict[str, str] | None:
    """Return one defensive trace record by its stable identity."""

    if not isinstance(trace_id, str) or not trace_id:
        raise ValueError("trace_id must be a non-empty string.")
    for trace in get_evidence_traces(world_state):
        if trace["trace_id"] == trace_id:
            return trace
    return None


def get_evidence_traces_at_location(
    world_state: dict[str, Any], location_id: str
) -> list[dict[str, str]]:
    """Return defensively copied traces at one exact location."""

    if not isinstance(location_id, str) or not location_id:
        raise ValueError("location_id must be a non-empty string.")
    return [
        trace for trace in get_evidence_traces(world_state)
        if trace["location_id"] == location_id
    ]
