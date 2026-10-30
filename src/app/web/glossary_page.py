"""Glossary page (M8 AK 3): every term with tooltip sentence, explanation and T2 example."""

from nicegui import ui

from app.messages import t
from app.present import glossary
from app.web.session import Session


def _matches(term: glossary.Term, query: str) -> bool:
    words = (term.label, *term.aliases, term.short)
    return not query or any(query in w.lower() for w in words)


def page(_session: Session) -> None:
    query = ui.input(t("glossary.filter")).props("outlined dense clearable").classes("w-80")
    query.mark("glossar_filter")

    @ui.refreshable
    def terms() -> None:
        wanted = str(query.value or "").strip().lower()
        for term in glossary.TERMS:
            if not _matches(term, wanted):
                continue
            with ui.column().classes("rp-panel p-4 gap-1 w-full").props(f"id={term.key}"):
                ui.label(term.label).classes("text-lg font-semibold").mark(f"term/{term.key}")
                ui.label(term.short).classes("rp-answer")
                ui.label(term.long)
                ui.label(f"{t('glossary.example')} {term.example}").classes("rp-muted")

    query.on_value_change(terms.refresh)
    terms()
