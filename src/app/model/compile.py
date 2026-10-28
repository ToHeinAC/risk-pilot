"""Validate a model and compile it into an immutable, executable form."""

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from difflib import get_close_matches

import numpy as np
from numpy.typing import NDArray

from app.dists.base import Family, ParamSpec, fill_defaults
from app.dists.registry import families, get_family
from app.errors import Issue, ModelError, Notice
from app.expr.evaluate import Const, Expr, Table
from app.expr.parser import BOOL, NUM, ExprIssue, VarType, choice_type, compile_expr
from app.model.graph import collect_refs, topo_order
from app.model.schema import (
    Bounds,
    ChoiceNode,
    ConstantNode,
    EventNode,
    Model,
    Node,
    OutputNode,
    ParamValue,
    Target,
    UncertainNode,
)


@dataclass(frozen=True)
class CConstant:
    value: float


@dataclass(frozen=True)
class CUncertain:
    family: Family
    mode: str
    params: Mapping[str, Expr]
    literal: bool


@dataclass(frozen=True)
class CEvent:
    p: Expr
    literal: bool


@dataclass(frozen=True)
class CChoice:
    cum: NDArray[np.float64]


@dataclass(frozen=True)
class CExpr:
    expr: Expr


Compiled = CConstant | CUncertain | CEvent | CChoice | CExpr


@dataclass(frozen=True)
class CNode:
    id: str
    type: str
    vtype: VarType
    body: Compiled
    bounds: Bounds | None
    target: Target | None
    tracked: bool


@dataclass(frozen=True)
class CompiledModel:
    model: Model
    order: tuple[str, ...]
    nodes: Mapping[str, CNode]
    model_hash: str
    canonical: Mapping[str, Mapping[str, object]]
    notices: tuple[Notice, ...]
    refs: Mapping[str, frozenset[str]]


