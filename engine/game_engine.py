from copy import deepcopy
from typing import Any, Dict

from engine.scene_loader import load_region, build_scene
from engine.perception_builder import build_perception
from engine.pressure_observation import derive_pressure_observation
from engine.unresolved_threads import (
    derive_resolved_thread_observation,
    derive_unresolved_thread_evidence,
    get_open_threads as get_world_open_threads,
    prepare_open_thread_candidate,
)
from engine.scene_narrator import narrate_scene
from engine.interaction_kernel import process_player_input
from engine.world_update import apply_interaction
from engine.region_validator import validate_region
from engine.destination_resolver import (
    DestinationResolution,
    resolve_destination,
)
from engine.skill_check import SkillCheckResult, resolve_skill_check
from engine.target_resolver import TargetResolution, resolve_scene_target
from engine.timekeeper import advance_time_by_hours
from engine.history_context import build_history_context_packet
from engine.narration_context import build_narration_context_packet
from engine.narration_output import (
    build_narration_output_contract,
    validate_narration_output_packet,
)
from engine.narration_pipeline import build_narration_preview_packet
from engine.pressure_state import (
    get_applicable_pressures as get_applicable_world_pressures,
    get_pressure as get_world_pressure,
    get_pressures as get_world_pressures,
    prepare_pressure_level_change,
    validate_pressure_state,
)
from engine.world_state import (
    DEFAULT_HISTORY_QUERY_COUNT,
    add_history_entry,
    create_initial_world_state,
    get_history,
    get_history_entry_by_id,
    get_effective_actor_location,
    get_static_actor,
    get_player_location_id,
    get_time,
    query_history,
    set_player_location_id,
    set_time,
    copy_world_state,
    validate_world_state
)
from engine.actor_knowledge import get_actor_knowledge as get_world_actor_knowledge
from engine.actor_knowledge_response import derive_conversation_actor_knowledge_response
from engine.evidence_traces import (
    get_evidence_trace as get_world_evidence_trace,
    get_evidence_traces as get_world_evidence_traces,
    get_evidence_traces_at_location as get_world_evidence_traces_at_location,
)


