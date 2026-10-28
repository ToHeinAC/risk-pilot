# Pflichtenheft M3 — Szenarien und Vergleich

**Stand:** 28. Oktober 2026, Entscheidungen E1–E10 bestätigt (Abschnitt 12) · **Bezug:**
[PRD.md](../../PRD.md), Meilenstein M3 (AK 1–8, Edge cases) · **Voraussetzung:** M1, M2

Dieses Pflichtenheft legt fest, **wie** M3 umgesetzt wird. Das PRD bleibt der Vertrag für das
**Was**; bei Widerspruch gilt das PRD, und der Widerspruch wird hier korrigiert.

***

## 1. Umfang

**In M3:**

- Szenarien im Modell: Hauptszenario (die Knoten des Modells) und beliebig tief geschachtelte
  Unterszenarien, die nur ihre Overrides samt Begründung speichern.
- Effektives Modell je Szenario (Eltern + Overrides), Validierung der Elternkette und Overrides.
- Szenariobaum, Anlegen, Duplizieren, Loslösen, Diff-Ansicht.
- Simulation und Ergebnisse je Szenario; Vergleichsseite mit gepaarten Differenzen.
- T2 erhält die Unterszenarien „B −3 Tage“ (AK 6) und „mit Nacharbeit“ (für M4 AK 6).

**Nicht in M3:** Korrelationswerte als Override-Ziel (das Format ist vorbereitet, die Gruppen
kommen mit M5), Sensitivität und Kritikalität (M4), Szenariowahrscheinlichkeiten oder
-mischung (Nicht-Ziel), Formular-Editor für Knoten (M6).

***

## 2. Modulstruktur

```text
src/app/
    model/
        schema.py        + Scenario, Override, Model.scenarios (additiv, schema_version 1)
        scenarios.py     effective_model(), chain(), diff(), detach(), duplicate() – rein
    analysis/
        compare.py       gepaarte Differenzen, Batch-Means-Unsicherheit, P(B besser als A)
    present/
        compare.py       Vergleichstabelle, Sätze, Figuren (überlagerte CDFs, Differenzverteilung)
    adapters/
        files.py         unverändert (Szenarien stehen im Modelltext)
    ui/pages/
        szenarien.py     Baum, Anlegen, Duplizieren, Loslösen, Diff
        vergleich.py     Auswahl A/B, Vergleichsansicht
        simulation.py    + Szenarioauswahl
examples/t2_terminplan.yaml  + scenarios
```

- Szenarien sind Teil des Modelltexts (E1); der YAML-Editor bleibt die Quelle, die Szenarioseite
  schreibt über reine Funktionen (`scenarios.py`) und `model_to_yaml` zurück (E7).
- `docs/architecture.md`: `model/scenarios.py`, `analysis/compare.py`, `present/compare.py`.

***

## 3. Modellformat

```yaml
scenarios:
  b_schneller:                         # Szenario-ID, Regeln wie Knoten-IDs; "basis" ist reserviert
    name: "B −3 Tage"
    parent: basis                      # optional, Standard basis (= Hauptszenario)
    why: "Zusätzliches Team für Vorgang B"
    overrides:
      b: {mean: 12, why: "Planung mit zweitem Team"}
  b_schneller_nacharbeit:
    name: "B −3 Tage, mit Nacharbeit"
    parent: b_schneller                # Tiefe ≥ 2 (AK 3)
    why: "Prüfung, ob der Gewinn die Nacharbeit überlebt"
    overrides:
      nacharbeit: {p: 0.2}             # Ereignisknoten existiert im Hauptszenario mit p = 0 (3.2)
```

### 3.1 Overrides (AK 1, 2)

- **Feldweise** (E2): Ein Override nennt einen Knoten und eines oder mehrere seiner Felder;
  nicht genannte Felder kommen vom Eltern. Erlaubt sind die Werte-Felder der Knotentypen:
  `value`, Verteilungsparameter, `p`, `expr`, `options`, `target`, `bounds`.
- **Familienwechsel:** Nennt ein Override `dist` oder `input`, ersetzt es den ganzen
  Parametersatz der Verteilung (die Felder des Overrides sind dann vollständig anzugeben); sonst
  würden alte Parameter in die neue Familie fallen.
- **Begründung:** `why` je Szenario Pflicht, je Override optional (AK 1 „samt Begründung“).
- **Typwechsel** (`type` im Override) → abgewiesen, `scenario.type_change` (Edge case).
- **Gleicher Wert wie beim Eltern** → zulässig, Hinweis `scenario.same_value`, in der
  Diff-Ansicht markiert (Edge case).
