# Pflichtenheft M2 — Erste App mit Lernpfad „Abhängigkeitsmuster“

**Stand:** 28. Oktober 2026, Entscheidungen E1–E8 eingearbeitet, M2 abgeschlossen (Abschnitt 13) · **Bezug:**
[PRD.md](../../PRD.md), Meilenstein M2 (AK 1–11, Edge cases) · **Voraussetzung:**
[m1-rechenkern.md](m1-rechenkern.md) vollständig umgesetzt

Dieses Pflichtenheft legt fest, **wie** M2 umgesetzt wird. Das PRD bleibt der Vertrag für das
**Was**; bei Widerspruch gilt das PRD, und der Widerspruch wird hier korrigiert.

***

## 1. Umfang

**In M2:**

- Streamlit-App mit den Seiten Start, Lernpfad, Modell, Simulation, Ergebnisse, Läufe.
- YAML-Editor mit Live-Validierung über den M1-Meldungskatalog.
- Ergebnisansicht je Ausgabe mit Kennzahlen in Modellsprache; analytische Überlagerung für T1/T2.
- Ablage und Neuladen von Läufen in `data/runs/`, Kopieren von Vorlagen nach `data/models/`.
- **Lernpfad „Abhängigkeitsmuster“** (neu): zehn kurze Lektionen plus Abschlusslektion, je ein
  Mini-Modell, Erklärtext, Vorhersagefrage, eine Stellschraube mit Vorher/Nachher-Vergleich und
  – wo möglich – analytischer Referenz (Abschnitt 6).
- Beenden-Schaltfläche (SIGTERM an die eigene PID).

**Nicht in M2:** Szenarien und Overrides als Modellbestandteil (M3; die Stellschraube des
Lernpfads ist eine flüchtige Änderung im Speicher, Abschnitt 6.4), Graph, Kritikalität, Tornado,
Sweep (M4), Korrelationsgruppen, Horizont, T3–T5 (M5), Formular-Editor und Export (M6).

***

## 2. Modulstruktur

```text
src/app/
    present/                 rein, ohne Streamlit-Import, voll getestet
        text.py              Ergebnissätze in Modellsprache, Zahlenformat (de)
        figures.py           Plotly-Figuren: Histogramm, CDF, Überlagerungen
        references.py        Zuordnung Modell-ID → analytische Referenz (T1, T2, Lektionen)
        validation.py        ModelError/Issue → Liste (Zeile, Knoten, Text) für den Editor
    lessons/
        catalog.py           Lernpfad-Manifest laden (Text → Lesson-Objekte), rein
        knob.py              with_value(model, node_id, field, value) -> Model, rein
        reference.py         analytische Referenzen der Lektionen (Abschnitt 6.3)
    adapters/
        files.py             + list_examples(), read_text(), copy_model() (exklusiv anlegen)
        runs.py              save_run(), list_runs(), load_run()
        process.py           shutdown(): os.kill(os.getpid(), SIGTERM)
        settings.py          DATA_DIR aus Umgebungsvariable RISK_PILOT_DATA_DIR (Standard data/)
    ui/
        main.py              Einstieg, st.navigation, Beenden-Schaltfläche in der Seitenleiste
        state.py             Schlüssel und Zugriffe auf st.session_state
        pages/               start.py, lernpfad.py, modell.py, simulation.py,
                             ergebnisse.py, laeufe.py
examples/
    t1_faltung.yaml, t2_terminplan.yaml, t1_faltung.md, t2_terminplan.md
    lernpfad/
        lernpfad.yaml        Manifest (Abschnitt 6.2)
        a01_serie.yaml/.md … a11_zusammenspiel.yaml/.md
.streamlit/config.toml       server.port = 8642, headless, Telemetrie aus
```

- `ui/` bleibt dünn: Widgets lesen, `present/`, `lessons/` und Adapter aufrufen, Ergebnis rendern.
  Alles, was sich ohne Streamlit prüfen lässt, liegt in `present/` und `lessons/`.
- **Laufzeitabhängigkeiten:** `streamlit` (Apache-2.0), `plotly` (MIT). Keine Editor-Komponente
  (E3).
