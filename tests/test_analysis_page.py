"""Figures and texts of the analysis page, without Streamlit (M4 AK 1-6)."""

from pathlib import Path
from typing import Any

from app.analysis.criticality import criticality
from app.analysis.riskmatrix import risk_matrix
from app.engine.simulate import simulate
from app.model.compile import compile_model
from app.model.graph import edges
from app.model.scenarios import effective_model
from app.model.yaml_io import model_from_yaml
from app.present import structure


def data(fig: object) -> list[Any]:
    """Traces of a plotly figure (plotly has no type stubs)."""
    return list(getattr(fig, "data"))  # noqa: B009 - untyped plotly


T2 = Path(__file__).resolve().parent.parent / "examples" / "t2_terminplan.yaml"
MIXED = (
    "schema_version: 1\nmodel: m\nnodes:\n"
    "  k: {type: constant, value: 2, why: 'Vertrag'}\n"
    "  u: {type: uncertain, dist: normal, mean: 'k', sd: 1}\n"
    "  e: {type: event, p: 0.5, why: 'Erfahrung'}\n"
    "  c: {type: choice, options: [{label: x, weight: 1}, {label: z, weight: 1}]}\n"
    "  d: {type: derived, expr: 'u + where(c == \"x\", 1, 0)'}\n"
    "  lonely: {type: constant, value: 1}\n"
    "  y: {type: output, expr: 'd + e'}\n"
)


def test_graph_symbols_per_type_and_line_styles() -> None:
    m = model_from_yaml(MIXED)
    fig = structure.graph_figure(m, edges(m), structure.missing_why(m), "Begründung fehlt", "y")
    symbols = {tr.name: tr.marker.symbol for tr in data(fig) if tr.mode == "markers+text"}
    assert set(symbols.values()) == set(structure.SYMBOLS.values())
    dashes = {tr.line.dash for tr in data(fig) if tr.mode == "lines"}
    assert dashes == {"solid", "dash"}


def test_missing_why_colouring_and_faded_nodes() -> None:
    m = model_from_yaml(MIXED)
    assert structure.missing_why(m) == {"k": 0.0, "u": 1.0, "e": 0.0, "lonely": 1.0}
    fig = structure.graph_figure(m, edges(m), structure.missing_why(m), "Begründung fehlt", "y")
    constants = next(tr for tr in data(fig) if tr.name == structure.type_label("constant"))
    opacity = dict(zip(constants.customdata, constants.marker.opacity, strict=True))
    assert opacity["lonely"] < opacity["k"]


T5 = T2.with_name("t5_fusion.yaml")


def test_graph_labels_fit_inside_the_plot() -> None:
    m = model_from_yaml(T5.read_text("utf-8"))
    fig = structure.graph_figure(m, edges(m), {}, "Sensitivität", "kommerziell")
    nodes = [tr for tr in data(fig) if tr.mode == "markers+text"]
    xs = [x for tr in nodes for x in tr.x]
    frame: Any = getattr(fig, "layout")  # noqa: B009 - untyped plotly
    lo, hi = frame.xaxis.range
    assert lo <= min(xs) - 0.5
    assert hi >= max(xs) + 0.5
    labels = [label for tr in nodes for label in tr.text]
    assert all(len(line) <= structure.LABEL_WIDTH for s in labels for line in s.split("<br>"))
    assert frame.height >= 9 * 60  # nine nodes in the first layer


def test_criticality_sentence_and_risk_figure() -> None:
    model = model_from_yaml(T2.read_text("utf-8"))
    c = compile_model(effective_model(model, "nacharbeit"))
    samples = simulate(c, n=5000, seed=0, keep="all").samples
    crit = criticality(c, samples, "ende")
    text = structure.criticality_sentence("Vorgang B", crit.index("b"))
    assert text.startswith("Im Modell liegt Vorgang B in ")
    assert "der Iterationen auf dem entscheidenden Pfad" in text
    rows = risk_matrix(c, samples, "ende")
    fig = structure.risk_figure(rows, {"nacharbeit": "Nacharbeit an B"}, "d")
    assert data(fig)[0].text[0] == "Nacharbeit an B"


def test_risk_figure_marks_undefined_difference() -> None:
    c = compile_model(effective_model(model_from_yaml(T2.read_text("utf-8")), "basis"))
    rows = risk_matrix(c, simulate(c, n=500, seed=0, keep="all").samples, "ende")
    (trace,) = data(structure.risk_figure(rows, {"nacharbeit": "Nacharbeit"}, "d"))
    assert trace.text[0] == "Nacharbeit (y nicht bestimmbar)"
    assert list(trace.y) == [0.0]


def test_graph_legend_does_not_cover_colour_scale() -> None:
    m = model_from_yaml(MIXED)
    fig = structure.graph_figure(m, edges(m), structure.missing_why(m), "Begründung fehlt", "y")
    assert getattr(fig, "layout").legend.orientation == "h"  # noqa: B009 - untyped plotly
