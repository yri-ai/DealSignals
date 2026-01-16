import re
from pathlib import Path


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


def main():
    # Setup paths
    base_dir = Path("experiments/wework-bowx")
    s4_path = base_dir / "data/merger/s-4-a/2021-09-17_d166510ds4a.txt"
    output_dir = base_dir / "data/layer-02"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Process S-4 Risk Factors
    print(f"Reading {s4_path}...")
    if not s4_path.exists():
        print(f"Error: File not found at {s4_path}")
        return

    with open(s4_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Simple extraction logic (adjust based on actual file structure inspection if needed)
    # Looking for "RISK FACTORS" header and stopping before next major section
    # This is a heuristic; might need tuning.
    start_marker = "RISK FACTORS"
    end_marker = "CAUTIONARY NOTE REGARDING FORWARD-LOOKING STATEMENTS"

    start_idx = text.find(start_marker)
    # Search for end marker after the start marker
    end_idx = text.find(end_marker, start_idx)

    if start_idx == -1:
        print("Warning: Could not find 'RISK FACTORS' marker.")
        # Fallback logic could go here, but for now we warn
        risk_text = "RISK FACTORS SECTION NOT FOUND"
    elif end_idx == -1:
        print(
            f"Warning: Could not find '{end_marker}' marker. "
            "Extracting from start marker to end of 100k chars."
        )
        risk_text = text[start_idx : start_idx + 100000]
    else:
        risk_text = text[start_idx:end_idx]
        print(f"Extracted Risk Factors: {len(risk_text)} chars")

    with open(output_dir / "s4_risk_factors.txt", "w", encoding="utf-8") as f:
        f.write(risk_text)

    # 2. Placeholder for Investor Presentation
    # (Assuming we might manually place it or it exists elsewhere)
    # For now, create a dummy if not exists to unblock config
    inv_deck_path = output_dir / "investor_presentation.txt"
    if not inv_deck_path.exists():
        print("Creating placeholder for Investor Presentation...")
        with open(inv_deck_path, "w", encoding="utf-8") as f:
            f.write("WEWORK INVESTOR PRESENTATION (Placeholder)\n\n[Full text would go here]")
    else:
        print("Investor Presentation file already exists.")


if __name__ == "__main__":
    main()
