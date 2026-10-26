# M2-1 authoritative acceptance and persistence model

Implementation model, October 26, 2026; owner review pending. Authority: the
owner's M2-1 instruction, CD-01–09, PT-D1–09 and IG-07/08/20/21. Elevated risk.
Established before incompatible writes; this is not a change to accepted Design.

The existing consequential `Runtime` gains an explicit new-domain campaign mode.
Its single immutable campaign root is the authoritative aggregate. It replaces
the finite I2/I3 representation for this mode, rather than embedding a traversal
store alongside a legacy GameEngine world. Modes are mutually exclusive. The
legacy runtime and v1/v2 readers keep their existing meaning.

World owns PhysicalFrame (position, time, surfaces, objects, relationships and
causal records). Character owns CreatureRules (capability, expenditure, equipment
readiness and legitimate access). Action owns accepted attempt identity and its
mechanical result. Scoped activity authorization/checkpoints preserve F05 limits.
Storage and coordination acquire none of those semantic authorities.

An increment reads domain-owned named dependencies, resolves M1 mechanics, and
prepares dependent World position/time and Character movement expenditure plus
the accepted result and safe receipt. All construction, owner validation,
aggregate/reference validation and receipt validation precede one root assignment.
Immediately before publication the captured root must still be current. No
callbacks or other fallible operations follow that assignment. Exact accepted
retry recognition precedes present-position checks; reused identity with changed
meaning rejects. A fresh attempt identity must meet current premises and F05.
Exact request field types are validated before any accepted-identity lookup.
Checkpoint `resolution_ref` must be null: M2-1 has no separate checkpoint result
reuse semantics. Non-null references, including actual accepted IDs, explicitly
reject during initial validation, restoration and execution authorization. Accepted
command retries use the accepted-unit history instead; no missing result is invented.

M2-1 supports deterministic full links between meaningful established positions,
with explicitly grounded elapsed seconds, not a universal six-second movement
loop. Unsupported check-bearing or partial-link execution stops before sampling.
No unsuccessful objective is silently accepted as safe. Existing M1 checks/falls
remain available as provisional mechanics. Hazardous failures, protected falls,
interruption and richer progression are subsequent M2 work; they can contribute
additional owner-validated fields/results to the same accepted-unit/root contract.

The version-3 envelope is explicitly opt-in and contains a separately versioned
domain campaign. It stores initial domain premises once, current domains, scoped
authorizations and consequential accepted units with named dependency evidence
and safe receipts. A finite non-executable codec rejects unknown records/fields.
The v3 file reader rejects duplicate JSON keys at every object depth, including
conflicting envelope versions in either order. V1/v2 decoding behavior is preserved.
Restoration validates types, reference closure, mechanical/cost/time/identity and
receipt meaning by pure reconstruction without randomness, then compares the
complete reconstructed state before adoption. Failed restoration never replaces
a live root. Missing traversal state in v1/v2 remains unsupported, never invented.

Saving validates and encodes before the established same-directory temporary
write, flush/fsync and atomic replacement. Failure preserves the prior destination
and live root. No autosave, migration, cross-process exactly-once guarantee or
directory power-loss durability is claimed.

Dependency discovery reads selected route/surface/means/creature records. A
deterministic climb needs no Strength/Athletics statistics. Named evidence allows
later selective retrieval and indexes without changing gameplay meaning. Current
local tuple scans, whole snapshot serialization and repeated growing-history
scans during reconstruction are scaling limits; validation is not linear in
accepted-unit count. No graph database or exhaustive event
ledger is introduced. Full authored composition remains upstream: validated
suppliers must compose applicable bindings; unresolved bindings fail closed.
