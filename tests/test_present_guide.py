"""Page directory: purpose and state-dependent next step (M8 AK 1)."""

import pytest

from app.messages import UI, t
from app.present import guide
from app.present.guide import Facts

NONE = Facts(has_model=False, has_run=False)
MODEL = Facts(has_model=True, has_run=False)
RUN = Facts(has_model=True, has_run=True)


def test_every_page_has_a_purpose_and_a_next_step_text() -> None:
    for path, page in guide.PAGES.items():
        assert page.purpose in UI["de"], path
        for facts in (NONE, MODEL, RUN):
            step = guide.next_step(path, facts)
            assert step.text in UI["de"], (path, step)
            assert step.target is None or step.target in guide.PAGES


@pytest.mark.parametrize("path", ["/modell", "/szenarien", "/simulation", "/vergleich", "/analyse"])
def test_without_a_model_the_next_step_is_the_start(path: str) -> None:
    assert guide.next_step(path, NONE).target == "/"


def test_next_step_follows_the_state() -> None:
    assert guide.next_step("/", NONE).target == "/lernpfad"
    assert guide.next_step("/", MODEL).target == "/modell"
    assert guide.next_step("/modell", MODEL).target == "/simulation"
    assert guide.next_step("/simulation", MODEL).target is None  # simulate right here
    assert guide.next_step("/simulation", RUN).target == "/ergebnisse"
    assert guide.next_step("/ergebnisse", MODEL).target == "/simulation"
    assert guide.next_step("/ergebnisse", RUN).target == "/vergleich"


def test_purpose_is_one_paragraph() -> None:
    for page in guide.PAGES.values():
        assert "\n" not in t(page.purpose)
