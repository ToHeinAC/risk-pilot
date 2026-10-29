"""Model page of the new UI (M7 step 2): workbench, form, YAML, save, hints."""

from pathlib import Path

import numpy as np
import pytest
from nicegui import ui
from nicegui.elements.upload_files import SmallFileUpload
from nicegui.testing import User
from web_util import drive, element, enabled, open_model, put, texts, until, value

from app.adapters import files, settings
from app.engine.simulate import simulate
from app.messages import t
from app.model.compile import compile_model, content_hash
from app.model.scenarios import effective_model
from app.model.schema import BASIS
from app.model.yaml_io import model_from_yaml

ROOT = Path(__file__).resolve().parent.parent
T2 = ROOT / "examples" / "t2_terminplan.yaml"
ONE = "schema_version: 1\nmodel: eigen\nnodes:\n  y: {type: output, expr: '1'}\n"


def own(text: str, stem: str = "eigen") -> None:
    files.create_model_text(settings.models_dir(), stem, text)


def own_t2(stem: str = "plan") -> None:
    files.copy_model(T2, settings.models_dir(), stem)


def pick(user: User, node_id: str) -> None:
    user.find(marker="nodes").trigger("pick", node_id)


def editor(user: User) -> str:
    return str(value(user, "editor"))


def test_tutorial_is_read_only() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        assert not enabled(user, "editor")
        await user.should_not_see(marker="save_model")
        await user.should_see(marker="form.ende.name")
        assert not enabled(user, "form.ende.name")
        await user.should_see(t("ui.readonly"))

    drive(steps)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "schema_version: 1\nmodel: eigen\nnodes:\n  a: {type: constant, value: [1\n",
            "YAML ist nicht lesbar",
        ),
        ("schema_version: 1\nmodel: eigen\nnodes:\n  a: {type: constant, value: 1}\n", "output"),
        ("schema_version: 1\nmodel: eigen\nnodes: {}\n", "noch keine Knoten"),
        (
            "schema_version: 1\nmodel: eigen\nnodes:\n"
            "  a: {type: uncertain, dist: normal, mean: 0, sd: -1}\n"
            "  y: {type: output, expr: a}\n",
            "verlangt ist sd > 0",
        ),
    ],
)
def test_validation_messages_in_german(text: str, expected: str) -> None:
    own(ONE)

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        put(user, "editor", text)
        await user.should_see(t("ui.unsaved"))
        assert expected in texts(user)

    drive(steps)


def test_edit_save_and_draft_survives_page_change() -> None:
    own(ONE)
    new = ONE.replace("'1'", "'2'")

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        put(user, "editor", new)
        await user.should_see(t("ui.unsaved"))
        user.find(marker="nav/simulation").click()
        await user.should_see(marker="sim_run")
        user.find(marker="nav/modell").click()
        await user.should_see(marker="editor")
        assert editor(user) == new
        user.find(marker="save_model").click()
        await user.should_see(t("ui.saved"))

    drive(steps)
    assert files.read_text(settings.models_dir() / "eigen.yaml") == new


def test_save_conflict_offers_overwrite_and_invalid_draft_warns() -> None:
    own(ONE)

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        (settings.models_dir() / "eigen.yaml").write_text("extern geändert\n", encoding="utf-8")
        put(user, "editor", "schema_version: 1\nmodel: eigen\nnodes: [\n")
        user.find(marker="save_model").click()
        await user.should_see("verändert")
        user.find(marker="save_force").click()
        await user.should_see("ungültig")

    drive(steps)
    assert files.read_text(settings.models_dir() / "eigen.yaml").endswith("nodes: [\n")


def test_discard_restores_the_file() -> None:
    own(ONE)

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        put(user, "editor", ONE.replace("'1'", "'5'"))
        user.find(marker="discard_model").click()
        await user.should_not_see(t("ui.unsaved"))
        assert editor(user) == ONE

    drive(steps)


def test_model_page_offers_copy_for_tutorial() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        put(user, "copy_id_modell", "aus_modellseite")
        user.find(marker="copy_modell").click()
        await user.should_see(t("ui.copied", name="aus_modellseite"))

    drive(steps)
    assert (settings.models_dir() / "aus_modellseite.yaml").is_file()


