"""Coordinator adapter for scoped owner contributions, without method dispatch."""
from dataclasses import replace

from engine.activity_control import decide_activity_control
from engine.domain_campaign import domain_owner, prior, scope_for
from engine.gameplay_coordination import DomainStep, Interpretation, SituatedContext, Target
from engine.information_adjudication import Unresolved


class CoordinatedDomain:
    def __init__(self, runtime, command):
        self.runtime, self.command = runtime, command
        self.scope = scope_for(runtime.campaign, command, execution=False, handlers=runtime.domain_handlers)
        self.owner = domain_owner(self.scope, runtime.domain_handlers)

    def interpretation(self):
        a = self.scope.authorization
        return Interpretation(a.method, self.scope.objective, self.scope.target, a.method, a.intent, a.constraints)

    def context(self):
        root, scope = self.runtime.campaign, self.scope
        method = scope.authorization.method
        return SituatedContext(str(root.revision), dict(root.current.world.positions)[scope.actor],
            targets=(Target(scope.target, (scope.target,), method, (method,)),),
            means=self.owner.means(self.command), accessible=scope.notices)

    def assess(self, undertaking, context):
        old = prior(self.runtime.campaign, self.command)
        unavailable = False
        if old is None:
            self.scope = scope_for(self.runtime.campaign, self.command, execution=False,
                                   handlers=self.runtime.domain_handlers)
            execute = self.scope.authorization.intent == 'commit'
            if not execute or decide_activity_control(self.scope.authorization, self.scope.checkpoint).status == 'continue':
                try:
                    self.owner.assess(self.runtime.campaign, self.command, self.scope, execution=execute)
                except Unresolved as error:
                    if execute and error.stage in {'eligibility', 'authorization'}:
                        unavailable = True
                    else:
                        raise
        answered = self.scope.authorization.answered_choices
        checkpoint = replace(self.scope.checkpoint, purpose=undertaking.ref,
            complete=self.scope.checkpoint.complete or old is not None,
            blocked=self.scope.checkpoint.blocked or unavailable,
            developments=tuple(d for d in self.scope.checkpoint.developments if d.choice_key not in answered))
        notices = tuple((k, t) for k, t in self.scope.notices if k not in answered)
        return DomainStep(self.command.id, checkpoint, (self.scope.domain,),
            required_means=self.owner.means(self.command), supported_constraints=self.scope.supported_constraints,
            public_refs=tuple(k for k, _ in notices), choices=tuple((k, k) for k, _ in notices))

    def execute(self, undertaking, step, context):
        if (undertaking.target, undertaking.method, undertaking.constraints) != (
                self.scope.target, self.scope.authorization.method, self.scope.authorization.constraints):
            raise Unresolved('authorization', 'request_mismatch')
        return self.runtime.accept_increment(self.runtime.prepare_increment(self.command))
