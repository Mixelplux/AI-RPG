Project: AI Narrative RPG Engine

Sprint 10.18 — Causally Referenced Actor-Knowledge Addition is complete, committed, and closed out.

## Authoritative owner-reported state

* Branch: `main`
* Working tree: clean
* Sprint 10.18 committed
* Save version remains `1`
* All 23 root repository test scripts passed
* ADR-047 records causally referenced actor-knowledge addition
* Sprint 10.19 has not been defined, staged, or started

The attached `post_sprint_10_18_architecture_review_packet.zip` is the canonical post-sprint review and handoff package generated before the owner commit.

The packet contains 38 validated entries and includes all six required evidence files, including restored `review_context.md`.

The previous architecture review noted one packet-format issue: `review_brief.md`, `review_context.md`, and `verification_results.txt` contain literal PowerShell `` `r`n `` markers instead of real line breaks. Correct this in the Sprint 10.19 review packet.

The packet records the pre-Sprint-10.18 source HEAD:

```text
29c5860e777059a6e169c3863d6d90eebd7adfd2
```

The current local repository is authoritative for the exact post-commit HEAD and clean status.

## Accepted architecture-review recommendation

The post-Sprint 10.18 architecture review is complete, and its recommendation has been accepted.

The next bounded Phase 2B capability is:

# One Declared Resolved-Conversation Actor-Knowledge Consequence

This acceptance selected the direction only. It did not define or start Sprint 10.19.

## Purpose of this chat

Inspect the actual repository state, then stage, implement, verify, document, and close out Sprint 10.19 as one bounded task.

Do not define or begin Sprint 10.20.

Start by inspecting the local repository and attached packet. Confirm that the committed repository state agrees with this handoff before defining Sprint 10.19.

## Current actor-knowledge foundation

Sprint 10.16 established:

* sparse persistent `world_state.actor_knowledge`;
* stable static actor identity as the ownership key;
* Region Pack knowledge arrays as new-game seeds;
* legacy version-1 missing-field normalization to `{}`;
* Region-aware validation;
* copy-safe inspection;
* no mutation or player-facing projection.

Sprint 10.17 added:

* explicit atomic `add_actor_knowledge(actor_id, knowledge_id)`;
* deterministic insertion order;
* one durable `actor_knowledge_added` entry for material additions;
* duplicate additions as unchanged no-ops;
* no Scene Snapshot rebuild;
* narration-context exclusion.

Sprint 10.18 added:

* explicit causally referenced actor-knowledge addition;
* one required backward `source_history_id`;
* structural source linkage without semantic interpretation;
* atomic membership and history commit;
* duplicate no-op behavior that still validates the source;
* save/load compatibility with source-free and causally referenced history;
* malformed causal-reference rejection during candidate load;
* no player-facing behavior.

## Existing conversation consequence foundation

The repository already contains a resolved-conversation transition that may compose:

* one durable `player_conversation` history entry;
* declared pressure consequences;
* declared actor-relocation consequences;
* unresolved-thread consequences;
* one copied candidate World State;
* final Region-aware validation;
* one candidate Scene Snapshot build;
* one live commit.

Inspect the exact current ordering, ownership, helper patterns, result packets, and failure boundaries before implementation.

## Sprint 10.19 objective

Stage Sprint 10.19 using the title:

**Sprint 10.19 — One Declared Resolved-Conversation Actor-Knowledge Consequence**

Use this objective:

> Add one strict immutable Region Pack declaration that causes one successfully resolved conversation with one declared static actor to add one exact knowledge identifier to one declared stable static actor, using the accepted conversation history entry as the causal source and committing the conversation, knowledge membership, and lifecycle history atomically within the existing conversation transition.

## Required initial inspection

Before defining the sprint, confirm:

* current branch;
* exact current HEAD;
* clean working tree;
* Sprint 10.18 completion and commit;
* canonical manifest agreement;
* `next_sprint` remains null;
* save version remains `1`;
* ADR-045, ADR-046, and ADR-047 content;
* complete root test inventory;
* exact actor-knowledge representation and Region-aware validation;
* exact source-free and causally referenced mutation implementations;
* existing private candidate helpers, if any;
* current resolved-conversation transition ordering;
* current conversation history construction;
* existing declared pressure-consequence schema and runtime pattern;
* existing declared actor-relocation consequence schema and runtime pattern;
* unresolved-thread consequence composition;
* result-packet conventions;
* history-ID generation and causal-order validation;
* Scene Snapshot build and commit rules;
* save/load candidate reconstruction;
* narration lifecycle-exclusion boundary;
* defensive-copy conventions.

