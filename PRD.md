# PRD — Risk Pilot: Weltmodell-Baukasten mit Monte-Carlo-Kern

> Spec, gegen die gebaut und geprüft wird. Herleitung und Begründungen:
> [ideas/concept-v2.md](ideas/concept-v2.md) (Konzept) und [ideas/basic-idea.md](ideas/basic-idea.md)
> (Erstanalyse). Die **Status**-Zeile jedes Meilensteins ist der einzige Ort für Fortschritt.
> Oberfläche Deutsch, Code und Bezeichner Englisch.

## 1. Problem & goal

Unsichere Fragen wie „Wann ist mein Projekt fertig?“, „Wann kommt das Fusionskraftwerk?“, „Erreiche
ich meinen Anschluss?“ oder „Was bringt mein Portfolio?“ werden heute mit Einzelwerten, Excel oder
Spezialsoftware je Domäne beantwortet; Abhängigkeiten, Szenarien und die Numerik bleiben dabei
undurchsichtig. **Gelöst** ist das Problem, wenn ich lokal aus wenigen generischen Bausteinen ein
Weltmodell aufbaue (oder ein Tutorial als Vorlage kopiere), es per Monte Carlo simuliere, in
Unterszenarien abwandle, die Ergebnisse vergleiche und Treiber, kritische Pfade und Risiken sehe –
mit Parametern aus meiner eigenen, externen Recherche und nachgewiesen korrekter Numerik.

## 2. Non-goals

- Web-Recherche, LLM-Anbindung, automatische Parameterfindung oder -prüfung im Tool.
- Evidenzgraph, Review- und Freigabeworkflow, Mehrbenutzerbetrieb.
- Datenbank, Server-Betrieb, Authentifizierung, Mandantentrennung, Bezahlfunktionen.
- Periodendimension (Zeitschritte, Rebalancing, `prev`/`cumprod`); Portfolio nur Buy-and-Hold.
- Grafischer Drag-and-drop-Modelleditor; der Graph ist Ansicht.
- Ressourcen- und Kalenderlogik in Terminplänen.
- Zyklische Modelle, Systemdynamik mit Differentialgleichungen.
- Bayessche Inferenz, automatische „beste Verteilung“, Datenfit über Quantil-Fit hinaus.
- Automatische Szenariomischung oder Szenariowahrscheinlichkeiten.
- Mischverteilungen als Familie, Sobol-Indizes, LHS- oder Quasi-Monte-Carlo-Sampling.
- Einheitenprüfung (z. B. `d + EUR` als Fehler, Umrechnung d ↔ h); `unit` ist bis dahin Freitext.
- Englische Oberfläche (Meldungskatalog ist ab M1 dafür vorbereitet).
- Anlageberatung, Derivatebewertung, Marktpreisprozesse.

## 3. Constraints

- Python ≥ 3.11, Abhängigkeiten nur über uv, Lizenzen Apache-2.0-kompatibel
  (NumPy, SciPy, Pydantic, PyYAML, Streamlit, Plotly, NetworkX, PyArrow; ab M7 NiceGUI statt
  Streamlit). Freigegebene Ausnahmen (29.10.2026): `bidict` (MPL-2.0) und `docutils` (Public
  Domain/BSD, einzelne Teile GPL) als transitive Abhängigkeiten von NiceGUI, unverändert genutzt.
- Repository-Gate bleibt verbindlich: Testsuite offline und ≤ 60 s, Branch-Coverage ≥ 85 %,
  pyright strict in `src/`. Langlaufende Statistiktests nur mit eigener Markierung außerhalb des
  Gates und nach Freigabe.
- Kern (`src/app/` ohne `adapters/` und `ui/`) ist rein: keine Datei-, Netzwerk- oder
  Datenbankzugriffe.
- Modelle sind YAML-Dateien; das Pydantic-Schema ist der Vertrag. Nutzer- und Laufdaten liegen in
  `data/` (gitignored), Tutorials in `examples/` (versioniert).
- Ausdrücke werden nie per `eval`/`exec` ausgeführt; nur `ast`-Whitelist.
- Zufallszahlen: ein eigener `SeedSequence`-Strom je Knoten, abgeleitet aus Lauf-Seed und
  Knoten-ID; Ziehen per Inversionsmethode aus dem Gleichverteilungsstrom des Knotens.