def test_graph_click_and_table_pick_open_the_node_card() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        table = element(user, "nodes")
        assert isinstance(table, ui.table)
        rows = {r["id"]: r for r in table.rows}
        assert rows["b"]["brief"] == "um 15 d ± 3"
        assert "<rect" in rows["b"]["spark"]  # trial run fills the table
        assert rows["b"]["p10"]
        user.find(marker="graph").trigger("plotly_click", {"points": [{"customdata": "c"}]})
        await user.should_see(marker="form.c.param.mean")
        pick(user, "a")
        await user.should_see(marker="form.a.param.mean")

    drive(steps)


def test_form_edit_keeps_comments_after_saving() -> None:
    own_t2()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        pick(user, "b")
        await user.should_see(marker="form.b.param.mean")
        put(user, "form.b.param.mean", "16")
        user.find(marker="save_model").click()
        await user.should_see(t("ui.saved"))

    drive(steps)
    saved = (settings.models_dir() / "plan.yaml").read_text("utf-8")
    for line in T2.read_text("utf-8").splitlines():
        if line.lstrip().startswith("#"):
            assert line in saved
    assert "mean: 16, sd: 3" in saved


def test_last_change_wins_between_yaml_and_form() -> None:
    own_t2()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        put(user, "editor", editor(user).replace("mean: 15", "mean: 13"))
        pick(user, "b")
        await user.should_see(marker="form.b.param.mean")
        assert value(user, "form.b.param.mean") == "13"
        put(user, "form.b.param.mean", "14")
        assert "mean: 14" in editor(user)
        await user.should_see(t("form.written"))

    drive(steps)


def test_unreadable_yaml_locks_the_form_and_invalid_model_has_no_preview() -> None:
    own_t2()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        pick(user, "b")
        await user.should_see(t("form.preview"))
        assert "Mittelwert" in texts(user)
        put(user, "form.b.param.sd", "")
        await user.should_see("sobald das Modell fehlerfrei ist", retries=20)
        put(user, "editor", "a: [1\n")
        await user.should_see("erst im Reiter „YAML“ korrigieren")
        await user.should_not_see(marker="form.b.param.sd")

    drive(steps)


def test_delete_needs_confirmation_and_no_references() -> None:
    own_t2()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        pick(user, "ende")
        await user.should_see(marker="form.ende.delete")
        assert not enabled(user, "form.ende.delete")
        user.find(marker="form.ende.delete_confirm").click()
        user.find(marker="form.ende.delete").click()
        await user.should_not_see(marker="form.ende.name")
        assert "  ende:" not in editor(user)
        pick(user, "b")
        await user.should_see(marker="form.b.delete_confirm")
        user.find(marker="form.b.delete_confirm").click()
        user.find(marker="form.b.delete").click()
        await user.should_see("lässt sich nicht löschen")

    drive(steps)


async def _uncertain(user: User, node: str, mean: str, sd: str, name: str) -> None:
    await _add(user, node, "uncertain")
    put(user, f"form.{node}.dist", "normal")
    await user.should_see(marker=f"form.{node}.param.sd")
    for field, new in (("param.mean", mean), ("param.sd", sd), ("unit", "d"), ("name", name)):
        put(user, f"form.{node}.{field}", new)


async def _add(user: User, node: str, node_type: str) -> None:
    put(user, "form_new_id", node)
    put(user, "form_new_type", node_type)
    user.find(marker="form_add").click()
    await user.should_see(marker=f"form.{node}.name")


async def _build_t2(user: User) -> None:
    reference = model_from_yaml(T2.read_text("utf-8"))
    for name, new in (
        ("title", reference.title),
        ("description", reference.description),
        ("n", "100000"),
        ("seed", "20261027"),
    ):
        put(user, f"form.{name}", new)
    await _uncertain(user, "a", "10", "2", "Vorgang A")
    await _uncertain(user, "b", "15", "3", "Vorgang B")
    await _uncertain(user, "c", "24", "4", "Vorgang C")
    await _add(user, "nacharbeit", "event")
    put(user, "form.nacharbeit.p", "0")
    put(user, "form.nacharbeit.name", "Nacharbeit an B")
    await _add(user, "pfad1", "derived")
    put(user, "form.pfad1.expr", "a + b + where(nacharbeit, 5, 0)")
    put(user, "form.pfad1.unit", "d")
    put(user, "form.pfad1.track", True)
    put(user, "form.pfad1.name", "Pfad 1")
    await _add(user, "ende", "output")
    put(user, "form.ende.expr", "max(pfad1, c)")
    put(user, "form.ende.unit", "d")
    put(user, "form.ende.target_op", "le")
    put(user, "form.ende.target_value", "30")
    put(user, "form.ende.name", "Projektende")


