# Development Workflow

## Technical Lead

The ChatGPT Project acts as Technical Lead.

Responsibilities:

* Sprint planning
* File creation
* Code generation
* Testing guidance
* Documentation updates
* Maintaining the roadmap

---

## Architecture Review

Separate chats are used only for:

* Architecture reviews
* Design discussions
* Major technology decisions
* Independent code reviews

Implementation decisions are returned to the Project before coding.

---

# Task Format

Every implementation task must contain:

1. Goal
2. Why
3. Files to Create or Modify
4. Complete Code
5. Where the Code Goes
6. How to Run It
7. Expected Output
8. Done When Checklist

Only one task is active at a time.

No future tasks are started until the current task is confirmed working.

---

# Sprint Workflow

Beginning of Sprint

* Load current documentation
* Review current sprint
* Implement one task at a time

End of Sprint

Generate or update:

* current_sprint.md
* sprint_log.md
* architecture.md (only if changed)
* roadmap.md (only if changed)

Commit code and documentation together.

---

# Chat Management

Create one Project chat per sprint.

Suggested naming:

Sprint 1 – Foundation

Sprint 2 – Perception Layer

Sprint 3 – Narrator

Sprint 4 – Interaction

Sprint 5 – Character System

At the end of each sprint:

1. Generate updated documentation.
2. Save the documentation into the repository.
3. Start a new Project chat.
4. Begin by providing the current documentation and requesting continuation from the latest sprint.

Never rely on previous chat history as the project's memory.

The repository is the project's permanent memory.

## File Reference Discipline

Before modifying code in any sprint task, the assistant must confirm the current project file tree or use only files explicitly provided in the attached documentation.

The assistant must not assume files, paths, function names, or module names exist.

Each task response must begin with:
- Files to modify
- Files to create, if any
- Files intentionally left unchanged

If a file path is uncertain, the assistant must ask for the current file tree or the relevant file contents before giving code.
