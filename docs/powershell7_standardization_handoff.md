# PowerShell 7 Workflow Standardization V1 — maintenance handoff

## Scope and repository state

Owner-authorized development-tooling maintenance, October 26, 2026. Routine risk.
This is an uncommitted implementation handoff; no acceptance or publication is
implied. No Git staging, commit, merge, push or publication is authorized.

- Baseline and candidate HEAD: `fa355a06e4b9f813ab7f5f03f6541ebf492831e2`.
- Branch: `codex/powershell7-standardization-v1`.
- Isolated root: `C:\Users\Richard\.codex\worktrees\powershell7-standardization-v1\AI RPG`.
- Original dirty checkout: `D:\AI RPG`, preserved on its existing branch/HEAD.
- The worktree's ignored `.venv` junction reuses `D:\AI RPG\.venv`; no environment
  was installed, recreated or upgraded. Project Python remains
  `.\.venv\Scripts\python.exe` (3.13.14).
- Local `main`, `origin/main` and the actual remote `main` match the baseline.
  The initial sandbox DNS failure was resolved with approved execution access;
  remote verification used read-only `git ls-remote`, not fetch or publication.

## Implementation and compatibility

Installed PowerShell 7.6.5 Core is the verified baseline. Windows PowerShell
5.1.26100.9711 remains installed but is unsupported for repository automation.
Mandatory preflight reports failure on 5.1; other PowerShell entry points require
version 7 before executing. The VS Code workspace terminal selects `pwsh.exe`
with `-NoProfile`. System defaults and user profiles are unchanged.

Lifecycle fixture mutations now parse JSON and modify an explicit property,
requiring that both its path and expected source value match. All 16 original
positive/negative cases and expected validation messages remain intact.
Formatted, compact and legacy-style whitespace exercise the same cases. The
validator's lifecycle rules and save-publication check are unchanged.

The offline runner uses the PowerShell 7 process environment dictionary instead
of the Windows PowerShell 5.1 collection-initialization retry. Its self-test had
a stale 23-fixture assertion; it now requires the actual 16-case fixture summary.
First-failure handling, complete stdout/stderr capture, child-only environment
overrides, cleanup and exact live-smoke exclusion remain tested.

The earlier save-boundary failure was environmental: sandbox access to linked
worktree Git metadata returned `must be run in a work tree`/permission denial.
The same name-only Git check and unchanged validator pass in the isolated
worktree with approved access. No save contents, ACLs or validation safeguards
were changed to work around it.

## Exact repository inventory

The candidate contains these 16 files, all unstaged:

| File | Change |
|---|---|
| `.vscode/settings.json` | Workspace PowerShell 7 terminal selection |
| `AGENTS.md` | Explicit PowerShell 7 execution requirement |
| `WORKFLOW.md` | Authoritative environment, verification, worktree-profile and troubleshooting guidance |
| `docs/conditional_procedures.md` | PowerShell selection and worktree Git-access recovery |
| `docs/powershell7_standardization_handoff.md` | This maintenance completion record |
| `tools/Invoke-ApiTask.ps1` | PowerShell 7 version guard |
| `tools/Test-ApiTask.ps1` | PowerShell 7 version guard |
| `tools/assemble_review_packet.ps1` | PowerShell 7 version guard |
| `tools/cleanup_handoff_candidates.ps1` | PowerShell 7 version guard |
| `tools/preflight.ps1` | Unsupported-shell failure instead of 5.1 warning |
| `tools/run_offline_behavioral_verification.ps1` | Version guard, modern environment overrides, corrected fixture-count assertion |
| `tools/test_powershell_workflow.ps1` | New shell enforcement and JSON-layout regression harness |
| `tools/test_project_records.ps1` | Version guard, structural mutations and layout variants |
| `tools/test_review_packet.ps1` | PowerShell 7 version guard |
| `tools/validate_project_records.ps1` | PowerShell 7 version guard; validation rules unchanged |
| `tools/validate_review_packet.ps1` | PowerShell 7 version guard |

## Separately authorized shared profile change

