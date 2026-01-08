from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class LayerConfig:
    id: str
    name: str
    description: str
    documents: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    system_prompt_path: Path | None = None
    user_prompt_path: Path | None = None
    models: list[str] = field(default_factory=list)
    question_filter: dict = field(default_factory=dict)
    evaluation: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict, base_path: Path) -> "LayerConfig":
        prompts = data.get("prompts", {})
        system_path = prompts.get("system")
        user_path = prompts.get("user")

        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            documents=data.get("documents", []),
            tools=data.get("tools", []),
            system_prompt_path=base_path / system_path if system_path else None,
            user_prompt_path=base_path / user_path if user_path else None,
            models=data.get("models", []),
            question_filter=data.get("question_filter", {}),
            evaluation=data.get("evaluation", {}),
        )


@dataclass
class ExperimentDefinition:
    case_study: str
    layer: LayerConfig
    ground_truth_path: Path
    output_dir: Path
    base_path: Path

    @classmethod
    def from_yaml(cls, config_path: Path) -> "ExperimentDefinition":
        config_path = Path(config_path)
        base_path = config_path.parent

        with open(config_path) as f:
            data = yaml.safe_load(f)

        layer = LayerConfig.from_dict(data["layer"], base_path)

        case_study = data.get("case_study", base_path.parent.parent.name)

        ground_truth = data.get("ground_truth", "../ground-truth/questions.yaml")
        ground_truth_path = (base_path / ground_truth).resolve()

        output_dir = data.get("output_dir", "results")
        output_path = (base_path / output_dir).resolve()

        return cls(
            case_study=case_study,
            layer=layer,
            ground_truth_path=ground_truth_path,
            output_dir=output_path,
            base_path=base_path,
        )

    def load_system_prompt(self) -> str | None:
        if self.layer.system_prompt_path and self.layer.system_prompt_path.exists():
            return self.layer.system_prompt_path.read_text()
        return None

    def load_user_prompt(self) -> str | None:
        if self.layer.user_prompt_path and self.layer.user_prompt_path.exists():
            return self.layer.user_prompt_path.read_text()
        return None
