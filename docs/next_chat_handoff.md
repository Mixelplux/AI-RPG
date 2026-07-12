# Next Chat Handoff: Sprint 10.17 Complete

Sprint 10.17 is complete. `GameEngine.add_actor_knowledge(actor_id, knowledge_id)` now atomically appends a new opaque identifier to a stable static actor's sparse World State membership and records exactly one durable `actor_knowledge_added` history entry. Duplicates are no-ops that preserve live World State and Scene Snapshot; material additions validate against the active Region Pack and do not rebuild the scene. The lifecycle record is durable and history-queryable but excluded from narration context. Save version remains 1; ADR-046 records the boundary.

All 23 root tests, Region Pack validation, save/load atomicity smoke, manifest deep comparison, preflight, and packet validation passed with the official interpreter. No Sprint 10.18 is defined or started. Changes remain uncommitted for owner review.
