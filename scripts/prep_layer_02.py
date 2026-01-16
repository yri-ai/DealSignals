import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

S4_HEADERS = [
    "RISK FACTORS",
    "SUMMARY",
    "SELECTED FINANCIAL DATA",
    "MANAGEMENT’S DISCUSSION AND ANALYSIS",
    "MANAGEMENT'S DISCUSSION AND ANALYSIS",
    "PROJECTIONS",
    "TRANSACTION TERMS",
    "RELATED-PARTY / CONFLICTS",
    "LEGAL / REGULATORY",
    "APPENDICES",
]
INVESTOR_HEADERS = [
    "EXECUTIVE SUMMARY",
    "MARKET / STRATEGY",
    "UNIT ECONOMICS",
    "FINANCIAL PROJECTIONS",
    "RISKS / DISCLAIMERS",
    "RISKS",
]
DEFAULT_S4_BUDGET_CHARS = 320000
DEFAULT_INVESTOR_BUDGET_CHARS = 160000


def parse_sections(text: str, headers: list[str]) -> dict[str, str]:
    matches: list[tuple[int, int, str]] = []
    for header in headers:
        pattern = re.compile(rf"(?m)^{re.escape(header)}\s*$")
        last_match: re.Match[str] | None = None
        for match in pattern.finditer(text):
            last_match = match
        if last_match:
            matches.append((last_match.start(), last_match.end(), header))

    matches.sort()
    sections: dict[str, str] = {}
    for index, (start, _end, header) in enumerate(matches):
        section_end = matches[index + 1][0] if index + 1 < len(matches) else len(text)
        sections[header] = text[start:section_end]
    return sections


def truncate_sections(
    sections: dict[str, str],
    priority: list[str],
    budget_chars: int,
) -> str:
    if budget_chars <= 0:
        return ""

    remaining = budget_chars
    output: list[str] = []
    for header in priority:
        if header not in sections or remaining <= 0:
            continue
        section_text = sections[header]
        if len(section_text) <= remaining:
            output.append(section_text)
            remaining -= len(section_text)
        else:
            output.append(section_text[:remaining])
            remaining = 0
    return "".join(output)


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _env_int(name: str, default: int) -> int:
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError:
        print(f"Warning: invalid {name}={raw_value!r}; using default {default}.")
        return default


def _section_coverage(headers: list[str], sections: dict[str, str]) -> dict[str, object]:
    found = [header for header in headers if header in sections]
    missing = [header for header in headers if header not in sections]
    coverage_ratio = len(found) / len(headers) if headers else 0.0
    return {
        "requested": headers,
        "found": found,
        "missing": missing,
        "coverage_ratio": coverage_ratio,
    }


def _truncate_with_fallback(
    text: str,
    headers: list[str],
    budget_chars: int,
) -> tuple[str, dict[str, str]]:
    sections = parse_sections(text, headers)
    if not sections:
        print("Warning: No section headers found; using fallback slice.")
        return text[: max(budget_chars, 0)], sections

    truncated = truncate_sections(sections, headers, budget_chars)
    if not truncated:
        truncated = text[: max(budget_chars, 0)]
    return truncated, sections


def _build_document_meta(
    source_path: Path,
    output_path: Path,
    source_text: str,
    output_text: str,
    headers: list[str],
    budget_chars: int,
    sections: dict[str, str],
) -> dict[str, object]:
    return {
        "source_path": str(source_path),
        "source_hash": _hash_text(source_text),
        "output_path": str(output_path),
        "output_hash": _hash_text(output_text),
        "budget_chars": budget_chars,
        "source_chars": len(source_text),
        "output_chars": len(output_text),
        "section_coverage": _section_coverage(headers, sections),
    }


def main() -> int:
    base_dir = Path(os.environ.get("LAYER_02_BASE_DIR", "experiments/wework-bowx"))
    s4_path = base_dir / "data/merger/s-4-a/2021-09-17_d166510ds4a.txt"
    output_dir = base_dir / "data/layer-02"
    output_dir.mkdir(parents=True, exist_ok=True)

    investor_path_value = os.environ.get("LAYER_02_INVESTOR_PRESENTATION_PATH")
    if investor_path_value:
        investor_source = Path(investor_path_value)
    else:
        investor_source = base_dir / "data/merger/investor_presentation.txt"

    if not s4_path.exists():
        print(f"Error: File not found at {s4_path}")
        return 1

    if not investor_source.exists():
        print(
            "Error: Investor presentation source file not found. "
            "Set LAYER_02_INVESTOR_PRESENTATION_PATH to a real file."
        )
        return 1

    s4_budget_chars = _env_int("LAYER_02_S4_BUDGET_CHARS", DEFAULT_S4_BUDGET_CHARS)
    investor_budget_chars = _env_int(
        "LAYER_02_INVESTOR_BUDGET_CHARS", DEFAULT_INVESTOR_BUDGET_CHARS
    )

    s4_text = s4_path.read_text(encoding="utf-8")
    investor_text = investor_source.read_text(encoding="utf-8")

    s4_output, s4_sections = _truncate_with_fallback(s4_text, S4_HEADERS, s4_budget_chars)
    investor_output, investor_sections = _truncate_with_fallback(
        investor_text, INVESTOR_HEADERS, investor_budget_chars
    )

    s4_output_path = output_dir / "s4_risk_factors.txt"
    investor_output_path = output_dir / "investor_presentation.txt"

    s4_output_path.write_text(s4_output, encoding="utf-8")
    investor_output_path.write_text(investor_output, encoding="utf-8")

    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rotation_mode": "none",
        "budgets": {
            "s4_chars": s4_budget_chars,
            "investor_presentation_chars": investor_budget_chars,
        },
        "documents": {
            "s4": _build_document_meta(
                s4_path,
                s4_output_path,
                s4_text,
                s4_output,
                S4_HEADERS,
                s4_budget_chars,
                s4_sections,
            ),
            "investor_presentation": _build_document_meta(
                investor_source,
                investor_output_path,
                investor_text,
                investor_output,
                INVESTOR_HEADERS,
                investor_budget_chars,
                investor_sections,
            ),
        },
    }

    meta_path = output_dir / "layer-02_meta.json"
    meta_path.write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote metadata to {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
