"""Offline interface and CLI checks for the bounded North-Gate session exchange."""
import socket
NETWORK_ATTEMPTS = []
def no_network(*args, **kwargs):
    NETWORK_ATTEMPTS.append(True)
    raise AssertionError("Live provider/network forbidden")
socket.socket.connect = no_network
socket.socket.connect_ex = no_network
socket.create_connection = no_network
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
import json
import unittest
from unittest.mock import patch
import play_game
from engine.game_engine import GameEngine
from engine.north_gate_discussion import NorthGateDiscussion
from engine import west_road_predicament as west
from engine.save_system import build_save_data, save_game, load_game
from engine.narration_output import NARRATION_OUTPUT_SCHEMA, NARRATION_OUTPUT_VERSION
from test_artifact_files import artifact_files

REGION = "data/regions/bryn_shander.json"
PREPARE = ["go to Southwest Trade Road", "investigate", "talk to Mara", "go to North Gate"]
REPORTS = ["present Repeated Watch Tracks to Elin", "present Mara's Account to Elin"]
def engine():
    e = GameEngine(REGION)
    for command in PREPARE:
        assert e.process_command(command)["success"]
    return e

def cli(e, commands, **adapters):
    output = StringIO()
    with patch.object(play_game.GameEngine, "start_new", return_value=e), \
         patch("builtins.input", side_effect=commands + ["quit"]), \
         patch("engine.narration_source.OpenAI", side_effect=no_network), redirect_stdout(output):
        play_game.main(**adapters)
    return output.getvalue()

