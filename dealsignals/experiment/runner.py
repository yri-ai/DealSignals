import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

from dealsignals.core.types import (
    Question,
    CompletionResponse,
    RunEvent,
    EventType,
)
from dealsignals.providers import ModelRegistry, get_registry
from dealsignals.questions import QuestionBank
from .definition import ExperimentDefinition
from .state import RunState


@dataclass
class RunSummary:
    run_id: str
    layer: str
    started_at: str
    completed_at: str
    total_questions: int
    total_models: int
    completed: int
    failed: int
    skipped: int
    total_cost_usd: float
    total_tokens: int


class ExperimentRunner:
    def __init__(
        self,
        definition: ExperimentDefinition,
        registry: ModelRegistry | None = None,
    ):
        self.definition = definition
        self.registry = registry or get_registry()

        self.output_dir = definition.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.state = RunState(self.output_dir / "events.jsonl")

        self.questions = QuestionBank.from_yaml(definition.ground_truth_path)

        self._system_prompt = definition.load_system_prompt()
        self._user_prompt_template = definition.load_user_prompt()

    def run(
        self,
        models: list[str] | None = None,
        questions: list[str] | None = None,
        dry_run: bool = False,
        on_progress: Callable[[str, str, str], None] | None = None,
    ) -> RunSummary:
        run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        started_at = datetime.utcnow().isoformat()

        target_models = models or self.definition.layer.models
        if not target_models:
            target_models = ["claude", "gpt4"]

        if questions:
            target_questions = self.questions.filter(ids=questions)
        else:
            filter_kwargs = self.definition.layer.question_filter
            if filter_kwargs:
                target_questions = self.questions.filter(**filter_kwargs)
            else:
                target_questions = list(self.questions)

        question_ids = [q.id for q in target_questions]
        documents = self.definition.layer.documents

        pending = self.state.get_pending(target_models, question_ids, documents)

        if dry_run:
            print(f"Dry run: {len(pending)} tasks pending")
            for model, doc, qid in pending:
                doc_info = f"[{Path(doc).name}] " if doc else ""
                print(f"  {model} x {doc_info}{qid}")
            return RunSummary(
                run_id=run_id,
                layer=self.definition.layer.id,
                started_at=started_at,
                completed_at=started_at,
                total_questions=len(target_questions),
                total_models=len(target_models),
                completed=0,
                failed=0,
                skipped=len(pending),
                total_cost_usd=0,
                total_tokens=0,
            )

        completed = 0
        failed = 0
        total_cost = 0.0
        total_tokens = 0

        for model, document, question_id in pending:
            question = self.questions.get(question_id)
            if not question:
                continue

            if on_progress:
                on_progress(model, question_id, "started")

            self.state.append(
                RunEvent(
                    run_id=run_id,
                    layer=self.definition.layer.id,
                    model=model,
                    question_id=question_id,
                    document=document,
                    event_type=EventType.STARTED,
                )
            )

            try:
                document_content = None
                if document:
                    doc_path = Path(document)
                    if doc_path.exists():
                        document_content = doc_path.read_text()
                    else:
                        raise FileNotFoundError(f"Document not found: {document}")

                response = self._execute(model, question, document_content)

                self._save_response(run_id, model, question_id, response, document)

                self.state.append(
                    RunEvent(
                        run_id=run_id,
                        layer=self.definition.layer.id,
                        model=model,
                        question_id=question_id,
                        document=document,
                        event_type=EventType.COMPLETED,
                        data={
                            "latency_ms": response.latency_ms,
                            "input_tokens": response.input_tokens,
                            "output_tokens": response.output_tokens,
                            "cost_usd": response.cost_usd,
                        },
                    )
                )

                completed += 1
                total_cost += response.cost_usd
                total_tokens += response.total_tokens

                if on_progress:
                    on_progress(model, question_id, "completed")

            except Exception as e:
                self.state.append(
                    RunEvent(
                        run_id=run_id,
                        layer=self.definition.layer.id,
                        model=model,
                        question_id=question_id,
                        document=document,
                        event_type=EventType.FAILED,
                        data={"error": str(e)},
                    )
                )

                failed += 1

                if on_progress:
                    on_progress(model, question_id, f"failed: {e}")

        completed_at = datetime.utcnow().isoformat()

        return RunSummary(
            run_id=run_id,
            layer=self.definition.layer.id,
            started_at=started_at,
            completed_at=completed_at,
            total_questions=len(target_questions),
            total_models=len(target_models),
            completed=completed,
            failed=failed,
            skipped=0,
            total_cost_usd=total_cost,
            total_tokens=total_tokens,
        )

    def _execute(
        self,
        model: str,
        question: Question,
        document_content: str | None = None,
    ) -> CompletionResponse:
        messages = []

        if self._system_prompt:
            messages.append({"role": "system", "content": self._system_prompt})

        user_content = self._build_user_prompt(question, document_content)
        messages.append({"role": "user", "content": user_content})

        return self.registry.complete(
            model=model,
            messages=messages,
            temperature=0.0,
            max_tokens=8192,
        )

    def _build_user_prompt(
        self,
        question: Question,
        document_content: str | None = None,
    ) -> str:
        text = question.text
        if self._user_prompt_template:
            text = self._user_prompt_template.replace("{{question}}", question.text)

        if document_content and "{{document}}" in text:
            text = text.replace("{{document}}", document_content)

        return text

    def _save_response(
        self,
        run_id: str,
        model: str,
        question_id: str,
        response: CompletionResponse,
        document: str | None = None,
    ) -> None:
        responses_dir = self.output_dir / "responses" / run_id
        responses_dir.mkdir(parents=True, exist_ok=True)

        safe_model = model.replace("/", "_")
        safe_doc = f"_{Path(document).stem}" if document else ""

        json_path = responses_dir / f"{safe_model}{safe_doc}_{question_id}.json"
        with open(json_path, "w") as f:
            json.dump(response.to_dict(), f, indent=2)

        md_path = responses_dir / f"{safe_model}{safe_doc}_{question_id}.md"
        with open(md_path, "w") as f:
            f.write(f"# {model} - {question_id}\n\n")
            if document:
                f.write(f"**Document:** {Path(document).name}\n")
            f.write(f"**Timestamp:** {response.timestamp}\n")
            f.write(f"**Latency:** {response.latency_ms}ms\n")
            f.write(f"**Tokens:** {response.input_tokens} in, {response.output_tokens} out\n")
            f.write(f"**Cost:** ${response.cost_usd:.6f}\n\n")
            f.write("---\n\n")
            f.write(response.content)

    def status(self) -> dict:
        return self.state.summary()
