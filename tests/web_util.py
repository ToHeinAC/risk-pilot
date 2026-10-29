"""Drive the NiceGUI app in-process (no browser, no socket), from synchronous tests."""

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from nicegui import ui
from nicegui.element import Element
from nicegui.testing import User
from nicegui.testing.user_simulation import user_simulation

from app.web import main

Steps = Callable[[User], Awaitable[None]]


def drive(steps: Steps) -> None:
    async def scenario() -> None:
        async with user_simulation(main.root) as user:
            await steps(user)

    asyncio.run(scenario())


def element(user: User, marker: str) -> Element:
    found = user.find(marker=marker).elements
    assert len(found) == 1, (marker, found)
    return next(iter(found))


def value(user: User, marker: str) -> Any:
    return getattr(element(user, marker), "value")  # noqa: B009 - Element has no typed value


def put(user: User, marker: str, new: Any) -> None:
    """Set a widget's value as a user would; its change handler runs at once."""
    target = element(user, marker)
    assert user.client is not None
    with user.client:
        setattr(target, "value", new)  # noqa: B010


def enabled(user: User, marker: str) -> bool:
    return bool(getattr(element(user, marker), "enabled", True))


def texts(user: User) -> str:
    """Every label and markdown text currently on the page."""
    parts = [str(e.text) for e in _all(user, ui.label)]
    parts += [str(e.content) for e in _all(user, ui.markdown)]
    return "\n".join(parts)


async def until(check: Callable[[], bool], retries: int = 100) -> None:
    """Wait until ``check`` holds; click handlers run as tasks, not at once."""
    for _ in range(retries):
        if check():
            return
        await asyncio.sleep(0.01)
    raise AssertionError("condition not met")


def cells(user: User, marker: str) -> list[tuple[str, ...]]:
    """The rows of the table marked ``marker``, every cell as text, in column order."""
    table = element(user, marker)
    assert isinstance(table, ui.table)
    keys = [str(c["field"]) for c in table.columns]
    return [tuple(str(row[k]) for k in keys) for row in table.rows]


def _all(user: User, kind: type[Element]) -> list[Any]:
    try:
        return list(user.find(kind).elements)
    except AssertionError:  # none on the page
        return []


async def open_model(user: User, stem: str) -> None:
    await user.open("/")
    await user.should_see(marker=f"open_{stem}")
    user.find(marker=f"open_{stem}").click()
    await user.should_see(marker="editor")
