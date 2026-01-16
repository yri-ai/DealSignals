import json

import pytest

from scripts.prep_layer_02 import parse_sections, truncate_sections


def test_section_priority_truncation_prefers_ordered_sections():
    text = "SECTION B\nb1\nb2\nSECTION A\na1\nSECTION C\nc1\nc2\n"
    headers = ["SECTION A", "SECTION B", "SECTION C"]

    sections = parse_sections(text, headers)

    budget_chars = len(sections["SECTION A"]) + 5
    result = truncate_sections(
        sections,
        priority=["SECTION A", "SECTION C", "SECTION B"],
        budget_chars=budget_chars,
    )

    expected = sections["SECTION A"] + sections["SECTION C"][:5]
    assert result == expected


def test_parse_sections_prefers_last_header_occurrence():
    text = "TABLE OF CONTENTS\nSECTION A\nSECTION B\n\nSECTION A\nA body\nSECTION B\nB body\n"
    headers = ["SECTION A", "SECTION B"]

    sections = parse_sections(text, headers)

    assert sections["SECTION A"] == "SECTION A\nA body\n"
    assert sections["SECTION B"] == "SECTION B\nB body\n"


def test_parse_sections_ignores_missing_headers():
    text = "SECTION A\nA body\n"
    headers = ["SECTION A", "SECTION B"]

    sections = parse_sections(text, headers)

    assert "SECTION A" in sections
    assert "SECTION B" not in sections


def test_truncate_sections_zero_budget_returns_empty():
    sections = {"SECTION A": "SECTION A\nA body\n"}

    assert truncate_sections(sections, priority=["SECTION A"], budget_chars=0) == ""


def test_truncate_sections_negative_budget_returns_empty():
    sections = {"SECTION A": "SECTION A\nA body\n"}

    assert truncate_sections(sections, priority=["SECTION A"], budget_chars=-10) == ""


def test_truncate_sections_exact_budget_keeps_full_sections():
    text = "SECTION A\nA body\nSECTION B\nB body\n"
    headers = ["SECTION A", "SECTION B"]
    sections = parse_sections(text, headers)
    budget_chars = len(sections["SECTION A"]) + len(sections["SECTION B"])

    result = truncate_sections(
        sections,
        priority=["SECTION A", "SECTION B"],
        budget_chars=budget_chars,
    )

    assert result == sections["SECTION A"] + sections["SECTION B"]


def test_prep_writes_metadata(tmp_path, monkeypatch):
    base_dir = tmp_path / "experiments/wework-bowx"
    s4_path = base_dir / "data/merger/s-4-a/2021-09-17_d166510ds4a.txt"
    investor_path = base_dir / "data/merger/investor_presentation.txt"

    s4_path.parent.mkdir(parents=True, exist_ok=True)
    investor_path.parent.mkdir(parents=True, exist_ok=True)

    s4_path.write_text("RISK FACTORS\nRisk body\nSUMMARY\nSummary body\n")
    investor_path.write_text("EXECUTIVE SUMMARY\nDeck body\nRISKS\nRisk deck\n")

    monkeypatch.setenv("LAYER_02_BASE_DIR", str(base_dir))
    monkeypatch.setenv("LAYER_02_INVESTOR_PRESENTATION_PATH", str(investor_path))

    from scripts import prep_layer_02

    prep_layer_02.main()

    meta_path = base_dir / "data/layer-02/layer-02_meta.json"
    assert meta_path.exists()

    metadata = json.loads(meta_path.read_text())
    assert "documents" in metadata
    assert "s4" in metadata["documents"]
    assert "investor_presentation" in metadata["documents"]

    s4_meta = metadata["documents"]["s4"]
    investor_meta = metadata["documents"]["investor_presentation"]

    assert len(s4_meta["source_hash"]) == 64
    assert len(investor_meta["source_hash"]) == 64
    assert s4_meta["budget_chars"] > 0
    assert investor_meta["budget_chars"] > 0
    assert "section_coverage" in s4_meta
    assert "section_coverage" in investor_meta
