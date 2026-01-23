from pathlib import Path

import httpx
import pytest

from dealsignals.parsing.ocr_client import OcrClient


@pytest.fixture
def mock_transport():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["request"] = request
        captured["body"] = request.read()
        return httpx.Response(200, json={"job_id": "job_abc"})

    transport = httpx.MockTransport(handler)
    transport.captured = captured
    return transport


def test_submit_job_uses_expected_payload(tmp_path, mock_transport):
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 sample")

    client = OcrClient(base_url="http://localhost:8000", transport=mock_transport)
    job_id = client.submit_pdf(
        file_path=str(pdf_path),
        run_id="run_123",
        document_id="doc_456",
        parser_profile="ocrmypdf_tesseract_v1",
        callback_url="http://localhost/callback",
    )

    assert job_id == "job_abc"

    request = mock_transport.captured["request"]
    body = mock_transport.captured["body"]

    assert request.method == "POST"
    assert str(request.url) == "http://localhost:8000/v1/ocr"
    assert request.headers["content-type"].startswith("multipart/form-data")
    assert b"run_123" in body
    assert b"doc_456" in body
    assert b"ocrmypdf_tesseract_v1" in body
    assert b"http://localhost/callback" in body
    assert b"sample.pdf" in body
