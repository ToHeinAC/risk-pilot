"""Expression language: parsing, whitelist, typing, evaluation (M1 AK 4, AP2)."""

from collections.abc import Mapping

import numpy as np
import pytest
from numpy.typing import NDArray

from app.expr.evaluate import EvalError
from app.expr.parser import BOOL, NUM, ExprIssue, VarType, choice_type, compile_expr

X = np.array([0.5, 1.0, 2.0, 4.0])
Y = np.array([2.0, 1.0, 0.5, 3.0])
E = np.array([True, False, True, False])
R = np.array([0.0, 1.0, 2.0, 1.0])  # choice codes of "route"
ENV: dict[str, VarType] = {
    "x": NUM,
    "y": NUM,
    "e": BOOL,
    "route": choice_type("route", ("ICE", "Regio", "Bus")),
    "nacharbeit": NUM,
}
VALUES: dict[str, NDArray[np.float64] | NDArray[np.bool_]] = {"x": X, "y": Y, "e": E, "route": R}


def ev(
    text: str, values: Mapping[str, NDArray[np.float64] | NDArray[np.bool_]] = VALUES
) -> NDArray:
    result = compile_expr(text, ENV).node.evaluate(values)
    return np.broadcast_to(result, X.shape)


def issue(text: str) -> ExprIssue:
    with pytest.raises(ExprIssue) as exc:
        compile_expr(text, ENV)
    return exc.value


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("x + y", X + Y),
        ("x - y", X - Y),
        ("x * y", X * Y),
        ("x / y", X / Y),
        ("x ** 2", X**2),
        ("x % 1.5", np.mod(X, 1.5)),
        ("-x", -X),
        ("+x", X),
        ("2 * (x + 1)", 2 * (X + 1)),
        ("min(x, y)", np.minimum(X, Y)),
        ("max(x, y, 1.5)", np.maximum(np.maximum(X, Y), 1.5)),
        ("sum(x, y, 1)", X + Y + 1),
        ("sum(x)", X),
        ("abs(-x)", X),
        ("exp(x)", np.exp(X)),
        ("log(x)", np.log(X)),
        ("sqrt(x)", np.sqrt(X)),
        ("floor(x)", np.floor(X)),
        ("ceil(x)", np.ceil(X)),
        ("clip(x, 1, 2)", np.clip(X, 1, 2)),
        ("where(e, x, y)", np.where(E, X, Y)),
        ("interp(x, [0, 1, 3], [0, 10, 20])", np.interp(X, [0, 1, 3], [0, 10, 20])),
        ("5 * e", 5.0 * E),
        ("e + e", 2.0 * E),
        ("-e", -1.0 * E),
        ("3", np.full(4, 3.0)),
    ],
)
def test_numeric_operators_and_functions(text: str, expected: NDArray) -> None:
    np.testing.assert_allclose(ev(text), expected)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("x < y", X < Y),
        ("x <= y", X <= Y),
        ("x > y", X > Y),
        ("x >= y", X >= Y),
        ("x == y", X == Y),
        ("x != y", X != Y),
        ("0.75 < x < 3", (X > 0.75) & (X < 3)),
        ("e and x > 1", E & (X > 1)),
        ("e or x > 1", E | (X > 1)),
        ("not e", ~E),
        ("e == (x > 1)", (X > 1) == E),
        ('route == "Bus"', R == 2),
        ('route != "ICE"', R != 0),
        ('"Regio" == route', R == 1),
        ("true", np.full(4, True)),
        ("e > 0", E),
    ],
)
def test_boolean_expressions(text: str, expected: NDArray) -> None:
    result = ev(text)
    assert result.dtype == np.bool_
    np.testing.assert_array_equal(result, expected)


def test_result_types() -> None:
    assert compile_expr("x + 1", ENV).type == NUM
    assert compile_expr("x > 1", ENV).type == BOOL
    assert compile_expr("where(e, e, x > 1)", ENV).type == BOOL
    assert compile_expr("where(e, 1, x)", ENV).type == NUM
    assert compile_expr("route", ENV).type == ENV["route"]


def test_refs() -> None:
    assert compile_expr("max(x, y) + where(e, 1, 0)", ENV).refs == frozenset({"x", "y", "e"})


def test_unchosen_where_branch_may_be_non_finite() -> None:
    zero = np.array([0.0, 1.0, 0.0, 2.0])
    out = compile_expr("where(z > 0, log(z), 0)", {"z": NUM}).node.evaluate({"z": zero})
    assert np.all(np.isfinite(out))


