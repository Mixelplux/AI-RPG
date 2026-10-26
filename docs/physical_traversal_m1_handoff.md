# Physical Traversal Core V1a — M1 implementation handoff

Initial implementation handoff October 25, 2026; blocking corrections completed
October 26, 2026. Owner formally accepted M1 on October 26 after both blocking
defects were corrected and verified; no known blocking defects remain.
Risk: Elevated. No M2 work or Git publication is authorized by this handoff.

## Environment recovery

The original approved Windows environment at `D:\AI RPG\.venv` exists and runs
Python 3.13.14. An ignored worktree-local directory junction exposes that same
environment through `.\.venv\Scripts\python.exe`; resolved prefix identity was
verified. No environment recreation, installation, executable copy, replacement
interpreter, ACL change or shared tooling edit. The initial sandbox link denial
was resolved by an approved narrowly scoped filesystem-link operation.

Focused preflight uses this isolated worktree for both `-RepoRoot` and
`-ExpectedRepoRoot`, including `-RequiredPythonModule openai,tiktoken`.
Recovery preflight: 23 passed, no warnings/failures/blocks. Post-implementation:
22 passed, one expected dirty-working-tree warning, no failures/blocks.

## Target model and implementation

See [the pre-implementation model and persistence approach](physical_traversal_m1_design.md).

- World: validated immutable local places, directed traversal links, surfaces,
  physical object instances and compatible held/carried/secured/attached/located
  relationships. Creature position, physical condition, fictional time, causal
  references and established fall occurrences have one World owner.
- Character: one sparse PC/NPC rule profile; ordinary and climb speeds, Strength,
  Athletics proficiency/expertise, scoped Strength-check traits, relevant conditions,
  HP premises, accepted movement expenditure, readiness and legitimate route access.
  The general PhysicalCapability query separates movement allowance, coordination
  and action economy under the owner's accepted October 26 clarification.
  Missing material statistics/resources remain unavailable rather than defaulting.
- Action: domain-owned dependency discovery; actual 2024 climb costs, justified
  optional Athletics checks, supplied d20 sampling, relevant modifiers/conditions,
  no automatic natural-1/20 ability-check outcome, and stale/forged-input rejection.
- Fall: a separate World-established occurrence produces bounded dry-ground damage
  and Prone contributions. A failed climb never manufactures a fall or injury.
- Common integration: the existing I1 Coordinator and F05 DomainStep/checkpoint
  interfaces assess these domains and enforce authorization, access and freshness.
  The adapter refuses execution until M2 acceptance integration is implemented.

Reused: I1/F05 interfaces, existing internal Unresolved error semantics, official
interpreter and workflow validator. Retained unchanged: GameEngine, accepted
I2/I3 gameplay and compatibility codecs, default CLI and existing save boundaries.
Excluded from new mechanics: finite routine/d6 resolution and inventory summaries
as physical truth. No existing implementation was replaced merely to rename it.

## Exact M1 limitations and M2 path

M1 delivers domain foundations and provisional rule results, not playable climbing
or a disposable scenario runtime. No new authoritative movement, injury, elapsed
time, resource expenditure, attachment setup, accepted attempt or save is published.
A provisional result can be sampled again; it is not an accepted retry receipt.
Successful partial extent is not an invented intermediate physical position.
Failed objectives leave physical disposition and any charge unresolved; neither a
safe final position nor a fall is asserted. Single-turn movement uses Character's
accepted expenditure; outdoor pacing and complete mixed-mode turn execution are
not implemented. Equipment access supports direct handling plus Character readiness;
it does not infer reach through attachment chains or grant rope bonuses/protection.

Supported conditions for climbing are Poisoned, Grappled, Restrained, Incapacitated,
Paralyzed, Stunned, Unconscious and separately leveled Exhaustion. Incapacitated
alone does not forbid movement. Stunned does not zero Speed: general Character
coordination capability is unavailable, and Resolution requires it for climbing,
even without a check. Actions, Bonus Actions and Reactions are unavailable while
Incapacitated, including through Stunned. Other Speed restrictions still apply.
No automatic fall or safe support is inferred. Unsupported conditions or explicitly unresolved
material effects/bindings block resolution. Creature anatomy and scoped trait
applicability must be supplied sufficiently by the owning composition boundary.
This does not implement complete character sheets, effects, combat, falling into
liquids/reactions/mitigation, HP/death application, NPC agency, general language,
production Region Pack composition, swimming or jumping.

M2 can build on these typed owner views and the common coordinator. It must
extend/replace the finite result/root shapes within one common acceptance owner,
validate current premises and authorization at publication, and retain stable
undertaking/attempt recognition with dependent position, time, resources, results
and activity restrictions in one accepted root. No second traversal truth store.
Concrete new campaign codec/envelope selection must precede incompatible writes.
Existing v1/v2 saves remain supported; no automatic migration or guessed legacy
traversal state. M1's codec rejection tests prevent provisional records being
mistaken for existing accepted campaign state.

## Verification and targeted architecture review

All checks offline; no live providers and no dependency installation.

