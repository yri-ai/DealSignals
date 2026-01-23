from scripts.prep_layer_03 import build_document_text


def test_build_document_text_includes_page_markers(tmp_path):
    pages = tmp_path / "pages.jsonl"
    pages.write_text(
        '{"page":1,"text":"Hello"}\n{"page":2,"text":"World"}\n',
        encoding="utf-8",
    )
    content = build_document_text(pages)
    assert "[Page 1]" in content
    assert "Hello" in content
    assert "[Page 2]" in content
