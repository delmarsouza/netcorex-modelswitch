from __future__ import annotations

import argparse
import json

from netcorex_modelswitch.channels.telegram.adapter import TelegramAdapter
from netcorex_modelswitch.execution.runner import ExecutionRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run NetCoreX ModelSwitch locally")
    parser.add_argument("--message", required=True, help="Message to send through the local execution flow")
    parser.add_argument("--user-id", default="local-user", help="Synthetic user id for local runs")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    adapter = TelegramAdapter()
    runner = ExecutionRunner()
    message = adapter.normalize(user_id=args.user_id, text=args.message)
    plan, result = runner.execute_message(message)

    payload = {
        "input": {
            "channel": message.channel.value,
            "user_id": message.user_id,
            "text": message.text,
        },
        "assessment": {
            "domain": plan.assessment.domain,
            "complexity": plan.assessment.complexity.value,
            "risk": plan.assessment.risk.value,
            "requires_multimodal": plan.assessment.requires_multimodal,
            "requires_specialist": plan.assessment.requires_specialist,
        },
        "routing": {
            "provider": plan.routing.provider,
            "model": plan.routing.model,
            "reason": plan.routing.reason,
            "fallback_chain": plan.routing.fallback_chain,
        },
        "specialists": [
            {"name": specialist.specialist, "reason": specialist.reason}
            for specialist in plan.specialists
        ],
        "result": {
            "provider": result.provider,
            "model": result.model,
            "content": result.content,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
            "estimated_cost": result.estimated_cost,
            "latency_ms": result.latency_ms,
        },
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print("=== NetCoreX ModelSwitch Local Run ===")
    print(f"Channel: {payload['input']['channel']}")
    print(f"User: {payload['input']['user_id']}")
    print(f"Message: {payload['input']['text']}")
    print()
    print("--- Assessment ---")
    print(f"Domain: {payload['assessment']['domain']}")
    print(f"Complexity: {payload['assessment']['complexity']}")
    print(f"Risk: {payload['assessment']['risk']}")
    print(f"Requires specialist: {payload['assessment']['requires_specialist']}")
    print(f"Requires multimodal: {payload['assessment']['requires_multimodal']}")
    print()
    print("--- Routing ---")
    print(f"Provider: {payload['routing']['provider']}")
    print(f"Model: {payload['routing']['model']}")
    print(f"Reason: {payload['routing']['reason']}")
    print(f"Fallback chain: {', '.join(payload['routing']['fallback_chain']) or 'none'}")
    print()
    print("--- Specialists ---")
    if payload['specialists']:
        for specialist in payload['specialists']:
            print(f"- {specialist['name']}: {specialist['reason']}")
    else:
        print("- none")
    print()
    print("--- Result ---")
    print(f"Provider: {payload['result']['provider']}")
    print(f"Model: {payload['result']['model']}")
    print(f"Input tokens: {payload['result']['input_tokens']}")
    print(f"Output tokens: {payload['result']['output_tokens']}")
    print(f"Estimated cost: {payload['result']['estimated_cost']}")
    print()
    print(payload['result']['content'])


if __name__ == "__main__":
    main()
