import time
from datetime import datetime

import httpx

from dealsignals.core.types import CompletionRequest, CompletionResponse, ModelInfo
from dealsignals.core.config import get_config
from .base import Provider


ZEN_BASE_URL = "https://opencode.ai/zen/v1"

ZEN_PRICING = {
    "gpt-5.2": {"input": 1.75, "output": 14.00},
    "gpt-5.1": {"input": 1.07, "output": 8.50},
    "gpt-5.1-codex": {"input": 1.07, "output": 8.50},
    "gpt-5.1-codex-max": {"input": 1.25, "output": 10.00},
    "gpt-5.1-codex-mini": {"input": 0.25, "output": 2.00},
    "gpt-5": {"input": 1.07, "output": 8.50},
    "gpt-5-codex": {"input": 1.07, "output": 8.50},
    "gpt-5-nano": {"input": 0.00, "output": 0.00},
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
    "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
    "claude-opus-4-5": {"input": 5.00, "output": 25.00},
    "claude-opus-4-1": {"input": 15.00, "output": 75.00},
    "gemini-3-pro": {"input": 2.00, "output": 12.00},
    "gemini-3-flash": {"input": 0.50, "output": 3.00},
    "glm-4.6": {"input": 0.60, "output": 2.20},
    "glm-4.7-free": {"input": 0.00, "output": 0.00},
    "kimi-k2": {"input": 0.40, "output": 2.50},
    "kimi-k2-thinking": {"input": 0.40, "output": 2.50},
    "qwen3-coder": {"input": 0.45, "output": 1.50},
    "grok-code": {"input": 0.00, "output": 0.00},
    "minimax-m2.1-free": {"input": 0.00, "output": 0.00},
    "big-pickle": {"input": 0.00, "output": 0.00},
}


class ZenMuxProvider(Provider):
    def __init__(self, api_key: str | None = None):
        config = get_config()
        self._api_key = api_key or config.zenmux_api_key
        self._models_cache: list[ModelInfo] | None = None

    @property
    def name(self) -> str:
        return "zen"

    def _get_format(self, model: str) -> str:
        if model.startswith("gpt-"):
            return "openai"
        elif model.startswith("claude-"):
            return "anthropic"
        else:
            return "oa-compat"

    def _get_endpoint(self, model: str) -> str:
        fmt = self._get_format(model)
        if fmt == "openai":
            return f"{ZEN_BASE_URL}/responses"
        elif fmt == "anthropic":
            return f"{ZEN_BASE_URL}/messages"
        else:
            return f"{ZEN_BASE_URL}/chat/completions"

    def _build_request_body(self, request: CompletionRequest) -> dict:
        fmt = self._get_format(request.model)

        if fmt == "openai":
            input_content = self._messages_to_input(request.messages)
            return {"model": request.model, "input": input_content}
        elif fmt == "anthropic":
            system_msg = None
            messages = []
            for msg in request.messages:
                if msg.get("role") == "system":
                    system_msg = msg.get("content", "")
                else:
                    messages.append(msg)
            body = {
                "model": request.model,
                "messages": messages,
                "max_tokens": request.max_tokens or 4096,
            }
            if system_msg:
                body["system"] = system_msg
            return body
        else:
            return {
                "model": request.model,
                "messages": request.messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            }

    def _messages_to_input(self, messages: list[dict]) -> str:
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                parts.append(f"[System]: {content}")
            elif role == "assistant":
                parts.append(f"[Assistant]: {content}")
            else:
                parts.append(content)
        return "\n\n".join(parts)

    def _parse_response(self, data: dict, model: str) -> tuple[str, int, int]:
        fmt = self._get_format(model)

        if fmt == "openai":
            content = ""
            for output in data.get("output", []):
                if output.get("type") == "message":
                    for c in output.get("content", []):
                        if c.get("type") == "output_text":
                            content += c.get("text", "")
            usage = data.get("usage", {})
            return content, usage.get("input_tokens", 0), usage.get("output_tokens", 0)
        elif fmt == "anthropic":
            content = ""
            for c in data.get("content", []):
                if c.get("type") == "text":
                    content += c.get("text", "")
            usage = data.get("usage", {})
            return content, usage.get("input_tokens", 0), usage.get("output_tokens", 0)
        else:
            choices = data.get("choices", [])
            content = choices[0].get("message", {}).get("content", "") if choices else ""
            usage = data.get("usage", {})
            return content, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        if not self._api_key:
            raise ValueError("ZENMUX_API_KEY not set")

        endpoint = self._get_endpoint(request.model)
        body = self._build_request_body(request)
        fmt = self._get_format(request.model)

        headers = {"Content-Type": "application/json"}
        if fmt == "anthropic":
            headers["x-api-key"] = self._api_key
            headers["anthropic-version"] = "2023-06-01"
        else:
            headers["Authorization"] = f"Bearer {self._api_key}"

        start_time = time.time()

        with httpx.Client(timeout=120) as client:
            response = client.post(endpoint, json=body, headers=headers)
            response.raise_for_status()
            data = response.json()

        latency_ms = int((time.time() - start_time) * 1000)

        content, input_tokens, output_tokens = self._parse_response(data, request.model)

        pricing = ZEN_PRICING.get(request.model, {"input": 0, "output": 0})
        cost_usd = (input_tokens / 1_000_000) * pricing["input"] + (
            output_tokens / 1_000_000
        ) * pricing["output"]

        return CompletionResponse(
            content=content,
            model=request.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            timestamp=datetime.utcnow().isoformat(),
            cost_usd=cost_usd,
            raw_response=data,
        )

    def list_models(self) -> list[ModelInfo]:
        if self._models_cache is not None:
            return self._models_cache

        try:
            with httpx.Client(timeout=30) as client:
                headers = {"Authorization": f"Bearer {self._api_key}"}
                response = client.get(f"{ZEN_BASE_URL}/models", headers=headers)
                response.raise_for_status()
                data = response.json()

            models = []
            for model in data.get("data", []):
                model_id = model.get("id", "")
                pricing = ZEN_PRICING.get(model_id, {"input": 0, "output": 0})
                models.append(
                    ModelInfo(
                        id=model_id,
                        provider="zen",
                        display_name=model_id,
                        input_price_per_m=pricing["input"],
                        output_price_per_m=pricing["output"],
                    )
                )
            self._models_cache = models
            return models
        except Exception:
            return [
                ModelInfo(id=model_id, provider="zen", display_name=model_id)
                for model_id in ZEN_PRICING.keys()
            ]

    def get_model(self, model_id: str) -> ModelInfo | None:
        for model in self.list_models():
            if model.id == model_id:
                return model
        return None

    def supports_model(self, model_id: str) -> bool:
        return model_id in ZEN_PRICING or model_id.startswith(
            (
                "gpt-",
                "claude-",
                "gemini-",
                "glm-",
                "kimi-",
                "qwen",
                "grok-",
                "minimax-",
                "big-pickle",
            )
        )
