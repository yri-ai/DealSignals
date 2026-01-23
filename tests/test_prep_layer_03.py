import logging

from scripts.prep_layer_03 import build_document_text


def test_build_document_text_includes_page_markers(tmp_path, caplog):
    pages = tmp_path / "pages.jsonl"
    pages.write_text(
        "\n".join(
            [
                '{"page":1,"text":"Hello"}',
                "not json",
                '{"page":2,"text":"World"}',
                '{"page":3}',
                '{"text":"Missing page"}',
                "",
            ]
        ),
        encoding="utf-8",
    )

    with caplog.at_level(logging.WARNING):
        content = build_document_text(pages)

    assert content == "[Page 1]\nHello\n\n[Page 2]\nWorld"
    warning_messages = [record.message for record in caplog.records]
    assert warning_messages == [
        "Skipping malformed JSONL line 2",
        "Skipping page entry missing keys: page, text on line 4",
        "Skipping page entry missing keys: page, text on line 5",
    ]
