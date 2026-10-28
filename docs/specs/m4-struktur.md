# Pflichtenheft M4 — Struktur-Auswertungen

**Stand:** 28. Oktober 2026, Entscheidungen E1–E10 bestätigt (Abschnitt 12) · **Bezug:**
[PRD.md](../../PRD.md), Meilenstein M4 (AK 1–6, Edge cases) · **Voraussetzung:** M1–M3

Dieses Pflichtenheft legt fest, **wie** M4 umgesetzt wird. Das PRD bleibt der Vertrag für das
**Was**; bei Widerspruch gilt das PRD, und der Widerspruch wird hier korrigiert.

***

## 1. Umfang

**In M4:** Abhängigkeitsgraph, Kritikalität mit Pfadkonstellationen, Tornado, Sweep,
Rangkorrelation (Spearman), Risikomatrix der Ereignisse – je Szenario, mit gemeinsamen
Zufallszahlen, auf einer neuen Seite „Analyse“.

**Nicht in M4:** Korrelationsgruppen (M5; der Graph ist für ihre Kanten vorbereitet),
Sobol-Indizes (Nicht-Ziel), Export der Auswertungen (M6).

***

## 2. Modulstruktur

```text
src/app/
    engine/simulate.py        + keep="outputs" | "all" (alle Knotenarrays behalten, E10)
    expr/activity.py          Aktivität je Referenz und Iteration (max/min-Gewinner, where-Zweig)
    model/graph.py            + edges(model) -> list[Edge(quelle, ziel, art)]
    analysis/
        criticality.py        Pfad-Masken, Kritikalitätsindex, Pfadkonstellationen
        tornado.py            P10/P90-Fixierung, Ausschläge
        sweep.py              Kennzahl über k Parameterwerte
        sensitivity.py        Spearman je Eingabe
        riskmatrix.py         p̂ (Wilson), bedingte Differenz (Welch)
    present/structure.py      Plotly-Figuren: Graph, Kritikalität, Tornado, Sweep, Risikomatrix
    ui/pages/analyse.py       Reiter je Auswertung, Szenario- und Ausgabewahl
```

- **Neue Abhängigkeit:** `networkx` (BSD) für das Schichten-Layout des Graphen (PRD Constraints).
- Alle Auswertungen sind reine Funktionen über `CompiledModel` und `SimulationResult`; die Seite
  ruft sie auf und zeichnet.

***

## 3. Abhängigkeitsgraph (AK 1)

- **Kanten** (`model/graph.py::edges`): Art `ausdruck` (Referenz in `expr`), `parameter`
  (Referenz in einem Verteilungsparameter oder `p`), `korrelation` (Korrelationsgruppe, ab M5;
  die Funktion liefert sie, sobald das Schema Gruppen kennt).
- **Darstellung** (E1): Plotly-Streudiagramm, Schichten-Layout über
  `networkx.topological_generations` (Eingaben links, Ausgaben rechts); Knotentyp als Symbol
  (Kreis unsicher, Raute Ereignis, Quadrat Konstante, Dreieck Auswahl, Punkt berechnet, Stern
  Ausgabe), Kantenart als Linienart (durchgezogen, gestrichelt, gepunktet); Tooltip mit Name,
  Einheit, Verteilung bzw. Ausdruck.
- **Einfärbung** (umschaltbar): Sensitivität = |Spearman| zur gewählten Ausgabe (E5),
  Kritikalitätsindex, fehlende Begründung (`why` fehlt bei `uncertain`/`event`/`constant`).
- Zyklen gibt es nicht (M1); Knoten ohne Pfad zur Ausgabe werden blass gezeichnet.

***

## 4. Kritikalität (AK 2)

### 4.1 Aktivität (`expr/activity.py`)

`activity(expr, values) -> dict[referenz, bool-Array]`: in welchen Iterationen eine Referenz das
Ergebnis eines Ausdrucks mitbestimmt.

| Ausdruck | Regel (E2) |
|---|---|
| Name | aktiv in allen Iterationen |
| `+ - * / ** %`, Funktionen, Vergleiche, `and/or/not`, `interp` | Vereinigung der Operanden |
| `max(a, b, …)`, `min(…)` | Operand i nur dort aktiv, wo er gewinnt (`== Ergebnis`); **bei Gleichstand alle Gewinner** |
| `where(c, a, b)` | `a` dort, wo `c` wahr, `b` dort, wo `c` falsch; die Bedingung selbst liegt **nicht** auf dem Pfad |
| `choice == "Label"` | aktiv in allen Iterationen |

- `Extremum` erhält dafür eine Methode `winners(values) -> list[bool-Array]`; die Auswertung
  selbst bleibt unverändert (M1-Vorbereitung).

### 4.2 Entscheidender Pfad und Index

