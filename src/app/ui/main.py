"""Entry point: ``uv run streamlit run src/app/ui/main.py`` (port from .streamlit/config.toml).

Every page calls ``views.sidebar_exit()`` itself: AppTest re-renders only the page after a
widget interaction under ``st.navigation``, so sidebar widgets placed here would vanish in tests.
"""

import streamlit as st

from app.messages import t

st.set_page_config(page_title="Risk Pilot", layout="wide")
navigation = st.navigation(
    [
        st.Page("pages/start.py", title=t("ui.page_start"), default=True),
        st.Page("pages/lernpfad.py", title=t("ui.page_lernpfad")),
        st.Page("pages/modell.py", title=t("ui.page_modell")),
        st.Page("pages/szenarien.py", title=t("ui.page_szenarien")),
        st.Page("pages/simulation.py", title=t("ui.page_simulation")),
        st.Page("pages/ergebnisse.py", title=t("ui.page_ergebnisse")),
        st.Page("pages/vergleich.py", title=t("ui.page_vergleich")),
        st.Page("pages/laeufe.py", title=t("ui.page_laeufe")),
    ]
)
navigation.run()
