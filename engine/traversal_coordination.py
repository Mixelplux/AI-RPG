"""M1 read-only domain adapter at the existing Coordinator/F05 interface.

No separate traversal runtime or acceptance owner. M2 supplies consequential
execution only after the common aggregate/persistence boundary is integrated.
"""
from engine.activity_control import ActivityCheckpoint
from engine.gameplay_coordination import DomainStep
from engine.information_adjudication import Unresolved


class TraversalDomain:
    def __init__(self, resolution, request, ruling):
        self.resolution, self.request, self.ruling = resolution, request, ruling

    def assess(self, undertaking, context):
        r = self.request
        if (undertaking.activity, undertaking.target, undertaking.method) != ('climb', r.route, 'climb'):
            return None
        world, characters = self.resolution.world(), self.resolution.characters()
        if not characters.knows_route(r.creature, r.route):
            raise Unresolved('access', 'route_not_legitimately_known')
        revision = f'{world.frame.revision}:{characters.revision}'
        if context.revision != revision or context.location != dict(world.frame.positions).get(r.creature):
            raise Unresolved('validation', 'stale_traversal_context')
        assessment = self.resolution.assess(r, self.ruling)
        # M1 permits read-only inquiry/preparation through the common coordinator.
        # No public_refs: hidden surface properties/bases never enter its output.
        return DomainStep(r.attempt, ActivityCheckpoint(undertaking.ref, undertaking.method,
            blocked=assessment.status == 'unavailable'),
            ('world_simulation', 'character_system', 'action_resolution'), required_means=r.means)

    def execute(self, undertaking, step, context):
        raise Unresolved('acceptance', 'm2_consequential_integration_required')


class ConsequentialTraversalDomain:
    """M2 adapter to the same Coordinator; no state or publication authority."""
    def __init__(self, runtime, command):
        from engine.historical_campaign import scope_for
        self.runtime, self.command = runtime, command
        self.scope = scope_for(runtime.campaign, command, execution=False)

    def interpretation(self):
        from engine.gameplay_coordination import Interpretation
        a = self.scope.authorization
        return Interpretation('climb', 'Climb the chosen route', self.scope.target,
                              a.method, a.intent, a.constraints)

    def context(self):
        from engine.gameplay_coordination import SituatedContext, Target
        root, r = self.runtime.campaign, self.command.request
        return SituatedContext(str(root.revision), dict(root.current.world.positions)[r.creature],
            targets=(Target(r.route, (r.route,), 'climb', ('climb',)),), means=r.means,
            accessible=self.scope.notices)

    def assess(self, undertaking, context):
        from engine.historical_campaign import inspect, prior, scope_for
        from engine.activity_control import decide_activity_control
        old = prior(self.runtime.campaign, self.command)
        if old is None:
            self.scope = scope_for(self.runtime.campaign, self.command, execution=False)
        unavailable = False
        if old is None:
            if self.scope.authorization.intent == 'commit':
                # A blocked or choice-bearing scope must reach the F05 decision
                # before any execution proposal is prepared.
                if decide_activity_control(self.scope.authorization, self.scope.checkpoint).status == 'continue':
                    try:
                        inspect(self.runtime.campaign, self.command)
                    except Unresolved as error:
                        if self.runtime.campaign.schema == 3 and error.stage in {'eligibility', 'authorization'}:
                            unavailable = True
                        else:
                            raise
            else:
                inspect(self.runtime.campaign, self.command, execution=False)
        checkpoint = self.scope.checkpoint
        from dataclasses import replace
        # Exact owner-recorded answers apply only to their established choice keys.
        answered = self.scope.authorization.answered_choices
        checkpoint = replace(checkpoint, purpose=undertaking.ref, complete=checkpoint.complete or old is not None,
            blocked=checkpoint.blocked or unavailable,
            developments=tuple(d for d in checkpoint.developments if d.choice_key not in answered))
        return DomainStep(self.command.request.attempt, checkpoint,
            ('world_simulation', 'character_system', 'action_resolution'),
            required_means=self.command.request.means, supported_constraints=self.scope.supported_constraints,
            public_refs=tuple(key for key, _ in self.scope.notices if key not in answered),
            choices=tuple((key, key) for key, _ in self.scope.notices if key not in answered))

    def execute(self, undertaking, step, context):
        if (undertaking.activity, undertaking.target, undertaking.method, undertaking.constraints) != (
                'climb', self.scope.target, 'climb', self.scope.authorization.constraints):
            raise Unresolved('authorization', 'request_mismatch')
        proposal = self.runtime.prepare_increment(self.command)
        return self.runtime.accept_increment(proposal)