- Rückwärts in umgekehrter topologischer Ordnung: Maske der Ausgabe = alle Iterationen; jeder
  Knoten gibt seine Maske an die Referenzen weiter, mit `maske_X & aktivität_r(X)`; mehrere
  Nachfolger werden mit ODER vereint.
- Parameter von `uncertain`- und `event`-Knoten liegen vollständig auf dem Pfad (bedingte
  Verteilung).
- **Index** eines Knotens = Anteil der Iterationen mit Maske wahr, mit Wilson-Intervall.
  Ausgewiesen für `uncertain`, `event` und `derived`; Indizes summieren nicht zu 100 %.
- **Pfadkonstellation** einer Iteration = Menge der kritischen `uncertain`/`event`-Knoten; die
  Anteile aller Konstellationen summieren zu 100 % (Tabelle, häufigste zuerst, Rest gesammelt
  ab Rang 10).
- **T2:** Index von A und B = P(Pfad 1 > C) ≈ 0.5737 (Anteils-Kriterium), C ≈ 0.4263.
- **Ohne `max`/`min`** (Edge case): Die Seite erklärt, dass dann jede Eingabe mit Pfad zur
  Ausgabe in jeder Iteration kritisch ist und der Index keine Information trägt.

***

## 5. Tornado (AK 3)

- **Eingaben** (E4): alle `uncertain`-Knoten mit Pfad zur Ausgabe sowie solche ohne (Ausschlag 0,
  als Probe der Kopplung). Ereignisse gehören in die Risikomatrix.
- **Fixwerte:** P10 und P90 der simulierten Randverteilung des Knotens (funktioniert auch für
  bedingte Verteilungen); diskrete Familien mit `np.quantile(..., method="inverted_cdf")`, also
  echte Werte der Verteilung (Edge case).
- **Läufe:** je Eingabe zwei Läufe mit demselben Seed, der Knoten als Konstante gesetzt; alle
  anderen Knoten ziehen dieselben Zufallszahlen (Ströme je Knoten-ID, M1) → **Ausschlag eines
  Knotens ohne Pfad zur Ausgabe exakt 0**.
- **Kennzahl** (E3): Mittelwert der Ausgabe (Standard), wählbar Median oder P(Ziel).
  Ausschlag = Kennzahl(P90) − Kennzahl(P10); sortiert nach |Ausschlag|.
- **N:** Standard 20 000 je Lauf, änderbar; Laufzeit-Hinweis bei mehr als 50 Läufen.
- **T1:** Ausschläge von X₁ und X₂ gleich (±2 %).

***

## 6. Sweep (AK 4)

- Parameter wie die Stellschraube im Lernpfad (E7): literale Zahl eines Knotens
  (`value`, Verteilungsparameter, `p`); Bereich von–bis, k Werte (Standard 9), gleicher Seed.
- Kennzahlen: Mittelwert, Median, wählbares Quantil, P(Ziel) – je mit Unsicherheit (SE,
  Quantil-KI bzw. Wilson aus M1).
- Ungültige Werte im Bereich (z. B. sd ≤ 0) werden vor dem Lauf gemeldet, nicht übersprungen.
- **T2:** P(Ende ≤ 30) ist über den Mittelwert von B monoton nicht steigend (wegen der Kopplung
  sogar in jeder Iteration).

***

## 7. Rangkorrelation (AK 5)

- Spearman-ρ jeder `uncertain`- und `event`-Eingabe zur gewählten Ausgabe aus **einem** Lauf
  (`keep="all"`), sortiert nach |ρ|, mit 95-%-Intervall (Fisher-z mit SE 1,03/√(N−3)).
- Beschriftung im UI: „Deskriptiv: zeigt Gleichlauf im Modell, keine Ursache und keine
  Wirkungsstärke.“

***

## 8. Risikomatrix (AK 6)

- Je `event`: x = p̂ mit Wilson-Intervall; y = E[Y | Ereignis] − E[Y | kein Ereignis] mit
  95-%-Intervall nach Welch (E8); Darstellung als Streudiagramm mit Fehlerbalken, Beschriftung
  mit Ereignisnamen.
- Tritt ein Ereignis nie oder immer ein, ist y nicht definiert: Punkt am Rand, markiert
  „y nicht bestimmbar“ (Edge case).
- **T2, Szenario „mit Nacharbeit“:** y ∈ (0, 5]; im Hauptszenario tritt das Ereignis nie ein.
- Sichtbarer Hinweis: „Die Differenz ist keine kausale Wirkung, wenn Ereignisse gemeinsame
  Ursachen haben oder zusammenwirken.“

***

## 9. Oberfläche

- Neue Seite **„Analyse“** (E6): Szenario, Ausgabe, N, Seed; Reiter Graph, Kritikalität,
  Tornado, Sweep, Rangkorrelation, Risikomatrix. Graph und Rangkorrelation rechnen aus einem
  Lauf; Tornado und Sweep starten eigene Läufe per Knopf.
