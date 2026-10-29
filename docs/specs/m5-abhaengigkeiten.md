# Pflichtenheft M5 — Abhängigkeiten und Tutorials T3–T5

**Stand:** 28. Oktober 2026, Entscheidungen E1–E12 bestätigt (Abschnitt 12) · **Bezug:**
[PRD.md](../../PRD.md), Meilenstein M5 (AK 1–9, Edge cases) · **Voraussetzung:** M1–M4

Dieses Pflichtenheft legt fest, **wie** M5 umgesetzt wird. Das PRD bleibt der Vertrag für das
**Was**; bei Widerspruch gilt das PRD, und der Widerspruch wird hier korrigiert.

***

## 1. Umfang

**In M5:** Korrelationsgruppen (Gaussian Copula, Eingabe Spearman), Stützstellen-Verteilung,
empirische Verteilung mit CSV-Import, Quantil-Fit (P10/P50/P90) für normal, lognormal, gamma,
weibull, Horizont je Ausgabe, Tutorials T3 (Bahn), T4 (Portfolio), T5 (Fusion) mit
Referenzprüfungen, Korrelationskanten im Graphen (M4 AK 1).

**Nicht in M5:** Verteilungsvorschau beim Eintragen und Formular-Editor (M6), Export (M6),
Mischverteilungen (Nicht-Ziel), Periodendimension (Nicht-Ziel), Hilfetexte über die Analyse
hinaus (M7).

***

## 2. Modulstruktur

```text
src/app/
    model/schema.py           + Model.correlations, Model.illustrative, OutputNode.horizon,
                                OutputNode.loss_reference; Scenario.correlations wird aktiv
    model/correlations.py     Prüfung der Gruppen, Spearman -> latent, Faktor der Matrix
    model/compile.py          + CompiledModel.groups; Quantil-Fit beim Kompilieren
    model/graph.py            + Kanten der Art "korrelation"
    dists/families.py         + Piecewise ("piecewise"), Empirical ("empirical"),
                                Modus "quantiles" für normal, lognormal, gamma, weibull
    dists/fit.py              Quantil-Fit und maximale Abweichung
    engine/copula.py          korrelierte Gleichverteilungen aus den Strömen der Gruppe
    engine/simulate.py        + Gruppen vor den Knoten ziehen, erreichte Spearman-ρ im Ergebnis
    analysis/stats.py         + Horizont (Zensierung), VaR/ES
    analysis/analytic.py      + Referenzen T3, T4
    adapters/files.py         + CSV-Spalte lesen (für den Import in eine Werteliste)
    present/...               Texte zu Horizont, Fit, Korrelation, Mehrgipfligkeit
    ui/pages/modell.py        + CSV-Import, „als Stützstellen übernehmen“
    ui/pages/ergebnisse.py    + erreichte Korrelationen, Horizont, VaR/ES
examples/
    t3_bahn.yaml/.md, t4_portfolio.yaml/.md, t5_fusion.yaml/.md
```

- Keine neue Abhängigkeit (SciPy enthält `optimize`, `stats`).
- Schema-Version bleibt 1: alle neuen Felder sind optional (E12).

***

## 3. Korrelationsgruppen (AK 1)

### 3.1 Modellformat (E1, E2)

```yaml
correlations:
  markt:
    nodes: [aktien, anleihen, gold]
    spearman:
      - [1.0, 0.3, 0.1]
      - [0.3, 1.0, 0.2]
      - [0.1, 0.2, 1.0]
scenarios:
  krise:
    name: "Krisenkorrelation"
    why: "In Krisen laufen Anlagen gleich."
    correlations:
      markt: {spearman: [[1, 0.8, 0.8], [0.8, 1, 0.8], [0.8, 0.8, 1]], why: "…"}
```

- Mitglieder: `uncertain` und `event` (E3); `choice` und berechnete Knoten nicht.
- Ein Szenario ersetzt die Matrix einer Gruppe als Ganzes; die Mitgliederliste bleibt fest.

