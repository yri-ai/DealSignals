import json
from pathlib import Path


def build_document_text(pages_path: Path) -> str:
    lines: list[str] = []
    for raw_line in pages_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        page = json.loads(raw_line)
        page_number = page["page"]
        page_text = str(page["text"]).strip()
        lines.append(f"[Page {page_number}]\n{page_text}\n")
    return "\n".join(lines).strip()
