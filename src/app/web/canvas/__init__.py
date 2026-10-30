"""The Vue Flow canvas as a NiceGUI element (M9, E6).

Props: ``nodes`` and ``edges`` from ``present.canvas_view.view``, ``readonly``, ``connectable``.
Events: ``move`` {id, x, y}, ``pick`` node ID, ``connect`` {source, target}, ``disconnect``
edge ID. The canvas never changes the model; Python writes the YAML and calls ``draw``.
"""

from pathlib import Path
from typing import Any

from nicegui import ui

LIB = Path(__file__).parent / "lib"


class FlowCanvas(ui.element, component="flow_canvas.js", esm={"vueflow": "lib"}):
    def __init__(
        self, nodes: list[dict[str, Any]], edges: list[dict[str, Any]], readonly: bool
    ) -> None:
        super().__init__()
        ui.add_css((LIB / "vueflow.css").read_text("utf-8"))
        self._props["readonly"] = readonly
        self._props["connectable"] = False  # connecting comes with the link dialog (AP5)
        self.draw(nodes, edges)

    def draw(self, nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> None:
        """New props in place: zoom and viewport stay."""
        self._props["nodes"] = nodes
        self._props["edges"] = edges
        self.update()

    def fit(self) -> None:
        self.run_method("fit")