- AST syntax: four source modules plus the test file passed before execution.
- `.\.venv\Scripts\python.exe -B test_physical_traversal.py`: **54 tests passed** after corrections (46 at initial handoff).
  Covers rule/world/character variation, PC/NPC and place changes, missing means,
  compatible/conflicting relationships, binding availability, stale and forged
  assessments, sampling faults, fall separation and common coordinator boundaries.
- `.\.venv\Scripts\python.exe -B -m unittest test_activity_control
  test_gameplay_coordination test_consequence_integration test_campaign_continuity
  test_player_activity test_information_adjudication test_information_resolution`:
  **246 tests passed**. Includes existing v2 restore/retry/corruption isolation.
- `test_save_load.py` via the official interpreter with socket connections patched
  to fail: **passed** (legacy v1 round-trip and invalid-reference checks).
- Lifecycle/project validator: **8 passed**. Whitespace, changed-file syntax,
  documentation link targets, UTF-8 and final scope/index checks: **passed**.

Targeted architecture review checked CD/PT ownership, domain dependency discovery,
provisional-versus-accepted state, F01 access, F05 control, no scenario-selected
outcome, legacy compatibility and the M2 seam. Corrections placed accepted movement
expenditure in Character, rejected unresolved material bindings/effects, and
rechecked premises after sampling. The subsequent independent code-level review
identified two blocking defects missed by that initial review; their corrections
and final verification are recorded below. No known unresolved required verification
failure remains after these bounded corrections.
This was a targeted implementation review, not an independent audit or owner smoke.
The full suite and live experiential climbing smoke were not run; climbing is not
yet routed into gameplay. Existing regression evidence is not new-domain durability.

## Blocking review findings and corrections — October 26, 2026

1. **P2, incorrect Stunned Speed restriction:** the previous resolver included
   Stunned in the Speed-zero condition set, and the immobilization test endorsed
   that error. The owner's subsequent accepted clarification preserves allowance
   for basic unsteady movement while prohibiting meaningful physical coordination.
   Character now supplies one general PhysicalCapability view, independent of any
   selected technique, with effective ordinary/special speeds, coordination and
   Actions/Bonus Actions/Reactions. Resolution requires coordination for climbing
   without inspecting Stunned. Thus a Stunned creature can retain Speed 30 / Climb
   Speed 40 while climbing is unavailable for `coordinated_movement_unavailable`.
   Genuine immobilizers still report Speed 0 / `movement_unavailable`.
2. **P2, mutable fall freshness baseline:** the previous post-sampling check read
   both the current and baseline frame through the same mutable WorldPhysics
   wrapper. It could return two dice from revision w1 / 20 feet after the actual
   frame changed to revision w2 / 100 feet. Resolution now captures the immutable
   initial frame and Character revision before sampling. Current World/Character
   values are read once per owner at validation and compared against those captures.
   Stale sampling raises `validation / stale_fall_assessment`; no result is returned.

Defect regression evidence: all 54 focused tests pass. The updated immobilizer
matrix excludes Stunned from Speed-zero semantics and checks the remaining four
conditions explicitly. New tests cover general Stunned capacity, deterministic
and uncertain climbing with ordinary/special speeds, combination with Exhaustion
or Grappled, and becoming Stunned after assessment without creating a fall.
Incapacitated's three economy restrictions are asserted independently of movement.
The required fall case runs with both reused-wrapper mutation and ordinary wrapper
replacement: initial w1 / 20 feet, two d6 samples, current w2 / 100 feet, followed by
stale rejection. Additional tests cover reused Character revision mutation and
unchanged reused suppliers. The existing codec also rejects the new capability
view as unaccepted campaign data.

