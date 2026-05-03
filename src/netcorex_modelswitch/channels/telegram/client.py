from __future__ import annotations

import requests


class TelegramClient:
    def __init__(self, bot_token: str) -> None:
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def get_updates(self, offset: int | None = None, timeout: int = 30) -> list[dict]:
        response = requests.get(
            f"{self.base_url}/getUpdates",
            params={"offset": offset, "timeout": timeout},
            timeout=timeout + 10,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("result", [])

    def send_message(self, chat_id: str, text: str) -> dict:
        response = requests.post(
            f"{self.base_url}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