### 3.2 Prüfung (`model/correlations.py`), nie Reparatur

| Fall | Code |
|---|---|
| Gruppe mit weniger als zwei Knoten | `corr.too_small` |
| Knoten unbekannt, falscher Typ, in zwei Gruppen oder doppelt in einer | `corr.node_unknown`, `corr.node_type`, `corr.node_twice`, `corr.node_repeated` |
| Matrix nicht k×k, Diagonale ≠ 1, \|ρ\| > 1, nicht symmetrisch | `corr.shape`, `corr.diagonal`, `corr.range`, `corr.asymmetric` |
| Spearman-Matrix nicht positiv semidefinit | `corr.not_psd` (kleinster Eigenwert genannt) |
| Latente Matrix 2 sin(π ρ_s / 6) nicht positiv semidefinit | `corr.latent_not_psd` (selten; Erklärung im Text) |

- Toleranz für Eigenwerte: −1e−10; Symmetrie exakt auf den eingegebenen Zahlen.
- Positiv semidefinit (singulär, z. B. ρ = 1) ist zulässig.

### 3.3 Ziehen (`engine/copula.py`)

- Je Mitglied die Gleichverteilung seines eigenen Stroms (M1), z = Φ⁻¹(u); z' = L·z mit L aus
  Cholesky der latenten Matrix (singulär: symmetrischer Faktor über Eigenzerlegung); u' = Φ(z').
- Der Knoten zieht dann mit u' statt u. Folge: Ohne Gruppe ändert sich nichts an M1–M4; mit
  Gruppe bleiben gemeinsame Zufallszahlen über Szenarien erhalten, weil die Ströme gleich bleiben.
- Ereignisse in einer Gruppe treten bei `u' > 1 − p` ein (außerhalb von Gruppen wie bisher
  `u < p`), damit ρ > 0 sie mit hohen Werten der anderen Mitglieder koppelt; diskrete Familien
  wie bisher über `ppf`. Bei diskreten Mitgliedern
  Hinweis `corr.discrete_ties` (erreichte Rangkorrelation liegt wegen Bindungen unter dem Ziel).
- Tornado (M4): Wird ein Mitglied fixiert, ziehen die übrigen weiter dieselben u'.

### 3.4 Erreichte Korrelation

- `SimulationResult.correlations`: je Gruppe die erreichte Spearman-Matrix der Mitglieder.
- Ergebnisseite: Tabelle „Paar · Ziel ρ · erreicht ρ“; AK 1 prüft |erreicht − Ziel| ≤ 0,02 bei
  N = 100 000.
- Graph: ungerichtete, gepunktete Kanten der Art `korrelation` zwischen allen Paaren der Gruppe;
  sie zählen nicht für die Schichten des Layouts.

***

## 4. Stützstellen- und empirische Verteilung (AK 2, 3)

- **`piecewise`:** `probs: [0, 0.1, 0.5, 0.9, 1]`, `values: [2030, 2034, 2040, 2052, 2080]`.
  Beide Listen gleich lang (≥ 2), streng steigend, `probs` beginnt mit 0 und endet mit 1 (E4).
  CDF stückweise linear; `ppf(u) = interp(u, probs, values)`. Analytische Referenz für den
  KS-Test ist dieselbe CDF.
- **`empirical`:** `values: [...]` (≥ 1 Wert); Ziehen mit Zurücklegen:
  `values[floor(u · n)]`. Diskret für Tornado-Quantile (M4).
- **CSV-Import (E5):** Auf der Modellseite eine CSV-Datei hochladen, Spalte wählen, Zielknoten
  wählen → die Werte werden als `values`-Liste ins YAML geschrieben (nur eigene Modelle). Leere
  Zellen werden übersprungen und gezählt; nicht lesbare oder nicht endliche Zahlen (`nan`, `inf`) brechen den Import mit Zeilenangabe
  ab. Höchstens 100 000 Werte. Die Datei muss UTF-8 sein; andere Kodierungen werden gemeldet
  (`csv.encoding`), nicht geraten.

