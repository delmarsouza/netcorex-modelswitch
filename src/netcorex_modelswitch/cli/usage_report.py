from __future__ import annotations

import argparse
import json

from netcorex_modelswitch.config.settings import Settings
from netcorex_modelswitch.reporting.usage import UsageReportService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate NetCoreX ModelSwitch usage report")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    service = UsageReportService(Settings().telemetry_log_file)
    summary = service.summarize()

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    totals = summary["totals"]
    print("=== NetCoreX ModelSwitch Usage Report ===")
    print(f"Requests: {totals[requests]}")
    print(f"Input tokens: {totals[input_tokens]}")
    print(f"Output tokens: {totals[output_tokens]}")
    print(f"Estimated cost: {totals[estimated_cost]}")
    print()
    print("--- Providers ---")
    providers = summary["providers"]
    if not providers:
        print("No telemetry events found.")
        return

    for provider, provider_data in providers.items():
        print(
            f"- {provider}: requests={provider_data[requests]}, "
            f"input_tokens={provider_data[input_tokens]}, "
            f"output_tokens={provider_data[output_tokens]}, "
            f"estimated_cost={provider_data[estimated_cost]}"
        )
        for model, model_data in provider_data["models"].items():
            print(
                f"  - {model}: requests={model_data[requests]}, "
                f"input_tokens={model_data[input_tokens]}, "
                f"output_tokens={model_data[output_tokens]}, "
                f"estimated_cost={model_data[estimated_cost]}"
            )


if __name__ == "__main__":
    main()
