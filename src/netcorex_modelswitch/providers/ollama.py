from __future__ import annotations

import requests

from netcorex_modelswitch.contracts.models import ModelExecutionResult


class OllamaProvider:
    def __init__(self, base_url: str = "http://127.0.0.1:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def execute(self, prompt: str, model: str) -> ModelExecutionResult:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return ModelExecutionResult(
            content=data.get("response", ""),
            provider="ollama",
            model=data.get("model", model),
            input_tokens=data.get("prompt_eval_count", 0),
            output_tokens=data.get("eval_count", 0),
            estimated_cost=0.0,
            latency_ms=0,
        )
