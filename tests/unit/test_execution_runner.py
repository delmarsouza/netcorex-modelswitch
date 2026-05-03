from netcorex_modelswitch.channels.telegram.adapter import TelegramAdapter
from netcorex_modelswitch.config.settings import Settings
from netcorex_modelswitch.execution.runner import ExecutionRunner


class FakeOllamaProvider:
    def execute(self, prompt: str, model: str):
        from netcorex_modelswitch.contracts.models import ModelExecutionResult

        return ModelExecutionResult(
            content=prompt,
            provider="ollama",
            model=model,
            input_tokens=10,
            output_tokens=20,
            estimated_cost=0.0,
            latency_ms=5,
        )


def test_execution_runner_uses_local_provider_for_simple_messages():
    runner = ExecutionRunner(settings=Settings())
    runner.ollama = FakeOllamaProvider()
    adapter = TelegramAdapter()

    plan, result, event = runner.execute_message(adapter.normalize(user_id="u1", text="Oi"))

    assert plan.routing.provider == "local"
    assert result.provider == "ollama"
    assert "User message" in result.content
    assert event.provider == "ollama"
    assert event.input_tokens == 10