***

## 5. Quantil-Fit (AK 4)

- Neuer Eingabemodus `quantiles` mit `p10`, `p50`, `p90` (nur literale Zahlen, streng steigend)
  für `normal`, `lognormal` (alle > 0), `gamma` (alle > 0), `weibull` (alle > 0, loc = 0).
- **Fit (`dists/fit.py`):** kleinste Quadrate der Quantilabweichung, normiert auf P90 − P10.
  normal: lineare Regression auf z = Φ⁻¹(p); lognormal: dasselbe auf log q; gamma, weibull:
  `scipy.optimize.least_squares` mit festem Startwert (deterministisch).
- **Abweichung (E6):** max |q_fit − q_gegeben| / (P90 − P10). Immer ausgewiesen (Notice
  `fit.deviation` mit Wert und den drei Quantilen gegen Fit); über 2 % stattdessen als eigene
  Notice `fit.conflict` (Warnung) mit Erklärung
  („Die drei Werte passen nicht zu einer {Familie}-Verteilung …“) und Knopf „Als
  Stützstellen-Verteilung übernehmen“ (E7): Die Felder P0 und P100 starten leer, der Knopf wird
  erst aktiv, wenn beide eingetragen sind. Liegt P0 nicht unter P10 oder P100 nicht über P90,
  meldet `fit.bounds` den Fehler.
- Kanonische Parameter erscheinen wie bisher in `canonical` (Lauf-Metadaten).

***

## 6. Horizont (AK 5)

- `horizon: 2100` an einer Ausgabe: Werte > Horizont gelten als „nicht im Horizont erreicht“.
- Kennzahlen: Anteil „nicht im Horizont“ mit Wilson-Intervall; ein Quantil, dessen Wert über dem
  Horizont liegt, erscheint als „> Horizont“ (Intervallgrenzen ebenso). Mittelwert und
  Standardabweichung (E8) werden bei zensierten Werten nicht als Zahl gezeigt, sondern als
  „nicht bestimmbar: x % jenseits des Horizonts“. P(Ziel) bleibt unverändert gültig.
- Edge case: alle Werte jenseits → alle Quantile „> Horizont“, Histogramm mit Hinweis.
- Vergleich und Analyse (M3, M4) rechnen weiter mit den Rohwerten; die Seiten weisen bei
  Ausgaben mit Horizont darauf hin.

***

## 7. VaR und ES (AK 7)

- `loss_reference: 100000` an einer Ausgabe (E9): Verlust = Referenz − Wert.
- Ergebnisseite: P(Verlust > 0) mit Wilson, VaR₉₅ = Referenz − Q₀,₀₅ (Quantil-KI wie M1),
  ES₉₅ = Referenz − Mittel der Werte ≤ Q₀,₀₅ (mit Standardfehler).

***

## 8. Mehrgipfligkeit (AK 6)

- Generischer Hinweis auf der Ergebnisseite (E10), wenn die Dichte (Histogramm mit 60 gleich
  breiten Klassen, geglättet über drei Klassen; Stand 29.10.2026, `analysis/stats.py`)
  mindestens zwei Gipfel hat, deren Höhe je ≥ 10 % des höchsten
  beträgt und zwischen denen die Dichte unter die Hälfte des kleineren Gipfels fällt:
  „Die Verteilung hat mehrere Gipfel: Median ({median}) und häufigster Bereich ({mode}) fallen
  auseinander; der Mittelwert beschreibt hier keinen typischen Fall.“ Bei einer Ausgabe mit
  Horizont zählen nur die Werte im Horizont; liegt der Median jenseits, entfällt der Hinweis.

***

## 9. Tutorials

Alle Zahlen illustrativ; `illustrative: true` im Modell (E11) zeigt auf Modell- und
Ergebnisseite „Illustrative Zahlen: didaktisch gesetzt, keine Rechercheergebnisse.“

