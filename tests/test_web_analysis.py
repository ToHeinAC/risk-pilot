"""Analysis page of the new UI (M7 step 5)."""

from nicegui import ui
from nicegui.testing import User
from web_util import cells, drive, element, open_model, put, texts

from app.adapters import files, settings
from app.messages import t

QUESTIONS = (
    "Wie hängen die Knoten zusammen?",
    "Welche Knoten bestimmen das Ergebnis tatsächlich?",
    "Welche unsichere Eingabe verschiebt das Ergebnis am stärksten?",
    "Wie ändert sich das Ergebnis, wenn ich einen Wert gezielt verändere?",
    "Welche Eingaben laufen mit dem Ergebnis gleich?",
    "Welche Ereignisse sind wahrscheinlich und folgenreich?",
)


async def analyse(user: User, stem: str, scenario: str = "basis", n: int = 5_000) -> None:
    await open_model(user, stem)
    user.find(marker="nav/analyse").click()
    await user.should_see(marker="ana_run")
    put(user, "ana_scenario", scenario)
    put(user, "ana_n", n)
    user.find(marker="ana_run").click()
    await user.should_see(marker="ana_tabs", retries=200)


def headers(user: User, marker: str) -> list[str]:
    table = element(user, marker)
    assert isinstance(table, ui.table)
    return [str(c["label"]) for c in table.columns]


def test_analysis_page_t2_all_tabs() -> None:
    async def steps(user: User) -> None:
        await analyse(user, "t2_terminplan", "nacharbeit")
        page = texts(user)
        assert "Im Modell liegt Vorgang B in " in page
        assert "Deskriptiv: zeigt Gleichlauf im Modell" in page
        assert "keine kausale Wirkung" in page
        assert any(row[0] == "Nacharbeit an B" for row in cells(user, "ana_risk_table"))
        put(user, "graph_color", "why")
        put(user, "tornado_n", 2_000)
        await user.should_see("Der Tornado braucht 6 Läufe")
        user.find(marker="tornado_run").click()
        await user.should_see(marker="ana_tornado_table", retries=200)
        assert any(row[0] == "Vorgang C" for row in cells(user, "ana_tornado_table"))
        assert t("analysis.col_swing") in headers(user, "ana_tornado_table")
        user.find(marker="sweep_run").click()
        await user.should_see(marker="ana_sweep_table", retries=200)
        assert t("analysis.col_interval") in headers(user, "ana_sweep_table")

    drive(steps)


def test_analysis_sweep_reports_invalid_values() -> None:
    async def steps(user: User) -> None:
        await analyse(user, "t2_terminplan")
        put(user, "sweep_param", "b.sd")
        await user.should_see(marker="sweep_from")
        put(user, "sweep_from", -1.0)
        user.find(marker="sweep_run").click()
        await user.should_see("nicht zulässig", retries=100)

    drive(steps)


def test_analysis_colourings_and_undefined_risk_marked() -> None:
    async def steps(user: User) -> None:
        await analyse(user, "t2_terminplan")  # main scenario: the rework never occurs
        assert any("y nicht bestimmbar" in " ".join(r) for r in cells(user, "ana_risk_table"))
        for mode in ("sensitivity", "criticality", "why"):
            put(user, "graph_color", mode)
            await user.should_see(marker="ana_graph")

    drive(steps)


def test_analysis_without_extremum_explains_empty_criticality() -> None:
    async def steps(user: User) -> None:
        await analyse(user, "t1_faltung")
        page = texts(user)
        assert "kein max, min oder where" in page
        assert t("analysis.no_events") in page

    drive(steps)


def test_analysis_tabs_explain_question_reading_and_limit() -> None:
    async def steps(user: User) -> None:
        await analyse(user, "t2_terminplan")
        page = texts(user)
        for question in QUESTIONS:
            assert question in page
        assert "Graph:" in page  # the guide "Wann welche Auswertung?"
        labels = [str(e.text) for e in user.find(ui.expansion).elements]
        assert labels.count(t("explain.how_label")) == len(QUESTIONS)
        assert t("analysis.guide_label") in labels

    drive(steps)


def test_changed_settings_mark_the_analysis_stale() -> None:
    async def steps(user: User) -> None:
        await analyse(user, "t2_terminplan")
        put(user, "ana_n", 6_000)
        await user.should_see(t("analysis.stale"))
        await user.should_not_see(marker="ana_tabs")

    drive(steps)


def test_invalid_model_blocks_analysis() -> None:
    files.create_model_text(
        settings.models_dir(), "eigen", "schema_version: 1\nmodel: eigen\nnodes: {}\n"
    )

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        user.find(marker="nav/analyse").click()
        await user.should_see(t("ui.sim_blocked"))
        await user.should_not_see(marker="ana_run")

    drive(steps)


def test_analysis_survives_a_page_change() -> None:
    async def steps(user: User) -> None:
        await analyse(user, "t2_terminplan")
        user.find(marker="nav/modell").click()
        await user.should_see(marker="editor")
        user.find(marker="nav/analyse").click()
        await user.should_see(marker="ana_tabs")

    drive(steps)


def test_tornado_and_sweep_results_survive_a_page_change() -> None:
    async def steps(user: User) -> None:
        await analyse(user, "t2_terminplan")
        put(user, "tornado_n", 1_000)
        user.find(marker="tornado_run").click()
        await user.should_see(marker="ana_tornado_table", retries=200)
        put(user, "sweep_k", 3)
        user.find(marker="sweep_run").click()
        await user.should_see(marker="ana_sweep_table", retries=200)
        user.find(marker="nav/modell").click()
        await user.should_see(marker="editor")
        user.find(marker="nav/analyse").click()
        await user.should_see(marker="ana_tornado_table")
        await user.should_see(marker="ana_sweep_table")
        assert len(cells(user, "ana_sweep_table")) == 3

    drive(steps)
