# Architecture Review Template

Use this template when it helps an owner-requested architecture review. Routine
reviews may use a concise diff and verification report; this template is required
only for explicitly requested formal architecture packets, whose existing
content contract remains in `docs/review_packet_profiles.md`. Review depth
follows `docs/engineering_posture.md`. Technical evidence belongs in an optional
appendix or requested packet.

## Review Type

State one:

- Sprint health check
- Capability-cluster review
- Deep architecture review

## Review Purpose

State the package or phase boundary and why this review is needed.

## Authoritative Repository State

State reviewed branch and HEAD, the completed package boundary, and the
authoritative architecture and simulation sources used by the brief.

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

## Owner Decision Request

End with exactly one requested decision:

- Accept the recommendation
- Reject the recommendation
- Defer the recommendation
- Request a deeper review of one named issue

Acceptance of review findings does not authorize a new capability package or
Git operation. Package selection/opening and Git authorization remain separate
owner decisions. A recommendation does not define, stage, or start a sprint.

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