- **Korrelationswerte** (AK 1): Schlüssel `correlations:` im Szenario ist reserviert und wird ab
  M5 ausgewertet; bis dahin `scenario.unsupported`.

### 3.2 Was Szenarien nicht dürfen

- Knoten hinzufügen oder löschen – Struktur gehört ins Hauptszenario. Soll ein Szenario einen
  Zweig abschalten, geschieht das wie im Lernpfad über eine `constant` und `where`.
  (Folge: Das „mit Nacharbeit“-Szenario braucht den Ereignisknoten `nacharbeit` mit p = 0 im
  Hauptszenario; das Override setzt p = 0,2. Die analytischen Werte von T2 bleiben gültig, weil
  das Ereignis dort nie eintritt – AK 6 von M4.)

### 3.3 Validierung (AK 3)

| Code | Wann |
|---|---|
| `scenario.id_invalid` | ID verletzt Regex, ist `basis` oder doppelt |
| `scenario.parent_unknown` | `parent` nennt kein Szenario |
| `scenario.parent_cycle` | Elternkette bildet einen Zyklus (Meldung nennt die Kette) |
| `scenario.node_unknown` | Override eines Knotens, den es nicht gibt, ohne `inactive: true` |
| `scenario.field_invalid` | Feld passt nicht zum Knotentyp |
| `scenario.type_change` | `type` im Override |
| Hinweis `scenario.inactive` | Override mit `inactive: true` auf einen gelöschten Knoten (E4) |
| Hinweis `scenario.same_value` | Override-Wert gleich dem Elternwert |

- Jedes Szenario wird zusätzlich als effektives Modell mit `compile_model` geprüft (Zyklen durch
  geänderte Ausdrücke, Parametergrenzen); Fehler nennen Szenario und Knoten.
- Alle Probleme aller Szenarien werden gesammelt (wie in M1).

### 3.4 Loslösen und Duplizieren (AK 4)

- **Duplizieren:** gleiche Eltern, gleiche Overrides, neue ID und Name „Kopie von …“.
- **Loslösen** (E3): Das Szenario bekommt statt `parent` + `overrides` einen vollständigen
  Knotensatz `nodes:` (das effektive Modell zum Zeitpunkt des Loslösens) und `detached_from:`
  als Herkunftsnotiz. Spätere Änderungen am früheren Eltern wirken nicht mehr. Es bleibt im
  selben Modell und in derselben Vergleichsauswahl.

***

## 4. Effektives Modell (`model/scenarios.py`)

```python
def chain(model: Model, scenario_id: str) -> list[str]           # basis … scenario_id
def effective_model(model: Model, scenario_id: str) -> Model       # ohne scenarios-Schlüssel
def diff(model: Model, scenario_id: str) -> list[DiffRow]          # AK 8
def duplicate(model: Model, scenario_id: str, new_id: str) -> Model
def detach(model: Model, scenario_id: str) -> Model
```

- `effective_model` wendet die Overrides von der Wurzel zum Blatt an; das Ergebnis ist ein
  gewöhnliches `Model` und läuft unverändert durch `compile_model` und `simulate`.
- **Gemeinsame Zufallszahlen (AK 5):** Ströme hängen nur von Seed und Knoten-ID ab (M1). Gleicher
  Seed → nicht überschriebene Knoten sind bitgleich, überschriebene über die Inversionsmethode
  monoton gekoppelt. Daraus folgt AK 6 (Differenz ≤ 0 in jeder Iteration).
- `DiffRow = (knoten, feld, elternwert, szenariowert, begründung, status)`, Status
  `geändert | gleich | inaktiv`. Die Diff-Ansicht listet genau diese Zeilen (AK 8).

***

## 5. Simulation und Ergebnisse

- Simulationsseite: Auswahl des Szenarios (Baum als eingerückte Liste), dann N und Seed wie in M2.
- `RunView.scenario` trägt ID und Namen; die Geltungszeile nennt das Szenario.
- Läufe speichern `scenario_id` und `scenario_name` in `meta.json`; Modell-Hash ist der des
  ganzen Modelltexts, zusätzlich `effective_hash` (Inhalts-Hash des effektiven Modells).
- Die analytische Überlagerung von T1/T2 gilt nur im Hauptszenario (Inhalts-Hash des
  effektiven Modells = Original).

***

## 6. Vergleich (`analysis/compare.py`, AK 7)

Zwei Szenarien A (Referenz) und B, gleiche N und gleicher Seed; je Ausgabe die Stichproben
`a`, `b` und die gepaarte Differenz `d = b − a`.

