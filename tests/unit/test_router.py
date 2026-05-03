from netcorex_modelswitch.contracts.models import ChannelMessage
from netcorex_modelswitch.router.engine import RouterEngine


def test_router_prefers_local_for_short_messages():
    engine = RouterEngine()
    decision = engine.route(ChannelMessage(channel="telegram", user_id="u1", text="Oi"))
    assert decision.provider == "local"


def test_router_escalates_longer_messages():
    engine = RouterEngine()
    decision = engine.route(ChannelMessage(channel="telegram", user_id="u1", text="Preciso de uma arquitetura completa para um roteador híbrido multi-bot."))
    assert decision.provider == "cloud"
