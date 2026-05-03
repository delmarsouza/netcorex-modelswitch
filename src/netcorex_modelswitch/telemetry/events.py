from dataclasses import dataclass


@dataclass
class TokenLedgerEvent:
    provider: str
    model: str
    route_reason: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    latency_ms: int
    fallback_triggered: bool = False