| Größe | Verfahren |
|---|---|
| Kennzahlen A, B | `summarize` aus M1 |
| Differenz der Mittelwerte | `mean(d)`, Standardfehler `sd(d)/√N` (gepaart, deshalb klein) |
| Differenz von Median, P10, P90, P(Ziel) | Punktwert aus A und B; Unsicherheit per **Batch-Means** (E6): 20 Blöcke gleicher Größe, Differenz je Block, Standardfehler = sd/√20, 95-%-Intervall mit t(19) |
| Verteilung von `d` | Histogramm und Kennzahlen von `d`; Anteil `d = 0` (unbeeinflusste Iterationen) |
| P(B besser als A) | Anteil der Iterationen mit `d < 0` bzw. `d > 0` je nach Zielrichtung, Wilson-Intervall; Gleichstände separat ausgewiesen |

- **Zielrichtung** (E5): aus `target` der Ausgabe (`le`/`lt` → kleiner ist besser, `ge`/`gt` →
  größer); ohne `target` neues optionales Ausgabefeld `better: lower | higher`; fehlt beides,
  zeigt die App beide Anteile und keinen „besser“-Satz.
- Sätze in Modellsprache, z. B. „Im Modell ist B in 41,3 % der Iterationen besser als A
  (40,8 … 41,9 %), in 58,7 % gleich, nie schlechter.“
- Figuren: überlagerte CDFs von A und B, Histogramm von `d`.
- Mehr als zwei Szenarien (E8): bis zu vier in einer überlagerten CDF; Tabelle und Differenzen
  jeweils gegen die gewählte Referenz A.
- Bool-Ausgaben: Anteile A, B, Differenz in Prozentpunkten (Batch-Means), P(B besser) entfällt.

***

## 7. Oberfläche

| Seite | Inhalt |
|---|---|
| Szenarien (neu) | Baum (eingerückt, mit Anzahl Overrides); Szenario anlegen (Eltern, ID, Name, Begründung); Override hinzufügen (Knoten → Feld → Wert → Begründung); Duplizieren; Loslösen (mit Bestätigung); Diff-Ansicht des gewählten Szenarios |
| Simulation | + Szenarioauswahl |
| Ergebnisse | Geltungszeile mit Szenario; Hinweise `scenario.same_value`/`inactive` |
| Vergleich (neu) | Auswahl Referenz A und 1–3 weitere; N, Seed; Kennzahltabelle A/B/Differenz ± Unsicherheit; Sätze; Figuren |

- Änderungen auf der Szenarioseite ändern den Modelltext im Editor-Entwurf (wie Tippen im
  YAML-Editor); gespeichert wird wie in M2. Tutorials bleiben schreibgeschützt: Szenarien lassen
  sich in T2 ansehen, simulieren und vergleichen, ändern erst in einer Kopie.
- **Gelöschter Knoten** (E4): Löscht der Nutzer im Editor einen Knoten, auf den Overrides
  zeigen, meldet die Validierung `scenario.node_unknown` mit Knopf „Overrides inaktiv setzen“; das
  setzt `inactive: true` an diesen Overrides (sichtbar, keine stille Reparatur). Inaktive
  Overrides bleiben in der Diff-Ansicht sichtbar.
- Alle Texte über `messages.t()`, neue Schlüssel `scenario.*`, `compare.*`.

***

## 8. Beispiel T2

`examples/t2_terminplan.yaml` erhält:

- Knoten `nacharbeit: {type: event, p: 0}` und `ende: max(pfad1 + where(nacharbeit, 5, 0), c)`
  im Hauptszenario (analytisch unverändert, weil p = 0).
- Szenario `b_schneller` („B −3 Tage“): `b.mean = 12`.
- Szenario `nacharbeit` („mit Nacharbeit“): `nacharbeit.p = 0.2` (für M4 AK 6).
- Erklärtext `t2_terminplan.md` um einen Abschnitt „Szenarien“ ergänzt.

Weil sich der Inhalts-Hash von T2 ändert, gelten bestehende Kopien von T2 danach als „geändert“
(Hinweis statt Überlagerung) – in Kauf genommen.

***

## 9. Tests

