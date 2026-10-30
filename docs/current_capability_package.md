# Player Intent Interpretation V1

Owner accepted the Design and authorized bounded implementation October 30, 2026.
Baseline: `870d1080e67c2f943d12a7bd74952d26ed56b5d2`.
The supplied Accepted Design → Implementation Handoff governs this package;
[the contract](design/player-intent-interpretation-v1.md) records its semantics
and the exact serialization chosen within the authorized implementation scope.

Implement only the model-independent interpretation contract, trusted validation,
replaceable invocation and minimal existing Coordinator handoff, with safe
clarification/failure and protection against automatic chaining. Interpret meaning;
F05/Coordinator authorize; domains adjudicate and accept consequences.

Risk: **Elevated**, because this input boundary can lead to cross-domain
consequential gameplay. Preserve the common acceptance/recovery boundary,
envelope V3, schema 4, historical schemas 1–3 and V1/V2 behavior. No migrations,
new mechanics, narration, model experiments, permanent model choice or owner-save
changes. Hosted/local providers remain replaceable; no live calls are authorized.

Only this single implementation milestone is staged. JSON is the sole lifecycle
authority. Stop at a locally verified, uncommitted implementation handoff for owner
review; acceptance, Git staging/commit/publication and any subsequent package
require separate authorization.

Implementation is locally verified and ready for owner review; see the
[handoff](player_intent_interpretation_v1_handoff.md). No acceptance, lifecycle
closure, publication or later milestone is implied by readiness.
