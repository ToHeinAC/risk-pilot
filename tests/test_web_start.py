"""Start page of the new UI (M7 step 2): tutorials, own models, copy, new model."""

import hashlib
from pathlib import Path

from nicegui.testing import User
from web_util import drive, open_model, put, texts

from app.adapters import files, settings
from app.messages import t

ROOT = Path(__file__).resolve().parent.parent
T2 = ROOT / "examples" / "t2_terminplan.yaml"


def test_start_lists_tutorials_and_learning_path() -> None:
    async def steps(user: User) -> None:
        await user.open("/")
        await user.should_see(t("ui.page_lernpfad"))
        for stem in ("t1_faltung", "t2_terminplan", "t3_bahn", "t4_portfolio", "t5_fusion"):
            await user.should_see(marker=f"open_{stem}")
        await user.should_see(t("ui.no_own_models"))

    drive(steps)


def test_open_tutorial_shows_model_page_and_name() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t1_faltung")
        await user.should_see("Gültig – 3 Knoten, 1 Ausgabe")
        await user.should_see("t1_faltung.yaml")

    drive(steps)


def test_copy_template_keeps_source_and_refuses_existing_name() -> None:
    before = hashlib.sha256(T2.read_bytes()).hexdigest()

    async def steps(user: User) -> None:
        await user.open("/")
        put(user, "copy_id_t2_terminplan", "mein_plan")
        user.find(marker="copy_t2_terminplan").click()
        await user.should_see(t("ui.copied", name="mein_plan"))
        await user.should_see(marker="open_mein_plan")  # listed under own models at once
        put(user, "copy_id_t2_terminplan", "mein_plan")
        user.find(marker="copy_t2_terminplan").click()
        await user.should_see("mein_plan_2")

    drive(steps)
    assert (settings.models_dir() / "mein_plan.yaml").is_file()
    assert hashlib.sha256(T2.read_bytes()).hexdigest() == before


def test_new_model_opens_empty_in_the_form() -> None:
    async def steps(user: User) -> None:
        await user.open("/")
        put(user, "new_model_id", "leer")
        user.find(marker="new_model_create").click()
        await user.should_see(marker="editor")
        assert "noch keine Knoten" in texts(user)

    drive(steps)
    assert (settings.models_dir() / "leer.yaml").is_file()


def test_tutorials_t3_to_t5_copy_as_illustrative() -> None:
    async def steps(user: User) -> None:
        await user.open("/")
        for stem in ("t3_bahn", "t4_portfolio", "t5_fusion"):
            put(user, f"copy_id_{stem}", f"meine_{stem}")
            user.find(marker=f"copy_{stem}").click()
            await user.should_see(t("ui.copied", name=f"meine_{stem}"))
        await open_model(user, "t4_portfolio")
        await user.should_see(t("lesson.illustrative"))

    drive(steps)
    for stem in ("t3_bahn", "t4_portfolio", "t5_fusion"):
        assert files.load_model(settings.models_dir() / f"meine_{stem}.yaml").illustrative


def test_unreadable_model_file_does_not_break_start() -> None:
    settings.models_dir().mkdir(parents=True, exist_ok=True)
    (settings.models_dir() / "kaputt.yaml").write_bytes(b"model: \xff\xfe\n")

    async def steps(user: User) -> None:
        await user.open("/")
        await user.should_see(marker="open_kaputt")

    drive(steps)