- Start: `uv run streamlit run src/app/ui/main.py`; README nennt Port und Beenden.
- `docs/architecture.md`: Schichten `present/`, `lessons/` (rein) und `ui/` (Einstieg) ergänzen.

***

## 3. Seiten und Bedienablauf

| Seite | Inhalt |
|---|---|
| Start | Galerie: Lernpfad, T1, T2, eigene Modelle aus `data/models/`; je Karte „Öffnen“ und „Als Vorlage kopieren“ |
| Lernpfad | Lektionsliste mit Fortschritt (nur Sitzung), Lektionsansicht (Abschnitt 6.4) |
| Modell | YAML-Editor (`st.text_area`), Validierungsliste darunter, „Speichern“ nur für Modelle in `data/models/` |
| Simulation | N (Standard aus `settings`, 1 … 2 000 000), Seed, „Simulieren“; Fortschritt und Laufzeit |
| Ergebnisse | Je Ausgabe ein Reiter (Abschnitt 4); für T1/T2 zusätzlich Referenz (Abschnitt 5) |
| Läufe | Gespeicherte Läufe des Modells; „Laden“ zeigt die Ergebnisansicht aus der Ablage |

- **Tutorials und Lektionen sind schreibgeschützt.** Der Editor zeigt sie; Ändern erfordert
  „Als Vorlage kopieren“. So bleibt die Quelldatei bytegleich (AK 4).
- **Live-Validierung:** bei jeder Änderung `model_from_yaml` + `compile_model`; Fehler als
  `render(issue)` mit Zeile bzw. Knoten. Der Simulieren-Knopf ist bei Fehlern gesperrt.
- **Leeres Modell** (`model.empty`) → Hinweis „Das Modell enthält noch keine Knoten“, kein
  Fehlerblock. Fehlendes `output` → Validierungsfehler `model.no_output`.
- Simulationen werden pro (Modell-Hash, N, Seed) im `st.session_state` gehalten; ein erneuter
  Klick mit gleichen Werten rechnet nicht neu.

### 3.1 YAML-Editor (Seite Modell)

Der Editor ist ein mehrzeiliges Textfeld (`st.text_area`, Festbreitenschrift, ca. 30 Zeilen)
mit dem Modelltext. Er leistet:

- **Prüfen nach jeder Übernahme:** Streamlit übernimmt den Text beim Verlassen des Felds oder mit
  Strg+Enter, nicht bei jedem Tastendruck. Danach laufen `model_from_yaml` und `compile_model`;
  „live“ heißt in M2 also „nach jeder Übernahme“.
- **Fehlerliste unter dem Feld:** alle Probleme auf einmal (M1 sammelt), je Eintrag Zeile bzw.
  Knoten-ID, deutscher Text aus `render()` und – bei Zeilenangabe – die betroffene Zeile als
  Auszug. Das Feld selbst hat keine Zeilennummern und keine Markierung im Text.
- **Statuszeile:** „Gültig – 6 Knoten, 1 Ausgabe“ oder „3 Probleme“, dazu „Ungespeicherte
  Änderungen“, wenn der Text von der Datei abweicht.
- **Knotenübersicht** (nur lesend) bei gültigem Modell: Tabelle ID, Typ, Name, Einheit,
  Verteilung bzw. Ausdruck.
- **Knöpfe:** „Speichern“ (nur eigene Modelle in `data/models/`; auch ungültige Entwürfe, mit
  Warnung; Simulieren bleibt dann gesperrt), „Verwerfen“ (Text aus der Datei neu laden),
  „Als Vorlage kopieren“. Tutorials und Lektionen sind schreibgeschützt (Feld deaktiviert).
- **Speichern sicher:** atomar (temporäre Datei, dann `rename`); hat sich die Datei seit dem
  Öffnen geändert (SHA-256), meldet die App das und bietet „Trotzdem überschreiben“ an.
- **Entwurf bleibt erhalten:** Der Editortext liegt zusätzlich außerhalb des Widgets im
  Sitzungszustand, weil Streamlit den Zustand eines Widgets löscht, sobald eine Seite ohne dieses
  Widget angezeigt wird.
