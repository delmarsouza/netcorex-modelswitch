from __future__ import annotations

from typing import Protocol

from netcorex_modelswitch.contracts.models import ModelExecutionResult


class ModelProvider(Protocol):
    def execute(self, prompt: str, model: str) -> ModelExecutionResult: ...
