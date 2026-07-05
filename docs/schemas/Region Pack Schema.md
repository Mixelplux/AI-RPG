# Region Pack Schema

## Purpose

A Region Pack defines one playable simulation boundary.

It is not required to represent a fixed geographic size. A small town, a city district, an island, a dungeon, or a wilderness route can all be Region Packs.

---

# Scale Rule

Use the smallest simulation boundary that can support play.

Examples:

* Bryn Shander = one Region Pack
* Waterdeep = atlas pack + district Region Packs
* Moonshae Isles = atlas pack + island or settlement Region Packs

---

# Required Top-Level Fields

```json
{
  "region_id": "string",
  "region_name": "string",
  "setting": "string",
  "canon_source": "string",
  "version": "string",

  "time": {},
  "region_state": {},
  "locations": [],
  "entities": [],
  "factions": [],
  "event_history": [],
  "simulation_hooks": {}
}
```

---

# Time

```json
"time": {
  "calendar_system": "string",
  "current_date": "string",
  "season": "string",
  "time_of_day": "string"
}
```

---

# Region State

Region state contains mutable simulation values.

Use numeric values where change over time matters.

```json
"region_state": {
  "weather": {
    "type": "string",
    "severity": 0.0,
    "temperature_c": 0,
    "wind_speed_kmh": 0,
    "visibility_m": 0
  },

  "economy_state": {
    "stability": 0.0,
    "primary_trade": [],
    "import_dependency": 0.0
  },

  "security_state": {
    "threat_level": 0.0,
    "watch_presence": 0.0,
    "wall_condition": 0.0
  },

  "population_state": {
    "total_estimated": 0,
    "density_level": "string",
    "active_distribution": {}
  }
}
```

Numeric values should generally use `0.0` to `1.0`.

---

# Locations

Each location is an interactable node.

```json
{
  "location_id": "string",
  "name": "string",
  "type": "string",
  "description_seed": "string",

  "state": {},

  "spawn_rules": {},

  "connected_locations": []
}
```

## Location Requirements

Each location must have:

* unique `location_id`
* clear `type`
* `description_seed`
* `state`
* `connected_locations`

---

# Spawn Rules

Spawn rules define what appears in a location.

```json
"spawn_rules": {
  "guards": {
    "count": 2,
    "template": "city_guard",
    "persistence": "dynamic"
  },

  "citizens": {
    "count_range": [5, 12],
    "template": "civilian",
    "persistence": "transient"
  }
}
```

## Persistence Types

* `static` = named permanent entity
* `dynamic` = generated entity that may become permanent
* `transient` = temporary scene entity

---

# Entities

Entities are persistent world objects.

They may be NPCs, monsters, buildings, organizations, or important items.

```json
{
  "entity_id": "string",
  "name": "string",
  "type": "string",
  "persistence": "static",
  "location": "location_id",

  "state": {},

  "knowledge": [],

  "relationships": {}
}
```

---

# Factions

```json
{
  "faction_id": "string",
  "name": "string",
  "type": "string",

  "influence_level": 0.0,
  "stance_toward_player": 0.5,

  "state": {},

  "objectives": []
}
```

---

# Events

Events record meaningful changes.

```json
{
  "event_id": "string",
  "type": "string",
  "timestamp": "string",
  "summary": "string",
  "participants": [],
  "outcomes": []
}
```

---

# Simulation Hooks

```json
"simulation_hooks": {
  "current_phase": "string",

  "allowed_systems": {
    "combat": false,
    "inventory": false,
    "magic": false,
    "skills": false
  },

  "entry_location": "location_id"
}
```

---

# Design Rules

## 1. Canon and State Must Stay Separate

Canon describes what is foundational.

State describes what is currently true.

---

## 2. Use IDs for Engine References

Names are for humans.

IDs are for the engine.

---

## 3. Prefer Numeric State for Changeable Values

Use numbers when the simulation may increase, decrease, or compare a value.

---

## 4. Do Not Overpopulate

Do not create every citizen, shopkeeper, traveler, or animal in advance.

Use spawn rules.

---

## 5. Generated Content Becomes Permanent Only When Meaningful

A transient traveler should not become permanent unless the player interacts with them or they affect the world.

---

## 6. Narration Does Not Belong in Region Packs

Region Packs contain data and description seeds.

They do not contain finished prose.

---

# Validation Checklist

A Region Pack is valid when:

* [ ] It has all required top-level fields.
* [ ] Every location has a unique `location_id`.
* [ ] Every entity location points to a valid location.
* [ ] Every connected location points to a valid location.
* [ ] The entry location exists.
* [ ] Spawn rules use valid persistence types.
* [ ] Mutable simulation values are numeric where appropriate.
* [ ] No hidden information is placed in player-facing description fields.