- Streamlit: eigener Port in `.streamlit/config.toml` (nicht 8501); Beenden-Schaltfläche, die nur
  den eigenen Prozess per SIGTERM beendet.
- Keine stille Reparatur ungültiger Eingaben (Abschneiden, Matrixprojektion, Nullsetzen).
- Ergebnistexte in Modellsprache: „Im Modell liegen 90 % der Werte höchstens bei …“.

**Gemeinsame Toleranzen der Abnahmen** (gelten in allen Meilensteinen):

- *KS-Kriterium:* maximaler Abstand empirische ↔ analytische CDF < ε = √(ln(2/α)/(2N)) mit
  α = 0.001 (DKW-Schranke).
- *Mittelwert-Kriterium:* |Schätzung − Sollwert| < 4 Standardfehler.
- *Anteils-Kriterium:* Sollwert liegt im Wilson-Intervall zum Niveau 99.9 %.
- Alle Tests mit festem Seed, damit sie deterministisch sind.

## 4. Milestones

### M1 — Rechenkern
- **Status:** done (verified by: tests/test_dists.py, test_expr.py, test_graph.py,
  test_validation.py, test_engine.py, test_stats.py, test_examples.py, test_yaml_io.py,
  test_messages.py) <!-- planned | in progress | done (verified by: <tests>) -->
- **Deliverable:** Modellschema (Knotentypen `constant`, `uncertain`, `event`, `choice`, `derived`,
  `output`), YAML-Lader (Adapter), Ausdruckssprache, Verteilungsregister, vektorisierte Engine,
  Grundstatistik; `examples/t1_faltung.yaml` und `examples/t2_terminplan.yaml`.
  Pflichtenheft: [docs/specs/m1-rechenkern.md](docs/specs/m1-rechenkern.md).
- **Acceptance criteria:**
  1. Verteilungen: uniform, triangular, pert (λ Standard 4), normal, truncnormal, lognormal, beta,
     student_t, exponential, gamma, weibull, bernoulli, discrete, poisson. Jede kontinuierliche
     Familie erfüllt mit N = 100 000 das KS-Kriterium gegen ihre SciPy-CDF.
  2. Eingabemodi: Parameter für alle Familien; zusätzlich Mittelwert/Std für normal, lognormal,
     beta, gamma und Min/Modus/Max für triangular, pert. Lognormal aus Mittelwert m und Std s ergibt
     σ² = ln(1 + s²/m²), μ = ln m − σ²/2; Eingabemodus und kanonische Parameter werden beide
     gespeichert.
  3. Ungültige Parameter (z. B. sd ≤ 0, min > max, Modus außerhalb, p ∉ [0, 1], ν ≤ 2) führen zu
     einem Validierungsfehler, der Knoten-ID und Parameter nennt.
  4. Ausdrücke: Operatoren `+ - * / ** %`, Vergleiche, `and or not`, Funktionen `min, max, abs,
     exp, log, sqrt, floor, ceil, clip, where, interp, sum` (`where(c, a, b)` wie in NumPy; `if`
     ist in Python ein Schlüsselwort). Attribute, Indizes, Lambdas, Aufrufe unbekannter
     Funktionen, unbekannte Namen und Ausdrücke über der Längen-/Tiefengrenze werden mit
     Fehlermeldung (Knoten, Ursache) abgewiesen.
  5. Verteilungsparameter dürfen Ausdrücke anderer Knoten sein (bedingte Verteilungen).
  6. Zyklen werden mit Angabe der beteiligten Knoten abgewiesen.
  7. Jeder unsichere Knoten wird pro Iteration genau einmal gezogen: `a = x; b = x` ergibt
     `a == b` in jeder Iteration.
  8. Gleiches Modell + Seed → bitgleiche Ergebnisse. Hinzufügen eines unabhängigen Knotens ändert
     die Ziehungen bestehender Knoten nicht. Ändern eines Anzeigenamens ändert keine Zahl.
  9. Konstante → exakt konstantes Ergebnis; Ereignis mit p = 0 bzw. 1 → nie bzw. immer.
  10. Statistik je Ausgabe: Mittelwert mit Standardfehler, Median, frei wählbare Quantile mit
      Konfidenzintervall (Ordnungsstatistik), P(Ziel erreicht) mit Wilson-Intervall. Null Treffer
      ergeben eine obere Intervallgrenze > 0.
  11. T1 (U(0,1) + U(0,1)): KS-Kriterium gegen die Dreiecks-CDF, Mittelwert-Kriterium gegen 1,
      Varianz innerhalb ±2 % von 1/6; zusätzlich numerische Faltung auf einem Gitter, deren CDF
      höchstens 0.001 von der analytischen abweicht.
  12. T2 (A ~ N(10, 2²), B ~ N(15, 3²), C ~ N(24, 4²), Ende = max(A + B, C)): KS-Kriterium
      gegen F(t) = Φ₁(t)·Φ₂(t), Mittelwert-Kriterium gegen den Clark-Wert 26.685.
