"""Scenarios: format, inheritance, validation, diff, duplicate, detach (M3 AK 1-4, 8, edges)."""

import pytest

from app.errors import Issue, ModelError
from app.messages import render
from app.model import scenarios as sc
from app.model.schema import ConstantNode, EventNode, Model, UncertainNode
from app.model.yaml_io import model_from_yaml, model_to_yaml

BASE = """schema_version: 1
model: m
nodes:
  a: {type: uncertain, dist: normal, mean: 10, sd: 2}
  b: {type: uncertain, dist: normal, mean: 15, sd: 3}
  k: {type: constant, value: 1}
  e: {type: event, p: 0}
  y: {type: output, expr: "a + b * k + where(e, 5, 0)", target: {le: 30}}
"""

SCEN = """scenarios:
  schnell:
    name: "B −3 Tage"
    why: "Zweites Team"
    overrides:
      b: {mean: 12, why: "Plan"}
  schnell_nach:
    name: "Schnell mit Nacharbeit"
    parent: schnell
    why: "Gewinn prüfen"
    overrides:
      e: {p: 0.2}
  tief:
    name: "Ebene 3"
    parent: schnell_nach
    why: "Tiefe"
    overrides:
      k: {value: 2}
"""


def load(text: str = BASE + SCEN) -> Model:
    return model_from_yaml(text)


def issues(text: str) -> list[Issue]:
    found, _ = sc.validate(model_from_yaml(text))
    return found


def test_scenario_stores_only_overrides_and_roundtrips() -> None:
    model = load()
    s = model.scenarios["schnell"]
    assert s.parent == "basis"
    assert s.why == "Zweites Team"
    assert s.overrides == {"b": {"mean": 12, "why": "Plan"}}
    assert model_from_yaml(model_to_yaml(model)) == model


def test_scenario_needs_why() -> None:
    with pytest.raises(ModelError):
        model_from_yaml(BASE + "scenarios:\n  s: {name: S, overrides: {}}\n")


def test_chain_and_effective_model_depth_three() -> None:
    model = load()
    assert sc.chain(model, "tief") == ["basis", "schnell", "schnell_nach", "tief"]
    eff = sc.effective_model(model, "tief")
    b, e, k = eff.nodes["b"], eff.nodes["e"], eff.nodes["k"]
    assert isinstance(b, UncertainNode)
    assert isinstance(e, EventNode)
    assert isinstance(k, ConstantNode)
    assert (b.params()["mean"], b.params()["sd"], e.p, k.value) == (12, 3, 0.2, 2)
    assert eff.scenarios == {}
    assert sc.effective_model(model, "basis").nodes == model.nodes


def test_parent_change_inherited_unless_overridden() -> None:
    changed = load(
        BASE.replace("mean: 15, sd: 3", "mean: 15, sd: 4").replace("value: 1}", "value: 3}") + SCEN
    )
    eff = sc.effective_model(changed, "schnell_nach")
    b, k = eff.nodes["b"], eff.nodes["k"]
    assert isinstance(b, UncertainNode)
    assert isinstance(k, ConstantNode)
    assert b.params() == {"mean": 12, "sd": 4}  # sd inherited, mean overridden
    assert k.value == 3


def test_family_change_replaces_parameter_set() -> None:
    text = BASE + (
        "scenarios:\n  pert:\n    name: P\n    why: W\n    overrides:\n"
        "      b: {dist: pert, low: 10, mode: 15, high: 25}\n"
    )
    b = sc.effective_model(load(text), "pert").nodes["b"]
    assert isinstance(b, UncertainNode)
    assert b.dist == "pert"
    assert b.params() == {"low": 10, "mode": 15, "high": 25}


def test_valid_scenarios_have_no_issues() -> None:
    found, notices = sc.validate(load())
    assert found == []
    assert notices == []


