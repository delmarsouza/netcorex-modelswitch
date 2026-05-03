from netcorex_modelswitch.contracts.models import ChannelMessage, RoutingDecision

class RouterEngine:
    def route(self, message: ChannelMessage) -> RoutingDecision:
        text = message.text.lower().strip()
        if len(text) < 40:
            return RoutingDecision(
                provider="local",
                model="local-default",
                reason="short_low_complexity_message",
            )
        return RoutingDecision(
            provider="cloud",
            model="premium-default",
            reason="default_escalation_rule",
        )
