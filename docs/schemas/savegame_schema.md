# Savegame Schema

## Purpose

Defines serialized engine state for saving and loading the game.

This schema is planned but not yet implemented.

---

## Producer

Future Save System

---

## Consumer

Future Load System

---

## JSON Structure

```json
{
  "save_version": "string",
  "created_at": "string",
  "active_region_id": "string",
  "current_scene_snapshot": {},
  "world_state": {},
  "player_state": {}
}
```

---

## Required Fields

To be defined when Save/Load begins.

---

## Optional Fields

To be defined when Save/Load begins.

---

## Notes

Save/Load should serialize deterministic state, not AI prose.