@pytest.mark.parametrize(
    ("text", "construct"),
    [
        ("x.real", "Attribute"),
        ("x[0]", "Subscript"),
        ("lambda: 1", "Lambda"),
        ("[v for v in x]", "ListComp"),
        ("(v for v in x)", "GeneratorExp"),
        ("x if e else y", "IfExp"),
        ("max(x, y, key=1)", "keyword"),
        ("max(*x)", "Starred"),
        ("(z := 1)", "NamedExpr"),
        ('f"{x}"', "JoinedStr"),
        ("(x + 1)(2)", "Call"),
        ("x & y", "BitAnd"),
        ("x // y", "FloorDiv"),
        ("x in y", "In"),
        ("x is y", "Is"),
        ("[1, 2]", "List"),
        ("{1: 2}", "Dict"),
        ("'text'", "str"),
    ],
)
def test_forbidden_constructs(text: str, construct: str) -> None:
    err = issue(text)
    assert err.code == "expr.forbidden"
    assert err.params["construct"] == construct


def test_if_expression_hints_where() -> None:
    assert "where(" in str(issue("x if e else y").params["hint"])


def test_unknown_function() -> None:
    err = issue("mean(x, y)")
    assert (err.code, err.params["name"]) == ("expr.unknown_function", "mean")


def test_unknown_name_with_suggestion() -> None:
    err = issue("nacharbiet + 1")
    assert err.code == "expr.unknown_name"
    assert "nacharbeit" in str(err.params["suggestion"])


def test_function_name_as_value_is_unknown_name() -> None:
    assert issue("max + 1").code == "expr.unknown_name"


@pytest.mark.parametrize("text", ["min(x)", "abs(x, y)", "clip(x, 1)", "where(e, x)", "sum()"])
def test_arity(text: str) -> None:
    assert issue(text).code == "expr.arity"


def test_syntax_error() -> None:
    assert issue("x +").code == "expr.syntax"


def test_length_limit_checked_before_parse() -> None:
    err = issue("x +" * 400)
    assert (err.code, err.params["limit"]) == ("expr.too_long", 1000)


def test_depth_limit() -> None:
    assert issue("(" * 40 + "x" + ")" * 40 + " + " + "-" * 40 + "x").code == "expr.too_deep"


def test_size_limit() -> None:
    assert issue("sum(" + ",".join(["-x"] * 200) + ")").code == "expr.too_large"


@pytest.mark.parametrize(
    "text",
    ["e and x", "not x", "where(x, 1, 2)", "x or e"],
)
def test_logic_needs_bool(text: str) -> None:
    assert issue(text).code == "expr.type"


@pytest.mark.parametrize("text", ["route + 1", "route > 1", "max(route, 1)", "route == 1", "route"])
def test_choice_usage(text: str) -> None:
    if text == "route":
        assert compile_expr(text, ENV).type.kind == "choice"
        return
    assert issue(text).code == "expr.choice_usage"


def test_unknown_label() -> None:
    err = issue('route == "Taxi"')
    assert (err.code, err.params["label"]) == ("expr.unknown_label", "Taxi")


def test_string_outside_choice_comparison() -> None:
    assert issue('x == "a"').code == "expr.forbidden"


@pytest.mark.parametrize(
    "text",
    [
        "interp(x, [0], [1])",
        "interp(x, [0, 1], [1])",
        "interp(x, [1, 0], [1, 2])",
        "interp(x, [0, 0], [1, 2])",
        "interp(x, [0, y], [1, 2])",
        "interp(x, y, [1, 2])",
    ],
)
def test_interp_table(text: str) -> None:
    assert issue(text).code == "expr.interp_table"


def test_clip_bounds_runtime_error_with_share() -> None:
    node = compile_expr("clip(x, y, 1)", ENV).node
    with pytest.raises(EvalError) as exc:
        node.evaluate(VALUES)
    assert exc.value.code == "runtime.clip_bounds"
    assert exc.value.share == pytest.approx(0.5)


def test_bool_constant_arithmetic() -> None:
    np.testing.assert_allclose(ev("true + 1"), np.full(4, 2.0))


@pytest.mark.parametrize("text", ["x+" * 499 + "x", "-" * 990 + "x", "(" * 300 + "x" + ")" * 300])
def test_deep_short_expressions_rejected_not_crashing(text: str) -> None:
    assert issue(text).code in {"expr.too_deep", "expr.syntax"}
