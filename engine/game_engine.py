from copy import deepcopy
from typing import Any, Dict

from engine.scene_loader import load_region, build_scene
from engine.perception_builder import build_perception
from engine.pressure_observation import derive_pressure_observation
from engine.unresolved_threads import (
    derive_unresolved_thread_evidence,
    get_open_threads as get_world_open_threads,
    prepare_open_thread_candidate,
)
from engine.scene_narrator import narrate_scene
from engine.navigation_projection import derive_navigation_projection
from engine.current_scene_projection import build_current_scene_projection
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
from engine.player_discovery_response import derive_conversation_player_discovery_response
from engine.conversation_affordance import derive_conversation_affordance
from engine.action_eligibility import (
    find_eligible_investigation_discovery,
    is_clue_presentation_acceptable,
)
from engine.contextual_action_projection import derive_contextual_action_projection
from engine.elapsed_time_transition_observation import (
    derive_elapsed_time_transition_observation,
)
from engine.evidence_traces import (
    get_evidence_trace as get_world_evidence_trace,
    get_evidence_traces as get_world_evidence_traces,
    get_evidence_traces_at_location as get_world_evidence_traces_at_location,
)
from engine import west_road_predicament as west_road
from engine import character_competence
from engine import west_road_market_theft


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
        declaration = find_eligible_investigation_discovery(self.region, candidate)
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
        if west_road.enabled(self.region):
            return self._share_west_road_clue(clue_title, actor_text)
        result = {"changed": False, "response_text": None, "resolved_observation": None,
                  "actor_location_consequence": None, "actor_knowledge_consequence": None,
                  "evidence_trace_consequence": None}
        if not isinstance(clue_title, str) or not isinstance(actor_text, str):
            return result
        clue = next((item for item in self.region.get("discovery_declarations", []) if item["title"].casefold() == clue_title.casefold()), None)
        target = self.resolve_target(actor_text)
        if not is_clue_presentation_acceptable(
            self.region, self.world_state, clue, target
        ):
            return result
        declaration = self.region.get("conversation_discovery_resolution")
        recall = self.region.get("conversation_discovery_actor_relocation")
        recall_matches = (
            isinstance(recall, dict)
            and clue["discovery_id"] == recall["required_discovery_id"]
            and target["identifier"] == recall["target_entity_id"]
        )
        if recall_matches:
            candidate = copy_world_state(self.world_state)
            candidate = add_history_entry(
                candidate, "clue_presented", "Player presented an authored clue.",
                extra={"target_entity_id": target["identifier"]},
            )
            source_id = candidate["history"][-1]["history_id"]
            candidate, relocation_result = self._prepare_actor_location_candidate(
                candidate, recall["actor_entity_id"],
                recall["destination_location_id"], source_id,
            )
            validate_world_state(candidate, self.region)
            scene = build_scene(self.region, candidate)
            self.world_state, self.scene_snapshot = candidate, scene
            result.update({
                "changed": True,
                "response_text": recall["response_text"],
                "actor_location_consequence": {
                    "status": "applied" if relocation_result["changed"] else "no_op"
                },
            })
            return deepcopy(result)
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
        knowledge_effect = self.region.get("resolved_thread_actor_knowledge_effect")
        if knowledge_effect is not None and knowledge_effect["resolved_thread_id"] == thread_id:
            candidate, knowledge_result = self._prepare_actor_knowledge_from_event_candidate(
                candidate, knowledge_effect["actor_entity_id"],
                knowledge_effect["knowledge_id"], source_id,
            )
            result["actor_knowledge_consequence"] = {
                "status": "applied" if knowledge_result["changed"] else "no_op"
            }
        trace_effect = self.region.get("resolved_thread_evidence_trace_effect")
        if trace_effect is not None and trace_effect["resolved_thread_id"] == thread_id:
            candidate, trace_result = self._prepare_evidence_trace_candidate(
                candidate, trace_effect["trace_id"], trace_effect["evidence_id"],
                trace_effect["location_id"], source_id,
            )
            result["evidence_trace_consequence"] = {
                "status": "applied" if trace_result["changed"] else "no_op"
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
        packet = build_narration_context_packet(
            self.world_state,
            {**self.scene_snapshot, **({"character_competence": self.get_competence_projection()} if west_road.enabled(self.region) else {})},
            player_input,
            history_count=history_count,
            pressure_cue=pressure_cues[0] if pressure_cues else None,
        )
        if west_road_market_theft.visible_text(self.world_state, get_player_location_id(self.world_state)):
            packet["boundary"]["drift_guardrail"] += " " + west_road_market_theft.NARRATION_LIMIT
        return packet

    def get_narration_output_contract(self) -> Dict[str, Any]:
        return build_narration_output_contract()

    def validate_narration_output(
        self,
        narration_output: Dict[str, Any]
    ) -> Dict[str, Any]:
        return validate_narration_output_packet(narration_output)

    def get_narration_preview(
        self,
        player_input: str,
        presentation: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        narration_context = self.get_narration_context(player_input)
        if presentation is not None:
            narration_context["scene_context"]["presentation"] = deepcopy(presentation)
        return build_narration_preview_packet(narration_context)

    def _prepare_time_advance_candidate(
        self, candidate_world_state: Dict[str, Any], duration_hours: int
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """Prepare one time transition without validating, building, or publishing."""
        previous_time = get_time(candidate_world_state)
        new_time = advance_time_by_hours(previous_time, duration_hours)
        location_id = get_player_location_id(candidate_world_state)
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
        candidate_world_state = west_road_market_theft.advance_candidate(
            candidate_world_state, previous_time, new_time, source_history_id
        )
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

        return candidate_world_state, {
            "duration_hours": duration_hours,
            "previous_time": previous_time,
            "new_time": new_time,
            "pressure_consequence": deepcopy(pressure_consequence),
            "actor_location_consequence": deepcopy(actor_location_consequence),
            "evidence_trace_consequence": deepcopy(evidence_trace_consequence),
        }

    def advance_time(self, duration_hours: int = 1) -> Dict[str, Any]:
        candidate_world_state, result = self._prepare_time_advance_candidate(
            copy_world_state(self.world_state), duration_hours
        )
        validate_world_state(candidate_world_state, self.region)
        candidate_scene_snapshot = build_scene(self.region, candidate_world_state)
        self.world_state = candidate_world_state
        self.scene_snapshot = candidate_scene_snapshot
        return result

    def _is_declared_one_hour_west_road_traversal(
        self,
        interaction_result: Dict[str, Any],
        world_state: Dict[str, Any] | None = None,
    ) -> bool:
        declaration = self.region.get("one_hour_west_road_exit_traversal")
        return (
            interaction_result.get("intent") == "movement"
            and interaction_result.get("success")
            and isinstance(declaration, dict)
            and get_player_location_id(world_state or self.world_state)
            == declaration.get("source_location_id")
            and interaction_result.get("destination_location_id")
            == declaration.get("destination_location_id")
        )

    def _prepare_declared_one_hour_west_road_traversal(
        self,
        candidate_world_state: Dict[str, Any],
        interaction_result: Dict[str, Any],
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        declaration = self.region["one_hour_west_road_exit_traversal"]
        candidate_world_state, time_result = self._prepare_time_advance_candidate(
            candidate_world_state, declaration["duration_hours"]
        )
        candidate_world_state = apply_interaction(
            candidate_world_state, interaction_result
        )
        arrival_trace = self.region.get("west_road_arrival_evidence_trace")
        if isinstance(arrival_trace, dict):
            movement_history_id = candidate_world_state["history"][-1]["history_id"]
            candidate_world_state, _ = self._prepare_evidence_trace_candidate(
                candidate_world_state,
                arrival_trace["trace_id"],
                arrival_trace["evidence_id"],
                arrival_trace["destination_location_id"],
                movement_history_id,
            )
        return candidate_world_state, time_result

    def _complete_declared_one_hour_west_road_traversal(
        self, interaction_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Commit the one supported timed traversal as one outer transition."""
        time_result = self._complete_movement_hop(interaction_result)
        if time_result is None:
            raise ValueError("Declared timed traversal did not advance time.")
        return time_result

    def _complete_movement_hop(
        self, interaction_result: Dict[str, Any]
    ) -> Dict[str, Any] | None:
        """Commit one validated movement hop and rebuild its authoritative scene."""
        candidate_world_state = copy_world_state(self.world_state)
        time_result = None
        if self._is_declared_one_hour_west_road_traversal(
            interaction_result, candidate_world_state
        ):
            candidate_world_state, time_result = (
                self._prepare_declared_one_hour_west_road_traversal(
                    candidate_world_state, interaction_result
                )
            )
        else:
            candidate_world_state = apply_interaction(
                candidate_world_state, interaction_result
            )
        validate_world_state(candidate_world_state, self.region)
        candidate_scene_snapshot = build_scene(self.region, candidate_world_state)
        self.world_state = candidate_world_state
        self.scene_snapshot = candidate_scene_snapshot
        return time_result

    def get_scene_snapshot(self) -> Dict[str, Any]:
        return deepcopy(self.scene_snapshot)

    def get_player_perception(self) -> Dict[str, Any]:
        applicable = self.get_applicable_pressures()
        cue = derive_pressure_observation(
            applicable,
            self.region.get("pressure_observation_cue"),
        )
        conversation_affordance = derive_conversation_affordance(
            self.region,
            get_player_location_id(self.world_state),
            self.scene_snapshot,
            tuple(self.world_state["player_discoveries"]),
            tuple(self.world_state["history"]),
        )
        perception = build_perception(
            self.scene_snapshot,
            [] if cue is None else [cue],
            derive_unresolved_thread_evidence(
                self.world_state["open_threads"],
                self.region.get("conversation_unresolved_thread"),
                get_player_location_id(self.world_state),
            ),
            {},
            conversation_affordance,
            derive_navigation_projection(
                self.scene_snapshot,
                self.region.get("locations", []),
            ),
            derive_contextual_action_projection(
                self.region,
                self.world_state,
                self.scene_snapshot,
                conversation_affordance,
            ),
        )

        if west_road.enabled(self.region):
            perception["character_competence"] = self.get_competence_projection()
        return perception

    def get_current_scene_projection(self) -> Dict[str, Any]:
        projection = build_current_scene_projection(
            self.region,
            self.scene_snapshot,
            self.get_player_perception(),
        )

        if west_road.enabled(self.region):
            projection["character_competence"] = self.get_competence_projection()
        return projection

    def get_narration(self) -> Dict[str, Any]:
        perception = self.get_player_perception()
        if west_road.scene_relevant(self.region, self.world_state):
            from engine.west_road_presentation import CURRENT_CIRCUMSTANCES, CURRENT_CHOICE_HINTS, compact_secondary_actions
            projection = self.get_current_scene_projection()
            base = narrate_scene(perception)
            actors = projection["entities"]["actors"]
            groups = projection["entities"]["groups"]
            names = [a["display_name"] for a in actors]
            base["title"] = projection["location"]["name"] + ", Bryn Shander"
            environment = [projection["location"]["description"]]
            weather = self.world_state["weather"].get("type")
            if weather:
                environment.append("Weather: " + weather + ".")
            environment.extend(cue["text"] for cue in perception["pressure_cues"])
            parts = [" ".join(environment)]
            present = names + [str(g["count"]) + " " + g["display_name"] for g in groups]
            if present:
                parts.append("Here: " + ", ".join(present) + ".")
            phase = self.world_state["west_road_predicament"]["phase"]
            parts.append(CURRENT_CIRCUMSTANCES[phase])
            competence = self.get_competence_projection()
            outcome_texts = [item["text"] for item in competence["accepted_outcomes"]]
            for layer in ("observations", "recognition", "findings"):
                parts.extend(item["text"] for item in competence[layer]
                             if layer != "findings" or not any(item["text"] in text for text in outcome_texts))
            parts.extend(outcome_texts)
            opportunities = perception["contextual_actions"]["opportunities"]
            choices = [text.removeprefix("You can choose: ") for text in opportunities if text.startswith("You can choose:")]
            if choices:
                parts.append("What now?\n" + "\n".join("- " + choice for choice in choices))
                choice_hint = CURRENT_CHOICE_HINTS[phase] if phase != "investigating" else "Choose 'advocate patrol' or 'continue investigation' now that Elin has both reports."
            else:
                next_action = CURRENT_CHOICE_HINTS[phase]
                if phase == "investigating":
                    discovered = set(self.world_state["player_discoveries"])
                    shared = set(self.world_state["actor_knowledge"].get(west_road.ELIN, []))
                    if set(west_road.INITIAL_EVIDENCE) <= discovered:
                        missing_reports = [d["title"] for d in self.region["discovery_declarations"] if d["discovery_id"] in west_road.INITIAL_EVIDENCE and west_road.shared_id(d["discovery_id"]) not in shared]
                        next_action = "Report " + " and ".join(missing_reports) + " to Elin at the North Gate before choosing a response."
                        if not missing_reports:
                            next_action = "Return to Grey and Elin at the North Gate to choose a response."
                    elif self.world_state["player"]["current_location_id"] == west_road.ROAD:
                        if "west_road_tracks" in discovered:
                            next_action = "Speak with Mara about the overdue caravan."
                        elif "west_road_merchant_account" in discovered:
                            next_action = "Investigate the tracks beside the road (investigate)."
                        else:
                            next_action = "Investigate the tracks and speak with Mara about the overdue caravan."
                elif phase in ("observers_withdrew", "wagon_intercepted"):
                    next_action = "Return to Grey and Elin at the North Gate. " + next_action
                parts.append("What now?\n" + next_action)
                choice_hint = next_action
            secondary = compact_secondary_actions(opportunities)
            routes = " ".join(cue["text"] for cue in perception["navigation"]["route_cues"])
            if secondary or routes:
                parts.append("Other actions:\n" + "\n".join(text for text in (secondary, routes) if text))
            base["description"] = "\n\n".join(parts)
            base["visible_entities"] = names
            base["player_prompt"] = ""
            base["current_choice_hint"] = choice_hint
            return base
        return narrate_scene(perception)

    def get_resume_summary(self) -> list[str]:
        if not west_road.enabled(self.region):
            return []
        return west_road.summary(self.region, self.world_state)

    def _publish_west_road_candidate(self, candidate):
        validate_world_state(candidate, self.region)
        scene = build_scene(self.region, candidate)
        self.world_state, self.scene_snapshot = candidate, scene

    def _acquire_west_road_discovery(self, candidate, discovery_id, source_id):
        clue = next(d for d in self.region["discovery_declarations"] if d["discovery_id"] == discovery_id)
        candidate, _ = self._prepare_evidence_trace_candidate(candidate, clue["trace_id"], discovery_id, clue["location_id"], source_id)
        if discovery_id not in candidate["player_discoveries"]:
            candidate["player_discoveries"].append(discovery_id)
            candidate = add_history_entry(candidate, "player_discovery_added", "Player learned: " + clue["title"], clue["location_id"], deepcopy(candidate["time"]), {"discovery_id": discovery_id, "source_history_id": source_id})
        return candidate

    def _share_west_road_clue(self, clue_title, actor_text):
        result = {"changed": False, "response_text": None}
        clue = next((d for d in self.region["discovery_declarations"] if d["title"].casefold() == clue_title.casefold()), None)
        target = self.resolve_target(actor_text)
        if clue is None or clue["discovery_id"] not in self.world_state["player_discoveries"] or target.get("status") != "resolved" or target.get("identifier") not in (west_road.GREY, west_road.ELIN):
            return result
        actor = target["identifier"]
        knowledge = west_road.shared_id(clue["discovery_id"])
        if knowledge in self.world_state["actor_knowledge"].get(actor, []):
            result["response_text"] = target["display_name"] + " already received that report."
            return result
        candidate = copy_world_state(self.world_state)
        candidate = add_history_entry(candidate, "west_road_evidence_shared", "Player reported " + clue["title"] + " to " + target["display_name"] + ".", get_player_location_id(candidate), deepcopy(candidate["time"]), {"actor_id": actor, "discovery_id": clue["discovery_id"]})
        candidate, _ = self._prepare_actor_knowledge_from_event_candidate(candidate, actor, knowledge, candidate["history"][-1]["history_id"])
        self._publish_west_road_candidate(candidate)
        result.update(changed=True, response_text=target["display_name"] + " receives the report. It informs the decision; it does not prove the observers' identity or select a response.")
        return result

    def _process_west_road_command(self, command):
        result = {"success": False, "intent": "west_road_decision", "message": "That decision is not available here. Return to Grey and Elin with the required evidence.", "action": {"type": "west_road_decision", "target": None, "parameters": {}, "confidence": 1.0}}
        if command not in west_road.available_commands(self.world_state, self.scene_snapshot):
            if self.world_state["west_road_predicament"]["phase"] != "investigating":
                result["message"] = "That choice does not apply to the current west-road situation. Your accepted decisions remain unchanged."
            return result
        candidate, result = self._prepare_west_road_command(copy_world_state(self.world_state), command, result)
        self._publish_west_road_candidate(candidate)
        return result

    def _prepare_west_road_command(self, candidate, command, result, source_id=None):
        before, after = west_road.COMMANDS[command]
        was_reduced = west_road_market_theft.reduced_coverage(candidate)
        candidate = add_history_entry(candidate, "west_road_commitment", "Player chose to " + command + ".", west_road.GATE, deepcopy(candidate["time"]), {"command": command, "from_phase": before, **({"source_history_id": source_id} if source_id else {})})
        commitment_id = candidate["history"][-1]["history_id"]
        time_id = None
        if before == "investigating":
            candidate, time_result = self._prepare_time_advance_candidate(candidate, 1)
            time_entry = next(e for e in reversed(candidate["history"]) if e["event_type"] == "time_advanced")
            time_entry["source_history_id"] = commitment_id
            time_id = time_entry["history_id"]
            result["time_advancement"] = time_result
        for discovery in west_road.PHASE_DISCOVERIES[after]:
            candidate = self._acquire_west_road_discovery(candidate, discovery, commitment_id)
            for actor in (west_road.GREY, west_road.ELIN):
                candidate = add_history_entry(candidate, "west_road_evidence_shared", "Player reported new west-road findings.", west_road.GATE, deepcopy(candidate["time"]), {"actor_id": actor, "discovery_id": discovery, "source_history_id": commitment_id})
                candidate, _ = self._prepare_actor_knowledge_from_event_candidate(candidate, actor, west_road.shared_id(discovery), candidate["history"][-1]["history_id"])
        candidate = add_history_entry(candidate, "west_road_outcome", self.region["west_road_predicament"]["phase_text"][after], west_road.GATE, deepcopy(candidate["time"]), {"phase": after, "source_history_id": commitment_id, "time_history_id": time_id, "witness_entity_ids": [west_road.GREY, west_road.ELIN]})
        candidate["west_road_predicament"] = {"phase": after, "last_outcome_history_id": candidate["history"][-1]["history_id"]}
        west_road_market_theft.allocation_changed(candidate, was_reduced)
        responses = [west_road.actor_response(self.region, candidate, actor)["text"] for actor in (west_road.GREY, west_road.ELIN)]
        result.update(success=True, message=self.region["west_road_predicament"]["phase_text"][after] + "\nGrey: " + responses[0] + "\nElin: " + responses[1])
        return candidate, deepcopy(result)

    def get_competence_projection(self):
        return character_competence.project(self.region, self.world_state, self.scene_snapshot)

    def attempt_competence(self, command):
        """Execute a bounded operation; draw and outcome are never input parameters."""
        command = command.strip().lower()
        accepted = self.world_state.get("competence_attempts", {}).get(command)
        result = {"success": False, "intent": "west_road_competence", "message": "", "action": {"type": "west_road_competence", "target": None, "parameters": {}, "confidence": 1.0}}
        if accepted is not None:
            result.update(success=True, changed=False, accepted_outcome=deepcopy(accepted), message=character_competence.outcome_text(self.region, command, accepted))
            return result
        decision = character_competence.assess(self.region, self.world_state, self.scene_snapshot, command)
        if not decision["eligible"]:
            result["message"] = decision["reason"]
            return result
        draw = character_competence.draw_d6() if decision["uncertain"] else None
        outcome = character_competence.resolve(draw, decision["specialist"]) if decision["uncertain"] else "full"
        candidate = copy_world_state(self.world_state)
        candidate = add_history_entry(candidate, "west_road_competence_attempt", "Player chose to " + command + ".", west_road.GATE, deepcopy(candidate["time"]), {"command": command, "from_phase": "observers_withdrew", "specialist": decision["specialist"], "assistance_entity_ids": [] if decision["uncertain"] else [west_road.GREY, west_road.ELIN]})
        source_id = candidate["history"][-1]["history_id"]
        candidate, time_result = self._prepare_time_advance_candidate(candidate, decision["cost_hours"])
        time_event = next(e for e in reversed(candidate["history"]) if e["event_type"] == "time_advanced")
        time_event["source_history_id"] = source_id
        time_id = time_event["history_id"]
        findings = []
        if outcome == "partial":
            findings = [character_competence.OPERATIONS[command][1]]
            candidate = self._acquire_west_road_discovery(candidate, findings[0], source_id)
        elif outcome == "full":
            findings = ["west_road_withdrawal_route"]
            candidate, _ = self._prepare_west_road_command(candidate, "pursue observers", {}, source_id)
        attempt = {"draw": draw, "result": outcome, "specialist": decision["specialist"], "cost_hours": decision["cost_hours"], "findings": findings, "source_history_id": source_id, "time_history_id": time_id, "outcome_history_id": None}
        candidate = add_history_entry(candidate, "west_road_competence_result", "Accepted " + outcome + " competence outcome.", west_road.GATE, deepcopy(candidate["time"]), {"source_history_id": source_id})
        attempt["outcome_history_id"] = candidate["history"][-1]["history_id"]
        candidate["history"][-1]["attempt"] = deepcopy(attempt)
        candidate.setdefault("competence_attempts", {})[command] = attempt
        self._publish_west_road_candidate(candidate)
        result.update(success=True, changed=True, accepted_outcome=deepcopy(attempt), time_advancement=time_result, message=character_competence.outcome_text(self.region, command, attempt))
        return result

    def _merchant_account(self):
        discovery = "west_road_merchant_account"
        result = {"success": True, "intent": "conversation", "message": "Mara has already told you about her detour.", "action": {"type": "talk", "target": "Mara", "parameters": {}, "confidence": 1.0}}
        if discovery in self.world_state["player_discoveries"]:
            return result
        candidate = copy_world_state(self.world_state)
        candidate = add_history_entry(candidate, "player_conversation", "Mara described seeing observers and avoiding the road.", west_road.ROAD, deepcopy(candidate["time"]), {"target_entity_id": west_road.MERCHANT, "target_display_name": "Mara, Caravan Driver"})
        candidate = self._acquire_west_road_discovery(candidate, discovery, candidate["history"][-1]["history_id"])
        self._publish_west_road_candidate(candidate)
        result["message"] = next(d["text"] for d in self.region["discovery_declarations"] if d["discovery_id"] == discovery)
        return result

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
        if player_input.strip().lower() in character_competence.OPERATIONS:
            return self.attempt_competence(player_input)
        if west_road.enabled(self.region) and player_input.strip().lower() in west_road.COMMANDS:
            return self._process_west_road_command(player_input.strip().lower())
        interaction_result = process_player_input(
            player_input,
            self.scene_snapshot,
            self.region.get("locations", []),
        )
        interaction_result["actor_knowledge_response"] = None
        interaction_result["player_discovery_response"] = None
        interaction_result["player_discovery_response_consequence"] = None
        command_start_actor_knowledge = deepcopy(self.world_state["actor_knowledge"])
        command_start_player_discoveries = tuple(self.world_state["player_discoveries"])
        command_start_history = tuple(deepcopy(self.world_state["history"]))

        if west_road.enabled(self.region) and interaction_result["intent"] == "conversation":
            target = self.resolve_target(interaction_result["action"].get("target") or "")
            if target.get("status") == "resolved" and target.get("identifier") == west_road.MERCHANT:
                return self._merchant_account()

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
            command_start_scene = deepcopy(self.scene_snapshot)
            duration_hours = interaction_result["action"]["parameters"][
                "duration_hours"
            ]
            interaction_result["time_advancement"] = self.advance_time(
                duration_hours
            )
            interaction_result["message"] = derive_elapsed_time_transition_observation(
                command_start_scene,
                self.scene_snapshot,
                self.region.get("entities", []),
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

        if self._is_declared_one_hour_west_road_traversal(interaction_result):
            interaction_result["time_advancement"] = (
                self._complete_declared_one_hour_west_road_traversal(
                    interaction_result
                )
            )
            return deepcopy(interaction_result)

        movement_hops = interaction_result.get("movement_hops")
        if (
            interaction_result["success"]
            and isinstance(movement_hops, list)
            and movement_hops
        ):
            time_advancements = []
            for hop_result in movement_hops:
                if not isinstance(hop_result, dict):
                    raise ValueError("Validated movement hops must be dictionaries.")
                time_result = self._complete_movement_hop(hop_result)
                if time_result is not None:
                    time_advancements.append(time_result)
            if time_advancements:
                interaction_result["time_advancements"] = time_advancements
            return deepcopy(interaction_result)
        elif not isinstance(movement_hops, list):
            candidate_world_state = apply_interaction(
                self.world_state,
                interaction_result
            )
        else:
            raise ValueError("Validated abstract traversal must contain one or more hops.")

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
            player_discovery_response = derive_conversation_player_discovery_response(
                self.region,
                target_entity_id,
                command_start_player_discoveries,
                command_start_history,
            )
            if player_discovery_response is not None:
                declaration = self.region["conversation_player_discovery_response"]
                candidate_world_state = add_history_entry(
                    candidate_world_state,
                    declaration["consequence_event_type"],
                    declaration["consequence_summary"],
                    get_player_location_id(candidate_world_state),
                    deepcopy(candidate_world_state["time"]),
                    {"response_id": declaration["response_id"]},
                )
                interaction_result["player_discovery_response"] = (
                    player_discovery_response
                )
                interaction_result["player_discovery_response_consequence"] = {
                    "event_type": declaration["consequence_event_type"],
                    "history_id": candidate_world_state["history"][-1]["history_id"],
                }

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

        if west_road.enabled(self.region) and interaction_result["intent"] == "conversation" and interaction_result["success"]:
            actor = interaction_result.get("target_resolution", {}).get("identifier")
            response = west_road.actor_response(self.region, self.world_state, actor)
            if response:
                interaction_result["actor_knowledge_response"] = response
        return deepcopy(interaction_result)
