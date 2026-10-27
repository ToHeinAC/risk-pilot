# Konzept v2: Weltmodell-Baukasten mit Monte-Carlo-Kern

**Stand:** 27. Oktober 2026 · **Status:** Entwurf zur Abstimmung, Vorstufe zum `PRD.md`
**Basis:** [basic-idea.md](basic-idea.md) (Erstanalyse vom 24.10.2026). Dieses Dokument beschreibt
nur, was sich ändert oder konkreter wird. Methodische Regeln der Erstanalyse gelten weiter, sofern
sie hier nicht ausdrücklich aufgehoben werden (Abschnitt 1.2).

***

## 0. Kurzfassung

- **Fokus:** Modellierung und Monte-Carlo-Auswertung. Web-Recherche und KI-gestützte
  Parameterprüfung entfallen im Tool; Recherche passiert extern (Perplexity, Claude Code), das
  Ergebnis wird als Verteilung plus Begründung eingetragen.
- **Produktbild:** Ein lokaler Baukasten, mit dem ich aus wenigen generischen Bausteinen ein
  Weltmodell meines Problems zusammenstelle – Terminplan, Technologieentwicklung, Bahnreise,
  Portfolio –, es simuliere, in Unterszenarien abwandle und die Ergebnisse vergleiche.
- **Kernauswertungen:** Ergebnisverteilungen, Szenariovergleich, Sensitivität (Tornado, Sweep,
  Rangkorrelation), kritische Pfade/Kritikalität, Abhängigkeitsgraph, simulationsgestützte
  Risikomatrix.
- **Einstieg:** Fünf Tutorials; zwei davon zeigen die numerische Lösung direkt neben der
  analytischen (Faltung, Maximum zweier Pfade) und weisen die Übereinstimmung quantitativ nach.
- **Technik:** Reiner Python-Kern (NumPy/SciPy, vektorisiert), Modelle als YAML-Dateien,
  Streamlit-Oberfläche, keine Datenbank, keine Netzwerkzugriffe.

***

## 1. Änderungen gegenüber der Erstanalyse

### 1.1 Was sich ändert

| Thema | Erstanalyse | Konzept v2 | Grund |
|---|---|---|---|
| Web-Recherche, KI | Kernfunktion (FR-09), optionaler LLM-Adapter | Entfällt im Tool | Modellierung lastet die App aus; spezialisierte Tools recherchieren besser |
| Evidenzgraph (Quellen, Aussagen, Reviews, Freigaben) | Fundament, eigener Meilenstein M2 | Reduziert auf ein **Begründungsfeld** je Annahme (Text, Links, Datum, Vertrauensnotiz) | Herkunft bleibt sichtbar, ohne eigenen Workflow |
| Domäne | Terminplanung als einzige Referenzdomäne | Generischer Kern, fünf Tutorials aus verschiedenen Domänen | Generalität ist das Produktversprechen |
| Szenarien | Ein Szenario im MVP | Hauptszenario plus abgeleitete Unterszenarien und Vergleich im MVP | Kern des gewünschten Arbeitsablaufs |
| Korrelation | Spätere Erweiterung (Soll) | Im MVP (Korrelationsgruppen) | Portfolio-Beispiel braucht sie |
| Risikomatrix | Als „nicht fundamental“ eingestuft | Quantitativ aus der Simulation abgeleitet, nicht ordinal geschätzt | Gewünschte Sicht, aber wissenschaftlich begründet |
| Analytische Verifikation | Interne Referenztests | Zusätzlich sichtbar in Tutorials | Vertrauen in die Numerik aufbauen |
| Architektur | FastAPI, PostgreSQL, Job-Worker, Objektspeicher | Lokale App: Kern + Streamlit + Dateien | Selbstnutzung zuerst; Betrieb ist kein Ziel der Phase 1 |
| Produktisierung, SaaS, Mandanten | Meilensteine M5/M6 | Nichtziel der Phase 1 | Fokus |

### 1.2 Was unverändert gilt (Verweise auf die Erstanalyse)

- **Verteilungen und Eingabemodi** („Wissenschaftliches Verteilungsmodell“): kanonische Parameter
  speichern, Konflikte erklären statt still nähern, Grenzen ≠ Quantile.
- **Keine stille Reparatur** ungültiger Eingaben (Abschneiden, Matrixprojektion, Nullsetzen sind
  sichtbare Modelländerungen).
- **Ergebnissprache** („Quantile korrekt erklären“): „Im Modell liegen 90 % der Werte unter …“,
  nicht „mit 90 % Sicherheit“.
- **Ereigniswahrscheinlichkeiten** mit Wilson-Intervall; null Treffer ≠ 0 % Risiko.
- **Konvergenz** statt fester Iterationszahl als Gütenachweis.
- **Szenario ≠ Wahrscheinlichkeit;** keine automatische Szenariomischung.
- **Sensitivität:** keine „Risikobeiträge in Prozent“ aus Korrelationskoeffizienten.
- **Sicherer Ausdruckseditor:** kein `eval`, keine Importe, begrenzte Tiefe und Größe.
- **Reproduzierbarkeit:** Seed, Generator, Versionen und Modellstand je Lauf speichern.

