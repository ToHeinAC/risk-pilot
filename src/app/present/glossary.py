"""Glossary of the UI's technical terms (M8 AK 3): one sentence for tooltips, a paragraph for the
glossary page and an example on tutorial T2 (mini schedule)."""

import re
from dataclasses import dataclass

from app.messages import t


@dataclass(frozen=True)
class Term:
    key: str  # also the anchor on the glossary page
    label: str
    short: str  # one sentence, the tooltip
    long: str
    example: str
    aliases: tuple[str, ...] = ()


TERMS: tuple[Term, ...] = (
    Term(
        "iteration",
        "Iteration",
        "Ein Durchlauf des Modells mit je einem gezogenen Wert für jede unsichere Eingabe.",
        "Die Simulation rechnet das Modell N-mal; jede Iteration ist eine mögliche Welt. Alle "
        "Kennzahlen zählen oder mitteln über diese Iterationen.",
        "In T2 zieht jede Iteration eine Dauer für A, B und C und rechnet das Projektende aus.",
        ("Iterationen",),
    ),
    Term(
        "seed",
        "Seed",
        "Startwert des Zufallsgenerators: gleicher Seed, gleiche Zahlen.",
        "Der Seed macht jeden Lauf wiederholbar. Szenarien im Vergleich laufen mit demselben "
        "Seed, damit Unterschiede nur aus den Overrides kommen.",
        "T2 mit Seed 20261027 liefert bei jedem Start dieselbe Wahrscheinlichkeit für Tag 30.",
    ),
    Term(
        "verteilung",
        "Verteilung",
        "Beschreibt, welche Werte eine unsichere Größe annehmen kann und wie oft.",
        "Eine Verteilung wird über eine Familie (z. B. normal, dreieck) und ihre Parameter oder "
        "über eine Spanne (P10/P50/P90) angegeben.",
        "In T2 ist Vorgang B normalverteilt mit Mittelwert 15 d und Standardabweichung 3 d.",
        ("Verteilungen",),
    ),
    Term(
        "quantil",
        "Quantil (P10, P50, P90)",
        "P90 ist der Wert, den 90 % der Iterationen nicht überschreiten.",
        "Quantile beschreiben eine Verteilung über Anteile: P10 ist ein günstiger, P90 ein "
        "ungünstiger, aber noch üblicher Wert; P50 ist der Median.",
        "Liegt P90 des Projektendes in T2 bei 30,7 d, dauert das Projekt in 90 % der "
        "Iterationen höchstens 30,7 d.",
        ("Quantil", "P10", "P90"),
    ),
    Term(
        "median",
        "Median",
        "Der mittlere Wert: die Hälfte der Iterationen liegt darunter, die Hälfte darüber.",
        "Der Median ist P50. Bei schiefen Verteilungen liegt er neben dem Mittelwert und ist "
        "oft der anschaulichere Wert.",
        "Ein Median des Projektendes von 26,6 d in T2 heißt: in der Hälfte der Iterationen ist "
        "das Projekt nach 26,6 d fertig.",
    ),
    Term(
        "erwartungswert",
        "Mittelwert",
        "Der Durchschnitt über alle Iterationen (Erwartungswert im Modell).",
        "Der Mittelwert reagiert auf seltene extreme Werte stärker als der Median; er trägt den "
        "Standardfehler als Maß seiner numerischen Genauigkeit.",
        "In T2 liegt der Mittelwert des Projektendes über dem Mittel von Pfad 1 und Vorgang C, "
        "weil das Maximum beider zählt.",
        ("Erwartungswert",),
    ),
    Term(
        "standardabweichung",
        "Standardabweichung",
        "Typischer Abstand der Werte vom Mittelwert: ein Maß für die Streuung.",
        "Die Standardabweichung beschreibt das Modell, nicht die Genauigkeit der Simulation; "
        "die misst der Standardfehler.",
        "Vorgang B in T2 hat eine Standardabweichung von 3 d.",
    ),
    Term(
        "standardfehler",
        "Standardfehler",
        "So genau ist ein simulierter Mittelwert bei diesem N.",
        "Der Standardfehler schrumpft mit der Wurzel aus N: viermal so viele Iterationen "
        "halbieren ihn. Er misst nur die Simulationsunsicherheit.",
        "Bei N = 100 000 ist der Standardfehler des Projektendes in T2 kleiner als 0,02 d.",
    ),
    Term(
        "intervall",
        "Intervall",
        "Bereich, in dem der wahre Wert des Modells bei diesem N mit 95 % Konfidenz liegt.",
        "Jede Kennzahl steht mit ihrem Intervall: es zeigt die numerische Unsicherheit der "
        "Simulation, nicht die Unsicherheit der Welt. Mehr Iterationen machen es schmaler.",
        "Bei N = 20 000 ist das Intervall für P(Ziel erreicht) in T2 rund ±0,5 Prozentpunkte "
        "breit; genauer lässt es sich mit diesem N nicht sagen.",
        ("Intervall", "Konfidenz"),
    ),
    Term(
        "szenario",
        "Szenario",
        "Eine Variante des Modells, die einzelne Werte des Hauptszenarios überschreibt.",
        "Szenarien bilden einen Baum: jedes Unterszenario erbt von seinem Eltern-Szenario und "
        "ändert nur, was es ausdrücklich überschreibt, mit Begründung.",
        "T2 hat die Szenarien „B −3 Tage“ und „mit Nacharbeit“.",
        ("Szenarien", "Hauptszenario"),
    ),
    Term(
        "override",
        "Override",
        "Ein Wert, den ein Szenario gegenüber seinem Eltern-Szenario überschreibt.",
        "Ein Override nennt Knoten, Feld, neuen Wert und Begründung. Alles andere bleibt wie im "
        "Eltern-Szenario.",
        "In T2 setzt „B −3 Tage“ den Mittelwert von Vorgang B von 15 auf 12 d.",
        ("Overrides",),
    ),
    Term(
        "ereignis",
        "Ereignis",
        "Etwas, das mit einer Wahrscheinlichkeit eintritt oder nicht (ja/nein).",
        "Ereignisse schalten Wirkungen zu, etwa eine Nacharbeit oder einen Ausfall. Die "
        "Risikomatrix ordnet sie nach Wahrscheinlichkeit und Folge.",
        "In T2 tritt die Nacharbeit an B im Szenario „mit Nacharbeit“ mit 20 % ein.",
        ("Ereignisse",),
    ),
    Term(
        "ausgabe",
        "Ausgabe",
        "Die Größe, nach der das Modell gefragt wird; die Ergebnisse beziehen sich auf sie.",
        "Eine Ausgabe kann ein Ziel, einen Horizont und eine Richtung (kleiner ist besser) tragen.",
        "Die Ausgabe von T2 ist das Projektende.",
        ("Ausgaben",),
    ),
    Term(
        "zielwert",
        "Ziel (P(Ziel erreicht))",
        "Anteil der Iterationen, in denen die Ausgabe ihr Ziel erreicht.",
        "Das Ziel ist eine Schwelle an der Ausgabe, z. B. ≤ 30 d. P(Ziel erreicht) ist die "
        "Antwort auf „Wie wahrscheinlich schaffen wir das?“ – im Modell.",
        "In T2 ist das Ziel „Projektende ≤ 30 d“.",
        ("Ziel",),
    ),
    Term(
        "horizont",
        "Horizont",
        "Grenze, bis zu der eine Ausgabe betrachtet wird; spätere Werte zählen als „nicht "
        "erreicht“.",
        "Ein Horizont trennt „tritt bis dahin ein“ von „nicht im Horizont“. Kennzahlen wie der "
        "Median beziehen sich dann auf die Werte innerhalb.",
        "T2 hat keinen Horizont; T5 betrachtet die Fusion bis 2100. Im Terminplan wäre ein "
        "Horizont etwa „bis Tag 60“.",
    ),
    Term(
        "korrelation",
        "Korrelationsgruppe",
        "Unsichere Eingaben, die im Modell gemeinsam steigen oder fallen.",
        "Eine Korrelationsgruppe gibt Rangkorrelationen vor; nach dem Lauf steht daneben, was "
        "die Simulation tatsächlich erreicht hat.",
        "Laufen A und B in T2 beim selben Team, könnten ihre Dauern korreliert sein.",
        ("Korrelation",),
    ),
    Term(
        "kritischer_pfad",
        "Kritischer Pfad",
        "Der Weg durch das Modell, der in einer Iteration das Ergebnis tatsächlich bestimmt.",
        "Bei max, min und where entscheidet je Iteration nur ein Zweig. Der Kritikalitätsindex "
        "zählt, wie oft ein Knoten auf diesem entscheidenden Pfad liegt.",
        "In T2 bestimmt mal Pfad 1 (A + B), mal Vorgang C das Projektende.",
        ("Kritikalität", "entscheidenden Pfad"),
    ),
    Term(
        "tornado",
        "Tornado",
        "Rangfolge der unsicheren Eingaben nach ihrer Wirkung auf eine Kennzahl.",
        "Jede Eingabe wird einmal auf ihr P10 und einmal auf ihr P90 gesetzt; der Balken zeigt, "
        "wie weit sich die Kennzahl dabei bewegt.",
        "In T2 zeigt der Tornado, ob Vorgang B oder C das Projektende stärker verschiebt.",
    ),
    Term(
        "sweep",
        "Sweep",
        "Ein Planwert läuft über mehrere Werte; je Wert ein Lauf mit demselben Seed.",
        "Der Sweep beantwortet Was-wäre-wenn-Fragen zu einem einzelnen Wert, etwa ab welcher "
        "Dauer ein Ziel kippt.",
        "Ein Sweep über den Mittelwert von Vorgang B in T2 zeigt, wie P(Ziel erreicht) fällt.",
    ),
    Term(
        "spearman",
        "Spearman-ρ",
        "Rangkorrelation zwischen −1 und 1: wie stark Eingabe und Ergebnis gleichlaufen.",
        "ρ nach Spearman vergleicht Ränge statt Werte und erfasst so jeden monotonen "
        "Zusammenhang. Deskriptiv: keine Ursache und keine Wirkungsstärke.",
        "In T2 zeigt ρ, wie stark die Vorgänge A, B und C mit dem Projektende gleichlaufen.",
        ("Rangkorrelation", "Spearman"),
    ),
    Term(
        "risikomatrix",
        "Risikomatrix",
        "Ereignisse nach Eintrittswahrscheinlichkeit und mittlerer Folge eingeordnet.",
        "Waagerecht steht, wie oft ein Ereignis eintritt, senkrecht, um wie viel die Ausgabe "
        "dann im Mittel höher liegt – aus der Simulation statt geschätzt.",
        "Im Szenario „mit Nacharbeit“ von T2 steht die Nacharbeit an B bei 20 %.",
    ),
    Term(
        "var_es",
        "VaR und ES",
        "Value at Risk: Verlust, der mit z. B. 95 % nicht überschritten wird; ES: Mittel darüber.",
        "VaR und Expected Shortfall beschreiben das ungünstige Ende einer Verlustverteilung; "
        "der ES schaut auch auf die Größe der seltenen großen Verluste.",
        "Im Terminplan T2 entspräche der VaR 95 % dem P95 des Projektendes; im Portfolio T4 "
        "geht es um Verluste.",
        ("VaR",),
    ),
    Term(
        "flaeche",
        "Fläche",
        "Das Modell als Knoten und Kanten zum Verschieben, Verbinden und Anklicken.",
        "Die Fläche zeigt dasselbe Modell wie Formular und YAML. Kanten werden aus den "
        "Ausdrücken abgeleitet; wer zwei Knoten verbindet, schreibt einen Ausdruck. Positionen "
        "stehen im Block „layout“ und ändern keine Zahl.",
        "In T2 führt eine Kante von Pfad 1 zum Projektende, weil dort max(pfad1, c) steht.",
        ("Zeichenfläche", "Szenario auf der Fläche"),
    ),
    Term(
        "zeitplan",
        "Zeitplan",
        "Das Modell als Gantt: wann jeder Vorgang beginnen kann und wann er endet.",
        "Der Zeitplan liest den Ausdruck der Ausgabe als Netzplan: bei a + b beginnt b, wenn a "
        "endet; bei max(a, b) laufen beide parallel und es geht weiter, wenn beide fertig sind; "
        "bei min(a, b), sobald einer fertig ist. Balken zeigen den Median, der Strich die "
        "Spanne P10–P90 des Endes, Pfeile die Voraussetzung für einen Start.",
        "In T2 beginnt Vorgang B, wenn A fertig ist; das Projektende wartet auf Pfad 1 und C.",
        ("Gantt", "Netzplan"),
    ),
    Term(
        "vorauswahl",
        "Vorauswahl",
        "Eine fertige Art der Verknüpfung, etwa Summe, Maximum oder Verzögerung bei Eintritt.",
        "Beim Verbinden bietet der Dialog nur Vorauswahlen an, die zum Ziel passen, und zeigt "
        "das Ergebnis in Klartext. Frei formulierte Ausdrücke schreibt die Fläche nie um.",
        "Verbindet man in T2 Vorgang A mit dem Projektende unter „Parallel – alle fertig“, "
        "wird aus max(pfad1, c) der Ausdruck max(pfad1, c, a).",
        ("Art der Verknüpfung",),
    ),
)