async def _scenarios(user: User) -> None:
    user.find(marker="nav/szenarien").click()
    await user.should_see(marker="scenario_add")
    reference = model_from_yaml(T2.read_text("utf-8")).scenarios
    for sid, node, field, new in (
        ("b_schneller", "b", "mean", "12"),
        ("nacharbeit", "nacharbeit", "p", "0.2"),
    ):
        s = reference[sid]
        put(user, "scenario_new_id", sid)
        put(user, "scenario_new_name", s.name)
        put(user, "scenario_new_why", s.why)
        put(user, "scenario_new_parent", BASIS)
        user.find(marker="scenario_add").click()
        await until(lambda sid=sid: value(user, "scenario_pick") == sid)
        put(user, "override_node", node)
        put(user, "override_field", field)
        put(user, "override_value", new)
        put(user, "override_why", str(s.overrides[node]["why"]))
        user.find(marker="override_set").click()
        await user.should_see(marker="override_remove")


def test_t2_rebuilt_through_the_form_gives_the_same_model_and_numbers() -> None:
    own("schema_version: 1\nmodel: x\nnodes: {}\n", "nachbau")

    async def steps(user: User) -> None:
        await open_model(user, "nachbau")
        await _build_t2(user)
        await _scenarios(user)
        user.find(marker="nav/modell").click()
        await user.should_see(marker="save_model")
        user.find(marker="save_model").click()
        await user.should_see(t("ui.saved"))

    drive(steps)
    built = files.load_model(settings.models_dir() / "nachbau.yaml")
    reference = model_from_yaml(T2.read_text("utf-8"))
    assert content_hash(built) == content_hash(reference)
    assert built.title == reference.title
    for sid in (BASIS, "b_schneller", "nacharbeit"):
        ours = simulate(compile_model(effective_model(built, sid)), n=5000).samples["ende"]
        theirs = simulate(compile_model(effective_model(reference, sid)), n=5000).samples["ende"]
        assert np.array_equal(ours, theirs), sid


def test_csv_column_becomes_empirical_distribution() -> None:
    own(
        "schema_version: 1\nmodel: eigen\nnodes:\n"
        "  x: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  y: {type: output, expr: x}\n"
    )

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        upload = element(user, "csv_file")
        assert isinstance(upload, ui.upload)
        data = SmallFileUpload("d.csv", "text/csv", b"tag;dauer\n1;3,5\n2;\n3;4\n")
        assert user.client is not None
        with user.client:
            await upload.handle_uploads([data])
        await user.should_see(marker="csv_column")
        put(user, "csv_column", "dauer")
        user.find(marker="csv_import").click()
        await user.should_see("2 Werte in „x“ übernommen (1 leere Zellen übersprungen)")
        assert "dist: empirical" in editor(user)
        assert "3.5" in editor(user)

    drive(steps)


def test_quantile_conflict_offers_piecewise_in_own_model() -> None:
    own(
        "schema_version: 1\nmodel: eigen\nnodes:\n"
        "  x: {type: uncertain, dist: normal, input: quantiles, p10: 2031, p50: 2038, p90: 2060}\n"
        "  y: {type: output, expr: x}\n"
    )

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        await user.should_see("passen nicht zu einer normal-Verteilung")
        assert not enabled(user, "to_piecewise_x")  # no made-up bounds (M5 E4, E7)
        put(user, "piecewise_p0_x", 2025.0)
        put(user, "piecewise_p100_x", 2090.0)
        assert enabled(user, "to_piecewise_x")
        user.find(marker="to_piecewise_x").click()
        await user.should_see(marker="editor")
        assert "dist: piecewise" in editor(user)
        assert "2090" in editor(user)

    drive(steps)
