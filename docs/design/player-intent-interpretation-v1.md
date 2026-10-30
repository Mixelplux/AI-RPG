# Player Intent Interpretation V1

Owner accepted the Design and authorized implementation October 30, 2026 in the
supplied **Accepted Design → Implementation Handoff**, against baseline
`870d1080e67c2f943d12a7bd74952d26ed56b5d2`. The semantics below record that
handoff. Exact serialization and local integration choices are implementation
details submitted for owner review, not claims of implementation acceptance.

The interpreter identifies intended meaning. It does not authorize, adjudicate,
execute, establish world truth, select mechanics or narrate results. Hosted and
local models use the same interface; Qwen3.5-2B is research evidence, not a
selected or qualified production dependency. No inference experiment is part of
this package.

## Accepted semantics and reconciliation

- Preserve feasibility inquiries, statements, preparations and committed
  in-world actions. Committed questioning of an NPC is an action. Expressed
  commitment is input to F05/Coordinator authorization, never an execution permit.
- Preserve affirmative requests and their chosen methods and restrictions.
  Omitted fields do not imply prohibitions: running toward a cart does not
  prohibit reaching it. Ordinary uncertain continuation is not an added action.
- Use appropriate specificity: examining a ledger may reveal relevant contents
  without the player naming an undiscovered correction note. Domains still
  discover and obtain their actual dependencies; interpreter omissions neither
  establish facts nor certify information sufficiency.
- Preserve separate intentions and expressed relationships. The Coordinator
  bounds execution to one coherent undertaking; no interpretation creates a
  queue. Material unresolved meaning returns control for clarification.
- Use only supplied context identifiers. Preserve continuation/retry meaning
  without deciding whether earlier mechanics repeat. Owning systems reassess
  circumstances and preserve accepted costs/results under existing continuity.
- Candidate domains are advisory. World, Character, Action & Resolution and
  Actors & Social Dynamics retain authority; Information Foundation retrieves
  legitimate information and confers no outcome authority.

