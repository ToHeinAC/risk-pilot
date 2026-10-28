"""Message catalogue: every code renders in German (M1 AP1)."""

import pytest

from app.errors import CODES, Issue, Notice
from app.messages import CATALOG, render


@pytest.mark.parametrize("code", sorted(CODES))
def test_every_code_has_german_template(code: str) -> None:
    assert code in CATALOG["de"]


@pytest.mark.parametrize("code", sorted(CODES))
def test_every_template_formats_with_documented_params(code: str) -> None:
    params = {name: f"<{name}>" for name in CODES[code]}
    text = render(Issue(code, node_id="knoten", field="feld", line=3, params=params))
    assert "{" not in text
    assert text.strip()


def test_catalog_has_no_undocumented_codes() -> None:
    assert set(CATALOG["de"]) == set(CODES)


def test_unknown_language_falls_back_to_german() -> None:
    issue = Issue("model.no_output")
    assert render(issue, lang="xx") == render(issue)


def test_render_mentions_node_field_and_share() -> None:
    text = render(
        Issue("param.invalid", node_id="a", field="sd", params={"value": -1, "rule": "sd > 0"})
    )
    assert "a" in text
    assert "sd" in text
    notice = Notice(
        "range.violation", node_id="a", share=0.025, params={"below": 0.025, "above": 0.0}
    )
    assert "2,5 %" in render(notice)


def test_cycle_rendered_in_order() -> None:
    text = render(Issue("graph.cycle", params={"cycle": ["a", "b", "c", "a"]}))
    assert "a → b → c → a" in text
