"""Simulation and results pages of the new UI (M7 step 3)."""

from nicegui import ui
from nicegui.testing import User
from web_util import drive, element, open_model, put, texts

from app.adapters import files, runs, settings
from app.messages import t
from app.present.text import integer

NO_TARGET = (
    "schema_version: 1\nmodel: eigen\nnodes:\n"
    "  a: {type: uncertain, dist: normal, mean: 0, sd: 1}\n  k: {type: constant, value: 1}\n"
    "  y: {type: output, expr: a * k}\n"
    "scenarios:\n  s: {name: Doppelt, why: W, overrides: {k: {value: 2}}}\n"
)


async def simulate(user: User, n: int, scenario: str = "basis") -> None:
    """Run on the simulation page, then open the results."""
    user.find(marker="nav/simulation").click()
    await user.should_see(marker="sim_run")
    put(user, "sim_scenario", scenario)
    put(user, "sim_n", n)
    user.find(marker="sim_run").click()
    await user.should_see("Fertig:", retries=100)
    user.find(marker="to_results").click()
    await user.should_see(marker="save_run")


def test_t1_simulate_reports_time_and_shows_metrics_with_reference() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t1_faltung")
        user.find(marker="nav/simulation").click()
        await user.should_see(marker="sim_run")
        put(user, "sim_n", 10_000)
        user.find(marker="sim_run").click()
        await user.should_see(f"Fertig: {integer(10_000)} Iterationen in", retries=100)
        user.find(marker="to_results").click()
        await user.should_see(marker="save_run")
        page = texts(user)
        for expected in ("Mittelwert", "Median", "Im Modell liegen 90 %", "Dieses Ergebnis gilt"):
            assert expected in page
        assert f"N = {integer(10_000)}" in page
        assert "DKW-Schranke" in page  # analytic overlay of T1 (M2 AK 3)
        assert "Numerische Faltung" in page

    drive(steps)


def test_t2_answer_first_target_and_clark() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        await simulate(user, 20_000)
        await user.should_see(t("result.target_label"))  # the answer card
        page = texts(user)
        assert "Clark" in page
        assert "Im Modell wird das Ziel ≤ 30 d in" in page

    drive(steps)


def test_results_offer_three_downloads() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        await simulate(user, 2000)
        await user.should_see(t("export.title"))
        for marker, start in (
            ("export_csv", b""),
            ("export_parquet", b"PAR1"),
            ("export_html", b"<!doctype html>"),
        ):
            user.find(marker=marker).click()
            response = await user.download.next()
            assert response.content.lower().startswith(start.lower())
            assert response.content

    drive(steps)


def test_sub_scenario_in_validity_line_and_saved_meta() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        await simulate(user, 5_000, "b_schneller")
        page = texts(user)
        assert "Szenario B −3 Tage" in page
        assert "DKW-Schranke" not in page  # analytic overlay only in the main scenario
        user.find(marker="save_run").click()
        await user.should_see("Lauf gespeichert")

    drive(steps)
    meta = runs.load_run(runs.list_runs(settings.runs_dir())[0]).meta
    assert (meta["scenario_id"], meta["scenario_name"]) == ("b_schneller", "B −3 Tage")
    assert "effective_hash" in meta


def test_scenario_list_is_indented() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        user.find(marker="nav/simulation").click()
        await user.should_see(marker="sim_scenario")
        select = element(user, "sim_scenario")
        assert isinstance(select, ui.select)
        labels = list(dict(select.options).values())
        assert labels[0] == "Hauptszenario"
        assert labels[1].startswith(chr(0x2003))  # indented one level (em space)

    drive(steps)


def test_scenario_hints_reach_results_page() -> None:
    files.create_model_text(
        settings.models_dir(), "eigen", NO_TARGET.replace("value: 2", "value: 1")
    )

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        await simulate(user, 2000, "s")
        assert "denselben Wert" in texts(user)

    drive(steps)


def test_invalid_model_blocks_simulation_and_results_wait_for_a_run() -> None:
    files.create_model_text(
        settings.models_dir(), "eigen", "schema_version: 1\nmodel: eigen\nnodes: {}\n"
    )

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        user.find(marker="nav/simulation").click()
        await user.should_see(t("ui.sim_blocked"))
        await user.should_not_see(marker="sim_run")
        user.find(marker="nav/ergebnisse").click()
        await user.should_see(t("ui.no_run"))

    drive(steps)


def test_results_show_correlations_losses_horizon_and_peaks() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t4_portfolio")
        await simulate(user, 20_000)
        page = texts(user)
        assert "Erreichte Rangkorrelation" in page
        assert "Illustrative Zahlen" in page
        assert "VaR 95 %" in page
        await open_model(user, "t5_fusion")
        await simulate(user, 5_000)
        assert "nicht erreicht" in texts(user)
        assert "> Horizont" in texts(user)
        await open_model(user, "t3_bahn")
        await simulate(user, 20_000)
        assert "mehrere Gipfel" in texts(user)

    drive(steps)


def test_unchanged_copy_keeps_overlay_changed_copy_gets_notice() -> None:
    files.copy_model(settings.examples_dir() / "t1_faltung.yaml", settings.models_dir(), "meine")

    async def steps(user: User) -> None:
        await open_model(user, "meine")
        await simulate(user, 10_000)
        assert "DKW-Schranke" in texts(user)
        user.find(marker="nav/modell").click()
        await user.should_see(marker="editor")
        text = str(getattr(element(user, "editor"), "value"))  # noqa: B009
        put(user, "editor", text.replace("high: 1,", "high: 2,"))
        await simulate(user, 10_000)
        page = texts(user)
        assert "gilt für das unveränderte Tutorial" in page
        assert "DKW-Schranke" not in page

    drive(steps)
