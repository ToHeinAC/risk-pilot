"""References between nodes, topological order and cycle detection."""

import ast
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from graphlib import CycleError, TopologicalSorter
from itertools import combinations
from typing import Literal

from app.expr.parser import ExprIssue, parse_expression
from app.model.schema import DerivedNode, EventNode, Model, Node, OutputNode, UncertainNode


def expression_fields(node: Node) -> Iterator[tuple[str, str]]:
    """Yield (field, expression text) for every expression of a node."""
    if isinstance(node, UncertainNode):
        for name, value in node.params().items():
            if isinstance(value, str):
                yield name, value
    elif isinstance(node, EventNode):
        if isinstance(node.p, str):
            yield "p", node.p
    elif isinstance(node, DerivedNode | OutputNode):
        yield "expr", node.expr


def expression_names(text: str) -> set[str]:
    """Names an expression refers to (calls excluded); empty if it does not parse."""
    try:
        tree = parse_expression(text)
    except ExprIssue:
        return set()  # compile_expr reports the problem with node and field
    called = {id(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)}
    return {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and id(n) not in called}


def collect_refs(model: Model) -> dict[str, set[str]]:
    """Node ID -> IDs of the nodes its expressions reference (syntactically)."""
    ids = set(model.nodes)
    return {
        node_id: {name for _, text in expression_fields(node) for name in expression_names(text)}
        & ids
        for node_id, node in model.nodes.items()
    }


EdgeKind = Literal["ausdruck", "parameter", "korrelation"]


@dataclass(frozen=True, order=True)
class Edge:
    source: str
    target: str
    kind: EdgeKind


def edges(model: Model) -> list[Edge]:
    """Edges of the dependency graph, sorted.

    ``ausdruck``: reference in ``expr``; ``parameter``: reference in a distribution parameter or
    ``p``; ``korrelation``: every pair of a correlation group (undirected, smaller ID first).
    """
    ids = set(model.nodes)
    found: set[Edge] = set()
    for node_id, node in model.nodes.items():
        for field, text in expression_fields(node):
            kind: EdgeKind = "ausdruck" if field == "expr" else "parameter"
            found |= {Edge(ref, node_id, kind) for ref in expression_names(text) & ids}
    for group in model.correlations.values():
        members = sorted(set(group.nodes) & ids)
        found |= {Edge(a, b, "korrelation") for a, b in combinations(members, 2)}
    return sorted(found)


def topo_order(refs: Mapping[str, set[str]]) -> tuple[list[str], list[str] | None]:
    """Deterministic dependency order, or ([], cycle) with the cycle's nodes in order."""
    sorter = TopologicalSorter[str]()
    for node_id in sorted(refs):
        sorter.add(node_id, *sorted(refs[node_id]))
    try:
        sorter.prepare()
    except CycleError as exc:
        cycle: list[str] = list(exc.args[1])
        return [], cycle
    order: list[str] = []
    while sorter.is_active():
        ready = sorted(sorter.get_ready())
        order.extend(ready)
        sorter.done(*ready)
    return order, None
