"""Guided tour banner: five steps through the real pages, then end (M8 AK 4, E13)."""

from nicegui.testing import User
from web_util import drive, put, texts, until

from app.messages import t
from app.present import guide
from app.web import main

T2 = "t2_terminplan"


def banner(step: int) -> str:
    return t("tour.banner", step=step, total=len(guide.TOUR), text=t(guide.TOUR[step - 1].text))


async def simulate(user: User, scenario: str) -> None:
    put(user, "sim_scenario", scenario)
    put(user, "sim_n", 2000)
    user.find(marker="sim_run").click()


def test_tour_runs_through_five_steps_and_ends() -> None:
    async def steps(user: User) -> None:
        await user.open("/")
        await user.should_see(marker="tour_start")
        await user.should_not_see(marker="tour_banner")
        user.find(marker="tour_start").click()
        await user.should_see(banner(1))
        user.find(marker=f"open_{T2}").click()
        await user.should_see(banner(2))
        user.find(marker="tour_go").click()
        await user.should_see(marker="sim_run")
        await simulate(user, "basis")
        await until(lambda: banner(3) in texts(user))
        await simulate(user, "nacharbeit")
        await until(lambda: banner(4) in texts(user))
        user.find(marker="tour_go").click()
        await user.should_see(banner(5))
        user.find(marker="tour_go").click()
        await user.should_see(t("tour.done"))
        user.find(marker="tour_end").click()
        await until(lambda: t("tour.done") not in texts(user))
        user.find(marker="nav/glossar").click()
        await user.should_see(t("guide.purpose_glossar"))
        await user.should_not_see(marker="tour_banner")

    drive(steps)


def test_banner_shows_on_every_page_while_the_tour_runs() -> None:
    async def steps(user: User) -> None:
        await user.open("/")
        user.find(marker="tour_start").click()
        await user.should_see(banner(1))
        for path, _key, _icon in main.PAGES:
            user.find(marker=f"nav{path}").click()
            await user.should_see(t(guide.PAGES[path].purpose))
            assert banner(1) in texts(user), path

    drive(steps)
