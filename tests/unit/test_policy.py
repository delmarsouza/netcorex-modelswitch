from netcorex_modelswitch.contracts.models import Complexity, IntentAssessment, RiskLevel
from netcorex_modelswitch.policies.routing import RoutingPolicyV1


def test_policy_prefers_local_for_low_complexity():
    policy = RoutingPolicyV1()
    decision = policy.decide(IntentAssessment(domain="general", complexity=Complexity.LOW, risk=RiskLevel.LOW))
    assert decision.provider == "local"


def test_policy_escalates_high_risk_to_chatgpt():
    policy = RoutingPolicyV1()
    decision = policy.decide(IntentAssessment(domain="strategy", complexity=Complexity.HIGH, risk=RiskLevel.HIGH))
    assert decision.provider == "chatgpt"
