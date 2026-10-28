"""Parse expression text against an AST whitelist, type-check it, build an Expr tree."""

import ast
import difflib
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from itertools import pairwise
from typing import Any, Literal

from app.expr.evaluate import (
    Arith,
    Call,
    ChoiceEq,
    Cmp,
    Const,
    Expr,
    Extremum,
    Interp,
    Logic,
    Neg,
    Not,
    Var,
    Where,
)
from app.expr.functions import get_function

MAX_LENGTH = 1000
MAX_DEPTH = 32
MAX_NODES = 500
_ARITH_OPS = frozenset({"Add", "Sub", "Mult", "Div", "Pow", "Mod"})
_COMPARE_OPS = frozenset({"Lt", "LtE", "Gt", "GtE", "Eq", "NotEq"})
_KIND_DE = {"num": "Zahl", "bool": "Wahrheitswert", "choice": "Auswahl"}


@dataclass(frozen=True)
class VarType:
    kind: Literal["num", "bool", "choice"]
    node: str | None = None
    labels: tuple[str, ...] = ()


NUM = VarType("num")
BOOL = VarType("bool")


def choice_type(node: str, labels: tuple[str, ...]) -> VarType:
    return VarType("choice", node, labels)


class ExprIssue(Exception):
    """A problem in one expression; the compiler adds node ID and field."""

    def __init__(self, code: str, **params: object) -> None:
        super().__init__(code)
        self.code = code
        self.params = params


@dataclass(frozen=True)
class CompiledExpr:
    node: Expr
    type: VarType
    refs: frozenset[str]


Typed = tuple[Expr, VarType]


def _forbidden(construct: str, hint: str = "") -> ExprIssue:
    return ExprIssue("expr.forbidden", construct=construct, hint=hint)


def _depth(node: ast.AST) -> int:
    """Nesting depth, computed iteratively so deep trees cannot exhaust the call stack."""
    deepest, stack = 0, [(node, 1)]
    while stack:
        current, depth = stack.pop()
        deepest = max(deepest, depth)
        stack.extend((child, depth + 1) for child in ast.iter_child_nodes(current))
    return deepest


def parse_expression(text: str) -> ast.Expression:
    """``ast.parse`` with every parser failure turned into an ExprIssue."""
    if len(text) > MAX_LENGTH:
        raise ExprIssue("expr.too_long", length=len(text), limit=MAX_LENGTH)
    try:
        return ast.parse(text.strip(), mode="eval")
    except SyntaxError as exc:
        raise ExprIssue("expr.syntax", expr=text, problem=exc.msg) from exc
    except (RecursionError, MemoryError) as exc:
        raise ExprIssue("expr.too_deep", depth=f"mehr als {MAX_DEPTH}", limit=MAX_DEPTH) from exc
    except ValueError as exc:
        raise ExprIssue("expr.syntax", expr=text, problem=str(exc)) from exc


def _number_literal(node: ast.expr) -> float | None:
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub | ast.UAdd):
        inner = _number_literal(node.operand)
        sign = -1.0 if isinstance(node.op, ast.USub) else 1.0
        return None if inner is None else sign * inner
    value = node.value if isinstance(node, ast.Constant) else None
    if isinstance(value, int | float) and not isinstance(value, bool):
        return float(value)
    return None


def _table(node: ast.expr) -> tuple[float, ...]:
    if not isinstance(node, ast.List | ast.Tuple):
        raise ExprIssue("expr.interp_table", reason="Stützstellen als Zahlenliste angeben")
    values = [_number_literal(e) for e in node.elts]
    numbers = [v for v in values if v is not None]
    if len(numbers) != len(values):
        raise ExprIssue("expr.interp_table", reason="nur Zahlen sind als Stützstellen erlaubt")
    return tuple(numbers)


