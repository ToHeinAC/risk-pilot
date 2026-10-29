"""Page directory: what each page is for and the next step, depending on the state (M8 AK 1)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    purpose: str  # message key, one paragraph
    needs_model: bool = True


@dataclass(frozen=True)
class Facts:
    """What the next step depends on."""

    has_model: bool
    has_run: bool


@dataclass(frozen=True)
class Step:
    text: str  # message key
    target: str | None  # page path; None: the step happens on this page


PAGES: dict[str, Page] = {
    "/": Page("ui.start_intro", needs_model=False),
    "/lernpfad": Page("ui.lernpfad_intro", needs_model=False),
    "/modell": Page("guide.purpose_modell"),
    "/szenarien": Page("guide.purpose_szenarien"),
    "/simulation": Page("guide.purpose_simulation"),
    "/ergebnisse": Page("guide.purpose_ergebnisse"),
    "/vergleich": Page("guide.purpose_vergleich"),
    "/analyse": Page("analysis.intro"),
    "/laeufe": Page("guide.purpose_laeufe"),
}

SIMULATE = Step("guide.next_simulate", "/simulation")
RESULTS = Step("guide.next_results", "/ergebnisse")
FOLLOWS: dict[str, Step] = {
    "/lernpfad": Step("guide.next_start", "/"),
    "/modell": SIMULATE,
    "/szenarien": SIMULATE,
    "/vergleich": Step("guide.next_analyse", "/analyse"),
    "/analyse": Step("guide.next_scenarios", "/szenarien"),
}


def next_step(path: str, facts: Facts) -> Step:
    if PAGES[path].needs_model and not facts.has_model:
        return Step("guide.next_open", "/")
    if path == "/":
        if facts.has_model:
            return Step("guide.next_model", "/modell")
        return Step("guide.next_lernpfad", "/lernpfad")
    if path == "/simulation":
        return RESULTS if facts.has_run else Step("guide.next_run_here", None)
    if path == "/ergebnisse":
        return Step("guide.next_compare", "/vergleich") if facts.has_run else SIMULATE
    if path == "/laeufe":
        return RESULTS if facts.has_run else SIMULATE
    return FOLLOWS[path]