**T3 Bahnreise** (`t3_bahn`): `puenktlich` (event, p = 0,6); `verspaetung` (exponential, mean 6
min), wirksam nur ohne Pünktlichkeit; `puffer` = 5 min (7 − 2); `anschluss = where(puenktlich, 0,
verspaetung) <= puffer` (Ausgabe, Wahrheitswert); `zug2` (exponential, mean 3); `bus` (triangular
33/35/40, damit der zweite Gipfel die Regel aus Abschnitt 8 erfüllt); `ankunft = where(anschluss, zug2, min(60 + zug2, bus))` (Ausgabe, Ziel ≤ 15 min).
Szenario „früherer Zug“ (`puffer` = 20). Referenz: P(Anschluss) = 0,6 + 0,4 (1 − e^(−5/6)) ≈
0,8262 (Anteils-Kriterium, AK 6).

**T4 Portfolio** (`t4_portfolio`): `w0` = 100 000, `t` = 10 Jahre; Log-Renditen über T als
`normal(mean: T·μ, sd: √T·σ)` für Aktien (μ 0,06, σ 0,18), Anleihen (0,02, 0,05), Gold (0,03,
0,15); Gewichte als Konstanten (0,6/0,3/0,1); Gruppe `markt` mit Spearman 0,2/0,1/0,3;
`vermoegen = w0 · Σ wᵢ exp(Lᵢ)` mit `loss_reference` = w0. Szenarien „defensiv“ (Gewichte),
„Krisenkorrelation“ (alle 0,8), „hohe Volatilität“. Referenz (AK 7): E[W] nach PRD
(Mittelwert-Kriterium), Standardabweichung aus der Kovarianzformel mit latenter Korrelation
(±3 %).

**T5 Fusion** (`t5_fusion`): Reifejahre von Plasma, Magneten, Materialien, Tritium-Brüten als
`piecewise`; Scheitern je Technologie als `event`; Durchbruch Magnete verkürzt Plasma (bedingte
Verteilung); Demo = max(Reifejahre) + Bauzeit (`interp` über Förderung); kommerziell nach Demo +
Bauzeit, bei Scheitern 2200; `horizon: 2100`, Ziel ≤ 2060. Szenarien „hohe Förderung“,
„Materialproblem“, „beides“ (AK 8). Keine analytische Referenz; Regressionstest prüft, dass
Kritikalität, Tornado (N = 2 000) und Risikomatrix Ergebnisse liefern und der Anteil „nicht bis
2100“ in (0, 1) liegt.

***

## 10. Tests

| AK | Test | Prüft |
|---|---|---|
| 1 | `test_correlations.py` | erreichte ρ ±0,02 bei N = 100 000; alle Abweisungen aus 3.2; Gruppe mit einem Knoten; Knoten in zwei Gruppen; diskrete Mitglieder mit Hinweis; Szenario ersetzt Matrix; gleiche Ströme ohne Gruppe (M1-Werte unverändert) |
| 2 | `test_dists.py` | piecewise: KS-Kriterium; nicht steigende Paare, fehlende 0/1 abgewiesen |
| 3 | `test_dists.py`, `test_adapters_files.py` | empirical: Häufigkeiten; CSV-Spalte, leere Zellen, Fehler mit Zeile |
| 4 | `test_fit.py` | exakte Quantile werden getroffen (< 0,1 %); widersprüchliche Quantile > 2 % mit Hinweis; Übernahme als piecewise |
| 5 | `test_stats.py` | Anteil jenseits mit Wilson; „> Horizont“; alle jenseits |
| 6–8 | `test_examples.py` | T3 Anteils-Kriterium; T4 Mittelwert-Kriterium und Std ±3 %; T5 Auswertungen laufen |
| 6 | `test_present_*.py` | Mehrgipfligkeit an T3 erkannt, an T1/T2 nicht |
| 9 | `test_app.py` | T3–T5 kopierbar, Hinweis „illustrative Zahlen“, Ergebnisseite mit Korrelationstabelle, VaR/ES, Horizont |