- **Nicht enthalten:** Syntaxfärbung, Autovervollständigung, Einrücken per Tab, Rückgängig über
  die Browser-Funktion hinaus. Komfortabler wird die Bearbeitung mit dem Formular in M6.

***

## 4. Ergebnisansicht (AK 2, 8)

Je `output`-Knoten:

- **Histogramm** (Dichte-normiert, Bins nach Freedman-Diaconis, höchstens 200) und **CDF**
  (empirisch, bei N > 20 000 auf 2 000 Stützpunkte ausgedünnt).
- **Kennzahlen:** Mittelwert ± Standardfehler, Median, P5/P10/P90/P95 mit Konfidenzintervall,
  P(Ziel) mit Wilson-Intervall, Min/Max.
- **Sätze in Modellsprache** (`present/text.py`), z. B.:
  - „Im Modell liegen 90 % der Werte höchstens bei 31,2 d (95-%-Intervall 31,1 … 31,3).“
  - „Im Modell wird das Ziel ≤ 30 d in 74,1 % der Iterationen erreicht (73,8 … 74,4 %).“
- **Numerische Güte:** Standardfehler des Mittelwerts, Breite der Quantilintervalle, relative
  Genauigkeit; Hinweis, wenn die halbe Intervallbreite von P(Ziel) > 1 Prozentpunkt ist.
- **Geltungszeile:** „Dieses Ergebnis gilt für Modell *t2_terminplan* (Hash 3f9a…), Szenario
  *Hauptszenario*, N = 100 000, Seed 20261027, berechnet am 28.10.2026 14:03 UTC.“ Das Szenario
  ist bis M3 immer „Hauptszenario“; in Lektionen steht dort die Stellschraube („a = 3“).
- Zahlenformat deutsch (Komma, schmales Leerzeichen als Tausendertrenner), Einheit aus `unit`.
- Bool-Ausgaben: nur Anteil mit Wilson-Intervall und Balken.

***

## 5. Analytische Überlagerung T1/T2 (AK 3)

`present/references.py` ordnet `model_id` eine Referenz zu; ohne Eintrag entfällt der Block.

| Modell | Dichte | CDF | Zusatz |
|---|---|---|---|
| T1 | Dreieck | Dreieck | Gitterfaltung als dritte Kurve, max. Abweichung Gitter ↔ analytisch |
| T2 | numerische Ableitung von Φ₁Φ₂ | Φ₁(t)·Φ₂(t) | Clark-Mittelwert neben dem simulierten |

- **KS-Block:** „Größter Abstand der CDFs: 0,0021 – zulässig bei N = 100 000: 0,0062
  (DKW-Schranke, α = 0,001).“ Ampel grün/rot.
- Die Referenz gilt nur, wenn der **Inhalts-Hash** (`content_hash`: ohne Modell-ID, Titel und
  Anzeigenamen) dem Tutorial-Original entspricht. „Als Vorlage kopieren“ schreibt die Herkunft als
  Kommentar `# Kopie von <tutorial>` in die Kopie; eine unveränderte Kopie behält so die
  Überlagerung, eine geänderte zeigt: „Die analytische Lösung gilt für das unveränderte Tutorial.“
  (Festlegung nach Review, 28.10.2026.)

***

## 6. Lernpfad „Abhängigkeitsmuster“

### 6.1 Ziel und Auswahl

Der Lernpfad zeigt, wie die Art der Verknüpfung unsicherer Größen das Ergebnis verschiebt –
und zwar **voraussichtlich in welche Richtung und wie stark**. Ausgewählt sind die Muster, die in
Terminplanung (PERT/Netzpläne), Zuverlässigkeitstechnik (Blockschaltbilder, Fehlerbäume) und
Entscheidungsanalyse als Grundbausteine gelten. Jede Lektion ist mit den M1-Bausteinen
modellierbar; Korrelation ohne Wirkungsmodell (Copula) folgt in M5, Rückkopplungen bleiben
Nicht-Ziel und werden in der Abschlusslektion als Grenze benannt.

