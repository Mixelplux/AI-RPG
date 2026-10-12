"""Offline milestone checks; redirect historical evidence into this worktree.

Uses the repository's standalone scripts/unittest cases, not pytest. Each script
has an isolated process and a network guard. Never write prior acceptance evidence.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
TESTS = (
    "test_contextual_action_consequence.py", "test_contextual_action_owner_correction.py", "test_contextual_action_structural_correction.py", "test_contextual_investigation.py",
    "test_character_competence.py", "test_north_gate_discussion.py",
    "test_scene_construction.py", "test_player_scene_route.py",
    "test_interaction_kernel.py", "test_interaction_history.py", "test_world_update.py",
    "test_history_query.py", "test_history_context.py", "test_save_load.py",
    "test_navigation_projection.py", "test_current_scene_projection.py",
    "test_contextual_action_projection.py", "test_time_actor_relocation.py",
    "test_time_pressure_effect.py", "test_time_evidence_trace_effect.py",
    "test_elapsed_time_transition_observation.py", "test_one_hour_west_road_exit_traversal.py",
    "test_west_road_predicament.py", "test_west_road_market_theft.py",
    "test_west_road_presentation.py", "test_west_road_scene_relevance.py",
    "test_actor_location.py", "test_actor_knowledge.py", "test_actor_knowledge_response.py",
    "test_conversation_actor_knowledge.py", "test_discovery.py",
    "test_scene_context.py", "test_narration_context.py", "test_narration_request.py",
    "test_narration_prompt.py", "test_narration_input_foundation.py", "test_resolved_narration.py",
)


def run_worker(name, output):
    attempts = []
    def denied(*args, **kwargs):
        attempts.append(True)
        raise AssertionError("Live network forbidden during local verification")
    socket.create_connection = denied
    socket.socket.connect = denied
    socket.socket.connect_ex = denied
    sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location(Path(name).stem, ROOT / name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if hasattr(module, "EVIDENCE"):
        module.EVIDENCE = output / "investigation"
    if hasattr(module, "ARTIFACTS"):
        module.ARTIFACTS = output / "material"
    if hasattr(module, "OUTPUT"):
        module.OUTPUT = output / Path(name).stem
        module.OUTPUT.mkdir(parents=True, exist_ok=True)
    artifact_path = getattr(module, "PATH", None)
    if isinstance(artifact_path, Path) and artifact_path.parent == Path(".artifacts"):
        module.PATH = output / artifact_path.name
    if callable(getattr(module, "get_test_output_path", None)):
        # The legacy save regression otherwise overwrites fixed prior outputs.
        module.get_test_output_path = lambda name: output / ("save_load_regression_" + name)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    if suite.countTestCases():
        passed = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    elif callable(getattr(module, "main", None)):
        module.main()
        passed = True
    else:
        functions = [v for k, v in vars(module).items() if k.startswith("test_") and callable(v)]
        if not functions:
            # Some early repository scripts execute their checks at import.
            print("Completed legacy top-level script (no assertion count): " + name)
        for function in functions: function()
        passed = True
    if attempts:
        raise AssertionError("A verification script attempted live network access")
    return 0 if passed else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tests", nargs="*", choices=TESTS)
    parser.add_argument("--worker", choices=TESTS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = (ROOT / (args.output or Path(".artifacts/contextual_action_verification"))).resolve()
    if not output.is_relative_to((ROOT / ".artifacts").resolve()):
        parser.error("Verification output must stay under this worktree's .artifacts.")
    output.mkdir(parents=True, exist_ok=True)
    if args.worker:
        return run_worker(args.worker, output)
    results = []
    for name in args.tests or TESTS:
        completed = subprocess.run([sys.executable, "-B", __file__, "--worker", name, "--output", str(output)],
                                   cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (output / (Path(name).stem + ".log")).write_text(completed.stdout + completed.stderr, encoding="utf-8")
        results.append({"script": name, "status": "passed" if completed.returncode == 0 else "failed"})
        print(results[-1]["status"].upper() + ": " + name, flush=True)
        if completed.returncode:
            print("\n".join((completed.stdout + completed.stderr).splitlines()[-35:]), flush=True)
            break
    (output / "summary.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if len(results) == len(args.tests or TESTS) and all(r["status"] == "passed" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
