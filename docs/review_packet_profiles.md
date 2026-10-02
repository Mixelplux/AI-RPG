# Review Packet Profiles

## Status and Authority

This document defines the optional formal review-packet contract used by the
existing assembly and validation tools. Load it only when a packet is explicitly
requested or required by an agreed risk boundary under `WORKFLOW.md`.
These manifest and evidence requirements apply to that artifact only; they do
not impose routine package scope, file lists, audits, or planning gates. It does
not replace repository architecture, simulation, or lifecycle authorities.

Packet-local synthesis is review convenience only. Its authoritative sources
remain `docs/architecture.md`, `docs/simulation_model.md`,
`docs/simulation_principles.md`, `docs/roadmap.md`, and `docs/decisions.md`.

## Supported Profiles

| Profile | Purpose | Required decision context |
|---|---|---|
| `package-review` | Auditable completed-package evidence. It does not select the next capability. | None beyond package, sprint, verification, Git, implementation, and test evidence. |
| `post-package-architecture-review` | Review a completed package and select, reject, or narrow the next bounded capability. | Owner review brief, architecture snapshot, simulation capability map, one or more structured scenarios, and authoritative architecture, roadmap, decision, and simulation sources. |
| `phase-architecture-review` | Review phase-level sequencing, ownership, dependency, or boundary decisions. | All post-package context plus broader scenarios, an explicit dependency map, ADR index, and unresolved phase-decision context. |

## Member Roles and Artifact Kinds

Every archive member declares one semantic role and one artifact kind.
Supported kinds are `authoritative_source`, `packet_synthesis`, `evidence`,
`implementation`, `test`, and `manifest`.

The validator enforces the role-to-kind mapping: packet, package, sprint,
verification, Git, and supporting-evidence roles use their declared evidence or
manifest kind; authored review, map, scenario, dependency, ADR, and phase
context roles use `packet_synthesis`; authoritative roles use
`authoritative_source`; implementation and test roles use `implementation` and
`test`. A role is valid only in the profile that permits it. This prevents a
synthesis role from being relabeled as ordinary evidence to bypass source pins.

Required roles by profile are defined in the validator. Their role names are:

- all profiles: `packet_manifest`, `package_record`, `sprint_record`,
  `verification_evidence`, `git_evidence`;
- architecture and phase profiles: `owner_review_brief`,
  `architecture_snapshot`, `simulation_capability_map`,
  `simulation_scenarios`, `authoritative_architecture_source`,
  `authoritative_simulation_source`,
  `authoritative_simulation_principles_source`,
  `authoritative_roadmap_source`, and `authoritative_decision_source`;
- phase profile additionally: `capability_dependency_map`,
  `architecture_decision_index`, and `phase_decision_context`.

`implementation_source` and `test_source` are permitted and expected when
relevant, but no fixed filename or count is imposed.

## Version 1 Manifest Contract

Every new profiled packet contains one root-level `review_packet_manifest.json`.
It is the sole `packet_manifest` member and is included in its own ordered
member list. The manifest contains:

- `schema_version` (`1.0.0`);
- `profile`, `packet_id`, `review_identity`, and `reviewed_head`;
- `creation_source_state` with repository-relative branch, HEAD, and status;
- ordered `members`, each with `path`, `role`, `artifact_kind`, and `sha256`;
- `repository_path` on each authoritative-source member, bound to the
  authoritative role as follows: `authoritative_architecture_source` to
  `docs/architecture.md`, `authoritative_simulation_source` to
  `docs/simulation_model.md`, `authoritative_simulation_principles_source` to
  `docs/simulation_principles.md`, `authoritative_roadmap_source` to
  `docs/roadmap.md`, and `authoritative_decision_source` to
  `docs/decisions.md`;
- `sources` on every `packet_synthesis` member, each containing a
  repository-relative `repository_path` and its `sha256` pin;
- `verification_evidence_path` and `git_evidence_path`; and
- `legacy` set to `false`.

Portable archive paths use forward slashes, are relative, and must not contain
empty segments, drive prefixes, `.` or `..` segments, trailing slashes, or
backslashes. Directory entries are rejected.

The manifest checksum for itself is the SHA-256 of its canonical JSON form with
the manifest member's `sha256` value set to `SELF`. The validator reproduces
that canonical form before accepting it.

`reviewed_head`, `creation_source_state.head`, the single `HEAD:` value in Git
evidence, and (when a repository root is supplied) the candidate repository
HEAD must agree exactly. The corresponding branch fields must also agree.

## Authored Review Inputs

Assembly never creates strategic recommendations, candidate capabilities,
dependency judgments, scenario conclusions, unresolved questions, or owner
decisions. Those are authored packet inputs.

Architecture and phase review briefs use the sections in
`docs/architecture_review_template.md`. They must contain exactly one
`## Owner Decision Request` heading and all required headings listed there.

Each scenario document uses one or more `## Scenario` sections. Each section
contains `### Initial State`, `### Trigger`, `### Authoritative State
Transitions`, `### Causal History`, `### Player-Facing Projection`, and
`### Decision Relevance`. A phase packet requires two or more scenario sections.

Every required member must contain substantive content. Empty, whitespace-only,
and placeholder-only records fail. An owner brief requires each template
heading exactly once and exactly one substantive `## Owner Decision Request`
whose body asks to accept, reject, defer, or request a deeper review.

Phase-only synthesis roles have separate content contracts. A
`capability_dependency_map` contains exactly one `## Capability Dependencies`
section and a populated `Capability | Dependencies | Decision Relevance` table.
An `architecture_decision_index` contains exactly one `## ADR Index` section
and a populated `ADR Identifier | Status | Decision Relevance` table; each ADR
status is accepted, proposed, deferred, or superseded. A
`phase_decision_context` contains substantive `## Unresolved Phase Questions`,
`## Alternatives`, and `## Decision Context` sections. Generic architecture or
simulation-map text cannot satisfy any of these phase-only roles.

## Synthesis and Freshness

Every packet-synthesis member pins every required authority in its manifest
sources. Architecture snapshots and simulation capability maps also name their
repository authorities in the authored document. With `-RepoRoot`, the
validator checks each pin's current repository hash, checks each bundled
authoritative member's bytes against its role-bound repository path, and rejects
unbundled or missing authority pins. A mismatch is stale and fails validation;
source material is not silently promoted to a new authority.

## Legacy Archives

Existing archives are legacy and remain unchanged. `-Legacy` validation checks
ZIP readability, safe paths, and duplicates, and may compare a simple
self-declared inventory. It does not claim that an old archive meets this
profile contract.
