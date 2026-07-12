# Sprint 10.18 Complete

Sprint 10.18 is complete. `GameEngine.add_actor_knowledge_from_event(actor_id, knowledge_id, source_history_id)` atomically appends opaque membership for one stable static actor and records a structural backward reference to one already accepted durable event. Duplicates validate the source but leave World State, history, and Scene Snapshot unchanged. The source remains separate and unmodified; `actor_knowledge_added` stays history-queryable and excluded from narration context.

Save version remains `1`; source-free Sprint 10.17 records remain valid. ADR-047 records the boundary. Sprint 10.19 is not defined or started.
