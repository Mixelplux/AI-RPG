# System Architecture

## Purpose

This document is a concise map of the current AI Narrative RPG Engine architecture.

Detailed architectural decisions belong in `docs/decisions.md`. Package-specific requirements belong in the current capability package.

Living responsibility models and shared design doctrines are indexed in
[System design manifests](design/systems/README.md). Their
[system map](design/systems/system-map.md) separates conceptual ownership from
the runtime flow and storage boundaries described here.

Do not add sprint history, full schemas, test inventories, or implementation walkthroughs here.

## Tech Stack

- Python 3.13
- CLI gameplay interface
- JSON Region Packs for authored world content
- Version-1 World State saves
- OpenAI Responses narration preview behind provider-neutral engine boundaries

## Directory Map

```text
/
├─ engine/          Simulation, interaction, state, projection, persistence, narration
├─ data/regions/    Immutable authored Region Packs
├─ docs/            Architecture, ADRs, workflow, package, and sprint records
├─ tools/           Validation, preflight, and review-packet tooling
├─ handoffs/        Review and handoff artifacts
├─ .artifacts/      Temporary evaluation evidence
├─ play_game.py     CLI entry point
└─ test_*.py        Automated tests
```

## Runtime Flow

```text
Player Input
    ↓
Interaction Kernel
    ↓
Structured Interaction Result
    ↓
GameEngine
    ↓
Candidate State Transition
    ↓
Validated World State
    ↓
Scene Snapshot
    ↓
Player-Safe Projection
    ↓
CLI or Narration Preview
```

`GameEngine` is the gameplay-facing orchestration boundary. Player-facing code must not directly mutate lower-level state.

## Sources of Truth

### World State

`world_state` owns mutable persistent simulation truth, including accepted runtime state such as:

- player location, time, and weather;
- durable history;
- pressures and thread state;
- actor location changes;
- actor knowledge;
- evidence traces and player discoveries;
- player competence tags and accepted attempts for the bounded West-Road slice;
- the fixed west-road reference predicament phase and causal outcome reference.

### Region Packs

Region Packs are immutable authored content.

They define locations, connections, actors, descriptions, initial values, and bounded authored declarations.

Runtime state may use Region Pack policy, but Region Packs themselves do not become mutable state.

### Derived Projection

Scene Snapshots, player perception, affordances, and narration context are derived from authoritative state and authored content.

They do not own persistent simulation state.

## Persistent Transitions

Material state changes use the established candidate-state pattern:

```text
Copy current state
    ↓
Prepare source event and consequences
    ↓
Validate completed candidate
    ↓
Build required derived scene
    ↓
Publish once
```

Failures must not leave partial durable mutation.

Durable causal references use stable backward `history_id` references.

Save envelope version remains `1`. Revised Bryn Shander content deliberately rejects prototype saves missing `west_road_predicament`; loading does not invent a branch or alter the existing file/session. See ADR-060. Other content retains its own validated state requirements.

Character Competence V1 uses one local authority for evidence applicability,
recognition, eligibility, costs and d6 interpretation. Accepted West-Road attempts
persist their draw/result and backward causal references; full results reuse the
existing pursuit outcome in the same candidate transaction. Missing additive
competence fields normalize empty only in a copied loaded payload. Projection
and narration receive player-safe layers, never authority to resolve attempts.

## Character Information and Spatial Projection

Keep these concepts separate:

- **World truth:** what is actually true.
- **Perception:** what the character can currently observe.
- **Familiarity:** broad background understanding.
- **Acquired information or belief:** selectively retained information encountered during play.

Player-facing projection must not expose hidden causes or information merely because the engine knows it.

Use minimum sufficient world detail:

- author important structure;
- resolve incidental detail only when needed;
- persist it only when future gameplay materially depends on it.

The authored map represents macro spatial relationships, not every possible traversal path. Spatial presentation should favor natural orientation over a raw compass-direction grid.

See ADR-059 for governing detail.

## Narration Boundary

```text
Bounded Narration Context
    ↓
Validated Provider-Neutral Request
    ↓
Validated Prompt
    ↓
Untrusted Candidate Source
    ↓
Source-Result Validation
    ↓
Narration-Output Validation
    ↓
Preview Display
```

The current live source is an explicit OpenAI Responses preview.

Narration:

- is preview-only;
- is untrusted until validated;
- has no simulation authority;
- does not persist prose;
- does not run automatically during normal gameplay;
- must fail closed without changing deterministic gameplay.

## Context Loading

Do not read this file for every routine implementation turn.

Read it when:

- the current task affects an architectural boundary;
- ownership or persistence is unclear;
- the capability package explicitly references it;
- a material architecture conflict must be resolved.

For ordinary bounded work, use the current capability package, current sprint, and specifically named ADRs.