- **Edge cases:**
  - uniform mit a = b → wird als Konstante behandelt.
  - pert mit Modus auf einer Grenze → zulässig, ergibt Randmodus.
  - Normal für einen Knoten mit `min: 0` → Warnung mit Anteil unzulässiger Werte, keine Kappung.
  - Nicht-endliche Werte (z. B. `log(0)`) → Fehler mit Knoten und Anteil betroffener Iterationen.
  - Ungültiges YAML → Fehler mit Zeilennummer.
- **Dependencies:** keine.

### M2 — Erste App
- **Status:** done (verified by: tests/test_app.py, test_present_*.py, test_lessons_*.py,
  test_adapters_*.py, test_messages_ui.py; manual click-through 28.10.2026)
- **Deliverable:** Streamlit-App mit den Seiten Tutorials, Modell (YAML-Editor mit
  Live-Validierung), Simulation (N, Seed), Ergebnisse; analytische Überlagerung für T1/T2;
  Ergebnisablage in `data/runs/`; Kopierfunktion für Vorlagen; Lernpfad „Abhängigkeitsmuster“
  (A1–A11) in `examples/lernpfad/`.
  Pflichtenheft: [docs/specs/m2-erste-app.md](docs/specs/m2-erste-app.md).
- **Acceptance criteria:**
  1. App startet auf dem konfigurierten Port; `streamlit.testing` (AppTest) lädt T1, simuliert und
     zeigt Kennzahlen ohne Ausnahme.
  2. Ergebnisansicht je Ausgabe: Histogramm, CDF, Mittelwert, Median, Quantile, P(Ziel), numerische
     Güte und „Dieses Ergebnis gilt für …“ (Modell, Szenario, N, Seed, Zeitpunkt).
  3. T1 und T2 zeigen analytische Dichte/CDF, numerische Faltung (T1) und den KS-Abstand neben der
     DKW-Schranke.
  4. „Als Vorlage kopieren“ legt aus einem Tutorial oder eigenen Modell ein neues Modell in
     `data/models/` an; die Quelldatei bleibt bytegleich.
  5. Ein gespeicherter Lauf zeigt nach Neuladen dieselben Kennzahlen; Metadaten enthalten
     Modell-Hash, Szenario, Seed, N und Paketversionen.
  6. Validierungsfehler erscheinen als deutscher Klartext an der Eingabe, die App stürzt nicht ab.
  7. Die Beenden-Schaltfläche sendet SIGTERM an die eigene PID (Test mit gemocktem `os.kill`).
  8. Alle sichtbaren Texte sind deutsch; Quantile sind in Modellsprache beschriftet.
  9. Lernpfad mit mindestens zehn Abhängigkeitsmustern: Serie, Parallel-UND (`max`),
     Parallel-ODER (`min`), k-von-n, Ereignis-Verzweigung, Schwelle, bedingte Verteilung,
     multiplikative Kette, nichtlineare Transformation (Jensen), gemeinsame Ursache; dazu eine
     Abschlusslektion, die mehrere Muster kombiniert. Jede Lektion hat Mini-Modell, Erklärtext,
     Faustregel zur voraussichtlichen Auswirkung, Vorhersagefrage und Quellenangabe.
  10. Jede Lektion mit analytischer Referenz erfüllt ihr Kriterium aus Abschnitt 3 im Ausgangswert
      und in einem gedrehten Wert der Stellschraube.
  11. Drehen der Stellschraube rechnet mit demselben Seed neu und zeigt Vorher/Nachher (CDFs,
      Kennzahlen, Differenz); nicht betroffene Knoten haben bitgleiche Ziehungen; die
      Lektionsdatei bleibt bytegleich.