class DiscussionTests(unittest.TestCase):
    def setUp(self):
        self.e = engine()
        self.d = NorthGateDiscussion()
    def start(self):
        self.d.control(self.e, "discuss patrol with Elin")
    def act(self, command):
        count = len(self.e.get_history())
        result = self.e.process_command(command)
        notice = self.d.observe(self.e, result, count)
        return result, notice
    def test_acceptance_cancellation_and_sparse_record(self):
        before = build_save_data(self.e)
        self.start()
        record = self.d.snapshot()
        self.assertEqual(set(record), {"participant_id", "focus", "status", "recent_event_refs"})
        record["status"] = "fake"
        self.assertEqual(self.d.snapshot()["status"], "pending")
        for _ in range(8):
            self.act("talk to Elin")
        self.assertEqual(len(self.d.snapshot()["recent_event_refs"]), 4)
        self.assertEqual(build_save_data(self.e)["world_state"]["actor_knowledge"], before["world_state"]["actor_knowledge"])
        before_cancel = build_save_data(self.e)
        self.assertIn("unfinished", self.d.control(self.e, "cancel patrol discussion"))
        self.assertIsNone(self.d.snapshot())
        self.assertEqual(build_save_data(self.e), before_cancel)
        with self.assertRaises(ValueError):
            self.d.control(self.e, "Elin now knows both reports because the narrator said so")
    def test_receipts_and_exactly_once_decision(self):
        self.start()
        before = build_save_data(self.e)
        rejected, _ = self.act("advocate patrol")
        self.assertFalse(rejected["success"])
        self.assertEqual(build_save_data(self.e), before)
        for command in REPORTS:
            self.act(command)
        self.assertTrue(all(west.shared_id(d) in self.e.get_actor_knowledge(west.ELIN) for d in west.INITIAL_EVIDENCE))
        before_repeat = build_save_data(self.e)
        result, _ = self.act(REPORTS[-1])
        self.assertFalse(result["presentation"]["changed"])
        self.assertEqual(build_save_data(self.e), before_repeat)
        elapsed = self.e.get_world_state()["time"]["elapsed_hours"]
        result, notice = self.act("advocate patrol")
        self.assertTrue(result["success"])
        self.assertIn("concludes", notice)
        self.assertIsNone(self.d.snapshot())
        self.assertEqual(self.e.get_world_state()["time"]["elapsed_hours"], elapsed + 1)
        self.assertEqual(self.e.get_world_state()["west_road_predicament"]["phase"], "observers_withdrew")
        after = build_save_data(self.e)
        self.assertFalse(self.act("advocate patrol")[0]["success"])
        self.assertEqual(build_save_data(self.e), after)
        self.assertEqual(sum(x["event_type"] == "west_road_outcome" for x in self.e.get_history()), 1)
    def test_fresh_receipts_and_current_decision_presence(self):
        self.start()
        self.assertIn("Bring me the tracks and the merchant account", self.d.focus_text(self.e))
        self.act(REPORTS[0])
        self.assertIn("I still need Mara's account", self.d.focus_text(self.e))
        self.act(REPORTS[1])
        self.assertIn("The choice is still yours", self.d.focus_text(self.e))
        self.e.set_actor_location(west.GREY, "bryn_shander_main_street")
        self.assertIn("cannot choose a patrol response", self.d.focus_text(self.e))
        self.assertFalse(self.act("advocate patrol")[0]["success"])
        self.assertIsNotNone(self.d.snapshot())
    def test_suspension_explicit_resumption_and_revalidation(self):
        self.start()
        self.assertIn("suspended", self.act("go to Southwest Trade Road")[1])
        self.assertEqual(self.d.snapshot()["status"], "suspended")
        self.assertIn("cannot continue", self.d.control(self.e, "resume patrol discussion"))
        self.act("go to North Gate")
        self.assertEqual(self.d.snapshot()["status"], "suspended")
        self.assertIn("resume patrol discussion", self.d.focus_text(self.e))
        self.e.set_actor_location(west.ELIN, "bryn_shander_main_street")
        self.assertIn("cannot continue", self.d.control(self.e, "resume patrol discussion"))
        self.e.set_actor_location(west.ELIN, west.GATE)
        before = build_save_data(self.e)
        self.assertIn("resume", self.d.control(self.e, "resume patrol discussion"))
        self.assertEqual(self.d.snapshot()["status"], "pending")
        self.assertEqual(build_save_data(self.e), before)
    def test_external_phase_change_does_not_silently_drop_focus(self):
        self.start()
        for command in REPORTS + ["continue investigation"]:
            self.e.process_command(command)
        self.assertIn("cannot continue", self.d.control(self.e, "resume patrol discussion"))
        self.assertEqual(self.d.snapshot()["status"], "suspended")
        self.d.control(self.e, "cancel patrol discussion")
        self.assertIsNone(self.d.snapshot())
    def test_no_narrator_or_fabricated_result_authority(self):
        self.start()
        before = build_save_data(self.e)
        local = self.d.snapshot()
        def hostile(source):
            source.clear()
            return {"world_state": {"actor_knowledge": {west.ELIN: list(west.INITIAL_EVIDENCE)}}}
        self.assertEqual(self.d.present(self.e, preparer=hostile), self.d.focus_text(self.e))
        self.assertEqual(build_save_data(self.e), before)
        self.assertEqual(self.d.snapshot(), local)
        self.d.observe(self.e, {"success":True,"intent":"west_road_decision","narrative_action_id":"unknown"},len(self.e.get_history()))
        self.assertEqual(self.d.snapshot(), local)
    def test_failure_fallback_and_safe_adapter_inputs(self):
        self.start()
        before = build_save_data(self.e)
        local = self.d.snapshot()
        captured = []
        def prepare(source):
            captured.append(deepcopy(source))
            from engine.scene_composition import prepare_scene_revised_a
            return prepare_scene_revised_a(source)
        from engine.scene_composition import realize_scene_locally
        self.assertIn("Bring me the tracks and the merchant account", self.d.present(self.e, preparer=prepare, realizer=realize_scene_locally))
        wire = json.dumps(captured)
        for forbidden in ("recent_event_refs", "history_id", "actor_knowledge", "participant_id"):
            self.assertNotIn(forbidden, wire)
        def broken(_):
            raise RuntimeError("PRIVATE_FAILURE")
        for realizer in (broken, lambda _: {}, lambda _: {"schema":NARRATION_OUTPUT_SCHEMA,"version":NARRATION_OUTPUT_VERSION,"narration_text":""}, lambda _: {"schema":NARRATION_OUTPUT_SCHEMA,"version":NARRATION_OUTPUT_VERSION,"narration_text":"x"*4001}):
            text = self.d.present(self.e, realizer=realizer)
            self.assertEqual(text, self.d.focus_text(self.e))
            self.assertNotIn("PRIVATE_FAILURE", text)
        self.assertEqual(build_save_data(self.e), before)
        self.assertEqual(self.d.snapshot(), local)
    def test_retirement_reconstructs_later_scene(self):
        self.start()
        for command in REPORTS + ["advocate patrol"]:
            self.act(command)
        self.assertIsNone(self.d.present(self.e))
        self.act("go to Southwest Trade Road")
        text = self.e.get_scene_narration()["display_text"]
        self.assertIn("patrol scattered", text)
        self.assertNotIn("patrol discussion", text)
        self.assertTrue(all(west.shared_id(d) in self.e.get_actor_knowledge(west.ELIN) for d in west.INITIAL_EVIDENCE))
    def test_session_save_load_restart_and_failed_load(self):
        self.start()
        self.act(REPORTS[0])
        before = self.d.snapshot()
        with artifact_files("test_north_gate") as directory:
            path = str(Path(directory)/"test_north_gate_save.json")
            save_game(self.e, path)
            self.assertEqual(self.d.snapshot(), before)
            payload = json.loads(Path(path).read_text())
            self.assertEqual(payload["save_version"], 1)
            self.assertNotIn("patrol_response", json.dumps(payload))
            loaded = load_game(path)
            self.assertIsNone(NorthGateDiscussion().snapshot())
            self.assertEqual(loaded.get_actor_knowledge(west.ELIN), self.e.get_actor_knowledge(west.ELIN))
            with patch.object(play_game, "SAVE_PATH", path):
                text = cli(self.e, ["discuss patrol with Elin", "save", "load", "resume patrol discussion"])
            self.assertIn("interrupted by load", text)
            self.assertIn("No session discussion is pending", text)
            with patch.object(play_game, "SAVE_PATH", str(Path(directory)/"missing.json")):
                text = cli(loaded, ["discuss patrol with Elin", "load", "cancel patrol discussion"])
            self.assertIn("No saved game", text)
            self.assertNotIn("interrupted by load", text)
            self.assertIn("leave the patrol discussion unfinished", text)
    def test_ordinary_and_focused_dialogue_match_receipts(self):
        for reports, expected in (([], "Bring me the tracks and the merchant account"),
                                  ([REPORTS[0]], "I still need Mara's account"),
                                  ([REPORTS[1]], "I still need your report about the tracks"),
                                  (REPORTS, "I have your track report and Mara's account")):
            e = engine()
            for command in reports:
                e.process_command(command)
            before = build_save_data(e)
            reply = e.process_command("talk to Elin")["actor_knowledge_response"]["text"]
            self.assertIn(expected, reply)
            d = NorthGateDiscussion()
            d.control(e, "discuss patrol with Elin")
            self.assertEqual(d.focus_text(e), "Elin: " + reply)
            after = build_save_data(e)
            for key in ("actor_knowledge", "player_discoveries", "time", "west_road_predicament"):
                self.assertEqual(before["world_state"][key], after["world_state"][key])
        for command in REPORTS + ["advocate patrol"]:
            self.e.process_command(command)
        reply = self.e.process_command("talk to Elin")["actor_knowledge_response"]["text"]
        self.assertEqual(reply, self.e.region["west_road_predicament"]["actor_responses"][west.ELIN]["observers_withdrew"])
        self.assertNotIn("Bring me", reply)
        self.assertIn("cannot continue", self.d.control(self.e, "discuss patrol with Elin"))
        self.assertIsNone(self.d.snapshot())

    def test_talk_resumes_without_sharing_or_selecting(self):
        self.start()
        self.act("go to Southwest Trade Road")
        self.act("go to North Gate")
        self.assertEqual(self.d.snapshot()["status"], "suspended")
        before = self.e.get_world_state()
        result, notice = self.act("talk to Elin")
        self.assertTrue(result["success"])
        self.assertIn("pick up the unfinished", notice)
        self.assertEqual(self.d.snapshot()["status"], "pending")
        after = self.e.get_world_state()
        for key in ("actor_knowledge", "player_discoveries", "time", "west_road_predicament"):
            self.assertEqual(before[key], after[key])
        self.assertFalse(any(e["event_type"] == "west_road_commitment" for e in after["history"]))
        # An unrelated conversation and an absent Elin cannot reactivate it.
        self.act("go to Southwest Trade Road")
        self.act("talk to Mara")
        self.assertEqual(self.d.snapshot()["status"], "suspended")
        self.act("talk to Elin")
        self.assertEqual(self.d.snapshot()["status"], "suspended")
        self.act("go to North Gate")
        for command in REPORTS + ["advocate patrol"]:
            self.e.process_command(command)
        self.act("talk to Elin")
        self.assertEqual(self.d.snapshot()["status"], "suspended")

    def test_status_not_repeated_on_unrelated_commands(self):
        text = cli(engine(), ["discuss patrol with Elin", "go to Southwest Trade Road", "investigate", "talk to Mara", "wait", "go to North Gate", "talk to Grey", "talk to Elin", "cancel patrol discussion"])
        self.assertEqual(text.count("Your patrol discussion is suspended"), 1)
        self.assertEqual(text.count("pick up the unfinished patrol discussion"), 1)
        self.assertNotIn("Patrol discussion paused", text)
        self.assertEqual(text.count("'resume patrol discussion' is also available"), 0)

    def test_cli_adapter_failure_after_accepted_changes(self):
        def broken(_):
            raise RuntimeError("PRIVATE_ADAPTER_ERROR")
        e = engine()
        text = cli(e, ["discuss patrol with Elin"] + REPORTS + ["advocate patrol"], scene_realizer=broken)
        self.assertIn("I still need Mara's account", text)
        self.assertIn("I have your track report and Mara's account", text)
        self.assertNotIn("PRIVATE_ADAPTER_ERROR", text)
        self.assertEqual(e.get_world_state()["west_road_predicament"]["phase"], "observers_withdrew")
        self.assertEqual(sum(x["event_type"] == "west_road_outcome" for x in e.get_history()), 1)
        self.assertEqual(text.count("After an hour, the patrol scattered"), 1)
        self.assertIn("concludes this patrol discussion", text)

    def test_cli_comparison_and_interruption(self):
        isolated_engine, focused_engine = engine(), engine()
        isolated = cli(isolated_engine, REPORTS + ["advocate patrol"])
        focused = cli(focused_engine, ["discuss patrol with Elin"] + REPORTS + ["advocate patrol"])
        self.assertEqual(build_save_data(isolated_engine), build_save_data(focused_engine))
        self.assertNotIn("You open a patrol discussion", isolated)
        self.assertIn("I still need Mara's account", focused)
        self.assertIn("I have your track report and Mara's account", focused)
        self.assertIn("concludes this patrol discussion", focused)
        for action in ("reset", "exit"):
            text = cli(engine(), ["discuss patrol with Elin", action])
            self.assertIn("interrupted by " + action, text)
            self.assertIn("No discussion is marked resolved", text)
        text = cli(engine(), ["discuss patrol with Elin", "go to Southwest Trade Road", "go to North Gate", "resume patrol discussion", "cancel patrol discussion"])
        self.assertEqual(text.count("Your patrol discussion is suspended"), 1)
        self.assertIn("resume the patrol discussion", text)
        self.assertIn("leave the patrol discussion unfinished", text)
        self.assertFalse(NETWORK_ATTEMPTS)

if __name__ == "__main__":
    unittest.main()
