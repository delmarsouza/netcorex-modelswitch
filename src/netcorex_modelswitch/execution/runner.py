from netcorex_modelswitch.config.settings import Settings
from netcorex_modelswitch.contracts.models import ChannelMessage, ExecutionPlan, ModelExecutionResult
from netcorex_modelswitch.orchestrator.planner import ExecutionPlanner
from netcorex_modelswitch.providers.ollama import OllamaProvider


class ExecutionRunner:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.planner = ExecutionPlanner()
        self.ollama = OllamaProvider(base_url=self.settings.ollama_base_url)

    def build_prompt(self, message: ChannelMessage, plan: ExecutionPlan) -> str:
        specialists = ", ".join(item.specialist for item in plan.specialists) or "none"
        return (
            f"Channel: {message.channel.value}\n"
            f"User: {message.user_id}\n"
            f"Domain: {plan.assessment.domain}\n"
            f"Complexity: {plan.assessment.complexity.value}\n"
            f"Risk: {plan.assessment.risk.value}\n"
            f"Specialists: {specialists}\n\n"
            f"User message:\n{message.text}\n"
        )

    def execute_message(self, message: ChannelMessage) -> tuple[ExecutionPlan, ModelExecutionResult]:
        plan = self.planner.plan(message)
        model = plan.routing.model
        if plan.routing.provider == "local":
            result = self.ollama.execute(self.build_prompt(message, plan), model=self.settings.ollama_default_model)
            return plan, result

        result = ModelExecutionResult(
            content="Premium provider execution not implemented yet.",
            provider=plan.routing.provider,
            model=model,
        )
        return plan, result