- **Edge cases:** leeres Modell (Hinweis statt Fehler); Modell ohne `output` (Validierungsfehler);
  Kopie mit bereits vorhandenem Namen (Nachfrage oder neuer Name, kein Überschreiben);
  Stellschraubenwert verletzt Parameterbedingung (Manifest-Validierung weist ab); geändertes
  Tutorial (keine analytische Überlagerung, Hinweis).
- **Dependencies:** M1.

### M3 — Szenarien und Vergleich
- **Status:** done (verified by: tests/test_scenarios.py, test_scenario_runs.py, test_compare.py,
  test_app.py; manual click-through 28.10.2026)
- **Deliverable:** Haupt- und Unterszenarien mit Overrides und Vererbung, Szenariobaum,
  Duplizieren, Loslösen, Diff-Ansicht, Vergleichsseite.
  Pflichtenheft: [docs/specs/m3-szenarien.md](docs/specs/m3-szenarien.md).
- **Acceptance criteria:**
  1. Ein Unterszenario speichert nur seine Overrides (Werte, Verteilungsfamilie/-parameter,
     Ereigniswahrscheinlichkeiten, Ausdrücke, Korrelationswerte) samt Begründung.
  2. Effektives Modell = Elternmodell + Overrides. Eine Änderung im Elternszenario wirkt im Kind,
     sofern das Kind den Wert nicht überschreibt; überschriebene Werte bleiben.
  3. Szenariobäume mit Tiefe ≥ 2 funktionieren; Zyklen in der Elternkette und Overrides
     unbekannter Knoten werden abgewiesen.
  4. Loslösen erzeugt eine vollständige Kopie; spätere Elternänderungen wirken nicht mehr.
  5. Nicht überschriebene Knoten haben in Eltern- und Kindlauf bitgleiche Ziehungen.
  6. In T2 senkt das Unterszenario „B −3 Tage“ das Ende in **jeder** Iteration oder lässt es
     gleich (paarweise Differenz ≤ 0).
  7. Vergleich: überlagerte CDFs, Kennzahlentabelle mit Differenzen und deren numerischer
     Unsicherheit, Verteilung der paarweisen Differenz, P(B besser als A).
  8. Die Diff-Ansicht listet genau die überschriebenen Werte.
- **Edge cases:** Override eines Knotens, der im Elternmodell gelöscht wurde (Warnung, Override
  bleibt sichtbar und inaktiv); Override mit identischem Wert (zulässig, als solcher markiert);
  Typwechsel eines Knotens per Override (abgewiesen).
- **Dependencies:** M2.

### M4 — Struktur-Auswertungen
- **Status:** done (verified by: tests/test_criticality.py, test_tornado.py, test_sweep.py,
  test_sensitivity.py, test_riskmatrix.py, test_graph.py, test_analysis_page.py, test_app.py;
  manual click-through 28.10.2026; correlation edges of AK 1 follow with M5)
- **Deliverable:** Abhängigkeitsgraph, Kritikalität und Pfadkonstellationen, Tornado, Sweep,
  Rangkorrelation, Risikomatrix.
  Pflichtenheft: [docs/specs/m4-struktur.md](docs/specs/m4-struktur.md).