class GameEngine:
    """
    Orchestrates the core AI Narrative RPG Engine pipeline.
    """

    def __init__(
        self,
        region_path: str,
        entry_location_id: str | None = None,
        initial_world_state: Dict[str, Any] | None = None
    ):
        self.region_path = region_path
        self.region = load_region(region_path)

        validate_region(self.region)

        if initial_world_state is None:
            self.world_state = create_initial_world_state(self.region)
        else:
            validate_world_state(initial_world_state, self.region)
            validate_pressure_state(initial_world_state["pressures"], self.region)
            self.world_state = copy_world_state(initial_world_state)

        if entry_location_id is not None:
            self.world_state = set_player_location_id(
                self.world_state,
                entry_location_id
            )

        self.scene_snapshot = build_scene(
            self.region,
            self.world_state
        )

    @classmethod
    def start_new(
        cls,
        region_path: str,
        entry_location_id: str | None = None
    ) -> "GameEngine":
        from engine.game_session import GameSession

        return GameSession.start_new(region_path, entry_location_id)

    def get_region_path(self) -> str:
        return self.region_path

    def get_world_state(self) -> Dict[str, Any]:
        return copy_world_state(self.world_state)

    def get_pressures(self) -> dict[str, dict]:
        return get_world_pressures(self.world_state)

    def get_pressure(self, pressure_id: str) -> dict | None:
        return get_world_pressure(self.world_state, pressure_id)

    def get_open_threads(self) -> dict[str, dict[str, str]]:
        return get_world_open_threads(self.world_state)

    def get_actor_knowledge(self, actor_id: str) -> tuple[str, ...]:
        get_static_actor(self.region, actor_id)
        return get_world_actor_knowledge(self.world_state["actor_knowledge"], actor_id)

    def get_evidence_trace(self, trace_id: str) -> Dict[str, str] | None:
        return get_world_evidence_trace(self.world_state, trace_id)

    def get_evidence_traces_at_location(self, location_id: str) -> list[Dict[str, str]]:
        return get_world_evidence_traces_at_location(self.world_state, location_id)

    def get_evidence_traces(self) -> list[Dict[str, str]]:
        return get_world_evidence_traces(self.world_state)

    def get_player_discoveries(self) -> tuple[str, ...]:
        return tuple(self.world_state["player_discoveries"])

    def get_known_clues(self) -> tuple[Dict[str, str], ...]:
        """Return authored, player-safe clues in declaration order."""
        known_ids = set(self.world_state["player_discoveries"])
        return tuple(
            {"title": declaration["title"], "text": declaration["text"]}
            for declaration in self.region.get("discovery_declarations", [])
            if declaration["discovery_id"] in known_ids
        )

    def investigate(self) -> Dict[str, Any]:
        candidate = copy_world_state(self.world_state)
        location_id = get_player_location_id(candidate)
        trace_ids = {
            trace["trace_id"]
            for trace in candidate["evidence_traces"]
            if trace["location_id"] == location_id
        }
        declaration = next((item for item in self.region.get("discovery_declarations", [])
                            if item["location_id"] == location_id and item["trace_id"] in trace_ids
                            and item["discovery_id"] not in candidate["player_discoveries"]), None)
        result = {"changed": False, "discovery_id": None, "text": None, "history_id": None}
        if declaration is None:
            return result
        candidate["player_discoveries"].append(declaration["discovery_id"])
        candidate = add_history_entry(candidate, "player_discovery_added",
            "Player discovered an authored clue.", location_id, deepcopy(candidate["time"]),
            {"discovery_id": declaration["discovery_id"]})
        validate_world_state(candidate, self.region)
        scene = build_scene(self.region, candidate)
        self.world_state = candidate
        self.scene_snapshot = scene
        return {"changed": True, "discovery_id": declaration["discovery_id"],
                "text": declaration["text"], "history_id": candidate["history"][-1]["history_id"]}

    def present_clue(self, clue_title: str, actor_text: str) -> Dict[str, Any]:
        declaration = self.region.get("conversation_discovery_resolution")
        result = {"changed": False, "response_text": None, "resolved_observation": None,
                  "actor_location_consequence": None}
        if declaration is None or not isinstance(clue_title, str) or not isinstance(actor_text, str):
            return result
        clue = next((item for item in self.region.get("discovery_declarations", []) if item["title"].casefold() == clue_title.casefold()), None)
        target = self.resolve_target(actor_text)
        if (clue is None or clue["discovery_id"] != declaration["required_discovery_id"]
                or clue["discovery_id"] not in self.world_state["player_discoveries"]
                or target["status"] != "resolved" or target["target_type"] != "entity"
                or target["identifier"] != declaration["target_entity_id"]):
            return result
        thread_id = declaration["required_thread_id"]
        if thread_id in self.world_state["resolved_threads"]:
            return result
        if thread_id not in self.world_state["open_threads"]:
            return result
        candidate = copy_world_state(self.world_state)
        candidate = add_history_entry(candidate, "clue_presented", "Player presented an authored clue.", extra={"target_entity_id": target["identifier"]})
        source_id = candidate["history"][-1]["history_id"]
        candidate["open_threads"].pop(thread_id)
        candidate["resolved_threads"][thread_id] = {"thread_id": thread_id, "status": "resolved", "resolved_by_history_id": source_id}
        candidate = add_history_entry(candidate, "unresolved_thread_resolved", "Unresolved thread resolved.", extra={"thread_id": thread_id, "status": "resolved", "source_history_id": source_id})
        relocation = self.region.get("resolved_thread_actor_relocation_effect")
        if relocation is not None and relocation["resolved_thread_id"] == thread_id:
            candidate, relocation_result = self._prepare_actor_location_candidate(
                candidate, relocation["actor_entity_id"],
                relocation["destination_location_id"], source_id,
            )
            result["actor_location_consequence"] = {
                "status": "applied" if relocation_result["changed"] else "no_op"
            }
        validate_world_state(candidate, self.region)
        scene = build_scene(self.region, candidate)
        self.world_state, self.scene_snapshot = candidate, scene
        result.update({"changed": True, "response_text": declaration["response_text"], "resolved_observation": declaration["resolved_observation"]})
        return deepcopy(result)

    def create_evidence_trace(self, trace_id: str, evidence_id: str, location_id: str) -> Dict[str, Any]:
        candidate, result = self._prepare_evidence_trace_candidate(
            copy_world_state(self.world_state), trace_id, evidence_id, location_id
        )
        if not result["changed"]:
            return deepcopy(result)
        validate_world_state(candidate, self.region)
        self.world_state = candidate
        return deepcopy(result)

    def create_evidence_trace_from_event(
        self, trace_id: str, evidence_id: str, location_id: str, source_history_id: str
    ) -> Dict[str, Any]:
        candidate, result = self._prepare_evidence_trace_candidate(
            copy_world_state(self.world_state), trace_id, evidence_id, location_id, source_history_id
        )
        if not result["changed"]:
            return deepcopy(result)
        validate_world_state(candidate, self.region)
        self.world_state = candidate
        return deepcopy(result)

    def _prepare_evidence_trace_candidate(
        self, candidate: Dict[str, Any], trace_id: str, evidence_id: str,
        location_id: str, source_history_id: str | None = None,
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        for name, value in (("trace_id", trace_id), ("evidence_id", evidence_id), ("location_id", location_id)):
            if not isinstance(value, str) or not value:
                raise ValueError(f"{name} must be a non-empty string.")
        location_ids = {item.get("location_id") for item in self.region.get("locations", []) if isinstance(item, dict)}
        if location_id not in location_ids:
            raise ValueError("location_id is unknown.")
        if source_history_id is not None:
            if not isinstance(source_history_id, str) or not source_history_id:
                raise ValueError("source_history_id must be a non-empty string.")
            if get_history_entry_by_id(candidate, source_history_id) is None:
                raise ValueError("Unknown source_history_id.")
        existing = next((trace for trace in candidate["evidence_traces"] if trace["trace_id"] == trace_id), None)
        result = {"changed": False, "trace_id": trace_id, "evidence_id": evidence_id,
                  "location_id": location_id, "source_history_id": source_history_id, "history_id": None}
        if existing is not None:
            if existing != {"trace_id": trace_id, "evidence_id": evidence_id, "location_id": location_id}:
                raise ValueError("Conflicting evidence trace identity.")
            return candidate, deepcopy(result)
        candidate["evidence_traces"].append({"trace_id": trace_id, "evidence_id": evidence_id, "location_id": location_id})
        extra = {"trace_id": trace_id, "evidence_id": evidence_id, "location_id": location_id}
        if source_history_id is not None:
            extra["source_history_id"] = source_history_id
        candidate = add_history_entry(candidate, "evidence_trace_added", f"Evidence trace added: {trace_id}.", location_id, deepcopy(candidate["time"]), extra)
        result["changed"] = True
        result["history_id"] = candidate["history"][-1]["history_id"]
        return candidate, deepcopy(result)

    def add_actor_knowledge(
        self,
        actor_id: str,
        knowledge_id: str,
    ) -> Dict[str, Any]:
        candidate_world_state = copy_world_state(self.world_state)
        get_static_actor(self.region, actor_id)
        if not isinstance(knowledge_id, str) or not knowledge_id:
            raise ValueError("knowledge_id must be a non-empty string.")

        actor_knowledge = candidate_world_state["actor_knowledge"]
        membership = actor_knowledge.setdefault(actor_id, [])
        result = {
            "changed": False,
            "actor_id": actor_id,
            "knowledge_id": knowledge_id,
            "history_id": None,
        }
        if knowledge_id in membership:
            return deepcopy(result)

        membership.append(knowledge_id)
        candidate_world_state = add_history_entry(
            candidate_world_state,
            event_type="actor_knowledge_added",
            summary=f"Actor {actor_id} gained knowledge {knowledge_id}.",
            time=deepcopy(candidate_world_state["time"]),
            extra={
                "actor_id": actor_id,
                "knowledge_id": knowledge_id,
            },
        )
        validate_world_state(candidate_world_state, self.region)
        result["changed"] = True
        result["history_id"] = candidate_world_state["history"][-1]["history_id"]
        self.world_state = candidate_world_state
        return deepcopy(result)

    def add_actor_knowledge_from_event(
        self,
        actor_id: str,
        knowledge_id: str,
        source_history_id: str,
    ) -> Dict[str, Any]:
        """Atomically add actor knowledge with one prior durable source event."""

        candidate_world_state = copy_world_state(self.world_state)
        candidate_world_state, result = (
            self._prepare_actor_knowledge_from_event_candidate(
                candidate_world_state, actor_id, knowledge_id, source_history_id
            )
        )
        if not result["changed"]:
            return deepcopy(result)
        validate_world_state(candidate_world_state, self.region)
        self.world_state = candidate_world_state
        return deepcopy(result)

    def _prepare_actor_knowledge_from_event_candidate(
        self,
        candidate_world_state: Dict[str, Any],
        actor_id: str,
        knowledge_id: str,
        source_history_id: str,
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """Prepare one causally linked actor-knowledge addition without commit."""

        get_static_actor(self.region, actor_id)
        if not isinstance(knowledge_id, str) or not knowledge_id:
            raise ValueError("knowledge_id must be a non-empty string.")
        if not isinstance(source_history_id, str) or not source_history_id:
            raise ValueError("source_history_id must be a non-empty string.")
        if get_history_entry_by_id(candidate_world_state, source_history_id) is None:
            raise ValueError("Unknown source_history_id.")

        actor_knowledge = candidate_world_state["actor_knowledge"]
        membership = actor_knowledge.setdefault(actor_id, [])
        result = {
            "changed": False,
            "actor_id": actor_id,
            "knowledge_id": knowledge_id,
            "source_history_id": source_history_id,
            "history_id": None,
        }
        if knowledge_id in membership:
            return candidate_world_state, deepcopy(result)

        membership.append(knowledge_id)
        candidate_world_state = add_history_entry(
            candidate_world_state,
            event_type="actor_knowledge_added",
            summary=f"Actor {actor_id} gained knowledge {knowledge_id}.",
            time=deepcopy(candidate_world_state["time"]),
            extra={
                "actor_id": actor_id,
                "knowledge_id": knowledge_id,
                "source_history_id": source_history_id,
            },
        )
        result["changed"] = True
        result["history_id"] = candidate_world_state["history"][-1]["history_id"]
        return candidate_world_state, deepcopy(result)

    def set_actor_location(
        self, entity_id: str, destination_location_id: str
    ) -> Dict[str, Any]:
        candidate_world_state = copy_world_state(self.world_state)
        candidate_world_state, result = self._prepare_actor_location_candidate(
            candidate_world_state, entity_id, destination_location_id
        )
        if not result["changed"]:
            return deepcopy(result)
        validate_world_state(candidate_world_state, self.region)
        candidate_scene_snapshot = build_scene(self.region, candidate_world_state)
        self.world_state = candidate_world_state
        self.scene_snapshot = candidate_scene_snapshot
        return deepcopy(result)

    def _prepare_actor_location_candidate(
        self,
        candidate_world_state: Dict[str, Any],
        entity_id: str,
        destination_location_id: str,
        source_history_id: str | None = None,
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        actor = get_static_actor(self.region, entity_id)
        if not isinstance(destination_location_id, str) or not destination_location_id:
            raise ValueError("destination_location_id must be a non-empty string.")
        location_ids = {
            location.get("location_id") for location in self.region.get("locations", [])
            if isinstance(location, dict)
        }
        if destination_location_id not in location_ids:
            raise ValueError("Unknown destination_location_id.")

        previous_location_id = get_effective_actor_location(
            self.region, candidate_world_state, entity_id
        )
        result = {
            "changed": False,
            "entity_id": entity_id,
            "previous_location_id": previous_location_id,
            "new_location_id": destination_location_id,
            "history_id": None,
        }
        if destination_location_id == previous_location_id:
            return candidate_world_state, deepcopy(result)

        overrides = candidate_world_state.setdefault("actor_location_overrides", {})
        if destination_location_id == actor["location"]:
            overrides.pop(entity_id, None)
        else:
            overrides[entity_id] = destination_location_id
        extra = {
            "entity_id": entity_id,
            "previous_location_id": previous_location_id,
            "new_location_id": destination_location_id,
        }
        if source_history_id is not None:
            extra["source_history_id"] = source_history_id
        candidate_world_state = add_history_entry(
            candidate_world_state,
            event_type="actor_moved",
            summary=(f"Actor {entity_id} moved from {previous_location_id} "
                     f"to {destination_location_id}."),
            location=destination_location_id,
            time=deepcopy(candidate_world_state["time"]),
            extra=extra,
        )
        result["changed"] = True
        result["history_id"] = candidate_world_state["history"][-1]["history_id"]
        return candidate_world_state, deepcopy(result)

    def get_applicable_pressures(
        self,
        location_id: str | None = None,
    ) -> dict[str, dict]:
        if location_id is None:
            location_id = get_player_location_id(self.world_state)
        elif not isinstance(location_id, str) or not location_id:
            raise ValueError("location_id must be a non-empty string.")

        location_ids = {
            location.get("location_id")
            for location in self.region.get("locations", [])
            if isinstance(location, dict)
        }
        if location_id not in location_ids:
            raise ValueError("Unknown location_id.")

        return get_applicable_world_pressures(
            self.world_state["pressures"],
            self.region,
            location_id,
        )

    def set_pressure_level(
        self,
        pressure_id: str,
        new_level: int,
    ) -> Dict[str, Any]:
        candidate_world_state = copy_world_state(self.world_state)
        updated_pressures, result = prepare_pressure_level_change(
            candidate_world_state["pressures"],
            pressure_id,
            new_level,
        )

        if not result["changed"]:
            return deepcopy(result)

        candidate_world_state["pressures"] = updated_pressures
        current_time = deepcopy(candidate_world_state["time"])
        target_pressure = updated_pressures[pressure_id]
        candidate_world_state = add_history_entry(
            candidate_world_state,
            event_type="pressure_changed",
            summary=(
                f"Pressure {pressure_id} changed from "
                f"{result['previous_level']} to {result['new_level']}."
            ),
            time=current_time,
            extra={
                "pressure_id": pressure_id,
                "pressure_type": target_pressure["pressure_type"],
                "scope_type": target_pressure["scope_type"],
                "scope_id": target_pressure["scope_id"],
                "previous_level": result["previous_level"],
                "new_level": result["new_level"],
            },
        )

        validate_world_state(candidate_world_state)

        history_entry = candidate_world_state["history"][-1]
        result["history_id"] = history_entry["history_id"]

        self.world_state = candidate_world_state

        return deepcopy(result)

    def set_pressure_level_from_event(
        self,
        pressure_id: str,
        new_level: int,
        source_history_id: str,
    ) -> Dict[str, Any]:
        candidate_world_state = copy_world_state(self.world_state)
        candidate_world_state, result = (
            self._prepare_pressure_level_from_event_candidate(
                candidate_world_state,
                pressure_id,
                new_level,
                source_history_id,
            )
        )

        if not result["changed"]:
            return deepcopy(result)

        validate_world_state(candidate_world_state)
        self.world_state = candidate_world_state

        return deepcopy(result)

    def _prepare_pressure_level_from_event_candidate(
        self,
        candidate_world_state: Dict[str, Any],
        pressure_id: str,
        new_level: int,
        source_history_id: str,
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:

        if not isinstance(source_history_id, str) or not source_history_id:
            raise ValueError("source_history_id must be a non-empty string.")

        source_entry = get_history_entry_by_id(
            candidate_world_state,
            source_history_id,
        )
        if source_entry is None:
            raise ValueError("Unknown source_history_id.")

        updated_pressures, result = prepare_pressure_level_change(
            candidate_world_state["pressures"],
            pressure_id,
            new_level,
        )
        result["source_history_id"] = source_history_id

        if not result["changed"]:
            return candidate_world_state, deepcopy(result)

        candidate_world_state["pressures"] = updated_pressures
        target_pressure = updated_pressures[pressure_id]
        candidate_world_state = add_history_entry(
            candidate_world_state,
            event_type="pressure_changed",
            summary=(
                f"Pressure {pressure_id} changed from "
                f"{result['previous_level']} to {result['new_level']}."
            ),
            time=deepcopy(candidate_world_state["time"]),
            extra={
                "pressure_id": pressure_id,
                "pressure_type": target_pressure["pressure_type"],
                "scope_type": target_pressure["scope_type"],
                "scope_id": target_pressure["scope_id"],
                "previous_level": result["previous_level"],
                "new_level": result["new_level"],
                "source_history_id": source_history_id,
            },
        )

        result["history_id"] = candidate_world_state["history"][-1][
            "history_id"
        ]
        return candidate_world_state, deepcopy(result)

    def get_history(self) -> list[Dict[str, Any]]:
        return get_history(self.world_state)

    def query_history(
        self,
        count: int | None = None,
        event_type: str | None = None,
        location: str | None = None
    ) -> list[Dict[str, Any]]:
        return query_history(
            self.world_state,
            count=count,
            event_type=event_type,
            location=location
        )

    def get_default_history_query_count(self) -> int:
        return DEFAULT_HISTORY_QUERY_COUNT

    def get_history_entry_by_id(
        self,
        history_id: str
    ) -> Dict[str, Any] | None:
        return get_history_entry_by_id(self.world_state, history_id)

    def get_history_context(
        self,
        count: int | None = None
    ) -> Dict[str, Any]:
        return build_history_context_packet(self.world_state, count=count)

    def get_narration_context(
        self,
        player_input: str,
        history_count: int | None = None
    ) -> Dict[str, Any]:
        perception = self.get_player_perception()
        pressure_cues = perception["pressure_cues"]
        return build_narration_context_packet(
            self.world_state,
            self.scene_snapshot,
            player_input,
            history_count=history_count,
            pressure_cue=pressure_cues[0] if pressure_cues else None,
        )

    def get_narration_output_contract(self) -> Dict[str, Any]:
        return build_narration_output_contract()

    def validate_narration_output(
        self,
        narration_output: Dict[str, Any]
    ) -> Dict[str, Any]:
        return validate_narration_output_packet(narration_output)

    def get_narration_preview(
        self,
        player_input: str
    ) -> Dict[str, Any]:
        narration_context = self.get_narration_context(player_input)
        return build_narration_preview_packet(narration_context)

    def advance_time(self, duration_hours: int = 1) -> Dict[str, Any]:
        previous_time = get_time(self.world_state)
        new_time = advance_time_by_hours(previous_time, duration_hours)
        location_id = get_player_location_id(self.world_state)

        candidate_world_state = copy_world_state(self.world_state)
        candidate_world_state = set_time(candidate_world_state, new_time)
        candidate_world_state = add_history_entry(
            candidate_world_state,
            event_type="time_advanced",
            summary=f"Player waited for {duration_hours} hour.",
            location=location_id,
            time=new_time,
            extra={
                "previous_time": previous_time,
                "new_time": new_time
            }
        )
        source_history_id = candidate_world_state["history"][-1]["history_id"]
        pressure_consequence = None
        effect = self.region.get("elapsed_time_pressure_effect")
        if effect is not None and (
            previous_time.get("elapsed_hours", 0)
            < effect["trigger_elapsed_hours"]
            <= new_time["elapsed_hours"]
        ):
            candidate_world_state, pressure_consequence = (
                self._prepare_pressure_level_from_event_candidate(
                    candidate_world_state,
                    effect["pressure_id"],
                    effect["new_level"],
                    source_history_id,
                )
            )
            pressure_consequence["effect_id"] = effect["effect_id"]

        actor_location_consequence = None
        actor_effect = self.region.get("elapsed_time_actor_relocation_effect")
        if actor_effect is not None and (
            previous_time.get("elapsed_hours", 0)
            < actor_effect["trigger_elapsed_hours"]
            <= new_time["elapsed_hours"]
        ):
            candidate_world_state, actor_result = (
                self._prepare_actor_location_candidate(
                    candidate_world_state,
                    actor_effect["actor_entity_id"],
                    actor_effect["destination_location_id"],
                    source_history_id,
                )
            )
            actor_location_consequence = {
                "effect_id": actor_effect["effect_id"],
                "trigger_elapsed_hours": actor_effect["trigger_elapsed_hours"],
                "actor_entity_id": actor_effect["actor_entity_id"],
                "previous_location_id": actor_result["previous_location_id"],
                "new_location_id": actor_result["new_location_id"],
                "changed": actor_result["changed"],
                "history_id": actor_result["history_id"],
            }

        evidence_trace_consequence = None
        trace_effect = self.region.get("elapsed_time_evidence_trace_effect")
        if trace_effect is not None and (
            previous_time.get("elapsed_hours", 0)
            < trace_effect["trigger_elapsed_hours"]
            <= new_time["elapsed_hours"]
        ):
            candidate_world_state, evidence_trace_consequence = (
                self._prepare_evidence_trace_candidate(
                    candidate_world_state,
                    trace_effect["trace_id"],
                    trace_effect["evidence_id"],
                    trace_effect["location_id"],
                    source_history_id,
                )
            )
            evidence_trace_consequence["effect_id"] = trace_effect["effect_id"]
            evidence_trace_consequence["trigger_elapsed_hours"] = trace_effect["trigger_elapsed_hours"]

        validate_world_state(candidate_world_state, self.region)
        candidate_scene_snapshot = build_scene(
            self.region,
            candidate_world_state
        )
        self.world_state = candidate_world_state
        self.scene_snapshot = candidate_scene_snapshot

        return {
            "duration_hours": duration_hours,
            "previous_time": previous_time,
            "new_time": new_time,
            "pressure_consequence": deepcopy(pressure_consequence),
            "actor_location_consequence": deepcopy(actor_location_consequence),
            "evidence_trace_consequence": deepcopy(evidence_trace_consequence),
        }

    def get_scene_snapshot(self) -> Dict[str, Any]:
        return deepcopy(self.scene_snapshot)

    def get_player_perception(self) -> Dict[str, Any]:
        applicable = self.get_applicable_pressures()
        cue = derive_pressure_observation(
            applicable,
            self.region.get("pressure_observation_cue"),
        )
        return build_perception(
            self.scene_snapshot,
            [] if cue is None else [cue],
            derive_unresolved_thread_evidence(
                self.world_state["open_threads"],
                self.region.get("conversation_unresolved_thread"),
                get_player_location_id(self.world_state),
            ),
            derive_resolved_thread_observation(
                self.world_state["resolved_threads"],
                self.region.get("conversation_unresolved_thread"),
                self.region.get("conversation_discovery_resolution"),
                get_player_location_id(self.world_state),
            ),
        )

    def get_narration(self) -> Dict[str, Any]:
        perception = self.get_player_perception()
        return narrate_scene(perception)

    def perform_skill_check(self, check_name: str) -> SkillCheckResult:
        """Resolve a gameplay-facing check using deterministic placeholders."""

        return resolve_skill_check(
            check_name=check_name,
            target_difficulty=10,
            result_value=12,
        )

    def resolve_target(self, target_text: str) -> TargetResolution:
        """Resolve text against entities and exits in the current scene."""

        return resolve_scene_target(
            target_text,
            self.scene_snapshot,
            self.region.get("entities", []),
        )

    def resolve_destination(
        self,
        destination_text: str,
    ) -> DestinationResolution:
        """Identify a known region location without moving the player."""

        return resolve_destination(
            destination_text,
            self.region.get("locations", []),
        )

    def save(self, save_path: str) -> None:
        """
        Persist the current engine state using the save system.

        Import is local to avoid a circular import:
        save_system depends on GameEngine for load reconstruction.
        """

        from engine.save_system import save_game

        save_game(self, save_path)

    def load(self, save_path: str) -> None:
        """
        Load saved engine state into this GameEngine instance.
        """

        from engine.game_session import GameSession

        loaded_engine = GameSession.load(save_path)

        self._replace_runtime_state(loaded_engine)

    def reset(self) -> None:
        """Replace the current runtime state with a fresh session."""

        from engine.game_session import GameSession

        fresh_engine = GameSession.reset(self.region_path)

        self._replace_runtime_state(fresh_engine)

    def _replace_runtime_state(self, other: "GameEngine") -> None:
        """Adopt canonical and derived runtime state from another engine."""

        self.region_path = other.region_path
        self.region = other.region
        self.world_state = other.get_world_state()
        self.scene_snapshot = other.get_scene_snapshot()

    def _compose_resolved_conversation_consequences(
        self,
        candidate_world_state: Dict[str, Any],
        interaction_result: Dict[str, Any],
        target_entity_id: str,
    ) -> Dict[str, Any]:
        """Prepare declared conversation consequences in their established order."""

        conversation_source_history_id = candidate_world_state["history"][-1][
            "history_id"
        ]
        effect = next(
            (
                item
                for item in self.region.get("conversation_pressure_effects", [])
                if item["target_entity_id"] == target_entity_id
            ),
            None,
        )
        if effect is not None:
            candidate_world_state, consequence = (
                self._prepare_pressure_level_from_event_candidate(
                    candidate_world_state,
                    effect["pressure_id"],
                    effect["new_level"],
                    conversation_source_history_id,
                )
            )
            consequence["effect_id"] = effect["effect_id"]
            interaction_result["pressure_consequence"] = {
                "effect_id": consequence["effect_id"],
                "changed": consequence["changed"],
                "pressure_id": consequence["pressure_id"],
                "previous_level": consequence["previous_level"],
                "new_level": consequence["new_level"],
                "history_id": consequence["history_id"],
                "source_history_id": consequence["source_history_id"],
            }

        relocation = self.region.get("conversation_actor_relocation_effect")
        interaction_result["actor_location_consequence"] = None
        if relocation is not None and relocation["trigger_entity_id"] == target_entity_id:
            candidate_world_state, actor_result = (
                self._prepare_actor_location_candidate(
                    candidate_world_state,
                    relocation["actor_entity_id"],
                    relocation["destination_location_id"],
                    conversation_source_history_id,
                )
            )
            interaction_result["actor_location_consequence"] = {
                "effect_id": relocation["effect_id"],
                "trigger_entity_id": relocation["trigger_entity_id"],
                "actor_entity_id": relocation["actor_entity_id"],
                "previous_location_id": actor_result["previous_location_id"],
                "new_location_id": actor_result["new_location_id"],
                "changed": actor_result["changed"],
                "history_id": actor_result["history_id"],
            }

        thread = self.region.get("conversation_unresolved_thread")
        interaction_result["unresolved_thread_consequence"] = None
        if thread is not None and thread["trigger_entity_id"] == target_entity_id:
            candidate_world_state, thread_result = prepare_open_thread_candidate(
                candidate_world_state, thread, conversation_source_history_id
            )
            interaction_result["unresolved_thread_consequence"] = thread_result

        knowledge_effect = self.region.get("conversation_actor_knowledge_effect")
        interaction_result["actor_knowledge_consequence"] = None
        if (
            knowledge_effect is not None
            and knowledge_effect["trigger_entity_id"] == target_entity_id
        ):
            candidate_world_state, knowledge_result = (
                self._prepare_actor_knowledge_from_event_candidate(
                    candidate_world_state,
                    knowledge_effect["actor_entity_id"],
                    knowledge_effect["knowledge_id"],
                    conversation_source_history_id,
                )
            )
            interaction_result["actor_knowledge_consequence"] = {
                "effect_id": knowledge_effect["effect_id"],
                "changed": knowledge_result["changed"],
                "actor_id": knowledge_result["actor_id"],
                "knowledge_id": knowledge_result["knowledge_id"],
                "source_history_id": knowledge_result["source_history_id"],
                "history_id": knowledge_result["history_id"],
            }

        trace_effect = self.region.get("conversation_evidence_trace_effect")
        interaction_result["evidence_trace_consequence"] = None
        if (
            trace_effect is not None
            and trace_effect["trigger_entity_id"] == target_entity_id
        ):
            candidate_world_state, trace_result = self._prepare_evidence_trace_candidate(
                candidate_world_state,
                trace_effect["trace_id"],
                trace_effect["evidence_id"],
                trace_effect["location_id"],
                conversation_source_history_id,
            )
            interaction_result["evidence_trace_consequence"] = {
                "effect_id": trace_effect["effect_id"],
                **trace_result,
            }

        return candidate_world_state

    def process_command(self, player_input: str) -> Dict[str, Any]:
        interaction_result = process_player_input(
            player_input,
            self.scene_snapshot
        )
        interaction_result["actor_knowledge_response"] = None
        command_start_actor_knowledge = deepcopy(self.world_state["actor_knowledge"])

        if (
            interaction_result["intent"] == "skill_check"
            and interaction_result["success"]
        ):
            check_name = interaction_result["action"]["target"]
            interaction_result["skill_check"] = self.perform_skill_check(
                check_name
            )

        if (
            interaction_result["intent"] == "destination"
            and interaction_result["success"]
        ):
            destination_text = interaction_result["action"]["target"]
            destination_resolution = self.resolve_destination(
                destination_text
            )
            interaction_result["destination_resolution"] = (
                destination_resolution
            )
            interaction_result["success"] = (
                destination_resolution["status"] == "resolved"
            )
            if destination_resolution["status"] == "ambiguous":
                interaction_result["message"] = (
                    "That destination is ambiguous in the loaded region."
                )
            elif destination_resolution["status"] == "unresolved":
                interaction_result["message"] = (
                    "No known destination matches that name."
                )

        if (
            interaction_result["intent"] == "wait"
            and interaction_result["success"]
        ):
            duration_hours = interaction_result["action"]["parameters"][
                "duration_hours"
            ]
            interaction_result["time_advancement"] = self.advance_time(
                duration_hours
            )
            return deepcopy(interaction_result)
        if interaction_result["intent"] == "investigation" and interaction_result["success"]:
            interaction_result["investigation"] = self.investigate()
            return deepcopy(interaction_result)
        if interaction_result["intent"] == "clue_recall" and interaction_result["success"]:
            interaction_result["known_clues"] = list(self.get_known_clues())
            return deepcopy(interaction_result)
        if interaction_result["intent"] == "clue_presentation" and interaction_result["success"]:
            interaction_result["presentation"] = self.present_clue(interaction_result["action"]["parameters"]["clue_title"], interaction_result["action"]["target"] or "")
            return deepcopy(interaction_result)

        target_text = interaction_result["action"].get("target")
        if target_text and interaction_result["intent"] in {
            "conversation",
            "movement",
        }:
            target_resolution = self.resolve_target(target_text)
            interaction_result["target_resolution"] = target_resolution

            if (
                interaction_result["intent"] == "conversation"
                and target_resolution["status"] != "resolved"
            ):
                interaction_result["success"] = False
                if target_resolution["status"] == "ambiguous":
                    interaction_result["message"] = (
                        "That target is ambiguous in the current scene."
                    )
                else:
                    interaction_result["message"] = (
                        "No matching target is present in the current scene."
                    )

        candidate_world_state = apply_interaction(
            self.world_state,
            interaction_result
        )

        if (
            interaction_result["intent"] == "conversation"
            and interaction_result["success"]
            and interaction_result.get("target_resolution", {}).get(
                "target_type"
            ) == "entity"
        ):
            target_entity_id = interaction_result["target_resolution"][
                "identifier"
            ]
            candidate_world_state = self._compose_resolved_conversation_consequences(
                candidate_world_state,
                interaction_result,
                target_entity_id,
            )

        validate_world_state(candidate_world_state, self.region)
        candidate_scene_snapshot = build_scene(
            self.region,
            candidate_world_state
        )

        self.world_state = candidate_world_state
        self.scene_snapshot = candidate_scene_snapshot

        if (
            interaction_result["intent"] == "conversation"
            and interaction_result["success"]
            and interaction_result.get("target_resolution", {}).get("target_type") == "entity"
        ):
            target_entity_id = interaction_result["target_resolution"]["identifier"]
            interaction_result["actor_knowledge_response"] = (
                derive_conversation_actor_knowledge_response(
                    self.region,
                    target_entity_id,
                    tuple(command_start_actor_knowledge.get(target_entity_id, [])),
                )
            )

        return deepcopy(interaction_result)
