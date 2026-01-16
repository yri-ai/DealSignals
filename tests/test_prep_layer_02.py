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
