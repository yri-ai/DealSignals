# Layer 03 Parsing (OCR) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a Layer 03 parsing experiment that consumes OCRmyPDF/Tesseract outputs from the local OCR service and runs the standard question set against those parsed documents.

**Architecture:** Add an OCR service client + prep script that submits PDFs to the local OCR service, waits for results, and materializes page-aware text files under `experiments/wework-bowx/data/layer-03/ocrmypdf_tesseract_v1/`. Create a new Layer 03 experiment config that points at those generated text files and uses the optimized prompt template.

**Tech Stack:** Python 3.11+, httpx (client), YAML configs, existing ExperimentRunner.

---

### Task 1: Add OCR service client

**Files:**
- Create: `dealsignals/parsing/ocr_client.py`
- Modify: `dealsignals/parsing/__init__.py`
- Modify: `pyproject.toml`
- Test: `tests/test_ocr_client.py`

**Step 1: Write the failing test**
```python
from dealsignals.parsing.ocr_client import OcrClient


def test_submit_job_uses_expected_payload(mock_transport):
    client = OcrClient(base_url="http://localhost:8000", transport=mock_transport)
    job_id = client.submit_pdf(
        file_path="/tmp/sample.pdf",
        run_id="run_123",
        document_id="doc_456",
        parser_profile="ocrmypdf_tesseract_v1",
        callback_url="http://localhost/callback",
    )
    assert job_id == "job_abc"
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/test_ocr_client.py::test_submit_job_uses_expected_payload -v`
Expected: FAIL (module not implemented)

**Step 3: Write minimal implementation**
```python
# dealsignals/parsing/ocr_client.py
import httpx
from dataclasses import dataclass

@dataclass
class OcrResult:
    job_id: str
    status: str
    artifacts: dict
    metadata: dict
    error: dict | None

class OcrClient:
    def __init__(self, base_url: str, transport: httpx.BaseTransport | None = None):
        self._client = httpx.Client(base_url=base_url, transport=transport, timeout=60.0)

    def submit_pdf(self, file_path: str, run_id: str, document_id: str, parser_profile: str, callback_url: str) -> str:
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "application/pdf")}
            data = {"run_id": run_id, "document_id": document_id, "parser_profile": parser_profile, "callback_url": callback_url}
            response = self._client.post("/v1/ocr", data=data, files=files)
            response.raise_for_status()
            return response.json()["job_id"]

    def get_status(self, job_id: str) -> dict:
        response = self._client.get(f"/v1/ocr/{job_id}")
        response.raise_for_status()
        return response.json()

    def get_result(self, job_id: str) -> OcrResult:
        response = self._client.get(f"/v1/ocr/{job_id}/result")
        response.raise_for_status()
        payload = response.json()
        return OcrResult(**payload)
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/test_ocr_client.py::test_submit_job_uses_expected_payload -v`
Expected: PASS

**Step 5: Commit**
```bash
git add dealsignals/parsing/ocr_client.py dealsignals/parsing/__init__.py tests/test_ocr_client.py pyproject.toml
git commit -m "feat: add OCR service client"
```

---

### Task 2: Build page-aware document materializer

**Files:**
- Modify: `scripts/prep_layer_03.py`
- Test: `tests/test_prep_layer_03.py`

**Step 1: Write the failing test**
```python
from dealsignals.parsing.ocr_client import build_document_text


def test_build_document_text_includes_page_markers(tmp_path):
    pages = tmp_path / "pages.jsonl"
    pages.write_text('{"page":1,"text":"Hello"}\n{"page":2,"text":"World"}\n')
    content = build_document_text(pages)
    assert "[Page 1]" in content
    assert "Hello" in content
    assert "[Page 2]" in content
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/test_prep_layer_03.py::test_build_document_text_includes_page_markers -v`
Expected: FAIL

**Step 3: Write minimal implementation**
```python
# scripts/prep_layer_03.py

def build_document_text(pages_path: Path) -> str:
    lines = []
    for raw in pages_path.read_text().splitlines():
        if not raw.strip():
            continue
        page = json.loads(raw)
        lines.append(f"[Page {page['page']}]\n{page['text'].strip()}\n")
    return "\n".join(lines).strip()
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/test_prep_layer_03.py::test_build_document_text_includes_page_markers -v`
Expected: PASS

**Step 5: Commit**
```bash
git add scripts/prep_layer_03.py tests/test_prep_layer_03.py
git commit -m "feat: add page-aware OCR materializer"
```

---

### Task 3: Implement Layer 03 prep script (OCR service)

**Files:**
- Create: `scripts/prep_layer_03.py`
- Test: `tests/test_prep_layer_03.py`

