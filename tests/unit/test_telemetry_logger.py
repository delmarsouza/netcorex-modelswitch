from pathlib import Path

from netcorex_modelswitch.telemetry.events import TokenLedgerEvent
from netcorex_modelswitch.telemetry.logger import TelemetryLogger


def test_telemetry_logger_appends_jsonl(tmp_path):
    file_path = tmp_path / "telemetry.log"
    logger = TelemetryLogger(str(file_path))
    event = TokenLedgerEvent(
        provider="ollama",
        model="qwen2.5:14b",
        route_reason="low_complexity_local_first",
        input_tokens=10,
        output_tokens=20,
        estimated_cost=0.0,
        latency_ms=5,
    )

    logger.append(event, extra={"chat_id": "1234"})

    assert Path(file_path).exists()
    content = file_path.read_text(encoding="utf-8")
    assert '"provider": "ollama"' in content
    assert '"chat_id": "1234"' in content