def model_hash(model: Model) -> str:
    """SHA-256 over the canonical JSON of the validated model."""
    text = json.dumps(model.model_dump(mode="json"), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


_LABELS = ("name", "description", "why", "tags")


def content_hash(model: Model) -> str:
    """SHA-256 over what determines the numbers: without model ID, title and display labels."""
    data = model.model_dump(mode="json", exclude={"model", "title", "description"})
    for node in data["nodes"].values():
        for key in _LABELS:
            node.pop(key, None)
    text = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class _Fail(Exception):
    """Collected issues of one node; compilation of that node stops."""

    def __init__(self, issues: list[Issue]) -> None:
        super().__init__()
        self.issues = issues


@dataclass
class _Compiler:
    env: dict[str, VarType] = field(default_factory=dict[str, VarType])
    canonical: dict[str, dict[str, object]] = field(default_factory=dict[str, dict[str, object]])
    notices: list[Notice] = field(default_factory=list[Notice])

    def expression(self, node_id: str, field_name: str, text: str) -> tuple[Expr, VarType]:
        try:
            compiled = compile_expr(text, self.env)
        except ExprIssue as exc:
            raise _Fail([Issue(exc.code, node_id, field_name, params=exc.params)]) from exc
        return compiled.node, compiled.type

    def numeric(self, node_id: str, field_name: str, text: str) -> Expr:
        expr, kind = self.expression(node_id, field_name, text)
        if kind.kind == "choice":
            issue = Issue("expr.choice_usage", node_id, field_name, params={"choice": kind.node})
            raise _Fail([issue])
        return expr

    def node(self, node_id: str, node: Node) -> tuple[Compiled, VarType]:
        if isinstance(node, ConstantNode):
            return CConstant(node.value), NUM
        if isinstance(node, UncertainNode):
            return self.uncertain(node_id, node), NUM
        if isinstance(node, EventNode):
            return self.event(node_id, node), BOOL
        if isinstance(node, ChoiceNode):
            weights = np.array([o.weight for o in node.options], dtype=np.float64)
            cum = weights.cumsum() / weights.sum()
            cum[-1] = 1.0
            return CChoice(cum), choice_type(node_id, tuple(o.label for o in node.options))
        expr, kind = self.expression(node_id, "expr", node.expr)
        if isinstance(node, OutputNode) and kind.kind == "choice":
            raise _Fail([Issue("expr.choice_usage", node_id, "expr", params={"choice": kind.node})])
        return CExpr(expr), kind

    def event(self, node_id: str, node: EventNode) -> CEvent:
        if isinstance(node.p, str):
            return CEvent(self.numeric(node_id, "p", node.p), literal=False)
        if not 0 <= node.p <= 1:
            issue = Issue(
                "param.invalid", node_id, "p", params={"value": node.p, "rule": "0 ≤ p ≤ 1"}
            )
            raise _Fail([issue])
        return CEvent(Const(node.p), literal=True)

    def uncertain(self, node_id: str, node: UncertainNode) -> CUncertain:
        family = get_family(node.dist)
        if family is None:
            known = get_close_matches(node.dist, families(), n=3) or families()
            raise _Fail(
                [Issue("dist.unknown", node_id, "dist", params={"dist": node.dist, "known": known})]
            )
        if node.input not in family.modes:
            params = {"dist": node.dist, "mode": node.input, "modes": list(family.modes)}
            raise _Fail([Issue("dist.mode_unknown", node_id, "input", params=params)])
        specs = family.modes[node.input]
        given = node.params()
        _check_names(node_id, node, specs, given)
        exprs = self.param_exprs(node_id, specs, given)
        literal = all(isinstance(e, Const | Table) for e in exprs.values())
        self.check_literals(node_id, node, family, exprs, given)
        if literal:
            self.record_canonical(node_id, node, family, exprs, given)
        return CUncertain(family, node.input, exprs, literal)

    def param_exprs(
        self, node_id: str, specs: tuple[ParamSpec, ...], given: Mapping[str, ParamValue]
    ) -> dict[str, Expr]:
        exprs: dict[str, Expr] = {}
        issues: list[Issue] = []
        for spec in specs:
            value = given.get(spec.name, spec.default)
            if value is None:
                continue
            try:
                exprs[spec.name] = self.param_expr(node_id, spec, value)
            except _Fail as fail:
                issues.extend(fail.issues)
        if issues:
            raise _Fail(issues)
        return exprs

    def param_expr(self, node_id: str, spec: ParamSpec, value: ParamValue) -> Expr:
        if spec.is_list != isinstance(value, list) or not _numbers_only(value):
            rule = "eine Zahlenliste" if spec.is_list else "eine Zahl oder ein Ausdruck"
            raise _Fail(
                [Issue("param.invalid", node_id, spec.name, params={"value": value, "rule": rule})]
            )
        if isinstance(value, list):
            return Table(tuple(float(v) for v in value))
        if isinstance(value, str):
            return self.numeric(node_id, spec.name, value)
        return Const(float(value))

    def check_literals(
        self,
        node_id: str,
        node: UncertainNode,
        family: Family,
        exprs: Mapping[str, Expr],
        given: Mapping[str, ParamValue],
    ) -> None:
        arrays = {k: _literal_array(e) for k, e in exprs.items()}
        with np.errstate(all="ignore"):
            violations = family.check(node.input, fill_defaults(family, node.input, arrays))
        issues = [
            Issue(
                "param.invalid",
                node_id,
                v.field,
                params={"value": given.get(v.field), "rule": v.rule},
            )
            for v in violations
            if v.mask.any()
        ]
        if issues:
            raise _Fail(_unique_fields(issues))

    def record_canonical(
        self,
        node_id: str,
        node: UncertainNode,
        family: Family,
        exprs: Mapping[str, Expr],
        given: Mapping[str, ParamValue],
    ) -> None:
        arrays = {k: _literal_array(e) for k, e in exprs.items()}
        canonical = family.to_canonical(node.input, arrays)
        self.canonical[node_id] = {
            "dist": family.name,
            "input": node.input,
            "given": dict(given),
            "canonical": {k: v.tolist() for k, v in canonical.items()},
        }
        if family.name == "uniform" and float(arrays["low"]) == float(arrays["high"]):
            self.notices.append(
                Notice("uniform.degenerate", node_id, params={"value": float(arrays["low"])})
            )


def _numbers_only(value: ParamValue) -> bool:
    """List parameters hold numbers only; booleans are not silently read as 0/1."""
    if not isinstance(value, list):
        return True
    items: list[object] = list(value)
    return all(isinstance(v, int | float) and not isinstance(v, bool) for v in items)


def _literal_array(expr: Expr) -> NDArray[np.float64]:
    """Literal values as arrays; expression parameters become NaN (never a violation)."""
    if isinstance(expr, Const | Table):
        return np.asarray(expr.evaluate({}), dtype=np.float64)
    return np.asarray(np.nan)


def _unique_fields(issues: list[Issue]) -> list[Issue]:
    seen: set[str | None] = set()
    unique: list[Issue] = []
    for issue in issues:
        if issue.field not in seen:
            seen.add(issue.field)
            unique.append(issue)
    return unique


def _check_names(
    node_id: str, node: UncertainNode, specs: tuple[ParamSpec, ...], given: Mapping[str, ParamValue]
) -> None:
    allowed = [s.name for s in specs]
    base = {"dist": node.dist, "mode": node.input}
    issues = [
        Issue("param.missing", node_id, s.name, params=base)
        for s in specs
        if s.default is None and s.name not in given
    ]
    issues += [
        Issue("param.unknown", node_id, name, params={**base, "allowed": allowed})
        for name in given
        if name not in allowed
    ]
    if issues:
        raise _Fail(issues)


def _structure_issues(model: Model) -> list[Issue]:
    if not any(isinstance(n, OutputNode) for n in model.nodes.values()):
        return [Issue("model.no_output")]
    return []


def compile_model(model: Model) -> CompiledModel:
    """Check the whole model and compile it; raise ModelError with every issue found."""
    if not model.nodes:
        raise ModelError([Issue("model.empty")])
    refs = collect_refs(model)
    order, cycle = topo_order(refs)
    if cycle is not None:
        raise ModelError([Issue("graph.cycle", params={"cycle": cycle}), *_structure_issues(model)])
    compiler = _Compiler()
    issues: list[Issue] = []
    failed: set[str] = set()
    nodes: dict[str, CNode] = {}
    for node_id in order:
        if refs[node_id] & failed:
            failed.add(node_id)
            continue
        node = model.nodes[node_id]
        try:
            body, vtype = compiler.node(node_id, node)
        except _Fail as fail:
            issues.extend(fail.issues)
            failed.add(node_id)
            continue
        compiler.env[node_id] = vtype
        target = node.target if isinstance(node, OutputNode) else None
        tracked = node.track or isinstance(node, OutputNode)
        nodes[node_id] = CNode(node_id, node.type, vtype, body, node.bounds, target, tracked)
    issues += _structure_issues(model)
    if issues:
        raise ModelError(issues)
    return CompiledModel(
        model,
        tuple(order),
        nodes,
        model_hash(model),
        compiler.canonical,
        tuple(compiler.notices),
        {k: frozenset(v) for k, v in refs.items()},
    )
