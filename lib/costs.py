"""
Cost tracking for Deal Signal experiments.
Tracks tokens, API costs, and latency per methodology requirements.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import json


# Pricing per 1M tokens (as of Dec 2024, update as needed)
PRICING = {
    # Anthropic
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    # OpenAI
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    # Google
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    # ZenMux Models (94 total models)
    # Auto Router
    "zenmux/auto": {"input": 0.0, "output": 0.0},  # Dynamic pricing
    # OpenAI Models via ZenMux
    "openai/gpt-5.2-pro": {"input": 21.00, "output": 168.00},
    "openai/gpt-5.2": {"input": 1.75, "output": 14.00},
    "openai/gpt-5.2-chat": {"input": 1.75, "output": 14.00},
    "openai/gpt-5.1": {"input": 1.25, "output": 10.00},
    "openai/gpt-5.1-chat": {"input": 1.25, "output": 10.00},
    "openai/gpt-5.1-codex": {"input": 1.25, "output": 10.00},
    # Anthropic Models via ZenMux
    "anthropic/claude-opus-4.5": {"input": 5.00, "output": 25.00},
    # Google Models via ZenMux
    "google/gemini-3-pro-preview": {"input": 3.00, "output": 15.00},  # Mid-range
    "google/gemini-3-flash-preview": {"input": 0.50, "output": 3.00},
    "google/gemini-3-flash-preview-free": {"input": 0.00, "output": 0.00},
    "google/gemini-3-pro-image-preview": {"input": 3.00, "output": 15.00},
    # Z.AI Models via ZenMux
    "z-ai/glm-4.7": {"input": 0.43, "output": 1.71},  # Mid-range average
    "z-ai/glm-4.6v": {"input": 0.21, "output": 0.64},  # Mid-range average
    "z-ai/glm-4.6v-flash": {"input": 0.03, "output": 0.32},  # Low-end
    "z-ai/glm-4.6v-flash-free": {"input": 0.00, "output": 0.00},
    # DeepSeek Models via ZenMux
    "deepseek/deepseek-v3.2": {"input": 0.28, "output": 0.43},
    "deepseek/deepseek-chat": {"input": 0.28, "output": 0.42},
    "deepseek/deepseek-reasoner": {"input": 0.28, "output": 0.42},
    # xAI Models via ZenMux
    "x-ai/grok-4.1-fast": {"input": 0.30, "output": 0.75},  # Mid-range average
    "x-ai/grok-4.1-fast-non-reasoning": {"input": 0.30, "output": 0.75},
    # Xiaomi Models via ZenMux
    "xiaomi/mimo-v2-flash": {"input": 0.00, "output": 0.00},  # Limited free
    "xiaomi/mimo-v2-flash-free": {"input": 0.00, "output": 0.00},  # Free
    # Mistral Models via ZenMux
    "mistralai/mistral-large-2512": {"input": 0.50, "output": 1.50},
    # MiniMax Models via ZenMux
    "minimax/minimax-m2.1": {"input": 0.30, "output": 1.20},
    # VolcanoEngine Models via ZenMux
    "volcengine/doubao-seed-1.8": {"input": 0.23, "output": 1.85},  # Mid-range average
    # inclusionAI Models via ZenMux
    "inclusionai/llada2.0-flash-cap": {"input": 0.28, "output": 2.85},
}


@dataclass
class CostEntry:
    """Cost tracking for a single LLM call."""

    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    input_cost: float  # USD
    output_cost: float  # USD
    total_cost: float  # USD
    latency_ms: int
    timestamp: str


@dataclass
class RunCosts:
    """Aggregated costs for an experiment run."""

    run_id: str
    entries: list[CostEntry]

    # Totals
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int
    total_cost: float
    total_latency_ms: int

    # Averages
    avg_latency_ms: float
    cost_per_question: float

    # Metadata
    model: str
    started_at: str
    completed_at: str


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    latency_ms: int = 0,
) -> CostEntry:
    """Calculate cost for a single LLM call."""
    pricing = PRICING.get(model, {"input": 0, "output": 0})

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return CostEntry(
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=input_tokens + output_tokens,
        input_cost=input_cost,
        output_cost=output_cost,
        total_cost=input_cost + output_cost,
        latency_ms=latency_ms,
        timestamp=datetime.utcnow().isoformat(),
    )


def aggregate_costs(entries: list[CostEntry], run_id: str) -> RunCosts:
    """Aggregate cost entries into run-level totals."""
    if not entries:
        raise ValueError("No cost entries to aggregate")

    total_input = sum(e.input_tokens for e in entries)
    total_output = sum(e.output_tokens for e in entries)
    total_cost = sum(e.total_cost for e in entries)
    total_latency = sum(e.latency_ms for e in entries)

    return RunCosts(
        run_id=run_id,
        entries=entries,
        total_input_tokens=total_input,
        total_output_tokens=total_output,
        total_tokens=total_input + total_output,
        total_cost=total_cost,
        total_latency_ms=total_latency,
        avg_latency_ms=total_latency / len(entries),
        cost_per_question=total_cost / len(entries),
        model=entries[0].model,
        started_at=entries[0].timestamp,
        completed_at=entries[-1].timestamp,
    )


def save_costs(costs: RunCosts, path: str) -> None:
    """Save cost data to JSON."""
    data = {
        "run_id": costs.run_id,
        "model": costs.model,
        "totals": {
            "input_tokens": costs.total_input_tokens,
            "output_tokens": costs.total_output_tokens,
            "total_tokens": costs.total_tokens,
            "total_cost_usd": round(costs.total_cost, 4),
            "total_latency_ms": costs.total_latency_ms,
        },
        "averages": {
            "latency_ms": round(costs.avg_latency_ms, 2),
            "cost_per_question_usd": round(costs.cost_per_question, 6),
        },
        "timing": {
            "started_at": costs.started_at,
            "completed_at": costs.completed_at,
        },
        "entries": [asdict(e) for e in costs.entries],
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def format_cost_summary(costs: RunCosts) -> str:
    """Format costs as human-readable summary."""
    return f"""
