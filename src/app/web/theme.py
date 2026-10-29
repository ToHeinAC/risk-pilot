"""Design tokens in one place: colours, spacing, type; applied once per page."""

# plotly ships without type stubs; its members are untyped for pyright.
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false, reportMissingTypeStubs=false
from typing import Any

import plotly.graph_objects as go
from nicegui import ui

INK = "#1c2430"
MUTED = "#5b6676"
LINE = "#e3e7ee"
SURFACE = "#ffffff"
CANVAS = "#f5f7fa"
ACCENT = "#2457d6"
ACCENT_SOFT = "#e8eefc"
GOOD = "#1f8a5b"
WARN = "#b7791f"
BAD = "#c2410c"

CSS = f"""
:root {{ --rp-ink:{INK}; --rp-muted:{MUTED}; --rp-line:{LINE}; --rp-accent:{ACCENT};
         --rp-accent-soft:{ACCENT_SOFT}; --rp-canvas:{CANVAS}; }}
body {{ background:{CANVAS}; color:{INK};
        font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
.rp-panel {{ background:{SURFACE}; border:1px solid {LINE}; border-radius:12px;
             box-shadow:none; }}
.rp-kicker {{ font-size:.72rem; letter-spacing:.06em; text-transform:uppercase;
              color:{MUTED}; font-weight:600; }}
.rp-big {{ font-size:2.4rem; line-height:1.1; font-weight:650; font-variant-numeric:tabular-nums; }}
.rp-num {{ font-variant-numeric:tabular-nums; }}
.rp-muted {{ color:{MUTED}; }}
.rp-answer {{ font-size:1.05rem; line-height:1.5; }}
.rp-spark {{ color:{ACCENT}; opacity:.85; }}
.rp-selected td {{ background:{ACCENT_SOFT} !important; }}
.rp-nav .q-item {{ border-radius:8px; margin:2px 8px; }}
.rp-nav .q-item.rp-active {{ background:{ACCENT_SOFT}; color:{ACCENT}; font-weight:600; }}
"""

PLOT: dict[str, Any] = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "system-ui, sans-serif", "size": 12, "color": INK},
    "colorway": [ACCENT, "#e07b39", GOOD, "#8e5bd6"],
    "xaxis": {"gridcolor": LINE, "zeroline": False},
    "yaxis": {"gridcolor": LINE, "zeroline": False},
}


def apply() -> None:
    ui.colors(primary=ACCENT, positive=GOOD, warning=WARN, negative=BAD)
    ui.add_css(CSS)
    ui.query("body").classes("rp")


def plot(fig: go.Figure, height: int) -> ui.plotly:
    """A chart in the app's look: tokens above, no plotly toolbar."""
    fig.update_layout(PLOT, height=height)
    options: dict[str, Any] = fig.to_plotly_json()
    options["config"] = {"displayModeBar": False, "responsive": True}
    return ui.plotly(options).classes("w-full")
