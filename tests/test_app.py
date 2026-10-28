"""The Streamlit app driven by AppTest, offline and without a server (M2 AK 1-8, 11)."""

import hashlib
import os
import signal
from pathlib import Path
from typing import cast

import pytest
from streamlit.testing.v1 import AppTest

from app.adapters import files, settings

ROOT = Path(__file__).resolve().parent.parent
MAIN = str(ROOT / "src" / "app" / "ui" / "main.py")
T2 = ROOT / "examples" / "t2_terminplan.yaml"


def start() -> AppTest:
    at = AppTest.from_file(MAIN, default_timeout=60).run()
    assert not at.exception
    return at


def texts(at: AppTest) -> str:
    parts = [m.value for m in (*at.title, *at.subheader, *at.markdown, *at.caption)]
    parts += [e.value for e in (*at.success, *at.info, *at.warning, *at.error)]
    return "\n".join(str(p) for p in parts)


def go(at: AppTest, page: str) -> AppTest:
    at.switch_page(f"pages/{page}.py").run()
    assert not at.exception
    return at


def has_button(at: AppTest, key: str) -> bool:
    return any(b.key == key for b in at.button)


def open_model(at: AppTest, stem: str) -> AppTest:
    at.button(key=f"open_{stem}").click().run()
    assert not at.exception
    return go(at, "modell")


def simulate(at: AppTest, n: int) -> AppTest:
    go(at, "simulation")
    at.number_input(key="sim_n").set_value(n).run()
    at.button(key="sim_run").click().run()
    assert not at.exception
    return go(at, "ergebnisse")


def test_start_page_lists_tutorials_and_learning_path() -> None:
    at = start()
    page = texts(at)
    assert "Lernpfad" in page
    assert has_button(at, "open_t1_faltung")
    assert has_button(at, "open_t2_terminplan")


def test_t1_open_simulate_and_show_metrics() -> None:
    at = open_model(start(), "t1_faltung")
    assert "Gültig – 3 Knoten, 1 Ausgabe" in texts(at)
    page = texts(simulate(at, 10_000))
    for expected in ("Mittelwert", "Median", "Im Modell liegen 90 %", "Dieses Ergebnis gilt für"):
        assert expected in page
    assert "N = 10 000" in page
    assert "DKW-Schranke" in page  # analytic overlay of T1 (AK 3)
    assert "Numerische Faltung" in page


def test_t2_shows_clark_and_target_sentence() -> None:
    page = texts(simulate(open_model(start(), "t2_terminplan"), 20_000))
    assert "Clark" in page
    assert "Im Modell wird das Ziel ≤ 30 d in" in page


def test_tutorial_is_read_only() -> None:
    at = open_model(start(), "t1_faltung")
    assert at.text_area(key="editor").disabled
    assert not has_button(at, "save_model")


def test_copy_template_keeps_source_and_refuses_existing_name() -> None:
    before = hashlib.sha256(T2.read_bytes()).hexdigest()
    at = start()
    at.text_input(key="copy_id_t2_terminplan").input("mein_plan").run()
    at.button(key="copy_t2_terminplan").click().run()
    assert (settings.models_dir() / "mein_plan.yaml").is_file()
    assert hashlib.sha256(T2.read_bytes()).hexdigest() == before
    at.text_input(key="copy_id_t2_terminplan").input("mein_plan").run()
    at.button(key="copy_t2_terminplan").click().run()
    assert not at.exception
    assert "mein_plan_2" in texts(at)


def own_model(text: str) -> AppTest:
    files.create_model_text(settings.models_dir(), "eigen", text)
    at = open_model(start(), "eigen")
    assert not at.text_area(key="editor").disabled
    return at


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
def test_validation_messages_in_german_without_crash(text: str, expected: str) -> None:
    at = own_model("schema_version: 1\nmodel: eigen\nnodes:\n  y: {type: output, expr: '1'}\n")
    at.text_area(key="editor").input(text).run()
    assert not at.exception
    assert expected in texts(at)
    go(at, "simulation")
    assert not has_button(at, "sim_run")


def test_edit_and_save_own_model() -> None:
    at = own_model("schema_version: 1\nmodel: eigen\nnodes:\n  y: {type: output, expr: '1'}\n")
    new = "schema_version: 1\nmodel: eigen\nnodes:\n  y: {type: output, expr: '2'}\n"
    at.text_area(key="editor").input(new).run()
    assert "Ungespeicherte Änderungen" in texts(at)
    at.button(key="save_model").click().run()
    assert not at.exception
    assert files.read_text(settings.models_dir() / "eigen.yaml") == new


