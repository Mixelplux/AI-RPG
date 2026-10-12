"""Exact owner smoke through production CLI, plus semantic authorization checks."""
from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import replace
from io import StringIO
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

import play_game
from engine import character_competence as competence, game_engine, material_state
from engine.game_engine import GameEngine
from engine.contextual_action import interpret
from engine.save_system import build_save_data

MARKET = "data/regions/market_passage_v1.json"
ARCHIVE = "test_fixtures/archive_shutter.json"
OUTPUT = Path(".artifacts/contextual_action_owner_correction")
OWNER_SEQUENCE = ["ask tessa if she needs help", "talk to tessa",
                  "ask driver if they need help", "help driver", "confirm",
                  "continue with help", "shift the cart", "move the cart aside"]


def denied(*args, **kwargs):
    raise AssertionError("No live provider or network during correction")


def run_cli(commands, *, draw=6, region_path=MARKET):
    """Observe ordinary CLI routing; actual engine construction/execution remain."""
    engines, trace = [], []
    original_start = GameEngine.start_new
    original_process = GameEngine.process_command
    inputs = iter([*commands, "quit"])
    output = StringIO()
    def start(path):
        engine = original_start(path)
        engines.append(engine)
        return engine
    def process(engine, raw):
        before = engine.get_world_state()
        result = original_process(engine, raw)
        after = engine.get_world_state()
        trace.append({"input": raw, "result": deepcopy(result),
                      "before_material": before[material_state.STATE_KEY],
                      "after_material": after[material_state.STATE_KEY],
                      "elapsed_hours": after["time"]["elapsed_hours"],
                      "outcomes": sum(e["event_type"] == "material_outcome" for e in after["history"])})
        return result
    def read(prompt):
        raw = next(inputs)
        print(prompt + raw)
        return raw
    with patch.object(GameEngine, "start_new", side_effect=start), \
         patch.object(GameEngine, "process_command", new=process), \
         patch("builtins.input", side_effect=read), \
         patch.object(competence, "draw_d6", return_value=draw,
                      side_effect=draw if isinstance(draw, (tuple, list)) else None) as rng, \
         patch.object(GameEngine, "get_narration_preview", side_effect=denied), \
         patch("engine.narration_source.OpenAI", side_effect=denied), \
         patch.object(socket.socket, "connect", side_effect=denied), \
         patch("socket.create_connection", side_effect=denied), redirect_stdout(output):
        play_game.main(region_path=region_path, save_path=str(OUTPUT / "unused_cli_save.json"))
    return engines[0], trace, output.getvalue(), rng.call_count