- **Acceptance criteria:**
  1. Graph: Kanten aus Ausdrucks- und Parameterreferenzen sowie Korrelationsgruppen; Knotentyp und
     Kantenart unterscheidbar; Einfärbung nach Sensitivität, Kritikalität oder fehlender Begründung.
  2. Kritikalität: `max`/`min` merken das gewinnende Argument; der Index eines Knotens ist der
     Anteil der Iterationen auf dem entscheidenden Pfad. T2: Index von A und B erfüllt das
     Anteils-Kriterium gegen 0.5737. Bei Gleichstand zählen alle Gewinner; Indizes müssen nicht
     zu 100 % summieren, Pfadkonstellationen summieren zu 100 %.
  3. Tornado: jede unsichere Eingabe auf ihr P10 und P90 fixiert, gemeinsame Zufallszahlen,
     sortiert nach Ausschlag. Ein Knoten ohne Pfad zur Ausgabe hat Ausschlag exakt 0; in T1 sind
     die Ausschläge von X₁ und X₂ gleich (±2 %).
  4. Sweep: Kennzahl über k Werte eines Parameters; in T2 ist P(Ende ≤ 30) monoton nicht steigend
     im Mittelwert von B.
  5. Rangkorrelation (Spearman) je Eingabe, im UI als deskriptiv gekennzeichnet.
  6. Risikomatrix je `event`: x = p̂ mit Wilson-Intervall, y = E[Y | Ereignis] − E[Y | kein
     Ereignis]; im T2-Unterszenario „mit Nacharbeit“ (p = 0.2, +5 Tage auf B) liegt y in (0, 5].
     Das Hauptszenario von T2 bleibt ohne Ereignis, damit seine analytischen Werte gelten. Hinweis auf
     Grenzen (gemeinsame Ursachen, Wechselwirkungen) ist sichtbar.
- **Edge cases:** Ereignis tritt nie oder immer ein (y nicht definiert, markiert); Modell ohne
  `max`/`min` (Kritikalitätsseite erklärt, warum sie leer ist); diskrete Eingaben im Tornado
  (P10/P90 der diskreten Verteilung).
- **Dependencies:** M3.

### M5 — Abhängigkeiten und Tutorials T3–T5
- **Status:** done (verified by: tests/test_correlations.py, test_dists.py, test_fit.py,
  test_stats.py, test_adapters_files.py, test_examples.py, test_present_text.py, test_app.py;
  review and manual click-through 29.10.2026)
- **Deliverable:** Korrelationsgruppen, Stützstellen- und empirische Verteilung, Quantil-Fit,
  Horizont/Zensierung, `examples/t3_bahn.yaml`, `t4_portfolio.yaml`, `t5_fusion.yaml` mit als
  illustrativ gekennzeichneten Zahlen.
  Pflichtenheft: [docs/specs/m5-abhaengigkeiten.md](docs/specs/m5-abhaengigkeiten.md).
- **Acceptance criteria:**
  1. Korrelationsgruppen: Eingabe als Spearman-ρ, Umrechnung ρ_latent = 2 sin(π ρ_s / 6),
     Gaussian Copula. Asymmetrische, nicht positiv semidefinite Matrizen oder |ρ| > 1 werden
     abgewiesen, nicht repariert. Erreichte Spearman-Korrelation bei N = 100 000 liegt innerhalb
     ±0.02 des Ziels und wird angezeigt.
  2. Stützstellen-Verteilung aus streng steigenden Quantilpaaren (CDF stückweise linear) erfüllt
     das KS-Kriterium; nicht steigende Paare werden abgewiesen.
  3. Empirische Verteilung aus Werteliste oder CSV-Spalte (Adapter), Ziehen mit Zurücklegen.
  4. Quantil-Fit: P10/P50/P90 → Parameter von normal, lognormal, gamma, weibull; die maximale
     Quantilabweichung wird ausgewiesen; über 2 % relativer Abweichung erklärt die App den
     Konflikt und bietet die Stützstellen-Verteilung an.
  5. Horizont je Ausgabe: Anteil „nicht im Horizont“ wird mit Wilson-Intervall ausgewiesen;
     Quantile jenseits des Horizonts erscheinen als „> Horizont“.
  6. T3: P(Anschluss) erfüllt das Anteils-Kriterium gegen 0.6 + 0.4·(1 − e^(−5/6)) ≈ 0.8262; die
     App weist auf die Mehrgipfligkeit hin (Median ≠ häufigster Wert).
  7. T4 (Buy-and-Hold, drei Anlagen): Mittelwert-Kriterium gegen E[W_T] = W₀ Σ wᵢ exp(Tμᵢ + Tσᵢ²/2);
     Standardabweichung innerhalb ±3 % des analytischen Werts; P(Verlust), VaR und ES werden
     angezeigt.
  8. T5 läuft mit mindestens zwei Unterszenarien; Kritikalität, Tornado und Risikomatrix liefern
     Ergebnisse; Anteil „nicht bis 2100“ wird ausgewiesen.
  9. T3–T5 sind kopierbar (M2 AK 4) und tragen im UI den Hinweis „illustrative Zahlen“.
