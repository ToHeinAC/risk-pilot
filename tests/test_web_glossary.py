"""Glossary page and tooltips in the new UI (M8 AK 3)."""

from nicegui import ui
from nicegui.testing import User
from web_util import drive, open_model, put, texts

from app.messages import t
from app.present import glossary


def tooltips(user: User) -> list[str]:
    try:
        return [str(e.text) for e in user.find(ui.tooltip).elements]
    except AssertionError:
        return []


def test_glossary_page_lists_every_term() -> None:
    async def steps(user: User) -> None:
        await user.open("/")
        user.find(marker="nav/glossar").click()
        await user.should_see(marker="glossar_filter")
        page = texts(user)
        for term in glossary.TERMS:
            assert term.label in page, term.key
            assert term.short in page, term.key

    drive(steps)


def test_glossary_filter_narrows_the_list() -> None:
    async def steps(user: User) -> None:
        await user.open("/glossar")
        await user.should_see(marker="glossar_filter")
        put(user, "glossar_filter", "seed")
        await user.should_not_see(marker="term/tornado")
        await user.should_see(marker="term/seed")

    drive(steps)


def test_fields_and_metrics_carry_tooltips() -> None:
    seed = glossary.term_for(t("ui.seed"))
    median = glossary.term_for(t("result.median"))
    assert seed is not None
    assert median is not None

    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        user.find(marker="nav/simulation").click()
        await user.should_see(marker="sim_run")
        assert seed.short in tooltips(user)
        put(user, "sim_n", 2_000)
        user.find(marker="sim_run").click()
        await user.should_see("Fertig:", retries=100)
        user.find(marker="to_results").click()
        await user.should_see(marker="save_run")
        assert median.short in tooltips(user)

    drive(steps)
