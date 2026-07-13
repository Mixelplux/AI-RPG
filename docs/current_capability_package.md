# Authored Actor-Knowledge Conversation Response

Status: Complete — implementation and package closeout complete; awaiting owner acceptance.

## Purpose and Owner-Visible Value

Permit a present authored static actor to return one exact Region Pack-owned
response after a successful conversation, but only when that actor held the
declared durable knowledge identifier at command start. This makes the existing
actor-knowledge domain visible without adding dialogue, reaction, or rule
infrastructure.

## Included Internal Milestones

1. Sprint 10.43 — Authored contract and architecture boundary — complete.
2. Sprint 10.44 — Deterministic derivation and conversation integration — complete.
3. Sprint 10.45 — Presentation, compatibility, verification, and closeout — complete.

## Scope, Ownership, and Compatibility

- Region Packs may declare exactly one optional immutable,
  `conversation_actor_knowledge_response`, with exactly `response_id`,
  `target_entity_id`, `required_knowledge_id`, and `response_text`.
- The response is an exact authored player-facing projection. World State owns
  only existing actor-knowledge membership; no response state, history, or save
  field is added.
- Eligibility is evaluated against durable command-start knowledge membership,
  only after a successful current-scene conversation with the declared present
  stable static actor.
- The normal conversation candidate, consequences, validation, one Scene
  Snapshot rebuild when required, and one live publication remain unchanged.
- Save version remains `1`; Region Packs without the declaration and existing
  saves retain their behavior.

## Exclusions

No dialogue system, topics, branching, semantic input interpretation,
disposition, relationship, player knowledge, actor knowledge propagation or
loss, evidence discovery, AI-generated dialogue, narration integration,
response persistence, response history, multiple declarations, generic
conditions, reaction registry, projection bus, generalized consequences, or
conversation-ordering change.

## Architecture Decisions and Stop Conditions

The response is a narrow, read-only, non-persistent projection derived once per
eligible successful result. It cannot mutate Region Pack data, candidate or
live World State, Scene Snapshot, or membership. Failed validation or Scene
construction publishes neither state nor response. Stop for a persistence or
ownership change, an unapproved player-visible behavior, a generic framework,
or another `WORKFLOW.md` stop condition.

## Verification, Completion, and Rollback

Focused declaration, derivation, conversation, location, save/load, isolation,
and rendering tests; relevant existing regressions; Region Pack validation; all
27 root test scripts; official preflight; canonical manifest deep agreement;
`git diff --check`; and independent `package-review` packet validation passed.
The final package-review archive will be regenerated for owner review from the
documentation-closeout commit. Save version remains `1`; `next_sprint` remains
`null`; no next capability package is selected or staged. Rollback is confined
to this feature branch; no migration or data conversion is introduced.