- Laufzeit: Korrelationstest mit N = 100 000 nur für eine Gruppe; Ziel ≤ 5 s zusätzlich im Gate.

***

## 11. Arbeitspakete und Abschluss

| AP | Inhalt | Fertig, wenn |
|---|---|---|
| AP1 | Schema, `model/correlations.py`, `engine/copula.py`, Szenario-Overrides, Graphkanten | AK 1 grün |
| AP2 | `piecewise`, `empirical`, CSV-Adapter | AK 2, 3 grün |
| AP3 | Modus `quantiles`, `dists/fit.py` | AK 4 grün |
| AP4 | Horizont, VaR/ES, Mehrgipfligkeit | AK 5 und Teile von 6, 7 grün |
| AP5 | T3–T5 mit Erklärtexten und Referenzen | AK 6–8 grün |
| AP6 | Oberfläche (Import, Fit-Knopf, Ergebnisseite), `illustrative` | AppTests grün, AK 9 |
| AP7 | Doku, Review, PRD-Status, manueller Durchlauf | Checkliste unten |

**Reihenfolge:** AP1 → AP2 → AP3 → AP4 → AP5 → AP6 → AP7.

- [x] PRD M5 AK 1–9 und Edge cases durch Tests belegt; Gate grün.
- [ ] Manuell: T3–T5 öffnen, simulieren, vergleichen, analysieren.
- [ ] README, `docs/architecture.md`; PRD M5 **Status** `done (verified by: …)`; Review.

***

## 12. Entscheidungen

Am 28.10.2026 alle wie vorgeschlagen bestätigt.

| Nr | Frage | Entscheidung |
|---|---|---|
| E1 | Wo stehen Korrelationsgruppen? | **Auf Modellebene unter `correlations:`** (nicht am Knoten), weil eine Gruppe mehrere Knoten verbindet |
| E2 | Matrix oder Paarliste? | **Vollständige Matrix** wie im PRD (Symmetrie wird geprüft); Szenarien ersetzen sie als Ganzes |
| E3 | Wer darf in eine Gruppe? | **`uncertain` und `event`**; diskrete Familien mit Hinweis auf Bindungen |
| E4 | Stützstellen ohne P0/P100? | **Nicht zulässig:** `probs` beginnt mit 0 und endet mit 1 (keine erfundenen Ränder) |
| E5 | CSV-Daten im Modell oder als Verweis? | **Import als Werteliste ins YAML:** Modell bleibt eigenständig, Hash deckt die Daten ab; Grenze 100 000 Werte |
| E6 | Bezug der „relativen Abweichung“ im Quantil-Fit | **Bezogen auf P90 − P10**, nicht auf den Wert: bei Jahreszahlen wären 2 % von 2040 sonst 40 Jahre |
| E7 | Was tut „als Stützstellen übernehmen“? | **Schreibt `piecewise` mit den drei gegebenen Quantilen und den Rändern P0/P100, die das Formular vom Nutzer abfragt** (keine erfundenen Ränder, passend zu E4) |
| E8 | Mittelwert bei Zensierung | **Nicht als Zahl zeigen** („nicht bestimmbar: x % jenseits“), statt eines verzerrten Werts |
| E9 | VaR/ES worauf? | **Feld `loss_reference` an der Ausgabe**, Niveau 95 % fest (später wählbar) |
| E10 | Mehrgipfligkeit | **Generische Regel aus dem Histogramm** (Abschnitt 8) statt nur im T3-Text |
| E11 | Hinweis „illustrative Zahlen“ | **Neues Modellfeld `illustrative: true`**, Kopien behalten es, bis man es entfernt |
| E12 | Schema-Version | **Bleibt 1:** nur optionale Felder, alte Modelle laufen unverändert |
