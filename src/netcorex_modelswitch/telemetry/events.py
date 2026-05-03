from dataclasses import dataclass

@dataclass
class TokenLedgerEvent:
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float
