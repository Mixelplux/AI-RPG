"""Bounded F05 control decisions over owning-system checkpoints.

This policy does not advance time, resolve attempts, persist progress or infer
character access. Callers establish the checkpoint and execute only permitted
work through the existing owning systems. Missing suppliers may be stipulated
in offline fixtures; that does not implement those systems.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ActivityAuthorization:
    purpose: str
    method: str
    intent: str = "commit"
    constraints: tuple[str, ...] = ()
    answered_choices: tuple[str, ...] = ()


@dataclass(frozen=True)
class ActivityDevelopment:
    kind: str  # ordinary, player_choice, increased_discovery_risk
    perceived: bool = True
    opportunity_to_respond: bool = True
    potentially_objectionable: bool = False
    choice_key: str | None = None


@dataclass(frozen=True)
class ActivityCheckpoint:
    purpose: str
    method: str
    blocked: bool = False
    missing_means: tuple[str, ...] = ()
    conflicting_constraints: tuple[str, ...] = ()
    complete: bool = False
    resolution_ref: str | None = None
    restart_required: bool = False
    developments: tuple[ActivityDevelopment, ...] = ()


@dataclass(frozen=True)
class ActivityControl:
    status: str  # continue, control, complete
    reason: str
    resolution: str  # unresolved, reuse, new_attempt_required
    resolution_ref: str | None


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _texts(value):
    return (isinstance(value, tuple) and all(_text(item) for item in value)
            and len(set(value)) == len(value))


def _validate(authorization, checkpoint):
    if not isinstance(authorization, ActivityAuthorization) or not isinstance(checkpoint, ActivityCheckpoint):
        raise ValueError("Expected an activity authorization and checkpoint.")
    if not all(_text(value) for value in (
            authorization.purpose, authorization.method, checkpoint.purpose, checkpoint.method)):
        raise ValueError("An immediate purpose and chosen method are required.")
    if not isinstance(authorization.intent, str) or authorization.intent not in {"inquiry", "prepare", "commit", "withdraw"}:
        raise ValueError("Unsupported activity intent.")
    if not all(_texts(value) for value in (
            authorization.constraints, authorization.answered_choices,
            checkpoint.missing_means, checkpoint.conflicting_constraints)):
        raise ValueError("Expected explicit, unique activity references.")
    if not all(type(value) is bool for value in (
            checkpoint.blocked, checkpoint.complete, checkpoint.restart_required)):
        raise ValueError("Expected checkpoint flags.")
    if checkpoint.resolution_ref is not None and not _text(checkpoint.resolution_ref):
        raise ValueError("Invalid accepted resolution reference.")
    if not isinstance(checkpoint.developments, tuple):
        raise ValueError("Expected established developments.")
    for item in checkpoint.developments:
        if not isinstance(item, ActivityDevelopment):
            raise ValueError("Invalid activity development.")
        if not isinstance(item.kind, str) or item.kind not in {"ordinary", "player_choice", "increased_discovery_risk"}:
            raise ValueError("Unsupported activity development.")
        if not all(type(value) is bool for value in (
                item.perceived, item.opportunity_to_respond, item.potentially_objectionable)):
            raise ValueError("Expected development access and response flags.")
        if item.choice_key is not None and not _text(item.choice_key):
            raise ValueError("Invalid prior-choice reference.")


def decide_activity_control(authorization, checkpoint):
    """Return permission for the next bounded continuation, never an outcome.

    Purpose/method IDs refer to one coherent undertaking, not a queue. Applicable
    authorities classify meaningful choices, available means and interruptions.
    A choice key refers to the exact previously answered development/risk; it
    cannot waive a missing prerequisite, change methods or lift a restriction.
    Hidden developments are never returned as player-facing material.
    """
    _validate(authorization, checkpoint)
    resolution = "reuse" if checkpoint.resolution_ref else "unresolved"

    def decision(status, reason, *, resolution_mode=resolution):
        return ActivityControl(status, reason, resolution_mode, checkpoint.resolution_ref)

    if authorization.intent != "commit":
        return decision("control", authorization.intent)
    if (authorization.purpose, authorization.method) != (checkpoint.purpose, checkpoint.method):
        return decision("control", "authorization_scope")
    if checkpoint.complete:
        return decision("complete", "concluded")
    if checkpoint.blocked or checkpoint.missing_means:
        return decision("control", "cannot_proceed")
    if set(authorization.constraints).intersection(checkpoint.conflicting_constraints):
        return decision("control", "authorization_constraint")
    if checkpoint.restart_required:
        return decision("control", "restart_requires_authorization",
                        resolution_mode="new_attempt_required")
    for item in checkpoint.developments:
        if not item.perceived or not item.opportunity_to_respond:
            continue
        answered = item.choice_key is not None and item.choice_key in authorization.answered_choices
        if item.kind == "player_choice" and not answered:
            return decision("control", "player_choice")
        if (item.kind == "increased_discovery_risk"
                and item.potentially_objectionable and not answered):
            return decision("control", "discovery_risk")
    return decision("continue", "within_authorization")
