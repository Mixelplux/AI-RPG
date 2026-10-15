# F01 first-candidate A–D evaluation

**Mixed result; owner review required.** Exactly four live calls completed on
October 15, 2026, one per moment, with no retries or further generation. One
significant local authority issue appears in A; no confirmed consequential or
epistemic distortion in B–D. A has a perceptual-timing omission/ambiguity; A and D
have material expression weaknesses. These contextual judgments are by the same
implementation agent, not an independent or blinded assessment. Offline shape
checks are not semantic evidence. No candidate or architecture was changed in
response to this evaluation.

## Complete unedited outputs and findings

### A — resolved conditional climb (42 words)

> A stone breaks loose beneath your boot, but you catch secure purchase and finish the climb. Two minutes pass; you reach the battlements unharmed. The gate guard is there to speak with, but you haven’t yet learned which way the merchant went.

Preserves recovery, completed climb, unharmed battlements endpoint and two-minute
cost. No fall, injury, alarm, new player action or knowing disregard of a stopping
condition is claimed.

**Significant authority issue:** “The gate guard is there to speak with” asserts
presence/availability that A's context does not establish. It supplies a player
objective to speak to the guard, which does not itself grant NPC presence/access.
B independently supplies that presence later, so the output matches the overall
fixture, but B is not available to the A call. This is local unsupported encounter
availability, not a contradiction with later authoritative truth. If presence is
intended to be narrated in A, it requires legitimate supplied context; otherwise
the narrator should omit it. No fixture repair or resampling was performed.

**Meaning/comprehension weakness:** failed advance recognition of crumbling
mortar is not clearly conveyed. The sudden stone event is compatible with
surprise but does not explicitly preserve the perceptual timing that explains
the conditional attempt. This is omission/ambiguity, not a demonstrated claim
that the player deliberately ignored danger.

The final merchant-knowledge reminder is off-focus. The passage is clear but thin
and does little to express climbing competence beyond the accepted recovery.

### B — knowledge-bounded exchange (30 words)

> The guard says porter Mara told him she saw the merchant leave through the west gate yesterday. He didn’t see it himself, and doesn’t know which road the merchant took.

Preserves Mara → guard → player attribution, historical timing, lack of firsthand
verification and unknown onward route. No destination, current whereabouts or
independent confirmation is invented. Relevant, economical and intelligible.
Its reported summary is less immediate than direct NPC speech; this is an owner
experiential question, not a requirement that dialogue always use quotation.

### C — established consequential development (32 words)

> The west gate settles fully shut below you, sealing the courtyard exit. Beside you, the guard explains that it’s the scheduled noon closure, then continues speaking as you listen from the battlements.

Expresses the supplied gate closure, blocked passage, guard explanation and
unchanged location. No causal connection to the climb or merchant, arrest,
confinement, threat, alarm or reopening time is invented. Unspecified continued
speech is harmless staging here; it establishes no new substantive answer or
commitment. A concise physical transition with no repeated earlier outcome.

### D — connected continuation (24 words)

> You ask the guard whether there’s another way out while the west gate is shut. He pauses before replying; his answer is still pending.

Carries the gate closure into the relevant authorized question, without travel,
search, route hint, invented exit, promise or refusal. The substantive answer
stays unresolved. No climb/merchant recap or manufactured reverification.

**Significant expression weakness:** “his answer is still pending” is mechanical
explanatory commentary after an adequate in-scene pause. It misses the intended
natural ending, while preserving consequential truth. This fixture deliberately
withholds answer authority; safe restraint is not evidence of a satisfying
ongoing NPC conversation or implemented answer-generation capability.

## Cross-moment assessment

| Dimension | Finding in this pass |
|---|---|
| Consequential fidelity | Resolved climb, endpoint, two-minute cost and gate consequence survive. A adds unsupported local NPC availability. |
| Epistemic fidelity | B retains source chain, timing and knowledge limits. A leaves failed early recognition unclear. No invented merchant route or alternate exit. |
| Agency and constraints | No unauthorized consequential player action or commitment; no assertion of knowingly disregarding danger. Conditional meaning is only partly communicated. |
| Continuity and causality | Consistent battlements location; gate closure motivates D. No invented merchant/closure cause. Later guard context cannot retroactively authorize A's assertion. |
| Relevance and clarity | B/C focused and clear. A's merchant reminder is unnecessary. D repeats conversational status mechanically. |
| Narrative quality | Readable but thin; B is summary, C is the most natural physical beat, D ends like a status message. Owner experience remains decisive. |
| Proportionality | 128 words total; no extended recap or control layers. Concision also omits useful A perceptual meaning. Four short samples establish no general adequacy. |

Historical report retention is only lightly tested: C/D need not repeat the
merchant report, so no long-chain narrated recall is demonstrated. The supplied
semantic history, not prior generated prose, carries continuity. No broad
gameplay, adversarial prior narration, upstream context production, general
memory or error-reliance reconciliation was evaluated.

## Execution, observable checks and reproducibility

First call began at `2026-10-15T17:30:45.653526+00:00`. Requested configuration:
OpenAI Responses, `gpt-6-luna`, low reasoning, 2,048 output-token allowance, existing
20-second timeout, zero SDK retries, `store=false`, no conversation linkage.
The existing text-only adapter returned prose after response-completion checks;
returned model identity, usage, cost and per-call timing were not retained and
are not claimed as independently verified response metadata. No raw response
bodies, response headers or credentials were stored. The existing DPAPI bridge
passed the credential only to the project Python child and removed its launch
environment copy. No credential was displayed, persisted or hashed.

Evidence under the isolated worktree's `.artifacts/f01-realization-evaluation/`:

- `prepared_inputs.json`: exact instructions/context strings, baseline HEAD,
  fixture/component SHA-256 and all evaluation anchors.
- `live_ledger.json`: requested settings, start time and four exact outputs.
- `transcript.md`: unedited prose; `verification.json`: observable results.
- `verify_evidence.py`: offline consistency check, no model-based judging.

Seven evidence checks pass: exact A–D count/order, four nonempty bounded outputs,
exact context/instruction reproduction, unchanged fixture/component bytes,
unchanged fixture in memory and requested configuration. Earlier five offline
component groups and three affected narration regressions remain passed. Tests
did not call providers. Exact inputs/settings support reproduction of the
procedure, not identical stochastic prose. The ledger refuses a second live
pass; none was attempted.

The unchanged candidate was evaluated at uncommitted baseline HEAD
`05bae5dc8504b00740f28be82e500155f39b42c1`; hashes bind its uncommitted component
and fixture. This is an implementation handoff, not a committed review candidate.

## Disposition

Stop for owner review of the four passages. Recommend considering a bounded
correction for A's unsupported availability/perceptual omission and D's ending
only after that review. No substantial missing gameplay design decision was
identified: the boundaries already say not to invent consequential access or
answers. These observations do not establish that single-call realization is
generally sufficient, that multi-stage planning is unnecessary, or which
alternative would help. The accepted reuse assessment remains provisional.
No architecture expansion, second candidate, new sample, merge, publication or
owner acceptance follows from this evaluation.