Read these packet-level files first:

* `packet_manifest.md`
* `review_brief.md`
* `review_context.md`
* `verification_results.txt`
* `git_status.txt`
* `git_log.txt`

Validate the exact ZIP inventory against `packet_manifest.md`.

## Canonical sprint staging

Define Sprint 10.19 in:

* `docs/current_sprint.md`
* `docs/current_sprint.yaml`
* `docs/current_sprint.json`
* `docs/next_chat_handoff.md`

Ensure the three canonical manifests deeply agree before implementation.

Do not stage Sprint 10.20.

## Required Region Pack declaration

Add one optional singular immutable declaration following current repository naming conventions, conceptually:

```json
{
  "effect_id": "captain_conversation_grants_knowledge",
  "trigger_entity_id": "captain_darvin_grey",
  "actor_entity_id": "captain_darvin_grey",
  "knowledge_id": "player_spoke_with_captain"
}
```

The exact field or container name should follow the established pressure and actor-location declaration conventions after inspection.

Prefer a name conceptually similar to:

```text
conversation_actor_knowledge_effect
```

The declaration must contain exactly:

* `effect_id`;
* `trigger_entity_id`;
* `actor_entity_id`;
* `knowledge_id`.

Do not add additional metadata.

Use one real Bryn Shander static actor as the conversation trigger and one stable static actor as the receiving actor. They may be the same actor if that produces the smallest valid fixture.

The knowledge identifier must remain an opaque identifier. Do not interpret it as truth, belief, certainty, or dialogue content.

## Declaration validation

The Region Pack validator must enforce:

* the declaration is optional and singular;
* the declaration is an object when present;
* exactly the required fields are present;
* no unknown fields are accepted;
* every field is a non-empty string;
* `effect_id` follows existing identifier validation conventions;
* `trigger_entity_id` resolves to a stable static actor;
* `actor_entity_id` resolves to a stable static actor;
* spawned or ephemeral actor identities are rejected;
* `knowledge_id` is structurally valid and non-empty;
* the knowledge identifier does not need to appear in authored seed membership;
* Region Pack content remains immutable at runtime.

Do not add a knowledge catalog or ontology.

## Runtime trigger

The consequence may occur only when:

* a conversation successfully resolves;
* the resolved target entity matches `trigger_entity_id`;
* the normal `player_conversation` history entry is accepted into the candidate transition.

Unmatched conversations must remain unaffected.

Failed, unresolved, malformed, or rejected conversations must not grant actor knowledge.

Do not inspect or interpret freeform conversation text.

## Required runtime composition

For one matching successful resolved conversation:

1. Copy the current World State through the existing conversation transition.
2. Prepare the normal `player_conversation` history entry.
3. Treat that new conversation entry as the `source_history_id`.
4. Evaluate the one declared actor-knowledge consequence.
5. Prepare the actor-knowledge addition against the same candidate World State.
6. Create a causally referenced `actor_knowledge_added` entry only for a material addition.
7. Preserve the existing consequence ordering required for causal integrity.
8. Apply any existing pressure, relocation, and unresolved-thread consequences according to current deterministic ordering.
9. Validate the completed candidate World State and history against the active Region Pack.
10. Build the candidate Scene Snapshot once through the existing conversation boundary.
11. Commit World State and Scene Snapshot once.

There must be no intermediate live commit.

There must be no additional Scene Snapshot build caused specifically by actor knowledge.

## Candidate helper

Inspect the Sprint 10.18 implementation and extract the smallest private non-committing candidate helper needed to reuse its validation and history semantics inside the conversation transition.

Conceptually:

```python
_prepare_actor_knowledge_from_event_candidate(
    candidate_world_state,
    actor_id,
    knowledge_id,
    source_history_id,
)
```

The exact location, name, parameters, and return shape should follow existing repository patterns.

The helper should:

