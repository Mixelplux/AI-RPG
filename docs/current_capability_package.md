# Sprint 10.79 - West-Road Market Causality

## Status and authority
Owner-accepted and complete October 4, 2026. Protected baseline:
`8d52ab0ef763846c598af8af29236475d34f42be` (Character Competence V1).
Branch: `codex/west-road-market-causality`. Risk: Elevated (time and persistence).
Sprint 10.79, Causal Follow-Through V1, is accepted and frozen. `next_sprint`
remains null. Narrative Scenario Quality presentation concerns remain deferred.

## Scope
Prove earlier approach/capability choices affect a later scene through elapsed
time and guard allocation. Two continuous hours of reduced coverage outside
the West-Road focus establish one independent theft of a crate of lamp oil
from a teamster's supply sled near the market approach. World truth belongs
to the deterministic engine; visiting the market reveals an existing event.
Reuse actual phase/allocation semantics and add only specific timing/event
state. Restore coverage ends the interval if the existing path is available.
Use copied candidate transactions and save-version-1 additive normalization;
malformed explicitly present fields reject. No retroactive theft on load.
Keep directly touched West-Road/market presentation concrete and playable.

## Exclusions
No generic scheduler, autonomous town, procedural crime, queues, faction AI,
consequence framework, economy, patrol simulator, new competence, profile UI,
quest chain, broad prose cleanup/refactor or Sprint 10.80. No thief identity,
observer/faction/conspiracy connection or mandatory quest is established.
Sprint 10.78 remains frozen.

## Verification and completion
Exact threshold; ordinary two-hour survey; tactical one-hour headroom followed
by another hour; equivalent composed one-hour activities; existing restoration;
idempotency; before/after save-load and legacy normalization; malformed saves
and command/load rollback; read-only observation and safe local revelation.
Run affected West-Road, time/world, scene/context, discovery/knowledge,
persistence, narration and navigation regressions offline. Generated test
artifacts stay under `.artifacts/`. Owner smoke exposed remote West-Road state
leaking into Market Square; the bounded projection correction was re-verified
and owner re-smoked successfully before acceptance. Real-tokenizer counts remain
unverified because the existing cache is absent; this is a known non-blocking
environment limitation.
