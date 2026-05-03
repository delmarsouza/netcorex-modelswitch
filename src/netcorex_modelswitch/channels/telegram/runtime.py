from __future__ import annotations

from netcorex_modelswitch.channels.telegram.adapter import TelegramAdapter
from netcorex_modelswitch.channels.telegram.client import TelegramClient
from netcorex_modelswitch.config.settings import Settings
from netcorex_modelswitch.execution.runner import ExecutionRunner


class TelegramRuntime:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        if not self.settings.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required for Telegram runtime")
        self.adapter = TelegramAdapter()
        self.client = TelegramClient(self.settings.telegram_bot_token)
        self.runner = ExecutionRunner(self.settings)

    def handle_update(self, update: dict) -> bool:
        message = self.adapter.from_update(update)
        if not message:
            return False

        chat_id = message.metadata.get("chat_id")
        if not chat_id:
            return False

        plan, result = self.runner.execute_message(message)
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

    @staticmethod
    def _format_reply(provider: str, reason: str, content: str) -> str:
        return f"[{provider} | {reason}]\n\n{content}".strip()