| Nr | Muster | Ausdruck | Beispiel | Voraussichtliche Auswirkung (Faustregel) | Analytische Referenz | Quelle |
|---|---|---|---|---|---|---|
| A1 | Serie (linear, additiv) | `a + b + c` | Fahrtabschnitte einer Bahnreise | Mittelwerte und Varianzen addieren sich; relative Streuung sinkt mit √n; Summe wird glockenförmig | N(Σμ, Σσ²) | Malcolm et al. 1959 (PERT); zentraler Grenzwertsatz |
| A2 | Parallel-UND („alle müssen fertig sein“) | `max(a, b, …)` | Demo-Anlage wartet auf Magnete **und** Plasma | Ergebnis später als jeder Einzelpfad im Mittel (Merge-Bias); wächst mit Zahl der Pfade | F(t) = Πᵢ Fᵢ(t) | Clark 1961; MacCrimmon & Ryavec 1964 |
| A3 | Parallel-ODER, Redundanz („erster gewinnt“) | `min(a, b, …)` | Nächster Zug oder Bus | Ergebnis früher und schmaler; jede Alternative hilft, mit abnehmendem Grenznutzen | 1 − Πᵢ(1 − Fᵢ(t)); min von Exp(λᵢ) = Exp(Σλᵢ) | Rausand & Høyland 2004, Kap. 6 |
| A4 | k-von-n | `(e1 + e2 + e3) >= 2` | Zwei von drei Materialkandidaten müssen sich bewähren | Liegt zwischen UND (k = n) und ODER (k = 1); sehr empfindlich gegenüber k | Binomialsumme | Barlow & Proschan 1965; Rausand & Høyland 2004 |
| A5 | Ereignis-Verzweigung (Mischung) | `where(e, x + d, x)` | Nacharbeit mit p = 0,2 kostet +5 Tage | Mehrgipflige Verteilung; Mittelwert steigt um p·d, Median kaum; Mittelwert beschreibt keinen typischen Fall | F = (1−p)·F₀ + p·F₁ | McLachlan & Peel 2000 |
| A6 | Schwelle / Kipppunkt | `where(v <= puffer, plan, plan + 60)` | Anschluss erreicht, wenn Verspätung ≤ Umstiegspuffer | Kleine Änderung nahe der Schwelle → großer Sprung im Ergebnis; Wirkung des Puffers ist stark nichtlinear | P = F_v(puffer) | Savage 2009 (Flaw of Averages) |
| A7 | Bedingte Verteilung | `mean: "12 - 4 * durchbruch"` | Magnet-Durchbruch verkürzt Plasmaentwicklung | Ergebnisverteilung ist eine Mischung über die Ursache; Streuung wächst um die Varianz der bedingten Mittelwerte | E[Y] = E[E[Y∣X]], Var = E[Var] + Var[E] | Gesetz der totalen Varianz |
| A8 | Multiplikative Kette | `p1 * p2 * p3`, `x1 * x2` | Erfolg nur, wenn jede Technologie funktioniert | Erfolgswahrscheinlichkeit fällt schneller als die schwächste Einzelwahrscheinlichkeit; Produkte sind rechtsschief | Π pᵢ; Produkt von Lognormalen ist lognormal | Kremer 1993 (O-Ring); Rausand & Høyland 2004 (Serienzuverlässigkeit) |
| A9 | Nichtlineare Transformation (Jensen) | `x ** 2`, `exp(x)`, `interp(...)` | Kosten steigen überproportional mit Verzug; Förderkennlinie mit Sättigung | f(E[X]) ≠ E[f(X)]: konvex → Planwert unterschätzt, konkav (Sättigung) → überschätzt | E[eˣ] = e^(μ+σ²/2) für X ~ N(μ, σ²) | Jensen 1906; Savage 2009 |
| A10 | Gemeinsame Ursache | `a = basis + ea; b = basis + eb` | Wetter verspätet beide Züge; Lieferkette trifft zwei Technologien | Gleichlauf (Korrelation) ohne Korrelationsangabe; Summen streuen stärker, Redundanz (A3) verliert an Wirkung | Var(a+b) = Var(ea)+Var(eb)+4·Var(basis) | Fleming 1974 (β-Faktor); Mosleh et al. 1998 (NUREG/CR-5485) |
| A11 | Zusammenspiel (Abschluss) | Kombination A2, A4, A7, A8 | Mini-Fusion: Demo = max(Magnete, Plasma) + Bau, Materialien 2 von 3 | Zeigt, welches Muster dominiert; Grenzen: Rückkopplung, Copula (M5), Zeitdynamik | keine | – |

