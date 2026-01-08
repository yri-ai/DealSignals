import time
from datetime import datetime

from dealsignals.core.types import CompletionRequest, CompletionResponse, ModelInfo
from dealsignals.core.config import get_config
from .base import Provider


ZENMUX_PRICING = {
    "zenmux/auto": {"input": 0.0, "output": 0.0},
    "openai/gpt-5.2-pro": {"input": 21.00, "output": 168.00},
    "openai/gpt-5.2": {"input": 1.75, "output": 14.00},
    "openai/gpt-5.2-chat": {"input": 1.75, "output": 14.00},
    "openai/gpt-5.1": {"input": 1.25, "output": 10.00},
    "openai/gpt-5.1-chat": {"input": 1.25, "output": 10.00},
    "openai/gpt-5.1-codex": {"input": 1.25, "output": 10.00},
    "anthropic/claude-opus-4.5": {"input": 5.00, "output": 25.00},
    "google/gemini-3-pro-preview": {"input": 3.00, "output": 15.00},
    "google/gemini-3-flash-preview": {"input": 0.50, "output": 3.00},
    "google/gemini-3-flash-preview-free": {"input": 0.00, "output": 0.00},
    "deepseek/deepseek-v3.2": {"input": 0.28, "output": 0.43},
    "deepseek/deepseek-chat": {"input": 0.28, "output": 0.42},
    "deepseek/deepseek-reasoner": {"input": 0.28, "output": 0.42},
    "x-ai/grok-4.1-fast": {"input": 0.30, "output": 0.75},
    "xiaomi/mimo-v2-flash": {"input": 0.00, "output": 0.00},
    "xiaomi/mimo-v2-flash-free": {"input": 0.00, "output": 0.00},
    "mistralai/mistral-large-2512": {"input": 0.50, "output": 1.50},
    "z-ai/glm-4.7": {"input": 0.43, "output": 1.71},
    "minimax/minimax-m2.1": {"input": 0.30, "output": 1.20},
}


class ZenMuxProvider(Provider):
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        config = get_config()
        self._api_key = api_key or config.zenmux_api_key
        self._base_url = base_url or config.zenmux_base_url
        self._client = None
        self._models_cache: list[ModelInfo] | None = None

    @property
    def name(self) -> str:
        return "zenmux"

    def _get_client(self):
        if self._client is None:
            try:
                import openai
            except ImportError:
                raise ImportError("pip install openai")

            if not self._api_key:
                raise ValueError("ZENMUX_API_KEY not set")

            self._client = openai.OpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
            )
        return self._client

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        client = self._get_client()

        start_time = time.time()

        response = client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        latency_ms = int((time.time() - start_time) * 1000)

        input_tokens = response.usage.prompt_tokens if response.usage else 0
        output_tokens = response.usage.completion_tokens if response.usage else 0

        pricing = ZENMUX_PRICING.get(request.model, {"input": 0, "output": 0})
        cost_usd = (input_tokens / 1_000_000) * pricing["input"] + (
            output_tokens / 1_000_000
        ) * pricing["output"]

        return CompletionResponse(
            content=response.choices[0].message.content or "",
            model=request.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            timestamp=datetime.utcnow().isoformat(),
            cost_usd=cost_usd,
            raw_response=response.model_dump(),
        )

    def list_models(self) -> list[ModelInfo]:
        if self._models_cache is not None:
            return self._models_cache

        client = self._get_client()

        try:
            response = client.models.list()
            models = []
            for model in response.data:
                model_id = model.id
                pricing = ZENMUX_PRICING.get(model_id, {"input": 0, "output": 0})
                models.append(
                    ModelInfo(
                        id=model_id,
                        provider="zenmux",
                        display_name=model_id.split("/")[-1] if "/" in model_id else model_id,
                        input_price_per_m=pricing["input"],
                        output_price_per_m=pricing["output"],
                    )
                )
            self._models_cache = models
            return models
        except Exception:
            return [
                ModelInfo(id=model_id, provider="zenmux", display_name=model_id.split("/")[-1])
                for model_id in ZENMUX_PRICING.keys()
            ]

    def get_model(self, model_id: str) -> ModelInfo | None:
        for model in self.list_models():
            if model.id == model_id:
                return model
        return None

    def supports_model(self, model_id: str) -> bool:
        return model_id in ZENMUX_PRICING or model_id.startswith(
            (
                "openai/",
                "anthropic/",
                "google/",
                "deepseek/",
                "x-ai/",
                "xiaomi/",
                "mistralai/",
                "z-ai/",
                "minimax/",
                "zenmux/",
            )
        )
