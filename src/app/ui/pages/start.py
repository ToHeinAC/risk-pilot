"""Start: learning path, tutorials, own models."""

from pathlib import Path

import streamlit as st

from app.adapters import files, settings
from app.errors import ModelError
from app.messages import t
from app.ui import views


def _title(path: Path) -> str:
    try:
        model = files.load_model(path)
    except (ModelError, OSError, UnicodeDecodeError):
        return path.stem
    return model.title or model.model


def _card(path: Path) -> None:
    with st.container(border=True):
        st.markdown(f"**{_title(path)}** · `{path.stem}`")
        if st.button(
            t("ui.open"), key=f"open_{path.stem}", on_click=views.open_model, args=(path,)
        ):
            st.switch_page("pages/modell.py")
        existing = {p.stem for p in files.list_models(settings.models_dir())}
        views.copy_form(path, path.stem, files.suggest_id(f"{path.stem}_kopie", existing))


def body() -> None:
    st.title("Risk Pilot")
    st.markdown(t("ui.start_intro"))
    st.subheader(t("ui.page_lernpfad"))
    st.markdown(t("ui.lernpfad_intro"))
    if st.button(t("ui.open_lernpfad"), key="open_lernpfad"):
        st.switch_page("pages/lernpfad.py")
    st.subheader(t("ui.tutorials"))
    for tutorial in sorted(settings.examples_dir().glob("t*.yaml")):
        _card(tutorial)
    st.subheader(t("ui.own_models"))
    own = files.list_models(settings.models_dir())
    if not own:
        st.caption(t("ui.no_own_models"))
    for path in own:
        _card(path)


views.run_page(body)
