"""Learning path and stored runs of the new UI (M7 step 6)."""

import hashlib
from typing import Any

import pytest
from nicegui.testing import User
from web_util import cells, drive, element, open_model, put, texts, value

from app.adapters import files, runs, settings
from app.messages import t
from app.model.compile import model_hash

T2 = settings.examples_dir() / "t2_terminplan.yaml"
LESSON_IDS = [
    "a01_serie",
    "a02_parallel_und",
    "a03_parallel_oder",
    "a04_k_von_n",
    "a05_verzweigung",
    "a06_schwelle",
    "a07_bedingt",
    "a08_kette",
    "a09_jensen",
    "a10_gemeinsame_ursache",
    "a11_zusammenspiel",
]


async def simulate_and_save(user: User, n: int, scenario: str = "basis") -> str:
    """Simulate T2, save the run; returns the answer sentences on the results page."""
    await open_model(user, "t2_terminplan")
    user.find(marker="nav/simulation").click()
    await user.should_see(marker="sim_run")
    put(user, "sim_scenario", scenario)
    put(user, "sim_n", n)
    user.find(marker="sim_run").click()
    await user.should_see("Fertig:", retries=100)
    user.find(marker="to_results").click()
    await user.should_see(marker="save_run")
    shown = answers(user)
    user.find(marker="save_run").click()
    await user.should_see("Lauf gespeichert")
    return shown


def answers(user: User) -> str:
    """The answer sentences, sorted (the element order of a page is not fixed)."""
    lines = {line for line in texts(user).splitlines() if line.startswith("Im Modell")}
    return "\n".join(sorted(lines))


async def load_first_run(user: User) -> None:
    user.find(marker="nav/laeufe").click()
    await user.should_see(marker="load_run_0")
    user.find(marker="load_run_0").click()


def test_saved_run_reloads_with_same_numbers() -> None:
    async def steps(user: User) -> None:
        shown = await simulate_and_save(user, 5_000)
        await load_first_run(user)
        await user.should_see(t("web.reading"))
        assert answers(user) == shown
        assert shown
        assert "weichen ab" not in texts(user)

    drive(steps)


def test_reloaded_run_keeps_scenario_and_full_model_hash() -> None:
    async def steps(user: User) -> None:
        await simulate_and_save(user, 2_000, "b_schneller")
        await load_first_run(user)
        await user.should_see(t("web.reading"))
        assert "Szenario B −3 Tage" in texts(user)
        user.find(marker="nav/ergebnisse").click()  # the loaded run is the current run
        await user.should_see("Szenario B −3 Tage")

    drive(steps)
    meta = runs.load_run(runs.list_runs(settings.runs_dir())[0]).meta
    full = model_hash(files.load_model(T2))
    assert meta["model_hash"] == full
    assert meta["effective_hash"] != full


def test_tampered_run_summary_is_reported() -> None:
    async def steps(user: User) -> None:
        await simulate_and_save(user, 5_000)
        summary = next(settings.runs_dir().iterdir()) / "summary.json"
        text = summary.read_text(encoding="utf-8").replace('"n": 5000', '"n": 4999', 1)
        summary.write_text(text, encoding="utf-8")
        await load_first_run(user)
        await user.should_see("weichen ab")

    drive(steps)


def test_corrupt_run_folder_shows_message_not_crash() -> None:
    broken = settings.runs_dir() / "20261028T000000Z_t2_terminplan_deadbeef"
    broken.mkdir(parents=True)
    (broken / "meta.json").write_text('{"model_id": "t2_terminplan"}', encoding="utf-8")

    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        await load_first_run(user)
        await user.should_see("Unerwarteter Fehler")
        await user.should_see(marker="load_run_0")  # page still usable

    drive(steps)


def test_no_runs_yet() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        user.find(marker="nav/laeufe").click()
        await user.should_see(t("ui.no_runs"))

    drive(steps)


async def lesson(user: User, lesson_id: str) -> None:
    await user.open("/")
    user.find(marker="open_lernpfad").click()
    await user.should_see(marker=f"lesson/{lesson_id}")
    user.find(marker=f"lesson/{lesson_id}").click()
    await user.should_see(marker="lesson_run")
    await user.should_see(marker=f"lesson_copy_id_{lesson_id}")


