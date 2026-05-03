from netcorex_modelswitch.contracts.models import ChannelMessage, Complexity, IntentAssessment, RiskLevel


class IntentAnalyzer:
    def assess(self, message: ChannelMessage) -> IntentAssessment:
        text = message.text.lower().strip()
        has_attachments = bool(message.attachments)
        strategic_terms = ["arquitetura", "estratégia", "proposta", "plano", "decisão", "mvp", "roteamento"]
        coding_terms = ["código", "python", "bug", "debug", "implementa", "adapter", "api"]

        if has_attachments:
            return IntentAssessment(
                domain="document_or_multimodal",
                complexity=Complexity.HIGH,
                risk=RiskLevel.MEDIUM,
                requires_multimodal=True,
                requires_specialist=True,
            )

        if any(term in text for term in strategic_terms):
            return IntentAssessment(
                domain="strategy",
                complexity=Complexity.HIGH,
                risk=RiskLevel.HIGH,
                requires_specialist=True,
            )

        if any(term in text for term in coding_terms):
            return IntentAssessment(
                domain="coding",
                complexity=Complexity.MEDIUM,
                risk=RiskLevel.MEDIUM,
                requires_specialist=True,
            )

        if len(text) < 40:
            return IntentAssessment(
                domain="general",
                complexity=Complexity.LOW,
                risk=RiskLevel.LOW,
            )

        return IntentAssessment(
            domain="general",
            complexity=Complexity.MEDIUM,
            risk=RiskLevel.MEDIUM,
        )