BY_KEY = {term.key: term for term in TERMS}
# UI labels (message keys) and the term they stand for.
LABELS = {
    "ui.n": "iteration",
    "ui.seed": "seed",
    "ui.scenario": "szenario",
    "result.mean": "erwartungswert",
    "result.median": "median",
    "result.sd": "standardabweichung",
    "result.se": "standardfehler",
    "result.target_label": "zielwert",
    "result.beyond_label": "horizont",
    "compare.p10": "quantil",
    "compare.p90": "quantil",
    "analysis.tab_crit": "kritischer_pfad",
    "analysis.tab_tornado": "tornado",
    "analysis.tab_sweep": "sweep",
    "analysis.tab_rho": "spearman",
    "analysis.tab_risk": "risikomatrix",
    "analysis.col_rho": "spearman",
    "canvas.preset": "vorauswahl",
    "canvas.scenario": "flaeche",
    "gantt.view_gantt": "zeitplan",
}
PATTERNS = (
    (re.compile(r"^P\d+ \(\d+-%-Quantil\)$"), "quantil"),
    (re.compile(r"^(VaR|ES) \d+"), "var_es"),
)


def term_for(label: str) -> Term | None:
    """The glossary entry of a label shown on screen, if it is a technical term."""
    for key, term in LABELS.items():
        if t(key) == label:
            return BY_KEY[term]
    for pattern, term in PATTERNS:
        if pattern.match(label):
            return BY_KEY[term]
    return None
