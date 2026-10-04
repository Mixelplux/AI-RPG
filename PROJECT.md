# AI Narrative RPG Engine

## Purpose

Build a single-player AI-driven narrative RPG with persistent simulation, emergent storytelling, natural-language interaction, canonical lore integration, and AI-assisted narration.

The world should remember meaningful events and respond coherently to player actions.

Use the [Story-First Design Doctrine v0.2](docs/story_first_design_doctrine.md)
as the design-evaluation lens for future decisions; its provisional mechanisms
and hypotheses do not mandate implementation.

## Development Approach

Development proceeds through small, bounded capability packages.

Each package should deliver one coherent capability, build on established architecture, remain testable, and avoid speculative infrastructure.

Implement the minimum sufficient detail justified by current player or architecture needs.

Use `docs/engineering_posture.md`: Routine is the default, Elevated covers
meaningful persistence or cross-system consequences, and Critical covers rare
high-consequence boundaries. Focused tests are normal; review and evidence
scale with credible consequence and recovery difficulty.

## Ownership

**Owner:** product direction, priorities, player-facing behavior, major scope and architecture decisions, risk acceptance, and merge authorization.

**ChatGPT:** requested architecture assessment, capability recommendations,
and review appropriate to the change's risk.

**Codex:** bounded repository implementation, testing, verification, and,
when authorized, review-candidate preparation under `AGENTS.md` and `WORKFLOW.md`.

See `docs/architecture.md` for the current system map.
