"""
Tracks per-request metrics: latency, retries, cost, failures.
"""
import time
import json
from dataclasses import dataclass, field, asdict
from typing import Optional

# Rough token cost (per 1M tokens, USD)
COST = {
    "gemini-2.5-flash": {"in": 0.15, "out": 0.60},
    "gemini-2.5-pro":   {"in": 1.25,  "out": 10.00},
    "llama-3.3-70b-versatile": {"in": 0.0, "out": 0.0},  # Groq free tier
}

@dataclass
class StageMetric:
    stage: str
    model: str
    success: bool
    retries: int = 0
    latency_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    error: Optional[str] = None

    @property
    def cost_usd(self) -> float:
        c = COST.get(self.model, {"in": 0, "out": 0})
        return (self.input_tokens * c["in"] + self.output_tokens * c["out"]) / 1_000_000


@dataclass
class RunMetrics:
    prompt: str
    stages: list[StageMetric] = field(default_factory=list)
    total_retries: int = 0
    success: bool = False
    _start: float = field(default_factory=time.time, repr=False)

    def add(self, m: StageMetric):
        self.stages.append(m)
        self.total_retries += m.retries

    @property
    def total_latency_ms(self) -> int:
        return sum(s.latency_ms for s in self.stages)

    @property
    def total_cost_usd(self) -> float:
        return sum(s.cost_usd for s in self.stages)

    def summary(self) -> dict:
        return {
            "success": self.success,
            "total_latency_ms": self.total_latency_ms,
            "total_retries": self.total_retries,
            "total_cost_usd": round(self.total_cost_usd, 6),
            "stages": [asdict(s) for s in self.stages],
        }


class Timer:
    """Context manager for timing a block."""
    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, *_):
        pass

    @property
    def elapsed_ms(self) -> int:
        return int((time.time() - self._start) * 1000)
