import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    zenmux_api_key: str | None = None
    openrouter_api_key: str | None = None
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None

    zenmux_base_url: str = "https://opencode.ai/zen/v1/"
    openrouter_base_url: str = "https://openrouter.ai/api/v1/"

    experiments_dir: Path = Path("experiments")
    results_dir: Path = Path("results")

    default_temperature: float = 0.0
    default_max_tokens: int = 8192

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            zenmux_api_key=os.getenv("ZENMUX_API_KEY"),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )


_config: Config | None = None


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


def set_config(config: Config) -> None:
    global _config
    _config = config
