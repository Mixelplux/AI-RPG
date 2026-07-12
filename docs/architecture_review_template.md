# Architecture Review Template

Use the lightest review type allowed by `WORKFLOW.md`. The main review is written for the project owner. Technical evidence belongs in the packet or appendix.

## Review Type

State one:

- Sprint health check
- Capability-cluster review
- Deep architecture review

## Plain-Language Outcome

In no more than approximately 800 words, answer:

1. What was completed?
2. Did it work as intended?
3. Was an important defect or risk found?
4. What does the engine now make possible for the game?
5. What should be built next, and why?

Avoid file names, function names, schema details, and test mechanics unless they change the decision. Translate technical findings into consequences for player value, project risk, scope, sequencing, or future flexibility.

## Decision Card

| Question | Answer |
|---|---|
| Recommended capability | |
| Why now | |
| Player or project value | |
| Technical risk | Low, medium, or high |
| Persistence impact | None, compatible extension, or compatibility change |
| New ADR | Required or not required |
| Expected scope | Health check, one bounded sprint, short sequence, or deep design work |
| Major alternatives deferred | |

## Decision Requested

End with exactly one requested decision:

- Accept the recommendation
- Reject the recommendation
- Defer the recommendation
- Request a deeper review of one named issue

Acceptance authorizes later sprint staging around the recommendation. It does not define, stage, or start a sprint.

## Technical Appendix

Omit from the main response unless a material defect exists, persistence or ownership changes, save compatibility is affected, alternatives are close, or the owner requests technical detail.

When needed, keep it clearly separated and cover only decision-relevant evidence:

- verified repository state;
- ownership and atomicity boundaries;
- persistence and save/load effects;
- failure behavior;
- focused verification;
- alternatives and tradeoffs;
- ADR implications.

