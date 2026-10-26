# Physical Traversal Core V1a — M1 implementation model

Status: bounded M1 implementation model accepted by the owner October 26, 2026.
Baseline: 85ec1811315686f9ea6691235078bf10c25265fc. Elevated risk.

## Domain interfaces and ownership

World supplies immutable local places, traversal links, surfaces, creature positions,
physical instances and simultaneous typed relationships. Identity is independent
of definition, name and inventory. Unknown material fields remain unavailable.
World owns fictional time and causal references, including established actual falls.
This is local relational space, not universal geometry or a physics simulation.

Character supplies the same sparse rule profile for PCs and NPCs: Speed/Climb Speed,
Strength, Athletics training, relevant conditions, scoped traits, accepted movement expenditure and HP premises,
equipment readiness and explicit legitimate route access. It never stores another
copy of physical position, attachment, possession or object condition.

Action & Resolution asks those owners for the selected movement's dependencies,
prepares a typed rule assessment, and optionally samples a provisional result.
Suppliers must compose all applicable material bindings before supplying a view;
known unresolved surface bindings or creature effects explicitly block resolution.
No fixture supplies a successful climb. No coordinator chooses a mechanical result.
Missing/unsupported facts and stale assessments raise internal unresolved errors.
The same position/link/profile contracts and general physical-capability query can
serve future swimming and jumping;
only climbing rules are implemented here. No generic effect/rules framework.

The existing I1 Coordinator and F05 checkpoint interface are reused for structural
assessment, authorization and stale-context tests. Its M1 adapter is read-only and
cannot accept execution. No alternate transaction/runtime or competing publication
authority is introduced. M2 must extend or replace the finite I2/I3 result/root
representation within the same common runtime authority, retaining compatibility
readers. It must connect these domain results to one common consequential aggregate, with exact attempt recognition, dependent costs/time,
World position and Character changes accepted together. The existing GameEngine,
I2/I3 root swap, receipts and finite codec are reusable resources, not prescribed
new-domain shapes. The finite d6 policy and inventory-as-physical-truth assumptions
are excluded from new mechanics. Legacy gameplay remains operational.

## Rules reference and bounded coverage

