"""The form editor driven by AppTest (M6 AK 1, 3 and edge cases)."""

from pathlib import Path

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from app.adapters import files, settings
from app.engine.simulate import simulate
from app.model.compile import compile_model, content_hash
from app.model.scenarios import effective_model
from app.model.schema import Model
from app.model.yaml_io import model_from_yaml

ROOT = Path(__file__).resolve().parent.parent
MAIN = str(ROOT / "src" / "app" / "ui" / "main.py")
T2 = ROOT / "examples" / "t2_terminplan.yaml"


def start() -> AppTest:
    at = AppTest.from_file(MAIN, default_timeout=60).run()
    assert not at.exception
    return at


def run(at: AppTest) -> AppTest:
    assert not at.exception, at.exception
    errors = [e.value for e in at.error]
    assert not any("Unerwarteter" in str(e) for e in errors), errors
    return at


def texts(at: AppTest) -> str:
    parts = [m.value for m in (*at.markdown, *at.caption, *at.subheader)]
    parts += [e.value for e in (*at.success, *at.info, *at.warning, *at.error)]
    return "\n".join(str(p) for p in parts)


def draft(at: AppTest) -> str:
    return str(at.text_area(key="editor").value)


def field(at: AppTest, node: str, name: str, value: str) -> None:
    key = f"form.{node}.{name}"
    widget = (
        at.text_area(key=key) if name in ("expr", "why", "description") else at.text_input(key=key)
    )
    run(widget.input(value).run())


def add(at: AppTest, node: str, node_type: str) -> None:
    at.text_input(key="form_new_id").input(node).run()
    at.selectbox(key="form_new_type").set_value(node_type).run()
    run(at.button(key="form_add").click().run())
    assert at.selectbox(key="form_pick").value == node


def uncertain(at: AppTest, node: str, mean: str, sd: str, name: str) -> None:
    add(at, node, "uncertain")
    run(at.selectbox(key=f"form.{node}.dist").set_value("normal").run())
    field(at, node, "param.mean", mean)
    field(at, node, "param.sd", sd)
    field(at, node, "unit", "d")
    field(at, node, "name", name)


def own_t2(stem: str = "plan") -> AppTest:
    files.copy_model(T2, settings.models_dir(), stem)
    at = start()
    at.button(key=f"open_{stem}").click().run()
    return run(at.switch_page("pages/modell.py").run())


def test_new_model_from_start_page_opens_in_the_form() -> None:
    at = start()
    at.text_input(key="new_model_id").input("leer").run()
    at.button(key="new_model_create").click().run()
    run(at)
    assert (settings.models_dir() / "leer.yaml").is_file()
    assert "noch keine Knoten" in texts(at)


def _header(at: AppTest) -> None:
    reference = model_from_yaml(T2.read_text("utf-8"))
    assert reference.title is not None
    assert reference.description is not None
    for name, value in (
        ("title", reference.title),
        ("description", reference.description),
        ("n", "100000"),
        ("seed", "20261027"),
    ):
        run(at.text_input(key=f"form.{name}").input(value).run())


def _nodes(at: AppTest) -> None:
    uncertain(at, "a", "10", "2", "Vorgang A")
    uncertain(at, "b", "15", "3", "Vorgang B")
    uncertain(at, "c", "24", "4", "Vorgang C")
    add(at, "nacharbeit", "event")
    field(at, "nacharbeit", "p", "0")
    field(at, "nacharbeit", "name", "Nacharbeit an B")
    add(at, "pfad1", "derived")
    field(at, "pfad1", "expr", "a + b + where(nacharbeit, 5, 0)")
    field(at, "pfad1", "unit", "d")
    run(at.checkbox(key="form.pfad1.track").check().run())
    field(at, "pfad1", "name", "Pfad 1")
    add(at, "ende", "output")
    field(at, "ende", "expr", "max(pfad1, c)")
    field(at, "ende", "unit", "d")
    run(at.selectbox(key="form.ende.target_op").set_value("le").run())
    field(at, "ende", "target_value", "30")
    field(at, "ende", "name", "Projektende")


def _scenario(at: AppTest, sid: str, name: str, why: str, override: tuple[str, ...]) -> None:
    at.text_input(key="scenario_new_id").input(sid).run()
    at.text_input(key="scenario_new_name").input(name).run()
    at.text_input(key="scenario_new_why").input(why).run()
    at.selectbox(key="scenario_new_parent").set_value("basis").run()
    run(at.button(key="scenario_add").click().run())
    node, name_, value, reason = override
    at.selectbox(key="override_node").set_value(node).run()
    at.text_input(key="override_field").input(name_).run()
    at.text_input(key="override_value").input(value).run()
    at.text_input(key="override_why").input(reason).run()
    run(at.button(key="override_set").click().run())


