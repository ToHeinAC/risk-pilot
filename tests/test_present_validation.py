"""Validation results for the YAML editor (M2 AK 6)."""

from app.present.validation import check_text


def test_valid_model_status() -> None:
    result = check_text(
        "schema_version: 1\nmodel: m\nnodes:\n  a: {type: constant, value: 1}\n"
        "  y: {type: output, expr: a}\n"
    )
    assert result.compiled is not None
    assert result.rows == []
    assert result.status == "Gültig – 2 Knoten, 1 Ausgabe"
    assert [r.node for r in result.node_table] == ["a", "y"]


def test_yaml_error_with_line_excerpt() -> None:
    result = check_text("schema_version: 1\nmodel: m\nnodes:\n  a: {type: constant, value: [1\n")
    assert result.compiled is None
    row = result.rows[0]
    assert row.line is not None
    assert row.excerpt
    assert "YAML" in row.message
    assert result.status == "1 Problem"


def test_cycle_and_missing_output_in_german() -> None:
    result = check_text(
        "schema_version: 1\nmodel: m\nnodes:\n  a: {type: derived, expr: b}\n"
        "  b: {type: derived, expr: a}\n"
    )
    messages = [r.message for r in result.rows]
    assert any("Zyklus" in m for m in messages)
    assert any("output" in m for m in messages)
    assert result.status == "2 Probleme"


def test_empty_model_is_hint_not_error() -> None:
    result = check_text("schema_version: 1\nmodel: m\nnodes: {}\n")
    assert result.rows == []
    assert result.hint == "Das Modell enthält noch keine Knoten."
    assert result.compiled is None


def test_blank_text_is_hint() -> None:
    assert check_text("   \n").hint
