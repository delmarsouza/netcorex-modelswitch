from netcorex_modelswitch.contracts.models import IntentAssessment, SpecialistAssignment


class SpecialistRegistry:
    def assign(self, assessment: IntentAssessment) -> list[SpecialistAssignment]:
        if not assessment.requires_specialist:
            return []

        mapping = {
            "strategy": [SpecialistAssignment("business_strategy", "strategic analysis required")],
            "coding": [SpecialistAssignment("coding", "implementation or debugging requested")],
            "document_or_multimodal": [
                SpecialistAssignment("research", "document or multimodal interpretation required"),
                SpecialistAssignment("content_communication", "response synthesis required"),
            ],
        }
        return mapping.get(assessment.domain, [SpecialistAssignment("research", "general specialist fallback")])
