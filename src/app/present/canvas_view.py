"""What the canvas draws (M9 AP4): Vue Flow nodes and edges from the raw draft, valid or not.

Pure. Node positions come from the ``layout`` block, else from the layered layout; edges are
derived (``canvas.links``) and carry their kind in the ID, so an event on an edge reads back.
"""

from typing import Any, cast

from app.model import canvas, layout
from app.model.graph import EdgeKind
from app.model.yaml_patch import Data
from app.present.structure import type_label

KINDS: tuple[EdgeKind, ...] = ("ausdruck", "parameter", "korrelation")


def _node(
    node_id: str, node: dict[str, Any], pos: tuple[float, float], selected: bool
) -> dict[str, Any]:
    kind = str(node.get("type", ""))
    return {
        "id": node_id,
        "position": {"x": pos[0], "y": pos[1]},
        "data": {"label": str(node.get("name") or node_id), "type": type_label(kind)},
        "class": f"rp-node rp-{kind}" + (" rp-selected" if selected else ""),
        "sourcePosition": "right",
        "targetPosition": "left",
    }


def _edge(link: canvas.Link) -> dict[str, Any]:
    edge: dict[str, Any] = {
        "id": f"{link.kind}:{link.source}->{link.target}",
        "source": link.source,
        "target": link.target,
        "class": f"rp-edge-{link.kind}",
    }
    if link.kind != "korrelation":
        edge["markerEnd"] = "arrowclosed"
    return edge


def view(data: Data, selected: str | None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Nodes in the order of ``nodes`` and edges, as Vue Flow props."""
    nodes = cast(dict[str, dict[str, Any]], data.get("nodes") or {})
    pos = layout.placed(data, auto(data))
    drawn = [_node(n, node, pos[n], n == selected) for n, node in nodes.items()]
    return drawn, [_edge(k) for k in canvas.links(data)]


def auto(data: Data) -> layout.Layered:
    """The layered layout of the draft (correlations do not order the layers)."""
    nodes = cast(dict[str, Any], data.get("nodes") or {})
    directed = [(k.source, k.target) for k in canvas.links(data) if k.kind != "korrelation"]
    return layout.layers(list(nodes), directed)


def edge_of(edge_id: str) -> tuple[str, str, EdgeKind] | None:
    """(source, target, kind) of an edge ID from ``view``; None for anything else."""
    kind, _, pair = edge_id.partition(":")
    source, _, target = pair.partition("->")
    if kind not in KINDS or not source or not target:
        return None
    return source, target, kind