***

## 2. Produktbild

> **Ein lokales Werkzeug, mit dem ich ein Weltmodell meines Problems aus wenigen generischen
> Bausteinen zusammenstelle, es per Monte-Carlo-Simulation auswerte, in Szenarien abwandle und die
> Ergebnisse vergleiche – mit sichtbaren Annahmen und nachvollziehbarer Numerik.**

**Leitfrage der App:**

> Wie ist meine Zielgröße unter meinen Annahmen verteilt, was treibt sie, und wie verändert sie
> sich, wenn ich Annahmen ändere?

**Nutzer der Phase 1:** ich selbst – fachkundig, kann Verteilungen aus eigener Recherche begründen,
will Modelle schnell aufbauen und tief auswerten.

**Arbeitsteilung mit externen Werkzeugen:**

```text
Externe Recherche (Perplexity, Claude Code, Literatur, eigene Daten)
        ↓  Ergebnis: Verteilung + Begründung, ggf. YAML-Entwurf eines Teilmodells
Risk Pilot: Modell bauen → validieren → simulieren → Szenarien → vergleichen → verstehen
```

Das **YAML-Modellformat** ist die Schnittstelle: Ein externer Assistent kann einen Modellentwurf
oder einzelne Verteilungen als YAML liefern, die App importiert und validiert ihn. Damit bleibt KI
nützlich, ohne Teil der App zu sein.

***

## 3. Die Beispielprobleme als Anforderungsquelle

Die vier genannten Probleme sind keine Fachmodule, sondern Prüfsteine für den generischen Kern.

| Problem | Struktur | Benötigte Bausteine | Zielgröße | Wichtigste Auswertung |
|---|---|---|---|---|
| **Terminplanung** | Netzplan: Vorgänge in Serie (Summe) und parallel (Maximum) | Unsichere Dauern, Ereignisse (Nacharbeit), `max` | Fertigstellungstermin | Kritischer Pfad, Kritikalität, P(Termin gehalten) |
| **Kernfusionskraftwerk** | Technologien mit unsicherem Reifezeitpunkt, Scheitern möglich, gegenseitige Beschleunigung oder Blockade | Ereignisse, bedingte Verteilungen, Schwellen, nichtlineare Ausdrücke, Zeithorizont | Jahr der ersten kommerziellen Anlage | Anteil „nicht im Horizont“, Kritikalität der Technologien, Tornado |
| **Bahnreise** | Verspätung → Anschluss erreicht oder nicht → Ausweichoption | Mischverteilungen, Bedingungen (`if`), Auswahl der besten Alternative (`min`) | Ankunftszeit | P(Ankunft vor X), mehrgipflige Verteilung, Sweep der Umstiegszeit |
| **Portfolio** | Korrelierte Renditen, multiplikative Entwicklung über die Zeit | Korrelationsgruppen, Lognormal, Szenarioparameter (Gewichte) | Endvermögen | P(Verlust), VaR/ES, Szenariovergleich (Gewichte, Krisenkorrelation) |

**Daraus abgeleitete Kernanforderungen:**

1. Lineare **und** nichtlineare funktionale Abhängigkeiten (`max`, `min`, `if`, Schwellen,
   Potenzen, Interpolationstabellen).
2. **Bedingte Verteilungen:** Parameter einer Verteilung dürfen von anderen Knoten abhängen.
3. **Ereignisse und diskrete Verzweigungen** mit Mischverteilungen als Ergebnis.
4. **Statistische Abhängigkeit** über Korrelationsgruppen, wo kein Wirkungsmodell bekannt ist.
5. **Zeithorizont und Zensierung:** Ergebnisse dürfen „nicht innerhalb des Horizonts erreicht“
   sein; Quantile werden dann als „> Horizont“ ausgewiesen statt verfälscht.
6. **Mehrgipflige Ergebnisse** werden korrekt dargestellt (Median ≠ wahrscheinlichster Wert).

***

## 4. Modellierungskern

### 4.1 Bausteine (Knotentypen)

| Typ | Bedeutung | Beispiel |
|---|---|---|
| `constant` | Fester Wert | Umstiegszeit 7 min |
| `uncertain` | Zufallsgröße mit Verteilung; Parameter dürfen Ausdrücke sein | Dauer Vorgang A ~ PERT(8, 10, 15) |
| `event` | Bernoulli-Ereignis mit Wahrscheinlichkeit (auch als Ausdruck) | Materialtest scheitert, p = 0.3 |
| `choice` | Diskrete Auswahl mit Gewichten | Route: {ICE, Regio, Bus} |
| `derived` | Berechnete Größe aus Ausdruck | `ende = max(pfad1, pfad2)` |
| `output` | Zielgröße mit Einheit, Zielrichtung, Schwellen | Ankunftszeit, Ziel ≤ 14:30 |

