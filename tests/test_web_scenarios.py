"""Scenario and comparison pages of the new UI (M7 step 4)."""

from pathlib import Path

from nicegui.testing import User
from web_util import cells, drive, element, enabled, open_model, put, texts, until, value

from app.adapters import files, settings
from app.messages import t

ROOT = Path(__file__).resolve().parent.parent
T2 = ROOT / "examples" / "t2_terminplan.yaml"
NO_TARGET = (
    "schema_version: 1\nmodel: eigen\nnodes:\n"
    "  a: {type: uncertain, dist: normal, mean: 0, sd: 1}\n  k: {type: constant, value: 1}\n"
    "  y: {type: output, expr: a * k}\n"
    "scenarios:\n  s: {name: Doppelt, why: W, overrides: {k: {value: 2}}}\n"
)


async def scenarios(user: User, stem: str, pick: str | None = None) -> None:
    await open_model(user, stem)
    user.find(marker="nav/szenarien").click()
    await user.should_see(marker="scenario_pick")
    if pick is not None:
        put(user, "scenario_pick", pick)
        await user.should_see(marker="scenario_diff")


async def override(user: User, node: str, field: str, new: str, why: str = "") -> None:
    put(user, "override_node", node)
    put(user, "override_field", field)
    put(user, "override_value", new)
    put(user, "override_why", why)
    user.find(marker="override_set").click()


async def editor_text(user: User) -> str:
    user.find(marker="nav/modell").click()
    await user.should_see(marker="editor")
    return str(value(user, "editor"))


def test_t2_scenario_tree_and_diff_read_only() -> None:
    async def steps(user: User) -> None:
        await scenarios(user, "t2_terminplan", "b_schneller")
        page = texts(user)
        assert "B −3 Tage" in page
        assert "mit Nacharbeit" in page
        assert "Ein zweites Team" in page  # the scenario's reason
        assert cells(user, "scenario_diff")[0][:4] == ("b", "mean", "15", "12")
        await user.should_not_see(marker="scenario_add")
        await user.should_see(t("scen.readonly"))

    drive(steps)


def test_edit_scenarios_in_own_copy() -> None:
    files.copy_model(T2, settings.models_dir(), "plan")

    async def steps(user: User) -> None:
        await scenarios(user, "plan")
        put(user, "scenario_new_id", "teuer")
        put(user, "scenario_new_name", "Teurer Plan")
        put(user, "scenario_new_why", "Test")
        user.find(marker="scenario_add").click()
        await user.should_see(marker="override_set")
        assert value(user, "scenario_pick") == "teuer"
        await override(user, "c", "mean", "30", "Angebot")
        await user.should_see(marker="override_remove")
        assert ("c", "mean", "24", "30", "Angebot", "geändert") in cells(user, "scenario_diff")
        user.find(marker="scenario_duplicate").click()
        await user.should_see("teuer_kopie")
        user.find(marker="scenario_detach").click()
        await user.should_see(marker="scenario_detach_confirm")
        user.find(marker="scenario_detach_confirm").click()
        await user.should_see(t("scen.detached"))
        text = await editor_text(user)
        assert "teuer:" in text
        assert "detached_from: basis" in text
        assert text.startswith("# Kopie von t2_terminplan")

    drive(steps)


def test_remove_override_and_comments_stay() -> None:
    files.copy_model(T2, settings.models_dir(), "plan")

    async def steps(user: User) -> None:
        await scenarios(user, "plan", "b_schneller")
        await override(user, "c", "sd", "5")
        await until(lambda: len(cells(user, "scenario_diff")) == 2)
        put(user, "override_remove_pick", "b.mean")
        user.find(marker="override_remove").click()
        await until(lambda: len(cells(user, "scenario_diff")) == 1)
        assert cells(user, "scenario_diff")[0][:2] == ("c", "sd")
        text = await editor_text(user)
        assert "sd: 5" in text
        for line in T2.read_text("utf-8").splitlines():
            if line.lstrip().startswith("#"):
                assert line in text

    drive(steps)


def test_scenario_form_refuses_invalid_edit() -> None:
    files.create_model_text(settings.models_dir(), "eigen", NO_TARGET)

    async def steps(user: User) -> None:
        await scenarios(user, "eigen", "s")
        await override(user, "k", "mean", "3")
        await user.should_see("nicht überschreiben", retries=20)
        assert "Doppelt" in texts(user)  # page still usable, model unchanged
        put(user, "override_value", "")
        user.find(marker="override_set").click()
        await user.should_see(t("scen.value_missing"))

    drive(steps)


def test_invalid_model_has_no_scenario_editing() -> None:
    files.create_model_text(
        settings.models_dir(), "eigen", "schema_version: 1\nmodel: eigen\nnodes: {}\n"
    )

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        user.find(marker="nav/szenarien").click()
        await user.should_see(t("scen.invalid_model"))
        await user.should_not_see(marker="scenario_pick")

    drive(steps)


async def compare(user: User, others: list[str], n: int) -> None:
    user.find(marker="nav/vergleich").click()
    await user.should_see(marker="compare_run")
    assert not enabled(user, "compare_run")  # nothing to compare with yet
    put(user, "compare_others", others)
    put(user, "compare_n", n)
    assert enabled(user, "compare_run")
    user.find(marker="compare_run").click()
    await user.should_see(t("compare.d_table"), retries=200)


def test_compare_page_t2() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        await compare(user, ["b_schneller", "nacharbeit"], 10_000)
        page = texts(user)
        assert "besser als „Hauptszenario“" in page
        assert "in 0 % schlechter" in page  # B −3 Tage is never worse (M3 AK 6)
        assert "Szenario Hauptszenario" in page  # validity line of the reference
        assert any(row[0] == t("result.mean") for row in cells(user, "compare_ende_b_schneller"))

    drive(steps)


def test_compare_without_direction_shows_shares_and_d_statistics() -> None:
    files.create_model_text(settings.models_dir(), "eigen", NO_TARGET)

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        await compare(user, ["s"], 2_000)
        assert "kleiner als „Hauptszenario“" in texts(user)
        assert any(row[0] == "Anteil B = A" for row in cells(user, "compare_d_y_s"))

    drive(steps)


def test_stale_comparison_hidden_after_model_change() -> None:
    files.create_model_text(settings.models_dir(), "eigen", NO_TARGET)

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        await compare(user, ["s"], 2_000)
        await editor_text(user)
        put(user, "editor", NO_TARGET.replace("value: 2", "value: 3"))
        user.find(marker="nav/vergleich").click()
        await user.should_see(t("compare.stale"))
        assert "kleiner als" not in texts(user)

    drive(steps)


def test_compare_needs_a_sub_scenario() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t1_faltung")
        user.find(marker="nav/vergleich").click()
        await user.should_see(t("compare.need_two"))
        await user.should_not_see(marker="compare_run")

    drive(steps)


def test_reference_is_not_offered_as_partner() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        user.find(marker="nav/vergleich").click()
        await user.should_see(marker="compare_run")
        put(user, "compare_others", ["b_schneller"])
        put(user, "compare_ref", "b_schneller")
        assert value(user, "compare_others") == []
        assert "b_schneller" not in dict(getattr(element(user, "compare_others"), "options"))  # noqa: B009
        assert not enabled(user, "compare_run")

    drive(steps)
