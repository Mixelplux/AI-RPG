# Player Perception Schema

## Purpose

Defines what the player can reasonably perceive from the current Scene Snapshot.

Player Perception is the only scene-state object the Narrator should receive.

---

## Producer

Perception Builder

---

## Consumer

Narrator

---

## JSON Structure

```json
{
  "title": "string",
  "location_description": "string",
  "visible_weather": {},
  "visible_entities": [],
  "available_exits": [],
  "sensory_details": [],
  "player_prompt": "string"
}
```

---

## Required Fields

- `title`
- `location_description`
- `visible_entities`
- `player_prompt`

---

## Optional Fields

- `visible_weather`
- `available_exits`
- `sensory_details`

---

## Notes

This object must exclude hidden state, concealed entities, secret motives, mechanical internals, and any information the player could not reasonably know.