- **Entscheidungen** werden in Phase 1 als Szenarioparameter (`constant`, im Unterszenario
  überschrieben) abgebildet, nicht als eigener Knotentyp.
- **Jeder Knoten** hat: stabile ID, Anzeigename, Einheit, Beschreibung, Begründung (Freitext,
  Links, Datum), Tags (für Gruppen und Risikomatrix).
- **Regel aus der Erstanalyse:** Jeder unsichere Knoten wird pro Iteration genau einmal gezogen;
  alle Referenzen verwenden denselben Wert (gemeinsamer Treiber).

### 4.2 Drei Arten von Abhängigkeiten

1. **Funktional (Ausdruck)** – bevorzugt. Lineare und nichtlineare Zusammenhänge:
   `kosten = dauer * tagessatz + if(nacharbeit, 50_000, 0)`.
2. **Bedingte Verteilung** – Parameter verweisen auf andere Knoten:
   `entwicklungszeit_B ~ Lognormal(mean = 12 - 4 * durchbruch_A, sd = 3)`.
3. **Statistisch (Korrelationsgruppe)** – nur wenn kein Wirkungsmodell bekannt ist. Gaussian
   Copula mit Eingabe als **Rangkorrelation (Spearman)**; Matrix wird auf Symmetrie, Bereich und
   positive Semidefinitheit geprüft und **nicht still repariert**; erreichte Korrelation wird
   nach dem Lauf ausgewiesen.

**Struktur:** Das Modell ist ein gerichteter azyklischer Graph. Zyklen werden mit Angabe des
Zyklus abgewiesen. Rückkopplungen über die Zeit sind erst mit der Periodendimension möglich
(Abschnitt 4.6).

### 4.3 Ausdruckssprache

- **Syntax:** Python-ähnliche Ausdrücke, geparst mit `ast` und gegen eine Whitelist geprüft,
  ausgewertet vektorisiert mit NumPy über alle Iterationen gleichzeitig.
- **Operatoren:** `+ - * / ** %`, Vergleiche, `and or not`.
- **Funktionen (Startumfang):** `min, max, abs, exp, log, sqrt, floor, ceil, clip, if(c, a, b),
  interp(x, xs, ys)` (stückweise linear, für nichtlineare Kennlinien), `sum(...)`.
- **Kritikalitätserfassung:** `max` und `min` merken pro Iteration, welches Argument gewonnen hat
  (Basis für kritische Pfade, Abschnitt 6.3).
- **Grenzen:** maximale Ausdruckslänge und -tiefe, keine Attribute, keine Indizes außer in
  definierten Funktionen, keine Namen außer Knoten-IDs und Whitelist-Funktionen.
- **Fehler** nennen Knoten, Position und Ursache in Klartext.

### 4.4 Verteilungen und Eingabe tiefen Wissens

**Startportfolio** (Erstanalyse plus Ergänzungen für Zeit-bis-Ereignis, Zählgrößen und frei
vorgegebene Verteilungen):

| Familie | Typische Verwendung | Eingabemodi |
|---|---|---|
| Uniform | Begründeter Bereich ohne Präferenz | Grenzen |
| Dreieck, Beta-PERT | Experten-Dreipunktschätzung | Min/Modus/Max (+ λ bei PERT, Standard 4 als Konvention) |
| Normal, trunkiert normal | Symmetrische Abweichungen | Mittelwert/Std, Quantile |
| Lognormal | Positive, rechtsschiefe Größen | Mittelwert/Std, Median/Faktor, P10/P90 |
| Beta | Anteile, begrenzte Größen | α/β, Mittelwert/Std, Quantile |
| Student-t | Symmetrisch mit schweren Rändern | Lage/Skala/ν (ν > 2) |
| Exponential, Gamma, Weibull | Wartezeiten, Zeit bis Ereignis, Verspätungen | Parameter, Mittelwert, Quantile |
| Bernoulli, Diskret | Ereignisse, Auswahl | p bzw. Werte + Gewichte |
| Poisson | Anzahl Ereignisse im Zeitraum | Rate |
| **Stützstellen-Verteilung** | Eigene Expertenkurve aus Recherche | Quantilpaare (z. B. P0, P10, P50, P90, P100), stückweise linear in der CDF |
| **Empirisch** | Eigene Messdaten | Werteliste oder CSV-Spalte, Ziehen mit Zurücklegen |
| Mischung (später) | Mehrere Regime | Komponenten + Gewichte |

**Eingabe aus externer Recherche:**

