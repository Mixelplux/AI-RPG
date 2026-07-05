# Scene Snapshot Schema

## Purpose

Defines the complete derived simulation view for the current scene.

The Scene Snapshot is not the persistent source of truth. It is rebuilt from Region Pack data and `world_state`.

---

## Producer

Scene Builder

---

## Consumer

Perception Builder

Future consumers may include debugging tools and AI narration pipelines.

---

## JSON Structure

```json
{
  "scene_id": "string",
  "region_id": "string",
  "location": {},
  "weather": {},
  "entities_present": [],
  "exits": [],
  "time": {},
  "hidden_state": {}
}
```

---

## Required Fields

- `scene_id`
- `region_id`
- `location`
- `entities_present`

---

## Optional Fields

- `weather`
- `exits`
- `time`
- `hidden_state`

---

## Notes

The full Scene Snapshot may contain hidden or non-obvious information. It must not be sent directly to the Narrator.

Current weather in the Scene Snapshot comes from `world_state.weather`.

Current time in the Scene Snapshot comes from `world_state.time`.
