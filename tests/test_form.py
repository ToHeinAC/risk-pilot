"""Form values <-> raw model data, lossless (M6 AK 2)."""

from pathlib import Path

import pytest

from app.errors import InputError
from app.model import form
from app.model.yaml_io import model_from_yaml
from app.model.yaml_patch import Data, load_data, patch

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
MODELS = sorted(
    p
    for p in [*EXAMPLES.glob("*.yaml"), *EXAMPLES.glob("lernpfad/*.yaml")]
    if "schema_version:" in p.read_text("utf-8")
)


def data(name: str) -> Data:
    return load_data((EXAMPLES / name).read_text("utf-8"))


@pytest.mark.parametrize("path", MODELS, ids=lambda p: p.stem)
def test_form_values_applied_unchanged_give_the_same_data(path: Path) -> None:
    d = load_data(path.read_text("utf-8"))
    for node_id in d["nodes"]:
        assert form.apply(d, node_id, form.values(d, node_id)) == d
    assert form.apply_header(d, form.header_values(d)) == d


def test_changed_fields_are_written_with_their_types() -> None:
    d = data("t2_terminplan.yaml")
    v = form.values(d, "b")
    assert v["param.mean"] == "15"
    assert v["name"] == "Vorgang B"
    v["param.mean"] = "16,5"
    v["why"] = "Erfahrung"
    v["unit"] = ""
    out = form.apply(d, "b", v)["nodes"]["b"]
    assert out["mean"] == 16.5
    assert out["why"] == "Erfahrung"
    assert "unit" not in out
    assert d["nodes"]["b"]["mean"] == 15  # the input stays unchanged


def test_expression_parameters_and_lists_stay_text_or_numbers() -> None:
    d = load_data(
        "schema_version: 1\nmodel: m\nnodes:\n"
        "  k: {type: constant, value: 2}\n"
        "  u: {type: uncertain, dist: normal, mean: 'k * 2', sd: 1}\n"
        "  e: {type: uncertain, dist: empirical, values: [1, 2.5, 3]}\n"
    )
    assert form.values(d, "u")["param.mean"] == "k * 2"
    assert form.values(d, "e")["param.values"] == "1; 2.5; 3"
    v = form.values(d, "e")
    v["param.values"] = "4; 5,5; 6"
    assert form.apply(d, "e", v)["nodes"]["e"]["values"] == [4, 5.5, 6]


def test_param_fields_come_from_the_family() -> None:
    d = data("t2_terminplan.yaml")
    assert [f.name for f in form.param_fields(d, "b")] == ["mean", "sd"]
    changed = form.set_dist(d, "b", "lognormal", "params")
    node = changed["nodes"]["b"]
    assert node["dist"] == "lognormal"
    assert "mean" not in node
    assert "sd" not in node
    assert node["name"] == "Vorgang B"


def test_why_with_links_keeps_links() -> None:
    d = load_data(
        "schema_version: 1\nmodel: m\nnodes:\n"
        "  k: {type: constant, value: 2, why: {text: alt, links: ['https://x.org']}}\n"
    )
    v = form.values(d, "k")
    assert v["why"] == "alt"
    v["why"] = "neu"
    assert form.apply(d, "k", v)["nodes"]["k"]["why"] == {"text": "neu", "links": ["https://x.org"]}


def test_output_target_choice_options_and_bounds() -> None:
    d = data("t2_terminplan.yaml")
    v = form.values(d, "ende")
    assert (v["target_op"], v["target_value"]) == ("le", "30")
    v["target_op"] = ""
    v["bounds_min"] = "0"
    out = form.apply(d, "ende", v)["nodes"]["ende"]
    assert "target" not in out
    assert out["bounds"] == {"min": 0}
    c = load_data(
        "schema_version: 1\nmodel: m\nnodes:\n"
        "  c: {type: choice, options: [{label: a, weight: 1}, {label: b, weight: 2}]}\n"
    )
    v = form.values(c, "c")
    assert v["options"] == [("a", "1"), ("b", "2")]
    v["options"] = [("a", "1"), ("b", "2"), ("c", "0,5")]
    assert form.apply(c, "c", v)["nodes"]["c"]["options"][2] == {"label": "c", "weight": 0.5}


def test_add_node_leaves_required_fields_empty() -> None:
    d = data("t2_terminplan.yaml")
    added = form.add_node(d, "puffer", "constant")
    assert added["nodes"]["puffer"] == {"type": "constant"}
    for bad in ("Puffer", "a", "max"):
        with pytest.raises(InputError):
            form.add_node(d, bad, "constant")


def test_new_uncertain_node_starts_with_the_range() -> None:
    added = form.add_node(data("t2_terminplan.yaml"), "puffer", "uncertain")
    assert added["nodes"]["puffer"] == {"type": "uncertain", "dist": "normal", "input": "quantiles"}
    assert [s.name for s in form.param_fields(added, "puffer")] == ["p10", "p50", "p90"]


def test_remove_node_only_without_references() -> None:
    d = data("t2_terminplan.yaml")
    with pytest.raises(InputError) as exc:
        form.remove_node(d, "b")
    assert exc.value.issue.code == "form.referenced"
    assert exc.value.issue.params["refs"] == ["pfad1", "Szenario b_schneller"]
    assert "ende" not in form.remove_node(d, "ende")["nodes"]
    t4 = data("t4_portfolio.yaml")
    with pytest.raises(InputError) as exc:
        form.remove_node(t4, "l_gold")
    assert "Korrelationsgruppe markt" in str(exc.value.issue.params["refs"])


def test_header_values_and_settings() -> None:
    d = data("t2_terminplan.yaml")
    v = form.header_values(d)
    assert v["n"] == "100000"
    v["seed"] = "7"
    v["illustrative"] = True
    out = form.apply_header(d, v)
    assert out["settings"] == {"n": 100000, "seed": 7}
    assert out["illustrative"] is True


@pytest.mark.parametrize("path", MODELS, ids=lambda p: p.stem)
def test_every_node_rebuilt_from_its_form_values_gives_the_same_model(path: Path) -> None:
    text = path.read_text("utf-8")
    d = load_data(text)
    for node_id, node in d["nodes"].items():
        empty = {**d, "nodes": {**d["nodes"], node_id: {"type": node["type"]}}}
        rebuilt = form.apply(empty, node_id, form.values(d, node_id))
        assert model_from_yaml(patch(text, rebuilt)) == model_from_yaml(text), node_id


@pytest.mark.parametrize(
    ("typed", "expected"), [("1e3", 1000.0), ("-0", 0), ("2,5", 2.5), ("-.5", -0.5), ("+3", 3)]
)
def test_number_inputs(typed: str, expected: float) -> None:
    assert form.number(typed) == expected


def test_invalid_bound_is_an_error_not_a_deletion() -> None:
    d = load_data(
        "schema_version: 1\nmodel: m\nnodes:\n  k: {type: constant, value: 2, bounds: {min: 0}}\n"
    )
    v = form.values(d, "k")
    v["bounds_min"] = "abc"
    with pytest.raises(InputError) as exc:
        form.apply(d, "k", v)
    assert exc.value.issue.code == "form.number"


def test_clearing_why_text_keeps_links() -> None:
    d = load_data(
        "schema_version: 1\nmodel: m\nnodes:\n"
        "  k: {type: constant, value: 2, why: {text: alt, links: ['https://x.org']}}\n"
    )
    v = form.values(d, "k")
    v["why"] = ""
    assert form.apply(d, "k", v)["nodes"]["k"]["why"] == {"text": "", "links": ["https://x.org"]}