def test_saved_run_reloads_with_same_numbers() -> None:
    at = simulate(open_model(start(), "t2_terminplan"), 5_000)
    shown = [m.value for m in at.markdown if "Mittelwert" in str(m.value)]
    at.button(key="save_run").click().run()
    assert not at.exception
    go(at, "laeufe")
    at.button(key="load_run_0").click().run()
    assert not at.exception
    reloaded = [m.value for m in at.markdown if "Mittelwert" in str(m.value)]
    assert reloaded == shown
    assert "weichen ab" not in texts(at)


def test_exit_sends_sigterm_to_own_pid(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[int, int]] = []
    monkeypatch.setattr(os, "kill", lambda pid, sig: calls.append((pid, sig)))
    at = start()
    at.button(key="exit").click().run()
    assert calls == []
    at.button(key="exit_confirm").click().run()
    assert calls == [(os.getpid(), signal.SIGTERM)]


def test_lesson_turn_knob_shows_before_after() -> None:
    at = go(start(), "lernpfad")
    at.selectbox(key="lesson").set_value("a02_parallel_und").run()
    assert "Merge-Bias" in texts(at)
    at.radio(key="prediction_a02_parallel_und").set_value("Es wird später").run()
    at.button(key="lesson_run").click().run()
    assert not at.exception
    at.select_slider(key="knob_a02_parallel_und").set_value(3.0).run()
    at.button(key="lesson_turn").click().run()
    assert not at.exception
    page = texts(at)
    assert "Vorher" in page
    assert "Deine Vorhersage: Es wird später" in page
    table = next(str(m.value) for m in at.markdown if "| Vorher" in str(m.value))
    mean_row = next(line for line in table.splitlines() if line.startswith("| Mittelwert"))
    assert "| +" in mean_row  # the mean rises with a third parallel path
    assert "erfüllt" in page


def test_lesson_copy_as_template() -> None:
    at = go(start(), "lernpfad")
    at.selectbox(key="lesson").set_value("a05_verzweigung").run()
    at.text_input(key="lesson_copy_id").input("meine_nacharbeit").run()
    at.button(key="lesson_copy").click().run()
    assert not at.exception
    assert (
        files.load_model(settings.models_dir() / "meine_nacharbeit.yaml").model
        == "meine_nacharbeit"
    )


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


@pytest.mark.parametrize("lesson_id", LESSON_IDS)
def test_every_lesson_runs_and_turns_without_error(lesson_id: str) -> None:
    at = go(start(), "lernpfad")
    at.selectbox(key="lesson").set_value(lesson_id).run()
    at.button(key="lesson_run").click().run()
    assert not at.exception
    knob = at.select_slider(key=f"knob_{lesson_id}")
    current = float(cast(float, knob.value))
    other = next(v for v in knob.options if float(v) != current)
    knob.set_value(float(other)).run()
    at.button(key="lesson_turn").click().run()
    assert not at.exception
    page = texts(at)
    assert "Faustregel" in page
    assert "nicht erfüllt" not in page


def lesson(at: AppTest, lesson_id: str, turn_to: float) -> AppTest:
    go(at, "lernpfad")
    at.selectbox(key="lesson").set_value(lesson_id).run()
    at.button(key="lesson_run").click().run()
    at.select_slider(key=f"knob_{lesson_id}").set_value(turn_to).run()
    at.button(key="lesson_turn").click().run()
    assert not at.exception
    return at


def test_prediction_resolved_from_simulation_not_manifest() -> None:
    at = go(start(), "lernpfad")
    at.selectbox(key="lesson").set_value("a02_parallel_und").run()
    at.radio(key="prediction_a02_parallel_und").set_value("Es wird später").run()
    at.button(key="lesson_run").click().run()
    at.select_slider(key="knob_a02_parallel_und").set_value(1.0).run()
    at.button(key="lesson_turn").click().run()
    page = texts(at)
    assert "Deine Vorhersage: Es wird später – Ergebnis: Mittelwert sinkt um" in page


def test_lesson_shows_validity_lines_and_progress() -> None:
    at = lesson(start(), "a05_verzweigung", 0.5)
    page = texts(at)
    assert page.count("Dieses Ergebnis gilt für Modell a05_verzweigung") >= 2
    assert "Stellschraube Wahrscheinlichkeit der Nacharbeit = 0,5" in page
    assert "1 von 11 Lektionen durchgearbeitet" in page


