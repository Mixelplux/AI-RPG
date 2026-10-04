# Sprint 10.79 - West-Road Market Causality

## Status
Complete, owner-accepted October 4, 2026. Elevated risk. Implementation branch:
`codex/west-road-market-causality`; protected baseline:
`8d52ab0ef763846c598af8af29236475d34f42be`.
Sprint 10.79, Causal Follow-Through V1, is complete and frozen; `next_sprint`
remains null. Narrative Scenario Quality presentation concerns remain deferred.

## Milestone
Implement and verify the bounded two-continuous-hour reduced-coverage theft
and its later market revelation. Scope and exclusions are in
`docs/current_capability_package.md`. Sprint 10.78 remains complete and frozen.
Implementation and bounded completion review passed after a small malformed-load
rejection correction. Owner smoke confirmed the principal causal cases and
exposed remote West-Road state leaking into unrelated current-scene prose.
The bounded road/gate projection correction and affected offline verification
passed; owner re-smoke then confirmed Market Square no longer exposes remote
West-Road state while North Gate still shows relevant road state. Owner accepted
the sprint after the correction and re-smoke. The projection defect is closed.
See `docs/sprint_10_79_handoff.md` for actual
allocation/timing, compatibility, observed causal cases and verification.
Real-tokenizer counts remain unverified because the existing cache is absent;
offline narration contracts passed and no live provider was contacted.
