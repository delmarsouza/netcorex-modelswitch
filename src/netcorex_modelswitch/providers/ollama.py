from netcorex_modelswitch.contracts.models import ModelExecutionResult


class OllamaProvider:
    def __init__(self, base_url: str = "http://127.0.0.1:11434") -> None:
        self.base_url = base_url

    def execute(self, prompt: str, model: str) -> ModelExecutionResult:
        return ModelExecutionResult(
            content=f"[mock-ollama:{model}] {prompt}",
            provider="ollama",
            model=model,
        )
