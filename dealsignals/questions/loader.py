from pathlib import Path

import yaml

from dealsignals.core.types import Question, QuestionType, ContaminationRisk


def load_questions(path: Path) -> list[Question]:
    with open(path) as f:
        data = yaml.safe_load(f)

    questions = []

    if "categories" in data:
        for category_name, category_data in data["categories"].items():
            for q_data in category_data.get("questions", []):
                questions.append(_parse_question(q_data, category_name))

    elif "questions" in data:
        for q_data in data["questions"]:
            questions.append(_parse_question(q_data, q_data.get("category", "unknown")))

    return questions


def _parse_question(data: dict, category: str) -> Question:
    q_type = data.get("type", "extraction")
    try:
        question_type = QuestionType(q_type)
    except ValueError:
        question_type = QuestionType.EXTRACTION

    c_risk = data.get("contamination_risk", "medium")
    try:
        contamination_risk = ContaminationRisk(c_risk)
    except ValueError:
        contamination_risk = ContaminationRisk.MEDIUM

    return Question(
        id=data["id"],
        text=data["text"],
        category=category,
        question_type=question_type,
        contamination_risk=contamination_risk,
        ground_truth=data.get("ground_truth"),
        metadata=data.get("metadata", {}),
    )