- **Edge cases:** Korrelationsgruppe mit einem einzigen Knoten (abgewiesen); Knoten in zwei
  Gruppen (abgewiesen); Copula auf diskrete Verteilungen (zulässig, Hinweis auf Bindungen);
  Ausgabe vollständig jenseits des Horizonts (alle Quantile „> Horizont“).
- **Dependencies:** M4.

### M6 — Formular-Editor und Export
- **Status:** done (verified by: tests/test_form.py, test_yaml_patch.py, test_preview.py,
  test_app_form.py, test_export.py, test_family_extension.py, test_app.py; review and manual
  click-through 29.10.2026)
- **Deliverable:** Knotentabelle und Knotenkarten mit Verteilungsvorschau und Begründungsfeld,
  Export, Dokumentation der Erweiterungspunkte (`docs/model-semantics.md`,
  `docs/statistical-methods.md`).
  Pflichtenheft: [docs/specs/m6-formular-export.md](docs/specs/m6-formular-export.md).
- **Acceptance criteria:**
  1. Knotenkarte zeigt beim Eintragen Dichte, CDF, Mittelwert, Median, P5/P95 und den Anteil
     unzulässiger Werte.
  2. Formular und YAML sind verlustfrei: Bearbeiten im Formular → YAML → Neuladen ergibt dasselbe
     Modell (Eigenschaftstest über alle Tutorials).
  3. T2 lässt sich per AppTest vollständig über das Formular nachbauen und liefert dieselben Zahlen
     wie `examples/t2_terminplan.yaml`.
  4. Export: Kennzahlen als CSV, Rohstichproben als Parquet, Bericht als eigenständige HTML-Datei.
  5. Eine in einem Test registrierte neue Verteilungsfamilie ist ohne Änderung an Engine und UI
     im Modell nutzbar.
- **Edge cases:** YAML-Kommentare und Formatierung bleiben beim Bearbeiten im Formular erhalten
  (Entscheidung 29.10.2026); gleichzeitige Bearbeitung in Formular und YAML-Editor (letzte
  Änderung gewinnt mit Hinweis).
- **Dependencies:** M5.

### M7 — Neue Oberfläche
- **Status:** in progress (AK 1 met: spike decided for NiceGUI on 2026-10-29, see spec §3.1)
- **Deliverable:** Die Oberfläche löst Streamlit ab, damit eine durchgestaltete Bedienung möglich
  wird, die Streamlits Seiten-Neulauf und Einheitsoptik nicht zulassen. Gewählt: NiceGUI
  (MIT, reines Python, ereignisgesteuert), entschieden nach einem Spike mit drei Ansichten nach
  den Leitbildern Hex (Ergebnisse), GoRules (Modell-Arbeitsfläche mit Probelauf) und
  Guesstimate (Unsicherheit als Spanne, Mini-Verteilung je Knoten). Pflichtenheft:
  [docs/specs/m7-neue-oberflaeche.md](docs/specs/m7-neue-oberflaeche.md).
- **Acceptance criteria:**
  1. Spike entschieden: Framework gewählt oder Abbruch mit Begründung (dann bleibt Streamlit).
  2. Alle Seiten aus M2–M6 laufen in der neuen Oberfläche mit gleichem Funktionsumfang; die
     AppTest-Tests sind durch gleichwertige Tests ohne Browser ersetzt, offline im Gate.
  3. Kern, `present/` und `adapters/` bleiben ohne UI-Import; die Oberfläche bleibt dünn.
  4. Eigener Port (8642), Beenden-Schaltfläche beendet nur den eigenen Prozess.
  5. Streamlit ist aus Code, Abhängigkeiten und Doku entfernt.
- **Edge cases:** Formular-Entwurf und YAML-Entwurf bleiben synchron ohne Neulauf-Tricks;
  lange Läufe blockieren die Oberfläche nicht.
- **Dependencies:** M6.

