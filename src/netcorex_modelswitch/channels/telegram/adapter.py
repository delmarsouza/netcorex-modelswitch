from netcorex_modelswitch.contracts.models import Channel, ChannelMessage


class TelegramAdapter:
    def normalize(self, user_id: str, text: str, message_id: str | None = None) -> ChannelMessage:
        return ChannelMessage(
            channel=Channel.TELEGRAM,
            user_id=user_id,
            text=text,
            message_id=message_id,
        )
