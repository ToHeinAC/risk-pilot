"""Figures, sentences and table rows of the structure analyses (M4)."""

# plotly ships without type stubs; its members are untyped for pyright.
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false, reportMissingTypeStubs=false
import math
from collections.abc import Mapping, Sequence

import networkx as nx
import plotly.graph_objects as go
from plotly.colors import sample_colorscale

from app.analysis.criticality import Constellation, Criticality
from app.analysis.riskmatrix import RiskRow
from app.analysis.sensitivity import RankCorrelation
from app.analysis.stats import Proportion
from app.analysis.sweep import Sweep
from app.analysis.tornado import Tornado
from app.messages import t
from app.model.graph import Edge
from app.model.schema import ConstantNode, EventNode, Model, UncertainNode
from app.present.figures import layout
from app.present.text import number, percent
from app.present.validation import node_table

SYMBOLS = {
    "uncertain": "circle",
    "event": "diamond",
    "constant": "square",
    "choice": "triangle-up",
    "derived": "circle-dot",
    "output": "star",
}
DASHES = {"ausdruck": "solid", "parameter": "dash", "korrelation": "dot"}
SCALE = "YlOrRd"
NO_VALUE = "#c8c8c8"
FADED = 0.25


def type_label(node_type: str) -> str:
    return t(f"type.{node_type}")


def missing_why(model: Model) -> dict[str, float]:
    """1 where an uncertain, event or constant node lacks a ``why``, else 0."""
    return {
        node_id: float(node.why is None)
        for node_id, node in model.nodes.items()
        if isinstance(node, UncertainNode | EventNode | ConstantNode)
    }


def _digraph(model: Model, edges: Sequence[Edge]) -> "nx.DiGraph[str]":
    graph: nx.DiGraph[str] = nx.DiGraph()
    graph.add_nodes_from(model.nodes)
    graph.add_edges_from((e.source, e.target) for e in edges if e.kind != "korrelation")
    return graph


def positions(model: Model, edges: Sequence[Edge]) -> dict[str, tuple[float, float]]:
    """Layered layout: inputs on the left, each node one layer right of its latest input."""
    pos: dict[str, tuple[float, float]] = {}
    for x, layer in enumerate(nx.topological_generations(_digraph(model, edges))):
        for i, node in enumerate(sorted(layer)):
            pos[node] = (float(x), (len(layer) - 1) / 2 - i)
    return pos


def _edge_traces(edges: Sequence[Edge], pos: Mapping[str, tuple[float, float]]) -> list[go.Scatter]:
    traces: list[go.Scatter] = []
    for kind, dash in DASHES.items():
        xs: list[float | None] = []
        ys: list[float | None] = []
        for e in (e for e in edges if e.kind == kind):
            xs += [pos[e.source][0], pos[e.target][0], None]
            ys += [pos[e.source][1], pos[e.target][1], None]
        if xs:
            traces.append(
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="lines",
                    name=t(f"analysis.edge_{kind}"),
                    line={"dash": dash, "color": "#888", "width": 1},
                    hoverinfo="skip",
                )
            )
    return traces


def _color(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return NO_VALUE
    return str(sample_colorscale(SCALE, [min(max(value, 0.0), 1.0)])[0])


def graph_figure(
    model: Model,
    edges: Sequence[Edge],
    colors: Mapping[str, float],
    color_title: str,
    output: str,
) -> go.Figure:
    """Dependency graph: symbol per node type, line style per edge kind, colour from ``colors``
    (values in [0, 1]); nodes without a path to ``output`` are drawn pale."""
    pos = positions(model, edges)
    on_path = nx.ancestors(_digraph(model, edges), output) | {output}
    fig = go.Figure(_edge_traces(edges, pos))
    rows = {row.node: row for row in node_table(model)}
    for node_type, symbol in SYMBOLS.items():
        ids = [i for i, node in model.nodes.items() if node.type == node_type]
        if not ids:
            continue
        hover = [
            f"{rows[i].name} ({i})<br>{rows[i].unit}<br>{rows[i].detail}<br>"
            f"{color_title}: {number(colors[i]) if i in colors else '–'}"
            for i in ids
        ]
        fig.add_trace(
            go.Scatter(
                x=[pos[i][0] for i in ids],
                y=[pos[i][1] for i in ids],
                mode="markers+text",
                name=type_label(node_type),
                text=[rows[i].name for i in ids],
                textposition="top center",
                customdata=ids,
                hovertext=hover,
                hoverinfo="text",
                marker={
                    "symbol": symbol,
                    "size": 18,
                    "color": [_color(colors.get(i)) for i in ids],
                    "opacity": [1.0 if i in on_path else FADED for i in ids],
                    "line": {"width": 1, "color": "#444"},
                },
            )
        )
    fig.add_trace(_colorbar(color_title))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(legend={"orientation": "h", "y": -0.05, "yanchor": "top"})
    return layout(fig, "", "")


def _colorbar(title: str) -> go.Scatter:
    """An invisible trace that only carries the colour scale's legend."""
    return go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        showlegend=False,
        marker={
            "colorscale": SCALE,
            "cmin": 0,
            "cmax": 1,
            "color": [0],
            "showscale": True,
            "colorbar": {"title": {"text": title}},
        },
    )


