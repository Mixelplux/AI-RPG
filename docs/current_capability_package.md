# One OpenAI Responses Narration Preview Source

Status: Complete - ready for owner review.

## Value and Scope

The explicit `narration preview <player input>` path will use one real OpenAI
Responses source instead of fixed sample prose. The source remains optional,
untrusted, read-only, nonauthoritative, synchronous, and replaceable. Normal
gameplay never waits for or calls it.

## Included Milestones

1. Stage Sprint 10.57 and verify the dependency/tokenizer preflight.
2. Add one adapter-local OpenAI source and bounded fail-closed pipeline path.
3. Prove request adaptation, local limits, response handling, no-network fake
   tests, regressions, one opt-in smoke request, ADR, and archive closeout.

## Decisions and Impacts

The fixed model is `gpt-4.1-mini with no reasoning field`; generation uses the synchronous Responses
API with a 20-second timeout, zero automatic retries, no storage, no tools,
no provider conversation state, an 8,000-token local input ceiling, and a
256-token output ceiling. Accepted provider text still passes the existing
source-result and narration-output boundaries. Save version remains 1.

## Exclusions and Rollback

No provider framework, second model/provider, streaming, retrying,
asynchronous/background work, routine gameplay use, persistence, cache,
World State/history mutation, save migration, generic tokenizer system, or
following package is permitted. Replacing the adapter with the prior fixed
source removes provider access without durable rollback.

## Verification and Completion

Automated tests inject a fake transport and must make zero real requests. One
separately invoked live smoke request is permitted after deterministic checks.
Completion requires full verification, ADR-058, canonical-record agreement,
a clean committed review candidate, and an independently validated
package-review archive. No next package is selected.
