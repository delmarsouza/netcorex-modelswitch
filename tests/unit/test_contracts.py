from netcorex_modelswitch.contracts.models import ChannelMessage


def test_channel_message_fields():
    msg = ChannelMessage(channel="telegram", user_id="u1", text="Olá")
    assert msg.channel == "telegram"
    assert msg.user_id == "u1"
    assert msg.text == "Olá"