**Literatur** (in der App als Leseliste je Lektion):

- Barlow, R. E.; Proschan, F. (1965): *Mathematical Theory of Reliability.* Wiley.
- Clark, C. E. (1961): The greatest of a finite set of random variables. *Operations Research*
  9(2), 145–162.
- Fleming, K. N. (1974): *A reliability model for common mode failures in redundant safety
  systems.* General Atomic, GA-A13284.
- Jensen, J. L. W. V. (1906): Sur les fonctions convexes et les inégalités entre les valeurs
  moyennes. *Acta Mathematica* 30, 175–193.
- Kremer, M. (1993): The O-Ring Theory of Economic Development. *Quarterly Journal of
  Economics* 108(3), 551–575.
- MacCrimmon, K. R.; Ryavec, C. A. (1964): An analytical study of the PERT assumptions.
  *Operations Research* 12(1), 16–37.
- Malcolm, D. G.; Roseboom, J. H.; Clark, C. E.; Fazar, W. (1959): Application of a technique
  for research and development program evaluation. *Operations Research* 7(5), 646–669.
- McLachlan, G.; Peel, D. (2000): *Finite Mixture Models.* Wiley.
- Mosleh, A. et al. (1998): *Guidelines on Modeling Common-Cause Failures in Probabilistic Risk
  Assessment.* NUREG/CR-5485, U.S. NRC.
- Rausand, M.; Høyland, A. (2004): *System Reliability Theory.* 2. Aufl., Wiley.
- Savage, S. L. (2009): *The Flaw of Averages.* Wiley.

Die bibliografischen Angaben wurden am 28.10.2026 online gegen Verlage, DOIs und
Bibliothekskataloge geprüft (AP-L4); die geprüfte Fassung mit DOIs steht in
`src/app/lessons/sources.py`. Einzige Unschärfe: Fleming GA-A13284 ist auf Dezember 1974 datiert
und wird wegen des Vortrags 1975 teils als 1975 zitiert. Zahlen in den Lektionen sind didaktisch
gesetzt und als „illustrativ“ gekennzeichnet.

### 6.2 Dateiformat

Jede Lektion besteht aus einem normalen Modell (`aNN_*.yaml`, Schema M1, ohne Erweiterung) und
einem Erklärtext (`aNN_*.md`). Das Manifest verbindet beides:

```yaml
# examples/lernpfad/lernpfad.yaml
schema: 1
lessons:
  - id: a02_parallel_und
    title: "Parallel-UND: Wenn alles fertig sein muss"
    model: a02_parallel_und.yaml
    text: a02_parallel_und.md
    output: ende                       # Ausgabe, auf die sich Frage und Referenz beziehen
    question:
      text: "Was passiert mit dem mittleren Ende, wenn ein dritter gleich langer Pfad hinzukommt?"
      options: ["steigt", "bleibt gleich", "sinkt"]
      answer: 0
      metric: mean                     # mean | sd | share | target: Kennzahl der Auflösung
    knob:                              # genau eine Stellschraube
      node: anzahl_pfade
      field: value
      label: "Anzahl paralleler Pfade"
      values: [1, 2, 3, 4]             # oder range: {min, max, step}
    reference: max_iid_normal          # Schlüssel in lessons/reference.py oder weglassen
    sources: [clark1961, maccrimmon1964]
```

- `lessons/catalog.py` validiert das Manifest mit Pydantic (`extra="forbid"`): Dateien
  existieren (geprüft im Adapter), `node`/`field` existieren im Modell und sind ein literales
  Zahlenfeld, `answer` liegt in `options`, Werte der Stellschraube erfüllen die
  Parameterbedingungen der Familie.
- Strukturänderungen (z. B. Zahl der Pfade) werden über eine `constant` und `where` modelliert,
  nicht über Knoten, die auftauchen und verschwinden – so bleibt die Stellschraube ein Wert.

### 6.3 Analytische Referenzen der Lektionen (`lessons/reference.py`)

