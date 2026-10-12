"""Offline production acceptance for two structurally different material scenes."""
from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import replace
from io import StringIO
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from engine.game_engine import GameEngine
from engine import game_engine, character_competence as competence, material_state as material
from engine.contextual_action import HandlingFrame, interpret
from engine.save_system import build_save_data, load_game
from engine.world_state import validate_world_state
from engine.region_validator import validate_region
import play_game

MARKET = "data/regions/market_passage_v1.json"
ARCHIVE = "test_fixtures/archive_shutter.json"
ARTIFACTS = Path(".artifacts")


def denied(*args, **kwargs):
    raise AssertionError("Provider/network forbidden")


class Acceptance(unittest.TestCase):
    def setUp(self):
        self.guards = [patch("socket.create_connection", side_effect=denied),
                       patch.object(socket.socket, "connect", side_effect=denied),
                       patch.object(socket.socket, "connect_ex", side_effect=denied),
                       patch("engine.narration_source.OpenAI", side_effect=denied)]
        for guard in self.guards: guard.start()
        self.addCleanup(lambda: [guard.stop() for guard in reversed(self.guards)])
        ARTIFACTS.mkdir(exist_ok=True)

    def engine(self, path=MARKET):
        return GameEngine(path)

    def record(self, e):
        return next(iter(e.get_world_state()[material.STATE_KEY].values()))

    def accept(self, e, command, draw=6):
        proposal = e.process_command(command)
        self.assertEqual(proposal["contextual_action"]["status"], "authorization_required", proposal)
        with patch.object(competence, "draw_d6", return_value=draw):
            return e.process_command("All right, try it carefully")

    def unchanged(self, e, world, scene=None, focus=None):
        self.assertEqual(e.get_world_state(), world)
        if scene is not None: self.assertEqual(e.get_scene_snapshot(), scene)
        if focus is not None: self.assertEqual(e.get_action_context(), focus)

    def test_01_equivalent_objectives_without_survey(self):
        for text in ("Help get the cart out of the passage without damaging the cargo",
                     "Clear the passage without harming the cargo",
                     "Move the cart aside carefully", "Brace the cart and push it aside",
                     "Shift the cart with the driver's help"):
            with self.subTest(text=text):
                e=self.engine(); r=self.accept(e,text)
                self.assertEqual(r["contextual_action"]["outcome"],"full")
                self.assertEqual(self.record(e)["conditions"],dict(stability="braced",fitting="crooked",position="clear",integrity="intact"))
                self.assertEqual(self.record(e)["cooperation"],"willing")
                self.assertEqual(e.get_world_state()["time"]["elapsed_hours"],1)
                self.assertEqual(e.get_player_discoveries(),())
                self.assertEqual(e.get_actor_knowledge("delivery_driver"),())

    def test_02_shared_raw_and_structured_pathways(self):
        for path,text in ((MARKET,"Move the cart aside"),(ARCHIVE,"Close the shutter"),(ARCHIVE,"Secure the reading area against drafts")):
            a,b=self.engine(path),self.engine(path)
            frame=interpret(b,text); self.assertIsInstance(frame,HandlingFrame)
            self.assertEqual(a.process_command(text),b.process_contextual_action(frame=frame))
            with patch.object(competence,"draw_d6",return_value=5):
                self.assertEqual(a.process_command("yes"),b.process_contextual_action("yes"))
            self.assertEqual(a.get_world_state(),b.get_world_state())
            self.assertEqual(a.assess_contextual_action(frame)["status"],"impossible")

    def test_03_risk_cost_disclosure_and_confirmation(self):
        e=self.engine(); before=e.get_world_state()
        with patch.object(competence,"draw_d6",side_effect=denied):
            r=e.process_command("Force the cart aside alone")
        self.assertIn("damage the cargo",r["message"]); self.assertIn("1 hour",r["message"])
        self.unchanged(e,before)
        self.assertFalse(e.process_command("maybe")["success"])
        self.assertFalse(e.process_command("yes")["success"])
        r=self.accept(e,"Force the cart aside alone",draw=1)
        self.assertEqual(r["contextual_action"]["outcome"],"failure")
        self.assertEqual(self.record(e)["conditions"]["integrity"],"damaged")
        validate_world_state(e.get_world_state(),e.region)

    def test_04_constraints_cannot_be_acknowledged_away(self):
        for command in ("Force the cart aside without damaging cargo", "Move the cart; do not move it", "Move the cart without talking to the driver", "Adjust the wheel without touching it", "Force the cart aside, keeping cargo intact"):
            e=self.engine(); before=e.get_world_state()
            r=e.process_command(command); self.assertFalse(r["success"],command)
            self.assertIsNone(e.get_action_context()["pending"])
            self.assertFalse(e.process_command("yes")["success"]); self.unchanged(e,before)
        e=self.engine(); e.process_command("Force the cart aside")
        before=e.get_world_state()
        self.assertFalse(e.process_command("yes, but don't damage the cargo")["success"])
        self.assertFalse(e.process_command("yes")["success"]); self.unchanged(e,before)

    def test_05_stale_and_ambiguous_authorization(self):
        e=self.engine(); e.process_command("Adjust the wheel"); e.advance_time(1)
        before=e.get_world_state()
        self.assertEqual(e.process_command("yes")["contextual_action"]["status"],"stale_authorization")
        self.unchanged(e,before)
        e=self.engine(); e.process_command("Move the cart"); e.set_actor_location("delivery_driver","side_lane")
        before=e.get_world_state(); self.assertFalse(e.process_command("yes")["success"]); self.unchanged(e,before)
        e=self.engine(); e.process_command("Move the cart"); before=e.get_world_state()
        self.assertFalse(e.process_command("yes or no")["success"])
        self.assertFalse(e.process_command("continue")["success"]); self.unchanged(e,before)

    def test_06_feasible_uncertain_impossible_unsupported(self):
        e=self.engine(); before=e.get_world_state()
        frame=interpret(e,"Adjust the wheel")
        self.assertEqual(e.assess_contextual_action(frame)["status"],"uncertain")
        self.assertEqual(e.assess_contextual_action(replace(frame,operation="fly"))["status"],"unsupported")
        self.assertEqual(e.process_contextual_action(frame={})["contextual_action"]["status"],"unsupported")
        for text in ("Unload the cart", "Move the cart using magic", "Move the cart with a crane", "Move and repair the cart"):
            self.assertFalse(e.process_command(text)["success"],text)
        self.unchanged(e,before)
        e.process_command("go to Side Lane")
        self.assertEqual(e.assess_contextual_action(frame)["status"],"impossible")

    def test_07_npc_willingness_and_presence(self):
        e=self.engine(); e.set_actor_location("delivery_driver","side_lane")
        self.assertFalse(e.process_command("Ask the driver to help")["success"])
        e.set_actor_location("delivery_driver","market_square")
        r=e.process_command("Ask the driver to help")
        self.assertTrue(r["success"]); self.assertEqual(self.record(e)["cooperation"],"willing")
        self.assertEqual(e.get_world_state()["time"]["elapsed_hours"],0)
        self.assertEqual(e.get_actor_knowledge("delivery_driver"),())
        e=self.engine(); self.accept(e,"Adjust the wheel",draw=1)
        self.assertEqual(self.record(e)["conditions"]["fitting"],"jammed")
        r=e.process_command("Ask the driver to help")
        self.assertIn("refuses",r["message"]); self.assertEqual(self.record(e)["cooperation"],"refused")
        self.assertFalse(e.process_command("Move the cart")["success"])

    def test_08_all_draws_both_fixtures(self):
        for path,text,full,partial,unchanged in ((MARKET,"Move the cart","clear","narrow","blocked"),(ARCHIVE,"Close the shutter","closed","ajar","open")):
            for draw in range(1,7):
                with self.subTest(path=path,draw=draw):
                    e=self.engine(path); r=self.accept(e,text,draw)
                    expected=competence.resolve(draw,False)
                    self.assertEqual(r["contextual_action"]["outcome"],expected)
                    self.assertEqual(self.record(e)["conditions"]["position"],{"full":full,"partial":partial,"failure":unchanged}[expected])
                    self.assertEqual(e.get_world_state()["time"]["elapsed_hours"],1)
                    validate_world_state(e.get_world_state(),e.region)

    def test_09_distinct_approaches_and_changed_feasibility(self):
        e=self.engine(); self.accept(e,"Brace the cart")
        self.assertEqual(self.record(e)["conditions"]["position"],"blocked")
        e=self.engine(); self.accept(e,"Adjust the wheel",draw=6)
        self.assertEqual(self.record(e)["conditions"]["fitting"],"aligned")
        self.assertEqual(self.record(e)["conditions"]["position"],"blocked")
        self.accept(e,"Move the cart",draw=6)
        self.assertEqual(self.record(e)["conditions"]["position"],"clear")
        self.assertEqual(self.record(e)["conditions"]["fitting"],"aligned")

    def test_10_no_free_redraw_or_presentation_execution(self):
        for path,text in ((MARKET,"Move the cart"),(ARCHIVE,"Close the shutter")):
            e=self.engine(path); self.accept(e,text,draw=1); before=e.get_world_state()
            with patch.object(competence,"draw_d6",side_effect=denied):
                r=e.process_command(text); self.assertEqual(r["contextual_action"]["status"],"replayed")
                for _ in range(3): e.get_scene_narration(); e.get_narration(); e.get_narration_context("look")
                r=e.process_command("Shift the cart" if path==MARKET else "Secure the shutter")
                self.assertEqual(r["contextual_action"]["status"],"replayed")
            self.unchanged(e,before)

    def test_11_threshold_off_location_once_and_large_jump(self):
        for hours in (2,7):
            e=self.engine(); e.process_command("go to Side Lane"); e.advance_time(hours)
            self.assertEqual(self.record(e)["conditions"]["position"],"narrow")
            events=[v for v in e.get_history() if v["event_type"]=="material_development"]
            self.assertEqual(len(events),1); self.assertTrue(events[0]["applied"])
            e.advance_time(3); self.assertEqual(len([v for v in e.get_history() if v["event_type"]=="material_development"]),1)
            e.process_command("go to Market Square"); self.assertIn("narrow passage",e.get_narration()["description"])
        e=self.engine(ARCHIVE); e.process_command("go to Corridor"); e.advance_time(2)
        self.assertEqual(self.record(e)["conditions"]["fitting"],"jammed")
        e=self.engine(ARCHIVE); self.accept(e,"Brace the shutter")
        e.advance_time(1); self.assertEqual(self.record(e)["conditions"]["fitting"],"loose")

    def test_12_interruption_retains_preparation_and_cost_without_draw(self):
        e=self.engine(); e.advance_time(1); e.process_command("Adjust the wheel")
        with patch.object(competence,"draw_d6",side_effect=denied): r=e.process_command("yes")
        self.assertEqual(r["contextual_action"]["status"],"interrupted")
        self.assertEqual(self.record(e)["conditions"]["position"],"narrow")
        self.assertEqual(self.record(e)["conditions"]["stability"],"braced")
        self.assertEqual(e.get_world_state()["time"]["elapsed_hours"],2)
        validate_world_state(e.get_world_state(),e.region)

    def test_13_atomic_failure_boundaries(self):
        failures=[(material,"transition"),(game_engine,"add_history_entry"),
                  (material,"changed_conditions"),(game_engine,"validate_world_state"),(game_engine,"build_scene")]
        for module,name in failures:
            e=self.engine(); e.process_command("Move the cart")
            before,scene,focus=e.get_world_state(),e.get_scene_snapshot(),e.get_action_context()
            with patch.object(module,name,side_effect=ValueError("injected")), patch.object(competence,"draw_d6",return_value=6):
                with self.assertRaises(ValueError): e.process_command("yes")
            self.unchanged(e,before,scene,focus)
        e=self.engine(); before,scene,focus=e.get_world_state(),e.get_scene_snapshot(),e.get_action_context()
        with patch.object(material,"advance_candidate",side_effect=ValueError("injected")):
            with self.assertRaises(ValueError): e.advance_time(2)
        self.unchanged(e,before,scene,focus)

    def test_14_save_load_outcomes_and_unsaved_context(self):
        path=ARTIFACTS/"material_roundtrip.json"
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        for fixture,command in ((MARKET,"Move the cart"),(ARCHIVE,"Close the shutter")):
            for draw in (1,3,6):
                e=self.engine(fixture); self.accept(e,command,draw); e.save(str(path))
                saved=build_save_data(e); self.assertEqual(saved["save_version"],1)
                self.assertNotIn("pending",json.dumps(saved)); self.assertNotIn("objective",json.dumps(saved))
                restored=load_game(str(path)); self.assertEqual(build_save_data(restored),saved)
                self.assertEqual(restored.get_action_context(),{"focus":None,"pending":None})
                restored.advance_time(4); restored.save(str(path)); restored=load_game(str(path)); restored.advance_time(1)
                self.assertEqual(len([v for v in restored.get_history() if v["event_type"]=="material_development"]),1)

    def test_15_malformed_state_and_failed_load_preserve_session(self):
        e=self.engine(); self.accept(e,"Force the cart aside",draw=1); good=e.get_world_state()
        variants=[]
        bad=deepcopy(good); bad[material.STATE_KEY]["delivery_cart"]["conditions"]["integrity"]="invented"; variants.append(bad)
        bad=deepcopy(good); bad.pop(material.STATE_KEY); variants.append(bad)
        bad=deepcopy(good); bad["history"][-1]["draw"]=6; variants.append(bad)
        bad=deepcopy(good); bad["history"][0]["risk_authorized"]=False; variants.append(bad)
        bad=deepcopy(good); bad["history"][0]["constraints"]=["preserve_integrity"]; variants.append(bad)
        bad=deepcopy(good); bad["history"][-1]["unexpected"]="forged"; variants.append(bad)
        bad=deepcopy(good); bad["history"][-1]["summary"]="Invented successful result"; variants.append(bad)
        for state in variants:
            with self.assertRaises(ValueError): validate_world_state(state,e.region)
        pending=self.engine(); pending.process_command("Adjust the wheel")
        before,scene,focus=pending.get_world_state(),pending.get_scene_snapshot(),pending.get_action_context()
        path=ARTIFACTS/"material_bad_save.json"; self.addCleanup(lambda: path.unlink(missing_ok=True))
        data=build_save_data(pending); data["world_state"]=variants[0]; path.write_text(json.dumps(data))
        with self.assertRaises(ValueError): pending.load(str(path))
        self.unchanged(pending,before,scene,focus)

    def test_16_default_compatibility_and_reset(self):
        e=self.engine("data/regions/bryn_shander.json")
        self.assertNotIn(material.STATE_KEY,e.get_world_state())
        before=e.get_world_state(); self.assertIsNone(e.process_contextual_action("Move the cart")); self.unchanged(e,before)
        e=self.engine(); self.accept(e,"Brace the cart"); e.process_command("Adjust the wheel"); e.reset()
        self.assertEqual(e.get_action_context(),{"focus":None,"pending":None})
        self.assertEqual(self.record(e)["conditions"]["stability"],"loose")

    def test_17_renamed_ids_and_reordered_declarations(self):
        for fixture,text in ((MARKET,"Move the cart"),(ARCHIVE,"Close the shutter")):
            r=json.loads(Path(fixture).read_text(encoding="utf-8")); item=r["material_targets"][0]
            old=item["target_id"]; item["target_id"]="renamed_target"; item["methods"].reverse()
            for m in item["methods"]: m["method_id"]="renamed_"+m["method_id"]
            r["region_id"]="unrelated"; r["entities"].reverse(); r["locations"].reverse()
            path=ARTIFACTS/"renamed_material_region.json"; path.write_text(json.dumps(r)); self.addCleanup(lambda: path.unlink(missing_ok=True))
            e=self.engine(str(path)); e.process_command("go to "+next(l["name"] for l in r["locations"] if l["location_id"]==item["location_id"]))
            self.accept(e,text); self.assertIn("renamed_target",e.get_world_state()[material.STATE_KEY]); self.assertNotIn(old,e.get_world_state()[material.STATE_KEY])

    def test_18_scene_fidelity_and_adapter_isolation(self):
        for fixture,command in ((MARKET,"Move the cart"),(ARCHIVE,"Close the shutter")):
            e=self.engine(fixture); r=self.accept(e,command); before=e.get_world_state()
            text=e.get_scene_narration()["display_text"]
            self.assertIn("wheel appears crooked" if fixture==MARKET else "closed against the draft",text)
            self.assertEqual(e.get_narration_context("result",accepted_action_id=r["narrative_action_id"])["narrative_projection"]["accepted_action"]["result"],"full")
            def broken(source): source.clear(); raise ValueError("private failure")
            self.assertFalse(e.get_scene_narration(preparer=broken)["accepted"])
            self.unchanged(e,before)
            self.assertIn("cart stands clear" if fixture==MARKET else "shutter is closed",e.get_narration()["description"])

    def test_19_cli_and_declining_are_bounded(self):
        output=StringIO(); path=ARTIFACTS/"material_cli_save.json"; self.addCleanup(lambda: path.unlink(missing_ok=True))
        with patch("builtins.input",side_effect=["look","Assess the cart","Move the cart","yes","look","save","load","decline involvement","quit"]), patch.object(competence,"draw_d6",return_value=6), redirect_stdout(output), patch.object(GameEngine,"get_narration_preview",side_effect=denied):
            play_game.main(region_path=MARKET,save_path=str(path))
        text=output.getvalue(); self.assertIn("Cost: 1 hour",text); self.assertIn("move the cart clear",text)
        self.assertIn("Game loaded",text); self.assertNotIn("quest",text.casefold())
        e=self.engine(); before=e.get_world_state(); e.process_command("decline involvement"); self.unchanged(e,before)

    def test_20_invalid_authored_contracts(self):
        r=json.loads(Path(MARKET).read_text()); variants=[]
        for mutate in (lambda d:d["conditions"]["position"].update(initial="invented"),
                       lambda d:d["methods"][0]["outcomes"]["full"]["effects"].update(unknown="fact"),
                       lambda d:d["methods"][0]["outcomes"]["full"]["effects"].update(integrity="damaged")):
            bad=deepcopy(r); mutate(bad["material_targets"][0]); variants.append(bad)
        for bad in variants:
            with self.assertRaises(ValueError): validate_region(bad)

    def test_21_actor_relocation_interrupts_and_absent_driver_cannot_act(self):
        r=json.loads(Path(MARKET).read_text())
        r["elapsed_time_actor_relocation_effect"]={"effect_id":"helper_leaves","trigger_elapsed_hours":1,
            "actor_entity_id":"delivery_driver","destination_location_id":"side_lane"}
        path=ARTIFACTS/"material_helper_leaves.json"; path.write_text(json.dumps(r)); self.addCleanup(lambda: path.unlink(missing_ok=True))
        e=self.engine(str(path)); e.process_command("Move the cart")
        with patch.object(competence,"draw_d6",side_effect=denied): result=e.process_command("yes")
        self.assertEqual(result["contextual_action"]["status"],"interrupted")
        self.assertEqual(self.record(e)["conditions"]["stability"],"braced")
        self.assertEqual(e.get_world_state()["time"]["elapsed_hours"],1)
        e.advance_time(1)
        self.assertEqual(self.record(e)["conditions"]["position"],"blocked")
        event=next(v for v in e.get_history() if v["event_type"]=="material_development")
        self.assertFalse(event["applied"])
        validate_world_state(e.get_world_state(),e.region)

    def test_22_player_movement_is_not_material_authorization(self):
        e=self.engine(); before=e.get_world_state()
        for text in ("I move around the cart", "I walk through the passage", "Find another route without intervening"):
            r=e.process_command(text)
            self.assertTrue(r["success"])
            self.assertIsNone(e.get_action_context()["pending"])
            self.unchanged(e,before)
        r=e.process_command("go to Side Lane")
        self.assertTrue(r["success"])
        self.assertEqual(self.record(e)["conditions"]["position"],"blocked")

    def test_23_fractional_cost_is_rejected_without_publication(self):
        e=self.engine(); before,scene=e.get_world_state(),e.get_scene_snapshot()
        with self.assertRaises(ValueError): e.advance_time(1.5)
        self.unchanged(e,before,scene)

    def test_24_unsupported_conditions_and_extra_commitments_cannot_disappear(self):
        e=self.engine(); before=e.get_world_state()
        for text in ("Force the cart as long as the cargo stays undamaged", "Move the cart only if nobody objects",
                     "Ask the driver to help and wait two hours", "Move the cart using a crane"):
            r=e.process_command(text)
            self.assertFalse(r["success"])
            self.assertIsNone(e.get_action_context()["pending"])
            self.unchanged(e,before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
