# F01/F05 consequential fidelity correction — offline candidate

October 16, 2026. Owner-authorized correction within the active damaged-gate
package; Routine risk. Uncommitted, unaccepted and not published.
Baseline/HEAD/main: `d2ededee58294002f522cef5ab61577270311997`.
Branch: `codex/f01-f05-bounded-playable-integration-v1` in the isolated checkout
`D:/AI RPG/.artifacts/f01-f05-bounded-playable-integration-v1`.

## Reproduction and diagnosis

The preserved [live evaluation](../.artifacts/gate-live-fidelity-20261016/report.md)
identified Case 5's significant omission. The current development explicitly says:

> Ten minutes of competent routine work secures the hinge and commits one spare pin. The repair is not yet finished.

The complete recorded prose is:

> As you expose the gate’s mounting, its support shifts. The hinge remains secured, but the repair is unfinished; completing it now requires bracing the mount with the stout timber, committing it to the repair.

The available pin supply has changed from two to one before a meaningful player
choice. The narration preserves the new support requirement but omits the already
committed pin. The pin is unavailable for other use even if the player withdraws.
This cost is relevant to that choice; no exhaustive inventory requirement follows.

Offline reproduction matched the preserved context/request exactly before edits.
Replaying the stored bad prose through accepted realization returned a structural
candidate, reproducing the verification blind spot without a provider call.
The information was current, accessible and complete, serialized exactly, and well
below the input/output bounds. No engine state, authorization or supply failure
explains the omission. The observed failure is consequential selection/compression
during expression, followed by structural validation that cannot assess meaning.
The model's internal cause cannot be established from one output. In particular,
record order/attention is a plausible contributor, not a proven causal mechanism.

The old instructions broadly required preserving costs, but emphasized current
focus/new developments and finishing when the current development was clear.
They did not explain how earlier accepted consequences remain part of the next
choice when a newer complication takes attention. This is the narrow guidance
ambiguity addressed here; the source already supplied sufficient information.
The same weakness could suppress another committed resource, elapsed work,
accepted failure, physical change or consequential agreement. It is not specific
to pins. No general supplier, activity or memory system is needed to explain it.

## Design sufficiency and implementation disposition

F01-D1/D6/D9 already require preserving consequential meaning, sufficient input
and materially relevant costs at player decisions; F01-D2/D5/D8 permit relevant
context to carry naturally without repetitive disclaimers. F05-D2/D3/D5/D6 govern
authorization, control, competent execution and retained work/consequences.
These accepted intentions are sufficient: no new gameplay doctrine or significant
unresolved design question was identified for this instruction-only correction.

| Existing mechanism | Disposition and reason |
|---|---|
| Gate state, costs, F05 control and context suppliers | Reuse unchanged: the pin, timing, partial work and new choice are correct and fully available. Reclassifying them or adding new fields would not repair observed loss during expression. |
| F01 explicit context/provenance and single-call realization | Reuse unchanged: authority, access, exact request and stateless behavior remain appropriate. |
| F01 expression instructions | Adapt the selection/framing guidance only: prioritize consequential understanding of the next choice over the latest development alone. |
| Existing prose validator and provider boundary | Reuse unchanged within their structural/safety scope; they do not certify semantic fidelity. |
| Literal pin detector, required-fact checklist, appended cost ledger, mandatory action flourishes, extra model/judge stage or general architecture replacement | Exclude: these would narrow natural expression, risk duplicated reporting, or add machinery not justified by this one omission. Historical mechanisms are resources, not design constraints. |

`engine/narrative_realization.py` changes **only `INSTRUCTIONS`**. The opening now
frames the supplied moment as the character's unfolding experience. Selection
prioritizes what matters to present understanding and the next choice, explicitly
carrying accepted work, commitments and consequential costs through a newer
complication. It asks for this meaning within supported action/transition rather
than a ledger or every supplied fact, while allowing known context to carry
implicitly where omission would not mislead. The finish condition becomes clarity
of the moment's consequential meaning, rather than the latest development alone.

No pin-specific sentence, mandatory inventory counts, new input field, semantic
matching, retry, postprocessing, fallback, provider configuration, gameplay rule
or F05 decision was added. No code outside the instruction assignment changes in
that module, verified by AST comparison against the preserved pre-correction file.
The revised instructions are a candidate correction, not an accepted replacement
or proof that future generated prose will preserve the pin.

## Offline regression evidence

- Changed Python syntax passed before execution.
- Seven new offline tests in `test_f01_consequential_fidelity.py` pass. A portable
  fixture freezes the actual Case 5 context, old instructions and bad prose, plus
  two clearly labeled human-authored reference expressions. Tests reproduce the
  current engine's exact case, the structural blind spot, propagation of revised
  guidance with unchanged input, compatible nonliteral reference prose without
  resource inventories/repeated uncertainty, record-order preservation, another
  spent means (failed timber leverage), and later observation without compulsory
  repetition of the known pin commitment. State/authorization/costs stay unchanged
  by realization. DNS/socket access is denied; generators are explicit stubs.
