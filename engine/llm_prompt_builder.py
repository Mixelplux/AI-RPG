from typing import Dict, Any


def build_narration_prompt(narration: Dict[str, Any]) -> str:
    """
    Build an LLM-ready prompt from structured narration.

    v0.1 rules:
    - Use only structured narration.
    - Do not expose raw world state.
    - Do not allow the LLM to invent new facts.
    """

    title = narration.get("title", "Unknown Location")
    description = narration.get("description", "")
    visible_entities = narration.get("visible_entities", [])
    player_prompt = narration.get("player_prompt", "What do you do?")

    visible_entities_text = "\n".join(
        f"- {entity}" for entity in visible_entities
    )

    if not visible_entities_text:
        visible_entities_text = "- None"

    return f"""
You are the narrator for a single-player narrative RPG.

Your job is to rewrite the provided scene information into natural language.

Rules:
- Do not invent new locations.
- Do not invent new characters.
- Do not invent dialogue.
- Do not reveal hidden information.
- Do not change the world state.
- Use only the facts provided below.
- End with the player prompt exactly as written.

Scene Title:
{title}

Scene Description:
{description}

Visible Entities:
{visible_entities_text}

Player Prompt:
{player_prompt}
""".strip()