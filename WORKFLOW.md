# WORKFLOW.md

## Governing Principle

Use the lowest reasoning level capable of completing the entire coherent task safely. Do not divide coherent work into many runs solely to obtain a lower reasoning setting.

The default delivery unit is an approved **capability package**: one coherent development objective containing several closely related internal milestones. A package has one clear purpose, one rollback boundary, and explicit exclusions. It must not combine unrelated systems merely to reduce review frequency, and it must never be an open-ended instruction to continue developing.

The project protects owner attention as well as implementation safety. **Review fatigue** from excessive low-value review, packets, and approvals is a governance risk: it can create the appearance of oversight while making it harder to notice meaningful product, architecture, and risk decisions. Optimize for fewer meaningful checkpoints, clear plain-language status, strong automated verification, recoverable internal milestones, explicit stop conditions, and preserved owner authority. More text or more approval steps are not inherently safer.

## Capability-Package Lifecycle

Exactly one sprint may be active at a time. A capability package may contain sequential internal milestones that would previously have been separate small sprints, but all work remains explicitly bounded and testable.

Before a package begins, the owner normally approves its direction, player or project value, major scope boundaries, and any architectural decision it requires. Each package record must state:

- goal and owner-visible value;
- included internal milestones;
- explicit exclusions;
- expected files or systems;
- persistence impact;
- player-facing impact;
- architecture decisions required;
- verification requirements;
- completion conditions; and
- rollback boundary.

After approval, one lead Codex session may define and record the internal milestones, stage their required manifest records, implement them sequentially, run focused and regression checks, update relevant documentation, create permitted checkpoint commits on a feature branch, complete package closeout, and assemble the final review packet. The lead agent must not stop after each routine milestone to ask permission to continue.

For each internal sprint or milestone, the lead agent must:

1. Work from the repository root in PowerShell and run the environment preflight.
2. Read the canonical project, package, and sprint documents and perform Startup Review.
3. Confirm the prior sprint is complete and `next_sprint` is `null` or matches the accepted package milestone.
4. Stage only the accepted active sprint in all three canonical manifests before changing implementation code.
5. Confirm the staged Markdown, YAML, and JSON manifests parse and deeply agree.
6. Continue directly into the bounded work unless a stop condition is encountered.
7. Run focused verification during implementation and before advancing between internal milestones.
8. Complete required documentation and ADR work.
9. Run the required closeout verification for that milestone or package boundary.
10. Close out the active sprint only after required verification succeeds. Do not define, stage, or begin work outside the accepted package automatically.

Closeout of a package must not select or start the following package. A package may contain several explicitly accepted internal milestones, but never more than one active sprint.

## Owner Approval and Stop Conditions

Owner approval is required at meaningful boundaries: package direction and value; major scope boundaries; player-visible behavior; new persistent-state ownership; save-version changes; generic frameworks; major refactors; live AI integration; and other independent architectural decisions.

Routine implementation choices inside an approved package do not require separate approval when they follow accepted architecture and remain within package scope. This includes established naming choices, expected focused-test repairs, documentation maintenance, and ordinary internal milestone progression.

Stop and request owner input when any of the following occurs:

- a required decision falls outside approved package boundaries;
- authoritative requirements conflict;
- a new ownership or persistence model is proposed;
- a save-version change is needed;
- unapproved player-visible behavior is needed;
- a generic framework or broad refactor is needed;
- required verification has an unresolved failure that cannot be safely corrected within scope;
- repository state is materially ambiguous;
- work risks destructive or irreversible change; or
- scope would enter an explicitly deferred capability.

A minor, clearly bounded defect may be repaired in the same run only when it was directly caused by the package work, does not broaden scope, requires no new architectural decision, and is recorded in the final report.

## Canonical Sprint and Package Records

The permanent current-sprint paths are:

- `docs/current_sprint.md`
- `docs/current_sprint.yaml`
- `docs/current_sprint.json`

Continue maintaining and validating all three. The active record must preserve goal, expected files, acceptance criteria, verification, status, and its relationship to the accepted package. Synchronize them during staging and closeout, and again only when a repair changes sprint-record content. Do not rewrite or repeatedly revalidate them between implementation edits that do not affect sprint metadata.

The JSON and YAML manifests must both parse successfully, use the same data types, contain the same keys and nesting, preserve equivalent ordered list values, and deeply agree after parsing. The embedded Markdown manifest must materially agree with them. JSON syntax validation alone is insufficient.

