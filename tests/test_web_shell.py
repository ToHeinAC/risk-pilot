"""New UI shell (M7 phase 2, step 1): navigation, exit, error boundary, port."""

import asyncio
from collections.abc import Awaitable, Callable

import pytest
from nicegui.testing import User
from nicegui.testing.user_simulation import user_simulation

from app.adapters import process, settings
from app.messages import t
from app.web import main
from app.web.session import OpenModel, Session

Steps = Callable[[User], Awaitable[None]]


def drive(steps: Steps) -> None:
    async def scenario() -> None:
        async with user_simulation(main.root) as user:
            await steps(user)

    asyncio.run(scenario())


def test_navigation_lists_every_page_and_opens_it() -> None:
    async def steps(user: User) -> None:
        await user.open("/")
        for _path, key, _icon in main.PAGES:
            await user.should_see(t(key))
        for path, key, _icon in main.PAGES:
            user.find(marker=f"nav{path}").click()
            await user.should_see(t(key))
        assert set(main.BUILDERS) == {path for path, _key, _icon in main.PAGES}

    drive(steps)


def test_exit_asks_first_and_ends_only_this_process(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    monkeypatch.setattr(process, "shutdown", lambda: calls.append("sigterm"))
    monkeypatch.setattr(main, "EXIT_DELAY", 0.01)

    async def steps(user: User) -> None:
        await user.open("/")
        user.find(marker="exit").click()
        await user.should_see(t("ui.exit_question"))
        assert calls == []
        user.find(marker="exit_confirm").click()
        await user.should_see(t("ui.exit_done"))
        await asyncio.sleep(main.EXIT_DELAY * 3)
        assert calls == ["sigterm"]

    drive(steps)


def test_exit_warns_about_unsaved_changes(monkeypatch: pytest.MonkeyPatch) -> None:
    dirty = OpenModel("m.yaml", "a: 1\n", readonly=False, draft="a: 2\n")
    monkeypatch.setattr(main, "new_session", lambda: Session(model=dirty))

    async def steps(user: User) -> None:
        await user.open("/")
        user.find(marker="exit").click()
        await user.should_see(t("ui.exit_unsaved"))

    drive(steps)


def test_unexpected_error_in_a_page_becomes_a_message(monkeypatch: pytest.MonkeyPatch) -> None:
    def broken(_session: Session) -> None:
        raise ValueError("kaputt")

    monkeypatch.setitem(main.BUILDERS, "/simulation", broken)

    async def steps(user: User) -> None:
        await user.open("/simulation")
        await user.should_see(t("ui.unexpected", detail="ValueError: kaputt"))
        await user.should_see(t("ui.page_simulation"))  # the shell keeps running

    drive(steps)


def test_port_defaults_beside_streamlit_and_is_configurable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert settings.port() == 8643  # Streamlit keeps 8642 until the switch
    monkeypatch.setenv("RISK_PILOT_PORT", "9001")
    assert settings.port() == 9001