## Cost Summary: {costs.run_id}

| Metric | Value |
|--------|-------|
| Model | {costs.model} |
| Total Tokens | {costs.total_tokens:,} |
| Input Tokens | {costs.total_input_tokens:,} |
| Output Tokens | {costs.total_output_tokens:,} |
| Total Cost | ${costs.total_cost:.4f} |
| Cost/Question | ${costs.cost_per_question:.6f} |
| Avg Latency | {costs.avg_latency_ms:.0f}ms |
| Total Time | {costs.total_latency_ms / 1000:.1f}s |
""".strip()


def update_zenmux_pricing(api_key: str) -> None:
    """Update PRICING dict with latest ZenMux models and pricing."""
    try:
        from .llm import list_zenmux_models

        models = list_zenmux_models(api_key)

        for model in models:
            model_id = model.get("id", "")
            if model_id and model_id not in PRICING:
                # Start with 0 pricing - will be updated if we get pricing info
                PRICING[model_id] = {"input": 0.0, "output": 0.0}

    except ImportError:
        print("Warning: Cannot update ZenMux pricing - openai library not installed")
    except Exception as e:
        print(f"Warning: Failed to update ZenMux pricing: {e}")


def get_cost_effective_models(max_cost_per_m: float = 2.0) -> list[str]:
    """Get models that are cost-effective (under specified threshold)."""
    cost_effective = []

    for model_id, pricing in PRICING.items():
        avg_cost = (pricing["input"] + pricing["output"]) / 2
        if avg_cost <= max_cost_per_m and avg_cost > 0:
            cost_effective.append(model_id)

    return sorted(cost_effective, key=lambda x: PRICING[x]["input"])


def get_free_models() -> list[str]:
    """Get all free models."""
    free_models = []

    for model_id, pricing in PRICING.items():
        if pricing["input"] == 0.0 and pricing["output"] == 0.0:
            free_models.append(model_id)

    return free_models
