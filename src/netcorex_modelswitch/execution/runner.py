from netcorex_modelswitch.config.settings import Settings
from netcorex_modelswitch.contracts.models import ChannelMessage, ExecutionPlan, ModelExecutionResult
from netcorex_modelswitch.orchestrator.planner import ExecutionPlanner
from netcorex_modelswitch.providers.ollama import OllamaProvider
from netcorex_modelswitch.telemetry.events import TokenLedgerEvent


class ExecutionRunner:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.planner = ExecutionPlanner()
        self.ollama = OllamaProvider(base_url=self.settings.ollama_base_url)

    def build_prompt(self, message: ChannelMessage, plan: ExecutionPlan) -> str:
        specialists = ", ".join(item.specialist for item in plan.specialists) or "none"
        return (
            "You are NetCoreX ModelSwitch running in Telegram-first pilot mode. "
            "Answer clearly, directly, and helpfully in the user's language when possible.\n\n"
            f"Channel: {message.channel.value}\n"
            f"User: {message.user_id}\n"
            f"Domain: {plan.assessment.domain}\n"
            f"Complexity: {plan.assessment.complexity.value}\n"
            f"Risk: {plan.assessment.risk.value}\n"
            f"Specialists: {specialists}\n\n"
            f"User message:\n{message.text}\n"
        )

    def execute_message(self, message: ChannelMessage) -> tuple[ExecutionPlan, ModelExecutionResult, TokenLedgerEvent]:
        plan = self.planner.plan(message)
        model = plan.routing.model
        if plan.routing.provider == "local":
            result = self.ollama.execute(self.build_prompt(message, plan), model=self.settings.ollama_default_model)
        else:
            result = ModelExecutionResult(
                content="Premium provider execution not implemented yet.",
                provider=plan.routing.provider,
                model=model,
            )

        event = TokenLedgerEvent(
            provider=result.provider,
            model=result.model,
            route_reason=plan.routing.reason,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            estimated_cost=result.estimated_cost,
            latency_ms=result.latency_ms,
            fallback_triggered=False,
        )
        return plan, result, event
