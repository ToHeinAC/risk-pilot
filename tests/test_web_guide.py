"""Page header of the new UI: title, purpose and next step on every page (M8 AK 1)."""

from nicegui.testing import User
from web_util import drive, open_model, texts

from app.messages import t
from app.present import guide
from app.web import main


def test_navigation_and_page_directory_match() -> None:
    assert {path for path, _key, _icon in main.PAGES} == set(guide.PAGES)


def test_every_page_starts_with_purpose_and_next_step() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        for path, _key, _icon in main.PAGES:
            user.find(marker=f"nav{path}").click()
            await user.should_see(t(guide.PAGES[path].purpose))
            assert t("guide.next_label") in texts(user), path

    drive(steps)


def test_next_step_link_changes_with_the_state() -> None:
    async def steps(user: User) -> None:
        await user.open("/ergebnisse")
        await user.should_see(t("guide.next_open"))
        user.find(marker="next_step").click()
        await user.should_see(marker="open_t2_terminplan")
        await open_model(user, "t2_terminplan")
        user.find(marker="nav/ergebnisse").click()
        await user.should_see(t("guide.next_simulate"))
        user.find(marker="next_step").click()
        await user.should_see(marker="sim_run")

    drive(steps)


def test_page_title_appears_once() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        user.find(marker="nav/simulation").click()
        await user.should_see(t("guide.purpose_simulation"))
        assert texts(user).splitlines().count(t("ui.page_simulation")) == 1

    drive(steps)