* operate only on a supplied candidate World State;
* validate actor, knowledge, and source linkage;
* add membership and history only to the candidate;
* return a deterministic defensive consequence packet;
* not assign live World State;
* not build or replace a Scene Snapshot;
* not mutate Region Pack content.

The public Sprint 10.18 operation should reuse this helper where practical so public and conversation-triggered operations share one mutation rule.

Do not introduce a generic consequence dispatcher, transaction system, actor-state framework, or rules engine.

## Material consequence behavior

When the receiving actor does not already possess the declared identifier:

* add the knowledge identifier exactly once;
* preserve existing membership and deterministic order;
* create exactly one `actor_knowledge_added` history entry;
* set its `source_history_id` to the accepted conversation entry;
* ensure the conversation entry precedes the knowledge entry;
* commit conversation history, knowledge membership, and consequence history atomically;
* return one deterministic `actor_knowledge_consequence` result packet;
* allow the existing conversation boundary to perform its normal single Scene Snapshot replacement.

Conceptual result:

```python
{
    "effect_id": "<effect-id>",
    "changed": True,
    "actor_id": "<actor-id>",
    "knowledge_id": "<knowledge-id>",
    "source_history_id": "<conversation-history-id>",
    "history_id": "<knowledge-history-id>"
}
```

Use exact repository result conventions after inspection.

## Duplicate consequence behavior

When the receiving actor already possesses the declared identifier:

* the successful conversation still commits normally;
* a new legitimate `player_conversation` history entry is still created;
* the declaration and source are still evaluated;
* no duplicate membership is added;
* no `actor_knowledge_added` entry is created;
* return a deterministic consequence packet with `changed: False`;
* return `history_id: None` if consistent with current conventions;
* preserve the existing membership order;
* perform no intermediate World State assignment;
* perform no additional Scene Snapshot build.

The conversation command may replace World State and Scene Snapshot once through its normal successful transition. The duplicate knowledge consequence itself must not create an extra commit or rebuild.

## Source-history semantics

The newly accepted `player_conversation` entry is the exact source event.

This establishes only that:

* the knowledge mutation was caused by the declared successful conversation transition;
* the source entry already exists earlier in the candidate history;
* the source entry is structurally linked through `source_history_id`.

It does not establish:

* what was said;
* whether the actor heard or understood anything;
* whether the knowledge is true;
* whether the source is reliable;
* whether the actor believes the information;
* certainty, confidence, evidence quality, or provenance beyond the structural source link.

Do not introduce semantic source eligibility rules.

## Atomic failure behavior

Any failure during:

* declaration validation;
* conversation resolution;
* trigger matching;
* source history preparation;
* source-history lookup or causal-order validation;
* receiving-actor validation;
* knowledge-identifier validation;
* candidate membership mutation;
* knowledge-history construction;
* pressure or actor-location consequence preparation;
* unresolved-thread consequence preparation;
* final Region-aware validation;
* final history-integrity validation;
* candidate Scene Snapshot construction;

must preserve the original live:

* World State;
* full durable history;
* actor knowledge;
* pressure state;
* actor locations;
* unresolved threads;
* Scene Snapshot identity and content;
* durable time;
* region identity and path;
* all other runtime state.

The conversation source and all prepared consequences must either commit together or not commit at all.

## Persistence and compatibility

* Save version remains `1`.
* No new World State field is required.
* The Region Pack declaration is immutable authored data and is not copied into saves.
* Materially granted knowledge survives save/load.
* The causally referenced `actor_knowledge_added` entry survives save/load.
* Its `source_history_id` continues to resolve to the persisted conversation entry.
* Loaded saves do not replay or regenerate the declaration consequence.
* Repeating the declared conversation after loading produces a legitimate new conversation entry but no duplicate knowledge lifecycle entry.
* Existing source-free actor-knowledge history remains valid.
* Existing causally referenced actor-knowledge history remains valid.
* Legacy missing actor-knowledge normalization remains unchanged.
* Malformed persisted knowledge causal linkage continues to fail through candidate-load validation.
* Failed load preserves the current live runtime state.

Do not bump the save version.

## Engine result and history visibility

Confirm that the resolved-conversation result includes one defensive actor-knowledge consequence packet when the declaration matches.

Use repository conventions for unmatched effects. The unmatched result may omit the field or set it to `None`, according to existing pressure and actor-location patterns.

Confirm:

