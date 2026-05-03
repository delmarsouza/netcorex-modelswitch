from __future__ import annotations

from netcorex_modelswitch.contracts.models import Channel, ChannelMessage


class TelegramAdapter:
    def normalize(self, user_id: str, text: str, message_id: str | None = None, chat_id: str | None = None) -> ChannelMessage:
        return ChannelMessage(
            channel=Channel.TELEGRAM,
            user_id=user_id,
            text=text,
            message_id=message_id,
            metadata={"chat_id": chat_id} if chat_id else {},
        )

    def from_update(self, update: dict) -> ChannelMessage | None:
        message = update.get("message") or update.get("edited_message")
        if not message:
            return None

        text = message.get("text")
        if not text:
            return None

        chat = message.get("chat", {})
        user = message.get("from", {})
        return self.normalize(
            user_id=str(user.get("id", "unknown")),
            text=text,
            message_id=str(message.get("message_id")) if message.get("message_id") is not None else None,
            chat_id=str(chat.get("id")) if chat.get("id") is not None else None,
        )
