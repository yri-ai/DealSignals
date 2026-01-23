import json
import logging
import os
import shutil
import time
from pathlib import Path

from dealsignals.parsing.ocr_client import OcrClient


def build_document_text(pages_path: Path) -> str:
    logger = logging.getLogger(__name__)
    lines: list[str] = []
    for line_number, raw_line in enumerate(
        pages_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not raw_line.strip():
            continue
        try:
            page = json.loads(raw_line)
        except json.JSONDecodeError:
            logger.warning("Skipping malformed JSONL line %s", line_number)
            continue
        if not isinstance(page, dict) or "page" not in page or "text" not in page:
            logger.warning(
                "Skipping page entry missing keys: page, text on line %s",
                line_number,
            )
            continue
        page_number = page["page"]
        page_text = str(page["text"]).strip()
        lines.append(f"[Page {page_number}]\n{page_text}\n")
    return "\n".join(lines).strip()


def _require_env(name: str) -> str | None:
    value = os.environ.get(name)
    if value:
        return value
    print(f"Error: {name} is required.")
    return None


def _wait_for_completion(client: OcrClient, job_id: str, sleep_seconds: float) -> str:
    while True:
        status_payload = client.get_status(job_id)
        status = status_payload.get("status")
        if status in {"succeeded", "failed"}:
            return str(status)
        time.sleep(sleep_seconds)


def _copy_artifacts(
    artifacts: dict[str, object],
    output_dir: Path,
    document_id: str,
) -> dict[str, Path]:
    mapping = {
        "searchable_pdf_path": f"{document_id}_searchable.pdf",
        "text_path": f"{document_id}_ocr.txt",
        "pages_path": f"{document_id}_pages.jsonl",
        "meta_path": f"{document_id}_meta.json",
    }
    copied: dict[str, Path] = {}
    for key, filename in mapping.items():
        source_value = artifacts.get(key)
        if not source_value:
            continue
        source_path = Path(str(source_value))
        destination = output_dir / filename
        shutil.copy(source_path, destination)
        copied[key] = destination
    return copied


def main(client: OcrClient | None = None, sleep_seconds: float = 1.0) -> int:
    base_url = os.environ.get("LAYER_03_BASE_URL", "http://localhost:8000")
    output_dir_value = os.environ.get("LAYER_03_OUTPUT_DIR")
    if output_dir_value:
        output_dir = Path(output_dir_value)
    else:
        output_dir = Path("experiments/wework-bowx/data/layer-03/ocrmypdf_tesseract_v1")

    s4_path_value = _require_env("LAYER_03_S4_PDF_PATH")
    investor_path_value = _require_env("LAYER_03_INVESTOR_PDF_PATH")
    if not s4_path_value or not investor_path_value:
        return 1

    documents = {
        "s4": Path(s4_path_value),
        "investor_presentation": Path(investor_path_value),
    }

    for document_id, path in documents.items():
        if not path.exists():
            print(f"Error: PDF not found for {document_id}: {path}")
            return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    parser_profile = "ocrmypdf_tesseract_v1"
    run_id = "layer-03"
    callback_url = f"{base_url}/v1/ocr/callback"

    def process_document(client_instance: OcrClient, document_id: str, path: Path) -> int:
        job_id = client_instance.submit_pdf(
            file_path=str(path),
            run_id=run_id,
            document_id=document_id,
            parser_profile=parser_profile,
            callback_url=callback_url,
        )
        status = _wait_for_completion(client_instance, job_id, sleep_seconds)
        if status != "succeeded":
            print(f"Error: OCR job {job_id} failed with status {status}.")
            return 1
        result = client_instance.get_result(job_id)
        if result.status != "succeeded":
            print(f"Error: OCR job {job_id} failed with status {result.status}.")
            return 1
        copied = _copy_artifacts(result.artifacts, output_dir, document_id)
        pages_path = copied.get("pages_path")
        if not pages_path:
            print(f"Error: Missing pages artifact for {document_id}.")
            return 1
        document_text = build_document_text(pages_path)
        output_path = output_dir / f"{document_id}_text.txt"
        output_path.write_text(document_text, encoding="utf-8")
        return 0

    if client is None:
        with OcrClient(base_url=base_url) as live_client:
            for document_id, path in documents.items():
                if process_document(live_client, document_id, path) != 0:
                    return 1
    else:
        for document_id, path in documents.items():
            if process_document(client, document_id, path) != 0:
                return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
