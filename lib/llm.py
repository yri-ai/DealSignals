"""
Thin LLM wrapper for Deal Signal experiments.
Supports Claude, GPT, ZenMux and other providers with unified interface.
"""

import os
import json
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""

    content: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    timestamp: str
    raw_response: Optional[dict] = None


@dataclass
class LLMConfig:
    """Configuration for LLM calls."""

    provider: str  # "anthropic", "openai", "google", "zenmux"
    model: str
    temperature: float = 0.0
    max_tokens: int = 4096
    api_key: Optional[str] = None  # Optional explicit API key


def call_llm(
    prompt: str,
    config: LLMConfig,
    system: Optional[str] = None,
) -> LLMResponse:
    """
    Call an LLM with given prompt and config.

    Returns standardized LLMResponse regardless of provider.
    """
    import time

    start = time.time()

    if config.provider == "anthropic":
        response = _call_anthropic(prompt, config, system)
    elif config.provider == "openai":
        response = _call_openai(prompt, config, system)
    elif config.provider == "zenmux":
        response = _call_zenmux(prompt, config, system)
    else:
        raise ValueError(f"Unknown provider: {config.provider}")

    response.latency_ms = int((time.time() - start) * 1000)
    response.timestamp = datetime.utcnow().isoformat()

    return response


def _call_anthropic(prompt: str, config: LLMConfig, system: Optional[str]) -> LLMResponse:
    """Call Anthropic Claude API."""
    try:
        import anthropic
    except ImportError:
        raise ImportError("pip install anthropic")

    client = anthropic.Anthropic(api_key=config.api_key)

    messages = [{"role": "user", "content": prompt}]

    kwargs = {
        "model": config.model,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "messages": messages,
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)

    return LLMResponse(
        content=response.content[0].text if response.content else "",
        model=config.model,
        input_tokens=response.usage.input_tokens if response.usage else 0,
        output_tokens=response.usage.output_tokens if response.usage else 0,
        latency_ms=0,  # Set by caller
        timestamp="",  # Set by caller
        raw_response=response.model_dump(),
    )


def _call_openai(prompt: str, config: LLMConfig, system: Optional[str]) -> LLMResponse:
    """Call OpenAI API."""
    try:
        import openai
    except ImportError:
        raise ImportError("pip install openai")

    client = openai.OpenAI(api_key=config.api_key)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=config.model,
        messages=messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )

    return LLMResponse(
        content=response.choices[0].message.content or "",
        model=config.model,
        input_tokens=response.usage.prompt_tokens if response.usage else 0,
        output_tokens=response.usage.completion_tokens if response.usage else 0,
        latency_ms=0,
        timestamp="",
        raw_response=response.model_dump(),
    )


def _call_zenmux(prompt: str, config: LLMConfig, system: Optional[str]) -> LLMResponse:
    """Call ZenMux API via OpenAI-compatible endpoint."""
    try:
        import openai
    except ImportError:
        raise ImportError("pip install openai")

    client = openai.OpenAI(api_key=config.api_key, base_url="https://api.zenmux.ai/v1/")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=config.model,
        messages=messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )

    return LLMResponse(
        content=response.choices[0].message.content or "",
        model=config.model,
        input_tokens=response.usage.prompt_tokens if response.usage else 0,
        output_tokens=response.usage.completion_tokens if response.usage else 0,
        latency_ms=0,
        timestamp="",
        raw_response=response.model_dump(),
    )


def save_response(response: LLMResponse, path: str) -> None:
    """Save LLM response to JSON file."""
    with open(path, "w") as f:
        json.dump(asdict(response), f, indent=2)


def load_response(path: str) -> LLMResponse:
    """Load LLM response from JSON file."""
    with open(path) as f:
        data = json.load(f)
    return LLMResponse(**data)


def list_zenmux_models(api_key: str) -> list[dict]:
    """Fetch available models from ZenMux API."""
    try:
        import openai
    except ImportError:
        raise ImportError("pip install openai")

    client = openai.OpenAI(api_key=api_key, base_url="https://api.zenmux.ai/v1/")

    try:
        response = client.models.list()
        return [model.model_dump() for model in response.data]
    except Exception as e:
        raise RuntimeError(f"Failed to fetch ZenMux models: {e}")


def get_zenmux_model_info(api_key: str, model_id: str) -> dict:
    """Get detailed information about a specific ZenMux model."""
    try:
        import openai
    except ImportError:
        raise ImportError("pip install openai")

    client = openai.OpenAI(api_key=api_key, base_url="https://api.zenmux.ai/v1/")

    try:
        response = client.models.retrieve(model_id)
        return response.model_dump()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch model info for {model_id}: {e}")
