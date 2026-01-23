import logging
from pathlib import Path

from dealsignals.parsing.ocr_client import OcrResult
from scripts import prep_layer_03
from scripts.prep_layer_03 import build_document_text


def test_build_document_text_includes_page_markers(tmp_path, caplog):
    pages = tmp_path / "pages.jsonl"
    pages.write_text(
        "\n".join(
            [
                '{"page":1,"text":"Hello"}',
                "not json",
                '{"page":2,"text":"World"}',
                '{"page":3}',
                '{"text":"Missing page"}',
                "",
            ]
        ),
        encoding="utf-8",
    )

    with caplog.at_level(logging.WARNING):
        content = build_document_text(pages)

    assert content == "[Page 1]\nHello\n\n[Page 2]\nWorld"
    warning_messages = [record.message for record in caplog.records]
    assert warning_messages == [
        "Skipping malformed JSONL line 2",
        "Skipping page entry missing keys: page, text on line 4",
        "Skipping page entry missing keys: page, text on line 5",
    ]


class FakeOcrClient:
    def __init__(self, results: dict[str, OcrResult]) -> None:
        self._results = results
        self.submissions: list[dict[str, str]] = []

    def submit_pdf(
        self,
        file_path: str,
        run_id: str,
        document_id: str,
        parser_profile: str,
        callback_url: str,
    ) -> str:
        self.submissions.append(
            {
                "file_path": file_path,
                "run_id": run_id,
                "document_id": document_id,
                "parser_profile": parser_profile,
                "callback_url": callback_url,
            }
        )
        return f"job_{document_id}"

    def get_status(self, job_id: str) -> dict[str, str]:
        document_id = job_id.replace("job_", "")
        return {"job_id": job_id, "status": self._results[document_id].status}

    def get_result(self, job_id: str) -> OcrResult:
        document_id = job_id.replace("job_", "")
        return self._results[document_id]


def _write_pages(path: Path, text: str) -> None:
    path.write_text(f'{{"page":1,"text":"{text}"}}\n', encoding="utf-8")


def _build_result(tmp_path: Path, document_id: str, text: str) -> OcrResult:
    searchable_pdf = tmp_path / f"{document_id}_searchable.pdf"
    searchable_pdf.write_bytes(b"%PDF-1.4")
    text_path = tmp_path / f"{document_id}_ocr.txt"
    text_path.write_text("raw text", encoding="utf-8")
    pages_path = tmp_path / f"{document_id}_pages.jsonl"
    _write_pages(pages_path, text)
    meta_path = tmp_path / f"{document_id}_meta.json"
    meta_path.write_text("{}", encoding="utf-8")
    return OcrResult(
        job_id=f"job_{document_id}",
        status="succeeded",
        artifacts={
            "searchable_pdf_path": str(searchable_pdf),
            "text_path": str(text_path),
            "pages_path": str(pages_path),
            "meta_path": str(meta_path),
        },
        metadata={},
    )


def test_prep_layer_03_writes_outputs(tmp_path, monkeypatch):
    output_dir = tmp_path / "layer-03/ocrmypdf_tesseract_v1"
    s4_pdf = tmp_path / "s4.pdf"
    investor_pdf = tmp_path / "investor.pdf"
    s4_pdf.write_bytes(b"%PDF-1.4 s4")
    investor_pdf.write_bytes(b"%PDF-1.4 investor")

    results = {
        "s4": _build_result(tmp_path, "s4", "S4 content"),
        "investor_presentation": _build_result(
            tmp_path,
            "investor_presentation",
            "Investor content",
        ),
    }
    fake_client = FakeOcrClient(results)

    monkeypatch.setenv("LAYER_03_OUTPUT_DIR", str(output_dir))
    monkeypatch.setenv("LAYER_03_S4_PDF_PATH", str(s4_pdf))
    monkeypatch.setenv("LAYER_03_INVESTOR_PDF_PATH", str(investor_pdf))
    monkeypatch.setattr(prep_layer_03.time, "sleep", lambda _: None)

    result = prep_layer_03.main(client=fake_client, sleep_seconds=0)

    assert result == 0
    assert (output_dir / "s4_text.txt").read_text(encoding="utf-8") == "[Page 1]\nS4 content"
    assert (output_dir / "investor_presentation_text.txt").read_text(
        encoding="utf-8"
    ) == "[Page 1]\nInvestor content"
    assert (output_dir / "s4_pages.jsonl").exists()
    assert (output_dir / "investor_presentation_searchable.pdf").exists()