def _pct_interval(p: Proportion) -> str:
    return f"{percent(p.p)} ({number(p.lo * 100)} … {number(p.hi * 100)} %)"


def criticality_sentence(name: str, p: Proportion) -> str:
    return t(
        "analysis.crit_sentence",
        name=name,
        p=percent(p.p),
        lo=number(p.lo * 100),
        hi=number(p.hi * 100),
    )


def criticality_rows(crit: Criticality, names: Mapping[str, str]) -> list[tuple[str, str]]:
    return [(names[node], _pct_interval(p)) for node, p in crit.indices]


def _constellation_label(c: Constellation, names: Mapping[str, str]) -> str:
    if c.rest:
        return t("analysis.constellation_rest", n=c.rest)
    if not c.nodes:
        return t("analysis.constellation_none")
    return ", ".join(names[node] for node in c.nodes)


def constellation_rows(crit: Criticality, names: Mapping[str, str]) -> list[tuple[str, str]]:
    return [(_constellation_label(c, names), _pct_interval(c.share)) for c in crit.constellations]


def criticality_figure(crit: Criticality, names: Mapping[str, str]) -> go.Figure:
    rows = list(reversed(crit.indices))
    fig = go.Figure(
        go.Bar(
            x=[p.p for _, p in rows],
            y=[names[node] for node, _ in rows],
            orientation="h",
            error_x={
                "type": "data",
                "symmetric": False,
                "array": [p.hi - p.p for _, p in rows],
                "arrayminus": [p.p - p.lo for _, p in rows],
            },
        )
    )
    fig.update_xaxes(range=[0, 1], tickformat=".0%")
    return layout(fig, t("analysis.crit_axis"), "")


def tornado_rows(tornado: Tornado, names: Mapping[str, str]) -> list[tuple[str, ...]]:
    return [
        (
            names[bar.node],
            number(bar.low_value),
            number(bar.high_value),
            _metric_text(tornado, bar.low),
            _metric_text(tornado, bar.high),
            _metric_text(tornado, bar.swing, signed=True),
        )
        for bar in tornado.bars
    ]


def tornado_base(tornado: Tornado) -> str:
    """The metric of the unchanged model, e.g. for the caption."""
    return _metric_text(tornado, tornado.base)


def _metric_text(tornado: Tornado, value: float, signed: bool = False) -> str:
    text = number(value * 100) + " %" if tornado.metric == "target" else number(value)
    return f"+{text}" if signed and value > 0 else text


def tornado_figure(tornado: Tornado, names: Mapping[str, str]) -> go.Figure:
    bars = list(reversed(tornado.bars))
    labels = [names[bar.node] for bar in bars]
    fig = go.Figure()
    for label, values in (
        (t("analysis.at_p10"), [bar.low for bar in bars]),
        (t("analysis.at_p90"), [bar.high for bar in bars]),
    ):
        fig.add_trace(
            go.Bar(
                x=[v - tornado.base for v in values],
                y=labels,
                base=tornado.base,
                orientation="h",
                name=label,
            )
        )
    fig.update_layout(barmode="overlay")
    return layout(fig, t(f"analysis.metric_{tornado.metric}"), "")