| Schlüssel | Lektion | Geprüfte Größe |
|---|---|---|
| `sum_normal` | A1 | CDF N(Σμ, Σσ²) – KS-Kriterium |
| `max_iid_normal` | A2 | CDF Φ((t−μ)/σ)ᵏ – KS-Kriterium |
| `min_exponential` | A3 | CDF 1 − e^(−Σλ·t) – KS-Kriterium |
| `k_of_n_binomial` | A4 | P(≥ k von n) – Anteils-Kriterium |
| `mixture_shift` | A5 | Mittelwert μ + p·d – Mittelwert-Kriterium; CDF-Mischung – KS-Kriterium |
| `threshold_exp` | A6 | P(Anschluss) = p₀ + (1−p₀)(1 − e^(−b/m)) – Anteils-Kriterium |
| `total_expectation` | A7 | E[Y] und Var[Y] nach totaler Varianz – Mittelwert-Kriterium, Varianz ±2 % |
| `product_prob` | A8 | Π pᵢ – Anteils-Kriterium |
| `lognormal_mean` | A9 | e^(μ+σ²/2) – Mittelwert-Kriterium |
| `common_cause_var` | A10 | Var(a+b) – ±2 % |

Jede Referenz ist eine Funktion des aktuellen Stellschraubenwerts, damit die Überlagerung auch
nach dem Drehen gilt. Toleranzen aus PRD Abschnitt 3.

### 6.4 Ablauf einer Lektion (Seite Lernpfad)

1. **Erklären:** Erklärtext (Markdown), Ausdruck des Musters hervorgehoben, Mini-Modell als
   YAML (schreibgeschützt), Leseliste.
2. **Vorhersagen:** Frage mit Antwortoptionen; Auflösung erst nach dem Drehen, aus den beiden
   Läufen berechnet (`question.metric`), nicht aus dem Manifest. Keine Bewertung, nur „Deine
   Vorhersage: steigt – Ergebnis: Mittelwert steigt um 0,85 d (von … auf …)“.
3. **Simulieren:** Ausgangswert der Stellschraube, N = 20 000 (Lernpfad-Standard, E6), fester
   Seed des Modells. Ergebnisansicht wie Abschnitt 4, plus Referenz.
4. **Drehen:** Stellschraube ändern → zweiter Lauf mit **demselben Seed** (gemeinsame
   Zufallszahlen, M1 AK 8). Anzeige: beide CDFs überlagert, Tabelle Vorher/Nachher/Differenz
   für Mittelwert, Median, P10, P90, P(Ziel), dazu die Faustregel der Lektion.
5. **Weiter:** „Als Vorlage kopieren“ übernimmt das Mini-Modell mit dem aktuellen Wert nach
   `data/models/`.

- `lessons/knob.py::with_value` gibt ein **neues** `Model` zurück (Pydantic `model_copy` mit
  Validierung); die Lektionsdatei wird nie geschrieben. Das ist bewusst kein Szenario (M3).
- Fortschritt (angesehen, durchgearbeitet) lebt nur in `st.session_state` und steht als Liste in
  der Seitenleiste.
- Beim Öffnen einer Lektion prüft die Seite Dateien und Manifest (`lesson_problems`) zur Laufzeit
  und zeigt Abweichungen statt abzustürzen.

***

## 7. Ablage (Adapter)

**Modelle** – `data/models/<model_id>.yaml`:

- `copy_model(src, new_id)` schreibt den Quelltext mit ersetzter `model:`-Zeile; Öffnen mit
  Modus `"x"` (exklusiv), damit nie überschrieben wird. Existiert der Name, schlägt die App
  `<id>_2`, `<id>_3`, … vor; der Nutzer bestätigt oder ändert (Edge case).
- Die Quelle wird nur gelesen; ein Test vergleicht SHA-256 vor und nach dem Kopieren (AK 4).
- Kommentare bleiben erhalten, weil Text kopiert wird, nicht das geparste Modell.

**Läufe** – `data/runs/<UTC-Zeit>_<model_id>_<hash8>/`:

