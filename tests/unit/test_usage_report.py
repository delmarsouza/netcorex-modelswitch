import json

from netcorex_modelswitch.reporting.usage import UsageReportService


def test_usage_report_aggregates_provider_and_model(tmp_path):
    log_file = tmp_path / "telemetry.log"
    events = [
        {
            "event": {
                "provider": "ollama",
                "model": "qwen2.5:14b",
                "input_tokens": 10,
                "output_tokens": 20,
                "estimated_cost": 0.0,
            }
        },
        {
            "event": {
                "provider": "chatgpt",
                "model": "gpt-5-mini",
                "input_tokens": 30,
                "output_tokens": 40,
                "estimated_cost": 0.12,
            }
        },
    ]
    log_file.write_text("\n".join(json.dumps(item) for item in events), encoding="utf-8")

    summary = UsageReportService(str(log_file)).summarize()

    assert summary["totals"]["requests"] == 2
    assert summary["totals"]["input_tokens"] == 40
    assert summary["providers"]["ollama"]["models"]["qwen2.5:14b"]["output_tokens"] == 20
    assert summary["providers"]["chatgpt"]["estimated_cost"] == 0.12
