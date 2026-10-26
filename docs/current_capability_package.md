# Physical Traversal Core V1a — M1 accepted and closed

Owner accepted M1 on October 26, 2026 following correction and verification of
both blocking defects. Risk: Elevated. Accepted implementation baseline:
`85ec1811315686f9ea6691235078bf10c25265fc`; the accepted M1 changes remain an
uncommitted working diff on `codex/physical-traversal-v1a-m1`.

M1 establishes reusable World Simulation, Character System and Action & Resolution
foundations under CD-01–CD-09 and PT-D1–PT-D9, including common I1/F05 assessment
and offline rule validation. Acceptance covers the bounded foundations and their
documented limitations; playable consequential traversal and new-domain save
integration remain M2. See the [M1 handoff](physical_traversal_m1_handoff.md),
[implementation model](physical_traversal_m1_design.md) and
[canonical traversal design](design/physical-traversal-domain-design-v1.md).

Lifecycle is complete/idle: no active sprint or capability package, latest
completed sprint `physical-traversal-v1a-m1`, and no next sprint selected.
`docs/current_sprint.json` remains the sole machine lifecycle authority.
M2 is neither staged nor started and requires separate owner authorization.

Preserved for M2: narrow unnecessarily broad Character dependencies; evaluate
named dependency records instead of positional tuples. The accepted realistic
climbing-failure/falling-risk matrix, common consequential acceptance,
continuation and versioned persistence validation requirements remain binding
deferred requirements, not implemented M1 behavior.

No mechanics, persistence model, save version or migration changes follow from
closure. Swimming, jumping, combat, autonomous NPC planning, World Forge and live
providers remain outside scope. Git staging, commit, merge and push require
separate publication authorization; acceptance grants none of those actions.
