"""M9 AP3: canvas actions on raw model data (spec sections 3 and 4)."""

from typing import Any

import pytest

from app.adapters import files, settings
from app.errors import InputError
from app.model import canvas
from app.model.yaml_patch import Data, load_data

T2 = load_data(files.read_text(settings.examples_dir() / "t2_terminplan.yaml"))


def _data(**nodes: dict[str, Any]) -> Data:
    return {"schema_version": 1, "model": "m", "nodes": nodes}


def _code(exc: pytest.ExceptionInfo[InputError]) -> str:
    return exc.value.issue.code


U = {"type": "uncertain", "dist": "normal", "mean": 10, "sd": 2}


@pytest.mark.parametrize(
    ("text", "preset", "args"),
    [
        ("", "empty", ()),
        ("a", "single", ("a",)),
        ("max(a, b)", "max", ("a", "b")),
        ("min(a, b, c)", "min", ("a", "b", "c")),
        ("a + b + c", "sum", ("a", "b", "c")),
        ("a * b", "product", ("a", "b")),
        ("max(a, 24)", None, ()),
        ("a + b * c", None, ()),
        ("a +", None, ()),
    ],
)
def test_shape_recognises_preset_expressions(
    text: str, preset: str | None, args: tuple[str, ...]
) -> None:
    assert canvas.shape(text) == canvas.Shape(preset, args)


@pytest.mark.parametrize(
    ("expr", "preset", "expected"),
    [
        ("", "max", "s"),
        ("a", "max", "max(a, s)"),
        ("max(a, b)", "max", "max(a, b, s)"),
        ("a + b", "sum", "a + b + s"),
        ("a * b", "product", "a * b * s"),
        ("min(a, s)", "min", "min(a, s)"),
    ],
)
def test_connect_writes_or_extends_a_preset(expr: str, preset: str, expected: str) -> None:
    data = _data(s=U, z={"type": "output", "expr": expr})
    assert canvas.connect(data, "s", "z", preset)["nodes"]["z"]["expr"] == expected


@pytest.mark.parametrize(("expr", "preset"), [("max(a, 24)", "max"), ("a + b", "max")])
def test_a_free_or_other_expression_is_never_rewritten(expr: str, preset: str) -> None:
    data = _data(s=U, z={"type": "output", "expr": expr})
    with pytest.raises(InputError) as exc:
        canvas.connect(data, "s", "z", preset)
    assert _code(exc) == "canvas.free_expression"


def test_presets_follow_the_target_and_put_the_current_one_first() -> None:
    data = _data(
        s=U,
        e={"type": "event", "p": 0.1},
        k={"type": "constant", "value": 1},
        u=U,
        v={"type": "event", "p": 0.5},
        z={"type": "output", "expr": "max(s, k)"},
        w={"type": "derived", "expr": "s * 2"},
    )
    assert canvas.presets(data, "s", "z") == ["max", "sum", "min", "product"]
    assert canvas.presets(data, "e", "z") == ["max", "sum", "min", "product", "delay"]
    assert canvas.presets(data, "s", "w") == ["edit"]
    assert canvas.presets(data, "s", "u") == ["param", "corr"]
    assert canvas.presets(data, "s", "v") == ["p", "corr"]
    with pytest.raises(InputError) as exc:
        canvas.presets(data, "s", "k")
    assert _code(exc) == "canvas.no_preset"


def test_self_and_cycles_are_refused() -> None:
    with pytest.raises(InputError) as exc:
        canvas.presets(T2, "a", "a")
    assert _code(exc) == "canvas.self"
    with pytest.raises(InputError) as exc:
        canvas.presets(T2, "ende", "a")  # a feeds pfad1 feeds ende
    assert _code(exc) == "canvas.cycle"


def test_parameter_and_probability_depend_on_the_source() -> None:
    data = _data(s=U, u=U, v={"type": "event", "p": 0.5})
    assert canvas.connect(data, "s", "u", "param", field="mean")["nodes"]["u"]["mean"] == "s"
    scaled = canvas.connect(data, "s", "u", "param", field="sd", value="0.1")
    assert scaled["nodes"]["u"]["sd"] == "s * 0.1"
    assert canvas.connect(data, "s", "v", "p")["nodes"]["v"]["p"] == "s"
    with pytest.raises(InputError) as exc:
        canvas.connect(data, "s", "u", "param", field="nope")
    assert _code(exc) == "canvas.field"


