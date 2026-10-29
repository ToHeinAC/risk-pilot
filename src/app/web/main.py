"""Entry point of the new UI (M7): ``uv run python -m app.web.main``.

Port from ``RISK_PILOT_PORT`` (default 8643 while Streamlit keeps 8642). One ``Session`` per
browser tab; pages are built by ``BUILDERS`` inside one shell with navigation and exit.
"""

import asyncio
from collections.abc import Callable
from pathlib import Path

from nicegui import ui

from app.adapters import process, settings
from app.messages import t
from app.web import model_page, start, theme
from app.web.session import OpenModel, Session

EXIT_DELAY = 0.3  # seconds: the goodbye text reaches the browser before SIGTERM
PAGES = (
    ("/", "ui.page_start", "home"),
    ("/lernpfad", "ui.page_lernpfad", "school"),
    ("/modell", "ui.page_modell", "account_tree"),
    ("/szenarien", "ui.page_szenarien", "call_split"),
    ("/simulation", "ui.page_simulation", "play_circle"),
    ("/ergebnisse", "ui.page_ergebnisse", "insights"),
    ("/vergleich", "ui.page_vergleich", "compare_arrows"),
    ("/analyse", "ui.page_analyse", "troubleshoot"),
    ("/laeufe", "ui.page_laeufe", "history"),
)

Builder = Callable[[Session], None]


def _follows(_session: Session) -> None:
    ui.label(t("web.page_follows")).classes("rp-muted")


BUILDERS: dict[str, Builder] = {path: _follows for path, _key, _icon in PAGES}
BUILDERS.update({"/": start.page, "/modell": model_page.page})


def new_session() -> Session:
    return Session()


def _exit_dialog(session: Session) -> Callable[[], None]:
    """The exit dialog; returns its opener. Confirming ends only this process."""
    dialog = ui.dialog()

    async def confirm() -> None:
        with card:
            ui.label(t("ui.exit_done"))
        await asyncio.sleep(EXIT_DELAY)
        process.shutdown()

    def open_dialog() -> None:
        card.clear()
        with card:
            ui.label(t("ui.exit")).classes("text-lg font-semibold")
            if session.model is not None and session.model.dirty:
                ui.label(t("ui.exit_unsaved")).classes("text-warning")
            ui.label(t("ui.exit_question")).classes("rp-muted")
            with ui.row().classes("justify-end w-full"):
                ui.button(t("ui.exit_cancel"), on_click=dialog.close).props("flat")
                ui.button(t("ui.exit_confirm"), color="negative", on_click=confirm).props(
                    "unelevated"
                ).mark("exit_confirm")
        dialog.open()

    with dialog, ui.card().classes("p-6 gap-3") as card:
        pass
    return open_dialog


def _model_name(model: OpenModel | None) -> str:
    if model is None:
        return t("web.no_model")
    return Path(model.path).name + (" •" if model.dirty else "")


def _header(session: Session, open_exit: Callable[[], None]) -> None:
    with ui.header().classes("bg-white text-dark border-b items-center px-4 gap-4 h-14"):
        ui.label("Risk Pilot").classes("text-lg font-semibold")
        ui.space()
        ui.label().classes("rp-muted text-sm").mark("model_name").bind_text_from(
            session, "model", _model_name
        )
        ui.button(icon="power_settings_new", on_click=open_exit).props("flat round").tooltip(
            t("ui.exit")
        ).mark("exit")


def _nav() -> dict[str, ui.item]:
    items: dict[str, ui.item] = {}
    drawer = ui.left_drawer(value=True, bordered=True).props("width=210").classes("bg-white p-0")
    with drawer, ui.list().classes("rp-nav w-full mt-2"):
        for path, key, icon in PAGES:
            with ui.item(on_click=_go(path)).mark(f"nav{path}") as item:
                with ui.item_section().props("avatar"):
                    ui.icon(icon)
                ui.item_section(t(key))
            items[path] = item
    return items


def _go(path: str) -> Callable[[], None]:
    return lambda: ui.navigate.to(path)


def _page(path: str, session: Session, nav: dict[str, ui.item]) -> Callable[[], None]:
    """Build one page; an unexpected error becomes a German message, the shell keeps running."""

    def build() -> None:
        for other, item in nav.items():
            item.classes(add="rp-active" if other == path else "", remove="rp-active")
        try:
            BUILDERS[path](session)
        except Exception as exc:  # last line of defence, shown to the user
            ui.label(t("ui.unexpected", detail=f"{type(exc).__name__}: {exc}")).classes(
                "text-negative"
            )

    return build


def root() -> None:
    theme.apply()
    session = new_session()
    open_exit = _exit_dialog(session)
    _header(session, open_exit)
    nav = _nav()
    with ui.column().classes("w-full max-w-[1400px] mx-auto p-4 gap-4"):
        ui.sub_pages({path: _page(path, session, nav) for path, _key, _icon in PAGES}).classes(
            "w-full"
        )


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(  # pyright: ignore[reportUnknownMemberType]
        root, port=settings.port(), title="Risk Pilot", reload=False, show=False, language="de"
    )