class OwnerCorrection(unittest.TestCase):
    def setUp(self):
        self.guards = [patch("engine.narration_source.OpenAI", side_effect=denied),
                       patch.object(socket.socket,"connect",side_effect=denied),
                       patch("socket.create_connection",side_effect=denied)]
        for guard in self.guards: guard.start()
        self.addCleanup(lambda: [g.stop() for g in reversed(self.guards)])

    def record(self, engine):
        return next(iter(engine.get_world_state()[material_state.STATE_KEY].values()))

    def test_01_exact_owner_sequence_through_cli(self):
        engine, trace, text, draws = run_cli(OWNER_SEQUENCE)
        for row in (trace[0],trace[2]):
            self.assertEqual(row["result"]["contextual_action"]["status"],"answered")
            self.assertEqual(row["before_material"],row["after_material"])
        self.assertTrue(trace[1]["result"]["success"])
        self.assertEqual(trace[1]["result"]["target_resolution"]["identifier"],"delivery_driver")
        self.assertEqual(trace[3]["result"]["contextual_action"]["status"],"authorization_required")
        self.assertEqual(trace[4]["result"]["contextual_action"]["status"],"accepted")
        self.assertEqual(draws,1)
        self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"],1)
        self.assertTrue(all(row["outcomes"] == 1 for row in trace[4:]))
        self.assertEqual(self.record(engine)["conditions"]["position"],"clear")
        self.assertEqual(self.record(engine)["conditions"]["integrity"],"intact")
        self.assertNotIn("Name one material target",text)
        self.assertNotIn("No matching target",text)
        OUTPUT.mkdir(exist_ok=True)
        (OUTPUT/"corrected_owner_cli.txt").write_text(text,encoding="utf-8")
        (OUTPUT/"corrected_owner_trace.json").write_text(json.dumps(trace,indent=2),encoding="utf-8")

    def test_02_named_actor_role_and_renamed_actor(self):
        engine=GameEngine(MARKET)
        for target in ("Tessa","Tessa, Delivery Driver","delivery driver","driver","the driver"):
            self.assertEqual(engine.resolve_target(target)["identifier"],"delivery_driver")
        for raw in ("talk to tessa","talk to the driver","talk to delivery driver"):
            row=engine.process_command(raw)
            self.assertTrue(row["success"])
            self.assertEqual(row["target_resolution"]["identifier"],"delivery_driver")
        engine.region["entities"][0]["name"]="Rina Voss, Delivery Driver"
        for raw in ("ask rina if she needs help","ask rina voss whether she needs assistance","does the driver need help?"):
            before=engine.get_world_state()
            row=engine.process_command(raw)
            self.assertEqual(row["contextual_action"]["status"],"answered")
            self.assertEqual(engine.get_world_state(),before)

    def test_03_questions_offers_and_physical_commitments(self):
        questions=("ask tessa if she needs help","ask driver if they need help",
                   "does tessa need assistance?","ask tessa whether she could use a hand")
        for raw in questions:
            engine=GameEngine(MARKET); before=engine.get_world_state()
            row=engine.process_command(raw)
            self.assertEqual(row["contextual_action"]["status"],"answered",raw)
            self.assertEqual(engine.get_world_state(),before)
            self.assertIsNone(engine.get_action_context()["pending"])
        for raw in ("offer to help tessa","ask tessa to help","request the driver's cooperation"):
            engine=GameEngine(MARKET); row=engine.process_command(raw)
            self.assertEqual(row["contextual_action"]["outcome"],"cooperation",raw)
            self.assertEqual(self.record(engine)["cooperation"],"willing")
            self.assertEqual(self.record(engine)["conditions"]["position"],"blocked")
            self.assertEqual(engine.get_world_state()["time"]["elapsed_hours"],0)
        engine=GameEngine(MARKET)
        self.assertEqual(engine.process_command("help tessa")["contextual_action"]["status"],"authorization_required")
        self.assertEqual(self.record(engine)["cooperation"],"unasked")

    def test_04_confirmations_and_equivalent_commitments_execute_once(self):
        for raw in ("confirm","yes, do it","confirm the proposal","go ahead",
                    "continue with help","shift the cart","move the cart aside","help tessa"):
            engine=GameEngine(MARKET)
            engine.process_command("Help get the cart out of the passage without damaging the cargo")
            with patch.object(competence,"draw_d6",return_value=6) as rng:
                row=engine.process_command(raw)
            self.assertEqual(row["contextual_action"]["status"],"accepted",raw)
            self.assertEqual(rng.call_count,1)
            prep=next(e for e in engine.get_history() if e["event_type"]=="material_preparation")
            self.assertIn("preserve_integrity",prep["constraints"])
            before=engine.get_world_state()
            with patch.object(competence,"draw_d6",side_effect=denied):
                self.assertFalse(engine.process_command("confirm")["success"])
                self.assertFalse(engine.process_command("yes, do it")["success"])
            self.assertEqual(engine.get_world_state(),before)

    def test_05_changed_method_constraints_and_ambiguous_confirmation(self):
        for raw in ("maybe shift the cart","confirm or cancel","continue","confirm?",
                    "yes, do it but don't damage the cargo","shift the cart without talking"):
            engine=GameEngine(MARKET); engine.process_command("Force the cart aside alone")
            before=engine.get_world_state()
            with patch.object(competence,"draw_d6",side_effect=denied): row=engine.process_command(raw)
            self.assertFalse(row["success"],raw)
            self.assertEqual(engine.get_world_state(),before)
        engine=GameEngine(MARKET); engine.process_command("Move the cart without damaging cargo")
        before=engine.get_world_state(); row=engine.process_command("Force the cart aside alone")
        self.assertEqual(row["contextual_action"]["status"],"constraint_conflict")
        self.assertEqual(engine.get_world_state(),before)

    def test_06_stale_equivalent_request_and_confirmation(self):
        for raw in ("confirm","shift the cart","continue with help"):
            engine=GameEngine(MARKET); engine.process_command("help driver"); engine.advance_time(1)
            before=engine.get_world_state()
            with patch.object(competence,"draw_d6",side_effect=denied): row=engine.process_command(raw)
            self.assertEqual(row["contextual_action"]["status"],"stale_authorization")
            self.assertEqual(engine.get_world_state(),before)

    def test_07_equivalent_confirmation_rollback_and_structured_safety(self):
        engine=GameEngine(MARKET); engine.process_command("help tessa")
        before,scene,focus=engine.get_world_state(),engine.get_scene_snapshot(),engine.get_action_context()
        with patch.object(game_engine,"build_scene",side_effect=ValueError("injected")), patch.object(competence,"draw_d6",return_value=6):
            with self.assertRaises(ValueError): engine.process_command("shift the cart")
        self.assertEqual(engine.get_world_state(),before)
        self.assertEqual(engine.get_scene_snapshot(),scene)
        self.assertEqual(engine.get_action_context(),focus)
        frame=interpret(engine,"Move the cart")
        row=engine.process_contextual_action(frame=frame)
        self.assertEqual(row["contextual_action"]["status"],"authorization_required")
        self.assertEqual(engine.get_world_state(),before)

    def test_08_archive_confirmation_and_mismatched_help_reference(self):
        engine=GameEngine(ARCHIVE); engine.process_command("Close the shutter")
        before=engine.get_world_state()
        self.assertFalse(engine.process_command("continue with help")["success"])
        self.assertEqual(engine.get_world_state(),before)
        engine=GameEngine(ARCHIVE); engine.process_command("Close the shutter")
        with patch.object(competence,"draw_d6",return_value=6): row=engine.process_command("shut the shutter")
        self.assertEqual(row["contextual_action"]["status"],"accepted")
        self.assertEqual(self.record(engine)["conditions"]["position"],"closed")

    def test_09_ambiguous_roles_named_disambiguation_and_wrong_helper(self):
        OUTPUT.mkdir(exist_ok=True)
        data=json.loads(Path(MARKET).read_text(encoding="utf-8"))
        other=deepcopy(data["entities"][0]); other.update(entity_id="other_driver",name="Mila, Delivery Driver")
        data["entities"].append(other)
        path=OUTPUT/"ambiguous_actor_fixture.json"
        path.write_text(json.dumps(data),encoding="utf-8")
        engine=GameEngine(str(path)); before=engine.get_world_state()
        self.assertEqual(engine.resolve_target("driver")["status"],"ambiguous")
        for raw in ("help driver","ask driver if they need help","help tessa and mila", "shift the cart with mila", "push tessa"):
            row=engine.process_command(raw)
            self.assertFalse(row["success"],raw)
            self.assertEqual(engine.get_world_state(),before)
        self.assertEqual(engine.process_command("help tessa the driver")["contextual_action"]["status"],"authorization_required")
        with patch.object(competence,"draw_d6",return_value=6):
            row=engine.process_command("shift the cart with tessa")
        self.assertEqual(row["contextual_action"]["status"],"accepted")

    def test_10_read_only_question_context_and_new_risk_revalidation(self):
        engine=GameEngine(MARKET); engine.process_command("ask tessa if she needs help")
        self.assertEqual(engine.process_command("help her")["contextual_action"]["status"],"authorization_required")
        before=engine.get_world_state()
        self.assertEqual(engine.process_command("ask driver if they need help")["contextual_action"]["status"],"answered")
        self.assertEqual(engine.get_world_state(),before)
        with patch.object(competence,"draw_d6",return_value=6):
            self.assertEqual(engine.process_command("confirm")["contextual_action"]["status"],"accepted")
        engine=GameEngine(MARKET); engine.process_command("force the cart aside alone")
        before=engine.get_world_state()
        method=next(m for m in engine.region["material_targets"][0]["methods"] if m["method_id"]=="force_shift")
        method["risk"] += " Newly disclosed material danger."
        with patch.object(competence,"draw_d6",side_effect=denied):
            row=engine.process_command("confirm")
        self.assertEqual(row["contextual_action"]["status"],"stale_authorization")
        self.assertEqual(engine.get_world_state(),before)

    def test_11_added_constraints_and_different_method_need_fresh_disclosure(self):
        engine=GameEngine(MARKET); engine.process_command("help driver")
        with patch.object(competence,"draw_d6",return_value=6):
            row=engine.process_command("confirm without damaging the cargo")
        self.assertEqual(row["contextual_action"]["status"],"accepted")
        prep=next(e for e in engine.get_history() if e["event_type"]=="material_preparation")
        self.assertEqual(prep["constraints"],["preserve_integrity"])
        engine=GameEngine(MARKET); engine.process_command("help driver")
        before=engine.get_world_state()
        row=engine.process_command("force the cart aside alone")
        self.assertEqual(row["contextual_action"]["status"],"authorization_required")
        self.assertIn("damage the cargo",row["message"])
        self.assertEqual(engine.get_world_state(),before)
        self.assertFalse(engine.process_command("continue with help")["success"])
        self.assertEqual(engine.get_world_state(),before)

    def test_12_question_subject_and_constraint_context_are_not_keyword_shortcuts(self):
        engine=GameEngine(MARKET)
        row=engine.process_command("shift the cart because tessa needs help")
        self.assertEqual(row["contextual_action"]["status"],"authorization_required")
        engine.process_command("cancel action")
        self.assertFalse(engine.process_command("shift the cart if it is safe")["success"])
        engine.process_command("force the cart aside alone")
        before=engine.get_world_state()
        self.assertEqual(engine.process_command("confirm without damaging cargo")["contextual_action"]["status"],"constraint_conflict")
        self.assertEqual(engine.process_command("force the cart aside alone")["contextual_action"]["status"],"constraint_conflict")
        self.assertEqual(engine.get_world_state(),before)
        engine.process_command("cancel action")
        self.assertEqual(engine.process_command("force the cart aside alone")["contextual_action"]["status"],"authorization_required")

    def test_13_existing_generic_role_ambiguity_is_preserved(self):
        engine=GameEngine("test_fixtures/bryn_shander_legacy.json")
        before=engine.get_world_state()
        row=engine.process_command("talk to guard")
        self.assertFalse(row["success"])
        self.assertEqual(row["target_resolution"]["status"],"ambiguous")
        self.assertEqual(engine.get_world_state(),before)

    def test_14_full_personal_names_match_the_canonical_resolver(self):
        OUTPUT.mkdir(exist_ok=True)
        data=json.loads(Path(MARKET).read_text(encoding="utf-8"))
        data["entities"][0]["name"]="Rina Voss, Delivery Driver"
        other=deepcopy(data["entities"][0]); other.update(entity_id="other_driver",name="Rina Vale, Delivery Driver")
        data["entities"].append(other)
        path=OUTPUT/"shared_first_name_fixture.json"; path.write_text(json.dumps(data),encoding="utf-8")
        engine=GameEngine(str(path)); before=engine.get_world_state()
        self.assertEqual(engine.resolve_target("Rina Voss")["identifier"],"delivery_driver")
        self.assertEqual(engine.process_command("ask rina voss if she needs help")["contextual_action"]["status"],"answered")
        for text in ("ask rina if she needs help","help rina voss and rina vale"):
            self.assertFalse(engine.process_command(text)["success"])
            self.assertEqual(engine.get_world_state(),before)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["--capture-before"]:
        OUTPUT.mkdir(exist_ok=True)
        engine, trace, text, draws = run_cli(OWNER_SEQUENCE)
        (OUTPUT/"before_owner_cli.txt").write_text(text,encoding="utf-8")
        (OUTPUT/"before_owner_trace.json").write_text(json.dumps(trace,indent=2),encoding="utf-8")
        for row in trace: print(row["input"]+" -> "+row["result"]["message"])
        print("Material outcomes:",trace[-1]["outcomes"],"Draws:",draws)
    else:
        unittest.main(verbosity=2)