@dataclass
class _Builder:
    env: Mapping[str, VarType]
    refs: set[str] = field(default_factory=set[str])

    def build(self, node: ast.expr) -> Typed:
        handler = _HANDLERS.get(type(node))
        if handler is None:
            if isinstance(node, ast.IfExp):
                raise _forbidden("IfExp", "Stattdessen where(Bedingung, a, b) verwenden.")
            raise _forbidden(type(node).__name__)
        return handler(self, node)

    def numeric(self, node: ast.expr) -> Expr:
        expr, kind = self.build(node)
        if kind.kind == "choice":
            raise ExprIssue("expr.choice_usage", choice=kind.node)
        return expr

    def boolean(self, node: ast.expr, context: str) -> Expr:
        expr, kind = self.build(node)
        if kind.kind != "bool":
            raise ExprIssue(
                "expr.type", expected="Wahrheitswert", got=_KIND_DE[kind.kind], context=context
            )
        return expr

    def constant(self, node: ast.Constant) -> Typed:
        if isinstance(node.value, bool):
            return Const(node.value), BOOL
        if isinstance(node.value, int | float):
            return Const(float(node.value)), NUM
        raise _forbidden(type(node.value).__name__)

    def name(self, node: ast.Name) -> Typed:
        if node.id in ("true", "false"):
            return Const(node.id == "true"), BOOL
        if node.id not in self.env:
            close = difflib.get_close_matches(node.id, list(self.env), n=1)
            hint = f"Meinten Sie „{close[0]}“?" if close else ""
            raise ExprIssue("expr.unknown_name", name=node.id, suggestion=hint)
        self.refs.add(node.id)
        return Var(node.id), self.env[node.id]

    def binop(self, node: ast.BinOp) -> Typed:
        op = type(node.op).__name__
        if op not in _ARITH_OPS:
            raise _forbidden(op)
        return Arith(op, self.numeric(node.left), self.numeric(node.right)), NUM

    def unary(self, node: ast.UnaryOp) -> Typed:
        if isinstance(node.op, ast.Not):
            return Not(self.boolean(node.operand, "not")), BOOL
        if isinstance(node.op, ast.USub | ast.UAdd):
            sign = -1.0 if isinstance(node.op, ast.USub) else 1.0
            return Neg(self.numeric(node.operand), sign), NUM
        raise _forbidden(type(node.op).__name__)

    def boolop(self, node: ast.BoolOp) -> Typed:
        op = type(node.op).__name__
        context = "and" if op == "And" else "or"
        return Logic(op, tuple(self.boolean(v, context) for v in node.values)), BOOL

    def compare(self, node: ast.Compare) -> Typed:
        lefts = [node.left, *node.comparators[:-1]]
        parts = [
            self.pair(type(op).__name__, a, b)
            for op, a, b in zip(node.ops, lefts, node.comparators, strict=True)
        ]
        return (parts[0] if len(parts) == 1 else Logic("And", tuple(parts))), BOOL

    def pair(self, op: str, left: ast.expr, right: ast.expr) -> Expr:
        if op not in _COMPARE_OPS:
            raise _forbidden(op)
        choice = self.choice_side(left) or self.choice_side(right)
        if choice is not None:
            return self.choice_compare(op, choice, left if choice is right else right)
        if _is_text(left) or _is_text(right):
            raise _forbidden("str")
        return Cmp(op, self.numeric(left), self.numeric(right))

    def choice_side(self, node: ast.expr) -> ast.Name | None:
        if isinstance(node, ast.Name) and self.env.get(node.id, NUM).kind == "choice":
            return node
        return None

    def choice_compare(self, op: str, choice: ast.Name, other: ast.expr) -> Expr:
        kind = self.env[choice.id]
        if op not in ("Eq", "NotEq") or not _is_text(other):
            raise ExprIssue("expr.choice_usage", choice=choice.id)
        assert isinstance(other, ast.Constant)
        label = str(other.value)
        if label not in kind.labels:
            raise ExprIssue(
                "expr.unknown_label", label=label, choice=choice.id, labels=list(kind.labels)
            )
        self.refs.add(choice.id)
        return ChoiceEq(choice.id, kind.labels.index(label), negate=op == "NotEq")

    def call(self, node: ast.Call) -> Typed:
        name = self.call_name(node)
        fn = get_function(name)
        if fn is None:
            raise ExprIssue("expr.unknown_function", name=name)
        got = len(node.args)
        if got < fn.min_args or (fn.max_args is not None and got > fn.max_args):
            limit = "beliebig viele" if fn.max_args is None else str(fn.max_args)
            expected = (
                str(fn.min_args) if fn.min_args == fn.max_args else f"{fn.min_args} bis {limit}"
            )
            raise ExprIssue("expr.arity", name=name, expected=expected, got=got)
        special = _SPECIAL_CALLS.get(name)
        if special is not None:
            return special(self, node)
        return Call(fn.impl, tuple(self.numeric(a) for a in node.args)), NUM

    def call_name(self, node: ast.Call) -> str:
        if not isinstance(node.func, ast.Name):
            raise _forbidden("Call")
        if node.keywords:
            raise _forbidden("keyword")
        if any(isinstance(a, ast.Starred) for a in node.args):
            raise _forbidden("Starred")
        return node.func.id

    def where(self, node: ast.Call) -> Typed:
        cond = self.boolean(node.args[0], "where-Bedingung")
        (a, ta), (b, tb) = self.build(node.args[1]), self.build(node.args[2])
        if "choice" in (ta.kind, tb.kind):
            raise ExprIssue("expr.choice_usage", choice=ta.node or tb.node)
        both_bool = ta.kind == tb.kind == "bool"
        return Where(cond, a, b), BOOL if both_bool else NUM

    def extremum(self, node: ast.Call) -> Typed:
        assert isinstance(node.func, ast.Name)
        return Extremum(node.func.id, tuple(self.numeric(a) for a in node.args)), NUM

    def interp(self, node: ast.Call) -> Typed:
        x = self.numeric(node.args[0])
        xs, ys = _table(node.args[1]), _table(node.args[2])
        if len(xs) != len(ys) or len(xs) < 2:
            raise ExprIssue("expr.interp_table", reason="gleich viele Werte, mindestens zwei")
        if any(b <= a for a, b in pairwise(xs)):
            raise ExprIssue("expr.interp_table", reason="x-Werte müssen streng steigen")
        return Interp(x, xs, ys), NUM


