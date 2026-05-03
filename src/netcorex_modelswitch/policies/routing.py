from netcorex_modelswitch.contracts.models import Complexity, IntentAssessment, RiskLevel, RoutingDecision


class RoutingPolicyV1:
    def decide(self, assessment: IntentAssessment) -> RoutingDecision:
        if assessment.requires_multimodal:
            return RoutingDecision(
                provider="gemini",
                model="gemini-multimodal-default",
                reason="multimodal_or_document_path",
                fallback_chain=["chatgpt-premium"],
            )

        if assessment.risk == RiskLevel.HIGH or assessment.complexity == Complexity.HIGH:
            return RoutingDecision(
                provider="chatgpt",
                model="chatgpt-premium-default",
                reason="high_risk_or_high_complexity",
                fallback_chain=["gemini-general", "local-premium"],
            )

        if assessment.complexity == Complexity.LOW:
            return RoutingDecision(
                provider="local",
                model="ollama-local-default",
                reason="low_complexity_local_first",
                fallback_chain=["chatgpt-economy"],
            )

        return RoutingDecision(
            provider="local",
            model="ollama-local-plus",
            reason="medium_complexity_local_bias",
            fallback_chain=["chatgpt-premium-default"],
        )