### M8 — UX und Selbsterklärung
- **Status:** planned
- **Deliverable:** Eine App, die sich Fachleuten ohne Monte-Carlo-Vorwissen selbst erklärt:
  geführter Einstieg, Hilfetexte je Seite und Auswertung, Begriffsglossar, Beispiele zur Lesart.
  Anlass: Rückmeldung nach M4, die Seite „Analyse“ erschließt sich zunächst nicht (erste
  Erklärtexte je Reiter seit M4).
- **Acceptance criteria:**
  1. Jede Seite beginnt mit einem kurzen Absatz, wofür sie da ist und was der nächste Schritt ist.
  2. Jede Auswertung (Ergebnisse, Vergleich, alle Reiter der Analyse) erklärt Frage, Lesart und
     Grenze und zeigt ein Lesebeispiel am geöffneten Modell.
  3. Ein Glossar erklärt die Fachbegriffe der Oberfläche (u. a. Iteration, Seed, Quantil,
     Intervall, Szenario, Override, kritischer Pfad, Tornado, Spearman-ρ) und ist von jeder Seite
     erreichbar; jeder Begriff im Glossar ist durch einen Test gegen die UI-Texte abgedeckt.
  4. Ein geführter Einstieg führt an T2 durch Öffnen, Simulieren, Szenario, Vergleich und
     Analyse; per Oberflächentest ohne Browser durchlaufbar.
  5. Manueller Durchgang mit einer Fachperson ohne Vorkenntnisse; ihre Befunde sind behoben oder
     als offene Punkte im PRD vermerkt.
- **Edge cases:** Modelle ohne Ereignisse, ohne Unterszenarien oder ohne max/min (Hilfetexte
  erklären, warum eine Auswertung leer bleibt).
- **Dependencies:** M7. Pflichtenheft (Entwurf):
  [docs/specs/m8-ux-selbsterklaerung.md](docs/specs/m8-ux-selbsterklaerung.md).

## 5. Open risks & assumptions

- **Inversionsmethode ist für manche Familien langsam** (SciPy-`ppf` bei beta, student_t, gamma).
  Messen in M1; Leistungsziel 30 Knoten × 100 000 Iterationen < 5 s auf dem Entwicklungsrechner.
  Trigger: Ziel verfehlt → schnellere Inversion je Familie, ohne die Kopplungseigenschaft aufzugeben.
- **60-s-Gate gegen statistische Tests:** Referenztests nutzen N ≤ 100 000 und feste Seeds. Trigger:
  Suite > 45 s → langsame Tests markieren und außerhalb des Gates fahren (nach Freigabe).
- **Ablösung von Streamlit (M7):** Der Spike hat die bessere Bedienung bestätigt (NiceGUI,
  ≈ 25–55 ms je Änderung, Tests ohne Browser offline). Restrisiko: Migrationsaufwand und
  Testumstellung über alle Seiten; Trigger: eine Seite lässt sich nicht gleichwertig testen →
  vor dem Weiterbauen mit dem Nutzer klären.
- **Illustrative Zahlen werden als Fakten gelesen:** Hinweis im UI und in den YAML-Dateien.
- **Spearman → latent ist nur für die Gaussian Copula exakt;** die erreichte Korrelation wird
  deshalb immer ausgewiesen.
- **Bedingte Differenz in der Risikomatrix ist kein kausaler Effekt,** wenn Ereignisse gemeinsame
  Ursachen haben; Grenze steht im UI.
- **Annahme:** Ein Nutzer (ich), lokal, Modelle bis ca. 100 Knoten.

## 6. Definition of done

- [ ] M1–M8 stehen auf `done` mit Verweis auf die prüfenden Tests.
- [ ] `uv run pre-commit run --all-files` ist grün.
- [ ] T1–T5 laufen in der App und als Regressionstests; T1–T4 bestehen ihre analytischen Abnahmen.
- [ ] Ein eigenes Modell lässt sich aus einer kopierten Vorlage aufbauen, in mindestens zwei
      Unterszenarien abwandeln, vergleichen und exportieren.
- [ ] README beschreibt Installation, Start (Port), Beenden und Tutorials; `docs/` beschreibt
      Modellsemantik, statistische Methoden und Erweiterungspunkte.