* `get_history()` exposes the conversation and knowledge entries;
* `query_history(event_type="player_conversation")` exposes the source;
* `query_history(event_type="actor_knowledge_added")` exposes the consequence;
* the knowledge entry contains the exact conversation `source_history_id`;
* returned history is defensively copied;
* the result packet cannot mutate live state.

## Player-facing boundaries

Sprint 10.19 must introduce no new player-visible information.

Do not project actor knowledge or its source linkage into:

* Scene Snapshots;
* perception;
* narration history or context;
* narration requests;
* narration prompts;
* dialogue output;
* target resolution;
* CLI commands;
* unresolved-thread evidence;
* quests or objectives.

Continue excluding `actor_knowledge_added` from narration-facing history/context.

The existing player-visible conversation behavior should remain unchanged.

## Explicitly out of scope

Do not add:

* freeform conversation analysis;
* dialogue-content interpretation;
* multiple actor-knowledge declarations;
* multiple knowledge additions per conversation;
* generic effect declarations;
* generic consequence dispatch;
* witness or presence rules beyond the declared trigger;
* source-event semantic eligibility;
* evidence discovery;
* actor-to-actor propagation;
* rumors;
* elapsed-time knowledge acquisition;
* knowledge removal or forgetting;
* replacement or correction;
* false or outdated beliefs;
* certainty or confidence;
* truth or reliability evaluation;
* autonomous actor decisions or reactions;
* dialogue changes based on knowledge;
* player knowledge;
* narration or perception projection;
* a knowledge catalog or ontology;
* Sprint 10.20 work.

## Focused tests

Add focused coverage for at minimum:

### Declaration validation

1. Region Pack without the optional declaration remains valid.
2. One well-formed declaration is accepted.
3. Non-object declaration is rejected.
4. Missing required fields are rejected.
5. Unknown fields are rejected.
6. Empty `effect_id` is rejected.
7. Empty `trigger_entity_id` is rejected.
8. Empty `actor_entity_id` is rejected.
9. Empty `knowledge_id` is rejected.
10. Non-string fields are rejected.
11. Unknown trigger actor is rejected.
12. Unknown receiving actor is rejected.
13. Spawned or ephemeral trigger identity is rejected.
14. Spawned or ephemeral receiving identity is rejected.
15. The knowledge identifier need not appear in authored seed membership.
16. Region Pack content remains unchanged after runtime use.

### Trigger behavior

17. Unmatched successful conversation produces no knowledge consequence.
18. Failed or unresolved conversation produces no knowledge consequence.
19. Matching successful conversation evaluates the declaration.
20. Freeform conversation text is not interpreted.
21. Only the declared trigger actor activates the consequence.

### Material consequence

22. Matching conversation adds the knowledge identifier once.
23. Existing actor membership is preserved.
24. New membership is appended in deterministic order.
25. Sparse membership is created when absent.
26. Exactly one `actor_knowledge_added` entry is created.
27. The source is the exact new `player_conversation` history entry.
28. The conversation entry precedes the knowledge entry.
29. The knowledge entry records the correct actor.
30. The knowledge entry records the correct identifier.
31. The knowledge history time matches current durable time.
32. Conversation, membership, and knowledge history commit together.
33. The result includes the deterministic consequence packet.
34. Existing pressure, relocation, and unresolved-thread consequences still compose correctly.
35. Only one final live World State assignment occurs where instrumentable.
36. Only one normal conversation Scene Snapshot build or replacement occurs.

### Duplicate behavior

37. Repeating the matching conversation still records a new conversation entry.
38. Existing knowledge is not duplicated.
39. No additional `actor_knowledge_added` entry is created.
40. The consequence reports `changed: False`.
41. Membership order remains unchanged.
42. No intermediate World State assignment occurs.
43. No additional Scene Snapshot build occurs because of knowledge.

### Atomic failure preservation

44. Invalid receiving actor preserves all live state.
45. Invalid knowledge identifier preserves all live state.
46. Source-history preparation failure preserves all live state.
47. Knowledge-history construction failure preserves all live state.
48. Final Region-aware validation failure preserves all live state.
49. Final Scene Snapshot construction failure preserves all live state.
50. Failed consequence preserves history.
51. Failed consequence preserves actor knowledge.
52. Failed consequence preserves pressure state.
53. Failed consequence preserves actor locations.
54. Failed consequence preserves unresolved threads.
55. Failed consequence preserves Scene Snapshot identity.
56. Failed consequence preserves durable time.
57. Failed consequence preserves region identity and path.

