from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any


class QuestionType(str, Enum):
    EXTRACTION = "extraction"
    CALCULATION = "calculation"
    COMPARISON = "comparison"
    INFERENCE = "inference"
    SIMULATION = "simulation"
    JUDGMENT = "judgment"


class ContaminationRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FailureMode(str, Enum):
    EXTRACTION_ERROR = "extraction_error"
    CALCULATION_ERROR = "calculation_error"
    REASONING_ERROR = "reasoning_error"
    OMISSION = "omission"
    HALLUCINATION = "hallucination"
    CONTAMINATION = "contamination"
    RELEVANCE_ERROR = "relevance_error"
    CONFIDENCE_ERROR = "confidence_error"


class EventType(str, Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Question:
    id: str
    text: str
    category: str
    question_type: QuestionType
    contamination_risk: ContaminationRisk
    ground_truth: str | None = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "category": self.category,
            "question_type": self.question_type.value,
            "contamination_risk": self.contamination_risk.value,
            "ground_truth": self.ground_truth,
            "metadata": self.metadata,
        }


@dataclass
class ModelInfo:
    id: str
    provider: str
    display_name: str
    context_window: int = 128000
    max_output: int = 8192
    input_price_per_m: float = 0.0
    output_price_per_m: float = 0.0
    capabilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CompletionRequest:
    model: str
    messages: list[dict]
    temperature: float = 0.0
    max_tokens: int = 4096

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CompletionResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    timestamp: str
    cost_usd: float = 0.0
    raw_response: dict = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CompletionResponse":
        return cls(**data)


@dataclass
class RunEvent:
    run_id: str
    layer: str
    model: str
    question_id: str
    event_type: EventType
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    data: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "layer": self.layer,
            "model": self.model,
            "question_id": self.question_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp,
            "data": self.data,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RunEvent":
        data["event_type"] = EventType(data["event_type"])
        return cls(**data)


@dataclass
class EvaluationScore:
    question_id: str
    model: str
    found: bool
    accurate: bool
    complete: float
    cited: int
    relevance: int
    actionable: int
    failure_modes: list[FailureMode] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "model": self.model,
            "found": self.found,
            "accurate": self.accurate,
            "complete": self.complete,
            "cited": self.cited,
            "relevance": self.relevance,
            "actionable": self.actionable,
            "failure_modes": [fm.value for fm in self.failure_modes],
            "notes": self.notes,
        }
