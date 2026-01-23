from pathlib import Path


def test_layer_03_readme_mentions_ocr_service():
    repo_root = Path(__file__).resolve().parents[1]
    readme_path = repo_root / "experiments/wework-bowx/layers/03-parsing/README.md"
    content = readme_path.read_text(encoding="utf-8")
    lowered = content.lower()

    assert "ocr" in lowered
    assert "prep_layer_03.py" in content