def _is_text(node: ast.expr) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, str)


_HANDLERS: dict[type[ast.AST], Callable[[_Builder, Any], Typed]] = {
    ast.Constant: _Builder.constant,
    ast.Name: _Builder.name,
    ast.BinOp: _Builder.binop,
    ast.UnaryOp: _Builder.unary,
    ast.BoolOp: _Builder.boolop,
    ast.Compare: _Builder.compare,
    ast.Call: _Builder.call,
}
_SPECIAL_CALLS: dict[str, Callable[[_Builder, ast.Call], Typed]] = {
    "where": _Builder.where,
    "interp": _Builder.interp,
    "min": _Builder.extremum,
    "max": _Builder.extremum,
}


def compile_expr(text: str, env: Mapping[str, VarType]) -> CompiledExpr:
    """Compile ``text`` given the types of the names it may reference."""
    tree = parse_expression(text)
    depth = _depth(tree.body)
    if depth > MAX_DEPTH:
        raise ExprIssue("expr.too_deep", depth=depth, limit=MAX_DEPTH)
    size = sum(1 for _ in ast.walk(tree.body))
    if size > MAX_NODES:
        raise ExprIssue("expr.too_large", size=size, limit=MAX_NODES)
    builder = _Builder(env)
    expr, kind = builder.build(tree.body)
    return CompiledExpr(expr, kind, frozenset(builder.refs))
