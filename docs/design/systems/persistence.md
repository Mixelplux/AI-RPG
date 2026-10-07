# Persistence — Design Manifest

## Status

- Overall: **Partial** — supported campaign state, copied-load normalization and
  reconstruction exist; disk durability and content revision compatibility have
  material limits.
- Last materially reviewed: October 6, 2026, protected baseline
  `1566af02db59c2c9dd5262f589d8255426a30086`.
- Review candidate. Relevant decisions: ADR-012/013, 025/026, 036/038,
  043–050 and 059–061 in the [decision ledger](../../decisions.md), plus
  [10.79 causal continuity](../../sprint_10_79_handoff.md) and
  [10.80 presentation continuity](../../sprint_10_80_handoff.md).

This living responsibility model follows the [manifest framework](README.md).
It authorizes no runtime changes, new storage model, migration or next package.
The six protected manifests retain their responsibility boundaries.

## Purpose

Preserve supported accepted campaign meaning across explicit save/load and
process boundaries. Own its stored representation, restoration and compatibility
handling, handing coherent state back to the systems that give it meaning.

## Player-facing goal

Resume with established choices, findings, costs, commitments and consequences
intact. A technical restart should not reroll an accepted attempt, forget a
shared report or erase an accumulated causal condition present in the save.
This direction does not promise recovery of unsaved play or every incidental
detail previously expressed in prose.

## Authority

Persistence is cross-cutting storage/restoration/compatibility authority. It
decides how supported representations are written, read, deliberately normalized
or rejected, and reconstructed for use. Gameplay owners supply the legitimate
state and semantic integrity requirements. Current validation is distributed
across state and domain modules; this responsibility does not require moving it.

Simulation owns consequential truth; untrusted provider output has no simulation
authority. Restoring state cannot become a new path for adjudicating outcomes or
inventing missing decisions. Storage in `world_state` transfers neither every
nested field to World Simulation nor its fictional authority to Persistence.

## Explicit non-authority

Persistence does not decide what facts exist, which changes are legitimate, what
a character knows or retains, what an attempt achieved, what an actor intends,
or what a scenario phase means. It does not choose narrative relevance, maintain
a second prose-based world, author content, parse commands or design save menus.
Future gameplay owners must establish any new continuity requirement before its
representation is selected. A save field is not evidence that a general gameplay
system exists.

## Governing principles