async def run_and_turn(user: User, lesson_id: str, turn_to: float) -> None:
    user.find(marker="lesson_run").click()
    await user.should_see(marker=f"knob_{lesson_id}", retries=200)
    put(user, f"knob_{lesson_id}", turn_to)
    user.find(marker="lesson_turn").click()
    await user.should_see(marker="lesson_compare", retries=200)


def test_lesson_turn_knob_shows_before_after() -> None:
    async def steps(user: User) -> None:
        await lesson(user, "a02_parallel_und")
        assert "Merge-Bias" in texts(user)
        put(user, "prediction_a02_parallel_und", "Es wird später")
        await run_and_turn(user, "a02_parallel_und", 3.0)
        page = texts(user)
        assert "Deine Vorhersage: Es wird später" in page
        assert "erfüllt" in page
        mean = next(r for r in cells(user, "lesson_compare") if r[0] == t("result.mean"))
        assert mean[3].startswith("+")  # the mean rises with a third parallel path

    drive(steps)


def test_prediction_resolved_from_simulation_not_manifest() -> None:
    async def steps(user: User) -> None:
        await lesson(user, "a02_parallel_und")
        put(user, "prediction_a02_parallel_und", "Es wird später")
        await run_and_turn(user, "a02_parallel_und", 1.0)
        expected = "Deine Vorhersage: Es wird später – Ergebnis: Mittelwert sinkt um"
        assert expected in texts(user)

    drive(steps)


def test_lesson_shows_validity_lines_and_progress() -> None:
    path = settings.examples_dir() / "lernpfad" / "a05_verzweigung.yaml"
    before = hashlib.sha256(path.read_bytes()).hexdigest()

    async def steps(user: User) -> None:
        await lesson(user, "a05_verzweigung")
        await run_and_turn(user, "a05_verzweigung", 0.5)
        page = texts(user)
        assert page.count("Dieses Ergebnis gilt für Modell a05_verzweigung") >= 2
        assert "Stellschraube Wahrscheinlichkeit der Nacharbeit = 0,5" in page
        assert "1 von 11 Lektionen durchgearbeitet" in page
        assert t("lesson.done").strip(" ·") in page  # the mark in the lesson list

    drive(steps)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before  # lesson file untouched


def test_lesson_copy_as_template_and_name_follows_lesson() -> None:
    async def steps(user: User) -> None:
        await lesson(user, "a01_serie")
        assert value(user, "lesson_copy_id_a01_serie") == "a01_serie_eigen"
        user.find(marker="lesson/a05_verzweigung").click()
        await user.should_see(marker="lesson_copy_id_a05_verzweigung")
        await user.should_not_see(marker="lesson_copy_id_a01_serie")
        put(user, "lesson_copy_id_a05_verzweigung", "meine_nacharbeit")
        user.find(marker="lesson_copy").click()
        await user.should_see(t("ui.copied", name="meine_nacharbeit"))

    drive(steps)
    copied = files.load_model(settings.models_dir() / "meine_nacharbeit.yaml")
    assert copied.model == "meine_nacharbeit"


@pytest.mark.parametrize("lesson_id", LESSON_IDS)
def test_every_lesson_runs_and_turns_without_error(lesson_id: str) -> None:
    async def steps(user: User) -> None:
        await lesson(user, lesson_id)
        user.find(marker="lesson_run").click()
        await user.should_see(marker=f"knob_{lesson_id}", retries=200)
        current = value(user, f"knob_{lesson_id}")
        knob: Any = element(user, f"knob_{lesson_id}")
        options = list(knob.options)
        other = next(v for v in options if float(v) != float(current))
        put(user, f"knob_{lesson_id}", other)
        user.find(marker="lesson_turn").click()
        await user.should_see(marker="lesson_compare", retries=200)
        page = texts(user)
        assert "Faustregel" in page
        assert "nicht erfüllt" not in page

    drive(steps)
