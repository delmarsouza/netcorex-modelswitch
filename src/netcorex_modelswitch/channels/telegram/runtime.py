from __future__ import annotations

from pathlib import Path

from netcorex_modelswitch.channels.telegram.adapter import TelegramAdapter
from netcorex_modelswitch.channels.telegram.client import TelegramClient
from netcorex_modelswitch.config.settings import Settings
from netcorex_modelswitch.execution.runner import ExecutionRunner
from netcorex_modelswitch.telemetry.logger import TelemetryLogger


class TelegramRuntime:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        if not self.settings.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required for Telegram runtime")
        self.adapter = TelegramAdapter()
        self.client = TelegramClient(self.settings.telegram_bot_token)
        self.runner = ExecutionRunner(self.settings)
        self.telemetry = TelemetryLogger(self.settings.telemetry_log_file)

    def handle_update(self, update: dict) -> bool:
        message = self.adapter.from_update(update)
        if not message:
            return False

        chat_id = message.metadata.get("chat_id")
        if not chat_id:
            return False

        command_reply = self._handle_command(message.text)
        if command_reply is not None:
            self.client.send_message(chat_id=chat_id, text=command_reply)
            return True

        plan, result, event = self.runner.execute_message(message)
        self.telemetry.append(
            event,
            extra={
                "chat_id": chat_id,
                "user_id": message.user_id,
                "message_id": message.message_id,
                "provider_requested": plan.routing.provider,
            },
        )
        reply = self._format_reply(plan.routing.provider, plan.routing.reason, result.content)
        self.client.send_message(chat_id=chat_id, text=reply)
        return True

    def poll_once(self, offset: int | None = None, timeout: int = 1) -> int | None:
        updates = self.client.get_updates(offset=offset, timeout=timeout)
        next_offset = offset
        for update in updates:
            self.handle_update(update)
            update_id = update.get("update_id")
            if update_id is not None:
                next_offset = int(update_id) + 1
        return next_offset

    def poll_once_with_state(self, timeout: int = 1) -> int | None:
        offset = self._read_offset()
        next_offset = self.poll_once(offset=offset, timeout=timeout)
        if next_offset is not None:
            self._write_offset(next_offset)
        return next_offset

    def _read_offset(self) -> int | None:
        path = Path(self.settings.telegram_offset_file)
        if not path.exists():
            return None
        raw = path.read_text(encoding="utf-8").strip()
        return int(raw) if raw else None

    def _write_offset(self, offset: int) -> None:
        path = Path(self.settings.telegram_offset_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(offset), encoding="utf-8")

    def _handle_command(self, text: str) -> str | None:
        command = text.strip().split()[0].lower()
        if command == "/start":
            return "NetCoreX ModelSwitch está no ar. Me manda uma mensagem e eu roteio pelo fluxo do piloto Telegram-first."
        if command == "/help":
            return "Comandos disponíveis: /start, /help. Também podes me mandar uma mensagem normal para testar o roteamento."
        return None

    def _format_reply(self, provider: str, reason: str, content: str) -> str:
        if self.settings.telegram_debug_replies:
            return f"[{provider} | {reason}]\n\n{content}".strip()
        return content.strip()