| Datei | Inhalt |
|---|---|
| `meta.json` | `SimulationResult.meta` (Modell-Hash, Seed, N, Paketversionen, Zeit), Szenario, Stellschraube, Format-Version 1 |
| `model.yaml` | Modelltext zum Zeitpunkt des Laufs |
| `samples.npz` | Stichproben der `output`- und `track`-Knoten (`np.savez_compressed`) |
| `summary.json` | Kennzahlen wie angezeigt |

- `load_run` liest `samples.npz`, berechnet `summarize` neu und vergleicht mit `summary.json`;
  Abweichung → Hinweis „Gespeicherte und neu berechnete Kennzahlen weichen ab“ (AK 5).
- Schreiben atomar: in `<ordner>.tmp` schreiben, dann `rename`.
- Größe: N = 2 000 000 × 5 Ausgaben ≈ 80 MB unkomprimiert; Hinweis ab 100 MB vor dem Speichern.
- Speichern ist ein expliziter Knopf, kein Automatismus.

***

## 8. Beenden (AK 7)

- Seitenleiste: „App beenden“ → Bestätigung → `adapters/process.shutdown()` sendet
  `signal.SIGTERM` an `os.getpid()`. Kein Port-Kill, keine fremden Prozesse.
- Vorher Hinweis „Ungespeicherte Änderungen im Editor gehen verloren“, falls der Editor-Inhalt
  von der Datei abweicht.
- Test: `os.kill` gemockt, Aufruf mit eigener PID und `SIGTERM` geprüft.

***

## 9. Texte und Meldungen (AK 6, 8)

- Alle sichtbaren Texte stehen im Meldungskatalog aus M1 (`messages.py`) unter neuen Codes
  `ui.*`, `result.*`, `lesson.*`; `render()` wie in M1. Englisch bleibt vorbereitet.
- Test: Jeder in `ui/` verwendete Code hat eine `de`-Vorlage (Suche nach `t("…")`-Aufrufen).
- Validierungsfehler aus M1 erscheinen unverändert über `render(issue)`; Ausnahmen in der UI
  werden abgefangen und als `ui.unexpected` mit Kurzbeschreibung gezeigt, die App läuft weiter
  (`views.run_page`; Streamlits Steuer-Ausnahmen erben von `BaseException` und passieren).
- Jede Seite ruft `views.sidebar_exit()` selbst auf: AppTest baut unter `st.navigation` nach einer
  Widget-Interaktion nur die Seite neu auf; Elemente des Hauptskripts fehlen dann.

***

## 10. Tests

| AK | Test | Prüft |
|---|---|---|
| 1 | `test_app.py` | AppTest: Start → T1 öffnen → N = 10 000 simulieren → Kennzahlen sichtbar, keine Ausnahme; `.streamlit/config.toml` Port ≠ 8501 |
| 2 | `test_present_text.py`, `test_app.py` | Sätze, Formate, Geltungszeile; alle Elemente in der Ergebnisansicht |
| 3 | `test_present_references.py` | T1/T2: KS-Abstand < DKW-Schranke mit N = 100 000; Gitterkurve vorhanden; geänderte Kopie → keine Referenz |
| 4 | `test_adapters_files.py` | Kopie in `tmp_path`, Quelle SHA-256-gleich, vorhandener Name → kein Überschreiben |
| 5 | `test_adapters_runs.py` | Speichern, Neuladen, gleiche Kennzahlen; Metadaten vollständig; atomares Schreiben |
| 6 | `test_present_validation.py`, `test_app.py` | Fehlerhaftes YAML, Zyklus, fehlendes `output`, leeres Modell → Klartext, keine Ausnahme |
| 7 | `test_adapters_process.py` | `os.kill` gemockt, eigene PID, SIGTERM |
| 8 | `test_messages_ui.py` | Codes vollständig; Quantilsätze in Modellsprache |
| 9 | `test_lessons_catalog.py` | Manifest gültig, alle Dateien vorhanden, Stellschrauben zulässig, jede Lektion kompiliert |
| 10 | `test_lessons_reference.py` | Jede Referenz in Ausgangs- und einem gedrehten Wert erfüllt ihr Kriterium (N = 100 000) |
| 11 | `test_lessons_knob.py`, `test_app.py` | `with_value` ändert nur das Feld; nicht betroffene Knoten bitgleich; AppTest: A2 drehen → Vorher/Nachher-Tabelle; Faustregel-Richtung stimmt (z. B. A2: Mittelwert steigt) |

