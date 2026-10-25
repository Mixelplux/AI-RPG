# Core Gameplay Domains — documentation incorporation review

Prepared October 25, 2026 for owner review. This is an uncommitted documentation
candidate, not publication or implementation authorization.

## Baseline and authority

Local and actual remote `main` both verified at
`86f0618e81dbfcc09b32233c9ab4c5485c6136dd` via `git rev-parse main` and
`git ls-remote origin refs/heads/main`. The managed isolated worktree uses branch
`codex/core-gameplay-domain-design-docs` at that same HEAD. The original
`D:\AI RPG` checkout remains on the unrelated experimental branch at
`618ad922c15d78d9d413cde73420fe1b0ce686fe`; its dirty changes and owner save were
not copied, edited, staged or reset. Existing worktrees were inventoried and left
in place. The established GitWorkflowTools state tool was used at task start.

The owner authorized repository documentation incorporation only. Source-document
future-work instructions record Design context; they do not authorize a handoff,
package selection, lifecycle staging, implementation, providers, migration or Git
publication in this task. Lifecycle remains complete/idle at M2-M1 with no active
or next sprint/package. No staging, commit, merge or push was performed.

## Exact accepted sources

The owner-supplied Downloads files, whose headers record October 25 acceptance,
were copied byte for byte, retaining their headings, qualifications, examples,
proposed future evidence/sequencing and acceptance statements:

| Supplied filename | Canonical repository record | SHA-256 |
|---|---|---|
| `AI_RPG_Core_Domains_Cross_Domain_Contract_Design_V1_Candidate_2026-10-25.md` | [Cross-Domain Contract Design V1](core-gameplay-domains-cross-domain-contract-design-v1.md) | `d9828d22309736f96d71e87ce24671a836402762b7597ba357f7a324dc3ba8cb` |
| `AI_RPG_Physical_Traversal_Domain_Design_V1_Candidate_2026-10-25.md` | [Physical Traversal Domain Design V1](physical-traversal-domain-design-v1.md) | `3d81e9c14303788319085349ae632d7a15fb9ec96f3d0e70d12b847fda4d01ed` |

All nine CD headings and nine PT headings are present in sequence. The Stage A
four consolidated architectural directions and Stage B consolidated direction
remain intact. Words such as “Proposed” and “candidate” within the accepted sources
are preserved; the explicit acceptance headers/statements establish Design status.
No contents were reconstructed from the earlier HTML shells or inaccessible links.

## Complete proposed file inventory

