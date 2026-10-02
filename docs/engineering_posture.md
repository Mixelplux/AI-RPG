# Proportional Engineering Posture

This small local single-player narrative RPG uses the minimum process justified
by credible consequence and recovery difficulty. Keep packages small and
coherent, one bounded task at a time, with an identifiable accepted Git baseline
and focused automated tests. `WORKFLOW.md` owns execution and lifecycle rules.

| Level | When it applies | Verification and review |
|---|---|---|
| **Routine (default)** | Localized gameplay, deterministic presentation, queries/read models, commands, narrow player improvements, and small contained refactors needed by an approved feature. | Relevant syntax/static checks, focused tests, directly relevant nearby regressions, diff checks and scope review; owner smoke for player-visible behavior. |
| **Elevated** | Persisted World State structure/semantics, save/load compatibility or migrations, Region Pack contracts/formats, major layer ownership, core time/movement/history/causality rules, or meaningful cross-system consequences. | Add broader affected-system regressions, targeted architecture review, explicit compatibility checks, and migration/recovery checks where applicable. |
| **Critical (rare)** | Destructive migration/data-loss risk, security-sensitive provider integration, credentials/secrets, untrusted external execution, or comparable high-consequence boundaries. | May justify deep adversarial review, broad verification, explicit evidence capture, and stricter agreed approval boundaries. |

Classify by actual impact, not a filename or subsystem label. Local movement
presentation may be Routine; changing core traversal semantics is Elevated;
destructive save conversion may be Critical. Ordinary ambiguity does not
automatically make work Critical. Resolve material risk before dependent work;
reclassify if evidence reveals materially different consequences.

Routine work has no default independent audit, exhaustive repository-wide
regression run, formal evidence package, ADR, exact immutable file manifest,
multiple review gates, or broad architecture revalidation. Escalation needs a
concrete reason. Expected files guide navigation; capability and subsystems
define scope.

Documentation, tests, and workflow maintenance are normally Routine unless
their actual consequences meet an Elevated or Critical boundary.

## Safeguards at Every Level

- Deterministic World State is simulation truth.
- Region Packs are authored/canonical inputs, not runtime mutation targets.
- Player-visible scene, perception, and presentation remain derived and
  player-safe.
- Provider/LLM output is untrusted and non-authoritative; requests remain
  explicit and isolated, with fail-closed behavior.
- Persistent transitions preserve atomicity; save compatibility and version
  changes are deliberate and authorized when needed.
- Lifecycle JSON is authoritative; stale prose cannot authorize work.
- The owner authorizes each new capability package. Authorized reversible
  work may finish without repeated intermediate approvals.
- Owner smoke/acceptance and Git authorization remain separate decisions.

Tooling/environment failure blocks the affected check; it does not prove a
product failure. Preserve GitWorkflowTools and Windows recovery procedures.
Do not add infrastructure merely to support more process.