### Persistence

58. Conversation-granted membership survives save/load.
59. Conversation history survives save/load.
60. Causally linked knowledge history survives save/load.
61. `source_history_id` resolves after loading.
62. Repeating the declared conversation after load remains a knowledge no-op.
63. The repeated conversation still records legitimate conversation history.
64. Save version remains `1`.
65. Source-free actor-knowledge entries remain compatible.
66. Existing causally referenced entries remain compatible.
67. Legacy missing-field normalization remains unchanged.
68. Malformed persisted causal linkage fails atomically.

### Defensive copies and inspection

69. `get_actor_knowledge(...)` returns updated membership.
70. Returned membership remains immutable or copy-safe.
71. Returned consequence result cannot mutate live state.
72. Returned history cannot mutate durable history.
73. The referenced conversation entry cannot be mutated through returned data.

### Player-facing isolation

74. Actor knowledge is absent from Scene Snapshot projection.
75. Actor knowledge is absent from perception.
76. `actor_knowledge_added` remains excluded from narration history/context.
77. Source linkage is absent from narration requests and prompts.
78. Dialogue behavior remains unchanged.
79. Existing narration output remains unchanged.
80. Existing targeting and CLI behavior remain unchanged.

### Regression coverage

81. Source-free actor-knowledge mutation tests remain valid.
82. Causally referenced actor-knowledge mutation tests remain valid.
83. Actor-knowledge baseline tests remain valid.
84. Pressure consequence regressions remain valid.
85. Actor-location consequence regressions remain valid.
86. Unresolved-thread regressions remain valid.
87. History and causal-integrity regressions remain valid.
88. Save/load and atomic-load regressions remain valid.
89. Complete root test inventory passes.

Use the current test framework and repository organization.

Do not migrate test tooling.

## ADR expectation

Do not create a new ADR unless implementation inspection reveals a genuinely new independent architectural decision.

This capability should be implementable as a direct composition of existing accepted decisions covering:

* resolved conversation history;
* Region-declared conversation consequences;
* actor-knowledge ownership;
* explicit atomic actor-knowledge addition;
* causally referenced actor-knowledge addition.

If no new ADR is created, document explicitly in the closeout that no ADR was required because the sprint composed existing boundaries without introducing a new ownership or persistence decision.

Do not create ADR-048 merely to restate existing decisions.

## Documentation

Update only relevant documentation, including as appropriate:

* `docs/architecture.md`
* `docs/decisions.md`
* `docs/roadmap.md`
* `docs/simulation_model.md`
* `docs/simulation_principles.md`
* `docs/sprint_log.md`
* `docs/next_chat_handoff.md`
* canonical sprint manifests.

Document precisely that:

* one declared conversation may cause one actor-knowledge addition;
* the accepted conversation entry is the structural causal source;
* membership does not imply truth or belief;
* no conversation-text interpretation occurs;
* duplicate knowledge is a no-op while the conversation still records normally;
* the transition commits atomically;
* no player-facing projection exists.

Reconcile only directly relevant summary drift. Do not perform a broad historical documentation rewrite.

## Verification

Run:

* focused Sprint 10.19 conversation actor-knowledge consequence tests;
* Sprint 10.18 causally referenced actor-knowledge tests;
* Sprint 10.17 source-free mutation tests;
* Sprint 10.16 baseline tests;
* conversation-transition tests;
* conversation-pressure consequence tests;
* conversation actor-relocation consequence tests;
* unresolved-thread consequence tests;
* generic history and causal-integrity tests;
* narration-context isolation tests;
* Scene Snapshot and perception tests;
* World State tests;
* save/load and atomic-load tests;
* GameEngine facade tests;
* complete root repository test inventory;
* Region Pack validation;
* canonical Markdown/YAML/JSON deep comparison;
* repository preflight;
* hardening validation;
* `git diff --check`;
* scripted matching-conversation material-addition smoke;
* repeated-conversation duplicate smoke;
* save/load and post-load duplicate smoke;
* invalid-consequence atomicity smoke;
* malformed-load preservation smoke;
* appropriate direct-launch smoke.

