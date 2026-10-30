"""Glossary: required terms, no dead entry, no unexplained term (M8 AK 3)."""

import pytest

from app.messages import UI, t
from app.present import glossary

REQUIRED = (
    "iteration",
    "seed",
    "quantil",
    "intervall",
    "szenario",
    "override",
    "kritischer_pfad",
    "tornado",
    "spearman",
)
# Labels people meet on screen: each one must lead to a glossary entry (no unexplained term).
LABELS = (
    "ui.n",
    "ui.seed",
    "ui.scenario",
    "result.mean",
    "result.median",
    "result.sd",
    "result.se",
    "result.target_label",
    "result.beyond_label",
    "compare.p10",
    "compare.p90",
    "analysis.tab_crit",
    "analysis.tab_tornado",
    "analysis.tab_sweep",
    "analysis.tab_rho",
    "analysis.tab_risk",
    "analysis.col_rho",
)


def test_required_terms_are_in_the_glossary() -> None:
    assert set(REQUIRED) <= {term.key for term in glossary.TERMS}


def test_every_term_is_used_in_the_ui() -> None:
    texts = " ".join(UI["de"].values()).lower()
    for term in glossary.TERMS:
        words = (term.label, *term.aliases)
        assert any(w.lower() in texts for w in words), term.key


@pytest.mark.parametrize("key", LABELS)
def test_every_ui_label_has_a_term(key: str) -> None:
    term = glossary.term_for(t(key))
    assert term is not None, key


def test_quantile_labels_and_risk_measures_are_explained() -> None:
    quantil = glossary.term_for(t("result.quantile_label", pct="90"))
    assert quantil is not None
    assert quantil.key == "quantil"
    var = glossary.term_for(t("result.var", pct="95"))
    assert var is not None
    assert var.key == "var_es"
    assert glossary.term_for("Kein Fachbegriff") is None


def test_terms_are_complete_and_unique() -> None:
    keys = [term.key for term in glossary.TERMS]
    assert len(keys) == len(set(keys))
    for term in glossary.TERMS:
        assert term.short.endswith(".")
        assert "\n" not in term.short
        assert term.long
        assert "T2" in term.example or "Terminplan" in term.example, term.key
