"""Evaluation blocks: question, reading example, chart, reading and limit (M8 AK 2, edge cases)."""

from nicegui import ui
from nicegui.testing import User
from test_web_analysis import analyse
from web_util import drive, open_model, put, texts

from app.adapters import files, settings
from app.messages import t

ANALYSIS = ("graph", "crit", "tornado", "sweep", "rho", "risk")
CONSTANT = (
    "schema_version: 1\nmodel: fest\nnodes:\n  k: {type: constant, value: 2}\n"
    "  s: {type: constant, value: 1}\n  y: {type: output, expr: k * s}\n"
    "scenarios:\n  d: {name: Doppelt, why: W, overrides: {k: {value: 4}}}\n"
)


def how_labels(user: User) -> list[str]:
    return [str(e.text) for e in user.find(ui.expansion).elements]


def test_results_block_reads_the_run() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        user.find(marker="nav/simulation").click()
        await user.should_see(marker="sim_run")
        put(user, "sim_n", 5_000)
        user.find(marker="sim_run").click()
        await user.should_see("Fertig:", retries=100)
        user.find(marker="to_results").click()
        await user.should_see(marker="reading_result")
        page = texts(user)
        assert t("explain.result.question") in page
        assert "Im Modell liegt Projektende in der Hälfte der Iterationen" in page
        assert t("explain.how_label") in how_labels(user)

    drive(steps)


def test_compare_block_reads_the_mean_difference() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        user.find(marker="nav/vergleich").click()
        await user.should_see(marker="compare_run")
        put(user, "compare_others", ["b_schneller"])
        put(user, "compare_n", 5_000)
        user.find(marker="compare_run").click()
        await user.should_see(marker="reading_compare", retries=200)
        assert "Im Modell liegt Projektende in „B −3 Tage“ im Mittel" in texts(user)
        assert t("explain.compare.question") in texts(user)

    drive(steps)


def test_every_analysis_tab_is_an_evaluation_block() -> None:
    async def steps(user: User) -> None:
        await analyse(user, "t2_terminplan", "nacharbeit")
        page = texts(user)
        for key in ANALYSIS:
            assert t(f"explain.{key}.question") in page, key
        for key in ("graph", "crit", "rho", "risk"):
            await user.should_see(marker=f"reading_{key}")
        assert how_labels(user).count(t("explain.how_label")) == len(ANALYSIS)
        put(user, "tornado_n", 1_000)
        user.find(marker="tornado_run").click()
        await user.should_see(marker="reading_tornado", retries=200)
        put(user, "sweep_k", 3)
        user.find(marker="sweep_run").click()
        await user.should_see(marker="reading_sweep", retries=200)

    drive(steps)


def test_empty_evaluations_give_their_reason() -> None:
    files.create_model_text(settings.models_dir(), "fest", CONSTANT)

    async def steps(user: User) -> None:
        await analyse(user, "fest")
        page = texts(user)
        assert t("analysis.no_events") in page
        assert t("analysis.crit_no_extremum") in page
        for key in ("tornado", "sweep", "rho"):
            await user.should_see(marker=f"empty_{key}")
        await user.should_not_see(marker="tornado_run")

    drive(steps)


def test_compare_without_sub_scenario_says_what_to_do() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t1_faltung")
        user.find(marker="nav/vergleich").click()
        await user.should_see(t("compare.need_two"))

    drive(steps)