@pytest.mark.parametrize(
    ("block", "code"),
    [
        ("  s: {name: S, why: W, parent: fehlt, overrides: {}}\n", "scenario.parent_unknown"),
        (
            "  s1: {name: S1, why: W, parent: s2, overrides: {}}\n"
            "  s2: {name: S2, why: W, parent: s1, overrides: {}}\n",
            "scenario.parent_cycle",
        ),
        ("  s: {name: S, why: W, overrides: {zz: {value: 1}}}\n", "scenario.node_unknown"),
        ("  s: {name: S, why: W, overrides: {k: {mean: 1}}}\n", "scenario.field_invalid"),
        ("  s: {name: S, why: W, overrides: {k: {name: Neu}}}\n", "scenario.field_invalid"),
        ("  s: {name: S, why: W, overrides: {k: {type: derived}}}\n", "scenario.type_change"),
        (
            "  s: {name: S, why: W, correlations: {zz: {spearman: [[1]]}}, overrides: {}}\n",
            "scenario.corr_unknown",
        ),
        ("  s: {name: S, why: W, overrides: {b: {sd: -1}}}\n", "param.invalid"),
        ("  s: {name: S, why: W, overrides: {k: {value: y}}}\n", "model.schema"),
        ("  s: {name: S, why: W, overrides: {a: {mean: 'y'}}}\n", "graph.cycle"),
    ],
)
def test_invalid_scenarios(block: str, code: str) -> None:
    found = issues(BASE + "scenarios:\n" + block)
    assert code in [i.code for i in found]
    assert all(i.scenario is not None for i in found)


def test_scenario_issue_names_scenario_in_text() -> None:
    found = issues(BASE + "scenarios:\n  s: {name: S, why: W, overrides: {b: {sd: -1}}}\n")
    assert "Szenario „s“" in render(found[0])


@pytest.mark.parametrize("bad", ["basis", "Neu", "1x"])
def test_invalid_scenario_ids(bad: str) -> None:
    with pytest.raises(ModelError) as exc:
        model_from_yaml(BASE + f"scenarios:\n  '{bad}': {{name: S, why: W, overrides: {{}}}}\n")
    assert exc.value.issues[0].code == "scenario.id_invalid"


def test_inactive_override_on_deleted_node_is_notice_and_ignored() -> None:
    text = (
        BASE + "scenarios:\n  s: {name: S, why: W, overrides: {weg: {value: 1, inactive: true}}}\n"
    )
    found, notices = sc.validate(load(text))
    assert found == []
    assert [(n.code, n.node_id) for n in notices] == [("scenario.inactive", "weg")]
    assert sc.effective_model(load(text), "s").nodes == load(text).nodes


def test_same_value_override_is_marked() -> None:
    text = BASE + "scenarios:\n  s: {name: S, why: W, overrides: {k: {value: 1}}}\n"
    _, notices = sc.validate(load(text))
    assert [(n.code, n.node_id) for n in notices] == [("scenario.same_value", "k")]


def test_diff_lists_exactly_the_overrides() -> None:
    text = BASE + (
        "scenarios:\n  s:\n    name: S\n    why: W\n    overrides:\n"
        "      b: {mean: 12, why: Plan}\n      k: {value: 1}\n"
        "      weg: {value: 2, inactive: true}\n"
    )
    rows = sc.diff(load(text), "s")
    assert [(r.node, r.field, r.before, r.after, r.why, r.status) for r in rows] == [
        ("b", "mean", 15, 12, "Plan", "geändert"),
        ("k", "value", 1.0, 1, None, "gleich"),
        ("weg", "value", None, 2, None, "inaktiv"),
    ]


def test_diff_against_parent_not_basis() -> None:
    rows = sc.diff(load(), "schnell_nach")
    assert [(r.node, r.field, r.before, r.after) for r in rows] == [("e", "p", 0.0, 0.2)]


def test_duplicate() -> None:
    model = sc.duplicate(load(), "schnell", "schnell_2")
    copy = model.scenarios["schnell_2"]
    assert copy.overrides == model.scenarios["schnell"].overrides
    assert copy.parent == "basis"
    assert copy.name == "Kopie von B −3 Tage"
    with pytest.raises(ValueError, match="vergeben"):
        sc.duplicate(model, "schnell", "schnell_2")


