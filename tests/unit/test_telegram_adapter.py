from netcorex_modelswitch.channels.telegram.adapter import TelegramAdapter


def test_telegram_adapter_from_update_extracts_message():
    adapter = TelegramAdapter()
    update = {
        "update_id": 1,
        "message": {
            "message_id": 10,
            "text": "Oi Tigun",
            "chat": {"id": 1234},
            "from": {"id": 999},
        },
    }

    message = adapter.from_update(update)

    assert message is not None
    assert message.user_id == "999"
    assert message.text == "Oi Tigun"
    assert message.metadata["chat_id"] == "1234"