Official references verified October 25, 2026:
[2024 Rules Glossary](https://www.dndbeyond.com/sources/dnd/br-2024/rules-glossary)
and [Playing the Game](https://www.dndbeyond.com/sources/dnd/br-2024/playing-the-game).

Movement cost per foot: ordinary climbing 2, difficult climbing 3; using Climb
Speed 1, or 2 in difficult terrain. Selected speed and already spent movement
constrain a turn segment. No universal six-second outdoor climbing loop.

A grounded DM ruling may invoke DC 15 Strength (Athletics) on slippery or sparse
handholds; such circumstances alone do not mandate a roll. Climb Speed does not
waive a justified check. Training/expertise, applicable Strength-check advantage,
poison disadvantage and Exhaustion apply. Unsupported conditions/effects remain
unresolved. Ability checks use totals without automatic natural-1/20 outcomes.

Failure establishes only the unsuccessful objective; physical disposition remains
for grounded World adjudication before acceptance. It neither asserts a safe
position nor creates a fall. A separately established dry-ground fall yields
capped d6 Bludgeoning damage and the applicable Prone result. Water entry,
mitigation, zero-HP/death handling and reactions require later supported rules.

## Accepted owner clarifications — October 26, 2026

Authority: owner's M1 Blocking Corrections and Accepted Clarifications instruction.
This records the explicitly authorized coordination treatment under CD-02's accepted
adaptation/ruling basis. It is not a claim that the 2024 Stunned text sets Speed to
zero or itself specifies this coordination restriction. Canonical CD/PT ownership
and consequence contracts remain unchanged; the owner subsequently accepted M1
on October 26 after both blocking corrections and verification.

Character's general `PhysicalCapability` query separates effective Speed/Climb Speed,
coordinated-movement capability and Actions/Bonus Actions/Reactions. Stunned leaves
Speed allowance intact but removes deliberate physical coordination; its
Incapacitated effect prevents all three action categories. Basic unsteady movement
allowance therefore remains. Incapacitated alone does not remove coordination or
Speed. Other supported immobility and Exhaustion effects retain their meanings.
Action & Resolution determines the technique's requirements: climbing requires
coordination even without an Athletics check. No method-specific Stunned branch
is introduced for future methods to copy. No other movement system is implemented.
Becoming Stunned invalidates an affected prepared climb; it does not establish a
fall, injury, lost grip or safe retained support.

Fall sampling captures the immutable starting PhysicalFrame and Character revision,
then compares current authoritative values against those captures before returning.
A reused mutable supplier wrapper cannot change the comparison baseline. Dependent
publication and accepted retry recognition still belong to M2.

The falling-risk principle is no automatic fall and no automatic safe failure.
`objective_not_achieved` is a mechanical objective result, not a safe-position or
no-injury adjudication. Loss of footing/grip, actual falling and damage are separate
meanings. A later grounded World fall occurrence can invoke the existing damage
contribution; M1 does not derive that occurrence from a failed die or suppress it.
M1 does not yet supply all elevation, footing, assistance and protection premises
needed for full failure-consequence adjudication. No convenient support may be
invented after sampling, and possession of a rope does not establish protection.

### Required M2 validation, not implementation in M1

- Exposed, unsecured difficult climb at meaningful height: establish position,
  elevation, handholds/footholds, absence of protection, assistance and relevant
  causes before resolution. Failed climbing must carry substantial grounded
  falling risk, rather than defaulting every failure to harmless no-progress.
  Distinguish failed progress, lost grip/footing, actual fall and damage. No new
  numerical risk rule is selected here; do not manufacture a ledge/anchor after
  the roll to preserve safety.
- Properly protected climb: verify actual anchor, rope, attachment, condition and
  applicable protection/assistance, not an inventory label. A failed objective or
  lost grip must respect that protection; it cannot manufacture an unprotected
  fall. Protection is not a blanket promise that any rope prevents every injury.
- Failure before substantial elevation: preserve established ground/low position;
  a failed check alone must not create a fall from height or falling damage.

Validate all three through the common coherent acceptance, continuation and save
boundary using current owner premises. Reject stale dependencies without effects;
no duplicate movement, costs or damage on resumption. These are M2 requirements,
not evidence of implemented M1 consequence adjudication or authorization to start M2.

## Persistence and compatibility established before writes

M1 introduces no save writes, version change, migration or accepted gameplay state.
The new typed records are read-only owner views and unaccepted results, not an
independent saved campaign. Existing v1 and v2 save readers/writers remain intact.
A missing new-domain model in old saves means unsupported traversal, never guessed
positions, equipment, character statistics or an automatic conversion.

For M2, use an explicitly versioned domain section in a deliberate new campaign
representation, rather than fitting these records into finite d6 Method/Assessment
shapes. Preserve existing v1/v2 load behavior; opt-in new campaigns only, no automatic
migration. Validate the complete candidate and references before adoption; save by
same-directory temporary file and atomic replacement. Persist one World physical
truth, Character capabilities/resources, and accepted attempt/result/cost/time and
activity recognition together. Reject unknown versions or incoherent references
without altering live state or the previous save. Concrete envelope/version selection
and codec integration precede M2 incompatible writes; no writer is introduced now.

## M1 boundary and verification

M1 demonstrates reusable domain mechanics, relationship invariants, selective
owner reads, unavailable-input containment, stale-state checks and the common I1
assessment seam. It does not claim continuing climb gameplay, persistent new-domain
state, accepted movement/damage, parser support or complete condition coverage.
M2 owns coherent consequential integration, save/load and resumption. No M2 begins
through this handoff. Region Pack authoring stays with World Forge; trusted runtime
suppliers may compose validated premises without predetermining outcomes.
