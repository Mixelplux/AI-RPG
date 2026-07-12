# PROJECT.md

# AI Narrative RPG Engine

## Purpose
A single-player AI-driven narrative RPG emphasizing persistent simulation, emergent storytelling, canonical lore integration, and incremental development.

## Architecture Ownership
- ChatGPT owns architecture, planning, documentation, and sprint definition.
- Codex owns local implementation and testing.
- The repository remains sprint-driven with one active sprint at a time.

## Development Environment
- Supported Python: 3.13.x
- Project virtual environment: .venv
- Verification should use the project virtual environment.

## Review Communication
- Architecture reviews must lead with a concise plain-language owner summary and a fixed decision card.
- Technical detail remains available in an appendix or evidence packet and is surfaced in the main review only when it changes scope, risk, persistence, ownership, or the requested decision.
- The project owner decides product direction, scope, sequencing, and acceptable risk; implementation agents validate low-level correctness.
- Use sprint health checks for routine closeouts, capability-cluster reviews for subsystem readiness, and deep architecture reviews only for consequential boundaries.
- Use `docs/architecture_review_template.md` for owner-facing review output.