def _scenarios(at: AppTest) -> None:
    run(at.switch_page("pages/szenarien.py").run())
    reference = model_from_yaml(T2.read_text("utf-8")).scenarios
    for sid, node, name, value in (
        ("b_schneller", "b", "mean", "12"),
        ("nacharbeit", "nacharbeit", "p", "0.2"),
    ):
        s = reference[sid]
        why = str(s.overrides[node]["why"])
        _scenario(at, sid, s.name, s.why, (node, name, value, why))


def _same_numbers(built: Model, reference: Model) -> None:
    for sid in ("basis", "b_schneller", "nacharbeit"):
        ours = simulate(compile_model(effective_model(built, sid)), n=5000).samples["ende"]
        theirs = simulate(compile_model(effective_model(reference, sid)), n=5000).samples["ende"]
        assert np.array_equal(ours, theirs), sid


def test_t2_rebuilt_through_the_form_gives_the_same_model_and_numbers() -> None:
    files.create_model_text(
        settings.models_dir(), "nachbau", "schema_version: 1\nmodel: x\nnodes: {}\n"
    )
    at = start()
    at.button(key="open_nachbau").click().run()
    run(at.switch_page("pages/modell.py").run())
    _header(at)
    _nodes(at)
    _scenarios(at)
    run(at.switch_page("pages/modell.py").run())
    run(at.button(key="save_model").click().run())
    built = files.load_model(settings.models_dir() / "nachbau.yaml")
    reference = model_from_yaml(T2.read_text("utf-8"))
    assert content_hash(built) == content_hash(reference)
    assert built.title == reference.title
    _same_numbers(built, reference)


def test_form_edit_keeps_comments_after_saving() -> None:
    at = own_t2()
    run(at.selectbox(key="form_pick").set_value("b").run())
    field(at, "b", "param.mean", "16")
    run(at.button(key="save_model").click().run())
    saved = (settings.models_dir() / "plan.yaml").read_text("utf-8")
    for line in T2.read_text("utf-8").splitlines():
        if line.lstrip().startswith("#"):
            assert line in saved
    assert "mean: 16, sd: 3" in saved


def test_last_change_wins_between_yaml_and_form() -> None:
    at = own_t2()
    run(at.text_area(key="editor").input(draft(at).replace("mean: 15", "mean: 13")).run())
    run(at.selectbox(key="form_pick").set_value("b").run())
    assert at.text_input(key="form.b.param.mean").value == "13"
    field(at, "b", "param.mean", "14")
    assert "mean: 14" in draft(at)
    assert "letzte Änderung" in texts(at)


def test_unreadable_yaml_locks_the_form_and_invalid_model_has_no_preview() -> None:
    at = own_t2()
    run(at.text_area(key="editor").input("a: [1\n").run())
    assert "erst im Reiter „YAML“ korrigieren" in texts(at)
    at = own_t2("plan2")
    run(at.selectbox(key="form_pick").set_value("b").run())
    assert "Vorschau der Verteilung" in texts(at)
    assert "Mittelwert" in texts(at)
    field(at, "b", "param.sd", "")
    assert "sobald das Modell fehlerfrei ist" in texts(at)


def test_delete_needs_confirmation_and_no_references() -> None:
    at = own_t2()
    run(at.selectbox(key="form_pick").set_value("ende").run())
    assert at.button(key="form.ende.delete").disabled
    run(at.checkbox(key="form.ende.delete_confirm").check().run())
    run(at.button(key="form.ende.delete").click().run())
    assert "  ende:" not in draft(at)
    run(at.selectbox(key="form_pick").set_value("b").run())
    run(at.checkbox(key="form.b.delete_confirm").check().run())
    run(at.button(key="form.b.delete").click().run())
    assert "lässt sich nicht löschen" in texts(at)


@pytest.mark.parametrize("stem", ["t1_faltung", "t2_terminplan"])
def test_tutorial_form_is_read_only(stem: str) -> None:
    at = start()
    at.button(key=f"open_{stem}").click().run()
    run(at.switch_page("pages/modell.py").run())
    assert all(w.disabled for w in at.text_input if str(w.key).startswith("form."))


def test_scenario_page_edit_keeps_comments() -> None:
    at = own_t2()
    run(at.switch_page("pages/szenarien.py").run())
    at.selectbox(key="scenario_pick").set_value("b_schneller").run()
    at.selectbox(key="override_node").set_value("c").run()
    at.text_input(key="override_field").input("sd").run()
    at.text_input(key="override_value").input("5").run()
    run(at.button(key="override_set").click().run())
    run(at.switch_page("pages/modell.py").run())
    text = draft(at)
    assert "c: {sd: 5}" in text or "sd: 5" in text
    for line in T2.read_text("utf-8").splitlines():
        if line.lstrip().startswith("#"):
            assert line in text
