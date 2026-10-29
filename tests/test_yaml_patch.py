"""Form edits written back into the YAML text, comments and layout kept (M6 AK 2, E4)."""

from pathlib import Path

import pytest

from app.errors import InputError
from app.model.yaml_io import model_from_yaml, model_to_yaml
from app.model.yaml_patch import load_data, patch

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
ALL = sorted(
    p
    for p in [*EXAMPLES.glob("*.yaml"), *EXAMPLES.glob("lernpfad/*.yaml")]
    if "schema_version:" in p.read_text("utf-8")
)
T2 = EXAMPLES / "t2_terminplan.yaml"


def comments(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip().startswith("#")]


@pytest.mark.parametrize("path", ALL, ids=lambda p: p.stem)
def test_unchanged_data_gives_the_same_text(path: Path) -> None:
    text = path.read_text("utf-8")
    assert patch(text, load_data(text)) == text


def test_changed_value_keeps_comments_and_flow_style() -> None:
    text = T2.read_text("utf-8")
    data = load_data(text)
    data["nodes"]["b"]["mean"] = 16
    out = patch(text, data)
    assert comments(out) == comments(text)
    assert (
        '  b: {type: uncertain, dist: normal, mean: 16, sd: 3, unit: d, name: "Vorgang B"}' in out
    )
    changed = [a for a, b in zip(text.splitlines(), out.splitlines(), strict=True) if a != b]
    assert len(changed) == 1


def test_added_node_follows_flow_style_and_removed_key_disappears() -> None:
    text = T2.read_text("utf-8")
    data = load_data(text)
    data["nodes"]["d"] = {"type": "constant", "value": 3}
    del data["nodes"]["a"]["unit"]
    out = patch(text, data)
    assert "  d: {type: constant, value: 3}" in out
    assert 'unit: d, name: "Vorgang A"' not in out
    assert load_data(out) == data
    assert comments(out) == comments(text)


def test_new_node_may_be_incomplete() -> None:
    text = "schema_version: 1\nmodel: m\nnodes: {}\n"
    data = load_data(text)
    data["nodes"]["x"] = {"type": "uncertain", "dist": "normal"}
    assert load_data(patch(text, data)) == data


def test_list_changes_are_written() -> None:
    text = (EXAMPLES / "t4_portfolio.yaml").read_text("utf-8")
    data = load_data(text)
    data["correlations"]["markt"]["spearman"][0][1] = 0.25
    out = patch(text, data)
    assert load_data(out) == data
    assert "      - [1.0, 0.25, 0.1]" in out


def test_text_that_is_no_mapping_is_rejected() -> None:
    with pytest.raises(InputError) as exc:
        load_data("- a\n- b\n")
    assert exc.value.issue.code == "form.no_mapping"
    with pytest.raises(InputError) as exc:
        load_data("a: [1\n")
    assert exc.value.issue.code == "form.no_mapping"


@pytest.mark.parametrize("path", ALL, ids=lambda p: p.stem)
def test_one_change_touches_one_line(path: Path) -> None:
    text = path.read_text("utf-8")
    data = load_data(text)
    key = "title" if "title" in data else next(iter(data))
    data[key] = "Geändert"
    out = patch(text, data)
    changed = [a for a, b in zip(text.splitlines(), out.splitlines(), strict=True) if a != b]
    assert len(changed) == 1
    assert comments(out) == comments(text)


def test_text_written_by_pyyaml_keeps_its_list_style() -> None:
    text = model_to_yaml(model_from_yaml((EXAMPLES / "t4_portfolio.yaml").read_text("utf-8")))
    data = load_data(text)
    data["title"] = "Geändert"
    changed = [
        a for a, b in zip(text.splitlines(), patch(text, data).splitlines(), strict=True) if a != b
    ]
    assert len(changed) == 1


def test_validated_model_dump_changes_only_the_edited_line() -> None:
    text = T2.read_text("utf-8")
    data = model_from_yaml(text).model_dump(mode="json", exclude_unset=True)  # 15 -> 15.0
    data["nodes"]["c"]["sd"] = 5
    out = patch(text, data)
    changed = [a for a, b in zip(text.splitlines(), out.splitlines(), strict=True) if a != b]
    line = '  c: {type: uncertain, dist: normal, mean: 24, sd: 4, unit: d, name: "Vorgang C"}'
    assert changed == [line]


def test_deleting_a_node_keeps_other_comments_and_drops_its_own() -> None:
    text = T2.read_text("utf-8")
    note = "  # Im Hauptszenario tritt die Nacharbeit nie ein"
    data = load_data(text)
    del data["nodes"]["c"]
    assert note in patch(text, data)
    data = load_data(text)
    del data["nodes"]["nacharbeit"]
    assert note not in patch(text, data)


def test_list_length_change_keeps_comments_and_item_style() -> None:
    text = (
        "schema_version: 1\nmodel: m\nnodes:\n  c:\n    type: choice\n    options:\n"
        "      - {label: a, weight: 1}  # erste\n      - {label: b, weight: 1}\n"
        "# Ende\n"
    )
    data = load_data(text)
    data["nodes"]["c"]["options"].append({"label": "c", "weight": 2})
    out = patch(text, data)
    assert "# erste" in out
    assert "# Ende" in out
    assert "      - {label: c, weight: 2}" in out
    data["nodes"]["c"]["options"] = data["nodes"]["c"]["options"][:1]
    assert "# erste" in patch(text, data)


def test_new_children_of_an_empty_flow_mapping_are_block_style() -> None:
    text = "schema_version: 1\nmodel: m\nnodes: {}\n"
    data = load_data(text)
    data["nodes"] = {"a": {"type": "constant", "value": 1}, "b": {"type": "constant", "value": 2}}
    out = patch(text, data)
    assert "nodes:\n  a:" in out
    assert len(out.splitlines()) > 3


@pytest.mark.parametrize("word", ["on", "yes", "No", "1_000", "1:30", "null", "~", "0x10"])
def test_strings_read_back_as_strings_by_the_app(word: str) -> None:
    text = T2.read_text("utf-8")
    data = load_data(text)
    data["nodes"]["a"]["name"] = word
    data["nodes"]["a"]["unit"] = word
    model = model_from_yaml(patch(text, data))
    assert model.nodes["a"].name == word
    assert model.nodes["a"].unit == word
