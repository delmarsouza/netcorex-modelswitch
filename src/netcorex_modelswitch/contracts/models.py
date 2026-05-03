from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class Complexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Channel(str, Enum):
    TELEGRAM = "telegram"
    SLACK = "slack"
    WEB = "web"
    API = "api"


@dataclass
class Attachment:
    kind: str
    name: Optional[str] = None
    mime_type: Optional[str] = None
    url: Optional[str] = None


@dataclass
class ChannelMessage:
    channel: Channel
    user_id: str
    text: str
    message_id: Optional[str] = None
    thread_id: Optional[str] = None
    attachments: list[Attachment] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class IntentAssessment:
    domain: str
    complexity: Complexity
    risk: RiskLevel
    requires_multimodal: bool = False
    requires_specialist: bool = False


@dataclass
class SpecialistAssignment:
    specialist: str
    reason: str


@dataclass
class RoutingDecision:
    provider: str
    model: str
    reason: str
    fallback_chain: list[str] = field(default_factory=list)


@dataclass
class ExecutionPlan:
    coordinator: str
    specialists: list[SpecialistAssignment]
    routing: RoutingDecision
    assessment: IntentAssessment


@dataclass
class ModelExecutionResult:
    content: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0
    estimated_cost: float = 0.0
