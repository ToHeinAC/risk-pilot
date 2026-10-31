"""The Gantt figure of a schedule: bars at the median, the finish spread P10–P90 as a whisker,
milestones as diamonds, one arrow from each precondition's end to the start it allows."""

# plotly ships without type stubs; its members are untyped for pyright.
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false, reportMissingTypeStubs=false

import plotly.graph_objects as go

from app.analysis.schedule import Bar
from app.messages import t
from app.present.figures import layout
from app.present.text import number

COLORS = {"activity": "#2457d6", "block": "#b7791f", "milestone": "#1f8a5b"}


def _hover(bar: Bar, unit: str) -> str:
    params = {
        "start": number(bar.start),
        "finish": number(bar.finish),
        "lo": number(bar.lo),
        "hi": number(bar.hi),
        "unit": unit,
    }
    return t(f"gantt.hover_{'point' if bar.kind == 'milestone' else 'bar'}", **params)


def _spans(rows: list[Bar], unit: str) -> list[go.Bar]:
    traces: list[go.Bar] = []
    for kind in ("activity", "block"):
        part = [(i, r) for i, r in enumerate(rows) if r.kind == kind]
        if not part:
            continue
        traces.append(
            go.Bar(
                name=t(f"gantt.{kind}"),
                y=[i for i, _ in part],
                x=[r.finish - r.start for _, r in part],
                base=[r.start for _, r in part],
                orientation="h",
                marker={"color": COLORS[kind]},
                hovertext=[_hover(r, unit) for _, r in part],
                hoverinfo="text",
                width=0.55,
            )
        )
    return traces


def _ends(rows: list[Bar], unit: str) -> go.Scatter:
    """Diamonds for milestones, an invisible point for bars; both carry the finish spread."""
    return go.Scatter(
        name=t("gantt.milestone"),
        x=[r.finish for r in rows],
        y=list(range(len(rows))),
        mode="markers",
        marker={
            "symbol": "diamond",
            "size": [14 if r.kind == "milestone" else 1 for r in rows],
            "color": COLORS["milestone"],
        },
        error_x={
            "type": "data",
            "symmetric": False,
            "array": [r.hi - r.finish for r in rows],
            "arrayminus": [r.finish - r.lo for r in rows],
            "color": "#5b6676",
            "thickness": 1.2,
            "width": 4,
        },
        hovertext=[_hover(r, unit) for r in rows],
        hoverinfo="text",
    )


def figure(rows: list[Bar], unit: str | None) -> go.Figure:
    fig = go.Figure([*_spans(rows, unit or ""), _ends(rows, unit or "")])
    row_of = {r.node: i for i, r in enumerate(rows)}
    for i, r in enumerate(rows):
        for before in r.after:
            j = row_of[before]
            fig.add_annotation(
                x=r.start, y=i, ax=rows[j].finish, ay=j, xref="x", yref="y", axref="x",
                ayref="y", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1,
                arrowcolor="#8a94a3", standoff=2, text="",
            )  # fmt: skip
    fig.update_yaxes(
        tickvals=list(range(len(rows))),
        ticktext=[r.label for r in rows],
        autorange="reversed",
        ticksuffix="  ",
    )
    fig.update_layout(barmode="overlay", legend={"orientation": "h", "y": -0.15})
    axis = t("fig.value_unit", unit=unit) if unit else t("fig.value")
    return layout(fig, axis, "")


def height(rows: list[Bar]) -> int:
    return 140 + 30 * len(rows)