def test_an_event_adds_a_delay_to_any_expression() -> None:
    data = _data(e={"type": "event", "p": 0.2}, z={"type": "output", "expr": "max(a, 24)"})
    out = canvas.connect(data, "e", "z", "delay", value="5")
    assert out["nodes"]["z"]["expr"] == "max(a, 24) + where(e, 5, 0)"
    empty = _data(e={"type": "event", "p": 0.2}, z={"type": "output", "expr": ""})
    assert (
        canvas.connect(empty, "e", "z", "delay", value="5")["nodes"]["z"]["expr"]
        == "where(e, 5, 0)"
    )


def test_connect_does_not_change_its_input() -> None:
    data = _data(s=U, z={"type": "output", "expr": "a"})
    canvas.connect(data, "s", "z", "sum")
    assert data["nodes"]["z"]["expr"] == "a"


@pytest.mark.parametrize(
    ("expr", "source", "expected"),
    [("max(a, b, c)", "b", "max(a, c)"), ("a + b", "a", "b"), ("a", "a", "")],
)
def test_disconnect_removes_one_argument(expr: str, source: str, expected: str) -> None:
    data = _data(z={"type": "derived", "expr": expr})
    assert canvas.disconnect(data, source, "z")["nodes"]["z"]["expr"] == expected


def test_disconnect_never_rewrites_free_expressions_or_parameters() -> None:
    with pytest.raises(InputError) as exc:
        canvas.disconnect(T2, "nacharbeit", "pfad1")  # a + b + where(...)
    assert _code(exc) == "canvas.free_expression"
    assert exc.value.issue.field == "expr"
    data = _data(s=U, u={**U, "mean": "s"})
    with pytest.raises(InputError) as exc:
        canvas.disconnect(data, "s", "u")
    assert exc.value.issue.field == "mean"


def test_correlate_creates_extends_and_sets_a_group() -> None:
    data = _data(a=U, b=U, c=U, e={"type": "event", "p": 0.1})
    one = canvas.correlate(data, "a", "b", 0.5)
    assert one["correlations"] == {
        "a_b": {"nodes": ["a", "b"], "spearman": [[1.0, 0.5], [0.5, 1.0]]}
    }
    two = canvas.correlate(one, "c", "a", 0.3)
    assert two["correlations"]["a_b"]["nodes"] == ["a", "b", "c"]
    assert two["correlations"]["a_b"]["spearman"] == [
        [1.0, 0.5, 0.3],
        [0.5, 1.0, 0.0],
        [0.3, 0.0, 1.0],
    ]
    three = canvas.correlate(two, "b", "a", -0.2)
    assert three["correlations"]["a_b"]["spearman"][0][1] == -0.2
    assert three["correlations"]["a_b"]["spearman"][1][0] == -0.2


def test_correlate_refuses_non_random_nodes_and_two_groups() -> None:
    data = _data(a=U, b=U, c=U, d=U, k={"type": "constant", "value": 1})
    with pytest.raises(InputError) as exc:
        canvas.correlate(data, "a", "k", 0.5)
    assert _code(exc) == "canvas.not_random"
    both = canvas.correlate(canvas.correlate(data, "a", "b", 0.5), "c", "d", 0.5)
    with pytest.raises(InputError) as exc:
        canvas.correlate(both, "a", "c", 0.5)
    assert _code(exc) == "canvas.other_group"


def test_uncorrelate_removes_members_and_empty_groups() -> None:
    data = _data(a=U, b=U, c=U)
    group = canvas.correlate(canvas.correlate(data, "a", "b", 0.5), "a", "c", 0.3)
    left = canvas.uncorrelate(group, "a", "c")
    assert left["correlations"]["a_b"] == {
        "nodes": ["a", "b"],
        "spearman": [[1.0, 0.5], [0.5, 1.0]],
    }
    assert canvas.uncorrelate(left, "b", "a")["correlations"] == {}


def test_links_follow_expressions_parameters_and_groups_on_raw_data() -> None:
    data = _data(
        a=U,
        b={**U, "mean": "a * 2"},
        e={"type": "event", "p": "a"},
        z={"type": "output", "expr": "max(a, b) + nope"},
    )
    data["correlations"] = {"g": {"nodes": ["a", "e"], "spearman": [[1, 0.2], [0.2, 1]]}}
    assert canvas.links(data) == [
        canvas.Link("a", "b", "parameter"),
        canvas.Link("a", "e", "korrelation"),
        canvas.Link("a", "e", "parameter"),
        canvas.Link("a", "z", "ausdruck"),
        canvas.Link("b", "z", "ausdruck"),
    ]


