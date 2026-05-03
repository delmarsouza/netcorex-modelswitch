from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


class UsageReportService:
    def __init__(self, log_file: str) -> None:
        self.log_file = Path(log_file)

    def load_events(self) -> list[dict[str, Any]]:
        if not self.log_file.exists():
            return []
        events = []
        for line in self.log_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
        return events

    def summarize(self) -> dict[str, Any]:
        events = self.load_events()
        by_provider: dict[str, dict[str, Any]] = defaultdict(lambda: {
            "requests": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "estimated_cost": 0.0,
            "models": defaultdict(lambda: {
                "requests": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "estimated_cost": 0.0,
            }),
        })

        totals = {
            "requests": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "estimated_cost": 0.0,
        }

        for item in events:
            event = item.get("event", {})
            provider = event.get("provider", "unknown")
            model = event.get("model", "unknown")
            input_tokens = int(event.get("input_tokens", 0) or 0)
            output_tokens = int(event.get("output_tokens", 0) or 0)
            estimated_cost = float(event.get("estimated_cost", 0.0) or 0.0)

            totals["requests"] += 1
            totals["input_tokens"] += input_tokens
            totals["output_tokens"] += output_tokens
            totals["estimated_cost"] += estimated_cost

            provider_row = by_provider[provider]
            provider_row["requests"] += 1
            provider_row["input_tokens"] += input_tokens
            provider_row["output_tokens"] += output_tokens
            provider_row["estimated_cost"] += estimated_cost

            model_row = provider_row["models"][model]
            model_row["requests"] += 1
            model_row["input_tokens"] += input_tokens
            model_row["output_tokens"] += output_tokens
            model_row["estimated_cost"] += estimated_cost

        normalized = {}
        for provider, data in by_provider.items():
            normalized[provider] = {
                "requests": data["requests"],
                "input_tokens": data["input_tokens"],
                "output_tokens": data["output_tokens"],
                "estimated_cost": round(data["estimated_cost"], 6),
                "models": {
                    model: {
                        "requests": model_data["requests"],
                        "input_tokens": model_data["input_tokens"],
                        "output_tokens": model_data["output_tokens"],
                        "estimated_cost": round(model_data["estimated_cost"], 6),
                    }
                    for model, model_data in data["models"].items()
                },
            }

        totals["estimated_cost"] = round(totals["estimated_cost"], 6)
        return {
            "totals": totals,
            "providers": normalized,
        }