- Jede Verteilung ist über den für die Quelle natürlichen Modus eingebbar (z. B. „P10 = 2031,
  P50 = 2038, P90 = 2050“). Die App bestimmt die kanonischen Parameter, zeigt die Abweichung des
  Fits und bietet die Stützstellen-Verteilung an, wenn keine Familie passt.
- **Vorschau** direkt beim Eintragen: Dichte, CDF, Mittelwert, Median, P5/P95, Anteil unzulässiger
  Werte (z. B. negative Dauern).
- **Begründungsfeld** für Recherchenotizen, Links und das Datum der Recherche.

**Erweiterbarkeit:** Verteilungen und Ausdrucksfunktionen stehen in Registern. Eine neue Familie
ist eine Klasse mit Parametervalidierung, Sampler, optional analytischer CDF/PDF und einem Test –
ohne Änderung an Engine oder Oberfläche.

### 4.5 Simulation

- **Vektorisiert:** Knoten in topologischer Reihenfolge, jeder Knoten als Array über alle N
  Iterationen. Ziel: Referenzmodelle mit ≤ 100 Knoten und 100 000 Iterationen in wenigen Sekunden
  (Messziel, keine Zusage vor Messung).
- **Zufallsströme je Knoten:** Aus Lauf-Seed und **Knoten-ID** wird pro Knoten ein eigener
  NumPy-`SeedSequence`-Strom abgeleitet. Folge: Hinzufügen oder Ändern eines Knotens verändert die
  Ziehungen der übrigen Knoten nicht. Das ergibt **gemeinsame Zufallszahlen** über alle
  Szenarien und macht Szenariodifferenzen rauscharm und paarweise vergleichbar.
- **Standard N:** 10 000 für interaktives Arbeiten, 100 000 für Endauswertungen; einstellbar.
- **Numerische Güte je Kennzahl:** Standardfehler des Mittelwerts, Konfidenzintervalle für
  Quantile (Ordnungsstatistik), Wilson-Intervall für Wahrscheinlichkeiten, Konvergenzplot über N.
  Unzureichende Güte wird markiert.
- **Zensierung:** Optionaler Horizont je Ausgabe; Werte jenseits des Horizonts zählen als
  „nicht erreicht“ und werden gesondert ausgewiesen.
- **Ergebnisspeicher:** Rohstichproben aller Ausgaben und markierten Zwischengrößen plus Metadaten
  (Modell-Hash, Szenario, Seed, N, Versionen) in `data/`.

### 4.6 Zeitdimension (Perioden)

Portfolio mit Rebalancing, jährliche Budgets oder Lernkurven brauchen wiederholte Schritte. Zwei
Wege:

- **A – ohne Perioden (MVP):** Horizontgrößen direkt modellieren (z. B. Summe der
  Log-Renditen über T Jahre). Reicht für Buy-and-Hold, Terminpläne, Bahn, Kernfusion.
- **B – Periodendimension (später):** Knoten können über Perioden indiziert sein; Funktionen
  `prev(x)`, `cumsum`, `cumprod`. Ermöglicht Rebalancing und zeitliche Rückkopplung ohne Zyklen
  im Graphen.

**Empfehlung:** A im MVP, B als eigener Meilenstein, sobald ein konkretes Modell ihn braucht.

***

## 5. Szenarien, Vergleich und Sensitivität

### 5.1 Hauptszenario und Unterszenarien

- **Hauptszenario** = Modell mit Basiswerten. Jedes Modell hat genau eines.
- **Unterszenario** = „Szenario duplizieren“ (Copy & Paste) und dann ändern. Gespeichert wird
  nur die **Differenz (Overrides)** zum Elternszenario:
  - Parameterwerte und Konstanten (inkl. Entscheidungen),
  - Verteilungsfamilie oder -parameter eines Knotens,
  - Ereigniswahrscheinlichkeiten,
  - Strukturvarianten über Schalterkonstanten (`if(variante_b, …, …)`) oder alternativen Ausdruck,
  - Korrelationswerte.
- **Vererbung:** Ändert sich das Hauptszenario, erben Unterszenarien die Änderung, sofern sie den
  Wert nicht selbst überschreiben. „Loslösen“ macht ein Unterszenario zur vollständigen Kopie.
- **Baumstruktur:** Unterszenarien dürfen selbst Unterszenarien haben (z. B. „Hohe Förderung“ →
  „Hohe Förderung + Materialproblem“).
- **Diff-Ansicht:** Für jedes Szenario sichtbar, welche Werte es gegenüber dem Elternszenario
  ändert, mit Begründung je Änderung.

### 5.2 Vergleich

- Überlagerte CDFs und Histogramme mehrerer Szenarien für dieselbe Ausgabe.
- Kennzahlentabelle mit Differenzen (Mittelwert, P10/P50/P90, P(Ziel)), inklusive numerischer
  Unsicherheit der Differenz.
- **Paarweiser Vergleich** dank gemeinsamer Zufallszahlen: Verteilung der Differenz B − A und
  P(B besser als A).
