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
