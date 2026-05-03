from netcorex_modelswitch.agents.registry import SpecialistRegistry
from netcorex_modelswitch.contracts.models import ChannelMessage, ExecutionPlan
from netcorex_modelswitch.intent.analyzer import IntentAnalyzer
from netcorex_modelswitch.policies.routing import RoutingPolicyV1


class ExecutionPlanner:
    def __init__(self) -> None:
        self.intent_analyzer = IntentAnalyzer()
        self.routing_policy = RoutingPolicyV1()
        self.registry = SpecialistRegistry()

    def plan(self, message: ChannelMessage) -> ExecutionPlan:
        assessment = self.intent_analyzer.assess(message)
        routing = self.routing_policy.decide(assessment)
        specialists = self.registry.assign(assessment)
        return ExecutionPlan(
            coordinator="coordinator",
            specialists=specialists,
            routing=routing,
            assessment=assessment,
        )