Apply the [shared doctrines](README.md#shared-doctrines), especially Fictional
Continuity Is Independent of Technical Boundaries and Sparse Epistemic State,
with ADR-012, ADR-059 and Story-First Part I.

- **Preserve accepted meaning.** Owning systems determine which consequential
  facts and provenance must survive; temporary implementation objects need not.
- **Restore before publish.** Validate and reconstruct a replacement session
  before adopting it. This is distinct from atomic replacement of a disk file.
- **Rebuild reliable derivations.** Scenes and projections derive from supported
  saved state plus content. Rebuilding must not replay gameplay consequences.
- **Technical restart is not fictional reset.** Loading supported state does not
  itself advance fictional time or reacquire information. Explicit new-game reset
  has a different purpose.
- **Compatibility is deliberate.** Known absent fields may normalize; unsupported
  representations reject. Rejection is not migration, and normalization is not
  permission to repair arbitrary damage or invent missing history.
- **Content is referenced.** Current saves do not duplicate the authored setting.
  This implemented choice has revision-compatibility limits, not a guarantee that
  any future source at the same path preserves meaning.

## Current model

Three **Provisional** conceptual responsibilities suffice; no runtime module split
or general serialization framework is selected.

| Responsibility | Present grounding and limit |
|---|---|
| Durable campaign state | Store supported accepted state and required references. Version-1 JSON exists; crash-safe disk replacement does not. “Durable” identifies intended continuity, not an fsync guarantee. |
| Restoration and reconstruction | Build a coherent engine from validated state and current referenced content, then adopt it. Derived scenes exist; arbitrary runtime objects and provider state are not restored. |
| Compatibility | Apply explicit version, shape, reference and domain checks, with narrow copied-load normalization. No general migration or content revision policy exists. |

## Resolution depth

Persistence supports the specificity selected by gameplay owners; it does not
escalate every observed detail into a record. Store accepted meaning that cannot
be reconstructed reliably, and rebuild derived state from authoritative saved
state plus supported content. Current sparse actor positions and membership,
accepted attempts and coverage timing exemplify this principle.

Ordinary inferred familiarity, background activity and descriptive props do not
need a ledger merely to make prose consistent. Conversely, a known causal
condition cannot be dropped because it is currently offscreen. General lazy
reconciliation, incidental-detail promotion and retention policy remain with
their owners and are not implemented by loading.

## State and lifecycle

### What a save represents

`build_save_data` emits exactly `save_version`, `region_path` and `world_state`.
The supported version is `1`; the state is defensively copied. Conceptually this
is a supported campaign-state envelope: mutable records and sparse overlays,
with a reference back to authored foundations. It is not a self-contained world
archive, frozen content pack, event-sourced reconstruction or engine snapshot.

| Kind | Stored or reconstructed meaning |
|---|---|
| Accepted fictional state | Player location and competence tags; weather/time; pressures; actor overrides and knowledge; traces/discoveries; open/resolved threads; history; supported scenario, attempt and theft records. Their respective gameplay owners retain semantics. |
| Authored foundations | Region path is stored. Locations/topology, names, descriptions, actor profiles, faction definitions, declarations and reply/clue wording reload from content. No complete mutable relationship, faction, inventory or character-sheet state exists. |
| Derived runtime state | Scene snapshot, effective actor presence, deterministic spawned template instances, perception, opportunities, competence projections and recap rebuild from state/content. Recognition is derived; accepted findings are retained. |
| Ephemeral presentation | Current-scene sentence claims, previous presentation conditions, attention stage, current input and last-displayed narration are session-only. No generated transcript or visited-location prose memory is saved. |
| Infrastructure | Provider transport/configuration, requests, credentials, process objects and PRNG state are not campaign save state. Persistence does not make provider memory authoritative. |

The writer copies the whole supported state container rather than selecting a
strict allowlist of its top-level fields. Unknown extensions are not thereby
recognized gameplay features or a stable compatibility contract.

### Restoration and failure isolation

The implemented sequence is:

1. Read the requested file as UTF-8 JSON and deep-copy the parsed payload.
2. Check the version and presence of `region_path`/`world_state`; require a
   dictionary state and player record. Apply the specific missing-field defaults
   below, then validate state without a region.
3. Construct a separate `GameEngine`: read content at the saved region path,
   validate recognized Region Pack structure, validate state against that content
   and validate pressure scopes/provenance, then defensively copy state.
4. Build the current scene. This resolves the saved player location, effective
   static actors, deterministic spawns and current state/content overlays.
5. Return the completed engine. `GameEngine.load` delegates through `GameSession`
   and only then calls `_replace_runtime_state` to adopt region path, region,
   world state and scene. Other projections are derived when requested.

File, parse, validation and scene-construction failures before adoption leave the
existing engine intact. Tests explicitly retain world/scene identity and save
bytes for rejected loads, including an injected scene-build failure. Loading
does not write the source save, even when normalization succeeds.

This is bounded synchronous failure isolation, not a database transaction or
concurrent-reader guarantee. `_replace_runtime_state` uses successive assignments
and copy getters; no rollback covers an arbitrary failure within that final
adoption itself. Similarly, gameplay's candidate validation/build/publication
protects supported transitions before saving but does not establish disk safety.

### Compatibility and normalization

All defaults below apply only to a copied loaded payload when a field is absent;
present malformed supported values reject. Later cross-record validation can
still reject a normalized payload whose remaining records require missing facts.

| Missing version-1 material | Current behavior |
|---|---|
| `pressures`, `actor_location_overrides`, `open_threads`, `resolved_threads`, `actor_knowledge` | Normalize to `{}`. Pressure and actor-knowledge seeds are not reapplied from content. |
| `evidence_traces`, `player_discoveries`, `player.competences` | Normalize to `[]`; no discovery, capability or history is invented. |
| `competence_attempts` | Normalize to `{}`. Historical ordinary pursuit needs no synthetic competence attempt. |
| `west_road_market_theft`, when a predicament record exists | Add the initial incident record. If coverage is already reduced, start its interval at saved elapsed time; otherwise leave the interval absent. Do not count old hours retroactively. Existing theft history without its record rejects. |
| `west_road_predicament` with revised West-Road content | Reject the unsupported prototype situation with the explicit new-game message under ADR-060. Do not choose a branch. |

`player.current_location_id`, weather and time are required; they are not supplied
from new-game defaults on load. History is not universally required by the base
shape check and is not synthesized. Existing history IDs are preserved, not
renumbered. Recognized linked/scenario records impose their own history needs;
this is not a promise to accept every historical payload lacking IDs or history.

Missing/unequal save versions reject. The current check is Python equality with
`1`, not a strict integer type check (JSON `true` and `1.0` compare equal).
Only version 1 has an implementation; there is no dispatcher for conversions.
Save-format version, a pack's descriptive `version`, and scenario requirements
are distinct. Pack version is not saved or negotiated; version 1 alone does not
guarantee compatibility with revised content. Normalization, intentional
incompatibility, future migration and damage repair must remain separate concepts.

### Accepted attempts, social state and causality

Competence saves preserve one record per supported operation with draw/result,
specialist basis, time cost, findings and source/time/outcome history references.
Validation checks types, supported operation, rule-consistent result/cost,
agreement with current competence tags, mirrored result history, causal order,
findings and applicable physical evidence/coordination. Replay returns the stored
accepted result before eligibility or drawing, without paying again or publishing
consequences again. Validation checks consistency; it does not reroll or replace
the result. Display text can still change with content. There is no universal
action ledger, stored PRNG stream or protection against loading a pre-attempt save.

Actor membership and discovered IDs preserve supported informational access;
Persistence does not infer familiarity, retention, truth or belief from them.
Static actor overrides retain accepted positions, with absence meaning the
authored baseline. West-Road phase, last outcome, commitments, report membership,
sharing history and named witnesses preserve the bounded scenario's social
continuity. They do not imply persisted general motives, relationships or goals.

The theft record stores coverage start and incident history reference; elapsed
time and referenced history preserve the qualifying interval and established
incident. Save/load before the threshold retains accumulated supported hours;
later time can cross it once. Restoring coverage stops an uncompleted interval
without erasing a theft that already occurred. Loading does not simulate offline
wall-clock time, replay threshold effects or identify a thief. Legacy timing
normalization is the explicit exception where an earlier duration was never
recorded; it begins tracking at the saved time without inventing a past incident.

### Content references and changed defaults

The region path is stored as supplied and opened as supplied. Relative paths
resolve against the process working directory, not the save file's directory;
absolute paths also work through ordinary file handling. There is no pack search,
path rebasing, frozen copy, checksum, revision pin or content-migration layer.
Missing content prevents reconstruction; malformed content or broken supported
references can reject it before adoption. Changing the working directory can
therefore break a relative reference even when the save itself is available.

Saved weather/time and current membership/pressures replace initialization, not
merge with new seeds. Saved actor overrides win over baseline positions, but an
override that now equals an edited baseline rejects as redundant. Actors without
overrides follow the newly loaded baseline. Source-only descriptions, names,
topology and clue/report text can change an existing campaign's derived views.
Structural validation cannot detect every change of meaning under unchanged IDs.

References have local contracts: location IDs must resolve where consumed;
actor keys must identify static actors; discoveries must remain declared; trace
IDs are unique with valid locations; pressure scopes/provenance match the region;
threads must match declarations and causal history. Generic evidence/knowledge
IDs remain opaque. Competence operation names and fixed West-Road IDs have narrow
scenario meaning. There is no universal entity namespace or complete historical
reference validator. Stable keys are necessary but insufficient for semantic
content compatibility.

### History, narrative and technical sessions

History is a persisted ordered list of accepted events, not just diagnostic
logging. Stable `history_id` and backward `source_history_id` references support
later integrity checks; scenario outcomes, attempts, thread lifecycle and theft
timing require particular records. Optional older unlinked events remain valid.
New history avoids reusing existing IDs after load. General source links establish
structural provenance; specific owners add stronger semantic constraints.

Conversation/movement summaries also aid inspection and bounded narration context.
They are not transcripts or exhaustive character memory. History queries default
to ten entries and context packets cap at 25; those are read limits, not storage
pruning. The whole current history list is copied/serialized. No retention cap,
compaction or event replay engine is implemented; no measured size bottleneck is
established by this review. Any future reduction must preserve owner-required
references and meaning, rather than treating all history as disposable logs or
requiring all conceivable events forever.

`Previously:` is rebuilt from West-Road phase, discoveries and reports. It is a
bounded reorientation aid, not complete narrative continuity or exact attempt
recap: the route-found phase can describe following the route after a guarded
survey. The accepted attempt remains correctly stored; recap fidelity belongs
to Narrative Experience. Saving more prose is not a necessary correction.

CLI startup creates a new game; it does not auto-load. `save`/`load` use the fixed
`saves/savegame.json`; engine functions accept explicit paths, allowing callers
to use different files without a slot catalog or management UI. Quit does not
autosave. Successful load clears presentation continuity and refreshes the scene;
failed load does not intentionally clear it. `reset` constructs fresh state from
the current region path and clears presentation continuity; it does not delete or
overwrite a save until an explicit save. Clearing a cache alone neither resets
the campaign nor advances time. A process restart can recover only saved state.

## Inputs

Accepted supported state from gameplay owners; explicit save/load paths; persisted
JSON to validate; currently referenced authored content; and the engine's known
format/domain compatibility rules. File contents are data to validate, not an
instruction source. Generated prose is not a candidate campaign-state input.

## Outputs

A version-1 JSON file, a reconstructed engine or adopted runtime state, or a
failure. Supported references and accepted meanings return to gameplay owners;
scenes and player-safe views derive from them. Compatibility errors do not
silently repair state or authorize a new fictional outcome.

## Relationships

See the [Persistence information flow](system-map.md#dependencies-and-information-flow-around-persistence).

| System | Ownership retained outside Persistence |
|---|---|
| [World Simulation](world-simulation.md) | External state, legitimate change and causal progression. Persistence preserves their supported state and provenance. |
| [Character System](character-system.md) | Capability, informational access and selective retention. Persistence preserves records without choosing knowledge or familiarity. |
| [Action & Resolution](action-resolution.md) | Accepted attempt semantics, cost and result. Persistence preserves replay-relevant meaning without adjudication. |
| [Actors & Social Dynamics](actors-social-dynamics.md) | Intentional choices and consequential social meaning. Supported reports/commitments survive; general social storage remains provisional. |
| [Scenario & Authored Content](scenario-authored-content.md) | Authored foundations and declarations. Persistence reloads their reference; safe evolution of content is a shared unresolved compatibility interface. |
| [Narrative Experience](narrative-experience.md) | Selection, expression and reorientation from restored truth. No prose cache or provider memory becomes authoritative save state. |
| Player Presentation | Initiates save/load/reset and communicates status/errors; command parsing and save UI remain outside Persistence. |

## Player-facing projection

The CLI reports save/load/reset success, missing save and caught `ValueError`
failures, then shows supported recap/scene after a successful load. Internal
history and causal records do not automatically become character knowledge.
Error handling is incomplete: save/reset errors and load exceptions outside
`FileNotFoundError`/`ValueError` are not uniformly converted into friendly messages.
This is a presentation/diagnostics limit, not authority to accept invalid state.

## Current implementation

### Disk durability

`save_game` builds/validates the payload before opening the destination, creates
parent directories, then opens the destination with `"w"` and calls `json.dump`.
There is no temporary save, explicit fsync, atomic rename/replacement, backup or
recovery copy. Closing the file is not a crash-durability protocol. Validation
failure before opening avoids truncation; a serialization or I/O failure after
opening, or interruption during writing, can leave a damaged/truncated destination.

This is a concrete local-game save-loss risk, distinct from the guarded gameplay
candidate and load-reconstruction patterns. It does not warrant describing the
project as a distributed storage system. Atomic file replacement/backups require
separate authorization; this review records the limitation without implementing it.

### Validation and trust limits

JSON parsing does not execute serialized Python objects. Domain validators reject
many malformed records and contradictory causal relationships. However, there
is no uniform exact envelope schema, file-size/depth limit, path allowlist or
hostile-import boundary. A non-object top-level JSON value can fail at `.get`;
region-path type/meaning is not explicitly checked before file use. Weather/time
and generic history receive uneven validation outside specific domain consumers.
Unknown envelope fields are ignored by construction; unknown state fields are
not blanket-rejected and may be copied through. Exact key checks apply to several
recognized records, not every object. Successful structural validation does not
prove every saved assertion or authored sentence semantically valid.

The implemented context is explicit local single-player file use. These limits
should guide a future real import/sharing requirement if one arises; they do not
authorize a generalized security project or imply all errors are gracefully caught.

| Capability | Classification |
|---|---|
| Version-1 save/read and supported state continuity | **Implemented**, bounded by domain checks and explicit file operations. |
| Candidate reconstruction and pre-adoption load failure isolation | **Implemented**, synchronous and scoped as described above. |
| Compatibility | **Partial:** deliberate additive normalization and rejection; no general migration or content revision negotiation. |
| Durable storage safety | **Partial:** ordinary successful writes exist; prior-save preservation on write failure is not guaranteed. |
| Sparse continuity and ownership separation | **Accepted design**, with the listed bounded implementations. |
| Three-part decomposition and broader owner interfaces | **Provisional**, not prescribed modules or a new schema. |
| Atomic disk replacement, backup/recovery, migrations, pinning, save management and general history reduction | **Deferred**; nothing is selected or scheduled by this manifest. |

## Accepted decisions

ADR-012 separates persisted World State from rebuilt scenes; ADR-013 establishes
session construction through the gameplay facade. ADR-025/038 preserve stable
history and backward references. ADR-036/043–050 define specific sparse records
and normalization; ADR-060 intentionally rejects prototype state; ADR-061
preserves accepted attempts. ADR-059 and shared continuity doctrine explain why
storage follows consequential need without becoming exhaustive memory.

These decisions support preserving accepted meaning and restoring before
publication. They do not establish atomic disk writing, automatic content
migration, all-event retention or narrator-owned truth.

## Provisional decisions

Durable campaign state / restoration and reconstruction / compatibility is the
smallest useful working model. How future owners declare compatible historical
meaning, or select records that cannot be rebuilt, remains unsettled. No serializer
registry, migration framework, content bundle format or storage partition is chosen.

## Deferred capabilities

Crash-safe file replacement and recovery, backups, autosave, slot UI/catalog,
portable path resolution, content pinning/migration, general save repair,
history compaction, character replacement, general social persistence and durable
generated prose. Player Presentation remains a later manifest. No runtime,
validator, test, content, save or lifecycle edits follow from this review.

## Known tensions / open questions

- **Disk gap:** what minimal prior-save preservation is justified for the local
  game? Existing atomic-transition wording cannot be cited as disk-write evidence.
- **Content evolution:** what smallest policy protects meaning when source-only
  text/defaults change under stable IDs? Current path/reference validation catches
  some breakage and misses semantic revision; no pinning design is selected.
- **Historical basis:** competence validation requires historical specialist basis
  to match current tags. Future gain/loss or rule changes must preserve accepted
  attempts without reinterpreting them. That needs owner-approved gameplay and
  compatibility policy together.
- **Retention:** which records can eventually be reduced while preserving causal
  links, unresolved obligations and accepted results? Current history is neither
  disposable diagnostics nor a universal reconstruction log.
- **Validation and errors:** exact domain records coexist with loose outer fields
  and nonuniform exceptions. A future import or portability use case should set
  the needed scope; passing current validators is not universal semantic proof.
- **Doctrine and implementation:** technical continuity is an accepted goal;
  explicit saves recover only saved supported state. Incidental prose and unsaved
  play are not protected. Older “once concretized” wording is qualified by ADR-059
  and later accepted incidental expression. Architecture's preview-only narration
  wording remains the historical mismatch already recorded by Narrative Experience.

No conflicting requirement needs resolution to complete this documentation task,
and no protected manifest needs alteration. The gaps above remain explicit rather
than being converted into implementation authority.

## Evidence

Runtime and test assertions were inspected at the protected baseline. Listed
gameplay tests were read, not executed for this documentation review; no provider
was called. Historical milestone verification is not a new test result. The local
modified `saves/savegame.json` was preserved and was not used as design evidence.

| Evidence | Supports |
|---|---|
| [Framework](README.md), [template](system-manifest-template.md), [map](system-map.md), six linked manifests | Shared ownership model, doctrine, earlier findings and scope |
| [Architecture](../../architecture.md), [principles](../../simulation_principles.md), [model](../../simulation_model.md), [Story-First](../../story_first_design_doctrine.md), [ADRs](../../decisions.md) | Storage/authority distinction, sparse continuity and accepted compatibility decisions |
| [Save system](../../../engine/save_system.py), [session](../../../engine/game_session.py), [GameEngine](../../../engine/game_engine.py) | Envelope, copied normalization, direct writes, reconstruction/adoption and reset |
| [World State](../../../engine/world_state.py), [pressures](../../../engine/pressure_state.py), [threads](../../../engine/unresolved_threads.py) | Required fields, stable history, reference integrity and sparse state |
| [Scene loader](../../../engine/scene_loader.py), [region validator](../../../engine/region_validator.py) | Content reloading, current-location resolution, overlays/spawns and validation limits |
| [Knowledge](../../../engine/actor_knowledge.py), [traces](../../../engine/evidence_traces.py), [knowledge tests](../../../test_actor_knowledge.py), [location tests](../../../test_actor_location.py), [discovery tests](../../../test_discovery.py) | Seeds versus restoration, sparse records, unknown-reference rejection and legacy normalization |
| [Save/load tests](../../../test_save_load.py) | State/history roundtrip, retained IDs, new-ID continuity and backward-reference rejection |
| [Predicament](../../../engine/west_road_predicament.py), [predicament tests](../../../test_west_road_predicament.py) | Phase/report/witness integrity, recap and prototype rejection without altering file/session |
| [Competence](../../../engine/character_competence.py), [competence tests](../../../test_character_competence.py) | Accepted-result consistency/replay, all supported profiles/operations, copied normalization and invalid basis/version rejection |
| [Theft rule](../../../engine/west_road_market_theft.py), [theft tests](../../../test_west_road_market_theft.py) | Timing continuity, no retroactive legacy theft, established-incident retention and injected load scene failure |
| [History context](../../../engine/history_context.py), [continuity](../../../engine/scene_continuity.py), [CLI](../../../play_game.py) | Bounded derived context, ephemeral prose, fixed path commands, reset/load distinction and error handling |

## Revision history

- October 6, 2026: initial Persistence review candidate; distinguish storage,
  reconstruction and compatibility from gameplay authority, and document exact
  version-1 normalization, content reload and disk durability limits.
