from pathlib import Path

from netcorex_modelswitch.channels.telegram.runtime import TelegramRuntime
from netcorex_modelswitch.config.settings import Settings
from netcorex_modelswitch.contracts.models import ModelExecutionResult


class FakeTelegramClient:
    def __init__(self):
        self.sent = []

    def get_updates(self, offset=None, timeout=30):
        return []

    def send_message(self, chat_id: str, text: str):
        self.sent.append({"chat_id": chat_id, "text": text})
        return {"ok": True}


class FakeRunner:
    def execute_message(self, message):
        from netcorex_modelswitch.contracts.models import (
            Complexity,
            ExecutionPlan,
            IntentAssessment,
            RiskLevel,
            RoutingDecision,
        )
        from netcorex_modelswitch.telemetry.events import TokenLedgerEvent

        plan = ExecutionPlan(
            coordinator="coordinator",
            specialists=[],
            routing=RoutingDecision(provider="local", model="ollama-local-default", reason="test_reason"),
            assessment=IntentAssessment(domain="general", complexity=Complexity.LOW, risk=RiskLevel.LOW),
        )
        result = ModelExecutionResult(content="Resposta teste", provider="ollama", model="qwen2.5:14b")
        event = TokenLedgerEvent(
            provider="ollama",
            model="qwen2.5:14b",
            route_reason="test_reason",
            input_tokens=1,
            output_tokens=2,
            estimated_cost=0.0,
            latency_ms=3,
        )
        return plan, result, event


def test_telegram_runtime_handles_update_and_sends_message(tmp_path):
    runtime = TelegramRuntime(
        settings=Settings(
            telegram_bot_token="token",
            telemetry_log_file=str(tmp_path / "telemetry.log"),
            telegram_offset_file=str(tmp_path / "offset.txt"),
        )
    )
    runtime.client = FakeTelegramClient()
    runtime.runner = FakeRunner()

    handled = runtime.handle_update(
        {
            "update_id": 1,
            "message": {
                "message_id": 10,
                "text": "Oi",
                "chat": {"id": 1234},
                "from": {"id": 999},
            },
        }
    )

    assert handled is True
    assert runtime.client.sent
    assert runtime.client.sent[0]["chat_id"] == "1234"
    assert "Resposta teste" in runtime.client.sent[0]["text"]
    assert Path(tmp_path / "telemetry.log").exists()


def test_telegram_runtime_handles_start_command(tmp_path):
    runtime = TelegramRuntime(
        settings=Settings(
            telegram_bot_token="token",
            telemetry_log_file=str(tmp_path / "telemetry.log"),
            telegram_offset_file=str(tmp_path / "offset.txt"),
        )
    )
    runtime.client = FakeTelegramClient()
    runtime.runner = FakeRunner()

    handled = runtime.handle_update(
        {
            "update_id": 2,
            "message": {
                "message_id": 11,
                "text": "/start",
                "chat": {"id": 1234},
                "from": {"id": 999},
            },
        }
    )

    assert handled is True
    assert "NetCoreX ModelSwitch está no ar" in runtime.client.sent[0]["text"]


def test_telegram_runtime_handles_usage_command(tmp_path):
    telemetry_log = tmp_path / "telemetry.log"
    telemetry_log.write_text(
        '{"event": {"provider": "ollama", "model": "qwen2.5:14b", "input_tokens": 10, "output_tokens": 20, "estimated_cost": 0.0}}\n',
        encoding="utf-8",
    )
    runtime = TelegramRuntime(
        settings=Settings(
            telegram_bot_token="token",
            telemetry_log_file=str(telemetry_log),
            telegram_offset_file=str(tmp_path / "offset.txt"),
        )
    )
    runtime.client = FakeTelegramClient()
    runtime.runner = FakeRunner()

    handled = runtime.handle_update(
        {
            "update_id": 3,
            "message": {
                "message_id": 12,
                "text": "/usage",
                "chat": {"id": 1234},
                "from": {"id": 999},
            },
        }
    )

    assert handled is True
    assert "NetCoreX Usage Summary" in runtime.client.sent[0]["text"]
    assert "qwen2.5:14b" in runtime.client.sent[0]["text"]
