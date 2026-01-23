import json
import logging
from pathlib import Path


def build_document_text(pages_path: Path) -> str:
    logger = logging.getLogger(__name__)
    lines: list[str] = []
    for raw_line in pages_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        try:
            page = json.loads(raw_line)
        except json.JSONDecodeError:
            logger.warning("Skipping malformed JSONL line")
            continue
        if not isinstance(page, dict) or "page" not in page or "text" not in page:
            logger.warning("Skipping page entry missing keys: page, text")
            continue
        page_number = page["page"]
        page_text = str(page["text"]).strip()
        lines.append(f"[Page {page_number}]\n{page_text}\n")
    return "\n".join(lines).strip()