def sweep_series(sweep: Sweep, metric: str) -> list[tuple[float, float, float, float]]:
    """(value, estimate, lower, upper) per point; metric: mean|median|quantile|target|share."""
    series: list[tuple[float, float, float, float]] = []
    for point in sweep.points:
        s = point.summary
        if metric == "mean" and s.mean is not None:
            half = 1.96 * s.se
            series.append((point.value, s.mean, s.mean - half, s.mean + half))
        elif metric in ("median", "quantile") and s.quantiles:
            q = s.quantiles[0 if metric == "median" else -1]
            series.append((point.value, q.value, q.lo, q.hi))
        elif metric in ("target", "share"):
            prop = s.target if metric == "target" else s.share
            if prop is not None:
                series.append((point.value, prop.p, prop.lo, prop.hi))
    return series


def sweep_rows(
    series: list[tuple[float, float, float, float]], share: bool
) -> list[tuple[str, ...]]:
    scale, suffix = (100, " %") if share else (1, "")
    return [
        (
            number(x),
            f"{number(y * scale)}{suffix}",
            f"{number(lo * scale)} … {number(hi * scale)}{suffix}",
        )
        for x, y, lo, hi in series
    ]


def sweep_figure(
    series: list[tuple[float, float, float, float]], x_title: str, y_title: str
) -> go.Figure:
    fig = go.Figure(
        go.Scatter(
            x=[x for x, _, _, _ in series],
            y=[y for _, y, _, _ in series],
            mode="lines+markers",
            error_y={
                "type": "data",
                "symmetric": False,
                "array": [hi - y for _, y, _, hi in series],
                "arrayminus": [y - lo for _, y, lo, _ in series],
            },
        )
    )
    return layout(fig, x_title, y_title)


def rho_rows(rows: list[RankCorrelation], names: Mapping[str, str]) -> list[tuple[str, str, str]]:
    return [
        (names[r.node], number(r.rho), f"{number(r.lo)} … {number(r.hi)}")
        if r.rho is not None
        else (names[r.node], t("analysis.undefined"), "–")
        for r in rows
    ]


def risk_rows(
    rows: list[RiskRow], names: Mapping[str, str], unit: str | None
) -> list[tuple[str, ...]]:
    u = f" {unit}" if unit else ""
    return [
        (
            names[r.node],
            _pct_interval(r.p),
            f"{number(r.diff.value)}{u} ({number(r.diff.lo)} … {number(r.diff.hi)}{u})"
            if r.diff is not None
            else t("analysis.risk_undefined"),
        )
        for r in rows
    ]


def risk_figure(rows: list[RiskRow], names: Mapping[str, str], unit: str | None) -> go.Figure:
    """p̂ against the conditional difference; events without a defined difference at y = 0."""
    defined = [r for r in rows if r.diff is not None]
    undefined = [r for r in rows if r.diff is None]
    fig = go.Figure()
    if defined:
        fig.add_trace(
            go.Scatter(
                x=[r.p.p for r in defined],
                y=[r.diff.value for r in defined if r.diff is not None],
                mode="markers+text",
                text=[names[r.node] for r in defined],
                textposition="top right",
                name=t("analysis.tab_risk"),
                error_x={
                    "type": "data",
                    "symmetric": False,
                    "array": [r.p.hi - r.p.p for r in defined],
                    "arrayminus": [r.p.p - r.p.lo for r in defined],
                },
                error_y={
                    "type": "data",
                    "symmetric": False,
                    "array": [r.diff.hi - r.diff.value for r in defined if r.diff is not None],
                    "arrayminus": [r.diff.value - r.diff.lo for r in defined if r.diff is not None],
                },
            )
        )
    if undefined:
        fig.add_trace(
            go.Scatter(
                x=[r.p.p for r in undefined],
                y=[0.0] * len(undefined),
                mode="markers+text",
                marker={"symbol": "x-open", "size": 12},
                text=[f"{names[r.node]} ({t('analysis.risk_undefined')})" for r in undefined],
                textposition="bottom right",
                name=t("analysis.risk_undefined"),
            )
        )
    fig.update_xaxes(range=[-0.05, 1.05], tickformat=".0%")
    y_title = t("analysis.risk_y") + (f" ({unit})" if unit else "")
    return layout(fig, t("analysis.risk_x"), y_title)
