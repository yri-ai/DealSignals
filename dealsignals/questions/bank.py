from pathlib import Path

from dealsignals.core.types import Question, QuestionType, ContaminationRisk
from .loader import load_questions


class QuestionBank:
    def __init__(self, questions: list[Question]):
        self._questions = questions
        self._by_id = {q.id: q for q in questions}

    @classmethod
    def from_yaml(cls, path: Path | str) -> "QuestionBank":
        path = Path(path)
        questions = load_questions(path)
        return cls(questions)

    def __len__(self) -> int:
        return len(self._questions)

    def __iter__(self):
        return iter(self._questions)

    def get(self, question_id: str) -> Question | None:
        return self._by_id.get(question_id)

    def filter(
        self,
        category: str | None = None,
        question_type: QuestionType | str | None = None,
        contamination_risk: ContaminationRisk | str | None = None,
        ids: list[str] | None = None,
    ) -> list[Question]:
        result = self._questions

        if category:
            result = [q for q in result if q.category == category]

        if question_type:
            if isinstance(question_type, str):
                question_type = QuestionType(question_type)
            result = [q for q in result if q.question_type == question_type]

        if contamination_risk:
            if isinstance(contamination_risk, str):
                contamination_risk = ContaminationRisk(contamination_risk)
            result = [q for q in result if q.contamination_risk == contamination_risk]

        if ids:
            id_set = set(ids)
            result = [q for q in result if q.id in id_set]

        return result

    def categories(self) -> list[str]:
        return sorted(set(q.category for q in self._questions))

    def ids(self) -> list[str]:
        return [q.id for q in self._questions]