- Standard ist **Nebeneinanderstellen**; gewichtete Mischung nur ausdrücklich mit begründeten
  Gewichten (Erstanalyse, „Keine automatische Szenariomischung“).

### 5.3 Sensitivität

| Verfahren | Frage | Umsetzung |
|---|---|---|
| **Tornado (Ein-Faktor-Variation)** | Wie stark ändert sich die Kennzahl, wenn eine Eingabe auf ihr P10 bzw. P90 fixiert wird? | Automatisch erzeugte Hilfsszenarien mit gemeinsamen Zufallszahlen |
| **Parameter-Sweep** | Wie hängt die Kennzahl von einem Parameter ab? | Kurve, z. B. P(Anschluss) über Umstiegszeit 0–20 min |
| **Rangkorrelation** | Welche Eingaben bewegen sich mit dem Ergebnis? | Spearman je Eingabe, ausdrücklich als deskriptiv gekennzeichnet |
| **Varianzbasiert (Sobol)** | Welche Unsicherheit erklärt welchen Anteil der Streuung? | Später, mit geprüften Voraussetzungen |

Sensitivitätsläufe sind gewöhnliche Unterszenarien und damit im Vergleich wiederverwendbar.

***

## 6. Auswertungen und Visualisierung

### 6.1 Ergebnisansicht je Ausgabe

- Histogramm und CDF, Mittelwert, Median, wählbare Quantile, P(Ziel erreicht), Anteil „nicht im
  Horizont“, numerische Güte.
- Hinweis bei Mehrgipfligkeit (Median liegt in einem Tal der Verteilung).
- „Dieses Ergebnis gilt für …“: Szenario, Modellstand, N, Seed, Zeitpunkt.

### 6.2 Abhängigkeitsgraph

- Darstellung des Modells als Graph: Knotentyp als Form, Abhängigkeitsart als Linienart
  (funktional durchgezogen, Korrelation gestrichelt).
- Einfärbung wahlweise nach Sensitivität, Kritikalität oder Begründungsstatus (fehlende
  Begründung sichtbar).
- Der Graph ist eine Ansicht; bearbeitet wird über Formular oder YAML (Abschnitt 8).

### 6.3 Kritischer Pfad und Kritikalität – generisch

- In jeder Iteration ist der **entscheidende Pfad** die Kette, die man von der Ausgabe rückwärts
  erhält, indem man an jedem `max`/`min` dem gewinnenden Argument folgt.
- **Kritikalitätsindex eines Knotens** = Anteil der Iterationen, in denen er auf dem
  entscheidenden Pfad liegt. Die Indizes summieren sich nicht zu 100 % (parallele kritische
  Pfade, Gleichstände).
- **Häufigste Pfadkonstellationen** mit Anteil.
- Funktioniert für Terminpläne (klassischer kritischer Pfad), Technologieentwicklung (welche
  Technologie zuletzt reif wird) und Routenwahl (welche Alternative gewählt wird).

### 6.4 Risikomatrix aus der Simulation

- Für jeden `event`-Knoten (und optional jede `choice`-Ausprägung):
  - **x-Achse:** Eintrittswahrscheinlichkeit, aus der Simulation (mit Intervall), nicht geschätzt.
  - **y-Achse:** Auswirkung auf die gewählte Ausgabe, z. B. E[Y | Ereignis] − E[Y | kein Ereignis]
    oder Differenz im P80.
- Darstellung als Streudiagramm mit optionalen Klassengrenzen (z. B. 5×5-Raster nur als Lesehilfe).
- **Grenze im UI benennen:** Bei gemeinsamen Ursachen enthält die bedingte Differenz auch Effekte
  korrelierter Größen; Wechselwirkungen mehrerer Ereignisse sind nicht additiv.

### 6.5 Weitere Sichten

- Konvergenzplot je Kennzahl.
- Streudiagramm Eingabe gegen Ausgabe (für nichtlineare Zusammenhänge).
- Export: Kennzahlen als CSV, Rohstichproben als Parquet, Bericht als HTML.

***

## 7. Tutorials

Jedes Tutorial ist eine YAML-Datei in `examples/`, mit Erklärtext in der App, und läuft zugleich
als Regressionstest mit festem Seed und definierten Toleranzen. Zahlen in T3–T5 sind
**illustrative Platzhalter**, keine Recherchewerte.

| Nr | Titel | Lernziel | Analytische Referenz |
|---|---|---|---|
| T1 | Faltung: Summe zweier Unsicherheiten | Bausteine, Simulation, Konvergenz | Vollständig (Dichte, CDF, Momente) |
| T2 | Mini-Terminplan: Serie und Parallelität | Kritischer Pfad, Merge-Bias | Vollständig (CDF, Mittelwert, Kritikalität) |
| T3 | Bahnreise mit Anschluss | Bedingungen, Mischverteilung, Sweep | Teilweise (P(Anschluss)) |
| T4 | Portfolio aus drei Anlagen | Korrelation, Szenarien, Tail-Kennzahlen | Teilweise (Mittelwert, Std, Einzelanlagen) |
| T5 | Wann kommt das Fusionskraftwerk? | Nichtlineare Kopplung, Ereignisse, Horizont, Tornado, Risikomatrix | Keine – reines Weltmodell |