| Path | Change |
|---|---|
| [core-gameplay-domains-cross-domain-contract-design-v1.md](core-gameplay-domains-cross-domain-contract-design-v1.md) | New, exact Stage A source. |
| [physical-traversal-domain-design-v1.md](physical-traversal-domain-design-v1.md) | New, exact Stage B source. |
| [README.md](README.md) | Index both accepted Design records and this review. |
| [systems/README.md](systems/README.md) | Add accepted Design navigation and status boundary. |
| [systems/system-map.md](systems/system-map.md#core-gameplay-domains-and-physical-traversal--accepted-design) | Add responsibility/contract reconciliation without revising runtime coverage. |
| [core-gameplay-domains-incorporation-review.md](core-gameplay-domains-incorporation-review.md) | This provenance, inventory, reconciliation and verification report. |

All paths above are under `docs/design/`. There are no other proposed changes.

## Reconciliation and material conflicts

The [system-map table](systems/system-map.md#core-gameplay-domains-and-physical-traversal--accepted-design)
connects the accepted sources to individual responsibility manifests and inherited
Design. No material conflict requiring owner resolution was identified:

- Integrated Gameplay Architecture IG-01–IG-18 and IG-20–IG-23 retain domain-owned
  dependency discovery, coherent dependent acceptance, current-premise validation,
  durable recognition, meaningful increments and common-runtime validation.
  IG-19 remains excluded. CD/PT specialize these contracts, not a new coordinator.
- F05 retains chosen methods, available means, ordinary execution, meaningful
  control boundaries and current-circumstance resumption. PT-D4 distinguishes
  no-attempt feasibility from a committed attempt with legitimate costs; it does
  not redefine prior bounded blocked-attempt behavior or require universal costs.
- F01 retains legitimate access, attribution, uncertainty, temporal distinctions,
  outcome fidelity and proportional reliance/correction. Hidden governing facts
  stay internal; presentation repair cannot reroll or republish accepted effects.
- Information Foundation D1–D16 and Adjudication D-A1–D-A6 retain selective
  direct/relationship/history access and the distinction between unspecified,
  established-but-unavailable and uncertain information. Explicit accepted
  adaptations/scoped authored effects do not silently override contradictions.
- World owns external object identity, condition and compatible physical
  relationships; Character owns creature capability, equipment readiness/use and
  legitimate access. Shared PC/NPC relevant rules semantics refine the earlier
  provisional NPC interface direction without selecting a schema or API.
- Actors owns meaningful intention separately from attempt success. Optional NPC
  participation does not require universal agency or make fixture intent an
  implemented actor planner. Persistence stores coherent domain-owned meaning
  without acquiring semantic authority or selecting a new save format/migration.
- Existing finite routine/d6 policies, fixtures and bounded version-2 continuity
  remain implementation evidence. They neither define traversal mechanics nor
  demonstrate complete CD/PT coverage. D&D 2024 with explicit justified adaptations
  is preserved as accepted direction; no rule corpus or adaptation is imported.

The Research handoff and T-R1–T-R11 are inherited references in the supplied
accepted sources, not separately supplied/reconstructed records in this candidate.
Rules-corpus/adaptation detail, content-revision compatibility, later domain detail
and separately authorized implementation remain as scoped in those sources.

## Meaningful no-change determinations

The inherited IG record/plan, F01, F05, Information Foundation and Adjudication
records need no decision edits: the central map links their retained boundaries.
Individual system manifests keep historical review identities, bounded evidence
and Partial classifications; the shared map/index make the new specialization
visible without duplicating accepted text across nine manifests. Shared doctrines,
PROJECT, WORKFLOW, runtime architecture, ADRs and deferred registers require no
revision because no new doctrine, runtime behavior or architectural mechanism is
introduced. Package/sprint records and machine lifecycle are unchanged. No code,
tests, content packs, saves, generated gameplay artifacts or provider calls change.

## Verification

- Passed exact source-byte equality and matching SHA-256 for both copies; nine
  sequential CD decisions and nine sequential PT decisions, acceptance statements
  and consolidated directions retained.
- Passed strict UTF-8 decoding, local Markdown link/anchor checks for the six-file
  candidate, and Markdown whitespace review. Source two-space hard breaks are
  intentional and preserved; no unexpected trailing whitespace or conflict markers.
- Passed `git diff --check` for tracked edits. New untracked files were checked
  separately because ordinary Git diff does not include them.
- Passed established `tools/validate_project_records.ps1`: 8 passed, 0 failed.
  Lifecycle JSON is unchanged and complete/idle; no player-save changes.
- Passed scope and index checks: exactly six Design Markdown paths, empty index,
  unchanged HEAD, no implementation/lifecycle/save changes. Original dirty
  checkout status remains as inventoried; no mutation there was performed.
- Both official reference URLs in Stage B loaded successfully: [Playing the
  Game](https://www.dndbeyond.com/sources/dnd/br-2024/playing-the-game) and [Rules
  Glossary](https://www.dndbeyond.com/sources/dnd/br-2024/rules-glossary/).
  This checks reference accessibility, not a new rules audit or rules import.
- Gameplay tests and live-provider evaluation were not run: no executable behavior
  changed. No formal review packet or committed candidate was requested/created.

Stop at this uncommitted documentation handoff for owner review. Publication and
implementation each require their respective separate authorization.
