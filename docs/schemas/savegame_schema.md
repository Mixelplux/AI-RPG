# Savegame Schema

## Purpose

Defines the serialized runtime state used by the deterministic save/load system.

## JSON Structure

```json
{
  "save_version": 1,
  "region_path": "data/regions/bryn_shander.json",
  "world_state": {}
}
```

## Required Fields

- save_version
- region_path
- world_state

## Notes

Only World State is serialized. Scene Snapshots, Player Perception, and Narration are regenerated after loading.