### T1 – Faltung: Summe zweier Unsicherheiten

- **Modell:** X₁, X₂ ~ U(0, 1) unabhängig, S = X₁ + X₂.
- **Analytisch:** Faltung der Dichten ergibt die Dreiecksverteilung
  f(s) = s für 0 ≤ s ≤ 1, f(s) = 2 − s für 1 < s ≤ 2; E[S] = 1, Var[S] = 1/6.
- **Zusätzlich numerische Faltung** auf einem Gitter (FFT) als dritte Kurve – zeigt das Verfahren,
  das auch für Summen ohne geschlossene Form funktioniert.
- **Varianten per Unterszenario:** n Summanden (Irwin-Hall, Übergang zur Normalverteilung),
  Exp(λ) + Exp(λ) = Gamma(2, λ).
- **Anzeige:** Histogramm mit analytischer Dichte, CDF-Überlagerung, Tabelle der Momente,
  maximaler CDF-Abstand (Kolmogorov) gegen die **DKW-Schranke**
  ε = √(ln(2/α) / (2N)); bei N = 100 000 und α = 0.001 ist ε ≈ 0.0062.
- **Abnahme:** Kolmogorov-Abstand < ε; Mittelwert innerhalb 4 Standardfehlern.

### T2 – Mini-Terminplan: Serie und Parallelität

- **Modell:** Pfad 1: A ~ N(10, 2²), danach B ~ N(15, 3²). Pfad 2: C ~ N(24, 4²). Ende = max(P₁, P₂).
- **Analytisch:**
  - P₁ ~ N(25, 13), P₂ ~ N(24, 16) (Faltung zweier Normalverteilungen).
  - CDF des Endes: F(t) = Φ₁(t) · Φ₂(t) (Maximum unabhängiger Größen).
  - Mittelwert nach Clark: E[Ende] ≈ 26.69 Tage – deutlich mehr als der deterministische Wert 25
    (**Merge-Bias**).
  - Kritikalität von Pfad 1: P(P₁ > P₂) = Φ((25 − 24)/√29) ≈ 0.574.
- **Anzeige:** Simulierte gegen analytische CDF, Mittelwert, simulierter Kritikalitätsindex gegen
  0.574. Geprüft: Die Simulation mit N = 10⁶ liefert 26.69 und 0.574.
- **Abnahme:** Kolmogorov-Abstand < DKW-Schranke; Kritikalität innerhalb des Wilson-Intervalls um
  den analytischen Wert.
- **Ausbau im Tutorial:** Ereignis „Nacharbeit an B“ (p = 0.2, +5 Tage) – ab hier keine
  geschlossene Lösung mehr, Übergang zur reinen Simulation.

### T3 – Bahnreise mit Anschluss

- **Modell:** Zug 1 ist mit 60 % pünktlich, sonst Verspätung ~ Exp(Mittel 6 min). Planmäßige
  Umstiegszeit 7 min, Mindestumstiegszeit 2 min (Puffer 5 min). Anschluss erreicht →
  Ankunft = Plan + Verspätung Zug 2. Verpasst → Minimum aus „nächster Zug (+60 min)“ und
  „Bus (+35 min, eigene Unsicherheit)“.
- **Analytisch:** P(Anschluss) = 0.6 + 0.4 · (1 − e^(−5/6)) ≈ 0.826.
- **Lernziele:** Mehrgipflige Ankunftsverteilung (Median ≠ häufigster Wert), Sweep der
  Umstiegszeit, Unterszenario „früherer Zug“, Kritikalität der Ausweichrouten.
- **Erweiterung:** Abfahrtsverspätung des Anschlusszugs (Anschluss wartet) als zweite Zufallsgröße.

### T4 – Portfolio aus drei Anlagen

- **Modell:** Drei Anlagen (z. B. Aktien, Anleihen, Gold) mit jährlichen Log-Renditen
  N(μᵢ, σᵢ²), Korrelationsgruppe, Horizont T Jahre, Buy-and-Hold: Wᵢ = w_i · W₀ · exp(Lᵢ) mit
  Lᵢ ~ N(T·μᵢ, T·σᵢ²).
- **Analytisch:** E[W_T] = W₀ Σ wᵢ exp(T μᵢ + T σᵢ²/2); Varianz über
  Cov(e^{Lᵢ}, e^{Lⱼ}) = E[e^{Lᵢ}] E[e^{Lⱼ}] (e^{T ρᵢⱼ σᵢ σⱼ} − 1); Quantile je Einzelanlage.
  Dabei Hinweis: Die Copula-Eingabe ist Rangkorrelation; für die analytische Prüfung wird die
  zugehörige Korrelation der Normalvariablen verwendet.