| AK | Test | Prüft |
|---|---|---|
| 1 | `test_scenarios.py` | Szenario speichert nur Overrides; Rundlauf YAML; `why` Pflicht je Szenario |
| 2 | `test_scenarios.py` | Elternänderung wirkt im Kind; überschriebener Wert bleibt |
| 3 | `test_scenarios.py` | Tiefe 3; Elternzyklus, unbekannter Eltern, unbekannter Knoten → Codes |
| 4 | `test_scenarios.py` | `detach`: vollständige Knoten; spätere Elternänderung wirkt nicht |
| 5 | `test_scenario_runs.py` | Nicht überschriebene Knoten bitgleich zwischen Eltern- und Kindlauf |
| 6 | `test_scenario_runs.py` | T2 „B −3 Tage“: `ende_B − ende_A ≤ 0` in jeder Iteration (N = 100 000) |
| 7 | `test_compare.py`, `test_app.py` | Mittelwertdifferenz gegen analytischen Wert bei bekanntem Shift; Batch-Means-Intervall deckt in ≥ 90 % von 100 kleinen Läufen; Wilson für P(besser); AppTest der Vergleichsseite |
| 8 | `test_scenarios.py`, `test_app.py` | `diff` listet genau die Overrides inkl. Status |
| Edge | `test_scenarios.py` | inaktiver Override (Hinweis, nicht angewandt); gleicher Wert (Hinweis); Typwechsel abgewiesen; Familienwechsel ersetzt Parameter |

- Gate-Laufzeit: Vergleichs- und Szenariotests ≤ 5 s zusammen.

***

## 10. Arbeitspakete

| AP | Inhalt | Fertig, wenn |
|---|---|---|
| AP1 | Schema `scenarios`, Codes, Meldungen | Schema-Tests grün |
| AP2 | `model/scenarios.py`: chain, effective_model, diff, duplicate, detach | AK 1–4, 8, Edge cases grün |
| AP3 | Simulation je Szenario, T2-Szenarien, Läufe mit Szenario-Metadaten | AK 5, 6 grün |
| AP4 | `analysis/compare.py`, `present/compare.py` | AK 7 (rein) grün |
| AP5 | Seiten Szenarien, Vergleich, Simulation/Ergebnisse erweitert | AppTests grün |
| AP6 | Doku, Review, PRD-Status | Abschnitt 11 |

**Reihenfolge:** AP1 → AP2 → (AP3 ∥ AP4) → AP5 → AP6.

***

## 11. Abschluss von M3

- [ ] PRD M3 AK 1–8 und Edge cases durch die Tests in Abschnitt 9 belegt.
- [ ] `uv run pre-commit run --all-files` grün.
- [ ] Manuell: T2-Kopie mit zwei Unterszenarien angelegt, verglichen, losgelöst.
- [ ] README und `docs/architecture.md` aktualisiert; PRD M3 **Status** `done (verified by: …)`.
- [ ] Review durch den `reviewer`-Agenten.

***

## 12. Entscheidungen

Am 28.10.2026 alle wie vorgeschlagen bestätigt. E4 löst zugleich den Widerspruch im PRD zwischen
AK 3 (unbekannte Knoten abweisen) und dem Edge case „Override eines gelöschten Knotens bleibt
sichtbar und inaktiv“: Ohne Änderungshistorie unterscheidet nur die sichtbare Markierung
`inactive: true` beide Fälle. E10 nimmt in Kauf, dass bestehende Kopien von T2 danach als
„geändert“ gelten (Hinweis statt analytischer Überlagerung).

| Nr | Frage | Entscheidung |
|---|---|---|
| E1 | Wo stehen Szenarien? | Im Modell-YAML unter `scenarios:` (eine Datei je Modell; Kopieren nimmt die Szenarien mit) |
| E2 | Override-Granularität | Feldweise; `dist`/`input` im Override ersetzt den ganzen Parametersatz |
| E3 | Loslösen | Im selben Modell: Szenario mit vollständigem `nodes:`-Satz und `detached_from:` |
| E4 | Gelöschter Knoten mit Overrides | Fehler `scenario.node_unknown`; Knopf „Overrides inaktiv setzen“ setzt sichtbar `inactive: true`; inaktive Overrides → Hinweis, nicht angewandt |
| E5 | Was heißt „besser“? | Aus `target` der Ausgabe; sonst neues Feld `better: lower | higher`; sonst kein „besser“-Satz |
| E6 | Unsicherheit von Quantil-Differenzen | Batch-Means mit 20 Blöcken (schnell, deterministisch); Mittelwertdifferenz exakt gepaart |
| E7 | Szenarien bearbeiten | Szenarioseite mit kleinem Formular schreibt in den Modelltext; YAML-Editor bleibt gleichwertig |
| E8 | Wie viele Szenarien im Vergleich? | Bis zu vier überlagert, Differenzen jeweils gegen die Referenz A |
| E9 | Szenarien ohne Strukturänderung | Szenarien dürfen keine Knoten hinzufügen/löschen; Zweige über `constant` + `where` |
| E10 | T2 erweitern | `nacharbeit` (p = 0) ins Hauptszenario, Szenarien „B −3 Tage“ und „mit Nacharbeit“ |
