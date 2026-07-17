import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import engine.game_engine as game_engine_module
from engine.game_engine import GameEngine
from engine.region_validator import validate_region
from engine.save_system import build_save_data, load_game


REGION = "data/regions/bryn_shander.json"
DISCOVERY = "west_gate_elin_report_trace"
TEXT = 'Elin Voss studies the folded order, then nods. "You found it. The West Gate patrol is moving before the road closes."'


def data(): return json.loads(Path(REGION).read_text(encoding="utf-8"))

def invalid(region, text):
    try: validate_region(region)
    except ValueError as error:
        assert text in str(error), str(error); return
    raise AssertionError("Expected Region Pack validation failure.")

def resolve_and_arrive(engine, discover=False):
    engine.process_command("talk to captain"); engine.process_command("investigate")
    assert engine.present_clue("The Captain's Deliberate Trail", "captain")["changed"]
    assert engine.process_command("go south")["success"]
    assert engine.process_command("go east")["success"]
    assert engine.process_command("go north")["success"]
    if discover: assert engine.process_command("investigate")["investigation"]["discovery_id"] == DISCOVERY

def test_validation():
    region = data(); validate_region(region)
    absent = deepcopy(region); del absent["conversation_player_discovery_response"]; del absent["conversation_affordance"]; validate_region(absent)
    for field in (
        "response_id", "target_entity_id", "required_discovery_id",
        "consequence_event_type", "consequence_summary", "response_text",
    ):
        bad=deepcopy(region); del bad["conversation_player_discovery_response"][field]; invalid(bad,"fields are invalid")
        bad=deepcopy(region); bad["conversation_player_discovery_response"][field]=""; invalid(bad,"non-empty strings")
    bad=deepcopy(region); bad["conversation_player_discovery_response"]["extra"]=True; invalid(bad,"fields are invalid")
    bad=deepcopy(region); bad["conversation_player_discovery_response"]["target_entity_id"]="missing"; invalid(bad,"static actor")
    bad=deepcopy(region); bad["conversation_player_discovery_response"]["required_discovery_id"]="missing"; invalid(bad,"unknown")
    bad=deepcopy(region); bad["conversation_player_discovery_response"]["target_entity_id"]="captain_darvin_grey"; invalid(bad,"relocation actor")
    bad=deepcopy(region); bad["conversation_player_discovery_response"]["required_discovery_id"]="north_gate_captain_trace"; invalid(bad,"evidence trace")
    bad=deepcopy(region); bad["conversation_actor_knowledge_response"]["target_entity_id"]="guard_elin_voss"; invalid(bad,"must not overlap")

def test_projection_command_start_and_non_mutation():
    engine=GameEngine(REGION); resolve_and_arrive(engine)
    before=len(engine.query_history(event_type="player_conversation")); first=engine.process_command("talk to elin")
    assert first["success"] and first["player_discovery_response"] is None and len(engine.query_history(event_type="player_conversation"))==before+1
    assert engine.process_command("investigate")["investigation"]["discovery_id"]==DISCOVERY
    state, scene=engine.get_world_state(), engine.scene_snapshot
    result=engine.process_command("talk to elin")
    assert result["player_discovery_response"]=={"text":TEXT} and result["actor_knowledge_response"] is None
    consequence = result["player_discovery_response_consequence"]
    assert consequence["event_type"] == "west_gate_patrol_dispatched"
    assert consequence["history_id"]
    assert len(engine.query_history(event_type="player_conversation"))==before+2
    assert engine.get_world_state()["player_discoveries"]==state["player_discoveries"] and engine.scene_snapshot is not scene
    assert len(engine.query_history(event_type="west_gate_patrol_dispatched")) == 1
    repeated = engine.process_command("talk to elin")
    assert repeated["success"] and repeated["player_discovery_response"] is None
    assert repeated["player_discovery_response_consequence"] is None
    assert len(engine.query_history(event_type="west_gate_patrol_dispatched")) == 1
    assert engine.get_player_perception()["conversation_affordance"] == {}
    for packet in (engine.get_scene_snapshot(),engine.get_player_perception(),engine.get_narration_context("look"),engine.get_narration_preview("look"),engine.process_command("talk to elin")):
        assert DISCOVERY not in repr(packet)
    engine.process_command("go east"); engine.process_command("go north")
    assert engine.process_command("talk to captain")["actor_knowledge_response"] is not None

def test_command_start_failure_and_save_load():
    engine=GameEngine(REGION); resolve_and_arrive(engine)
    original=game_engine_module.apply_interaction
    def add_discovery(candidate, result):
        candidate=original(candidate,result)
        if result["intent"]=="conversation": candidate["player_discoveries"].append(DISCOVERY)
        return candidate
    with patch.object(game_engine_module,"apply_interaction",side_effect=add_discovery):
        assert engine.process_command("talk to elin")["player_discovery_response"] is None
    assert engine.process_command("talk to elin")["player_discovery_response"]=={"text":TEXT}
    state, scene=engine.get_world_state(), engine.scene_snapshot
    with patch.object(game_engine_module,"build_scene",side_effect=RuntimeError("scene")):
        try: engine.process_command("talk to elin")
        except RuntimeError: pass
        else: raise AssertionError("Expected scene failure")
    assert engine.get_world_state()==state and engine.scene_snapshot is scene
    with TemporaryDirectory() as directory:
        path=Path(directory)/"save.json"; path.write_text(json.dumps(build_save_data(engine)),encoding="utf-8")
        loaded = load_game(str(path))
        assert loaded.process_command("talk to elin")["player_discovery_response"] is None
        assert len(loaded.query_history(event_type="west_gate_patrol_dispatched")) == 1

def main():
    test_validation(); test_projection_command_start_and_non_mutation(); test_command_start_failure_and_save_load()
    print("Discovery-gated relocated-actor response tests passed.")

if __name__ == "__main__": main()
