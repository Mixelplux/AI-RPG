# Region Pack Schema

## Purpose

Defines static world data for a playable simulation region.

A Region Pack is a simulation boundary. It may include locations, entities, initial weather values, encounter rules, and lore references needed to run a focused part of the world.

---

## Producer

Human-authored content, tools, or future content pipeline.

---

## Consumer

Scene Loader / Scene Builder

---

## JSON Structure

```json
{
  "region_id": "string",
  "name": "string",
  "version": "string",
  "locations": {},
  "entities": {},
  "weather": {},
  "spawn_rules": [],
  "lore": {}
}
```

---

## Required Fields

- `region_id`
- `name`
- `version`
- `locations`

---

## Optional Fields

- `entities`
- `weather`
- `spawn_rules`
- `lore`

---

## Weather

The Region Pack `weather` field provides initial weather values only.

Runtime weather ownership belongs to `world_state.weather`.

Scene Builder must read current weather from `world_state`, not directly from the Region Pack, except during world-state initialization.

No weather simulation is implemented yet.

---

## Connected Locations

Each location may define `connected_locations`.

Each connection includes:

- `direction`
- `location_id`

Directions are canonical values such as `north`, `south`, `east`, `west`, `in`, `out`, `up`, or `down`. Future Region Packs may define additional canonical directions.

Every referenced `location_id` must exist in the same Region Pack. Validation occurs during engine startup.

---

## Notes

Region Pack data is not player-facing by default. It becomes player-facing only after passing through Scene Snapshot, Perception Builder, and Narrator.