Falling-risk assessment: the provisional failure record has no final destination,
no accepted cost, no injury and no declaration that physical safety was retained.
An added test demonstrates failed progress at height followed by a separately
World-established loss-of-support fall and its damage contribution. The World
fall supplier is an explicit missing-M2 adjudication boundary in this test; it is
not implemented automatic fall-risk resolution. No support or protection is
invented after the failed check. The [accepted clarification and M2 validation
matrix](physical_traversal_m1_design.md#accepted-owner-clarifications--october-26-2026)
requires exposed unsecured failure at height, properly protected failure and
failure before substantial elevation, with grounded substantial risk in the first.

Final correction verification: five-file AST syntax, 54 focused traversal tests,
the established 246-test affected group, offline socket-blocked legacy save/load,
all eight lifecycle checks, whitespace, UTF-8, documentation link targets and
scope/index validation passed. Targeted ownership review confirms that Character
supplies capacities, Resolution selects technique requirements, and World still
owns actual position, supports, grip/footing consequences and fall occurrences.
No scenario identity selects behavior; no d6 climb policy, new save representation
or consequential writer is introduced. No M2 implementation was started.

Remaining findings: no known blocking defect after corrections. Two nonblocking (P3)
review concerns remain for M2 consideration as directed: unnecessarily broad
Character dependencies and positional dependency tuples. These were not expanded
into a general dependency/refactoring project. New-domain coherent acceptance,
resumption, complete grounded risk and versioned persistence remain unimplemented
M2 obligations, not passed M1 gameplay evidence. Canonical CD/PT design permits
explicit owner adaptations and already prohibits both fabricated falls and
fabricated safety; no material ownership conflict was found.

Correction-turn inventory (**10 existing M1 paths edited**):
`engine/character_rules.py`, `engine/traversal_resolution.py`,
`test_physical_traversal.py`, `docs/physical_traversal_m1_design.md`, this handoff,
`docs/architecture.md`, `docs/design/systems/character-system.md`,
`docs/design/systems/action-resolution.md`, `docs/current_sprint.md`, and
`docs/current_capability_package.md`. The original 17-path implementation diff
remains the overall handoff; no new path or subsystem was added by corrections.

## Documentation reconciliation and file scope

Updated runtime architecture, World/Character/Action/Persistence manifests, system
map and manifest index, current package/sprint records, this handoff and M1 design.
Canonical accepted CD/PT, F01/F05, Information Foundation, integrated architecture
and Region Pack design are unchanged: implementation status belongs in living
runtime records and does not amend accepted design. No ADR added: ownership follows
accepted decisions and a new persistence implementation is deferred. Roadmap,
historical handoffs, actor/narrative manifests and authored packs need no change;
no new capability selection, actor intention, narration or content is implemented.

Changed paths: 12 documentation files, four new `engine` modules and one new test
file (**17 total**). Additional living system records are directly necessary
reconciliation within authorized domain scope. Generated test files stay ignored
under `.artifacts/`; the environment junction is ignored.

## Exact repository and lifecycle status

Repository: `Mixelplux/AI-RPG`.
Worktree: `C:\Users\Richard\.codex\worktrees\physical-traversal-v1a-m1\AI RPG`.
Branch: `codex/physical-traversal-v1a-m1`.
HEAD and local/verified remote main baseline:
`85ec1811315686f9ea6691235078bf10c25265fc`.

Implementation is an uncommitted working diff; index empty. No commit, merge,
push, publication, save-version change or migration. Original dirty checkout,
player saves, shared dependencies and unrelated worktrees were not edited.
Owner acceptance is recorded October 26, 2026. M1 lifecycle is closed with
`sprint.status: complete`; `active_sprint` and `active_capability_package` are
null, latest completed is `physical-traversal-v1a-m1`, and `next_sprint` is null.
The lifecycle is idle. M2 is not selected, staged or started and requires separate
owner authorization. Acceptance covers only the bounded M1 foundations and their
documented limits; it does not imply playable traversal or M2 validation passed.

## Acceptance reconciliation and exact publication inventory — October 26, 2026

Closure updates acceptance/lifecycle records, runtime architecture, affected
World/Character/Action/Persistence manifest status, manifest index and this model
and handoff. The system map needs no further change: its ownership relationships
already match the accepted mechanics. Canonical design, ADRs, roadmap, historical
handoffs and unrelated manifests need no change for the reasons recorded above.
No runtime or test code is changed by closure. Both P3 observations and all
accepted realistic failure, falling consequence, consequential acceptance,
continuation and persistence requirements remain deferred to M2 as recorded above
and in the implementation model.

Exact publication inventory against baseline
`85ec1811315686f9ea6691235078bf10c25265fc`: 10 modified tracked paths and seven
untracked additions, all unstaged (17 total). This inventory includes acceptance
and lifecycle closure; it excludes ignored environment/generated files.

Modified:

- `docs/architecture.md`
- `docs/current_capability_package.md`
- `docs/current_sprint.json`
- `docs/current_sprint.md`
- `docs/design/systems/README.md`
- `docs/design/systems/action-resolution.md`
- `docs/design/systems/character-system.md`
- `docs/design/systems/persistence.md`
- `docs/design/systems/system-map.md`
- `docs/design/systems/world-simulation.md`

Added:

- `docs/physical_traversal_m1_design.md`
- `docs/physical_traversal_m1_handoff.md`
- `engine/character_rules.py`
- `engine/physical_world.py`
- `engine/traversal_coordination.py`
- `engine/traversal_resolution.py`
- `test_physical_traversal.py`

Accepted gameplay verification remains the 54 focused tests, 246 regressions and
offline legacy save/load above. Prepublication record checks are reported separately
from that accepted evidence. Fresh closure/prepublication checks passed: isolated
preflight 22 passed, one expected warning for the 17-path working diff, zero
failures/blocks; project/lifecycle validator eight passed, zero failed; official
interpreter and JSON parse, five-file AST syntax, all 17 files UTF-8/whitespace,
local documentation link targets, exact inventory/baseline/branch, empty index,
player-save boundary and `git diff --check`. Gameplay tests were not rerun for
record-only closure; the accepted 54/246/offline compatibility evidence is retained.
The canonical shared workflow state tool was run read-only; its profile targets
`D:\AI RPG`, so the actual isolated worktree checks used explicit roots instead.
No shared tooling/profile was changed and no live provider was invoked.

No technical publication blocker is known. Ready for separate publication
authorization. No final committed candidate exists: all publication
actions require separate owner authorization.