def test_lesson_file_stays_byte_identical() -> None:
    path = settings.examples_dir() / "lernpfad" / "a05_verzweigung.yaml"
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    lesson(start(), "a05_verzweigung", 0.5)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before


def test_lesson_reference_curve_in_comparison() -> None:
    at = lesson(start(), "a02_parallel_und", 3.0)
    assert "erfüllt" in texts(at)


def test_unchanged_copy_keeps_overlay_changed_copy_gets_notice() -> None:
    at = start()
    at.text_input(key="copy_id_t1_faltung").input("meine_faltung").run()
    at.button(key="copy_t1_faltung").click().run()
    at = open_model(start(), "meine_faltung")
    assert "DKW-Schranke" in texts(simulate(at, 10_000))
    go(at, "modell")
    changed = str(at.text_area(key="editor").value).replace("high: 1,", "high: 2,")
    at.text_area(key="editor").input(changed).run()
    page = texts(simulate(at, 10_000))
    assert "gilt für das unveränderte Tutorial" in page
    assert "DKW-Schranke" not in page


def test_tampered_run_summary_is_reported() -> None:
    at = simulate(open_model(start(), "t2_terminplan"), 5_000)
    at.button(key="save_run").click().run()
    folder = next(settings.runs_dir().iterdir())
    summary = folder / "summary.json"
    summary.write_text(
        summary.read_text(encoding="utf-8").replace('"n": 5000', '"n": 4999', 1), encoding="utf-8"
    )
    go(at, "laeufe")
    at.button(key="load_run_0").click().run()
    assert not at.exception
    assert "weichen ab" in texts(at)


def test_corrupt_run_folder_shows_message_not_crash() -> None:
    broken = settings.runs_dir() / "20261028T000000Z_t2_terminplan_deadbeef"
    broken.mkdir(parents=True)
    (broken / "meta.json").write_text('{"model_id": "t2_terminplan"}', encoding="utf-8")
    at = open_model(start(), "t2_terminplan")
    go(at, "laeufe")
    at.button(key="load_run_0").click().run()
    assert not at.exception
    assert "Unerwarteter Fehler" in texts(at)


def test_non_utf8_model_file_does_not_crash_start() -> None:
    settings.models_dir().mkdir(parents=True, exist_ok=True)
    (settings.models_dir() / "kaputt.yaml").write_bytes(b"model: \xff\xfe\n")
    at = AppTest.from_file(MAIN, default_timeout=60).run()
    assert not at.exception


def test_save_conflict_offers_overwrite_and_invalid_draft_warns() -> None:
    at = own_model("schema_version: 1\nmodel: eigen\nnodes:\n  y: {type: output, expr: '1'}\n")
    (settings.models_dir() / "eigen.yaml").write_text("extern geändert\n", encoding="utf-8")
    at.text_area(key="editor").input("schema_version: 1\nmodel: eigen\nnodes: [\n").run()
    at.button(key="save_model").click().run()
    assert "verändert" in texts(at)
    at.button(key="save_force").click().run()
    assert not at.exception
    assert files.read_text(settings.models_dir() / "eigen.yaml").endswith("nodes: [\n")
    assert "ungültig" in texts(at)


def test_model_page_offers_copy_for_tutorial() -> None:
    at = open_model(start(), "t2_terminplan")
    at.text_input(key="copy_id_modell").input("aus_modellseite").run()
    at.button(key="copy_modell").click().run()
    assert (settings.models_dir() / "aus_modellseite.yaml").is_file()


def test_simulation_reports_run_time() -> None:
    at = open_model(start(), "t1_faltung")
    go(at, "simulation")
    at.number_input(key="sim_n").set_value(10_000).run()
    at.button(key="sim_run").click().run()
    assert " s." in texts(at)
    assert "Fertig: 10 000 Iterationen in" in texts(at)


def test_editor_draft_survives_page_change() -> None:
    at = own_model("schema_version: 1\nmodel: eigen\nnodes:\n  y: {type: output, expr: '1'}\n")
    draft = "schema_version: 1\nmodel: eigen\nnodes:\n  y: {type: output, expr: '7'}\n"
    at.text_area(key="editor").input(draft).run()
    go(at, "simulation")
    go(at, "modell")
    assert at.text_area(key="editor").value == draft
    assert "Ungespeicherte Änderungen" in texts(at)
