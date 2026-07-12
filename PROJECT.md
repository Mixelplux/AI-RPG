# PROJECT.md

# AI Narrative RPG Engine

## Purpose
A single-player AI-driven narrative RPG emphasizing persistent simulation, emergent storytelling, canonical lore integration, and incremental development.

## Architecture Ownership
- ChatGPT owns architecture, planning, documentation, and sprint definition.
- Codex owns local implementation and testing.
- The owner approves capability-package direction and consequential architecture decisions; the lead Codex session owns routine in-scope implementation and verification.
- The repository remains capability-package driven with one active sprint at a time.

## Development Environment
- Supported Python: 3.13.x
- Project virtual environment: .venv
- Verification should use the project virtual environment.

## Review Communication
- Architecture reviews must lead with a concise plain-language owner summary and a fixed decision card.
- Technical detail remains available in an appendix or evidence packet and is surfaced in the main review only when it changes scope, risk, persistence, ownership, or the requested decision.
- The project owner decides product direction, scope, sequencing, and acceptable risk; implementation agents validate low-level correctness.
- Use brief internal health checks for routine milestones, capability-package reviews at meaningful boundaries, and deep architecture reviews only for consequential boundaries.
- Review fatigue is a project risk: prefer fewer meaningful approvals, strong automated verification, auditable checkpoint history, and clear owner-level reporting over repetitive technical packets or low-value continuation approvals.
- Use `docs/architecture_review_template.md` for owner-facing review output.