- **Szenarien:** Gewichtungen (Entscheidung), „Krisenkorrelation“ (ρ → 0.8), höhere Volatilität.
- **Auswertungen:** P(Verlust), VaR/ES, Szenariovergleich, Rangkorrelation.

### T5 – Wann kommt das Fusionskraftwerk?

- **Modell (illustrativ):** Schlüsseltechnologien wie Plasmaeinschluss, supraleitende Magnete,
  neutronenresistente Materialien, Tritium-Brüten, Wärmeauskopplung. Je Technologie:
  Reifejahr (Stützstellen-Verteilung) und Scheiternswahrscheinlichkeit im Horizont.
- **Nichtlineare Kopplungen:** Ein Durchbruch bei Magneten verkürzt die Plasmaentwicklung
  (bedingte Verteilung); Materialqualifikation braucht eine Testanlage (Reihenfolge);
  Demonstrationsanlage startet bei max(Reifejahre) + Bauzeit; kommerzielle Anlage nach
  erfolgreicher Demo + Bauzeit; Finanzierung als Szenarioparameter mit Kennlinie (`interp`).
- **Horizont:** 2100; Anteil „nicht bis 2100“ wird ausgewiesen.
- **Szenarien:** „Hohe Förderung“, „Materialproblem“, Kombination.
- **Auswertungen:** P(vor 2045/2060), Kritikalität der Technologien, Tornado, Risikomatrix der
  Scheiternsereignisse.

***

## 8. Bedienung

- **Start:** Tutorialgalerie, neues Modell (leer oder aus Vorlage), Modell öffnen/importieren.
- **Als Vorlage kopieren:** Jedes Tutorial und jedes eigene Modell lässt sich samt Szenarien als
  neues Modell kopieren und anpassen; das Original bleibt unverändert.
- **Navigation:** Modell → Szenarien → Simulation → Ergebnisse → Vergleich → Sensitivität.
- **Modell bearbeiten auf zwei gleichwertigen Wegen** auf demselben Schema:
  - **Formular:** Knotentabelle, Karte je Knoten mit Verteilungsvorschau und Begründung.
  - **YAML-Editor:** für schnelle Bearbeitung und für Entwürfe aus externen Werkzeugen.
- **Live-Validierung:** unbekannte Namen, Zyklen, Parametergrenzen, unzulässige Wertebereiche,
  ungültige Korrelationsmatrix – jeweils mit Erklärung, nie mit stiller Korrektur.
- **Kein grafischer Drag-and-drop-Editor** in Phase 1; der Graph ist Ansicht und Navigation.
- **Streamlit-Betrieb:** eigener, nicht standardmäßiger Port in der Projektkonfiguration;
  Beenden-Schaltfläche, die nur den eigenen Prozess per SIGTERM beendet.

### Beispiel des Modellformats (Entwurf)

```yaml
model: mini-terminplan
units: {time: d}
nodes:
  A: {type: uncertain, dist: normal, mean: 10, sd: 2, why: "Erfahrungswert Projekt X"}
  B: {type: uncertain, dist: normal, mean: 15, sd: 3}
  C: {type: uncertain, dist: normal, mean: 24, sd: 4}
  nacharbeit: {type: event, p: 0.2}
  pfad1: {type: derived, expr: "A + B + if(nacharbeit, 5, 0)"}
  ende: {type: output, expr: "max(pfad1, C)", target: {le: 30}}
scenarios:
  basis: {}
  schnelleres_B:
    parent: basis
    overrides: {B: {mean: 12}}
    why: "Zusätzliches Team"
```

***

## 9. Architektur

| Schicht | Inhalt | Regel |
|---|---|---|
| Kern (rein) | Schema (Pydantic), Ausdrucksparser, Verteilungsregister, Engine, Statistik, Sensitivität, Kritikalität, Risikomatrix, analytische Referenzen | Keine I/O, vollständig typisiert, direkt getestet |
| Adapter | YAML lesen/schreiben, Ergebnisse in `data/` speichern, Export | Einzige Stelle für Datei-I/O |
| Einstieg | Streamlit-App | Dünn: verdrahtet Adapter und Kern |

**Vorgeschlagene Paketstruktur** (wird erst mit den Meilensteinen angelegt):

```text
src/app/
    model/        schema.py, validate.py, scenarios.py (Overrides, Vererbung)
    expr/         parser.py (ast-Whitelist), functions.py (Register)
    dists/        registry.py, families/*.py, fit.py (Quantile → Parameter)
    engine/       sampler.py (Ströme je Knoten), evaluate.py, copula.py
    analysis/     stats.py, sensitivity.py, criticality.py, riskmatrix.py, analytic.py
    adapters/     files.py, export.py
    ui/           streamlit_app.py, pages/
examples/         t1_faltung.yaml … t5_fusion.yaml
```

