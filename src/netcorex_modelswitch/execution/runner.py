from netcorex_modelswitch.config.settings import Settings
from netcorex_modelswitch.contracts.models import ChannelMessage, ExecutionPlan, ModelExecutionResult
from netcorex_modelswitch.orchestrator.planner import ExecutionPlanner
from netcorex_modelswitch.providers.ollama import OllamaProvider
from netcorex_modelswitch.providers.openai_provider import OpenAIProvider
from netcorex_modelswitch.telemetry.events import TokenLedgerEvent


class ExecutionRunner:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.planner = ExecutionPlanner()
        self.ollama = OllamaProvider(base_url=self.settings.ollama_base_url)
        self.openai = OpenAIProvider(
            api_key=self.settings.openai_api_key,
            base_url=self.settings.openai_base_url,
        ) if self.settings.openai_api_key else None

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
        prompt = self.build_prompt(message, plan)
        fallback_triggered = False

        if plan.routing.provider == "local":
            result = self.ollama.execute(prompt, model=self.settings.ollama_default_model)
        elif plan.routing.provider in {"chatgpt", "openai"}:
            if self.openai is not None:
                result = self.openai.execute(prompt, model=self.settings.openai_default_model)
            else:
                fallback_triggered = True
                result = self.ollama.execute(prompt, model=self.settings.ollama_default_model)
        else:
            if self.openai is not None:
                fallback_triggered = True
                result = self.openai.execute(prompt, model=self.settings.openai_default_model)
            else:
                fallback_triggered = True
                result = self.ollama.execute(prompt, model=self.settings.ollama_default_model)

        event = TokenLedgerEvent(
            provider=result.provider,
            model=result.model,
            route_reason=plan.routing.reason,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            estimated_cost=result.estimated_cost,
            latency_ms=result.latency_ms,
            fallback_triggered=fallback_triggered,
        )
        return plan, result, event