def test_links_match_the_model_graph_on_every_tutorial() -> None:
    from app.model.graph import edges
    from app.model.yaml_io import model_from_yaml

    for name in ("t1_faltung", "t2_terminplan", "t3_bahn", "t4_portfolio", "t5_fusion"):
        text = files.read_text(settings.examples_dir() / f"{name}.yaml")
        found = [(e.source, e.target, e.kind) for e in edges(model_from_yaml(text))]
        assert [(k.source, k.target, k.kind) for k in canvas.links(load_data(text))] == found


def test_two_random_nodes_can_be_correlated_from_the_link_dialog() -> None:
    data = _data(a=U, b=U, e={"type": "event", "p": 0.1}, z={"type": "output", "expr": ""})
    assert canvas.presets(data, "a", "b") == ["param", "corr"]
    assert canvas.presets(data, "a", "e") == ["p", "corr"]
    assert "corr" not in canvas.presets(data, "a", "z")
    out = canvas.connect(data, "a", "b", "corr", value="0,4")
    assert out["correlations"]["a_b"]["spearman"][0][1] == 0.4
    with pytest.raises(InputError) as exc:
        canvas.connect(data, "a", "b", "corr", value="viel")
    assert _code(exc) == "canvas.rho"


@pytest.mark.parametrize(
    ("name", "taken", "expected"),
    [
        ("Vorgang Ä", [], "vorgang_ae"),
        ("Projektende", ["projektende"], "projektende_2"),
        ("3 Tage", [], "k_3_tage"),
        ("max", [], "max_2"),
        ("", ["knoten"], "knoten_2"),
    ],
)
def test_an_id_is_suggested_from_the_name(name: str, taken: list[str], expected: str) -> None:
    assert canvas.suggest_id(name, taken) == expected


def test_place_adds_a_named_node_at_the_drop_point() -> None:
    data = canvas.place(_data(), "dauer", "uncertain", "Dauer", "d", 40.4, 80)
    node = data["nodes"]["dauer"]
    assert (node["type"], node["name"], node["unit"], node["input"]) == (
        "uncertain",
        "Dauer",
        "d",
        "quantiles",
    )
    assert data["layout"]["dauer"] == [40, 80]
    bare = canvas.place(_data(), "k", "constant", "", "", 0, 0)["nodes"]["k"]
    assert "name" not in bare
    assert "unit" not in bare


def test_t2_can_be_rebuilt_on_the_canvas_with_the_same_numbers() -> None:
    from app.engine.simulate import simulate
    from app.model.compile import compile_model
    from app.model.scenarios import effective_model
    from app.model.schema import BASIS
    from app.model.yaml_io import model_from_yaml
    from app.model.yaml_patch import patch

    data: Data = {"schema_version": 1, "model": "t2_terminplan", "settings": T2["settings"]}
    nodes = [
        ("a", "uncertain", "Vorgang A"),
        ("b", "uncertain", "Vorgang B"),
        ("c", "uncertain", "Vorgang C"),
        ("nacharbeit", "event", "Nacharbeit an B"),
        ("pfad1", "derived", "Pfad 1"),
        ("ende", "output", "Projektende"),
    ]
    for i, (node_id, kind, name) in enumerate(nodes):
        data = canvas.place(data, node_id, kind, name, "", 0, 100 * i)
    for node_id, fields in {  # numbers come from the node card
        "a": {"input": "params", "mean": 10, "sd": 2},
        "b": {"input": "params", "mean": 15, "sd": 3},
        "c": {"input": "params", "mean": 24, "sd": 4},
        "nacharbeit": {"p": 0},
        "pfad1": {"track": True},
        "ende": {"target": {"le": 30}},
    }.items():
        data["nodes"][node_id].update(fields)
    for source, target, preset, value in [
        ("a", "pfad1", "sum", ""),
        ("b", "pfad1", "sum", ""),
        ("nacharbeit", "pfad1", "delay", "5"),
        ("pfad1", "ende", "max", ""),
        ("c", "ende", "max", ""),
    ]:
        data = canvas.connect(data, source, target, preset, value=value)
    assert data["nodes"]["pfad1"]["expr"] == T2["nodes"]["pfad1"]["expr"]
    assert data["nodes"]["ende"]["expr"] == T2["nodes"]["ende"]["expr"]
    rebuilt = compile_model(model_from_yaml(patch("schema_version: 1\n", data)))
    t2 = model_from_yaml(files.read_text(settings.examples_dir() / "t2_terminplan.yaml"))
    original = compile_model(effective_model(t2, BASIS))
    mine, theirs = simulate(rebuilt, n=2000), simulate(original, n=2000)
    assert (mine.samples["ende"] == theirs.samples["ende"]).all()