**Abhängigkeiten (Lizenz Apache-2.0-kompatibel):** NumPy, SciPy (BSD), Pydantic (MIT), PyYAML
(MIT), Streamlit (Apache-2.0), Plotly (MIT), NetworkX (BSD) für Graphalgorithmen; Graph-Layout
über Plotly oder Graphviz (zu prüfen).

**Tests:** Tutorials T1/T2 als analytische Referenztests im schnellen Gate; Eigenschaftstests
(Umbenennen ändert nichts, ungenutzter Knoten ändert nichts, Skalierung skaliert); langlaufende
statistische Tests als eigene Markierung außerhalb des 60-Sekunden-Gates – nur mit ausdrücklicher
Freigabe.

***

## 10. Meilensteine (Vorschlag)

Jeder Meilenstein endet mit etwas Benutzbarem.

| Meilenstein | Ergebnis | Zentrale Abnahme |
|---|---|---|
| **M1 – Rechenkern** | Schema, Ausdruckssprache, Verteilungen (ohne Stützstellen/Empirisch), Engine mit Strömen je Knoten, Grundstatistik | T1 und T2 bestehen ihre analytischen Abnahmen als Tests |
| **M2 – Erste App** | Streamlit: YAML laden/bearbeiten, validieren, simulieren, Ergebnisansicht; T1/T2 mit analytischer Überlagerung | T1/T2 in der App durchspielbar |
| **M3 – Szenarien und Vergleich** | Haupt-/Unterszenarien mit Overrides und Vererbung, Diff-Ansicht, Vergleich, paarweise Differenzen | Szenarioänderung wirkt nur auf überschriebene Knoten; Differenzen mit gemeinsamen Zufallszahlen |
| **M4 – Struktur-Auswertungen** | Abhängigkeitsgraph, Kritikalität und Pfadkonstellationen, Tornado, Sweep, Rangkorrelation, Risikomatrix | Kritikalität in T2 trifft den analytischen Wert |
| **M5 – Abhängigkeiten und Tutorials** | Korrelationsgruppen, Stützstellen- und empirische Verteilung, Quantil-Fit, Horizont/Zensierung, T3–T5 | T3 trifft P(Anschluss), T4 trifft E/Std; T5 läuft |
| **M6 – Formular-Editor und Export** | Knotenkarten mit Verteilungsvorschau, CSV/Parquet/HTML-Export, Dokumentation der Erweiterungspunkte | Ein eigenes Modell vollständig ohne YAML-Editor aufbaubar |
| **Später** | Periodendimension, Mischverteilungen, Sobol-Indizes, LHS/Sobol-Sampling, Datenfit | Nach Bedarf |

***

## 11. Nichtziele der Phase 1

- Web-Recherche, LLM-Anbindung, automatische Parameterfindung oder -prüfung im Tool.
- Evidenzgraph, Review- und Freigabeworkflow, Mehrbenutzerbetrieb.
- Datenbank, Server-Betrieb, Authentifizierung, Mandantentrennung, Bezahlfunktionen.
- Grafischer Drag-and-drop-Modelleditor.
- Ressourcen- und Kalenderlogik in Terminplänen.
- Zyklische Modelle und kontinuierliche Systemdynamik (Differentialgleichungen).
- Bayessche Inferenz und automatische „beste Verteilung“.
- Automatische Szenariomischung oder Szenariowahrscheinlichkeiten.
- Anlageberatung, Derivatebewertung, Marktpreisprozesse.

***

## 12. Entscheidungen (getroffen am 27.10.2026)

| Nr | Entscheidung | Ergebnis |
|---|---|---|
| E1 | UI-Framework | **Streamlit** |
| E2 | Modellformat | **YAML** als Quelle, Pydantic-Schema als Vertrag |
| E3 | Szenario-Speicherung | **Overrides mit Vererbung**, „Loslösen“ als Option |
| E4 | Periodendimension | **Nicht im MVP**; T4 als Buy-and-Hold, kein Rebalancing |
| E5 | Sprache | **Oberfläche Deutsch, Code und Bezeichner Englisch** |
| E6 | Zahlen in T3–T5 | **Illustrative Platzhalter.** Jedes Tutorial lässt sich als Vorlage für ein eigenes Modell kopieren und anpassen, damit neue Modelle nicht bei null beginnen |
| E7 | Gate und `ideas/` | **`ideas/` ist von der Dokumentgrößenprüfung ausgenommen**; Links werden weiter geprüft |

**Nächster Schritt:** [PRD.md](../PRD.md) mit M1–M6 und testbaren Abnahmekriterien ist daraus
abgeleitet. Später folgen vertiefende Inhalte nach `docs/model-semantics.md` und
`docs/statistical-methods.md`.
