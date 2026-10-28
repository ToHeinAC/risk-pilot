"""Check model text for the editor: issues as rows, status line, node overview."""

from dataclasses import dataclass

from app.errors import ModelError
from app.messages import render, t
from app.model.compile import CompiledModel, compile_model
from app.model.schema import ConstantNode, EventNode, Model, Node, UncertainNode
from app.model.yaml_io import model_from_yaml


@dataclass(frozen=True)
class IssueRow:
    line: int | None
    node: str | None
    message: str
    excerpt: str


@dataclass(frozen=True)
class NodeRow:
    node: str
    type: str
    name: str
    unit: str
    detail: str


@dataclass(frozen=True)
class CheckResult:
    compiled: CompiledModel | None
    rows: list[IssueRow]
    status: str
    hint: str | None
    node_table: list[NodeRow]


def _detail(node: Node) -> str:
    if isinstance(node, ConstantNode):
        return str(node.value)
    if isinstance(node, UncertainNode):
        params = ", ".join(f"{k}={v}" for k, v in node.params().items())
        return f"{node.dist}({params})"
    if isinstance(node, EventNode):
        return f"p = {node.p}"
    return getattr(node, "expr", "") or ", ".join(o.label for o in getattr(node, "options", []))


def node_table(model: Model) -> list[NodeRow]:
    return [
        NodeRow(node_id, node.type, node.name or node_id, node.unit or "", _detail(node))
        for node_id, node in model.nodes.items()
    ]


def _rows(error: ModelError, lines: list[str]) -> list[IssueRow]:
    rows: list[IssueRow] = []
    for issue in error.issues:
        # A parser error at the end of the stream points one line past the text.
        excerpt = lines[min(issue.line, len(lines)) - 1].strip() if issue.line and lines else ""
        rows.append(IssueRow(issue.line, issue.node_id, render(issue), excerpt))
    return rows


def _problems(count: int) -> str:
    return t("ui.problems_one") if count == 1 else t("ui.problems_many", n=count)


def check_text(text: str) -> CheckResult:
    """Validate and compile; never raises for model problems."""
    if not text.strip():
        return CheckResult(None, [], "", t("ui.model_blank"), [])
    try:
        model = model_from_yaml(text)
        compiled = compile_model(model)
    except ModelError as error:
        if [i.code for i in error.issues] == ["model.empty"]:
            return CheckResult(None, [], "", render(error.issues[0]), [])
        rows = _rows(error, text.splitlines())
        return CheckResult(None, rows, _problems(len(rows)), None, [])
    outputs = sum(1 for n in model.nodes.values() if n.type == "output")
    label = t("ui.outputs_one") if outputs == 1 else t("ui.outputs_many", n=outputs)
    status = t("ui.status_valid", nodes=len(model.nodes), outputs=label)
    return CheckResult(compiled, [], status, None, node_table(model))