Temporary planning files may be promoted into the canonical paths when supplied, then deleted only after successful promotion and validation. Their presence does not require a separate staging run. Future tooling may choose one structured canonical source and generate the others mechanically, but that does not change the present three-manifest policy until separately accepted.

## Architecture Reviews and Packets

Architecture reviews serve two audiences and must separate owner-level conclusions from technical evidence. Use the lightest review that safely supports the next decision.

### Review cadence

- **Sprint health check:** brief routine confirmation during internal work or at closeout that scope, verification, and boundaries remain sound. It does not require a full packet.
- **Capability-package review:** normally required before a new capability cluster, after a completed package, when the existing architecture no longer safely supports the intended work, or when implementation reveals a genuinely new architectural decision.
- **Deep architecture review:** required for a new persistent domain or schema, save-compatibility change, established ownership change, autonomous simulation, generic infrastructure, live AI authority, material canonical-lore ownership change, serious contradiction, or consequential alternatives with similar merit.

Do not automatically conduct a new architecture review after every routine extension of an approved pattern. Review again when a package ends, implementation materially diverges, a stop condition occurs, or the next capability crosses an architecture boundary.

### Owner-facing review and report

Use `docs/architecture_review_template.md` for a review. Begin every completion report with a concise plain-language owner summary covering:

- what the engine can now do and the value it adds;
- player-facing change, if any;
- intentionally unsupported behavior;
- whether verification passed;
- real compromises, defects, or decisions needing attention; and
- the recommended owner action.

Do not require the owner to review helper signatures, schema checks, test case numbers, or internal mechanics unless a failure occurred, a new architectural decision was made, the owner asks, or the detail is needed for a meaningful decision. Keep detailed evidence in an appendix or packet.

End every owner-facing architecture review with exactly one decision request: accept, reject, defer, or request a deeper review of one named issue. Acceptance authorizes later bounded staging inside the approved package; it does not authorize speculative work or automatically start a package.

### Packet and handoff policy

Create a full architecture-review packet only when a capability package is complete, a major architectural decision is required, a package is blocked and needs external review, a repository-access boundary requires it, or the owner explicitly requests it. Internal milestones retain enough records, tests, and checkpoint history to make the final package auditable, but do not generate a full packet merely because an internal milestone completed.

A handoff ZIP is required only when moving across an actual repository-access boundary, moving to an environment without repository access, creating a formal milestone artifact, or when explicitly requested. Within one repository session, continue from stable project records. Do not make the owner a courier for prompts, files, summaries, routine continuation approval, or repeated Git checks.

