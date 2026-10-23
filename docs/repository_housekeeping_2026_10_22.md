# Repository housekeeping — October 22, 2026

Standalone owner-authorized maintenance at published baseline
`fdfc95760ae2dfa9f83fd7ba97239bcb5991acef`. No capability was selected or staged;
accepted runtime, Design, save format and lifecycle records are unchanged.
At maintenance completion on October 22, 2026, the changes were an uncommitted
maintenance handoff and had not been published. This records the state on that
date; consult Git history for any subsequent publication.

## Archive and recovery

Archive: `D:/AI-RPG-Archive/2026-10-22-housekeeping`.
`manifest.json` summarizes preservation; `inventory.jsonl` maps each original file
to its byte-verified archive copy. `evidence-plan.jsonl` records excluded originals.
`refs-before.txt` and `worktrees-before.json` preserve branch/worktree provenance;
`actions.jsonl` records actual removals, retirements and recoverable branch names.

Restore an evidence file from `files/<drive>/<original path remainder>` to its
recorded original location, or to an isolated recovery tree retaining relative
paths. Compare the recorded public source hash where present. Representative
R1/R2/R3/R5/R6 reports, evaluator source and patch were restored and byte-compared
before original-file cleanup. Archive copies were verified byte-for-byte first.

R2 and R3 depend on R1's parent study and evaluator; R5 A/B and R6 C share baseline,
fixtures and comparison results. Failed and superseded runs remain evidence, not
accepted implementation. Private/uncertain save, state, raw-response and binary
payloads were excluded from the archive; unique ignored originals remain in place.
Clean tracked defaults in retired worktrees remain recoverable from recorded commits.
Reproduction can
require both restored archive files and those retained originals. No provider
reproduction is authorized by housekeeping.

Clean retired worktrees can be recreated at the exact commits in the saved worktree
record; restore their archived ignored evidence afterward. Deleted branch names can
be recreated with `git branch <name> <saved-head>` using the refs/action records.
Only branches already reachable from the unchanged published baseline were removed.
Git objects, reflogs for retained refs, the outstanding non-ancestor branch and
existing dangling objects remain in the original repository; no GC/pruning was run.

## Tool and output cleanup

`tools/play_north_gate_discussion_smoke.py` duplicated the ordinary offline CLI
entry point and provider/socket blocking in `tools/play_contextual_investigation_smoke.py`.
The former source is archived; the shared launcher remains. North-Gate experiential
instructions now use it. Other smoke launchers have distinct setups; the focused
verification wrapper provides useful output isolation and remains available.
No accepted behavior/compatibility tests or fixtures were removed.

Investigation acceptance tests and the shared offline launcher now write new
outputs under the current checkout's ignored `.artifacts`, instead of reusing
historical `C:/tmp` evidence. Local `.codex-remote-attachments` inputs are ignored;
accepted documents remain tracked at their canonical paths.

## Protected and unresolved material

The original dirty checkout, Condition E dirty worktree and architecture
clarification dirty worktree are preserved. Recent Warded Tower research keeps its
originals. The clean publication checkout and official original interpreter remain.
Historical worktrees containing uncertain ignored saves/raw data remain registered.
Legacy ZIPs and loosely named files without clear ownership remain in place.

Runtime architecture, system ownership manifests, ADRs, accepted Design, persisted
state and lifecycle documents need no reconciliation: this maintenance changes
only development entry points, generated-output locations and evidence locators.
See the archive's cleanup summary and verification record for execution results.

## Execution results

- Archived 12,581 selected evidence files (141,601,831 bytes); all were byte-verified.
- Six representative restorations passed; final inventory and 6,036 public source hashes passed.
- Retired 11 clean worktrees and deleted 77 branches already reachable from main.
- Removed 6,743 archived historical source files, 20 loose historical files and 288 direct bytecode files; retired worktrees also included disposable caches.
- Eight clean historical worktrees retain uncertain ignored data; all three dirty worktrees and recent Warded Tower originals remain protected.
- Git and publication status at maintenance completion (October 22, 2026): the
  baseline was unchanged, the maintenance diff was uncommitted, and no staging,
  commits, merges or pushes had occurred during the maintenance task.
