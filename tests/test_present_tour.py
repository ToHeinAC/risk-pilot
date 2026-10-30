"""Guided tour at T2: progress is read from the state, not ticked off (M8 AK 4)."""

from app.messages import UI
from app.present import guide
from app.present.guide import TourFacts

T2 = "t2_terminplan"


def facts(
    model: str | None = None, runs: tuple[str, ...] = (), visited: tuple[str, ...] = ()
) -> TourFacts:
    return TourFacts(model=model, run_scenarios=frozenset(runs), visited=frozenset(visited))


def test_five_steps_with_texts_and_pages() -> None:
    assert len(guide.TOUR) == 5
    for step in guide.TOUR:
        assert step.text in UI["de"]
        assert step.target in guide.PAGES


def test_progress_follows_the_state() -> None:
    assert guide.tour_step(facts()) == 1
    assert guide.tour_step(facts(T2)) == 2
    assert guide.tour_step(facts(T2, ("basis",))) == 3
    assert guide.tour_step(facts(T2, ("basis", "nacharbeit"))) == 4
    assert guide.tour_step(facts(T2, ("basis", "nacharbeit"), ("/vergleich",))) == 5
    done = facts(T2, ("basis", "nacharbeit"), ("/vergleich", "/analyse"))
    assert guide.tour_step(done) is None


def test_a_step_out_of_order_counts_and_the_first_open_step_is_shown() -> None:
    assert guide.tour_step(facts(T2, ("nacharbeit",), ("/analyse",))) == 2
    assert guide.tour_step(facts(T2, ("basis", "nacharbeit"), ("/analyse",))) == 4


def test_another_model_is_not_t2() -> None:
    assert guide.tour_step(facts("t3_bahn", ("basis",))) == 1
