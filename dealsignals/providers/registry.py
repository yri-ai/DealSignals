from dealsignals.core.types import CompletionRequest, CompletionResponse, ModelInfo
from .base import Provider


MODEL_ALIASES = {
    "claude": "anthropic/claude-opus-4.5",
    "gpt4": "openai/gpt-5.2",
    "gpt5": "openai/gpt-5.2",
    "gemini": "google/gemini-3-flash-preview",
    "gemini-pro": "google/gemini-3-pro-preview",
    "gemini-flash": "google/gemini-3-flash-preview",
    "deepseek": "deepseek/deepseek-reasoner",
    "grok": "x-ai/grok-4.1-fast",
    "mistral": "mistralai/mistral-large-2512",
    "glm": "z-ai/glm-4.7",
    "auto": "zenmux/auto",
}


class ModelRegistry:
    def __init__(self):
        self._providers: dict[str, Provider] = {}
        self._aliases: dict[str, str] = MODEL_ALIASES.copy()
        self._provider_priority: list[str] = ["zenmux", "openrouter", "direct"]

    def register_provider(self, provider: Provider) -> None:
        self._providers[provider.name] = provider

    def register_alias(self, alias: str, model_id: str) -> None:
        self._aliases[alias] = model_id

    def resolve_model(self, model: str) -> str:
        return self._aliases.get(model, model)

    def get_provider_for_model(self, model_id: str) -> Provider | None:
        resolved = self.resolve_model(model_id)

        for provider_name in self._provider_priority:
            if provider_name in self._providers:
                provider = self._providers[provider_name]
                if provider.supports_model(resolved):
                    return provider

        return None

    def complete(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.0,
        max_tokens: int = 4096,
    ) -> CompletionResponse:
        resolved = self.resolve_model(model)
        provider = self.get_provider_for_model(resolved)

        if provider is None:
            raise ValueError(f"No provider found for model: {model} (resolved: {resolved})")

        request = CompletionRequest(
            model=resolved,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return provider.complete(request)

    def list_all_models(self) -> list[ModelInfo]:
        models = []
        seen_ids = set()

        for provider in self._providers.values():
            for model in provider.list_models():
                if model.id not in seen_ids:
                    models.append(model)
                    seen_ids.add(model.id)

        return sorted(models, key=lambda m: m.id)

    def list_aliases(self) -> dict[str, str]:
        return self._aliases.copy()


_registry: ModelRegistry | None = None


def get_registry() -> ModelRegistry:
    global _registry
    if _registry is None:
        _registry = ModelRegistry()

        from .zenmux import ZenMuxProvider

        try:
            _registry.register_provider(ZenMuxProvider())
        except ValueError:
            pass

    return _registry
