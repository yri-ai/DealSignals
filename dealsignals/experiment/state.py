import json
from pathlib import Path

from dealsignals.core.types import RunEvent, EventType


class RunState:
    def __init__(self, events_path: Path):
        self.events_path = Path(events_path)
        self._events: list[RunEvent] = []
        self._load()

    def _load(self) -> None:
        if not self.events_path.exists():
            return

        with open(self.events_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    self._events.append(RunEvent.from_dict(data))

    def append(self, event: RunEvent) -> None:
        self.events_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.events_path, "a") as f:
            f.write(json.dumps(event.to_dict()) + "\n")

        self._events.append(event)

    def get_completed(self) -> set[tuple[str, str]]:
        completed = set()

        for event in self._events:
            key = (event.model, event.question_id)
            if event.event_type == EventType.COMPLETED:
                completed.add(key)
            elif event.event_type == EventType.FAILED:
                completed.discard(key)

        return completed

    def get_failed(self) -> set[tuple[str, str]]:
        failed = set()
        completed = set()

        for event in self._events:
            key = (event.model, event.question_id)
            if event.event_type == EventType.COMPLETED:
                completed.add(key)
                failed.discard(key)
            elif event.event_type == EventType.FAILED:
                if key not in completed:
                    failed.add(key)

        return failed

    def get_pending(
        self,
        models: list[str],
        question_ids: list[str],
    ) -> list[tuple[str, str]]:
        completed = self.get_completed()
        pending = []

        for model in models:
            for question_id in question_ids:
                key = (model, question_id)
                if key not in completed:
                    pending.append(key)

        return pending

    def is_complete(self, model: str, question_id: str) -> bool:
        return (model, question_id) in self.get_completed()

    def summary(self) -> dict:
        completed = self.get_completed()
        failed = self.get_failed()

        models = set()
        questions = set()

        for event in self._events:
            models.add(event.model)
            questions.add(event.question_id)

        return {
            "total_events": len(self._events),
            "completed": len(completed),
            "failed": len(failed),
            "models": sorted(models),
            "questions": sorted(questions),
        }
