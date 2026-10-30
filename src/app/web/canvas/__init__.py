"""The Vue Flow canvas as a NiceGUI element (M9, E6).

Props: ``nodes`` and ``edges`` from ``present.canvas_view.view``, ``palette`` [{type, label,
hint}], ``readonly``, ``connectable``. Events: ``move`` {id, x, y}, ``pick`` node ID, ``connect``
{source, target}, ``disconnect`` edge ID, ``drop`` {type, x, y} (palette item placed). The
canvas never changes the model; Python writes the YAML and calls ``draw``.
"""

from pathlib import Path
from typing import Any

from nicegui import ui

LIB = Path(__file__).parent / "lib"


class FlowCanvas(ui.element, component="flow_canvas.js", esm={"vueflow": "lib"}):
    def __init__(
        self,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
        readonly: bool,
        palette: list[dict[str, str]] | None = None,
    ) -> None:
        super().__init__()
        ui.add_css((LIB / "vueflow.css").read_text("utf-8"))
        self._props["readonly"] = readonly
        self._props["connectable"] = True
        self._props["palette"] = palette or []
        self.draw(nodes, edges)

    def draw(self, nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> None:
        """New props in place: zoom and viewport stay."""
        self._props["nodes"] = nodes
        self._props["edges"] = edges
        self.update()

    def fit(self) -> None:
        self.run_method("fit")

    def mode(self, connectable: bool, palette: list[dict[str, str]]) -> None:
        """Structure edits on or off (scenario mode, M9 E3); sent with the next ``draw``."""
        self._props["connectable"] = connectable
        self._props["palette"] = palette