**Step 1: Write the failing test**
```python
from scripts import prep_layer_03


def test_prep_layer_03_writes_outputs(tmp_path, monkeypatch):
    output_dir = tmp_path / "layer-03/ocrmypdf_tesseract_v1"
    monkeypatch.setenv("LAYER_03_OUTPUT_DIR", str(output_dir))
    monkeypatch.setenv("LAYER_03_S4_PDF_PATH", str(tmp_path / "s4.pdf"))
    monkeypatch.setenv("LAYER_03_INVESTOR_PDF_PATH", str(tmp_path / "deck.pdf"))
    # stub client returns a pages.jsonl fixture
    prep_layer_03.main(client=FakeOcrClient(...))
    assert (output_dir / "s4_text.txt").exists()
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/test_prep_layer_03.py::test_prep_layer_03_writes_outputs -v`
Expected: FAIL

**Step 3: Write minimal implementation**
```python
# scripts/prep_layer_03.py
# - read env: LAYER_03_BASE_URL (default http://localhost:8000)
# - read env: LAYER_03_S4_PDF_PATH, LAYER_03_INVESTOR_PDF_PATH
# - submit jobs via OcrClient
# - poll status until succeeded/failed
# - fetch result and copy artifacts
# - build page-aware text with build_document_text
# - write outputs under experiments/wework-bowx/data/layer-03/ocrmypdf_tesseract_v1/
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/test_prep_layer_03.py::test_prep_layer_03_writes_outputs -v`
Expected: PASS

**Step 5: Commit**
```bash
git add scripts/prep_layer_03.py tests/test_prep_layer_03.py
git commit -m "feat: add Layer 03 OCR prep script"
```

---

### Task 4: Add Layer 03 experiment config + prompts

**Files:**
- Create: `experiments/wework-bowx/layers/03-parsing/config_ocr.yaml`
- Create: `experiments/wework-bowx/layers/03-parsing/prompts/system.md`
- Create: `experiments/wework-bowx/layers/03-parsing/prompts/optimized.md`
- Create: `experiments/wework-bowx/layers/03-parsing/README.md`
- Test: `tests/test_layer_03_config.py`

**Step 1: Write the failing test**
```python
from pathlib import Path


def test_layer_03_readme_mentions_ocr_service():
    content = Path("experiments/wework-bowx/layers/03-parsing/README.md").read_text()
    assert "ocr" in content.lower()
    assert "prep_layer_03.py" in content
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/test_layer_03_config.py::test_layer_03_readme_mentions_ocr_service -v`
Expected: FAIL

**Step 3: Write minimal implementation**
```yaml
# config_ocr.yaml
layer:
  id: "03-parsing-ocr"
  name: "Parsing Comparison (OCRmyPDF)"
  description: "OCRmyPDF/Tesseract outputs as Layer 03 parser baseline."
  documents:
    - experiments/wework-bowx/data/layer-03/ocrmypdf_tesseract_v1/investor_presentation_text.txt
    - experiments/wework-bowx/data/layer-03/ocrmypdf_tesseract_v1/s4_text.txt
  prompts:
    system: prompts/system.md
    user: prompts/optimized.md
  models:
    - claude-sonnet-4-5
    - gpt-5.2
    - claude-opus-4-5

ground_truth: ../../ground-truth/questions.yaml
output_dir: ../../../../results/wework-bowx/layers/03-parsing/ocr
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/test_layer_03_config.py::test_layer_03_readme_mentions_ocr_service -v`
Expected: PASS

**Step 5: Commit**
```bash
git add experiments/wework-bowx/layers/03-parsing tests/test_layer_03_config.py
git commit -m "feat: add Layer 03 OCR experiment config"
```

---

### Task 5: Document run instructions

**Files:**
- Modify: `experiments/wework-bowx/layers/03-parsing/README.md`

**Step 1: Write the failing test**
```python
from pathlib import Path


def test_layer_03_readme_includes_run_commands():
    content = Path("experiments/wework-bowx/layers/03-parsing/README.md").read_text()
    assert "scripts/prep_layer_03.py" in content
    assert "scripts/run.py" in content
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/test_layer_03_config.py::test_layer_03_readme_includes_run_commands -v`
Expected: FAIL

**Step 3: Write minimal implementation**
```md
# README additions
- Service URL env: `LAYER_03_BASE_URL`
- PDF paths: `LAYER_03_S4_PDF_PATH`, `LAYER_03_INVESTOR_PDF_PATH`
- Run prep: `python scripts/prep_layer_03.py`
- Run layer: `python scripts/run.py --config .../03-parsing/config_ocr.yaml`
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/test_layer_03_config.py::test_layer_03_readme_includes_run_commands -v`
Expected: PASS

**Step 5: Commit**
```bash
git add experiments/wework-bowx/layers/03-parsing/README.md tests/test_layer_03_config.py
git commit -m "docs(layer-03): add run instructions"
```

---

## Notes / Decisions Needed Before Implementation
- Confirm OCR service base URL (`LAYER_03_BASE_URL`, default `http://localhost:8000`).
- Confirm source PDF paths for S-4 and investor deck on the local machine.

## Verification
- Run `pytest` for each added test case.
- Use `ruff check .` if linting issues appear in new code.