- `tests/conftest.py` setzt `RISK_PILOT_DATA_DIR` auf `tmp_path`; kein Test schreibt nach `data/`.
- AppTest läuft ohne Netzwerk (kein Server); falls doch ein Socket geöffnet wird, Fixture
  gezielt lockern und begründen.
- **Laufzeit:** AppTests mit N ≤ 20 000; Lektionsreferenzen 10 × 2 Läufe mit N = 100 000 –
  vorher messen, Ziel < 10 s für alle Lektionstests zusammen.

***

## 11. Arbeitspakete

| AP | Inhalt | Fertig, wenn |
|---|---|---|
| AP0 | `streamlit`, `plotly` hinzufügen, `.streamlit/config.toml`, `ui/main.py` mit Beenden | AK 7 grün, App startet auf 8642 |
| AP1 | `adapters/settings.py`, `files.py`-Erweiterung, `runs.py` | AK 4, 5 grün |
| AP2 | `present/text.py`, `validation.py`, Meldungscodes | AK 6, 8 grün |
| AP3 | `present/figures.py`, `references.py`, T1/T2-Erklärtexte | AK 3 grün |
| AP4 | Seiten Start, Modell, Simulation, Ergebnisse, Läufe | AK 1, 2 grün |
| AP-L1 | `lessons/catalog.py`, `knob.py`, Manifest-Schema | AK 9 (Schema) grün |
| AP-L2 | Lektionen A1–A10 (YAML, MD, Referenzen) | AK 10 grün |
| AP-L3 | A11, Seite Lernpfad | AK 11 grün |
| AP-L4 | Literatur prüfen, README, `docs/architecture.md`, PRD-Status | Abschnitt 12 |

**Reihenfolge:** AP0 → AP1 → AP2 → (AP3 ∥ AP-L1) → AP4 → AP-L2 → AP-L3 → AP-L4.

***

## 12. Abschluss von M2

- [ ] PRD M2 AK 1–11 und Edge cases durch die Tests in Abschnitt 10 belegt.
- [ ] `uv run pre-commit run --all-files` grün; neue Dateien vorher `git add`.
- [x] Manuell: App gestartet, Lernpfad A1–A11 durchgeklickt (Nutzer, 28.10.2026); Beenden per
      SIGTERM an die eigene PID geprüft.
- [ ] README: Installation, Start (Port 8642), Beenden, Tutorials und Lernpfad.
- [ ] `docs/architecture.md` um `present/`, `lessons/`, `ui/` ergänzt.
- [ ] PRD M2 **Status:** `done (verified by: …)`.
- [ ] Review durch den `reviewer`-Agenten gegen PRD M2 und dieses Pflichtenheft.

***

## 13. Entscheidungen

Am 28.10.2026 alle wie vorgeschlagen bestätigt.

| Nr | Frage | Entscheidung |
|---|---|---|
| E1 | Lernpfad in M2 oder eigener Meilenstein? | In M2 (AK 9–11). Falls M2 zu groß wird: AP-L1…L4 als M2b direkt danach, ohne Änderung an M3 ff. |
| E2 | Port | 8642 in `.streamlit/config.toml`; am 28.10.2026 auf dem Entwicklungsrechner frei (belegt u. a. 8502–8560) |
| E3 | YAML-Editor | `st.text_area` (keine Zusatzabhängigkeit), Umfang Abschnitt 3.1; Syntaxfärbung frühestens mit M6 |
| E4 | Laufformat | JSON + `npz` (nur NumPy); Parquet bleibt Export in M6 |
| E5 | Musterauswahl | A1–A10 wie Abschnitt 6.1; Copula-Korrelation als Lektion A12 mit M5 nachziehen |
| E6 | N im Lernpfad | 20 000 (Antwort < 1 s), änderbar; = 20 % der 100 000 der Tutorials T1/T2 |
| E7 | Vorhersagefragen | Ohne Punktzahl, nur Gegenüberstellung |
| E8 | Fortschritt im Lernpfad | Nur Sitzung, keine Datei |