Only `D:\Codex Tools\GitWorkflowTools\Profiles\AINarrativeRPG.psd1` changed
outside the candidate. Exactly two `powershell.exe` tokens became `pwsh.exe`:
mandatory preflight and mandatory lifecycle validation. All original command
arguments and other profile bytes remain unchanged. The profile still targets
only AI RPG at `D:\AI RPG`; no shared scripts or other project profiles changed.

A recoverable byte copy is preserved at
`<isolated root>\.artifacts\powershell7-maintenance\AINarrativeRPG.original.psd1`.
The ignored `AINarrativeRPG.worktree.psd1` beside it is the established local
verification copy. It changes only the repository path and adds the explicit
matching preflight expected root. It retains all four mandatory commands, the
protected branch and evidence location. Shared GitWorkflowTools itself is used
for state capture and verification, including repository-mutation detection.

## Verification evidence

Evidence is under `<isolated root>\.artifacts\powershell7-maintenance\`.

| Check | Result | Evidence |
|---|---|---|
| PowerShell syntax | All 11 repository scripts parse | `workflow-regression.log` |
| Shell/layout workflow regression | 29 checks pass, including mandatory 5.1 rejection | `workflow-regression.log` |
| Lifecycle fixtures | All 16 pass in each of Pretty, Compact and LegacyWhitespace layouts (48 cases); invalid lifecycle/save-type cases remain rejected | `fixtures-*.log`, `workflow-regression.log` |
| Offline runner self-test | 17 pass, including environment isolation, complete error capture, failure propagation and live-smoke exclusion | `runner-selftest.log` |
| PowerShell 7 preflight | 20 pass, one expected dirty-candidate warning, zero blocks/failures | `preflight.log` |
| Current lifecycle and save boundary | 8 pass, zero failures | `shared-verification.log` |
| Shared GitWorkflowTools verification | All four mandatory commands plus both diff checks pass; repository state unchanged | `shared-verification.log` |
| Review-packet regression | Complete malformed-fixture matrix passes (49 PASS assertions) | `review-packet-regression.log` |
| Synthetic API launcher regression | 10 pass; zero provider requests/generations | `api-launcher-regression.log` |
| Full established offline behavioral runner | 75 commands pass, including all 73 behavioral test scripts and lifecycle/fixture validation; live provider smoke excluded | `offline-behavioral.log` |
| Independent fresh-process verification | Pass: exact scope, baseline/branch, empty index, unchanged runtime/lifecycle, profile substitution/encoding, and separate workflow/shared-verifier child runs | `independent-verification.log`, `independent-workflow.log`, `independent-shared.log` |
| Remote baseline | Read-only actual remote main matches local main and origin/main; initial DNS limitation resolved | `git ls-remote origin refs/heads/main` |

Independent verification here means a separate fresh PowerShell process and
independent command execution, not a second human/agent review. No independent
reviewer was used. All verification uses installed PowerShell 7.6.5 and the
official Windows Python environment. No live smoke was run.

Final name/scope, syntax and whitespace checks pass; the worktree index remains
empty and HEAD remains the exact baseline. All 16 files are intentionally
uncommitted. No remaining DNS/remote-verification blocker was observed. Linked
worktree Git checks still require the approved execution context on this host.

## Documentation reconciliation and limits

Execution requirements belong to `WORKFLOW.md`, with concise standing guidance
in `AGENTS.md` and recovery guidance in `docs/conditional_procedures.md`.
No duplicate standalone environment policy was introduced. This report records
the candidate's scope, compatibility and verification limits.

No changes are needed to gameplay architecture, system manifests, relationship
maps, ADRs, accepted design, deferred capabilities, historical reports or current
package/sprint records: no runtime behavior, persistence, ownership, save version,
acceptance or lifecycle state changed. Lifecycle remains complete/idle with no
next package. No live provider requests or generations are authorized or used.

The shared tool's committed-candidate evidence-export and publication paths are
not invoked for this uncommitted handoff. Destructive cleanup tooling is checked
for syntax/version enforcement, not run against historical artifacts. Git
staging, commit and publication remain separate owner decisions.