Architecture-review packets are evidence packages, not the owner-facing recommendation. They contain the smallest complete set of canonical documents, changed or directly relevant implementation files, focused tests, verification evidence, and Git evidence needed to support the decision. When a ZIP is required, use PowerShell `Compress-Archive`, deterministic inventory, exact archive-membership validation, readability checks, temporary-assembly cleanup, and recorded Git evidence. Generated content must stay under `.build\`, `.artifacts\`, or `handoffs\` according to repository policy. Packaging success remains independent from application-test success.

Capture Git status separately as pre-assembly source status and post-cleanup final status.

### Handoff artifact retention

Assemble a review packet in a temporary directory outside the repository working tree. Temporary packet content must never appear in captured Git status. Name a review candidate `<package-slug>-<short-head>.zip`; the packet manifest must enumerate every archive member exactly, and the evidence must record the exact branch, HEAD, clean `git_status`, commands, and results used to create it. A corrected candidate may replace an earlier candidate only after archive creation, manifest comparison, and archive-integrity verification succeed. Remove its temporary assembly directory immediately afterward.

After package acceptance and merge, retain exactly one canonical accepted ZIP for that package, with the suffix matching the accepted review HEAD. Remove only superseded candidate ZIPs for that same package; preserve unrelated accepted archives and unresolved review candidates. Confirm that `handoffs\` contains no temporary extraction or assembly directories before capturing final Git evidence.

Use `tools\cleanup_handoff_candidates.ps1` for a dry-run-first cleanup of a completed package. It requires a package slug and accepted short HEAD, fails if the accepted archive is absent, and only removes matching superseded candidate ZIPs plus explicitly named temporary directories under `handoffs\`. Run it without `-Apply` to review the exact paths, then rerun with `-Apply` only when the preview is correct. Do not delete an artifact whose package status or purpose is ambiguous.

## Model and Reasoning Routing

- **Low reasoning:** mechanical setup or closeout, approved documentation edits, established validation, package generation, archive inspection, Git evidence, and deterministic cleanup.
- **Medium reasoning:** normal bounded implementation inside an approved package, including startup review, staging, focused tests, documentation, closeout, and reporting.
- **High reasoning:** architecture or scope review, unclear or systemic failures, ownership conflict, persistence design, atomicity problems, or material contradictions.

The owner should not need to route ordinary internal tasks manually. Escalate only when the coherent work genuinely requires it.

## Verification Cadence

During implementation, run new focused tests, directly affected regressions, and necessary syntax or static checks. Do not repeatedly run the entire official suite after every small edit.

At each required closeout, run the documented complete verification cycle, including focused and required regressions; save/load and Region Pack validation where applicable; canonical manifest parsing and deep agreement; environment preflight; hardening validation; launch and scripted smoke checks where applicable; and `git diff --check`.

If a repair changes only documentation, rerun manifest validation, applicable documentation or governance validators, `git diff --check`, and directly affected checks. Do not rerun unrelated application tests unless the repair could affect them. Required failures block closeout; blocked commands must be reported accurately and never treated as passes.

Infrastructure-only packages that intentionally create no player-visible behavior may close without owner gameplay testing. Player-visible packages must provide a short, concrete playtest procedure focused on behavior the owner can meaningfully evaluate. Do not ask the owner to validate invisible internals manually when automated verification is the appropriate evidence.

## Canonical Windows Environment

- Open `D:\AI RPG` directly as the active Codex workspace, or open `D:\AI RPG\AI RPG.code-workspace`, before implementation or closeout. Work from the repository root in PowerShell.
- Confirm the active Git root before implementation with `git rev-parse --show-toplevel`.
- Run the official-interpreter preflight before implementation and closeout:

  ```powershell
  .\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\preflight.ps1 -RepoRoot .
  ```

  The preflight path-normalizes the Git root and requires `D:\AI RPG` by default; its `-ExpectedRepoRoot` parameter exists for an explicit diagnostic override.
- Use only `.\.venv\Scripts\python.exe` for Python setup, tests, validation, and closeout evidence.
- Do not substitute bundled, system, Windows Store, alternate, `uv`, or fallback Python environments.
- Record exact verification commands, exit codes, outcomes, artifact paths, and whether Codex or the owner ran each command.

If the official interpreter returns `Access is denied` or cannot create a
process, first confirm the repository root, branch, and working-tree state
once. When those checks identify the expected repository, retry the exact
official-interpreter command using the available workspace permission or
approval mechanism. Do not recreate `.venv`, change permissions, elevate
Codex, or substitute another interpreter. Continue normally when the
authorized retry succeeds. Treat preflight as blocked, and ask to reopen
`D:\AI RPG` or `AI RPG.code-workspace`, only when both attempts fail or the
repository/workspace evidence shows a mismatch. Never report owner-executed
evidence as Codex-executed or claim blocked validation passed.

## Git and Recovery Policy

For a larger capability package, prefer a dedicated feature branch when practical. Use logical, focused checkpoint commits or equivalent recoverable milestones when the project policy and task authorization permit them; run verification before advancing between milestones. Preserve a straightforward rollback path, do not rewrite or destroy owner work, and do not merge to `main` without owner approval unless that authority has been explicitly delegated.

Codex must not create a Git commit unless the task prompt explicitly authorizes it. When authorization is absent, report the exact changed-file list and a recommended commit title. An authorized normal package may use focused checkpoint commits and a final logical commit; checkpoints must not become an excuse for uncontrolled writes.

## Task Prompt Guidance and Invariants

Package prompts should reference canonical repository documents instead of repeating stable architecture. They should state the accepted package, value, milestones or boundaries, ownership, persistence and player-facing impact, verification, explicit exclusions, stop conditions, and commit authority. Missing package details must not be invented.

Preserve provider neutrality, deterministic behavior, simulation-owned truth, exactly one active sprint, atomicity expectations, persistence compatibility, canonical manifest agreement, fail-closed behavior, ADR discipline, scope boundaries, unrelated user changes, and owner authority over high-impact decisions. Never begin the next sprint or capability package automatically.
