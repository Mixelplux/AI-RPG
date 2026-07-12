# Evidence Trace Foundations

Status: Complete.

## Owner-Visible Value

The engine can retain grounded, simulation-owned traces of accepted events for
future discovery systems. This package establishes trusted hidden state only;
it does not decide whether a trace is noticed, interpreted, believed, or acted
upon.

## Accepted Internal Milestones

1. Sprint 10.20 — persistent located evidence-trace representation.
2. Sprint 10.21 — explicit atomic evidence-trace creation.
3. Sprint 10.22 — causally referenced evidence-trace creation.
4. Sprint 10.23 — one declared resolved-conversation evidence-trace consequence.
5. Sprint 10.24 — defensive inspection and package closeout.

## Boundaries

- Persistence impact: one sparse World State `evidence_traces` collection;
  save version remains `1`, with candidate-load-only missing-field normalization.
- Player-facing impact: none. Traces remain outside scene, perception,
  narration, dialogue, targeting, CLI, and gameplay behavior.
- Architecture: one ADR establishes World State ownership, identity, location,
  opaque content semantics, duplicate behavior, persistence, copying, and
  non-projection boundaries.
- Exclusions: discovery, investigation, interpretation, reliability or belief,
  actor reactions, removal or decay, generic frameworks, automatic event rules,
  and all work outside Sprints 10.20–10.24.

## Verification and Stop Conditions

Each milestone requires focused tests, affected regressions, manifest agreement,
and `git diff --check` before its checkpoint. Final closeout requires the full
repository verification cycle and one review packet.

Stop for conflicting authority, a different ownership model, a save-version
change, generic framework or broad refactor, unsafe conversation composition,
unapproved player-visible behavior, excluded discovery or interpretation work,
material repository ambiguity, irreversible risk, or an unresolved required
failure outside package scope.

## Recovery and Git

Feature branch: `feature/evidence-trace-foundations`.

Each accepted milestone is a focused checkpoint commit after verification. The
package is removable by reverting its feature-branch commits. Do not merge,
rebase, force-push, or begin another package without owner approval.
