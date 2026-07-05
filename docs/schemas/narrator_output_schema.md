# Narrator Output Schema

## Purpose

Defines the output produced by the Narrator from Player Perception.

Narrator Output is descriptive. It does not alter simulation state.

---

## Producer

Narrator

---

## Consumer

Player-facing interface

---

## JSON Structure

```json
{
  "narration": "string",
  "player_prompt": "string"
}
```

---

## Required Fields

- `narration`
- `player_prompt`

---

## Optional Fields

None currently.

---

## Notes

Narration must stay grounded in Player Perception. It must not invent entities, outcomes, lore changes, hidden knowledge, or world state.
