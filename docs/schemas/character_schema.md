# Character Schema

## Purpose

Defines player character and NPC state.

This schema is planned but not yet implemented.

---

## Producer

Future Character System

---

## Consumer

Future systems may include Interaction Kernel, Perception Builder, Combat, Skills, Save/Load, and Narrator through filtered perception only.

---

## JSON Structure

```json
{
  "character_id": "string",
  "name": "string",
  "type": "string",
  "description": "string",
  "location_id": "string",
  "state": {},
  "relationships": {},
  "hidden_state": {}
}
```

---

## Required Fields

To be defined when Sprint 5 begins.

---

## Optional Fields

To be defined when Sprint 5 begins.

---

## Notes

Do not implement a full character system before it is required by a vertical slice.
