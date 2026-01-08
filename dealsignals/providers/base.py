from abc import ABC, abstractmethod

from dealsignals.core.types import CompletionRequest, CompletionResponse, ModelInfo


class Provider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def complete(self, request: CompletionRequest) -> CompletionResponse:
        pass

    @abstractmethod
    def list_models(self) -> list[ModelInfo]:
        pass

    @abstractmethod
    def get_model(self, model_id: str) -> ModelInfo | None:
        pass

    @abstractmethod
    def supports_model(self, model_id: str) -> bool:
        pass
