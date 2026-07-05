# Future Design

This document is a parking lot for important design ideas that are not ready to implement.

Ideas here may later become simulation principles, architecture decisions, schemas, or sprint tasks.

Nothing in this document should change engine behavior until it is explicitly promoted into the roadmap or current sprint.

---

## How To Use This Document

When a broad game-behavior idea comes up during discussion:

1. Capture the scenario or principle here.
2. Mark its status.
3. Avoid defining data fields or code unless implementation is near.
4. Continue the current sprint.

Use this document to preserve design thinking without violating the No Premature Systems rule.

---

## Template

```md
## Idea Name

**Status:** Idea

### Scenario

Describe the gameplay situation or design problem.

### Design Question

What should the world decide, remember, ignore, or react to?

### Current Thinking

Capture the principle, tradeoff, or possible direction.

### Possible Future Implementation

List possible systems only as placeholders.

### Not Before

Name the phase, sprint, or dependency that should exist first.
```

---

## Scenario Exploration: Stolen Object From an Apparently Abandoned Shack

**Status:** Captured Scenario

### Scenario

The player finds a shack that appears abandoned, searches it, takes an item of high interest, and leaves.

Later, the owner or another interested actor may return and discover the item is missing.

### Design Question

When should the world ignore this, let it fade, or activate it into a meaningful consequence?

### Current Thinking

This scenario is governed by the World Attention Budget principle.

The theft should not automatically become a quest or response. It should become active only if an actor plausibly notices the evidence, cares about it, has a way to respond, and the response creates meaningful play.

### Possible Future Implementation

- evidence records
- ownership records
- actor goals
- discovery checks
- investigation behavior
- rumor or report propagation
- thread activation

### Not Before

Do not implement before the engine supports persistent world state, actor goals, and time advancement.