- All 45 relevant unittest tests pass: seven new plus 19 gate, 11 accepted F05
  and eight API-readiness tests. The existing five F01 component groups and three
  adjacent narration scripts also pass with DNS/socket access denied and fake
  provider transport. Existing tokenizer cache is used; no download/API call.
- Offline comparison replays **all eight original contexts/outputs**: only
  instructions differ, serialized authoritative inputs are identical and all
  existing structural results remain candidates. Replayed historical outputs are
  not new generations or predicted corrected outputs. In particular, the old
  defective Case 5 still passes structural validation; no semantic gate is claimed.

Evidence is in the new ignored directory
`../.artifacts/f01-consequence-correction-20261016/`: `before.json`,
`narrative_realization_before.py`, `reproduction.json` and
`eight_case_offline_comparison.json`. The original eight live input/output/
assessment records and evaluation ledger are preserved byte-for-byte for a future
comparison. Zero live/API calls or generations were used by this correction;
the previous eight-generation allowance remains exhausted.

## Effect on the accepted experiential findings

| Finding | What this candidate addresses; what remains unverified |
|---|---|
| Mechanical outcome reporting | The frame is now the character's supported action/change, with consequences woven into the transition to choice. This is an intended emphasis change; no generated improvement has been observed. |
| Repeated established uncertainty | Consequential relevance governs selection and known context may carry implicitly. Existing attribution/uncertainty safeguards remain: omission must not mislead. No symptom-specific ban on uncertainty was added. Actual repetition may persist. |
| Underrepresented physical action/character experience | The opening asks for unfolding experience of supplied action rather than simply a latest-result report. It creates no feelings, competence, physical events or mandatory embellishment. New prose quality is unverified. |
| Repeated options/resources (Case 3) | A next choice needs enough relevant meaning, not every known option/resource. Reference prose can omit inventories and stale caveats while retaining incurred cost. The original Case 3 source/prose remain unchanged; revised model selection is unverified. |

These are related selection/framing effects of one principle, not four separate
rules or expanded implementation requirements. Human-authored examples establish
that natural selective wording is compatible with the contract; they do not
establish live semantic fidelity or experiential improvement.

## Remaining risks and owner smoke

The correction relies on model adherence to instructions. A model can still omit,
overstate or invent consequential meaning, repeat qualifications, flatten action
or over-recite context. Structural validation still cannot detect those failures.
No new semantic guarantee, recovery system or general architecture is claimed.
The wider instruction emphasis reaches all callers of this bounded F01 component;
offline checks preserve their interfaces but cannot establish their new prose
quality. Campaign routes that do not call this component are unchanged.

The candidate is ready to be **evaluated** in a small, explicitly authorized owner
experiential smoke, with the known historical failure disclosed. It is not yet
demonstrated fidelity-corrected or ready for acceptance on that basis. Offline
reference review and deterministic gameplay smoke require no provider calls;
any new live smoke/comparison requires separate authorization and a fresh budget.
Recommended next step: owner review of this diff and evidence, then, if desired,
a bounded live comparison of the decision point plus nearby ordinary play. No
live call, implementation acceptance, commit, merge or publication follows here.

## Documentation reconciliation and preservation

Updated the current package/sprint records, architecture narration boundary,
Narrative Experience manifest, system map and integration handoff to distinguish
the accepted base from this unaccepted instruction candidate and the exhausted
live budget. Historical acceptance and live reports remain unchanged. This report
records diagnosis, source disposition, verification limits and no-change decisions.

Meaningful no-change determinations: canonical F01/F05 Design, shared doctrines,
ADRs and process contract need no revision because no design principle or durable
architecture changed. Other system manifests, gameplay suppliers, persistence,
save version, provider configuration, API tooling and ordinary input/UI routes
remain unchanged. No historical experiment was reconciled and no new system or
package was opened. Original checkout, saves, credentials and prior evidence are
preserved. All changes stay isolated and uncommitted, with an empty index and
protected baseline unchanged.

Final verification passed: lifecycle 7/7, shared GitWorkflowTools verification,
tracked/index diff checks, new-file whitespace, documentation links and the
11-file correction scope. All other prior candidate files, the original checkout
status/HEAD, protected HEAD/main/origin-main and every prior live-evidence file
remain unchanged. The original eight outputs/ledger were not overwritten.
The index remains empty. Detailed verification is preserved in
`../.artifacts/f01-consequence-correction-20261016/final_verification.json`;
the shared tool log is in that directory's `verification/workflow.log`.
Shared tooling and profiles were not modified; only an ignored worktree-bound
profile was copied for this check. No additional live verification was performed.
