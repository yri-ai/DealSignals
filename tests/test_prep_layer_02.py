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