def test_detach_freezes_effective_model() -> None:
    model = sc.detach(load(), "schnell_nach")
    detached = model.scenarios["schnell_nach"]
    assert detached.overrides == {}
    assert detached.nodes is not None
    assert detached.detached_from == "schnell"
    later = model.model_copy(
        update={
            "scenarios": {
                **model.scenarios,
                "schnell": model.scenarios["schnell"].model_copy(
                    update={"overrides": {"b": {"mean": 5}}}
                ),
            }
        }
    )
    b = sc.effective_model(later, "schnell_nach").nodes["b"]
    assert isinstance(b, UncertainNode)
    assert b.params()["mean"] == 12  # parent change no longer applies
    assert sc.chain(later, "tief") == ["schnell_nach", "tief"]
    assert sc.validate(later)[0] == []


def test_add_and_set_override_and_mark_inactive() -> None:
    model = sc.add_scenario(load(BASE), "neu", "Neu", "basis", "Test")
    model = sc.set_override(model, "neu", "b", "mean", 11, "Annahme")
    assert model.scenarios["neu"].overrides == {"b": {"mean": 11, "why": "Annahme"}}
    model = sc.remove_override(model, "neu", "b", "mean")
    assert model.scenarios["neu"].overrides == {}
    with pytest.raises(ValueError, match="vergeben"):
        sc.add_scenario(model, "neu", "X", "basis", "W")
    broken = load(BASE + "scenarios:\n  s: {name: S, why: W, overrides: {weg: {value: 1}}}\n")
    fixed = sc.mark_unknown_inactive(broken)
    assert fixed.scenarios["s"].overrides["weg"]["inactive"] is True
    assert sc.validate(fixed)[0] == []


def test_ordered_tree() -> None:
    assert sc.tree(load()) == [("basis", 0), ("schnell", 1), ("schnell_nach", 2), ("tief", 3)]


def test_cycle_message_names_chain_in_order() -> None:
    found = issues(
        BASE + "scenarios:\n  s1: {name: S1, why: W, parent: s2, overrides: {}}\n"
        "  s2: {name: S2, why: W, parent: s1, overrides: {}}\n"
    )
    cycle = next(i for i in found if i.code == "scenario.parent_cycle" and i.scenario == "s1")
    assert cycle.params["cycle"] == ["s1", "s2", "s1"]


def test_child_of_detached_checked_against_frozen_nodes() -> None:
    model = sc.detach(load(BASE + SCEN), "schnell")
    frozen = dict(model.scenarios["schnell"].nodes or {})
    del frozen["k"]
    data = model.model_dump(mode="json", exclude_unset=True)
    data["scenarios"]["schnell"]["nodes"] = {
        k: v.model_dump(mode="json", exclude_unset=True) for k, v in frozen.items()
    }
    data["nodes"]["y"]["expr"] = "a + b + where(e, 5, 0)"
    data["scenarios"]["schnell"]["nodes"]["y"]["expr"] = "a + b + where(e, 5, 0)"
    data["scenarios"]["tief"]["overrides"] = {"k": {"value": 2}}  # k exists in basis only
    found, _ = sc.validate(Model.model_validate(data))
    assert ("scenario.node_unknown", "tief") in [(i.code, i.scenario) for i in found]


@pytest.mark.parametrize(("sid", "why"), [("Neu", "W"), ("", "W"), ("ok", "")])
def test_add_scenario_rejects_bad_id_or_missing_why(sid: str, why: str) -> None:
    with pytest.raises(ValueError, match=r"nicht zulässig|Begründung"):
        sc.add_scenario(load(BASE), sid, "N", "basis", why)


@pytest.mark.parametrize(("node", "field"), [("zz", "value"), ("k", "mean"), ("k", "type")])
def test_set_override_rejects_unknown_node_or_field(node: str, field: str) -> None:
    model = sc.add_scenario(load(BASE), "s", "S", "basis", "W")
    with pytest.raises(ValueError, match=r"gibt es nicht|nicht überschreiben"):
        sc.set_override(model, "s", node, field, 1, None)


def test_empty_why_rejected_by_schema() -> None:
    with pytest.raises(ModelError):
        model_from_yaml(BASE + "scenarios:\n  s: {name: S, why: '', overrides: {}}\n")