This specializes [IG-01–03, IG-20, IG-22–23](integrated-gameplay-architecture-v1.md),
[F05](f05-authorized-activities-and-player-control.md), the
[shared doctrines](systems/README.md#shared-doctrines),
[Information Foundation](information-foundation-functional-design-v1.md),
[Information-Grounded Adjudication](information-grounded-adjudication-v1.md) and
[Core Gameplay Domains](core-gameplay-domains-cross-domain-contract-design-v1.md).
Existing consequential acceptance, recovery and save compatibility remain
authoritative. No conflicting accepted requirement was identified.

## Exact wire contract

Input to `engine.player_intent.normalize` is **JSON text**, not a Python mapping,
provider envelope, Markdown fence or executable object. UTF-8 is the wire
encoding. Exactly these four top-level fields are required:

```json
{"version":1,"intentions":[],"relationships":[],"ambiguities":[]}
```

`version` is integer `1` (boolean/float are invalid). The other fields are arrays.
No field is nullable. Unknown keys at every object level are rejected, including
authorization, execution, outcome, cost, roll, world-state and queue fields.

Each intention is an object:

| Field | Type and meaning |
|---|---|
| `id` | Required locally unique identifier. |
| `mode` | Required: `inquiry`, `statement`, `preparation`, `action`. |
| `commitment` | Required: `none`, `now`, `conditional`. |
| `activity` | Required natural-language description of the requested activity. |
| `goal` | Optional natural-language objective, string. |
| `targets` | Optional array of natural-language intended targets; naming one does not establish existence/access. |
| `method` | Optional natural-language chosen method, string. |
| `constraints` | Optional array of expressed restrictions. |
| `conditions` | Optional array of natural-language conditions/premises. No conditional programming language. |
| `stop_at` | Optional array of expressed stopping boundaries. |
| `context_refs` | Optional array of identifiers from this request's accessible context only. |
| `candidate_domains` | Optional array containing `world`, `character`, `resolution`, `actors`, advisory only. |
| `source` | Optional string containing a verbatim contiguous excerpt of the original player input. |

Inquiry and statement require commitment `none`. Action requires `now` or
`conditional`. Preparation allows all three: `none` is a read-only preparation
assessment; actual preparation can be committed, subject to a supported owning
capability. Conditional commitment requires at least one condition. Commitment
`now` with conditions is inconsistent and rejected; use `conditional` instead.
Uncommitted inquiry/statement/preparation can carry hypothetical conditions.
Methods, constraints and stop boundaries remain separate.

Relationships are objects with exactly `type`, `from`, `to`; the endpoints must
be distinct existing intention IDs. Type is `precedes`, `depends_on`,
`alternative`, `together` or `independent`. `from depends_on to` means `to` is a
prerequisite of `from`. Duplicate relationships, including reversed duplicates
of symmetric relationships, are rejected. Precedence/dependency cycles are
rejected. For the same pair, alternative conflicts with precedes/depends_on/
together; together conflicts with independent. Ordered independent intentions
are representable. Relationships describe meaning and confer no execution order.

Ambiguities are objects with exactly `intentions` (array of affected IDs) and
`issue` (natural-language material unresolved meaning). Empty affected IDs mean
the entire input. Duplicate ambiguities and nonexistent references are rejected.
Empty intentions and ambiguities are structurally valid; gameplay asks for an
immediate undertaking. Missing domain facts alone are not material intent ambiguity.

Bounds: 32,768 UTF-8 output bytes; 8 intentions; 32 relationships; 8 ambiguities;
16 entries per optional string array; 1,024 characters per nonempty text;
64 characters per identifier. Identifiers match
`[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}`. Ambiguity ID arrays have at most 8 entries.
String arrays cannot contain duplicates after trimming. Control characters
other than newline, carriage return and tab, lone Unicode surrogates, duplicate
JSON keys, non-finite numbers, trailing content and malformed JSON are rejected.

Normalization trims leading/trailing descriptive whitespace, preserves internal
wording and optional omissions/empty arrays, and performs no semantic repair,
method selection or inference. Canonical serialization is Python JSON with
`sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=False`,
`allow_nan=False`, no trailing newline. `InterpretationV1.json` is immutable;
`to_dict()` returns a fresh copy. Normalization does not prove semantic fidelity.

## Local integration contract

`Coordinator.decide_intent(text, provider=callable)` obtains trusted current
`SituatedContext`. The replaceable callable receives an immutable
`InterpretationRequest(player_input, context, instructions)` and returns JSON
text. It receives the exact original input and only `context.accessible` pairs,
never hidden conditions, internal means, targets or full adjudication context.
Accessible context IDs follow the identifier rule; at most 64 pairs, each text
at most 8,192 characters. Original input is nonempty and at most 8,192 characters.
The provider adapter owns its transport timeout/cancellation and response-text
extraction. This implementation performs no retry, selects no model and adds no
SDK/server dependency or implicit live call.

Validated single-intention meaning, exact original input and original trusted
context form immutable `IntentHandoff`. The installed domain may implement
read-only `bind_intent(handoff) -> existing Interpretation | None` to bind a
supported meaning/target/method to its existing internal capability identifiers.
This is the owning capability adapter, not another general-purpose interpreter.
It must reject unsupported or materially incomplete meaning, methods and
targets, and must not choose unrequested consequential means. It receives all
optional details; binding cannot rely on candidate-domain labels as authority.
No general natural-language binder is claimed or installed for legacy routes.

The Coordinator derives inquiry/preparation/commitment from validated V1,
preserves expressed constraints, conditions and stop boundaries, and rechecks
context after inference/binding, at decision and before execution. Existing
target/method availability, F05, single-use permission, domain assessment and
consequential acceptance remain required. Owners establish `satisfied_conditions`
and implement `supported_stops` on `DomainStep`; absent support fails closed.
These strings are never evaluated as code. All three boundary kinds carry
forward when refining/resuming an existing undertaking.

Material ambiguity returns generic clarification before binding. Multiple
intentions always return a choice of one immediate undertaking in this V1
integration, including `together`; their representation is preserved, but none
are selected, executed or queued automatically. This conservative local boundary
does not redefine coherent routine steps within an already authorized activity.
A single bound undertaking retains existing bounded situated progression/F05.

Statements return a non-fictional acknowledgment without domain execution.
Malformed output, fabricated refs, unsupported bindings, stale context and
provider/adapter exceptions return contained operational failures. They never
fall through to another interpreter, expose model diagnostics or consume time,
resources or accepted campaign state. A previously pending permit is invalidated;
already accepted progress remains intact.

`process_intent` reuses existing Coordinator progression. The explicit
`GameEngine.process_player_intent` entry returns its existing public result
shape. Ordinary `process_command`, Watchhouse CLI and older deterministic
harnesses retain their existing paths; no production model is silently enabled.
Continuation/retry references pass to the owner binding; accepted-step recognition
and common Runtime receipts retain their existing no-reroll/no-duplicate rules.
Provider/interpretation objects and conditions/stop support are session-local;
no persisted record, save version, codec, migration or publication path changes.

## Research and remaining limits

Stage A's P10 invented a stop-before-arrival restriction; P03/P07 used imprecise
commitment terminology. Stage B's E03/E04 omitted a possible note-existence gap.
Focused offline cases cover these failure classes without rerunning inference:
preserve affirmative scope, committed questioning/search, proportionate targets,
and owner-discovered prerequisites. Conditions, stopping, multiple intentions,
missing contextual references and continuation also reuse representative research
themes. They test the contract and integration, not model language quality.

Evidence remains unchanged at
`C:/tmp/AI-RPG-Intent-Pilot-20261029T232046Z` and
`C:/tmp/AI-RPG-Intent-StageB-20261029-V1`. Neither research output schema was
promoted to the production contract. Structural checks cannot detect every
misread commitment, invented restriction, omitted condition, wrong target or
authority claim embedded in prose. Trusted domain binding and owner validation
remain essential; a structurally valid interpretation is never world truth.
Model qualification and broader language integration remain separately authorized.