Use temporary or Git-ignored, non-tracked save paths.

Do not overwrite committed save fixtures such as:

```text
saves/savegame.json
```

Record exact commands and actual results.

If the repository preflight again reports agent-execution-context limitations while the same official interpreter successfully runs the required tests, document the distinction precisely rather than treating the environment limitation as an implementation failure.

## Closeout

Only after every required verification passes:

* mark Sprint 10.19 complete in all canonical manifests;
* ensure Markdown, YAML, and JSON deeply agree;
* set `next_sprint` to null;
* leave Sprint 10.20 undefined and unstarted;
* leave all changes uncommitted for owner review.

No owner gameplay playtest is required because the new actor knowledge remains intentionally invisible to the player.

## Post-sprint architecture-review packet

Create:

```text
D:\AI RPG\handoffs\post_sprint_10_19_architecture_review_packet.zip
```

Use a reliable temporary assembly directory or temporary build script.

The packet must include:

### Evidence files

* `packet_manifest.md`
* `review_brief.md`
* `review_context.md`
* `verification_results.txt`
* `git_status.txt`
* `git_log.txt`

Write all evidence files with real newline characters. Do not emit literal PowerShell `` `r`n `` text.

### Canonical records

* `docs/current_sprint.md`
* `docs/current_sprint.yaml`
* `docs/current_sprint.json`
* `docs/next_chat_handoff.md`

### Relevant documentation

* architecture;
* decisions;
* roadmap;
* sprint log;
* simulation model and principles;
* relevant workflow and project-structure documents.

### Implementation and data

* every changed implementation file;
* conversation transition;
* actor-knowledge implementation and candidate helper;
* World State;
* GameEngine;
* history construction and validation;
* narration context;
* save/load;
* Region Pack validation;
* modified Bryn Shander Region Pack data.

### Tests

* all changed tests;
* focused conversation actor-knowledge consequence tests;
* causally referenced actor-knowledge tests;
* source-free actor-knowledge tests;
* actor-knowledge baseline tests;
* affected conversation, history, narration, save/load, World State, and engine tests;
* pressure, actor-location, and unresolved-thread regressions.

Validate:

* every manifest-listed source exists;
* exact ZIP inventory matches `packet_manifest.md`;
* all six required evidence files are present;
* all evidence files contain real line breaks;
* all changed implementation and test files are included;
* the ZIP opens successfully;
* no duplicate ZIP entries exist;
* no unintended files are included;
* temporary assembly, readback, smoke, and build-script files are removed.

Do not commit.

## Required completion report

Report:

* Sprint name and final status;
* branch;
* starting HEAD;
* final HEAD;
* pre-edit Git status;
* final Git status;
* files changed and created;
* exact Region Pack declaration name and schema;
* exact declaration fixture;
* exact validation behavior;
* exact trigger behavior;
* exact candidate helper name and signature;
* relationship to the public Sprint 10.18 operation;
* exact material consequence behavior;
* exact duplicate consequence behavior;
* exact result-packet structure;
* exact conversation and knowledge history ordering;
* exact `source_history_id` behavior;
* exact atomic failure behavior;
* whether existing pressure, relocation, and unresolved-thread consequences still compose atomically;
* World State commit count where verified;
* Scene Snapshot build or replacement behavior;
* save/load behavior;
* compatibility with source-free and existing causally referenced history;
* engine history visibility;
* narration-context exclusion;
* player-visible result;
* focused test commands and results;
* affected regression commands and results;
* complete root test count and result;
* Region Pack validation result;
* canonical manifest comparison result;
* preflight and hardening results;
* scripted smoke results;
* save version;
* whether a new ADR was created and why;
* review-packet path;
* ZIP entry count;
* archive inventory-validation result;
* confirmation all six required evidence files are present;
* confirmation evidence files use real newlines;
* confirmation archive opened successfully;
* confirmation no duplicate entries exist;
* confirmation temporary files were removed;
* whether an owner gameplay playtest was requested;
* whether Sprint 10.20 was defined or started;
* confirmation no commit was created;
* recommended Git commit title.

Recommended commit title:

```text
Complete Sprint 10.19 conversation actor knowledge consequence
```

Do not begin another sprint.