- Ergebnisse in Modellsprache, z. B. „Im Modell liegt Vorgang B in 57,4 % der Iterationen auf
  dem entscheidenden Pfad (57,1 … 57,7 %).“
- Texte über `messages.t()`, Schlüssel `analysis.*`.

***

## 10. Tests

| AK | Test | Prüft |
|---|---|---|
| 1 | `test_graph.py`, `test_analysis_page.py` | Kantenarten aus `expr` und Parametern; Symbole je Knotentyp; Einfärbung „fehlende Begründung“ |
| 2 | `test_criticality.py` | T2: Index A, B gegen 0,5737 (Wilson 99,9 %), C gegen 0,4263; Gleichstand zählt beide; Konstellationen summieren zu 1; `where`-Bedingung nicht auf dem Pfad; Modell ohne `max` |
| 3 | `test_tornado.py` | Unverbundener Knoten Ausschlag exakt 0; T1 X₁ ≈ X₂ (±2 %); diskrete Eingabe nimmt echte Werte; Sortierung |
| 4 | `test_sweep.py` | T2 monoton nicht steigend über mean(B); ungültiger Wert wird gemeldet |
| 5 | `test_sensitivity.py` | ρ einer unabhängigen Eingabe ≈ 0, einer linear wirkenden > 0,9; Beschriftung |
| 6 | `test_riskmatrix.py` | T2 „mit Nacharbeit“: y ∈ (0, 5]; nie/immer → nicht definiert |
| UI | `test_app.py` | Seite Analyse mit T2: alle Reiter ohne Ausnahme; Kritikalitätssatz; Hinweise sichtbar |

- Laufzeit: Tornado- und Sweep-Tests mit N ≤ 20 000; Ziel ≤ 5 s zusätzlich im Gate.

***

## 11. Arbeitspakete und Abschluss

| AP | Inhalt | Fertig, wenn |
|---|---|---|
| AP1 | `keep="all"`, `expr/activity.py`, `analysis/criticality.py` | AK 2 grün |
| AP2 | `analysis/tornado.py`, `sweep.py` | AK 3, 4 grün |
| AP3 | `analysis/sensitivity.py`, `riskmatrix.py` | AK 5, 6 grün |
| AP4 | `graph.edges`, `present/structure.py` | AK 1 (rein) grün |
| AP5 | Seite Analyse, Texte | AppTests grün |
| AP6 | Doku, Review, PRD-Status, manueller Durchlauf | Checkliste unten |

**Reihenfolge:** AP1 → (AP2 ∥ AP3) → AP4 → AP5 → AP6.

- [ ] PRD M4 AK 1–6 und Edge cases durch Tests belegt; Gate grün.
- [ ] Manuell: T2 und Lektion A11 auf der Seite Analyse durchgesehen.
- [ ] README, `docs/architecture.md`; PRD M4 **Status** `done (verified by: …)`; Review.

***

## 12. Entscheidungen

Am 28.10.2026 alle wie vorgeschlagen bestätigt. E1 bringt `networkx` (BSD) als neue
Laufzeitabhängigkeit.

| Nr | Frage | Entscheidung |
|---|---|---|
| E1 | Graph zeichnen | Plotly mit NetworkX-Schichten-Layout (keine Systemabhängigkeit wie Graphviz) |
| E2 | Was liegt auf dem entscheidenden Pfad? | `max`/`min`: nur Gewinner (Gleichstand: alle); `where`: nur der gewählte Zweig, nicht die Bedingung; Rechenoperationen: alle Operanden; Verteilungsparameter: vollständig |
| E3 | Kennzahl des Tornados | Mittelwert der Ausgabe; wählbar Median oder P(Ziel); N = 20 000 je Lauf |
| E4 | Welche Eingaben im Tornado? | Alle `uncertain`-Knoten; P10/P90 aus der simulierten Randverteilung (diskret: echte Werte); Ereignisse nur in der Risikomatrix |
| E5 | Einfärbung „Sensitivität“ im Graphen | \|Spearman\| zur gewählten Ausgabe aus einem Lauf (schnell); Tornado bleibt eigener Reiter |
| E6 | Oberfläche | Eine neue Seite „Analyse“ mit Reitern, Szenario- und Ausgabewahl |
| E7 | Sweep-Parameter | Literale Zahlen wie die Stellschraube; k = 9 Standard; gleicher Seed |
| E8 | Unsicherheit in der Risikomatrix | x: Wilson; y: Welch-Intervall (95 %) als Fehlerbalken |
| E9 | Spearman | Für `uncertain` und `event`, mit Fisher-z-Intervall, deutlich als deskriptiv beschriftet |
| E10 | Speicher | `simulate(keep="all")` hält alle Knotenarrays für die Analysen; Hinweis ab 500 MB |
