# Project Structure

This document provides a clean, human-readable map of the AI Narrative RPG Engine project.

Generated folders such as `.venv/`, `__pycache__/`, and temporary ZIP archives are intentionally excluded from the project map. They should not be treated as part of the source architecture.

## Root Structure

```text
AI RPG/
├── .vscode/
├── chat_history/
├── data/
│   └── regions/
├── docs/
│   └── schemas/
├── engine/
├── .gitignore
├── AI RPG.code-workspace
├── play_game.py
├── requirements.txt
├── run_scene_test.py
├── test_interaction_kernel.py
└── test_world_update.py
```

## Directory Purposes

### `.vscode/`

Project-specific Visual Studio Code configuration.

Expected contents:

```text
.vscode/
├── launch.json
├── settings.json
└── tasks.json
```

Purpose:

- Defines debug launch targets.
- Defines repeatable project tasks.
- Stores workspace-level editor and Python settings.

This folder is part of the project and should be committed to Git.

---

### `chat_history/`

Optional local archive of project-related chat notes or exports.

Purpose:

- Stores reference material from development discussions.
- Not required by the engine at runtime.
- May be ignored by Git if it becomes large or personal.

---

### `data/`

Static data used by the engine.

```text
data/
└── regions/
    ├── bryn_shander.json
    ├── bryn_shander_v0_2.json
    └── bryn_shander_v0_3.json
```

Purpose:

- Stores Region Packs.
- Defines immutable world seed data such as locations, entities, factions, initial weather, and initial time.
- Runtime changes should not be written back into these files during gameplay.

---

### `docs/`

Project documentation and design records.

```text
docs/
├── api_reference.md
├── architecture.md
├── current_sprint.md
├── decisions.md
├── development_workflow.md
├── future_design.md
├── project_constitution.md
├── project_structure.md
├── roadmap.md
├── simulation_principles.md
├── sprint_log.md
└── schemas/
```

Purpose:

- Serves as the authoritative project design source.
- Records architecture, workflow, decisions, sprint status, future ideas, and simulation principles.
- Should be updated at the end of each sprint.

---

### `docs/schemas/`

Schema documentation for major engine data structures.

Expected contents include:

```text
docs/schemas/
├── character_schema.md
├── interaction_schema.md
├── narrator_output_schema.md
├── player_perception_schema.md
├── region_pack_schema.md
├── savegame_schema.md
└── scene_snapshot_schema.md
```

Purpose:

- Documents the shape and ownership of project data.
- Helps prevent drift between code and design intent.
- Should be updated when a data structure changes.

---

### `engine/`

Core Python engine modules.

```text
engine/
├── __init__.py
├── game_engine.py
├── interaction_kernel.py
├── llm_prompt_builder.py
├── perception_builder.py
├── region_validator.py
├── scene_loader.py
├── scene_narrator.py
├── world_state.py
└── world_update.py
```

Purpose:

- Contains the runtime engine code.
- Keeps simulation, projection, perception, narration, and orchestration separated.
- Should remain modular and incremental.

Current architectural ownership:

```text
Region Pack
    ↓
World State
    ↓
Scene Loader
    ↓
Scene Snapshot
    ↓
Player Perception
    ↓
Narration
```

---

### Root Python Files

```text
play_game.py
run_scene_test.py
test_interaction_kernel.py
test_world_update.py
```

Purpose:

- `play_game.py` runs the current playable command-line loop.
- `run_scene_test.py` runs scene, perception, narration, and prompt tests.
- `test_interaction_kernel.py` tests player input interpretation.
- `test_world_update.py` tests world update behavior.

Future cleanup may move test files into a dedicated `tests/` directory, but that is not required yet.

---

### `requirements.txt`

Python dependency list for the project.

Purpose:

- Records third-party packages required to run the project.
- Allows the environment to be recreated with:

```bash
pip install -r requirements.txt
```

At the current stage, the project may have few or no external dependencies.

---

### `.gitignore`

Defines files and folders excluded from Git tracking.

Should exclude:

```text
.venv/
__pycache__/
*.pyc
*.zip
```

Purpose:

- Prevents generated files, local environments, and temporary exports from entering version control.

## Generated / Ignored Folders

The following folders are expected but should not be treated as source architecture:

```text
.venv/
__pycache__/
engine/__pycache__/
```

### `.venv/`

Local Python virtual environment.

Purpose:

- Stores the local Python interpreter and installed packages.
- Created by:

```bash
python -m venv .venv
```

This folder should not be committed to Git.

---

### `__pycache__/`

Python bytecode cache folders.

Purpose:

- Generated automatically by Python.
- Safe to delete.
- Should not be committed to Git.

## Standard Future Chat Structure

For future sprint chats, use the simplified structure above instead of pasting a full `tree /F` output.

If the structure has not changed, say:

```text
Project structure unchanged since project_structure.md.
```

If a new source folder or major file is added, update this document and include the changed section only.
