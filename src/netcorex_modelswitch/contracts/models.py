from dataclasses import dataclass
from typing import Optional

@dataclass
class ChannelMessage:
    channel: str
    user_id: str
    text: str
    thread_id: Optional[str] = None

@dataclass
class RoutingDecision:
    provider: str
    model: str
    reason: str
